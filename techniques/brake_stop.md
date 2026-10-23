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


## Axis (Phase 26, software/hardware tranche A)

**VINYL BRAKE staging (DJM-V10)** — Pioneer's Beat FX form of
this base, banked as its staging ground truth rather than a new
base (same mechanism: rate ramps to a full stop, pitch coupled):
the stop is beat-quantised (1/16–16 beats, 10–4000 ms) and
LEVEL/DEPTH *is* the playback-speed control — the performer can
scrub the rate by hand instead of firing a fixed curve. This
base's curve presets are the automated form of that scrub.
Evidence: DJM-V10 manual via manua.ls, p65, fetched 2026-10-23.
