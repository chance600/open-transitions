# riser_drop

**Bank:** — · **Automatability:** ADOPT · **Confidence:** medium

**Source:** engine original: riser synth + HP thinning into a tempo-jump drop

## Signature

```python
riser_drop(a, b, sr, bar_s, riser_bars=8, riser_db=-14.0)
```

## Spec

Riser over the last riser_bars of `a` + HP thinning, hard cut to `b`.

For tempo jumps: the riser/drum-cut masks the BPM change; `b` drops on
the 1 at its own tempo. `a` should end exactly on a phrase boundary.
