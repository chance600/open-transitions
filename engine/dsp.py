"""
open-transitions engine — DSP building blocks.

Deterministic, dependency-light (numpy + scipy only). No model required.
All functions operate on float64 mono numpy arrays in [-1, 1].

Conventions:
  - Gains are linear amplitude unless suffixed _db.
  - Envelopes are per-sample float arrays in [0, 1] (or dB arrays where noted).
  - Filters that change over time are applied block-wise with state carryover
    so there are no clicks at block boundaries.
"""

import numpy as np
from scipy import signal


# ----------------------------------------------------------------------------
# Level helpers
# ----------------------------------------------------------------------------

def db_to_gain(db):
    """dB (scalar or array) -> linear amplitude gain."""
    return 10.0 ** (np.asarray(db, dtype=np.float64) / 20.0)


def gain_to_db(g):
    g = np.maximum(np.asarray(g, dtype=np.float64), 1e-12)
    return 20.0 * np.log10(g)


def normalize_peak(x, target_db=-1.0):
    """Scale so peak hits target_db dBFS. Returns (scaled, applied_gain_db)."""
    peak = np.max(np.abs(x))
    if peak < 1e-12:
        return x, 0.0
    g = db_to_gain(target_db) / peak
    return x * g, gain_to_db(g)


def raised_cosine(n, up=True):
    """Smooth 0->1 (up) or 1->0 (down) ramp, length n."""
    t = np.linspace(0.0, 1.0, n)
    r = 0.5 - 0.5 * np.cos(np.pi * t)
    return r if up else 1.0 - r


def adsr_swish(n, attack_frac=0.7):
    """Swell envelope: smooth rise then quick settle to 1. For risers."""
    t = np.linspace(0.0, 1.0, n)
    env = np.where(t < attack_frac,
                   0.5 - 0.5 * np.cos(np.pi * t / attack_frac),
                   1.0)
    return env


# ----------------------------------------------------------------------------
# 3-band EQ (DJ mixer: Low <250 Hz, Mid 250 Hz-5 kHz, High >5 kHz)
# ----------------------------------------------------------------------------

def split_3band(x, sr, low_cut=250.0, high_cut=5000.0):
    """Split into (low, mid, high) with 2nd-order Linkwitz-Riley crossovers.

    Construction guarantees lo + mid + hi == x (flat reconstruction), so
    time-varying per-band gains can be applied without filter artifacts.
    """
    # 2nd-order Butterworth sections, applied twice each = LR 12 dB/oct
    sos_lo = signal.butter(2, low_cut, btype="lowpass", fs=sr, output="sos")
    sos_hi = signal.butter(2, high_cut, btype="lowpass", fs=sr, output="sos")

    lo = signal.sosfilt(sos_lo, signal.sosfilt(sos_lo, x))
    midhi = x - lo
    mid = signal.sosfilt(sos_hi, signal.sosfilt(sos_hi, midhi))
    hi = midhi - mid
    return lo, mid, hi


def apply_3band_eq(x, sr, low_db, mid_db, high_db, low_cut=250.0, high_cut=5000.0):
    """Apply 3-band EQ with per-sample gain envelopes (dB arrays or scalars).

    low_db / mid_db / high_db: scalar dB or array of length len(x).
    """
    n = len(x)
    lo, mid, hi = split_3band(x, sr, low_cut, high_cut)

    def env(v):
        v = np.asarray(v, dtype=np.float64)
        if v.ndim == 0:
            return np.full(n, float(v))
        assert len(v) == n, "envelope length must match audio"
        return v

    out = (lo * db_to_gain(env(low_db))
           + mid * db_to_gain(env(mid_db))
           + hi * db_to_gain(env(high_db)))
    return out


# ----------------------------------------------------------------------------
# Time-varying sweep filter (for filter-sweep transitions / riser thinning)
# ----------------------------------------------------------------------------

