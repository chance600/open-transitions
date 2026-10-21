# shepard_riser

**Bank:** Web-mined 2026-10-21 (WEB-05) — Shepard-Risset endless rise as a build layer (DJM Mobius applies the same illusion as a filter) · **Automatability:** High · **Confidence:** High

**Source:** Pestrela DJ Knowledge Base, Effects (Mobius = Shepard Tone) · Sound on Sound — iZotope Mobius Filter review

## Signature

`shepard_riser` — family SYNTH, exit snap, energy delta +2 (rising).

## Spec

Shepard riser: an endless-rise synth layer under A's final bars.

    A Shepard-Risset glissando: `partials` sine partials spaced in
    octaves above `base_hz`, all gliding up (or down) together through
    repeated octave cycles, each partial's level wrapped in a Gaussian
    envelope over log-frequency centered at `center_hz` — partials fade
    in at the bottom of the spectrum and out at the top, so the pitch
    seems to rise forever without ever getting higher. Pioneer's DJM
    Mobius beat FX applies the same illusion as a filter; this renders
    it as a synthesized layer (the T-018/T-035 riser family member that
    cannot run out of headroom). The layer fades in over the first bar
    of the zone, sits at `level_db` relative to A's peak, and cuts dead
    on the handoff — `b` inherits all the unresolved rising tension.
    Output is len(a) + len(b) (3 ms seam guard).

    Parameters
    ----------
    a : outgoing segment (mono float64); the layer zone is its final
        `bars`.
    b : incoming segment (mono float64), entered at len(a).
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    bars : layer zone length in bars (default 8); the glide completes
        one octave cycle per 4 bars.
    direction : +1 rises, -1 falls (default +1).
    level_db : layer peak relative to A's peak (default -9.0 dB —
        presence without masking).
    partials : number of octave partials (default 7).
    base_hz : lowest partial's starting frequency (default 55 Hz).
    center_hz : Gaussian envelope center (default 640 Hz).
    sigma_oct : envelope width in octaves (default 1.15).

    Why it works: a conventional riser spends pitch and loudness and
    arrives; the Shepard layer never arrives, so tension can stretch
    across a whole phrase without the fatigue of a sound that is
    literally getting louder and higher the whole time. The only
    resolution on offer is B's first bar.
