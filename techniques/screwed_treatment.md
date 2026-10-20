# screwed_treatment

**Bank:** T-039 · **Automatability:** ADOPT · **Confidence:** high

**Source:** DJ Screw canon (pitch-coupled slowdown + chops); 'slowed + reverb' variant; note ideas #20, #27, #39

## Signature

```python
screwed_treatment(x, sr, bpm=None, rate=0.7, pitch_coupled=True, chop_every_beats=0, chop_repeats=2)
```

## Spec

Chopped-and-screwed style track treatment (pre-transition).

The idea IS the treatment (note ideas #20, #27, #39): slow the track
down DJ-Screw style, optionally with chop/retrigger stutters.

Parameters
----------
rate : playback rate (< 1 = slowed, > 1 = sped up). Classic screw zone
    is 0.6-0.8.
pitch_coupled : True (default) = vinyl-style — pitch drops WITH tempo
    (the authentic Screw sound). False = phase-vocoder slowdown,
    tempo drops but pitch holds ("slowed + reverb" style).
chop_every_beats : 0 = no chop; else every N beats the last beat
    retriggers `chop_repeats` times (the chop). Needs bpm.
bpm : required when chopping.
