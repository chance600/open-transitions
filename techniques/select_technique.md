# select_technique

**Bank:** T-037 · **Automatability:** ADOPT · **Confidence:** high

**Source:** bank synthesis: rejection rules prune first, decision table picks

## Signature

```python
select_technique(f)
```

## Spec

Choose the technique from the musical situation.

f: feature dict —
    bpm_delta_pct   float: |BPM_B - BPM_A| / BPM_A * 100
    half_double_ok  bool:  exact 2x/1x ratio available
    camelot_distance int:  0 (same) / 1 (+-1 or relative) / 2-3 / 4+ (clash)
    energy_delta    float: energy_B - energy_A on a 1-10 scale
    phrase_a        str:   breakdown / outro / build / drop / verse / chorus
    vocal           str:   "a_only" / "b_only" / "both" / "neither"
    genre_pair      str:   "same" / "neighbor" / "leap"
    b_has_build     bool
    a_has_breakdown bool
    iconic_vocal    str:   "a" / "b" / None  (signature hook available)
    b_intro_bars    int:   usable intro length of B in bars
    drop_pair_ok    bool:  two drops complement (<=1 vocal), for T-024

Selection is constraint satisfaction: rejection rules prune first
(most trainwrecks come from blending where a cut was required), the
decision table picks among survivors. Returns
{"technique": id, "reasons": [...], "rejected": {...},
 "alternatives": [...]}.
NOTE: the table may return "build_to_drop" (T-009 dual-build layering),
which is choreography-specified but not yet implemented in the engine —
treat it as a plan flag and render with "loop_roll_build" until it lands.
A deliberate human contrast choice may overrule this output.
