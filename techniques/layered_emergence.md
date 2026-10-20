# layered_emergence

**Bank:** T-004c · **Automatability:** ADOPT · **Confidence:** high

**Source:** engine original; field-tested on blend 02/03 work

## Signature

```python
layered_emergence(a, b, sr, bpm, bar_s, beat_div=0.5, wet=0.65, feedback=0.62, throw_beats=1, tail_beats=12, thin_start_hz=30.0, thin_end_hz=1200.0, thin_bars=8, riser_bars=8, riser_db=-16.0, hp_start_hz=120.0, hp_open_bars=8, xfade_bars=16, wash_decay=2.5, wash_bed_db=-18.0)
```

## Spec

STACKED transition: multiple DJ tricks layered, each in its own
spectral/temporal slot (v3 of Anchor Point -> Wings).

User verdicts: v1 (echo-out + drop) "too abrupt"; v2 (echo-out-blend)
"still a little abrupt, we need more mixing tricks". The directive is
LAYERING — the way a real DJ stacks moves instead of relying on one.

OUTGOING (a, e.g. Anchor's 8-bar wind-down):
  1. HPF thinning sweep (thin_start_hz -> thin_end_hz, exponential, over
     thin_bars): subtractive — clears low-mid space so the riser, the
     echo, and the incoming track never fight. The track "lifts off".
  2. Riser underneath (riser_bars, peaks EXACTLY at the throw, cut dead
     on the throw): the vacuum after the riser cut makes the incoming
     track's arrival feel EARNED, not just revealed.
  3. Echo throw on the last beat(s) (T-004: lows killed, dry gated,
     feedback tail) — the rhythmic handoff.
TAIL (post-throw):
  4. Wash BLOOM (T-005, time-varying): reverb wet ramps 0->1 over
     bloom_bars as the echo pulses decay — the wash GROWS out of the
     pulse train instead of replacing it at a fixed mix.
INCOMING (b, starts at the throw):
  5. HP opens hp_start_hz -> 20 Hz exponentially over hp_open_bars
     (v2-tuned: 120 Hz keeps body above the silence floor).
  6. Equal-power fade-in over xfade_bars (v2).

Anti-mush design: trick 1 is subtractive (removes energy); the riser is
HP-swept noise living in mids/highs; the echo's lows are killed; the
incoming HP keeps its lows out until the wash has room. Nothing stacks
in the same band at the same time.
