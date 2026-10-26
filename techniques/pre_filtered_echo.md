# pre_filtered_echo

**Bank:** WEB-22 · **Automatability:** ADAPT · **Confidence:** medium

**Source:** Mixxx 2.5 Manual, Ch. 11 Effects — the Dry+Wet worked example (filter before Echo in a serial chain; dry at full volume), fetched first-hand 2026-10-23.

## Signature

```python
pre_filtered_echo(a, b, sr, bpm, bar_s, beat_div=0.5, cutoff_hz=300.0, feedback=0.55, wet=0.6, tail_beats=4)
```

`pre_filtered_echo` — family SPACE, exit tail, energy delta 0 (falling).

## Spec

Echo throw whose SEND is band-shaped; the dry never ducks.

    The Mixxx 2.5 manual's Dry+Wet worked example (Ch. 11): a filter
    placed BEFORE the Echo in a serial chain, with the unit in
    Dry+Wet mode, so "the filter or equalizer can remove bass
    frequencies from the echoed signal without removing them from
    the unechoed signal" — and "in Dry+Wet mode, the dry signal is
    always at full volume."

    Rendered as a transition: A's final beat is thrown exactly as
    in `echo_out` (T-004), but the signal entering the delay is a
    lowpassed copy (cutoff_hz), shaped ONCE at the send, outside
    the feedback loop — so repeat 1 is already bass-less and the
    repeats do NOT progressively darken. The dry path is additive
    (Dry+Wet law): A plays at full level and full spectrum to its
    end, and the shaped tail rings over B's entrance on top.

    Why it is not its neighbours: `echo_out`'s send is full-spectrum
    and its law is substitution (gated dry + wet series);
    `aging_echo` (CMP-01) puts the lowpass INSIDE the loop, so
    repeat k is filtered k times and repeat 1 is bright. Here the
    conditioning is at the send and the dry is preserved — the
    complementary topology of the same family.

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (sets the delay grid).
    bar_s : seconds per bar (signature parity with the SPACE family).
    beat_div : delay time in beats (default 0.5).
    cutoff_hz : send lowpass (default 300 Hz — bass removed from
        every repeat, kept in the dry).
    feedback : loop gain per repeat (default 0.55).
    wet : tail level in the mix (default 0.6).
    tail_beats : pure-tail length past A's end (default 4 beats).

    Returns a mono float64 mix of length len(a) + len(b).

## Axes (Phase 32, Class 5 tranche B)

**Pre- vs post-delay filter placement (Xone:PX5 delays)** —
the Xcite delays disagree about where the filter sits, and the
disagreement is the lesson: PCM DELAY filters PRE-delay ("the
filter section is pre-delay allowing one to shape the frequency
focus of the decay trails"), while MASIF-Q and FILTER DELAY
filter POST-delay (MASIF-Q's extended sweep range "especially
suited for focusing the delay on individual track elements";
FILTER DELAY adds a frequency-conscious limiter that pushes
back on dense-input trails). The staging for this base's
send-side conditioning: pre-delay filtering shapes what ENTERS
the loop (every repeat inherits it); post-delay filtering
shapes what LEAVES it (the loop's own evolution survives).
Evidence: Xone:PX5 FX Notes V1.00 (Nov 2016), MASIF-Q / PCM /
FILTER DELAY entries, fetched 2026-10-26.
