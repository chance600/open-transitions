# instant_double_stutter

**Bank:** WEB-33 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Crossfader, "How To Mix Hip Hop" — instant doubles; https://wearecrossfader.co.uk/blog/how-to-mix-hip-hop/, fetched first-hand 2026-10-24.

## Signature

```python
instant_double_stutter(a, b, sr, bar_s, stutter_bars=2)
```

`instant_double_stutter` — family PERF, exit snap, energy delta +1 (build).

## Spec

One track doubled against itself at a half-beat offset, crossfader-spliced every half beat, then B drops.

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

## Parameters

- `stutter_bars` (int, 1–4, default 2): stuttered region at A's
  end in bars. 1 is the tight stab staging; 4 is the extended
  doubling sequence.

## Selection

Requires: BPM delta ≤ 10%, Camelot distance ≤ 3, vocal pair
any, A's phrase outro / verse / chorus / drop, genre pair
same / neighbor, no needs.
Prefers: A iconic vocal (+2, the stutter effect lands hardest
on vocals — an iconic A vocal doubles against itself); energy
delta ≥ 1 (+1, the stutter builds tension into a
higher-energy drop).

## Demo

`demos/ext_genre.py`: A's final 2 bars replaced by the
half-beat dual-stream splice; B enters full at 8 bars.
Handoff = the drop. Sketch caveat: stemsB carries no vocal
hook, so the demo's stuttered content is A's own hook bars —
the doubling mechanism, not a vocal stutter, is what renders.

## Variants

`stutter_bars` presets 1bar / 2bar / 4bar → 3 variants (single-axis base).
