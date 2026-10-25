"""open-transitions — genre traditions tranche B domain module
(FRAMEWORK.md §7).

Registers the Phase 27 expansion tranche 6 bases (WEB-30..WEB-33):
genre traditions tranche B — techno multi-deck doctrine, trance /
harmonic traditions, open-format tables — mined 2026-10-24 from
free / public sources fetched first-hand in full:

* Mixgraph, "DJ Transition Techniques" (breakdown swap)
* Pioneer DJ blog, "A complete guide to multi-deck mixing"
  (toolkit / molecular / high-performance multi-deck doctrine)
* DJ Gym, "The Ultimate Guide to Multi-Deck Mixing"
  (frequency-pyramid roles, phase management)
* DJ.Studio, "Techno DJ Techniques" (corroboration)
* Crossfader, "3 Ways To Mix Techno" via the summarize.tech
  transcript mirror (AI-summary grade — corroboration only)
* Club Ready DJ School, harmonic-mixing guide (compatibility vs
  modulation, +7 / +9 moves, unforgiving set)
* Mixed In Key wiki, harmonic-mixing explained + 5 techniques
  (vendor canon, power block, energy-boost staging + quota)
* PulseDJ blog, open-format guide (strategy table: hard cut /
  wordplay mix / echo out reset / transition track)
* Crossfader, "How To Mix Hip Hop" (sampler deck, stabbed
  wordplay, instant doubles, sample pairing, transition-track
  selection)
* DJ Brian B, wordplay archive (phrase wordplay, snapping,
  acapella-dodges-key)
* GMB Connect DJ-tutorials feed (first item AI-grade;
  half/double corroboration only)

NOT fetched, by the standing paid-canon rule (his 2026-10-22
call, all paid canons parked indefinitely): the Ferry Corsten
trance masterclass (Digital DJ Tips) and Crossfader's trance
course. Nothing below rests on them.

All material renders on the suite's synthesized sketch audio —
no copyrighted audio. Demos prove shape, not feel: nothing in
this tranche was heard by human ears.
"""

import numpy as np


# ----------------------------------------------------------------------------
# Small DSP helpers (module-local; the patterns mirror engine/dsp.py
# conventions without importing the whole DSP surface)
# ----------------------------------------------------------------------------

def _seg(x, n):
    """Trim / zero-pad an array to exactly n samples."""
    x = np.asarray(x, dtype=np.float64)
    if len(x) >= n:
        return x[:n]
    return np.pad(x, (0, n - len(x)))


def _smootherstep(n):
    """Smootherstep 0 -> 1 across n samples (zero-slope ends)."""
    t = np.linspace(0.0, 1.0, n)
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


def _join(head, tail, guard):
    """Concatenate with an equal-power guard crossfade at the seam."""
    if guard <= 0 or len(head) == 0 or len(tail) == 0:
        return np.concatenate([head, tail])
    g = min(guard, len(head), len(tail))
    t = np.linspace(0.0, np.pi / 2.0, g)
    out = np.concatenate([head, tail])
    out[len(head) - g:len(head)] = (head[-g:] * np.cos(t)
                                    + tail[:g] * np.sin(t))
    out = np.concatenate([out[:len(head)],
                          tail[g:]])
    return out


def _onepole_lowpass(x, alpha=0.35):
    """Gentle one-pole lowpass (echo-tail darkening, SP-404 damping law)."""
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1.0 - alpha) * acc + alpha * v
        y[i] = acc
    return y


def _default_bed(n, sr, bar_s):
    """Neutral ambient bed: slow sines + 1-bar attack/release envelope.

    Used when the caller supplies no third-deck bed audio. The bed
    is deliberately beatless — no kick, no hats — so it carries no
    tempo reference of its own; that absence is the mechanism.
    """
    t = np.arange(n) / sr
    pad = (0.5 * np.sin(2 * np.pi * 55.0 * t)
           + 0.3 * np.sin(2 * np.pi * 82.5 * t)
           + 0.2 * np.sin(2 * np.pi * 110.0 * t))
    bar_n = max(1, int(round(bar_s * sr)))
    env = np.ones(n)
    a = min(bar_n, n)
    env[:a] = 0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a)
    env[-a:] = 0.5 + 0.5 * np.cos(np.pi * np.arange(a) / a)
    pad = pad * env
    peak = np.max(np.abs(pad)) + 1e-9
    return pad / peak * 0.6


