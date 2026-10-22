# dual_loop_composite

**Bank:** PERF-EZ · **Automatability:** ADAPT · **Confidence:** medium

**Source:** DJ EZ, Boiler Room x RBMA London (14 Dec 2012), minute ~14 — a tiny loop of Wookie's "Battle" used as the bass drum on one CDJ while Cleptomaniacs' "All I Do" (Bump & Flex Dance Floor Dub) plays as a percussive stutter on the other; timestamped watcher anatomy in Line Noise, "DJ EZ: Pure Garage and the DJs' DJ" (Substack). Set-level record: 31 cuts in 45 minutes (Mixmag's "20 Best DJ Mixes of the Decade", via BCR001); trademark style stated by fabric (FABRICLIVE 71 newsflash, 2013).

## Signature

```python
dual_loop_composite(a, b, sr, bar_s, comp_bars=4, role_split_hz=250.0)
```

## Spec

For `comp_bars` bars, both records leave and a composite groove
plays in their place: A's last bar, looped and low-passed below
`role_split_hz` (the kick role), under B's first bar, looped and
high-passed above the split (the percussive role). Then B plays in
full from its start — its entrance lands as a reveal, since the
crowd has already heard its percussion stripped of body. A's head
passes through untouched before the composite window.

Neither source is playing as itself inside the composite; a third,
synthetic groove built from two role-stripped loops is — watchers
of the original called it "DJing as production". The composite is
a neutral rhythmic ground both records can exit and enter through.
Distinct from loop juggling one track's own loops (T-031), from
layering full tracks (T-020), from firing a prepared element from
a spare deck (GAP-16), and from a pattern bridge layered over a
playing track (WEB-12). Confidence L1: the audio anatomy is
documented with a timestamp and named sources; the demo render is
the re-render proof. The goal workspace's performers.md named this
exact move "the extraction target not yet in the engine"
(2026-10-17); this build closes it.
