# DRAFT: greed_cue_pointed_blend

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: greed-automix (https://adoomi.dev/blog/how-greed-automix-works)
- License note: Public article — learn-from and link only; no license claimed
- Summary: Cue-pointed blend length with filter envelopes (Greed automix write-up): the brain decides cue points, blend length, and filter timing; the DSP engine applies gain/filter envelopes.

## Evidence (mechanism confirmed)

Cue-pointed blend with filter envelopes, verified first-hand
2026-10-29 against the registered source
(https://adoomi.dev/blog/how-greed-automix-works, public
article, learn-from and link only): the article's design split
is explicit — "The TypeScript side is the brain. It decides
what plays next, how to transition, where the cue points are,
how long the blend is, and which filters run when. It never
touches audio" — while "The node is a DSP engine. It holds
two decks, mixes them, applies the gain and filter envelopes
it is told to, and makes no musical decisions at all." Cue
points come from structure, not arithmetic — mix-out at the
outro start, mix-in at the intro end — both snapped to the
phrase grid, not just the bar grid. Blend length is the outro
length rounded to whole phrases, capped at 32 seconds, then
shortened a phrase at a time while the two vocals would
overlap for more than four bars (a hard constraint, not a
score). Timing is armed, not fired live: the scheduler fires
four seconds early and tells the node where the cue is; the
node holds the fade and releases it on the first frame that
crosses the cue, with the incoming deck pre-rolled to a
downbeat in its own grid so the two grids line up (99.1% of
logged releases landed within 20 ms, i.e. within one frame).
Tempo handling is bounded: within 8% the incoming deck is
time-stretched to match and walks back to natural speed over
about eleven seconds after the fade; outside the window the
stretch is left off entirely. The mechanism is exactly the
queue summary's claim. Note the source is a Discord-bot
automix, not a live DJ set: the transfer is a planner/DSP
split plus render primitives, as the queue summary states.

## Applicability (selector fields)

- Tempo: within 8% of each other for the stretch to apply
  (outside it, no stretch — a slight drift over a few
  seconds is accepted instead); the analyzer folds half
  and double time into one octave (90–180 BPM corpus
  range) and the planner checks half and double time
  when comparing tempos.
- Key/harmonic: no key-compatibility gate is stated for
  the blend itself; harmony is 15% of the pair score.
  The article's own caveat applies: its key detector is
  biased (four Camelot cells hold 99% of its corpus),
  so its harmonic signal is weak evidence, not a gate.
- Energy: no energy-delta threshold is stated; energy
  is 15% of the pair score, and big energy jumps in
  either direction fire energy-rise/energy-release
  instead of a blend.
- Sections: outgoing outro x incoming intro alignment
  (outro-intro strategy), or the other shape-selected
  strategies (phrase-blend on a close tempo match,
  breakdown-drop for outgoing breakdown into incoming
  build, hard bass-swap when a tempo match has no outro
  to mix over). Both cue points must sit on the phrase
  grid.
- Vocals: blend length is shortened phrase by phrase
  while the two vocals would overlap for more than four
  bars — vocal overlap beyond four bars is a hard
  constraint, not a scored preference.
- Genre families: source states no genre gate; its
  corpus tempo peaks sit around pop, house, trap, and
  drum and bass, which describes the measured corpus,
  not a restriction on the blend.
- Use when: both tracks are analyzed (tempo, beat
  grid, bars/phrases, key, loudness, intro end, outro
  start, vocal positions), the pair scores above the
  minimum, an outro-intro or other shape-selected
  alignment exists, and phrase-grid cue points are
  available.
- Avoid when: the pair scores below the minimum (the
  article: below the minimum it "does not try to be
  clever and just plays the next song"); no outro
  exists to mix over (that case falls to the 4-second
  floor or the hard bass-swap strategy, not a
  cue-pointed blend); tempo gap exceeds 8% (stretch
  off, drift accepted); vocal overlap would exceed
  four bars after phrase-by-phrase shortening; only a
  bar grid is available (bar-only snapping landed
  transitions "halfway through a sentence").

## Registry fit (META schema)

- Kind: automix planner/DSP split (brain decides cue
  points, blend length, filter timing; engine applies
  gain/filter envelopes), not a live deck move — a
  promotion assessment should check for duplication
  against the existing blend and bass-swap families and
  against the sibling greed_phrase_boundary_bass_swap
  draft before any META entry.
- Requires: analyzed pair (tempo, beat grid, phrase
  grid, key, loudness, intro/outro boundaries, vocal
  positions); phrase-grid snapping; a 4-second pre-roll
  arming step with frame-crossing cue release; equal-power
  fade envelope by default; bass cut at 220 Hz and
  filter sweeps available as engine envelopes. No
  bpm_delta_pct_max, camelot_max, or genre gating is
  stated for the blend itself beyond the 8% stretch
  window.
- Energy: delta not thresholded for the blend itself
  (energy is 15% of the pair score; large jumps select
  other strategies). Exit: incoming enters under the
  outgoing at a matched level (gain trim from integrated
  loudness, clamped at ±6 dB); blend length is the
  outro length rounded to whole phrases, capped at
  32 s with a 4 s floor; incoming deck pre-rolled to a
  downbeat so grids align. Clash risk: vocal overlap
  hard-capped at four bars; key clash only weakly
  modeled (see the detector-bias caveat above).
- Evidence reference: Greed automix write-up
  (https://adoomi.dev/blog/how-greed-automix-works):
  "The split that came out of that is the most
  important design decision" (brain vs DSP engine),
  "Planning a transition" (phrase-grid snapping,
  blend-length rule, strategy table), "Landing on
  the beat" (4-second early fire, frame-crossing
  release), "Matching tempo" (8% stretch window).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from greed-automix. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