def sweep_filter(x, sr, cutoff_env_hz, ftype="highpass", q=0.707, block=1024):
    """Apply a biquad HP/LP filter whose cutoff follows cutoff_env_hz.

    cutoff_env_hz: scalar or per-sample array. Block-wise coefficient updates
    with state carryover keep it click-free.
    """
    x = np.asarray(x, dtype=np.float64)
    n = len(x)
    if np.ndim(cutoff_env_hz) == 0:
        cut = np.full(n, float(cutoff_env_hz))
    else:
        cut = np.asarray(cutoff_env_hz, dtype=np.float64)
        assert len(cut) == n

    y = np.zeros(n)
    zi = np.zeros(2)
    nyq = sr / 2.0
    for start in range(0, n, block):
        stop = min(start + block, n)
        fc = float(np.mean(cut[start:stop]))
        fc = min(max(fc, 10.0), nyq * 0.99)
        b, a = signal.iirfilter(2, fc / nyq, btype=ftype,
                                ftype="butter", output="ba")
        # normalize biquad-ish: iirfilter returns butterworth; fine for sweeps
        seg, zi = signal.lfilter(b, a, x[start:stop], zi=zi)
        y[start:stop] = seg
    return y


# ----------------------------------------------------------------------------
# Feedback delay (echo-out)
# ----------------------------------------------------------------------------

def feedback_delay(x, sr, delay_s, feedback=0.55, wet=0.6, input_gate=None):
    """Feedback echo. input_gate (per-sample 0..1) models the channel fader.

    For a classic echo-out: gate drops to 0 at the throw while the feedback
    loop keeps ringing (post-fader FX behavior).

    Implements y[n] = x[n] + feedback*y[n-d] as the closed-form geometric
    series y = sum_k feedback^k * shift(x, k*d). This is O(n) per term
    (fully vectorized); the naive sparse-lfilter formulation is O(n*d)
    and hangs on full-length renders (d=8704 at 1/2-beat/152 BPM turned a
    30 s render into ~14 min). Output matches lfilter to ~1e-15.
    """
    x = np.asarray(x, dtype=np.float64)
    n = len(x)
    if input_gate is not None:
        x = x * np.asarray(input_gate, dtype=np.float64)
    d = max(1, int(round(delay_s * sr)))
    # geometric series of the feedback recurrence; stop when the term is
    # below -240 dB (inaudible, and bounds the work for feedback near 1)
    y = x.copy()
    fbp = float(feedback)
    k = 1
    while fbp > 1e-12 and k * d < n:
        y[k * d:] += fbp * x[:-k * d]
        fbp *= feedback
        k += 1
    dry = x
    return (1.0 - wet) * dry + wet * y


# ----------------------------------------------------------------------------
# Schroeder reverb (reverb wash)
# ----------------------------------------------------------------------------

def schroeder_reverb(x, sr, wet=0.7, decay=2.8):
    """Simple Schroeder reverb: 4 parallel combs -> 2 series allpasses.

    decay ~ RT60 in seconds (approx, via comb feedback tuning).
    """
    x = np.asarray(x, dtype=np.float64)

    def comb_delay(d_s, fb):
        d = max(1, int(round(d_s * sr)))
        b = np.zeros(d + 1); b[0] = 1.0
        a = np.zeros(d + 1); a[0] = 1.0; a[d] = -fb
        return b, a

    def allpass_delay(d_s, g):
        d = max(1, int(round(d_s * sr)))
        b = np.zeros(d + 1); b[0] = -g; b[d] = 1.0
        a = np.zeros(d + 1); a[0] = 1.0; a[d] = -g
        return b, a

    # comb feedback from desired decay: fb = 10^(-3 * d_s / decay)
    comb_ds = [0.0297, 0.0371, 0.0411, 0.0437]
    wet_sum = np.zeros_like(x)
    for d_s in comb_ds:
        fb = 10.0 ** (-3.0 * d_s / decay)
        b, a = comb_delay(d_s, fb)
        wet_sum += signal.lfilter(b, a, x)
    wet_sum /= len(comb_ds)
    for d_s, g in [(0.005, 0.7), (0.0017, 0.7)]:
        b, a = allpass_delay(d_s, g)
        wet_sum = signal.lfilter(b, a, wet_sum)

    return (1.0 - wet) * x + wet * wet_sum


# ----------------------------------------------------------------------------
# Riser synthesis (for riser + drop transitions)
# ----------------------------------------------------------------------------

