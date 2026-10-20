# three_deck_layer

**Bank:** T-020 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** null-set-ai-dj (MIT); glue-layer selection is curatorial; Garrix / Andy C practitioners

## Signature

```python
three_deck_layer(a, b, glue, sr, bar_s, swap_bar=16, glue_in_bars=16, glue_out_bars=16, glue_level=0.75)
```

## Spec

Two primaries + a persistent high-passed glue layer.

a owns the lows until swap_bar; b enters with lows killed and takes
full bass at the swap; glue (percussion loop / pad / chant) rides
high-passed at glue_level through the whole transition zone so the
energy floor never dips. Tri-partite frequency slotting: no two decks
own the same band.
