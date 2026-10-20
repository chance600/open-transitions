# whoa_reverb_wobble

**Bank:** DM-A39 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** Philip Harris (@phlourishmusic) — https://www.instagram.com/reel/Dc3HMj2NMqc/?id=3978680445254814364_36159507742&is_sponsored=false&is_ineligible_for_clips_chaining=false (saved 2026-09-05)

## Signature

```python
whoa_reverb_wobble(vocal, sr, tail_s=2.5, reverb_wet=0.9, decay_s=4.0, rate_start_hz=2.0, rate_end_hz=12.0, trem_depth=0.9)
```

## Spec

The 'whoa': a vocal hit drowned in reverb, tail wobbling faster and faster.

A vocal hit is run through a big reverb (90% wet, ~4 s decay, the
clip's settings) with `tail_s` of ringing room appended, then a
tremolo is applied whose rate accelerates exponentially from
`rate_start_hz` to `rate_end_hz` across the clip — the tail starts
breathing slowly and ends up fluttering, the 'wo-wo-wo' wobble.
(The clip also overlaps a reversed copy for a pre-tail; this ADOPT
keeps the signature move — reverb + accelerating tremolo — and
leaves the pre-tail to reverse_vocal_ambience, DM-A23.)

Parameters
----------
vocal : the vocal hit (mono float64) — in the clip, just the first
    bit of the vocal, isolated.
sr : sample rate, Hz.
tail_s : reverb tail room appended after the hit, in seconds
    (default 2.5 s; output is len(vocal) + tail_s long).
reverb_wet : reverb wet mix (default 0.9 = the clip's ~90%).
decay_s : reverb decay (approx. RT60) in seconds (default 4.0 s =
    the clip's ~4 seconds).
rate_start_hz : tremolo rate at the hit, in Hz (default 2.0 Hz).
rate_end_hz : tremolo rate at the tail's end, in Hz
    (default 12.0 Hz — the speed-up is the signature).
trem_depth : tremolo depth, 0..1 (default 0.9; gain dips to
    1 - depth at each trough).

Why it works: the reverb strips the hit of its dry attack context
and stretches it into a pad; a *static* tremolo on that pad would
read as a cheap organ effect, but an accelerating rate creates
forward motion inside a sound that is otherwise only decaying —
energy seems to gather even as level falls, which is exactly the
tension the 'whoa' is used for.
