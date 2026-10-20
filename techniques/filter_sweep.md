# filter_sweep

**Bank:** T-003 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT), MusicRadar

## Signature

```python
filter_sweep(a, b, sr, bar_s, tease_bars=8, sweep_bars=7)
```

## Spec

A thins out under HPF while B opens up; snap B open on the downbeat.

a: outgoing (tease_bars + sweep_bars + 1 bars). b: incoming, same length,
pre-filtered to thin top-end during the tease (caller may pass full b;
the tease HPF is applied here).
Returns mix of length (tease+sweep+1) bars; B fully open at the drop bar.
