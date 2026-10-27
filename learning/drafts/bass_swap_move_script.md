# DRAFT: bass_swap_move_script

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: rustlarpdj (https://github.com/T-Perm/RustLarpDJ)
- License note: license unconfirmed - learn-from only, no code reuse
- Summary: A chosen style compiles to a timed automation script of EQ/filter/gain moves in beats (incoming bass killed, tucked -14 dB pre-swap, swap window, highs opened/ducked); transfers as techniques that output executable move lists, not just names.

## Evidence (mechanism confirmed)

RustLarpDJ `crates/ai/src/moves.rs`, verified first-hand 2026-10-27:
TUCK_DB -14.0; move labelled "incoming bass killed";
`swap_window_beats()` bounding the swap; "opening the incoming
highs" (from a -6 dB rolloff) and "ducking the outgoing highs"
(-9 dB); a vocal-clash duck move on the outgoing mids (-9 dB,
starting 1 beat early). Evidence path:
`RustLarpDJ/crates/ai/src/moves.rs` (survey: STAR-DEEP-CANDIDATES
`bass_swap_move_script`).

## Applicability (selector fields)

- Tempo: beat-anchored moves scheduled in beats. Source states no
  BPM-gap cap for the move list itself (tempo fit is scored
  upstream in `choose_transition`, not in `moves.rs`).
- Key/harmonic: source gives no key applicability for the move
  list itself.
- Energy: source gives no energy applicability.
- Sections: swaps anchor to named sections (source tests: a bass
  kill lands a bar before the drop; scripted kills name a
  section). Use when a section boundary can host the swap
  window. Avoid when no section anchor exists inside the overlap.
- Vocals: the script carries a vocal-clash duck (outgoing mids
  -9 dB, 1 beat early). Use when lyric windows overlap and a duck
  is acceptable. Avoid when both sides carry vocals that must
  stay fully present — the duck audibly suppresses the outgoing
  vocal.
- Genre families: source gives no genre applicability.

## Registry fit (META schema)

- Kind: render (move-list primitive — a technique that outputs
  executable moves, not just a name).
- Requires: needs a beat grid and a section anchor; no
  bpm_delta_pct_max or camelot_max stated in the source;
  vocal_ok: a_only / b_only / both / neither (ducking guards
  overlap); phrase_a_ok: any section the script can name.
- Energy: delta 0, tension flat. Exit: snap (swap window).
  Clash risk: bass (primary), vocal guarded.
- Evidence reference: RustLarpDJ `moves.rs` (learn-only,
  license unconfirmed).

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