def synth_riser(n, sr, f_noise_lo=400.0, f_noise_hi=8000.0,
                f_tone_lo=110.0, f_tone_hi=880.0, level_db=-14.0,
                duck_bpm=None, duck_db=0.0, duck_bars=None, bar_s=None,
                hp_hz=200.0, lp_hz=12000.0):
    """Classic DJ riser: HP-swept noise + exponentially rising tone + swell.

    Returns mono float array, peak-normalized to level_db.

    T-035 (riser ducking & placement):
      - Placement (caller): start on Bar 1 of the FINAL 8-bar phrase before
        the transition; peak at Bar 8 Beat 4-and; END on the drop's Beat 1 —
        never overlapping the drop.
      - Level: riser peaks -6 dB UNDER the mix bus (level_db=-7 when the mix
        peaks at -1 dBFS).
      - duck_bpm/duck_db: sidechain-style pumping — dips the riser by
        duck_db dB on every beat grid hit (fast attack, ~100 ms release).
        duck_bars limits ducking to the first duck_bars bars (bars 1-4 of an
        8-bar riser); needs bar_s to convert bars to the beat grid.
      - The riser is HP-filtered at hp_hz (never fights the kick's sub) and
        LP-filtered at lp_hz (leaves air for the drop's crash).
    """
    rng = np.random.default_rng(7)  # deterministic
    t = np.arange(n) / sr
    dur = n / sr

    # Exponential sweep curves 0->1
    k = 3.0
    sweep = (np.exp(k * t / dur) - 1.0) / (np.exp(k) - 1.0)

    # Noise through time-varying highpass
    noise = rng.standard_normal(n)
    cut = f_noise_lo * (f_noise_hi / f_noise_lo) ** sweep
    noise_hp = sweep_filter(noise, sr, cut, ftype="highpass", block=2048)

    # Rising tone (sine + a touch of saw-ish via 2nd harmonic)
    phase = 2 * np.pi * np.cumsum(
        f_tone_lo * (f_tone_hi / f_tone_lo) ** sweep) / sr
    tone = np.sin(phase) + 0.3 * np.sin(2 * phase)

    # Swell envelope: grows, slight dip right before the end is added by caller
    env = adsr_swish(n, attack_frac=0.85) ** 1.5

    riser = (noise_hp / (np.max(np.abs(noise_hp)) + 1e-9) * 0.7
             + tone / (np.max(np.abs(tone)) + 1e-9) * 0.5) * env

    # T-035: slot the riser into the kick's gaps (rhythmic slotting).
    if duck_bpm and duck_db > 0:
        beat_s = 60.0 / duck_bpm
        duck_env = np.ones(n)
        if duck_bars is not None and bar_s is not None:
            duck_n = min(n, int(duck_bars * bar_s * sr))
        else:
            duck_n = n
        atk = int(0.005 * sr)          # 5 ms attack
        rel = int(0.100 * sr)          # 100 ms release
        dip = db_to_gain(-duck_db)
        b = 0
        while True:
            hit = int(b * beat_s * sr)
            if hit >= duck_n:
                break
            e = min(hit + atk, duck_n)
            duck_env[hit:e] = np.linspace(1.0, dip, e - hit)
            r = min(hit + atk + rel, duck_n)
            if r > e:
                duck_env[e:r] = np.linspace(dip, 1.0, r - e)
            b += 1
        riser[:duck_n] *= duck_env[:duck_n]

    riser = riser / (np.max(np.abs(riser)) + 1e-9) * db_to_gain(level_db)

    # T-035: never fight the sub, leave air for the crash.
    if hp_hz and hp_hz > 10:
        riser = sweep_filter(riser, sr, hp_hz, ftype="highpass", block=2048)
    if lp_hz and lp_hz < sr / 2 * 0.99:
        riser = sweep_filter(riser, sr, lp_hz, ftype="lowpass", block=2048)
    return riser


# ----------------------------------------------------------------------------
# Time-varying playback rate (brake / tape-stop / power-down / vinyl ramps)
# ----------------------------------------------------------------------------

