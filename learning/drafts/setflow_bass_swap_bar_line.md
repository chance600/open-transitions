# DRAFT: setflow_bass_swap_bar_line

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: setflow-guide (https://www.setflow.app/blog/learn-dj-transitions-move-by-move)
- License note: Public article — learn-from and link only; no license claimed
- Summary: Bass swap on the bar line (SetFlow guide): incoming LOW fully down until the swap, then outgoing LOW out and incoming LOW in, in one move — never two basslines at full weight.

## When to use / when to avoid

See Applicability below (grounded in the source article, 2026-10-29).

## Evidence (mechanism confirmed)

Bass swap on the bar line, verified first-hand 2026-10-29 against
the registered source (https://www.setflow.app/blog/learn-dj-transitions-move-by-move,
public article, learn-from and link only): move 4 of the article's
five-move routine — "Swap the bass. On a bar line, turn the
outgoing LOW out and the incoming LOW in, in one move. Two
basslines at once turn to mud." Setup (move 1): incoming LOW
fully down, HI down a little, fader down, SYNC pressed. Timing
(FAQ): "On a bar line, usually where the outgoing track starts
winding down." Variant: when the incoming track has no bass until
its drop, keep the outgoing bass on and swap on the drop instead
of the planned bar line.

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from setflow-guide. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.

## Applicability

Grounded in the SetFlow article (read first-hand 2026-10-29); generic
descriptors only, no song, artist, or title named.

- Tempo: beat-matched pair (SYNC pressed during setup). The article
  gives no BPM range or maximum BPM delta; none is stated here.
- Key/harmonic situation: planned per pair from "whether the keys
  clash". Use when the pair's keys do not clash; the article states
  no Camelot-distance threshold, so none is asserted.
- Energy: outgoing track winding down at the swap; incoming track
  building toward its drop. Variant stated in the article: when the
  incoming track has no bass until its drop, keep the outgoing bass
  on and swap on the drop instead of the planned bar line.
- Sections: swap lands on a bar line, usually where the outgoing
  track starts winding down; incoming LOW held at kill from setup
  until the swap.
- Vocals: the source gives no vocal guidance; no vocal
  applicability is claimed for this draft.
- Genre families: house or techno blend (the article's own framing).

Use-when: a beat-matched house or techno pair with non-clashing keys,
an outgoing track winding down, and a bar line (or, per the article's
variant, the incoming drop) available as the single swap point.
Avoid-when: keys clash; the pair is not beat-matched; no bar-line
swap point or drop anchor is available; two basslines would run at
full weight together (the article: "two basslines at once turn to mud").

## Registry fit

Mapping to the META schema (engine/meta.py), as a proposal for a
future META entry — not an entry itself.

- Preconditions (requires): beat-matched pair; bar-line swap point
  (or incoming drop anchor per the article's variant); incoming LOW
  at kill until the swap. camelot_max: unspecified — the source only
  requires non-clashing keys, no numeric threshold. vocal_ok:
  unspecified — the source gives no vocal guidance. genre_pair_ok:
  same-family (house/techno) per the source framing.
- Energy/exit profile: lateral energy (outgoing winding down,
  incoming taking over at the swap); exit: seamless handover, the
  swap itself is the moment of transition; clash_risk: bass (the
  single-bassline-at-a-time rule is the move's core constraint).
- Evidence reference: SetFlow, "Learn DJ Transitions Move by Move"
  (https://www.setflow.app/blog/learn-dj-transitions-move-by-move),
  move 4 confirmed first-hand 2026-10-29: on a bar line, outgoing
  LOW out and incoming LOW in, in one move. Learn-from and link only.
