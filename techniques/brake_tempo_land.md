# brake_tempo_land

**Bank:** WEB-37 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Serato forum, mister_wilson, "transition between genres / huge tempo gaps", trick 2 — "set the braking speed such that the fast track will slow from its tempo to roughly the tempo of the next track in two beats (or four beats for more drama). Start braking the track an eighth note after the two beat (or an eighth note after the four beat for the more dramatic method). Start the slower track on the 1"; https://serato.com/forum/discussion/28193, fetched first-hand 2026-10-25.

## Signature

```python
brake_tempo_land(a, b, sr, bpm, land_beats=2, target_ratio=0.8)
```

`brake_tempo_land` — family DYN, exit snap, energy delta 0 (falling tension).

## Spec

A brakes from its tempo to B's tempo over N beats; B starts on the 1.

    Rendered: A's last `land_beats` beats play back with a
    linearly falling rate (1.0 -> `target_ratio`, turntable
    physics: pitch and time slow together) via resampling;
    the eighth-note start offset is absorbed into the window
    edge (performance detail, inaudible at sketch scale); B
    starts full on the 1 after the braked window. The brake
    lands ON a tempo, not on silence — that is the whole
    difference from a stop.

    Why it is not its neighbours: not `brake_stop` (brakes to
    zero — a stop, not a landing); not T-013 `power_down` (a
    manual drag to zero, longer and unmetered — here the brake
    is metered to a target tempo over a counted beat span);
    not WEB-32 `bed_tempo_switch` (a bed covers the jump — here
    the outgoing track itself becomes the new tempo).

## Parameters

- `land_beats` (int, 1–8, default 2): brake span in beats. 2
  is the source's standard; 4 is the dramatic staging.
- `target_ratio` (float, 0.5–0.95, default 0.8): end rate as a
  fraction of A's rate. 0.9 is gentle, 0.7 deep.

## Selection

Requires: no BPM or key gate (the brake IS the tempo move),
vocal pair any, A's phrase outro / chorus / verse, genre pair
same / neighbor / leap, no needs.
Prefers: BPM delta ≥ 5% (+2, the brake IS the tempo move —
a small gap wastes a counted brake).
