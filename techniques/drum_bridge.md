# drum_bridge

**Bank:** T-022 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT); strip is a full-mix approximation — stems are exact

## Signature

```python
drum_bridge(a, b, sr, bar_s, strip_bars=4, interlude_bars=12, blend_bars=8)
```

## Spec

Strip A to drums (key-neutral zone), hold the interlude, blend B in.

a: outgoing, length strip_bars + interlude_bars (caller provides).
The strip is a full-mix approximation (HPF + mid kill); with stems the
caller passes the drum stem for exactness.
In the absence of pitched material the ear cannot perceive key — B can
be ANY Camelot. B's drums layer over A's, then A cuts as B's melody
enters.
