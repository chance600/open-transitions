# underlap

**Bank:** KEEP-02 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** Lane keeper — Rapture -> Kombucha underlap_carry v16a, heart PASS (verdict-dataset rows 76, 94, 2026-10-21). Promoted to a registry entry in Phase 30; previously a gap-flagged custom-shape recommendation in engine/fit_select.py.

## Signature

```python
underlap(a_stems, b_stems, sr, bar_s, zone_bars=12, entry_db=-26.0,
         parity_db=-10.8)
```

## Spec

Over a `zone_bars` zone: B's non-vocal stems enter at `entry_db` (a whisper) and rise on two C1-smooth smootherstep segments — entry -> parity (`parity_db`, the handover anchor, at 2/3 of the zone) -> full (0 dB, at the zone end). A plays at unity until the final two bars, then dissolves to exactly zero at the zone end. B's vocal stem is withheld for the whole zone except its final bar (the re-entry bar), so the first B vocal heard is the re-entry, never a chant leaking under A's exit.

The keeper's parity (-10.77 dB) was solved from its measured components; the generic form fixes parity at -10.8 dB and lets the caller override it. The keeper's stem surgery (zeroing one excerpt bar's stem) is NOT reproduced — the generic move is the emergence curve plus the vocal hold, which is what a new pair can reuse without the keeper's forensic record.

Why it is not its neighbours: `layered_emergence` (T-004c) brings B in as a texture under A; the underlap is a full slow emergence with a solved parity point and a gated vocal re-entry. `stem_element_crossfade` (GAP-08) hands stems over one at a time in stages; the underlap holds B's vocal back while its groove emerges as a whole.

## Selection

Requires stems (the vocal hold is a stem operation). Tempo cap 10% (the Phase 29 Kim-band outlier line); key-unconstrained, because keys coexist only in groove stems while B's vocal is withheld — the keeper worked at Camelot distance 5. Prefers groove (not vocal) B entries and gaps >= 3%. Evidence is THIN (n=1 keeper pair).
