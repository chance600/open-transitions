"""
open-transitions engine — hardware/software domain module (Phase 26).

Expansion tranche 5 (V2 queue item 4): the Class 5 software/hardware
remainder, tranche A — six free/public doc bodies mined first-hand:
Mixxx 2.5 Manual Ch. 11 (Effects), Algoriddim djay Pro Neural Mix
docs, VirtualDJ Stems 2.0 manual pages, the Roland SP-404MKII
Reference v5.5 (BUS FX cluster + all 46 MFX pages + DJ Mode
cluster), the Allen & Heath Xone:96 User Guide (official support
HTML), and the Pioneer DJM-V10 manual via the manua.ls mirror (the
official Pioneer PDF is login-walled; mirror facts are labelled).

Admitted bases (bank WEB-22..WEB-29):

  WEB-22 pre_filtered_echo   Mixxx Dry+Wet: filter at the echo SEND,
                             outside the loop; dry pinned at full
  WEB-23 notch_carve_sweep   Xone:96 dual state-variable VCF: HPF+LPF
                             summed = a travelling notch carve
  WEB-24 phaser_sweep        SP-404MKII Phaser / Xone all-pass sum:
                             allpass cascade, magnitude-flat sweep
  WEB-25 stem_swap_replace   VirtualDJ StemSwap: a captured stem loop
                             replaces the host's corresponding stem
  WEB-26 djfx_microloop      SP-404MKII DJFX Looper: free-time
                             12-230 ms grain loop, varispeed through
                             zero (forward / stop / backward)
  WEB-27 cyclic_speed_dip    SP-404MKII Downer: tempo-period cyclic
                             playback-rate dip with HF tracking
  WEB-28 pattern_gate_slicer SP-404MKII Slicer (+ DJM-V10 TRANS duty
                             staging): preset 16-step gate pattern
  WEB-29 sideband_comb_filter SP-404MKII SBF: scalable comb of
                             narrow bandpass bands

Phase 32 (Class 5 tranche B, 2026-10-26) adds the remainder of
V2 queue item 4, all from free/public mirrors and docs:

  WEB-40 sculpt_bell_sweep   PLAYdifferently MODEL 1 Sculpt EQ:
                             travelling parametric bell, +8 boost /
                             -20 cut over ~7 octaves
  WEB-41 lfo_filter_sweep    Xone:92 LFO modulation: cyclic filter
                             cutoff oscillation, TAP rate, DEPTH ramp
  WEB-42 linked_filter_handover  Xone:92 VCF LINK 2-1: one cutoff joins
                             A's lows to B's highs, travelling down

Conventions follow engine/techniques.py: numpy mono float64 in/out,
timing in bars/beats, the docstring IS the spec source
(techniques/*.md mirror it). Synthesized sketch audio only.
"""

import numpy as np
from scipy import signal

from . import dsp

KILL_DB = -60.0  # mirrors engine/techniques.py convention


def _lp(x, sr, cutoff_hz):
    """2nd-order Butterworth lowpass, zero-phase-free (causal)."""
    b, a = signal.butter(2, min(cutoff_hz, sr * 0.45) / (sr / 2.0),
                         btype="low")
    return signal.lfilter(b, a, x)


def _eq_power_pair(n):
    """(fade_out, fade_in) equal-power envelopes of length n."""
    u = np.linspace(0.0, 1.0, max(n, 1))
    return np.cos(0.5 * np.pi * u), np.sin(0.5 * np.pi * u)


# ----------------------------------------------------------------------------
# WEB-22 — Pre-filtered echo (Mixxx Dry+Wet send conditioning)
# ----------------------------------------------------------------------------

def pre_filtered_echo(a, b, sr, bpm, bar_s, beat_div=0.5,
                      cutoff_hz=300.0, feedback=0.55, wet=0.6,
                      tail_beats=4):
    """Echo throw whose SEND is band-shaped; the dry never ducks.

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
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = bar_s / 4.0
    beat_n = int(round(beat_s * sr))
    throw_n = beat_n  # the throw is A's final beat, as in T-004
    throw0 = max(0, len(a) - throw_n)
    tail_n = int(round(tail_beats * beat_s * sr))

    # Shape the send: filter the throw with one beat of context so
    # the filter's edge transient lands before the throw itself.
    ctx0 = max(0, throw0 - beat_n)
    shaped = _lp(a[ctx0:], sr, cutoff_hz)[throw0 - ctx0:]

    send_ext = np.zeros(len(a) + tail_n)
    send_ext[throw0:throw0 + len(shaped)] = shaped
    series = dsp.feedback_delay(send_ext, sr, beat_div * beat_s,
                                feedback=feedback, wet=1.0)
    wet_line = (series - send_ext) * wet  # repeats only, from +1 div

    out = np.zeros(len(a) + len(b))
    out[:len(a)] += a
    out[len(a):] += b
    m = min(len(wet_line), len(out))
    out[:m] += wet_line[:m]
    return out


# ----------------------------------------------------------------------------
# WEB-23 — Notch carve sweep (Xone:96 dual state-variable VCF)
# ----------------------------------------------------------------------------

def notch_carve_sweep(a, b, sr, bpm, bar_s, sweep_bars=4, q=8.0,
                      fade_bars=1):
    """A travelling spectral hole carves A away; B enters clean.

    The Xone:96's filters are state-variable: they "provide three
    simultaneous filter response output types: High-Pass (HPF),
    Band-Pass (BPF) and Low-Pass (LPF)... Any combination can be
    pressed together to create different response types such as
    'notch'". Summing the HPF and LPF outputs gives a notch: full
    energy everywhere except a rejection band at FREQ, its width
    set by RES.

    Rendered as a transition: across A's final `sweep_bars` the
    notch centre log-ramps 60 Hz -> 15 kHz. The track thins
    locally and reversibly — when the hole crosses the kick band
    the kick vanishes and returns; when it crosses the vocal band
    the vocal does — instead of the monotonic thinning of
    `filter_sweep` (T-003). At the top of the band the notch exits
    the spectrum (transparent) as B fades in over `fade_bars`.

    Why it is not its neighbours: not T-003 (a monotonic slope,
    energy removed on one side forever); not `eq_blend` (fixed
    band gains at fixed frequencies — no travelling hole, no
    resonance); not `resonator_tail` WEB-18 (a ringing decay tail,
    not a rejection band in a continuing signal); not
    `flanger_sweep` WEB-02 (delay-comb notches are periodic and
    multiple — this is a single state-variable rejection band).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    sweep_bars : carve window at A's end (default 4).
    q : notch Q from the RES staging (default 8.0; MILD ~ wide,
        WILD ~ needle — the guide gives no numeric Q, the mapping
        is an implementation choice, stated here).
    fade_bars : B's entrance crossfade at the seam (default 1).

    Returns a mono float64 mix of length len(a) + len(b) - fade.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    win_n = min(len(a), sweep_bars * bar_n)
    fade_n = min(bar_n * fade_bars, len(b), win_n)

    out_a = a.copy()
    if win_n > 0:
        seg = a[-win_n:]
        y = np.zeros(win_n)
        zi = np.zeros(2)
        block = 1024
        f0 = np.exp(np.linspace(np.log(60.0), np.log(15000.0), win_n))
        for s in range(0, win_n, block):
            e = min(s + block, win_n)
            w0 = float(np.mean(f0[s:e])) / (sr / 2.0)
            w0 = min(max(w0, 0.002), 0.95)
            bb, aa = signal.iirnotch(w0, q)
            y[s:e], zi = signal.lfilter(bb, aa, seg[s:e], zi=zi)
        out_a[-win_n:] = y

    out = np.zeros(len(a) + len(b) - fade_n)
    out[:len(a)] += out_a
    if fade_n > 0:
        fo, fi = _eq_power_pair(fade_n)
        out[len(a) - fade_n:len(a)] *= fo
        out[len(a) - fade_n:len(a)] += b[:fade_n] * fi
        out[len(a):] += b[fade_n:]
    else:
        out[len(a):] += b
    return out


