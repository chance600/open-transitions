# reverb_wash

**Bank:** T-005 · **Automatability:** ADOPT · **Confidence:** high

**Source:** null-set-ai-dj (MIT), MusicRadar

## Signature

```python
reverb_wash(a, b, sr, bar_s, wash_start_bar=4, b_start_bar=6, wet_max=0.7)
```

## Spec

Dissolve `a` into reverb from wash_start_bar; `b` emerges at b_start_bar.

a: outgoing segment (bars). b: incoming segment, aligned so its bar 0
coincides with a's b_start_bar.

## Axes (Phase 32, Class 5 tranche B)

**Attack-gated reverb (Xone:PX5 ATTACK GATE)** — a gated
reverb whose attack envelope the DJ controls, "for creating
dramatic reverse swells, and extended pre-delay time for
pushing and pulling the effect in and out of the beat grid":
INTERVAL at minimum, DECAY at minimum, FOCUS at 12 o'clock,
then interval spun out past 300 ms until it overlaps the beat,
decay unwound to maximum to stretch the reverb and slow down
time. The staging for this base's wash: gate the reverb's
ATTACK, not just its decay — a wash that swells backwards
into the seam reads as a reverse cymbal, not a room.
Evidence: Xone:PX5 FX Notes V1.00 (Nov 2016), ATTACK GATE
entry, fetched 2026-10-26.
