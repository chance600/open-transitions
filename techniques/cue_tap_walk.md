# cue_tap_walk

**Bank:** WEB-36 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Serato forum, mister_wilson, "transition between genres / huge tempo gaps", trick 1 — "set a cue point in the slow track... maybe just a kick drum or a more recognizable part of the track intro. When ready to transition I simply tap the cue button on the second track to the beat of the first track and bring up the volume of the second track. I can then cut the first track and start slowly hitting the cue button at a slower tempo until I roughly match the tempo of the second track"; https://serato.com/forum/discussion/28193, fetched first-hand 2026-10-25.

## Signature

```python
cue_tap_walk(a, b, sr, bar_s, bpm, taps=4, walk_beats=4)
```

`cue_tap_walk` — family PERF, exit snap, energy delta 0 (rising tension).

## Spec

B's cue tapped to A's beat, then the taps decelerate to B's tempo and B plays from the cue.

    Rendered: B's first beat (the cue) sounds `taps` times at
    A's beat grid while A fades out; then `walk_beats`
    further cue taps arrive at stretching intervals (×1.2 per
    tap in the sketch — the real stretch ratio is caller
    context, the sketch proves the tap-deceleration shape, cf.
    WEB-32's fixed-BPM caveat); then B plays full from the
    cue. Each tap restarts the cue — the playhead never
    advances past it until the walk ends, which is the whole
    mechanism.

    Why it is not its neighbours: not T-030 `hard_cut` (the
    cut alone has no tempo negotiation — the taps ARE the
    negotiation); not WEB-35 `loop_click_bridge` (a loop cycles
    freely — taps are discrete, hand-triggered restarts);
    not T-008 `loop_roll_build` (a roll builds — taps walk).

## Parameters

- `taps` (int, 1–8, default 4): cue taps at A's tempo. 2 is a
  double, 8 long.
- `walk_beats` (int, 1–8, default 4): decelerating cue taps.
  2 is quick, 8 long.

## Selection

Requires: no BPM or key gate (hand-walked negotiation covers
the gap), vocal pair any, A's phrase outro / chorus, genre
pair same / neighbor / leap, no needs.
Prefers: genre leap (+2, hand-walked tempo negotiation — the
taps replace the pitch fader across a gap).
