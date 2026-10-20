# mic_talkover_reset

**Bank:** GAP-18 · **Automatability:** planning only — not renderable · **Confidence:** medium

**Source:** open-format source — mic talk-over as a named transition tool — Transition Gap Report 2026-10-19, GAP-18

## Signature

No function. `kind: "planning"` in the registry — there is no audio
operation to render. The move is executed by a human with a microphone.

## Spec

Talk over the outgoing track's outro on the mic to reset the room, then
drop the next track cold.

- A's outro plays under the voice (ducked ~6 dB is the working default;
  `duck_db` and `talkover_bars` are plan parameters, not render params).
- The talk-over does the transition's social work: it marks the end of a
  section, re-aims the room's attention, and makes the incoming track's
  cold entrance read as an event instead of a mistake.
- B enters cold on the 1 — no blend. Because the room was just addressed
  by a human, the cut needs no musical justification, which is why this
  is the library's bridge for energy jumps (≥3) and genre leaps that no
  render technique survives.

Registry entry exists so selection can *recommend* it (SET family,
phrase_a "outro") where every render technique is rejected — the honest
answer to some pairs is "a person talks, then the track drops."
