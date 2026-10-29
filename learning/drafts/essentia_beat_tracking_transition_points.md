# DRAFT: essentia_beat_tracking_transition_points

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: essentia (https://github.com/MTG/essentia)
- License note: AGPL-3.0 — learn-from only
- Summary: Beat tracking (src/algorithms/rhythm: BeatTrackerMultifeature, BeatTrackerDegara, BPMHistogram) for beat-grid and transition-point measurement. [Repo-grounded; scout named no mechanism for essentia.]

## Evidence (mechanism confirmed)

Beat tracking and tempo estimation, verified first-hand
2026-10-29 against a shallow sparse clone of the registered
source (https://github.com/MTG/essentia, AGPL-3.0 — learn-from
only): `src/algorithms/rhythm/` contains
`beattrackermultifeature.h/.cpp` (BeatTrackerMultiFeature,
outputs beat ticks plus a confidence value, with minTempo /
maxTempo detector parameters defaulting to 40 / 208 BPM),
`beattrackerdegara.h/.cpp` (BeatTrackerDegara), and
`bpmhistogram.h/.cpp` (BpmHistogram, outputs BPM candidates
and magnitudes). The mechanism is exactly the queue summary's
claim: beat tracking for beat-grid and transition-point
measurement. No correction to the summary was needed. Note the
source is an analysis library, not a DJ transition: its output
is measurement (beat ticks, tempo estimates, confidence), not
a render move.

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap or transition tempo
  applicability (the 40–208 BPM figures are detector parameter
  bounds, not a gate on which transitions fit).
- Key/harmonic: source gives no key applicability.
- Energy: source gives no energy applicability.
- Sections: source gives no song-section applicability (no
  intro/outro/chorus gating is stated; beats are tracked
  across the audio).
- Vocals: source gives no vocal applicability (no
  vocal-presence gating is stated).
- Genre families: source gives no genre applicability.
- Use when: beat-grid or transition-point measurement is
  wanted before a transition is built — e.g. measuring a
  track's beat positions and tempo offline before the
  set/render, so a later transition can be placed on a beat.
- Avoid when: a transition move itself is required (this is a
  measurement/prep step, not a blend, swap, or fade); a
  detection-accuracy guarantee is required (a confidence
  output exists, but no accuracy or error bound is stated in
  the checked headers); the measurement must come from a
  live deck (the source documents library analysis of audio,
  no live-deck mode is stated).

## Registry fit (META schema)

- Kind: measurement/prep enabling step for beat-grid and
  transition-point-dependent techniques, not itself a render
  move — a promotion assessment should decide whether the
  META entry is the transition that consumes these
  measurements, with this draft as its evidence, rather than
  a standalone technique entry; it should also check for
  duplication against the existing beat-grid/cue family and
  the aubio onset/beat-detection and librosa beat-tracked
  drafts before any META entry.
- Requires: audio analyzed offline (library step) yielding
  beat ticks, tempo estimates, and confidence before the
  set/render; no bpm_delta_pct_max, camelot_max, phrase, or
  genre gating stated for the tracking itself.
- Energy: delta 0 for the measurement step itself (energy
  profile belongs to the transition that consumes the
  measurements, not to the tracking). Exit: n/a for the prep
  step (the consuming transition's exit profile applies).
  Clash risk: tracking confidence is output but no accuracy
  bound is stated, so it is not modeled as a guarantee.
- Evidence reference: essentia `src/algorithms/rhythm/`
  (`beattrackermultifeature.h` ticks + confidence, minTempo
  40 / maxTempo 208 defaults; `beattrackerdegara.h`;
  `bpmhistogram.h` BPM candidates), source essentia
  (https://github.com/MTG/essentia, AGPL-3.0 — learn-from
  only, never copy code).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from essentia. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
