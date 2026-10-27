# DRAFT: downbeat_anchored_cue_window

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: djtransgan (https://github.com/ChenPaulYu/DJtransGAN)
- License note: MIT
- Summary: Transition window starts 8 bars before the cue, snapped to the nearest detected downbeat; transfers as a placement rule: never start a transition mid-bar, always on a downbeat N bars early.

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap for cue placement itself;
  the window is defined in bars (CUE_BAR = 8), not in seconds or
  BPM delta. Tempo-gap handling stays the selector's separate job.
- Key/harmonic: source gives no key applicability — anchoring a
  window on a downbeat does not change harmonic compatibility.
- Energy: source gives no energy applicability. The rule sets
  where a transition window starts, not how energy moves.
- Sections: the window runs from a downbeat 8 bars before the
  cue to the cue itself, on both decks. Use when the cues mark
  the intended transition edges; the window is a lead-in, not a
  section-crossing move.
- Vocals: source gives no vocal applicability — downbeat
  anchoring does not gate on vocals.
- Genre families: source gives no genre applicability; bar and
  downbeat structure is the only structural assumption.
- Use when: a transition is placed by cue points on both decks
  and an 8-bar downbeat-anchored lead-in window is wanted, so
  the move never starts mid-bar.
- Avoid when: either side lacks a detected downbeat grid or a
  cue point (the window cannot be anchored), or the move is
  instantaneous (a cut or drop) and takes no lead-in window.

## Registry fit (META schema)

- Kind: placement rule (cue-window placement), not a standalone
  render move — it sets where a transition's window starts, and
  rides on the host transition's own move.
- Requires: detected downbeats for both tracks plus a cue point
  on each side; parameter CUE_BAR (8 in the source). No stems,
  vocal, or key precondition of its own.
- Energy: delta 0, tension flat (placement only, not an energy
  move). Exit: seamless (as the host transition's exit).
  Clash risk: none of its own.
- Evidence reference: DJtransGAN `djtransgan/process/utils.py`
  `select_cue_points` + `correct_cue`, `djtransgan/config/
  settings.py` CUE_BAR = 8 (MIT).

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
