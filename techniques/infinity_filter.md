# infinity_filter

**Bank:** Web-mined 2026-10-21 (WEB-11) — Serato Infinity Filter (endless barber-pole resonant sweep), hardware effect rendered in DSP · **Automatability:** High · **Confidence:** Medium

**Source:** Serato Support, DJ-FX & Channel FX list (Infinity Filter, Advanced FX) · Serato Hex FX ("endless sweeping peaks") · Pestrela DJ Knowledge Base (Mobius = Shepard Tone)

## Signature

`infinity_filter` — family FREQ, exit snap, energy delta +1 (rising).

## Spec

Infinity filter: A's exit through an endlessly sweeping
    resonant peak stack (barber-pole filter); B enters dry.

    Serato's DJ-FX catalog (3.2+) lists an "Infinity Filter" among
    its Advanced FX, and Serato's Hex FX page describes the family
    mechanism: "endless sweeping peaks for evolving, dramatic
    soundscapes" — a filter sweep that never arrives, the frequency-
    domain sibling of the Shepard tone (the legacy Serato packs named
    the same idea "Shepard Filter"; Pestrela decomposes Pioneer's
    Mobius as "Shepard Tone"). This renders the transition use with
    the Shepard construction itself: a bank of narrow resonant peaks
    spaced one octave apart, each sweeping exponentially upward
    (direction=-1: downward); a peak's gain follows a Gaussian window
    over log-frequency, so peaks fade in at the bottom of the window
    and out at the top — the ear tracks one peak rising forever while
    A is still, recognizably, A. Across the final `sweep_bars` bars
    the wet stack crossfades in to `mix` while the peaks complete
    `cycles` full wraps; at the seam the filtered A cuts and `b`
    enters dry, faded over `fade_bars`.

    Parameters
    ----------
    a : outgoing segment (mono float64); its final `sweep_bars`
        bars pass through the peak stack.
    b : incoming segment (mono float64), faded in over `fade_bars`
        at the seam.
    sr : sample rate, Hz.
    bar_s : seconds per bar (sets the sweep zone and B's fade).
    direction : +1 sweeps up (default), -1 sweeps down.
    cycles : full octave wraps completed across the zone
        (default 2.0).
    sweep_bars : length of the filtered zone in bars (default 4).
    mix : wet level at full engagement, 0..1 (default 0.85; the
        remaining dry residue keeps A's body in the exit).
    fade_bars : B's entrance fade in bars (default 0.5 — the
        infinity motion, not B, is the event; B arrives promptly).

    Why it works: a one-way filter sweep (T-003) spends its motion
    and arrives — the exit is the arrival. An endless sweep never
    resolves, so A's final bars hang in permanent departure: the
    track is leaving the whole time, and B's dry downbeat is the
    only arrival on offer. Distinct from WEB-05 `shepard_riser`
    (an *added* oscillator layer under an intact A): here A's own
    spectrum is what climbs.
