# lfo_filter_sweep

**Bank:** WEB-41 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Allen & Heath Xone:92 User Guide p. 24 (manualsdir mirror) — LFO modulation: "two independent LFOs... for additional cyclic filter modulation effects," ON switch, DEPTH, TAP tempo, X2 doubling; fetched first-hand 2026-10-26 (https://www.manualsdir.com/manuals/554322/allenheath-xone-92-xone92.html?page=24).

## Signature

```python
lfo_filter_sweep(a, b, sr, bpm, bar_s, lfo_bars=4, lfo_cycles=4, depth_oct=2.0, fade_bars=1)
```

`lfo_filter_sweep` — family FREQ, exit snap, energy delta 0 (flat).

## Spec

A's exit wahs under a cyclic filter LFO; B enters clean.

    The Xone:92's VCFs are "further enhanced by two independent
    LFOs... for additional cyclic filter modulation effects": an
    ON switch punches the LFO in or out, DEPTH sets the modulation
    amount, TAP sets the rate from the last two presses, X2
    doubles it. The LFO is a cyclic control, not a sweep: the
    cutoff returns to where it started every cycle.

    Rendered as a transition: across A's final `lfo_bars` a
    lowpass cutoff oscillates log-sinusoidally around 1 kHz,
    `lfo_cycles` whole cycles (integer, so the filter returns to
    centre exactly at the seam), with the oscillation depth
    ramping 0 -> `depth_oct` octaves across the window — the
    DEPTH knob turning up through the exit. At the seam B fades
    in over `fade_bars`, the filter at centre, neither open nor
    closed.

    Why it is not its neighbours: not T-003 (a monotonic slope —
    this returns, every cycle); not WEB-27 `cyclic_speed_dip` (a
    tempo-period LFO on playback RATE — this modulates the
    filter, not the speed); not WEB-24 `phaser_sweep` (an allpass
    cascade, magnitude-flat — this is a cutoff oscillation with
    real spectral loss at the troughs).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    lfo_bars : LFO window at A's end (default 4).
    lfo_cycles : whole LFO cycles inside the window (default 4 —
        one per bar at the default window).
    depth_oct : peak oscillation depth in octaves at the seam
        (default 2.0; the depth ramps 0 -> depth_oct).
    fade_bars : B's entrance crossfade at the seam (default 1).

## Selection

Requires: no BPM gate, no key gate, vocal pair any, A's phrase outro / chorus / build,
genre pair same / neighbor / leap, no needs.
Prefers: genre pair same (+1, cyclic filter motion sits inside a like-for-like blend); energy delta >= 0 (+1, the LFO's rising depth lifts a flat-or-rising exit).
