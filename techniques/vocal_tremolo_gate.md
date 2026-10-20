# vocal_tremolo_gate

**Bank:** DM-A44 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** PascFrenk — https://www.instagram.com/reel/Dbv_hcQxFuq/?id=3958661972500962218_73805508040&is_sponsored=false&is_ineligible_for_clips_chaining=false (saved 2026-10-19)

## Signature

```python
vocal_tremolo_gate(x, sr, bpm, subdiv=16, ramp_start_frac=0.5, depth_max=1.0)
```

## Spec

House vocal tremolo gate: 1/16 amplitude tremolo, amount slammed in.

Mono adaptation — stated honestly: the source trick is Ableton's
Auto Pan at Phase 360°, Rate 1/16, with the Amount automated up to
100% on one target note. At 360° phase the two channels' LFOs are
IN PHASE — left and right receive the *same* gain at every instant —
so the stereo original folds down to mono as a pure amplitude
tremolo with nothing lost: there is no stereo width in the source
effect to lose. This function is that exact fold-down: a sine-LFO
amplitude tremolo locked to the 1/`subdiv` grid, with the amount
(depth) automation rising steeply (fast-attack cubic) from
`ramp_start_frac` to 100% at the end of the segment — caller aligns
the segment so the target note sits in the ramp's second half.
(The clip's Warp Mode Complex step is a DAW playback setting for
stretching the clip, not part of the effect; it has no audio-DSP
counterpart here.)

Parameters
----------
x : vocal segment (mono float64).
sr : sample rate, Hz.
bpm : tempo, beats per minute (sets the tremolo rate: at
    subdiv=16 the LFO runs at 16th notes = bpm * 16 / 240 Hz).
subdiv : tremolo grid as a note-value denominator (default 16 =
    1/16 notes, the clip's rate).
ramp_start_frac : where the amount automation starts rising, as a
    fraction of len(x) (default 0.5 — dry first half, gated second
    half, amount reaching 100% at the end).
depth_max : maximum tremolo depth at amount=100%, 0..1
    (default 1.0 — full gating, gain touches zero at LFO peaks,
    which is what makes the vocal read as stuttered syllables).

Why it works: a grid-locked tremolo doesn't fight the groove, it
*joins* it — the vocal starts chopping in the same 16th-note
language as the hats. Automating the amount instead of switching
the effect on keeps the entrance musical: the listener hears the
vocal gradually taken over by the rhythm, and the moment depth hits
100% the chop becomes the hook.
