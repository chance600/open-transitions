# loop_click_bridge

**Bank:** WEB-35 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Serato forum, grotesque, "transition between genres / huge tempo gaps" — "get a track that doesn't start with drums, put a tiny loop on the sound at the start, then when you play the loop it should be like a click track. match the clicking to the track that's playing, fade out the old track then turn the loop off"; https://serato.com/forum/discussion/28193, fetched first-hand 2026-10-25.

## Signature

```python
loop_click_bridge(a, b, sr, bar_s, click_ms=150, click_bars=4)
```

`loop_click_bridge` — family TIME, exit snap, energy delta 0 (flat).

## Spec

A micro-loop of B's non-drum intro becomes a click track matched to A's grid; A fades out, the loop switches off, B plays on.

    Rendered: B's head slice (`click_ms`) tiles back-to-back
    across `click_bars` bars — a loop cycles continuously, so
    the click train never gaps — while A fades out on a cosine
    ramp; at the window end the loop switches off and B
    continues from just past the clicked slice (the loop was
    cycling B's own head, so releasing it lets the intro play
    on — the clicked fragment is not replayed). The click is a
    metronome, not a loop effect: it carries no groove of its
    own, which is why it bridges tempos the beat grids cannot.

    Sketch caveat, stated not hidden: the sketch proves the
    loop-as-metronome structure, not the beat-match — matching
    the clicking to the playing track is the DJ's slice choice,
    caller context (cf. WEB-32's fixed-BPM caveat).

    Why it is not its neighbours: not T-008 `loop_roll_build`
    (a loop that builds tension toward a drop — here the loop
    is a timing utility, then discarded); not WEB-32
    `bed_tempo_switch` (a beatless bed covers the jump — here
    a rhythmic click grids it); not T-020-style glue loops
    (the click never becomes musical material).

## Parameters

- `click_ms` (int, 50–500, default 150): head-slice length in
  ms. 100 is short, 250 long.
- `click_bars` (int, 1–8, default 4): click-track window in
  bars. 2 is tight, 8 long.

## Selection

Requires: no BPM or key gate (the click exists for gaps the
grids cannot negotiate), vocal pair any, A's phrase outro /
verse / chorus, genre pair same / neighbor / leap, no needs.
Prefers: genre leap (+2, the click exists for tempo gaps —
a leap is its home).
