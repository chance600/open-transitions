# polyrhythmic_loops

**Bank:** GAP-04 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Transition Gap Report 2026-10-19 GAP-04 — open-format (polyrhythmic looping)

## Signature

```python
polyrhythmic_loops(a, b, sr, bar_s)
```

## Spec

Two loops with contrasting patterns layered as an evolving transition
bed: A's first bar as a 4-beat cycle against B's first 3 beats as a
3-beat cycle, each at -3 dB, for 12 beats, under a slow HPF opening
(200 -> 1500 Hz). A 4-bar lead-in of A precedes the bed; B enters in
full on the alignment.

The two cycles disagree for 11 beats and agree on beat 12
(LCM(3, 4) = 12), so the bed feels like it is searching and then
locks — B's entrance is heard as the resolution the polyrhythm was
pointing at. T-020 layers one static glue loop; two loops in metric
conflict are a different, evolving device.
