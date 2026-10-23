# cyclic_speed_dip

**Bank:** WEB-27 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Roland SP-404MKII Reference v5.5 (official) — Downer MFX page; fetched first-hand 2026-10-23.

## Signature

```python
cyclic_speed_dip(a, b, sr, bpm, bar_s, dip_bars=8, rate_beats=4.0, depth=0.45, pitch_correct=False, fade_bars=1)
```

`cyclic_speed_dip` — family DYN, exit snap, energy delta -1 (falling).

## Spec

Playback rate dipped cyclically, on a tempo-period LFO.

    The SP-404MKII's Downer "cyclically slows down the audio
    playback speed": RATE is musical (2/1..1/32), DEPTH sets how
    far the rate falls, FILTER attenuates HF as the speed drops,
    and PITCH ON converts the lowered pitches back ("pitches
    lowered due to the change in speed are converted to their
    original pitch") — a time-stretch dip instead of varispeed.

    Rendered as a transition: across A's final `dip_bars`, the
    playback rate follows rate(t) = 1 - depth * pulse(t), the
    pulse a raised cosine with period `rate_beats` beats on the
    output clock. The segment LENGTHENS (it is consumed slower);
    a lowpass tracks the instantaneous rate, so each dip darkens
    as it sags. With pitch_correct=True each period-chunk is
    phase-vocoder stretched to its dipped duration instead, so
    the tempo sags but the pitch holds. B fades in over
    `fade_bars` at the end of the dipped segment.

    Why it is not its neighbours: not `brake_stop` T-006 (a
    ONE-SHOT terminal deceleration — this returns to full rate
    every period and never stops); not `screwed_treatment` T-039
    (a static drag at one rate); not `tempo_bridge` T-021 (a
    one-way ramp between two tempos — this oscillates around one).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (clocks the LFO).
    bar_s : seconds per bar.
    dip_bars : dipped window at A's end (default 8).
    rate_beats : LFO period in beats (default 4).
    depth : rate-fall fraction (default 0.45).
    pitch_correct : Downer's PITCH ON (default False).
    fade_bars : B's entrance crossfade (default 1).

    Returns a mix whose A part is longer than A's dipped window
    by ~1/(1 - depth/2); total = len(a) - window + dipped + len(b).
