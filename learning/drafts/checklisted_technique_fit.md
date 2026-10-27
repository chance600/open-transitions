# DRAFT: checklisted_technique_fit

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: null-set-ai-dj (https://github.com/sanchitd5/null-set-ai-dj)
- License note: MIT
- Summary: Each technique expressed as boolean checks returning fit plus per-check reasons measured from a real studied set; transfers as explainable per-technique fit reports (why this move fits / does not).

## Evidence (mechanism confirmed)

null-set-ai-dj `app/music_brain/matching/techniques.py`, verified
first-hand 2026-10-27: `Technique.assess` returns fits plus
per-check reasons; `rank()` returns every technique with fits
and reasons, fitting ones first. Checks read measured
PairFeatures (tempo gap, key score, vocal style, stem maps,
breakdowns); learned techniques carry observations from studied
sets ("seen Nx"). Evidence path:
`null-set-ai-dj/app/music_brain/matching/techniques.py` (survey:
STAR-DEEP-CANDIDATES `checklisted_technique_fit`).

## Applicability (selector fields)

- Tempo / key / energy / sections / vocals: the checks read
  whatever PairFeatures are measured (tempo_gap, key, vocal
  style, stem maps, breakdowns). Use for any pair with measured
  features — the more features measured, the more checks can
  pass or fail informatively. Avoid as a verdict: a failing
  check explains why a move does not fit; it does not itself
  render or repair the pair.
- Genre families: source gives no genre applicability for the
  checklists themselves.
- Avoid when features are unmeasured: checks can only assess
  measured features.

## Registry fit (META schema)

- Kind: selector (per-technique fit reporting, not a render).
- Requires: needs measured pair features. Outputs fits plus
  reasons per technique.
- Energy / exit / clash risk: N/A — it reports fit, no audio.
- Evidence reference: null-set-ai-dj `techniques.py` (MIT).

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
