# scale_down_exit

**Bank:** Web-mined 2026-10-21 (WEB-14) — Engine DJ 3.1 Scale Down / Pitch Down (beat-stepped pitch descent), Main FX rendered in DSP · **Automatability:** High · **Confidence:** Medium

**Source:** Engine DJ v3.1.0 release article (Main FX list) · Engine DJ 3.1 Release Notes (inMusic Support)

## Signature

`scale_down_exit` — family TIME, exit tail, energy delta +0 (falling).

## Spec

    Scale down exit: A's captured final beat replays once per beat
    across B's entrance, each replay pitched one scale step lower.

    Engine DJ 3.1's Main FX include a matched pair, in Engine's own
    release copy: Pitch Down — "an effect which chromatically
    pitches down the captured audio in time with the beat"; Scale
    Down — "similar to Pitch Down, using four different scales to
    add color to a transition." The mechanism: audio is captured,
    then replayed in beat slots, each replay one step lower —
    chromatically for Pitch Down, along a scale for Scale Down.
    This renders it as the exit: `a` plays dry to its end; its final
    `capture_beats` fragment is replayed `steps` times at
    `step_beats` spacing across `b`'s entrance, replay k pitched
    down by the cumulative scale descent (phase-vocoder shift, so
    each replay stays on the beat grid), decaying x0.85 per step;
    `b` fades up underneath over `fade_bars`. Engine names "four
    different scales" without enumerating them — the render adopts
    the standard four (major, natural minor, major pentatonic,
    minor pentatonic) and carries chromatic as the Pitch Down axis
    of the same base (disclosed in the bank entry, WEB-14).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bpm : tempo of the pair (the step grid).
    bar_s : seconds per bar (sets B's fade).
    scale : "major" / "minor" / "major_pent" / "minor_pent" (Scale
        Down's four) or "chromatic" (Pitch Down's axis).
    steps : number of descending replays (default 4).
    capture_beats : length of the captured fragment (default 1.0).
    step_beats : spacing between replays (default 1.0).
    fade_bars : B's entrance fade in bars (default 2.0).

    Why it works: a pitch descent in discrete, beat-locked,
    scale-quantized steps reads as deliberate — A walks downstairs
    and out, each step landing on a beat and a scale tone, instead
    of falling apart (T-013's continuous dive) or evaporating
    upward (WEB-01's climbing tail). Every replay leaves A's pitch
    center further behind, so B's tonal space is never contested,
    and the scale quantization keeps the descent musical against
    B's entrance where a chromatic slide would smear.
