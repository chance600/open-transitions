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


## Axes (Phase 26, software/hardware tranche A)

**Four-band asymmetric staging (Xone:96)** — the 96's channel
EQ is four bands with asymmetric law: HI 3 kHz and LO 180 Hz at
+6 dB / full kill; HI-MID 1.1 kHz and LO-MID 350 Hz at
+10 / −27 dB. Staged on this base: the bass hand-off splits into
TWO events — LO-MID (350 Hz) trades first, the true kill waits
for LO (180 Hz) — and the midrange gets its own two-step trade
at 350/1100 instead of sharing the single MID knob's arc. The
aux channels' swept parametric MID (190 Hz–2.75 kHz, +10/−24)
is the return-path form of the same idea. Evidence: Xone:96
User Guide (official support HTML), fetched 2026-10-23.

**DJM-V10 four-band + master isolator staging** — Pioneer's
flagship gives the same four-band idea different numbers:
HI 2 kHz and LOW 200 Hz kill to −∞ with +6 dB boost; HI MID
1.2 kHz and LOW MID 400 Hz floor at −26 dB with +6 dB. And
where the 96 has NO master processing at all, the V10 adds a
3-band MASTER ISOLATOR — every band −∞ to +9 dB — staged on
the SUMMED mix: this base fired on both tracks at once, the
whole programme's low end killed and returned as one gesture.
Crossover frequencies are stated nowhere in the manual
(recorded gap); renders use registry-standard crossovers.
Evidence: DJM-V10 manual via manua.ls, pp27/34 + specs p82,
fetched 2026-10-23.

## Axes (Phase 32, Class 5 tranche B)

**Xone:92 four-band law** — the 92's EQ is four bands with an
asymmetric-Q rule the two flagship laws do not state: +6 dB
boost on every band, infinite kill (total attenuation, sharp
12 dB/oct roll-off) on HI and LO, a massive -30 dB of cut on the
two MIDs — and wide Q for cut, narrow Q for boost, so a cut
scoops broadly while a boost highlights narrowly. The staging
for this base's four-band form: cuts are the blend tool (broad,
forgiving), boosts are the highlight tool (narrow, deliberate) —
never the reverse. Evidence: Xone:92 User Guide p. 7 (manualsdir
mirror), fetched 2026-10-26.
