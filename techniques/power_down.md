# power_down

**Bank:** T-013 · **Automatability:** ADOPT · **Confidence:** high

**Source:** standard turntablist technique; curve shape is the tuning parameter

## Signature

```python
power_down(a, sr, bpm, down_beats=1.5, curve='linear', tail_pad_beats=1.0)
```

## Spec

Drag the pitch fader 0 -> -100%: the track slows AND drops in pitch
over down_beats, dying into a low growl. Longer and more manual than
T-006 — the track "runs out of life".

Often paired with a reverb/echo tail so the death isn't followed by
true silence (or deliberately IS, for maximum contrast).
