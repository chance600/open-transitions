# beat_jump

**Bank:** T-028 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT); Coach Hapa 4-step; planning primitive — pure playhead arithmetic

## Signature

```python
beat_jump(b_full, sr, bpm, cue_t, jump_beats=32)
```

## Spec

Teleport b's playhead by an exact bar multiple so drops align.

b_full: the incoming track audio (longer than needed).
cue_t: current cue position in seconds.
jump_beats: signed beat count; +32 jumps forward 8 bars, -32 jumps
    back 8 bars (extends a short intro). MUST be a multiple of 32
    beats (8 bars) or phrasing breaks — a warning is printed otherwise.

Returns (jumped_segment_start_sample, applied_beats). The caller cuts
b from the returned sample; the jump itself is pure playhead
arithmetic — the engine's phrase grid makes it trivial, which is the
point: pre-compute the offset instead of hoping intros match.
