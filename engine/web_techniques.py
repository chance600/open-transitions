"""
open-transitions engine — web-mined techniques (domain module,
FRAMEWORK.md §7).

Six techniques mined from DJ literature outside the bank (2026-10-21
tranche; banked as WEB-01..WEB-06 in technique-bank/TECHNIQUES.md with
full provenance). Each function takes numpy mono float64 audio + sr and
returns mono float64. Docstrings are the spec source; techniques/<name>.md
mirrors them.

  WEB-01 spiral_echo     feedback delay whose repeats pitch-shift
                         (Pioneer DJM SPIRAL beat FX, rendered)
  WEB-02 flanger_sweep   feedback-jet comb sweep over A's final bars
  WEB-03 reverse_roll    reversed loop-sampler roll build (REV ROLL)
  WEB-04 crush_degrade   bit-depth + sample-rate degradation exit
  WEB-05 shepard_riser   Shepard-Risset endless-rise build layer
  WEB-06 granular_freeze frozen-moment grain-cloud handoff

All six are two-track renderers, exported via TECHNIQUE_FUNCS.
"""

import numpy as np

from . import dsp


def _edge_fades(x, sr, fade_ms=5.0):
    """Protective raised-cosine fades at both ends (click avoidance only)."""
    n = len(x)
    f = min(int(fade_ms / 1000.0 * sr), n // 2)
    if f > 1:
        x = x.copy()
        x[:f] *= dsp.raised_cosine(f, up=True)
        x[-f:] *= dsp.raised_cosine(f, up=False)
    return x


def _seam_concat(a, b, sr, guard_ms=3.0):
    """Concatenate with a short crossfade at the seam (click guard).

    Length is len(a) + len(b) - guard. Used where the technique's design
    is a hard join (a flanged/crushed A handing to a dry B) — the guard
    is 3 ms, far below any rhythmic perception; the cut stays a cut.
    """
    g = min(int(guard_ms / 1000.0 * sr), len(a), len(b))
    if g <= 1:
        return np.concatenate([a, b])
    w = np.linspace(0.0, 1.0, g)
    mid = a[-g:] * (1.0 - w) + b[:g] * w
    return np.concatenate([a[:-g], mid, b[g:]])


def _frac_delay(x, delay_samples):
    """Fractional delay line: y[i] = x[i - delay_samples[i]], linear
    interpolation, zero before the start."""
    n = len(x)
    idx = np.arange(n, dtype=np.float64) - np.asarray(delay_samples,
                                                      dtype=np.float64)
    return np.interp(idx, np.arange(n, dtype=np.float64), x,
                     left=0.0, right=0.0)


# ----------------------------------------------------------------------------
# WEB-01 — Spiral Echo (pitch-riding feedback delay)
# ----------------------------------------------------------------------------

def spiral_echo(a, b, sr, bpm, bar_s, delay_beats=0.75,
                shift_semitones=2.0, repeats=8, feedback=0.62,
                fade_bars=2.0):
    """Spiral echo: A's last fragment recirculates, pitch-shifting per repeat.

    The Pioneer DJM SPIRAL beat FX changes delay time as it repeats, so
    pitch rides with it: every return of the echo comes back shifted.
    This renders the transition use: `a` plays dry to its end (the
    fader-kill moment), its final `delay_beats` fragment is thrown into
    the spiral, and the tail of pitch-climbing (or pitch-diving) repeats
    decays across `b`'s entrance — B fades up underneath over
    `fade_bars` while the tail evaporates. Output is len(a) + len(b).

    Parameters
    ----------
    a : outgoing segment (mono float64); the thrown fragment is its
        final `delay_beats`.
    b : incoming segment (mono float64), faded in over `fade_bars`
        starting at the handoff (len(a)).
    sr : sample rate, Hz.
    bpm : tempo of the pair (sets the delay grid).
    bar_s : seconds per bar (sets B's fade).
    delay_beats : delay time in beats (default 0.75 — the dotted value
        the DJM SPIRAL is most often thrown at).
    shift_semitones : pitch step per repeat, signed (default +2.0 —
        spiral up; negative spirals down). This is a *tail* effect:
        the T-032 ±2 formant rule governs vocal overlays, not decaying
        echo repeats; later repeats are `feedback`-attenuated whispers.
    repeats : number of repeats rendered (default 8).
    feedback : per-repeat gain (default 0.62, the DJM LEVEL/DEPTH
        mid-position behaviour).
    fade_bars : B's entrance fade in bars (default 2.0).

    Why it works: an ordinary echo tail keeps the outgoing track's
    pitch center alive under the next track — a clash risk the
    selection layer must police. A spiral tail *leaves* the pitch
    center with every repeat, so it reads as the track evaporating
    rather than ending: B owns the tonal space from its first bar
    while A's rhythm still ghosts across the entrance.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / float(bpm)
    delay_n = max(256, int(round(delay_beats * beat_s * sr)))
    if len(a) >= delay_n:
        seg = a[-delay_n:]
    else:
        seg = np.pad(a, (delay_n - len(a), 0))

    tail = np.zeros(delay_n * int(repeats))
    for k in range(1, int(repeats) + 1):
        rep = dsp.pitch_shift(seg, sr, shift_semitones * k)
        if len(rep) >= delay_n:
            rep = rep[:delay_n]
        else:
            rep = np.pad(rep, (0, delay_n - len(rep)))
        tail[(k - 1) * delay_n:k * delay_n] += rep * (float(feedback) ** k)
    # Tail dies out smoothly instead of truncating mid-repeat.
    f = min(delay_n, len(tail))
    if f > 1:
        tail[-f:] *= dsp.raised_cosine(f, up=False)

    out = np.zeros(len(a) + len(b))
    out[:len(a)] += a
    out[len(a):len(a) + len(tail)] += tail
    fade_n = min(len(b), int(round(fade_bars * bar_s * sr)))
    if fade_n > 0:
        env = np.ones(len(b))
        env[:fade_n] = dsp.raised_cosine(fade_n, up=True)
        out[len(a):] += b * env
    else:
        out[len(a):] += b
    return out


# ----------------------------------------------------------------------------
# WEB-02 — Flanger Sweep (jet comb build/exit)
# ----------------------------------------------------------------------------

def flanger_sweep(a, b, sr, bar_s, sweep_bars=8, cycles=2.0,
                  depth_ms=2.2, base_ms=0.35, mix=0.85):
    """Flanger sweep: a jet comb washes A's final bars; B enters dry.

    A feedback flanger is a copy of the signal delayed by a fraction of
    a millisecond to a few ms, the delay time swept slowly — the comb
    notches it carves sweep the spectrum (Pioneer's Colour FX call it
    "Jet"). Here the sweep runs across A's final `sweep_bars` with the
    wet mix ramping in over the first bar, then A hands to a completely
    dry `b` on the downbeat (3 ms seam guard only — the cut is the
    point). The two-tap feedforward comb (delay d and 2d) is the render
    approximation of the feedback original; the notch sweep, which is
    what the ear tracks, is identical.

    Parameters
    ----------
    a : outgoing segment (mono float64); the sweep zone is its final
        `sweep_bars`.
    b : incoming segment (mono float64), entered dry at len(a).
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    sweep_bars : length of the flanged zone in bars (default 8).
    cycles : full delay-sweep cycles across the zone (default 2.0 —
        slow enough to read as one rising wash per phrase half).
    depth_ms : sweep depth — delay travels base_ms .. base_ms+depth_ms
        (default 2.2 ms, the heart of the jet range).
    base_ms : minimum delay (default 0.35 ms).
    mix : wet tap strength (default 0.85).

    Why it works: the sweep is continuous spectral motion the ear
    tracks effortlessly, and comb cancellation thins A's perceived
    body without touching the fader — so when B arrives unprocessed
    and full-bodied, the contrast lands like a physical entrance.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    zone_n = min(len(a), int(round(sweep_bars * bar_s * sr)))
    if zone_n < 16:
        return _seam_concat(a, b, sr)
    zone = a[-zone_n:]
    t = np.arange(zone_n) / float(sr)
    zone_s = zone_n / float(sr)
    phase = 2.0 * np.pi * float(cycles) * t / zone_s
    d_ms = base_ms + depth_ms * (0.5 - 0.5 * np.cos(phase))
    d1 = _frac_delay(zone, d_ms * sr / 1000.0)
    d2 = _frac_delay(zone, 2.0 * d_ms * sr / 1000.0)
    ramp_n = min(int(round(bar_s * sr)), zone_n)
    ramp = np.ones(zone_n)
    if ramp_n > 0:
        ramp[:ramp_n] = dsp.raised_cosine(ramp_n, up=True)
    wet = zone + float(mix) * ramp * (0.75 * d1 + 0.35 * d2)
    a_out = a.copy()
    a_out[-zone_n:] = wet
    return _seam_concat(a_out, b, sr)


# ----------------------------------------------------------------------------
# WEB-03 — Reverse Roll (reversed loop-sampler build)
# ----------------------------------------------------------------------------

def _tile_window(n, sr):
    """Trapezoid click-guard for one roll tile: 1 ms edges, flat middle."""
    g = max(1, min(n // 4, int(0.001 * sr)))
    w = np.ones(n)
    if n > 2 * g:
        w[:g] = np.linspace(0.3, 1.0, g)
        w[-g:] = np.linspace(1.0, 0.3, g)
    return w


def reverse_roll(a, b, sr, bar_s, roll_bars=2):
    """Reverse roll: A's last beat loops backwards, tightening, into B.

    The Pioneer REV ROLL beat FX grabs a beat fraction and loops it
    reversed. As a transition: `a` plays clean, then its final beat is
    grabbed and tiled backwards across the last `roll_bars` — the tile
    length halves every two tiles (1 beat -> 1/2 -> 1/4 -> 1/8), so the
    reversed suck inward accelerates — and `b` releases on the downbeat
    the roll was consuming. Output is len(a) + len(b).

    Parameters
    ----------
    a : outgoing segment (mono float64); its final beat is the grabbed
        material, its final `roll_bars` are the roll zone.
    b : incoming segment (mono float64), entered at len(a).
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    roll_bars : roll zone length in bars (default 2).

    Why it works: forward rolls (T-008) build by insistence — the same
    hit harder and faster. Reversed tiles build by *inhalation*: every
    transient sucks back into the deck instead of punching out, the
    phrase feels vacuumed away, and B's first downbeat exhales. It is
    the mirror mechanism of the backspin (T-007) — but where a backspin
    is one continuous spin of the whole tail, the reverse roll stays on
    the grid, so B can land beat-locked.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    beat_n = max(64, bar_n // 4)
    zone_n = min(len(a), int(roll_bars) * bar_n)
    if len(a) < beat_n or zone_n < beat_n // 2:
        return _seam_concat(a, b, sr)
    rev = a[-beat_n:][::-1].copy()

    tiles = []
    remaining = zone_n
    f = beat_n
    reps_at_f = 0
    while remaining > 0:
        tl = min(f, remaining)
        tiles.append(tl)
        remaining -= tl
        reps_at_f += 1
        if reps_at_f >= 2:
            f = max(beat_n // 8, f // 2)
            reps_at_f = 0
    roll = np.concatenate([rev[:tl] * _tile_window(tl, sr) for tl in tiles])
    out = np.concatenate([a[:len(a) - zone_n], roll])
    return _seam_concat(out, b, sr)


# ----------------------------------------------------------------------------
# WEB-04 — Crush Degrade (bit-reduction exit)
# ----------------------------------------------------------------------------

def crush_degrade(a, b, sr, bar_s, bars=4, bits_end=5.0, rate_end=0.25,
                  fade_bars=1.0):
    """Crush degrade: A degrades to lo-fi over its final bars; B is clean.

    Pioneer's Crush Colour FX reduces bit resolution (paired with a
    filter); the RMX line adds the crushed echo. As a transition the
    full recipe is: across A's final `bars`, bit depth ramps 16 ->
    `bits_end`, the effective sample rate folds down to `rate_end` of
    the original (sample-hold), and a low-pass folds 12 kHz -> 700 Hz
    alongside. During the final `fade_bars` the crushed ghost
    equal-power-crossfades into `b` arriving at full fidelity — the
    fidelity contrast itself is the drop. Output length is
    len(a) + len(b) - fade.

    Parameters
    ----------
    a : outgoing segment (mono float64); the crush zone is its final
        `bars`.
    b : incoming segment (mono float64), clean, faded in across the
        crush zone's last `fade_bars`.
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    bars : crush zone length in bars (default 4).
    bits_end : final bit depth (default 5.0 — unmistakably crushed,
        still rhythmic).
    rate_end : final sample-rate fraction (default 0.25).
    fade_bars : B's crossfade length in bars (default 1.0).

    Why it works: fidelity is an energy dimension. The crowd hears A
    turn into a toy version of itself — same groove, collapsing
    resolution — while B assembles in full range underneath. No pitch,
    key, or tempo negotiation is involved, so the move is legal across
    genre leaps where blends are not.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    zone_n = min(len(a), int(round(bars * bar_s * sr)))
    if zone_n < 1024:
        return _seam_concat(a, b, sr)
    zone = a[-zone_n:]
    block = 512
    zc = zone.copy()
    for s in range(0, zone_n, block):
        e = min(zone_n, s + block)
        p = (s + block / 2.0) / zone_n
        bits = 16.0 + (float(bits_end) - 16.0) * p
        q = 2.0 ** (bits - 1.0)
        seg = np.round(zc[s:e] * q) / q
        k = max(1, int(round(1.0 + (1.0 / float(rate_end) - 1.0) * p)))
        if k > 1:
            idx = (np.arange(e - s) // k) * k
            seg = seg[idx]
        zc[s:e] = seg
    env = np.exp(np.linspace(np.log(12000.0), np.log(700.0), zone_n))
    zc = dsp.sweep_filter(zc, sr, env, ftype="lowpass")
    a_out = a.copy()
    a_out[-zone_n:] = zc

    fade_n = min(int(round(fade_bars * bar_s * sr)), zone_n, len(b))
    if fade_n <= 0:
        return _seam_concat(a_out, b, sr)
    out = np.zeros(len(a) + len(b) - fade_n)
    out[:len(a)] = a_out
    w = np.linspace(0.0, 1.0, fade_n)
    seg = out[len(a) - fade_n:len(a)].copy()
    out[len(a) - fade_n:len(a)] = (seg * np.cos(w * np.pi / 2.0)
                                   + b[:fade_n] * np.sin(w * np.pi / 2.0))
    out[len(a):] += b[fade_n:]
    return out


# ----------------------------------------------------------------------------
# WEB-05 — Shepard Riser (endless-rise build layer)
# ----------------------------------------------------------------------------

def shepard_riser(a, b, sr, bar_s, bars=8, direction=1, level_db=-9.0,
                  partials=7, base_hz=55.0, center_hz=640.0,
                  sigma_oct=1.15):
    """Shepard riser: an endless-rise synth layer under A's final bars.

    A Shepard-Risset glissando: `partials` sine partials spaced in
    octaves above `base_hz`, all gliding up (or down) together through
    repeated octave cycles, each partial's level wrapped in a Gaussian
    envelope over log-frequency centered at `center_hz` — partials fade
    in at the bottom of the spectrum and out at the top, so the pitch
    seems to rise forever without ever getting higher. Pioneer's DJM
    Mobius beat FX applies the same illusion as a filter; this renders
    it as a synthesized layer (the T-018/T-035 riser family member that
    cannot run out of headroom). The layer fades in over the first bar
    of the zone, sits at `level_db` relative to A's peak, and cuts dead
    on the handoff — `b` inherits all the unresolved rising tension.
    Output is len(a) + len(b) (3 ms seam guard).

    Parameters
    ----------
    a : outgoing segment (mono float64); the layer zone is its final
        `bars`.
    b : incoming segment (mono float64), entered at len(a).
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    bars : layer zone length in bars (default 8); the glide completes
        one octave cycle per 4 bars.
    direction : +1 rises, -1 falls (default +1).
    level_db : layer peak relative to A's peak (default -9.0 dB —
        presence without masking).
    partials : number of octave partials (default 7).
    base_hz : lowest partial's starting frequency (default 55 Hz).
    center_hz : Gaussian envelope center (default 640 Hz).
    sigma_oct : envelope width in octaves (default 1.15).

    Why it works: a conventional riser spends pitch and loudness and
    arrives; the Shepard layer never arrives, so tension can stretch
    across a whole phrase without the fatigue of a sound that is
    literally getting louder and higher the whole time. The only
    resolution on offer is B's first bar.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    zone_n = min(len(a), int(round(bars * bar_s * sr)))
    if zone_n < 1024:
        return _seam_concat(a, b, sr)
    t = np.arange(zone_n) / float(sr)
    zone_s = zone_n / float(sr)
    cycles = max(1.0, float(bars) / 4.0)
    frac = (t * cycles / zone_s) % 1.0
    if direction < 0:
        frac = (1.0 - frac) % 1.0
    layer = np.zeros(zone_n)
    for k in range(int(partials)):
        f = float(base_hz) * 2.0 ** (k + frac)
        amp = np.exp(-(np.log2(f / float(center_hz)) ** 2)
                     / (2.0 * float(sigma_oct) ** 2))
        phase = 2.0 * np.pi * np.cumsum(f) / float(sr)
        layer += amp * np.sin(phase)
    peak_layer = np.max(np.abs(layer))
    peak_a = np.max(np.abs(a)) if len(a) else 0.0
    if peak_layer > 0 and peak_a > 0:
        layer *= (dsp.db_to_gain(float(level_db)) * peak_a) / peak_layer
    ramp_n = min(int(round(bar_s * sr)), zone_n)
    if ramp_n > 0:
        layer[:ramp_n] *= dsp.raised_cosine(ramp_n, up=True)
    layer = _edge_fades(layer, sr, fade_ms=2.0)
    a_out = a.copy()
    a_out[-zone_n:] += layer
    return _seam_concat(a_out, b, sr)


# ----------------------------------------------------------------------------
# WEB-06 — Granular Freeze (frozen-moment cloud handoff)
# ----------------------------------------------------------------------------

def granular_freeze(a, b, sr, bar_s, cloud_bars=4, capture_ms=150.0,
                    grain_ms=70.0, density=45.0, drift=0.7, seed=7):
    """Granular freeze: A's last moment becomes a grain cloud; B enters in it.

    At the freeze point (`cloud_bars` before A's end), a `capture_ms`
    fragment of `a` is sustained as a cloud of overlapping Hann-windowed
    grains — the Amazing Noises Grain Freezer recipe (capture ~150 ms,
    sustain as a texture of up to dozens of simultaneous grains). Across
    the cloud zone the grain read position drifts forward through the
    capture (`drift` of its length) while `b` equal-power-fades up
    *inside* the cloud; at the zone's end the cloud is gone and B plays
    alone. Output length is len(a) - cloud_zone + len(b).

    The cloud is A's own material — its harmonics, its formants — with
    its rhythm and pitch commitment dissolved by the grain window,
    which is exactly what separates this from T-034 (reverb freeze
    freezes the *room's* tail; this freezes the *source*).

    Parameters
    ----------
    a : outgoing segment (mono float64); the capture is taken from
        just before the freeze point.
    b : incoming segment (mono float64); its first `cloud_bars` play
        inside the cloud.
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    cloud_bars : cloud zone length in bars (default 4).
    capture_ms : captured fragment length (default 150 ms, the Grain
        Freezer's capture size).
    grain_ms : grain length (default 70 ms).
    density : grains per second (default 45 — dense enough to read as
        texture, sparse enough to keep the source's grain).
    drift : how far the read position scans through the capture across
        the zone, as a fraction (default 0.7).
    seed : grain-position jitter seed (default 7) — the render is
        deterministic; the jitter is frozen into the recipe.

    Why it works: the ear recognizes the cloud as *made of A* while
    owing it no beat or key allegiance, so B can enter at any tempo or
    key inside it and still feel handed-over rather than interrupted —
    a texture bridge whose provenance is the audio itself.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    zone_n = int(round(cloud_bars * bar_s * sr))
    freeze = len(a) - zone_n
    if freeze <= 0 or len(b) <= zone_n:
        return _seam_concat(a, b, sr)
    cap_n = int(round(capture_ms / 1000.0 * sr))
    grain_n = max(64, int(round(grain_ms / 1000.0 * sr)))
    cap = a[max(0, freeze - cap_n):freeze]
    if len(cap) < grain_n:
        cap = np.pad(cap, (0, grain_n - len(cap)), mode="wrap")
    win = np.hanning(grain_n)
    rng = np.random.default_rng(int(seed))
    hop = max(1, int(round(sr / float(density))))
    cloud = np.zeros(zone_n + grain_n)
    max_start = max(1, len(cap) - grain_n)
    for start in range(0, zone_n, hop):
        u = start / max(1, zone_n)
        center = (u * float(drift) * max_start
                  + rng.uniform(-0.1, 0.1) * grain_n)
        s0 = int(np.clip(center, 0, max_start))
        cloud[start:start + grain_n] += cap[s0:s0 + grain_n] * win
    cloud = cloud[:zone_n]
    rms_cap = float(np.sqrt(np.mean(cap ** 2))) + 1e-12
    rms_cloud = float(np.sqrt(np.mean(cloud ** 2))) + 1e-12
    cloud *= rms_cap / rms_cloud
    u = np.linspace(0.0, 1.0, zone_n)
    zone = (cloud * np.cos(u * np.pi / 2.0)
            + b[:zone_n] * np.sin(u * np.pi / 2.0))
    return np.concatenate([a[:freeze], zone, b[zone_n:]])


# ----------------------------------------------------------------------------
# Metadata registry (FRAMEWORK.md §3) — merged by engine/meta.py
# ----------------------------------------------------------------------------

_PEST = {"type": "cookbook",
         "ref": "Pestrela DJ Knowledge Base — Effects (DJM Beat FX / "
                "Colour FX taxonomy)",
         "url": "https://pestrela.github.io/dj_kb/effects/",
         "date": "2026-10-21"}

META = {
    "spiral_echo": {
        "title": "Spiral Echo (Pitch-Riding Feedback Delay)",
        "bank": "WEB-01", "family": "SPACE", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 10.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "breakdown", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "camelot>=2", "weight": 2,
             "reason": "the tail leaves A's pitch center — key distance "
                       "is forgiven"},
            {"when": "phrase_a==outro", "weight": 1,
             "reason": "a thrown final fragment is the classic spiral "
                       "exit"},
        ],
        "energy": {"delta": 0, "tension": "falling"},
        "exit": "tail", "clash_risk": "none",
        "params": {
            "delay_beats": {"type": "float", "range": [0.25, 1.5],
                            "default": 0.75, "unit": "beats",
                            "presets": {"quarter": 0.25, "dotted": 0.75,
                                        "beat": 1.0}},
            "shift_semitones": {"type": "float", "range": [-6.0, 6.0],
                                "default": 2.0, "unit": "semitones",
                                "presets": {"up2": 2.0, "up4": 4.0,
                                            "down2": -2.0, "down4": -4.0}},
            "repeats": {"type": "int", "range": [2, 16], "default": 8,
                        "unit": "repeats"},
            "feedback": {"type": "float", "range": [0.0, 0.85],
                         "default": 0.62, "unit": "ratio"},
            "fade_bars": {"type": "float", "range": [0.5, 8.0],
                          "default": 2.0, "unit": "bars"},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Pioneer DJM-450 manual — SPIRAL beat FX: pitch "
                    "changes simultaneously with delay time; LEVEL/DEPTH "
                    "sets feedback",
             "url": "https://www.manua.ls/pioneer/djm-450/manual?p=12",
             "date": "2026-10-21"},
            dict(_PEST),
        ],
        "composed_of": ["echo_out"],
    },
    "flanger_sweep": {
        "title": "Flanger Sweep (Jet Comb Build/Exit)",
        "bank": "WEB-02", "family": "FREQ", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "build", "drop", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta>=1", "weight": 2,
             "reason": "B's dry fullness contrasts the thinned A — "
                       "better when B is the bigger record"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "sweep_bars": {"type": "int", "range": [2, 16], "default": 8,
                           "unit": "bars",
                           "presets": {"tight": 4, "standard": 8,
                                       "long": 16}},
            "depth_ms": {"type": "float", "range": [0.5, 5.0],
                         "default": 2.2, "unit": "ms",
                         "presets": {"subtle": 1.2, "jet": 2.2,
                                     "deep": 3.8}},
            "cycles": {"type": "float", "range": [0.5, 8.0],
                       "default": 2.0, "unit": "cycles"},
            "mix": {"type": "float", "range": [0.0, 1.0],
                    "default": 0.85, "unit": "ratio"},
        },
        "evidence": [
            dict(_PEST),
            {"type": "course",
             "ref": "Engine DJ transition techniques — modulation "
                    "effects (flanger/phaser) for transition movement",
             "url": "https://app.studyraid.com/en/read/5035/107802/"
                    "layering-and-transition-techniques",
             "date": "2026-10-21"},
        ],
        "composed_of": [],
    },
    "reverse_roll": {
        "title": "Reverse Roll (Reversed Loop-Sampler Build)",
        "bank": "WEB-03", "family": "TIME", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 5.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "build", "drop"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta>=1", "weight": 2,
             "reason": "the inhalation build pays off into a bigger B"},
            {"when": "bpm_delta_pct<=1", "weight": 1,
             "reason": "grid-locked release — matched tempos keep the "
                       "roll honest"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "roll_bars": {"type": "int", "range": [1, 4], "default": 2,
                          "unit": "bars",
                          "presets": {"quick": 1, "standard": 2,
                                      "long": 4}},
        },
        "evidence": [dict(_PEST)],
        "composed_of": ["loop_roll_build"],
    },
    "crush_degrade": {
        "title": "Crush Degrade (Bit-Reduction Exit)",
        "bank": "WEB-04", "family": "DYN", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "verse", "chorus", "drop"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "genre_pair==leap", "weight": 2,
             "reason": "no pitch/tempo negotiation — the fidelity "
                       "contrast carries genre leaps"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "bits_end": {"type": "float", "range": [3.0, 10.0],
                         "default": 5.0, "unit": "bits",
                         "presets": {"lofi": 7.0, "crushed": 5.0,
                                     "destroyed": 3.5}},
            "bars": {"type": "int", "range": [2, 8], "default": 4,
                     "unit": "bars",
                     "presets": {"short": 2, "standard": 4, "long": 8}},
            "rate_end": {"type": "float", "range": [0.1, 0.75],
                         "default": 0.25, "unit": "ratio"},
            "fade_bars": {"type": "float", "range": [0.25, 4.0],
                          "default": 1.0, "unit": "bars"},
        },
        "evidence": [dict(_PEST)],
        "composed_of": [],
    },
    "shepard_riser": {
        "title": "Shepard Riser (Endless-Rise Build Layer)",
        "bank": "WEB-05", "family": "SYNTH", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "build", "drop", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta>=2", "weight": 2,
             "reason": "unresolved rising tension wants a much bigger "
                       "B to resolve into"},
            {"when": "phrase_a==build", "weight": 1,
             "reason": "the layer doubles a build that is already "
                       "rising"},
        ],
        "energy": {"delta": 2, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "direction": {"type": "int", "range": [-1, 1], "default": 1,
                          "unit": "sign",
                          "presets": {"up": 1, "down": -1}},
            "bars": {"type": "int", "range": [4, 16], "default": 8,
                     "unit": "bars",
                     "presets": {"short": 4, "standard": 8, "long": 16}},
            "level_db": {"type": "float", "range": [-24.0, -3.0],
                         "default": -9.0, "unit": "dB"},
            "partials": {"type": "int", "range": [4, 10], "default": 7,
                         "unit": "partials"},
        },
        "evidence": [
            dict(_PEST),
            {"type": "tutorial",
             "ref": "Sound on Sound — iZotope Mobius Filter review: "
                    "Shepard-tone construction (octave sine stack under "
                    "a level envelope) as perpetual-motion build",
             "url": "https://www.soundonsound.com/reviews/"
                    "izotope-mobius-filter",
             "date": "2026-10-21"},
        ],
        "composed_of": ["noise_echo_buildup"],
    },
    "granular_freeze": {
        "title": "Granular Freeze (Frozen-Moment Cloud Handoff)",
        "bank": "WEB-06", "family": "SPACE", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "breakdown", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "genre_pair==leap", "weight": 2,
             "reason": "the cloud owes no key/tempo allegiance — it "
                       "bridges leaps"},
            {"when": "phrase_a==breakdown", "weight": 1,
             "reason": "a sparse A freezes into a richer cloud than a "
                       "dense one"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "tail", "clash_risk": "none",
        "params": {
            "grain_ms": {"type": "float", "range": [25.0, 150.0],
                         "default": 70.0, "unit": "ms",
                         "presets": {"fine": 35.0, "standard": 70.0,
                                     "coarse": 120.0}},
            "cloud_bars": {"type": "int", "range": [2, 8], "default": 4,
                           "unit": "bars",
                           "presets": {"short": 2, "standard": 4,
                                       "long": 8}},
            "capture_ms": {"type": "float", "range": [80.0, 250.0],
                           "default": 150.0, "unit": "ms"},
            "density": {"type": "float", "range": [10.0, 90.0],
                        "default": 45.0, "unit": "grains/s"},
            "drift": {"type": "float", "range": [0.0, 1.0],
                      "default": 0.7, "unit": "fraction"},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Amazing Noises Grain Freezer — captures a ~150 ms "
                    "fragment and sustains it as a cloud of overlapping "
                    "grains (Rekkerd, 2026-10-21)",
             "url": "https://rekkerd.org/free-grain-freezer-granular-"
                    "effect-plugin-by-amazing-noises-vst3-au/",
             "date": "2026-10-21"},
            {"type": "tutorial",
             "ref": "Sound on Sound — Granular Synthesis: A Practical "
                    "Introduction (size/density/position; smeared and "
                    "frozen textures)",
             "url": "https://www.soundonsound.com/techniques/"
                    "granular-synthesis-practical-introduction",
             "date": "2026-10-21"},
        ],
        "composed_of": ["reverb_freeze"],
    },
}


# Plan-renderer exports (FRAMEWORK.md §7): fn(a, b, sr, **kwargs).
TECHNIQUE_FUNCS = {
    "spiral_echo": spiral_echo,
    "flanger_sweep": flanger_sweep,
    "reverse_roll": reverse_roll,
    "crush_degrade": crush_degrade,
    "shepard_riser": shepard_riser,
    "granular_freeze": granular_freeze,
}
