# DRAFT: ffmpeg_curve_equal_power_crossfade

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: ffmpeg (https://github.com/FFmpeg/FFmpeg)
- License note: LGPL-2.1-or-later (GPL-2.0-or-later for optional parts) — learn-from only
- Summary: Curve-selected equal-power crossfade via afade/acrossfade (libavfilter/af_afade.c): per-stream fade curve selection (tri, qsin, esin, hsin, log, ...) for the acrossfade. Chained-multi-input and band-split variants NOT queued (unverified in official docs).

## Evidence (mechanism confirmed)

FFmpeg `acrossfade` filter, verified first-hand 2026-10-29
against the official filters documentation (acrossfade section:
`curve1` sets the curve for the first stream, `curve2` for the
second, curve types as described under `afade`) and the local
FFmpeg 8.1.2 build (`ffmpeg -h filter=acrossfade`): `curve1` /
`curve2` (default `tri`) with `tri`, `qsin`, `esin`, `hsin`,
`log`, `ipar`, `qua`, `cub`, `squ`, `cbr`, `par`, `exp`, and
inverted variants; duration set by `duration` / `nb_samples`,
`overlap` on by default. Correction to the queue summary's
label: FFmpeg names no "equal-power" mode — equal-power behaviour
is a curve-pair choice (complementary sine-family curves), not a
dedicated mode, and the draft is written on that corrected basis
(filename kept for queue linkage). The chained-multi-input and
band-split variants stay unqueued, as the queue entry states.

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap and no beat quantization
  (duration is in samples/seconds, not beats).
- Key/harmonic: source gives no key applicability.
- Energy: source gives no energy applicability.
- Sections: source gives no section applicability.
- Vocals: source gives no vocal applicability (no vocal
  detection or ducking in the filter options).
- Genre families: source gives no genre applicability.
- Use when: a timed crossfade between two audio streams with a
  per-stream curve choice is wanted, in generic terms (e.g. a
  sine-family pair where constant perceived loudness through the
  middle matters). Avoid when: a beat- or phrase-aligned
  transition is required (the filter places by time, not by
  beat); when vocal-clash protection is required (none is
  provided); when the seam must be sequential rather than
  overlapped (that is the `overlap=0` case, a different shape
  from a blend).

## Registry fit (META schema)

- Kind: render (curve-shape parameter for crossfades: per-stream
  curve1/curve2, duration, overlap) — overlaps the existing
  fade-shape vocabulary family; a promotion assessment should
  check for duplication against `fade_shape_vocabulary` before
  any META entry.
- Requires: two audio streams and a duration; no bpm_delta_pct_max,
  camelot_max, vocal, phrase, or genre gating stated for the
  filter itself.
- Energy: delta 0, tension flat. Exit: crossfade completion at
  duration end. Clash risk: none stated (no clash model in the
  filter).
- Evidence reference: FFmpeg `acrossfade` / `afade` filter
  documentation and local FFmpeg 8.1.2 filter help
  (LGPL-2.1-or-later, learn-from only).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from ffmpeg. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
