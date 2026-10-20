# loop_juggle_replace

**Bank:** T-031 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** djwes/ausdjforums (The Replace); digital hot-cue adaptation

## Signature

```python
loop_juggle_replace(a_bar, b_bar, b_full, sr, bpm, cycles=4)
```

## Spec

Turntablist beat-juggling as a transition: steal the groove hit by
hit. Each 1-bar cycle: A plays beats 1-3, B's loop-start replaces beat 4.
On the final cycle, B re-establishes the downbeat from its first kick.

a_bar, b_bar: 1-bar loops (caller-provided, beatmatched).
b_full: B from its phrase start (first kick) — takes over after.
Digital adaptation: hot cues replace rewinds (instant, quantized).
