# hotcue_drop_swap

**Bank:** T-014 · **Automatability:** ADOPT · **Confidence:** high

**Source:** Virtual Clubbing Life (4-beats-before-the-drop)

## Signature

```python
hotcue_drop_swap(a, b, sr, bpm, xfade_beats=4)
```

## Spec

Replace A's drop with B's: volume cross-swap over the run-up.

a: outgoing, ends at its drop point (the last xfade_beats are the
    "1-2-3-DROP" run-up).
b: incoming, STARTS at its own run-up (hot cue = drop - 4 beats;
    caller aligns).
Equal-power swap over xfade_beats; optional echo/filter layered by
the caller for style.
