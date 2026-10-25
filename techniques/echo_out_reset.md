# echo_out_reset

**Bank:** WEB-31 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** PulseDJ blog, "Ultimate Open Format DJing Guide" — the Echo Out Reset; https://blog.pulsedj.com/open-format-djing, fetched first-hand 2026-10-24.

## Signature

```python
echo_out_reset(a, b, sr, bar_s, bpm, tail_bars=2, beat_div=0.5)
```

`echo_out_reset` — family COMP (composed of `echo_out` + `hard_cut`), exit tail, energy delta 0 (release).

## Spec

Echo tail stands alone, resets the room's metronome, then B drops on a clean downbeat at any BPM.

    PulseDJ's Echo Out Reset: a heavy 1/2- or 3/4-beat echo on a
    vocal loop or melody on the outgoing deck, the channel fader
    pulled down dramatically, "a rhythmic ambient tail drifting
    through the speakers. This resets the room's internal
    metronome, allowing you to drop your new track at any BPM
    on the next clean downbeat." Best at the climax of a
    build-up or the end of a phrase; "clean palette cleanser;
    resets room expectations."

    Rendered: A plays full; then a feedback-delay tail (the
    delay line's buffered content playing out at decaying gain,
    gently darkened — the buffer holds the throw's last
    `beat_div` beats, so the tail starts immediately, with no
    silence gap); then B enters dry at full level on the next
    downbeat. The tail is the whole bridge: B is never
    underneath it. The BPM gap is unlimited by construction —
    there is no overlap in which tempos could fight.

    Why it is not its neighbours: not T-004 `echo_out` (the
    tail there covers B's entrance underneath — here the tail
    stands ALONE and B starts after it; the reset law, not the
    echo, is the technique); not T-034 `reverb_freeze` (B
    launches INSIDE the frozen tail — here B launches AFTER
    the tail, on a clean downbeat); not T-030 `hard_cut` (the
    cut alone has no metronome reset — the tail is what lets
    any-BPM drops land).

## Parameters

- `tail_bars` (int, 1–4, default 2): tail length in bars. The
  source's tail drifts "through the speakers" for a
  phrase-scale span, not a single beat.
- `beat_div` (float, 0.25–1.0, default 0.5): echo division in
  beats. 0.5 (half) is the default; 0.75 (dotted) is the
  source's second named division.

## Selection

Requires: no BPM or key gate (the reset erases both), vocal
pair any, A's phrase build / chorus / outro, genre pair same /
neighbor / leap, no needs.
Prefers: genre leap (+3, the reset exists for leaps — the tail
erases the old tempo before B drops); BPM delta ≥ 10% (+2,
large tempo gaps are where long blends fail and the reset
earns its place); A's phrase = build (+1, climax-of-buildup
placement is the source's best structural position).

## Demo

`demos/ext_genre.py`: A 8 bars, 2-bar echo tail standing alone,
B drops dry at 10 bars. Handoff = the drop. Allowed silence:
the tail's decayed portion only — the tail decays 5.19 dB per
0.234 s repeat (feedback 0.55), so from a ~-32 dBFS throw it
crosses -60 dBFS ~1.3 s into the tail and stays below it until
B drops; that decay to inaudibility IS the reset mechanism,
not a defect. The tail's first second stays gated (allowed
span starts at A_end + 1.0 s), so a tail silent from the start
still fails the battery.

## Variants

`tail_bars` × `beat_div` → 10 variants (3 tail singles, 6
pairwise combos, 1 dotted-only expansion single).
