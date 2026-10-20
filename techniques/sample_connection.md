# sample_connection

**Bank:** GAP-01 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Transition Gap Report 2026-10-19 GAP-01 — DDT + open-format (sample connection / sample switch-up)

## Signature

```python
sample_connection(a, b, sr, bpm, hit_t, hit_len_s=0.5)
```

## Spec

Hot-cue swap from A into the track that samples it, at the shared hit.

a plays through the shared sampled element (starting at hit_t, length
hit_len_s, default 0.5 s); the hit then retriggers twice in rhythmic
unison, and B enters from its own statement of that element — caller
aligns b so the element starts at sample 0; the second retrigger
crossfades (equal-power) into B's head.

Wordplay (T-011) chains lyric *words*; this chains *source material*.
The ear recognises the sampled element as the same object in both
tracks, so the retriggers read as call-and-response and the swap
lands as revelation, not as a cut.
