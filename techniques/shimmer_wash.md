# shimmer_wash

**Bank:** Web-mined 2026-10-21 (WEB-10) — Pioneer RMX-1000 Reverb Up (reverb whose echo pitch rises over time) / the shimmer-reverb principle, rendered in DSP · **Automatability:** High · **Confidence:** Medium

**Source:** Pioneer RMX-1000 manual (Reverb Up / Reverb Down, via Pestrela DJ Knowledge Base) · Production Expert, "How To Create Two Specialist Reverbs" (shimmer = +12 st pitch shift before the reverb)

## Signature

`shimmer_wash` — family SPACE, exit tail, energy delta +0 (falling).

## Spec

Shimmer wash: A's tail pitch-shifted up into a long reverb,
    swelling as dry A exits; B enters under the climbing tail.

    Pioneer's RMX-1000 "Reverb Up" adds reverberation and raises the
    pitch of the echo as time passes — the shimmer-reverb principle
    (a pitch-shifted layer, classically +12 semitones, fed into the
    reverb) applied to an exit. The hardware climbs inside a feedback
    loop; this render uses the feed-forward architecture — A's final
    `swell_bars` bars are pitch-shifted by `shift_semitones` and fed
    (zero-padded, so the tail rings out naturally) into a Schroeder
    reverb — as the approximation, the same honesty convention as
    WEB-02's feed-forward flanger. The layer swells in across the
    swell region while `a` plays dry to its end, and hangs over `b`'s
    entrance (B fades in over `fade_bars`) for up to `decay_s`
    seconds.

    Parameters
    ----------
    a : outgoing segment (mono float64); its final `swell_bars`
        bars feed the shimmer layer.
    b : incoming segment (mono float64), faded in over `fade_bars`.
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    shift_semitones : layer pitch shift (default +12.0 — the
        classic octave; +7/+5 keep more of A's key for shorter
        distances. This is a diffuse reverb tail, not a vocal
        overlay — the T-032 ±2 formant rule does not apply).
    swell_bars : bars of A feeding the layer (default 4).
    level_db : layer peak level (default -12.0).
    decay_s : tail length over B in seconds (default 6.0).
    fade_bars : B's entrance fade in bars (default 2.0).

    Why it works: a plain reverb tail decays in place and keeps A's
    key center alive under B; a shimmer tail *leaves* the key center
    upward while staying unmistakably made of A — the exit reads as
    the track dissolving into light rather than stopping, and B's
    entrance is graded against a tail that is already departing.
