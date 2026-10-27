# Learning tracks: production + DJing (2026-10-27)

One loop, two tracks. Same mechanics on both — propose, measure,
human disposes; a pass never merges, never commits, never promotes;
promotion needs a human PASS/heart; partials, machine verdicts, and
silence never promote. What differs is the sources, and therefore
what each track learns.

## Layout

| | DJing track | Production track |
|---|---|---|
| Sources | `learning/sources.json` (9 repos: transition library, selector) | `learning/sources_production.json` (9 public IG breakdown accounts) |
| Queue | `learning/queue.json` | `learning/queue_production.json` |
| Drafts | `learning/drafts/` | `learning/drafts_production/` |
| Verdicts | `learning/verdicts.jsonl` (shared: verdicts are about techniques, both tracks read the same gate) | same file |

Run a pass per track from the repo root:

```
python -m learning.loop --queue learning/queue.json \
  --verdicts learning/verdicts.jsonl --drafts learning/drafts \
  --sources learning/sources.json
python -m learning.loop --queue learning/queue_production.json \
  --verdicts learning/verdicts.jsonl --drafts learning/drafts_production \
  --sources learning/sources_production.json
```

An empty queue is a quiet note, not an error ("queue empty or all
items claimed; nothing proposed"). The production queue starts
empty on purpose — it fills only from validated public-source finds,
never from invention.

## Why IG sources register at domain level

`Candidate.validate` requires the candidate URL to contain the
registered source URL. An Instagram reel URL does not contain its
author's profile URL, so IG sources register with
`url = https://www.instagram.com/` and the handle carried in `name`
(e.g. `ig:jameshypestories (instagram.com/jameshypestories)`).
License note on every IG source is learn-from and link only —
creators retain rights; nothing is copied into the repo.

## Feeds, both directions

- Loop → mixes chat (DJ chat, 293f1315): techniques, selector
  rankings, rebuild assignments via
  `mixing-lane/work/inbox-from-learning.md`.
- Loop → style lab chat (2df600c4): production-breakdown finds via
  the rolling watch (cron `dj-style-ref-watch`), plus production
  drafts as study references. Nothing sent is a verdict.
- Mixes chat → loop: verdict dataset rows feed
  `learning/verdicts.jsonl` and the promotion gates.
- Style lab → loop: the style lab's inbox file
  (`mixing-lane/work/inbox-from-style.md`) and its study references
  are read-only inputs to the production track. No lane invents
  another lane's verdicts — ❤️ / PASS / REJECT only ever come from
  his words in the mixes chat.

## Personal-source boundary (hard, updated 2026-10-27 by his call)

His Instagram DMs to self (alec_brewer) are a production-track
input. The summarized index now lives IN this repo as
`learning/producer-tricks-index.jsonl` (42 tricks, published here
by his explicit 2026-10-27 decision, knowing the repo is public).
It is a REFERENCE, not a mining source: it is NOT registered in
any sources file (`Source.validate` rejects `free_public=false`
by design) and tricks from it are NOT queued as candidates and
NOT copied into drafts. Personal knowledge informs study in the
chats; the repo's queues hold public-source learning only.
Registering or queueing the personal index would be a further
explicit call, not a worker's judgment.

## Transfer note — Oct-20 DM study, merged into this track 2026-10-27

The other DJ chat's Oct-20 work was NOT lost and is now this
track's seed, not a duplicate:
- Study document (workspace, provenance-rich, NOT in this repo):
  `technique-bank/DM-CLIP-STUDY.md` (634 lines, 2026-10-20) —
  91 self-DM messages, 81 IG clips studied, 44 bank candidates
  from clips + 56 creator-backtrack teachings (19 concrete).
  Every technique carries source clip URL, creator handle, save
  date, and DM thread ref (standing provenance rule). Raw data:
  `technique-bank/hidden_files/dm-harvest/` (clip-study.json,
  creator-digests.json, selfthread-index.json).
- Repo implementation of those candidates: `engine/dm_techniques.py`
  and `techniques/*.md` specs carrying DM-Axx provenance.
- The 9 backtracked creators are now registered production
  sources (18 total with the original 9): @morsbeats_,
  @nest.acoustics, @marshalljamesmusic, @dnksaus,
  @djsfrenchcandy, @imtrvcy, @mattstonedj, @illumizotti,
  @enamourmusic. Highest signal for ongoing mining:
  @marshalljamesmusic (densest written advice), @dnksaus
  (most concrete/technical), @morsbeats_ (named Ableton moves,
  needs video mining). Low yield, still monitored, criteria-judged:
  @djsfrenchcandy, @mattstonedj, @enamourmusic (mostly
  promo/lifestyle). @maxanddana backtrack failed (0 posts).
- The published `producer-tricks-index.jsonl` (42 summaries,
  Oct-27 thread re-read) is the public summary; the study doc
  above is the provenance record. Overlap between the 42 and the
  DM-Axx specs is NOT yet measured — a future pass may attach
  creators per trick from the study doc, but must not invent
  them. The study's own line stands: "New content from these
  creators flows through the same distill → provenance →
  bank-flag pipeline" — that pipeline is now this watch + loop.
- Merge 2026-10-27: full self-DM source-account extraction
  (`transition-lab/SELF-DM-SOURCE-ACCOUNTS-2026-10-27.json`,
  workspace only) — 65 distinct accounts (61 IG + 4 Threads),
  92 thread messages fully accounted for (82 IG posts, 4
  Threads links, 4 unresolvable, 2 grips3d profile refs, not
  posts). All 9 backtracked creators confirmed present in
  current thread data. All 52 further IG accounts registered
  (70 production sources total, all validate); the 4 Threads
  accounts are NOT IG sources and stay out. Watch design,
  rate-limit-grounded (429 hit after ~14 lookups during
  extraction): per-account checks cover jameshypestories +
  12 accounts (9 backtrack + ammo.amor, evolving.ai,
  goldo.musicproducer, the further multi-share sources);
  the 49 single-share accounts are covered by search queries
  + source registration, not per-account checks.
