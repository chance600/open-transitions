# fader_synth

**Bank:** Web-mined 2026-10-21 (WEB-15) — Pioneer DJM-S11 FADER SYNTH (source-replacing fader oscillator), Beat FX rendered in DSP · **Automatability:** High · **Confidence:** Medium

**Source:** Pioneer DJM-S11 manual (Beat FX types and settings, FADER SYNTH p.61)

## Signature

`fader_synth` — family SYNTH, exit seamless, energy delta +1 (rising).

## Spec

    Fader synth: A's channel is replaced by an oscillator line
    whose pitch follows a scripted fader ride across the seam.

    The DJM-S11's Beat FX table (p.61) lists FADER SYNTH
    (SINE/SAW/SQUARE): "outputs the synth sound as the audio source
    of the base oscillation frequency" — the input sound is
    replaced by an oscillator and the channel fader becomes its
    pitch control (the manual's footnote: with the effect on, the
    fader no longer adjusts volume). The BEAT buttons set the base
    oscillation frequency level (-3 to +3); LEVEL/DEPTH is the
    effect volume; the sub parameter quantizes the fader's pitch
    travel to a scale (AUTO SCALE, MAJOR, MINOR, MINOR H,
    JAPANESE, ...). This renders a transition ride: across the seam
    zone (the last `zone_bars`/2 bars of `a` + the first
    `zone_bars`/2 bars of `b`), `a` fades out inside the zone's
    first beat — the fader pull — and a synthesized line plays the
    ride: "steps" (one scale degree per beat, climbing through
    octaves), "glide" (a continuous one-octave glide), "arp" (a
    0-2-4-2 degree pattern per beat), or "hold" (parked at the
    octave). `b` fades in across its zone half and is established
    as the synth cuts at the zone's end.

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bar_s : seconds per bar (sizes the zone and the beat grid).
    waveform : "sine" / "saw" / "square" — the manual's three.
    ride : "steps" / "glide" / "arp" / "hold" — the fader path.
    scale : "major" / "minor" / "minor_h" / "japanese" — the
        manual's sub-parameter set, render subset.
    root_hz : the line's root frequency (default 110.0 = A2).
    base_octave : the manual's base-frequency level, -3..+3
        octaves applied to the root (default 0).
    zone_bars : seam-zone length in bars (default 4).
    level_db : synth line level (default -6.0).

    Why it works: every other exit treats A's audio; this one
    substitutes for it. The moment the record becomes a synth
    tone, the pair's key/tempo negotiation ends — the line owes
    A's harmony nothing beyond its starting root, and its
    scale-quantized climb is pure directed energy that B inherits
    at the seam. Distinct from DM-A15 `cdj_synth_lead` (a loop
    grab of A's own audio resynthesized — the source is still A)
    and from T-032 `pitch_play` (the input sound, pitched): this
    oscillator never contained the record at all.
