# strip_down_buildup

**Bank:** GAP-09 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** James Hype / stems-first method (Hype/stems) — Transition Gap Report 2026-10-19, GAP-09

## Signature

```python
strip_down_buildup(a_stems, b, sr, bar_s)
```

## Spec

The build is progressive element *removal* on the outgoing track, not
addition on the incoming one:

- Bars 1–4: A full (drums+bass+melody+vocal).
- Bars 5–8: A's drums stem muted — the groove hollows out.
- Bars 9–12: A's bass stem muted — only vocal+melody exposed.
- Bar 13, beat 1: B's full drums+bass slam in at unity; A is cut.

Discrete staged muting is the build itself (a 5 ms click guard at each
step, inaudible). T-022 strips *to* drums — the inverse; T-003 thins
continuously by filter. Here the low end drains away so the slam lands
relative to near-silence down low, not relative to A's kick.

Requires stems on A ("needs": ["stems"]). Best with a vocal on A: the
exposed vocal+melody passage (bars 9–12) is the payoff image.
