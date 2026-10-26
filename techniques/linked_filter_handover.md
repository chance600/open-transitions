# linked_filter_handover

**Bank:** WEB-42 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Allen & Heath Xone:92 User Guide p. 24 (manualsdir mirror) — VCF LINK 2-1: "the low frequencies of channel 1 will be accurately joined to the high frequencies of channel 2... incredibly smooth mixes"; fetched first-hand 2026-10-26 (https://www.manualsdir.com/manuals/554322/allenheath-xone-92-xone92.html?page=24).

## Signature

```python
linked_filter_handover(a, b, sr, bpm, bar_s, handover_bars=4)
```

`linked_filter_handover` — family FREQ, exit snap, energy delta 0 (flat).

## Spec

One cutoff joins A below to B above; the join travels down.

    The Xone:92's VCF LINK 2-1 switch links FILTER 2's FREQ to
    FILTER 1's: "FILTER 2 FREQ can now be controlled by the FREQ
    VCF sweep control of FILTER 1... assign Channel 1 to Filter 1
    and Channel 2 to Filter 2. Select a low pass filter on filter 1
    and a high pass on filter 2. With both filters ON and the link
    switch selected, the low frequencies of channel 1 will be
    accurately joined to the high frequencies of channel 2. This
    can be used to produce incredibly smooth mixes or to mix tracks
    that would otherwise clash when mixed conventionally."

    Rendered as a transition: the handover window is A's final
    `handover_bars` overlapped with B's first `handover_bars`.
    Across it ONE cutoff trajectory log-falls 8 kHz -> 150 Hz: A
    passes through a lowpass at that cutoff, B through a highpass
    at the same cutoff, and the two filtered signals sum. At every
    instant the spectrum is partitioned at exactly one frequency —
    A owns below it, B above it — so the join is exact, with no
    gap band and no overlap band; as the cutoff falls, B takes over
    progressively from the top down. Past the window B plays full.

    Why it is not its neighbours: not T-003's dual-VCF
    counter-sweep axis (two INDEPENDENT sweeps, one per side,
    with no render — here the two filters share one parameter,
    and the exactness of the join is the mechanism); not
    `eq_blend` (fixed band gains — no moving partition); not
    `bass_swap` (a 1-beat bass exchange — this is a
    full-spectrum handover over bars, top-down rather than
    bottom-up).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    handover_bars : overlap window in bars (default 4).

## Selection

Requires: no BPM gate, no key gate, vocal pair any, A's phrase outro / chorus,
genre pair same / neighbor / leap, no needs.
Prefers: genre pair neighbor (+2, the exact spectral join is the clash-proof handover — neighbouring genres that would fight in a plain blend meet at one cutoff); camelot <= 2 (+1, the join is exact at one cutoff, so a close key pair hands over without a clash window).
