# DRAFT: note_anchored_crossfade

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: endeless (https://github.com/Aurbcd/Endeless)
- License note: MIT
- Summary: Fade-out starts exactly at the outgoing song's last-note time and fade-in ends exactly at the incoming song's first-note time, overlap capped at 5 s; transfers as anchoring fades to detected musical events rather than fixed offsets.

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

## Applicability (evidence-grounded, added 2026-10-27 under DRAFT-QUALITY.md)

- Evidence path (confirmed first-hand): `Endeless/Endeless/workers/endeless_worker.py`,
  lines 53–55 — crossfade comment "guaranty a 5 seconds fade maximum";
  fade-out runs from the outgoing song's `Last_Note_Time`, capped at
  +5000 ms; fade-in ends at the incoming song's `First_Note_Time`,
  starting at most 5000 ms earlier. Survey entry (STAR-DEEP-CANDIDATES
  line 15) matches this code.
- Use when: per-song first/last-note times are known — dataset with
  manual entry or chord-recognition fill, per the survey's endeless
  description. Fits any tempo/key/genre where boundary notes are
  detectable; the mechanism is note-time driven, not tempo driven.
  Best where the seam should land on a musical event rather than a
  fixed offset, and where a short (≤5 s) overlap is acceptable.
- Avoid when: boundary note times are unknown, unreliable, or
  manually unentered; songs with legato/ambiguous boundaries where
  a "first/last note" does not mark a clean seam; any blend needing
  an overlap longer than 5 s (the cap is structural in the source).
- Melody note: in the full endeless system this fade pairs with
  first-note/last-note domino chaining (next first note equals
  previous last note); this draft is the fade mechanism alone and
  does not require the chaining rule.

## Registry fit (META mapping)

- Preconditions: outgoing `Last_Note_Time` present; incoming
  `First_Note_Time` present; both durations known.
- Energy/exit profile: short, seam-tight event-anchored fade;
  maximum 5 s overlap; exit lands exactly on the outgoing last note.
- Evidence reference: endeless worker lines 53–55 (see above).
