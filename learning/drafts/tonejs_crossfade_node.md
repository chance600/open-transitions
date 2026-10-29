# DRAFT: tonejs_crossfade_node

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: tonejs (https://github.com/Tonejs/Tone.js)
- License note: MIT
- Summary: CrossFade node (Tone/component/channel/CrossFade.ts): equal-power crossfade between two audio inputs in the browser. Feedback-delay candidate DROPPED (paths unverified).

## Evidence (mechanism confirmed)

Equal-power two-input crossfade, verified first-hand
2026-10-29 against a shallow sparse clone of the registered
source (https://github.com/Tonejs/Tone.js, MIT):
`Tone/component/channel/CrossFade.ts` documents "Tone.Crossfade
provides equal power fading between two inputs", implemented
via a StereoPannerNode splitting the fade control into two
gains. Inputs are `a` (full level when fade = 0) and `b`
(full level when fade = 1), driven by a single `fade`
parameter (NormalRange, 0-1). The mechanism is exactly the
queue summary's claim. No correction to the summary was
needed. Note the source is a web-audio component, not a DJ
transition: its output is a gain crossfade between two
inputs, not a deck move with tempo/key/energy gating.

## Applicability (selector fields)

- Tempo: source gives no tempo applicability (the node is
  tempo-agnostic; no BPM gate is stated).
- Key/harmonic: source gives no key applicability.
- Energy: source gives no energy applicability.
- Sections: source gives no song-section applicability.
- Vocals: source gives no vocal applicability.
- Genre families: source gives no genre applicability (a
  browser audio node, genre-agnostic by construction).
- Use when: a two-input crossfade in a browser/web-audio
  context is wanted, with a single 0-1 fade control driving
  both gains.
- Avoid when: a DJ-set render move with tempo/key/energy
  gating is required (the node itself carries no such
  gating); a live-deck move is required (the source is a
  web-audio component, not deck hardware or DJ software);
  more than two inputs must be faded at once (the node has
  exactly two inputs, a and b).

## Registry fit (META schema)

- Kind: render primitive / curve family for a two-input
  equal-power crossfade, not itself a standalone named DJ
  technique with its own exit profile — a promotion
  assessment should check for duplication against the
  existing crossfade/eq_blend family before any META entry.
- Requires: two audio inputs and a fade parameter in 0-1;
  no bpm_delta_pct_max, camelot_max, phrase, or genre
  gating stated for the node itself.
- Energy: delta 0 for the node itself (energy profile
  belongs to the transition that consumes it, not to the
  crossfade). Exit: fade completes at fade = 1 with input b
  at full level. Clash risk: none modeled — the node
  applies no key, tempo, or vocal gating.
- Evidence reference: tonejs
  `Tone/component/channel/CrossFade.ts` (equal-power
  fading between two inputs; a full at fade = 0, b full at
  fade = 1), source tonejs
  (https://github.com/Tonejs/Tone.js, MIT).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from tonejs. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
