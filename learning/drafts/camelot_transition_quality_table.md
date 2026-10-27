# DRAFT: camelot_transition_quality_table

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: djkr8 (https://github.com/schoi80/djkr8)
- License note: MIT
- Summary: Every key pair maps to a 0.0-1.0 quality and type (same key 1.0, +/-1 same letter 0.95, same-hour letter swap 0.9, energy boosts 0.6/0.5, else 0.0 violation); transfers as the selector's harmonic scoring table.

## Parameters (to be specified by the implementer)

- (fill in: named parameters with defaults and ranges)

## When to use / when to avoid (to be specified)

- Use when: (fill in, grounded in evidence, not invented)
- Avoid when: (fill in)

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
