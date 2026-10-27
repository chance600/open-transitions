# DRAFT: brute_force_alignment_search

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: automix (https://github.com/MZehren/Automix)
- License note: MIT
- Summary: Every combination of outgoing boundary x incoming boundary x bar-overlap is rendered and graded and the best-scoring alignment wins; transfers as a selector that searches cue-point pairs rather than scoring one fixed exit/entry point.

## Parameters (to be specified by the implementer)

- (fill in: named parameters with defaults and ranges)

## When to use / when to avoid (to be specified)

- Use when: (fill in, grounded in evidence, not invented)
- Avoid when: (fill in)

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from automix. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.

## Applicability (evidence-grounded, selector fields)

Mechanism confirmed first-hand in source: `automix/transition/ruleDriven.py`
`generateMix` — `itertools.product` over outgoing boundaries × incoming
boundaries × bar-overlaps (default `[8]`), each alignment rendered via
`generateFX` and graded by `rules.runAll`, best grade kept. Boundaries are
`track.features["selectedPeaks"].times`; incoming track is synchronized to
the outgoing tempo before grading.

- Tempo: use when the pair synchronizes with playrate change under 5%
  (full score in `maxPlayrateChangeRule`); score decays to 0 at 20% change.
  Avoid when tempo sync would need a playrate change at or above 20%.
- Key/harmonic situation: use when the graded rules can discriminate —
  the source grades harmonic transition, percussive fit, and suitable key
  per alignment. No key-distance cutoff is stated in the source; none is
  claimed here.
- Energy: not specified by the source; no energy claim made.
- Sections: use at detected segment boundaries only — switch points come
  exclusively from the `selectedPeaks` boundary lists. Avoid mid-segment
  switches: the search cannot place one.
- Vocals: not specified by the source's grading rules; no vocal claim made.
- Genre families: not specified by the source (rules are genre-agnostic);
  no genre restriction claimed.
- Avoid when: either side yields too few boundaries for the product to
  search (a single boundary collapses the search to one alignment), or
  boundary/peak detection is unreliable on either track.

## Registry fit (META schema mapping)

- Preconditions: both tracks carry `selectedPeaks` boundary times plus
  beat/tempo features; incoming track synchronizable to outgoing tempo.
- `requires`: `bpm_delta_pct_max` graded, not binary — full score ≤5%
  playrate change, 0 at ≥20% (`maxPlayrateChangeRule`); `camelot_max`,
  `vocal_ok`, `phrase_a_ok`, `genre_pair_ok` unset (source states no
  cutoffs; to be fixed by the implementer from the graded rules, not
  guessed here); `needs`: [] (no stems; operates on track audio +
  extracted features).
- Energy/exit profile: `energy.delta` 0, `tension` flat (overlap blend, no
  built-in lift or drop); `exit`: seamless; `clash_risk`: key + percussive
  (the two graded fit rules).
- `params`: `barOverlaps` (source default `[8]`, unit bars); boundary lists
  from `selectedPeaks`.
- Evidence reference: MZehren/Automix (MIT),
  `automix/transition/ruleDriven.py` `generateMix`,
  `automix/rules/maxPlayrateChangeRule.py`; STAR survey 2026-10-26.
