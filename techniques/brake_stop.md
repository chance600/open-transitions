# brake_stop

**Bank:** T-006 · **Automatability:** ADOPT · **Confidence:** high

**Source:** Virtual Clubbing Life (rekordbox brake dial), Cassette Transport

## Signature

```python
brake_stop(a, sr, bpm, stop_beats=0.25, curve='exp', tail_pad_beats=1.0)
```

## Spec

Vinyl-slowing-to-a-halt. Pitch and tempo dive together over
stop_beats (default 1/4 beat — the sweet spot), then the drop.

a: outgoing, ends at the brake point (end of a phrase).
curve: "exp" (brake-dial feel) or "linear" (pitch-fader pull).
Returns a + dived tail + silence pad; caller drops the next track on
the following downbeat.
