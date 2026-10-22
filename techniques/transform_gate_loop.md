# transform_gate_loop

**Bank:** PERF-ZAB · **Automatability:** ADAPT · **Confidence:** high

**Source:** James Zabiela, "How To DJ" Episode 3, Parts 7–8 (DJdownload.com presents How to DJ, prod. DJdownload.com + Ministry of Sound TV, 2009) — Part 7: scratching/transforming JZ-style, including a feedback loop of his scratching via the EFX-1000; Part 8: the EFX-1000 transform effect reproducing a transform scratch digitally — looping a scratch sample, introducing the transform effect, improvising patterns on the EFX's beat-select buttons. Episode descriptions fetched first-hand 2026-10-22 (Listen Notes series pages).

## Signature

```python
transform_gate_loop(a, b, sr, bpm, bar_s, gate_bars=4, duty_cycle=0.5)
```

## Spec

A's last `gate_bars` bars are replaced by a loop of A's final bar,
gated by a transform pattern whose subdivision doubles every bar
(1, 2, 4, then 8 gates per beat, capped), each gate open for
`duty_cycle` of its subdivision (1.5 ms click-guarded edges). Then a
hard cut (2 ms guard) and B at full power. Earlier bars of A pass
through untouched.

The material never changes; the *gate pattern* is the performance,
and its acceleration is the build — the same tension curve as a
loop tightening, produced by chopping instead of shortening.
Distinct from the manual two-deck fader chops (GAP-15, the fader
moves between sources), from retrigger stutters (T-019, playback
restarts), and from the vocal tremolo gate (an LFO pattern on an
overlay) — here a single held source is amplitude-gated by a DSP
beat-select pattern the performer switches live. Zabiela's
canonical material is a loop of his own scratching; any held
fragment works.
