# flanger_sweep

**Bank:** Web-mined 2026-10-21 (WEB-02) — DJM Colour FX "Jet" flanger sweep as a transition build/exit · **Automatability:** High · **Confidence:** High

**Source:** Pestrela DJ Knowledge Base, Effects (Jet = flanger) · Engine DJ transition-techniques course (modulation effects)

## Signature

`flanger_sweep` — family FREQ, exit snap, energy delta +1 (rising).

## Spec

Flanger sweep: a jet comb washes A's final bars; B enters dry.

    A feedback flanger is a copy of the signal delayed by a fraction of
    a millisecond to a few ms, the delay time swept slowly — the comb
    notches it carves sweep the spectrum (Pioneer's Colour FX call it
    "Jet"). Here the sweep runs across A's final `sweep_bars` with the
    wet mix ramping in over the first bar, then A hands to a completely
    dry `b` on the downbeat (3 ms seam guard only — the cut is the
    point). The two-tap feedforward comb (delay d and 2d) is the render
    approximation of the feedback original; the notch sweep, which is
    what the ear tracks, is identical.

    Parameters
    ----------
    a : outgoing segment (mono float64); the sweep zone is its final
        `sweep_bars`.
    b : incoming segment (mono float64), entered dry at len(a).
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    sweep_bars : length of the flanged zone in bars (default 8).
    cycles : full delay-sweep cycles across the zone (default 2.0 —
        slow enough to read as one rising wash per phrase half).
    depth_ms : sweep depth — delay travels base_ms .. base_ms+depth_ms
        (default 2.2 ms, the heart of the jet range).
    base_ms : minimum delay (default 0.35 ms).
    mix : wet tap strength (default 0.85).

    Why it works: the sweep is continuous spectral motion the ear
    tracks effortlessly, and comb cancellation thins A's perceived
    body without touching the fader — so when B arrives unprocessed
    and full-bodied, the contrast lands like a physical entrance.
