"""
open-transitions engine — transition cleanliness QC (doctrine D6).

verify.py checks that a render is *mechanically* sound (no unintended
silence, headroom, tempo coherence). It cannot hear whether a fade is
*clean*. This module is the perceptual gate that runs before any render
reaches the listener's ears:

  1. beat_phase    — grid coherence of the handoff: the two sides'
                     downbeat-grid offset from the build record (patterned
                     audio cannot yield grid phase — different patterns
                     locked to the same grid have different beat-component
                     phases), plus an audio truth-check that B's solo
                     tail really sits on the grid (beat-tracked tempo
                     and phase). Render-only mode falls back to mix
                     onsets vs the grid + a double-hit rate.
  2. low_clash     — low-band energy in the overlap vs the louder solo
                     side: two kicks/basslines summing into mud/boom.
  3. loudness      — per-bar RMS trajectory across the handoff: boundary
                     steps, roughness (jitter), energy holes (dips).
  4. key_clash     — chroma agreement between the sides inside the
                     window, including the cross terms that matter for
                     band-split techniques (A melody vs B bassline).
  5. vocal_collision — both sides vocal-active at once (weighted by how
                     much mid-band overlap the render actually contains),
                     plus a vocal-first-entry flag on the incoming side.
  6. tail_hygiene  — outgoing-side content still detectable over the
                     incoming side's first solo bars.

Inputs: the render, a spec (blend window in seconds, mix BPM, bar
length, beat-grid offset), and — in full mode — the two source excerpts
*as placed* on the render timeline (already time-warped by the builder,
supplied as arrays or as wav paths + placement offsets in the spec).
Without sides, a degraded render-only mode runs the subset that is
measurable from the mix alone and says so in the receipt.

Output: a QC receipt dict (also JSON-serializable):
  {clip, mode, window_s, checks: [{name, status, score, metrics, note}],
   cleanliness_score, verdict, summary: [one line per check]}

Status is pass / warn / fail per check; verdict is fail if any check
fails or the weighted cleanliness score < 55, warn if any check warns
or score < 75, else pass. Scores are 0-100 per check; None means the
check could not be measured (excluded from the weighted mean, and the
receipt says why). Thresholds were calibrated once against the
listener's verdicts on Set-1 (see demos/qc_calibration.py); residual
disagreements are documented in the transition-qc skill, not hidden.
"""

import numpy as np
from scipy import signal

from . import dsp

# ----------------------------------------------------------------------------
# Constants / bands
# ----------------------------------------------------------------------------

LOW_HZ = 250.0                 # matches dsp.split_3band DJ-mixer low band
VOCAL_LO_HZ, VOCAL_HI_HZ = 300.0, 3400.0
CHROMA_FMIN, CHROMA_FMAX = 50.0, 4000.0

WEIGHTS = {
    "beat_phase": 0.25,
    "low_clash": 0.20,
    "loudness": 0.20,
    "key_clash": 0.15,
    "vocal_collision": 0.12,
    "tail_hygiene": 0.08,
}

# beat_phase: matched-onset offset (s) and flam fraction
BP_OFFSET_GOOD, BP_OFFSET_BAD = 0.012, 0.072
BP_FLAM_MIN, BP_FLAM_MAX = 0.045, 0.32   # offset band that reads as a flam
# low_clash: p90 per-beat low-band excess over the louder side (dB)
LC_EXCESS_GOOD, LC_EXCESS_BAD = 1.0, 6.0
# loudness: boundary step / jitter / dip (dB)
LD_STEP_GOOD, LD_STEP_BAD = 1.5, 6.0
LD_JIT_GOOD, LD_JIT_BAD = 0.6, 3.0
LD_DIP_GOOD, LD_DIP_BAD = 2.0, 9.0
# key_clash: chroma cosine similarity
KEY_SIM_GOOD, KEY_SIM_BAD = 0.85, 0.35
# vocal_collision: energy-weighted simultaneous-vocal ratio
VC_RATIO_GOOD, VC_RATIO_BAD = 0.02, 0.30
VC_ENTRY_DBFS = -32.0           # B enters clearly vocal-forward at/above this
# tail_hygiene
TAIL_EXCESS_FREE_DB = 1.0


def _clamp01(v):
    return float(min(1.0, max(0.0, v)))


def _lin_score(v, good, bad):
    """100 at/below `good`, 0 at/above `bad` (for lower-is-better metrics)."""
    if bad == good:
        return 100.0 if v <= good else 0.0
    return round(100.0 * _clamp01((bad - v) / (bad - good)), 1)


def _status(score, pass_at=70.0, warn_at=45.0):
    if score is None:
        return "n/a"
    if score >= pass_at:
        return "pass"
    if score >= warn_at:
        return "warn"
    return "fail"


def _db(v):
    return float(20.0 * np.log10(max(float(v), 1e-12)))


# ----------------------------------------------------------------------------
# Signal helpers
# ----------------------------------------------------------------------------

def _band(x, sr, lo_hz, hi_hz, order=4):
    sos = signal.butter(order, [lo_hz, hi_hz], btype="bandpass", fs=sr,
                        output="sos")
    return signal.sosfilt(sos, x)


