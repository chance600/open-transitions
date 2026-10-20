# spare_deck_element_firing

**Bank:** GAP-16 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Transition Gap Report 2026-10-19, GAP-16 — spare-deck element firing (James Hype: decks 3/4 as fireable element bank)

## Signature

```python
spare_deck_element_firing(a, b, sr, bar_s, bpm)
```

## Spec

Spare-deck bank fired like orchestra sections over an EQ-blend
bed: elements sit muted on decks 3/4 and are fired in real time.

Parameters
----------
a : np.ndarray, mono float64
    Outgoing primary (deck 1). Truncated/zero-padded to the
    16-bar bed.
b : np.ndarray, mono float64
    Incoming primary (deck 2), phrase-aligned with `a`. Same
    16-bar treatment.
sr : int or float
    Sample rate, Hz.
bar_s : float
    Seconds per bar (4 beats). All fire points are bar-indexed.
bpm : float
    Tempo of the pair, beats per minute (the riser element's
    ducking follows this grid).

Render (the firing schedule — muted means exactly zero gain)
-------------------------------------------------------------
Bed (bars 1-16): a staged 3-band EQ blend — B's highs open over
bars 1-4, mids over bars 5-8, the bass swap lands as a step on
bar 9's downbeat, and A's remaining bands + fader are gone by
bar 15. Deck 1 owns the lows until the swap; deck 2 after it.
Element 1 (bar 8): a synthesized riser loop is FIRED on deck 3 —
silent for bars 1-7, then a 4-bar riser (HP-swept noise + rising
tone via dsp.synth_riser, peaking -14 dB, lightly ducked 2 dB to
the kick grid for its first 2 bars) carries bars 8-11 and is cut
dead on bar 12's downbeat.
Element 2 (bar 12): a synthesized vocal one-shot is FIRED on
deck 4 — a single formant hit (2 beats with decay tail, peaking
-8 dB) exactly where the riser dies, marking the new section the
way a conductor cues the brass.

Why it works: T-020's third deck carries ONE continuous glue layer;
a spare-deck *bank* is a different instrument — discrete elements
with entrances, like orchestra sections. The bed guarantees the
groove never dips (the blend is always running underneath), while
the fired elements supply the events: the riser manufactures
tension the bed can't, and the one-shot punctuates the section
change so the crowd hears the firing as arrangement, not mixing.
Frequency discipline keeps it clean: the riser is high-passed by
construction (never fights the bed's kick), and the one-shot lives
in the vocal band the bed's EQ swap has just vacated.
ADAPT because WHICH elements to fire (and whether the room wants
them) is curatorial — the schedule and rendering are deterministic.
