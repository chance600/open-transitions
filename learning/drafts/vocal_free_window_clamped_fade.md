# DRAFT: vocal_free_window_clamped_fade

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: auto-dj-ai (https://github.com/caffettino87/auto-dj-ai)
- License note: MIT
- Summary: Fade length hard-capped to min(outgoing vocal-free outro, incoming vocal-free intro) from a full-track vocal timeline, so a fade never covers vocals on either side; transfers as a duration clamp driven by per-track vocal windows.

## Evidence (mechanism confirmed)

auto-dj-ai `src/player.js`, verified first-hand 2026-10-27:
"Crossfade length, clamped so it fits inside both the outgoing
vocal-free outro" — fade = min(fade, outro), then min(fade,
intro); plus the comment "Crossfade length is capped to the
vocal-free outro so we never fade over vocals." Evidence path:
`auto-dj-ai/src/player.js` (survey: STAR-DEEP-CANDIDATES
`vocal_free_window_clamped_fade`).

## Applicability (selector fields)

- Tempo: fade length is computed in beats, then capped by the
  vocal windows. Source gives no BPM-gap cap for the clamp
  itself.
- Key / energy / sections / genre: source gives no
  applicability.
- Vocals: this IS the vocal-window clamp. Use when
  vocal-free outro / intro windows are measured for both
  sides. Avoid fading over vocals — that is exactly what the
  clamp prevents. Note the guard behavior: the clamp applies
  only when a window is finite and > 0, so an unmeasured
  window does NOT clamp (it is skipped, not treated as zero).
- Use when both sides offer vocal-free edges. Avoid relying
  on the clamp when windows are unmeasured.

## Registry fit (META schema)

- Kind: render (duration clamp applied to a fade).
- Requires: needs measured vocal-free outro + intro windows.
- Energy: delta 0, tension flat. Exit: seamless. Clash risk:
  vocal (prevented by the clamp).
- Evidence reference: auto-dj-ai `player.js` (MIT).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from auto-dj-ai. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
