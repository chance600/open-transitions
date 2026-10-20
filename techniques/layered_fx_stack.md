# layered_fx_stack

**Bank:** T-017 · **Automatability:** ADOPT · **Confidence:** high

**Source:** VirtualDJ mapping community, ProDJ School, Club Ready

## Signature

```python
layered_fx_stack(a, b, sr, bar_s, bpm, echo_bars=8, filter_bars=4, reverb_bars=2, enter_bars=4)
```

## Spec

The upgrade path from a flat T-004: stack echo (time), HPF (frequency)
and reverb (space) on the outgoing track so it has nowhere left to exist.

Order: echo ON at -echo_bars, HPF sweep starts at -filter_bars,
reverb send opens at -reverb_bars, fader kill on the 1. B enters over
-enter_bars with a mirror filter opening.
Each FX attacks a different perceptual dimension — a single FX leaves
the others intact, which is why plain echo-outs can feel abrupt.
