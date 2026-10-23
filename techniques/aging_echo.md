# aging_echo

**Bank:** CMP-01 · **Automatability:** ADAPT · **Confidence:** high

**Source:** The dub tradition's feedback delay (King Tubby / Scientist; carried into dub techno) — an echo throw whose feedback loop carries a lowpass, so every repeat is darker than the last. Promoted by the Phase 24 combinatorial enumeration (ENUMERATION.md Part B): the atom pair echo × filter already existed as *parallel* atoms in `layered_fx_stack` / `layered_emergence`; this is the serial topology, where the filter sits inside the recurrence.

## Signature

```python
aging_echo(a, b, sr, bpm, bar_s, beat_div=0.5, feedback=0.55, wet=0.6, cutoff_hz=4500.0, tail_beats=4)
```

## Spec

A's final beat is thrown exactly as in `echo_out` (T-004): lows
killed over the throw beat, input gated at the throw, post-fader
tail. The difference is the loop: a 2nd-order lowpass at
`cutoff_hz` sits inside the feedback path, so the series is
y = Σ feedback^k · shift^k(LP^k(x)) — repeat k has passed the
filter k times. Level and brightness decay together; repeat
spectra descend measurably (the verification the enumeration
asked for). The tail rings `tail_beats` past A's end, over B's
entrance at full level.

Why it is not its neighbours: `echo_out`'s repeats are equally
bright copies (`dsp.feedback_delay` is a pure geometric
series); `spiral_echo` (WEB-01) conditions the same loop with
pitch instead of tone — the standing precedent that a
loop-internal modification earns a base. The vendor name "Dub
Echo" was resolved in the bank (Phases 6/8) as a knob form of
T-004 — an echo throw with a colour control; this entry is the
tradition mechanism the name points at, named for the
mechanism so the two records do not collide. Feed conditioning
as doctrine (input EQ, ghost-trigger carve) is banked in
knowledge/mixing (iZotope, Phase 18).


## Axis (Phase 26, software/hardware tranche A)

**Tape Echo head-combo staging (SP-404MKII)** — Roland's RE-201
model parameterises the in-loop lowpass's partner: three tape
heads (S/M/L) in seven combinations (S, M, L, S+M, S+L, M+L,
S+M+L) make the "loop" a multi-tap comb — repeats arrive in
head-spaced clusters, each cluster aging together. TIME
(10–800 ms) is staged as tape SPEED, not division, and
wow/flutter modulates the loop length itself, so the darkening
per repeat wobbles. Evidence: SP-404MKII Reference v5.5, Tape
Echo page, fetched 2026-10-23.
