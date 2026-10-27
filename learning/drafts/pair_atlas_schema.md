# DRAFT: pair_atlas_schema

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: null-set-ai-dj (https://github.com/sanchitd5/null-set-ai-dj)
- License note: MIT
- Summary: Per-pair, per-move compatibility scores as an evidence layer above the selector (from the STAR survey top-5, 2026-10-26).

## Evidence (mechanism confirmed)

null-set-ai-dj `app/music_brain/atlas/pair_atlas.py`, verified
first-hand 2026-10-27: per-pair rows (`pairs_for`) carrying
merge plans, works_score (weights: key 0.30, tempo 0.20,
energy 0.15, vocal 0.15, stems 0.10, move 0.10), gates, and
recipe picks; the atlas is rebuilt incrementally per set
(`agent_bridge.py`). Evidence path:
`null-set-ai-dj/app/music_brain/atlas/pair_atlas.py` (survey:
STAR-REPOS-SURVEY §1 top-5 `pair_atlas_schema`).

## Applicability (selector fields)

- Tempo / key / energy / vocals: the atlas scores all of them
  per pair (weights above). Use for any pair with measured
  features — the atlas row is the evidence layer above the
  selector (pair history, not just song features).
- Sections: rows carry exit / entry points.
- Genre families: source gives no genre applicability.
- Avoid as a standalone verdict: a row scores a pair; it does
  not render.

## Registry fit (META schema)

- Kind: selector (evidence layer, not a render).
- Requires: needs measured pair features (plus stems for
  stem-gated rows). Outputs per-pair, per-move scores.
- Energy / exit / clash risk: N/A — row-level, no audio.
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
