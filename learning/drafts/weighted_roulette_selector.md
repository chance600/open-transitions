# DRAFT: weighted_roulette_selector

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: rustlarpdj (https://github.com/T-Perm/RustLarpDJ)
- License note: license unconfirmed - learn-from only, no code reuse
- Summary: Per-style scores sampled by roulette, not argmaxed, with score floors, a 0.4x repeat-style penalty and a 1.5x style-hint boost; transfers as a selector that preserves variety across a set instead of always picking the top score.

## Evidence (mechanism confirmed)

RustLarpDJ `crates/ai/src/transition_style.rs`
`choose_transition`, verified first-hand 2026-10-27: score
floors 0.03 (DoubleDrop) / 0.05 (all other styles);
REPEAT_STYLE_PENALTY 0.4; STYLE_HINT_BOOST 1.5; true roulette
sampling (r = random * total, position walk through scores —
not argmax); a reason string (stretch %, key match %,
energy delta %, confidence %). Evidence path:
`RustLarpDJ/crates/ai/src/transition_style.rs` (survey:
STAR-DEEP-CANDIDATES `weighted_roulette_selector`).

## Applicability (selector fields)

- Tempo / key / energy: scores read stretch, key match,
  energy delta, and confidence (per the reason string). Use
  when variety across a set matters more than always picking
  the top score — roulette preserves variety. Avoid when
  determinism is required: roulette is random by construction,
  so identical inputs can yield different picks.
- Sections / vocals: source gives no applicability for the
  sampling policy itself.
- Genre families: source gives no genre applicability (the
  genre field is present but unset — `genre: None` — in the
  scoring path).

## Registry fit (META schema)

- Kind: selector (sampling policy, not a render).
- Requires: needs scored candidates plus floors. Outputs a
  sampled pick plus a reason string.
- Energy / exit / clash risk: per picked style, not per
  policy.
- Evidence reference: RustLarpDJ `transition_style.rs`
  (learn-only, license unconfirmed).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from rustlarpdj. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
