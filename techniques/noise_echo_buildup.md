# noise_echo_buildup

**Bank:** T-018 · **Automatability:** ADOPT · **Confidence:** high

**Source:** ProDJ School (Noise color FX + empty channel + Echo 1/2)

## Signature

```python
noise_echo_buildup(a, b, sr, bar_s, bpm, build_bars=8, noise_db=-16.0, echo_div=0.5, feedback=0.6)
```

## Spec

Build a riser from nothing: white noise + 1/2-beat echo on an empty
channel, raised over build_bars, killed dead on the drop.

a: outgoing; the noise layers over its last build_bars.
The 1/2-beat echo gates the noise into rhythm so it grooves instead of
hissing. The sudden absence of the noise wall makes B's drop hit
harder (contrast principle).
