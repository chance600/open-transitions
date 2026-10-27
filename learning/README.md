# Learning loops

The repo can now learn — but only under one rule:

**The loop proposes and measures. A human disposes.**

A loop cannot hear. QC-clean renders have been rejected by ear, so no
machine metric in this package can promote a technique, and silence
never approves. Promotion into the registry requires a human PASS/heart
verdict row (see `verdicts.py`).

## The three loops

1. **Mining loop** (`ingest.py`) — a sources registry, candidate
   validation, and a queue with claim/release semantics.
   - Free/public sources only, confirmed by a human at registration.
     Paid, login-walled, or unconfirmed sources are refused.
   - Zero spend. Nothing here calls a paid API.
   - Provenance on every candidate: source URL + license note, or the
     candidate is invalid.
   - Claim protocol: claim before working an item, release only after
     the work verifies; a live claim (< 24h) blocks a double run.
   - The only shipped adapter reads a local JSONL file
     (`FileSourceAdapter`). Web fetchers are a later, separately
     approved addition — nothing here pretends to fetch.
2. **Spec → demo → verify loop** (`propose.py`, `gates.py`) —
   `propose_draft` writes a markdown spec draft (never a registry
   entry) with a demo + verification checklist. `demo_verify_gate`
   measures whether a technique is registered AND its demo
   verification is fully clean. Implementation, demo, and merge happen
   only after a human approves the draft.
3. **Verdict → selector loop** (`verdicts.py`) — a verdict schema
   (pair, technique, outcome, verifier_type human/machine, heart,
   source) and `promotion_gate`, the backtest-grade gate: human pass
   with no later human block promotes; machine verdicts, partials,
   positives, and silence never do.

`loop.py` runs one pass: claim the next unclaimed queue item, write
its draft, evaluate promotion gates over a verdicts file, print a
JSON report. It never merges, commits, or promotes. The repo ships
seeded inputs — `learning/sources.json` (9 human-registered
free/public sources), `learning/queue.json` (5 queued candidates from
the 2026-10-26 STAR survey), and `learning/verdicts.jsonl` (3
verified human verdict rows from the dataset) — and the first pass
already ran: `learning/drafts/pair_atlas_schema.md`.

## Running it

```bash
# one pass (queue + verdicts files are caller-supplied)
python -m learning.loop --queue learning/queue.json \
    --verdicts learning/verdicts.jsonl --drafts learning/drafts

# tests (stdlib only, offline)
python -m unittest discover -s learning/tests -v
```

## What is deliberately NOT here

- No web fetchers, no scheduled runner (GitHub Actions or a cron
  supplies the runner; the CI workflow runs the tests + a registry
  smoke check only).
- No auto-implementation, auto-demo, auto-merge, or auto-promotion.
- No GPL code copying: GPL sources are learn-from only — reimplement,
  never copy code or prose verbatim. (Mixxx is the standing example.)
- No technique expiry: there is no freshness cap on techniques or
  mixes. A stale source is flagged as stale, never deleted.
