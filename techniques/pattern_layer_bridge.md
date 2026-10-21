# pattern_layer_bridge

**Bank:** Web-mined 2026-10-21 (WEB-12) — Traktor Pro 4 Pattern Player (synthesized drum-pattern seam layer), performance feature rendered in DSP · **Automatability:** High · **Confidence:** Medium

**Source:** Native Instruments Traktor Pro 4 manual (Pattern Player mode, ducking) · Native Instruments Blog, "Beyond four-on-the-floor: mixing with the Pattern Player in Traktor Pro 4"

## Signature

`pattern_layer_bridge` — family SYNTH, exit seamless, energy delta +1 (rising).

## Spec

Pattern layer bridge: a synthesized drum pattern (Traktor Pro 4
    Pattern Player) carries the seam while the decks hand over.

    Traktor Pro 4's Pattern Player is an FX-unit mode that plays
    rhythmic one-shot patterns (808/909-style kits, 8 samples, patterns
    "sorted by increasing activity") in sync with the master clock,
    on top of a deck; its Decay knob doubles as the release of an
    optional ducking envelope that sidechains the deck under the
    pattern (manual, Pattern Player controls). NI's own transition
    recipe: start the pattern during A's breakdown, raise the pattern
    activity to build, drop B in, swap the bass under the pattern,
    fade A out, then dial the pattern back. This renders that arc:
    across the seam zone (the last `bars`/2 bars of `a` + the first
    `bars`/2 bars of `b`) a synthesized pattern plays at the pair's
    tempo; `a` exits with a one-beat fade into the seam (the pattern
    masks it), `b` fades in across its zone half and is established
    as the pattern stops. With `duck_db` > 0 both decks dip on every
    kick step — fast attack, `duck_release_ms` release (the manual's
    200–500 ms duck-release range).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bpm : tempo of the pair (the pattern's clock).
    bar_s : seconds per bar.
    pattern : named density — "foundation" (kick + offbeat hats),
        "groove" (+ backbeat snare, 8th hats), "build" (+ 16th
        hats, extra snare), "roll" (groove + a final-bar snare
        roll into the seam's B side establishment).
    kit : "kit808" / "kit909" — parametric one-shot voices.
    bars : total seam-zone length in bars (default 8).
    level_db : pattern bus peak level (default -9.0).
    duck_db : deck ducking depth on kick steps (default 0.0 = off).
    duck_release_ms : duck release (default 300 ms; manual range
        200–500).

    Why it works: the seam's hardest moment is two records trading
    rhythmic authority. A third, neutral rhythm — owned by neither
    track, locked to the shared grid — holds the floor's pulse
    constant while the records swap underneath it, so neither A's
    exit nor B's entrance has to carry the groove alone. Distinct
    from T-022 `drum_bridge` (which strips to *A's own* drums) and
    T-020 `three_deck_layer` (a third *track* as glue): the glue
    here is synthesized, keyless, and identical under both tracks.
