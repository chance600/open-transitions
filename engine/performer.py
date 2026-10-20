"""
open-transitions engine — performer lane (PERF gaps + T-035 riser overlay).

Domain module per FRAMEWORK.md §7: functions + META dict + TECHNIQUE_FUNCS
dict. `engine/meta.py` and `engine/render.py` auto-merge this module;
`demos/make_demos.py` auto-merges `demos/ext_performer.py`. Adding this
file is the whole integration — no shared file is edited.

Techniques:
  GAP-14 scratch_in                B's drop beat baby-scratched over A's
                                   last phrase, released on the downbeat
  GAP-15 rhythmic_fader_chops      transformer-style rhythmic fader chops
                                   as the transition gesture itself
  GAP-16 spare_deck_element_firing spare decks 3/4 as an orchestra: an
                                   EQ-blend bed + elements muted/fired
                                   in real time (riser loop, vocal hit)
  T-035  riser_ducking_overlay     the bank's riser ducking & placement
                                   recipe as a renderable overlay
                                   (kind "overlay" — see TECHNIQUE_FUNCS
                                   note at the bottom of this file)

All functions take/return mono float64 numpy arrays (synthesized sketch
audio only). Gains are linear amplitude unless suffixed _db.
"""

import numpy as np

from . import dsp


KILL_DB = -60.0  # "7 o'clock" — effectively silent, avoids denormals


def _db_env_bars(n, bar_s, sr, points, step_points=()):
    """Per-sample dB envelope from (bar, dB) breakpoints.

    Linear interpolation in dB between breakpoints; bars in
    `step_points` jump instantaneously on that bar's first sample
    (a bass swap, not a ramp). Mirrors techniques._db_envelope.
    """
    bars = np.array([p[0] for p in points], dtype=float)
    dbs = np.array([p[1] for p in points], dtype=float)
    t_bars = np.arange(n) / sr / bar_s
    env = np.interp(t_bars, bars, dbs)
    for sb in step_points:
        idx = int(sb * bar_s * sr)
        if 0 <= idx < n:
            post = np.interp(sb + 1e-9, bars, dbs)
            nxt = bars[bars > sb]
            end = int(nxt[0] * bar_s * sr) if len(nxt) else n
            env[idx:end] = post
    return env


def _guard(x, sr, guard_ms=2.0, head=True, tail=True):
    """2 ms raised-cosine click guards at an array's edges (cf. hard_cut)."""
    g = max(1, int(guard_ms / 1000.0 * sr))
    y = np.asarray(x, dtype=np.float64).copy()
    if tail and g < len(y):
        y[-g:] *= 0.5 + 0.5 * np.cos(np.pi * np.linspace(0, 1, g))
    if head and g < len(y):
        y[:g] *= 0.5 - 0.5 * np.cos(np.pi * np.linspace(0, 1, g))
    return y


# ----------------------------------------------------------------------------
# GAP-14 — Scratch-In / Scratch Drop (PERF)
# ----------------------------------------------------------------------------

