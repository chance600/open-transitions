# acapella_overlay

**Bank:** T-010 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** null-set-ai-dj (MIT); phrase selection + fader riding are human

## Signature

```python
acapella_overlay(a, b_vocal, sr, bar_s, overlay_bars=16, phrase_windows=None)
```

## Spec

Sing B's vocal over A's instrumental.

b_vocal: acapella or stem-isolated vocal. EQ preset: lows killed,
    highs tamed (-2 dB), mids flat. Key Lock assumed (caller's domain).
overlay_bars: overlay window; gentle 2-bar fades each end.
phrase_windows: optional list of (start_bar, end_bar, gain) — the
    manual fader ride ("up when the singer sings"). Without it, the
    overlay is a fixed bed; the ride remains a human-feel judgment.
Never overlay on A's vocal — the caller guarantees a vocal-free window.
