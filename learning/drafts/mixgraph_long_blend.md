# DRAFT: mixgraph_long_blend

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: mixgraph-guide (https://www.mixgraph.io/learn/dj-transition-techniques)
- License note: Public article — learn-from and link only; no license claimed
- Summary: Long blend, 16-32 bars (MixGraph guide): incoming in low during a rhythmic section, bass cut until the switch point, then a single clean bass swap; requires compatible keys and similar energy.

## When to use / when to avoid

See Applicability below (grounded in the source article, 2026-10-29).

## Evidence (mechanism confirmed)

Long blend, verified first-hand 2026-10-29 against the
registered source (https://www.mixgraph.io/learn/dj-transition-techniques,
public article, learn-from and link only), section "The long
blend": the incoming track enters at low volume during a
rhythmic section; over 16-32 bars its volume rises while the
outgoing track's falls, with a crossover period where both are
fully audible; the incoming track's bass stays cut until the
switch point, then bass swaps from outgoing to incoming in one
clean move — the article calls the bass swap the moment of
transition. It works when both tracks have high harmonic
compatibility (same or adjacent Camelot key) and similar energy,
and fails when keys are incompatible, energy levels are
dramatically different, or both tracks have prominent vocals.

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from mixgraph-guide. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.

## Applicability

Grounded in the MixGraph article (read first-hand 2026-10-29);
generic descriptors only, no song, artist, or title named.

- Tempo: the source gives no BPM range or maximum BPM delta for
  this technique; none is stated here. The article's chemistry
  profile requires high rhythmic compatibility.
- Key/harmonic situation: high harmonic compatibility — same or
  adjacent Camelot key. Both melodies are audible together for a
  long time, so a key clash is exposed for the full 16-32 bars.
- Energy: similar energy between outgoing and incoming; the
  article's chemistry profile is high harmonic, high rhythmic,
  similar energy.
- Sections: incoming track enters at low volume during a
  rhythmic section; overlap runs 16-32 bars with a crossover
  period where both tracks are fully audible; the bass swap is
  the switch point, after which the incoming track takes control.
- Vocals: avoid when both tracks have prominent vocals — a
  32-bar blend of two competing vocal hooks sounds chaotic, per
  the article. The article gives no safe vocal-overlap window of
  its own (it points to a separate vocal-mixing guide); none is
  asserted here.
- Genre families: the source names no specific genres for the
  long blend beyond framing it as bread-and-butter for
  same-genre mixing within compatible keys; no genre list is
  asserted here.

Use-when: a pair with high harmonic compatibility (same or
adjacent Camelot key), high rhythmic compatibility, and similar
energy, with a rhythmic section available for a 16-32 bar overlap
and a single clean bass swap at the switch point.
Avoid-when: keys are incompatible; energy levels are
dramatically different; or both tracks carry prominent vocals
(the article: shorten the blend or switch techniques instead).

## Registry fit

Mapping to the META schema (engine/meta.py), as a proposal for a
future META entry — not an entry itself.

- Preconditions (requires): high harmonic compatibility (same
  or adjacent Camelot key); high rhythmic compatibility; similar
  energy; a rhythmic section for the incoming track's low-volume
  entry; a 16-32 bar overlap window. camelot_max: unspecified
  numerically — the source requires same-or-adjacent Camelot
  keys but states no numeric threshold. vocal_ok: false when
  both tracks carry prominent vocals; otherwise unspecified —
  the source gives no safe vocal-overlap window of its own.
  genre_pair_ok: unspecified beyond the article's same-genre
  framing.
- Energy/exit profile: similar-energy handover; exit: seamless —
  the article describes the result as one continuous piece of
  music, the crowd hearing the music gradually evolving rather
  than two tracks. clash_risk: harmonic (both melodies audible
  together for the full overlap) and vocal (competing vocal
  hooks over a long blend).
- Evidence reference: MixGraph, "DJ Transition Techniques: 7 Ways
  to Mix Between Tracks"
  (https://www.mixgraph.io/learn/dj-transition-techniques),
  section "The long blend" confirmed first-hand 2026-10-29:
  incoming in low during a rhythmic section, 16-32 bar overlap,
  incoming bass cut until the switch point, one clean bass swap,
  requires same-or-adjacent Camelot keys and similar energy.
  Learn-from and link only.
