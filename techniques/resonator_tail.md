# resonator_tail

**Bank:** Web-mined 2026-10-21 (WEB-18) — Ableton Resonators five-parallel-resonator bank tuned to B's chord, rendered in DSP · **Automatability:** High · **Confidence:** Medium

**Source:** Ableton Live 12 manual — Live Audio Effect Reference, Resonators + Spectral Resonator

## Signature

`resonator_tail` — family SPACE, exit tail, energy delta 0 (flat).

## Spec

    Resonator tail: A's final bars ring away through a tuned
    resonator bank while B enters under the ring.

    Ableton's Resonators device (Live 12 manual, Live Audio
    Effect Reference) runs the input through "five parallel
    resonators that add a tonal character to the input signal
    and can be tuned in semitones or scale degrees," producing
    "results ranging from plucked-string timbres to
    vocoder-like tones." Resonator I sets the root (its Note
    parameter); II–V are tuned relative to it in musical
    intervals, each transposable ±24 semitones. The Decay
    parameter sets "the amount of time it takes for the
    resonators to be silent after getting an input signal...
    similar to the behavior of an undamped piano string," and
    — as with a real string — the decay time depends on the
    pitch, low notes lasting longer than higher ones; Color
    sets the brightness. Rendered as a transition: A's final
    `zone_bars` bars excite a five-comb resonator bank tuned
    to the `chord` voicing on `root_midi`; across the zone the
    dry signal crossfades into the ring, so by the seam A is
    present only as its own resonance, pitched to the chord.
    The ring decays naturally (pitch-dependent, per the
    manual) across B's entrance while `b` fades in under it
    over `fade_bars`. Output is len(a) + len(b).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bar_s : seconds per bar (sizes the zone and B's fade).
    root_midi : Resonator I's Note as a MIDI number (default
        45 = A2, 110 Hz). Selection passes B's tonic: the
        ring is tuned to the *incoming* chord, so A's energy
        arrives already speaking B's harmony.
    chord : the II–V interval voicing above the root —
        "major" (0, +4, +7, +12, +19), "minor"
        (0, +3, +7, +12, +19), "power" (0, +7, +12, +19,
        +24), "octave" (0, +12, +24).
    decay_s : the manual's Decay — seconds for the root
        resonator to fall to silence (−60 dB); higher
        resonators decay faster, scaled by (f_root/f)^0.5,
        the manual's pitch dependence.
    color : the manual's Color, 0..1 (default 0.5) —
        brightness, rendered as the damping lowpass inside
        each comb's feedback path.
    zone_bars : excitation zone length in bars (default 2).
    ring_level : ring level relative to A's peak, 0..1
        (default 0.85).
    fade_bars : B's entrance fade in bars (default 1.0).

    Why it works: every other tail in the library carries
    A's *pitch content* forward — an echo repeats it, a
    reverb diffuses it, a shimmer transposes it by a fixed
    interval. A resonator bank replaces it: the tail keeps
    A's rhythm and energy contour but its pitch content is
    the bank's tuning, chosen here as B's chord. The seam
    therefore has no key negotiation at all — what crosses
    it is A's gesture re-pitched into B's harmony, decaying
    like strings while B establishes itself underneath.


## Axes (Phase 26, software/hardware tranche A)

**Chord-bank staging (SP-404MKII Resonator)** — Roland's
Karplus-Strong form of this bank: up to SIX resonators against
this base's five, tuned by ROOT (C-1–G9) and 15 named CHORD
voicings, with BRIGHT as the damping control and ENV MOD —
feedback that *grows with input level*, so loud passages ring
longer than quiet ones (a level-dependent decay this base's
fixed decay_s does not stage). Same mechanism family (feedback
combs, damping lowpass in the loop), banked as the voicing axis
of this base rather than a new base. Evidence: SP-404MKII
Reference v5.5, Resonator page, fetched 2026-10-23.

**Hyper-Reso scale staging (SP-404MKII Hyper-Reso)** — the bank
addressed in scale degrees instead of semitone intervals: NOTE
−17…+18 in major/minor SCALE steps, SPREAD from UNISON to HUGE
octave dispersion — the ring tuned by key signature, the
performance form of this base's `chord` parameter. Evidence:
SP-404MKII Reference v5.5, Hyper-Reso page, fetched 2026-10-23.
