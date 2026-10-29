# DRAFT: aubio_onset_beat_detection

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: aubio (https://github.com/aubio/aubio)
- License note: GPL-3.0-or-later
- Summary: Onset/beat detection for cue placement and beat-grid measurement (aubio: library for audio and music analysis). [Repo-grounded; scout named no mechanism for aubio.]

## Evidence (mechanism confirmed)

Onset detection and tempo/beat tracking, verified first-hand
2026-10-29 against a shallow clone of the registered source
(https://github.com/aubio/aubio, GPL-3.0-or-later): `src/onset/`
(onset.c, onset.h, peakpicker) exposes `new_aubio_onset` /
`aubio_onset_do` with last-onset sample/ms accessors, and
`src/tempo/` (tempo.c, beattracking.c) provides tempo tracking
and beat detection. The README describes the same scope —
"several onset detection methods", "tempo tracking and beat
detection", `aubiocut` slicing sound files at onset or beat
timestamps, and `aubioonset` outputting detected note-onset
timestamps. The mechanism is exactly the queue summary's claim:
onset/beat detection usable for cue placement and beat-grid
measurement. No correction to the summary was needed. Note the
source is an analysis library, not a DJ transition: its output
is measurement (timestamps/tempo), not a render move.

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap or tempo applicability
  (detection is applied to audio, not gated on tempo).
- Key/harmonic: source gives no key applicability.
- Energy: source gives no energy applicability.
- Sections: source gives no song-section applicability (no
  intro/outro/chorus gating is stated; onsets/beats are
  detected across the file).
- Vocals: source gives no vocal applicability (no
  vocal-presence gating is stated).
- Genre families: source gives no genre applicability.
- Use when: cue placement or beat-grid measurement is wanted
  before a transition is built — e.g. placing a cue on a
  detected onset or beat, or measuring a track's beat grid
  offline before the set/render.
- Avoid when: a transition move itself is required (this is a
  measurement/prep step, not a blend, swap, or fade); a
  detection-accuracy guarantee is required (no accuracy or
  error bound is stated in the source's detection
  description); the measurement must come from a live deck
  (the source documents library/CLI analysis of audio, no
  live-deck mode is stated).

## Registry fit (META schema)

- Kind: measurement/prep enabling step for cue placement and
  beat-grid-dependent techniques, not itself a render move —
  a promotion assessment should decide whether the META entry
  is the transition that consumes these measurements, with
  this draft as its evidence, rather than a standalone
  technique entry; it should also check for duplication
  against the existing beat-grid/cue family and the Essentia
  beat-tracking and librosa beat-tracked drafts before any
  META entry.
- Requires: audio analyzed offline (library/CLI step) yielding
  onset timestamps and tempo/beat data before the set/render;
  no bpm_delta_pct_max, camelot_max, phrase, or genre gating
  stated for the detection itself.
- Energy: delta 0 for the measurement step itself (energy
  profile belongs to the transition that consumes the
  measurements, not to the detection). Exit: n/a for the prep
  step (the consuming transition's exit profile applies).
  Clash risk: detection accuracy is not modeled in the
  source's description (no accuracy bound is stated).
- Evidence reference: aubio `src/onset/onset.h`
  (`new_aubio_onset`, `aubio_onset_do`, last-onset accessors),
  `src/tempo/` (tempo.c, beattracking.c), and README onset /
  tempo / beat-detection description, source aubio
  (https://github.com/aubio/aubio, GPL-3.0-or-later —
  learn-from only, never copy code).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from aubio. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
