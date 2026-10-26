# wera_weave

**Bank:** KEEP-04 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** Lane keeper — Tuk Tuk -> Tunapewa wera_weave v3c, heart PASS (verdict-dataset row 93, 2026-10-21). Promoted to a registry entry in Phase 30; previously a gap-flagged custom-shape recommendation in engine/fit_select.py.

## Signature

```python
wera_weave(a_stems, b_stems, sr, bar_s, weave_bars=8, chant_bars=2,
           intro_bars=4, exit_bars=1, recognition_bars=2)
```

## Spec

Intro: A plays full for `intro_bars`. Weave: A's vocal stem leads over B's groove (drums + bass + melody) for `weave_bars` — A's other stems are out, B's vocal is withheld. Exit: A's vocal fades to zero over `exit_bars` while B's groove continues. Recognition: B's groove alone for `recognition_bars` — the listener recognizes B before its vocal arrives (D10). Chant: B full, vocal included, for `chant_bars`. A-vocal and B-vocal never coexist: the slices are disjoint in the output timeline by construction.

The keeper's weave was tempo-matched by a diagnosis-led repair (true-rate phase-vocoder stretch, single kick-pairing fit); tempo matching is caller context here, not part of the move. What transfers is the choreography: lead vocal, staged exit, recognition span, chant last.

Why it is not its neighbours: `acapella_overlay` (T-010) overlays a vocal over a backing with EQ and fader riding; the weave is a staged choreography with a vocal exit, a recognition span, and a chant-last close — and a zero-coexistence guarantee the overlay does not make. `accidental_duet` (GAP-12) IS two vocals; the weave is the opposite discipline (never two vocals).

## Selection

Requires stems and a vocal A (vocal_ok a_only/both). Tempo cap 5% (zone fitting is tempo work); Camelot cap 3, the top of the workable band (keeper distance 3). Prefers an A motif and groove B entries. Evidence is THIN (n=1 keeper pair). Overlap caveat, kept from the selector report: wera_weave and ooh_tail_pickup both key on "A hook vocal" — disambiguation needs motif-role detail (lead line vs tail fragment); the evidence layer now keys ooh_tail_pickup on a "tail" vocal_detail and wera_weave on a "hook" vocal_detail where the profile states one, and both rank (with flags) where it does not.
