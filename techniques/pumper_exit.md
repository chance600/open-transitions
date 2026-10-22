# pumper_exit

**Bank:** Web-mined 2026-10-21 (WEB-13) — Denon X1850 PRIME Pumper (beat-synced downbeat ducking), BPM FX rendered in DSP · **Automatability:** High · **Confidence:** Medium

**Source:** Denon DJ X1850 PRIME User Guide (Effects chapter, Pumper) · rekordbox DDJ-RZX / XDJ-RX3 manuals (Release FX DUCKING)

## Signature

`pumper_exit` — family DYN, exit snap, energy delta +1 (build).

## Spec

    Pumper exit: A's final bars duck on the downbeat grid, deepening
    cycle by cycle; the last recovery is withheld and B fills the hole.

    Denon's X1850 PRIME BPM FX list includes Pumper — "this effect
    attenuates or 'ducks' audio on the downbeat, similar to a sidechain
    compressor" — with two parameters: Duck (attenuation, -2 to -20 dB)
    and Offset (the ducking offset in beats: -1/16, -1/8, -1/4, -1/2,
    always anticipatory, so the dip is already open when the downbeat
    lands); the module's FX Time division sets the duck rate. This
    renders the transition use: across A's final `pump_bars` bars a
    duck cycle of `rate_beats` beats repeats, its depth ramping from
    1/n to the full `duck_db` (the manual's Duck range); each dip
    attacks over 15% of the cycle and recovers across its back half.
    The final cycle never recovers — A fades out inside the duck over
    its last beat — and `b` enters dry at full level at the seam, in
    the hole the withheld recovery leaves. rekordbox's Release FX
    DUCKING pad is the same mechanism in exit form (second vendor).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bpm : tempo of the pair (the duck grid).
    bar_s : seconds per bar (sizes the pump zone).
    duck_db : full duck depth at the final cycle, -2..-20 dB (the
        manual's Duck parameter; default -10).
    offset_beats : dip start relative to the beat, in beats — the
        manual's Offset set is -1/16..-1/2; 0.0 is on-grid
        (default -0.25).
    rate_beats : duck cycle length in beats (the FX Time division;
        default 1.0).
    pump_bars : length of the deepening zone in bars (default 4).

    Why it works: the pump pre-carves rhythmic holes in A's final
    bars, so the ear leans into the gaps and B — arriving dry in the
    last, unrecovered hole — reads as the drop the pumping promised.
    Distinct from T-035 `riser_ducking_overlay` (ducking in service
    of an added riser layer): nothing is added here; the ducking
    itself is the exit. Distinct from the gate family: the dips are
    shallow-to-moderate, rounded, and recover between beats —
    sidechain breathing, not chopping.
