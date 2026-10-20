# flying_solo_acapella

**Bank:** GAP-10 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Hype/DDT — Transition Gap Report 2026-10-19, GAP-10

## Signature

```python
flying_solo_acapella(a_stems, b, sr, bar_s, bpm, solo_beats=4)
```

## Spec

All music drops out. A's soloed acapella hangs alone for `solo_beats`
(default 4 beats), loops once more — the naked-vocal reset is the defining
move — then B filters up from a low-pass (400 Hz → 16 kHz, exponential,
over `rise_bars` = 4 bars) *underneath* the still-looping vocal, and the
vocal exits into the drop (100 ms guard fade; B owns beat 1).

T-010 overlays a vocal over a playing instrumental; the naked-vocal reset
(nothing under it at all) is what this move adds. The room hears one human
voice and nothing else — the loudest quiet in the library.

Requires A's vocal stem plus an anchor vocal ("needs":
["stems", "anchor_vocal"]). Loop-point selection inside the vocal phrase
is the ADAPT part: the engine loops the stem head; a DJ picks the exact
phrase that survives being naked twice.
