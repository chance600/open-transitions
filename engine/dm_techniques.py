"""
open-transitions engine — DM-clip techniques (domain module, FRAMEWORK.md §7).

Six techniques distilled from the user's self-DM clip study
(technique-bank/DM-CLIP-STUDY.md, Part A). Each function takes numpy mono
float64 audio + sr and returns mono float64. Docstrings are the spec source;
techniques/<name>.md mirrors them.

  DM-A14 live_loop_mix          2-bar auto-loop + 1/4-beat TRANS gate handoff
  DM-A15 cdj_synth_lead         single-cycle synthesis lead from a loop grab
  DM-A21 tempo_double_trick     pitch-coupled 1x -> 2x ramp into B at 2:1
  DM-A23 reverse_vocal_ambience reverse -> delay -> reverb -> reverse swell
  DM-A39 whoa_reverb_wobble     huge reverb hit + accelerating tremolo tail
  DM-A44 vocal_tremolo_gate     mono fold-down of the Auto-Pan 1/16 trick

TECHNIQUE_FUNCS exports only the two-track renderers compatible with the
plan renderer (fn(a, b, sr, **kwargs)); the single-track FX (A15/A23/A39/
A44) are registered in META and demonstrated via demos/ext_dm.py.
"""

import numpy as np

from . import dsp


def _smooth_gate(gate, sr, smooth_ms=2.0):
    """Click-guard a hard gate envelope with a short Hann moving average."""
    k = max(1, int(smooth_ms / 1000.0 * sr))
    if k <= 1:
        return gate
    kernel = np.hanning(k + 2)[1:-1]
    kernel = kernel / kernel.sum()
    return np.convolve(gate, kernel, mode="same")


