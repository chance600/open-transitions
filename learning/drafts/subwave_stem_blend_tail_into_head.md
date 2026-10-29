# DRAFT: subwave_stem_blend_tail_into_head

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: subwave (https://github.com/perminder-klair/subwave)
- License note: MIT — radio-automation transfer (conceptual, not a DJ-set technique)
- Summary: Stem-blend tail-into-head (radio-automation transfer, conceptual): opt-in stem blends mix the outgoing tail into the incoming head for a produced seam.

## Evidence (mechanism confirmed)

Stem-blend tail-into-head, verified first-hand
2026-10-29 against a shallow clone of the registered
source (https://github.com/perminder-klair/subwave, MIT):
README "Ending-aware transitions" states "opt-in stem
blends mix the outgoing tail into the incoming head
for a produced-sounding seam." `docs/internals/broadcast.md`
("Stem blends", opt-in `transitions.stemBlends`,
`broadcast/stem-blend.ts` + worker `render_transition`):
at a pair drain, a cache-hit-only render mixes the
outgoing tail stems x incoming head stems (`state/stems/`,
written during analysis when `audio.stemCache` is on)
into a clip that airs between them — outgoing cues out
at the blend start, the clip carries the INCOMING track's
identity, incoming cues in past its pre-mixed head. Any
miss falls back to a plain pair-aware crossfade. A blend
needs stems on both tracks (`docs/concepts.md` stem cache:
four separated stems — drums, bass, other, vocals — for
both sides), and the seam sides must carry bar grids
(incoming bars, outgoing outro bars + duration). No
blend length in seconds is stated in the source, and
none is invented here. The mechanism is exactly the
queue summary's claim. Note the source is radio
automation, not a DJ set: the transfer is conceptual,
as the queue summary itself states.

## Applicability (selector fields)

- Tempo: source gives no tempo gate for stem blends
  (the analyzer measures BPM, but no BPM gate on the
  blend is stated).
- Key/harmonic: source gives no key gate for stem blends.
- Energy: source gives no energy gate for stem blends.
- Sections: outgoing tail x incoming head only; both
  sides must carry bar grids (incoming bars, outgoing
  outro bars).
- Vocals: source gives no vocal applicability rule for
  the blend (vocals are one of the four separated stems,
  but no vocal-presence gate is stated).
- Genre families: source gives no genre applicability
  (a radio-playout rule, genre-agnostic by construction).
- Use when: the stem cache is on, stems are cached for
  both sides of the pair, and the seam is a pair drain
  with an outgoing tail and an incoming head available.
- Avoid when: either side's stems are missing (the seam
  falls back to a plain crossfade, so a blend cannot be
  planned as guaranteed); a live deck move is required
  (the source is radio-automation playout, not deck
  hardware or DJ software).

## Registry fit (META schema)

- Kind: pre-rendered seam clip aired between two tracks,
  not a live deck move — a promotion assessment should
  check for duplication against the existing stem /
  element-trading family before any META entry.
- Requires: stem cache on; cached stems for both tracks
  with tail alignment metadata; bar grids on both seam
  sides; a pair drain (pair-aware drains are DJ-mode
  personas only in the source). No bpm_delta_pct_max,
  camelot_max, phrase, or genre gating stated for the
  blend itself.
- Energy: delta not stated for the blend itself (the
  clip's level is whatever the render baked in, via the
  source's shared gain calculation). Exit: outgoing
  cues out at the blend start; the clip carries the
  incoming track's identity; incoming cues in past its
  pre-mixed head. Clash risk: none modeled — separation
  addresses stems only, not key, tempo, or vocal clash.
- Evidence reference: subwave README "Ending-aware
  transitions" + `docs/internals/broadcast.md` stem
  blends + `docs/concepts.md` stem cache, source subwave
  (https://github.com/perminder-klair/subwave, MIT).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from subwave. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
