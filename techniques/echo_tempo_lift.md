# echo_tempo_lift

**Bank:** WEB-39 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Serato forum, mister_wilson — "I make the slower track echo/repeat at 3/4 beat length. The echo has a tempo that is 33% faster than the original. You still need to do some beat matching but it can work in a pinch"; https://serato.com/forum/discussion/28193, fetched first-hand 2026-10-26. Named in Phase 28 and deliberately not landed there — it needs a tempo-measurement staging the sketch pipeline could not yet prove; the staging is proven in Phase 31 (see below).

## Signature

```python
echo_tempo_lift(a, b, sr, bar_s, bpm, tail_repeats=8, delay_beats=0.75)
```

`echo_tempo_lift` — family TIME, exit snap, energy delta 1 (rising).

## Spec

A slow -> fast bridge: A's tail echoes on a grid whose repeat rate IS the new tempo, then B drops on the grid.

    Rendered: A plays to its end, then its final `delay_beats`
    fragment repeats alone, feedback-decaying (0.80 per repeat
    — the grid must stay audible across all repeats),
    for `tail_repeats` repeats — the grid establishes itself in
    the open, with nothing underneath — and B drops full on the
    next repeat boundary, the tail cut dead at the handoff. The
    arithmetic is the technique: repeats spaced `delay_beats` of
    a beat apart recur at bpm / delay_beats, so a 3/4-beat echo
    on a 90 BPM track implies 120 BPM. The tail alone is the
    bridge: no bed, no brake, no click track.

    Why it is not its neighbours: not WEB-01 `spiral_echo`
    (the spiral's repeats pitch-ride and decay UNDER B's
    entrance — an exit, with no tempo claim and no B-on-grid
    drop); not WEB-38 `delay_drum_roll` (a 1/2-beat send that
    fakes density at the SAME tempo and slams shut before B —
    a roll, not a grid redefinition); not WEB-32
    `bed_tempo_switch` (a beatless bed covers the jump — here
    the grid itself is the bridge); not WEB-35
    `loop_click_bridge` (the click is B's own intro tiled as a
    metronome — here the grid is A's echo, thrown before B
    exists in the mix); not WEB-37 `brake_tempo_land` (a counted
    brake, fast -> slow — this is the slow -> fast direction,
    which the registry's tempo-gap family covered only via bed
    and click until now).

    The tempo-measurement staging (the Phase 28 hold, cleared
    in Phase 31): the grid is not asserted from the delay
    parameter — it is measured from the rendered tail. Correlating
    the rendered tail against the thrown fragment peaks at
    multiples of the 3/4-beat delay, and the measured inter-peak
    interval implies bpm / 0.75: the shipped demo wav (128 BPM
    grid) measures peak lags at exact multiples of 15504 samples
    with correlation 1.0, implying 170.67 BPM vs 170.67 nominal
    (error 0.001%), and a fresh 90 BPM render measures 120.0 vs
    120 nominal (error 0.0%); half-delay off-grid controls read
    -0.26 / -0.00. Full method + script: BUILD-LOG Phase 31 and
    transition-lab/work/echo_grid_measure.py.
    The sketch proves the grid arithmetic, not the lift: whether
    a room hears a tempo lift rather than a dotted delay is a
    listening verdict, and the source's own caveat stands — the
    DJ still has to beat-match B onto the grid; the echo does
    not do the matching.

## Parameters

- `tail_repeats` (int, 1–16, default 8): repeats rung alone
  before B. 4 is short, 8 the standard — six beats of grid at
  3/4, enough to establish it.
- `delay_beats` (float, 0.25–1.0, default 0.75): echo division
  in beats. 0.75 is the source's 3/4 (+33% lift); 0.5 is the
  double-tempo variant (+100%).

## Selection

Requires: no BPM gate (the lift IS the gap device), no key
gate, vocal pair any, A's phrase outro / chorus,
genre pair same / neighbor / leap, no needs.
Prefers: genre pair leap (+2, the echo grid is the tempo
bridge — a leap pair is its home); BPM delta ≥ 20% (+1, a grid
redefinition pays on a real gap, not a nudge).
