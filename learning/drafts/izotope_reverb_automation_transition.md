# DRAFT: izotope_reverb_automation_transition

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: izotope-guide (https://www.izotope.com/community/blog/how-to-create-better-transitions-in-your-mix)
- License note: Public article — learn-from and link only; no license claimed
- Summary: Reverb wet/dry automation across a seam (iZotope guide): Neoverb wet/dry ridden over time to create movement through the transition.

## When to use / when to avoid

See Applicability below (grounded in the source article, 2026-10-29).

## Evidence (mechanism confirmed)

Reverb wet/dry automation across a seam, verified first-hand
2026-10-29 against the registered source
(https://www.izotope.com/community/blog/how-to-create-better-transitions-in-your-mix,
public article, learn-from and link only), section "Automate
reverb with Neoverb": the Neoverb wet/dry slider adjusted over
time to create a sense of movement in a vocal-chop element across
a transition. Note the framing: the article teaches
section-to-section transitions inside a mix/production, not
deck-to-deck DJ transitions; the mechanism transfers as an
automation arc, not as a DJ-set claim.

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
  guidance for this reverb automation; none is claimed here.
- Energy: the source frames the automation as creating a sense
  of movement across the transition; it states no energy delta
  or energy floor, so none is asserted.
- Sections: a transition between sections inside a mix, with the
  wet/dry automation ridden across the seam.
- Vocals: the article's example applies the automation to a
  vocal-chop element; no broader vocal rule (vocal-free,
  background, hook, or iconic) is stated in the source, so none
  is claimed.
- Genre families: the source is a general mixing/production
  article and names no genre family for this automation; none is
  claimed here.

Use-when: a section-to-section transition where an element needs
a sense of movement across the seam, with an automatable reverb
wet/dry control available.
Avoid-when: the source states no avoid case for this automation,
so none is claimed here rather than invented.

## Registry fit

Mapping to the META schema (engine/meta.py), as a proposal for a
future META entry — not an entry itself.

- Preconditions (requires): a section-boundary transition; an
  automatable reverb wet/dry control. camelot_max: unspecified —
  the source gives no harmonic guidance. vocal_ok: unspecified —
  the source's only vocal mention is the vocal-chop example, not a
  vocal-state rule. genre_pair_ok: unspecified — the source names
  no genre family for this automation.
- Energy/exit profile: movement arc across the seam (the
  article's stated effect); exit: seamless as a proposal mapping,
  not a source claim. clash_risk: unspecified — the source makes
  no clash claim for this automation.
- Evidence reference: iZotope, "How to Create Better Transitions
  in Your Mix"
  (https://www.izotope.com/community/blog/how-to-create-better-transitions-in-your-mix),
  section "Automate reverb with Neoverb" confirmed first-hand
  2026-10-29: Neoverb wet/dry slider adjusted over time to create
  a sense of movement across the transition. Learn-from and link
  only.