def _low(x, sr):
    return dsp.split_3band(x, sr)[0]


def _mid(x, sr):
    return dsp.split_3band(x, sr)[1]


def _frames(x, sr, win_s, hop_s):
    """RMS frames. Returns (center_times, rms)."""
    w = max(1, int(win_s * sr))
    hop = max(1, int(hop_s * sr))
    n = 1 + max(0, (len(x) - w) // hop)
    idx = np.arange(n) * hop
    segs = np.lib.stride_tricks.sliding_window_view(x, w)[idx]
    rms = np.sqrt(np.mean(segs ** 2, axis=1) + 1e-18)
    times = (idx + w / 2) / sr
    return times, rms


def _onsets(x, sr, prom_frac=0.25):
    """Kick-band onset times via positive spectral-energy flux + peak pick."""
    low = _low(x, sr)
    times, rms = _frames(low, sr, win_s=0.03, hop_s=0.01)
    if len(rms) < 3:
        return np.array([]), times, rms
    flux = np.maximum(0.0, np.diff(rms, prepend=rms[0]))
    prom = prom_frac * (np.percentile(flux, 95) + 1e-12)
    peaks, _ = signal.find_peaks(flux, prominence=prom,
                                 distance=max(1, int(0.18 / 0.01)))
    return times[peaks], times, rms


def _chroma(x, sr):
    """12-dim pitch-class energy vector (L2-normalized) + total magnitude."""
    n_fft = 4096
    if len(x) < n_fft:
        return None, 0.0
    _, _, z = signal.stft(x, fs=sr, nperseg=n_fft, noverlap=n_fft // 2)
    mag = np.abs(z)
    freqs = np.fft.rfftfreq(n_fft, 1.0 / sr)
    keep = (freqs >= CHROMA_FMIN) & (freqs <= CHROMA_FMAX)
    if not np.any(keep):
        return None, 0.0
    midi = 69.0 + 12.0 * np.log2(freqs[keep] / 440.0)
    pc = np.mod(np.round(midi).astype(int), 12)
    energy = mag[keep].sum(axis=1)
    chroma = np.zeros(12)
    np.add.at(chroma, pc, energy)
    total = float(chroma.sum())
    if total <= 1e-12:
        return None, 0.0
    return chroma / (np.linalg.norm(chroma) + 1e-12), total


def _cosine(u, v):
    if u is None or v is None:
        return None
    return float(np.dot(u, v))


def _seg(x, sr, t0, t1):
    i0 = max(0, int(t0 * sr))
    i1 = min(len(x), int(t1 * sr))
    return x[i0:i1] if i1 > i0 else np.zeros(0)


def _place(excerpt, sr, offset_s, total_len):
    out = np.zeros(total_len)
    i0 = int(round(offset_s * sr))
    i1 = min(total_len, i0 + len(excerpt))
    if i1 > i0:
        out[i0:i1] = excerpt[:i1 - i0]
    return out


# ----------------------------------------------------------------------------
# Check 1 — beat-phase coherence
# ----------------------------------------------------------------------------

def _wrap(v, period):
    return (v + period / 2) % period - period / 2


# NOTE: there is deliberately no audio-only grid-phase estimator here.
# An exact-frequency DFT of a side's low-band envelope was tried and
# measured 0.7-1.0 s phantom offsets on grid-locked Set-1 renders:
# the beat-component phase of a patterned envelope is set by WHERE
# the pattern's energy sits inside the beat, not by the grid origin,
# so two different patterns on the same grid read as "offset".
# beat_phase therefore takes grid offsets from the build record and
# uses audio only as a tail regularity/tempo truth-check.


def _tail_grid_check(x, sr, spec):
    """Audio truth-check for beat_phase: beat-track the render just
    after the blend window, where B plays solo, and confirm its tempo
    and phase sit on the mix grid. Returns (score, note, metrics) or
    None when the tail is too short or cannot be tracked."""
    try:
        import librosa
    except Exception:
        return None
    w1 = spec["window_s"][1]
    bar_s = spec["bar_s"]
    bpm = spec["bpm"]
    beat_s = 60.0 / bpm
    t1 = min(len(x) / sr, w1 + 6 * bar_s)
    if t1 - w1 < 3 * bar_s:
        return None
    seg = _seg(x, sr, w1, t1)
    try:
        tempo, times = librosa.beat.beat_track(
            y=seg, sr=sr, start_bpm=bpm, units="time", hop_length=512)
    except Exception:
        return None
    tempo = float(np.atleast_1d(tempo)[0])
    times = np.atleast_1d(times) + w1
    if len(times) < 4 or tempo <= 0:
        return None
    ratio = tempo / bpm
    while ratio > 1.41:
        ratio /= 2.0
    while ratio < 0.71:
        ratio *= 2.0
    terr = abs(ratio - 1.0)
    off = spec.get("beat_offset_s", 0.0)
    med = float(np.median([abs(_wrap(t - off, beat_s)) for t in times]))
    # Scored on tempo error + beat regularity (IOI coefficient of
    # variation), NOT absolute phase vs the grid origin: the tracker
    # carries a material-dependent phase bias on syncopated low-end
    # (65-165 ms on Set-1 tails the builders verified coherent), so
    # absolute phase measures the tracker, not the render. Phase is
    # still reported in metrics. A real trainwreck tail shows up as
    # tempo that never landed and/or galloping IOIs — that is what
    # this scores. (Absolute phase truth comes from the build-record
    # grid offsets when supplied.)
    iois = np.diff(times)
    ioi_cv = float(np.std(iois) / np.mean(iois)) if len(iois) > 2 \
        and np.mean(iois) > 0 else 1.0
    m = {"tail_tempo_bpm": round(tempo, 2),
         "tail_phase_dev_ms": round(med * 1000, 1),
         "tail_ioi_cv": round(ioi_cv, 3),
         "tail_beats": int(len(times))}
    if terr > 0.06:
        return 10.0, (f"B's tail tracks at {tempo:.1f} BPM vs grid "
                      f"{bpm:.1f} — the tempo never landed"), m
    score = round(min(_lin_score(terr, 0.02, 0.06),
                      _lin_score(ioi_cv, 0.03, 0.12)), 1)
    return score, (f"B's tail steady on the grid: tempo {tempo:.1f} "
                   f"vs {bpm:.1f} BPM, beat regularity "
                   f"{ioi_cv:.2f}"), m


def check_beat_phase(x, sr, spec, a=None, b=None):
    w0, w1 = spec["window_s"]
    bpm = spec["bpm"]
    beat_s = 60.0 / bpm
    bar_s = spec["bar_s"]
    metrics = {"beat_s": round(beat_s, 4)}

    if a is not None and b is not None:
        # Grid phase cannot be read off patterned audio: two different
        # patterns locked to the SAME grid have different beat-component
        # phases (measured on Set-1: 0.7-1.0 s phantom offsets on
        # grid-locked renders). The offset therefore comes from the
        # build record (a_grid_offset_s / b_grid_offset_s — the phase
        # of each side's downbeat grid as placed, which every builder
        # knows), and audio enters as an independent truth-check on
        # B's solo tail.
        parts, notes = [], []
        if "a_grid_offset_s" in spec and "b_grid_offset_s" in spec:
            d = _wrap(spec["b_grid_offset_s"]
                      - spec["a_grid_offset_s"], beat_s)
            metrics["grid_offset_ms"] = round(abs(d) * 1000, 1)
            metrics["grid_basis"] = "build record"
            parts.append(_lin_score(abs(d), BP_OFFSET_GOOD,
                                    BP_OFFSET_BAD))
            notes.append(f"grid offset {abs(d) * 1000:.0f} ms between "
                         f"the sides (build record)")
        tail = _tail_grid_check(x, sr, spec)
        if tail is not None:
            parts.append(tail[0])
            notes.append(tail[1])
            metrics["tail_grid"] = tail[2]
        if not parts:
            return {"name": "beat_phase", "status": "n/a",
                    "score": None, "metrics": metrics,
                    "note": "no grid offsets in the build record and "
                            "B's tail could not be beat-tracked — "
                            "supply a_grid_offset_s/b_grid_offset_s"}
        score = round(min(parts), 1)
        return {"name": "beat_phase", "status": _status(score),
                "score": score, "metrics": metrics,
                "note": "; ".join(notes)}

    # render-only: onsets vs the grid + double-hit rate inside cells
    off = spec.get("beat_offset_s", 0.0)
    ox, _, _ = _onsets(_seg(x, sr, w0, w1), sr)
    ox = ox + w0
    if len(ox) < 4:
        return {"name": "beat_phase", "status": "n/a", "score": None,
                "metrics": metrics,
                "note": "too few onsets in window to judge phase"}
    phase = (ox - off) % beat_s
    dev = np.minimum(phase, beat_s - phase)
    med = float(np.median(dev))
    cells = {}
    for t in ox:
        cells.setdefault(int((t - off) // beat_s), []).append(t)
    doubles = 0
    for ts in cells.values():
        ts = sorted(ts)
        if any(BP_FLAM_MIN < ts[i + 1] - ts[i] < BP_FLAM_MAX
               for i in range(len(ts) - 1)):
            doubles += 1
    flam = doubles / max(1, len(cells))
    metrics["median_grid_dev_ms"] = round(med * 1000, 1)
    metrics["double_hit_fraction"] = round(flam, 3)
    score = min(_lin_score(med, BP_OFFSET_GOOD, BP_OFFSET_BAD),
                _lin_score(flam, 0.02, 0.28))
    return {"name": "beat_phase", "status": _status(score), "score": score,
            "metrics": metrics,
            "note": f"render-only: median grid deviation {med*1000:.0f} ms; "
                    f"double-hit cells {flam:.0%}"}


# ----------------------------------------------------------------------------
# Check 2 — low-band clash
# ----------------------------------------------------------------------------

def check_low_clash(x, sr, spec, a=None, b=None):
    w0, w1 = spec["window_s"]
    beat_s = 60.0 / spec["bpm"]
    metrics = {}
    low_x = _low(x, sr)

    def beat_lows(sig, t_start):
        """Per-beat low RMS (dB) for beats fully inside [w0, w1]."""
        out = []
        t = t_start
        while t + beat_s <= w1 + 1e-9:
            seg = _seg(sig, sr, t, t + beat_s)
            out.append(_db(np.sqrt(np.mean(seg ** 2) + 1e-18))
                       if len(seg) else -120.0)
            t += beat_s
        return np.array(out)

    off = spec.get("beat_offset_s", 0.0)
    first = off + np.ceil((w0 - off) / beat_s) * beat_s
    mix_l = beat_lows(low_x, first)
    if len(mix_l) == 0:
        return {"name": "low_clash", "status": "n/a", "score": None,
                "metrics": metrics, "note": "window shorter than one beat"}
    if a is not None and b is not None:
        a_l = beat_lows(_low(a, sr), first)
        b_l = beat_lows(_low(b, sr), first)
        n = min(len(mix_l), len(a_l), len(b_l))
        louder = np.maximum(a_l[:n], b_l[:n])
        active = louder > -48.0
        if active.sum() < 2:
            return {"name": "low_clash", "status": "n/a", "score": None,
                    "metrics": metrics,
                    "note": "neither side has low-band energy in window"}
        excess = mix_l[:n][active] - louder[active]
        deficit = louder[active] - mix_l[:n][active]
    else:
        bar_s = spec["bar_s"]
        a_solo = _seg(low_x, sr, max(0.0, w0 - 4 * bar_s), w0)
        b_solo = _seg(low_x, sr, w1, min(len(x) / sr, w1 + 4 * bar_s))
        base = -120.0
        for s in (a_solo, b_solo):
            if len(s):
                base = max(base, float(np.percentile(
                    _frames(s, sr, beat_s, beat_s)[1], 90)))
        base = _db(base) if base > 0 else -120.0
        excess = mix_l - base
        deficit = np.zeros_like(excess)
        metrics["solo_low_baseline_db"] = round(base, 1)
        active = np.ones_like(excess, dtype=bool)
    p90 = float(np.percentile(excess, 90))
    mean_pos = float(np.mean(np.maximum(excess, 0.0)))
    metrics["excess_p90_db"] = round(p90, 2)
    metrics["excess_mean_pos_db"] = round(mean_pos, 2)
    s_excess = _lin_score(p90, LC_EXCESS_GOOD, LC_EXCESS_BAD)
    score = s_excess
    note = (f"low band in overlap runs {p90:+.1f} dB (p90) over the louder "
            f"solo side — " +
            ("summed kicks/bass read as mud" if s_excess < 45 else
             "within summing tolerance" if s_excess >= 70 else
             "some low-end doubling"))
    if a is not None and b is not None:
        # deficit: the overlap's low end is *thinner* than the louder
        # side promised (weak incoming lows under a groove, a low-end
        # hole mid-fade). Holes are more forgivable than mud: wider map.
        # Only scored when the technique's contract promises a
        # continuous bottom (spec lows_contract): washes, sweeps and
        # chops thin the low end BY DESIGN — for those the hole is the
        # technique, and loudness sag is the check that judges it.
        contract = spec.get("lows_contract", "continuous")
        metrics["lows_contract"] = contract
        d90 = float(np.percentile(deficit, 90))
        metrics["deficit_p90_db"] = round(d90, 2)
        if contract != "free":
            s_deficit = _lin_score(d90, 2.0, 10.0)
            if s_deficit < score:
                score = s_deficit
                note = (f"low end in overlap sits {d90:.1f} dB (p90) "
                        f"under the louder side — the bottom drops "
                        f"out mid-blend")
    return {"name": "low_clash", "status": _status(score), "score": score,
            "metrics": metrics, "note": note}


# ----------------------------------------------------------------------------
# Check 3 — loudness trajectory
# ----------------------------------------------------------------------------

def check_loudness(x, sr, spec, a=None, b=None):
    w0, w1 = spec["window_s"]
    bar_s = spec["bar_s"]
    off = spec.get("beat_offset_s", 0.0)
    dur = len(x) / sr
    k0 = int(np.floor((max(0.0, w0 - 4 * bar_s) - off) / bar_s))
    k1 = int(np.ceil((min(dur, w1 + 4 * bar_s) - off) / bar_s))
    bars, vals = [], []
    for k in range(k0, k1):
        t0 = off + k * bar_s
        seg = _seg(x, sr, t0, t0 + bar_s)
        if len(seg) < int(0.5 * bar_s * sr):
            continue
        bars.append(t0)
        vals.append(_db(np.sqrt(np.mean(seg ** 2) + 1e-18)))
    bars = np.array(bars)
    vals = np.array(vals)
    if len(vals) < 5:
        return {"name": "loudness", "status": "n/a", "score": None,
                "metrics": {}, "note": "too few bars around the handoff"}
    trend = signal.medfilt(vals, kernel_size=5)
    in_win = (bars >= w0 - bar_s) & (bars <= w1)
    step_zone = (bars >= w0 - bar_s) & (bars <= w1 + bar_s)
    d = np.abs(np.diff(vals))
    step = float(np.max(d[step_zone[:-1] & step_zone[1:]])) if \
        np.any(step_zone[:-1] & step_zone[1:]) else 0.0
    jit = float(np.median(d[in_win[:-1] & in_win[1:]])) if \
        np.any(in_win[:-1] & in_win[1:]) else 0.0
    dip = float(np.max(trend[in_win] - vals[in_win])) if \
        np.any(in_win) else 0.0
    s_step = _lin_score(step, LD_STEP_GOOD, LD_STEP_BAD)
    s_jit = _lin_score(jit, LD_JIT_GOOD, LD_JIT_BAD)
    s_dip = _lin_score(dip, LD_DIP_GOOD, LD_DIP_BAD)
    metrics = {"max_bar_step_db": round(step, 2),
               "bar_jitter_db": round(jit, 2),
               "max_dip_below_trend_db": round(dip, 2)}
    note = (f"bar-to-bar: worst step {step:.1f} dB, jitter {jit:.1f} dB, "
            f"deepest dip {dip:.1f} dB below local trend")
    if a is not None and b is not None:
        # blend sag: per-bar, how far the render sags under the louder
        # side's own bar level inside the window. A long crossfade where
        # both sides are attenuated at once (the classic filter-sweep
        # energy collapse) reads as "doesn't fade cleanly" even when
        # every bar-to-bar step is smooth. Sustained sag (p75) counts,
        # a one-bar breath does not.
        def bar_db(sig, t0):
            seg = _seg(sig, sr, t0, t0 + bar_s)
            return _db(np.sqrt(np.mean(seg ** 2) + 1e-18)) \
                if len(seg) else -120.0
        sags = []
        for t0, v in zip(bars, vals):
            if w0 - 0.01 <= t0 <= w1 - bar_s + 0.01:
                sags.append(max(bar_db(a, t0), bar_db(b, t0)) - v)
        if sags:
            sag = float(np.percentile(np.maximum(sags, 0.0), 75))
            metrics["blend_sag_p75_db"] = round(sag, 2)
            s_sag = _lin_score(sag, 1.5, 7.0)
            score = round(0.4 * s_step + 0.4 * s_sag + 0.2 * s_jit, 1)
            note += (f"; sustained blend sag {sag:.1f} dB under the "
                     f"louder side")
            return {"name": "loudness", "status": _status(score),
                    "score": score, "metrics": metrics, "note": note}
    score = round(0.5 * s_step + 0.3 * s_jit + 0.2 * s_dip, 1)
    return {"name": "loudness", "status": _status(score), "score": score,
            "metrics": metrics, "note": note}


# ----------------------------------------------------------------------------
# Check 4 — key clash
# ----------------------------------------------------------------------------

def check_key_clash(x, sr, spec, a=None, b=None):
    w0, w1 = spec["window_s"]
    metrics = {}
    if a is None or b is None:
        return {"name": "key_clash", "status": "n/a", "score": None,
                "metrics": metrics,
                "note": "needs both sides — not measurable render-only"}
    a_win = _seg(a, sr, w0, w1)
    b_win = _seg(b, sr, w0, w1)
    # harmonic-presence gate first: if either side is effectively not
    # present in the window, there is no simultaneous harmony to clash
    # (and chroma of silence is None, which must not read as "too
    # short").
    rms_a = float(np.sqrt(np.mean(a_win ** 2) + 1e-18)) if len(a_win) \
        else 0.0
    rms_b = float(np.sqrt(np.mean(b_win ** 2) + 1e-18)) if len(b_win) \
        else 0.0
    metrics["side_rms_db"] = [round(_db(rms_a), 1), round(_db(rms_b), 1)]
    if min(rms_a, rms_b) < dsp.db_to_gain(-46.0):
        return {"name": "key_clash", "status": "n/a", "score": None,
                "metrics": metrics,
                "note": "one side is effectively absent in the window — "
                        "no simultaneous harmony to clash"}
    ca, ta = _chroma(a_win, sr)
    cb, tb = _chroma(b_win, sr)
    if ca is None or cb is None:
        return {"name": "key_clash", "status": "n/a", "score": None,
                "metrics": metrics, "note": "window too short for chroma"}
    sims = {"full": _cosine(ca, cb)}
    a_lo, a_mh = _low(a_win, sr), a_win - _low(a_win, sr)
    b_lo, b_mh = _low(b_win, sr), b_win - _low(b_win, sr)
    ca_lo, _ = _chroma(a_lo, sr)
    ca_mh, _ = _chroma(a_mh, sr)
    cb_lo, _ = _chroma(b_lo, sr)
    cb_mh, _ = _chroma(b_mh, sr)
    s1 = _cosine(ca_mh, cb_lo)   # A melody vs B bassline (bass-swap case)
    s2 = _cosine(ca_lo, cb_mh)   # A bassline vs B melody
    if s1 is not None:
        sims["a_melody_vs_b_bass"] = s1
    if s2 is not None:
        sims["a_bass_vs_b_melody"] = s2
    worst_name = min(sims, key=lambda k: sims[k])
    worst = sims[worst_name]
    metrics["chroma_similarity"] = {k: round(v, 3) for k, v in sims.items()}
    metrics["worst_pair"] = worst_name
    score = round(100.0 * _clamp01(
        (worst - KEY_SIM_BAD) / (KEY_SIM_GOOD - KEY_SIM_BAD)), 1)
    note = (f"weakest chroma agreement {worst:.2f} ({worst_name}) — " +
            ("keys sit together" if score >= 70 else
             "audible tension between the sides' harmony" if score >= 45
             else "the sides fight harmonically in the overlap"))
    return {"name": "key_clash", "status": _status(score), "score": score,
            "metrics": metrics, "note": note}


# ----------------------------------------------------------------------------
# Check 5 — vocal collision (+ incoming vocal-first entry)
# ----------------------------------------------------------------------------

def _vocal_env(x, sr, win_s=0.05, hop_s=0.025):
    """Vocal/melodic activity envelope of a signal.

    Band energy (300 Hz-3.4 kHz) alone fires on snares and hats, so
    each frame's RMS is gated by spectral peakiness: voices and melodic
    lines are strongly harmonic (peaky spectrum); drums are broadband
    (flat spectrum) and get attenuated to ~5%.
    """
    band = _band(x, sr, VOCAL_LO_HZ, VOCAL_HI_HZ)
    w = max(256, int(win_s * sr))
    hop = max(1, int(hop_s * sr))
    if len(band) < w:
        return np.array([]), np.array([])
    n = 1 + (len(band) - w) // hop
    idx = np.arange(n) * hop
    segs = np.lib.stride_tricks.sliding_window_view(band, w)[idx]
    rms = np.sqrt(np.mean(segs ** 2, axis=1) + 1e-18)
    spec = np.abs(np.fft.rfft(segs * np.hanning(w), axis=1)) + 1e-12
    peakiness = spec.max(axis=1) / (np.median(spec, axis=1) + 1e-12)
    gate = np.clip((peakiness - 3.0) / 6.0, 0.05, 1.0)
    return idx / sr, rms * gate


def check_vocal(x, sr, spec, a=None, b=None):
    w0, w1 = spec["window_s"]
    bar_s = spec["bar_s"]
    metrics = {}
    if a is None or b is None:
        return {"name": "vocal_collision", "status": "n/a", "score": None,
                "metrics": metrics,
                "note": "needs both sides — not measurable render-only"}
    _, ea = _vocal_env(_seg(a, sr, w0, w1), sr)
    _, eb = _vocal_env(_seg(b, sr, w0, w1), sr)
    n = min(len(ea), len(eb))
    if n < 4:
        return {"name": "vocal_collision", "status": "n/a", "score": None,
                "metrics": metrics, "note": "window too short"}
    ea, eb = ea[:n], eb[:n]
    thr = dsp.db_to_gain(-48.0)
    both = (ea > thr) & (eb > thr)
    denom = float(np.sum(np.maximum(ea, eb))) + 1e-12
    ratio_raw = float(np.sum(np.minimum(ea, eb)[both]) / denom)
    # exposure: how much mid-band overlap the render actually contains.
    # Band-split techniques (bass swap) kill one side's mids, so placed
    # sides can "collide" on paper while the render stays sequential.
    pa = float(np.mean(_seg(_mid(a, sr), sr, w0, w1) ** 2))
    pb = float(np.mean(_seg(_mid(b, sr), sr, w0, w1) ** 2))
    # exposure = how much of EACH side's mid-band signal is literally
    # present in the render, measured by waveform projection: per
    # frame, alpha = <x, a>/<a, a> and beta = <x, b>/<b, b> in the mid
    # band (uncorrelated sources cross-project to ~0, so a side the
    # technique killed reads ~0 even when its envelope pulses on the
    # same grid as the surviving side — the failure mode of both
    # earlier estimators: the window-mean formula read 1.00 and an
    # envelope regression split credit arbitrarily on sequential bass
    # swaps, which are sequential BY CONSTRUCTION). Co-presence per
    # frame is min(alpha, beta); exposure is its p75 over the window.
    # A reverb-smeared side also projects weakly onto its dry self —
    # correctly: wet background texture is not a second lead.
    exposure = 0.0
    xm = _seg(_mid(x, sr), sr, w0, w1)
    am = _seg(_mid(a, sr), sr, w0, w1)
    bm = _seg(_mid(b, sr), sr, w0, w1)
    wf, hf = int(0.25 * sr), int(0.125 * sr)
    if len(xm) >= wf and len(am) >= wf and len(bm) >= wf:
        def proj(ref):
            n = 1 + (min(len(xm), len(ref)) - wf) // hf
            idx = np.arange(n) * hf
            xv = np.lib.stride_tricks.sliding_window_view(xm, wf)[idx]
            rv = np.lib.stride_tricks.sliding_window_view(ref, wf)[idx]
            num = np.sum(xv * rv, axis=1)
            den = np.sum(rv * rv, axis=1) + 1e-18
            return np.clip(num / den, 0.0, 1.5)
        al, be = proj(am), proj(bm)
        co = np.clip(np.minimum(al, be), 0.0, 1.0)
        exposure = float(np.percentile(co, 75))
        metrics["mid_presence_a"] = round(float(np.median(al)), 3)
        metrics["mid_presence_b"] = round(float(np.median(be)), 3)
    ratio = ratio_raw * exposure
    metrics["simultaneous_vocal_ratio_raw"] = round(ratio_raw, 3)
    metrics["mid_overlap_exposure"] = round(exposure, 3)
    metrics["simultaneous_vocal_ratio"] = round(ratio, 3)
    score = _lin_score(ratio, VC_RATIO_GOOD, VC_RATIO_BAD)
    notes = [f"simultaneous-vocal energy ratio {ratio:.2f} "
             f"(raw {ratio_raw:.2f} x mid-overlap exposure {exposure:.2f})"]
    # Incoming side enters vocal-first? Only meaningful for late/hard
    # entries — when B's content starts at/near the handoff point. For
    # gradual blends and band-split swaps B is present from the window
    # start and its vocal entrance is a section-choice matter the
    # simultaneity ratio already covers; the flag stays silent there.
    _, eb_full = _frames(b, sr, 0.05, 0.025)
    eb_db = dsp.gain_to_db(eb_full)
    sounding = eb_db > -50.0
    b_onset = float(np.argmax(sounding) * 0.025) if np.any(sounding) \
        else float("inf")
    in_win = eb_db[int(w0 / 0.025):int(w1 / 0.025)]
    silent_frac = float(np.mean(in_win < -50.0)) if len(in_win) else 0.0
    late_entry = (b_onset >= w1 - bar_s) or (silent_frac > 0.7)
    metrics["b_onset_s"] = None if np.isinf(b_onset) else round(b_onset, 2)
    metrics["b_silent_frac_in_window"] = round(silent_frac, 2)
    if late_entry:
        _, eb_post = _vocal_env(_seg(b, sr, w1, w1 + bar_s), sr)
        if len(eb_post):
            entry_db = _db(float(np.sqrt(np.mean(eb_post ** 2) + 1e-18)))
            metrics["b_entry_vocal_db"] = round(entry_db, 1)
            if entry_db >= VC_ENTRY_DBFS:
                score = min(score, 60.0)
                notes.append(
                    f"incoming side enters vocal-first ({entry_db:.0f} "
                    f"dBFS gated vocal band in its first solo bar) — "
                    f"drums-first is the house preference")
    return {"name": "vocal_collision", "status": _status(score),
            "score": score, "metrics": metrics, "note": "; ".join(notes)}


# ----------------------------------------------------------------------------
# Check 6 — tail hygiene
# ----------------------------------------------------------------------------

def check_tail(x, sr, spec, a=None, b=None):
    w0, w1 = spec["window_s"]
    bar_s = spec["bar_s"]
    dur = len(x) / sr
    metrics = {}
    t_end = min(dur, w1 + 2 * bar_s)
    if t_end - w1 < 0.5 * bar_s:
        return {"name": "tail_hygiene", "status": "n/a", "score": None,
                "metrics": metrics,
                "note": "render ends at the handoff — no B-solo tail"}
    post = _seg(x, sr, w1, w1 + bar_s)
    post_db = _db(np.sqrt(np.mean(post ** 2) + 1e-18)) if len(post) else -120.0
    if b is not None:
        b_post = _seg(b, sr, w1, w1 + bar_s)
        base_db = _db(np.sqrt(np.mean(b_post ** 2) + 1e-18)) \
            if len(b_post) else -120.0
    else:
        later = _seg(x, sr, w1 + 2 * bar_s, min(dur, w1 + 4 * bar_s))
        base_db = _db(np.sqrt(np.mean(later ** 2) + 1e-18)) \
            if len(later) else post_db
    excess = post_db - base_db
    metrics["first_bar_excess_over_b_db"] = round(excess, 2)
    score = 100.0 - float(np.clip(12.0 * max(0.0, excess
                                             - TAIL_EXCESS_FREE_DB),
                                  0.0, 40.0))
    notes = [f"B's first solo bar runs {excess:+.1f} dB over B's own level"]
    if a is not None:
        cr, _ = _chroma(post, sr)
        a_ref = _seg(a, sr, max(0.0, w0 - 4 * bar_s), w0)
        b_ref = _seg(b, sr, w1 + bar_s, min(dur, w1 + 3 * bar_s)) \
            if b is not None else np.zeros(0)
        ca, _ = _chroma(a_ref, sr)
        cb, _ = _chroma(b_ref, sr)
        sa, sb = _cosine(cr, ca), _cosine(cr, cb)
        if sa is not None and sb is not None:
            metrics["post_handoff_chroma_sim_a"] = round(sa, 3)
            metrics["post_handoff_chroma_sim_b"] = round(sb, 3)
            if sa > sb + 0.08 and excess > 1.5:
                score = min(score, 45.0)
                notes.append("post-handoff audio still resembles A more "
                             "than B — A's tail is bleeding over B's "
                             "entrance")
    score = round(score, 1)
    return {"name": "tail_hygiene", "status": _status(score, 75.0, 50.0),
            "score": score, "metrics": metrics, "note": "; ".join(notes)}


# ----------------------------------------------------------------------------
# Suite entry point
# ----------------------------------------------------------------------------

_CHECKS = (check_beat_phase, check_low_clash, check_loudness,
           check_key_clash, check_vocal, check_tail)


def qc_render(x, sr, spec, a=None, b=None, clip_id="clip"):
    """Run the cleanliness suite.

    x: render (mono float). spec: {window_s: (w0, w1), bpm, bar_s,
    beat_offset_s=0, a_grid_offset_s, b_grid_offset_s, lows_contract}.
    a_grid_offset_s / b_grid_offset_s: phase of each side's downbeat
    grid as placed, from the build record (beat_phase scores their
    offset; omit for tempo bridges, where the sides' grids are not
    commensurable and the tail audio check carries the check).
    lows_contract: "continuous" (default) or "free" for techniques
    whose contract lets the low end breathe (wash, sweep, chop) — the
    low-end deficit is then measured but not scored. a/b: the two sides
    as placed on the render timeline (same length as x), or None for
    render-only mode.
    """
    x = np.asarray(x, dtype=np.float64)
    if a is not None:
        a = np.asarray(a, dtype=np.float64)
    if b is not None:
        b = np.asarray(b, dtype=np.float64)
    checks = []
    for fn in _CHECKS:
        try:
            checks.append(fn(x, sr, spec, a, b))
        except Exception as e:  # a broken check must not kill the gate
            checks.append({"name": fn.__name__.replace("check_", ""),
                           "status": "error", "score": None, "metrics": {},
                           "note": f"check errored: {e}"})
    num = den = 0.0
    for c in checks:
        if c["score"] is not None:
            w = WEIGHTS[c["name"]]
            num += w * c["score"]
            den += w
    cleanliness = round(num / den, 1) if den else None
    statuses = {c["status"] for c in checks}
    if "fail" in statuses or (cleanliness is not None
                               and cleanliness < 55.0):
        verdict = "fail"
    elif "warn" in statuses or (cleanliness is not None
                                and cleanliness < 75.0):
        verdict = "warn"
    elif cleanliness is None:
        verdict = "warn"
    else:
        verdict = "pass"
    receipt = {
        "clip": clip_id,
        "mode": "sides" if (a is not None and b is not None)
                else "render-only",
        "duration_s": round(len(x) / sr, 2),
        "window_s": [round(float(spec["window_s"][0]), 2),
                     round(float(spec["window_s"][1]), 2)],
        "checks": checks,
        "cleanliness_score": cleanliness,
        "verdict": verdict,
        "summary": [f"{c['name']}: {c['status']}"
                    + (f" ({c['score']:.0f})" if c["score"] is not None
                       else "")
                    + f" — {c['note']}" for c in checks],
    }
    for line in receipt["summary"]:
        print(f"    qc: {line}", flush=True)
    print(f"    qc: cleanliness={cleanliness} verdict={verdict}",
          flush=True)
    return receipt


def load_side(path, sr, offset_s, total_len, total_sr):
    """Load an excerpt wav, resample to the render sr, place it."""
    from scipy.io import wavfile
    from scipy import signal as sig
    s_sr, raw = wavfile.read(path)
    s = np.asarray(raw, dtype=np.float64)
    if s.ndim > 1:
        s = s.mean(axis=1)
    if np.issubdtype(raw.dtype, np.integer):
        s = s / float(np.iinfo(raw.dtype).max)
    if s_sr != total_sr:
        g = np.gcd(s_sr, total_sr)
        s = sig.resample_poly(s, total_sr // g, s_sr // g)
    return _place(s, total_sr, offset_s, total_len)


def main():
    import argparse
    import json
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    from engine.render import load_mono

    ap = argparse.ArgumentParser(description="transition cleanliness QC")
    ap.add_argument("--render", required=True)
    ap.add_argument("--spec", required=True,
                    help="JSON: {window_s, bpm, bar_s, beat_offset_s, "
                         "a_wav, a_offset_s, b_wav, b_offset_s, "
                         "a_grid_offset_s, b_grid_offset_s, "
                         "lows_contract, clip_id}")
    ap.add_argument("--out", default=None,
                    help="receipt JSON path (default: <render>.qc.json)")
    args = ap.parse_args()

    with open(args.spec) as f:
        spec = json.load(f)
    sr, x = load_mono(args.render)
    a = b = None
    if spec.get("a_wav"):
        a = load_side(spec["a_wav"], sr, spec.get("a_offset_s", 0.0),
                      len(x), sr)
    if spec.get("b_wav"):
        b = load_side(spec["b_wav"], sr, spec.get("b_offset_s", 0.0),
                      len(x), sr)
    receipt = qc_render(x, sr, spec, a, b,
                        clip_id=spec.get("clip_id",
                                         os.path.basename(args.render)))
    out = args.out or (os.path.splitext(args.render)[0] + ".qc.json")
    with open(out, "w") as f:
        json.dump(receipt, f, indent=2)
    print(f"qc receipt -> {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
