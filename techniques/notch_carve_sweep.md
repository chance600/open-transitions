# notch_carve_sweep

**Bank:** WEB-23 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Allen & Heath Xone:96 User Guide (official Allen & Heath support HTML, the complete guide — no PDF is linked from it) — dual state-variable VCFs, simultaneous HPF/BPF/LPF outputs, combinations creating 'notch' and 'all-pass' responses; fetched first-hand 2026-10-23.

## Signature

```python
notch_carve_sweep(a, b, sr, bpm, bar_s, sweep_bars=4, q=8.0, fade_bars=1)
```

`notch_carve_sweep` — family FREQ, exit snap, energy delta 0 (flat).

## Spec

A travelling spectral hole carves A away; B enters clean.

    The Xone:96's filters are state-variable: they "provide three
    simultaneous filter response output types: High-Pass (HPF),
    Band-Pass (BPF) and Low-Pass (LPF)... Any combination can be
    pressed together to create different response types such as
    'notch'". Summing the HPF and LPF outputs gives a notch: full
    energy everywhere except a rejection band at FREQ, its width
    set by RES.

    Rendered as a transition: across A's final `sweep_bars` the
    notch centre log-ramps 60 Hz -> 15 kHz. The track thins
    locally and reversibly — when the hole crosses the kick band
    the kick vanishes and returns; when it crosses the vocal band
    the vocal does — instead of the monotonic thinning of
    `filter_sweep` (T-003). At the top of the band the notch exits
    the spectrum (transparent) as B fades in over `fade_bars`.

    Why it is not its neighbours: not T-003 (a monotonic slope,
    energy removed on one side forever); not `eq_blend` (fixed
    band gains at fixed frequencies — no travelling hole, no
    resonance); not `resonator_tail` WEB-18 (a ringing decay tail,
    not a rejection band in a continuing signal); not
    `flanger_sweep` WEB-02 (delay-comb notches are periodic and
    multiple — this is a single state-variable rejection band).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    sweep_bars : carve window at A's end (default 4).
    q : notch Q from the RES staging (default 8.0; MILD ~ wide,
        WILD ~ needle — the guide gives no numeric Q, the mapping
        is an implementation choice, stated here).
    fade_bars : B's entrance crossfade at the seam (default 1).

    Returns a mono float64 mix of length len(a) + len(b) - fade.
