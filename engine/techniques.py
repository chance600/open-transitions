"""
open-transitions engine — named DJ transition techniques.

Each technique is a function taking the outgoing segment `a` and the incoming
segment `b` (float mono arrays) plus timing, and returning the rendered
transition audio. Names follow the technique bank (techniques/ or TECHNIQUES.md):

  T-001 eq_blend        3-band EQ frequency-replacement blend
  T-002 bass_swap       (used inside eq_blend; also standalone)
  T-003 filter_sweep    HPF/LPF opposing sweep transition
  T-004 echo_out        echo throw + drop on the 1
  T-004b echo_out_blend echo throw with incoming emerging under the tail
  T-004c layered_emergence stacked transition (thinning + riser + echo + wash)
  T-005 reverb_wash     dissolve outgoing into reverb, incoming emerges
  T-006 brake_stop      vinyl brake / tape stop into the drop
  T-007 backspin        spinback rewind, slam on the downbeat
  T-008 loop_roll_build 1/2 -> 1/16 roll build with HPF thinning
  T-010 acapella_overlay vocal over instrumental (EQ preset + overlay)
  T-013 power_down      pitch-fader drag to zero (manual, longer than brake)
  T-014 hotcue_drop_swap replace A's drop with B's over the run-up
  T-015 harmonic_mix    Camelot compatibility decision function
  T-017 layered_fx_stack echo + HPF + reverb stacked on the outgoing
  T-018 noise_echo_buildup empty-channel noise riser with 1/2-beat echo
  T-019 stutter_transition hot-cue vocal stutter taps, then release
  T-021 tempo_bridge    BPM ramp (phase-vocoder) or half/double shift
  T-022 drum_bridge     strip to drums (key-neutral zone), blend B in
  T-023 breakdown_transition whole transition inside A's breakdown
  T-024 double_drop     two builds, one downbeat, one sub-bass
  T-025 vocal_punchline_snap low-kill -> vocal isolate -> void -> drop
  T-026 genre_bridge    pivot genres on a looping vocal anchor
  T-027 loop_transition bounded 2-cycle loop handoff + EQ blend
  T-029 fake_drop       build, 2-4 beat void, real drop
  T-030 hard_cut        no blend, no FX — the cut
  T-031 loop_juggle_replace steal the groove hit by hit (The Replace)
  T-033 vocal_chop_build chop-density ladder + band-pass sweep -> drop
  T-034 reverb_freeze   frozen reverb tail, B launches inside it
  T-037 select_technique decision brain: features -> technique + reasons
  T-038 hook_drop_handoff signature vocal hook is the final event; bloom in
  T-039 screwed_treatment chopped & screwed / slowed / 2x-speed treatment
  T-009 build_to_drop dual-build layering: two builds fuse, B drops
  T-011 wordplay   shared-lyric word answered by the incoming track
  T-020 three_deck_layer glue layer: tri-partite frequency slotting
  T-028 beat_jump   phrase-realignment playhead arithmetic (+ renderer)
  T-032 pitch_play  key-shifted vocal overlay (±2 semitones max)
  riser_drop            riser + HP thinning into a tempo-jump drop
                        (composes riser synthesis with a T-004-style drop)

All timing is in bars; bar_s (seconds per bar) comes from the track analysis.
"""

import numpy as np

from . import dsp


KILL_DB = -60.0  # "7 o'clock" — effectively silent, avoids denormals


def _db_envelope(n, bar_s, sr, points, step_points=()):
    """Build a per-sample dB envelope from (bar, db) breakpoints.

    points: list of (bar, db) sorted by bar; linear interp in dB between them.
    step_points: set of bar values where the change is instantaneous (a step
    on that bar's first sample) instead of ramped.
    """
    bars = np.array([p[0] for p in points], dtype=float)
    dbs = np.array([p[1] for p in points], dtype=float)
    t_bars = np.arange(n) / sr / bar_s
    env = np.interp(t_bars, bars, dbs)
    for sb in step_points:
        idx = int(sb * bar_s * sr)
        if 0 <= idx < n:
            # hold the post-step value from idx onward until next breakpoint
            post = np.interp(sb + 1e-9, bars, dbs)
            nxt = bars[bars > sb]
            end = int(nxt[0] * bar_s * sr) if len(nxt) else n
            env[idx:end] = post
    return env


def _master_envelope(n, bar_s, sr, points):
    """Per-sample 0..1 master gain envelope from (bar, gain) breakpoints."""
    bars = np.array([p[0] for p in points], dtype=float)
    gs = np.array([p[1] for p in points], dtype=float)
    t_bars = np.arange(n) / sr / bar_s
    return np.interp(t_bars, bars, gs)


# ----------------------------------------------------------------------------
# T-001 — EQ Blend (3-band frequency replacement)
# ----------------------------------------------------------------------------

def eq_blend(a, b, sr, bar_s, blend_bars=32):
    """Long harmonic EQ blend. a and b should each be blend_bars long.

    Canonical 32-bar shape (breakpoints scale as fractions of blend_bars):
    Bars 1-8:   B high kill->open,  A high 0->-8 dB
    Bars 9-16:  B mid  kill->open,  A mid  0->-8 dB
    Bar 17 beat 1: bass swap (instant)
    Bars 17-24: A highs/mids -> kill, A fader -> 0
    Bars 25+:   B alone
    """
    n = int(blend_bars * bar_s * sr)
    a = np.asarray(a, dtype=np.float64)[:n]
    b = np.asarray(b, dtype=np.float64)[:n]
    if len(a) < n:
        a = np.pad(a, (0, n - len(a)))
    if len(b) < n:
        b = np.pad(b, (0, n - len(b)))

    # Breakpoints are fractions of the blend (the canonical 32-bar shape:
    # hi swap 1-8, mid swap 9-16, bass swap at 17, departure 17-24).
    bb = float(blend_bars)
    B_HI_IN, B_HI_OPEN = bb * 1 / 32, bb * 8 / 32
    B_MID_IN, B_MID_OPEN = bb * 9 / 32, bb * 16 / 32
    SWAP = bb * 17 / 32
    A_OUT = bb * 24 / 32

    # --- B envelopes: starts killed, bands open in stages ---
    b_hi = _db_envelope(n, bar_s, sr, [(0, KILL_DB), (B_HI_IN, KILL_DB),
                                       (B_HI_OPEN, 0.0), (blend_bars, 0.0)])
    b_mid = _db_envelope(n, bar_s, sr, [(0, KILL_DB), (B_MID_IN, KILL_DB),
                                        (B_MID_OPEN, 0.0), (blend_bars, 0.0)])
    b_lo = _db_envelope(n, bar_s, sr, [(0, KILL_DB), (SWAP, KILL_DB)],
                        step_points={SWAP})
    # fix: after step at SWAP, b_lo should be 0 dB
    idx_swap = int(SWAP * bar_s * sr)
    if idx_swap < n:
        b_lo[idx_swap:] = 0.0

    # --- A envelopes: starts open, bands close in stages ---
    a_hi = _db_envelope(n, bar_s, sr, [(0, 0.0), (B_HI_IN, 0.0),
                                       (B_HI_OPEN, -8.0), (SWAP, -8.0),
                                       (A_OUT, KILL_DB), (blend_bars, KILL_DB)])
    a_mid = _db_envelope(n, bar_s, sr, [(0, 0.0), (B_MID_IN, 0.0),
                                        (B_MID_OPEN, -8.0), (SWAP, -8.0),
                                        (A_OUT, KILL_DB), (blend_bars, KILL_DB)])
    a_lo = np.zeros(n)
    a_lo[:idx_swap] = 0.0
    a_lo[idx_swap:] = KILL_DB

    # A master fader: full until the swap, cos-fade out by A_OUT
    a_master = _master_envelope(n, bar_s, sr, [(0, 1.0), (SWAP, 1.0)])
    fstart, fend = idx_swap, int(A_OUT * bar_s * sr)
    if fend > fstart and fstart < n:
        fend = min(fend, n)
        flen = fend - fstart
        a_master[fstart:fend] = np.cos(0.5 * np.pi * np.linspace(0, 1, flen))
    if fend < n:
        a_master[fend:] = 0.0
    elif fstart < n:
        pass  # fade runs to the end of the (short) blend

    a_eq = dsp.apply_3band_eq(a, sr, a_lo, a_mid, a_hi) * a_master
    b_eq = dsp.apply_3band_eq(b, sr, b_lo, b_mid, b_hi)
    return a_eq + b_eq


# ----------------------------------------------------------------------------
# T-002 — Bass swap (standalone; also the bar-17 move inside eq_blend)
# ----------------------------------------------------------------------------

def bass_swap(a, b, sr):
    """Instantaneous low-band handover. a, b equal length; swap at sample 0.

    Caller aligns the arrays so index 0 is the downbeat.
    """
    n = len(a)
    assert len(b) == n
    a_lo, a_mid, a_hi = dsp.split_3band(a, sr)
    b_lo, b_mid, b_hi = dsp.split_3band(b, sr)
    kill = dsp.db_to_gain(KILL_DB)
    return (a_mid + a_hi) * 1.0 + a_lo * kill + b_lo * 1.0 + (b_mid + b_hi) * kill


# ----------------------------------------------------------------------------
# T-003 — Filter sweep transition
# ----------------------------------------------------------------------------

def filter_sweep(a, b, sr, bar_s, tease_bars=8, sweep_bars=7):
    """A thins out under HPF while B opens up; snap B open on the downbeat.

    a: outgoing (tease_bars + sweep_bars + 1 bars). b: incoming, same length,
    pre-filtered to thin top-end during the tease (caller may pass full b;
    the tease HPF is applied here).
    Returns mix of length (tease+sweep+1) bars; B fully open at the drop bar.
    """
    total_bars = tease_bars + sweep_bars + 1
    n = int(total_bars * bar_s * sr)
    a = np.asarray(a, dtype=np.float64)[:n]
    b = np.asarray(b, dtype=np.float64)[:n]
    if len(a) < n:
        a = np.pad(a, (0, n - len(a)))
    if len(b) < n:
        b = np.pad(b, (0, n - len(b)))

    drop = int((tease_bars + sweep_bars) * bar_s * sr)

    # B tease: HPF at ~3kHz until the sweep, then opens to neutral by the drop
    t = np.arange(n) / sr / bar_s
    b_cut = np.where(t < tease_bars, 3000.0,
                     np.where(t < tease_bars + sweep_bars,
                              3000.0 * (20.0 / 3000.0) ** (
                                  (t - tease_bars) / sweep_bars),
                              20.0))
    b_f = dsp.sweep_filter(b, sr, b_cut, ftype="highpass", block=2048)

    # A: neutral through tease, HPF sweep up during sweep_bars, cut at drop
    a_cut = np.where(t < tease_bars, 20.0,
                     np.where(t < tease_bars + sweep_bars,
                              20.0 * (6000.0 / 20.0) ** (
                                  (t - tease_bars) / sweep_bars),
                              6000.0))
    a_f = dsp.sweep_filter(a, sr, a_cut, ftype="highpass", block=2048)
    a_f[drop:] = 0.0
    # B snaps fully open at drop (remove residual tease filtering)
    b_f[drop:] = b[drop:]

    return a_f + b_f


# ----------------------------------------------------------------------------
# T-004 — Echo out
# ----------------------------------------------------------------------------

