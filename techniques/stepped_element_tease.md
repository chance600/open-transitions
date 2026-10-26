# stepped_element_tease

**Bank:** WEB-34 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** DJTechTools forum, djproben, "need advice in mixing technique" — "bring one sound in at a time... four beats at 25% volume, four beats at 50% volume, four beats at 75% volume, then four at 100%, then leave the volume up as you swap the basslines in and pull the volume on track A right at the drop on track B"; https://forum.djtechtools.com/t/need-advice-in-mixing-technique/54216/8, fetched first-hand 2026-10-25.

## Signature

```python
stepped_element_tease(a, b, sr, bar_s, step_beats=4)
```

`stepped_element_tease` — family TIME, exit snap, energy delta 1 (rising).

## Spec

One B element teased in at 25/50/75/100% over 4 beats each, then the bassline swaps and A pulls at B's drop.

    Rendered: B's top layer (one-pole highpass — the hats/vocal
    top the source teases) enters over A at the stepped gains,
    one step per `step_beats` beats; at the ladder's end B —
    which has been running underneath — takes over full from
    that bar onward (the bassline swap + A pull at the drop).
    The ladder, not a continuous fade, is the technique: each
    step is a discrete, audible commitment the crowd can track.

    Why it is not its neighbours: not T-003 `filter_sweep` (a
    continuous filter motion, no stepped ladder, no bass-swap
    payoff); not T-002 `bass_swap` (the swap alone, without the
    stepped tease that earns it); not T-022 `drum_bridge` (a
    drums-only bridge, not a single-element gain ladder).

## Parameters

- `step_beats` (int, 1–8, default 4): beats per ladder step. The
  source's is 4; 2 is the tight staging, 8 the long one.

## Selection

Requires: BPM delta ≤ 10%, no key gate, vocal B-only or
neither (the teased top layer must not fight an A vocal), A's
phrase outro / breakdown / verse / chorus, genre pair same /
neighbor, no needs.
Prefers: A's phrase outro (+2, the ladder earns the drop it
precedes — an outro gives it room without fighting a vocal).