# ----------------------------------------------------------------------------
# WEB-24 — Phaser sweep (SP-404MKII Phaser / Xone all-pass sum)
# ----------------------------------------------------------------------------

def _allpass_cascade(x, sr, fc_env, stages):
    """First-order allpass sections in cascade, per-block fc."""
    y = np.asarray(x, dtype=np.float64)
    block = 1024
    for _ in range(stages):
        out = np.zeros(len(y))
        zi = np.zeros(1)
        for s in range(0, len(y), block):
            e = min(s + block, len(y))
            fc = float(np.mean(fc_env[s:e]))
            fc = min(max(fc, 20.0), sr * 0.45)
            t = np.tan(np.pi * fc / sr)
            c = (t - 1.0) / (t + 1.0)
            seg, zi = signal.lfilter([c, 1.0], [1.0, c], y[s:e],
                                     zi=zi)
            out[s:e] = seg
        y = out
    return y


def phaser_sweep(a, b, sr, bpm, bar_s, sweep_bars=4, rate_bars=1.0,
                 stages=4, fade_bars=1):
    """Magnitude-flat phase movement carries the seam.

    Two vendor attestations of one topology: the SP-404MKII's
    Phaser "creates modulation by adding a phase-shifted sound"
    (allpass network; DEPTH/RATE/MANUAL/RESONANCE, RATE syncable),
    and the Xone:96's state-variable sum giving "interesting
    'all-pass' effects" — flat magnitude, frequency-dependent
    phase rotation around FREQ.

    Rendered as a transition: across A's final `sweep_bars`, A is
    mixed with a cascade of `stages` allpass sections whose break
    frequency oscillates (period `rate_bars` bars, centre 800 Hz,
    ±1.2 octaves). The moving phase interference hollows the
    texture cyclically while the spectrum and loudness stay put —
    the track moves without thinning — then B fades in over
    `fade_bars` as the sweep parks.

    Why it is not its neighbours: not `flanger_sweep` WEB-02 (a
    modulated DELAY line: comb magnitude response, harmonic notch
    spacing, feedback whistle) — an allpass cascade's notches are
    non-harmonic and there is no delay line; not
    `formant_morph_exit` WEB-17 (formant peaks MOVE — magnitude
    changes by design; here magnitude is flat by construction).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    sweep_bars : phased window at A's end (default 4).
    rate_bars : LFO period in bars (default 1.0).
    stages : allpass sections (default 4).
    fade_bars : B's entrance crossfade (default 1).

    Returns a mono float64 mix of length len(a) + len(b) - fade.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    win_n = min(len(a), sweep_bars * bar_n)
    fade_n = min(bar_n * fade_bars, len(b), win_n)

    out_a = a.copy()
    if win_n > 0:
        seg = a[-win_n:]
        t = np.arange(win_n) / sr
        phase = 2.0 * np.pi * t / (rate_bars * bar_s)
        fc_env = 800.0 * (2.0 ** (1.2 * np.sin(phase)))
        ap = _allpass_cascade(seg, sr, fc_env, stages)
        phased = 0.5 * seg + 0.5 * ap
        # wet ramps in over the window's first bar, holds, and the
        # seam crossfade (below) carries the exit
        ramp_n = min(bar_n, win_n)
        env = np.ones(win_n)
        env[:ramp_n] = np.linspace(0.0, 1.0, ramp_n)
        out_a[-win_n:] = seg * (1.0 - env) + phased * env

    out = np.zeros(len(a) + len(b) - fade_n)
    out[:len(a)] += out_a
    if fade_n > 0:
        fo, fi = _eq_power_pair(fade_n)
        out[len(a) - fade_n:len(a)] *= fo
        out[len(a) - fade_n:len(a)] += b[:fade_n] * fi
        out[len(a):] += b[fade_n:]
    else:
        out[len(a):] += b
    return out


# ----------------------------------------------------------------------------
# WEB-25 — Stem swap replace (VirtualDJ StemSwap)
# ----------------------------------------------------------------------------

def _stem(stems, name, n):
    x = (stems or {}).get(name)
    if x is None:
        return np.zeros(n)
    x = np.asarray(x, dtype=np.float64)
    if len(x) >= n:
        return x[:n]
    return np.pad(x, (0, n - len(x)))


def stem_swap_replace(a_stems, b_stems, sr, bar_s,
                      swap_stems=("drums",), loop_bars=2,
                      start_bar=4, swap_bars=8, tail_bars=4):
    """A captured stem loop replaces the host's own stem, gated.

    VirtualDJ's StemSwap sampler: a pad records a stem-selected
    loop from one track; triggered on the deck playing another,
    "stems samples from a StemSwap bank will mute the
    corresponding stem from the track playing on the deck where
    the sample was triggered, effectively 'swapping' the stems."

    Rendered: B plays full for `start_bar` bars. For `swap_bars`
    bars, B's `swap_stems` are muted and A's same stems — captured
    as a `loop_bars` loop, decoupled from A's playhead — play in
    their place through B's timeline. When the gate ends, B's own
    stems return (3 ms guards at the gate edges); B plays out for
    `tail_bars` bars. The swap is a sustained substitution inside
    one host track, not a handover: nothing requires the mix to
    move to A.

    Why it is not its neighbours: not GAP-08
    `stem_element_crossfade` (two linear playheads, a staged
    16-bar progressive handover — here the donor is a captured
    loop, the replacement instantaneous, trigger-gated and
    reversible); not GAP-16 `spare_deck_element_firing`
    (synthesised elements ADDED over an EQ bed — nothing is muted
    and nothing is captured); not WEB-21 `drop_insert` (the whole
    MIX is substituted at a drop downbeat — here only the named
    stems, inside a continuing host).

    Parameters
    ----------
    a_stems, b_stems : dicts {"drums","bass","melody","vocal"}.
    sr : sample rate (Hz). bar_s : seconds per bar.
    swap_stems : stem names replaced (default ("drums",)).
    loop_bars : captured loop length in bars (default 2).
    start_bar : bar where the gate opens (default 4).
    swap_bars : gate length in bars (default 8).
    tail_bars : B plays out after the gate (default 4).

    Returns a mono float64 mix of (start+swap+tail) bars.
    """
    bar_n = int(round(bar_s * sr))
    total_bars = start_bar + swap_bars + tail_bars
    n = total_bars * bar_n
    g0 = start_bar * bar_n
    g1 = (start_bar + swap_bars) * bar_n
    guard = max(1, int(0.003 * sr))
    mix = np.zeros(n)
    names = dict.fromkeys(list(a_stems or {}) + list(b_stems or {}))
    for name in names:
        bst = _stem(b_stems, name, n)
        if name in swap_stems:
            ast = _stem(a_stems, name, loop_bars * bar_n)
            win = np.tile(ast, int(np.ceil(swap_bars / loop_bars)))
            win = win[:swap_bars * bar_n]
            gb = np.ones(n)
            gb[g0:g1] = 0.0
            gb[g0 - guard:g0] = np.linspace(1.0, 0.0, guard)
            gb[g1:g1 + guard] = np.linspace(0.0, 1.0, guard)
            ga = np.zeros(n)
            ga[g0:g1] = 1.0
            ga[g0 - guard:g0] = np.linspace(0.0, 1.0, guard)
            ga[g1:g1 + guard] = np.linspace(1.0, 0.0, guard)
            layer = np.zeros(n)
            layer[g0 - guard:g1 + guard] = 1.0
            seg = np.zeros(n)
            seg[g0:g1] = win
            # donor sounds only inside the (guarded) gate span
            mix += bst * gb + seg * ga
        else:
            mix += bst
    return mix


# ----------------------------------------------------------------------------
# WEB-26 — DJFX microloop (SP-404MKII DJFX Looper)
# ----------------------------------------------------------------------------

def djfx_microloop(a, b, sr, bpm, bar_s, length_ms=120.0,
                   mode="reverse", loop_bars=2, fade_beats=1):
    """A 12-230 ms grain of A, performed like a turntable.

    The SP-404MKII's DJFX Looper "loops the sound in short cycles.
    You can vary the playback direction and playback speed of the
    input sound to get a turntable-type effect": LENGTH is
    0.230-0.012 SECONDS (absolute time, not a beat grid) and SPEED
    is -100..100 — "plays backward when negative, stops when
    zero, plays forward when positive".

    Rendered as a transition: A's final `loop_bars` are replaced
    by the performance. The grain — A's last `length_ms` before
    the window — loops while the read rate sweeps by `mode`:
    "reverse" sweeps +1 -> -1 (through the stop instant into
    backward play), "stop" eases +1 -> 0 (the grain crawls to a
    standstill), "hold" parks the rate at +0.25 (a slow drag of
    the same grain). B then enters, faded over `fade_beats`.

    Why it is not its neighbours: not `loop_roll_build` T-008 (a
    beat-quantised roll that TIGHTENS through subdivisions — it
    never runs at sub-beat absolute lengths, never reverses, never
    freezes at rate 0); not `granular_freeze` WEB-06 (a sustained
    texture cloud — no directional varispeed performance of a
    single captured grain); not `backspin` T-007 (a one-shot
    reverse gesture on the whole record, not a captured loop).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity; the
        grain length is deliberately NOT derived from it).
    bar_s : seconds per bar.
    length_ms : grain length in milliseconds (default 120; the
        hardware range is 12-230).
    mode : "reverse" | "stop" | "hold" (default "reverse").
    loop_bars : performance window in bars (default 2).
    fade_beats : B's entrance fade in beats (default 1).

    Returns len(a) - loop window + loop window + len(b) samples.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    beat_n = int(round(bar_s / 4.0 * sr))
    loop_n = min(len(a), loop_bars * bar_n)
    cap_end = len(a) - loop_n
    grain_n = max(16, int(round(length_ms / 1000.0 * sr)))
    grain = a[max(0, cap_end - grain_n):cap_end]
    if len(grain) < grain_n:
        grain = np.pad(grain, (grain_n - len(grain), 0))
    u = np.linspace(0.0, 1.0, loop_n)
    if mode == "stop":
        rate = (1.0 - u) ** 1.5
        rate = np.maximum(rate, 0.02)
    elif mode == "hold":
        rate = np.full(loop_n, 0.25)
    else:  # reverse
        rate = 1.0 - 2.0 * u
    pos = np.cumsum(rate)
    idx = np.mod(pos, grain_n)
    loop = np.interp(idx, np.arange(grain_n), grain)

    fade_n = min(beat_n * fade_beats, len(b))
    b_head = b.copy()
    if fade_n > 0:
        _, fi = _eq_power_pair(fade_n)
        b_head[:fade_n] *= fi
    return np.concatenate([a[:cap_end], loop, b_head])


