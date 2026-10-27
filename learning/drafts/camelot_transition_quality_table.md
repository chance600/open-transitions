# DRAFT: camelot_transition_quality_table

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: djkr8 (https://github.com/schoi80/djkr8)
- License note: MIT
- Summary: Every key pair maps to a 0.0-1.0 quality and type (same key 1.0, +/-1 same letter 0.95, same-hour letter swap 0.9, energy boosts 0.6/0.5, else 0.0 violation); transfers as the selector's harmonic scoring table.

## Evidence (mechanism confirmed)

djkr8 `src/djkr8/camelot.py` `get_transition_quality`, verified
first-hand 2026-10-27. Full table (the draft summary's list is
partial — it omits the 0.8 and 0.4 rows, completed here from the
source): same key 1.0 (SMOOTH); hour distance 1, same letter
0.95 (SMOOTH); same hour, letter swap 0.9 (SMOOTH); hour
distance 1, letter swap 0.8 (SMOOTH); hour distance 2, same
letter 0.6 (ENERGY_BOOST); hour distance 5, 0.5 (ENERGY_BOOST);
hour distance 3, 0.4 (SMOOTH); anything else, including
unparseable keys, 0.0 (VIOLATION). Evidence path:
`djkr8/src/djkr8/camelot.py` (survey: STAR-DEEP-CANDIDATES
`camelot_transition_quality_table`).

## Applicability (selector fields)

- Tempo: source gives no tempo applicability (key-only table).
- Key/harmonic: this IS the harmonic scorer. Use for any pair
  with Camelot keys on both sides. Avoid as a sole gate: a 0.0
  pair is a violation in the table, but the optimizer caps
  violations by percentage (default max_violation_pct 0.10)
  rather than banning them outright — a 0.0 pair is usable only
  inside that budget.
- Energy: the 0.6 / 0.5 rows are energy boosts, not smooth
  moves. Use them when an energy lift is intended. Avoid
  treating a boost row as harmonically smooth (it scores below
  the smooth rows).
- Sections: source gives no section applicability.
- Vocals: source gives no vocal applicability.
- Genre families: source gives no genre applicability.

## Registry fit (META schema)

- Kind: selector (harmonic scoring table, not a render).
- Requires: needs Camelot keys on both sides. No camelot_max
  (the table scores all pairs 0.0–1.0); no BPM, vocal, phrase,
  or genre gating in the table itself.
- Energy: boost rows carry +energy intent. Exit / clash risk:
  N/A (scores, does not render); what it measures is key clash
  risk.
- Evidence reference: djkr8 `camelot.py` (MIT).

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
