# DRAFT: setflow_five_move_blend

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: setflow-guide (https://www.setflow.app/blog/learn-dj-transitions-move-by-move)
- License note: Public article — learn-from and link only; no license claimed
- Summary: Five-move house/techno blend routine (SetFlow guide): set up incoming deck (LOW down), start on the downbeat, make room (HI up, outgoing MID dipped), swap bass on a bar line, fade out.

## Evidence (mechanism confirmed)

Five-move house/techno blend routine, verified first-hand
2026-10-29 against the registered source
(https://www.setflow.app/blog/learn-dj-transitions-move-by-move,
public article, learn-from and link only): "A transition is
five moves" — (1) Set up the incoming deck: cue the track,
turn its LOW fully down and its HI down a little, keep its
fader down, and press SYNC. (2) Start it on the downbeat:
press play on the first beat of a bar and ease the fader up.
(3) Make room: open the incoming HI back up as you go, and
dip the outgoing MID a little. (4) Swap the bass: on a bar
line, turn the outgoing LOW out and the incoming LOW in, in
one move ("Two basslines at once turn to mud"). (5) Fade out:
bring the outgoing fader down so the old track has gone a bar
after the new one's drop. Variant stated in the article: when
the incoming track has no bass until its drop, keep the
outgoing bass on and swap on the drop instead of the planned
bar line. The article uses a 16-bar blend as its example
length ("At full speed a 16-bar blend is over in half a…");
no "typical" length is asserted beyond that example.

## When to use / when to avoid

See Applicability below (grounded in the source article, 2026-10-29).

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
  The article uses a 16-bar blend as its example length.
- Key/harmonic situation: planned per pair from "whether the keys
  clash". Use when the pair's keys do not clash; the article states
  no Camelot-distance threshold, so none is asserted.
- Energy: outgoing track winding down at the swap; incoming track
  building toward its drop; outgoing fades out a bar after the
  incoming drop. Variant stated in the article: when the incoming
  track has no bass until its drop, keep the outgoing bass on and
  swap on the drop instead of the planned bar line.
- Sections: incoming starts on the first beat of a bar (downbeat);
  bass swap lands on a bar line; outgoing exits a bar after the
  incoming drop. The article's tutor example counts 8 bars to the
  drop; a 16-bar blend is the article's example length.
- Vocals: the source gives no vocal guidance; no vocal
  applicability is claimed for this draft.
- Genre families: house or techno blend (the article's own framing).

Use-when: a beat-matched house or techno pair with non-clashing keys,
an outgoing track winding down, and an incoming track with a clear
drop to hand over to, started on a downbeat with a bar-line bass swap.
Avoid-when: keys clash; the pair is not beat-matched; no bar-line
swap point or drop anchor is available; two basslines would run at
full weight together (the article: "two basslines at once turn to mud").

## Registry fit

Mapping to the META schema (engine/meta.py), as a proposal for a
future META entry — not an entry itself.

- Preconditions (requires): beat-matched pair; downbeat start;
  bar-line swap point; incoming drop anchor for the exit fade.
  Incoming LOW at kill until the swap, incoming HI slightly down at
  setup and opened during the blend, outgoing MID dipped while making
  room. camelot_max: unspecified — the source only requires
  non-clashing keys, no numeric threshold. vocal_ok: unspecified —
  the source gives no vocal guidance. genre_pair_ok: same-family
  (house/techno) per the source framing.
- Energy/exit profile: lateral energy (outgoing winding down,
  incoming rising to its drop); exit: seamless handover, outgoing
  gone a bar after the incoming drop; clash_risk: bass (the
  single-bassline-at-a-time rule is the move's core constraint).
- Evidence reference: SetFlow, "Learn DJ Transitions Move by Move"
  (https://www.setflow.app/blog/learn-dj-transitions-move-by-move),
  five moves confirmed first-hand 2026-10-29: setup (incoming LOW
  fully down, HI down a little, fader down, SYNC), start on the
  downbeat, make room (incoming HI up, outgoing MID dipped), swap
  bass on a bar line in one move, fade out a bar after the
  incoming drop. Learn-from and link only.
