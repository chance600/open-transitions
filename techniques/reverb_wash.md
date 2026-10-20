# reverb_wash

**Bank:** T-005 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT), MusicRadar

## Signature

```python
reverb_wash(a, b, sr, bar_s, wash_start_bar=4, b_start_bar=6, wet_max=0.7)
```

## Spec

Dissolve `a` into reverb from wash_start_bar; `b` emerges at b_start_bar.

a: outgoing segment (bars). b: incoming segment, aligned so its bar 0
coincides with a's b_start_bar.
