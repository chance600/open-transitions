# beat_switch_under_acapella

**Bank:** GAP-11 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** open-format toolkit — Transition Gap Report 2026-10-19, GAP-11

## Signature

```python
beat_switch_under_acapella(a_stems, b_stems, sr, bar_s)
```

## Spec

One acapella runs uninterrupted (looped, 8 bars) while the instrumental
underneath it is swapped at bar 4: A drums+bass → B drums+bass (5 ms guard
crossfade at the switch). The vocal is the constant, the beats rotate.

Adjacent to T-010 but inverted: T-010's overlay window ends with the vocal;
here the vocal never stops and the *bed* is what changes. That makes it a
genre pivot — a continuous, familiar vocal carries the room across a leap
the drums alone couldn't — and it can repeat (swap again at the next
phrase) without the vocal ever breaking.

Requires stems on both tracks plus A's anchor vocal ("needs":
["stems", "anchor_vocal"]). Tempo tolerance is tight (1.5%): the looped
vocal must sit on both grids. Key tolerance 2 — the vocal rides over B's
bass for half the move.
