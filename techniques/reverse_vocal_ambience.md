# reverse_vocal_ambience

**Bank:** DM-A23 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** Russell Jarvis (@morsbeats_) — https://www.instagram.com/reel/DKzpecXsAgh/?id=3653446134681045025_52378568733&is_sponsored=false&is_ineligible_for_clips_chaining=false (saved 2025-06-12)

## Signature

```python
reverse_vocal_ambience(vocal, sr, delay_s=0.375, feedback=0.4, delay_wet=1.0, reverb_decay_s=3.5, reverb_wet=0.85, swell_s=1.5)
```

## Spec

Reverse-vocal ambience: a reverb/delay swell that blooms INTO the vocal.

The vocal is reversed, run through a feedback delay at 100% wet and
then a heavy reverb, and the whole result is reversed back to the
original orientation. Every tail the chain generates in reversed
time lands *before* its source event in forward time, so the vocal
arrives preceded by its own ghost — a swelling pre-drop texture
built from nothing but the vocal itself. `swell_s` of headroom is
padded into the reversed pass so the tails have somewhere to ring;
it becomes the pre-swell in the output, which is therefore
len(vocal) + swell_s long.

Parameters
----------
vocal : vocal segment (mono float64). Works best on a vocal that
    already has a little reverb/delay printed — the printed tails
    give the chain more to smear (the clip's own note).
sr : sample rate, Hz.
delay_s : feedback-delay time in seconds (default 0.375 s).
feedback : delay feedback ratio (default 0.4 = the clip's 40%).
delay_wet : delay wet mix (default 1.0 = the clip's 100% wet).
reverb_decay_s : reverb decay (approx. RT60) in seconds
    (default 3.5 s — "heavy").
reverb_wet : reverb wet mix, 0..1 (default 0.85).
swell_s : pre-swell headroom in seconds (default 1.5 s).

Why it works: reverb and delay are causal — tails only ever follow
their source. Reversing the signal before the chain and reversing
back after it is the only way to make a tail precede its source
without time travel, and because the swell is literally the vocal's
own spectrum played backwards, it harmonizes with the entrance
perfectly while reading as pure atmosphere.
