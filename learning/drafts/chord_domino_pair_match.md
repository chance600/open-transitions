# DRAFT: chord_domino_pair_match

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: endeless (https://github.com/Aurbcd/Endeless)
- License note: MIT
- Summary: Next song eligible only if its first chord exactly equals the previous song's last chord, chosen among matches without repeating a song; transfers as a hard pair-eligibility rule on boundary chords.

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

Mined from endeless. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
