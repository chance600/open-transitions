# vocal_punchline_snap

**Bank:** T-025 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT)

## Signature

```python
vocal_punchline_snap(a, b, sr, bpm, lowkill_beat=3.0, void_ms=175.0, isolate_mode='midpass')
```

## Spec

Surgical 2-bar transition: beat 3 kills the lows, beat 4 isolates the
vocal word, 150-200 ms of pure void, then B's drop at unity.

a: outgoing, ends EXACTLY on the drop downbeat (the final bar of a is
    the snap bar; beats are 1-indexed within it).
b: incoming drop, enters at full power (no fade).
lowkill_beat: beat of the final bar where lows die (default 3.0).
void_ms: pre-drop silence, 150-200 ms. This resets the ear's loudness
    adaptation (~200 ms windows) — the drop lands relative to nothing.
isolate_mode: "midpass" (default) — on beat 4, kill low+high bands,
    leaving the vocal band. A full-mix approximation: with stems, pass
    the vocal stem and use "stem" for exact isolation.
