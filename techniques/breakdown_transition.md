# breakdown_transition

**Bank:** T-023 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT)

## Signature

```python
breakdown_transition(a, b, sr, bar_s, bpm_from=None, bpm_to=None, blend_bars=16)
```

## Spec

Execute the whole transition inside A's breakdown.

a: A's breakdown segment (kick dropped out; pads/piano/vocal remain).
b: B's melodic intro/breakdown.
With no drums there is no beatmatching constraint and no audible tempo
reference — bpm_from -> bpm_to slides over the blend (pitch-preserving;
drumless audio stretches cleanly). Blend with mid/high EQs only.
