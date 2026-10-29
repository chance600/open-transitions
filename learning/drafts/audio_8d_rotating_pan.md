# DRAFT: audio_8d_rotating_pan

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge. STUDY-ONLY (user direction
2026-10-29 via style lab): learn the implementation/algorithm.
Do NOT build an 8D version or present this as a style to apply
unless the user says otherwise — his "maybe" on direct application
stays tentative.

- Source: speechgen-8d (https://speechgen.io/en/effect/audio_8d/)
- Supporting source: vocalcut-8d (https://vocalcut.com/8d-audio)
- License note: Public articles — learn-from and link only; no license claimed
- Summary: 8D audio rotating-pan effect: a slow auto-pan cycles
  sound left-to-right and back, plus echo/reverb for space, so on
  headphones the sound seems to circle the listener's head. An
  ordinary stereo file, not a spatial format.

## Evidence (mechanism confirmed)

8D audio implementation, verified first-hand 2026-10-29 against
the registered sources (public articles, learn-from and link only):

- DSP chain (SpeechGen): "No AI — just a short, classic DSP chain."
  Rotation: a slow auto-pan cycles the sound left-to-right and back,
  so it seems to circle the head (works only in headphones). Space:
  a short 180 ms echo adds depth and a sense of room. Stereo: the
  track is widened to full stereo before panning.
- What it is (VocalCut): continuously panning the audio in a circle
  around a virtual listener, plus a touch of reverb for space, at a
  rotation speed the maker sets. "There's nothing literally
  eight-dimensional about it" — a marketing name, not a dimension.
- Rotation speed (VocalCut): most 8D edits circle once every 5–15
  seconds — faster feels dizzying or gimmicky, much slower gets hard
  to notice. A little reverb sells the sense of space; too much
  washes out the detail.
- Headphones requirement (both sources): the whole effect lives in
  left-right stereo movement. Headphones/earbuds keep the two
  channels separate, which is what creates the orbiting sensation.
  On speakers the two channels blend in the air before they reach
  the listener, so the movement mostly collapses into ordinary
  panning and the effect is lost. On a single speaker the effect
  disappears (SpeechGen: "it disappears on a single speaker").
- Applied across a whole track: the rotation runs continuously at a
  set speed and is baked into the exported stereo file, so it travels
  with the track and plays anywhere a normal song does. A section
  can be trimmed first so the effect covers only that part.
- Mono behavior (sourced parts): a mono SOURCE can be made 8D —
  the export is always stereo, because the movement is created
  during processing (VocalCut). Mono PLAYBACK (one speaker, or a
  summed-mono feed) loses the orbit: with no inter-ear difference
  there is nothing left to circle. The file itself still plays —
  it is an ordinary stereo file, not a format that needs a special
  player.
- NOT spatial audio (VocalCut): Dolby Atmos places sounds as objects
  in 3D space and needs a compatible player to render them. 8D is an
  ordinary two-channel stereo file — the circling comes from smoothly
  moving sound between the left and right ears at a steady volume,
  plus reverb. No special app or format required.

OPEN QUESTION — mono-sum level: whether a mono-summed 8D file holds
steady level or pumps as the pan crosses center depends on the pan
law (equal-power vs linear), and neither source states which law
their chain uses. Do not assert a mono-sum level behavior until it
is measured on an actual render. The sourced claim stops at: the
orbit disappears in mono; the file still plays.

## Applicability (selector fields)

- Tempo: source gives no tempo applicability (the rotation is a
  time-based pan cycle, 5–15 s per turn, independent of song tempo).
- Key/harmonic: source gives no key applicability.
- Energy: source gives no energy applicability; reverb amount is
  the stated taste control (a little sells space, too much washes
  out detail).
- Sections: source gives no section applicability; the rotation can
  run across a whole track or a trimmed section.
- Vocals: source gives no vocal-specific applicability; wide stereo
  songs feel most spacious (SpeechGen tips); the effect applies to
  music and voices alike.
- Genre families: source gives no genre limit (any genre works per
  the tool pages; no genre-specific claim is asserted here).
- Use when: STUDY ONLY — understanding how a rotating-pan +
  reverb chain creates a headphone orbit illusion, its speed range,
  and its mono/headphone limits. No applied use is claimed.
- Avoid when: any applied use — this draft is study-only by
  direction. Do not present it as a style to apply, and do not build
  an 8D version, unless the user says otherwise.

STUDY-ONLY BANNER (carried, not lifted): the 2026-10-29 direction
marks 8D audio STUDY-ONLY. Learn the implementation/algorithm; do
NOT build an 8D version or present it as an applicable style unless
the user says otherwise. His "maybe" on direct application stays
tentative and does not authorize a build.

## Registry fit (META schema)

Mapping to the META schema (engine/meta.py), as a proposal for a
future META entry — not an entry itself. NOTE: this mapping is
analytical only; study-only status means no META entry should be
created from it without a further user direction lifting the ban.

- Preconditions (requires): a stereo (or mono-to-stereo) source;
  slow auto-pan rotation at 5–15 s per turn; echo/reverb for space
  (180 ms echo in the SpeechGen recipe); headphone playback for the
  effect to read at all. No camelot_max, vocal_ok, or genre_pair_ok
  threshold is asserted — the sources state none.
- Energy/exit profile: no handover profile applies — this is a
  whole-track spatial treatment, not a seam between two tracks.
  Exit: the export runs slightly longer than the original where a
  reverb tail is allowed to fade (VocalCut: ~2.5 s longer).
- Evidence reference: SpeechGen, "8D Audio Maker"
  (https://speechgen.io/en/effect/audio_8d/), DSP recipe
  (auto-pan + 180 ms echo + stereo widening) and single-speaker
  disappearance, read first-hand 2026-10-29; VocalCut, "8D Audio
  Maker" (https://vocalcut.com/8d-audio), rotation speed range,
  headphone collapse, mono-source handling, and Atmos distinction,
  read first-hand 2026-10-29. Learn-from and link only; no preset,
  sample, hook, or melody copied.

## Demo + verification checklist (all must pass before merge)

- [ ] STUDY-ONLY: no demo, no implementation, no merge unless the
      user lifts the study-only direction explicitly
- [ ] If lifted: implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from speechgen-8d + vocalcut-8d. Public articles: learn-from
only — reimplement, never copy code or prose verbatim. No sample,
hook, or melody lifted; technique + implementation only.
