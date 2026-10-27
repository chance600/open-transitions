# DRAFT: vocal_clash_ducking

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: rustlarpdj (https://github.com/T-Perm/RustLarpDJ)
- License note: license unconfirmed - learn-from only, no code reuse
- Summary: Lyric vocal windows for both tracks mapped onto wall-clock overlap via tempo anchors, with overlapping windows triggering a -9 dB mid-EQ duck on the outgoing deck starting 1 beat early; transfers as a vocal guard that ducks rather than blocks a blend.

## Evidence (mechanism confirmed)

RustLarpDJ `crates/ai/src/vocal_clash.rs` + `moves.rs`,
verified first-hand 2026-10-27: `clash_windows` maps lyric
vocal windows for both tracks onto wall-clock overlap via
tempo anchors (overlap = clash; empty when either side has no
windows); the move script ducks the outgoing mids -9 dB
(VOCAL_DUCK_DB), starting 1 beat early
((duck_in - 1.0)), restoring after the clash. Evidence path:
`RustLarpDJ/crates/ai/src/vocal_clash.rs` +
`RustLarpDJ/crates/ai/src/moves.rs` (survey:
STAR-DEEP-CANDIDATES `vocal_clash_ducking`).

## Applicability (selector fields)

- Tempo: windows map via tempo anchors. Use when lyric timing
  plus tempo anchors exist for both sides. Avoid when lyric
  data is missing for either side: `clash_windows` returns
  empty, so the guard silently does nothing.
- Key / energy / sections / genre: source gives no
  applicability.
- Vocals: this IS the vocal guard. Use when lyric windows
  overlap and a -9 dB mid duck on the outgoing deck is
  acceptable. Avoid when the outgoing vocal must stay fully
  present through the overlap — the duck audibly suppresses
  it, so the pair needs a different arrangement (a cut, not a
  blend).

## Registry fit (META schema)

- Kind: render (guard, applied within a blend).
- Requires: needs lyric windows plus tempo anchors on both
  sides; vocal_ok: both (it exists for the overlap case).
- Energy: delta 0, tension flat (guard, not arc). Exit:
  seamless (the guard preserves the blend). Clash risk: vocal
  (managed by the duck).
- Evidence reference: RustLarpDJ `vocal_clash.rs` + `moves.rs`
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