# ----------------------------------------------------------------------------
# WEB-30 — breakdown_swap (Mixgraph)
# ----------------------------------------------------------------------------

def breakdown_swap(a, b, sr, bar_s, swap_bars=8, b_drums=None):
    """B's beat enters under A's drumless breakdown; the handoff
    completes when the breakdown resolves.

    Mixgraph's breakdown swap: "Track A enters a breakdown — the
    beat drops out, the melody floats — and during that open
    space, Track B's beat enters underneath. When Track A's
    breakdown ends, the DJ has already transitioned to Track B's
    groove." The window needs at least 8 bars of open space;
    a 4-bar breakdown "doesn't give you enough time to establish
    the incoming track" and sounds rushed, not intentional.

    Rendered: A's breakdown segment plays for `swap_bars` bars
    while B's drums stem fades in on a smootherstep (0 -> full
    across the window); at the window end B plays full from its
    bar `swap_bars` onward (no repeated drums bars). The drums
    fade is the whole gesture: B's groove is already running
    when A's breakdown resolves, so the crowd barely notices
    the transition — "the most musical transition technique
    because it uses the structure of the music itself."

    Why it is not its neighbours: not T-023
    `breakdown_transition` (two DRUMLESS sections blended with
    mid/high EQs only, no beatmatching constraint — here B
    brings its BEAT into the open space, so the grids must
    agree and the handoff is a drum entry, not a blend); not
    T-001 `eq_blend` (no breakdown window, no drum-entry law);
    not T-022 `drum_bridge` (a bridge built from drums alone
    between two full sections — here the drums arrive inside
    an existing breakdown).

    Parameters
    ----------
    a : A's breakdown segment (drumless audio, caller-supplied).
    b : B full track (continues from bar `swap_bars` onward).
    sr : sample rate (Hz). bar_s : seconds per bar.
    swap_bars : open-space window in bars (default 8, the
        source's floor; 16 is the long-breakdown staging).
    b_drums : B's drums stem for the window (caller-supplied,
        same class as cue times: render_variant callers pass it
        via ctx). Required — the beat entering under the
        breakdown must be drums, not B's full mix.

    Returns a mono float64 mix of len(b) samples (window +
    B's continuation).
    """
    if b_drums is None:
        raise ValueError(
            "breakdown_swap needs b_drums (B's drums stem) — "
            "pass it via ctx, as with cue times")
    bar_n = int(round(bar_s * sr))
    n = swap_bars * bar_n
    a_win = _seg(a, n)
    drums = _seg(b_drums, n)
    env = _smootherstep(n)
    win = a_win + drums * env * 0.9
    tail = np.asarray(b, dtype=np.float64)[n:]
    guard = max(1, int(0.003 * sr))
    return _join(win, tail, guard)


# ----------------------------------------------------------------------------
# WEB-31 — echo_out_reset (PulseDJ; compound of echo_out + hard_cut)
# ----------------------------------------------------------------------------

