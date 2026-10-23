# echo_out

**Bank:** T-004 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT), DJ Carlo Atendido, MusicRadar

## Signature

```python
echo_out(a, sr, bpm, beat_div=0.5, wet=0.6, feedback=0.55, tail_beats=4)
```

## Spec

Echo throw on the final beat of `a`, post-fader tail.

- Low EQ killed over the throw beat (avoids boomy rumble).
- Input gate cuts at the throw (fader to 0); feedback loop rings on.
- Returns a + tail_beats of pure tail appended.


## Axes (Phase 26, software/hardware tranche A)

**Stem-mute echo tail (djay Mute FX)** — Algoriddim's Mute FX
turns this base's throw into a *stem event*: "replacing abrupt
cuts with smooth echo tails when you mute or solo Neural Mix™
stems", the tail starting on the beat or a subdivision —
quantised to 1, ¾, or ½ beat (the ¾ length is the fingerprint).
Staged here: the throw fires on a single stem's mute/solo while
the other stems continue or cut dry; the tail is that stem's echo
only. Evidence: djay Pro help, Neural Mix / Mute FX pages,
fetched 2026-10-23.

**Per-repeat damping tables (SP-404MKII Sync Delay / SX Delay /
Ko-Da-Ma)** — Roland's delays parameterise what this base leaves
as one damping choice: TIME spans tempo divisions 1/32–1/1
including triplets and dotted values; each repeat passes L DAMP
F (FLAT / 80–800 Hz) and H DAMP F (630–12500 Hz / FLAT), so the
darkening *trajectory* is staged per band edge, not per repeat
count. Ko-Da-Ma adds a SEND staging and a SINGLE/PAN placement
axis. The DJM-V10's SEND SHORT/LONG DELAYs are this same family
by the mirror manual (knob semantics only — no ranges stated).
Evidence: SP-404MKII Reference v5.5, delay MFX pages; DJM-V10
manual via manua.ls, p49 — fetched 2026-10-23.
