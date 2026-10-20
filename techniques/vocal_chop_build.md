# vocal_chop_build

**Bank:** T-033 · **Automatability:** ADOPT · **Confidence:** high

**Source:** MusicRadar, DJ Carlo cue-drumming lineage

## Signature

```python
vocal_chop_build(a, b, sr, bar_s, chop_t, chop_len_s=1.0, build_bars=8, bp_lo_hz=500.0, bp_hi_hz=5000.0)
```

## Spec

Chop a vocal phrase into a density ladder (1/4 -> 1/8 -> 1/16),
brightening through a band-pass sweep, then hard-cut to B's drop.

a: outgoing (the chop source lives at chop_t).
chop_t: start (seconds) of the vocal phrase to chop.
build_bars: 8 default — bars 1-4 at 1/4-note, 5-6 at 1/8, 7-8 at 1/16.
The silence between the last chop and the drop is < 100 ms (a T-025
micro-void without the vocal hang).
