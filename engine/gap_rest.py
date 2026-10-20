"""
open-transitions engine — gap-rest domain module (Worker C lane).

TIME / DYN / SYNTH gap techniques from the Transition Gap Report
2026-10-19 (gaps 1, 2, 4, 5, 7, 17) plus two James Zabiela performer
moves reverse-engineered in edu-survey-G §4 (EFX-1000 feedback loops,
beat roll / transform craft, and the 2020 3:4 tempo-modulation demo).

  GAP-01 sample_connection        hot-cue swap into the track that samples A
  GAP-02 loop_tightening_build    Hype-Loop-style halving build over B
  GAP-04 polyrhythmic_loops       4-beat vs 3-beat loop bed, 12-beat LCM
  GAP-05 slip_mode_flourish       slip safety-net live flourish over A
  GAP-07 premade_tempo_bridge_edit produced-artifact tempo bridge
  GAP-17 sampler_one_shot_mask    one-shot fired on the cut to mask the join
  PERF-ZAB feedback_loop_build    EFX-1000 feedback ramp, cut, B slams
  PERF-ZAB metric_loop_pivot      3:4 metric pivot (130 -> 173.4, no sync)

Conventions follow engine/techniques.py: numpy mono float64 in/out,
timing in bars/beats, the docstring IS the spec source (techniques/*.md
mirror it). Synthesized sketch audio only — no recorded material.

Deliberate exclusions honoured (Gap Report / FRAMEWORK.md §9): gap 3
(holding-pattern loop) and gap 6 (toneplay) are NOT implemented here.
"""

import inspect

import numpy as np
from scipy import signal

from . import dsp

KILL_DB = -60.0  # mirrors engine/techniques.py convention


# ----------------------------------------------------------------------------
# Shared helpers
# ----------------------------------------------------------------------------

def _fit(x, n):
    """Trim or zero-pad x to exactly n samples."""
    x = np.asarray(x, dtype=np.float64)
    if len(x) >= n:
        return x[:n]
    return np.pad(x, (0, n - len(x)))


def _guard(x, sr, ms=2.0):
    """Tiny raised-cosine guards on both ends (click avoidance only)."""
    x = np.asarray(x, dtype=np.float64).copy()
    g = max(1, int(ms / 1000.0 * sr))
    if 2 * g < len(x):
        w = 0.5 - 0.5 * np.cos(np.pi * np.linspace(0, 1, g))
        x[:g] *= w
        x[-g:] *= w[::-1]
    return x


def _synth_kick(sr, n):
    """Deterministic kick sketch (sine pitch-drop), mirrors demos' sketch."""
    t = np.arange(n) / sr
    f = 55.0 * np.exp(-t * 30.0) + 38.0
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 18.0)


def _synth_hat(sr, n, seed=3):
    """Deterministic hat sketch (high-passed noise, fast decay)."""
    rng = np.random.default_rng(seed)
    hp = np.diff(rng.standard_normal(n), prepend=0.0)
    return hp * np.exp(-np.arange(n) / sr * 80.0)


def _tv_feedback_delay(x, sr, delay_s, fb_env, block=8192):
    """Time-varying feedback delay: y[n] = x[n] + fb[n] * y[n-d].

    Block-wise geometric series (the dsp.feedback_delay trick) with the
    feedback held constant per block — fb ramps are slow (bars), so the
    per-block constant is inaudible, and the closed form stays O(K * n)
    instead of the O(n * d) a sparse lfilter would cost. Cross-block
    echoes are exact: every term indexes the (fully known) input x.
    """
    x = np.asarray(x, dtype=np.float64)
    n = len(x)
    d = max(1, int(round(delay_s * sr)))
    fb_env = np.asarray(fb_env, dtype=np.float64)
    y = np.zeros(n)
    for s in range(0, n, block):
        e = min(s + block, n)
        fb = float(np.mean(fb_env[s:e]))
        fb = min(max(fb, 0.0), 0.999)
        acc = x[s:e].copy()
        fbp = fb
        k = 1
        while fbp > 1e-9 and k * d < e:
            j0 = max(0, k * d - s)
            if j0 < e - s:
                acc[j0:] += fbp * x[s + j0 - k * d:e - k * d]
            fbp *= fb
            k += 1
        y[s:e] = acc
    return y


# ----------------------------------------------------------------------------
# GAP-01 — Sample connection / sample switch-up (TIME, ADAPT)
# ----------------------------------------------------------------------------

