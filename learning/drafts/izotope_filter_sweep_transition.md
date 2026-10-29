# DRAFT: izotope_filter_sweep_transition

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: izotope-guide (https://www.izotope.com/community/blog/how-to-create-better-transitions-in-your-mix)
- License note: Public article — learn-from and link only; no license claimed
- Summary: Automated filter sweep through a transition (iZotope guide): highpass EQ band automated 44 Hz -> 1320 Hz -> back to 44 Hz across the seam.

## When to use / when to avoid

See Applicability below (grounded in the source article, 2026-10-29).

## Evidence (mechanism confirmed)

Automated filter sweep through a transition, verified first-hand
2026-10-29 against the registered source
(https://www.izotope.com/community/blog/how-to-create-better-transitions-in-your-mix,
public article, learn-from and link only), section "Add filter
sweeps with Neutron": a basic highpass EQ band whose frequency is
automated over the transition, starting at 44 Hz, ramping up to
1320 Hz, then quickly back down to 44 Hz at the end of the
transition, applied in the article's example to a vocal-chop element
to give it a sense of change over time into the next section.
Note the framing: the article teaches section-to-section transitions
inside a mix/production, not deck-to-deck DJ transitions; the
mechanism transfers as an automation arc, not as a DJ-set claim.

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from izotope-guide. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.

## Applicability

Grounded in the iZotope article (read first-hand 2026-10-29);
generic descriptors only, no song, artist, or title named.

- Tempo: the source gives no tempo, BPM range, or maximum BPM
  delta; none is stated here.
- Key/harmonic situation: the source gives no key or harmonic
  guidance for this sweep; none is claimed here.
- Energy: the source frames the sweep as giving an element a sense
  of change over time into the next section; it states no energy
  delta or energy floor, so none is asserted.
- Sections: a transition between sections inside a mix, with the
  sweep arc running across the seam (44 Hz up to 1320 Hz, then
  quickly back to 44 Hz in the article's example values).
- Vocals: the article's example applies the sweep to a vocal-chop
  element; no broader vocal rule (vocal-free, background, hook, or
  iconic) is stated in the source, so none is claimed.
- Genre families: the source is a general mixing/production article
  and names no genre family for this sweep; none is claimed here.

Use-when: a section-to-section transition where an element needs a
sense of change over time across the seam, with an automatable
highpass EQ band available for the sweep arc.
Avoid-when: the source states no avoid case for this sweep, so none
is claimed here rather than invented.

## Registry fit

Mapping to the META schema (engine/meta.py), as a proposal for a
future META entry — not an entry itself.

- Preconditions (requires): a section-boundary transition; an
  automatable highpass EQ band. camelot_max: unspecified — the
  source gives no harmonic guidance. vocal_ok: unspecified — the
  source's only vocal mention is the vocal-chop example, not a
  vocal-state rule. genre_pair_ok: unspecified — the source names
  no genre family for this sweep.
- Energy/exit profile: change-over-time arc across the seam (the
  article's stated effect); exit: seamless as a proposal mapping,
  not a source claim. clash_risk: unspecified — the source makes
  no clash claim for this sweep.
- Evidence reference: iZotope, "How to Create Better Transitions
  in Your Mix"
  (https://www.izotope.com/community/blog/how-to-create-better-transitions-in-your-mix),
  section "Add filter sweeps with Neutron" confirmed first-hand
  2026-10-29: highpass EQ band automated 44 Hz -> 1320 Hz -> back
  to 44 Hz across the transition. Learn-from and link only.
