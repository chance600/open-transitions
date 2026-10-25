# bed_tempo_switch

**Bank:** WEB-32 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Pioneer DJ blog, "A complete guide to multi-deck mixing" — Djrum's ambient third-deck bed; https://blog.pioneerdj.com/djtips/a-complete-guide-to-multi-deck-mixing/, fetched first-hand 2026-10-24. Corroboration: DJ.Studio, "Techno DJ Techniques" — ambient / minimal tracks as bridges; https://dj.studio/blog/dj-techno-music, fetched first-hand 2026-10-24.

## Signature

```python
bed_tempo_switch(a, b, sr, bar_s, bed=None, bed_bars=4)
```

`bed_tempo_switch` — family STRUCT, exit seamless, energy delta 0 (flat).

## Spec

A beatless third-deck ambient bed covers a hard tempo discontinuity; B drops at the new tempo from the bed.

    Pioneer DJ's multi-deck guide: Djrum "showed how an ambient
    track on a third deck can be used as a transitional sound
    bed for big switches between tempos." DJ.Studio corroborates
    the shape from the other side: ambient / minimal tracks
    "serve as excellent bridges between more high-energy techno
    tracks." The mechanism is the bed's beatlessness: with no
    kick, no hats, no tempo reference sounding, the room's
    metronome is unanchored, so B can arrive at a wholly
    different tempo without a ramp, a stretch, or a clash.

    Rendered: A crossfades into the bed over its final 2 bars
    (equal-power); the bed sustains alone for `bed_bars` bars
    total; B enters dry at full level on the next downbeat.
    When the caller supplies no bed audio, a neutral synthesized
    pad (slow sines, 1-bar attack/release) stands in — the
    structure, not any particular bed's content, is the
    technique.

    Why it is not its neighbours: not T-021 `tempo_bridge`
    (a live pitch-preserving ramp — here nothing ramps; the
    tempo jumps under cover); not WEB-31 `echo_out_reset`
    (A's OWN tail covers a brief reset — here a THIRD deck's
    sustained bed covers a phrase-scale switch); not T-023
    `breakdown_transition` (a drumless BLEND of two tracks —
    here the bed is neither track, and B drops after it, not
    through it).

## Parameters

- `bed_bars` (int, 2–8, default 4): bed length in bars,
  including the 2-bar crossfade. 2 is the floor (crossfade
  only, no sustain); 8 is the long-sustain staging.
- `bed` (caller-supplied or None): ambient bed audio. None
  falls back to the neutral synthesized pad. Tempo endpoints
  are caller context: the render proves the bed structure,
  and the demo's fixed sketch BPM means the demo proves
  structure, not the discontinuity itself — recorded as a
  caveat, not hidden.

## Selection

Requires: no BPM or key gate (the bed erases both), vocal pair
any, A's phrase outro / verse / chorus / breakdown / build,
genre pair same / neighbor / leap, third deck available
(`third_deck` need).
Prefers: genre leap (+3, the bed covers leaps the ramp cannot
— no tempo reference sounds during the switch); BPM delta
≥ 10% (+2, large tempo gaps are the bed's home ground, not
the ramp's).

## Demo

`demos/ext_genre.py`: A 8 bars crossfading into the neutral pad
bed over its final 2 bars; bed sustains 4 bars total; B drops
at 10 bars. Handoff = the drop. Sketch caveat: fixed sketch BPM
— structure demo only.

## Variants

`bed_bars` presets 2bar / 4bar / 8bar → 3 variants (single-axis base).
