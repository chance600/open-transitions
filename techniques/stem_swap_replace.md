# stem_swap_replace

**Bank:** WEB-25 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** VirtualDJ Manual — Stems 2.0 / Sampler (StemSwap banks) / Pads (Stems) pages, official virtualdj.com; fetched first-hand 2026-10-23.

## Signature

```python
stem_swap_replace(a_stems, b_stems, sr, bar_s, swap_stems=('drums',), loop_bars=2, start_bar=4, swap_bars=8, tail_bars=4)
```

`stem_swap_replace` — family ROUTING, exit loop, energy delta 0 (flat).

## Spec

A captured stem loop replaces the host's own stem, gated.

    VirtualDJ's StemSwap sampler: a pad records a stem-selected
    loop from one track; triggered on the deck playing another,
    "stems samples from a StemSwap bank will mute the
    corresponding stem from the track playing on the deck where
    the sample was triggered, effectively 'swapping' the stems."

    Rendered: B plays full for `start_bar` bars. For `swap_bars`
    bars, B's `swap_stems` are muted and A's same stems — captured
    as a `loop_bars` loop, decoupled from A's playhead — play in
    their place through B's timeline. When the gate ends, B's own
    stems return (3 ms guards at the gate edges); B plays out for
    `tail_bars` bars. The swap is a sustained substitution inside
    one host track, not a handover: nothing requires the mix to
    move to A.

    Why it is not its neighbours: not GAP-08
    `stem_element_crossfade` (two linear playheads, a staged
    16-bar progressive handover — here the donor is a captured
    loop, the replacement instantaneous, trigger-gated and
    reversible); not GAP-16 `spare_deck_element_firing`
    (synthesised elements ADDED over an EQ bed — nothing is muted
    and nothing is captured); not WEB-21 `drop_insert` (the whole
    MIX is substituted at a drop downbeat — here only the named
    stems, inside a continuing host).

    Parameters
    ----------
    a_stems, b_stems : dicts {"drums","bass","melody","vocal"}.
    sr : sample rate (Hz). bar_s : seconds per bar.
    swap_stems : stem names replaced (default ("drums",)).
    loop_bars : captured loop length in bars (default 2).
    start_bar : bar where the gate opens (default 4).
    swap_bars : gate length in bars (default 8).
    tail_bars : B plays out after the gate (default 4).

    Returns a mono float64 mix of (start+swap+tail) bars.
