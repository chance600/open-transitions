# build_to_drop

**Bank:** T-009 · **Automatability:** ADAPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT); build-boundary detection is the caller's job (ADAPT caveat)

## Signature

```python
build_to_drop(a_build, b_build, sr, bar_s, build_bars=16, wash_start_bar=9, pre_drop_cut_beats=1.0)
```

## Spec

Layer two build-ups, fuse them, drop the incoming track.

a_build / b_build: build sections, each build_bars long. b_build should
EXTEND past the build into its drop (caller supplies build+drop).
Build detection (where each build starts, 8 vs 16 bars) is the caller's
job — the ADAPT caveat in T-009.

Bars 1-8: b's build at 100% fader but low EQ killed — blends into a.
wash_start_bar..build_bars: HPF washes a into the background.
Last pre_drop_cut_beats: a cut to 0 (step).
Bar build_bars+1 beat 1: b's drop at full.
