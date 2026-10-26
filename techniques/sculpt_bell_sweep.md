# sculpt_bell_sweep

**Bank:** WEB-40 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** PLAYdifferently MODEL 1 User Guide Issue 1 (2016) — Contour/Sculpt EQ: "a semi-parametric swept bell filter" with FREQ + CUT/BOOST, boost +8 dB max, cut -20 dB, "nearly seven octaves"; fetched first-hand 2026-10-26 via the manuals.plus mirror (https://manuals.plus/m/2e08027386c2634318a547d8f72de490ee6e062fab9a20bdc1bb80e3108f491b).

## Signature

```python
sculpt_bell_sweep(a, b, sr, bpm, bar_s, sweep_bars=4, bell_db=8.0, fade_bars=1)
```

`sculpt_bell_sweep` — family FREQ, exit snap, energy delta 0 (flat).

## Spec

A travelling parametric bell tours A's spectrum; B enters clean.

    The MODEL 1 replaces the fixed-band EQ with a hybrid: Contour
    (cut-only low-Q HPF/LPF pair) plus Sculpt, a swept bell whose
    centre frequency the DJ moves and whose gain is asymmetric —
    +8 dB of boost, -20 dB of cut, over nearly seven octaves, with
    a wide Q. Instead of cutting or boosting one band, the DJ
    sweeps the bell itself.

    Rendered as a transition: across A's final `sweep_bars` the
    bell centre log-ramps 60 Hz -> 15 kHz at `bell_db` gain (the
    implementation range mirrors WEB-23's; the manual states the
    span as "nearly seven octaves" without Hz numbers). At +8 dB
    each element of A is highlighted in turn as the bell passes —
    kick, then bass, then vocal, then hats — a tour, not a
    thinning; at -20 dB the same travel is a moving cut. At the
    top of the band the bell exits the spectrum (transparent) as
    B fades in over `fade_bars`.

    Why it is not its neighbours: not WEB-23
    `notch_carve_sweep` (a rejection band from summed HPF+LPF
    outputs — this is a parametric bell, and its headline form
    is a travelling BOOST, which no neighbour renders); not
    T-003 (a monotonic slope, energy removed on one side
    forever); not `eq_blend` (fixed band gains at fixed
    frequencies — no travelling centre).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    sweep_bars : bell travel window at A's end (default 4).
    bell_db : bell gain in dB (default 8.0 — the manual's max
        boost; -20.0 is the max cut).
    fade_bars : B's entrance crossfade at the seam (default 1).

## Selection

Requires: no BPM gate, no key gate, vocal pair any, A's phrase outro / chorus,
genre pair same / neighbor / leap, no needs.
Prefers: genre pair same (+1, the bell tours A's spectrum inside one genre's blend — no gap device needed); A's phrase outro (+1, the sweep window is A's outro — the bell has a full phrase to travel).

## Axes (Phase 32, Class 5 tranche B)

**VCF TO XFADER staging (Xone:92)** — the 92 lets the crossfader
drive a filter cutoff instead of the FREQ knob, "to create filter
effects whilst crossfading." The staging this base's fixed
trajectory does not express: the bell's travel driven by the
fader's position rather than the clock, so the tour speeds up,
slows, and reverses with the DJ's hand. Evidence: Xone:92 User
Guide p. 24 (manualsdir mirror), fetched 2026-10-26.
