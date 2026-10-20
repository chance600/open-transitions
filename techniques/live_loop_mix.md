# live_loop_mix

**Bank:** DM-A14 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** French Candy — https://www.instagram.com/reel/DGLi_b8CgRn/?id=3570101022527980647_358532258&is_sponsored=false&is_ineligible_for_clips_chaining=false (saved 2025-02-19)

## Signature

```python
live_loop_mix(a, b, sr, bpm, bar_s, loop_bars=2, trans_depth=0.85, ramp_beats=8.0)
```

## Spec

Live loop mix: A's outro locks into a short auto-loop while B enters.

The last `loop_bars` of `a` are tiled for the full render (the deck's
AUTO LOOP), a TRANS-style gate chops the loop in 1/4-beat slices, B's
fader comes up over `ramp_beats`, and the loop fades out underneath —
the Pioneer DDJ move (SYNC + PLAY, AUTO LOOP, TRANS at 1/4) rendered
as a two-track transition.

Parameters
----------
a : outgoing segment (mono float64); only its final `loop_bars` are
    used — the caller passes A's outro, the loop IS the outro once
    engaged. Loop points are assumed bar-aligned.
b : incoming segment (mono float64); the output is len(b) long.
sr : sample rate, Hz.
bpm : tempo of the pair, beats per minute (sets the TRANS grid).
bar_s : seconds per bar.
loop_bars : auto-loop length in bars (default 2 bars, the clip's
    setting; the bank's T-027 discipline caps transition loops at
    2 cycles of material).
trans_depth : TRANS gate depth, 0..1 (default 0.85) — how far the
    gated slices duck. 1.0 = full on/off chopping.
ramp_beats : fader move duration in beats (default 8.0 beats = 2 bars
    at 4/4): B rises 0->1 while the loop falls 1->0, raised-cosine.

Why it works: the loop freezes A's groove so its rhythm never decays
while hands are busy; the 1/4-beat gate is pure theatre on top of a
stable loop — it signals "something is happening" without disturbing
the underlying pulse, and because the gate period divides the beat,
the chops land on grid and read as rhythm, not as dropouts. B entering
under a still-full-energy loop hides the seam the fader move makes.
