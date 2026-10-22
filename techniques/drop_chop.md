# drop_chop

**Bank:** WEB-20 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** DJGear2K, "What Is A Double Drop?" (2023), step 4 — fetched 2026-10-22; DJ.Studio, "How To Mix Drum And Bass" (2024), method 8 "Cutting and Switching"

## Signature

```python
drop_chop(a, b, sr, bar_s, chop_bars=2, rounds=2, land_bars=1)
```

## Spec

Two drops land together, then full-level ownership alternates
between them on a bar grid before committing to B.

a, b: phrase-aligned DROP segments (caller aligns the drops'
    downbeats); the shorter is zero-padded.
land_bars: both drops play together first (default 1 — the
    landing must register as a double drop before it trades).
Then ownership alternates every chop_bars bars (A, B, A, B) for
`rounds` full cycles; the non-owner is killed outright (3 ms
smoothed edges, never a blend). After the last alternation the
mix commits to B. The chop is the single-sub rule performed:
exactly one bassline exists at any instant.

Distinct from rhythmic_fader_chops (GAP-15: a 16th-note gate on
an EXITING A while B fades in — an entry gesture; here both
tracks are already the main event and the period is bars), and
from double_drop (T-024: both drops held under one enforced
sub, then a bass swap — the chop replaces the hold with
alternation).
