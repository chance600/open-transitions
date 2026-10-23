# pitch_play

**Bank:** T-032 · **Automatability:** ADOPT · **Confidence:** high

**Source:** Virtual Clubbing Life Acapella Pitch Play; |semitones| <= 2 bank rule; not formant-preserving

## Signature

```python
pitch_play(vocal, backing, sr, bar_s, semitones=1, overlay_bars=8)
```

## Spec

Shift the incoming vocal by integer semitones into the backing track's
key, then overlay it (T-010 mechanics).

|semitones| <= 2 enforced — beyond that formants shift into the
chipmunk/demonic uncanny valley (bank rule). Shift is NOT
formant-preserving (dsp.pitch_shift documents this).


## Axes (Phase 26, software/hardware tranche A)

**Chromatic PS two-voice staging (SP-404MKII)** — two
independent pitch voices (−24…+12 semitones each) over one
input: the played note plus a staged harmony voice, the
two-voice form of this base's single-line play. Evidence:
SP-404MKII Reference v5.5, Chromatic PS page, fetched
2026-10-23.

**DJ Bend momentary staging (SP-404MKII)** — pitch AND speed
coupled, momentary, with Bend Sens 10–200 as the rate law: the
nudge as a played gesture rather than a sync correction — this
base's smallest unit, fired by hand. Evidence: SP-404MKII
Reference v5.5, DJ Mode pages, fetched 2026-10-23.
