# delay_drum_roll

**Bank:** WEB-38 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** DJ Mag, Tips & Tricks for DJs — "set the delay time to 1/2 and engage the effect with the dry/wet control completely closed. As you approach the end of the phrase... quickly twist the dry/wet to around 11am — leave it open for 2–4 beats and then slam the rotary back to the left as the beat drops back in"; https://djmag.com/content/tips-tricks-djs, fetched first-hand 2026-10-25.

## Signature

```python
delay_drum_roll(a, b, sr, bar_s, bpm, roll_beats=4, delay_beats=0.5)
```

`delay_drum_roll` — family SPACE, exit snap, energy delta 1 (rising).

## Spec

A 1/2-beat delay send opens briefly to fake a drum roll, then slams shut as B drops.

    Rendered: A's last `roll_beats` beats carry a feedback
    delay (division `delay_beats`, feedback 0.45) whose wet
    level ramps 0 -> 0.6 over the roll, then cuts to zero at
    the handoff while B drops full on the beat. The roll is an
    illusion — no loop, no new rhythm, just the delay line
    doubling the existing groove into density — and the slam
    shut is part of the technique: a roll that bleeds into B
    is a wash, not a roll.

    Why it is not its neighbours: not T-004 `echo_out` (the
    tail covers B's entrance — here the delay is cut BEFORE
    B, and B drops dry); not WEB-31 `echo_out_reset` (a tail
    standing alone to reset the metronome — here the delay
    builds density into a drop, same tempo); not T-008
    `loop_roll_build` (a loop roll, not a delay illusion).

## Parameters

- `roll_beats` (int, 1–8, default 4): roll span in beats. 2
  is short, 4 the source's standard.
- `delay_beats` (float, 0.25–1.0, default 0.5): delay division
  in beats. 0.25 is the quarter staging, 0.5 the source's half.

## Selection

Requires: BPM delta ≤ 10% (the roll is beat-synced), no key
gate, vocal pair any, A's phrase build / chorus / outro,
genre pair same / neighbor, no needs.
Prefers: A's phrase build (+2, the roll is drama before a
drop — a build is its home phrase); energy delta ≥ 1 (+1,
the slam shut pays off into a bigger B).
