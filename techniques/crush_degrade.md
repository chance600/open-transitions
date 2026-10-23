# crush_degrade

**Bank:** Web-mined 2026-10-21 (WEB-04) — DJM Crush Colour FX (bit reduction) extended to a full fidelity-degrade exit · **Automatability:** High · **Confidence:** High

**Source:** Pestrela DJ Knowledge Base, Effects — crush reduces bit resolution (+ filter); RMX-1000 crush echo

## Signature

`crush_degrade` — family DYN, exit snap, energy delta +1 (rising).

## Spec

Crush degrade: A degrades to lo-fi over its final bars; B is clean.

    Pioneer's Crush Colour FX reduces bit resolution (paired with a
    filter); the RMX line adds the crushed echo. As a transition the
    full recipe is: across A's final `bars`, bit depth ramps 16 ->
    `bits_end`, the effective sample rate folds down to `rate_end` of
    the original (sample-hold), and a low-pass folds 12 kHz -> 700 Hz
    alongside. During the final `fade_bars` the crushed ghost
    equal-power-crossfades into `b` arriving at full fidelity — the
    fidelity contrast itself is the drop. Output length is
    len(a) + len(b) - fade.

    Parameters
    ----------
    a : outgoing segment (mono float64); the crush zone is its final
        `bars`.
    b : incoming segment (mono float64), clean, faded in across the
        crush zone's last `fade_bars`.
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    bars : crush zone length in bars (default 4).
    bits_end : final bit depth (default 5.0 — unmistakably crushed,
        still rhythmic).
    rate_end : final sample-rate fraction (default 0.25).
    fade_bars : B's crossfade length in bars (default 1.0).

    Why it works: fidelity is an energy dimension. The crowd hears A
    turn into a toy version of itself — same groove, collapsing
    resolution — while B assembles in full range underneath. No pitch,
    key, or tempo negotiation is involved, so the move is legal across
    genre leaps where blends are not.


## Axes (Phase 26, software/hardware tranche A)

**Lo-fi type stagings (SP-404MKII Lo-fi)** — the crush with a
front end: PRE FILT 1–6 pre-shapes the signal before the
degrade (feeding the fold a chosen band, not the whole track),
LOFI TYPE 1–9 selects the degradation algorithm, and a
post-filter (200–8000 Hz) decides what of the damage reaches
the mix — the three-stage form of this base's single ramp.
Evidence: SP-404MKII Reference v5.5, Lo-fi page, fetched
2026-10-23.

**Cassette saturation staging (SP-404MKII Cassette Sat)** —
age as a parameter: AGE adds wow/flutter (the pitch wobble of
worn tape) and Catch (pitch instability) on top of the
saturation — degradation of the *timebase*, where this base
degrades the *word length*. The two compose: a cassette-aged
crush is this axis fired over this base. Evidence: SP-404MKII
Reference v5.5, Cassette Sat page, fetched 2026-10-23.
