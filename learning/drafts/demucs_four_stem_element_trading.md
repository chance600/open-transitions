# DRAFT: demucs_four_stem_element_trading

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: demucs (https://github.com/adefossez/demucs)
- License note: MIT
- Summary: Four-stem separation (drums/bass/other/vocals, Hybrid Transformer Demucs v4) for element trading between separated stems.

## Evidence (mechanism confirmed)

Four-stem separation, verified first-hand 2026-10-29
against a shallow clone of the registered source
(https://github.com/adefossez/demucs, MIT): README line 12,
"This is the 4th release of Demucs (v4), featuring Hybrid
Transformer based source separation"; line 21, "The v4
version features [Hybrid Transformer Demucs][htdemucs]";
line 241, "`htdemucs`: first version of Hybrid Transformer
Demucs. ... Default model."; and lines 221-222, "Separated
tracks are stored in the `separated/MODEL_NAME/TRACK_NAME`
folder. There you will find four stereo wav files sampled at
44.1 kHz: `drums.wav`, `bass.wav`, `other.wav`, `vocals.wav`."
The mechanism is exactly the queue summary's claim: a
four-stem drums/bass/other/vocals split from the default
Hybrid Transformer Demucs v4 model, usable as the input to
element trading between separated stems. No correction to
the summary was needed. This draft covers the four-stem
mode only; the two-stem vocals-vs-rest mode is the separate
draft `demucs_two_stem_vocal_isolation`. Note the
six-source variant (`htdemucs_6s`, adding piano and guitar)
is a different model and is NOT covered by this draft.

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap or tempo applicability
  (separation is applied to audio files, not gated on tempo).
- Key/harmonic: source gives no key applicability.
- Energy: source gives no energy applicability.
- Sections: source gives no song-section applicability (the
  option separates whole files; no intro/outro/chorus gating
  is stated).
- Vocals: the four stems include a dedicated vocals stem,
  so the mechanism supports vocal-isolation swaps as one
  element-trading case, alongside drums, bass, and other.
- Genre families: source gives no genre applicability.
- Use when: per-element trading between separated stems is
  wanted — e.g. carrying one side's drums under the other
  side's bass, or swapping a single element across the seam
  while the remaining stems stay in place — with the stems
  produced offline before the set/render.
- Avoid when: only a vocals-vs-rest split is required (that
  is the two-stem candidate, not this one); a live in-set
  separation is required (the source documents file
  separation via its CLI, no live-deck mode is stated);
  separation artifacts would be audible at the seam (the
  source notes output may need clipping handling and that
  rescaling can break relative stem volume, lines 233-235 —
  no artifact or bleed guarantee is stated).

## Registry fit (META schema)

- Kind: stem-prep enabling step for element-trading
  techniques, not itself a render move — a promotion
  assessment should decide whether the META entry is the
  trade that consumes these stems, with this draft as its
  evidence, rather than a standalone technique entry; it
  should also check for duplication against the existing
  stem/vocal family and the two-stem draft before any META
  entry.
- Requires: four separated stems (drums, bass, other,
  vocals) produced before the set/render (offline CLI step);
  no bpm_delta_pct_max, camelot_max, phrase, or genre gating
  stated for the separation itself.
- Energy: delta 0 for the separation step itself (energy
  profile belongs to the trade that consumes the stems, not
  to the split). Exit: n/a for the prep step (the trade's
  exit profile applies). Clash risk: separation quality is
  not modeled in the source's option description (no
  artifact or bleed guarantee is stated).
- Evidence reference: Demucs README, v4 / Hybrid Transformer
  description (lines 12, 21, 241) and separated-output
  description (lines 221-222), source demucs
  (https://github.com/adefossez/demucs, MIT).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from demucs. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
