# DRAFT: merge_hold_handover

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: null-set-ai-dj (https://github.com/sanchitd5/null-set-ai-dj)
- License note: MIT
- Summary: Named compound base: merge, hold, hand over, with hold length from measured stem energy and vocal gaps (from the STAR survey top-5, 2026-10-26).

## Evidence (mechanism confirmed)

null-set-ai-dj `app/music_brain/atlas/pair_atlas.py` and
`macros.py`, verified first-hand 2026-10-27: merge -> hold
planning with hold_bars / hold_phrases; holdPlan computed on
per-bar stem RMS; macros carry the merge plan on 8-bar lines;
pair feasibility gates on vocal entry, vocal phrase length,
and keys clashing under a sung vocal. Evidence path:
`null-set-ai-dj/app/music_brain/atlas/pair_atlas.py` (survey:
STAR-REPOS-SURVEY §1 top-5 `merge_hold_handover`).

Correction to the draft summary, from the source: hold length
derives from measured stem energy (per-bar stem RMS); vocal
presence gates feasibility (vocal entry, phrase length,
keys-clash-under-sung-vocal refusal) — vocal gaps are NOT the
length source. The compound itself (merge -> hold -> handover)
is confirmed.

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap for the compound itself
  (pair feasibility scores tempo separately).
- Key/harmonic: gated — a merge is refused when keys clash
  under a sung vocal.
- Energy: pair works_score weighs energy (0.15 of the score).
  Use when the pair's energy flow is acceptable to the works
  score. Avoid when the merge gates refuse (no B vocal entry,
  vocal phrase too short, keys clash under sung vocal).
- Sections: holds run on 8-bar lines (hold_phrases). Use when
  the overlap affords whole-phrase holds. Avoid when the
  available overlap is shorter than a phrase hold.
- Vocals: requires a usable B vocal entry and room in A. Avoid
  when B's vocal phrase is too short or there is no room left
  in A.
- Genre families: source gives no genre applicability.

## Registry fit (META schema)

- Kind: render (compound base: merge + hold + handover).
- Requires: needs stems (stem-RMS holdPlan), a B vocal entry,
  and phrase-length overlap; vocal_ok: gated (refuses
  keys-clash-under-sung-vocal); phrase_a_ok: phrase-structured
  exits.
- Energy: delta per the pair works score. Exit: seamless.
  Clash risk: vocal + bass (one track owns the sub-bass at
  handover, per the survey).
- Evidence reference: null-set-ai-dj `pair_atlas.py` (MIT).

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
