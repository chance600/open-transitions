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

## Personal-source boundary (hard)

His Instagram DMs to self (alec_brewer) are a production-track
input, and they are PERSONAL, not public. The index lives only in
the workspace
(`transition-lab/SELF-DM-PRODUCER-TRICKS-2026-10-27.jsonl`),
summarized, never verbatim, never sent anywhere. It must NEVER be
registered as a loop source (`Source.validate` rejects
`free_public=false` by design) and tricks from it must NEVER enter
a repo queue or draft as if publicly sourced. Personal knowledge
informs study in the chats; the public repo holds public-source
learning only. Changing this boundary is his explicit call, not a
worker's judgment.
