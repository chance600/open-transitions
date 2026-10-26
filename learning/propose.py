"""Spec -> demo -> verify loop, first half: propose a spec draft.

A draft is NOT a registry entry. It is a markdown file in a drafts
directory that a human reviews before anything is implemented, demoed,
or merged. The draft template mirrors the technique-bank anatomy
(name, family, parameters, when/avoid, provenance) so a draft can be
checked against the same shape as a shipped technique.

Deliberately absent: auto-implementation, auto-demo, auto-merge.
Those steps run only after a human approves the draft.
"""

from __future__ import annotations

from pathlib import Path

from learning.ingest import Candidate

DRAFT_TEMPLATE = """# DRAFT: {name}

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: {source_name} ({source_url})
- License note: {license_note}
- Summary: {summary}

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

Mined from {source_name}. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
"""


def draft_path(drafts_dir: str | Path, name: str) -> Path:
    slug = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name)
    return Path(drafts_dir) / f"{slug}.md"


def propose_draft(candidate: Candidate, drafts_dir: str | Path, overwrite: bool = False) -> Path:
    """Write a spec draft for a candidate. Refuses to clobber by default."""
    path = draft_path(drafts_dir, candidate.name)
    if path.exists() and not overwrite:
        raise FileExistsError(
            f"draft already exists: {path} (pass overwrite=True to replace it)"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        DRAFT_TEMPLATE.format(
            name=candidate.name,
            source_name=candidate.source_name,
            source_url=candidate.source_url,
            license_note=candidate.license_note or "(none recorded)",
            summary=candidate.summary,
        )
    )
    return path
