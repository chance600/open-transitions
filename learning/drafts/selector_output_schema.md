# DRAFT: selector_output_schema

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: rustlarpdj (https://github.com/T-Perm/RustLarpDJ)
- License note: license unconfirmed — learn-from only, no code reuse
- Summary: Richer selector output: duration_beats, quantize level, curve, fallback duration, reason string, transition-type class, vocal-clash risk, conflict-only EQ plan (from the STAR survey top-5, 2026-10-26). Learn-from only.

## Evidence (mechanism confirmed, composite)

RustLarpDJ `crates/ai/src/transition_style.rs`
`TransitionPlan`, verified first-hand 2026-10-27: style,
duration_beats, fallback_duration, quantize, curve, wordplay,
label, reason. Composite note, stated plainly: the draft's
extra fields trace to the other sources named in the survey
top-5, not to this struct alone — transition-type class to
Automix's transition-type classifier (survey §3), vocal-clash
risk to RustLarpDJ `vocal_clash.rs`, conflict-only EQ plan to
auto-dj-ai's `bandClash` plus clash-scaled cuts. Evidence path:
`RustLarpDJ/crates/ai/src/transition_style.rs` + survey top-5
composite note (survey: STAR-REPOS-SURVEY §2 top-5
`selector_output_schema`).

## Applicability (selector fields)

- Tempo / key / energy / sections / vocals / genre: the schema
  carries fields for the pair's structure (duration, quantize,
  curve, reason string) rather than gating on any one field.
  Use as the output contract for every selector pick — it is
  field-level, not pair-level. Avoid treating the schema as a
  technique: it outputs a plan; it does not render.

## Registry fit (META schema)

- Kind: selector (output schema, not a render).
- Requires: needs a chosen style plus fitted
  duration / quantize / curve. Maps to META requires via the
  plan's fields.
- Energy / exit / clash risk: per chosen style, not per
  schema.
- Evidence reference: RustLarpDJ `transition_style.rs`
  (learn-only, license unconfirmed) + Automix + auto-dj-ai per
  the survey composite note.

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
