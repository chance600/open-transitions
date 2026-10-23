# backspin

**Bank:** T-007 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** null-set-ai-dj (MIT); flick force is feel — 1-beat default

## Signature

```python
backspin(a, b, sr, bpm, spin_beats=1.0, src_beats=2.0)
```

## Spec

Fling the jog wheel backward on beat 4; slam B on the next downbeat.

The reversed audio decays exponentially over exactly spin_beats
(~1 beat: long enough to read as a rewind, short enough not to kill
momentum). Vinyl Mode assumed — this is the digital equivalent.


## Axis (Phase 26, software/hardware tranche A)

**Back Spin ground truth (SP-404MKII)** — Roland's form fixes
this base's staging numbers: LENGTH is in BEAT DIVISIONS
(1/1–1/16), SPEED 0–100, and the gesture has a *charge*: the
sample must play for roughly 3 seconds before BACK SW can fire
— a backspin is armed, not instant. DJ-mode rolls cannot exceed
the sample length, the same physical bound. Evidence:
SP-404MKII Reference v5.5, Back Spin / DJ Mode pages, fetched
2026-10-23.
