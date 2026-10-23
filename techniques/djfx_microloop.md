# djfx_microloop

**Bank:** WEB-26 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Roland SP-404MKII Reference v5.5 (official) — DJFX Looper BUS FX page (complete BUS FX cluster read first-hand); fetched 2026-10-23.

## Signature

```python
djfx_microloop(a, b, sr, bpm, bar_s, length_ms=120.0, mode='reverse', loop_bars=2, fade_beats=1)
```

`djfx_microloop` — family TIME, exit snap, energy delta 0 (build).

## Spec

A 12-230 ms grain of A, performed like a turntable.

    The SP-404MKII's DJFX Looper "loops the sound in short cycles.
    You can vary the playback direction and playback speed of the
    input sound to get a turntable-type effect": LENGTH is
    0.230-0.012 SECONDS (absolute time, not a beat grid) and SPEED
    is -100..100 — "plays backward when negative, stops when
    zero, plays forward when positive".

    Rendered as a transition: A's final `loop_bars` are replaced
    by the performance. The grain — A's last `length_ms` before
    the window — loops while the read rate sweeps by `mode`:
    "reverse" sweeps +1 -> -1 (through the stop instant into
    backward play), "stop" eases +1 -> 0 (the grain crawls to a
    standstill), "hold" parks the rate at +0.25 (a slow drag of
    the same grain). B then enters, faded over `fade_beats`.

    Why it is not its neighbours: not `loop_roll_build` T-008 (a
    beat-quantised roll that TIGHTENS through subdivisions — it
    never runs at sub-beat absolute lengths, never reverses, never
    freezes at rate 0); not `granular_freeze` WEB-06 (a sustained
    texture cloud — no directional varispeed performance of a
    single captured grain); not `backspin` T-007 (a one-shot
    reverse gesture on the whole record, not a captured loop).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity; the
        grain length is deliberately NOT derived from it).
    bar_s : seconds per bar.
    length_ms : grain length in milliseconds (default 120; the
        hardware range is 12-230).
    mode : "reverse" | "stop" | "hold" (default "reverse").
    loop_bars : performance window in bars (default 2).
    fade_beats : B's entrance fade in beats (default 1).

    Returns len(a) - loop window + loop window + len(b) samples.
