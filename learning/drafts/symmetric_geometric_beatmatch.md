# DRAFT: symmetric_geometric_beatmatch

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: auto-dj-ai (https://github.com/caffettino87/auto-dj-ai)
- License note: MIT
- Summary: Both decks meet at the geometric-mean tempo, each bending half the octave-folded BPM difference, with no stretch outside a +/-6% tolerance; transfers as a beatmatch mode with a tolerance parameter and a no-stretch fallback.

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

Mined from auto-dj-ai. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
