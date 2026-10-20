# rhythmic_fader_chops

**Bank:** GAP-15 · **Automatability:** ADOPT · **Confidence:** high

**Source:** Transition Gap Report 2026-10-19, GAP-15 — rhythmic fader chops, transformer-style (James Hype / stems-first method + open-format toolkits)

## Signature

```python
rhythmic_fader_chops(a, b, sr, bpm, bar_s, chop_beats=4)
```

## Spec

Transformer-style rhythmic fader chops as the transition gesture:
A is chopped in/out on a quarter-beat grid while B fades in
underneath; A is fully out by bar 5 and B owns the mix.

Parameters
----------
a : np.ndarray, mono float64
    Outgoing segment, phrase-aligned with `b` (overlapping segments
    of equal length; the shorter is zero-padded to the longer).
b : np.ndarray, mono float64
    Incoming segment, aligned so b[0] coincides with a[0] — B is
    already playing (cued and beatmatched) when the chops start.
sr : int or float
    Sample rate, Hz.
bpm : float
    Tempo of the pair, beats per minute (sets the chop grid).
bar_s : float
    Seconds per bar (4 beats). Sets the bar-5 deadline for A's exit.
chop_beats : int, default 4, unit: beats
    Duration of the chop gesture. Four beats (one bar) is the
    statement length: two beats reads as a stutter, eight bars of
    chopping reads as a routine, not a transition.

Render
------
Beats 0..chop_beats: A's channel fader is gated in/out every
quarter-beat (16th-note grid, 50% duty, ~3 ms smoothed edges — hard
digital edges click; a real transformer's edges are fast but never
instantaneous). B fades in underneath over the same span
(0.35 -> 0.75 gain), so A's off-phases are never silence — the
groove's floor transfers before its identity does. After the chops,
A fades out on a cosine curve reaching zero at bar 5 (sample
4 * bar_s * sr), while B completes its fade to unity; past bar 5
the mix is B alone. If the segments end before bar 5, A's fade
compresses to the remaining length (it still ends at zero).

Why it works: the chop turns the crossfader itself into a rhythm
instrument — the crowd hears the *mix* being performed, and the
rhythmic holes in A are exactly where B's groove pokes through, so
by the time A leaves, B has already been the groove for a bar.
Unlike T-030's single committed cut, the gesture is the repetition:
each chop is a downbeat-level reminder that a handover is happening.
