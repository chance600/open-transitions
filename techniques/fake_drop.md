# fake_drop

**Bank:** T-029 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** null-set-ai-dj (MIT); human-triggered weapon, never auto-deployed

## Signature

```python
fake_drop(a, b, sr, bpm, void_beats=3.0, interlude=None)
```

## Spec

Build to the drop, then DON'T: 2-4 beats of void, then the real drop.

a: outgoing build, ends at the rug-pull point (bar 17 beat 1 equivalent).
void_beats: 2-4 beats of zero audio. The crowd's screams fill the club.
interlude: optional dry one-shot (e.g. a vocal quip) placed at the
    void's start, in samples (mono array) or None.
b: the real drop, slams after the void.
Human-triggered weapon — the engine renders it, never auto-deploys it.
