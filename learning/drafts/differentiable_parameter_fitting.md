# DRAFT: differentiable_parameter_fitting

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge.

- Source: djtransgan (https://github.com/ChenPaulYu/DJtransGAN)
- License note: MIT
- Summary: Fit technique parameter defaults from example mixes and freeze them as deterministic defaults — the DJTransGAN method, not its torch stack (from the STAR survey top-5, 2026-10-26).

## Evidence (mechanism confirmed, method level)

DJtransGAN README + STAR survey §8, verified first-hand
2026-10-27: ICASSP 2022 differentiable DJ mixer (differentiable
fader, time-frequency-domain EQ masks) trained on DJ mixsets,
with a pre-trained model and training code. Caveat, stated
plainly: the repo trains a GAN; it does NOT ship a "freeze
fitted values as defaults" step. That step is the adaptation
proposed by the survey (fit a technique's curve parameters to
example mixes by optimization, then freeze the fitted values as
deterministic defaults) — the transfer is the method, not the
torch stack, and the survey verdict says so (method only, never
import the GAN into the numpy/scipy engine). Evidence path:
`DJtransGAN/README.md` + STAR-REPOS-SURVEY §8 (survey:
STAR-DEEP-CANDIDATES top-5 `differentiable_parameter_fitting`).

## Applicability (selector fields)

- Tempo / key / energy / sections / vocals / genre: source
  gives no per-field applicability. The method operates on mix
  examples generally; the paper's corpus is DJ mixsets plus a
  jamendo-style track corpus.
- Use when example mixes exist to fit against. Avoid when no
  example mixes exist (nothing to fit). Avoid importing the
  torch stack into the numpy/scipy engine (survey verdict:
  method only).

## Registry fit (META schema)

- Kind: process (parameter fitting, not a render).
- Requires: needs example mixes plus a parameterized technique
  to fit. Outputs deterministic defaults for that technique.
- Energy / exit / clash risk: N/A — these belong to the fitted
  technique's own profile, not to the fitting step.
- Evidence reference: DJtransGAN README (MIT) + survey §8.

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote

## Provenance

Mined from djtransgan. If the source is GPL-licensed, this draft
is learn-from only: reimplement, never copy code or prose verbatim.
