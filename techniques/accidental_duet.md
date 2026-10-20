# accidental_duet

**Bank:** GAP-12 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Digital DJ Tips (DDT) — Transition Gap Report 2026-10-19, GAP-12

## Signature

```python
accidental_duet(a_stems, b_stems, sr, bpm, bar_s, duet_bars=8)
```

## Spec

Two isolated vocals run simultaneously, tempo/key-synced, so two singers
read as a duet for a section (default 8 bars, 2-beat raised-cosine edge
fades floored at 0.25 — the section swells in over a playing floor, it
never fades from silence — a bounded section, not an infinite overlay). A's instrumental
thins to a pad (its melody stem at 0.5 gain); B's drums hold the grid.
A's drums and bass stay out — one rhythmic engine, one harmonic cushion,
two voices.

T-010 handles exactly one vocal over an instrumental; a vocal-on-vocal
overlay is the gap this fills.

The strictest preconditions in the library, by design: both tracks must
have vocals ("vocal_ok": ["both"]), camelot_max 1, BPM delta ≤ 1% — two
simultaneous singers expose key and tempo mismatches instantly. The ADAPT
part is phrase pairing: which 8 bars of each vocal actually converse is a
human ear call; the engine renders the section once chosen.
