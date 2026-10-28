# DRAFT: tail_ring_breath

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: multiple public production guides (see Evidence)
- License note: public articles — learn-from and link only;
  creators retain rights
- Summary: Instead of a pure digital cut, let a reverb or delay
  tail from the outgoing side's last element ring into the gap
  and decay toward silence before the return downbeat — or
  strip the arrangement to a single sustaining element (vocal,
  tail) for up to a bar, then re-enter hard. The tail is the
  continuity thread: it tells the ear the silence is composed,
  not a fault, while the arrangement still empties. The tail
  must decay to near-silence BEFORE the return transient, or
  it muddies the very contrast the gap exists to create.
  Transfers as the tail-carried variant of the air-gap family.

## Evidence (mechanism confirmed)

- Methodic Truth, arrangement guide
  (https://methodictruth.com/arrangement), "The Cutout":
  "Drop everything for a beat — or throw a big reverb/delay
  tail on the last word and let it ring into silence.
  Negative space IS a transition." The same source frames the
  tail as the alternative that keeps the cutout readable:
  pure cut OR tail-ring, same device family.
- BrahmStorm, Suno silence prompts
  (https://brahmstorm.com/blog/suno-silence-prompts-how-to-make-space-work-in-your-tracks/):
  "[full band drops to vocal only, no instruments] [1 bar,
  then full band re-enters hard on the chorus]" — the
  strip-to-one-element breath at one-bar scale, with a hard
  re-entry. The same source notes that "spacious" (reverb and
  room tone) is the OPPOSITE of silence — so a tail-ring
  breath is a distinct choice from pure silence, not a
  synonym: the tail must be a decaying remnant, not a
  sustained wash.
- LyricAssistant, electro-industrial arrangement
  (https://lyricassistant.com/how-to-write-electro-industrial-songs/):
  "Do not be afraid to remove everything for several bars
  then return with more teeth" and "Silence before a drop is
  a weapon. The absence of sound makes the return heavier."
  This attests the longer breath scale, with the return
  carrying the payoff — but note the multi-bar form is
  attested as a song-section device, not as a standard
  between-songs seam; see Avoid when.
- Contrast mechanism shared with pre_drop_air_gap (ProSonic
  vacuum/ear-reset; EDM Templates "silence creates power"):
  the tail does not replace the contrast, it frames it. If
  the tail is still loud at the return downbeat, the contrast
  is gone and the device fails on its own terms.

## Applicability (selector fields)

- Tempo: source gives no BPM cap; the tail's decay time is
  the binding constraint, not tempo — the gap must be at
  least as long as the tail's audible decay, or the tail
  collides with the return.
- Key/harmonic: source gives no key applicability. A tail
  carries the outgoing side's harmony as it decays; if that
  harmony clashes with the return's first chord, the tail
  advertises the clash instead of hiding it — prefer a
  neutral tail (noise/reverb wash, single non-chord tone)
  when the return key is distant.
- Energy: like the air gap, needs a tension peak before it.
  The tail softens the energy floor during the gap (less
  stark than pure silence), so the return step-up is slightly
  smaller but the continuity is higher.
- Sections: applies at section boundaries and downbeat
  returns, especially where pure silence would read as a
  fault — mid-weave seams, high-continuity contexts, and
  vocal-led exits where the last word deserves a trail.
- Vocals: the tail's natural home — a vocal last word with
  a reverb/delay throw is the canonical tail source. Avoid
  tailing a vocal that is still delivering lyric content
  into the gap (the words smear); tail only the final word
  or phrase ending.
- Genre families: source gives no genre restriction; attested
  in EDM arrangement guides and song-section writing. The
  longer (multi-bar) breath form belongs to song sections,
  not to between-songs seams.
- Use when: pure silence would read as a technical fault
  (dense weave, high-continuity context); the outgoing side
  has a strong last element worth trailing (vocal, lead);
  the tail can decay to near-silence before the return
  downbeat; or the gap needs to run to a full bar and a
  sustaining element is required to hold it.
- Avoid when: the tail cannot decay before the return
  (decay longer than the gap — it muddies the transient);
  the tail's harmony clashes with the return's first chord;
  the goal is maximum stark contrast (pure cut beats tail
  there); or the gap is meant to run multi-bar between songs
  (that is a song-section device, and between songs it reads
  as an ending, not a breath).

## Registry fit (META schema)

- Kind: seam/exit device (tail-carried variant of the air-gap
  family), not a standalone render move — it shapes the
  outgoing side's decay into the host transition's return.
- Requires: a tail source on the outgoing side (reverb/delay
  throw or single sustaining element); tail decay time
  shorter than the gap; a downbeat-aligned return; phrase-
  boundary placement. Parameters: gap length in beats/bars;
  tail decay time; tail level at return (must be near
  silence).
- Energy: tension peak → decaying tail (falling floor) →
  step up at return. Exit: hard return on the downbeat, with
  the tail already spent. Clash risk: tail harmony vs return
  chord (see Avoid when); tail-vs-transient masking if the
  decay overruns the gap.
- Evidence reference: Methodic Truth cutout (tail-ring
  variant); BrahmStorm strip-to-one-element bar; LyricAssistant
  multi-bar breath (section device, flagged as such).

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
