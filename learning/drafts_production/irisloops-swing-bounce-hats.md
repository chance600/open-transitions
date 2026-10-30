# DRAFT: irisloops-swing-bounce-hats

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: ig:irisloops_ (instagram.com/irisloops_) (https://www.instagram.com/reel/DfGGO1htP4U/)
- License note: Public Instagram post — learn-from and link only; creator retains rights
- Summary: Tech-house bounce from hat swing at 125 BPM: kick straight on every beat, hats on every sixteenth, every second sixteenth delayed (start mid-50s percent, raise to around 60 percent; video demos 55 percent then 62 percent, straight 50 percent vs swung 62 percent A/B); only hats and percussion swing; off-beat hats slightly lower in level. Evidence: creator own written breakdown on own account plus matching video demo, with independent MPC/DAW percent-convention corroboration (50 percent = straight). OPEN: whether the bass also swings is unanswered (commenter asked, reel names hats/percussion only) — do not assert it. Counterpoint carried: straight timing works sometimes too; swing is a choice for bounce, not a law.

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from ig:irisloops_ (instagram.com/irisloops_). If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.

## Applicability (selector fields, grounded in the source)

- Tempo: 125 BPM tech-house groove (the reel's demonstrated tempo).
- Key/harmonic situation: not specified by the source — no key or harmonic claim is made here.
- Energy: grooves that read stiff or robotic at straight timing and need bounce; a feel move, not an energy lift.
- Sections: a 16-step bar with kick on every beat and hats on every sixteenth; the swing applies to the hat/percussion layer only.
- Vocals: not addressed by the source — no vocal claim is made here.
- Genre families: tech house (house family).
- Use when: a tech-house groove at around 125 BPM needs bounce; hats/percussion sit on sixteenths under a straight kick; straight timing reads stiff.
- Avoid when: straight timing is the intent (the source's own counterpoint: straight works sometimes too — swing is a choice, not a law); never swing the kick (source constraint: kick stays straight like a clock); never assume the bass swings (the source names hats/percussion only — bass treatment is open, not asserted); never compare swing percentages across DAW conventions (MPC-style 50% = straight vs Cubase/FL-style 0% = straight).

## Registry fit

- META preconditions: 16-step bar; straight kick on every beat; hats on every sixteenth; swing parameter starting mid-50s percent and raised to around 60 percent (MPC-style convention, 50% = straight; video demos 55% then 62%); off-beat hats slightly lower in level; kick excluded from swing; bass excluded (unspecified).
- Energy/exit profile: production groove technique, not a transition — it carries no transition exit profile. Its effect is feel (bounce via deliberate high-band timing irregularity), and it maps to groove-density reading (swung hats are signal, not drift) rather than to a transition META entry. Promotion still requires a human PASS/heart plus a clean demo heard by a human.
- Evidence reference: creator's own written breakdown on the creator's own account plus matching video A/B demo (straight 50% labeled ROBOT vs swung 62% labeled BOUNCE) at https://www.instagram.com/reel/DfGGO1htP4U/ ; study note transition-lab/STUDY-irisloops-swing-bounce-2026-10-30.md (workspace-only). Independent MPC/DAW percent-convention corroboration only (50% = straight); no song, artist, or title is invoked.
