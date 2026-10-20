# double_drop

**Bank:** T-024 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** null-set-ai-dj (MIT); drop-pair complementarity is curatorial

## Signature

```python
double_drop(a, b, sr, bar_s, drop_at_bar=16, drop_bars=16)
```

## Spec

Two builds converge on ONE downbeat. Single-sub-bass rule enforced:
B's lows stay killed through the drop; bass swaps after drop_bars.

a, b: build+drop segments, SAME length, builds starting together
    (caller aligns). drop_at_bar: bar index (0-based) of the drop.
Prerequisite (caller's taste call): at most ONE drop carries a vocal.