def echo_out_reset(a, b, sr, bar_s, bpm, tail_bars=2, beat_div=0.5):
    """Echo tail stands alone, resets the room's metronome, then
    B drops on a clean downbeat at any BPM.

    PulseDJ's Echo Out Reset: a heavy 1/2- or 3/4-beat echo on a
    vocal loop or melody on the outgoing deck, the channel fader
    pulled down dramatically, "a rhythmic ambient tail drifting
    through the speakers. This resets the room's internal
    metronome, allowing you to drop your new track at any BPM
    on the next clean downbeat." Best at the climax of a
    build-up or the end of a phrase; "clean palette cleanser;
    resets room expectations." The BPM gap is unlimited by
    construction — there is no overlap in which tempos could
    fight.

    Rendered: A plays full; then a feedback-delay tail (the
    delay line's buffered content playing out at decaying gain,
    gently darkened — the buffer holds the throw's last
    `beat_div` beats, so the tail starts immediately, with no
    silence gap); then B enters dry at full level on the next
    downbeat. The tail is the whole bridge: B is never
    underneath it.

    Why it is not its neighbours: not T-004 `echo_out` (the
    tail there covers B's entrance underneath — here the tail
    stands ALONE and B starts after it; the reset law, not the
    echo, is the technique); not T-034 `reverb_freeze` (B
    launches INSIDE the frozen tail — here B launches AFTER
    the tail, on a clean downbeat); not T-030 `hard_cut` (the
    cut alone has no metronome reset — the tail is what lets
    any-BPM drops land).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bar_s : seconds per bar.
    bpm : tempo, caller context / signature parity (the echo
        grid derives from bar_s; the drop itself is
        tempo-independent by the reset law).
    tail_bars : tail length in bars (default 2; the source's
        tail drifts "through the speakers" for a phrase-scale
        span, not a single beat).
    beat_div : echo division in beats (default 0.5; 0.75 is
        the dotted staging — the same divisions PulseDJ names).

    Returns a mono float64 mix of len(a) + tail + len(b).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    beat_n = max(1, bar_n // 4)
    d = max(1, int(round(beat_div * beat_n)))
    tail_n = tail_bars * bar_n
    buf = a[-d:] if len(a) >= d else _seg(a, d)
    reps = int(np.ceil(tail_n / d))
    tail = np.concatenate([buf * (0.55 ** k) for k in range(reps)])[:tail_n]
    tail = _onepole_lowpass(tail, alpha=0.35)
    guard = max(1, int(0.003 * sr))
    out = _join(a, tail, guard)
    out = _join(out, b, guard)
    return out


# ----------------------------------------------------------------------------
# WEB-32 — bed_tempo_switch (Pioneer Djrum + DJ.Studio corroboration)
# ----------------------------------------------------------------------------

def bed_tempo_switch(a, b, sr, bar_s, bed=None, bed_bars=4):
    """A beatless third-deck ambient bed covers a hard tempo
    discontinuity; B drops at the new tempo from the bed.

    Pioneer DJ's multi-deck guide: Djrum "showed how an ambient
    track on a third deck can be used as a transitional sound
    bed for big switches between tempos." DJ.Studio corroborates
    the shape from the other side: ambient / minimal tracks
    "serve as excellent bridges between more high-energy techno
    tracks." The mechanism is the bed's beatlessness: with no
    kick, no hats, no tempo reference sounding, the room's
    metronome is unanchored, so B can arrive at a wholly
    different tempo without a ramp, a stretch, or a clash.

    Rendered: A crossfades into the bed over its final 2 bars
    (equal-power); the bed sustains alone for `bed_bars` bars
    total; B enters dry at full level on the next downbeat.
    When the caller supplies no bed audio, a neutral synthesized
    pad (slow sines, 1-bar attack/release) stands in — the
    structure, not any particular bed's content, is the
    technique.

    Why it is not its neighbours: not T-021 `tempo_bridge`
    (a live pitch-preserving ramp — here nothing ramps; the
    tempo jumps under cover); not WEB-31 `echo_out_reset`
    (A's OWN tail covers a brief reset — here a THIRD deck's
    sustained bed covers a phrase-scale switch); not T-023
    `breakdown_transition` (a drumless BLEND of two tracks —
    here the bed is neither track, and B drops after it, not
    through it).

    Parameters
    ----------
    a : outgoing segment. b : incoming segment (at the new
        tempo — tempo endpoints are caller context; the render
        proves the bed structure, and the demo's fixed sketch
        BPM means the demo proves structure, not the
        discontinuity itself).
    sr : sample rate (Hz). bar_s : seconds per bar.
    bed : ambient bed audio, or None for the neutral
        synthesized pad (default None — the pad fallback is
        what lets the variant binder render this base without
        caller-supplied bed audio).
    bed_bars : bed length in bars, including the 2-bar
        crossfade (default 4; range 2–8).

    Returns a mono float64 mix of len(a) + bed + len(b) minus
    the 2-bar crossfade overlap.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    n_bed = bed_bars * bar_n
    fade_n = 2 * bar_n
    bed_seg = (_default_bed(n_bed, sr, bar_s) if bed is None
               else _seg(bed, n_bed))
    if len(a) <= fade_n or n_bed < fade_n:
        raise ValueError("bed_tempo_switch needs a longer than "
                         "2 bars and bed_bars >= 2")
    t = np.linspace(0.0, np.pi / 2.0, fade_n)
    cross = a[-fade_n:] * np.cos(t) + bed_seg[:fade_n] * np.sin(t)
    mid = bed_seg[fade_n:]
    guard = max(1, int(0.003 * sr))
    out = np.concatenate([a[:-fade_n], cross, mid])
    out = _join(out, b, guard)
    return out


# ----------------------------------------------------------------------------
# WEB-33 — instant_double_stutter (Crossfader hip-hop)
# ----------------------------------------------------------------------------

