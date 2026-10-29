# DRAFT: demucs_two_stem_vocal_isolation

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: demucs (https://github.com/adefossez/demucs)
- License note: MIT
- Summary: Two-stem vocal isolation via --two-stems=vocals (README): vocals vs rest of accompaniment, for vocal-isolation swaps.

## Evidence (mechanism confirmed)

Demucs `--two-stems=vocals`, verified first-hand 2026-10-29
against a shallow clone of the registered source
(https://github.com/adefossez/demucs, MIT): README line 212,
"If you only want to separate vocals out of an audio, use
`--two-stems=vocals`", with the example command at line 213,
and line 254, "The `--two-stems=vocals` option allows
separating vocals from the rest of the accompaniment (i.e.,
karaoke mode)." The mechanism is exactly the queue summary's
claim: a two-stem split, vocals vs everything else, usable as
the input to a vocal-isolation swap. No correction to the
summary was needed. This draft covers the two-stem mode only;
the four-stem drums/bass/other/vocals split is the separate
queued candidate `demucs_four_stem_element_trading`.

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap or tempo applicability
  (separation is applied to audio files, not gated on tempo).
- Key/harmonic: source gives no key applicability.
- Energy: source gives no energy applicability.
- Sections: source gives no song-section applicability (the
  option separates whole files; no intro/outro/chorus gating
  is stated).
- Vocals: the mechanism IS vocal: it applies only where a
  distinct vocal stem is wanted, separated from the rest of
  the accompaniment.
- Genre families: source gives no genre applicability.
- Use when: a vocal-only stem vs accompaniment split is
  wanted as the input to a vocal-isolation swap — i.e. the
  outgoing side's vocal is to be carried, dropped, or traded
  independently of its accompaniment.
- Avoid when: per-element trading beyond vocals-vs-rest is
  required (drums, bass, or other stems separately — that is
  the four-stem candidate, not this one); the source file has
  no separable vocal content (nothing vocal to isolate); a
  live in-set separation is required (the source documents
  file separation via its CLI, no live-deck mode is stated).

## Registry fit (META schema)

- Kind: stem-prep enabling step for a vocal-isolation swap
  technique, not itself a render move — a promotion
  assessment should decide whether the META entry is the swap
  that consumes these stems, with this draft as its evidence,
  rather than a standalone technique entry; it should also
  check for duplication against the existing stem/vocal
  family before any META entry.
- Requires: a separated vocals stem and an accompaniment
  stem produced before the set/render (offline CLI step);
  no bpm_delta_pct_max, camelot_max, phrase, or genre gating
  stated for the separation itself.
- Energy: delta 0 for the separation step itself (energy
  profile belongs to the swap that consumes the stems, not
  to the split). Exit: n/a for the prep step (the swap's
  exit profile applies). Clash risk: separation quality is
  not modeled in the source's option description (no
  artifact or bleed guarantee is stated).
- Evidence reference: Demucs README, `--two-stems=vocals`
  section (lines 212-213, 254), source demucs
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