# ----------------------------------------------------------------------------
# WEB-27 — Cyclic speed dip (SP-404MKII Downer)
# ----------------------------------------------------------------------------

def cyclic_speed_dip(a, b, sr, bpm, bar_s, dip_bars=8,
                     rate_beats=4.0, depth=0.45,
                     pitch_correct=False, fade_bars=1):
    """Playback rate dipped cyclically, on a tempo-period LFO.

    The SP-404MKII's Downer "cyclically slows down the audio
    playback speed": RATE is musical (2/1..1/32), DEPTH sets how
    far the rate falls, FILTER attenuates HF as the speed drops,
    and PITCH ON converts the lowered pitches back ("pitches
    lowered due to the change in speed are converted to their
    original pitch") — a time-stretch dip instead of varispeed.

    Rendered as a transition: across A's final `dip_bars`, the
    playback rate follows rate(t) = 1 - depth * pulse(t), the
    pulse a raised cosine with period `rate_beats` beats on the
    output clock. The segment LENGTHENS (it is consumed slower);
    a lowpass tracks the instantaneous rate, so each dip darkens
    as it sags. With pitch_correct=True each period-chunk is
    phase-vocoder stretched to its dipped duration instead, so
    the tempo sags but the pitch holds. B fades in over
    `fade_bars` at the end of the dipped segment.

    Why it is not its neighbours: not `brake_stop` T-006 (a
    ONE-SHOT terminal deceleration — this returns to full rate
    every period and never stops); not `screwed_treatment` T-039
    (a static drag at one rate); not `tempo_bridge` T-021 (a
    one-way ramp between two tempos — this oscillates around one).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (clocks the LFO).
    bar_s : seconds per bar.
    dip_bars : dipped window at A's end (default 8).
    rate_beats : LFO period in beats (default 4).
    depth : rate-fall fraction (default 0.45).
    pitch_correct : Downer's PITCH ON (default False).
    fade_bars : B's entrance crossfade (default 1).

    Returns a mix whose A part is longer than A's dipped window
    by ~1/(1 - depth/2); total = len(a) - window + dipped + len(b).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    beat_s = bar_s / 4.0
    win_n = min(len(a), dip_bars * bar_n)
    seg = a[len(a) - win_n:]
    head = a[:len(a) - win_n]
    period_s = rate_beats * beat_s

    def pulse(t):
        return 0.5 - 0.5 * np.cos(2.0 * np.pi * t / period_s)

    if pitch_correct:
        # per-period PV stretch: chunk k is stretched to the
        # duration its mean rate implies, pitch preserved
        chunk_n = max(1024, int(round(period_s * sr)))
        pieces = []
        for s in range(0, win_n, chunk_n):
            chunk = seg[s:s + chunk_n]
            tt = (s + np.arange(len(chunk))) / sr
            r_mean = float(np.mean(1.0 - depth * pulse(tt)))
            r_mean = min(max(r_mean, 0.2), 1.0)
            pieces.append(dsp.phase_vocoder_stretch(
                chunk, sr, 1.0 / r_mean))
        join = max(1, int(0.005 * sr))
        dipped = pieces[0]
        for p in pieces[1:]:
            fo, fi = _eq_power_pair(join)
            merged = np.concatenate([dipped[:-join],
                                     dipped[-join:] * fo
                                     + p[:join] * fi,
                                     p[join:]])
            dipped = merged
    else:
        mean_rate = 1.0 - depth * 0.5
        out_n = int(round(win_n / mean_rate))
        t_out = np.arange(out_n) / sr
        rate_env = 1.0 - depth * pulse(t_out)
        pos = np.cumsum(rate_env)
        pos *= (win_n - 1) / max(pos[-1], 1.0)
        dipped = np.interp(pos, np.arange(win_n), seg)
        fc_env = np.clip(14000.0 * rate_env, 800.0, 16000.0)
        dipped = dsp.sweep_filter(dipped, sr, fc_env,
                                   ftype="lowpass", q=0.707)

    fade_n = min(bar_n * fade_bars, len(b), len(dipped))
    body = np.concatenate([head, dipped])
    if fade_n > 0:
        fo, fi = _eq_power_pair(fade_n)
        out = np.zeros(len(body) + len(b) - fade_n)
        out[:len(body)] += body
        out[len(body) - fade_n:len(body)] *= fo
        out[len(body) - fade_n:len(body)] += b[:fade_n] * fi
        out[len(body):] += b[fade_n:]
        return out
    return np.concatenate([body, b])


# ----------------------------------------------------------------------------
# WEB-28 — Pattern gate slicer (SP-404MKII Slicer; DJM-V10 TRANS duty)
# ----------------------------------------------------------------------------

_PATTERNS = {
    # 16-step level tables (1 = step sounds at full, 0 = silenced
    # before depth scaling). Roland does not publish its 32 tables
    # (a recorded gap); these are the registry's own stagings of
    # the documented mechanism.
    "offbeat": [0.15, 0.15, 1.0, 0.15, 0.15, 0.15, 1.0, 0.15,
                0.15, 0.15, 1.0, 0.15, 0.15, 0.15, 1.0, 0.15],
    "pulse": [1.0, 0.2, 0.2, 0.2, 1.0, 0.2, 0.2, 0.2,
              1.0, 0.2, 0.2, 0.2, 1.0, 0.2, 0.2, 0.2],
    "cascade": [1.0, 0.94, 0.88, 0.81, 0.75, 0.69, 0.63, 0.56,
                0.5, 0.44, 0.38, 0.31, 0.25, 0.19, 0.13, 0.06],
    "stutter": [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0,
                1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0],
}


def pattern_gate_slicer(a, b, sr, bpm, bar_s, pattern="offbeat",
                        step_beats=0.25, depth=1.0, shuffle=0.0,
                        mode="slash", gate_bars=4, fade_beats=2):
    """A preset 16-step gate pattern imposed on the live track.

    The SP-404MKII's Slicer "slices the sound up into small pieces
    ... slices up the sound at certain intervals into 16 parts
    (16 steps) ... a rhythm that follows the sequence pattern":
    PATTERN selects a 16-step level table, SPEED the step grid
    (syncable 2/1..1/64T), DEPTH the gate depth, SHUFFLE delays
    the even-numbered steps (swing), and MODE is LEGATO (level
    holds across steps) or SLASH ("volume is reset to zero before
    the next step sounds"). The audio is NOT reordered and NOT
    resampled — a pattern of gain is imposed in place. Pioneer's
    DJM-V10 TRANS is the same family's duty form ("cuts the sound
    cyclically according to the beat", LEVEL/DEPTH setting
    balance AND duty): a pattern whose open steps form one
    contiguous block per cycle.

    Rendered as a transition: A's final `gate_bars` run under the
    pattern (step grid locked to A's tempo); the pattern's last
    cycle completes and B enters, faded over `fade_beats`.

    Why it is not its neighbours: not `beatslicer_shuffle` WEB-08
    (slices are REARRANGED there — here nothing moves, only gain
    is patterned); not GAP-15 `rhythmic_fader_chops` (a performer's
    free-timed chops on an exiting A under B's entry — here a
    looping preset pattern with swing, on A alone, before B);
    not PERF-ZAB `transform_gate_loop` (the gate chops a HELD
    LOOP with doubling subdivisions — here the live track flows
    through a fixed 16-step table); not DM-A44
    `vocal_tremolo_gate` (a smooth LFO tremolo scoped to the
    vocal stem — this is a hard-edged step table on the full mix).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    pattern : step-table name (default "offbeat").
    step_beats : step grid in beats (default 0.25 = 16ths; a
        16-step cycle is then exactly one bar).
    depth : gate depth 0..1 (default 1.0).
    shuffle : even-step delay as a fraction of the step
        (default 0.0; the hardware's SHUFFLE).
    mode : "slash" (2 ms zero notch at each step boundary) or
        "legato" (levels hold; 3 ms edge ramps only).
    gate_bars : gated window at A's end (default 4).
    fade_beats : B's entrance fade in beats (default 2).

    Returns a mono float64 mix of length len(a) + len(b).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    beat_s = bar_s / 4.0
    win_n = min(len(a), gate_bars * bar_n)
    table = _PATTERNS[pattern]
    step_n = max(8, int(round(step_beats * beat_s * sr)))

    n_steps = int(np.ceil(win_n / step_n))
    onsets = []
    for j in range(n_steps + 1):
        t0 = j * step_n
        if j % 2 == 1:
            t0 += int(round(shuffle * step_n))
        onsets.append(min(t0, win_n))
    env = np.ones(win_n)
    for j in range(n_steps):
        s0, s1 = onsets[j], onsets[j + 1]
        if s1 <= s0:
            continue
        lvl = table[j % 16]
        env[s0:s1] = 1.0 - depth * (1.0 - lvl)
    # edge smoothing: 3 ms raised ramps at step boundaries
    edge = max(1, int(0.003 * sr))
    ker = np.hanning(2 * edge + 1)
    ker /= ker.sum()
    env = np.convolve(np.pad(env, edge, mode="edge"), ker,
                      mode="same")[edge:-edge]
    if mode == "slash":
        notch = max(1, int(0.002 * sr))
        for j in range(1, n_steps):
            s0 = onsets[j]
            env[s0:s0 + notch] *= np.linspace(0.0, 1.0, notch)

    out_a = a.copy()
    out_a[len(a) - win_n:] *= env
    fade_n = min(int(round(fade_beats * beat_s * sr)), len(b))
    b_head = b.copy()
    if fade_n > 0:
        _, fi = _eq_power_pair(fade_n)
        b_head[:fade_n] *= fi
    return np.concatenate([out_a, b_head])


# ----------------------------------------------------------------------------
# WEB-29 — Sideband comb filter (SP-404MKII SBF)
# ----------------------------------------------------------------------------

def sideband_comb_filter(a, b, sr, bpm, bar_s, zone_bars=4,
                         base_hz=110.0, interval=0.5, width=0.35,
                         fade_bars=1):
    """A dissolves into a scalable comb of narrow passbands.

    The SP-404MKII's SBF is "a sideband filter that lets specific
    frequency components pass through": INTERVAL simultaneously
    widens the spacing between bands and raises every band's
    frequency, WIDTH narrows each band ("further isolates the
    specific frequency components"), TYPE selects the operating
    range, and BALANCE mixes the combed signal against dry.

    Rendered as a transition: across A's final `zone_bars` the
    mix crossfades from dry A to combed A — bands at
    base_hz * (1+interval)^k, each a Gaussian in log-frequency of
    width `width` octaves, floored at -36 dB — so A ends as its
    own spectral skeleton, rhythm and envelope intact, pitch
    content thinned to the comb. B fades in over `fade_bars`.

    Why it is not its neighbours: not `filter_sweep` T-003 (one
    moving slope — this is a static-but-scalable SET of bands
    across the whole spectrum); not `formant_morph_exit` WEB-17
    (formant peaks travel along a trajectory in a continuing
    voice — the comb's bands are geometric and fixed per
    staging); not `ring_mod_dissolve` WEB-16 (sidebands
    GENERATED by modulation — here existing components are
    selected, none are created).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    zone_bars : dissolve window at A's end (default 4).
    base_hz : lowest band centre (default 110).
    interval : band spacing/growth factor (default 0.5; band k
        sits at base_hz * (1+interval)^k, per the manual's
        coupled spacing+frequency behaviour).
    width : band width in octaves (default 0.35).
    fade_bars : B's entrance crossfade (default 1).

    Returns a mono float64 mix of length len(a) + len(b) - fade.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    win_n = min(len(a), zone_bars * bar_n)
    fade_n = min(bar_n * fade_bars, len(b), win_n)

    out_a = a.copy()
    if win_n > 0:
        seg = a[-win_n:]
        n_fft = 4096
        f, tt, Z = signal.stft(seg, fs=sr, nperseg=n_fft,
                               noverlap=n_fft * 3 // 4)
        bands = []
        fk = float(base_hz)
        while fk < min(16000.0, sr * 0.45):
            bands.append(fk)
            fk *= (1.0 + interval)
        mask = np.full(len(f), 10.0 ** (-36.0 / 20.0))
        lf = np.log2(np.maximum(f, 1.0))
        for fk in bands:
            mask = np.maximum(
                mask, np.exp(-0.5 * ((lf - np.log2(fk)) / width) ** 2))
        Z2 = Z * mask[:, None]
        _, wet = signal.istft(Z2, fs=sr, nperseg=n_fft,
                              noverlap=n_fft * 3 // 4)
        wet = wet[:win_n] if len(wet) >= win_n else np.pad(
            wet, (0, win_n - len(wet)))
        env = np.linspace(0.0, 1.0, win_n)
        out_a[-win_n:] = seg * (1.0 - env) + wet * env

    out = np.zeros(len(a) + len(b) - fade_n)
    out[:len(a)] += out_a
    if fade_n > 0:
        fo, fi = _eq_power_pair(fade_n)
        out[len(a) - fade_n:len(a)] *= fo
        out[len(a) - fade_n:len(a)] += b[:fade_n] * fi
        out[len(a):] += b[fade_n:]
    else:
        out[len(a):] += b
    return out


# ----------------------------------------------------------------------------
# WEB-40 — Sculpt bell sweep (PLAYdifferently MODEL 1 Sculpt EQ)
# ----------------------------------------------------------------------------

def _peaking_bell(x, sr, centre_env_hz, gain_db, q=1.0, block=1024):
    """RBJ peaking-EQ biquad whose centre follows centre_env_hz.

    Block-wise coefficient updates with state carryover (the
    dsp.sweep_filter pattern), so a travelling bell stays click-free.
    """
    x = np.asarray(x, dtype=np.float64)
    n = len(x)
    y = np.zeros(n)
    zi = np.zeros(2)
    nyq = sr / 2.0
    A = 10.0 ** (gain_db / 40.0)
    for start in range(0, n, block):
        stop = min(start + block, n)
        fc = min(max(float(np.mean(centre_env_hz[start:stop])), 20.0),
                 nyq * 0.95)
        w0 = 2.0 * np.pi * fc / sr
        alpha = np.sin(w0) / (2.0 * q)
        cw = np.cos(w0)
        b0 = 1.0 + alpha * A
        b1 = -2.0 * cw
        b2 = 1.0 - alpha * A
        a0 = 1.0 + alpha / A
        a1 = -2.0 * cw
        a2 = 1.0 - alpha / A
        seg, zi = signal.lfilter([b0 / a0, b1 / a0, b2 / a0],
                                 [1.0, a1 / a0, a2 / a0],
                                 x[start:stop], zi=zi)
        y[start:stop] = seg
    return y


def sculpt_bell_sweep(a, b, sr, bpm, bar_s, sweep_bars=4, bell_db=8.0,
                      fade_bars=1):
    """A travelling parametric bell tours A's spectrum; B enters clean.

    The PLAYdifferently MODEL 1's Sculpt EQ is a semi-parametric
    swept bell: FREQ sets the centre, CUT/BOOST sets the gain —
    boost asymmetric at +8 dB max, cut extending to -20 dB, over
    nearly seven octaves, with a wide Q. It replaces the fixed-band
    EQ: instead of cutting or boosting one band, the DJ sweeps the
    bell itself.

    Rendered as a transition: across A's final `sweep_bars` the
    bell centre log-ramps 60 Hz -> 15 kHz at `bell_db` gain (the
    implementation range mirrors WEB-23's; the manual states the
    span as "nearly seven octaves" without Hz numbers). At +8 dB
    each element of A is highlighted in turn as the bell passes —
    kick, then bass, then vocal, then hats — a tour, not a thinning;
    at -20 dB the same travel is a moving cut. At the top of the
    band the bell exits the spectrum (transparent) as B fades in
    over `fade_bars`.

    Why it is not its neighbours: not WEB-23 `notch_carve_sweep`
    (a rejection band from summed HPF+LPF outputs — this is a
    parametric bell, and its headline form is a travelling BOOST,
    which no neighbour renders); not T-003 (a monotonic slope,
    energy removed on one side forever); not `eq_blend` (fixed band
    gains at fixed frequencies — no travelling centre).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    sweep_bars : bell travel window at A's end (default 4).
    bell_db : bell gain in dB (default 8.0 — the manual's max
        boost; -20.0 is the max cut).
    fade_bars : B's entrance crossfade at the seam (default 1).

    Returns a mono float64 mix of length len(a) + len(b) - fade.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    win_n = min(len(a), sweep_bars * bar_n)
    fade_n = min(bar_n * fade_bars, len(b), win_n)

    out_a = a.copy()
    if win_n > 0:
        seg = a[-win_n:]
        centre = np.exp(np.linspace(np.log(60.0), np.log(15000.0), win_n))
        out_a[-win_n:] = _peaking_bell(seg, sr, centre, bell_db)

    out = np.zeros(len(a) + len(b) - fade_n)
    out[:len(a)] += out_a
    if fade_n > 0:
        fo, fi = _eq_power_pair(fade_n)
        out[len(a) - fade_n:len(a)] *= fo
        out[len(a) - fade_n:len(a)] += b[:fade_n] * fi
        out[len(a):] += b[fade_n:]
    else:
        out[len(a):] += b
    return out


# ----------------------------------------------------------------------------
# WEB-41 — LFO filter sweep (Allen & Heath Xone:92 LFO modulation)
# ----------------------------------------------------------------------------

def lfo_filter_sweep(a, b, sr, bpm, bar_s, lfo_bars=4, lfo_cycles=4,
                     depth_oct=2.0, fade_bars=1):
    """A's exit wahs under a cyclic filter LFO; B enters clean.

    The Xone:92's VCFs are "further enhanced by two independent
    LFOs... for additional cyclic filter modulation effects": an ON
    switch punches the LFO in or out, DEPTH sets the modulation
    amount, TAP sets the rate from the last two presses, X2 doubles
    it. The LFO is a cyclic control, not a sweep: the cutoff returns
    to where it started every cycle.

    Rendered as a transition: across A's final `lfo_bars` a lowpass
    cutoff oscillates log-sinusoidally around 1 kHz, `lfo_cycles`
    whole cycles (integer, so the filter returns to centre exactly
    at the seam), with the oscillation depth ramping 0 -> `depth_oct`
    octaves across the window — the DEPTH knob turning up through
    the exit. At the seam B fades in over `fade_bars`, the filter
    at centre, neither open nor closed.

    Why it is not its neighbours: not T-003 (a monotonic slope —
    this returns, every cycle); not WEB-27 `cyclic_speed_dip` (a
    tempo-period LFO on playback RATE — this modulates the filter,
    not the speed); not WEB-24 `phaser_sweep` (an allpass cascade,
    magnitude-flat — this is a cutoff oscillation with real
    spectral loss at the troughs).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    lfo_bars : LFO window at A's end (default 4).
    lfo_cycles : whole LFO cycles inside the window (default 4 —
        one per bar at the default window).
    depth_oct : peak oscillation depth in octaves at the seam
        (default 2.0; the depth ramps 0 -> depth_oct).
    fade_bars : B's entrance crossfade at the seam (default 1).

    Returns a mono float64 mix of length len(a) + len(b) - fade.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    win_n = min(len(a), lfo_bars * bar_n)
    fade_n = min(bar_n * fade_bars, len(b), win_n)

    out_a = a.copy()
    if win_n > 0:
        seg = a[-win_n:]
        t = np.arange(win_n) / win_n
        ramp = t  # DEPTH turning up across the window
        osc = np.sin(2.0 * np.pi * lfo_cycles * t)
        centre = 1000.0 * (2.0 ** (depth_oct * ramp * osc))
        out_a[-win_n:] = dsp.sweep_filter(seg, sr, centre,
                                          ftype="lowpass")

    out = np.zeros(len(a) + len(b) - fade_n)
    out[:len(a)] += out_a
    if fade_n > 0:
        fo, fi = _eq_power_pair(fade_n)
        out[len(a) - fade_n:len(a)] *= fo
        out[len(a) - fade_n:len(a)] += b[:fade_n] * fi
        out[len(a):] += b[fade_n:]
    else:
        out[len(a):] += b
    return out


# ----------------------------------------------------------------------------
# WEB-42 — Linked filter handover (Allen & Heath Xone:92 VCF LINK 2-1)
# ----------------------------------------------------------------------------

def linked_filter_handover(a, b, sr, bpm, bar_s, handover_bars=4):
    """One cutoff joins A below to B above; the join travels down.

    The Xone:92's VCF LINK 2-1 switch links FILTER 2's FREQ to
    FILTER 1's: "FILTER 2 FREQ can now be controlled by the FREQ
    VCF sweep control of FILTER 1... assign Channel 1 to Filter 1
    and Channel 2 to Filter 2. Select a low pass filter on filter 1
    and a high pass on filter 2. With both filters ON and the link
    switch selected, the low frequencies of channel 1 will be
    accurately joined to the high frequencies of channel 2. This
    can be used to produce incredibly smooth mixes or to mix tracks
    that would otherwise clash when mixed conventionally."

    Rendered as a transition: the handover window is A's final
    `handover_bars` overlapped with B's first `handover_bars`.
    Across it ONE cutoff trajectory log-falls 8 kHz -> 150 Hz: A
    passes through a lowpass at that cutoff, B through a highpass
    at the same cutoff, and the two filtered signals sum. At every
    instant the spectrum is partitioned at exactly one frequency —
    A owns below it, B above it — so the join is exact, with no
    gap band and no overlap band; as the cutoff falls, B takes over
    progressively from the top down. Past the window B plays full.

    Why it is not its neighbours: not T-003's dual-VCF
    counter-sweep axis (two INDEPENDENT sweeps, one per side, with
    no render — here the two filters share one parameter, and the
    exactness of the join is the mechanism); not `eq_blend`
    (fixed band gains — no moving partition); not `bass_swap`
    (a 1-beat bass exchange — this is a full-spectrum handover over
    bars, top-down rather than bottom-up).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate (Hz). bpm : tempo (signature parity).
    bar_s : seconds per bar.
    handover_bars : overlap window in bars (default 4).

    Returns a mono float64 mix of length
    len(a) + len(b) - handover window.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    win_n = min(len(a), len(b), handover_bars * bar_n)

    head = a[:-win_n] if win_n < len(a) else np.zeros(0)
    a_seg = a[-win_n:] if win_n > 0 else np.zeros(0)
    b_seg = b[:win_n] if win_n > 0 else np.zeros(0)
    b_tail = b[win_n:] if win_n < len(b) else np.zeros(0)

    if win_n > 0:
        fc = np.exp(np.linspace(np.log(8000.0), np.log(150.0), win_n))
        win = (dsp.sweep_filter(a_seg, sr, fc, ftype="lowpass")
               + dsp.sweep_filter(b_seg, sr, fc, ftype="highpass"))
    else:
        win = np.zeros(0)
    return np.concatenate([head, win, b_tail])


# ----------------------------------------------------------------------------
# Registry
# ----------------------------------------------------------------------------

META = {
    "pre_filtered_echo": {
        "title": "Pre-Filtered Echo (Dry+Wet Send Conditioning)",
        "bank": "WEB-22", "family": "SPACE", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "verse", "chorus", "drop",
                                     "build", "breakdown"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "camelot>=4", "weight": 2,
             "reason": "bass-less repeats shed A's key residue while "
                       "the dry keeps its low end to the last beat"},
            {"when": "energy_delta<=0", "weight": 2,
             "reason": "the additive tail decays under a falling or "
                       "lateral exit without ducking the dry"},
            {"when": "genre_pair==leap", "weight": 1,
             "reason": "genre independence — the shaped tail lets B "
                       "arrive from another world"},
        ],
        "energy": {"delta": 0, "tension": "falling"},
        "exit": "tail", "clash_risk": "none",
        "params": {
            "beat_div": {"type": "float", "range": [0.25, 1.0],
                         "default": 0.5, "unit": "beats",
                         "presets": {"quarter": 0.25, "dotted": 0.75,
                                     "full": 1.0}},
            "cutoff_hz": {"type": "float", "range": [80.0, 4000.0],
                          "default": 300.0, "unit": "hz",
                          "presets": {"sub_only": 120.0,
                                      "open": 1200.0}},
            "feedback": {"type": "float", "range": [0.0, 0.9],
                         "default": 0.55, "unit": "gain"},
            "wet": {"type": "float", "range": [0.0, 1.0],
                    "default": 0.6, "unit": "wet"},
            "tail_beats": {"type": "int", "range": [2, 8],
                           "default": 4, "unit": "beats"},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Mixxx 2.5 Manual, Ch. 11 Effects — the Dry+Wet "
                    "worked example: a filter before the Echo removes "
                    "bass from the echoed signal without removing it "
                    "from the unechoed signal; 'in Dry+Wet mode, the "
                    "dry signal is always at full volume'",
             "url": "https://manual.mixxx.org/2.5/de/chapters/effects.html",
             "date": "2026-10-23"},
        ],
        "composed_of": ["echo_out"],
    },
    "notch_carve_sweep": {
        "title": "Notch Carve Sweep (Dual State-Variable VCF)",
        "bank": "WEB-23", "family": "FREQ", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 8.0, "camelot_max": 4,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "build", "verse", "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta_abs<=1", "weight": 2,
             "reason": "lateral move — the carve moves the texture "
                       "without an energy slope"},
            {"when": "camelot>=3", "weight": 1,
             "reason": "the travelling hole thins the clash bands one "
                       "at a time instead of stacking them"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "snap", "clash_risk": "key",
        "params": {
            "sweep_bars": {"type": "int", "range": [2, 16],
                           "default": 4, "unit": "bars",
                           "presets": {"quick": 2, "long": 8}},
            "q": {"type": "float", "range": [0.7, 30.0],
                  "default": 8.0, "unit": "q",
                  "presets": {"wide": 2.0, "needle": 24.0}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Allen & Heath Xone:96 User Guide (official "
                    "support) — state-variable filters provide HPF/"
                    "BPF/LPF simultaneously; 'Any combination can "
                    "be pressed together to create different "
                    "response types such as notch'",
             "url": "https://support.allen-heath.com/hc/en-gb/articles/43053562464017-Xone-96-User-Guide",
             "date": "2026-10-23"},
        ],
        "composed_of": [],
    },
    "phaser_sweep": {
        "title": "Phaser Sweep (Allpass Cascade)",
        "bank": "WEB-24", "family": "FREQ", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 8.0, "camelot_max": 4,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "build", "verse", "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta_abs<=1", "weight": 2,
             "reason": "lateral move — texture travels while spectrum "
                       "and loudness stay put"},
            {"when": "camelot>=4", "weight": 1,
             "reason": "phase churn smears key residue at the seam "
                       "without thinning either track"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "snap", "clash_risk": "key",
        "params": {
            "sweep_bars": {"type": "int", "range": [2, 16],
                           "default": 4, "unit": "bars",
                           "presets": {"quick": 2, "long": 8}},
            "rate_bars": {"type": "float", "range": [0.25, 4.0],
                          "default": 1.0, "unit": "bars",
                          "presets": {"fast": 0.5, "slow": 2.0}},
            "stages": {"type": "int", "range": [2, 8],
                       "default": 4, "unit": "sections",
                       "presets": {"duo": 2, "deep": 6}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Roland SP-404MKII Reference v5.5 — Phaser MFX: "
                    "'creates modulation by adding a phase-shifted "
                    "sound' (DEPTH/RATE/MANUAL/RESONANCE, syncable)",
             "url": "https://static.roland.com/manuals/sp-404mk2_reference_v550/en-US/7899047578463371.html",
             "date": "2026-10-23"},
            {"type": "tutorial",
             "ref": "Allen & Heath Xone:96 User Guide — summed "
                    "state-variable outputs give 'interesting "
                    "all-pass effects'",
             "url": "https://support.allen-heath.com/hc/en-gb/articles/43053562464017-Xone-96-User-Guide",
             "date": "2026-10-23"},
        ],
        "composed_of": [],
    },
    "stem_swap_replace": {
        "title": "Stem Swap Replace (Captured-Loop Stem Substitution)",
        "bank": "WEB-25", "family": "ROUTING", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 3.0, "camelot_max": 4,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "drop", "chorus", "build",
                                     "verse"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": ["stems"]},
        "prefers": [
            {"when": "energy_delta_abs<=1", "weight": 2,
             "reason": "the host's energy contour never breaks — one "
                       "element is substituted inside it"},
            {"when": "drop_pair", "weight": 1,
             "reason": "a captured drop stem riding the other track's "
                       "drop is the mashup form of the swap"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "loop", "clash_risk": "bass",
        "params": {
            "loop_bars": {"type": "int", "range": [1, 8],
                          "default": 2, "unit": "bars",
                          "presets": {"1bar": 1, "4bar": 4}},
            "swap_bars": {"type": "int", "range": [4, 32],
                          "default": 8, "unit": "bars",
                          "presets": {"4bar": 4, "16bar": 16}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "VirtualDJ Manual — Sampler (StemSwap Banks) + "
                    "Stems 2.0: 'stems samples from a StemSwap bank "
                    "will mute the corresponding stem from the track "
                    "playing on the deck where the sample was "
                    "triggered, effectively swapping the stems'",
             "url": "https://www.virtualdj.com/manuals/virtualdj/interface/stems2.html",
             "date": "2026-10-23"},
        ],
        "composed_of": ["stem_element_crossfade"],
    },
    "djfx_microloop": {
        "title": "DJFX Microloop (Free-Time Grain Loop)",
        "bank": "WEB-26", "family": "TIME", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "drop", "chorus", "build"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_a>=7", "weight": 2,
             "reason": "the grain needs loud, dense material to read "
                       "as a catch, not a glitch"},
            {"when": "genre_pair==leap", "weight": 1,
             "reason": "no shared grid or key is needed — the grain "
                       "is absolute time, B enters free"},
        ],
        "energy": {"delta": 0, "tension": "build"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "length_ms": {"type": "float", "range": [12.0, 230.0],
                          "default": 120.0, "unit": "ms",
                          "presets": {"tight": 30.0, "wide": 230.0}},
            "mode": {"type": "str", "range": ["reverse", "stop",
                                              "hold"],
                     "default": "reverse", "unit": "mode",
                     "presets": {"stop": "stop", "hold": "hold"}},
            "loop_bars": {"type": "int", "range": [1, 4],
                          "default": 2, "unit": "bars",
                          "presets": {"1bar": 1, "4bar": 4}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Roland SP-404MKII Reference v5.5 — DJFX Looper: "
                    "'loops the sound in short cycles; vary the "
                    "playback direction and playback speed... "
                    "turntable-type effect' (LENGTH 0.230-0.012 s, "
                    "SPEED -100..100, backward when negative, stops "
                    "at zero)",
             "url": "https://static.roland.com/manuals/sp-404mk2_reference_v550/en-US/7899047578463371.html",
             "date": "2026-10-23"},
        ],
        "composed_of": [],
    },
    "cyclic_speed_dip": {
        "title": "Cyclic Speed Dip (Downer)",
        "bank": "WEB-27", "family": "DYN", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "build", "verse", "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "bpm_delta_pct>=6", "weight": 2,
             "reason": "a sagging outgoing tempo reads as intentional "
                       "across a wide gap; B enters at its own tempo"},
            {"when": "energy_delta<=0", "weight": 1,
             "reason": "each dip sheds energy in waves under a "
                       "falling or lateral exit"},
        ],
        "energy": {"delta": -1, "tension": "falling"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "rate_beats": {"type": "float", "range": [0.5, 32.0],
                           "default": 4.0, "unit": "beats",
                           "presets": {"half_bar": 2.0,
                                       "two_bar": 8.0}},
            "depth": {"type": "float", "range": [0.1, 0.9],
                      "default": 0.45, "unit": "fraction",
                      "presets": {"shallow": 0.25, "deep": 0.7}},
            "dip_bars": {"type": "int", "range": [4, 32],
                         "default": 8, "unit": "bars",
                         "presets": {"4bar": 4, "16bar": 16}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Roland SP-404MKII Reference v5.5 — Downer: "
                    "'cyclically slows down the audio playback "
                    "speed' (RATE 2/1..1/32, DEPTH, FILTER HF "
                    "tracking, PITCH correction mode)",
             "url": "https://static.roland.com/manuals/sp-404mk2_reference_v550/en-US/7899047578463371.html",
             "date": "2026-10-23"},
        ],
        "composed_of": [],
    },
    "pattern_gate_slicer": {
        "title": "Pattern Gate Slicer (16-Step Gate Pattern)",
        "bank": "WEB-28", "family": "PERF", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 5.0, "camelot_max": 3,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "drop", "chorus", "build"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": []},
        "prefers": [
            {"when": "energy_a>=6", "weight": 2,
             "reason": "the pattern needs a full groove to carve — "
                       "on sparse material the gates read as dropouts"},
            {"when": "energy_delta>=1", "weight": 1,
             "reason": "a gated exit builds rhythmic tension into "
                       "B's entrance"},
        ],
        "energy": {"delta": 0, "tension": "build"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "pattern": {"type": "str",
                        "range": ["offbeat", "pulse", "cascade",
                                  "stutter"],
                        "default": "offbeat", "unit": "pattern",
                        "presets": {"pulse": "pulse",
                                    "cascade": "cascade",
                                    "stutter": "stutter"}},
            "step_beats": {"type": "float", "range": [0.0625, 1.0],
                           "default": 0.25, "unit": "beats",
                           "presets": {"8th": 0.5, "quarter": 1.0}},
            "mode": {"type": "str", "range": ["slash", "legato"],
                     "default": "slash", "unit": "mode",
                     "presets": {"legato": "legato"}},
            "gate_bars": {"type": "int", "range": [2, 16],
                          "default": 4, "unit": "bars",
                          "presets": {"2bar": 2, "8bar": 8}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Roland SP-404MKII Reference v5.5 — Slicer: "
                    "'slices the sound at certain intervals into 16 "
                    "parts (16 steps)... a rhythm that follows the "
                    "sequence pattern' (PATTERN 1-32, SHUFFLE swing, "
                    "LEGATO/SLASH modes)",
             "url": "https://static.roland.com/manuals/sp-404mk2_reference_v550/en-US/7899047578463371.html",
             "date": "2026-10-23"},
            {"type": "tutorial",
             "ref": "Pioneer DJM-V10 manual (manua.ls mirror) — "
                    "Beat FX TRANS: 'cuts the sound cyclically "
                    "according to the beat', LEVEL/DEPTH sets "
                    "balance and duty",
             "url": "https://www.manua.ls/pioneer/djm-v10/manual?p=49",
             "date": "2026-10-23"},
        ],
        "composed_of": [],
    },
    "sideband_comb_filter": {
        "title": "Sideband Comb Filter (SBF)",
        "bank": "WEB-29", "family": "FREQ", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 8.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "breakdown", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "camelot>=4", "weight": 2,
             "reason": "the comb strips A's pitch content to a "
                       "skeleton — key clash has nothing to bite on"},
            {"when": "energy_delta<=0", "weight": 1,
             "reason": "a dissolving exit under falling energy"},
        ],
        "energy": {"delta": -1, "tension": "falling"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "base_hz": {"type": "float", "range": [40.0, 880.0],
                        "default": 110.0, "unit": "hz",
                        "presets": {"sub": 55.0, "mid": 220.0,
                                    "high": 440.0}},
            "interval": {"type": "float", "range": [0.1, 1.5],
                         "default": 0.5, "unit": "factor",
                         "presets": {"tight": 0.25, "wide": 1.0}},
            "width": {"type": "float", "range": [0.08, 1.0],
                      "default": 0.35, "unit": "octaves"},
            "zone_bars": {"type": "int", "range": [2, 16],
                          "default": 4, "unit": "bars",
                          "presets": {"2bar": 2, "8bar": 8}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Roland SP-404MKII Reference v5.5 — SBF: 'a "
                    "sideband filter that lets specific frequency "
                    "components pass through' (INTERVAL widens "
                    "spacing and raises band frequencies, WIDTH "
                    "narrows each band, TYPE SBF1-6 range)",
             "url": "https://static.roland.com/manuals/sp-404mk2_reference_v550/en-US/7899047578463371.html",
             "date": "2026-10-23"},
        ],
        "composed_of": [],
    },
    "sculpt_bell_sweep": {
        "title": "Sculpt Bell Sweep (Travelling Parametric Bell)",
        "bank": "WEB-40", "family": "FREQ", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "genre_pair==same", "weight": 1,
             "reason": "the bell tours A's spectrum inside one "
                       "genre's blend — no gap device needed"},
            {"when": "phrase_a==outro", "weight": 1,
             "reason": "the sweep window is A's outro — the bell "
                       "has a full phrase to travel"},
        ],
        "energy": {"delta": 0, "tension": "build"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "sweep_bars": {"type": "int", "range": [2, 16],
                           "default": 4, "unit": "bars",
                           "presets": {"short": 2, "standard": 4}},
            "bell_db": {"type": "float", "range": [-20.0, 8.0],
                        "default": 8.0, "unit": "db",
                        "presets": {"highlight": 8.0, "carve": -20.0}},
            "fade_bars": {"type": "int", "range": [1, 4],
                          "default": 1, "unit": "bars"},
        },
        "evidence": [
            {"type": "manual",
             "ref": "PLAYdifferently MODEL 1 User Guide Issue 1 "
                    "(2016) — Contour/Sculpt EQ: 'a semi-parametric "
                    "swept bell filter' with FREQ + CUT/BOOST, "
                    "boost +8 dB max, cut -20 dB, 'nearly seven "
                    "octaves'",
             "url": "https://manuals.plus/m/2e08027386c2634318a547d8f72de490ee6e062fab9a20bdc1bb80e3108f491b",
             "date": "2026-10-26"},
        ],
        "composed_of": [],
    },
    "lfo_filter_sweep": {
        "title": "LFO Filter Sweep (Cyclic Filter Modulation)",
        "bank": "WEB-41", "family": "FREQ", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "chorus", "build"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "genre_pair==same", "weight": 1,
             "reason": "cyclic filter motion sits inside a "
                       "like-for-like blend"},
            {"when": "energy_delta>=0", "weight": 1,
             "reason": "the LFO's rising depth lifts a flat-or-"
                       "rising exit"},
        ],
        "energy": {"delta": 0, "tension": "build"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "lfo_bars": {"type": "int", "range": [2, 16],
                         "default": 4, "unit": "bars",
                         "presets": {"short": 2, "standard": 4}},
            "lfo_cycles": {"type": "int", "range": [1, 16],
                           "default": 4, "unit": "cycles",
                           "presets": {"slow": 2, "fast": 8}},
            "depth_oct": {"type": "float", "range": [0.5, 4.0],
                          "default": 2.0, "unit": "octaves",
                          "presets": {"shallow": 1.0, "deep": 3.0}},
            "fade_bars": {"type": "int", "range": [1, 4],
                          "default": 1, "unit": "bars"},
        },
        "evidence": [
            {"type": "manual",
             "ref": "Allen & Heath Xone:92 User Guide p. 24 "
                    "(manualsdir mirror) — LFO modulation: 'two "
                    "independent LFOs... for additional cyclic "
                    "filter modulation effects', ON switch, DEPTH, "
                    "TAP tempo, X2 doubling",
             "url": "https://www.manualsdir.com/manuals/554322/allenheath-xone-92-xone92.html?page=24",
             "date": "2026-10-26"},
        ],
        "composed_of": [],
    },
    "linked_filter_handover": {
        "title": "Linked Filter Handover (One-Cutoff Spectral Join)",
        "bank": "WEB-42", "family": "FREQ", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "genre_pair==neighbor", "weight": 2,
             "reason": "the exact spectral join is the clash-proof "
                       "handover — neighbouring genres that would "
                       "fight in a plain blend meet at one cutoff"},
            {"when": "camelot<=2", "weight": 1,
             "reason": "the join is exact at one cutoff, so a "
                       "close key pair hands over without a clash "
                       "window"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "handover_bars": {"type": "int", "range": [2, 16],
                              "default": 4, "unit": "bars",
                              "presets": {"short": 2, "standard": 4}},
        },
        "evidence": [
            {"type": "manual",
             "ref": "Allen & Heath Xone:92 User Guide p. 24 "
                    "(manualsdir mirror) — VCF LINK 2-1: 'the low "
                    "frequencies of channel 1 will be accurately "
                    "joined to the high frequencies of channel 2... "
                    "incredibly smooth mixes'",
             "url": "https://www.manualsdir.com/manuals/554322/allenheath-xone-92-xone92.html?page=24",
             "date": "2026-10-26"},
        ],
        "composed_of": [],
    },
}

TECHNIQUE_FUNCS = {
    "pre_filtered_echo": pre_filtered_echo,
    "notch_carve_sweep": notch_carve_sweep,
    "phaser_sweep": phaser_sweep,
    "stem_swap_replace": stem_swap_replace,
    "djfx_microloop": djfx_microloop,
    "cyclic_speed_dip": cyclic_speed_dip,
    "pattern_gate_slicer": pattern_gate_slicer,
    "sideband_comb_filter": sideband_comb_filter,
    "sculpt_bell_sweep": sculpt_bell_sweep,
    "lfo_filter_sweep": lfo_filter_sweep,
    "linked_filter_handover": linked_filter_handover,
}
