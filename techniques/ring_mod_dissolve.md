# ring_mod_dissolve

**Bank:** Web-mined 2026-10-21 (WEB-16) — Traktor Ring Modulator (§14.4.25) carrier-multiplication dissolve exit, rendered in DSP · **Automatability:** High · **Confidence:** Medium

**Source:** Native Instruments Traktor 2 manual — The Effects in Detail, §14.4.25 Ring Modulator (p.245)

## Signature

`ring_mod_dissolve` — family FREQ, exit snap, energy delta +1 (rising).

## Spec

    Ring mod dissolve: A's final bars are multiplied by a rising
    carrier until the track dissolves into inharmonic sidebands;
    B enters dry.

    Traktor's manual (§14.4.25) documents the Ring Modulator as a
    standalone effect: it "modulates the tracks by multiplying the
    high frequency signal onto the audio material" — the input is
    multiplied by an oscillator whose PITCH runs 100 Hz to
    8371 Hz, with an AM-RM control morphing between amplitude
    modulation (soft, the dry signal survives inside the product)
    and full ring modulation (the dry signal is gone; only
    sidebands at f +/- fc remain), and a RAW switch changing the
    carrier from a sine to a filtered square. Rendered as a
    transition: across A's final `zone_bars` bars the mix ramps
    from dry A to the fully modulated signal while the carrier
    sweeps logarithmically from `carrier_start_hz` to
    `carrier_end_hz`. As the carrier climbs through the audio
    band, A's partials smear into inharmonic sideband pairs and
    the track's pitch identity dissolves into metallic shimmer;
    at the seam the shimmer cuts and `b` enters dry, faded over
    `fade_bars`.

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bar_s : seconds per bar (sizes the zone and B's fade).
    carrier_start_hz : carrier frequency at the zone's start
        (default 100.0 — the manual's range floor).
    carrier_end_hz : carrier frequency at the zone's end
        (default 2800.0; the manual's ceiling is 8371.0).
    morph : AM <-> RM morph, 0..1 (default 1.0 = full ring
        modulation; 0.0 = pure amplitude modulation).
    raw : "sine" carrier (default) or "square" — the manual's
        RAW filtered-square carrier, rendered as a soft-clipped
        sine (odd harmonics, rolled-off top).
    zone_bars : dissolve zone length in bars (default 4).
    fade_bars : B's entrance fade in bars (default 0.5).

    Why it works: multiplication is the one basic operation the
    rest of the registry never performs — filters subtract
    (T-003), quantization coarsens (WEB-04 crush_degrade), combs
    interfere (WEB-02 flanger_sweep). A ring modulator *adds new
    partials* at sum-and-difference frequencies, so the exit is
    not A getting quieter or duller but A becoming a different
    spectrum altogether: recognizability drains as the carrier
    rises, which is exactly the perceptual job of an exit, and
    because the sidebands are inharmonic the move owes the pair
    no key negotiation at all.