def scratch_in(a, b, sr, bpm, scratch_beats=1.0):
    """Baby-scratch B's first beat in rhythm over A's last phrase, then
    release it on the downbeat as A hard-cuts.

    Parameters
    ----------
    a : np.ndarray, mono float64
        Outgoing segment. The scratch gesture is mixed over its final
        `scratch_beats` beats (its last phrase); `a` then ends — the
        concatenation with `b` IS the hard cut.
    b : np.ndarray, mono float64
        Incoming segment, STARTING on its drop beat (caller aligns: b[0]
        is the first beat that gets scratched and then released).
    sr : int or float
        Sample rate, Hz.
    bpm : float
        Tempo of the (beatmatched) pair, beats per minute. The scratch
        rhythm is locked to this grid — an off-grid scratch reads as a
        mistake, not a gesture.
    scratch_beats : float, default 1.0, unit: beats
        Length of the scratch gesture. One beat is the classic tease:
        long enough for the crowd to register B's timbre, short enough
        that the release still lands as a drop.

    Render
    ------
    The gesture is B's drop beat resampled forward/backward as two chirps
    (baby scratch: push forward, pull back, twice) via a time-varying
    playback-rate envelope (+2x forward, -2x backward, net displacement
    zero), mixed at -4 dB over A's final beat. On the next downbeat A
    hard-cuts (2 ms click guards only — no fade) and B plays full from
    its drop beat.

    Why it works: the scratch is a timbral trailer — the crowd hears the
    incoming track's first sound as *percussion* before they hear it as
    music, so the release on the 1 feels both surprising and inevitable.
    It is the incoming-side mirror of the backspin (T-007): T-007 winds
    the outgoing track backward; this winds the incoming track forward.
    ADAPT because chirp rate/depth are feel parameters — the 2x chirp at
    one beat is the documented default, not a law.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / bpm
    beat_n = int(beat_s * sr)
    g_n = min(len(a), max(1, int(scratch_beats * beat_s * sr)))

    # --- Scratch gesture: B's drop beat, chirped forward/backward x2 ---
    src = b[:beat_n] if len(b) >= beat_n else np.pad(b, (0, beat_n - len(b)))
    n_chirps = max(1, int(round(2 * scratch_beats)))
    chirp_n = max(2, g_n // n_chirps)
    gesture = np.zeros(g_n)
    for c in range(n_chirps):
        s0 = c * chirp_n
        s1 = min(g_n, s0 + chirp_n)
        m = s1 - s0
        if m < 2:
            break
        half = m // 2
        rate = np.concatenate([np.full(half, 2.0),
                               np.full(m - half, -2.0)])
        seg = dsp.warp_resample(src, sr, rate, out_len=m)
        # per-chirp window: the hand's pressure envelope (attacks read as
        # intent; unwindowed chirps click at every direction change)
        seg = seg * np.sin(np.pi * np.linspace(0, 1, m)) ** 0.5
        gesture[s0:s1] = seg
    # 5 ms edge fades: the gesture must start/stop like a hand, not a gate
    ef = min(int(0.005 * sr), g_n // 2)
    if ef > 1:
        gesture[:ef] *= dsp.raised_cosine(ef, up=True)
        gesture[-ef:] *= dsp.raised_cosine(ef, up=False)
    gesture = gesture * dsp.db_to_gain(-4.0)  # sits -4 dB over A

    # --- Assemble: A (+ gesture over its tail), hard cut, B full ---
    a_out = a.copy()
    a_out[len(a) - g_n:] += gesture
    return np.concatenate([_guard(a_out, sr, head=False),
                           _guard(b, sr, tail=False)])


# ----------------------------------------------------------------------------
# GAP-15 — Rhythmic Fader Chops (PERF)
# ----------------------------------------------------------------------------

def rhythmic_fader_chops(a, b, sr, bpm, bar_s, chop_beats=4):
    """Transformer-style rhythmic fader chops as the transition gesture:
    A is chopped in/out on a quarter-beat grid while B fades in
    underneath; A is fully out by bar 5 and B owns the mix.

    Parameters
    ----------
    a : np.ndarray, mono float64
        Outgoing segment, phrase-aligned with `b` (overlapping segments
        of equal length; the shorter is zero-padded to the longer).
    b : np.ndarray, mono float64
        Incoming segment, aligned so b[0] coincides with a[0] — B is
        already playing (cued and beatmatched) when the chops start.
    sr : int or float
        Sample rate, Hz.
    bpm : float
        Tempo of the pair, beats per minute (sets the chop grid).
    bar_s : float
        Seconds per bar (4 beats). Sets the bar-5 deadline for A's exit.
    chop_beats : int, default 4, unit: beats
        Duration of the chop gesture. Four beats (one bar) is the
        statement length: two beats reads as a stutter, eight bars of
        chopping reads as a routine, not a transition.

    Render
    ------
    Beats 0..chop_beats: A's channel fader is gated in/out every
    quarter-beat (16th-note grid, 50% duty, ~3 ms smoothed edges — hard
    digital edges click; a real transformer's edges are fast but never
    instantaneous). B fades in underneath over the same span
    (0.35 -> 0.75 gain), so A's off-phases are never silence — the
    groove's floor transfers before its identity does. After the chops,
    A fades out on a cosine curve reaching zero at bar 5 (sample
    4 * bar_s * sr), while B completes its fade to unity; past bar 5
    the mix is B alone. If the segments end before bar 5, A's fade
    compresses to the remaining length (it still ends at zero).

    Why it works: the chop turns the crossfader itself into a rhythm
    instrument — the crowd hears the *mix* being performed, and the
    rhythmic holes in A are exactly where B's groove pokes through, so
    by the time A leaves, B has already been the groove for a bar.
    Unlike T-030's single committed cut, the gesture is the repetition:
    each chop is a downbeat-level reminder that a handover is happening.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n = max(len(a), len(b))
    if len(a) < n:
        a = np.pad(a, (0, n - len(a)))
    if len(b) < n:
        b = np.pad(b, (0, n - len(b)))
    beat_s = 60.0 / bpm
    beat_n = max(1, int(beat_s * sr))

    # --- Chop gate: quarter-beat period, 50% duty, ~3 ms smoothed ---
    chop_n = min(n, int(chop_beats * beat_s * sr))
    period = max(2, beat_n // 4)
    phase = (np.arange(chop_n) % period) / period
    gate = (phase < 0.5).astype(np.float64)
    sm = max(1, int(0.003 * sr))
    if sm > 1:
        kernel = np.ones(sm) / sm
        gate = np.convolve(np.pad(gate, (sm, sm), mode="edge"),
                           kernel, mode="same")[sm:-sm]

    # --- A envelope: chopped, then cosine out to zero by bar 5 ---
    a_env = np.ones(n)
    a_env[:chop_n] = gate
    bar5 = int(4 * bar_s * sr)  # first sample of bar 5
    fade_end = min(n, max(bar5, chop_n))
    if fade_end > chop_n:
        m = fade_end - chop_n
        a_env[chop_n:fade_end] = np.cos(
            0.5 * np.pi * np.linspace(0, 1, m))
    if fade_end < n:
        a_env[fade_end:] = 0.0

    # --- B envelope: rises under the chops, unity by bar 5 ---
    b_env = np.ones(n)
    if chop_n > 0:
        b_env[:chop_n] = np.linspace(0.35, 0.75, chop_n)
    if fade_end > chop_n:
        m = fade_end - chop_n
        b_env[chop_n:fade_end] = np.linspace(0.75, 1.0, m)
    if chop_n >= n:
        b_env[:] = np.linspace(0.35, 0.75, n)

    return a * a_env + b * b_env


# ----------------------------------------------------------------------------
# GAP-16 — Spare-Deck Element Firing (ROUTING)
# ----------------------------------------------------------------------------

def _synth_vocal_oneshot(n, sr, f0=220.0, level_db=-8.0):
    """Synthesized vocal one-shot ('yeah!'-class hit): a formant-ish
    harmonic stack with a pitch settle (220 -> 180 Hz) and a two-stage
    syllable pump, peak-normalized to level_db. Deterministic sketch
    material standing in for a sampler-fired vocal hit."""
    t = np.arange(n) / sr
    dur = max(n / sr, 1e-3)
    f = f0 * (180.0 / f0) ** (t / dur)  # settle down into the hit
    phase = 2 * np.pi * np.cumsum(f) / sr
    harm = np.zeros(n)
    for h, amp in [(1, 1.0), (2, 0.55), (3, 0.32), (4, 0.18), (5, 0.1)]:
        harm += amp * np.sin(h * phase)
    env = np.exp(-t * 5.0) * (0.7 + 0.3 * np.sin(np.pi * np.clip(t / dur, 0, 1)))
    y = harm * env
    peak = np.max(np.abs(y)) + 1e-12
    return y / peak * dsp.db_to_gain(level_db)


def spare_deck_element_firing(a, b, sr, bar_s, bpm):
    """Spare-deck bank fired like orchestra sections over an EQ-blend
    bed: elements sit muted on decks 3/4 and are fired in real time.

    Parameters
    ----------
    a : np.ndarray, mono float64
        Outgoing primary (deck 1). Truncated/zero-padded to the
        16-bar bed.
    b : np.ndarray, mono float64
        Incoming primary (deck 2), phrase-aligned with `a`. Same
        16-bar treatment.
    sr : int or float
        Sample rate, Hz.
    bar_s : float
        Seconds per bar (4 beats). All fire points are bar-indexed.
    bpm : float
        Tempo of the pair, beats per minute (the riser element's
        ducking follows this grid).

    Render (the firing schedule — muted means exactly zero gain)
    -------------------------------------------------------------
    Bed (bars 1-16): a staged 3-band EQ blend — B's highs open over
    bars 1-4, mids over bars 5-8, the bass swap lands as a step on
    bar 9's downbeat, and A's remaining bands + fader are gone by
    bar 15. Deck 1 owns the lows until the swap; deck 2 after it.
    Element 1 (bar 8): a synthesized riser loop is FIRED on deck 3 —
    silent for bars 1-7, then a 4-bar riser (HP-swept noise + rising
    tone via dsp.synth_riser, peaking -14 dB, lightly ducked 2 dB to
    the kick grid for its first 2 bars) carries bars 8-11 and is cut
    dead on bar 12's downbeat.
    Element 2 (bar 12): a synthesized vocal one-shot is FIRED on
    deck 4 — a single formant hit (2 beats with decay tail, peaking
    -8 dB) exactly where the riser dies, marking the new section the
    way a conductor cues the brass.

    Why it works: T-020's third deck carries ONE continuous glue layer;
    a spare-deck *bank* is a different instrument — discrete elements
    with entrances, like orchestra sections. The bed guarantees the
    groove never dips (the blend is always running underneath), while
    the fired elements supply the events: the riser manufactures
    tension the bed can't, and the one-shot punctuates the section
    change so the crowd hears the firing as arrangement, not mixing.
    Frequency discipline keeps it clean: the riser is high-passed by
    construction (never fights the bed's kick), and the one-shot lives
    in the vocal band the bed's EQ swap has just vacated.
    ADAPT because WHICH elements to fire (and whether the room wants
    them) is curatorial — the schedule and rendering are deterministic.
    """
    bed_bars = 16
    n = int(bed_bars * bar_s * sr)
    a = np.asarray(a, dtype=np.float64)[:n]
    b = np.asarray(b, dtype=np.float64)[:n]
    if len(a) < n:
        a = np.pad(a, (0, n - len(a)))
    if len(b) < n:
        b = np.pad(b, (0, n - len(b)))
    bar_n = int(bar_s * sr)

    # --- Bed: staged EQ blend, bass swap as a step on bar 9 (index 8) ---
    swap = 8.0
    b_hi = _db_env_bars(n, bar_s, sr,
                        [(0, KILL_DB), (4, 0.0), (bed_bars, 0.0)])
    b_mid = _db_env_bars(n, bar_s, sr,
                         [(0, KILL_DB), (4, KILL_DB), (8, 0.0),
                          (bed_bars, 0.0)])
    b_lo = _db_env_bars(n, bar_s, sr,
                        [(0, KILL_DB), (swap, KILL_DB), (bed_bars, 0.0)],
                        step_points={swap})
    a_hi = _db_env_bars(n, bar_s, sr,
                        [(0, 0.0), (4, -8.0), (12, KILL_DB),
                         (bed_bars, KILL_DB)])
    a_mid = _db_env_bars(n, bar_s, sr,
                         [(0, 0.0), (8, -8.0), (12, KILL_DB),
                          (bed_bars, KILL_DB)])
    a_lo = _db_env_bars(n, bar_s, sr,
                        [(0, 0.0), (swap, 0.0), (bed_bars, KILL_DB)],
                        step_points={swap})
    # fix the stepped bands past the swap (interp resumes from the
    # post-step breakpoint; pin them explicitly, as in eq_blend)
    idx_swap = int(swap * bar_s * sr)
    b_lo[idx_swap:] = 0.0
    a_lo[idx_swap:] = KILL_DB
    a_master = np.ones(n)
    f0, f1 = idx_swap, int(14 * bar_s * sr)
    if f1 > f0:
        a_master[f0:f1] = np.cos(0.5 * np.pi * np.linspace(0, 1, f1 - f0))
        a_master[f1:] = 0.0

    bed = (dsp.apply_3band_eq(a, sr, a_lo, a_mid, a_hi) * a_master
           + dsp.apply_3band_eq(b, sr, b_lo, b_mid, b_hi))

    # --- Element 1: riser loop fired at bar 8 (1-indexed: starts after
    # 7 full bars). It spans bars 8-11 — its final bar rides the swapped
    # bed (bass swap on bar 9) — and is cut dead on bar 12's downbeat,
    # where the one-shot fires.
    riser_start = 7 * bar_n
    riser_n = 4 * bar_n
    riser = dsp.synth_riser(riser_n, sr, level_db=-14.0,
                            duck_bpm=bpm, duck_db=2.0, duck_bars=2,
                            bar_s=bar_s)
    bed[riser_start:riser_start + riser_n] += riser

    # --- Element 2: vocal one-shot fired at bar 12 (index 11) ---
    shot_start = 11 * bar_n
    shot_n = int(2 * (60.0 / bpm) * sr)  # 2 beats incl. decay tail
    shot = _synth_vocal_oneshot(shot_n, sr)
    bed[shot_start:shot_start + shot_n] += shot
    return bed


# ----------------------------------------------------------------------------
# T-035 — Riser Ducking & Placement (SYNTH, kind "overlay")
# ----------------------------------------------------------------------------

def _synth_downlifter(n, sr, level_db=-7.0):
    """Downlifter / reverse-crash cover: noise swept DOWN 12 kHz ->
    400 Hz plus a falling tone (880 -> 110 Hz) under a fast-attack
    exponential decay. Fills beats 1-2 of the drop bar, covering the
    riser's absence after its hard cut (bank T-035 exit rule).
    Deterministic sketch material."""
    rng = np.random.default_rng(9)
    t = np.arange(n) / sr
    dur = max(n / sr, 1e-3)
    sweep = 1.0 - (1.0 - np.exp(-3.0 * t / dur)) / (1.0 - np.exp(-3.0))
    cut = 400.0 * (12000.0 / 400.0) ** sweep
    noise = dsp.sweep_filter(rng.standard_normal(n), sr, cut,
                             ftype="lowpass", block=2048)
    phase = 2 * np.pi * np.cumsum(
        880.0 * (110.0 / 880.0) ** (t / dur)) / sr
    tone = np.sin(phase)
    env = np.exp(-t * 4.0)
    y = (noise / (np.max(np.abs(noise)) + 1e-9) * 0.7
         + tone * 0.4) * env
    peak = np.max(np.abs(y)) + 1e-12
    return y / peak * dsp.db_to_gain(level_db)


def riser_ducking_overlay(x, sr, bar_s, bpm, pre_drop_bars=8):
    """The bank's T-035 ducking recipe as a renderable overlay: a riser
    ducked into the kick's gaps over the final phrase, hard-cut on the
    drop's Beat 1, with a downlifter covering the drop's first 2 beats.

    This is the first parameterized software recipe for T-035 — the bank
    entry itself notes that no DJ tutorial documents riser ducking; the
    parameters below ARE the bank's spec, made executable.

    Parameters
    ----------
    x : np.ndarray, mono float64
        The mix segment the riser rides over. It must END exactly on
        the drop's Beat 1 (caller aligns: x's last sample is the final
        sample before the drop). The riser occupies the last
        `pre_drop_bars` bars of `x` (or all of `x` if shorter).
    sr : int or float
        Sample rate, Hz.
    bar_s : float
        Seconds per bar (4 beats). Sets the placement grid.
    bpm : float
        Tempo, beats per minute. The ducking follows the kick grid at
        this tempo (one dip per beat, i.e. per kick in 4/4).
    pre_drop_bars : int, default 8, unit: bars
        Riser length. T-035 placement rule: start on Bar 1 of the FINAL
        8-bar phrase before the transition — never earlier (a 16-bar
        riser exhausts the crowd).

    Render (the T-035 recipe, parameter for parameter)
    ---------------------------------------------------
    - Placement: riser starts Bar 1 of the final `pre_drop_bars`-bar
      phrase, peaks at the last beat, ENDS on the drop's Beat 1 — it
      never overlaps the drop.
    - Level: the riser peaks -6 dB UNDER the mix (measured from x's
      own peak: riser_level_db = mix_peak_db - 6 dB).
    - Ducking: sidechain-style pumping at 4:1 character, rendered as
      3 dB dips on every kick hit (5 ms attack, 100 ms release) for
      bars 1-4 only — the bank's manual-method window; in bars 5-8 the
      riser rises un-dipped as the arrangement strips back (the dsp
      synth's duck_bars=4).
    - Filters: high-pass 200 Hz (never fights the kick's sub),
      low-pass 12 kHz (leaves air for the drop's crash).
    - Exit: the riser is hard-cut at x's final sample (the drop's
      Beat 1). A synthesized downlifter (reverse crash) is APPENDED as
      a 2-beat tail: it is the cover for beats 1-2 of the drop bar, and
      the caller overlaps it onto the drop (the demo does exactly
      this) — sequentially auditioned, it reads as the crash decay
      that masks the cut.

    Why it works: a riser is broadband energy competing with the track.
    Ducking carves it into the kick's gaps (rhythmic slotting), so it
    breathes inside the groove instead of sitting on top; the -6 dB
    ceiling keeps it subliminal until the final bars, when the
    arrangement strips back and the riser becomes the track. The hard
    cut + downlifter exit gives the drop its full frequency space
    while masking the riser's absence. This is an overlay (FRAMEWORK
    §6): it decorates a base render rather than handing over between
    two tracks, which is why its signature takes a single segment.
    """
    x = np.asarray(x, dtype=np.float64)
    n = len(x)
    riser_n = min(n, int(pre_drop_bars * bar_s * sr))
    start = n - riser_n

    peak = float(np.max(np.abs(x))) if n else 0.0
    mix_peak_db = float(dsp.gain_to_db(peak)) if peak > 1e-12 else -1.0
    riser_level_db = mix_peak_db - 6.0  # T-035: -6 dB under the mix bus

    riser = dsp.synth_riser(riser_n, sr, level_db=riser_level_db,
                            duck_bpm=bpm, duck_db=3.0, duck_bars=4,
                            bar_s=bar_s, hp_hz=200.0, lp_hz=12000.0)
    out = x.copy()
    out[start:] += riser  # hard cut: the riser array ends at the drop

    beat_s = 60.0 / bpm
    down = _synth_downlifter(int(2 * beat_s * sr), sr,
                              level_db=riser_level_db)
    return np.concatenate([out, down])


# ----------------------------------------------------------------------------
# Registry (FRAMEWORK.md §3) — merged by engine/meta.py all_meta()
# ----------------------------------------------------------------------------

META = {
    # ---------------------------------------------------------------- GAP-14
    "scratch_in": {
        "title": "Scratch-In / Scratch Drop",
        "bank": "GAP-14", "family": "PERF", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 5.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "chorus", "drop", "build"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "genre_pair==leap", "weight": 2,
             "reason": "open-format staple — the scratch owns the leap"},
            {"when": "energy_delta>=1", "weight": 2,
             "reason": "the release lands harder into a hotter B"},
        ],
        "energy": {"delta": 1, "tension": "build"},
        "exit": "snap", "clash_risk": "none",
        "params": {"scratch_beats": {"type": "float", "range": [0.5, 2.0],
                                     "default": 1.0, "unit": "beats",
                                     "presets": {"half": 0.5, "one": 1.0,
                                                 "two": 2.0}}},
        "evidence": [
            {"type": "tutorial",
             "ref": "Transition Gap Report 2026-10-19, GAP-14 — open-format scratch-in / scratch drop (open-format toolkits; the library's only prior turntablist move was the outgoing-side backspin, T-007)",
             "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    # ---------------------------------------------------------------- GAP-15
    "rhythmic_fader_chops": {
        "title": "Rhythmic Fader Chops (Transformer)",
        "bank": "GAP-15", "family": "PERF", "kind": "render",
        "verdict": "ADOPT", "confidence": "high",
        "requires": {"bpm_delta_pct_max": 5.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "build", "chorus", "drop"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta>=1", "weight": 2,
             "reason": "each chop is a downbeat-level handover reminder"},
            {"when": "genre_pair==leap", "weight": 1,
             "reason": "the performed gesture carries a contrast move"},
        ],
        "energy": {"delta": 1, "tension": "build"},
        "exit": "snap", "clash_risk": "none",
        "params": {"chop_beats": {"type": "int", "range": [2, 8],
                                  "default": 4, "unit": "beats",
                                  "presets": {"2beat": 2, "4beat": 4,
                                              "8beat": 8}}},
        "evidence": [
            {"type": "tutorial",
             "ref": "Transition Gap Report 2026-10-19, GAP-15 — rhythmic fader chops, transformer-style (James Hype / stems-first method + open-format toolkits)",
             "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    # ---------------------------------------------------------------- GAP-16
    "spare_deck_element_firing": {
        "title": "Spare-Deck Element Firing",
        "bank": "GAP-16", "family": "ROUTING", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 3.0, "camelot_max": 3,
                     "vocal_ok": ["a_only", "b_only", "neither"],
                     "phrase_a_ok": ["outro", "build", "chorus"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": ["third_deck"]},
        "prefers": [
            {"when": "energy_delta_abs<=1", "weight": 2,
             "reason": "the bed never dips — fired elements supply the events"},
            {"when": "energy_delta>=1", "weight": 1,
             "reason": "riser + one-shot punctuate the lift into B"},
        ],
        "energy": {"delta": 1, "tension": "build"},
        "exit": "seamless", "clash_risk": "bass",
        "params": {},
        "evidence": [
            {"type": "set",
             "ref": "Transition Gap Report 2026-10-19, GAP-16 — spare-deck element firing (James Hype: decks 3/4 hold fireable loops, samples, acapellas, muted/fired like orchestra sections)",
             "url": None, "date": "2026-10-19"},
        ],
        "composed_of": ["eq_blend"],
    },
    # ----------------------------------------------------------------- T-035
    "riser_ducking_overlay": {
        "title": "Riser Ducking & Placement (Overlay)",
        "bank": "T-035", "family": "SYNTH", "kind": "overlay",
        "verdict": "ADOPT", "confidence": "high",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["build", "outro", "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "phrase_a==build", "weight": 3,
             "reason": "the final 8-bar phrase is the riser's home"},
            {"when": "energy_delta>=1", "weight": 2,
             "reason": "the ducked riser manufactures the lift into the drop"},
        ],
        "energy": {"delta": 1, "tension": "build"},
        "exit": "snap", "clash_risk": "none",
        "params": {"pre_drop_bars": {"type": "int", "range": [4, 16],
                                     "default": 8, "unit": "bars",
                                     "presets": {"4bar": 4, "8bar": 8,
                                                 "16bar": 16}}},
        "evidence": [
            {"type": "tutorial",
             "ref": "Technique bank T-035 — Riser Ducking & Placement: derived from production sidechain practice (MusicRadar 'Sidechains'); no DJ tutorial documents riser ducking — the bank entry is the first written recipe, and this function is its first parameterized software recipe",
             "url": None, "date": None},
        ],
        "composed_of": [],
    },
}


# TECHNIQUE_FUNCS exports ONLY fn(a, b, sr, **kwargs)-compatible pair
# renders (the engine/render.py plan-file contract):
#   - scratch_in, rhythmic_fader_chops: pair renders by construction.
#   - spare_deck_element_firing: honestly (a, b, sr)-compatible — its
#     spare-deck elements are SYNTHESIZED in-function (riser loop +
#     vocal one-shot), so no third audio argument exists to pass; the
#     plan renderer injects bar_s/bpm as it does for core techniques.
#   - riser_ducking_overlay is EXCLUDED: it is a kind="overlay"
#     decoration over a SINGLE segment, signature (x, sr, bar_s, bpm),
#     not a two-track handover. It is registered in META and demoed via
#     demos/ext_performer.py; chains apply it per FRAMEWORK.md §6.
TECHNIQUE_FUNCS = {
    "scratch_in": scratch_in,
    "rhythmic_fader_chops": rhythmic_fader_chops,
    "spare_deck_element_firing": spare_deck_element_firing,
}