def warp_resample(x, sr, rate_env, out_len=None):
    """Play `x` with a time-varying playback rate (pitch-coupled, like vinyl).

    rate_env: per-sample playback rate (1.0 = normal speed). Output sample i
    reads input position cumsum(rate_env)[i] via linear interpolation.
    Brake/tape-stop: rate ramps 1 -> 0 (T-006, T-013). Power-down: 1 -> 0
    over 1-2 beats. This changes pitch AND tempo together — the physical
    deceleration the brain reads as "the track dying".
    """
    x = np.asarray(x, dtype=np.float64)
    rate = np.asarray(rate_env, dtype=np.float64)
    n = len(rate) if out_len is None else out_len
    if len(rate) < n:
        rate = np.pad(rate, (0, n - len(rate)), mode="edge")
    pos = np.cumsum(rate[:n])
    pos = np.clip(pos, 0, len(x) - 1)
    return np.interp(pos, np.arange(len(x)), x)


def pitch_dive(x, sr, dive_samples, curve="linear"):
    """Tape-stop dive: playback rate 1 -> 0 over dive_samples (T-006/T-013).

    curve: "linear" (pitch fader pull) or "exp" (vinyl brake dial feel).
    Returns the dived audio (same length as dive_samples; caller pads/mixes).
    """
    n = int(dive_samples)
    u = np.linspace(0.0, 1.0, n)
    if curve == "exp":
        rate = np.exp(-3.0 * u)
        rate = rate / rate[0]
    else:
        rate = 1.0 - u
    rate[-1] = 0.0
    return warp_resample(x, sr, rate, out_len=n)


# ----------------------------------------------------------------------------
# Phase-vocoder time stretch (pitch-preserving, for tempo ramps)
# ----------------------------------------------------------------------------

