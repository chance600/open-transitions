# DRAFT: thetokenwise-tech-house-breakdown-chain

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: ig:thetokenwise (instagram.com/thetokenwise) (https://www.instagram.com/reel/DfTZ1nHx_lf/)
- License note: Public Instagram post — learn-from and link only; creator retains rights
- Summary: Six-device tech-house breakdown chain from the creator's 2026-11-03 tutorial: pull kick and bass, marking the break with an impact and a downlifter; move the chord bed from the Cm9 drop chord through Cm9, Abmaj9, Fm9, Gm7; open a filter slowly so the pad brightens bar by bar; accelerate a clap roll from quarters to 8ths to 16ths; layer a riser across the mix; end with a reverse cymbal into half a beat of silence, then impact plus crash on the drop. Bar counts per stage and the riser construction are unstated. First-party caption evidence.

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

- Tempo: not stated as a single value in this post; the page's tech-house posts cluster at 128-134 BPM, but no tempo is claimed for this chain.
- Key/harmonic situation: a moving chord bed is required — the drop chord Cm9 moves through Cm9, Abmaj9, Fm9, Gm7 across the breakdown. A track with a static single-chord bed cannot carry the progression stage.
- Energy: a lift into a drop built by subtraction then staged re-entry; tension rises as elements leave and return, not by adding layers throughout.
- Sections: a breakdown section with room for a multi-bar staged build — kick and bass leave, then return on the drop after the silence beat.
- Vocals: not addressed by the source — no vocal claim is made here.
- Genre families: tech house (house family); the devices are arrangement devices, not genre-exclusive, but the source demonstrates them only in a tech-house breakdown.
- Use when: a section needs a lift into a drop and the arrangement has a chord bed that can move; tension can be built by removing elements and re-entering them in stages.
- Avoid when: a track relies on continuous kick momentum (pulling the kick would stall it); the arrangement is too short for a multi-bar staged build; bar counts per stage are needed — they are unstated by the source and must not be assumed; the riser's construction is needed — it is unstated by the source and must not be assumed.

## Registry fit

- META preconditions: a breakdown section the arrangement can spare the kick and bass from; a chord bed able to move Cm9 through Abmaj9, Fm9, Gm7; a pad whose filter can open bar by bar; claps available for an accelerating roll (quarters to 8ths to 16ths); a reverse cymbal, impact, and crash for the re-entry. The source states all synths were made in its own synth — the device chain transfers, the synth choice is not a precondition.
- Energy/exit profile: production arrangement technique, not a transition — it carries no transition exit profile. Its shape is subtraction (kick and bass out, break marked) followed by staged re-entry ending in half a beat of silence, then impact plus crash on the drop. Promotion still requires a human PASS/heart plus a clean demo heard by a human.
- Evidence reference: creator's own written breakdown (first-party caption on the creator's own account) at https://www.instagram.com/reel/DfTZ1nHx_lf/ , verified first-hand 2026-11-04 (all six devices and the chord progression stated in the caption); study note transition-lab/STUDY-thetokenwise-first-pass-2026-11-04.md (workspace-only). No song, artist, or title is invoked; the DM-gated MIDI offer behind the post is not evidence and was not engaged.
