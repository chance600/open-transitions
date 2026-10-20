# scratch_in

**Bank:** GAP-14 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Transition Gap Report 2026-10-19, GAP-14 — open-format scratch-in / scratch drop (open-format toolkits)

## Signature

```python
scratch_in(a, b, sr, bpm, scratch_beats=1.0)
```

## Spec

Baby-scratch B's first beat in rhythm over A's last phrase, then
release it on the downbeat as A hard-cuts.

Parameters
----------
a : np.ndarray, mono float64
    Outgoing segment. The scratch gesture is mixed over its final
    `scratch_beats` beats (its last phrase); `a` then ends — the
    concatenation with `b` IS the hard cut.
b : np.ndarray, mono float64
    Incoming segment, STARTING on its drop beat (caller aligns: b[0]
    is the first beat that gets scratched and then released).
sr : int or float
    Sample rate, Hz.
bpm : float
    Tempo of the (beatmatched) pair, beats per minute. The scratch
    rhythm is locked to this grid — an off-grid scratch reads as a
    mistake, not a gesture.
scratch_beats : float, default 1.0, unit: beats
    Length of the scratch gesture. One beat is the classic tease:
    long enough for the crowd to register B's timbre, short enough
    that the release still lands as a drop.

Render
------
The gesture is B's drop beat resampled forward/backward as two chirps
(baby scratch: push forward, pull back, twice) via a time-varying
playback-rate envelope (+2x forward, -2x backward, net displacement
zero), mixed at -4 dB over A's final beat. On the next downbeat A
hard-cuts (2 ms click guards only — no fade) and B plays full from
its drop beat.

Why it works: the scratch is a timbral trailer — the crowd hears the
incoming track's first sound as *percussion* before they hear it as
music, so the release on the 1 feels both surprising and inevitable.
It is the incoming-side mirror of the backspin (T-007): T-007 winds
the outgoing track backward; this winds the incoming track forward.
ADAPT because chirp rate/depth are feel parameters — the 2x chirp at
one beat is the documented default, not a law.
