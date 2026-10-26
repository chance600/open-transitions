"""Per-passage key + energy measurement for the lane selector.

Why this exists (technique-selector-2026-10-25.md §6, priority order):
key (Camelot) per placed passage is the single biggest selector upgrade —
it unlocks camelot gates + prefers that never fire on lane profiles today —
energy (1-10) + energy_contour is second, groove_density third. All three
are measured on the PLACED PASSAGE (the bars actually used in the blend),
never per track: a track's key/energy in its intro is not its key/energy
at the seam.

Method (numpy/scipy only — no librosa dependency, so this runs wherever
the repo runs; librosa 1.0.0 IS available on the VM, essentia is NOT —
the dependency-light choice is portability, not necessity. Lane
precedent transition-lab/analyze.py uses the same Krumhansl-Schmuckler
profiles via librosa chroma_cqt; this script's STFT-fold chroma is the
equivalent variant, and its confidence rule differs deliberately: a hard
margin bar instead of analyze.py's blended confidence score, so a weak
key stays unknown rather than weakly claimed):
- Key: STFT magnitude folded into a 12-bin pitch-class (chroma) vector,
  averaged over the passage, correlated against Krumhansl-Schmuckler
  major/minor profiles for every tonic. Best correlation wins; the
  margin to the runner-up is the confidence signal. A low-margin result
  is reported as key=None with the runner-up noted — an unknown key
  becomes an UNVERIFIED gate in fit_select, never a guessed key.
- Energy: per-bar RMS (bar length from the caller's bpm — the passage
  grid the build already uses), mapped to 1-10 on fixed anchors
  (-32 dBFS bar RMS = 1, -6 dBFS = 10, linear in dB). The anchors are a
  starting calibration, NOT bank truth: re-anchor on 2-3 lane passages
  whose bank-scale energy is already recorded before treating scores as
  comparable across pairs. The bar RMS curve is returned in full so the
  contour (rise/fall/flat/peak) is auditable, not just the number.
- Groove proxy (third): onset density from positive spectral flux, and
  low-band (<120 Hz) RMS share + level — a kick/sub character PROXY for
  the missing bass_swap discriminator. It is not a kick classifier and
  must not be cited as one; a real kick/sub feature still needs the
  drums stem (Demucs) + kick-pattern classification.

Usage:
    python3 -m engine.measure_passage --wav <passage.wav> --bpm 123.0
        [--start 12.0 --end 44.0]
    Prints one JSON object to stdout. Exit non-zero on unreadable audio.

Provenance: a measured field fills a LaneSong field with prov="record"
only when this script's output file is cited in the build record; an
unmeasured field stays "unknown" in fit_select.
"""

import argparse
import json
import sys

import numpy as np
from scipy.io import wavfile
from scipy import signal as sig

# Krumhansl-Schmuckler profiles (Krumhansl & Kessler 1982, as used by
# the D3 analysis step: CQT chroma -> Krumhansl).
MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
                          2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
                          2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

# Pitch class 0=C ... 11=B -> Camelot code.
MINOR_CAMELOT = {9: "8A", 4: "9A", 11: "10A", 6: "11A", 1: "12A",
                 8: "1A", 3: "2A", 10: "3A", 5: "4A", 0: "5A",
                 7: "6A", 2: "7A"}
MAJOR_CAMELOT = {0: "8B", 7: "9B", 2: "10B", 9: "11B", 4: "12B",
                 11: "1B", 6: "2B", 1: "3B", 8: "4B", 3: "5B",
                 10: "6B", 5: "7B"}
PC_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

ENERGY_DB_FLOOR = -32.0  # bar RMS at energy 1
ENERGY_DB_CEIL = -6.0    # bar RMS at energy 10


