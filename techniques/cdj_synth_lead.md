# cdj_synth_lead

**Bank:** DM-A15 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** LoDran (@jred_in_ya_area) — https://www.instagram.com/reel/DA-8LgSIMNV/?id=3476480635745387349_288018017&is_sponsored=false&is_ineligible_for_clips_chaining=false (saved 2025-02-24)

## Signature

```python
cdj_synth_lead(x, sr, bar_s, loop_beats=1.0, root_hz=110.0, level_db=-6.0)
```

## Spec

CDJ-as-synth: turn a short loop grab into a playable lead layer.

The CDJ trick — grab a very short loop, tighten it to a single cycle,
disable Master Tempo, tune it with the (wide) pitch fader, colour it
with a band-pass sweep and ping-pong delay — is single-cycle
synthesis. This renders it directly: one cycle is extracted from a
`loop_beats` grab at the head of `x` (rising-zero-crossing pair),
resampled to `root_hz` (the resample IS the pitch tuning — playback
rate and pitch stay coupled, exactly like Master Tempo off), tiled
for the length of `x`, swept through a rising band-pass, and given a
two-tap feedback-delay tail (mono approximation of ping-pong: dotted
3/4-beat and 1/2-beat taps alternate energy the way the stereo
original bounces it side to side).

Parameters
----------
x : source segment (mono float64); the cycle is grabbed from its
    first `loop_beats`, and the lead is rendered len(x) long so it
    can be layered over the same groove it was grabbed from.
sr : sample rate, Hz.
bar_s : seconds per bar (sets the delay taps via beat = bar_s / 4).
loop_beats : loop-grab length in beats (default 1.0 beat — the
    clip tightens from a short loop down to one cycle; the grab only
    needs to contain a clean cycle or two).
root_hz : target root pitch in Hz (default 110.0 Hz = A2). Tune this
    to the track's key — the lead is a pitched instrument now.
level_db : lead peak level relative to x's peak, in dB
    (default -6.0 dB, so the layer sits on the groove, not over it).

Why it works: any periodic-enough slice of audio, looped at cycle
length, becomes an oscillator whose timbre is the slice's harmonic
content — a kick+bass grab turns into a buzzy synth tone for free.
Because the cycle comes from the track itself, the lead's harmonics
are guaranteed to belong to the track's sound world.
