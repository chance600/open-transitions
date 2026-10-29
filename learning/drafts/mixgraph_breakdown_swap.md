# DRAFT: mixgraph_breakdown_swap

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: mixgraph-guide (https://www.mixgraph.io/learn/dj-transition-techniques)
- License note: Public article — learn-from and link only; no license claimed
- Summary: Breakdown swap (MixGraph guide): start the incoming track's intro under an 8-16 bar open breakdown; the incoming beat drops as the breakdown resolves (needs >=8 bars of open space).

## When to use / when to avoid

See Applicability below (grounded in the source article, 2026-10-29).

## Evidence (mechanism confirmed)

Breakdown swap, verified first-hand 2026-10-29 against the
registered source (https://www.mixgraph.io/learn/dj-transition-techniques,
public article, learn-from and link only), section "The breakdown
swap": the outgoing track enters a long, open breakdown (8-16 bars
with minimal percussion); the incoming track's intro starts under
that breakdown, with its beat timed to drop at the moment the
breakdown feels resolved. The article frames it as the most musical
technique because it uses the structure of the music itself, and
states a minimum of 8 bars of open space — a 4-bar breakdown does
not give enough time to establish the incoming track.

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
  this technique; none is stated here.
- Key/harmonic situation: high harmonic compatibility — both
  tracks' melodic elements are audible during the breakdown, so
  the pair must align harmonically; the article states no Camelot
  numeric threshold, so none is asserted.
- Energy: matched energy between outgoing and incoming; the
  incoming beat is synced to drop as the outgoing breakdown
  resolves.
- Sections: outgoing track in a long, open breakdown of 8-16 bars
  with minimal percussion; incoming track's intro starts under
  that breakdown and its beat drops at the breakdown's resolution.
  At least 8 bars of open space is required.
- Vocals: the source gives no vocal guidance for the breakdown
  swap; no vocal applicability is claimed for this draft.
- Genre families: particularly effective in progressive house,
  melodic techno, and trance — genres built around long
  breakdowns, per the article.

Use-when: an outgoing track with a usable open breakdown of at
least 8 bars, an incoming intro available to start under it, high
harmonic compatibility, and matched energy.
Avoid-when: the tracks have no usable breakdowns, or the breakdown
is too short (the article: a 4-bar breakdown does not give enough
time to establish the incoming track); harmonic compatibility is
low, since both melodic elements are audible together.

## Registry fit

Mapping to the META schema (engine/meta.py), as a proposal for a
future META entry — not an entry itself.

- Preconditions (requires): outgoing track in an open breakdown
  of at least 8 bars with minimal percussion; incoming intro
  available to start under the breakdown; high harmonic
  compatibility; matched energy. camelot_max: unspecified — the
  source requires high harmonic compatibility but states no
  numeric threshold. vocal_ok: unspecified — the source gives no
  vocal guidance for this technique. genre_pair_ok: unspecified
  beyond the article's named effective families (progressive
  house, melodic techno, trance).
- Energy/exit profile: matched-energy handover; exit: seamless —
  the article describes the result as seamless, with the crowd
  barely noticing because the breakdown provides a natural gap.
  clash_risk: harmonic (both tracks' melodic elements are audible
  during the breakdown).
- Evidence reference: MixGraph, "DJ Transition Techniques: 7 Ways
  to Mix Between Tracks"
  (https://www.mixgraph.io/learn/dj-transition-techniques),
  section "The breakdown swap" confirmed first-hand 2026-10-29:
  incoming intro under an 8-16 bar open breakdown, incoming beat
  dropping as the breakdown resolves, minimum 8 bars of open
  space. Learn-from and link only.
