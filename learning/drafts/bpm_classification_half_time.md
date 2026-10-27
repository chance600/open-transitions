# DRAFT: bpm_classification_half_time

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: null-set-ai-dj (https://github.com/sanchitd5/null-set-ai-dj)
- License note: MIT
- Summary: BPM gaps classified seamless (<=3%), ramp (<=6%), half_time (half/double fold within 6%), else cut_required; transfers as a tempo-gap classifier feeding technique eligibility.

## Evidence (mechanism confirmed)

null-set-ai-dj `app/music_brain/matching/recipe_matcher.py`,
verified first-hand 2026-10-27: BPM-gap classification returning
a score and a label — seamless at pct_diff <= 0.03 (1.0), ramp at
<= 0.06 (0.75), half_time at folded gap <= 0.06 (0.75 if <= 0.03
else 0.6), else cut_required (0.2). Evidence path:
`null-set-ai-dj/app/music_brain/matching/recipe_matcher.py`
(survey: STAR-DEEP-CANDIDATES `bpm_classification_half_time`).

## Applicability (selector fields)

- Tempo: this IS the tempo classifier. Use for any pair with
  measured BPMs on both sides — it returns a class for every
  pair, including cut_required. Avoid as a sole selector: it
  only classifies the gap; it does not pick a technique (its
  scores feed recipe matching).
- Key/harmonic: source gives no key applicability (the
  classifier reads BPM only).
- Energy: source gives no energy applicability.
- Sections: source gives no section applicability.
- Vocals: source gives no vocal applicability.
- Genre families: source gives no genre applicability.

## Registry fit (META schema)

- Kind: selector (tempo-gap classifier, not a render).
- Requires: needs measured BPM on both sides. No
  bpm_delta_pct_max (it classifies all gaps, including
  cut_required); no camelot_max, vocal, phrase, or genre
  gating in the classifier itself.
- Energy / exit / clash risk: N/A — it outputs a class and a
  score, no audio.
- Evidence reference: null-set-ai-dj `recipe_matcher.py` (MIT).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from null-set-ai-dj. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
