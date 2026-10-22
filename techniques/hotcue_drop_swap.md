# hotcue_drop_swap

**Bank:** T-014 · **Automatability:** ADOPT · **Confidence:** high

**Source:** Virtual Clubbing Life (4-beats-before-the-drop)

## Signature

```python
hotcue_drop_swap(a, b, sr, bpm, xfade_beats=4)
```

## Spec

Replace A's drop with B's: volume cross-swap over the run-up.

a: outgoing, ends at its drop point (the last xfade_beats are the
    "1-2-3-DROP" run-up).
b: incoming, STARTS at its own run-up (hot cue = drop - 4 beats;
    caller aligns).
Equal-power swap over xfade_beats; optional echo/filter layered by
the caller for style.

## Axis (Phase 23, genre traditions tranche A)

**Dual-build staging** — Pioneer DJ's official form of the drop
swap (DDJ-400 technique tutorials, DJ Ravine, 2019; fetched
2026-10-22), named there "a staple of trap and dubstep music":
play the build-ups of BOTH songs simultaneously, then swap
quickly before the drop. Where this base's default enters B at
its run-up and cross-swaps over xfade_beats, the dual-build form
layers the two builds for their full length (one lows-killed)
and makes the swap effectively instant at the drop boundary —
the crowd hears two builds and one drop, and the drop is the
other track's. It is the performed fake-out: the build you hear
is not the drop you get.
