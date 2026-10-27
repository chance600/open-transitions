# DRAFT: sub_bass_crossover_swap

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: null-set-ai-dj (https://github.com/sanchitd5/null-set-ai-dj)
- License note: MIT
- Summary: 4th-order Linkwitz-Riley split at 120 Hz where exactly one track's low band is present at any sample while mids/highs blend; transfers as the render primitive for the whole bass-swap family.

## Evidence (mechanism confirmed)

null-set-ai-dj `app/music_brain/audio/dsp_rack.py`, verified
first-hand 2026-10-27: "a strict 4th-order Linkwitz-Riley
120Hz sub-bass crossover (for zero-overlap Bass Swaps)";
`linkwitz_riley_split` cascades two 2nd-order Butterworth
stages to 4th-order; the mix docstring states sub-bass
ownership "snaps instantly at swap_sample: exactly one track's
low band is present" while mids/highs blend. Evidence path:
`null-set-ai-dj/app/music_brain/audio/dsp_rack.py` (survey:
STAR-DEEP-CANDIDATES `sub_bass_crossover_swap`).

## Applicability (selector fields)

- Tempo / key / energy / sections / vocals / genre: source
  gives no applicability beyond the crossover itself. The
  primitive is signal-level: it enforces single low-band
  ownership at the swap sample regardless of pair features.
- Use when a bass swap needs zero-overlap sub-bass (the
  primitive guarantees it by construction). Avoid as a complete
  transition: it is a render primitive for the bass-swap
  family, not a standalone technique — mids/highs blend
  separately.

## Registry fit (META schema)

- Kind: render (primitive).
- Requires: needs audio-rate implementation (4th-order LR at
  120 Hz). No pair-feature gating stated.
- Energy: delta 0, tension flat. Exit: snap. Clash risk: bass
  (eliminated by construction below the crossover).
- Evidence reference: null-set-ai-dj `dsp_rack.py` (MIT).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from null-set-ai-dj. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
