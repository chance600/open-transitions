# spiral_echo

**Bank:** Web-mined 2026-10-21 (WEB-01) — Pioneer DJM SPIRAL beat FX (pitch-riding feedback delay), hardware effect rendered in DSP · **Automatability:** High · **Confidence:** High

**Source:** Pioneer DJM-450 manual (SPIRAL: pitch changes with delay time; LEVEL/DEPTH sets feedback) · Pestrela DJ Knowledge Base, Effects

## Signature

`spiral_echo` — family SPACE, exit tail, energy delta +0 (falling).

## Spec

Spiral echo: A's last fragment recirculates, pitch-shifting per repeat.

    The Pioneer DJM SPIRAL beat FX changes delay time as it repeats, so
    pitch rides with it: every return of the echo comes back shifted.
    This renders the transition use: `a` plays dry to its end (the
    fader-kill moment), its final `delay_beats` fragment is thrown into
    the spiral, and the tail of pitch-climbing (or pitch-diving) repeats
    decays across `b`'s entrance — B fades up underneath over
    `fade_bars` while the tail evaporates. Output is len(a) + len(b).

    Parameters
    ----------
    a : outgoing segment (mono float64); the thrown fragment is its
        final `delay_beats`.
    b : incoming segment (mono float64), faded in over `fade_bars`
        starting at the handoff (len(a)).
    sr : sample rate, Hz.
    bpm : tempo of the pair (sets the delay grid).
    bar_s : seconds per bar (sets B's fade).
    delay_beats : delay time in beats (default 0.75 — the dotted value
        the DJM SPIRAL is most often thrown at).
    shift_semitones : pitch step per repeat, signed (default +2.0 —
        spiral up; negative spirals down). This is a *tail* effect:
        the T-032 ±2 formant rule governs vocal overlays, not decaying
        echo repeats; later repeats are `feedback`-attenuated whispers.
    repeats : number of repeats rendered (default 8).
    feedback : per-repeat gain (default 0.62, the DJM LEVEL/DEPTH
        mid-position behaviour).
    fade_bars : B's entrance fade in bars (default 2.0).

    Why it works: an ordinary echo tail keeps the outgoing track's
    pitch center alive under the next track — a clash risk the
    selection layer must police. A spiral tail *leaves* the pitch
    center with every repeat, so it reads as the track evaporating
    rather than ending: B owns the tonal space from its first bar
    while A's rhythm still ghosts across the entrance.


## Axis (Phase 26, software/hardware tranche A)

**Cloud Delay staging (SP-404MKII)** — the spiral's diffuse
cousin: multiple delays plus reverb diffusion (WINDOW/CLOUDY),
the recirculation pitch-shiftable −12…+12 semitones like this
base's step, and two properties this render lacks: NEGATIVE
feedback (to −100 — phase-inverted repeats that hollow as they
climb) and a LOFI stage on the wet path only, so the dry stays
clean while the spiral degrades. Evidence: SP-404MKII Reference
v5.5, Cloud Delay page, fetched 2026-10-23.
