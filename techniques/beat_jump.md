# beat_jump

**Bank:** T-028 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT); Coach Hapa 4-step; planning primitive — pure playhead arithmetic

## Signature

```python
beat_jump(b_full, sr, bpm, cue_t, jump_beats=32)
```

## Spec

Teleport b's playhead by an exact bar multiple so drops align.

b_full: the incoming track audio (longer than needed).
cue_t: current cue position in seconds.
jump_beats: signed beat count; +32 jumps forward 8 bars, -32 jumps
    back 8 bars (extends a short intro). MUST be a multiple of 32
    beats (8 bars) or phrasing breaks — a warning is printed otherwise.

Returns (jumped_segment_start_sample, applied_beats). The caller cuts
b from the returned sample; the jump itself is pure playhead
arithmetic — the engine's phrase grid makes it trivial, which is the
point: pre-compute the offset instead of hoping intros match.


## Axis (Phase 26, software/hardware tranche A)

**Stored-marker jump (SP-404MKII DJ mode)** — the jump targets
are up to SEVEN stored, NON-UNIFORM markers, fired instantly
mid-playback: where this base jumps a fixed beat count, the
marker form jumps a memorised *form* — intro marker to chorus
marker in one press, distances arbitrary and per-track.
Evidence: SP-404MKII Reference v5.5, DJ Mode pages, fetched
2026-10-23.

## Axes (Phase 32, Class 5 tranche B)

**Scripted jump sizing (VDJScript beatjump_select)** — the
jump size is itself a scripted parameter: `beatjump_select`
sets it absolutely, steps it relatively (+1 to the next higher
size), or scales it (50% halves, 200% doubles), and `beatjump`
then jumps by that size — but only with relative values, so a
scripted size must pass through `param_cast 'relative'` first
(an absolute value is silently wrong, not an error). The
staging for this base's fixed-count jump: size selection and
jump execution as two verbs, with the cast between them — a
jump whose size a knob or a script chose, not a constant.
Evidence: VirtualDJ official VDJScript verb list
(virtualdj.com/wiki/VDJscript_verbs.html) + Script School
forum threads, fetched 2026-10-26.
