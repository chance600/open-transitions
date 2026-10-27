# DRAFT: note_anchored_crossfade

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: endeless (https://github.com/Aurbcd/Endeless)
- License note: MIT
- Summary: Fade-out starts exactly at the outgoing song's last-note time and fade-in ends exactly at the incoming song's first-note time, overlap capped at 5 s; transfers as anchoring fades to detected musical events rather than fixed offsets.

## Evidence (mechanism confirmed)

Endeless `Endeless/workers/endeless_worker.py`
`add_with_transition`, verified first-hand 2026-10-27: the
outgoing fade starts at the last-note position (start =
track_end - Duration + Last_Note_Time) and the incoming fade
ends exactly at First_Note_Time; the code comment states the
cap ("guaranty a 5 seconds fade maximum"). Note: the 5 s cap
applies per fade. Evidence path:
`Endeless/Endeless/workers/endeless_worker.py` (survey:
STAR-DEEP-CANDIDATES `note_anchored_crossfade`).

## Applicability (selector fields)

- Tempo: source gives no tempo applicability (fades are
  time-anchored in milliseconds, not beat-anchored — the worker
  uses no beat grid).
- Key/harmonic: source gives no key applicability for the fade
  itself (note equality is the sibling chaining rule, not this
  fade).
- Energy: source gives no energy applicability.
- Sections: source gives no section applicability.
- Vocals: source gives no vocal applicability.
- Genre families: source gives no genre applicability.
- Use when first/last note times are known for both sides.
- Note times come from the source's per-song dataset (manual entry or chord-recognition fill, per the survey's endeless description). In the full endeless system this fade pairs with first-note/last-note domino chaining; this draft is the fade mechanism alone and does not require the chaining rule.
  Avoid when note times are unknown (the anchors do not exist)
  or when either fade would need more than 5 s (the cap
  truncates it).

## Registry fit (META schema)

- Kind: render (anchored fade).
- Requires: needs first/last note times on both sides. No
  bpm_delta_pct_max, camelot_max, vocal, phrase, or genre
  gating stated for the fade itself.
- Energy: delta 0, tension flat. Exit: seamless. Clash risk:
  none stated (time-anchored; no clash logic in the worker).
- Evidence reference: Endeless `endeless_worker.py` (MIT).

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
