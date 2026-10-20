# echo_out_blend

**Bank:** T-004b · **Automatability:** ADOPT · **Confidence:** high

**Source:** engine original; field-tested on blend 02/03 work

## Signature

```python
echo_out_blend(a, b, sr, bpm, bar_s, beat_div=0.5, wet=0.65, feedback=0.62, throw_beats=1, tail_beats=12, hp_start_hz=200.0, hp_open_bars=8, xfade_bars=16, diffuse_tail=True, diffuse_wet=0.7, diffuse_decay=1.2)
```

## Spec

Echo throw on outgoing, incoming EMERGES under the tail (no hard drop).

v2 of the Anchor Point -> Wings transition (user verdict: the v1 drop on
the 1 was too abrupt — Wings opens at peak with no intro, so slamming in
reads as a cut, not a blend).

- Outgoing: same T-004 throw as echo_out (lows killed over the throw
  beat(s), dry gated at the throw, feedback tail rings for tail_beats).
- The tail is diffused (Schroeder reverb, post-throw region only): a raw
  feedback tail is a pulse train with deep inter-echo nulls, which reads
  as gating under the emerging track. Diffusion melts it into a continuous
  dubby wash — the bed Wings rises out of.
- Incoming: starts AT the throw, under the tail, with a high-pass at
  hp_start_hz opening exponentially to 20 Hz over hp_open_bars, and an
  equal-power fade-in over xfade_bars.
- Crossfade: equal-power — outgoing side is cos(0.5*pi*u), incoming side
  is sin(0.5*pi*u), both over xfade_bars from the throw. The outgoing
  tail's natural feedback decay dominates the first ~2 bars; the slow
  cos fade just guarantees no residual tail past the blend.

Returns the full mix; b starts at the throw point (overlapping the tail).
