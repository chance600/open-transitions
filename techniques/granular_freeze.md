# granular_freeze

**Bank:** Web-mined 2026-10-21 (WEB-06) — granular freeze: the outgoing track's last moment sustained as a grain cloud (Amazing Noises Grain Freezer recipe) · **Automatability:** High · **Confidence:** High

**Source:** Amazing Noises Grain Freezer (Rekkerd) — ~150 ms capture sustained as overlapping grains · Sound on Sound — Granular Synthesis: A Practical Introduction

## Signature

`granular_freeze` — family SPACE, exit tail, energy delta +0 (flat).

## Spec

Granular freeze: A's last moment becomes a grain cloud; B enters in it.

    At the freeze point (`cloud_bars` before A's end), a `capture_ms`
    fragment of `a` is sustained as a cloud of overlapping Hann-windowed
    grains — the Amazing Noises Grain Freezer recipe (capture ~150 ms,
    sustain as a texture of up to dozens of simultaneous grains). Across
    the cloud zone the grain read position drifts forward through the
    capture (`drift` of its length) while `b` equal-power-fades up
    *inside* the cloud; at the zone's end the cloud is gone and B plays
    alone. Output length is len(a) - cloud_zone + len(b).

    The cloud is A's own material — its harmonics, its formants — with
    its rhythm and pitch commitment dissolved by the grain window,
    which is exactly what separates this from T-034 (reverb freeze
    freezes the *room's* tail; this freezes the *source*).

    Parameters
    ----------
    a : outgoing segment (mono float64); the capture is taken from
        just before the freeze point.
    b : incoming segment (mono float64); its first `cloud_bars` play
        inside the cloud.
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    cloud_bars : cloud zone length in bars (default 4).
    capture_ms : captured fragment length (default 150 ms, the Grain
        Freezer's capture size).
    grain_ms : grain length (default 70 ms).
    density : grains per second (default 45 — dense enough to read as
        texture, sparse enough to keep the source's grain).
    drift : how far the read position scans through the capture across
        the zone, as a fraction (default 0.7).
    seed : grain-position jitter seed (default 7) — the render is
        deterministic; the jitter is frozen into the recipe.

    Why it works: the ear recognizes the cloud as *made of A* while
    owing it no beat or key allegiance, so B can enter at any tempo or
    key inside it and still feel handed-over rather than interrupted —
    a texture bridge whose provenance is the audio itself.
