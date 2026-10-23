# beatslicer_shuffle

**Bank:** Web-mined 2026-10-21 (WEB-08) — Native Instruments Traktor BeatSlicer Buffer (bar buffer, slice-permutation replay), software effect rendered in DSP · **Automatability:** High · **Confidence:** Medium

**Source:** Native Instruments Traktor 2 manual §14.4.29, BeatSlicer Buffer (manua.ls mirror, p.248)

## Signature

`beatslicer_shuffle` — family TIME, exit snap, energy delta +1 (rising).

## Spec

BeatSlicer shuffle: A's final bar(s) replayed slice-permuted,
    then B releases on the downbeat.

    Traktor's BeatSlicer buffers up to 2 bars, subdivides the buffer
    into small chunks and replays them in a different sequence — "a
    rhythmically shuffled version of the original music" — from 20
    hardware patterns in 5 styles. This renders the transition use:
    `a` plays dry; its final `buffer_bars` bars are re-dealt as 8
    slices per bar replayed in the named permutation `pattern`; the
    effect's BUZZ control is rendered as a half-slice self-repeat on
    the final beat when `buzz` is 1; `b` then enters on the next
    downbeat through a 3 ms seam guard. The shuffled region is
    exactly as long as the region it replaces — permutation scrambles
    order, never the grid.

    Parameters
    ----------
    a : outgoing segment (mono float64); its final `buffer_bars`
        bars are the slicer's buffer.
    b : incoming segment (mono float64), entering dry at the seam.
    sr : sample rate, Hz.
    bar_s : seconds per bar (the buffer and slice grids).
    pattern : permutation name — one of identity, reverse,
        swap_pairs, bookends, stride, halves, inside_out
        (default "stride").
    buffer_bars : buffered bars, 1 or 2 (default 1; the hardware
        buffers 2 bars and applies its pattern across them).
    buzz : 1 renders the BUZZ half-slice repeat on the final beat,
        0 leaves the final beat as permuted (default 1).

    Why it works: every slice is A's own audio on A's own beat grid,
    so the floor keeps dancing while the pattern stops making sense —
    a build made of pure expectation violation, resolved by B.
    Distinct from a beat-repeat roll (one fragment tiled forward) and
    a stutter (onset repeats): the whole bar is re-dealt.


## Axes (Phase 26, software/hardware tranche A)

**Scatter staging (SP-404MKII)** — Roland's Scatter performs
this base's step-redeal with three extensions: per-step
DIRECTION (a step can play reversed), a per-step gate length,
and DEPTH in 10% steps meaning the *proportion of steps
affected* (a density dial, not an intensity dial); SPEED has
SINGLE/DOUBLE forms. The fixed TYPE 1–10 permutation tables are
not published anywhere in the reference (recorded gap) — the
axis is the mechanism, rendered with the registry's own deals.
Evidence: SP-404MKII Reference v5.5, Scatter page, fetched
2026-10-23.

**Stem-scoped redeal (VirtualDJ Instrument Beat Grid)** —
Beat Grid applies the redeal to the INSTRUMENTAL stems only
while vocal and drums continue linearly: the shuffle as a
routing scope, not a new mechanism — GAP-08's stem vocabulary
composing this base. No grid parameters are documented in the
manual (recorded gap). Evidence: VirtualDJ Manual, Stems pages,
fetched 2026-10-23.
