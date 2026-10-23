# filter_sweep

**Bank:** T-003 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT), MusicRadar

## Signature

```python
filter_sweep(a, b, sr, bar_s, tease_bars=8, sweep_bars=7)
```

## Spec

A thins out under HPF while B opens up; snap B open on the downbeat.

a: outgoing (tease_bars + sweep_bars + 1 bars). b: incoming, same length,
pre-filtered to thin top-end during the tease (caller may pass full b;
the tease HPF is applied here).
Returns mix of length (tease+sweep+1) bars; B fully open at the drop bar.


## Axes (Phase 26, software/hardware tranche A)

**Dual-VCF counter-sweep (Xone:96)** — the 96 carries TWO
independent stereo state-variable VCFs, one each side of the
crossfader, with channels assignable per side (FILTER 1 / FILTER
2 / direct to LR MIX) and independent type, FREQ and RES per
side. The staging this base's single-filter render does not
express: A swept HPF-up on VCF 1 while B is swept LPF-down on
VCF 2 — two filters counter-moving through the blend, meeting in
a mid band neither track owns. Soft-switching makes type and
assignment changes click-free mid-performance, licensing
downbeat type-switches inside the sweep. Evidence: Xone:96 User
Guide (official support HTML), fetched 2026-10-23.

**CRUNCH pre-filter drive (Xone:96)** — each VCF has a CRUNCH
control (0–10): "harmonic distortion... derived from the signal
just before it enters the filter," optimum drive ±6 dB. The
staging: saturate *analogue-style* (harmonics ADDED) immediately
before the carve, so the filter has new partials to bite on —
the opposite sign of `crush_degrade` WEB-04, whose quantisation
*removes* information. Drive is staged pre-filter here, never as
a post effect.

**WILD resonance staging (Xone:96)** — RES runs MILD to WILD,
WILD "just short of self-oscillation": parking this base's sweep
at the top of its resonance range turns the cutoff into a
whistling oscillator edge the sweep can lean on. The guide gives
no numeric Q; the registry's Q values remain implementation
choices (stated in WEB-23's spec as the same convention).

**Global scope + LFO cycle (DJM-V10)** — the V10's FILTER
section applies ONE resonant LPF/HPF "to all channels, [1] to
[6]": the sweep staged on the summed mix rather than a deck —
this base fired on the whole programme at a set climax. Its
Beat FX FILTER adds the cyclic form: cutoff modulated on a
1/16–64-beat cycle (10–32000 ms) — the sweep as LFO, not gesture.
Evidence: DJM-V10 manual via manua.ls, pp42–43 + p63, fetched
2026-10-23.

**SP-404MKII filter stagings** — Super Filter: the same sweep
automated cyclically with "an extremely sharp slope" (CUTOFF
0–100 unmapped to Hz in the manual — a recorded gap). Wah: the
cyclic form on a resonant band emphasis (LPF wide / BPF narrow).
Filter+Drive: the parameter ground truth for the swept form —
CUTOFF 20–16000 Hz, RES 0–100, DRIVE 0–100, plus a low shelf
±24 dB. Evidence: SP-404MKII Reference v5.5, filter MFX pages,
fetched 2026-10-23.
