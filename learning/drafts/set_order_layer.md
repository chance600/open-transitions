# DRAFT: set_order_layer

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: djkr8 (https://github.com/schoi80/djkr8)
- License note: MIT
- Summary: Longest-path set ordering under Camelot-key and energy-flow constraints, run before transition selection (from the STAR survey top-5, 2026-10-26).

## Evidence (mechanism confirmed)

djkr8 `src/djkr8/optimizer.py` + `cli.py`, verified first-hand
2026-10-27: CP-SAT ordering model; energy flow non-decreasing
with max +1 per transition (enforceable, with an
allow-energy-drops flag); max_energy_boosts 3 per set;
max_violation_pct 0.10 default; Camelot quality table scores
edges. Evidence path: `djkr8/src/djkr8/optimizer.py` (survey:
STAR-REPOS-SURVEY §5 top-5 `set_order_layer`).

## Applicability (selector fields)

- Tempo: BPM tolerance with halftime/doubletime equivalence
  (survey §5; the optimizer reads track BPM). Use when ordering
  a set whose tracks carry BPM plus Camelot plus energy 1–5.
  Avoid as a transition picker: it solves ordering, not
  transitions (survey verdict — it complements rather than
  competes with transition selection).
- Key/harmonic: Camelot quality scores edges (0.0 = violation,
  capped by the violation percentage).
- Energy: flow non-decreasing, max +1 per step, max 3 boosts
  per set. Use when a rising or flat energy arc is wanted.
  Avoid when the set needs an energy drop — flow enforcement
  forbids it unless allow-energy-drops is set.
- Sections / vocals / genre: source gives no applicability.

## Registry fit (META schema)

- Kind: selector (set-order layer, runs BEFORE transition
  selection; order and technique are chosen jointly, not in
  isolation).
- Requires: needs BPM + Camelot + energy per track. Outputs an
  ordering.
- Energy / exit / clash risk: N/A — ordering-level, no audio.
- Evidence reference: djkr8 `optimizer.py` (MIT).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from djkr8. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
