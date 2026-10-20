# echo_out

**Bank:** T-004 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT), DJ Carlo Atendido, MusicRadar

## Signature

```python
echo_out(a, sr, bpm, beat_div=0.5, wet=0.6, feedback=0.55, tail_beats=4)
```

## Spec

Echo throw on the final beat of `a`, post-fader tail.

- Low EQ killed over the throw beat (avoids boomy rumble).
- Input gate cuts at the throw (fader to 0); feedback loop rings on.
- Returns a + tail_beats of pure tail appended.
