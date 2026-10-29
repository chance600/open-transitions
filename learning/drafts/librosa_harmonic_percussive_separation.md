# DRAFT: librosa_harmonic_percussive_separation

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: librosa (https://github.com/librosa/librosa)
- License note: ISC
- Summary: Harmonic-percussive separation (librosa.effects.hpss/harmonic/percussive): split harmonic vs percussive content for element-level trading. [Repo-grounded; scout named no mechanism for librosa.]

## When to use / when to avoid

See Applicability below (grounded in the source docs, 2026-10-29).

## Evidence (mechanism confirmed)

Harmonic-percussive separation, verified first-hand 2026-10-29
against the librosa docs: the official tutorial gives
`y_harmonic, y_percussive = librosa.effects.hpss(y)` — the input
time series separated into harmonic (tonal) and percussive
(transient) portions, each the same shape and duration as the
input — and the HPSS example doc gives the same split at
spectrogram level via `librosa.decompose.hpss`. The candidate's
transfer — splitting harmonic vs percussive content for
element-level trading — is a proposal built on that confirmed
split, not a claim the docs make about DJ transitions. Caveat
from the same docs: the default split assigns every bin to one
side or the other and handles noise poorly; vocals and other
sounds that are not purely harmonic or percussive end up spread
between the two components.

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from librosa. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.

## Applicability

Grounded in the librosa docs (read first-hand 2026-10-29);
generic descriptors only, no song, artist, or title named.

- Tempo: the source gives no tempo, BPM range, or maximum BPM
  delta for this separation; none is stated here.
- Key/harmonic situation: the source gives no key or harmonic
  guidance for this separation; none is claimed here.
- Energy: the source gives no energy delta or energy floor for
  this separation; none is asserted.
- Sections: the source gives no section restriction — the split
  applies to a track's audio generally, not to a named section.
- Vocals: the source's own caveat applies — vocals are not
  purely harmonic or percussive and spread between the two
  components, so this split is not a vocal-isolation tool.
- Genre families: the source names no genre family for this
  separation; none is claimed here.

Use-when: an element-level trade needs the tonal content
separated from the transient content of a track (for example
keeping one side's harmonic bed while trading its percussive
layer), with the split treated as an estimate to check.
Avoid-when: the job is vocal isolation or clean stem
separation — the docs state vocals and noise spread across
both components, so a stem separator, not HPSS, is the tool
for that; or the split is treated as ground truth rather
than an estimated decomposition.

## Registry fit

Mapping to the META schema (engine/meta.py), as a proposal for a
future META entry — not an entry itself.

- Preconditions (requires): audio input for each track to
  separate; no bpm_delta_pct_max, camelot_max, phrase, or genre
  precondition of its own — separation precedes selection.
  vocal_ok: unspecified as a rule, with the docs' caveat that
  vocals spread across both components.
- Energy/exit profile: delta 0, tension flat (separation only,
  not an energy move). Exit: none of its own (the host
  transition's exit). clash_risk: unspecified — the source
  makes no clash claim for this separation.
- Evidence reference: librosa official tutorial,
  `librosa.effects.hpss` (ISC), and librosa HPSS example doc,
  `librosa.decompose.hpss`, both confirmed first-hand
  2026-10-29: input separated into harmonic (tonal) and
  percussive (transient) portions.
