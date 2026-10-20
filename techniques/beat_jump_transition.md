# beat_jump_transition

**Bank:** T-028 · **Automatability:** ADOPT · **Confidence:** high

**Source:** rendered demo of the beat_jump repair primitive

## Signature

```python
beat_jump_transition(a, b_full, sr, bpm, bar_s, cue_t, jump_beats=32, play_bars=8)
```

## Spec

Render a beat-jump repair: a plays, b enters from the jumped cue,
drops aligned via hard cut.
