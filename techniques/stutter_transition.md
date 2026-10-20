# stutter_transition

**Bank:** T-019 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** null-set-ai-dj (MIT); hot-cue transient placement needs onset detection

## Signature

```python
stutter_transition(a, b, sr, bpm, cue_t, cue_len_s=0.25, tap_beats=(3.0, 3.5, 4.0, 4.5), release_t=None)
```

## Spec

Re-trigger B's iconic vocal word in accelerating taps, then release.

a: outgoing; its final bar is the stutter bar (4 beats).
b: incoming track (full). cue_t: hot-cue position (seconds) of the
    iconic word's transient in b. cue_len_s: slice length per tap.
tap_beats: 1-indexed beats within the final bar (default 3, 3-and,
    4, 4-and — the accelerating "Ye-Ye-Ye-Yeah!").
release_t: where b plays from after the bar (default: cue_t — LET IT
    PLAY from the cue).
Each tap is low-killed (the stutter is percussion, not bass). On the
last tap, a's fader dies; b enters full with lows restored.