def instant_double_stutter(a, b, sr, bar_s, stutter_bars=2):
    """One track doubled against itself at a half-beat offset,
    crossfader-spliced every half beat, then B drops.

    Crossfader's instant doubles: the same track on both
    channels, "at the same tempo and with the same amount of
    volume gain, but with a half-beat delay. The crossfader is
    now used to splice between the channels creating some
    interesting patterns and also giving a nice stutter effect
    to vocals." The classic execution cuts at every half beat
    — "counting, to the beat, 'one and two and three and
    four.' Cut at every number and also at every 'and'." The
    modern form pairs instant-double loading with beat jump
    (half-beat back pad); DJ Lawrence exits the sequence with
    a brake effect (documented here as a staging — the base's
    default exit is B entering full).

    Rendered: A's final `stutter_bars` bars are replaced by
    the dual-stream splice. With the two streams S1(t) = a(t)
    and S2(t) = a(t - half_beat), alternating every half beat
    starting on S1, each even half-beat slice sounds twice and
    each odd slice is skipped: [R0, R0, R2, R2, ...]. The
    doubling, not a reordering, is the effect — every beat
    repeats against itself. Then B enters full.

    Why it is not its neighbours: not T-019
    `stutter_transition` (B's iconic WORD re-triggered in
    accelerating taps — here one track stutters against
    ITSELF, no second track involved until the drop); not
    T-031 `loop_juggle_replace` (groove stolen hit by hit
    between TWO bars — here the source is one track doubled);
    not WEB-08 `beatslicer_shuffle` (one stream's slices
    PERMUTED — here two streams alternate, repeating rather
    than reordering).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bar_s : seconds per bar.
    stutter_bars : stuttered region at A's end in bars
        (default 2; 1-bar and 4-bar stagings).

    Returns a mono float64 mix of len(a) + len(b).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    hb = max(1, bar_n // 8)  # half a beat: bar = 4 beats
    n = stutter_bars * bar_n
    if len(a) < n:
        n = (len(a) // hb) * hb
    head, region = a[:-n], a[len(a) - n:]
    out_region = np.zeros(n)
    for i in range(n // hb):
        src = i if i % 2 == 0 else i - 1
        out_region[i * hb:(i + 1) * hb] = region[src * hb:(src + 1) * hb]
    guard = max(1, int(0.003 * sr))
    out = _join(np.concatenate([head, out_region]), b, guard)
    return out


META = {
    "breakdown_swap": {
        "title": "Breakdown Swap (Beat Entry Under Open Space)",
        "bank": "WEB-30", "family": "STRUCT", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 3.0, "camelot_max": 2,
                     "vocal_ok": ["a_only", "neither"],
                     "phrase_a_ok": ["breakdown"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": ["a_breakdown"]},
        "prefers": [
            {"when": "camelot<=1", "weight": 3,
             "reason": "both tracks' melodic elements are audible "
                       "through the window — high harmonic "
                       "compatibility is the premium case"},
            {"when": "energy_delta_abs<=1", "weight": 2,
             "reason": "matched energy — the swap rewards "
                       "preparation, not rescue"},
            {"when": "b_intro_bars>=8", "weight": 1,
             "reason": "B has a full intro whose beat can "
                       "establish under the breakdown"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "seamless", "clash_risk": "key",
        "params": {
            "swap_bars": {"type": "int", "range": [8, 16],
                          "default": 8, "unit": "bars",
                          "presets": {"8bar": 8, "16bar": 16}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Mixgraph, 'DJ Transition Techniques: 7 Ways to "
                    "Mix Between Tracks' — the breakdown swap: "
                    "A enters a breakdown, B's beat enters "
                    "underneath, the transition completes when "
                    "the breakdown resolves; needs at least "
                    "8 bars of open space",
             "url": "https://www.mixgraph.io/learn/dj-transition-techniques",
             "date": "2026-10-24"},
        ],
        "composed_of": [],
    },
    "echo_out_reset": {
        "title": "Echo Out Reset (Metronome Reset, Any-BPM Drop)",
        "bank": "WEB-31", "family": "COMP", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["build", "chorus", "outro"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "genre_pair==leap", "weight": 3,
             "reason": "the reset exists for leaps — the tail "
                       "erases the old tempo before B drops"},
            {"when": "bpm_delta_pct>=10", "weight": 2,
             "reason": "large tempo gaps are where long blends "
                       "fail and the reset earns its place"},
            {"when": "phrase_a==build", "weight": 1,
             "reason": "climax-of-buildup placement is the "
                       "source's best structural position"},
        ],
        "energy": {"delta": 0, "tension": "release"},
        "exit": "tail", "clash_risk": "none",
        "params": {
            "tail_bars": {"type": "int", "range": [1, 4],
                          "default": 2, "unit": "bars",
                          "presets": {"1bar": 1, "2bar": 2,
                                      "4bar": 4}},
            "beat_div": {"type": "float", "range": [0.25, 1.0],
                         "default": 0.5, "unit": "beats",
                         "presets": {"half": 0.5, "dotted": 0.75}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "PulseDJ blog, 'Ultimate Open Format DJing "
                    "Guide' — Echo Out Reset: heavy 1/2- or "
                    "3/4-beat echo, fader pulled down, tail "
                    "resets the room's internal metronome, "
                    "new track drops at any BPM on the next "
                    "clean downbeat",
             "url": "https://blog.pulsedj.com/open-format-djing",
             "date": "2026-10-24"},
        ],
        "composed_of": ["echo_out", "hard_cut"],
    },
    "bed_tempo_switch": {
        "title": "Bed Tempo Switch (Ambient Third-Deck Cover)",
        "bank": "WEB-32", "family": "STRUCT", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "verse", "chorus",
                                      "breakdown", "build"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": ["third_deck"]},
        "prefers": [
            {"when": "genre_pair==leap", "weight": 3,
             "reason": "the bed covers leaps the ramp cannot "
                       "— no tempo reference sounds during "
                       "the switch"},
            {"when": "bpm_delta_pct>=10", "weight": 2,
             "reason": "large tempo gaps are the bed's home "
                       "ground, not the ramp's"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "seamless", "clash_risk": "none",
        "params": {
            "bed_bars": {"type": "int", "range": [2, 8],
                         "default": 4, "unit": "bars",
                         "presets": {"2bar": 2, "4bar": 4,
                                     "8bar": 8}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Pioneer DJ blog, 'A complete guide to "
                    "multi-deck mixing' — Djrum: an ambient "
                    "track on a third deck as a transitional "
                    "sound bed for big switches between tempos",
             "url": "https://blog.pioneerdj.com/djtips/a-complete-guide-to-multi-deck-mixing/",
             "date": "2026-10-24"},
            {"type": "tutorial",
             "ref": "DJ.Studio, 'Techno DJ Techniques' — "
                    "ambient / minimal tracks as bridges "
                    "between high-energy tracks (corroboration)",
             "url": "https://dj.studio/blog/dj-techno-music",
             "date": "2026-10-24"},
        ],
        "composed_of": [],
    },
    "instant_double_stutter": {
        "title": "Instant Double Stutter (Half-Beat Dual-Stream Splice)",
        "bank": "WEB-33", "family": "PERF", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 10.0, "camelot_max": 3,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "verse", "chorus", "drop"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": []},
        "prefers": [
            {"when": "iconic_a", "weight": 2,
             "reason": "the stutter effect lands hardest on "
                       "vocals — an iconic A vocal doubles "
                       "against itself"},
            {"when": "energy_delta>=1", "weight": 1,
             "reason": "the stutter builds tension into a "
                       "higher-energy drop"},
        ],
        "energy": {"delta": 1, "tension": "build"},
        "exit": "snap", "clash_risk": "vocal",
        "params": {
            "stutter_bars": {"type": "int", "range": [1, 4],
                             "default": 2, "unit": "bars",
                             "presets": {"1bar": 1, "2bar": 2,
                                         "4bar": 4}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Crossfader, 'How To Mix Hip Hop' — "
                    "instant doubles: same track on both "
                    "channels at a half-beat delay, "
                    "crossfader spliced every half beat "
                    "('one and two and three and four', "
                    "cutting on numbers AND 'ands'), "
                    "stutter effect on vocals; brake exit",
             "url": "https://wearecrossfader.co.uk/blog/how-to-mix-hip-hop/",
             "date": "2026-10-24"},
        ],
        "composed_of": [],
    },
}

TECHNIQUE_FUNCS = {
    "breakdown_swap": breakdown_swap,
    "echo_out_reset": echo_out_reset,
    "bed_tempo_switch": bed_tempo_switch,
    "instant_double_stutter": instant_double_stutter,
}
