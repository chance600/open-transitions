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
