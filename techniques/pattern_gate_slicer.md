# pattern_gate_slicer

**Bank:** WEB-28 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Roland SP-404MKII Reference v5.5 (official) — Slicer MFX page; duty-form corroboration from the Pioneer DJM-V10 manual via the manua.ls mirror (Beat FX TRANS; the official Pioneer PDF is login-walled). Fetched 2026-10-23.

## Signature

```python
pattern_gate_slicer(a, b, sr, bpm, bar_s, pattern='offbeat', step_beats=0.25, depth=1.0, shuffle=0.0, mode='slash', gate_bars=4, fade_beats=2)
```

`pattern_gate_slicer` — family PERF, exit snap, energy delta 0 (build).

## Spec

A preset 16-step gate pattern imposed on the live track.

    The SP-404MKII's Slicer "slices the sound up into small pieces
    ... slices up the sound at certain intervals into 16 parts
    (16 steps) ... a rhythm that follows the sequence pattern":
    PATTERN selects a 16-step level table, SPEED the step grid
    (syncable 2/1..1/64T), DEPTH the gate depth, SHUFFLE delays
    the even-numbered steps (swing), and MODE is LEGATO (level
    holds across steps) or SLASH ("volume is reset to zero before
    the next step sounds"). The audio is NOT reordered and NOT
    resampled — a pattern of gain is imposed in place. Pioneer's
    DJM-V10 TRANS is the same family's duty form ("cuts the sound
    cyclically according to the beat", LEVEL/DEPTH setting
    balance AND duty): a pattern whose open steps form one
    contiguous block per cycle.

    Rendered as a transition: A's final `gate_bars` run under the
    pattern (step grid locked to A's tempo); the pattern's last
    cycle completes and B enters, faded over `fade_beats`.

    Why it is not its neighbours: not `beatslicer_shuffle` WEB-08
    (slices are REARRANGED there — here nothing moves, only gain
    is patterned); not GAP-15 `rhythmic_fader_chops` (a performer's
    free-timed chops on an exiting A under B's entry — here a
    looping preset pattern with swing, on A alone, before B);
    not PERF-ZAB `transform_gate_loop` (the gate chops a HELD
    LOOP with doubling subdivisions — here the live track flows
    through a fixed 16-step table); not DM-A44
    `vocal_tremolo_gate` (a smooth LFO tremolo scoped to the
    vocal stem — this is a hard-edged step table on the full mix).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    pattern : step-table name (default "offbeat").
    step_beats : step grid in beats (default 0.25 = 16ths; a
        16-step cycle is then exactly one bar).
    depth : gate depth 0..1 (default 1.0).
    shuffle : even-step delay as a fraction of the step
        (default 0.0; the hardware's SHUFFLE).
    mode : "slash" (2 ms zero notch at each step boundary) or
        "legato" (levels hold; 3 ms edge ramps only).
    gate_bars : gated window at A's end (default 4).
    fade_beats : B's entrance fade in beats (default 2).

    Returns a mono float64 mix of length len(a) + len(b).
