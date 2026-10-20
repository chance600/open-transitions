# eq_blend

**Bank:** T-001 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj Transition Cookbook (MIT), MusicRadar, mixingguide.com

## Signature

```python
eq_blend(a, b, sr, bar_s, blend_bars=32)
```

## Spec

Long harmonic EQ blend. a and b should each be blend_bars long.

Canonical 32-bar shape (breakpoints scale as fractions of blend_bars):
Bars 1-8:   B high kill->open,  A high 0->-8 dB
Bars 9-16:  B mid  kill->open,  A mid  0->-8 dB
Bar 17 beat 1: bass swap (instant)
Bars 17-24: A highs/mids -> kill, A fader -> 0
Bars 25+:   B alone
