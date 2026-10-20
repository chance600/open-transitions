# hook_drop_handoff

**Bank:** T-038 · **Automatability:** ADOPT · **Confidence:** field-tested

**Source:** original — distilled from blend 01 workshopping (v9-v18); v14 = user-approved keeper, v17 = 'Awesome, yes'

## Signature

```python
hook_drop_handoff(a, b, sr, bar_s, exit_fade_ms=70.0, bloom_bars=3, bloom_offset_ms=0.0, bloom_curve='sqrt')
```

## Spec

Outgoing track's signature vocal hook is the final event; incoming
blooms in as texture AT the drop point. No verse runway, no dead air.

Parameters
----------
a : outgoing segment, ENDS exactly on the hook's phrase boundary
    (caller aligns: the hook's final syllable is a's last sample).
b : incoming segment, STARTS on its phrase beginning (never mid-groove).
exit_fade_ms : protective fade on a's tail, 60-80 ms cosine to hard zero.
    Click avoidance only — not an audible fade.
bloom_bars : incoming bloom duration in bars (2-4). Texture first, then
    takes over.
bloom_offset_ms : bloom start relative to the drop point. 0 = at the
    drop; negative tucks the bloom under the exit fade (variant).
bloom_curve : "sqrt" (default) or "linear". NEVER cosine — a cosine
    fade-in sits at ~0.8% amplitude after 80 ms and reads as dead air
    (v17 lesson); sqrt is at ~24% by 80 ms, so there is zero perceived
    gap. The drop's punch comes from the vocal hard-zero, not silence.

Banked rule: the blend lives in the entrance; the drop lives in the
exit. A fading outgoing lead over a blooming texture reads as
indecisive; a hard exit over a blooming entrance reads as a statement.
