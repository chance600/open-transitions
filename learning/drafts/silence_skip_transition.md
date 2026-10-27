# DRAFT: silence_skip_transition

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: mixxx (https://github.com/mixxxdj/mixxx)
- License note: GPL-2.0-or-later - learn-from only, never copy code
- Summary: AutoDJ modes that skip silent intros/outros, backed by a dedicated silence analyzer; transfers as a selector rule: when either side has leading/trailing silence, skip it instead of fading through dead air.

## Evidence (mechanism confirmed)

Mixxx `src/library/autodj/autodjprocessor.cpp`, verified first-hand
2026-10-27: `TransitionMode::FixedSkipSilence` and
`FixedStartCenterSkipSilence` (fixed fade time, outgoing fade ends
at the outgoing track's last sound, incoming track starts at its
first sound) — i.e. silent intros/outros are skipped, not faded
through. Backed by `src/analyzer/analyzersilence.cpp`:
`AnalyzerSilence` detects first/last sound at a -60 dB threshold
(0.001f), places the intro start at first sound and the outro end
at last sound, and AutoDJ falls back to those positions when no
user intro/outro cues are set. Evidence paths:
`mixxx/src/library/autodj/autodjprocessor.cpp` (SkipSilence cases)
and `mixxx/src/analyzer/analyzersilence.cpp` (survey evidence
cited `autodjprocessor.h`; the mechanism itself lives in the .cpp
plus the analyzer). License: GPL-2.0-or-later, learn-from only.

## Applicability (selector fields)

- Tempo: source gives no tempo applicability — the modes use a
  fixed fade time and key off sound positions, not tempo.
- Key / harmonic situation: source gives none — level-based, not
  key-based.
- Energy: source gives no energy applicability — the trigger is
  leading/trailing sub-threshold silence, not energy level.
- Sections: intro/outro boundaries only — the rule trims the
  edges of a track, never a mid-track section.
- Vocals: source gives no vocal applicability — detection is
  level-based (-60 dB), not vocal-aware.
- Genre families: source gives none.
- Use when: either side has leading/trailing silence (below the
  analyzer's -60 dB threshold) that would otherwise be faded
  through as dead air.
- Avoid when: a quiet intro/outro passage is musically
  intentional but sits below the -60 dB threshold — the analyzer
  would treat it as silence and the skip would cut it.

## Registry fit (META schema)

- Kind: selector rule (edge trim), not a render effect.
- Preconditions: first-sound / last-sound positions for both
  tracks (AnalyzerSilence-derived intro/outro cues, or
  user-placed intro/outro cues as fallback overrides).
- Energy / exit profile: exit at the outgoing track's last sound,
  entry at the incoming track's first sound; fixed fade time
  between them. No energy or clash scoring in the source.
- Evidence reference: mixxx `autodjprocessor.cpp`
  (FixedSkipSilence / FixedStartCenterSkipSilence) +
  `analyzersilence.cpp` (GPL, learn-from only).

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from mixxx. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
