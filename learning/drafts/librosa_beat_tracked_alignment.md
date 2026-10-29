# DRAFT: librosa_beat_tracked_alignment

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: librosa (https://github.com/librosa/librosa)
- License note: ISC
- Summary: Beat-tracked alignment (librosa.beat.beat_track): beat grid measurement for cue placement and segment alignment. [Repo-grounded; scout named no mechanism for librosa.]

## Evidence (mechanism confirmed)

librosa official tutorial (0.10.2), verified first-hand
2026-10-29: `tempo, beat_frames =
librosa.beat.beat_track(y=y, sr=sr)` — the beat tracker
returns an estimated tempo (in beats per minute) and an array
of frame numbers for detected beat events, convertible to
timestamps with `librosa.frames_to_time`. The candidate's
transfer — beat-grid measurement for cue placement and
segment alignment — is exactly what this output supplies:
a measured grid, not a transition move.

## Applicability (selector fields)

- Tempo: the grid is measured per track and the tracker
  itself estimates tempo, so the source states no BPM-gap
  cap for this measurement step; tempo-gap handling stays
  the selector's separate job.
- Key/harmonic: source gives no key applicability — a beat
  grid is key-independent.
- Energy: source gives no energy applicability.
- Sections: source gives no section restriction — the grid
  covers the track and serves cue placement / segment
  alignment anywhere in it.
- Vocals: source gives no vocal applicability.
- Genre families: source gives no genre applicability.
- Use when: a measured beat grid is needed to place cues
  or align segments before a transition is chosen or
  executed.
- Avoid when: the job is the transition move itself (this
  supplies the grid the move rides on, it is not the move);
  or the grid is treated as ground truth rather than an
  estimate — the source's own wording is "estimated tempo"
  and detected beat events, so a grid that misreads the
  beat needs checking before it places cues.

## Registry fit (META schema)

- Kind: measurement/decision primitive, not a standalone
  render move — it decides where cues and segments sit,
  and rides on the host transition's own move (same class
  select.py already excludes from ranked transitions).
- Requires: audio input for each track to measure; no
  bpm_delta_pct_max, camelot_max, vocal, phrase, or genre
  precondition of its own — measurement precedes selection.
- Energy: delta 0, tension flat (measurement only, not an
  energy move). Exit: none of its own (host transition's
  exit). Clash risk: none of its own.
- Evidence reference: librosa official tutorial,
  `librosa.beat.beat_track` (ISC).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from librosa. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
