# formant_morph_exit

**Bank:** Web-mined 2026-10-21 (WEB-17) — Traktor Formant Filter (§14.4.30) vowel-series spectral morph exit, rendered in DSP · **Automatability:** High · **Confidence:** Medium

**Source:** Native Instruments Traktor 2 manual — The Effects in Detail, §14.4.30 Formant Filter (p.249)

## Signature

`formant_morph_exit` — family FREQ, exit snap, energy delta 0 (flat).

## Spec

    Formant morph exit: A's final bars morph through a series
    of vowel formants — the track "talks" its way out; B enters
    dry.

    Traktor's manual (§14.4.30) documents the Formant Filter: it
    "imitates the sound of spoken vowels by morphing three
    bandpass filters into each other." The TALK control morphs
    through the formants produced from the mouth (a, e, i, o, u)
    — dark at the left, brighter to the right; SHARP makes the
    vowel sound more present; the TYP button switches German /
    English vowel character. Rendered as a transition: across
    A's final `zone_bars` bars the wet signal crossfades in to
    `mix` while the three formant peaks travel — in log
    frequency, at even keyframe spacing — through the vowel
    series named by `path`, each vowel defined by its
    (F1, F2, F3) targets in `table`. At the seam the last vowel
    cuts and `b` enters dry, faded over `fade_bars`.

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bar_s : seconds per bar (sizes the zone and B's fade).
    path : the vowel series to morph through, as a string of
        vowel letters (default "aeiou" — the manual's TALK
        order; "ouiea" runs it backwards).
    table : "english" (default) or "german" — the manual's TYP
        switch; the German table is a systematic shift of the
        English one (tenser vowels), a render approximation.
    sharp : the manual's SHARP — formant presence, 0.5..2.0
        (default 1.0); higher = narrower, more resonant peaks.
    zone_bars : morph zone length in bars (default 4).
    mix : wet level at full engagement, 0..1 (default 0.9; the
        dry residue keeps a whisper of A's body under the
        vowels).
    fade_bars : B's entrance fade in bars (default 0.5).

    Why it works: a filter sweep (T-003) translates one peak
    across the spectrum and a peak stack (WEB-11
    infinity_filter) translates many together — the spectral
    *shape* never changes, only its address. A formant morph
    moves the peaks to vowel-specific relative configurations
    and interpolates between shapes, so A keeps its rhythm and
    rough spectrum while its timbre cycles through the most
    recognisable shapes a listener knows: speech vowels. The
    track appears to pronounce its own exit — a lateral,
    characterful departure that needs no key or tempo
    negotiation, and on a vocal A the effect doubles: the
    singer's vowels are re-articulated by the morph itself.