def _edge_fades(x, sr, fade_ms=5.0):
    """Protective raised-cosine fades at both ends (click avoidance only)."""
    n = len(x)
    f = min(int(fade_ms / 1000.0 * sr), n // 2)
    if f > 1:
        x = x.copy()
        x[:f] *= dsp.raised_cosine(f, up=True)
        x[-f:] *= dsp.raised_cosine(f, up=False)
    return x


# ----------------------------------------------------------------------------
# DM-A14 — Live Loop Mix (auto-loop + TRANS gate handoff)
# ----------------------------------------------------------------------------

def live_loop_mix(a, b, sr, bpm, bar_s, loop_bars=2, trans_depth=0.85,
                  ramp_beats=8.0):
    """Live loop mix: A's outro locks into a short auto-loop while B enters.

    The last `loop_bars` of `a` are tiled for the full render (the deck's
    AUTO LOOP), a TRANS-style gate chops the loop in 1/4-beat slices, B's
    fader comes up over `ramp_beats`, and the loop fades out underneath —
    the Pioneer DDJ move (SYNC + PLAY, AUTO LOOP, TRANS at 1/4) rendered
    as a two-track transition.

    Parameters
    ----------
    a : outgoing segment (mono float64); only its final `loop_bars` are
        used — the caller passes A's outro, the loop IS the outro once
        engaged. Loop points are assumed bar-aligned.
    b : incoming segment (mono float64); the output is len(b) long.
    sr : sample rate, Hz.
    bpm : tempo of the pair, beats per minute (sets the TRANS grid).
    bar_s : seconds per bar.
    loop_bars : auto-loop length in bars (default 2 bars, the clip's
        setting; the bank's T-027 discipline caps transition loops at
        2 cycles of material).
    trans_depth : TRANS gate depth, 0..1 (default 0.85) — how far the
        gated slices duck. 1.0 = full on/off chopping.
    ramp_beats : fader move duration in beats (default 8.0 beats = 2 bars
        at 4/4): B rises 0->1 while the loop falls 1->0, raised-cosine.

    Why it works: the loop freezes A's groove so its rhythm never decays
    while hands are busy; the 1/4-beat gate is pure theatre on top of a
    stable loop — it signals "something is happening" without disturbing
    the underlying pulse, and because the gate period divides the beat,
    the chops land on grid and read as rhythm, not as dropouts. B entering
    under a still-full-energy loop hides the seam the fader move makes.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    sr = float(sr)
    beat_s = 60.0 / float(bpm)
    loop_n = int(loop_bars * bar_s * sr)
    if len(a) < loop_n:
        a = np.pad(a, (loop_n - len(a), 0))
    loop = a[-loop_n:]

    n = len(b)
    reps = int(np.ceil(n / loop_n)) if loop_n > 0 else 1
    tiled = np.tile(loop, reps)[:n]

    # TRANS gate: alternate on / ducked every 1/4 beat, edges smoothed.
    q = max(1, int(round(0.25 * beat_s * sr)))
    idx = np.arange(n)
    gate = np.where((idx // q) % 2 == 0, 1.0, 1.0 - float(trans_depth))
    gate = _smooth_gate(gate, sr)

    # Fader move: B up (raised cosine), loop down, over ramp_beats.
    ramp_n = min(n, int(round(ramp_beats * beat_s * sr)))
    b_env = np.ones(n)
    a_env = np.zeros(n)
    if ramp_n > 0:
        up = dsp.raised_cosine(ramp_n, up=True)
        b_env[:ramp_n] = up
        a_env[ramp_n:] = 0.0
        a_env[:ramp_n] = 1.0 - up
    return tiled * gate * a_env + b * b_env


# ----------------------------------------------------------------------------
# DM-A15 — CDJ Synth Lead (single-cycle synthesis from a loop grab)
# ----------------------------------------------------------------------------

def _extract_cycle(grab, sr):
    """One waveform cycle from `grab` via rising zero crossings.

    Returns (cycle, f0_hz). The chosen cycle is the one whose length is
    closest to the median crossing period, taken from the back two-thirds
    of the grab (past any hit transient at the grab's head).
    """
    x = np.asarray(grab, dtype=np.float64)
    xc = x - np.mean(x)
    zc = np.flatnonzero((xc[:-1] <= 0) & (xc[1:] > 0)) + 1
    if len(zc) < 3:
        return x.copy(), sr / max(1, len(x))
    periods = np.diff(zc)
    med = float(np.median(periods))
    start_min = len(x) // 3
    cand = [k for k in range(len(periods)) if zc[k] >= start_min]
    if not cand:
        cand = list(range(len(periods)))
    k = min(cand, key=lambda j: abs(periods[j] - med))
    cyc = x[zc[k]:zc[k + 1]]
    if len(cyc) < 8:
        return x.copy(), sr / max(1, len(x))
    return cyc, sr / len(cyc)


def cdj_synth_lead(x, sr, bar_s, loop_beats=1.0, root_hz=110.0,
                   level_db=-6.0):
    """CDJ-as-synth: turn a short loop grab into a playable lead layer.

    The CDJ trick — grab a very short loop, tighten it to a single cycle,
    disable Master Tempo, tune it with the (wide) pitch fader, colour it
    with a band-pass sweep and ping-pong delay — is single-cycle
    synthesis. This renders it directly: one cycle is extracted from a
    `loop_beats` grab at the head of `x` (rising-zero-crossing pair),
    resampled to `root_hz` (the resample IS the pitch tuning — playback
    rate and pitch stay coupled, exactly like Master Tempo off), tiled
    for the length of `x`, swept through a rising band-pass, and given a
    two-tap feedback-delay tail (mono approximation of ping-pong: dotted
    3/4-beat and 1/2-beat taps alternate energy the way the stereo
    original bounces it side to side).

    Parameters
    ----------
    x : source segment (mono float64); the cycle is grabbed from its
        first `loop_beats`, and the lead is rendered len(x) long so it
        can be layered over the same groove it was grabbed from.
    sr : sample rate, Hz.
    bar_s : seconds per bar (sets the delay taps via beat = bar_s / 4).
    loop_beats : loop-grab length in beats (default 1.0 beat — the
        clip tightens from a short loop down to one cycle; the grab only
        needs to contain a clean cycle or two).
    root_hz : target root pitch in Hz (default 110.0 Hz = A2). Tune this
        to the track's key — the lead is a pitched instrument now.
    level_db : lead peak level relative to x's peak, in dB
        (default -6.0 dB, so the layer sits on the groove, not over it).

    Why it works: any periodic-enough slice of audio, looped at cycle
    length, becomes an oscillator whose timbre is the slice's harmonic
    content — a kick+bass grab turns into a buzzy synth tone for free.
    Because the cycle comes from the track itself, the lead's harmonics
    are guaranteed to belong to the track's sound world.
    """
    x = np.asarray(x, dtype=np.float64)
    sr = float(sr)
    n = len(x)
    beat_s = bar_s / 4.0
    grab_n = min(n, max(16, int(round(loop_beats * beat_s * sr))))
    grab = x[:grab_n]

    cycle, _f0 = _extract_cycle(grab, sr)
    target_len = max(8, int(round(sr / float(root_hz))))
    cyc_rs = np.interp(np.linspace(0, len(cycle) - 1, target_len),
                       np.arange(len(cycle)), cycle)
    reps = int(np.ceil(n / target_len)) if target_len > 0 else 1
    lead = np.tile(cyc_rs, reps)[:n]

    # Band-pass colour sweep, opening up over the layer's span.
    lo_env = np.exp(np.linspace(np.log(300.0), np.log(2500.0), n))
    hi_env = np.exp(np.linspace(np.log(1800.0), np.log(12000.0), n))
    lead = dsp.bandpass_sweep(lead, sr, lo_env, hi_env)

    # Mono ping-pong approximation: two feedback taps at dotted-3/4-beat
    # and 1/2-beat, summed — the alternation reads as bounce in mono.
    wet1 = dsp.feedback_delay(lead, sr, 0.75 * beat_s, feedback=0.42,
                              wet=1.0)
    wet2 = dsp.feedback_delay(lead, sr, 0.50 * beat_s, feedback=0.32,
                              wet=1.0)
    lead = 0.55 * lead + 0.35 * wet1 + 0.25 * wet2

    peak_x = np.max(np.abs(x)) if n else 0.0
    peak_l = np.max(np.abs(lead)) if n else 0.0
    if peak_l > 1e-12 and peak_x > 1e-12:
        lead = lead * (peak_x * dsp.db_to_gain(level_db) / peak_l)
    return _edge_fades(lead, sr, fade_ms=10.0)


# ----------------------------------------------------------------------------
# DM-A21 — Tempo Double Trick (metric doubling ramp)
# ----------------------------------------------------------------------------

def tempo_double_trick(a, b, sr, bar_s, ramp_bars=4, ramp_curve="linear"):
    """Tempo double trick: A's tail pitch-ramps 1x -> 2x, B enters at 2:1.

    The last `ramp_bars` of `a` are played with a vinyl-style rate ramp
    from 1.0 to 2.0 (pitch-coupled — pitch and tempo double together,
    Master Tempo off, the CDJ wide-range pitch-fader move). The ramp
    consumes the tail in tail/mean-rate time; at the alignment point,
    where A reaches exactly double tempo, `b` enters full. For the move
    to land on grid, B's tempo must be (close to) twice A's — see the
    META `needs: [half_double_ok]` precondition.

    Parameters
    ----------
    a : outgoing segment (mono float64); its final `ramp_bars` are the
        ramp, everything before plays untouched.
    b : incoming segment (mono float64) at ~2x A's tempo; appended in
        full at the alignment point (3 ms protective fade-in only —
        it enters FULL, not faded).
    sr : sample rate, Hz.
    bar_s : seconds per bar (of A — the ramp length is measured in A's
        bars).
    ramp_bars : length of A's tail that is ramped, in bars
        (default 4 bars).
    ramp_curve : "linear" (steady fader push, default) or "exp"
        (2**u — slow start, fast finish, more turntable-like).

    Why it works: a pitch-coupled doubling is heard as the *same track*
    accelerating, not as a new track — the ear tracks A's timbre through
    the ramp, so when B locks in at the doubled rate the tempo jump
    feels earned rather than imposed. Keeping B's vocal at its natural
    pitch (it never goes through the ramp) is the clip's point: A's
    sacrifice buys B's intact entrance.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    sr = float(sr)
    tail_n = int(ramp_bars * bar_s * sr)
    if len(a) <= tail_n:
        a = np.pad(a, (tail_n - len(a) + 1, 0))
    head, tail = a[:-tail_n], a[-tail_n:]

    # Mean of the 1->2 rate curve sets how long the ramped tail lasts.
    probe = np.linspace(0.0, 1.0, 4096)
    if ramp_curve == "exp":
        mean_rate = float(np.mean(2.0 ** probe))
    else:
        mean_rate = 1.5
    m = max(16, int(round(tail_n / mean_rate)))
    u = np.linspace(0.0, 1.0, m)
    rate = 2.0 ** u if ramp_curve == "exp" else 1.0 + u
    ramped = dsp.warp_resample(tail, sr, rate, out_len=m)

    # B enters FULL: protective 3 ms fade-in only, no fade-out.
    b_in = b
    if len(b):
        b_in = b.copy()
        f = min(int(0.003 * sr), len(b))
        if f > 1:
            b_in[:f] *= dsp.raised_cosine(f, up=True)
    return np.concatenate([head, ramped, b_in])


# ----------------------------------------------------------------------------
# DM-A23 — Reverse Vocal Ambience (reverse -> delay -> reverb -> reverse)
# ----------------------------------------------------------------------------

def reverse_vocal_ambience(vocal, sr, delay_s=0.375, feedback=0.4,
                           delay_wet=1.0, reverb_decay_s=3.5,
                           reverb_wet=0.85, swell_s=1.5):
    """Reverse-vocal ambience: a reverb/delay swell that blooms INTO the vocal.

    The vocal is reversed, run through a feedback delay at 100% wet and
    then a heavy reverb, and the whole result is reversed back to the
    original orientation. Every tail the chain generates in reversed
    time lands *before* its source event in forward time, so the vocal
    arrives preceded by its own ghost — a swelling pre-drop texture
    built from nothing but the vocal itself. `swell_s` of headroom is
    padded into the reversed pass so the tails have somewhere to ring;
    it becomes the pre-swell in the output, which is therefore
    len(vocal) + swell_s long.

    Parameters
    ----------
    vocal : vocal segment (mono float64). Works best on a vocal that
        already has a little reverb/delay printed — the printed tails
        give the chain more to smear (the clip's own note).
    sr : sample rate, Hz.
    delay_s : feedback-delay time in seconds (default 0.375 s).
    feedback : delay feedback ratio (default 0.4 = the clip's 40%).
    delay_wet : delay wet mix (default 1.0 = the clip's 100% wet).
    reverb_decay_s : reverb decay (approx. RT60) in seconds
        (default 3.5 s — "heavy").
    reverb_wet : reverb wet mix, 0..1 (default 0.85).
    swell_s : pre-swell headroom in seconds (default 1.5 s).

    Why it works: reverb and delay are causal — tails only ever follow
    their source. Reversing the signal before the chain and reversing
    back after it is the only way to make a tail precede its source
    without time travel, and because the swell is literally the vocal's
    own spectrum played backwards, it harmonizes with the entrance
    perfectly while reading as pure atmosphere.
    """
    v = np.asarray(vocal, dtype=np.float64)
    sr = float(sr)
    pad_n = int(round(swell_s * sr))
    rev = np.concatenate([v[::-1], np.zeros(pad_n)])
    delayed = dsp.feedback_delay(rev, sr, delay_s, feedback=feedback,
                                 wet=delay_wet)
    reverbed = dsp.schroeder_reverb(delayed, sr, wet=reverb_wet,
                                    decay=reverb_decay_s)
    out = reverbed[::-1].copy()
    return _edge_fades(out, sr, fade_ms=5.0)


# ----------------------------------------------------------------------------
# DM-A39 — Whoa Reverb Wobble (Skrillex 'whoa')
# ----------------------------------------------------------------------------

def whoa_reverb_wobble(vocal, sr, tail_s=2.5, reverb_wet=0.9,
                       decay_s=4.0, rate_start_hz=2.0, rate_end_hz=12.0,
                       trem_depth=0.9):
    """The 'whoa': a vocal hit drowned in reverb, tail wobbling faster and faster.

    A vocal hit is run through a big reverb (90% wet, ~4 s decay, the
    clip's settings) with `tail_s` of ringing room appended, then a
    tremolo is applied whose rate accelerates exponentially from
    `rate_start_hz` to `rate_end_hz` across the clip — the tail starts
    breathing slowly and ends up fluttering, the 'wo-wo-wo' wobble.
    (The clip also overlaps a reversed copy for a pre-tail; this ADOPT
    keeps the signature move — reverb + accelerating tremolo — and
    leaves the pre-tail to reverse_vocal_ambience, DM-A23.)

    Parameters
    ----------
    vocal : the vocal hit (mono float64) — in the clip, just the first
        bit of the vocal, isolated.
    sr : sample rate, Hz.
    tail_s : reverb tail room appended after the hit, in seconds
        (default 2.5 s; output is len(vocal) + tail_s long).
    reverb_wet : reverb wet mix (default 0.9 = the clip's ~90%).
    decay_s : reverb decay (approx. RT60) in seconds (default 4.0 s =
        the clip's ~4 seconds).
    rate_start_hz : tremolo rate at the hit, in Hz (default 2.0 Hz).
    rate_end_hz : tremolo rate at the tail's end, in Hz
        (default 12.0 Hz — the speed-up is the signature).
    trem_depth : tremolo depth, 0..1 (default 0.9; gain dips to
        1 - depth at each trough).

    Why it works: the reverb strips the hit of its dry attack context
    and stretches it into a pad; a *static* tremolo on that pad would
    read as a cheap organ effect, but an accelerating rate creates
    forward motion inside a sound that is otherwise only decaying —
    energy seems to gather even as level falls, which is exactly the
    tension the 'whoa' is used for.
    """
    v = np.asarray(vocal, dtype=np.float64)
    sr = float(sr)
    tail_n = int(round(tail_s * sr))
    padded = np.concatenate([v, np.zeros(tail_n)])
    rv = dsp.schroeder_reverb(padded, sr, wet=reverb_wet, decay=decay_s)

    n = len(rv)
    t = np.arange(n) / sr
    dur = max(n / sr, 1e-6)
    rate_env = rate_start_hz * (rate_end_hz / rate_start_hz) ** (t / dur)
    phase = 2.0 * np.pi * np.cumsum(rate_env) / sr
    trem = 1.0 - float(trem_depth) * (0.5 - 0.5 * np.cos(phase))
    out = rv * trem
    return _edge_fades(out, sr, fade_ms=5.0)


# ----------------------------------------------------------------------------
# DM-A44 — Vocal Tremolo Gate (Auto-Pan 1/16 house vocal, mono)
# ----------------------------------------------------------------------------

def vocal_tremolo_gate(x, sr, bpm, subdiv=16, ramp_start_frac=0.5,
                       depth_max=1.0):
    """House vocal tremolo gate: 1/16 amplitude tremolo, amount slammed in.

    Mono adaptation — stated honestly: the source trick is Ableton's
    Auto Pan at Phase 360°, Rate 1/16, with the Amount automated up to
    100% on one target note. At 360° phase the two channels' LFOs are
    IN PHASE — left and right receive the *same* gain at every instant —
    so the stereo original folds down to mono as a pure amplitude
    tremolo with nothing lost: there is no stereo width in the source
    effect to lose. This function is that exact fold-down: a sine-LFO
    amplitude tremolo locked to the 1/`subdiv` grid, with the amount
    (depth) automation rising steeply (fast-attack cubic) from
    `ramp_start_frac` to 100% at the end of the segment — caller aligns
    the segment so the target note sits in the ramp's second half.
    (The clip's Warp Mode Complex step is a DAW playback setting for
    stretching the clip, not part of the effect; it has no audio-DSP
    counterpart here.)

    Parameters
    ----------
    x : vocal segment (mono float64).
    sr : sample rate, Hz.
    bpm : tempo, beats per minute (sets the tremolo rate: at
        subdiv=16 the LFO runs at 16th notes = bpm * 16 / 240 Hz).
    subdiv : tremolo grid as a note-value denominator (default 16 =
        1/16 notes, the clip's rate).
    ramp_start_frac : where the amount automation starts rising, as a
        fraction of len(x) (default 0.5 — dry first half, gated second
        half, amount reaching 100% at the end).
    depth_max : maximum tremolo depth at amount=100%, 0..1
        (default 1.0 — full gating, gain touches zero at LFO peaks,
        which is what makes the vocal read as stuttered syllables).

    Why it works: a grid-locked tremolo doesn't fight the groove, it
    *joins* it — the vocal starts chopping in the same 16th-note
    language as the hats. Automating the amount instead of switching
    the effect on keeps the entrance musical: the listener hears the
    vocal gradually taken over by the rhythm, and the moment depth hits
    100% the chop becomes the hook.
    """
    x = np.asarray(x, dtype=np.float64)
    sr = float(sr)
    n = len(x)
    rate_hz = float(bpm) * float(subdiv) / 240.0
    phase = 2.0 * np.pi * rate_hz * np.arange(n) / sr
    shape = 0.5 - 0.5 * np.cos(phase)  # 0..1, starts open

    amount = np.zeros(n)
    start = int(ramp_start_frac * n)
    if start < n:
        u = np.linspace(0.0, 1.0, n - start)
        amount[start:] = 1.0 - (1.0 - u) ** 3  # steep: fast rise, settles at 1
    gain = 1.0 - amount * float(depth_max) * shape
    return x * gain


# ----------------------------------------------------------------------------
# Metadata registry (FRAMEWORK.md §3) — evidence from DM-CLIP-STUDY.md Part A
# ----------------------------------------------------------------------------

_DM_THREAD = "self-DM thread 542187470506577; technique-bank/DM-CLIP-STUDY.md"

META = {
    "live_loop_mix": {
        "title": "Live Loop Mix (Auto-Loop + TRANS Gate Handoff)",
        "bank": "DM-A14", "family": "COMP", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 5.0, "camelot_max": 3,
                     "vocal_ok": ["a_only", "b_only", "neither"],
                     "phrase_a_ok": ["outro", "breakdown", "chorus"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta_abs<=1", "weight": 2,
             "reason": "lateral energy — the loop holds A's groove while B lands"},
            {"when": "camelot<=1", "weight": 2,
             "reason": "looped outro and B overlap for bars — keys must sit together"},
        ],
        "energy": {"delta": 0, "tension": "rising"},
        "exit": "loop", "clash_risk": "none",
        "params": {
            "loop_bars": {"type": "int", "range": [1, 4], "default": 2,
                          "unit": "bars"},
            "trans_depth": {"type": "float", "range": [0.0, 1.0],
                            "default": 0.85, "unit": "ratio"},
            "ramp_beats": {"type": "float", "range": [2.0, 16.0],
                           "default": 8.0, "unit": "beats"},
        },
        "evidence": [
            {"type": "clip",
             "ref": f"French Candy — live loop mix on DDJ-RZX ({_DM_THREAD})",
             "url": "https://www.instagram.com/reel/DGLi_b8CgRn/?id=3570101022527980647_358532258&is_sponsored=false&is_ineligible_for_clips_chaining=false",
             "date": "2025-02-19"},
        ],
        "composed_of": ["loop_transition"],
    },
    "cdj_synth_lead": {
        "title": "CDJ Synth Lead (Single-Cycle Synthesis Layer)",
        "bank": "DM-A15", "family": "SYNTH", "kind": "overlay",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "breakdown", "build", "drop",
                                     "verse", "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_a>=5", "weight": 2,
             "reason": "the groove has enough body to carry a synth lead layer"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "tail", "clash_risk": "key",
        "params": {
            "loop_beats": {"type": "float", "range": [0.25, 2.0],
                           "default": 1.0, "unit": "beats"},
            "root_hz": {"type": "float", "range": [55.0, 440.0],
                        "default": 110.0, "unit": "Hz"},
            "level_db": {"type": "float", "range": [-18.0, 0.0],
                         "default": -6.0, "unit": "dB"},
        },
        "evidence": [
            {"type": "clip",
             "ref": f"LoDran (@jred_in_ya_area) — CDJs as playable synths ({_DM_THREAD})",
             "url": "https://www.instagram.com/reel/DA-8LgSIMNV/?id=3476480635745387349_288018017&is_sponsored=false&is_ineligible_for_clips_chaining=false",
             "date": "2025-02-24"},
        ],
        "composed_of": [],
    },
    "tempo_double_trick": {
        "title": "Tempo Double Trick (Metric Doubling Ramp)",
        "bank": "DM-A21", "family": "DYN", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 100.0, "camelot_max": None,
                     "vocal_ok": ["b_only", "neither"],
                     "phrase_a_ok": ["outro", "build", "drop"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": ["half_double_ok"]},
        "prefers": [
            {"when": "half_double_ok", "weight": 3,
             "reason": "exact 2:1 tempo relation — the double lands on grid"},
            {"when": "energy_delta>=1", "weight": 2,
             "reason": "doubling reads as escalation — B should be the bigger record"},
        ],
        "energy": {"delta": 2, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "ramp_bars": {"type": "int", "range": [2, 8], "default": 4,
                          "unit": "bars"},
        },
        "evidence": [
            {"type": "clip",
             "ref": f"French Candy — tempo-doubling pitch trick ({_DM_THREAD})",
             "url": "https://www.instagram.com/reel/DHlriZFiyIK/?id=3595471356923945482_358532258&is_sponsored=false&is_ineligible_for_clips_chaining=false",
             "date": "2025-03-25"},
        ],
        "composed_of": [],
    },
    "reverse_vocal_ambience": {
        "title": "Reverse Vocal Ambience (Pre-Swell Texture)",
        "bank": "DM-A23", "family": "SPACE", "kind": "overlay",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "breakdown", "build", "drop",
                                     "verse", "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "vocal_pair==a_only", "weight": 2,
             "reason": "A carries the vocal — the swell is built from it"},
        ],
        "energy": {"delta": 0, "tension": "rising"},
        "exit": "tail", "clash_risk": "none",
        "params": {
            "delay_s": {"type": "float", "range": [0.05, 1.0],
                        "default": 0.375, "unit": "s"},
            "feedback": {"type": "float", "range": [0.0, 0.7],
                         "default": 0.4, "unit": "ratio"},
            "reverb_decay_s": {"type": "float", "range": [1.0, 8.0],
                               "default": 3.5, "unit": "s"},
            "swell_s": {"type": "float", "range": [0.5, 4.0],
                        "default": 1.5, "unit": "s"},
        },
        "evidence": [
            {"type": "clip",
             "ref": f"Russell Jarvis (@morsbeats_) — reverse vocal ambience ({_DM_THREAD})",
             "url": "https://www.instagram.com/reel/DKzpecXsAgh/?id=3653446134681045025_52378568733&is_sponsored=false&is_ineligible_for_clips_chaining=false",
             "date": "2025-06-12"},
        ],
        "composed_of": [],
    },
    "whoa_reverb_wobble": {
        "title": "Whoa Reverb Wobble (Accelerating Tremolo Tail)",
        "bank": "DM-A39", "family": "SPACE", "kind": "overlay",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "breakdown", "build", "drop",
                                     "verse", "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "vocal_pair==a_only", "weight": 2,
             "reason": "the 'whoa' is built from A's vocal hit"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "tail", "clash_risk": "none",
        "params": {
            "reverb_wet": {"type": "float", "range": [0.5, 1.0],
                           "default": 0.9, "unit": "ratio"},
            "decay_s": {"type": "float", "range": [2.0, 6.0],
                        "default": 4.0, "unit": "s"},
            "rate_end_hz": {"type": "float", "range": [6.0, 20.0],
                            "default": 12.0, "unit": "Hz"},
            "tail_s": {"type": "float", "range": [1.0, 6.0],
                       "default": 2.5, "unit": "s"},
        },
        "evidence": [
            {"type": "clip",
             "ref": f"Philip Harris (@phlourishmusic) — Skrillex 'whoa' vocal ({_DM_THREAD})",
             "url": "https://www.instagram.com/reel/Dc3HMj2NMqc/?id=3978680445254814364_36159507742&is_sponsored=false&is_ineligible_for_clips_chaining=false",
             "date": "2026-09-05"},
        ],
        "composed_of": [],
    },
    "vocal_tremolo_gate": {
        "title": "Vocal Tremolo Gate (Auto-Pan 1/16, Mono)",
        "bank": "DM-A44", "family": "TIME", "kind": "overlay",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 10.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "breakdown", "build", "drop",
                                     "verse", "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "vocal_pair!=neither", "weight": 2,
             "reason": "a vocal is present — the gate needs a vocal to chop"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "seamless", "clash_risk": "none",
        "params": {
            "subdiv": {"type": "int", "range": [4, 32], "default": 16,
                       "unit": "note denominator"},
            "ramp_start_frac": {"type": "float", "range": [0.0, 0.9],
                                "default": 0.5, "unit": "fraction"},
            "depth_max": {"type": "float", "range": [0.0, 1.0],
                          "default": 1.0, "unit": "ratio"},
        },
        "evidence": [
            {"type": "clip",
             "ref": f"PascFrenk — Auto Pan house vocal trick ({_DM_THREAD})",
             "url": "https://www.instagram.com/reel/Dbv_hcQxFuq/?id=3958661972500962218_73805508040&is_sponsored=false&is_ineligible_for_clips_chaining=false",
             "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
}


# Plan-renderer exports (FRAMEWORK.md §7): only fn(a, b, sr, **kwargs)
# renderers. The single-track FX above are META + demo only.
TECHNIQUE_FUNCS = {
    "live_loop_mix": live_loop_mix,
    "tempo_double_trick": tempo_double_trick,
}
