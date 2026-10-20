# harmonic_mix

**Bank:** T-015 · **Automatability:** ADOPT · **Confidence:** high

**Source:** Camelot wheel; pure decision function over key codes

## Signature

```python
harmonic_mix(key_a, key_b)
```

## Spec

Camelot compatibility check. Keys like "8A" (minor) / "8B" (major).

The four legal moves: same key (perfect), +/-1 step (bread and butter,
~80% of pro harmonic sets), relative major/minor (same number, mood
flips), +2 energy boost (sparingly). Wheel wraps 12 <-> 1.
Returns {"compatible": bool, "move": str}.
