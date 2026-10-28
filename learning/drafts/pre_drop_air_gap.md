# DRAFT: pre_drop_air_gap

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: multiple public production guides (see Evidence)
- License note: public articles — learn-from and link only;
  creators retain rights
- Summary: Cut everything for a short, grid-aligned silence
  immediately before a downbeat return, so the return hits with
  maximum contrast. Length ladder from the sources: micro-gap
  1/16–1/4 beat; beat or half-beat cut; 1/4 bar or 1/8 note;
  up to one full beat as the standard cutout. The mechanism is
  contrast: loudness is relative, and a brief vacuum resets
  the ear (and the speakers) so the first transient of the
  return fills it completely. Transfers as a seam device placed
  exactly on the incoming track's downbeat.

## Evidence (mechanism confirmed)

- ProSonic Studios, "The Secret to Better Drops"
  (https://www.prosonic-studios.com/songcraft/articles/better-drops-and-tension):
  "Right before the first beat of the drop, leave a tiny window
  of absolute silence — anywhere from 1/16th to 1/4 of a beat.
  This 'breath' resets the listener's ear and creates a vacuum
  that the subsequent bass hit fills completely. Without this
  gap, the transition often feels blurred or 'muddy.'"
- EDM Templates, arrangement guide
  (https://edmtemplates.net/blogs/edm-templates-blog/arrangement-techniques),
  Rule #3 "Silence Creates Power": "Delete everything on the
  grid for the last 1/4 bar or 1/8th note before the drop.
  That tiny gap of pure silence resets the speakers and makes
  the first kick of the drop hit with maximum impact." Same
  source warns that cluttering the run-up with risers, white
  noise, and crashes "right up to the transient of the kick"
  makes the drop feel weak.
- RouteNote Create, "How to Create Impactful EDM Drops"
  (http://create.routenote.com/blog/how-to-create-impactful-edm-drops-5-top-tips/):
  "Drop Outs: Add a moment of silence or a 1/4 beat pause
  before the drop hits"; "Cut everything for a beat or
  half-beat. Let the tension hang for a split second."
- Methodic Truth, arrangement guide
  (https://methodictruth.com/arrangement), "The Cutout":
  "Drop everything for a beat ... Negative space IS a
  transition." Same source's cheapest-transition rule:
  "remove everything for one beat immediately before the new
  section starts. No riser, no fill, no crash. Silence."
- Convergent duration band across sources: a fraction of a
  beat to one beat for the standard device; up to one bar for
  the longer breath form (see tail_ring_breath for the
  tail-carried variant). No source supports a multi-second
  dead stop as a standard seam device — beyond ~1 bar with
  nothing sustaining, the gap stops reading as a breath (see
  Avoid when).

## Applicability (selector fields)

- Tempo: source gives no BPM cap; the gap is defined in beats/
  bars, so it scales with tempo. At very slow tempos a 1-beat
  gap is long in milliseconds — judge by ear, not by the clock.
- Key/harmonic: source gives no key applicability — the device
  is rhythmic/contrast-based, not harmonic. It does not fix a
  key clash and does not create one.
- Energy: the device NEEDS a tension peak before it. The gap
  is the held breath after a build, and the return is a step
  up. It is not an energy move by itself; it multiplies the
  return's energy by contrast.
- Sections: applies at section boundaries and downbeat returns
  (drop, chorus, new track's bar 1). It is a seam device, not
  a blend — it replaces overlap, it does not accompany it.
- Vocals: source gives no vocal gate, but a vocal line cut
  mid-phrase by the gap reads as an error; the gap must fall
  on a phrase boundary, never mid-word or mid-phrase.
- Genre families: source gives no genre restriction; attested
  in EDM/bass/techno production guides. In a continuous-groove
  context (unbroken dancefloor flow) it is a marked,
  attention-calling device, not a neutral default.
- Use when: the return has a full, clean first transient
  available; the outgoing side has built tension (riser,
  build, dense weave) so the silence reads as held breath;
  the seam falls exactly on the incoming downbeat; and the
  goal is contrast — a hard, clean arrival rather than a
  smooth blend.
- Avoid when: nothing has built tension before the gap (it
  reads as a dropout, a fault, or an ending); the gap lands
  off-grid or mid-phrase; the return is a blend or a
  continuous groove that the gap would break; the gap exceeds
  ~1 bar with nothing sustaining (it reads as an ending and
  the energy collapses rather than releasing); or the
  incoming transient is weak, masked, or cluttered by a
  riser/crash crossing into it (the contrast has nothing to
  multiply).

## Registry fit (META schema)

- Kind: seam/exit device (placement + exit), not a standalone
  render move — it sets the silence immediately before the
  host transition's return downbeat.
- Requires: a downbeat-aligned seam; a full-transient return
  on the incoming side; a tension peak on the outgoing side;
  phrase-boundary placement (no mid-phrase vocal cut).
  Parameter: gap length in beats (ladder: 1/16–1/4 beat micro,
  1/2–1 beat standard, up to 1 bar breath).
- Energy: tension peak → flat (gap) → step up at return.
  Exit: hard cut to full (the return downbeat).
  Clash risk: none of its own; it removes clash by removing
  overlap, but a mistimed gap creates a false-ending read.
- Evidence reference: ProSonic micro-gap; EDM Templates Rule
  #3; RouteNote drop-outs; Methodic Truth cutout (all public
  articles, learn-from only).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from public production guides (URLs in Evidence).
Learn-from and link only; no source prose copied verbatim
into the draft beyond short quoted mechanism lines with
attribution.
