# Draft quality bar — what "legit" means here (2026-10-27)

A draft is a claim about a real educational source. This file states
what is checked, what is NOT checked, and what must be true before
a draft counts as knowledge rather than pollution.

## Quarantine facts (verified)

- Drafts are markdown docs in `learning/drafts/` (production:
  `learning/drafts_production/`). No engine code reads them; they
  cannot affect a render. The registry is untouched by the loop:
  113 bases, unchanged since the loop started.
- A draft is NOT a registry entry. Its own header says so, and its
  checklist requires implementation + META entry + a clean demo +
  a technique named in a shipped render AND heard by a human.

## Gates that exist (code-enforced)

1. **Source registration** (`learning/ingest.py:Source.validate`):
   human-registered only, `free_public` must be true, URL must be
   http(s). A non-public source can never be registered.
2. **Candidate validation** (`Candidate.validate`): name + summary
   required; `source_name` must be registered; `source_url` must
   contain the registered source URL; `license_note` required.
3. **Promotion gate** (`learning/verdicts.py:promotion_gate`):
   only a human PASS (heart counts) promotes; a later human reject
   blocks; partial/positive alone never promote; machine verdicts
   are ignored entirely; silence never approves.
4. **Demo gate** (`learning/gates.py:demo_verify_gate`): META entry
   + fully clean demo verification (render/silence/headroom).
   Machine QC only — the module itself notes QC-clean renders
   have been rejected by ear. Hearing is the real gate.

## Gaps (honest, as of 2026-10-27)

1. **No per-draft content re-verification.** Candidate validation
   checks URL *shape*, not content. A summary could drift from its
   source and nothing mechanical catches it. The one content-truth
   step that exists is the STAR survey (sources read first-hand,
   evidence paths recorded) — a one-time survey, not a per-draft
   check.
2. **Applicability was empty in all 19 drafts.** Every draft
   carried "When to use / when to avoid (to be specified)" and
   "Parameters (to be specified by the implementer)" as
   placeholders. No draft said which song types, tempos, keys,
   energies, vocal situations, or genres it fits. That is the
   pollution vector: summaries that look like knowledge but carry
   no applicability.
3. **Production track unverified in practice.** Its queue is empty,
   so its checks (reel URL + license + link verified via post
   --url) have never run on a real find. A reel's spoken content
   is not in its caption, so caption paraphrase alone cannot
   verify a production technique's claims — transcripts (or the
   creator's own written breakdown) are required evidence.

## The bar (effective 2026-10-27, from his quality question)

Every draft, new or existing, must carry all four before it counts:

1. **Mechanism confirmed against the source.** The worker opens
   the source (repo file, survey evidence path, or verified post)
   and confirms the mechanism appears there. Evidence path is
   recorded in the draft. Unconfirmable → candidate is PARKED,
   never drafted. Invented detail → rejected.
2. **Applicability block, in the selector's own fields** (tempo,
   key/harmonic situation, energy, sections, vocals, genre
   families — the fields `engine/select.py` actually ranks on).
   Both Use-when AND Avoid-when, grounded in the source, in
   generic descriptors (e.g. "high-energy house with a vocal-free
   outro"). Never an invented song, artist, or title. If the
   source gives no applicability, the block says so explicitly —
   it is never filled by guesswork.
3. **Registry-fit block**, mapping to the META schema:
   preconditions, energy/exit profile, evidence reference. A draft
   that cannot be mapped cannot be assessed for promotion.
4. **Promotion bar unchanged:** human PASS/heart + clean demo
   (including heard by a human) + backtest that does not regress.
   Until then the draft stays a draft, however good it reads.

## What this does NOT claim

- A draft passing this bar is still not proven. Proof is a
  shipped render, heard by a human, passing the promotion gate.
- The production track meets this bar only once its first real
  find is transcript-verified; until then its checks are
  untested, and this file says so.

## Unverified + negative-data ledger (workspace-only)

Unconfirmed candidates and drafts, and confirmed failures, are NOT
published in this repo. They live in a workspace-only ledger:
`transition-lab/UNVERIFIED-AND-NEGATIVE-DATA.md` (his delegation
2026-10-27, lane's call on placement: workspace-only beats a
public listing (pollution), a second repo (overhead), and a Drive
file (sync drift)). The ledger has two sections — UNVERIFIED
(items that may graduate when new evidence arrives: similar
confirmed techniques, better source reads, corrected summaries)
and NEGATIVE DATA (confirmed failures kept as warnings, even if a
similar technique later verifies). Graduation re-enters the normal
loop; entries are never deleted, only marked graduated. Loop-side
failures only — mixes verdict data is never copied here.
