# DRAFT: hold_blend_curve

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: rustlarpdj (https://github.com/T-Perm/RustLarpDJ)
- License note: license unconfirmed - learn-from only, no code reuse
- Summary: Crossfade curve ramping to a -3 dB centre, holding both decks audible through the middle, then completing; transfers as a curve family with a centre-hold parameter, distinct from linear/smoothstep fades.

## Evidence (mechanism confirmed)

RustLarpDJ `crates/ai/src/transition_style.rs`
`Curve::HoldBlend { ramp_in, ramp_out }`, verified first-hand
2026-10-27: the curve ramps in, holds at 0.5 gain through the
middle, then ramps out; the shipped BLEND_CURVE uses ramp_in
0.15, ramp_out 0.20. The draft's "-3 dB centre" phrasing matches
the source's own test language ("holding at the -3 dB centre").
Evidence path: `RustLarpDJ/crates/ai/src/transition_style.rs`
(survey: STAR-DEEP-CANDIDATES `hold_blend_curve`).

## Applicability (selector fields)

- Tempo: beat-anchored curve (durations in beats). Source
  states no BPM-gap cap.
- Key/harmonic: source gives no key applicability.
- Energy: the hold keeps both decks audible through the middle.
  Use when a sustained dual-presence middle is wanted (both
  tracks audible, neither dropped). Avoid when the outgoing
  track must exit cleanly before the incoming establishes — a
  hold keeps it present, which is the opposite of a cut.
- Sections: source gives no section applicability (the curve
  applies to any overlap window).
- Vocals: source gives no vocal applicability for the curve
  itself (vocal clashes are handled by the separate vocal-clash
  module, not by the curve).
- Genre families: source gives no genre applicability.

## Registry fit (META schema)

- Kind: render (curve family, distinct from linear/smoothstep
  fades).
- Requires: needs an overlap window in beats. No
  bpm_delta_pct_max, camelot_max, vocal, phrase, or genre
  gating stated for the curve itself.
- Energy: delta 0, tension flat (both decks held). Exit:
  seamless. Clash risk: bass (both decks' lows are present
  through the middle unless separately managed).
- Evidence reference: RustLarpDJ `transition_style.rs`
  (learn-only, license unconfirmed).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from rustlarpdj. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
