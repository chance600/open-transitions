# slip_mode_flourish

**Bank:** GAP-05 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Transition Gap Report 2026-10-19 GAP-05 — open-format (slip-mode flourish, general)

## Signature

```python
slip_mode_flourish(a, sr, bpm, flourish_beats=1.0)
```

## Spec

Slip engaged as a general safety net: a live flourish — a reversed
snippet of A's own next beat (flourish_beats, default 1.0 beat)
followed by a spin chirp (exponential pitch-dive of the same snippet
over 1/2 beat) — rides over A's continuing drums at -6 dB. A itself
is never interrupted: the playhead keeps advancing under the
flourish, so release lands back in phrase by construction.

The library used slip only inside T-008's roll build. As a general
tool, slip decouples performance from risk: any gesture can be thrown
live because the underlying phrase never moved — the worst case is
an odd beat, never a trainwreck.
