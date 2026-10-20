# metric_loop_pivot

**Bank:** PERF-ZAB · **Automatability:** ADAPT · **Confidence:** medium

**Source:** edu-survey-G §4, performer #2 James Zabiela — 2020 3:4 tempo-modulation demo (house 130 -> DnB 173.4 via layered 3/4 and 3/2 loops, no sync)

## Signature

```python
metric_loop_pivot(a, b, sr, bar_s, cycle_beats=3, total_beats=12)
```

## Spec

A's 1-bar groove cell played in 3-beat cycles against the 4-beat
grid for 12 beats (cycle_beats=3, total_beats=12; total must be a
whole number of cycles); a 4-bar lead-in of A precedes the pivot and
B enters at the 12-beat LCM alignment.

House at 130 BPM becomes DnB at 173.4 BPM with no sync because the
tempo ratio 173.4 / 130 = 4/3 is metric, not gradual. Retriggering
a 4-beat cell every 3 beats walks its downbeat against the grid
(3:4 polymeter); after 12 beats — the least common multiple — both
grids agree again, and B enters at the new tempo on a downbeat both
tempi share. The crowd hears a rhythm puzzle resolving, not a tempo
change being performed.
