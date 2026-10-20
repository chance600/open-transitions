# loop_roll_build

**Bank:** T-008 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT), Crossfader

## Signature

```python
loop_roll_build(a, b, sr, bpm, roll_bars=1, hpf_end_hz=6000.0)
```

## Spec

Invent a build-up from slip-mode rolls: 1/2 -> 1/4 -> 1/8 -> 1/16
across the final bar, HPF thinning, release into B's drop.

a: outgoing; the roll happens over its last roll_bars (default 1 bar).
Each beat of the roll bar loops a shrinking slice anchored at the bar
start (digital hot-cue adaptation of the manual roll).
b: incoming drop, slams on the downbeat after the roll.
