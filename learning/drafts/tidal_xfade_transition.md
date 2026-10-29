# DRAFT: tidal_xfade_transition

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: tidalcycles (https://codeberg.org/uzu/tidal)
- License note: GPL-3.0
- Summary: xfade/xfadeIn transition functions (Boot.hs): crossfade one pattern into another over a set number of cycles (xfade defaults to 4).

## Evidence (mechanism confirmed)

TidalCycles `xfade` / `xfadeIn`, verified first-hand 2026-10-29
against the official Transitions documentation (current docs
signatures: `xfade :: Show a => a -> ControlPattern -> IO ()`,
`xfadeIn :: Show a => a -> Time -> ControlPattern -> IO ()`;
docs example: `xfadeIn 1 8` fades over 8 cycles, and the "In"
variant is documented as specifying "the number of cycles that
the transition takes to complete"). Correction to the queue
summary's label: the file is BootTidal.hs, not Boot.hs
(filename kept for queue linkage). Correction to an earlier
draft claim, made on verification 2026-10-29: the quoted
definition `xfade i = transition tidal True
(Sound.Tidal.Transition.xfadeIn 4) i` was NOT reproduced in
the current source — the mirror's BootTidal.hs is a 27-line
boot stub with no xfade definition, and its Transition.hs
shows a Time-based `xfadeIn`. So the "xfade defaults to 4
cycles" detail is older-API/unconfirmed-in-current-source and
is NOT relied on here; the draft's operative claim is only
what the current docs confirm: xfade crossfades one pattern
into another, and xfadeIn takes an explicit cycle count. The mechanism is a live-coding
pattern transition, not a DJ track transition: both patterns run
under one shared tempo (patterns do not have independent tempos
in Tidal), and the fade length is counted in cycles, not beats
or bars of a song.

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap; the fade is cycle-counted
  under a single shared tempo, so no tempo-gap applicability is
  stated.
- Key/harmonic: source gives no key applicability.
- Energy: source gives no energy applicability.
- Sections: source gives no song-section applicability (the unit
  is a pattern, not an intro/outro/chorus).
- Vocals: source gives no vocal applicability (no vocal
  detection, ducking, or clash guard in the transition).
- Genre families: source gives no genre applicability.
- Use when: a gradual change from one pattern to another over a
  set number of cycles is wanted, with both patterns audible
  through the middle of the fade.
- Avoid when: an immediate switch is required (that is the
  `jump` transition, not a crossfade); when the seam must land
  on a song-section boundary (the source counts cycles, not
  sections); when the two sides run at independent tempos (the
  source supports one shared tempo only); when vocal- or
  key-clash protection is required (none is provided).

## Registry fit (META schema)

- Kind: render (crossfade over N cycles; parameter: cycle count,
  default 4 via `xfade`, explicit via `xfadeIn`) — overlaps the
  existing crossfade family (`eq_blend` and the fade-shape
  vocabulary); a promotion assessment should check for
  duplication against those before any META entry.
- Requires: two patterns on the same stream/channel under one
  shared tempo; no bpm_delta_pct_max, camelot_max, vocal,
  phrase, or genre gating stated for the transition itself.
- Energy: delta 0, tension flat. Exit: seamless (crossfade
  completion at cycle-count end). Clash risk: not modeled in
  the source (both patterns overlap audibly with no key or
  vocal guard).
- Evidence reference: TidalCycles Transitions documentation and
  BootTidal.hs `xfade` / `xfadeIn` definitions, source
  tidalcycles (https://codeberg.org/uzu/tidal, GPL-3.0,
  learn-from only).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from tidalcycles. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