def echo_out(a, sr, bpm, beat_div=0.5, wet=0.6, feedback=0.55,
             tail_beats=4):
    """Echo throw on the final beat of `a`, post-fader tail.

    - Low EQ killed over the throw beat (avoids boomy rumble).
    - Input gate cuts at the throw (fader to 0); feedback loop rings on.
    - Returns a + tail_beats of pure tail appended.
    """
    a = np.asarray(a, dtype=np.float64)
    n = len(a)
    sr = float(sr)
    beat_s = 60.0 / bpm
    throw_n = int(beat_s * sr)  # last beat is the throw
    throw_start = max(0, n - throw_n)

    # Kill lows over the throw beat
    lo_db = np.zeros(n)
    lo_db[throw_start:] = KILL_DB
    a_eq = dsp.apply_3band_eq(a, sr, lo_db, 0.0, 0.0)

    # Post-fader gate: input stops at throw start
    gate = np.ones(n)
    gate[throw_start:] = 0.0

    delay_s = beat_div * beat_s
    echoed = dsp.feedback_delay(a_eq, sr, delay_s, feedback=feedback,
                                wet=wet, input_gate=gate)

    # Pure tail: keep filtering zeros so the feedback loop decays naturally
    tail_n = int(tail_beats * beat_s * sr)
    d = max(1, int(round(delay_s * sr)))
    b_ = np.zeros(d + 1); b_[0] = 1.0
    a_ = np.zeros(d + 1); a_[0] = 1.0; a_[d] = -feedback
    # re-run with state: easiest is to process [echoed, zeros] in one go
    extended = np.concatenate([a_eq * gate, np.zeros(tail_n)])
    # gate the extension too (zeros anyway)
    tail_full = dsp.feedback_delay(extended, sr, delay_s, feedback=feedback,
                                   wet=wet, input_gate=np.concatenate(
                                       [gate, np.zeros(tail_n)]))
    return tail_full


# ----------------------------------------------------------------------------
# T-005 — Reverb wash
# ----------------------------------------------------------------------------

def reverb_wash(a, b, sr, bar_s, wash_start_bar=4, b_start_bar=6,
                wet_max=0.7):
    """Dissolve `a` into reverb from wash_start_bar; `b` emerges at b_start_bar.

    a: outgoing segment (bars). b: incoming segment, aligned so its bar 0
    coincides with a's b_start_bar.
    """
    a = np.asarray(a, dtype=np.float64)
    n_a = len(a)
    b = np.asarray(b, dtype=np.float64)

    wash_start = int(wash_start_bar * bar_s * sr)
    b_start = int(b_start_bar * bar_s * sr)

    # Wet ramp on A: 0 -> wet_max over the wash
    wet_env = np.zeros(n_a)
    wlen = max(1, n_a - wash_start)
    wet_env[wash_start:] = wet_max * dsp.raised_cosine(wlen, up=True)

    # Low EQ kill on A from wash start (mandatory: no sub mud)
    lo_db = np.zeros(n_a)
    lo_db[wash_start:] = KILL_DB

    # A fader: full until wash start, fades to 0 by end
    a_master = np.ones(n_a)
    a_master[wash_start:] = 1.0 - dsp.raised_cosine(wlen, up=True)

    # Time-varying wet is approximated block-wise: split A into dry/wet parts.
    # wet reverb of whole A, then crossfade dry->wet along wet_env.
    a_eq = dsp.apply_3band_eq(a, sr, lo_db, 0.0, 0.0)
    a_wet = dsp.schroeder_reverb(a_eq, sr, wet=1.0)
    # per-sample blend: out = (1-w)*dry + w*wet
    w = wet_env
    a_out = (1 - w) * a_eq + w * a_wet
    a_out = a_out * a_master

    # B: gentle 2-bar fade in from its start point
    b_in = np.ones(len(b))
    fin = int(min(len(b), 2 * bar_s * sr))
    b_in[:fin] = dsp.raised_cosine(fin, up=True)

    total_n = max(n_a, b_start + len(b))
    mix = np.zeros(total_n)
    mix[:n_a] += a_out
    mix[b_start:b_start + len(b)] += b * b_in
    return mix


# ----------------------------------------------------------------------------
# T-004b — Echo out + filtered blend-in (emergence variant)
# ----------------------------------------------------------------------------

