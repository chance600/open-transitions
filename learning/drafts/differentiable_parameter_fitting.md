# DRAFT: differentiable_parameter_fitting

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: djtransgan (https://github.com/ChenPaulYu/DJtransGAN)
- License note: MIT
- Summary: Fit technique parameter defaults from example mixes and freeze them as deterministic defaults — the DJTransGAN method, not its torch stack (from the STAR survey top-5, 2026-10-26).

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

Mined from djtransgan. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
