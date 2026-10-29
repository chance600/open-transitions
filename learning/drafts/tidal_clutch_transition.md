# DRAFT: tidal_clutch_transition

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: tidalcycles (https://codeberg.org/uzu/tidal)
- License note: GPL-3.0
- Summary: clutch/clutchIn transition functions: cycle-counted
  pattern handover by event degradation (clutch = 2 cycles,
  clutchIn = explicit count).

## Evidence (mechanism confirmed)

TidalCycles `clutch` / `clutchIn`, verified first-hand 2026-10-29
against the official Transitions documentation
(tidalcycles.org/docs/reference/transitions/): `clutch` "degrades
the current pattern while undegrading the next" — "like `xfade`
but not by gain of samples but by randomly removing events from
the current pattern and slowly adding back in missing events from
the next one." `clutch` takes two cycles for the transition
(essentially `clutchIn 2`); `clutchIn` is the `In` variant taking
an explicit cycle count. Correction to the queue summary's label:
the mechanism is NOT "hold the current pattern while the incoming
pattern prepares, then switch" — the docs describe no hold and no
deferred switch, only a gradual event-degradation handover spread
over cycles. The draft's operative claim is only what the docs
confirm: a cycle-counted pattern transition by event degradation,
not by gain. The mechanism is a live-coding pattern transition,
not a DJ track transition: both patterns run under one shared
tempo (patterns do not have independent tempos in Tidal), and the
handover length is counted in cycles, not beats or bars of a song.

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap; the handover is
  cycle-counted under a single shared tempo, so no tempo-gap
  applicability is stated.
- Key/harmonic: source gives no key applicability.
- Energy: source gives no energy applicability.
- Sections: source gives no song-section applicability (the unit
  is a pattern, not an intro/outro/chorus).
- Vocals: source gives no vocal applicability (no vocal
  detection, ducking, or clash guard in the transition).
- Genre families: source gives no genre applicability.
- Use when: a gradual change from one pattern to another over a
  set number of cycles is wanted, with the outgoing pattern's
  events thinning out while the incoming pattern's events fill
  in — a textural handover rather than a gain crossfade.
- Avoid when: a gain crossfade is required (that is `xfade`, not
  `clutch`); an immediate switch is required (that is the `jump`
  transition); the seam must land on a song-section boundary
  (the source counts cycles, not sections); the two sides run at
  independent tempos (the source supports one shared tempo only);
  vocal- or key-clash protection is required (none is provided).

## Registry fit (META schema)

- Kind: render (event-degradation handover over N cycles;
  parameter: cycle count, default 2 via `clutch`, explicit via
  `clutchIn`) — a textural alternative to the existing
  crossfade family (`eq_blend`, `tidal_xfade_transition` draft);
  a promotion assessment should check for duplication against
  those before any META entry, and should decide whether event
  thinning maps onto the render engine at all (the source
  thins pattern events, not audio stems).
- Requires: two patterns on the same stream/channel under one
  shared tempo; no bpm_delta_pct_max, camelot_max, vocal,
  phrase, or genre gating stated for the transition itself.
- Energy: delta 0, tension flat. Exit: seamless (handover
  completion at cycle-count end). Clash risk: not modeled in
  the source (both patterns' events interleave audibly with no
  key or vocal guard).
- Evidence reference: TidalCycles Transitions documentation,
  `clutch` / `clutchIn` section, source tidalcycles
  (https://codeberg.org/uzu/tidal, GPL-3.0, learn-from only).

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
