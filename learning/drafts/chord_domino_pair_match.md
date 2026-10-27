> **UNCONFIRMED — mechanism not found in source.**
>
> The draft claims the next song is eligible only if its
> FIRST CHORD exactly equals the previous song's LAST CHORD.
> The cited source does not chain on chords: Endeless
> `Endeless/workers/endeless_worker.py`
> `random_search_next_song` chains on NOTES —
> `df["First_Note"] == df["Last_Note"][index]` — with random
> choice among matches and re-rolls while the choice is
> already in the playlist ("Do not select the same song").
> `chord_recognition.py` exists in the repo but only fills
> dataset fields; it is not the chaining key. The
> repeat-exclusion and random-choice-among-matches parts of
> the draft ARE confirmed; the chord-equality key is NOT.
> Do not implement, demo, or promote this draft until the
> summary is corrected to note-equality (or the draft is
> parked). No applicability or registry-fit sections were
> added, because they would describe a mechanism the source
> does not contain.

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
