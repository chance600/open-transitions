# DRAFT: spleeter_multistem_element_trading

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: spleeter (https://github.com/deezer/spleeter)
- License note: MIT
- Summary: 4stems/5stems models (spleeter/resources/4stems.json, 5stems.json): per-element stems for element trading.

## Evidence (mechanism confirmed)

Per-element stem separation, verified first-hand 2026-10-29
against a shallow clone of the registered source
(https://github.com/deezer/spleeter, MIT):
`spleeter/resources/4stems.json` lists instrument_list
["vocals", "drums", "bass", "other"], and
`spleeter/resources/5stems.json` lists ["vocals", "piano",
"drums", "bass", "other"]; README lines 16-17 describe the
same two models as vocals / drums / bass / other separation
(4 stems) and vocals / drums / bass / piano / other
separation (5 stems). The mechanism is exactly the queue
summary's claim: per-element stems usable as the input to
element trading between separated stems. No correction to
the summary was needed. This draft covers the 4- and
5-stem modes only; the 2-stem vocals-vs-accompaniment mode
is the separate draft `spleeter_two_stem_vocal_split`. Note
the 5-stem model adds piano, not guitar — it is not the
Demucs six-source variant.

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap or tempo applicability
  (separation is applied to audio files, not gated on tempo).
- Key/harmonic: source gives no key applicability.
- Energy: source gives no energy applicability.
- Sections: source gives no song-section applicability (the
  models separate whole files; no intro/outro/chorus gating
  is stated).
- Vocals: both models include a dedicated vocals stem, so
  the mechanism supports vocal-element trading alongside
  drums, bass, piano (5-stem only), and other.
- Genre families: source gives no genre applicability.
- Use when: per-element trading between separated stems is
  wanted — e.g. carrying one side's drums under the other
  side's bass, or swapping a single element across the seam
  while the remaining stems stay in place — with the stems
  produced offline before the set/render.
- Avoid when: only a vocals-vs-rest split is required (that
  is the two-stem draft, not this one); a live in-set
  separation is required (the source documents file
  separation via its CLI, no live-deck mode is stated);
  separation artifacts would be audible at the seam (no
  artifact or bleed guarantee is stated in the source's
  model description).

## Registry fit (META schema)

- Kind: stem-prep enabling step for element-trading
  techniques, not itself a render move — a promotion
  assessment should decide whether the META entry is the
  trade that consumes these stems, with this draft as its
  evidence, rather than a standalone technique entry; it
  should also check for duplication against the existing
  stem/vocal family and the Demucs four-stem and Spleeter
  two-stem drafts before any META entry.
- Requires: separated stems (4-stem: vocals, drums, bass,
  other; 5-stem: vocals, piano, drums, bass, other)
  produced before the set/render (offline CLI step); no
  bpm_delta_pct_max, camelot_max, phrase, or genre gating
  stated for the separation itself.
- Energy: delta 0 for the separation step itself (energy
  profile belongs to the trade that consumes the stems, not
  to the split). Exit: n/a for the prep step (the trade's
  exit profile applies). Clash risk: separation quality is
  not modeled in the source's model description (no artifact
  or bleed guarantee is stated).
- Evidence reference: Spleeter `spleeter/resources/4stems.json`
  and `spleeter/resources/5stems.json` (instrument lists)
  and README lines 16-17, source spleeter
  (https://github.com/deezer/spleeter, MIT).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from spleeter. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
