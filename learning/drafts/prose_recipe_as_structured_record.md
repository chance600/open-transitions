# DRAFT: prose_recipe_as_structured_record

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: null-set-ai-dj (https://github.com/sanchitd5/null-set-ai-dj)
- License note: MIT
- Summary: Cookbook prose files parsed into TransitionRecipe structs with machine gating fields (requires_stems, max_bpm_delta, camelot_compatible_only); transfers as registry entries that carry executable gates, not just prose.

## Evidence (mechanism confirmed)

null-set-ai-dj `app/music_brain/matching/knowledge_parser.py`,
verified first-hand 2026-10-27: cookbook prose files parsed
into `TransitionRecipe` structs with machine gating fields
(requires_stems, max_bpm_delta, camelot_compatible_only);
`_derive_prerequisites` sets max_bpm_delta 0.06 for some
recipes and camelot_compatible_only True except for a bypass
list; recipes also carry genre tags (`find_by_genre`) and
difficulty. Evidence path:
`null-set-ai-dj/app/music_brain/matching/knowledge_parser.py`
(survey: STAR-DEEP-CANDIDATES `prose_recipe_as_structured_record`).

## Applicability (selector fields)

- Tempo: recipes carry max_bpm_delta (0.06 where derived). Use
  when the pair's BPM gap is within the recipe's max. Avoid
  when the gap exceeds it.
- Key/harmonic: camelot_compatible_only defaults True. Use
  when keys are Camelot-compatible. Avoid for Camelot-bypassing
  recipes only where the bypass list names them.
- Energy / sections / vocals: source gives no applicability
  beyond the three gating fields (recipes carry section and
  genre information in prose, but the machine gates are the
  three fields).
- Genre families: recipes carry genre tags (the parser offers
  find_by_genre). Use when the pair matches the recipe's genre
  tags; note the genre field is prose-derived, not measured.

## Registry fit (META schema)

- Kind: schema (record format, not a render).
- Requires: maps directly onto META requires —
  bpm_delta_pct_max from max_bpm_delta, camelot_max from
  camelot_compatible_only, needs from requires_stems.
- Energy / exit / clash risk: per-recipe, not per-schema.
- Evidence reference: null-set-ai-dj `knowledge_parser.py`
  (MIT).

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
