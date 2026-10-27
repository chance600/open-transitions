# DRAFT: spectral_band_swap

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: auto-dj-ai (https://github.com/caffettino87/auto-dj-ai)
- License note: MIT
- Summary: 3-band EQ swap where the low band is always deep-cut on the incoming track (-26 dB) and restored over the fade, and mid/high cuts scale by per-band spectral clash; transfers as a parameterized registry technique with band corners, cut depths and swap timing.

## Evidence (mechanism confirmed)

auto-dj-ai `src/player.js`, verified first-hand 2026-10-27:
BASS_CUT_DB -26 ("deep low cut on the incoming track (bass
swap)"); MID_MAX_DB 9 "scaled by how much the mids clash";
HIGH_MAX_DB 5 "scaled by clash"; clash-proportioned cuts
(midCut = -9 * clash.mid, highCut = -5 * clash.high) with the
low band held then swapped; `bandClash` per-band intensity as
the geometric mean of normalized band energies. Evidence path:
`auto-dj-ai/src/player.js` (survey: STAR-DEEP-CANDIDATES
`spectral_band_swap`).

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap (the swap is EQ-timed to
  the fade, not beat-quantized in the cited code).
- Key/harmonic: source gives no key applicability.
- Energy: source gives no energy applicability.
- Sections: source gives no section applicability.
- Vocals: source gives no vocal applicability for the swap
  itself (vocal-aware cut points are a separate schema in the
  same file — not conflated here).
- Genre families: source gives no genre applicability.
- Use when per-band spectral clash is measured for both tracks
  (the cuts scale from measured band energy). Avoid when band
  energy is unmeasured: `bandClash` falls back to low-only
  (mid/high cuts zero), so the swap degrades to a bass-only
  cut.

## Registry fit (META schema)

- Kind: render (parameterized EQ swap: band corners, cut
  depths, swap timing).
- Requires: needs measured band energy on both sides. No
  bpm_delta_pct_max, camelot_max, vocal, phrase, or genre
  gating stated for the swap itself.
- Energy: delta 0, tension flat. Exit: snap (swap window).
  Clash risk: bass (primary, managed by the cut).
- Evidence reference: auto-dj-ai `player.js` (MIT).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from auto-dj-ai. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
