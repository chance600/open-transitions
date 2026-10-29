# DRAFT: greed_phrase_boundary_bass_swap

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: greed-automix (https://adoomi.dev/blog/how-greed-automix-works)
- License note: Public article — learn-from and link only; no license claimed
- Summary: Phrase-boundary blend with mid-blend bass swap (Greed automix write-up): next track enters under the current one, in time, at matched level, on a phrase boundary, bass swapping partway through.

## Evidence (mechanism confirmed)

Phrase-boundary blend with mid-blend bass swap, verified
first-hand 2026-10-29 against the registered source
(https://adoomi.dev/blog/how-greed-automix-works, public
article, learn-from and link only): the article's opening
states the automix behaviour verbatim in substance — "the
next track comes in under the current one, in time, at a
matched level, on a phrase boundary, and the bass of one
swaps for the other partway through." The bass-swap
mechanism is a per-deck bass cut, `x - (1 - gain) *
lowpass(x)` at 220 Hz: the outgoing track loses its bass
at the same moment the incoming one gains it, "so two
kick drums never fight." Cue points come from structure,
not arithmetic — mix-out at the outro start, mix-in at
the intro end — and both are snapped to the phrase grid,
not just the bar grid ("the single biggest improvement
in how transitions sound"). Blend length is the outro
length rounded to whole phrases, capped at 32 seconds,
then shortened a phrase at a time while the two vocals
would overlap for more than four bars — a hard constraint,
not a score. Strategy selection from the pair's shape: a
close tempo match gets a `phrase-blend`; an outgoing
breakdown into an incoming build gets a `breakdown-drop`,
where the bass swap comes late; a tempo match with no
outro to mix over gets a fast, hard `bass-swap` (fixed
4 seconds by design). The mechanism is exactly the queue
summary's claim. Note the source is a Discord-bot
automix, not a live DJ set: the transfer is a selector
strategy plus render primitives, as the queue summary
states.

## Applicability (selector fields)

- Tempo: no numeric BPM gate is stated for the blend
  itself; the firing condition is a close tempo match
  (phrase-blend), and the analyzer folds half/double
  time into one octave with the planner checking half
  and double time as well.
- Key/harmonic: no key-compatibility requirement is
  stated for the blend itself; harmony is 15% of the
  pair score. The article's own caveat applies: its key
  detector is biased (four Camelot cells hold 99% of
  its corpus), so its harmonic signal is weak evidence,
  not a gate.
- Energy: no energy-delta threshold is stated; energy
  is 15% of the pair score, and big energy jumps in
  either direction fire `energy-rise`/`energy-release`
  instead of a phrase-blend. Phrase-blend runs longest
  (median 12.5 s in the article's corpus) because it
  only fires when the tempos already agree.
- Sections: outgoing outro x incoming intro alignment
  (outro-intro strategy), or an outgoing breakdown into
  an incoming build (breakdown-drop). Both cue points
  must sit on the phrase grid.
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
  start, vocal positions), tempos closely match, an
  outro-intro alignment or breakdown-build shape is
  present, and phrase-grid cue points are available.
- Avoid when: the pair scores below the minimum (the
  article: below the minimum it "does not try to be
  clever and just plays the next song"); vocal overlap
  would exceed four bars after phrase-by-phrase
  shortening; only a bar grid is available (bar-only
  snapping landed transitions "halfway through a
  sentence"); no outro/intro shape exists (that case
  fires the hard bass-swap strategy, not this blend).

## Registry fit (META schema)

- Kind: automix selector strategy (phrase-blend) plus
  render primitives (equal-power envelope, 220 Hz bass
  cut), not a live deck move — a promotion assessment
  should check for duplication against the existing
  bass-swap and blend families before any META entry.
- Requires: analyzed pair (tempo, beat grid, phrase
  grid, key, loudness, intro/outro boundaries, vocal
  positions); phrase-grid snapping; equal-power fade
  envelope by default; bass cut at 220 Hz on both
  decks. No bpm_delta_pct_max, camelot_max, or genre
  gating is stated for the blend itself.
- Energy: delta not thresholded for the blend itself
  (energy is 15% of the pair score; large jumps select
  other strategies). Exit: incoming enters under the
  outgoing at a matched level (gain trim from
  integrated loudness, clamped at ±6 dB); bass swaps
  partway through (late in breakdown-drop, fixed 4 s
  in the hard bass-swap variant); blend length is the
  outro length rounded to whole phrases, capped at
  32 s. Clash risk: vocal overlap is hard-capped at
  four bars; key clash is only weakly modeled (see
  the detector-bias caveat above).
- Evidence reference: Greed automix write-up
  (https://adoomi.dev/blog/how-greed-automix-works):
  opening behaviour statement, "Two decks, one
  encoder" (bass cut + swap), "Planning a transition"
  (phrase-grid snapping, blend-length rule, strategy
  table).

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
