# tempo_double_trick

**Bank:** DM-A21 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** French Candy — https://www.instagram.com/reel/DHlriZFiyIK/?id=3595471356923945482_358532258&is_sponsored=false&is_ineligible_for_clips_chaining=false (saved 2025-03-25)

## Signature

```python
tempo_double_trick(a, b, sr, bar_s, ramp_bars=4, ramp_curve='linear')
```

## Spec

Tempo double trick: A's tail pitch-ramps 1x -> 2x, B enters at 2:1.

The last `ramp_bars` of `a` are played with a vinyl-style rate ramp
from 1.0 to 2.0 (pitch-coupled — pitch and tempo double together,
Master Tempo off, the CDJ wide-range pitch-fader move). The ramp
consumes the tail in tail/mean-rate time; at the alignment point,
where A reaches exactly double tempo, `b` enters full. For the move
to land on grid, B's tempo must be (close to) twice A's — see the
META `needs: [half_double_ok]` precondition.

Parameters
----------
a : outgoing segment (mono float64); its final `ramp_bars` are the
    ramp, everything before plays untouched.
b : incoming segment (mono float64) at ~2x A's tempo; appended in
    full at the alignment point (3 ms protective fade-in only —
    it enters FULL, not faded).
sr : sample rate, Hz.
bar_s : seconds per bar (of A — the ramp length is measured in A's
    bars).
ramp_bars : length of A's tail that is ramped, in bars
    (default 4 bars).
ramp_curve : "linear" (steady fader push, default) or "exp"
    (2**u — slow start, fast finish, more turntable-like).

Why it works: a pitch-coupled doubling is heard as the *same track*
accelerating, not as a new track — the ear tracks A's timbre through
the ramp, so when B locks in at the doubled rate the tempo jump
feels earned rather than imposed. Keeping B's vocal at its natural
pitch (it never goes through the ramp) is the clip's point: A's
sacrifice buys B's intact entrance.
