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
