# DRAFT: chord_domino_pair_match

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: endeless (https://github.com/Aurbcd/Endeless)
- License note: MIT
- Name note: the filename keeps the survey's "chord_domino"
  phrasing for queue linkage; the mechanism is NOTE-equality,
  not chord-equality (corrected 2026-10-27 — see Evidence).
- Summary: Next song eligible only if its FIRST NOTE exactly
  equals the previous song's LAST NOTE, chosen at random among
  all matching songs, re-rolling while the choice is already in
  the playlist; if every match is already used (or none exists)
  the chain is exhausted. A bridge variant fills between a
  start and an end song: the fill song's first note must equal
  the start song's last note AND its last note must equal the
  end song's first note. Transfers as a hard pair-eligibility /
  selection rule on boundary notes.

## Evidence (mechanism confirmed)

Endeless `Endeless/workers/endeless_worker.py`, verified
first-hand 2026-10-27: `random_search_next_song` filters
`df["First_Note"] == df["Last_Note"][index]`, picks with
`random.choice` among matches ("random search, show be more
like dominos"), re-rolls `while index_next_song in playlist`
("Do not select the same song"), and raises
`NoMoreSongToFitIn` when all matches are used or none exist.
The fill variant applies the same key at both ends
(`First_Note == Last_Note[start]` and
`Last_Note == First_Note[end]`). `First_Note` / `Last_Note`
are per-song dataset fields (with `First_Note_Time` /
`Last_Note_Time`); `chord_recognition.py` only fills dataset
fields and is not the chaining key. The earlier chord-equality
wording was the survey's phrasing, not the source; corrected
here, nothing else in the mechanism changed — repeat-exclusion
and random-choice-among-matches were already confirmed.

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap for chaining itself; the
  rule is note identity, not tempo. Tempo-gap handling stays
  the selector's separate job.
- Key/harmonic: note identity is the compatibility signal, but
  the source gives no Camelot/key-distance rule — a shared
  boundary note is not claimed as harmonic compatibility.
- Energy: source gives no energy applicability. The rule selects
  which track follows, not how energy moves.
- Sections: applies at track boundaries in playlist/sequence
  construction, not inside a transition; it is a selection
  rule, not a section-crossing move.
- Vocals: source gives no vocal applicability — note-equality
  does not gate on vocals.
- Genre families: source gives no genre applicability; the
  only structural assumption is measured first/last notes.
- Use when: building a sequence where consecutive tracks
  should share a boundary note and a pool of candidate tracks
  with measured first/last notes exists.
- Avoid when: no unused match exists (the chain is exhausted
  by design, not a failure to retry blindly); the job is a
  single pair rather than a sequence (selection is not the
  question); or tracks lack measured first/last notes (the
  rule cannot be evaluated).

## Registry fit (META schema)

- Kind: selection rule (pair eligibility), not a standalone
  render move — it decides which track follows, and rides on
  the host transition's own move.
- Requires: a first note and a last note measured for each
  candidate track; a pool with at least one unused match.
  No stems, vocal, key, or tempo precondition of its own.
- Energy: delta 0, tension flat (selection only, not an
  energy move). Exit: seamless (as the host transition's
  exit). Clash risk: none of its own.
- Evidence reference: Endeless
  `Endeless/workers/endeless_worker.py`
  `random_search_next_song` + bridge-fill variant (MIT).

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
