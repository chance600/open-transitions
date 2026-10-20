# sampler_one_shot_mask

**Bank:** GAP-17 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** Transition Gap Report 2026-10-19 GAP-17 — open-format (sampler one-shot mask)

## Signature

```python
sampler_one_shot_mask(a, b, sr, one_shot_db=-3.0)
```

## Spec

A synthesized one-shot fired exactly on a hard cut to mask the join
and mark the section: a 0.45 s shot (falling saw burst at 196 Hz
with pitch sag + noise stab, exponentially decaying) centred on the
cut at one_shot_db (default -3.0 dBFS), over A (2 ms click guard on
its tail) immediately followed by B at full level.

A hard cut's weakness is the seam — two unrelated spectra meeting
sample-to-sample. The one-shot gives the ear a single foreground
event to attend to (auditory masking) and marks the new section the
way a DJ drop does socially. T-018 builds from continuous noise and
T-029's optional one-shot sits in a void; neither fires a shot over
a live cut, which is the whole point: the music never stops.
