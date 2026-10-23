# stem_element_crossfade

**Bank:** GAP-08 · **Automatability:** ADOPT · **Confidence:** medium

**Source:** James Hype / stems-first method (Hype/stems) — Transition Gap Report 2026-10-19, GAP-08

## Signature

```python
stem_element_crossfade(a_stems, b_stems, sr, bar_s, order=("bass","drums","melody","vocal"), bars_per=4)
```

## Spec

A 16-bar handover one stem at a time. A plays full for bars 1–4; then per
4-bar stage, B's next stem (default order: bass → drums → melody → vocal)
enters at unity while A's corresponding stem mutes with a 1-beat
equal-power crossfade.

The signature move is stage one (bars 5–8): B's isolated bassline plays
under A's *intact* drums/melody/vocal — a bass entry with no kick attached.
EQ tools cannot do this: opening B's low band always brings B's kick with
it; only a stem separates bass from kick. T-001/T-002 hand over frequency
bands, never elements.

Requires stems on both tracks ("needs": ["stems"]). Key matters more than
in a band blend — B's bare bass sits against A's melody for a full stage —
so camelot_max is 2. Stems not listed in `order` stay with A throughout.


## Axes (Phase 26, software/hardware tranche A)

**ModernEQ coupled morph law (VirtualDJ)** — VDJ's middle
ModernEQ knob is a *coupled two-stem law* on this base's
substrate: one scalar θ ∈ [−1, 1] drives vocal and melody gains
in opposite senses with ASYMMETRIC kill order — leftward, the
vocal reaches silence at θ = −0.5 and both are dead at −1;
rightward, the vocal *boosts* slightly while the melody dies at
+1 — a non-monotonic vocal curve no pair of independent fades
reproduces. Staged here as a one-knob vocal↔melody morph inside
the sixteen-bar handover. Evidence: VirtualDJ Manual, Mixer /
ModernEQ pages, fetched 2026-10-23. (The manual's 5-knob Stems
EQ never names its five stems in text — recorded gap.)

**Kick/hihat sub-split (VirtualDJ ModernEQ)** — the drums stem
splits into kick and hihat sub-stems with different laws: hihats
crossfade CONTINUOUSLY (an "energy" control), kicks are kept
mutually exclusive — step-swapped, never blended. Staged here:
the drums stage of the handover splits, hats morphing across
the full drums window while the kick changes hands on one bar
line. The surrogate set grows 4 → 6 under this staging.

**EZRemix right-isolate law (VirtualDJ)** — right of centre, a
stem knob stops being a gain and becomes a SOLO: the selected
group at unity, all others removed. A staging of this base
where one element's takeover is total by construction.

**Parallel stem crossfader bank (djay Neural Mix)** — djay
gives each stem its own A/B crossfader: "Use the individual
crossfaders to swap or cut stems between the decks." Where this
base sequences the handover in a fixed order over 16 bars, the
bank staging runs the four balances in PARALLEL and
independently — including holding a composite (A's drums under
B's vocal) indefinitely mid-transition. The held composite is a
state, not a gesture; see the workflows knowledge entry on
scheme-gap stagings for what the registry cannot name about it.
Evidence: djay Pro help, Neural Mix pages, fetched 2026-10-23.

**Automix neural handover (djay)** — the unattended form: an
Automix Neural Mix transition whose only documented parameter
is duration (bars/seconds). Banked as a staging note only — the
internal element order is a black box in the source (recorded
gap), so this base's documented order remains the renderable
form.
