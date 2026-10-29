# DRAFT: subwave_ending_shaped_crossfade

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: subwave (https://github.com/perminder-klair/subwave)
- License note: MIT — radio-automation transfer (conceptual, not a DJ-set technique)
- Summary: Ending-shaped crossfade length (radio-automation transfer, conceptual): crossfade sizes itself to how the track ends — a real fade rides out long, a cold ending cuts tight.

## Evidence (mechanism confirmed)

Ending-shaped crossfade length, verified first-hand
2026-10-29 against a shallow clone of the registered
source (https://github.com/perminder-klair/subwave, MIT):
README "Ending-aware transitions" states the bundled
analyzer "measures BPM, key, loudness, and how every
track actually ends, so crossfades size themselves to
the material: a real fade rides out long, a cold ending
cuts tight." The playout side carries per-track sizing:
`liquidsoap/radio.liq` reads a per-track
`liq_cross_duration` / `liq_cross_end_duration` stamp
against a station crossfade default, so the length is a
per-track value, not one fixed duration. No numeric
mapping (fade-out -> N seconds, cold ending -> M
seconds) is stated in the source, and none is invented
here. The mechanism is exactly the queue summary's
claim. Note the source is radio automation, not a DJ
set: the transfer is conceptual, as the queue summary
itself states.

## Applicability (selector fields)

- Tempo: source gives no tempo applicability for the
  sizing rule (the analyzer measures BPM, but no BPM
  gate on crossfade length is stated).
- Key/harmonic: source gives no key applicability for
  the sizing rule (key is measured, but no key gate on
  crossfade length is stated).
- Energy: source gives no energy applicability (loudness
  is measured, but no energy gate on crossfade length
  is stated).
- Sections: ending shape only — the outgoing track's
  tail/outro: a real fade-out vs a cold ending.
- Vocals: source gives no vocal applicability for the
  sizing rule (its vocal detection guards DJ talk-over
  a sung intro, a separate decision).
- Genre families: source gives no genre applicability
  (a radio-playout rule, genre-agnostic by construction).
- Use when: the outgoing track's ending shape has been
  measured (real fade-out vs cold ending) and the
  crossfade length is being sized to that ending.
- Avoid when: the outgoing ending is unmeasured or
  unknown (there is then no basis for sizing); a live
  deck move is required (the source is radio-automation
  playout, not deck hardware or DJ software).

## Registry fit (META schema)

- Kind: crossfade-length rule / playout parameter, not
  itself a standalone named DJ technique with its own
  exit profile — a promotion assessment should check
  for duplication against the existing crossfade/eq_blend
  family before any META entry.
- Requires: a measured ending classification for the
  outgoing track plus a per-track crossfade duration;
  no bpm_delta_pct_max, camelot_max, phrase, or genre
  gating stated for the sizing rule itself.
- Energy: delta 0 for the rule itself (energy profile
  belongs to the transition that consumes it, not to
  the length rule). Exit: fade-out ending rides out
  long; cold ending cuts tight. Clash risk: none modeled
  — sizing addresses ending shape only, not key, tempo,
  or vocal clash.
- Evidence reference: subwave README "Ending-aware
  transitions" + `liquidsoap/radio.liq` per-track cross
  stamps, source subwave
  (https://github.com/perminder-klair/subwave, MIT).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from subwave. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
