# tempo_bridge

**Bank:** T-021 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT); the engine's authorized time-stretch primitive

## Signature

```python
tempo_bridge(a, sr, bpm_from, bpm_to, bar_s, ramp_bars=12, method='ramp')
```

## Spec

Cross wide BPM gaps without chipmunk vocals.

method "ramp": pitch-preserving phase-vocoder ramp over ramp_bars —
    ONE continuous pass with a per-frame rate envelope (~1 BPM/bar;
    the brain reads it as pre-drop tension, not a DJ error).
    Master-Tempo behavior.
method "half_double": exact 2x/1x ratios need no ramp — beatmatch at the
    doubled grid. Returns a unchanged; the caller re-grids.
Returns (ramped_audio, bpm_to). The ramped audio is ramp_bars long in
musical time at the new tempo.


## Axis (Phase 26, software/hardware tranche A)

**Dual-converge (djay Tempo Blend)** — Algoriddim's Crossfader
FX Tempo Blend couples this ramp to the crossfader itself:
"load tracks with different tempos onto each deck, and Tempo
Blend will automatically sync them as you move the crossfader."
Where this base ramps the outgoing track alone over a fixed bar
count, the dual-converge staging re-solves BOTH tracks' tempos
as a function of fader position — A slows as B speeds, meeting
mid-fade — so the tempo trajectory and the level trajectory are
one gesture, and pausing the fader pauses the convergence.
Automix's "Sync + Tempo Blend" is the unattended form. Evidence:
djay Pro help, Crossfader FX / Automix pages, fetched 2026-10-23.