def sample_connection(a, b, sr, bpm, hit_t, hit_len_s=0.5):
    """Hot-cue swap from A into the track that samples it, at the shared hit.

    Parameters
    ----------
    a : outgoing track segment (mono float64). Its phrase plays through
        the shared sampled element; the element starts at `hit_t`.
    b : incoming track segment (mono float64) — the track that samples A
        (or A's source). Caller aligns b so its own statement of the
        shared element starts at sample 0.
    sr : sample rate (Hz).
    bpm : tempo of the pair (beats/min) — documents the grid; the move is
        cue-triggered, not bar-counted, so bpm only anchors hit timing.
    hit_t : position of the shared sampled element in `a` (seconds).
    hit_len_s : length of the shared element (seconds, default 0.5 s).

    Returns
    -------
    Mono float64 mix: A through the shared hit -> the hit retriggered
    twice in rhythmic unison -> B entering from its own statement of
    that element (equal-power crossfade under the second retrigger).

    Why it works
    ------------
    Wordplay (T-011) chains lyric *words*; this chains *source material*.
    The ear recognises the sampled element as the same object in both
    tracks, so the retriggers read as a deliberate call-and-response and
    the swap lands as revelation, not as a cut. The second retrigger
    crossfading into B hides the join inside the one sound both tracks
    share.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    hit_i = int(hit_t * sr)
    hit_n = max(1, int(hit_len_s * sr))
    if hit_i + hit_n > len(a):
        hit_i = max(0, len(a) - hit_n)
    hit = _fit(a[hit_i:hit_i + hit_n], hit_n)
    pre = a[:hit_i + hit_n]  # A plays through the shared hit

    hit_g = _guard(hit, sr, ms=2.0)
    retrig1 = hit_g.copy()
    # second retrigger dissolves into B's own statement of the element
    b_head = _fit(b[:hit_n], hit_n)
    retrig2 = dsp.equal_power_xfade(hit_g, b_head)
    tail = b[hit_n:] if len(b) > hit_n else np.zeros(0)
    return np.concatenate([pre, retrig1, retrig2, tail])


# ----------------------------------------------------------------------------
# GAP-02 — Loop-tightening build / "Hype Loops" (TIME, ADOPT)
# ----------------------------------------------------------------------------

def loop_tightening_build(loop_src, b, sr, bar_s, bpm):
    """A grabbed loop held over B's buildup, halved 4 -> 2 -> 1 -> 1/2 bars.

    Parameters
    ----------
    loop_src : loop material (mono float64) — a vocal/harmonic fragment;
        at least 4 bars (padded if shorter). Successively shorter slices
        are taken from its head: 4 bars, 2 bars, 1 bar, 1/2 bar.
    b : incoming track's buildup segment (mono float64); the build runs
        over its first 8 bars and the output has len(b).
    sr : sample rate (Hz).
    bar_s : seconds per bar.
    bpm : tempo (beats/min) — sets the 1/4-beat fader-chop grid.

    Returns
    -------
    Mono float64 mix: B's buildup with the loop layer on top (-3 dB),
    stages of 4 / 2 / 1 / 1 bars (the last stage loops the 1/2-bar
    slice), HPF cutoff rising 200 -> 500 -> 1200 -> 3000 Hz per stage,
    1/4-beat fader chops on the loop throughout, loop released with a
    1/2-bar raised-cosine fade so B's drop (caller-side) lands clean.

    Why it works
    ------------
    James Hype's "Hype Loops" move: the loop is a constant the crowd can
    hold onto while its *rate of change* accelerates — halving the loop
    doubles its repetition rate, the rising HPF strips its body, and the
    chops turn it percussive. Tension comes from the loop, so B's own
    buildup stays intact underneath. T-008's roll lives inside A's last
    bar and T-020's glue loop is static; neither sustains a tightening
    loop across B's build — this does.
    """
    loop_src = np.asarray(loop_src, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(bar_s * sr)
    beat_n = max(1, bar_n // 4)
    build_n = 8 * bar_n
    loop_src = _fit(loop_src, 4 * bar_n)
    b = _fit(b, build_n) if len(b) < build_n else b

    # 1/4-beat fader chops: on for one quarter-beat, off for the next,
    # 8 ms trapezoid edges (convolution smoothing of the square wave).
    def chop_env(n):
        q = max(2, beat_n // 4)
        sq = ((np.arange(n) // q) % 2 == 0).astype(np.float64)
        k = max(1, int(0.008 * sr))
        return np.convolve(sq, np.ones(k) / k, mode="same")

    stages = [(4, loop_src[:4 * bar_n], 200.0),
              (2, loop_src[:2 * bar_n], 500.0),
              (1, loop_src[:bar_n], 1200.0),
              (1, loop_src[:bar_n // 2], 3000.0)]
    layer = np.zeros(build_n)
    t = 0
    for bars_i, seg, hpf in stages:
        n_i = bars_i * bar_n
        part = np.tile(seg, int(np.ceil(n_i / len(seg))))[:n_i]
        part = dsp.sweep_filter(part, sr, hpf, ftype="highpass",
                                block=2048)
        layer[t:t + n_i] = part * chop_env(n_i)
        t += n_i
    # release: loop fades over the final 1/2 bar so the drop is B alone
    rel = bar_n // 2
    layer[-rel:] *= dsp.raised_cosine(rel, up=False)

    out = b.copy()
    out[:build_n] += layer * dsp.db_to_gain(-3.0)
    return out


# ----------------------------------------------------------------------------
# GAP-04 — Polyrhythmic looping (TIME, ADAPT)
# ----------------------------------------------------------------------------

def polyrhythmic_loops(a, b, sr, bar_s):
    """Two contrasting loops layered as an evolving bed; B enters at LCM.

    Parameters
    ----------
    a : outgoing track segment (mono float64). A 4-bar lead-in plays,
        then its first bar is the 4-beat-cycle loop.
    b : incoming track segment (mono float64). Its first 3 beats are
        the 3-beat-cycle loop; B itself enters in full after the bed.
    sr : sample rate (Hz).
    bar_s : seconds per bar.

    Returns
    -------
    Mono float64 mix: 4 bars of A -> 12 beats of bed (A's 4-beat loop
    tiled x3 against B's 3-beat loop tiled x4, each at -3 dB, under a
    slow HPF opening 200 -> 1500 Hz) -> B in full.

    Why it works
    ------------
    The two cycles disagree for 11 beats and agree on beat 12
    (LCM(3, 4) = 12), so the bed feels like it is *searching* and then
    locks — B's entrance on the alignment is heard as the resolution
    the polyrhythm was pointing at. T-020 layers one static glue loop;
    two loops in metric conflict are a different, evolving device.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(bar_s * sr)
    beat_n = max(1, bar_n // 4)
    bed_n = 12 * beat_n

    lead = a[-4 * bar_n:] if len(a) >= 4 * bar_n else a
    loop4 = _fit(a[:bar_n], bar_n)
    loop3 = _fit(b[:3 * beat_n], 3 * beat_n)
    bed = (np.tile(loop4, 3)[:bed_n] * dsp.db_to_gain(-3.0)
           + np.tile(loop3, 4)[:bed_n] * dsp.db_to_gain(-3.0))
    # evolution: the bed brightens as the alignment approaches. The
    # swept half is layered over a dry half — a pure HPF bed would
    # strip the final loop chunk to hat-only residue and the floor
    # would collapse; the dry half keeps the groove's body honest.
    cut = 200.0 * (1500.0 / 200.0) ** np.linspace(0.0, 1.0, bed_n)
    bed_f = dsp.sweep_filter(bed, sr, cut, ftype="highpass", block=2048)
    bed = 0.5 * bed + 0.5 * bed_f
    return np.concatenate([lead, bed, b])


# ----------------------------------------------------------------------------
# GAP-05 — Slip-mode flourish, general (TIME, ADAPT)
# ----------------------------------------------------------------------------

def slip_mode_flourish(a, sr, bpm, flourish_beats=1.0):
    """Slip as a safety net: a live flourish rides over A's continuing drums.

    Parameters
    ----------
    a : the playing track segment (mono float64). It is NEVER
        interrupted — slip means the playhead keeps advancing under
        the flourish, so release lands back in phrase by construction.
    sr : sample rate (Hz).
    bpm : tempo (beats/min) — sets the beat grid.
    flourish_beats : length of the reversed snippet (beats,
        default 1.0 beat).

    Returns
    -------
    Mono float64, same length as `a`: A untouched, plus at 75% through
    the segment a flourish at -6 dB — a reversed snippet of A's own
    next beat, followed by a spin chirp (exponential pitch-dive of the
    same snippet over 1/2 beat).

    Why it works
    ------------
    The library used slip only inside T-008's roll. As a general tool,
    slip decouples *performance* from *risk*: any gesture (reverse,
    chirp, juggle) can be thrown live because the underlying phrase
    never moved — the worst case is an odd beat, never a trainwreck.
    Layering at -6 dB keeps A's drums as the floor's anchor; the
    flourish is heard as decoration on a groove that never stopped.
    """
    a = np.asarray(a, dtype=np.float64)
    beat_s = 60.0 / bpm
    beat_n = max(1, int(beat_s * sr))
    fn = max(1, int(flourish_beats * beat_n))
    # flourish point: 75% through, snapped DOWN to the beat grid
    fp = int(len(a) * 0.75)
    fp = (fp // beat_n) * beat_n
    fp = min(fp, max(0, len(a) - 2 * fn))

    out = a.copy()
    g = dsp.db_to_gain(-6.0)
    snip = _fit(a[fp:fp + fn], fn)
    rev = _guard(snip[::-1], sr, ms=3.0)
    k = min(fn, len(out) - fp)
    if k > 0:
        out[fp:fp + k] += rev[:k] * g
    chirp_n = max(1, fn // 2)
    chirp = dsp.pitch_dive(snip, sr, chirp_n, curve="exp")
    c0 = fp + fn
    k2 = min(chirp_n, len(out) - c0)
    if k2 > 0:
        out[c0:c0 + k2] += _guard(chirp, sr, ms=3.0)[:k2] * g
    return out


# ----------------------------------------------------------------------------
# GAP-07 — Pre-made tempo-bridge edit / "transition track" (DYN, ADOPT)
# ----------------------------------------------------------------------------

def bridge_edit_seconds(bpm_from, bpm_to, edit_bars=8):
    """Duration (seconds) of the synthesized bridge edit.

    Bar i of the edit plays at bpm_from + (bpm_to-bpm_from)*i/edit_bars,
    so the edit's bar lengths shrink as it accelerates. Shared by
    premade_tempo_bridge_edit and its demo so the handoff time is exact.
    """
    total = 0.0
    for i in range(edit_bars):
        lb = bpm_from + (bpm_to - bpm_from) * i / edit_bars
        total += 4 * 60.0 / lb
    return total


def premade_tempo_bridge_edit(a, b, sr, bpm_from, bpm_to, bar_s,
                              edit_bars=8):
    """A produced-artifact bridge: an 8-bar edit that itself ramps tempo.

    Parameters
    ----------
    a : outgoing track segment (mono float64) at ~bpm_from.
    b : incoming track segment (mono float64) at ~bpm_to.
    sr : sample rate (Hz).
    bpm_from : tempo at the edit's first bar (beats/min).
    bpm_to : tempo at the edit's last bar (beats/min) — the ramp target.
    bar_s : seconds per bar at the caller grid (reference only; the
        edit's own bars are timed by bpm_from -> bpm_to).
    edit_bars : length of the bridge edit (bars, default 8 bars).

    Returns
    -------
    Mono float64 mix: A -> the edit section -> B. The edit is a
    synthesized drums + riser section (kick on every beat, offbeat
    hats, noise clap on beats 2 and 4, riser over the last 4 bars)
    whose per-bar tempo ramps linearly bpm_from -> bpm_to, peaking at
    -3 dBFS. No live pitch work happens anywhere in the move.

    Why it works
    ------------
    T-021 ramps tempo live (phase-vocoder, DJ riding the fader). The
    transition-edit workflow moves that labour into production: the
    bridge is a finished artefact with its own drums and riser, so the
    tempo change reads as *the record doing it*, and the DJ only has
    to cue two clean joins (A->edit, edit->B) instead of performing
    one continuous ramp. This is the standard open-format tool for
    wide jumps (e.g. 100 -> 128 BPM).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)

    parts = []
    for i in range(edit_bars):
        lb = bpm_from + (bpm_to - bpm_from) * i / edit_bars
        beat_n = int(60.0 / lb * sr)
        bar = np.zeros(4 * beat_n)
        kick = _synth_kick(sr, beat_n)
        hat = _synth_hat(sr, beat_n // 2, seed=3 + i)
        rng = np.random.default_rng(31 + i)
        clap_t = np.arange(beat_n // 2) / sr
        clap = (rng.standard_normal(beat_n // 2)
                * np.exp(-clap_t * 25.0))
        for beat in range(4):
            s0 = beat * beat_n
            bar[s0:s0 + beat_n] += kick * 0.9
            h0 = s0 + beat_n // 2
            bar[h0:h0 + beat_n // 2] += hat[:beat_n // 2] * 0.25
            if beat in (1, 3):
                bar[s0:s0 + beat_n // 2] += clap * 0.35
        parts.append(bar)
    edit = np.concatenate(parts) if parts else np.zeros(0)

    # continuous harmonic bed under the drums: a real transition edit
    # carries a tonal drone, and without it the gaps between kick hits
    # fall to digital silence (the demo tracks solve this the same way)
    if len(edit) > 0:
        t_e = np.arange(len(edit)) / sr
        bed = (np.sin(2 * np.pi * 110.0 * t_e)
               + 0.4 * np.sin(2 * np.pi * 165.0 * t_e)
               + 0.25 * np.sin(2 * np.pi * 220.0 * t_e))
        bed = bed / (np.max(np.abs(bed)) + 1e-9)
        lfo = 0.7 + 0.3 * np.sin(2 * np.pi * 0.125 * t_e)
        edit = edit + bed * lfo * 0.06

    # riser over the last 4 bars of the edit (its own, shorter, clock)
    if edit_bars >= 4 and len(edit) > 0:
        r_n = int(sum(len(p) for p in parts[-4:]))
        riser = dsp.synth_riser(r_n, sr, level_db=-14.0)
        edit[-r_n:] += riser
    peak = np.max(np.abs(edit)) if len(edit) else 0.0
    if peak > 1e-9:
        edit = edit / peak * dsp.db_to_gain(-3.0)
    return np.concatenate([a, edit, b])


# ----------------------------------------------------------------------------
# GAP-17 — Sampler one-shot mask (SYNTH, ADOPT)
# ----------------------------------------------------------------------------

def sampler_one_shot_mask(a, b, sr, one_shot_db=-3.0):
    """A synthesized one-shot fired exactly on a hard cut masks the join.

    Parameters
    ----------
    a : outgoing track segment (mono float64), ends at the cut.
    b : incoming track segment (mono float64), starts at the cut.
    sr : sample rate (Hz).
    one_shot_db : peak level of the one-shot (dBFS, default -3.0 dB).

    Returns
    -------
    Mono float64 mix: A (2 ms click guard on its tail) immediately
    followed by B, with a 0.45 s one-shot centred on the join — a
    falling saw burst (196 Hz, pitch sagging) plus a noise stab,
    both exponentially decaying — layered over the cut at one_shot_db.

    Why it works
    ------------
    A hard cut's weakness is the seam: two unrelated spectra meeting
    sample-to-sample. A one-shot at the join gives the ear a single
    foreground event to attend to (auditory masking) and marks the
    new section the way a DJ drop or air horn does socially. T-018
    builds from continuous noise and T-029's optional one-shot sits
    in a void — neither fires a shot *over a live cut*, which is the
    whole point here: the music never stops, the shot covers the join.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n_os = int(0.45 * sr)
    t = np.arange(n_os) / sr
    dur = n_os / sr
    saw = signal.sawtooth(2 * np.pi * 196.0 * t * (1.0 - 0.35 * t / dur))
    rng = np.random.default_rng(21)  # deterministic
    stab = rng.standard_normal(n_os) * 0.6
    one = saw * np.exp(-t * 9.0) + stab * np.exp(-t * 28.0)
    one = _guard(one, sr, ms=2.0)
    one = one / (np.max(np.abs(one)) + 1e-12) * dsp.db_to_gain(one_shot_db)

    # only A's tail needs the click guard (its head must stay untouched)
    a_out = a.copy()
    g = max(1, int(0.002 * sr))
    if g < len(a_out):
        a_out[-g:] *= 0.5 + 0.5 * np.cos(np.pi * np.linspace(0, 1, g))
    out = np.concatenate([a_out, b])
    j = len(a_out)
    lo = j - n_os // 2
    hi = lo + n_os
    s0, s1 = max(0, lo), min(len(out), hi)
    out[s0:s1] += one[s0 - lo:s1 - lo]
    return out


# ----------------------------------------------------------------------------
# PERF-ZAB — Feedback-loop build, Zabiela EFX-1000 move (PERF, ADOPT)
# ----------------------------------------------------------------------------

def feedback_loop_build(a, b, sr, bpm, bar_s, build_bars=8):
    """A's last phrase through a feedback delay whose feedback ramps up.

    Parameters
    ----------
    a : outgoing track segment (mono float64); its last `build_bars`
        are the build (earlier bars pass through untouched).
    b : incoming track segment (mono float64) — slams in at full level
        the moment the loop cuts.
    sr : sample rate (Hz).
    bpm : tempo (beats/min) — the delay is a 1/2-beat echo.
    bar_s : seconds per bar.
    build_bars : build length (bars, default 8 bars).

    Returns
    -------
    Mono float64 mix: A, with its last build_bars run through a
    feedback delay (1/2 beat) whose feedback ramps 0.5 -> 0.95 and
    whose wet mix ramps 0.25 -> 0.85 across the build; then a hard cut
    (2 ms guard) and B at full power. The feedback tail is cut WITH
    the loop — the slam is the payoff.

    Why it works
    ------------
    James Zabiela's signature EFX-1000 craft (edu-survey-G §4): a
    feedback loop is a build the *room's own sound* performs — each
    repeat is louder and denser than the last as feedback approaches
    unity, so tension rises without any new material. Cutting the
    loop dead and slamming B converts that stored energy into the
    drop. Evidence: Pioneer DJ "How To DJ" series / NXS2 trick
    videos (feedback loops, beat roll, transform), surveyed in
    edu-survey-G §4 (performer #2, L4 calibration material).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / bpm
    n_build = int(build_bars * bar_s * sr)
    n_build = min(n_build, len(a))
    head, seg = a[:-n_build], a[-n_build:]

    fb_env = np.linspace(0.5, 0.95, n_build)
    wet_env = np.linspace(0.25, 0.85, n_build)
    echoed = _tv_feedback_delay(seg, sr, 0.5 * beat_s, fb_env)
    build = (1.0 - wet_env) * seg + wet_env * echoed

    a_out = np.concatenate([head, build]) if len(head) else build
    g = max(1, int(0.002 * sr))
    if g < len(a_out):
        a_out = a_out.copy()
        a_out[-g:] *= 0.5 + 0.5 * np.cos(np.pi * np.linspace(0, 1, g))
    return np.concatenate([a_out, b])


# ----------------------------------------------------------------------------
# PERF-ZAB — Metric loop pivot, the 2020 3:4 demo (TIME, ADAPT)
# ----------------------------------------------------------------------------

def metric_loop_pivot(a, b, sr, bar_s, cycle_beats=3, total_beats=12):
    """Zabiela's 3:4 tempo modulation: A's bar retriggered every 3 beats.

    Parameters
    ----------
    a : outgoing track segment (mono float64). A 4-bar lead-in plays;
        its first bar is the groove cell that gets pivoted.
    b : incoming track segment (mono float64), entering in full at the
        alignment point.
    sr : sample rate (Hz).
    bar_s : seconds per bar.
    cycle_beats : retrigger period of the pivoted cell (beats,
        default 3 beats).
    total_beats : pivot duration (beats, default 12 beats) — must be
        a whole number of cycles; 12 = LCM(3, 4).

    Returns
    -------
    Mono float64 mix: 4 bars of A -> the pivot (A's 1-bar cell sliced
    to `cycle_beats` and tiled for `total_beats`) -> B at full level.

    Why it works
    ------------
    From Zabiela's 2020 tempo-modulation demo (edu-survey-G §4):
    house at 130 BPM becomes DnB at 173.4 BPM with NO sync, because
    the tempo ratio 173.4 / 130 = 4/3 is *metric*, not gradual.
    Retriggering a 4-beat cell every 3 beats makes the cell's downbeat
    walk against the 4-beat grid (3:4 polymeter); after 12 beats —
    the least common multiple — both grids agree again, and B enters
    at the new tempo on a downbeat both tempi share. The crowd hears
    a rhythm puzzle resolving, not a tempo change being performed.
    """
    if total_beats % cycle_beats != 0:
        raise ValueError("metric_loop_pivot: total_beats must be a "
                         "whole number of cycles (LCM alignment)")
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(bar_s * sr)
    beat_n = max(1, bar_n // 4)
    lead = a[-4 * bar_n:] if len(a) >= 4 * bar_n else a
    cell = _fit(a[:bar_n], bar_n)
    chunk = cell[:cycle_beats * beat_n]
    pivot = np.tile(chunk, total_beats // cycle_beats)
    pivot = pivot[:total_beats * beat_n]
    return np.concatenate([lead, pivot, b])


# ----------------------------------------------------------------------------
# Metadata (FRAMEWORK.md §3) + TECHNIQUE_FUNCS export
# ----------------------------------------------------------------------------

META = {
    "sample_connection": {
        "title": "Sample Connection (Sample Switch-Up)",
        "bank": "GAP-01", "family": "TIME", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 5.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "verse", "chorus", "drop"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": ["sample_link"]},
        "prefers": [
            {"when": "sample_link", "weight": 5,
             "reason": "the shared sampled element IS the connection"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "snap", "clash_risk": "none",
        "params": {"hit_len_s": {"type": "float", "range": [0.1, 2.0],
                                 "default": 0.5, "unit": "s"}},
        "evidence": [
            {"type": "tutorial",
             "ref": "Transition Gap Report 2026-10-19 GAP-01 — DDT + open-format (sample connection / sample switch-up)",
             "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    "loop_tightening_build": {
        "title": "Loop-Tightening Build (Hype Loops)",
        "bank": "GAP-02", "family": "TIME", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 5.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "neither"],
                     "phrase_a_ok": ["build", "outro", "chorus"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": ["b_build"]},
        "prefers": [
            {"when": "energy_delta>=2", "weight": 3,
             "reason": "the tightening loop manufactures the lift into B"},
        ],
        "energy": {"delta": 1, "tension": "build"},
        "exit": "snap", "clash_risk": "vocal",
        "params": {},
        "evidence": [
            {"type": "tutorial",
             "ref": "Transition Gap Report 2026-10-19 GAP-02 — Hype + open-format (Hype Loops / loop-tightening)",
             "url": None, "date": "2026-10-19"},
            {"type": "course",
             "ref": "James Hype 'Hype Loops' method via edu-survey-G §4 (performer #1)",
             "url": None, "date": None},
        ],
        "composed_of": [],
    },
    "polyrhythmic_loops": {
        "title": "Polyrhythmic Loops (3-vs-4 Bed)",
        "bank": "GAP-04", "family": "TIME", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 3.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "neither"],
                     "phrase_a_ok": ["outro", "chorus", "drop"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta_abs<=1", "weight": 2,
             "reason": "the bed evolves in place — a lateral, patient move"},
        ],
        "energy": {"delta": 0, "tension": "build"},
        "exit": "seamless", "clash_risk": "bass",
        "params": {},
        "evidence": [
            {"type": "tutorial",
             "ref": "Transition Gap Report 2026-10-19 GAP-04 — open-format (polyrhythmic looping)",
             "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    "slip_mode_flourish": {
        "title": "Slip-Mode Flourish",
        "bank": "GAP-05", "family": "TIME", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "chorus", "drop", "verse"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_a>=6", "weight": 1,
             "reason": "a busy floor forgives a flourish; a thin one exposes it"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "seamless", "clash_risk": "none",
        "params": {"flourish_beats": {"type": "float",
                                      "range": [0.5, 4.0],
                                      "default": 1.0, "unit": "beats",
                                      "presets": {"half": 0.5, "one": 1.0,
                                                  "two": 2.0}}},
        "evidence": [
            {"type": "tutorial",
             "ref": "Transition Gap Report 2026-10-19 GAP-05 — open-format (slip-mode flourish, general)",
             "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    "premade_tempo_bridge_edit": {
        "title": "Pre-Made Tempo-Bridge Edit (Transition Track)",
        "bank": "GAP-07", "family": "DYN", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "build", "chorus", "drop"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "bpm_delta_pct>=8", "weight": 3,
             "reason": "wide tempo jump — the produced edit does the ramp"},
            {"when": "genre_pair==leap", "weight": 1,
             "reason": "the edit is a third artefact — genre rules suspend inside it"},
        ],
        "energy": {"delta": 1, "tension": "build"},
        "exit": "snap", "clash_risk": "none",
        "params": {"edit_bars": {"type": "int", "range": [4, 16],
                                 "default": 8, "unit": "bars",
                                 "presets": {"4bar": 4, "8bar": 8,
                                             "16bar": 16}}},
        "evidence": [
            {"type": "tutorial",
             "ref": "Transition Gap Report 2026-10-19 GAP-07 — open-format (pre-made tempo-bridge edit / transition track)",
             "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    "sampler_one_shot_mask": {
        "title": "Sampler One-Shot Mask",
        "bank": "GAP-17", "family": "SYNTH", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "drop", "chorus", "build"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "camelot>=4", "weight": 2,
             "reason": "the shot masks exactly the clash a cut would expose"},
            {"when": "genre_pair==leap", "weight": 2,
             "reason": "the shot marks the leap as intentional"},
        ],
        "energy": {"delta": 0, "tension": "reset"},
        "exit": "snap", "clash_risk": "none",
        "params": {"one_shot_db": {"type": "float", "range": [-12.0, 0.0],
                                   "default": -3.0, "unit": "dB"}},
        "evidence": [
            {"type": "tutorial",
             "ref": "Transition Gap Report 2026-10-19 GAP-17 — open-format (sampler one-shot mask)",
             "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    "feedback_loop_build": {
        "title": "Feedback-Loop Build (Zabiela EFX-1000)",
        "bank": "PERF-ZAB", "family": "PERF", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 5.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "neither"],
                     "phrase_a_ok": ["outro", "build", "chorus"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta>=1", "weight": 2,
             "reason": "stored feedback energy converts straight into B's drop"},
        ],
        "energy": {"delta": 1, "tension": "build"},
        "exit": "snap", "clash_risk": "none",
        "params": {"build_bars": {"type": "int", "range": [2, 16],
                                  "default": 8, "unit": "bars",
                                  "presets": {"4bar": 4, "8bar": 8}}},
        "evidence": [
            {"type": "clip",
             "ref": "edu-survey-G §4, performer #2 James Zabiela — Pioneer EFX-1000/DJM beat-FX composition (feedback loops, beat roll, transform); Pioneer DJ 'How To DJ' series (2009) + NXS2 trick videos",
             "url": None, "date": None},
        ],
        "composed_of": [],
    },
    "metric_loop_pivot": {
        "title": "Metric Loop Pivot (3:4 Tempo Modulation)",
        "bank": "PERF-ZAB", "family": "TIME", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "neither"],
                     "phrase_a_ok": ["outro", "chorus", "drop"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "bpm_delta_pct>=20", "weight": 3,
             "reason": "a 4:3 metric ratio (e.g. 130 -> 173.4) is free — no ramp, no sync"},
        ],
        "energy": {"delta": 1, "tension": "build"},
        "exit": "snap", "clash_risk": "none",
        "params": {"cycle_beats": {"type": "int", "range": [2, 4],
                                   "default": 3, "unit": "beats",
                                   "presets": {"3beat": 3}},
                   "total_beats": {"type": "int", "range": [6, 24],
                                   "default": 12, "unit": "beats",
                                   "presets": {"12beat": 12}}},
        "evidence": [
            {"type": "clip",
             "ref": "edu-survey-G §4, performer #2 James Zabiela — 2020 3:4 tempo-modulation demo (house 130 -> DnB 173.4 via layered 3/4 and 3/2 loops, no sync)",
             "url": None, "date": "2020"},
        ],
        "composed_of": [],
    },
}


def _is_pair_fn(fn):
    """Signature check for the render pipeline contract.

    engine/render.py calls TECHNIQUE_FUNCS entries as fn(a, b, sr, **args):
    the first two positional parameters must be named `a` and `b`, and an
    `sr` parameter must exist. Anything else is excluded — honestly, not
    wrapped — so the export list never lies about call compatibility.
    """
    try:
        params = list(inspect.signature(fn).parameters.values())
    except (TypeError, ValueError):
        return False
    if len(params) < 3:
        return False
    names = [p.name for p in params]
    return names[0] == "a" and names[1] == "b" and "sr" in names


_ALL_FUNCS = {
    "sample_connection": sample_connection,
    "loop_tightening_build": loop_tightening_build,
    "polyrhythmic_loops": polyrhythmic_loops,
    "slip_mode_flourish": slip_mode_flourish,
    "premade_tempo_bridge_edit": premade_tempo_bridge_edit,
    "sampler_one_shot_mask": sampler_one_shot_mask,
    "feedback_loop_build": feedback_loop_build,
    "metric_loop_pivot": metric_loop_pivot,
}

# Qualify (fn(a, b, sr, **kwargs)): sample_connection, polyrhythmic_loops,
# premade_tempo_bridge_edit, sampler_one_shot_mask, feedback_loop_build,
# metric_loop_pivot.
# Excluded: loop_tightening_build (first input is `loop_src`, a loop
# fragment, not the outgoing track — positional pair-calling would be a
# semantic lie) and slip_mode_flourish (single-deck move over A; there is
# no `b` at all). Both are demoed via demos/ext_gap_rest.py, which calls
# them with their true signatures.
TECHNIQUE_FUNCS = {tid: fn for tid, fn in _ALL_FUNCS.items()
                   if _is_pair_fn(fn)}
