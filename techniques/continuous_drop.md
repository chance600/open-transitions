# continuous_drop

**Bank:** WEB-19 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** kohadachan, "A Personal Drum and Bass DJ how to" (note.com, 2024) — transition-pattern taxonomy, fetched 2026-10-22; family corroborated by DJ.Studio, "How To Mix Drum And Bass" (2024)

## Signature

```python
continuous_drop(a, b, sr, bar_s, stage_bars=8, stage_from_db=-14.0, stage_to_db=-6.0)
```

## Spec

A's drop plays out while B is staged beneath its final bars; B's
drop lands on the exact downbeat A's ends. No breakdown, no
valley — A's drop is the transition surface.

a: outgoing segment, ENDS at its drop's end (caller aligns).
b: incoming segment, STARTS at its drop; its first bar doubles
    as the staging cell.
stage_bars: staging window inside A's tail (source's number: 8;
    4 = late staging, 16 = the long liquid form). Across the
    window, B's first bar loops with lows killed (−60 dB low
    band), ramping −14 -> −6 dB against the window's own peak.
At A's final sample, B starts at full level.

Distinct from build_to_drop (T-009: two BUILDS layer, only B
drops), breakdown_transition (T-023: seam inside a breakdown —
the energy opposite), hook_drop_handoff (T-038: A exits on a
vocal hook; here A exits by completing its drop). The sparse
cousin, DJ.Studio's "Intro Over Outro", is an EQ-blend staging,
not this base: here both segments are drops.
