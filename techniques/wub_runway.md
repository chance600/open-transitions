# wub_runway

**Bank:** KEEP-03 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** Lane keepers — Balkans -> Cola wub_runway v11-solo, heart PASS, and v10b-with-drums, PASS (verdict-dataset rows 103, 120, 2026-10-21/22). Promoted to a registry entry in Phase 30; previously a gap-flagged custom-shape recommendation in engine/fit_select.py.

## Signature

```python
wub_runway(a_stems, b_stems, sr, bar_s, runway_bars=6, figure="melody",
           intro_bars=4, tail_bars=4)
```

## Spec

Intro: A plays full for `intro_bars`. Runway: A's drums are cut at the runway start and A's vocal is excluded from the tail; A's remaining stems (bass + melody) ease out attenuation-only on a smootherstep dB curve (0 dB -> -60 dB) reaching exactly zero at the runway end. Meanwhile B's signature figure (`figure` stem, default melody) tiles across the runway in plays, play-staged: play 1 ramps -1.0 -> -0.5 dB, play 2 ramps -0.5 -> 0 dB, play 3+ sits at 0 dB. After the runway, B proper continues from where the figure's first play left off.

The keeper's runway curve was a per-bar PCHIP solve from its components; the generic form is the smootherstep dB curve, which preserves the properties that matter (attenuation-only, exact zero at the runway end) without the keeper's numbers. The figure is caller-nominated: the caller passes the stem that IS the signature figure for the pair.

Why it is not its neighbours: D10 recognition-first staging is the rationale — the listener recognizes B by its figure before B proper arrives, with drums excluded so the figure, not a beat, is what registers. `stem_element_crossfade` (GAP-08) hands elements over in stages; the runway previews one figure while A eases out whole.

## Selection

Requires stems (figure isolation + drums exclusion are stem operations). Tempo cap 5% — the runway is staging, not tempo work. Key-unconstrained: the keeper worked at Camelot distance 6 because A vocal is excluded, A drums are cut, and coexistence is A bass/melody under a featured figure. Prefers a B signature motif and Delta~0%. Evidence is THIN (n=1 keeper pair, two standing variant lines).
