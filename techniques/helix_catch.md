# helix_catch

**Bank:** Web-mined 2026-10-21 (WEB-07) — Pioneer DJM HELIX beat FX (loop sampler with progressive pitch change), hardware effect rendered in DSP · **Automatability:** High · **Confidence:** Medium

**Source:** Pioneer DJM-900NXS2 manual p.17 (via the Pioneer official forum HELIX/FREEZE thread) · Pestrela DJ Knowledge Base, Effects · DJM-A9 spec (HELIX persists in the current Beat FX generation)

## Signature

`helix_catch` — family TIME, exit snap, energy delta +1 (rising).

## Spec

Helix catch: A's final fragment loops while its pitch ramps; B
    enters at natural pitch on the release.

    The Pioneer DJM HELIX beat FX captures the playing sound into a
    loop the moment it engages; while held, the loop's pitch changes
    progressively (LEVEL/DEPTH sets the ramp — turned fully right it
    *fixes* the pitch, rendered here as ramp_semitones=0); on release
    the pitch returns to the point where the effect was switched on.
    This renders the transition use: `a` plays dry, its final
    `capture_beats` fragment is caught and looped for `hold_bars`
    bars with the playback rate (pitch-coupled, like the hardware)
    ramping linearly in semitones from 0 to `ramp_semitones`, then
    the hold ends and `b` enters faded over `fade_bars` at its own
    pitch — the ramp's tension resolves into the new track instead
    of evaporating (contrast WEB-01's decaying spiral tail).

    Parameters
    ----------
    a : outgoing segment (mono float64); the caught fragment is its
        final `capture_beats`.
    b : incoming segment (mono float64), faded in over `fade_bars`
        starting at the release.
    sr : sample rate, Hz.
    bpm : tempo of the pair (sets the capture grid).
    bar_s : seconds per bar (sets the hold length and B's fade).
    capture_beats : caught fragment length in beats (default 1.0).
    hold_bars : hold length in bars (default 2).
    ramp_semitones : total pitch ramp across the hold, signed
        (default +12.0 — one octave up; 0.0 renders the fixed-pitch
        loop behaviour).
    fade_bars : B's entrance fade in bars (default 0.5 — the release
        is a near-snap by design).

    Why it works: a caught loop is the outgoing track insisting on
    staying; the continuous pitch ramp makes that insistence
    unstable, so the ear waits for the release. The loop is A's own
    material on A's own grid, so B can enter beat-locked the moment
    the helix lets go.
