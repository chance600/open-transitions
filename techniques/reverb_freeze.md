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


## Axis (Phase 26, software/hardware tranche A)

**Tails-only break (SP-404MKII MUTE BUS)** — the freeze's
decaying sibling: with a wet chain running on BUS 1/2, [SHIFT]+
[BUS FX] mutes the bus INPUT ("the input to BUS 1 and BUS 2 is
muted... only the reverberations or delay sound are heard") —
the pre-existing tail sounds *alone* in a void window, decaying,
where this base's freeze *sustains* its tail by recirculation.
On release the input returns AND the bus effect switches off at
the same time, so re-entry is clean dry signal with the chain
reset — the state-clear is part of the gesture. Roland frames it
as "an effective performance technique" for "expressive breaks".
Scope is ALL buses or a selected bus. Evidence: SP-404MKII
Reference v5.5, BUS FX pages, fetched 2026-10-23.
