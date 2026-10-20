# same_song_switchup

**Bank:** GAP-13 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** open-format toolkit — Transition Gap Report 2026-10-19, GAP-13

## Signature

```python
same_song_switchup(a_full, a_alt, sr, bar_s, section_bars=2)
```

## Spec

Two arrangements of the *same* track alternated live: 2-bar sections
full ↔ drums-only arrangement for 8 bars, with 50 ms cosine guards at the
flips (the hot-cue flip feel — protective, not audible fades). Familiarity
is constant; only the arrangement changes mid-track. The crowd never hears
a new song, but the floor's energy steps up and down on command.

Renderer-compatible: both arguments are plain audio arrays (the two
arrangements), so this is the one gap_struct technique exported in
TECHNIQUE_FUNCS.

The ADAPT part is prep, not rendering: the two arrangements must be
grid-aligned versions of one track (same tempo, same key, downbeats
coincident). Preconditions encode that literally — bpm_delta_pct_max 0,
camelot_max 0, genre_pair "same". No stems required: the alternate
arrangement can be a second edit, a dub, or a drums stem bounced to audio.
