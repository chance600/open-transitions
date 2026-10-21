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
