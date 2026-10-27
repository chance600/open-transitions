# DRAFT: symmetric_geometric_beatmatch

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: auto-dj-ai (https://github.com/caffettino87/auto-dj-ai)
- License note: MIT
- Summary: Both decks meet at the geometric-mean tempo, each bending half the octave-folded BPM difference, with no stretch outside a +/-6% tolerance; transfers as a beatmatch mode with a tolerance parameter and a no-stretch fallback.

## Evidence (mechanism confirmed)

auto-dj-ai `src/player.js` `matchRatesSymmetric`, verified
first-hand 2026-10-27. The code comment states it verbatim:
"the two tracks meet at the geometric-mean tempo, each bending
half the (octave-folded) difference. Outside tolerance, neither
is stretched." TEMPO_TOLERANCE 0.06; octave folding at ratio
thresholds 1.41 / 0.71; meeting rate via sqrt(ratio), outgoing
bends one way, incoming the other. Evidence path:
`auto-dj-ai/src/player.js` (survey: STAR-DEEP-CANDIDATES
`symmetric_geometric_beatmatch`).

## Applicability (selector fields)

- Tempo: this IS the tempo matcher. Use when the octave-folded
  BPM ratio is within ±6% — outside tolerance neither deck is
  stretched and beatmatch is disabled (no-change returned).
  Avoid when either BPM is unmeasured (returns no-change).
- Key / energy / sections / vocals / genre: source gives no
  applicability.

## Registry fit (META schema)

- Kind: selector (beatmatch mode, not a render).
- Requires: needs measured BPM on both sides. Outputs
  fromRate / toRate.
- Energy / exit / clash risk: N/A — it sets rates, no audio.
- Evidence reference: auto-dj-ai `player.js` (MIT).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from auto-dj-ai. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
