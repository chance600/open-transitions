# DRAFT: spleeter_two_stem_vocal_split

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: spleeter (https://github.com/deezer/spleeter)
- License note: MIT
- Summary: 2stems model (spleeter/resources/2stems.json): vocals vs accompaniment split for vocal/accompaniment swaps.

## Evidence (mechanism confirmed)

Spleeter 2stems model, verified first-hand 2026-10-29
against a shallow clone of the registered source
(https://github.com/deezer/spleeter, MIT):
`spleeter/resources/2stems.json` lists exactly two instruments,
vocals and accompaniment; README line 15 describes vocals
(singing voice) / accompaniment separation (2 stems), line 60
gives the command `spleeter separate -p spleeter:2stems`,
and line 67 states the output is two separated files,
vocals and accompaniment. The mechanism is exactly the queue
summary's claim: a two-stem split, vocals vs accompaniment,
usable as the input to a vocal/accompaniment swap. No
correction to the summary was needed. This draft covers the
two-stem mode only; the four/five-stem per-element splits are
the separate queued candidate
`spleeter_multistem_element_trading`.

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap or tempo applicability
  (separation is applied to audio files, not gated on tempo).
- Key/harmonic: source gives no key applicability.
- Energy: source gives no energy applicability.
- Sections: source gives no song-section applicability (the
  model separates whole files; no intro/outro/chorus gating
  is stated).
- Vocals: the mechanism IS vocal: it applies only where a
  distinct vocal stem is wanted, separated from accompaniment.
- Genre families: source gives no genre applicability.
- Use when: a vocal-only stem vs accompaniment split is
  wanted as the input to a vocal/accompaniment swap — i.e. the
  outgoing side's vocal is to be carried, dropped, or traded
  independently of its accompaniment.
- Avoid when: per-element trading beyond vocals-vs-rest is
  required (drums, bass, piano, or other stems separately —
  that is the multistem candidate, not this one); the source
  file has no separable vocal content (nothing vocal to
  isolate); a live in-set separation is required (the source
  documents file separation via its CLI, no live-deck mode
  is stated).

## Registry fit (META schema)

- Kind: stem-prep enabling step for a vocal/accompaniment
  swap technique, not itself a render move — a promotion
  assessment should decide whether the META entry is the swap
  that consumes these stems, with this draft as its evidence,
  rather than a standalone technique entry; it should also
  check for duplication against the existing stem/vocal
  family (including the Demucs two-stem draft) before any
  META entry.
- Requires: separated vocals and accompaniment stems produced
  before the set/render (offline CLI step); no
  bpm_delta_pct_max, camelot_max, phrase, or genre gating
  stated for the separation itself.
- Energy: delta 0 for the separation step itself (energy
  profile belongs to the swap that consumes the stems, not
  to the split). Exit: n/a for the prep step (the swap's
  exit profile applies). Clash risk: separation quality is
  not modeled in the source's model description (no artifact
  or bleed guarantee is stated).
- Evidence reference: Spleeter `spleeter/resources/2stems.json`
  (vocals/accompaniment instrument list) and README lines
  15, 60, 67, source spleeter
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
