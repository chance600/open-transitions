# drop_insert

**Bank:** WEB-21 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** kohadachan, "A Personal Drum and Bass DJ how to" (note.com, 2024) — fetched 2026-10-22; performed-family corroboration: Pioneer DJ, DDJ-400 technique tutorials (2019)

## Signature

```python
drop_insert(a, b, sr, bar_s, insert_bars=1, drop_bar=8)
```

## Spec

At A's drop downbeat, B's drop plays for `insert_bars` bars
INSTEAD — then A's drop resumes.

a: build + drop segment; the drop's first downbeat is at bar
    `drop_bar` (caller aligns).
b: incoming segment, STARTS at its drop.
A keeps running underneath while muted (the deck never stops),
so A's drop resumes at the position it would have reached —
the insert is a substitution window in A's timeline, not a
pause. insert_bars: 1 = the source's bar; 2 = a statement;
4 = the full dubstep switch, A's drop withheld a whole phrase.

A human-triggered weapon like fake_drop (T-029): it only reads
on a well-known A whose drop the crowd can predict. Distinct
from T-029 (the rug-pull is a void — here a foreign drop
plays), hotcue_drop_swap (T-014: the replacement is permanent;
here A returns), same_song_switchup (GAP-13: one track's two
arrangements; here the guest is a different track).
