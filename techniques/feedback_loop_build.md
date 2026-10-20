# feedback_loop_build

**Bank:** PERF-ZAB · **Automatability:** ADOPT · **Confidence:** medium

**Source:** edu-survey-G §4, performer #2 James Zabiela — Pioneer EFX-1000/DJM beat-FX composition (feedback loops, beat roll, transform); Pioneer DJ "How To DJ" series (2009) + NXS2 trick videos

## Signature

```python
feedback_loop_build(a, b, sr, bpm, bar_s, build_bars=8)
```

## Spec

Zabiela's EFX-1000 move: A's last phrase (build_bars, default 8
bars) runs through a feedback delay (1/2 beat) whose feedback ramps
0.5 -> 0.95 and whose wet mix ramps 0.25 -> 0.85 across the build;
then the loop cuts dead (2 ms guard) and B slams in at full power.
Earlier bars of A pass through untouched.

A feedback loop is a build the room's own sound performs — each
repeat is louder and denser than the last as feedback approaches
unity, so tension rises without any new material. Cutting the loop
dead and slamming B converts that stored energy into the drop.
