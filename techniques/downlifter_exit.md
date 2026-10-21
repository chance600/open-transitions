# downlifter_exit

**Bank:** Web-mined 2026-10-21 (WEB-09) — the producer's "downer" (descending synth sweep), arrangement FX ported to a deck-to-deck seam mask · **Automatability:** High · **Confidence:** Medium

**Source:** MusicRadar, "How to make synth sweep FX for EDM drops" (risers vs downers; noise + low-pass cutoff automation) · sonical.ly, "How to Create Epic Risers and Transition Effects for Electronic Music"

## Signature

`downlifter_exit` — family SYNTH, exit snap, energy delta +0 (falling).

## Spec

Downlifter exit: a descending filtered-noise sweep spans the
    seam and masks the cut.

    The producer's "downer" — the riser's mirror. Synthesized white
    noise runs through a low-pass whose cutoff falls exponentially
    from `f_start` to `f_end` Hz across `sweep_bars` bars; the sweep
    swells in over the first three quarters (A's final stretch) and
    crashes down through the last quarter (B's first beat), dying as
    B establishes. Underneath it, `a` hands to `b` with a plain 3 ms
    seam guard — a hard join the sweep exists to hide. Where a riser
    builds tension *before* a change and is killed at the seam, the
    downlifter spends tension *across* the seam.

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bar_s : seconds per bar (the sweep grid).
    sweep_bars : sweep length in bars (default 1.0).
    f_start, f_end : cutoff sweep endpoints in Hz (defaults
        12000 -> 300 — full-spectrum crash to a low rumble).
    level_db : sweep peak level (default -9.0 — loud enough to mask,
        under the mix's own peaks).
    seed : noise seed (default 11; renders are deterministic).

    Why it works: the falling sweep is a full-spectrum event with a
    clear trajectory, so the ear tracks *it* through the exact moment
    the tracks change; the seam hides inside the loudest, fastest-
    moving part of the sweep. It also reads as punctuation — "that
    section is over" — which licenses hard changes (tempo, key,
    genre) underneath it.
