# DRAFT: fit_downgrade_ladder

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: rustlarpdj (https://github.com/T-Perm/RustLarpDJ)
- License note: license unconfirmed - learn-from only, no code reuse
- Summary: Each style fit to available seconds before selection: phrase quantize downgrades to bar, then to a 4-beat minimum, then a 0.05x score multiplier; transfers as a feasibility step so long blends degrade gracefully instead of collapsing into cuts.

## Evidence (mechanism confirmed)

RustLarpDJ `crates/ai/src/transition_style.rs` `fit()`,
verified first-hand 2026-10-27: cost model (None 0 beats, Bar
4 beats, Phrase 32 beats); Phrase quantize downgrades to Bar;
MIN_BEATS 4.0; when even the minimum does not fit, a 0.05 score
multiplier; duration jitter ±15% (JITTER_FRACTION 0.15).
Evidence path: `RustLarpDJ/crates/ai/src/transition_style.rs`
(survey: STAR-DEEP-CANDIDATES `fit_downgrade_ladder`).

## Applicability (selector fields)

- Tempo: beat-anchored; available seconds are computed from the
  effective BPM. Use for any style whose base duration exceeds
  the available overlap — the ladder is the feasibility path
  that keeps long blends degrading gracefully instead of
  collapsing into cuts.
- Key / energy / sections / vocals / genre: source gives no
  applicability (feasibility here is duration-only).
- Avoid as a quality claim: a 0.05-multiplied pick is a degraded
  fallback, not a preferred pick — the multiplier exists to
  demote it.

## Registry fit (META schema)

- Kind: selector (feasibility step, not a render).
- Requires: needs available seconds plus effective BPM.
  Outputs fitted beats, fitted quantize, and multiplier.
- Energy / exit / clash risk: N/A — it sizes a pick, no audio.
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