def phase_vocoder_stretch(x, sr, rate, n_fft=2048, hop=None):
    """Stretch without changing pitch (STFT phase vocoder, Laroche/Dolson).

    rate: scalar (>1 = longer), or a per-analysis-frame array for ramps
        (T-021: the BPM ramp is one continuous pass — chunking into
        constant-rate pieces puts a fade-in at every chunk boundary).
    Synthesis frames advance through the analysis at 1/rate frames per
    output frame; phase accumulates from instantaneous frequency so
    transients stay coherent. Good for small ratios (|rate-1| < ~0.15);
    artifacts grow past that — T-021 keeps ramps gentle (~1 BPM/bar) and
    prefers breakdown (drumless) zones for bigger shifts.
    """
    x = np.asarray(x, dtype=np.float64)
    if hop is None:
        hop = n_fft // 4
    win = np.hanning(n_fft)
    frames = []
    for start in range(0, max(1, len(x) - n_fft + 1), hop):
        frames.append(x[start:start + n_fft] * win)
    if not frames:
        return x.copy()
    frames = np.array(frames)
    n_frames = len(frames)

    rates = np.asarray(rate, dtype=np.float64)
    if rates.ndim == 0:
        if abs(float(rates) - 1.0) < 1e-6:
            return x.copy()
        rates = np.full(n_frames, float(rates))
    else:
        if len(rates) != n_frames:
            # resample the rate envelope onto the frame grid
            xp = np.linspace(0, 1, len(rates))
            rates = np.interp(np.linspace(0, 1, n_frames), xp, rates)

    X = np.fft.rfft(frames, axis=1)
    mag = np.abs(X)
    phase = np.angle(X)
    # instantaneous frequency, radians per analysis hop:
    omega = 2 * np.pi * hop * np.fft.rfftfreq(n_fft, 1.0 / sr) / sr
    dphase = np.diff(phase, axis=0) - omega
    dphase = (dphase + np.pi) % (2 * np.pi) - np.pi
    inst = omega + dphase  # rad per hop, per frame transition
    # synthesis: hop_s == hop (analysis hop); advance phase by inst freq
    # per synthesis frame, stepping through analysis at 1/rate.
    mean_rate = float(np.mean(rates))
    n_synth = max(1, int(n_frames * mean_rate))
    y = np.zeros(n_synth * hop + n_fft)
    wsum = np.zeros_like(y)
    synth_phase = phase[0].copy()
    pos = 0.0
    for i in range(n_synth):
        i0 = int(pos)
        frac = pos - i0
        ia = min(i0, n_frames - 1)
        ib = min(i0 + 1, n_frames - 1)
        m = mag[ia] * (1 - frac) + mag[ib] * frac
        ja = min(i0, len(inst) - 1)
        jb = min(i0 + 1, len(inst) - 1)
        f = inst[ja] * (1 - frac) + inst[jb] * frac
        spec = m * np.exp(1j * synth_phase)
        frame = np.fft.irfft(spec, n=n_fft) * win
        s = i * hop
        y[s:s + n_fft] += frame
        wsum[s:s + n_fft] += win ** 2
        pos += 1.0 / rates[ia]
        synth_phase = synth_phase + f
    wsum[wsum < 1e-9] = 1.0
    y = y / wsum
    # OLA edge hygiene: where overlap is thin (signal edges) the window
    # values approach zero and the division amplifies numerical noise into
    # huge spikes (invisible in RMS, fatal for peak normalization).
    y[wsum < 0.05] = 0.0
    fe = min(int(0.005 * sr), len(y) // 4)
    if fe > 1:
        fade = 0.5 - 0.5 * np.cos(np.pi * np.linspace(0, 1, fe))
        y[:fe] *= fade
        y[-fe:] *= fade[::-1]
    return y[:int(len(x) * mean_rate)]


# ----------------------------------------------------------------------------
# Pitch shift at constant duration (T-032 pitch-play)
# ----------------------------------------------------------------------------

def pitch_shift(x, sr, semitones, n_fft=2048):
    """Shift pitch by `semitones` (positive = up) keeping duration constant.

    Phase-vocoder stretch (pitch-preserving) followed by resampling: net
    effect is a pure pitch shift. |semitones| <= 2 recommended — formants
    shift along with pitch, and beyond ±2 vocals hit the chipmunk/demonic
    uncanny valley (T-032 bank rule). Not formant-preserving.
    """
    x = np.asarray(x, dtype=np.float64)
    if abs(semitones) < 1e-9:
        return x.copy()
    factor = 2.0 ** (semitones / 12.0)
    stretched = phase_vocoder_stretch(x, sr, factor, n_fft=n_fft)
    n_out = len(x)
    pos = np.linspace(0, len(stretched) - 1, n_out)
    return np.interp(pos, np.arange(len(stretched)), stretched)


# ----------------------------------------------------------------------------
# Band-pass sweep (vocal-chop brightness ladder, T-033)
# ----------------------------------------------------------------------------

def bandpass_sweep(x, sr, lo_env_hz, hi_env_hz, block=2048):
    """Time-varying band-pass = HP sweep followed by LP sweep."""
    y = sweep_filter(x, sr, lo_env_hz, ftype="highpass", block=block)
    y = sweep_filter(y, sr, hi_env_hz, ftype="lowpass", block=block)
    return y


# ----------------------------------------------------------------------------
# Crossfades
# ----------------------------------------------------------------------------

def equal_power_xfade(a, b):
    """Equal-power crossfade of two equal-length arrays."""
    n = len(a)
    assert len(b) == n
    u = np.linspace(0.0, 1.0, n)
    return a * np.cos(0.5 * np.pi * u) + b * np.sin(0.5 * np.pi * u)


def linear_fade(n, up=True):
    t = np.linspace(0.0, 1.0, n)
    return t if up else 1.0 - t


# ----------------------------------------------------------------------------
# Analysis helpers (for verification)
# ----------------------------------------------------------------------------

def rms_envelope(x, sr, win_s=0.05):
    """RMS per window (win_s seconds). Returns (times, rms)."""
    w = max(1, int(win_s * sr))
    n = len(x) // w
    xr = x[:n * w].reshape(n, w)
    rms = np.sqrt(np.mean(xr ** 2, axis=1) + 1e-18)
    return np.arange(n) * win_s, rms


def spectral_centroid_track(x, sr, win_s=0.1, hop_s=0.05):
    """Spectral centroid over sliding windows. Returns (times, centroid_hz)."""
    w = max(256, int(win_s * sr))
    hop = max(1, int(hop_s * sr))
    win = np.hanning(w)
    freqs = np.fft.rfftfreq(w, 1.0 / sr)
    times, cents = [], []
    for start in range(0, len(x) - w, hop):
        seg = x[start:start + w] * win
        mag = np.abs(np.fft.rfft(seg)) + 1e-12
        cents.append(np.sum(freqs * mag) / np.sum(mag))
        times.append(start / sr)
    return np.array(times), np.array(cents)