def echo_out_blend(a, b, sr, bpm, bar_s, beat_div=0.5, wet=0.65,
                   feedback=0.62, throw_beats=1, tail_beats=12,
                   hp_start_hz=200.0, hp_open_bars=8, xfade_bars=16,
                   diffuse_tail=True, diffuse_wet=0.7, diffuse_decay=1.2):
    """Echo throw on outgoing, incoming EMERGES under the tail (no hard drop).

    v2 of the Anchor Point -> Wings transition (user verdict: the v1 drop on
    the 1 was too abrupt — Wings opens at peak with no intro, so slamming in
    reads as a cut, not a blend).

    - Outgoing: same T-004 throw as echo_out (lows killed over the throw
      beat(s), dry gated at the throw, feedback tail rings for tail_beats).
    - The tail is diffused (Schroeder reverb, post-throw region only): a raw
      feedback tail is a pulse train with deep inter-echo nulls, which reads
      as gating under the emerging track. Diffusion melts it into a continuous
      dubby wash — the bed Wings rises out of.
    - Incoming: starts AT the throw, under the tail, with a high-pass at
      hp_start_hz opening exponentially to 20 Hz over hp_open_bars, and an
      equal-power fade-in over xfade_bars.
    - Crossfade: equal-power — outgoing side is cos(0.5*pi*u), incoming side
      is sin(0.5*pi*u), both over xfade_bars from the throw. The outgoing
      tail's natural feedback decay dominates the first ~2 bars; the slow
      cos fade just guarantees no residual tail past the blend.

    Returns the full mix; b starts at the throw point (overlapping the tail).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n_a = len(a)
    n_b = len(b)
    beat_s = 60.0 / bpm
    throw_n = int(throw_beats * beat_s * sr)
    throw_start = max(0, n_a - throw_n)

    # --- Outgoing: echo throw (T-004 mechanics) ---
    lo_db = np.zeros(n_a)
    lo_db[throw_start:] = KILL_DB
    a_eq = dsp.apply_3band_eq(a, sr, lo_db, 0.0, 0.0)
    gate = np.ones(n_a)
    gate[throw_start:] = 0.0
    delay_s = beat_div * beat_s
    tail_n = int(tail_beats * beat_s * sr)
    extended = np.concatenate([a_eq * gate, np.zeros(tail_n)])
    in_gate = np.concatenate([gate, np.zeros(tail_n)])
    echoed = dsp.feedback_delay(extended, sr, delay_s, feedback=feedback,
                                wet=wet, input_gate=in_gate)

    # Diffuse the post-throw tail into a continuous wash (fills the deep
    # inter-echo nulls of the raw pulse train). Dry Anchor stays clean;
    # 1-beat raised-cosine crossfade hides the timbral seam at the throw.
    if diffuse_tail:
        tail_region = echoed[throw_start:].copy()
        washed = dsp.schroeder_reverb(tail_region, sr, wet=diffuse_wet,
                                      decay=diffuse_decay)
        xf = min(int(beat_s * sr), len(tail_region))
        w = dsp.raised_cosine(xf, up=True)
        tail_region[:xf] = ((1.0 - w) * tail_region[:xf] + w * washed[:xf])
        tail_region[xf:] = washed[xf:]
        echoed = np.concatenate([echoed[:throw_start], tail_region])

    # Outgoing crossfade side: full until throw, equal-power cos out
    n_e = len(echoed)
    xf_n = int(xfade_bars * bar_s * sr)
    a_env = np.ones(n_e)
    xf_end = min(n_e, throw_start + xf_n)
    if xf_end > throw_start:
        u = np.linspace(0.0, 1.0, xf_end - throw_start)
        a_env[throw_start:xf_end] = np.cos(0.5 * np.pi * u)
        a_env[xf_end:] = 0.0
    a_out = echoed * a_env

    # --- Incoming: HP opens hp_start_hz -> 20 Hz over hp_open_bars ---
    t_bars = np.arange(n_b) / sr / bar_s
    cut = np.full(n_b, 20.0)
    ramp_n = min(int(hp_open_bars * bar_s * sr), n_b)
    if ramp_n > 0:
        k = np.linspace(0.0, 1.0, ramp_n)
        cut[:ramp_n] = hp_start_hz * (20.0 / hp_start_hz) ** k
    b_hp = dsp.sweep_filter(b, sr, cut, ftype="highpass", block=2048)

    # Incoming crossfade side: equal-power sin in over xfade_bars
    b_env = np.zeros(n_b)
    bf = min(xf_n, n_b)
    if bf > 0:
        ub = np.linspace(0.0, 1.0, bf)
        b_env[:bf] = np.sin(0.5 * np.pi * ub)
        b_env[bf:] = 1.0
    b_out = b_hp * b_env

    # --- Assemble: b starts under the tail at the throw ---
    total = max(n_e, throw_start + n_b)
    mix = np.zeros(total)
    mix[:n_e] += a_out
    mix[throw_start:throw_start + n_b] += b_out
    return mix


# ----------------------------------------------------------------------------
# T-004c — Layered emergence (stacked transition)
# ----------------------------------------------------------------------------

def layered_emergence(a, b, sr, bpm, bar_s, beat_div=0.5, wet=0.65,
                      feedback=0.62, throw_beats=1, tail_beats=12,
                      thin_start_hz=30.0, thin_end_hz=1200.0, thin_bars=8,
                      riser_bars=8, riser_db=-16.0,
                      hp_start_hz=120.0, hp_open_bars=8, xfade_bars=16,
                      wash_decay=2.5, wash_bed_db=-18.0):
    """STACKED transition: multiple DJ tricks layered, each in its own
    spectral/temporal slot (v3 of Anchor Point -> Wings).

    User verdicts: v1 (echo-out + drop) "too abrupt"; v2 (echo-out-blend)
    "still a little abrupt, we need more mixing tricks". The directive is
    LAYERING — the way a real DJ stacks moves instead of relying on one.

    OUTGOING (a, e.g. Anchor's 8-bar wind-down):
      1. HPF thinning sweep (thin_start_hz -> thin_end_hz, exponential, over
         thin_bars): subtractive — clears low-mid space so the riser, the
         echo, and the incoming track never fight. The track "lifts off".
      2. Riser underneath (riser_bars, peaks EXACTLY at the throw, cut dead
         on the throw): the vacuum after the riser cut makes the incoming
         track's arrival feel EARNED, not just revealed.
      3. Echo throw on the last beat(s) (T-004: lows killed, dry gated,
         feedback tail) — the rhythmic handoff.
    TAIL (post-throw):
      4. Wash BLOOM (T-005, time-varying): reverb wet ramps 0->1 over
         bloom_bars as the echo pulses decay — the wash GROWS out of the
         pulse train instead of replacing it at a fixed mix.
    INCOMING (b, starts at the throw):
      5. HP opens hp_start_hz -> 20 Hz exponentially over hp_open_bars
         (v2-tuned: 120 Hz keeps body above the silence floor).
      6. Equal-power fade-in over xfade_bars (v2).

    Anti-mush design: trick 1 is subtractive (removes energy); the riser is
    HP-swept noise living in mids/highs; the echo's lows are killed; the
    incoming HP keeps its lows out until the wash has room. Nothing stacks
    in the same band at the same time.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n_a = len(a)
    n_b = len(b)
    beat_s = 60.0 / bpm
    throw_n = int(throw_beats * beat_s * sr)
    throw_start = max(0, n_a - throw_n)

    # --- Layer 1: HPF thinning sweep over the outgoing zone ---
    t_bars_a = np.arange(n_a) / sr / bar_s
    k = np.clip(t_bars_a / thin_bars, 0.0, 1.0)
    cut_thin = thin_start_hz * (thin_end_hz / thin_start_hz) ** k
    a_thin = dsp.sweep_filter(a, sr, cut_thin, ftype="highpass", block=2048)

    # --- Layer 2: riser under the zone, peaking exactly at the throw ---
    riser_n = min(int(riser_bars * bar_s * sr), n_a)
    riser = dsp.synth_riser(riser_n, sr, level_db=riser_db)
    a_layered = a_thin.copy()
    a_layered[n_a - riser_n:] += riser
    # (the riser is cut dead by the gate below — the vacuum is the point)

    # --- Layer 3: echo throw (T-004 mechanics on the layered signal) ---
    lo_db = np.zeros(n_a)
    lo_db[throw_start:] = KILL_DB
    a_eq = dsp.apply_3band_eq(a_layered, sr, lo_db, 0.0, 0.0)
    gate = np.ones(n_a)
    gate[throw_start:] = 0.0
    delay_s = beat_div * beat_s
    tail_n = int(tail_beats * beat_s * sr)
    extended = np.concatenate([a_eq * gate, np.zeros(tail_n)])
    in_gate = np.concatenate([gate, np.zeros(tail_n)])
    echoed = dsp.feedback_delay(extended, sr, delay_s, feedback=feedback,
                                wet=wet, input_gate=in_gate)

    # --- Layer 4: wash BED — reverb excited by the FULL pre-throw signal ---
    # A feedback echo with 1/2-beat delay decays too fast to sustain a
    # 2+ second tail (0.62^19 = -79 dB by 2.3 s), and its inter-pulse nulls
    # line up with Wings' own micro-dynamics dips (a 60 ms hole at ~2.3 s
    # post-throw hit -61.8 dBFS). A real DJ's reverb throw works because the
    # reverb is excited by the full signal BEFORE the fader cuts — so the
    # wash bed is generated from the 2 pre-throw bars at full level, not
    # from the decaying tail. As the echo pulses die, the bed becomes
    # relatively more prominent: perceptual bloom, no crossfade needed.
    # (An earlier bloom-crossfade revision left the nulls exposed; the bed
    # is simpler and strictly more robust.)
    tail = echoed[throw_start:].copy()
    wash_src_bars = 2
    ws_n = int(wash_src_bars * bar_s * sr)
    wash_src = a_eq[max(0, throw_start - ws_n):throw_start]
    if len(wash_src) < ws_n:
        wash_src = np.pad(wash_src, (ws_n - len(wash_src), 0))
    wash_bed = dsp.schroeder_reverb(wash_src, sr, wet=1.0, decay=wash_decay)
    # Bed sits wash_bed_db under the throw transient: glue, not a feature.
    bed_peak = np.max(np.abs(wash_bed)) + 1e-12
    throw_peak = np.max(np.abs(
        a_eq[max(0, throw_start - 1102):throw_start])) + 1e-12
    wash_bed = wash_bed * (throw_peak / bed_peak) * dsp.db_to_gain(wash_bed_db)
    bed_n = min(len(wash_bed), len(tail))
    tail = tail.copy()
    tail[:bed_n] += wash_bed[:bed_n]
    echoed = np.concatenate([echoed[:throw_start], tail])

    # Outgoing crossfade side: full until throw, equal-power cos out
    n_e = len(echoed)
    xf_n = int(xfade_bars * bar_s * sr)
    a_env = np.ones(n_e)
    xf_end = min(n_e, throw_start + xf_n)
    if xf_end > throw_start:
        u = np.linspace(0.0, 1.0, xf_end - throw_start)
        a_env[throw_start:xf_end] = np.cos(0.5 * np.pi * u)
        a_env[xf_end:] = 0.0
    a_out = echoed * a_env

    # --- Layers 5+6: incoming HP open + equal-power fade-in (v2) ---
    t_bars = np.arange(n_b) / sr / bar_s
    cut = np.full(n_b, 20.0)
    ramp_n = min(int(hp_open_bars * bar_s * sr), n_b)
    if ramp_n > 0:
        kk = np.linspace(0.0, 1.0, ramp_n)
        cut[:ramp_n] = hp_start_hz * (20.0 / hp_start_hz) ** kk
    b_hp = dsp.sweep_filter(b, sr, cut, ftype="highpass", block=2048)

    b_env = np.zeros(n_b)
    bf = min(xf_n, n_b)
    if bf > 0:
        ub = np.linspace(0.0, 1.0, bf)
        b_env[:bf] = np.sin(0.5 * np.pi * ub)
        b_env[bf:] = 1.0
    b_out = b_hp * b_env

    # --- Assemble: b starts under the tail at the throw ---
    total = max(n_e, throw_start + n_b)
    mix = np.zeros(total)
    mix[:n_e] += a_out
    mix[throw_start:throw_start + n_b] += b_out
    return mix


# ----------------------------------------------------------------------------
# Riser + tempo-jump drop
# ----------------------------------------------------------------------------

def riser_drop(a, b, sr, bar_s, riser_bars=8, riser_db=-14.0):
    """Riser over the last riser_bars of `a` + HP thinning, hard cut to `b`.

    For tempo jumps: the riser/drum-cut masks the BPM change; `b` drops on
    the 1 at its own tempo. `a` should end exactly on a phrase boundary.
    """
    a = np.asarray(a, dtype=np.float64)
    n_a = len(a)
    b = np.asarray(b, dtype=np.float64)

    riser_n = int(riser_bars * bar_s * sr)
    rstart = max(0, n_a - riser_n)

    # HP sweep on A's tail: 30 Hz -> 5 kHz exponential (thinning)
    t = np.arange(n_a) / sr / bar_s
    tb = (t - (n_a / sr / bar_s - riser_bars)) / riser_bars
    tb = np.clip(tb, 0, 1)
    cut = np.where(t * 0 + 1, 30.0, 30.0)  # base
    cut = 30.0 * (5000.0 / 30.0) ** tb
    cut[:rstart] = 30.0
    a_thin = dsp.sweep_filter(a, sr, cut, ftype="highpass", block=2048)

    # Riser layered over the tail
    riser = dsp.synth_riser(riser_n, sr, level_db=riser_db)
    # duck the riser slightly on its final beat for the drop vacuum
    beat_n = int(60.0 / 120 * sr)  # ~1 beat reference; caller passes bar_s
    a_thin[rstart:] += riser * 1.0

    # Hard cut: A (and riser) die at the last sample; B starts on the 1
    out = np.concatenate([a_thin, b])
    return out


# ----------------------------------------------------------------------------
# T-038 — Hook-Drop Handoff (the signature-moment drop)
# ----------------------------------------------------------------------------

def hook_drop_handoff(a, b, sr, bar_s, exit_fade_ms=70.0, bloom_bars=3,
                      bloom_offset_ms=0.0, bloom_curve="sqrt"):
    """Outgoing track's signature vocal hook is the final event; incoming
    blooms in as texture AT the drop point. No verse runway, no dead air.

    Parameters
    ----------
    a : outgoing segment, ENDS exactly on the hook's phrase boundary
        (caller aligns: the hook's final syllable is a's last sample).
    b : incoming segment, STARTS on its phrase beginning (never mid-groove).
    exit_fade_ms : protective fade on a's tail, 60-80 ms cosine to hard zero.
        Click avoidance only — not an audible fade.
    bloom_bars : incoming bloom duration in bars (2-4). Texture first, then
        takes over.
    bloom_offset_ms : bloom start relative to the drop point. 0 = at the
        drop; negative tucks the bloom under the exit fade (variant).
    bloom_curve : "sqrt" (default) or "linear". NEVER cosine — a cosine
        fade-in sits at ~0.8% amplitude after 80 ms and reads as dead air
        (v17 lesson); sqrt is at ~24% by 80 ms, so there is zero perceived
        gap. The drop's punch comes from the vocal hard-zero, not silence.

    Banked rule: the blend lives in the entrance; the drop lives in the
    exit. A fading outgoing lead over a blooming texture reads as
    indecisive; a hard exit over a blooming entrance reads as a statement.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n_a = len(a)
    n_b = len(b)

    # Protective exit fade: last exit_fade_ms of a -> 0 (cosine, click only)
    ef = max(1, int(exit_fade_ms / 1000.0 * sr))
    a_out = a.copy()
    if ef < n_a:
        a_out[-ef:] *= np.cos(0.5 * np.pi * np.linspace(0, 1, ef))
    else:
        a_out *= np.cos(0.5 * np.pi * np.linspace(0, 1, n_a))

    # Bloom envelope: fast attack over bloom_bars, then full
    bloom_n = int(bloom_bars * bar_s * sr)
    env = np.ones(n_b)
    bn = min(bloom_n, n_b)
    if bn > 0:
        u = np.linspace(0.0, 1.0, bn)
        env[:bn] = np.sqrt(u) if bloom_curve == "sqrt" else u

    drop = n_a
    start = int(drop - bloom_offset_ms / 1000.0 * sr)
    start = max(0, start)
    total = max(n_a, start + n_b)
    mix = np.zeros(total)
    mix[:n_a] += a_out
    mix[start:start + n_b] += b * env
    return mix


# ----------------------------------------------------------------------------
# T-030 — Hard Cut / Quick Cut
# ----------------------------------------------------------------------------

def hard_cut(a, b, sr, guard_ms=2.0):
    """No blend, no FX — the cut, executed with total commitment.

    a: outgoing, ends at peak energy (last beat of a build / iconic chorus).
    b: incoming, enters at full power immediately (no ramp-up).
    guard_ms: tiny raised-cosine guards at the cut to avoid digital clicks.
        Not an audible fade — the violence IS the technique.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    g = max(1, int(guard_ms / 1000.0 * sr))
    a_out = a.copy()
    b_out = b.copy()
    if g < len(a_out):
        a_out[-g:] *= 0.5 + 0.5 * np.cos(np.pi * np.linspace(0, 1, g))
    if g < len(b_out):
        b_out[:g] *= 0.5 - 0.5 * np.cos(np.pi * np.linspace(0, 1, g))
    return np.concatenate([a_out, b_out])


# ----------------------------------------------------------------------------
# T-006 — Brake / Tape Stop
# ----------------------------------------------------------------------------

def brake_stop(a, sr, bpm, stop_beats=0.25, curve="exp", tail_pad_beats=1.0):
    """Vinyl-slowing-to-a-halt. Pitch and tempo dive together over
    stop_beats (default 1/4 beat — the sweet spot), then the drop.

    a: outgoing, ends at the brake point (end of a phrase).
    curve: "exp" (brake-dial feel) or "linear" (pitch-fader pull).
    Returns a + dived tail + silence pad; caller drops the next track on
    the following downbeat.
    """
    a = np.asarray(a, dtype=np.float64)
    beat_s = 60.0 / bpm
    src_n = int(1.0 * beat_s * sr)  # dive the last beat (plugin behavior)
    tail_src = a[-src_n:] if len(a) >= src_n else a
    dived = dsp.pitch_dive(tail_src, sr, int(stop_beats * beat_s * sr),
                           curve=curve)
    pad = np.zeros(int(tail_pad_beats * beat_s * sr))
    return np.concatenate([a, dived, pad])


# ----------------------------------------------------------------------------
# T-013 — Power-Down
# ----------------------------------------------------------------------------

def power_down(a, sr, bpm, down_beats=1.5, curve="linear",
               tail_pad_beats=1.0):
    """Drag the pitch fader 0 -> -100%: the track slows AND drops in pitch
    over down_beats, dying into a low growl. Longer and more manual than
    T-006 — the track "runs out of life".

    Often paired with a reverb/echo tail so the death isn't followed by
    true silence (or deliberately IS, for maximum contrast).
    """
    a = np.asarray(a, dtype=np.float64)
    beat_s = 60.0 / bpm
    src_n = int(min(2.0, down_beats) * beat_s * sr)
    tail_src = a[-src_n:] if len(a) >= src_n else a
    dived = dsp.pitch_dive(tail_src, sr, int(down_beats * beat_s * sr),
                           curve=curve)
    pad = np.zeros(int(tail_pad_beats * beat_s * sr))
    return np.concatenate([a, dived, pad])


# ----------------------------------------------------------------------------
# T-007 — Backspin (Spinback)
# ----------------------------------------------------------------------------

def backspin(a, b, sr, bpm, spin_beats=1.0, src_beats=2.0):
    """Fling the jog wheel backward on beat 4; slam B on the next downbeat.

    The reversed audio decays exponentially over exactly spin_beats
    (~1 beat: long enough to read as a rewind, short enough not to kill
    momentum). Vinyl Mode assumed — this is the digital equivalent.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / bpm
    src_n = int(src_beats * beat_s * sr)
    src = a[-src_n:] if len(a) >= src_n else a
    spin_n = int(spin_beats * beat_s * sr)
    rev = src[::-1]
    # take the first spin_n of the reversed audio (== last spin_n of a)
    seg = rev[:spin_n] if len(rev) >= spin_n else np.pad(
        rev, (0, spin_n - len(rev)))
    env = np.exp(-6.9078 * np.linspace(0, 1, spin_n))  # -> -60 dB at end
    spin = seg * env
    return np.concatenate([a, spin, b])


# ----------------------------------------------------------------------------
# T-025 — Vocal Punchline Drop Snap
# ----------------------------------------------------------------------------

def vocal_punchline_snap(a, b, sr, bpm, lowkill_beat=3.0, void_ms=175.0,
                         isolate_mode="midpass"):
    """Surgical 2-bar transition: beat 3 kills the lows, beat 4 isolates the
    vocal word, 150-200 ms of pure void, then B's drop at unity.

    a: outgoing, ends EXACTLY on the drop downbeat (the final bar of a is
        the snap bar; beats are 1-indexed within it).
    b: incoming drop, enters at full power (no fade).
    lowkill_beat: beat of the final bar where lows die (default 3.0).
    void_ms: pre-drop silence, 150-200 ms. This resets the ear's loudness
        adaptation (~200 ms windows) — the drop lands relative to nothing.
    isolate_mode: "midpass" (default) — on beat 4, kill low+high bands,
        leaving the vocal band. A full-mix approximation: with stems, pass
        the vocal stem and use "stem" for exact isolation.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / bpm
    n = len(a)
    bar_n = int(4 * beat_s * sr)
    bar_start = max(0, n - bar_n)

    # Low kill from lowkill_beat of the final bar
    lk = bar_start + int((lowkill_beat - 1) * beat_s * sr)
    lo_db = np.zeros(n)
    lo_db[lk:] = KILL_DB

    # Beat 4: isolate the vocal word
    iso = bar_start + int(3 * beat_s * sr)
    mid_db = np.zeros(n)
    hi_db = np.zeros(n)
    if isolate_mode == "midpass":
        mid_db[iso:] = 0.0
        hi_db[iso:] = KILL_DB
        # lows already killed above
    a_eq = dsp.apply_3band_eq(a, sr, lo_db, mid_db, hi_db)

    # The void: hard mute void_ms before the drop
    void_n = int(void_ms / 1000.0 * sr)
    a_out = a_eq.copy()
    if void_n < n:
        a_out[n - void_n:] = 0.0

    total = n + len(b)
    mix = np.zeros(total)
    mix[:n] += a_out
    mix[n:n + len(b)] += b  # at unity — the punch
    return mix


# ----------------------------------------------------------------------------
# T-029 — Fake Drop (Rug Pull)
# ----------------------------------------------------------------------------

def fake_drop(a, b, sr, bpm, void_beats=3.0, interlude=None):
    """Build to the drop, then DON'T: 2-4 beats of void, then the real drop.

    a: outgoing build, ends at the rug-pull point (bar 17 beat 1 equivalent).
    void_beats: 2-4 beats of zero audio. The crowd's screams fill the club.
    interlude: optional dry one-shot (e.g. a vocal quip) placed at the
        void's start, in samples (mono array) or None.
    b: the real drop, slams after the void.
    Human-triggered weapon — the engine renders it, never auto-deploys it.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / bpm
    void_n = int(void_beats * beat_s * sr)
    void = np.zeros(void_n)
    if interlude is not None:
        inter = np.asarray(interlude, dtype=np.float64)
        k = min(len(inter), void_n)
        void[:k] += inter[:k]
    return np.concatenate([a, void, b])


# ----------------------------------------------------------------------------
# T-008 — Loop Roll Build
# ----------------------------------------------------------------------------

def loop_roll_build(a, b, sr, bpm, roll_bars=1, hpf_end_hz=6000.0):
    """Invent a build-up from slip-mode rolls: 1/2 -> 1/4 -> 1/8 -> 1/16
    across the final bar, HPF thinning, release into B's drop.

    a: outgoing; the roll happens over its last roll_bars (default 1 bar).
    Each beat of the roll bar loops a shrinking slice anchored at the bar
    start (digital hot-cue adaptation of the manual roll).
    b: incoming drop, slams on the downbeat after the roll.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / bpm
    beat_n = int(beat_s * sr)
    roll_n = int(roll_bars * 4 * beat_s * sr)
    rstart = max(0, len(a) - roll_n)

    out = a.copy()
    # Roll each beat of the final bar with doubling density
    bar_start = max(0, len(a) - int(4 * beat_s * sr))
    for i in range(4):
        div = 2 ** (i + 1)          # hits per beat: 2, 4, 8, 16
        b0 = bar_start + i * beat_n
        slice_n = max(1, beat_n // div)
        anchor = a[b0:b0 + slice_n]
        if len(anchor) < slice_n:
            anchor = np.pad(anchor, (0, slice_n - len(anchor)))
        tiled = np.tile(anchor, div)
        if len(tiled) < beat_n:  # beat_n not divisible by div — pad, don't clip
            tiled = np.pad(tiled, (0, beat_n - len(tiled)))
        out[b0:b0 + beat_n] = tiled[:beat_n]

    # HPF sweep over the roll bar: thinning before impact
    t = np.arange(len(out)) / sr
    tb = np.clip((t - bar_start / sr) / (4 * beat_s), 0, 1)
    cut = 30.0 * (hpf_end_hz / 30.0) ** tb
    cut[:bar_start] = 30.0
    out = dsp.sweep_filter(out, sr, cut, ftype="highpass", block=2048)
    return np.concatenate([out, b])


# ----------------------------------------------------------------------------
# T-019 — Stutter Transition (hot-cue drumming)
# ----------------------------------------------------------------------------

def stutter_transition(a, b, sr, bpm, cue_t, cue_len_s=0.25,
                       tap_beats=(3.0, 3.5, 4.0, 4.5), release_t=None):
    """Re-trigger B's iconic vocal word in accelerating taps, then release.

    a: outgoing; its final bar is the stutter bar (4 beats).
    b: incoming track (full). cue_t: hot-cue position (seconds) of the
        iconic word's transient in b. cue_len_s: slice length per tap.
    tap_beats: 1-indexed beats within the final bar (default 3, 3-and,
        4, 4-and — the accelerating "Ye-Ye-Ye-Yeah!").
    release_t: where b plays from after the bar (default: cue_t — LET IT
        PLAY from the cue).
    Each tap is low-killed (the stutter is percussion, not bass). On the
    last tap, a's fader dies; b enters full with lows restored.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / bpm
    beat_n = int(beat_s * sr)
    n = len(a)
    bar_start = max(0, n - 4 * beat_n)

    cue_n = int(cue_len_s * sr)
    ci = int(cue_t * sr)
    cue = b[ci:ci + cue_n]
    if len(cue) < cue_n:
        cue = np.pad(cue, (0, cue_n - len(cue)))
    # taps are percussion: kill the lows
    cue_lo, cue_mid, cue_hi = dsp.split_3band(cue, sr)
    cue = cue_mid + cue_hi

    mix = a.copy().astype(np.float64)
    # a's fader dies on the last tap
    last_tap = bar_start + int((tap_beats[-1] - 1) * beat_s * sr)
    mix = np.pad(mix, (0, 4 * beat_n))  # room for the release bar region
    mix[last_tap:] = 0.0
    for tb in tap_beats:
        ti = bar_start + int((tb - 1) * beat_s * sr)
        k = min(cue_n, len(mix) - ti)
        if k > 0:
            mix[ti:ti + k] += cue[:k]

    # Release: b plays from release_t at the bar after the stutter bar
    rel = release_t if release_t is not None else cue_t
    ri = int(rel * sr)
    b_seg = b[ri:]
    # restore lows with a 1-beat fade (the "slam Low EQ to 12 o'clock")
    lo_db = np.full(len(b_seg), KILL_DB)
    lo_db[beat_n:] = 0.0
    # smooth the step
    st = min(beat_n, len(b_seg))
    lo_db[:st] = np.linspace(KILL_DB, 0.0, st)
    b_full = dsp.apply_3band_eq(b_seg, sr, lo_db, 0.0, 0.0)

    bar_end = bar_start + 4 * beat_n
    total = max(len(mix), bar_end + len(b_full))
    out = np.zeros(total)
    out[:len(mix)] += mix
    out[bar_end:bar_end + len(b_full)] += b_full
    return out


# ----------------------------------------------------------------------------
# T-033 — Vocal-Chop Build Transition
# ----------------------------------------------------------------------------

def vocal_chop_build(a, b, sr, bar_s, chop_t, chop_len_s=1.0, build_bars=8,
                     bp_lo_hz=500.0, bp_hi_hz=5000.0):
    """Chop a vocal phrase into a density ladder (1/4 -> 1/8 -> 1/16),
    brightening through a band-pass sweep, then hard-cut to B's drop.

    a: outgoing (the chop source lives at chop_t).
    chop_t: start (seconds) of the vocal phrase to chop.
    build_bars: 8 default — bars 1-4 at 1/4-note, 5-6 at 1/8, 7-8 at 1/16.
    The silence between the last chop and the drop is < 100 ms (a T-025
    micro-void without the vocal hang).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = bar_s / 4.0

    ci = int(chop_t * sr)
    cn = int(chop_len_s * sr)
    chop = a[ci:ci + cn]
    if len(chop) < cn:
        chop = np.pad(chop, (0, cn - len(chop)))

    build_n = int(build_bars * bar_s * sr)
    build = np.zeros(build_n)
    # density ladder: (bars, notes_per_bar)
    ladder = [(4, 4), (2, 8), (2, 16)]
    t = 0
    for bars, npb in ladder:
        note_n = int(bar_s * sr / npb)
        for _ in range(bars * npb):
            if t + note_n > build_n:
                break
            k = min(note_n, cn)
            build[t:t + k] += chop[:k]
            t += note_n

    # Brightness ladder: band-pass sweeps 500 Hz -> 5 kHz over the build
    u = np.linspace(0, 1, build_n)
    lo_env = bp_lo_hz * np.ones(build_n)
    hi_env = bp_lo_hz * (bp_hi_hz / bp_lo_hz) ** u
    build = dsp.bandpass_sweep(build, sr, lo_env, hi_env)

    return np.concatenate([build, b])


# ----------------------------------------------------------------------------
# T-018 — Noise + Echo Buildup (empty-channel riser)
# ----------------------------------------------------------------------------

def noise_echo_buildup(a, b, sr, bar_s, bpm, build_bars=8, noise_db=-16.0,
                       echo_div=0.5, feedback=0.6):
    """Build a riser from nothing: white noise + 1/2-beat echo on an empty
    channel, raised over build_bars, killed dead on the drop.

    a: outgoing; the noise layers over its last build_bars.
    The 1/2-beat echo gates the noise into rhythm so it grooves instead of
    hissing. The sudden absence of the noise wall makes B's drop hit
    harder (contrast principle).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / bpm
    build_n = int(build_bars * bar_s * sr)
    rstart = max(0, len(a) - build_n)

    rng = np.random.default_rng(11)  # deterministic
    noise = rng.standard_normal(build_n)
    echoed = dsp.feedback_delay(noise, sr, echo_div * beat_s,
                                feedback=feedback, wet=0.8)
    env = dsp.raised_cosine(build_n, up=True) ** 1.5
    noise_ch = echoed * env
    noise_ch = noise_ch / (np.max(np.abs(noise_ch)) + 1e-9)
    noise_ch = noise_ch * dsp.db_to_gain(noise_db)

    out = a.copy()
    out[rstart:rstart + build_n] += noise_ch[:len(out) - rstart]
    # kill dead on the drop — no tail, no fade
    return np.concatenate([out, b])


# ----------------------------------------------------------------------------
# T-014 — Hot-Cue Drop Swap
# ----------------------------------------------------------------------------

def hotcue_drop_swap(a, b, sr, bpm, xfade_beats=4):
    """Replace A's drop with B's: volume cross-swap over the run-up.

    a: outgoing, ends at its drop point (the last xfade_beats are the
        "1-2-3-DROP" run-up).
    b: incoming, STARTS at its own run-up (hot cue = drop - 4 beats;
        caller aligns).
    Equal-power swap over xfade_beats; optional echo/filter layered by
    the caller for style.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / bpm
    xf_n = int(xfade_beats * beat_s * sr)
    n_a = len(a)

    a_env = np.ones(n_a)
    s0 = max(0, n_a - xf_n)
    u = np.linspace(0.0, 1.0, n_a - s0)
    a_env[s0:] = np.cos(0.5 * np.pi * u)
    b_env = np.zeros(len(b))
    k = min(xf_n, len(b))
    ub = np.linspace(0.0, 1.0, k)
    b_env[:k] = np.sin(0.5 * np.pi * ub)
    b_env[k:] = 1.0

    total = max(n_a, s0 + len(b))
    mix = np.zeros(total)
    mix[:n_a] += a * a_env
    mix[s0:s0 + len(b)] += b * b_env
    return mix


# ----------------------------------------------------------------------------
# T-024 — Double Drop (dual-build collision)
# ----------------------------------------------------------------------------

def double_drop(a, b, sr, bar_s, drop_at_bar=16, drop_bars=16):
    """Two builds converge on ONE downbeat. Single-sub-bass rule enforced:
    B's lows stay killed through the drop; bass swaps after drop_bars.

    a, b: build+drop segments, SAME length, builds starting together
        (caller aligns). drop_at_bar: bar index (0-based) of the drop.
    Prerequisite (caller's taste call): at most ONE drop carries a vocal.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]

    drop = int(drop_at_bar * bar_s * sr)
    swap = int(min(n, (drop_at_bar + drop_bars) * bar_s * sr))

    # B's low band: killed until the drop, stays killed for drop_bars
    b_lo = np.full(n, KILL_DB)
    b_lo[swap:] = 0.0
    # smooth the swap over 1 beat
    beat_n = int(bar_s * sr / 4)
    e0, e1 = max(0, swap - beat_n // 2), min(n, swap + beat_n // 2)
    if e1 > e0:
        b_lo[e0:e1] = np.linspace(KILL_DB, 0.0, e1 - e0)
    # A's low band: full until the swap, then killed
    a_lo = np.zeros(n)
    a_lo[swap:] = KILL_DB
    if e1 > e0:
        a_lo[e0:e1] = np.linspace(0.0, KILL_DB, e1 - e0)

    a_eq = dsp.apply_3band_eq(a, sr, a_lo, 0.0, 0.0)
    b_eq = dsp.apply_3band_eq(b, sr, b_lo, 0.0, 0.0)
    return a_eq + b_eq


# ----------------------------------------------------------------------------
# T-027 — Loop Transition (bounded loop handoff)
# ----------------------------------------------------------------------------

def loop_transition(a, b, sr, bar_s, loop_bars=8, cycles=2):
    """Loop A's last clean groove for exactly `cycles` (default 2 x 8 bars
    = 16 bars) to manufacture an outro, then a standard T-001 EQ blend.

    The 2-cycle cap is the discipline: one repetition reads as groove, two
    as build, three as "the DJ is stuck". If B isn't ready by cycle 2,
    echo-out (T-004) — NEVER a third cycle.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    loop_n = int(loop_bars * bar_s * sr)
    loop_src = a[-loop_n:] if len(a) >= loop_n else a
    a_looped = np.tile(loop_src, cycles)
    return eq_blend(a_looped, b, sr, bar_s, blend_bars=loop_bars * cycles)


# ----------------------------------------------------------------------------
# T-017 — Layered FX Stack (echo + filter + reverb combo)
# ----------------------------------------------------------------------------

def layered_fx_stack(a, b, sr, bar_s, bpm, echo_bars=8, filter_bars=4,
                     reverb_bars=2, enter_bars=4):
    """The upgrade path from a flat T-004: stack echo (time), HPF (frequency)
    and reverb (space) on the outgoing track so it has nowhere left to exist.

    Order: echo ON at -echo_bars, HPF sweep starts at -filter_bars,
    reverb send opens at -reverb_bars, fader kill on the 1. B enters over
    -enter_bars with a mirror filter opening.
    Each FX attacks a different perceptual dimension — a single FX leaves
    the others intact, which is why plain echo-outs can feel abrupt.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n_a = len(a)
    beat_s = 60.0 / bpm

    # --- Echo from -echo_bars (1/2 beat, wet 50%, feedback 60-70%) ---
    e0 = max(0, n_a - int(echo_bars * bar_s * sr))
    region = a[e0:].copy()
    echoed_region = dsp.feedback_delay(region, sr, 0.5 * beat_s,
                                       feedback=0.65, wet=0.5)
    a_fx = a.copy()
    a_fx[e0:] = echoed_region

    # --- HPF sweep over the last filter_bars (30 Hz -> 3 kHz) ---
    f0 = max(0, n_a - int(filter_bars * bar_s * sr))
    t = np.arange(n_a) / sr
    fb = np.clip((t - f0 / sr) / (filter_bars * bar_s), 0, 1)
    cut = 30.0 * (3000.0 / 30.0) ** fb
    cut[:f0] = 30.0
    a_fx = dsp.sweep_filter(a_fx, sr, cut, ftype="highpass", block=2048)

    # --- Reverb send over the last reverb_bars (dissolve the tail) ---
    r0 = max(0, n_a - int(reverb_bars * bar_s * sr))
    wet = dsp.schroeder_reverb(a_fx, sr, wet=1.0, decay=1.5)
    w = np.zeros(n_a)
    w[r0:] = dsp.raised_cosine(n_a - r0, up=True) * 0.8
    a_fx = (1 - w) * a_fx + w * wet

    # --- Fader kill on the 1 ---
    a_fx[-int(0.01 * sr):] *= np.linspace(1, 0, int(0.01 * sr))

    # --- B enters with mirror filter opening over enter_bars ---
    b_start = max(0, n_a - int(enter_bars * bar_s * sr))
    n_b = len(b)
    tb = np.arange(n_b) / sr / bar_s
    eb = min(enter_bars, tb[-1] if len(tb) else enter_bars)
    bcut = np.where(tb < enter_bars,
                    3000.0 * (20.0 / 3000.0) ** np.clip(tb / enter_bars, 0, 1),
                    20.0)
    b_f = dsp.sweep_filter(b, sr, bcut, ftype="highpass", block=2048)
    benv = np.zeros(n_b)
    en = min(int(enter_bars * bar_s * sr), n_b)
    benv[:en] = dsp.raised_cosine(en, up=True)
    benv[en:] = 1.0

    total = max(n_a, b_start + n_b)
    mix = np.zeros(total)
    mix[:n_a] += a_fx
    mix[b_start:b_start + n_b] += b_f * benv
    return mix


# ----------------------------------------------------------------------------
# T-034 — Reverb Freeze Transition
# ----------------------------------------------------------------------------

def reverb_freeze(a, b, sr, bar_s, bpm, freeze_bars=2, void_beats=3,
                  decay_s=8.0, release_bars=4):
    """Halt time with a frozen reverb tail, launch B inside it, release.

    a: outgoing; its last freeze_bars feed the freeze.
    The freeze: reverb send to 100% wet with a long decay while the dry
    fader falls — the tail stops decaying and a smeared chord hangs,
    harmonically static but texturally alive (holds A's key with no rhythm).
    void_beats of limbo, then B's first beat lands INSIDE the tail; the
    freeze releases over release_bars as B plays.
    Software freeze (no freeze button): decay -> long + input killed — the
    existing tail recirculates.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / bpm
    n_a = len(a)
    fz_n = int(freeze_bars * bar_s * sr)
    f0 = max(0, n_a - fz_n)

    # Wet tail excited by the pre-freeze signal (a real throw works because
    # the reverb is excited BEFORE the fader cuts).
    wet = dsp.schroeder_reverb(a[f0:], sr, wet=1.0, decay=decay_s)
    void_n = int(void_beats * beat_s * sr)
    tail_need = fz_n + void_n
    if len(wet) < tail_need:
        # extend the frozen tail: loop its last second (it's near-static)
        tailbit = wet[-int(sr):] if len(wet) >= sr else wet
        reps = int(np.ceil((tail_need - len(wet)) / max(1, len(tailbit)))) + 1
        wet = np.concatenate([wet] + [tailbit] * reps)
    tail = wet[:tail_need].copy()
    # fade the tail's own end so the loop seam never clicks
    fl = min(int(0.5 * sr), len(tail))
    tail[-fl:] *= np.linspace(1, 0, fl)

    # Dry crossfade: full dry until f0, then wet takes over the freeze window
    dry_part = np.zeros(tail_need)
    k = min(fz_n, len(a) - f0)
    dry_part[:k] = a[f0:f0 + k]
    w = np.zeros(tail_need)
    w[:fz_n] = dsp.raised_cosine(fz_n, up=True)
    w[fz_n:] = 1.0
    frozen = dry_part * (1 - w) + tail * w

    # B launches inside the tail (at the void start), freeze releases
    b_at = f0 + fz_n
    rel_n = int(release_bars * bar_s * sr)
    n_b = len(b)
    # release: frozen tail fades as B establishes
    tail_total = b_at + max(n_b, rel_n)
    mix = np.zeros(tail_total)
    mix[:f0] += a[:f0]
    # frozen region gets the tail; after b_at the tail releases over rel_n
    fz_full = np.zeros(tail_total - f0)
    fz_full[:len(frozen)] += frozen
    if rel_n > 0 and b_at + rel_n <= len(fz_full) + f0:
        r0 = b_at - f0
        r1 = min(len(fz_full), r0 + rel_n)
        fz_full[r0:r1] *= 1.0 - dsp.raised_cosine(r1 - r0, up=True)
        fz_full[r1:] = 0.0
    mix[f0:] += fz_full
    mix[b_at:b_at + n_b] += b
    return mix


# ----------------------------------------------------------------------------
# T-021 — Tempo Bridge (BPM ramp / half-double metric shift)
# ----------------------------------------------------------------------------

def tempo_bridge(a, sr, bpm_from, bpm_to, bar_s, ramp_bars=12,
                 method="ramp"):
    """Cross wide BPM gaps without chipmunk vocals.

    method "ramp": pitch-preserving phase-vocoder ramp over ramp_bars —
        ONE continuous pass with a per-frame rate envelope (~1 BPM/bar;
        the brain reads it as pre-drop tension, not a DJ error).
        Master-Tempo behavior.
    method "half_double": exact 2x/1x ratios need no ramp — beatmatch at the
        doubled grid. Returns a unchanged; the caller re-grids.
    Returns (ramped_audio, bpm_to). The ramped audio contains ramp_bars of
    beats (the input's beats, retimed along the ramp); its duration is the
    sum of the per-beat periods along the ramp — NOT ramp_bars at the new
    tempo. Callers must use len(ramped_audio), never a theoretical length.
    """
    a = np.asarray(a, dtype=np.float64)
    if method == "half_double":
        ratio = bpm_to / bpm_from
        assert abs(ratio - 2.0) < 0.02 or abs(ratio - 0.5) < 0.02, \
            "half_double needs an exact 2x/1x ratio"
        return a, bpm_to
    # per-frame rate envelope: linear BPM ramp from bpm_from to bpm_to.
    # dsp.phase_vocoder_stretch convention: rate > 1 = LONGER output.
    # Slowing the tempo needs longer audio, so the envelope is
    # bpm_from / bpm(u) (2026-10-19 fix: it was bpm(u)/bpm_from, inverted —
    # slow-downs came out shorter, speed-ups longer).
    n_fft, hop = 2048, 512
    n_frames = max(1, (len(a) - n_fft) // hop + 1)
    u = np.linspace(0.0, 1.0, n_frames)
    rates = bpm_from / (bpm_from + (bpm_to - bpm_from) * u)
    return dsp.phase_vocoder_stretch(a, sr, rates), bpm_to


# ----------------------------------------------------------------------------
# T-022 — Drum Bridge (atonal rhythmic neutralization)
# ----------------------------------------------------------------------------

def drum_bridge(a, b, sr, bar_s, strip_bars=4, interlude_bars=12,
                blend_bars=8):
    """Strip A to drums (key-neutral zone), hold the interlude, blend B in.

    a: outgoing, length strip_bars + interlude_bars (caller provides).
    The strip is a full-mix approximation (HPF + mid kill); with stems the
    caller passes the drum stem for exactness.
    In the absence of pitched material the ear cannot perceive key — B can
    be ANY Camelot. B's drums layer over A's, then A cuts as B's melody
    enters.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    strip_n = int(strip_bars * bar_s * sr)

    # Strip: HPF ramp 30 -> 400 Hz + mid-band kill over strip_bars
    t = np.arange(len(a)) / sr
    sb = np.clip(t / (strip_bars * bar_s), 0, 1)
    cut = 30.0 * (400.0 / 30.0) ** sb
    a_hp = dsp.sweep_filter(a, sr, cut, ftype="highpass", block=2048)
    mid_db = np.zeros(len(a))
    mid_db[:strip_n] = np.linspace(0.0, KILL_DB, strip_n)
    mid_db[strip_n:] = KILL_DB
    a_drums = dsp.apply_3band_eq(a_hp, sr, 0.0, mid_db, 0.0)

    # B blends in over the last blend_bars (drums first, melody later)
    bl_n = int(blend_bars * bar_s * sr)
    b_start = max(0, len(a) - bl_n)
    n_b = len(b)
    benv = np.zeros(n_b)
    en = min(bl_n, n_b)
    benv[:en] = np.sin(0.5 * np.pi * np.linspace(0, 1, en))  # eq-power in
    benv[en:] = 1.0
    # B's lows stay out until A's drums are gone (single-sub rule)
    b_lo = np.full(n_b, KILL_DB)
    b_lo[en:] = 0.0
    b_eq = dsp.apply_3band_eq(b, sr, b_lo, 0.0, 0.0)

    total = max(len(a), b_start + n_b)
    mix = np.zeros(total)
    mix[:len(a)] += a_drums
    mix[b_start:b_start + n_b] += b_eq * benv
    return mix


# ----------------------------------------------------------------------------
# T-023 — Breakdown Transition (drumless tempo/key change)
# ----------------------------------------------------------------------------

def breakdown_transition(a, b, sr, bar_s, bpm_from=None, bpm_to=None,
                         blend_bars=16):
    """Execute the whole transition inside A's breakdown.

    a: A's breakdown segment (kick dropped out; pads/piano/vocal remain).
    b: B's melodic intro/breakdown.
    With no drums there is no beatmatching constraint and no audible tempo
    reference — bpm_from -> bpm_to slides over the blend (pitch-preserving;
    drumless audio stretches cleanly). Blend with mid/high EQs only.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    if bpm_from and bpm_to and abs(bpm_to - bpm_from) > 0.5:
        a = dsp.phase_vocoder_stretch(a, sr, bpm_to / bpm_from)

    bl_n = int(blend_bars * bar_s * sr)
    n_a, n_b = len(a), len(b)
    # B enters at bar 1 of the blend zone (overlapping a's breakdown)
    b_start = max(0, n_a - bl_n)
    u = np.linspace(0.0, 1.0, min(bl_n, n_a))
    a_env = np.ones(n_a)
    s0 = max(0, n_a - bl_n)
    a_env[s0:] = np.cos(0.5 * np.pi * u[:n_a - s0])
    benv = np.zeros(n_b)
    en = min(bl_n, n_b)
    benv[:en] = np.sin(0.5 * np.pi * np.linspace(0, 1, en))
    benv[en:] = 1.0

    total = max(n_a, b_start + n_b)
    mix = np.zeros(total)
    mix[:n_a] += a * a_env
    mix[b_start:b_start + n_b] += b * benv
    return mix


# ----------------------------------------------------------------------------
# T-026 — Genre Bridge (prepared multi-song pivot)
# ----------------------------------------------------------------------------

def genre_bridge(a, b, sr, bar_s, bpm, anchor_t, anchor_len_s=4.0,
                 anchor_cycles=4, wash_wet=0.6):
    """Pivot genres on a familiar vocal anchor (the Ship of Theseus).

    anchor_t: start (seconds) in a of the recognizable vocal phrase.
    The anchor loops (4 bars x anchor_cycles) in a reverb wash while B's
    drums build underneath; on the drop, A cuts and B snaps open.
    The vocal is the cognitive anchor — as long as it persists, the crowd
    tolerates radical change underneath it.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    ai = int(anchor_t * sr)
    an = int(anchor_len_s * sr)
    anchor = a[ai:ai + an]
    if len(anchor) < an:
        anchor = np.pad(anchor, (0, an - len(anchor)))
    looped = np.tile(anchor, anchor_cycles)
    washed = dsp.schroeder_reverb(looped, sr, wet=wash_wet, decay=2.5)

    # B builds underneath: HPF engaged, low volume, filter opening
    n_w = len(washed)
    t = np.arange(len(b)) / sr / bar_s
    bcut = np.where(t < anchor_cycles,
                    3000.0 * (20.0 / 3000.0) ** np.clip(
                        t / anchor_cycles, 0, 1),
                    20.0)
    b_hp = dsp.sweep_filter(b, sr, bcut, ftype="highpass", block=2048)
    benv = np.zeros(len(b))
    en = min(n_w, len(b))
    benv[:en] = 0.5 * dsp.raised_cosine(en, up=True)
    benv[en:] = 0.5

    total = max(n_w, len(b))
    mix = np.zeros(total)
    mix[:n_w] += washed
    mix[:len(b)] += b_hp * benv
    # The drop: wash cuts dead at the loop's end, B snaps to full dry
    drop = n_w
    out = mix.copy()
    if drop < len(out):
        out[drop:] = 0.0
        bj = min(len(b), len(out) - drop)
        if bj > 0:
            out[drop:drop + bj] += b[:bj]
    return out


# ----------------------------------------------------------------------------
# T-031 — Loop-Juggle Transition (The Replace)
# ----------------------------------------------------------------------------

def loop_juggle_replace(a_bar, b_bar, b_full, sr, bpm, cycles=4):
    """Turntablist beat-juggling as a transition: steal the groove hit by
    hit. Each 1-bar cycle: A plays beats 1-3, B's loop-start replaces beat 4.
    On the final cycle, B re-establishes the downbeat from its first kick.

    a_bar, b_bar: 1-bar loops (caller-provided, beatmatched).
    b_full: B from its phrase start (first kick) — takes over after.
    Digital adaptation: hot cues replace rewinds (instant, quantized).
    """
    a_bar = np.asarray(a_bar, dtype=np.float64)
    b_bar = np.asarray(b_bar, dtype=np.float64)
    b_full = np.asarray(b_full, dtype=np.float64)
    beat_s = 60.0 / bpm
    beat_n = int(beat_s * sr)
    bar_n = 4 * beat_n

    def one_bar(x):
        return x[:bar_n] if len(x) >= bar_n else np.pad(x, (0, bar_n - len(x)))

    ab, bb = one_bar(a_bar), one_bar(b_bar)
    out = []
    for _ in range(cycles):
        cyc = ab.copy()
        cyc[3 * beat_n:4 * beat_n] = bb[0:beat_n]  # steal beat 4
        out.append(cyc)
    out.append(b_full)
    return np.concatenate(out)


# ----------------------------------------------------------------------------
# T-010 — Acapella Overlay (live mashup)
# ----------------------------------------------------------------------------

def acapella_overlay(a, b_vocal, sr, bar_s, overlay_bars=16,
                     phrase_windows=None):
    """Sing B's vocal over A's instrumental.

    b_vocal: acapella or stem-isolated vocal. EQ preset: lows killed,
        highs tamed (-2 dB), mids flat. Key Lock assumed (caller's domain).
    overlay_bars: overlay window; gentle 2-bar fades each end.
    phrase_windows: optional list of (start_bar, end_bar, gain) — the
        manual fader ride ("up when the singer sings"). Without it, the
        overlay is a fixed bed; the ride remains a human-feel judgment.
    Never overlay on A's vocal — the caller guarantees a vocal-free window.
    """
    a = np.asarray(a, dtype=np.float64)
    v = np.asarray(b_vocal, dtype=np.float64)
    n_a = len(a)
    ov_n = int(overlay_bars * bar_s * sr)
    v_seg = v[:ov_n] if len(v) >= ov_n else np.pad(v, (0, ov_n - len(v)))

    # Deck-2 EQ preset
    v_eq = dsp.apply_3band_eq(v_seg, sr, KILL_DB, 0.0, -2.0)

    env = np.ones(ov_n)
    f = min(int(2 * bar_s * sr), ov_n)
    env[:f] = dsp.raised_cosine(f, up=True)
    env[-f:] *= 1.0 - dsp.raised_cosine(f, up=True)
    if phrase_windows:
        for s_bar, e_bar, g in phrase_windows:
            s = int(s_bar * bar_s * sr)
            e = min(ov_n, int(e_bar * bar_s * sr))
            if e > s:
                env[s:e] *= g
    v_out = v_eq * env

    total = max(n_a, ov_n)
    mix = np.zeros(total)
    mix[:n_a] += a
    mix[:ov_n] += v_out
    return mix


# ----------------------------------------------------------------------------
# T-015 — Harmonic Mixing (Camelot wheel, pure decision function)
# ----------------------------------------------------------------------------

def harmonic_mix(key_a, key_b):
    """Camelot compatibility check. Keys like "8A" (minor) / "8B" (major).

    The four legal moves: same key (perfect), +/-1 step (bread and butter,
    ~80% of pro harmonic sets), relative major/minor (same number, mood
    flips), +2 energy boost (sparingly). Wheel wraps 12 <-> 1.
    Returns {"compatible": bool, "move": str}.
    """
    def parse(k):
        k = k.strip().upper()
        return int(k[:-1]), k[-1]

    na, la = parse(key_a)
    nb, lb = parse(key_b)
    if na == nb and la == lb:
        return {"compatible": True, "move": "same key"}
    if na == nb:
        return {"compatible": True, "move": "relative major/minor"}
    step = (nb - na) % 12
    if la == lb and step in (1, 11):
        return {"compatible": True,
                "move": "+1 lift" if step == 1 else "-1 deepen"}
    if la == lb and step == 2:
        return {"compatible": True, "move": "+2 energy boost"}
    return {"compatible": False, "move": "clash — pick another technique"}


# ----------------------------------------------------------------------------
# T-037 — Transition Selection Framework (the decision brain)
# ----------------------------------------------------------------------------

def select_technique(f):
    """Choose the technique from the musical situation.

    f: feature dict —
        bpm_delta_pct   float: |BPM_B - BPM_A| / BPM_A * 100
        half_double_ok  bool:  exact 2x/1x ratio available
        camelot_distance int:  0 (same) / 1 (+-1 or relative) / 2-3 / 4+ (clash)
        energy_delta    float: energy_B - energy_A on a 1-10 scale
        phrase_a        str:   breakdown / outro / build / drop / verse / chorus
        vocal           str:   "a_only" / "b_only" / "both" / "neither"
        genre_pair      str:   "same" / "neighbor" / "leap"
        b_has_build     bool
        a_has_breakdown bool
        iconic_vocal    str:   "a" / "b" / None  (signature hook available)
        b_intro_bars    int:   usable intro length of B in bars
        drop_pair_ok    bool:  two drops complement (<=1 vocal), for T-024
        shared_lyric    str/None: the shared word/phrase for T-011 wordplay
        screwed         bool:  outgoing gets the T-039 screwed treatment
        pitch_shift_st  int/None: semitone shift for T-032 pitch-play overlay

    Selection is constraint satisfaction: rejection rules prune first
    (most trainwrecks come from blending where a cut was required), the
    decision table picks among survivors. Returns
    {"technique": id, "reasons": [...], "rejected": {...},
     "alternatives": [...]}.
    A deliberate human contrast choice may overrule this output.
    """
    bpm = f.get("bpm_delta_pct", 0)
    cam = f.get("camelot_distance", 0)
    dE = f.get("energy_delta", 0)
    phrase = f.get("phrase_a", "outro")
    voc = f.get("vocal", "neither")
    genre = f.get("genre_pair", "same")
    rejected = {}

    def reject(tid, reason):
        rejected[tid] = reason

    # --- rejection rules (prune first) ---
    if not (f.get("energy_ok", True)) or bpm >= 5:
        reject("bass_swap", "energy<6 or BPM gap >= 5% or off phrase")
    if bpm >= 8:
        reject("filter_sweep", "can't bridge tempo >= 8%")
    if bpm >= 10 or cam >= 4:
        reject("eq_blend", "BPM gap >= 10% or Camelot distance >= 4")
    if phrase == "drop" and genre == "same":
        reject("echo_out", "overkill for same-BPM/same-mood")
    if voc == "both":
        reject("acapella_overlay", "never two vocals")
        reject("double_drop", "both drops have vocals — use drop swap")
    if f.get("b_intro_bars", 16) < 8:
        reject("eq_blend", "B has no usable intro — loop it first (T-027)")

    cands = []

    def consider(tid, reason):
        if tid not in rejected:
            cands.append((tid, reason))

    # --- decision table ---
    if bpm < 3 and cam <= 1 and abs(dE) <= 1:
        consider("eq_blend", "lateral: same BPM/key/energy — invisible handoff")
        consider("filter_sweep", "lateral alternative with more motion")
    if bpm < 3 and cam <= 2 and dE >= 0:
        consider("bass_swap", "kick-driven handover, same tempo")
        consider("hotcue_drop_swap", "drop currency available")
    if f.get("iconic_vocal") == "b":
        consider("stutter_transition", "iconic vocal on B — signpost it")
        consider("vocal_punchline_snap", "iconic vocal -> bass punch")
    if f.get("iconic_vocal") == "a":
        consider("hook_drop_handoff", "A's signature hook is the final event")
    if cam >= 4 or genre == "leap":
        consider("echo_out", "key/genre independence — reset the canvas")
        consider("drum_bridge", "atonal zone grants total harmonic freedom")
        consider("hard_cut", "deliberate energy reset")
    if bpm >= 8 or f.get("half_double_ok"):
        consider("tempo_bridge", "wide BPM gap — ramp or half/double")
        consider("breakdown_transition", "change BPM+key+genre inside the drums")
    if phrase == "breakdown" or f.get("a_has_breakdown"):
        consider("breakdown_transition", "the rules suspend inside a breakdown")
    if phrase == "build" and dE >= 2 and f.get("b_has_build"):
        consider("build_to_drop", "dual-build layering (T-009 choreography)")
        consider("loop_roll_build", "manufacture the lift")
        consider("noise_echo_buildup", "empty-channel riser")
    if f.get("shared_lyric"):
        consider("wordplay", f"shared lyric '{f['shared_lyric']}' — the idea IS the wordplay")
    if f.get("screwed"):
        consider("screwed_treatment", "pre-transition screwed treatment (T-039)")
    if f.get("pitch_shift_st") and voc in ("b_only", "both"):
        consider("pitch_play", f"key-shift the vocal {f['pitch_shift_st']:+d} st into the backing key")
    if dE <= -2:
        consider("reverb_wash", "let the floor breathe — never fake-lift")
        consider("reverb_freeze", "the classiest hard reset")
    if f.get("drop_pair_ok"):
        consider("double_drop", "two drops, one downbeat, one sub-bass")
    if f.get("b_intro_bars", 16) < 8:
        consider("loop_transition", "manufacture B's intro")
    if genre == "leap" and voc in ("a_only", "b_only"):
        consider("genre_bridge", "vocal anchor carries the pivot")
    # default fallback
    if not cands:
        consider("echo_out", "fallback: the Swiss-army knife")

    # priority order when several survive
    priority = ["hook_drop_handoff", "wordplay", "screwed_treatment", "eq_blend", "bass_swap", "breakdown_transition",
                "filter_sweep", "tempo_bridge", "drum_bridge", "echo_out",
                "reverb_wash", "reverb_freeze", "hotcue_drop_swap", "double_drop",
                "loop_roll_build", "noise_echo_buildup", "stutter_transition",
                "vocal_punchline_snap", "loop_transition", "genre_bridge",
                "hard_cut", "build_to_drop", "pitch_play",
                "three_deck_layer"]
    cands.sort(key=lambda c: priority.index(c[0]) if c[0] in priority else 99)
    best, reason = cands[0]
    return {"technique": best, "reasons": [reason] +
            [r for t, r in cands[1:3]],
            "rejected": rejected,
            "alternatives": [t for t, _ in cands[1:4]]}


# ----------------------------------------------------------------------------
# T-011 — Wordplay (lyric-matched cut)
# ----------------------------------------------------------------------------

def wordplay(a, b, sr, bpm, a_word_t, b_word_t, word_len_s=0.5,
             exit="hard_cut", exit_beats=4.0):
    """Chain two tracks through a shared lyric word.

    a plays until its shared-word onset (a_word_t); b's matching word
    (at b_word_t, length word_len_s) triggers in rhythmic unison — the
    crowd hears the word "answered" by the new track. After the word
    completes, the transition finishes via `exit`.

    Parameters
    ----------
    a : outgoing segment; must contain the shared word at a_word_t.
    b : incoming segment; must contain the matching word at b_word_t.
    a_word_t / b_word_t : word onset times in seconds within a / b.
        From WhisperX-class word alignment in production; caller-supplied.
        Trigger must land within ~±50 ms or the illusion breaks.
    word_len_s : duration of the shared word (both tracks).
    exit : "hard_cut" (default) — a dies at word end, b continues;
           "echo_out" — a gets a 1/2-beat echo tail while b takes over.

    Returns the rendered mix. Handoff point = a_word_t.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / bpm
    a_wn = int(a_word_t * sr)
    b_wn = int(b_word_t * sr)
    w_n = int(word_len_s * sr)
    a_wn = min(max(0, a_wn), len(a))
    b_wn = min(max(0, b_wn), len(b))

    # b's word lands in unison with a's word: align b_word_t -> a_word_t
    offset = a_wn - b_wn  # where b[0] sits in mix time
    word_end = a_wn + w_n

    # Total: the word end + exit tail, or b's full continuation — whichever
    # is longer. NOT len(a): a is cut at word_end, so sizing to len(a)
    # leaves a dead tail (2026-10-19 fix).
    total = max(word_end + int(exit_beats * beat_s * sr),
                offset + len(b))
    mix = np.zeros(total)
    # a runs through the end of the shared word (2 ms protective fade —
    # click avoidance only, T-030 guard convention)
    a_end = min(word_end, len(a))
    a_seg = a[:a_end].copy()
    g = min(int(0.002 * sr), len(a_seg))
    if g > 1:
        a_seg[-g:] *= np.cos(0.5 * np.pi * np.linspace(0, 1, g))
    mix[:a_end] += a_seg
    # b enters with its word in unison (b may start before mix 0)
    b0 = max(0, offset)
    bs0 = max(0, -offset)
    n_b = min(len(b) - bs0, total - b0)
    if n_b > 0:
        mix[b0:b0 + n_b] += b[bs0:bs0 + n_b]

    if exit == "echo_out":
        # echo tail on a's word while b takes over
        tail = dsp.feedback_delay(a[max(0, a_wn - int(beat_s * sr)):word_end],
                                  sr, delay_s=beat_s / 2, feedback=0.5,
                                  wet=0.5)
        t0 = max(0, word_end - int(beat_s * sr))
        n_t = min(len(tail), total - t0)
        if n_t > 0:
            mix[t0:t0 + n_t] += tail[:n_t] * 0.5
    elif exit == "hard_cut":
        # a already ends at word_end; b owns the mix from here. Nothing
        # more to do — the cut is the statement (T-030).
        pass
    else:
        raise ValueError(f"unknown wordplay exit: {exit!r}")

    # b's post-word continuation is already in the mix via the unison
    # overlay; nothing more to do.
    return mix


# ----------------------------------------------------------------------------
# T-009 — Build-to-Drop (dual-build layering)
# ----------------------------------------------------------------------------

def build_to_drop(a_build, b_build, sr, bar_s, build_bars=16,
                  wash_start_bar=9, pre_drop_cut_beats=1.0):
    """Layer two build-ups, fuse them, drop the incoming track.

    a_build / b_build: build sections, each build_bars long. b_build should
    EXTEND past the build into its drop (caller supplies build+drop).
    Build detection (where each build starts, 8 vs 16 bars) is the caller's
    job — the ADAPT caveat in T-009.

    Bars 1-8: b's build at 100% fader but low EQ killed — blends into a.
    wash_start_bar..build_bars: HPF washes a into the background.
    Last pre_drop_cut_beats: a cut to 0 (step).
    Bar build_bars+1 beat 1: b's drop at full.
    """
    a = np.asarray(a_build, dtype=np.float64)
    b = np.asarray(b_build, dtype=np.float64)
    n = int(build_bars * bar_s * sr)
    a = a[:n] if len(a) >= n else np.pad(a, (0, n - len(a)))
    # b keeps its drop tail
    if len(b) < n:
        b = np.pad(b, (0, n - len(b)))

    bb = float(build_bars)
    B_LO_OPEN = bb * 8 / 32 * 2  # b's lows open halfway through (bar 8)
    # --- b: fader 100%, lows killed for first 8 bars ---
    b_lo = _db_envelope(n, bar_s, sr,
                        [(0, KILL_DB), (B_LO_OPEN, KILL_DB),
                         (B_LO_OPEN + 2, 0.0), (bb, 0.0)])
    b_proc = dsp.apply_3band_eq(b[:n], sr, b_lo,
                                np.zeros(n), np.zeros(n))

    # --- a: HPF wash from wash_start_bar, step-cut before the drop ---
    wash_n = n
    cutoff = np.full(wash_n, 40.0)
    w0 = int(wash_start_bar * bar_s * sr)
    if w0 < wash_n:
        u = np.linspace(0, 1, wash_n - w0)
        cutoff[w0:] = 40.0 * (200.0 ** u)  # 40 Hz -> 8 kHz log sweep
    a_washed = dsp.sweep_filter(a, sr, cutoff, ftype="highpass")
    cut_at = int((bb - pre_drop_cut_beats / 4.0) * bar_s * sr)
    cut_at = min(max(0, cut_at), n)
    a_washed[cut_at:] = 0.0

    total = max(n, len(b))
    mix = np.zeros(total)
    mix[:n] += a_washed + b_proc
    # b's drop tail past the build (already full level)
    if len(b) > n:
        mix[n:len(b)] += b[n:]
    return mix


# ----------------------------------------------------------------------------
# T-020 — 3-Deck Layering (glue layer)
# ----------------------------------------------------------------------------

def three_deck_layer(a, b, glue, sr, bar_s, swap_bar=16, glue_in_bars=16,
                    glue_out_bars=16, glue_level=0.75):
    """Two primaries + a persistent high-passed glue layer.

    a owns the lows until swap_bar; b enters with lows killed and takes
    full bass at the swap; glue (percussion loop / pad / chant) rides
    high-passed at glue_level through the whole transition zone so the
    energy floor never dips. Tri-partite frequency slotting: no two decks
    own the same band.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    glue = np.asarray(glue, dtype=np.float64)

    swap_n = int(swap_bar * bar_s * sr)
    pre_n = int(glue_in_bars * bar_s * sr)
    post_n = int(glue_out_bars * bar_s * sr)
    total = swap_n + post_n
    # pad inputs to the timeline
    def _pad(x, nn):
        return x[:nn] if len(x) >= nn else np.pad(x, (0, nn - len(x)))
    a = _pad(a, swap_n + int(bar_s * sr))  # a needs 1 extra bar for exit fade
    b = _pad(b, total)
    glue = _pad(glue, total)

    mix = np.zeros(total)
    # --- a: full until swap, 1-beat exit fade (glue covers the seam) ---
    a_env = np.ones(swap_n)
    beat_n = int(bar_s * sr / 4)
    f0 = max(0, swap_n - beat_n)
    a_env[f0:] = np.linspace(1, 0, swap_n - f0)
    mix[:swap_n] += a[:swap_n] * a_env

    # --- b: lows killed until swap (bass swap moment), then full ---
    b_lo = np.where(np.arange(total) < swap_n, KILL_DB, 0.0)
    b_eq = dsp.apply_3band_eq(b, sr, b_lo, np.zeros(total), np.zeros(total))
    # b fades in over the first 4 bars of the zone
    b_in = np.ones(total)
    fi = min(int(4 * bar_s * sr), total)
    b_in[:fi] = np.linspace(0, 1, fi)
    mix += b_eq * b_in

    # --- glue: high-passed, in 4 bars, out over last 4 of the ride ---
    from scipy import signal as _sig
    sos = _sig.butter(2, 5000.0, btype="highpass", fs=sr, output="sos")
    glue_hp = _sig.sosfilt(sos, glue) * glue_level
    g_env = np.zeros(total)
    gi = min(int(4 * bar_s * sr), total)
    g_env[:gi] = np.linspace(0, 1, gi)
    g_env[gi:swap_n + post_n - gi] = 1.0
    tail = slice(max(gi, swap_n + post_n - gi), total)
    tlen = total - max(gi, swap_n + post_n - gi)
    if tlen > 0:
        g_env[tail] = np.linspace(1, 0, tlen)
    mix += glue_hp * g_env
    return mix


# ----------------------------------------------------------------------------
# T-028 — Beat Jump (phrase-realignment planning primitive)
# ----------------------------------------------------------------------------

def beat_jump(b_full, sr, bpm, cue_t, jump_beats=32):
    """Teleport b's playhead by an exact bar multiple so drops align.

    b_full: the incoming track audio (longer than needed).
    cue_t: current cue position in seconds.
    jump_beats: signed beat count; +32 jumps forward 8 bars, -32 jumps
        back 8 bars (extends a short intro). MUST be a multiple of 32
        beats (8 bars) or phrasing breaks — a warning is printed otherwise.

    Returns (jumped_segment_start_sample, applied_beats). The caller cuts
    b from the returned sample; the jump itself is pure playhead
    arithmetic — the engine's phrase grid makes it trivial, which is the
    point: pre-compute the offset instead of hoping intros match.
    """
    if jump_beats % 32 != 0:
        print(f"    beat_jump WARNING: {jump_beats} beats is not a multiple "
              f"of 8 bars — phrasing will break")
    beat_s = 60.0 / bpm
    start_s = cue_t + jump_beats * beat_s
    start_n = int(start_s * sr)
    if start_n < 0:
        print(f"    beat_jump WARNING: jump lands before track start; "
              f"clamped to 0")
        start_n = 0
    if start_n >= len(b_full):
        raise ValueError("beat_jump lands past the end of the track")
    return start_n, jump_beats


def beat_jump_transition(a, b_full, sr, bpm, bar_s, cue_t, jump_beats=32,
                         play_bars=8):
    """Render a beat-jump repair: a plays, b enters from the jumped cue,
    drops aligned via hard cut."""
    start_n, _ = beat_jump(b_full, sr, bpm, cue_t, jump_beats)
    n = int(play_bars * bar_s * sr)
    a_seg = a[:n] if len(a) >= n else np.pad(a, (0, n - len(a)))
    b_seg = b_full[start_n:start_n + n]
    if len(b_seg) < n:
        b_seg = np.pad(b_seg, (0, n - len(b_seg)))
    return hard_cut(a_seg, b_seg, sr)


# ----------------------------------------------------------------------------
# T-032 — Pitch-Play (key-shifted vocal overlay)
# ----------------------------------------------------------------------------

def pitch_play(vocal, backing, sr, bar_s, semitones=1, overlay_bars=8):
    """Shift the incoming vocal by integer semitones into the backing track's
    key, then overlay it (T-010 mechanics).

    |semitones| <= 2 enforced — beyond that formants shift into the
    chipmunk/demonic uncanny valley (bank rule). Shift is NOT
    formant-preserving (dsp.pitch_shift documents this).
    """
    if abs(semitones) > 2:
        raise ValueError(f"pitch_play: |{semitones}| > 2 semitones — "
                         f"formant uncanny valley (T-032 bank rule)")
    vocal = np.asarray(vocal, dtype=np.float64)
    backing = np.asarray(backing, dtype=np.float64)
    n = int(overlay_bars * bar_s * sr)
    v = vocal[:n] if len(vocal) >= n else np.pad(vocal, (0, n - len(vocal)))
    bk = backing[:n] if len(backing) >= n else np.pad(backing, (0, n - len(backing)))

    shifted = dsp.pitch_shift(v, sr, semitones)
    # T-010 EQ preset: low killed, highs tamed, mids flat
    v_eq = dsp.apply_3band_eq(shifted, sr, KILL_DB, 0.0, -3.0)
    # ride in/out over 2 bars each end
    env = np.ones(n)
    fi = min(int(2 * bar_s * sr), n // 2)
    env[:fi] = np.linspace(0, 1, fi)
    env[-fi:] = np.linspace(1, 0, fi)
    return bk + v_eq * env * 0.9


# ----------------------------------------------------------------------------
# T-039 — Screwed Treatment (chopped & screwed / slowed / 2x-speed)
# ----------------------------------------------------------------------------

def screwed_treatment(x, sr, bpm=None, rate=0.7, pitch_coupled=True,
                      chop_every_beats=0, chop_repeats=2):
    """Chopped-and-screwed style track treatment (pre-transition).

    The idea IS the treatment (note ideas #20, #27, #39): slow the track
    down DJ-Screw style, optionally with chop/retrigger stutters.

    Parameters
    ----------
    rate : playback rate (< 1 = slowed, > 1 = sped up). Classic screw zone
        is 0.6-0.8.
    pitch_coupled : True (default) = vinyl-style — pitch drops WITH tempo
        (the authentic Screw sound). False = phase-vocoder slowdown,
        tempo drops but pitch holds ("slowed + reverb" style).
    chop_every_beats : 0 = no chop; else every N beats the last beat
        retriggers `chop_repeats` times (the chop). Needs bpm.
    bpm : required when chopping.
    """
    x = np.asarray(x, dtype=np.float64)
    if rate <= 0:
        raise ValueError("screwed_treatment: rate must be > 0")
    if chop_every_beats and bpm is None:
        raise ValueError("screwed_treatment: bpm required for chopping")

    if pitch_coupled:
        n_out = int(len(x) / rate)
        y = dsp.warp_resample(x, sr,
                              np.full(n_out, rate), out_len=n_out)
    else:
        y = dsp.phase_vocoder_stretch(x, sr, 1.0 / rate)
        n_out = len(y)

    if chop_every_beats:
        beat_n = int(60.0 / bpm * sr)
        every_n = int(chop_every_beats * beat_n)
        out = []
        pos = 0
        while pos < n_out:
            chunk_end = min(pos + every_n, n_out)
            out.append(y[pos:chunk_end])
            # retrigger the last beat chop_repeats times
            if chunk_end < n_out:
                cb0 = max(pos, chunk_end - beat_n)
                chop = y[cb0:chunk_end]
                for _ in range(chop_repeats):
                    out.append(chop)
            pos = chunk_end
        y = np.concatenate(out) if out else y
    return y
