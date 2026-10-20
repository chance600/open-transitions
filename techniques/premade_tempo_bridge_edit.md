# premade_tempo_bridge_edit

**Bank:** GAP-07 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** Transition Gap Report 2026-10-19 GAP-07 — open-format (pre-made tempo-bridge edit / "transition track")

## Signature

```python
premade_tempo_bridge_edit(a, b, sr, bpm_from, bpm_to, bar_s, edit_bars=8)
```

## Spec

The produced-artifact bridge: an 8-bar "transition edit" section
(drums + riser) that itself ramps rate sits between A and B — zero
live pitch work. The edit is synthesized here as the sketch of the
artefact: kick on every beat, offbeat hats, noise clap on beats 2
and 4, riser over the last 4 bars, each bar timed at a tempo ramping
linearly bpm_from -> bpm_to (default example 100 -> 128), peaking at
-3 dBFS.

T-021 ramps tempo live (phase-vocoder, DJ riding the fader). The
transition-edit workflow moves that labour into production: the
tempo change reads as the record doing it, and the DJ only cues two
clean joins (A->edit, edit->B) instead of performing one continuous
ramp. The standard open-format tool for wide tempo jumps.
