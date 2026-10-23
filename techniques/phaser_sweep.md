# phaser_sweep

**Bank:** WEB-24 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Roland SP-404MKII Reference v5.5 (official) — Phaser MFX page; corroborated by the Xone:96 User Guide's all-pass state-variable sum. Fetched first-hand 2026-10-23.

## Signature

```python
phaser_sweep(a, b, sr, bpm, bar_s, sweep_bars=4, rate_bars=1.0, stages=4, fade_bars=1)
```

`phaser_sweep` — family FREQ, exit snap, energy delta 0 (flat).

## Spec

Magnitude-flat phase movement carries the seam.

    Two vendor attestations of one topology: the SP-404MKII's
    Phaser "creates modulation by adding a phase-shifted sound"
    (allpass network; DEPTH/RATE/MANUAL/RESONANCE, RATE syncable),
    and the Xone:96's state-variable sum giving "interesting
    'all-pass' effects" — flat magnitude, frequency-dependent
    phase rotation around FREQ.

    Rendered as a transition: across A's final `sweep_bars`, A is
    mixed with a cascade of `stages` allpass sections whose break
    frequency oscillates (period `rate_bars` bars, centre 800 Hz,
    ±1.2 octaves). The moving phase interference hollows the
    texture cyclically while the spectrum and loudness stay put —
    the track moves without thinning — then B fades in over
    `fade_bars` as the sweep parks.

    Why it is not its neighbours: not `flanger_sweep` WEB-02 (a
    modulated DELAY line: comb magnitude response, harmonic notch
    spacing, feedback whistle) — an allpass cascade's notches are
    non-harmonic and there is no delay line; not
    `formant_morph_exit` WEB-17 (formant peaks MOVE — magnitude
    changes by design; here magnitude is flat by construction).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    sweep_bars : phased window at A's end (default 4).
    rate_bars : LFO period in bars (default 1.0).
    stages : allpass sections (default 4).
    fade_bars : B's entrance crossfade (default 1).

    Returns a mono float64 mix of length len(a) + len(b) - fade.
