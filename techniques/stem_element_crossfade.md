# stem_element_crossfade

**Bank:** GAP-08 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** James Hype / stems-first method (Hype/stems) — Transition Gap Report 2026-10-19, GAP-08

## Signature

```python
stem_element_crossfade(a_stems, b_stems, sr, bar_s, order=("bass","drums","melody","vocal"), bars_per=4)
```

## Spec

A 16-bar handover one stem at a time. A plays full for bars 1–4; then per
4-bar stage, B's next stem (default order: bass → drums → melody → vocal)
enters at unity while A's corresponding stem mutes with a 1-beat
equal-power crossfade.

The signature move is stage one (bars 5–8): B's isolated bassline plays
under A's *intact* drums/melody/vocal — a bass entry with no kick attached.
EQ tools cannot do this: opening B's low band always brings B's kick with
it; only a stem separates bass from kick. T-001/T-002 hand over frequency
bands, never elements.

Requires stems on both tracks ("needs": ["stems"]). Key matters more than
in a band blend — B's bare bass sits against A's melody for a full stage —
so camelot_max is 2. Stems not listed in `order` stay with A throughout.