def _load_mono(path):
    sr, x = wavfile.read(path)
    x = np.asarray(x, dtype=np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    if np.issubdtype(np.asarray(wavfile.read(path)[1]).dtype, np.integer):
        x = x / 32768.0
    # Deliberately NO peak normalization: energy must reflect the
    # passage's actual level (a quiet passage peak-normalized to match
    # a loud one would erase exactly the difference energy measures).
    return sr, x


def _chroma(x, sr):
    """Mean pitch-class vector over the passage (STFT, Hann, 4096)."""
    f, _t, z = sig.stft(x, fs=sr, window="hann", nperseg=4096,
                        noverlap=3072, boundary=None)
    mag = np.abs(z)
    # Drop sub-50 Hz and above ~4 kHz (harmonics dominate chroma there).
    keep = (f >= 50) & (f <= 4000)
    f, mag = f[keep], mag[keep]
    midi = 69 + 12 * np.log2(np.maximum(f, 1.0) / 440.0)
    pc = np.round(midi).astype(int) % 12
    chroma = np.zeros(12)
    np.add.at(chroma, pc, mag.sum(axis=1))
    total = chroma.sum()
    return chroma / total if total > 0 else chroma


def _key_from_chroma(chroma):
    """Returns (camelot, key_name, correlation, margin, runner_up)."""
    if chroma.sum() == 0:
        return None, None, 0.0, 0.0, None
    scored = []
    for tonic in range(12):
        for mode, prof, table in (("major", MAJOR_PROFILE, MAJOR_CAMELOT),
                                  ("minor", MINOR_PROFILE, MINOR_CAMELOT)):
            rotated = np.roll(prof, tonic)
            corr = float(np.corrcoef(chroma, rotated)[0, 1])
            scored.append((corr, table[tonic],
                           f"{PC_NAMES[tonic]} {mode}"))
    scored.sort(key=lambda s: -s[0])
    best, second = scored[0], scored[1]
    return best[1], best[2], best[0], best[0] - second[0], second[1]


def _bar_rms_db(x, sr, bpm):
    bar_s = 240.0 / bpm
    bar_n = max(1, int(round(bar_s * sr)))
    n_bars = max(1, len(x) // bar_n)
    out = []
    for i in range(n_bars):
        seg = x[i * bar_n:(i + 1) * bar_n]
        rms = float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0.0
        out.append(20 * np.log10(rms + 1e-12))
    return out


def _contour(bar_db):
    if len(bar_db) < 3:
        return "flat"
    third = max(1, len(bar_db) // 3)
    first = float(np.mean(bar_db[:third]))
    mid = float(np.mean(bar_db[third:2 * third]))
    last = float(np.mean(bar_db[2 * third:]))
    if mid > first + 1.5 and mid > last + 1.5:
        return "peak"
    if last > first + 1.5:
        return "rise"
    if first > last + 1.5:
        return "fall"
    return "flat"


def _groove_proxy(x, sr):
    """Onset density + low-band share. Proxy only — see module docstring."""
    f, _t, z = sig.stft(x, fs=sr, window="hann", nperseg=2048,
                        noverlap=1536, boundary=None)
    mag = np.abs(z)
    flux = np.diff(mag, axis=1)
    flux = np.where(flux > 0, flux, 0).sum(axis=0)
    if len(flux) == 0:
        return 0.0, 0.0, 0.0
    thresh = float(np.median(flux) + 2.0 * np.std(flux))
    onsets = int(np.sum(flux > thresh))
    hop_s = (2048 - 1536) / sr
    onset_rate = onsets / max(len(flux) * hop_s, 1e-9)  # per second
    power = mag ** 2
    low_power = float(power[f < 120].sum())
    total_power = float(power.sum())
    low_share = low_power / total_power if total_power > 0 else 0.0
    # Low-band energy share in dB (power ratio, always <= 0 dB).
    low_db = 10 * np.log10(low_share + 1e-12)
    return onset_rate, low_share, low_db


def measure_passage(path, bpm, start_s=None, end_s=None):
    sr, x = _load_mono(path)
    if start_s is not None or end_s is not None:
        i0 = int((start_s or 0.0) * sr)
        i1 = int(end_s * sr) if end_s else len(x)
        x = x[i0:i1]
    if len(x) < sr:  # <1 s of audio cannot support a passage measurement
        raise ValueError(f"passage too short: {len(x) / sr:.2f}s")
    chroma = _chroma(x, sr)
    camelot, key_name, corr, margin, runner_up = _key_from_chroma(chroma)
    # Confidence rule: a key is claimed only on a clear margin AND a
    # real correlation. Otherwise the passage stays key=unknown.
    key_confident = bool(corr >= 0.5 and margin >= 0.08)
    bar_db = _bar_rms_db(x, sr, bpm)
    med_db = float(np.median(bar_db))
    energy = float(np.clip(1 + 9 * (med_db - ENERGY_DB_FLOOR)
                           / (ENERGY_DB_CEIL - ENERGY_DB_FLOOR), 1, 10))
    onset_rate, low_share, low_db = _groove_proxy(x, sr)
    return {
        "file": path,
        "duration_s": round(len(x) / sr, 3),
        "bpm_used": bpm,
        "key": {
            "camelot": camelot if key_confident else None,
            "key_name": key_name if key_confident else None,
            "correlation": round(corr, 3),
            "margin": round(margin, 3),
            "runner_up": runner_up,
            "confident": key_confident,
            "note": ("low margin/correlation — treat as unknown in "
                     "LaneSong, do not guess") if not key_confident else None,
        },
        "energy": {
            "energy_1_10": round(energy, 2),
            "median_bar_rms_db": round(med_db, 2),
            "contour": _contour(bar_db),
            "bar_rms_db": [round(v, 2) for v in bar_db],
            "calibration": "anchors -32 dBFS=1, -6 dBFS=10; re-anchor on "
                           "2-3 recorded lane passages before cross-pair "
                           "comparison",
        },
        "groove_proxy": {
            "onset_rate_per_s": round(onset_rate, 2),
            "low_band_share": round(low_share, 3),
            "low_band_relative_db": round(low_db, 2),
            "note": "proxy only — not a kick classifier; kick/sub character "
                    "needs the drums stem + kick-pattern classification",
        },
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--wav", required=True)
    ap.add_argument("--bpm", type=float, required=True)
    ap.add_argument("--start", type=float, default=None)
    ap.add_argument("--end", type=float, default=None)
    args = ap.parse_args(argv)
    try:
        result = measure_passage(args.wav, args.bpm, args.start, args.end)
    except Exception as exc:  # noqa: BLE001 — CLI reports, does not guess
        print(f"measure_passage: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
