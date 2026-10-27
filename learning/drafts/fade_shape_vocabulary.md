# DRAFT: fade_shape_vocabulary

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: djtransgan (https://github.com/ChenPaulYu/DJtransGAN)
- License note: MIT
- Summary: Five named fade shapes (linear, exponential, logarithmic, quarter-sine, half-sine) x fade-in/fade-out; transfers directly as the curve-shape parameter of every technique in the registry.

## Evidence (mechanism confirmed)

DJtransGAN `djtransgan/mixer/transform.py`, verified first-hand
2026-10-27: `choose_fade_shape` defines exactly five shapes —
linear, exponential, logarithmic, quarter-sine, half-sine — and
`fade_transform` applies a chosen shape to fade-in (`fi`, curve
as-is) and fade-out (`fo`, curve reversed). The five-shape x
fade-in/fade-out vocabulary in the summary matches the code
exactly. Evidence path: `DJtransGAN/djtransgan/mixer/transform.py`
(survey: STAR-DEEP-CANDIDATES `fade_shape_vocabulary`).

## Applicability (selector fields)

- Tempo: source gives no BPM-gap cap for the curve shapes
  themselves; shapes parameterize a fade of any length.
- Key/harmonic: source gives no key applicability — a curve
  shape does not change harmonic compatibility.
- Energy: source gives no energy applicability. Use when a fade
  is the chosen move and its curve needs shaping; the shape
  choice is a curve parameter, not an energy decision.
- Sections: source gives no section applicability.
- Vocals: source gives no vocal applicability — shapes do not
  gate on vocals.
- Genre families: source gives no genre applicability.
- Use when: any fade-based technique needs a named curve shape
  (fade-in or fade-out) as a parameter.
- Avoid when: the move is not a fade (cuts, drops, and other
  non-fade moves take no curve-shape parameter).

## Registry fit (META schema)

- Kind: parameter (curve-shape parameter carried by every
  fade-based registry technique), not a standalone render move.
- Requires: a fade-based technique to parameterize; no stems,
  vocal, or phrase precondition of its own.
- Energy: delta 0, tension flat (a shape parameter, not an
  energy move). Exit: seamless (as the host fade's exit).
  Clash risk: none of its own.
- Evidence reference: DJtransGAN `transform.py` (MIT).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from djtransgan. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
