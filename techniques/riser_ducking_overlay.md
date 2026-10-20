# riser_ducking_overlay

**Bank:** T-035 · **Automatability:** ADOPT · **Confidence:** high

**Source:** Technique bank T-035 — Riser Ducking & Placement (derived from production sidechain practice, MusicRadar 'Sidechains'; first written recipe in the bank, first parameterized software recipe here)

## Signature

```python
riser_ducking_overlay(x, sr, bar_s, bpm, pre_drop_bars=8)
```

## Spec

The bank's T-035 ducking recipe as a renderable overlay: a riser
ducked into the kick's gaps over the final phrase, hard-cut on the
drop's Beat 1, with a downlifter covering the drop's first 2 beats.

This is the first parameterized software recipe for T-035 — the bank
entry itself notes that no DJ tutorial documents riser ducking; the
parameters below ARE the bank's spec, made executable.

Parameters
----------
x : np.ndarray, mono float64
    The mix segment the riser rides over. It must END exactly on
    the drop's Beat 1 (caller aligns: x's last sample is the final
    sample before the drop). The riser occupies the last
    `pre_drop_bars` bars of `x` (or all of `x` if shorter).
sr : int or float
    Sample rate, Hz.
bar_s : float
    Seconds per bar (4 beats). Sets the placement grid.
bpm : float
    Tempo, beats per minute. The ducking follows the kick grid at
    this tempo (one dip per beat, i.e. per kick in 4/4).
pre_drop_bars : int, default 8, unit: bars
    Riser length. T-035 placement rule: start on Bar 1 of the FINAL
    8-bar phrase before the transition — never earlier (a 16-bar
    riser exhausts the crowd).

Render (the T-035 recipe, parameter for parameter)
---------------------------------------------------
- Placement: riser starts Bar 1 of the final `pre_drop_bars`-bar
  phrase, peaks at the last beat, ENDS on the drop's Beat 1 — it
  never overlaps the drop.
- Level: the riser peaks -6 dB UNDER the mix (measured from x's
  own peak: riser_level_db = mix_peak_db - 6 dB).
- Ducking: sidechain-style pumping at 4:1 character, rendered as
  3 dB dips on every kick hit (5 ms attack, 100 ms release) for
  bars 1-4 only — the bank's manual-method window; in bars 5-8 the
  riser rises un-dipped as the arrangement strips back (the dsp
  synth's duck_bars=4).
- Filters: high-pass 200 Hz (never fights the kick's sub),
  low-pass 12 kHz (leaves air for the drop's crash).
- Exit: the riser is hard-cut at x's final sample (the drop's
  Beat 1). A synthesized downlifter (reverse crash) is APPENDED as
  a 2-beat tail: it is the cover for beats 1-2 of the drop bar, and
  the caller overlaps it onto the drop (the demo does exactly
  this) — sequentially auditioned, it reads as the crash decay
  that masks the cut.

Why it works: a riser is broadband energy competing with the track.
Ducking carves it into the kick's gaps (rhythmic slotting), so it
breathes inside the groove instead of sitting on top; the -6 dB
ceiling keeps it subliminal until the final bars, when the
arrangement strips back and the riser becomes the track. The hard
cut + downlifter exit gives the drop its full frequency space
while masking the riser's absence. This is an overlay (FRAMEWORK
§6): it decorates a base render rather than handing over between
two tracks, which is why its signature takes a single segment.
