# reverb_freeze

**Bank:** T-034 · **Automatability:** ADOPT · **Confidence:** high

**Source:** DJM-V10 freeze translated to software parameters; first written recipe

## Signature

```python
reverb_freeze(a, b, sr, bar_s, bpm, freeze_bars=2, void_beats=3, decay_s=8.0, release_bars=4)
```

## Spec

Halt time with a frozen reverb tail, launch B inside it, release.

a: outgoing; its last freeze_bars feed the freeze.
The freeze: reverb send to 100% wet with a long decay while the dry
fader falls — the tail stops decaying and a smeared chord hangs,
harmonically static but texturally alive (holds A's key with no rhythm).
void_beats of limbo, then B's first beat lands INSIDE the tail; the
freeze releases over release_bars as B plays.
Software freeze (no freeze button): decay -> long + input killed — the
existing tail recirculates.
