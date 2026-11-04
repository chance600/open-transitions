# DRAFT: thetokenwise-bass-kick-turn-taking

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: ig:thetokenwise (instagram.com/thetokenwise) (https://www.instagram.com/reel/DfUc2HWROjL/)
- License note: Public Instagram post — learn-from and link only; creator retains rights
- Summary: Tech-house low-end placement rule from the creator's 2026-11-04 explainer: keep bass notes off the kick hits and place them on the 16th-note gaps between kicks; the alternation creates bounce and clears low-end mud, with sidechain compression as the final glue. Stated at 130 BPM in A minor, and corroborated by the page's drum posts repeatedly placing bass in the gaps rather than on the kick. Sidechain depth, release, and routing are unstated. First-party caption evidence.

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from ig:thetokenwise (instagram.com/thetokenwise). If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.

## Applicability (selector fields, grounded in the source)

- Tempo: 130 BPM as stated in the source; a four-on-the-floor groove tempo.
- Key/harmonic situation: A minor as stated in the source; the rule itself is rhythmic placement, not a harmonic move.
- Energy: low-end clarity and kick punch — the move addresses a muddy low end, not an energy lift.
- Sections: the groove body where kick and bass run together; a placement rule for an ongoing pattern, not a transition or a breakdown device.
- Vocals: not addressed by the source — no vocal claim is made here.
- Genre families: tech house (house family); corroborated by the page's drum posts repeatedly placing bass in the gaps rather than on the kick.
- Use when: a four-on-the-floor groove feels muddy in the low end or the kick loses punch under the bass; a bassline needs bounce without changing its notes.
- Avoid when: the arrangement intentionally stacks bass and kick for weight (for example a sustained sub under a sparse kick); the bassline's rhythm is itself the lead hook and shifting it off the kick would break its phrasing; sidechain settings are needed — depth, release, and routing are unstated by the source and must not be assumed.

## Registry fit

- META preconditions: four-on-the-floor kick; bass notes placed on the 16th-note gaps between kicks, never on the kick hits; sidechain compression as the final glue with settings unstated (not a precondition that can be gated until specified).
- Energy/exit profile: production groove technique, not a transition — it carries no transition exit profile. Its effect is low-end separation and bounce via kick/bass alternation. Promotion still requires a human PASS/heart plus a clean demo heard by a human.
- Evidence reference: creator's own written breakdown (first-party caption on the creator's own account) at https://www.instagram.com/reel/DfUc2HWROjL/ , verified first-hand 2026-11-04 (mechanism, 130 BPM, A minor all stated in the caption); study note transition-lab/STUDY-thetokenwise-first-pass-2026-11-04.md (workspace-only). No song, artist, or title is invoked; the DM-gated MIDI offer behind the post is not evidence and was not engaged.
