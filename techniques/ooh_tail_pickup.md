# ooh_tail_pickup

**Bank:** KEEP-01 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** Lane keeper — Stay High -> Rapture ooh_tail_pickup v4, heart PASS ("SO GOOD", verdict-dataset row 39, 2026-10-20). Promoted to a registry entry in Phase 30; previously a gap-flagged custom-shape recommendation in engine/fit_select.py.

## Signature

```python
ooh_tail_pickup(a, b, sr, bar_s, tail_bars=2, tail_level=0.5,
                tail_decay_bars=2.5)
```

## Spec

A plays at unity, unprocessed, for its full length — no wash, no duck, no master fade. The device is what happens AT the seam: the motif completes, and B enters at full level (a 15 ms raised-cosine anti-click ramp only — click protection, not a fade-in). The only addition is a tail generated from A's last phrase region (its final `tail_bars`): high-passed at 180 Hz (lows stripped), scaled so its RMS equals `tail_level` x A's RMS, and decayed to exactly zero over at most `tail_decay_bars` under B's entrance (clamped to the tail source's length, so the tail never runs past its own material).

The motif itself is caller context: in real use the caller places A's segment so it ends on the tail motif (the keeper's "ooh"); the function does not detect motifs. What transfers is the pickup grammar — dry A, straight B entry, decaying tail — not the keeper's re-picked B passage or its +7 dB entry gain ride.

Why it is not its neighbours: `echo_out` (T-004) throws A's tail into a repeating echo train; this tail is a single decaying phrase tail, not a repeat. `reverb_wash` (T-005) builds a wash A exits inside; here A never enters a wash — it plays dry to its end and the tail is the only residue.

## Selection

Requires a vocal A (vocal_ok a_only/both); tempo- and key-independent (a straight pickup needs no shared grid — the tail overlap is low-stripped and decaying). Prefers an A motif (`a_motif`) and same-genre pairs. Evidence is THIN (n=1 keeper pair) — the fit reasons, not the score, are the claim.
