# breakdown_swap

**Bank:** WEB-30 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Mixgraph, "DJ Transition Techniques: 7 Ways to Mix Between Tracks" — the breakdown swap; https://www.mixgraph.io/learn/dj-transition-techniques, fetched first-hand 2026-10-24.

## Signature

```python
breakdown_swap(a, b, sr, bar_s, swap_bars=8, b_drums=None)
```

`breakdown_swap` — family STRUCT, exit seamless, energy delta 0 (flat).

## Spec

B's beat enters under A's drumless breakdown; the handoff completes when the breakdown resolves.

    Mixgraph's breakdown swap: "Track A enters a breakdown — the
    beat drops out, the melody floats — and during that open
    space, Track B's beat enters underneath. When Track A's
    breakdown ends, the DJ has already transitioned to Track B's
    groove."

    Rendered: A's breakdown segment plays for `swap_bars` bars
    while B's drums stem fades in on a smootherstep (0 -> full
    across the window); at the window end B plays full from its
    bar `swap_bars` onward (no repeated drums bars). The drums
    fade is the whole gesture: B's groove is already running
    when A's breakdown resolves, so the crowd barely notices
    the transition — "the most musical transition technique
    because it uses the structure of the music itself."

    Why it is not its neighbours: not T-023
    `breakdown_transition` (two DRUMLESS sections blended with
    mid/high EQs only, no beatmatching constraint — here B
    brings its BEAT into the open space, so the grids must
    agree and the handoff is a drum entry, not a blend); not
    T-001 `eq_blend` (no breakdown window, no drum-entry law);
    not T-022 `drum_bridge` (a bridge built from drums alone
    between two full sections — here the drums arrive inside
    an existing breakdown).

## Parameters

- `swap_bars` (int, 8–16, default 8): open-space window in bars.
  The source's floor is 8: a 4-bar breakdown "doesn't give you
  enough time to establish the incoming track" and sounds
  rushed, not intentional. 16 is the long-breakdown staging.
- `b_drums` (caller-supplied, required): B's drums stem for the
  window — the same class as cue times. The beat entering under
  the breakdown must be drums, not B's full mix; passing None
  raises. Renderers that lack a drums stem cannot stage this
  base (it is not silently degraded to a full-mix entry).

## Selection

Requires: BPM delta ≤ 3%, Camelot distance ≤ 2, vocal pair
a_only / neither, A's phrase = breakdown, genre pair same /
neighbor, A has a breakdown (`a_breakdown` need).
Prefers: Camelot ≤ 1 (+3, both tracks' melodic elements are
audible through the window); energy delta ≤ 1 (+2, matched
energy — the swap rewards preparation, not rescue); B intro
≥ 8 bars (+1, B has a full intro whose beat can establish).

## Demo

`demos/ext_genre.py`: A's 8-bar drumless breakdown sketch with
stemsB's drums fading in across the window; B full from bar 8.
Handoff = breakdown resolution at 8 bars. Sketch caveat: the
breakdown's melodic content is the suite's sketch, not a real
track's breakdown — the demo proves the drum-entry mechanism.

## Variants

`swap_bars` presets 8bar / 16bar → 2 variants (single-axis base).
