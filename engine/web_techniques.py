"""
open-transitions engine — web-mined techniques (domain module,
FRAMEWORK.md §7).

Eighteen techniques mined from DJ literature outside the bank
(2026-10-21 tranches; banked as WEB-01..WEB-18 in
technique-bank/TECHNIQUES.md with full provenance). Each function
takes numpy mono float64 audio + sr and returns mono float64.
Docstrings are the spec source; techniques/<name>.md mirrors them.

  WEB-01 spiral_echo     feedback delay whose repeats pitch-shift
                         (Pioneer DJM SPIRAL beat FX, rendered)
  WEB-02 flanger_sweep   feedback-jet comb sweep over A's final bars
  WEB-03 reverse_roll    reversed loop-sampler roll build (REV ROLL)
  WEB-04 crush_degrade   bit-depth + sample-rate degradation exit
  WEB-05 shepard_riser   Shepard-Risset endless-rise build layer
  WEB-06 granular_freeze frozen-moment grain-cloud handoff
  WEB-07 helix_catch     loop-sampler catch, pitch ramps during the
                         hold, release snaps home into B (DJM HELIX)
  WEB-08 beatslicer_shuffle  A's final bar(s) slice-permuted as a
                         build (Traktor BeatSlicer)
  WEB-09 downlifter_exit descending synth sweep across the seam —
                         the riser's mirror, masking the cut
  WEB-10 shimmer_wash    octave-up pitch-shifted reverb exit tail
                         (RMX-1000 Reverb Up / shimmer principle)
  WEB-11 infinity_filter endless barber-pole resonant sweep exit
                         (Serato Infinity Filter / Shepard Filter)
  WEB-12 pattern_layer_bridge  synthesized Pattern Player drum
                         layer carrying the seam (Traktor Pro 4)
  WEB-13 pumper_exit     beat-synced duck pump exit: A's final bars
                         duck on the downbeat, the last recovery is
                         withheld, B fills the hole (Denon Pumper)
  WEB-14 scale_down_exit captured beat replays down a musical
                         scale, one beat-locked step at a time
                         (Engine DJ Scale Down / Pitch Down)
  WEB-15 fader_synth     source-replacing fader oscillator line
                         across the seam (Pioneer DJM-S11 FADER
                         SYNTH)
  WEB-16 ring_mod_dissolve  carrier-multiplication dissolve: A's
                         final bars ring-modulate away under a
                         rising carrier (Traktor Ring Modulator)
  WEB-17 formant_morph_exit  A's final bars morph through a vowel
                         formant series (Traktor Formant Filter)
  WEB-18 resonator_tail  A's final bars ring away through a tuned
                         five-resonator bank voiced as B's chord
                         (Ableton Resonators)
  WEB-19 continuous_drop A's drop plays out with B staged beneath
                         its final bars; B's drop lands on the
                         downbeat A's ends (DnB drop-to-drop relay)
  WEB-20 drop_chop       two landed drops alternate full-level
                         ownership on a bar grid, then commit to B
                         (DnB / riddim chopping between drops)
  WEB-21 drop_insert     B's drop substitutes for A's for 1-4 bars
                         at the drop downbeat, then A's drop resumes
                         (the guest bar; dubstep switch, shortest form)

All twenty-one are two-track renderers, exported via TECHNIQUE_FUNCS.
WEB-19..21 were mined in Phase 23 (genre traditions tranche A) from
fetched DnB/dubstep texts — see technique-bank/TECHNIQUES.md.
"""

import numpy as np
from scipy import signal

from . import dsp


def _edge_fades(x, sr, fade_ms=5.0):
    """Protective raised-cosine fades at both ends (click avoidance only)."""
    n = len(x)
    f = min(int(fade_ms / 1000.0 * sr), n // 2)
    if f > 1:
        x = x.copy()
        x[:f] *= dsp.raised_cosine(f, up=True)
        x[-f:] *= dsp.raised_cosine(f, up=False)
    return x


def _seam_concat(a, b, sr, guard_ms=3.0):
    """Concatenate with a short crossfade at the seam (click guard).

    Length is len(a) + len(b) - guard. Used where the technique's design
    is a hard join (a flanged/crushed A handing to a dry B) — the guard
    is 3 ms, far below any rhythmic perception; the cut stays a cut.
    """
    g = min(int(guard_ms / 1000.0 * sr), len(a), len(b))
    if g <= 1:
        return np.concatenate([a, b])
    w = np.linspace(0.0, 1.0, g)
    mid = a[-g:] * (1.0 - w) + b[:g] * w
    return np.concatenate([a[:-g], mid, b[g:]])


def _frac_delay(x, delay_samples):
    """Fractional delay line: y[i] = x[i - delay_samples[i]], linear
    interpolation, zero before the start."""
    n = len(x)
    idx = np.arange(n, dtype=np.float64) - np.asarray(delay_samples,
                                                      dtype=np.float64)
    return np.interp(idx, np.arange(n, dtype=np.float64), x,
                     left=0.0, right=0.0)


# ----------------------------------------------------------------------------
# WEB-01 — Spiral Echo (pitch-riding feedback delay)
# ----------------------------------------------------------------------------

def spiral_echo(a, b, sr, bpm, bar_s, delay_beats=0.75,
                shift_semitones=2.0, repeats=8, feedback=0.62,
                fade_bars=2.0):
    """Spiral echo: A's last fragment recirculates, pitch-shifting per repeat.

    The Pioneer DJM SPIRAL beat FX changes delay time as it repeats, so
    pitch rides with it: every return of the echo comes back shifted.
    This renders the transition use: `a` plays dry to its end (the
    fader-kill moment), its final `delay_beats` fragment is thrown into
    the spiral, and the tail of pitch-climbing (or pitch-diving) repeats
    decays across `b`'s entrance — B fades up underneath over
    `fade_bars` while the tail evaporates. Output is len(a) + len(b).

    Parameters
    ----------
    a : outgoing segment (mono float64); the thrown fragment is its
        final `delay_beats`.
    b : incoming segment (mono float64), faded in over `fade_bars`
        starting at the handoff (len(a)).
    sr : sample rate, Hz.
    bpm : tempo of the pair (sets the delay grid).
    bar_s : seconds per bar (sets B's fade).
    delay_beats : delay time in beats (default 0.75 — the dotted value
        the DJM SPIRAL is most often thrown at).
    shift_semitones : pitch step per repeat, signed (default +2.0 —
        spiral up; negative spirals down). This is a *tail* effect:
        the T-032 ±2 formant rule governs vocal overlays, not decaying
        echo repeats; later repeats are `feedback`-attenuated whispers.
    repeats : number of repeats rendered (default 8).
    feedback : per-repeat gain (default 0.62, the DJM LEVEL/DEPTH
        mid-position behaviour).
    fade_bars : B's entrance fade in bars (default 2.0).

    Why it works: an ordinary echo tail keeps the outgoing track's
    pitch center alive under the next track — a clash risk the
    selection layer must police. A spiral tail *leaves* the pitch
    center with every repeat, so it reads as the track evaporating
    rather than ending: B owns the tonal space from its first bar
    while A's rhythm still ghosts across the entrance.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / float(bpm)
    delay_n = max(256, int(round(delay_beats * beat_s * sr)))
    if len(a) >= delay_n:
        seg = a[-delay_n:]
    else:
        seg = np.pad(a, (delay_n - len(a), 0))

    tail = np.zeros(delay_n * int(repeats))
    for k in range(1, int(repeats) + 1):
        rep = dsp.pitch_shift(seg, sr, shift_semitones * k)
        if len(rep) >= delay_n:
            rep = rep[:delay_n]
        else:
            rep = np.pad(rep, (0, delay_n - len(rep)))
        tail[(k - 1) * delay_n:k * delay_n] += rep * (float(feedback) ** k)
    # Tail dies out smoothly instead of truncating mid-repeat.
    f = min(delay_n, len(tail))
    if f > 1:
        tail[-f:] *= dsp.raised_cosine(f, up=False)

    out = np.zeros(len(a) + len(b))
    out[:len(a)] += a
    out[len(a):len(a) + len(tail)] += tail
    fade_n = min(len(b), int(round(fade_bars * bar_s * sr)))
    if fade_n > 0:
        env = np.ones(len(b))
        env[:fade_n] = dsp.raised_cosine(fade_n, up=True)
        out[len(a):] += b * env
    else:
        out[len(a):] += b
    return out


# ----------------------------------------------------------------------------
# WEB-02 — Flanger Sweep (jet comb build/exit)
# ----------------------------------------------------------------------------

def flanger_sweep(a, b, sr, bar_s, sweep_bars=8, cycles=2.0,
                  depth_ms=2.2, base_ms=0.35, mix=0.85):
    """Flanger sweep: a jet comb washes A's final bars; B enters dry.

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
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    zone_n = min(len(a), int(round(sweep_bars * bar_s * sr)))
    if zone_n < 16:
        return _seam_concat(a, b, sr)
    zone = a[-zone_n:]
    t = np.arange(zone_n) / float(sr)
    zone_s = zone_n / float(sr)
    phase = 2.0 * np.pi * float(cycles) * t / zone_s
    d_ms = base_ms + depth_ms * (0.5 - 0.5 * np.cos(phase))
    d1 = _frac_delay(zone, d_ms * sr / 1000.0)
    d2 = _frac_delay(zone, 2.0 * d_ms * sr / 1000.0)
    ramp_n = min(int(round(bar_s * sr)), zone_n)
    ramp = np.ones(zone_n)
    if ramp_n > 0:
        ramp[:ramp_n] = dsp.raised_cosine(ramp_n, up=True)
    wet = zone + float(mix) * ramp * (0.75 * d1 + 0.35 * d2)
    a_out = a.copy()
    a_out[-zone_n:] = wet
    return _seam_concat(a_out, b, sr)


# ----------------------------------------------------------------------------
# WEB-03 — Reverse Roll (reversed loop-sampler build)
# ----------------------------------------------------------------------------

def _tile_window(n, sr):
    """Trapezoid click-guard for one roll tile: 1 ms edges, flat middle."""
    g = max(1, min(n // 4, int(0.001 * sr)))
    w = np.ones(n)
    if n > 2 * g:
        w[:g] = np.linspace(0.3, 1.0, g)
        w[-g:] = np.linspace(1.0, 0.3, g)
    return w


def reverse_roll(a, b, sr, bar_s, roll_bars=2):
    """Reverse roll: A's last beat loops backwards, tightening, into B.

    The Pioneer REV ROLL beat FX grabs a beat fraction and loops it
    reversed. As a transition: `a` plays clean, then its final beat is
    grabbed and tiled backwards across the last `roll_bars` — the tile
    length halves every two tiles (1 beat -> 1/2 -> 1/4 -> 1/8), so the
    reversed suck inward accelerates — and `b` releases on the downbeat
    the roll was consuming. Output is len(a) + len(b).

    Parameters
    ----------
    a : outgoing segment (mono float64); its final beat is the grabbed
        material, its final `roll_bars` are the roll zone.
    b : incoming segment (mono float64), entered at len(a).
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    roll_bars : roll zone length in bars (default 2).

    Why it works: forward rolls (T-008) build by insistence — the same
    hit harder and faster. Reversed tiles build by *inhalation*: every
    transient sucks back into the deck instead of punching out, the
    phrase feels vacuumed away, and B's first downbeat exhales. It is
    the mirror mechanism of the backspin (T-007) — but where a backspin
    is one continuous spin of the whole tail, the reverse roll stays on
    the grid, so B can land beat-locked.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    beat_n = max(64, bar_n // 4)
    zone_n = min(len(a), int(roll_bars) * bar_n)
    if len(a) < beat_n or zone_n < beat_n // 2:
        return _seam_concat(a, b, sr)
    rev = a[-beat_n:][::-1].copy()

    tiles = []
    remaining = zone_n
    f = beat_n
    reps_at_f = 0
    while remaining > 0:
        tl = min(f, remaining)
        tiles.append(tl)
        remaining -= tl
        reps_at_f += 1
        if reps_at_f >= 2:
            f = max(beat_n // 8, f // 2)
            reps_at_f = 0
    roll = np.concatenate([rev[:tl] * _tile_window(tl, sr) for tl in tiles])
    out = np.concatenate([a[:len(a) - zone_n], roll])
    return _seam_concat(out, b, sr)


# ----------------------------------------------------------------------------
# WEB-04 — Crush Degrade (bit-reduction exit)
# ----------------------------------------------------------------------------

def crush_degrade(a, b, sr, bar_s, bars=4, bits_end=5.0, rate_end=0.25,
                  fade_bars=1.0):
    """Crush degrade: A degrades to lo-fi over its final bars; B is clean.

    Pioneer's Crush Colour FX reduces bit resolution (paired with a
    filter); the RMX line adds the crushed echo. As a transition the
    full recipe is: across A's final `bars`, bit depth ramps 16 ->
    `bits_end`, the effective sample rate folds down to `rate_end` of
    the original (sample-hold), and a low-pass folds 12 kHz -> 700 Hz
    alongside. During the final `fade_bars` the crushed ghost
    equal-power-crossfades into `b` arriving at full fidelity — the
    fidelity contrast itself is the drop. Output length is
    len(a) + len(b) - fade.

    Parameters
    ----------
    a : outgoing segment (mono float64); the crush zone is its final
        `bars`.
    b : incoming segment (mono float64), clean, faded in across the
        crush zone's last `fade_bars`.
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    bars : crush zone length in bars (default 4).
    bits_end : final bit depth (default 5.0 — unmistakably crushed,
        still rhythmic).
    rate_end : final sample-rate fraction (default 0.25).
    fade_bars : B's crossfade length in bars (default 1.0).

    Why it works: fidelity is an energy dimension. The crowd hears A
    turn into a toy version of itself — same groove, collapsing
    resolution — while B assembles in full range underneath. No pitch,
    key, or tempo negotiation is involved, so the move is legal across
    genre leaps where blends are not.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    zone_n = min(len(a), int(round(bars * bar_s * sr)))
    if zone_n < 1024:
        return _seam_concat(a, b, sr)
    zone = a[-zone_n:]
    block = 512
    zc = zone.copy()
    for s in range(0, zone_n, block):
        e = min(zone_n, s + block)
        p = (s + block / 2.0) / zone_n
        bits = 16.0 + (float(bits_end) - 16.0) * p
        q = 2.0 ** (bits - 1.0)
        seg = np.round(zc[s:e] * q) / q
        k = max(1, int(round(1.0 + (1.0 / float(rate_end) - 1.0) * p)))
        if k > 1:
            idx = (np.arange(e - s) // k) * k
            seg = seg[idx]
        zc[s:e] = seg
    env = np.exp(np.linspace(np.log(12000.0), np.log(700.0), zone_n))
    zc = dsp.sweep_filter(zc, sr, env, ftype="lowpass")
    a_out = a.copy()
    a_out[-zone_n:] = zc

    fade_n = min(int(round(fade_bars * bar_s * sr)), zone_n, len(b))
    if fade_n <= 0:
        return _seam_concat(a_out, b, sr)
    out = np.zeros(len(a) + len(b) - fade_n)
    out[:len(a)] = a_out
    w = np.linspace(0.0, 1.0, fade_n)
    seg = out[len(a) - fade_n:len(a)].copy()
    out[len(a) - fade_n:len(a)] = (seg * np.cos(w * np.pi / 2.0)
                                   + b[:fade_n] * np.sin(w * np.pi / 2.0))
    out[len(a):] += b[fade_n:]
    return out


# ----------------------------------------------------------------------------
# WEB-05 — Shepard Riser (endless-rise build layer)
# ----------------------------------------------------------------------------

def shepard_riser(a, b, sr, bar_s, bars=8, direction=1, level_db=-9.0,
                  partials=7, base_hz=55.0, center_hz=640.0,
                  sigma_oct=1.15):
    """Shepard riser: an endless-rise synth layer under A's final bars.

    A Shepard-Risset glissando: `partials` sine partials spaced in
    octaves above `base_hz`, all gliding up (or down) together through
    repeated octave cycles, each partial's level wrapped in a Gaussian
    envelope over log-frequency centered at `center_hz` — partials fade
    in at the bottom of the spectrum and out at the top, so the pitch
    seems to rise forever without ever getting higher. Pioneer's DJM
    Mobius beat FX applies the same illusion as a filter; this renders
    it as a synthesized layer (the T-018/T-035 riser family member that
    cannot run out of headroom). The layer fades in over the first bar
    of the zone, sits at `level_db` relative to A's peak, and cuts dead
    on the handoff — `b` inherits all the unresolved rising tension.
    Output is len(a) + len(b) (3 ms seam guard).

    Parameters
    ----------
    a : outgoing segment (mono float64); the layer zone is its final
        `bars`.
    b : incoming segment (mono float64), entered at len(a).
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    bars : layer zone length in bars (default 8); the glide completes
        one octave cycle per 4 bars.
    direction : +1 rises, -1 falls (default +1).
    level_db : layer peak relative to A's peak (default -9.0 dB —
        presence without masking).
    partials : number of octave partials (default 7).
    base_hz : lowest partial's starting frequency (default 55 Hz).
    center_hz : Gaussian envelope center (default 640 Hz).
    sigma_oct : envelope width in octaves (default 1.15).

    Why it works: a conventional riser spends pitch and loudness and
    arrives; the Shepard layer never arrives, so tension can stretch
    across a whole phrase without the fatigue of a sound that is
    literally getting louder and higher the whole time. The only
    resolution on offer is B's first bar.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    zone_n = min(len(a), int(round(bars * bar_s * sr)))
    if zone_n < 1024:
        return _seam_concat(a, b, sr)
    t = np.arange(zone_n) / float(sr)
    zone_s = zone_n / float(sr)
    cycles = max(1.0, float(bars) / 4.0)
    frac = (t * cycles / zone_s) % 1.0
    if direction < 0:
        frac = (1.0 - frac) % 1.0
    layer = np.zeros(zone_n)
    for k in range(int(partials)):
        f = float(base_hz) * 2.0 ** (k + frac)
        amp = np.exp(-(np.log2(f / float(center_hz)) ** 2)
                     / (2.0 * float(sigma_oct) ** 2))
        phase = 2.0 * np.pi * np.cumsum(f) / float(sr)
        layer += amp * np.sin(phase)
    peak_layer = np.max(np.abs(layer))
    peak_a = np.max(np.abs(a)) if len(a) else 0.0
    if peak_layer > 0 and peak_a > 0:
        layer *= (dsp.db_to_gain(float(level_db)) * peak_a) / peak_layer
    ramp_n = min(int(round(bar_s * sr)), zone_n)
    if ramp_n > 0:
        layer[:ramp_n] *= dsp.raised_cosine(ramp_n, up=True)
    layer = _edge_fades(layer, sr, fade_ms=2.0)
    a_out = a.copy()
    a_out[-zone_n:] += layer
    return _seam_concat(a_out, b, sr)


# ----------------------------------------------------------------------------
# WEB-06 — Granular Freeze (frozen-moment cloud handoff)
# ----------------------------------------------------------------------------

def granular_freeze(a, b, sr, bar_s, cloud_bars=4, capture_ms=150.0,
                    grain_ms=70.0, density=45.0, drift=0.7, seed=7):
    """Granular freeze: A's last moment becomes a grain cloud; B enters in it.

    At the freeze point (`cloud_bars` before A's end), a `capture_ms`
    fragment of `a` is sustained as a cloud of overlapping Hann-windowed
    grains — the Amazing Noises Grain Freezer recipe (capture ~150 ms,
    sustain as a texture of up to dozens of simultaneous grains). Across
    the cloud zone the grain read position drifts forward through the
    capture (`drift` of its length) while `b` equal-power-fades up
    *inside* the cloud; at the zone's end the cloud is gone and B plays
    alone. Output length is len(a) - cloud_zone + len(b).

    The cloud is A's own material — its harmonics, its formants — with
    its rhythm and pitch commitment dissolved by the grain window,
    which is exactly what separates this from T-034 (reverb freeze
    freezes the *room's* tail; this freezes the *source*).

    Parameters
    ----------
    a : outgoing segment (mono float64); the capture is taken from
        just before the freeze point.
    b : incoming segment (mono float64); its first `cloud_bars` play
        inside the cloud.
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    cloud_bars : cloud zone length in bars (default 4).
    capture_ms : captured fragment length (default 150 ms, the Grain
        Freezer's capture size).
    grain_ms : grain length (default 70 ms).
    density : grains per second (default 45 — dense enough to read as
        texture, sparse enough to keep the source's grain).
    drift : how far the read position scans through the capture across
        the zone, as a fraction (default 0.7).
    seed : grain-position jitter seed (default 7) — the render is
        deterministic; the jitter is frozen into the recipe.

    Why it works: the ear recognizes the cloud as *made of A* while
    owing it no beat or key allegiance, so B can enter at any tempo or
    key inside it and still feel handed-over rather than interrupted —
    a texture bridge whose provenance is the audio itself.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    zone_n = int(round(cloud_bars * bar_s * sr))
    freeze = len(a) - zone_n
    if freeze <= 0 or len(b) <= zone_n:
        return _seam_concat(a, b, sr)
    cap_n = int(round(capture_ms / 1000.0 * sr))
    grain_n = max(64, int(round(grain_ms / 1000.0 * sr)))
    cap = a[max(0, freeze - cap_n):freeze]
    if len(cap) < grain_n:
        cap = np.pad(cap, (0, grain_n - len(cap)), mode="wrap")
    win = np.hanning(grain_n)
    rng = np.random.default_rng(int(seed))
    hop = max(1, int(round(sr / float(density))))
    cloud = np.zeros(zone_n + grain_n)
    max_start = max(1, len(cap) - grain_n)
    for start in range(0, zone_n, hop):
        u = start / max(1, zone_n)
        center = (u * float(drift) * max_start
                  + rng.uniform(-0.1, 0.1) * grain_n)
        s0 = int(np.clip(center, 0, max_start))
        cloud[start:start + grain_n] += cap[s0:s0 + grain_n] * win
    cloud = cloud[:zone_n]
    rms_cap = float(np.sqrt(np.mean(cap ** 2))) + 1e-12
    rms_cloud = float(np.sqrt(np.mean(cloud ** 2))) + 1e-12
    cloud *= rms_cap / rms_cloud
    u = np.linspace(0.0, 1.0, zone_n)
    zone = (cloud * np.cos(u * np.pi / 2.0)
            + b[:zone_n] * np.sin(u * np.pi / 2.0))
    return np.concatenate([a[:freeze], zone, b[zone_n:]])


# ----------------------------------------------------------------------------
# WEB-07 — Helix Catch (loop-sampler pitch-ramp hold & release)
# ----------------------------------------------------------------------------

def helix_catch(a, b, sr, bpm, bar_s, capture_beats=1.0, hold_bars=2,
                ramp_semitones=12.0, fade_bars=0.5):
    """Helix catch: A's final fragment loops while its pitch ramps; B
    enters at natural pitch on the release.

    The Pioneer DJM HELIX beat FX captures the playing sound into a
    loop the moment it engages; while held, the loop's pitch changes
    progressively (LEVEL/DEPTH sets the ramp — turned fully right it
    *fixes* the pitch, rendered here as ramp_semitones=0); on release
    the pitch returns to the point where the effect was switched on.
    This renders the transition use: `a` plays dry, its final
    `capture_beats` fragment is caught and looped for `hold_bars`
    bars with the playback rate (pitch-coupled, like the hardware)
    ramping linearly in semitones from 0 to `ramp_semitones`, then
    the hold ends and `b` enters faded over `fade_bars` at its own
    pitch — the ramp's tension resolves into the new track instead
    of evaporating (contrast WEB-01's decaying spiral tail).

    Parameters
    ----------
    a : outgoing segment (mono float64); the caught fragment is its
        final `capture_beats`.
    b : incoming segment (mono float64), faded in over `fade_bars`
        starting at the release.
    sr : sample rate, Hz.
    bpm : tempo of the pair (sets the capture grid).
    bar_s : seconds per bar (sets the hold length and B's fade).
    capture_beats : caught fragment length in beats (default 1.0).
    hold_bars : hold length in bars (default 2).
    ramp_semitones : total pitch ramp across the hold, signed
        (default +12.0 — one octave up; 0.0 renders the fixed-pitch
        loop behaviour).
    fade_bars : B's entrance fade in bars (default 0.5 — the release
        is a near-snap by design).

    Why it works: a caught loop is the outgoing track insisting on
    staying; the continuous pitch ramp makes that insistence
    unstable, so the ear waits for the release. The loop is A's own
    material on A's own grid, so B can enter beat-locked the moment
    the helix lets go.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / float(bpm)
    frag_n = max(256, int(round(capture_beats * beat_s * sr)))
    if len(a) >= frag_n:
        pre, frag = a[:-frag_n], a[-frag_n:]
    else:
        pre = np.zeros(0)
        frag = np.pad(a, (frag_n - len(a), 0))
    hold_n = max(frag_n, int(round(hold_bars * bar_s * sr)))
    u = np.linspace(0.0, 1.0, hold_n)
    rate = 2.0 ** (float(ramp_semitones) * u / 12.0)
    # warp_resample consumes source at cumsum(rate); tile the fragment
    # so the read head never runs dry (worst case: max rate throughout).
    need = int(np.sum(rate)) + frag_n
    reps = int(np.ceil(need / max(1, frag_n))) + 1
    src = np.tile(frag, reps)
    hold = dsp.warp_resample(src, sr, rate, out_len=hold_n)
    hold = _edge_fades(hold, sr, 5.0)
    held = np.concatenate([pre, hold]) if len(pre) else hold

    fade_n = min(len(b), int(round(fade_bars * bar_s * sr)))
    if fade_n > 0:
        env = np.ones(len(b))
        env[:fade_n] = dsp.raised_cosine(fade_n, up=True)
        b = b * env
    return _seam_concat(held, b, sr)


# ----------------------------------------------------------------------------
# WEB-08 — BeatSlicer Shuffle (buffer slice-permutation build)
# ----------------------------------------------------------------------------

_SLICE_PATTERNS = {
    "identity": [0, 1, 2, 3, 4, 5, 6, 7],
    "reverse": [7, 6, 5, 4, 3, 2, 1, 0],
    "swap_pairs": [1, 0, 3, 2, 5, 4, 7, 6],
    "bookends": [0, 7, 1, 6, 2, 5, 3, 4],
    "stride": [0, 2, 4, 6, 1, 3, 5, 7],
    "halves": [4, 5, 6, 7, 0, 1, 2, 3],
    "inside_out": [3, 4, 2, 5, 1, 6, 0, 7],
}


def beatslicer_shuffle(a, b, sr, bar_s, pattern="stride",
                       buffer_bars=1, buzz=1):
    """BeatSlicer shuffle: A's final bar(s) replayed slice-permuted,
    then B releases on the downbeat.

    Traktor's BeatSlicer buffers up to 2 bars, subdivides the buffer
    into small chunks and replays them in a different sequence — "a
    rhythmically shuffled version of the original music" — from 20
    hardware patterns in 5 styles. This renders the transition use:
    `a` plays dry; its final `buffer_bars` bars are re-dealt as 8
    slices per bar replayed in the named permutation `pattern`; the
    effect's BUZZ control is rendered as a half-slice self-repeat on
    the final beat when `buzz` is 1; `b` then enters on the next
    downbeat through a 3 ms seam guard. The shuffled region is
    exactly as long as the region it replaces — permutation scrambles
    order, never the grid.

    Parameters
    ----------
    a : outgoing segment (mono float64); its final `buffer_bars`
        bars are the slicer's buffer.
    b : incoming segment (mono float64), entering dry at the seam.
    sr : sample rate, Hz.
    bar_s : seconds per bar (the buffer and slice grids).
    pattern : permutation name — one of identity, reverse,
        swap_pairs, bookends, stride, halves, inside_out
        (default "stride").
    buffer_bars : buffered bars, 1 or 2 (default 1; the hardware
        buffers 2 bars and applies its pattern across them).
    buzz : 1 renders the BUZZ half-slice repeat on the final beat,
        0 leaves the final beat as permuted (default 1).

    Why it works: every slice is A's own audio on A's own beat grid,
    so the floor keeps dancing while the pattern stops making sense —
    a build made of pure expectation violation, resolved by B.
    Distinct from a beat-repeat roll (one fragment tiled forward) and
    a stutter (onset repeats): the whole bar is re-dealt.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = max(8, int(round(bar_s * sr)))
    buf_n = bar_n * int(buffer_bars)
    if len(a) >= buf_n:
        pre, buf = a[:-buf_n], a[-buf_n:].copy()
    else:
        pre = np.zeros(0)
        buf = np.pad(a, (buf_n - len(a), 0))
    perm = _SLICE_PATTERNS[pattern]
    # Slice boundaries tile each bar exactly (last slice absorbs the
    # rounding remainder), so the shuffled region keeps the bar grid.
    bounds = [int(round(i * bar_n / 8.0)) for i in range(9)]
    slice_n = bounds[1] - bounds[0]
    out_buf = np.zeros(buf_n)
    for bar_i in range(int(buffer_bars)):
        base = bar_i * bar_n
        for slot in range(8):
            s_lo = base + bounds[perm[slot]]
            s_hi = base + bounds[perm[slot] + 1]
            seg = _edge_fades(buf[s_lo:s_hi], sr, 1.5)
            d_lo = base + bounds[slot]
            d_hi = base + bounds[slot + 1]
            n = min(len(seg), d_hi - d_lo)
            out_buf[d_lo:d_lo + n] = seg[:n]
    if buzz:
        # BUZZ: the final beat's two slices each repeat their first
        # half — an intra-beat insistence right before the release.
        beat_n = bounds[8] - bounds[6]
        region = out_buf[-beat_n:].copy()
        mid = beat_n // 2
        for lo, hi in ((0, mid), (mid, beat_n)):
            s = region[lo:hi]
            h = max(1, len(s) // 2)
            buzzed = np.concatenate([s[:h], s[:h]])
            if len(buzzed) < len(s):
                buzzed = np.concatenate([buzzed, s[len(buzzed):]])
            region[lo:hi] = buzzed[:len(s)]
        out_buf[-beat_n:] = region
    body = np.concatenate([pre, out_buf]) if len(pre) else out_buf
    return _seam_concat(body, b, sr)


# ----------------------------------------------------------------------------
# WEB-09 — Downlifter Exit (descending sweep seam mask)
# ----------------------------------------------------------------------------

def downlifter_exit(a, b, sr, bar_s, sweep_bars=1.0, f_start=12000.0,
                    f_end=300.0, level_db=-9.0, seed=11):
    """Downlifter exit: a descending filtered-noise sweep spans the
    seam and masks the cut.

    The producer's "downer" — the riser's mirror. Synthesized white
    noise runs through a low-pass whose cutoff falls exponentially
    from `f_start` to `f_end` Hz across `sweep_bars` bars; the sweep
    swells in over the first three quarters (A's final stretch) and
    crashes down through the last quarter (B's first beat), dying as
    B establishes. Underneath it, `a` hands to `b` with a plain 3 ms
    seam guard — a hard join the sweep exists to hide. Where a riser
    builds tension *before* a change and is killed at the seam, the
    downlifter spends tension *across* the seam.

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bar_s : seconds per bar (the sweep grid).
    sweep_bars : sweep length in bars (default 1.0).
    f_start, f_end : cutoff sweep endpoints in Hz (defaults
        12000 -> 300 — full-spectrum crash to a low rumble).
    level_db : sweep peak level (default -9.0 — loud enough to mask,
        under the mix's own peaks).
    seed : noise seed (default 11; renders are deterministic).

    Why it works: the falling sweep is a full-spectrum event with a
    clear trajectory, so the ear tracks *it* through the exact moment
    the tracks change; the seam hides inside the loudest, fastest-
    moving part of the sweep. It also reads as punctuation — "that
    section is over" — which licenses hard changes (tempo, key,
    genre) underneath it.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    out = _seam_concat(a, b, sr)
    g = min(int(3.0 / 1000.0 * sr), len(a), len(b))
    seam = len(a) - g
    total = int(round(sweep_bars * bar_s * sr))
    pre_n = int(round(0.75 * total))
    post_n = total - pre_n
    start = max(0, seam - pre_n)
    length = min(total, len(out) - start)
    if length <= 0:
        return out
    rng = np.random.default_rng(int(seed))
    noise = rng.standard_normal(length)
    u = np.linspace(0.0, 1.0, length)
    cut = float(f_start) * (float(f_end) / float(f_start)) ** u
    swept = dsp.sweep_filter(noise, sr, cut, ftype="lowpass",
                             block=2048)
    env = np.ones(length)
    atk = min(seam - start, length)
    if atk > 1:
        env[:atk] = np.linspace(0.0, 1.0, atk) ** 1.5
    dec0 = atk
    if length > dec0:
        env[dec0:] = np.exp(-3.0 * np.linspace(0.0, 1.0,
                                               length - dec0))
    swept = swept * env
    peak = float(np.max(np.abs(swept))) + 1e-12
    swept *= dsp.db_to_gain(float(level_db)) / peak
    out[start:start + length] += swept
    return out


# ----------------------------------------------------------------------------
# WEB-10 — Shimmer Wash (octave-climbing reverb exit)
# ----------------------------------------------------------------------------

def shimmer_wash(a, b, sr, bar_s, shift_semitones=12.0, swell_bars=4,
                 level_db=-12.0, decay_s=6.0, fade_bars=2.0):
    """Shimmer wash: A's tail pitch-shifted up into a long reverb,
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
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    swell_n = min(len(a), int(round(swell_bars * bar_s * sr)))
    if swell_n <= 0:
        swell_n = len(a)
    src = a[-swell_n:]
    tail_n = min(len(b), int(round(float(decay_s) * sr)))
    shifted = dsp.pitch_shift(src, sr, float(shift_semitones))
    padded = np.pad(shifted, (0, tail_n))
    wet = dsp.schroeder_reverb(padded, sr, wet=1.0,
                               decay=max(2.0, float(decay_s) * 0.7))
    layer = wet[:swell_n + tail_n]
    env = np.ones(len(layer))
    env[:swell_n] = dsp.raised_cosine(swell_n, up=True)
    f = min(int(0.05 * sr), len(layer))
    if f > 1:
        env[-f:] *= dsp.raised_cosine(f, up=False)
    layer = layer * env
    peak = float(np.max(np.abs(layer))) + 1e-12
    layer *= dsp.db_to_gain(float(level_db)) / peak

    out = np.zeros(len(a) + len(b))
    out[:len(a)] += a
    s0 = len(a) - swell_n
    out[s0:s0 + len(layer)] += layer
    fade_n = min(len(b), int(round(fade_bars * bar_s * sr)))
    if fade_n > 0:
        benv = np.ones(len(b))
        benv[:fade_n] = dsp.raised_cosine(fade_n, up=True)
        out[len(a):] += b * benv
    else:
        out[len(a):] += b
    return out


# ----------------------------------------------------------------------------
# WEB-11 — Infinity Filter (endless barber-pole sweep exit)
# ----------------------------------------------------------------------------

def _bp_sweep_bank(x, sr, centers_hz, gains, half_width_oct=0.35,
                   block=1024):
    """Sum of narrow bandpasses whose centers follow centers_hz (n, k),
    each weighted by its per-sample gain envelope gains (n, k).

    Block-wise coefficient updates with state carryover, mirroring
    dsp.sweep_filter's pattern: one 2nd-order bandpass per peak, edges
    at center * 2^(+-half_width_oct). Returns the summed wet signal.
    """
    x = np.asarray(x, dtype=np.float64)
    n = len(x)
    k = centers_hz.shape[1]
    y = np.zeros(n)
    nyq = sr / 2.0
    for j in range(k):
        zj = None
        col = np.zeros(n)
        for start in range(0, n, block):
            stop = min(start + block, n)
            fc = float(np.mean(centers_hz[start:stop, j]))
            fc = min(max(fc, 15.0), nyq * 0.95)
            lo = max(10.0, fc * 2.0 ** (-half_width_oct)) / nyq
            hi = min(nyq * 0.98, fc * 2.0 ** half_width_oct) / nyq
            if hi <= lo:
                continue
            b, a = signal.iirfilter(2, [lo, hi], btype="bandpass",
                                    output="ba")
            if zj is None or len(zj) != max(len(b), len(a)) - 1:
                zj = np.zeros(max(len(b), len(a)) - 1)
            seg, zj = signal.lfilter(b, a, x[start:stop], zi=zj)
            col[start:stop] = seg
        y += col * gains[:, j]
    return y


def infinity_filter(a, b, sr, bar_s, direction=1, cycles=2.0,
                    sweep_bars=4, mix=0.85, fade_bars=0.5):
    """Infinity filter: A's exit through an endlessly sweeping
    resonant peak stack (barber-pole filter); B enters dry.

    Serato's DJ-FX catalog (3.2+) lists an \"Infinity Filter\" among
    its Advanced FX, and Serato's Hex FX page describes the family
    mechanism: \"endless sweeping peaks for evolving, dramatic
    soundscapes\" — a filter sweep that never arrives, the frequency-
    domain sibling of the Shepard tone (the legacy Serato packs named
    the same idea \"Shepard Filter\"; Pestrela decomposes Pioneer's
    Mobius as \"Shepard Tone\"). This renders the transition use with
    the Shepard construction itself: a bank of narrow resonant peaks
    spaced one octave apart, each sweeping exponentially upward
    (direction=-1: downward); a peak's gain follows a Gaussian window
    over log-frequency, so peaks fade in at the bottom of the window
    and out at the top — the ear tracks one peak rising forever while
    A is still, recognizably, A. Across the final `sweep_bars` bars
    the wet stack crossfades in to `mix` while the peaks complete
    `cycles` full wraps; at the seam the filtered A cuts and `b`
    enters dry, faded over `fade_bars`.

    Parameters
    ----------
    a : outgoing segment (mono float64); its final `sweep_bars`
        bars pass through the peak stack.
    b : incoming segment (mono float64), faded in over `fade_bars`
        at the seam.
    sr : sample rate, Hz.
    bar_s : seconds per bar (sets the sweep zone and B's fade).
    direction : +1 sweeps up (default), -1 sweeps down.
    cycles : full octave wraps completed across the zone
        (default 2.0).
    sweep_bars : length of the filtered zone in bars (default 4).
    mix : wet level at full engagement, 0..1 (default 0.85; the
        remaining dry residue keeps A's body in the exit).
    fade_bars : B's entrance fade in bars (default 0.5 — the
        infinity motion, not B, is the event; B arrives promptly).

    Why it works: a one-way filter sweep (T-003) spends its motion
    and arrives — the exit is the arrival. An endless sweep never
    resolves, so A's final bars hang in permanent departure: the
    track is leaving the whole time, and B's dry downbeat is the
    only arrival on offer. Distinct from WEB-05 `shepard_riser`
    (an *added* oscillator layer under an intact A): here A's own
    spectrum is what climbs.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    zone_n = min(len(a), int(round(sweep_bars * bar_s * sr)))
    if zone_n <= 0:
        zone_n = len(a)
    x = a[-zone_n:]
    n = zone_n

    # Shepard geometry: peaks one octave apart across a fixed
    # log-frequency window; sweep phase advances `cycles` wraps.
    f_lo, f_hi = 120.0, 6000.0
    span_oct = np.log2(f_hi / f_lo)
    n_peaks = int(np.ceil(span_oct)) + 1
    t = np.arange(n) / max(n - 1, 1)
    phase = float(direction) * float(cycles) * t  # in octaves
    centers = np.empty((n, n_peaks))
    gains = np.empty((n, n_peaks))
    mid_oct = 0.5 * np.log2(f_lo * f_hi)
    sigma_oct = span_oct / 4.0
    for j in range(n_peaks):
        # Peak j's log-frequency position: drifts with the sweep phase
        # and wraps inside the window (negative phase = descending
        # peaks, wrapping bottom -> top). The Gaussian gain over
        # position is what makes the wrap inaudible.
        pos = np.log2(f_lo) + (j + phase) % span_oct
        centers[:, j] = 2.0 ** pos
        gains[:, j] = np.exp(-0.5 * ((pos - mid_oct) / sigma_oct) ** 2)
    wet = _bp_sweep_bank(x, sr, centers, gains)
    # The Gaussian window keeps the stack's summed energy ~constant as
    # peaks wrap (the illusion's evenness); normalize the wet stack to
    # the dry zone's peak so `mix` means what it says.
    wpeak = float(np.max(np.abs(wet))) + 1e-12
    wet = wet / wpeak * (float(np.max(np.abs(x))) + 1e-12)

    ramp_n = max(1, zone_n // 2)
    menv = np.full(n, float(mix))
    menv[:ramp_n] = float(mix) * dsp.raised_cosine(ramp_n, up=True)
    zone_out = (1.0 - menv) * x + menv * wet
    zone_out = _edge_fades(zone_out, sr)

    out = np.zeros(len(a) + len(b))
    out[:len(a)] += a
    out[len(a) - zone_n:len(a)] = zone_out
    fade_n = min(len(b), int(round(fade_bars * bar_s * sr)))
    if fade_n > 0:
        benv = np.ones(len(b))
        benv[:fade_n] = dsp.raised_cosine(fade_n, up=True)
        out[len(a):] += b * benv
    else:
        out[len(a):] += b
    return out


# ----------------------------------------------------------------------------
# WEB-12 — Pattern Layer Bridge (Pattern Player seam layer)
# ----------------------------------------------------------------------------

def _oneshot_kick(n, sr, f_start, f_end, decay_s):
    """Synthesized kick: sine with exponential pitch drop + amp decay."""
    t = np.arange(n) / sr
    freq = f_end + (f_start - f_end) * np.exp(-t / (decay_s * 0.35))
    phase = 2.0 * np.pi * np.cumsum(freq) / sr
    return np.sin(phase) * np.exp(-t / decay_s)


def _oneshot_noise(n, sr, seed, decay_s, kind, kit):
    """Synthesized snare/hat: seeded noise burst, shaped + decayed."""
    rng = np.random.default_rng(seed)
    t = np.arange(n) / sr
    raw = rng.standard_normal(n)
    nyq = sr / 2.0
    if kind == "snare":
        lo, hi = (1500.0, 7000.0) if kit == "kit909" else (1200.0, 5500.0)
        bb, aa = signal.iirfilter(2, [lo / nyq, hi / nyq],
                                  btype="bandpass", output="ba")
        body = signal.lfilter(bb, aa, raw)
        tone = np.sin(2.0 * np.pi * 190.0 * t) * np.exp(-t / 0.03)
        sig = body * 0.8 + tone * 0.5
    else:  # hat
        fc = 7800.0 if kit == "kit909" else 6800.0
        bb, aa = signal.iirfilter(2, fc / nyq, btype="highpass",
                                  output="ba")
        sig = signal.lfilter(bb, aa, raw)
    return sig * np.exp(-t / decay_s)


_PATTERN_STEPS = {
    # 16-step bars: (kick, snare, hat) step sets. Activity order is
    # the manual's: patterns are "sorted by increasing activity".
    "foundation": ({0, 4, 8, 12}, set(), {2, 6, 10, 14}),
    "groove": ({0, 4, 8, 12}, {4, 12}, {0, 2, 4, 6, 8, 10, 12, 14}),
    "build": ({0, 4, 8, 12}, {4, 12, 15},
              set(range(16))),
    "roll": ({0, 4, 8, 12}, {4, 12}, {0, 2, 4, 6, 8, 10, 12, 14}),
}

_KITS = {
    # Parametric approximations of the two classic kits the manual
    # names (808 / 909): kick pitch envelope + decay, hat brightness.
    "kit808": dict(kick=(105.0, 40.0, 0.42), snare_dec=0.11,
                   hat_dec=0.045),
    "kit909": dict(kick=(122.0, 44.0, 0.27), snare_dec=0.13,
                   hat_dec=0.05),
}


def pattern_layer_bridge(a, b, sr, bpm, bar_s, pattern="groove",
                         kit="kit909", bars=8, level_db=-9.0,
                         duck_db=0.0, duck_release_ms=300.0):
    """Pattern layer bridge: a synthesized drum pattern (Traktor Pro 4
    Pattern Player) carries the seam while the decks hand over.

    Traktor Pro 4's Pattern Player is an FX-unit mode that plays
    rhythmic one-shot patterns (808/909-style kits, 8 samples, patterns
    \"sorted by increasing activity\") in sync with the master clock,
    on top of a deck; its Decay knob doubles as the release of an
    optional ducking envelope that sidechains the deck under the
    pattern (manual, Pattern Player controls). NI's own transition
    recipe: start the pattern during A's breakdown, raise the pattern
    activity to build, drop B in, swap the bass under the pattern,
    fade A out, then dial the pattern back. This renders that arc:
    across the seam zone (the last `bars`/2 bars of `a` + the first
    `bars`/2 bars of `b`) a synthesized pattern plays at the pair's
    tempo; `a` exits with a one-beat fade into the seam (the pattern
    masks it), `b` fades in across its zone half and is established
    as the pattern stops. With `duck_db` > 0 both decks dip on every
    kick step — fast attack, `duck_release_ms` release (the manual's
    200–500 ms duck-release range).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bpm : tempo of the pair (the pattern's clock).
    bar_s : seconds per bar.
    pattern : named density — \"foundation\" (kick + offbeat hats),
        \"groove\" (+ backbeat snare, 8th hats), \"build\" (+ 16th
        hats, extra snare), \"roll\" (groove + a final-bar snare
        roll into the seam's B side establishment).
    kit : \"kit808\" / \"kit909\" — parametric one-shot voices.
    bars : total seam-zone length in bars (default 8).
    level_db : pattern bus peak level (default -9.0).
    duck_db : deck ducking depth on kick steps (default 0.0 = off).
    duck_release_ms : duck release (default 300 ms; manual range
        200–500).

    Why it works: the seam's hardest moment is two records trading
    rhythmic authority. A third, neutral rhythm — owned by neither
    track, locked to the shared grid — holds the floor's pulse
    constant while the records swap underneath it, so neither A's
    exit nor B's entrance has to carry the groove alone. Distinct
    from T-022 `drum_bridge` (which strips to *A's own* drums) and
    T-020 `three_deck_layer` (a third *track* as glue): the glue
    here is synthesized, keyless, and identical under both tracks.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    total = len(a) + len(b)
    beat_s = 60.0 / float(bpm)
    step_s = beat_s / 4.0
    half_bars = max(1, int(bars) // 2)
    zone_a_n = min(len(a), int(round(half_bars * bar_s * sr)))
    zone_b_n = min(len(b), int(round(half_bars * bar_s * sr)))
    zone_start = len(a) - zone_a_n
    zone_end = len(a) + zone_b_n
    zone_n = zone_end - zone_start

    kitp = _KITS.get(kit, _KITS["kit909"])
    kicks, snares, hats = _PATTERN_STEPS.get(pattern,
                                             _PATTERN_STEPS["groove"])
    pat = np.zeros(zone_n)
    kick_steps = []
    n_steps = int(np.ceil(zone_n / (step_s * sr)))
    zone_bars = zone_n / (bar_s * sr)
    for s in range(n_steps):
        at = int(round(s * step_s * sr))
        if at >= zone_n:
            break
        step_in_bar = s % 16
        bar_idx = s // 16
        # Activity arc: later bars hit slightly harder (NI: raise
        # pattern activity into the drop, dial back after) — velocity
        # only; the step sets themselves are the named patterns.
        vel = 0.85 + 0.15 * (bar_idx / max(zone_bars - 1.0, 1.0))
        if step_in_bar in kicks:
            g = _oneshot_kick(int(0.6 * sr), sr, *kitp["kick"])
            m = min(len(g), zone_n - at)
            pat[at:at + m] += vel * g[:m]
            kick_steps.append(at)
        is_roll_bar = (pattern == "roll"
                       and bar_idx == int(zone_bars) - 1
                       and at >= zone_a_n)
        if step_in_bar in snares or is_roll_bar:
            g = _oneshot_noise(int(0.3 * sr), sr, 1000 + s,
                               kitp["snare_dec"], "snare", kit)
            m = min(len(g), zone_n - at)
            pat[at:at + m] += vel * 0.8 * g[:m]
        if step_in_bar in hats:
            g = _oneshot_noise(int(0.12 * sr), sr, 5000 + s,
                               kitp["hat_dec"], "hat", kit)
            m = min(len(g), zone_n - at)
            pat[at:at + m] += vel * 0.45 * g[:m]
    ppeak = float(np.max(np.abs(pat))) + 1e-12
    pat = pat / ppeak * dsp.db_to_gain(float(level_db))

    # Track gains on the concatenated timeline.
    ga = np.ones(total)
    fade_a_n = min(zone_a_n, int(round(beat_s * sr)))
    if fade_a_n > 1:
        ga[len(a) - fade_a_n:len(a)] = dsp.raised_cosine(fade_a_n,
                                                         up=False)
    ga[len(a):] = 0.0
    gb = np.zeros(total)
    if zone_b_n > 1:
        gb[len(a):zone_end] = dsp.raised_cosine(zone_b_n, up=True)
    gb[zone_end:] = 1.0

    mix_ab = ga * np.concatenate([a, np.zeros(len(b))]) \
        + gb * np.concatenate([np.zeros(len(a)), b])

    # Optional ducking: decks dip under each kick step (the pattern
    # itself is the sidechain source and is not ducked).
    if duck_db > 0 and kick_steps:
        env = np.ones(zone_n)
        dip = dsp.db_to_gain(-float(duck_db))
        atk = max(1, int(0.005 * sr))
        rel = max(1, int(float(duck_release_ms) / 1000.0 * sr))
        for at in kick_steps:
            e = min(at + atk, zone_n)
            env[at:e] = np.linspace(1.0, dip, e - at)
            r = min(at + atk + rel, zone_n)
            if r > e:
                env[e:r] = np.minimum(env[e:r],
                                      np.linspace(dip, 1.0, r - e))
        mix_ab[zone_start:zone_end] *= env

    out = mix_ab
    out[zone_start:zone_end] += pat
    return _edge_fades(out, sr)


# ----------------------------------------------------------------------------
# WEB-13 — Pumper Exit (beat-synced duck pump exit)
# ----------------------------------------------------------------------------

def pumper_exit(a, b, sr, bpm, bar_s, duck_db=-10.0, offset_beats=-0.25,
                rate_beats=1.0, pump_bars=4):
    """Pumper exit: A's final bars duck on the downbeat grid, deepening
    cycle by cycle; the last recovery is withheld and B fills the hole.

    Denon's X1850 PRIME BPM FX list includes Pumper — "this effect
    attenuates or 'ducks' audio on the downbeat, similar to a sidechain
    compressor" — with two parameters: Duck (attenuation, -2 to -20 dB)
    and Offset (the ducking offset in beats: -1/16, -1/8, -1/4, -1/2,
    always anticipatory, so the dip is already open when the downbeat
    lands); the module's FX Time division sets the duck rate. This
    renders the transition use: across A's final `pump_bars` bars a
    duck cycle of `rate_beats` beats repeats, its depth ramping from
    1/n to the full `duck_db` (the manual's Duck range); each dip
    attacks over 15% of the cycle and recovers across its back half.
    The final cycle never recovers — A fades out inside the duck over
    its last beat — and `b` enters dry at full level at the seam, in
    the hole the withheld recovery leaves. rekordbox's Release FX
    DUCKING pad is the same mechanism in exit form (second vendor).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bpm : tempo of the pair (the duck grid).
    bar_s : seconds per bar (sizes the pump zone).
    duck_db : full duck depth at the final cycle, -2..-20 dB (the
        manual's Duck parameter; default -10).
    offset_beats : dip start relative to the beat, in beats — the
        manual's Offset set is -1/16..-1/2; 0.0 is on-grid
        (default -0.25).
    rate_beats : duck cycle length in beats (the FX Time division;
        default 1.0).
    pump_bars : length of the deepening zone in bars (default 4).

    Why it works: the pump pre-carves rhythmic holes in A's final
    bars, so the ear leans into the gaps and B — arriving dry in the
    last, unrecovered hole — reads as the drop the pumping promised.
    Distinct from T-035 `riser_ducking_overlay` (ducking in service
    of an added riser layer): nothing is added here; the ducking
    itself is the exit. Distinct from the gate family: the dips are
    shallow-to-moderate, rounded, and recover between beats —
    sidechain breathing, not chopping.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / float(bpm)
    beat_n = max(64, int(round(beat_s * sr)))
    zone_n = min(len(a), int(round(pump_bars * bar_s * sr)))
    zone_start = len(a) - zone_n
    cycle_n = max(64, int(round(rate_beats * beat_s * sr)))
    n_cycles = max(1, int(np.ceil(zone_n / float(cycle_n))))
    off_n = int(round(offset_beats * beat_s * sr))
    atk_n = max(1, int(0.15 * cycle_n))
    rel_start = int(0.45 * cycle_n)
    gain = np.ones(len(a))
    for k in range(n_cycles):
        depth = abs(float(duck_db)) * (k + 1) / n_cycles
        floor_g = dsp.db_to_gain(-depth)
        c0 = zone_start + k * cycle_n + off_n
        last = (k == n_cycles - 1)
        prof_n = cycle_n if not last else len(a) - c0
        if prof_n <= 0:
            continue
        prof = np.ones(prof_n)
        atk = min(atk_n, prof_n)
        prof[:atk] = floor_g + (1.0 - floor_g) \
            * dsp.raised_cosine(atk, up=False)
        if last:
            prof[atk:] = floor_g
        else:
            hold_end = min(max(rel_start, atk), prof_n)
            prof[atk:hold_end] = floor_g
            rel_n = prof_n - hold_end
            if rel_n > 1:
                prof[hold_end:] = floor_g + (1.0 - floor_g) \
                    * dsp.raised_cosine(rel_n, up=True)
        lo = max(c0, 0)
        hi = min(c0 + prof_n, len(a))
        if hi > lo:
            gain[lo:hi] = np.minimum(gain[lo:hi],
                                     prof[lo - c0:hi - c0])
    # The exit fade: A's final beat falls away inside the last duck.
    fade_n = min(len(a), beat_n)
    if fade_n > 1:
        gain[-fade_n:] *= dsp.raised_cosine(fade_n, up=False)
    out = np.concatenate([a * gain, b])
    return _edge_fades(out, sr)


# ----------------------------------------------------------------------------
# WEB-14 — Scale Down Exit (beat-stepped pitch descent)
# ----------------------------------------------------------------------------

_SCALE_DOWN_INTERVALS = {
    "chromatic": [1],
    "major": [2, 2, 1, 2, 2, 2, 1],
    "minor": [2, 1, 2, 2, 1, 2, 2],
    "major_pent": [2, 2, 3, 2, 3],
    "minor_pent": [3, 2, 2, 3, 2],
}


def _scale_descent(scale, steps):
    """Cumulative semitone descent after each of `steps` steps,
    walking the scale's interval pattern (cycling octaves)."""
    ivs = _SCALE_DOWN_INTERVALS.get(scale,
                                    _SCALE_DOWN_INTERVALS["major"])
    cum, total = [], 0
    for k in range(int(steps)):
        total += ivs[k % len(ivs)]
        cum.append(total)
    return cum


def scale_down_exit(a, b, sr, bpm, bar_s, scale="major", steps=4,
                    capture_beats=1.0, step_beats=1.0, fade_bars=2.0):
    """Scale down exit: A's captured final beat replays once per beat
    across B's entrance, each replay pitched one scale step lower.

    Engine DJ 3.1's Main FX include a matched pair, in Engine's own
    release copy: Pitch Down — "an effect which chromatically
    pitches down the captured audio in time with the beat"; Scale
    Down — "similar to Pitch Down, using four different scales to
    add color to a transition." The mechanism: audio is captured,
    then replayed in beat slots, each replay one step lower —
    chromatically for Pitch Down, along a scale for Scale Down.
    This renders it as the exit: `a` plays dry to its end; its final
    `capture_beats` fragment is replayed `steps` times at
    `step_beats` spacing across `b`'s entrance, replay k pitched
    down by the cumulative scale descent (phase-vocoder shift, so
    each replay stays on the beat grid), decaying x0.85 per step;
    `b` fades up underneath over `fade_bars`. Engine names "four
    different scales" without enumerating them — the render adopts
    the standard four (major, natural minor, major pentatonic,
    minor pentatonic) and carries chromatic as the Pitch Down axis
    of the same base (disclosed in the bank entry, WEB-14).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bpm : tempo of the pair (the step grid).
    bar_s : seconds per bar (sets B's fade).
    scale : "major" / "minor" / "major_pent" / "minor_pent" (Scale
        Down's four) or "chromatic" (Pitch Down's axis).
    steps : number of descending replays (default 4).
    capture_beats : length of the captured fragment (default 1.0).
    step_beats : spacing between replays (default 1.0).
    fade_bars : B's entrance fade in bars (default 2.0).

    Why it works: a pitch descent in discrete, beat-locked,
    scale-quantized steps reads as deliberate — A walks downstairs
    and out, each step landing on a beat and a scale tone, instead
    of falling apart (T-013's continuous dive) or evaporating
    upward (WEB-01's climbing tail). Every replay leaves A's pitch
    center further behind, so B's tonal space is never contested,
    and the scale quantization keeps the descent musical against
    B's entrance where a chromatic slide would smear.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    beat_s = 60.0 / float(bpm)
    cap_n = max(256, int(round(capture_beats * beat_s * sr)))
    step_n = max(256, int(round(step_beats * beat_s * sr)))
    if len(a) >= cap_n:
        seg = a[-cap_n:]
    else:
        seg = np.pad(a, (cap_n - len(a), 0))
    cum = _scale_descent(scale, steps)
    tail = np.zeros(step_n * int(steps))
    edge = max(1, int(0.010 * sr))
    for k in range(int(steps)):
        rep = dsp.pitch_shift(seg, sr, -float(cum[k]))
        if len(rep) >= cap_n:
            rep = rep[:cap_n]
        else:
            rep = np.pad(rep, (0, cap_n - len(rep)))
        w = np.ones(len(rep))
        e = min(edge, len(rep) // 2)
        if e > 1:
            w[:e] = dsp.raised_cosine(e, up=True)
            w[-e:] = dsp.raised_cosine(e, up=False)
        at = k * step_n
        m = min(len(rep), len(tail) - at)
        if m > 0:
            tail[at:at + m] += rep[:m] * w[:m] * (0.85 ** (k + 1))
    # The final replay decays instead of truncating mid-step.
    f = min(step_n, len(tail))
    if f > 1:
        tail[-f:] *= dsp.raised_cosine(f, up=False)
    out = np.zeros(len(a) + len(b))
    out[:len(a)] += a
    out[len(a):len(a) + len(tail)] += tail
    fade_n = min(len(b), int(round(fade_bars * bar_s * sr)))
    if fade_n > 0:
        env = np.ones(len(b))
        env[:fade_n] = dsp.raised_cosine(fade_n, up=True)
        out[len(a):] += b * env
    else:
        out[len(a):] += b
    return out


# ----------------------------------------------------------------------------
# WEB-15 — Fader Synth (source-replacing fader oscillator)
# ----------------------------------------------------------------------------

_FADER_SYNTH_SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "minor_h": [0, 2, 3, 5, 7, 8, 11],
    "japanese": [0, 1, 5, 7, 10],
}


def _fader_osc(waveform, phase):
    """The S11's three oscillator shapes at the given phase track
    (cycles). Naive saw/square (aliasing) — the hardware's
    band-limited voice differs in sheen, not in gesture."""
    if waveform == "sine":
        return np.sin(2.0 * np.pi * phase)
    frac = phase - np.floor(phase)
    if waveform == "square":
        return np.where(frac < 0.5, 1.0, -1.0)
    return 2.0 * frac - 1.0


def fader_synth(a, b, sr, bar_s, waveform="saw", ride="steps",
                scale="major", root_hz=110.0, base_octave=0,
                zone_bars=4, level_db=-6.0):
    """Fader synth: A's channel is replaced by an oscillator line
    whose pitch follows a scripted fader ride across the seam.

    The DJM-S11's Beat FX table (p.61) lists FADER SYNTH
    (SINE/SAW/SQUARE): "outputs the synth sound as the audio source
    of the base oscillation frequency" — the input sound is
    replaced by an oscillator and the channel fader becomes its
    pitch control (the manual's footnote: with the effect on, the
    fader no longer adjusts volume). The BEAT buttons set the base
    oscillation frequency level (-3 to +3); LEVEL/DEPTH is the
    effect volume; the sub parameter quantizes the fader's pitch
    travel to a scale (AUTO SCALE, MAJOR, MINOR, MINOR H,
    JAPANESE, ...). This renders a transition ride: across the seam
    zone (the last `zone_bars`/2 bars of `a` + the first
    `zone_bars`/2 bars of `b`), `a` fades out inside the zone's
    first beat — the fader pull — and a synthesized line plays the
    ride: "steps" (one scale degree per beat, climbing through
    octaves), "glide" (a continuous one-octave glide), "arp" (a
    0-2-4-2 degree pattern per beat), or "hold" (parked at the
    octave). `b` fades in across its zone half and is established
    as the synth cuts at the zone's end.

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bar_s : seconds per bar (sizes the zone and the beat grid).
    waveform : "sine" / "saw" / "square" — the manual's three.
    ride : "steps" / "glide" / "arp" / "hold" — the fader path.
    scale : "major" / "minor" / "minor_h" / "japanese" — the
        manual's sub-parameter set, render subset.
    root_hz : the line's root frequency (default 110.0 = A2).
    base_octave : the manual's base-frequency level, -3..+3
        octaves applied to the root (default 0).
    zone_bars : seam-zone length in bars (default 4).
    level_db : synth line level (default -6.0).

    Why it works: every other exit treats A's audio; this one
    substitutes for it. The moment the record becomes a synth
    tone, the pair's key/tempo negotiation ends — the line owes
    A's harmony nothing beyond its starting root, and its
    scale-quantized climb is pure directed energy that B inherits
    at the seam. Distinct from DM-A15 `cdj_synth_lead` (a loop
    grab of A's own audio resynthesized — the source is still A)
    and from T-032 `pitch_play` (the input sound, pitched): this
    oscillator never contained the record at all.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    total = len(a) + len(b)
    beat_n = max(64, int(round(bar_s * sr / 4.0)))
    half = max(1, int(zone_bars) // 2)
    zone_a_n = min(len(a), int(round(half * bar_s * sr)))
    zone_b_n = min(len(b), int(round(half * bar_s * sr)))
    zone_start = len(a) - zone_a_n
    zone_end = len(a) + zone_b_n
    zone_n = zone_end - zone_start
    root = float(root_hz) * (2.0 ** int(base_octave))
    scale_iv = _FADER_SYNTH_SCALES.get(scale,
                                       _FADER_SYNTH_SCALES["major"])

    def deg_freq(d):
        L = len(scale_iv)
        return root * (2.0 ** ((scale_iv[d % L] + 12 * (d // L))
                               / 12.0))

    n_beats = max(1, int(round(zone_n / float(beat_n))))
    line = np.zeros(zone_n)
    if ride == "glide":
        t = np.arange(zone_n)
        freq = root * (2.0 ** (t / max(zone_n - 1, 1)))
        line = _fader_osc(waveform, np.cumsum(freq) / sr)
    else:
        if ride == "arp":
            pat = [0, 2, 4, 2]
            beat_freqs = [deg_freq(pat[i % len(pat)])
                          for i in range(n_beats)]
        elif ride == "hold":
            beat_freqs = [root * 2.0] * n_beats
        else:  # steps
            beat_freqs = [deg_freq(i) for i in range(n_beats)]
        for i, f in enumerate(beat_freqs):
            s0 = i * beat_n
            s1 = min(zone_n, s0 + beat_n)
            if s1 <= s0:
                break
            n = s1 - s0
            seg = _fader_osc(waveform, f * np.arange(n) / sr)
            e = min(int(0.008 * sr), n // 2)
            if e > 1:
                seg = seg.copy()
                seg[:e] *= dsp.raised_cosine(e, up=True)
                seg[-e:] *= dsp.raised_cosine(e, up=False)
            line[s0:s1] += seg
    line = line * dsp.db_to_gain(float(level_db))
    atk = min(int(0.025 * sr), max(zone_n // 4, 1))
    if atk > 1 and zone_n > 2 * atk:
        line[:atk] *= dsp.raised_cosine(atk, up=True)
        line[-atk:] *= dsp.raised_cosine(atk, up=False)

    ga = np.ones(total)
    fade_a = min(zone_a_n, beat_n)
    if fade_a > 1:
        ga[zone_start:zone_start + fade_a] = dsp.raised_cosine(
            fade_a, up=False)
    ga[zone_start + fade_a:] = 0.0
    gb = np.zeros(total)
    if zone_b_n > 1:
        gb[len(a):zone_end] = dsp.raised_cosine(zone_b_n, up=True)
    gb[zone_end:] = 1.0
    out = ga * np.concatenate([a, np.zeros(len(b))]) \
        + gb * np.concatenate([np.zeros(len(a)), b])
    out[zone_start:zone_end] += line
    return _edge_fades(out, sr)


# ----------------------------------------------------------------------------
# WEB-16 — Ring Mod Dissolve (carrier-multiplication exit)
# ----------------------------------------------------------------------------

def ring_mod_dissolve(a, b, sr, bar_s, carrier_start_hz=100.0,
                      carrier_end_hz=2800.0, morph=1.0, raw="sine",
                      zone_bars=4, fade_bars=0.5):
    """Ring mod dissolve: A's final bars are multiplied by a rising
    carrier until the track dissolves into inharmonic sidebands;
    B enters dry.

    Traktor's manual (§14.4.25) documents the Ring Modulator as a
    standalone effect: it "modulates the tracks by multiplying the
    high frequency signal onto the audio material" — the input is
    multiplied by an oscillator whose PITCH runs 100 Hz to
    8371 Hz, with an AM-RM control morphing between amplitude
    modulation (soft, the dry signal survives inside the product)
    and full ring modulation (the dry signal is gone; only
    sidebands at f +/- fc remain), and a RAW switch changing the
    carrier from a sine to a filtered square. Rendered as a
    transition: across A's final `zone_bars` bars the mix ramps
    from dry A to the fully modulated signal while the carrier
    sweeps logarithmically from `carrier_start_hz` to
    `carrier_end_hz`. As the carrier climbs through the audio
    band, A's partials smear into inharmonic sideband pairs and
    the track's pitch identity dissolves into metallic shimmer;
    at the seam the shimmer cuts and `b` enters dry, faded over
    `fade_bars`.

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bar_s : seconds per bar (sizes the zone and B's fade).
    carrier_start_hz : carrier frequency at the zone's start
        (default 100.0 — the manual's range floor).
    carrier_end_hz : carrier frequency at the zone's end
        (default 2800.0; the manual's ceiling is 8371.0).
    morph : AM <-> RM morph, 0..1 (default 1.0 = full ring
        modulation; 0.0 = pure amplitude modulation).
    raw : "sine" carrier (default) or "square" — the manual's
        RAW filtered-square carrier, rendered as a soft-clipped
        sine (odd harmonics, rolled-off top).
    zone_bars : dissolve zone length in bars (default 4).
    fade_bars : B's entrance fade in bars (default 0.5).

    Why it works: multiplication is the one basic operation the
    rest of the registry never performs — filters subtract
    (T-003), quantization coarsens (WEB-04 crush_degrade), combs
    interfere (WEB-02 flanger_sweep). A ring modulator *adds new
    partials* at sum-and-difference frequencies, so the exit is
    not A getting quieter or duller but A becoming a different
    spectrum altogether: recognizability drains as the carrier
    rises, which is exactly the perceptual job of an exit, and
    because the sidebands are inharmonic the move owes the pair
    no key negotiation at all.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    zone_n = min(len(a), int(round(zone_bars * bar_s * sr)))
    if zone_n <= 0:
        zone_n = len(a)
    x = a[-zone_n:]
    n = zone_n
    t = np.arange(n, dtype=np.float64)
    f0 = max(20.0, float(carrier_start_hz))
    f1 = max(f0, float(carrier_end_hz))
    freq = f0 * (f1 / f0) ** (t / max(n - 1, 1))
    carrier = np.cos(2.0 * np.pi * np.cumsum(freq) / sr)
    if raw == "square":
        carrier = np.tanh(2.5 * carrier)
        carrier = carrier / (float(np.max(np.abs(carrier))) + 1e-12)
    m = min(max(float(morph), 0.0), 1.0)
    mod = (1.0 - m) * (0.5 + 0.5 * carrier) + m * carrier
    wet = x * mod
    wpeak = float(np.max(np.abs(wet))) + 1e-12
    wet = wet / wpeak * (float(np.max(np.abs(x))) + 1e-12)

    ramp_n = max(1, int(0.75 * n))
    menv = np.ones(n)
    menv[:ramp_n] = dsp.raised_cosine(ramp_n, up=True)
    zone_out = (1.0 - menv) * x + menv * wet
    zone_out = _edge_fades(zone_out, sr)

    out = np.zeros(len(a) + len(b))
    out[:len(a)] += a
    out[len(a) - zone_n:len(a)] = zone_out
    fade_n = min(len(b), int(round(fade_bars * bar_s * sr)))
    if fade_n > 0:
        benv = np.ones(len(b))
        benv[:fade_n] = dsp.raised_cosine(fade_n, up=True)
        out[len(a):] += b * benv
    else:
        out[len(a):] += b
    return out


# ----------------------------------------------------------------------------
# WEB-17 — Formant Morph Exit (vowel-series spectral morph)
# ----------------------------------------------------------------------------

# Classic adult-male formant targets (Peterson & Barney-style
# published averages), F1/F2/F3 in Hz. The manual's TYP button
# switches German/English vowel character; German vowels are
# tenser / more peripheral, rendered here as a small systematic
# shift of the same table (an approximation — NI publishes no
# formant numbers).
_FORMANT_TABLES = {
    "english": {
        "a": (730.0, 1090.0, 2440.0),
        "e": (530.0, 1840.0, 2480.0),
        "i": (270.0, 2290.0, 3010.0),
        "o": (570.0, 840.0, 2410.0),
        "u": (300.0, 870.0, 2240.0),
    },
    "german": {
        "a": (700.0, 1060.0, 2400.0),
        "e": (490.0, 1920.0, 2520.0),
        "i": (250.0, 2380.0, 3060.0),
        "o": (540.0, 820.0, 2380.0),
        "u": (280.0, 840.0, 2180.0),
    },
}
_FORMANT_GAINS = (1.0, 0.55, 0.30)


def formant_morph_exit(a, b, sr, bar_s, path="aeiou",
                       table="english", sharp=1.0, zone_bars=4,
                       mix=0.9, fade_bars=0.5):
    """Formant morph exit: A's final bars morph through a series
    of vowel formants — the track "talks" its way out; B enters
    dry.

    Traktor's manual (§14.4.30) documents the Formant Filter: it
    "imitates the sound of spoken vowels by morphing three
    bandpass filters into each other." The TALK control morphs
    through the formants produced from the mouth (a, e, i, o, u)
    — dark at the left, brighter to the right; SHARP makes the
    vowel sound more present; the TYP button switches German /
    English vowel character. Rendered as a transition: across
    A's final `zone_bars` bars the wet signal crossfades in to
    `mix` while the three formant peaks travel — in log
    frequency, at even keyframe spacing — through the vowel
    series named by `path`, each vowel defined by its
    (F1, F2, F3) targets in `table`. At the seam the last vowel
    cuts and `b` enters dry, faded over `fade_bars`.

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bar_s : seconds per bar (sizes the zone and B's fade).
    path : the vowel series to morph through, as a string of
        vowel letters (default "aeiou" — the manual's TALK
        order; "ouiea" runs it backwards).
    table : "english" (default) or "german" — the manual's TYP
        switch; the German table is a systematic shift of the
        English one (tenser vowels), a render approximation.
    sharp : the manual's SHARP — formant presence, 0.5..2.0
        (default 1.0); higher = narrower, more resonant peaks.
    zone_bars : morph zone length in bars (default 4).
    mix : wet level at full engagement, 0..1 (default 0.9; the
        dry residue keeps a whisper of A's body under the
        vowels).
    fade_bars : B's entrance fade in bars (default 0.5).

    Why it works: a filter sweep (T-003) translates one peak
    across the spectrum and a peak stack (WEB-11
    infinity_filter) translates many together — the spectral
    *shape* never changes, only its address. A formant morph
    moves the peaks to vowel-specific relative configurations
    and interpolates between shapes, so A keeps its rhythm and
    rough spectrum while its timbre cycles through the most
    recognisable shapes a listener knows: speech vowels. The
    track appears to pronounce its own exit — a lateral,
    characterful departure that needs no key or tempo
    negotiation, and on a vocal A the effect doubles: the
    singer's vowels are re-articulated by the morph itself.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    zone_n = min(len(a), int(round(zone_bars * bar_s * sr)))
    if zone_n <= 0:
        zone_n = len(a)
    x = a[-zone_n:]
    n = zone_n
    tbl = _FORMANT_TABLES.get(table, _FORMANT_TABLES["english"])
    vowels = [c for c in str(path).lower() if c in tbl]
    if not vowels:
        vowels = ["a", "e", "i", "o", "u"]
    if len(vowels) == 1:
        vowels = vowels * 2
    k = len(vowels)
    key_pos = np.linspace(0.0, n - 1, k)
    t = np.arange(n, dtype=np.float64)
    centers = np.empty((n, 3))
    gains = np.empty((n, 3))
    for j in range(3):
        lf = np.log2([tbl[v][j] for v in vowels])
        centers[:, j] = 2.0 ** np.interp(t, key_pos, lf)
        gains[:, j] = _FORMANT_GAINS[j]
    hw = float(np.clip(0.32 / max(float(sharp), 0.05), 0.08, 0.8))
    wet = _bp_sweep_bank(x, sr, centers, gains, half_width_oct=hw)
    wpeak = float(np.max(np.abs(wet))) + 1e-12
    wet = wet / wpeak * (float(np.max(np.abs(x))) + 1e-12)

    ramp_n = max(1, n // 2)
    menv = np.full(n, float(mix))
    menv[:ramp_n] = float(mix) * dsp.raised_cosine(ramp_n, up=True)
    zone_out = (1.0 - menv) * x + menv * wet
    zone_out = _edge_fades(zone_out, sr)

    out = np.zeros(len(a) + len(b))
    out[:len(a)] += a
    out[len(a) - zone_n:len(a)] = zone_out
    fade_n = min(len(b), int(round(fade_bars * bar_s * sr)))
    if fade_n > 0:
        benv = np.ones(len(b))
        benv[:fade_n] = dsp.raised_cosine(fade_n, up=True)
        out[len(a):] += b * benv
    else:
        out[len(a):] += b
    return out


def resonator_tail(a, b, sr, bar_s, root_midi=45, chord="major",
                   decay_s=2.5, color=0.5, zone_bars=2,
                   ring_level=0.85, fade_bars=1.0):
    """Resonator tail: A's final bars ring away through a tuned
    resonator bank while B enters under the ring.

    Ableton's Resonators device (Live 12 manual, Live Audio
    Effect Reference) runs the input through "five parallel
    resonators that add a tonal character to the input signal
    and can be tuned in semitones or scale degrees," producing
    "results ranging from plucked-string timbres to
    vocoder-like tones." Resonator I sets the root (its Note
    parameter); II–V are tuned relative to it in musical
    intervals, each transposable ±24 semitones. The Decay
    parameter sets "the amount of time it takes for the
    resonators to be silent after getting an input signal...
    similar to the behavior of an undamped piano string," and
    — as with a real string — the decay time depends on the
    pitch, low notes lasting longer than higher ones; Color
    sets the brightness. Rendered as a transition: A's final
    `zone_bars` bars excite a five-comb resonator bank tuned
    to the `chord` voicing on `root_midi`; across the zone the
    dry signal crossfades into the ring, so by the seam A is
    present only as its own resonance, pitched to the chord.
    The ring decays naturally (pitch-dependent, per the
    manual) across B's entrance while `b` fades in under it
    over `fade_bars`. Output is len(a) + len(b).

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64).
    sr : sample rate, Hz.
    bar_s : seconds per bar (sizes the zone and B's fade).
    root_midi : Resonator I's Note as a MIDI number (default
        45 = A2, 110 Hz). Selection passes B's tonic: the
        ring is tuned to the *incoming* chord, so A's energy
        arrives already speaking B's harmony.
    chord : the II–V interval voicing above the root —
        "major" (0, +4, +7, +12, +19), "minor"
        (0, +3, +7, +12, +19), "power" (0, +7, +12, +19,
        +24), "octave" (0, +12, +24).
    decay_s : the manual's Decay — seconds for the root
        resonator to fall to silence (−60 dB); higher
        resonators decay faster, scaled by (f_root/f)^0.5,
        the manual's pitch dependence.
    color : the manual's Color, 0..1 (default 0.5) —
        brightness, rendered as the damping lowpass inside
        each comb's feedback path.
    zone_bars : excitation zone length in bars (default 2).
    ring_level : ring level relative to A's peak, 0..1
        (default 0.85).
    fade_bars : B's entrance fade in bars (default 1.0).

    Why it works: every other tail in the library carries
    A's *pitch content* forward — an echo repeats it, a
    reverb diffuses it, a shimmer transposes it by a fixed
    interval. A resonator bank replaces it: the tail keeps
    A's rhythm and energy contour but its pitch content is
    the bank's tuning, chosen here as B's chord. The seam
    therefore has no key negotiation at all — what crosses
    it is A's gesture re-pitched into B's harmony, decaying
    like strings while B establishes itself underneath.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    zone_n = min(len(a), int(round(zone_bars * bar_s * sr)))
    if zone_n <= 0:
        zone_n = len(a)
    x = a[-zone_n:]
    total = zone_n + len(b)
    intervals = _RESONATOR_CHORDS.get(
        str(chord).lower(), _RESONATOR_CHORDS["major"])
    f_root = 440.0 * 2.0 ** ((float(root_midi) - 69.0) / 12.0)
    damp = 0.05 + 0.65 * (1.0 - float(np.clip(color, 0.0, 1.0)))
    excite = np.zeros(total)
    excite[:zone_n] = x
    ring = np.zeros(total)
    for iv in intervals:
        f = f_root * 2.0 ** (iv / 12.0)
        d = max(2, int(round(sr / f)))
        t60 = float(decay_s) * (f_root / f) ** 0.5
        t60 = max(0.15, t60)
        g = 0.001 ** (d / (t60 * sr))
        acoef = np.zeros(d + 2)
        acoef[0] = 1.0
        acoef[d] = -g * (1.0 - damp)
        acoef[d + 1] = -g * damp
        ring += signal.lfilter([1.0], acoef, excite)
    rpeak = float(np.max(np.abs(ring))) + 1e-12
    ring = ring / rpeak * (float(np.max(np.abs(x))) + 1e-12)
    ring *= float(ring_level)

    w = dsp.raised_cosine(zone_n, up=True)
    zone_out = (1.0 - w) * x + w * ring[:zone_n]
    zone_out = _edge_fades(zone_out, sr)

    out = np.zeros(len(a) + len(b))
    out[:len(a)] += a
    out[len(a) - zone_n:len(a)] = zone_out
    fade_n = min(len(b), int(round(fade_bars * bar_s * sr)))
    benv = np.ones(len(b))
    if fade_n > 0:
        benv[:fade_n] = dsp.raised_cosine(fade_n, up=True)
    out[len(a):] += b * benv + ring[zone_n:]
    return out


_RESONATOR_CHORDS = {
    "major": (0, 4, 7, 12, 19),
    "minor": (0, 3, 7, 12, 19),
    "power": (0, 7, 12, 19, 24),
    "octave": (0, 12, 24),
}


# ----------------------------------------------------------------------------
# WEB-19 — Continuous drop (Phase 23, genre traditions tranche A: DnB)
# ----------------------------------------------------------------------------

def continuous_drop(a, b, sr, bar_s, stage_bars=8, stage_from_db=-14.0,
                    stage_to_db=-6.0):
    """Continuous drop: A's drop plays out while B is staged beneath
    its final bars; B's drop lands on the exact downbeat A's ends.

    The lead pattern of a working DnB DJ's own transition taxonomy
    (kohadachan, note.com, "A Personal Drum and Bass DJ how to",
    fetched 2026-10-22): "Continuous Drop — the end of the previous
    track's drop -> the start of the next track's drop (start from 8
    bars before the previous track drop's end)". There is no
    breakdown, no valley, no breath between the drops: A's drop is
    the transition surface. Across its final `stage_bars` bars,
    B's first bar is looped underneath with its lows killed,
    rising from `stage_from_db` to `stage_to_db` against the
    window's own peak, so the crowd registers B's rhythm arriving
    inside A's drop before it owns anything. At A's final sample
    B starts — at its drop, at full level.

    Parameters
    ----------
    a, b : outgoing / incoming segments (mono float64). `a` ENDS
        at its drop's end (caller aligns); `b` STARTS at its drop,
        and its first bar doubles as the staging cell.
    sr : sample rate, Hz.
    bar_s : seconds per bar (sizes the staging window).
    stage_bars : staging window in bars (default 8 — the source's
        number; 4 = late staging for short drops, 16 = the long
        liquid form).
    stage_from_db / stage_to_db : the staged cell's gain ramp
        against the window peak of `a` (defaults −14 -> −6 dB:
        felt as pressure before it is heard as a track).

    Why it works: at DnB tempo a breakdown between every pair of
    drops bleeds the floor; the genre's default seam is drop ->
    drop with the energy line unbroken. Staging B's own first bar
    (not a foreign loop) under A's tail means the drop that lands
    is already familiar — its rhythm has been playing, at pressure
    level, for the whole window. Distinct from build_to_drop
    (T-009: two BUILDS layer and only B drops — A never reaches
    its own drop), from breakdown_transition (T-023: the seam
    lives inside a breakdown, the energy opposite), and from
    hook_drop_handoff (T-038: A exits ON a vocal hook; here A
    exits by completing its drop). The sparse cousin — B's intro
    over A's outro — is DJ.Studio's "Intro Over Outro" method and
    stays an EQ-blend staging, not this base: here both segments
    are drops and the window sits inside A's.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    stage_n = min(len(a), int(stage_bars) * bar_n)
    out_a = a.copy()
    if stage_n > 0 and len(b) > 0 and bar_n > 0:
        cell = b[:bar_n]
        if len(cell) < bar_n:
            cell = np.pad(cell, (0, bar_n - len(cell)))
        staged = np.resize(cell, stage_n)
        # lows killed: the staged cell is rhythm + timbre, never a
        # second bassline (the genre's one-bassline doctrine)
        staged = dsp.apply_3band_eq(staged, sr, -60.0, 0.0, 0.0)
        ref = float(np.max(np.abs(a[-stage_n:]))) + 1e-12
        peak = float(np.max(np.abs(staged))) + 1e-12
        staged = staged / peak * ref
        ramp = np.linspace(dsp.db_to_gain(stage_from_db),
                           dsp.db_to_gain(stage_to_db), stage_n)
        out_a[-stage_n:] += staged * ramp
    g = max(1, int(0.002 * sr))
    if g < len(out_a):
        out_a[-g:] *= 0.5 + 0.5 * np.cos(np.pi * np.linspace(0, 1, g))
    return np.concatenate([out_a, b])


# ----------------------------------------------------------------------------
# WEB-20 — Drop chop (Phase 23, genre traditions tranche A: DnB / riddim)
# ----------------------------------------------------------------------------

def drop_chop(a, b, sr, bar_s, chop_bars=2, rounds=2, land_bars=1):
    """Drop chop: two drops land together, then full-level ownership
    alternates between them on a bar grid before committing to B.

    Named in two fetched DnB texts: DJGear2K's double-drop guide
    (step 4 — once both drops are playing, "use the channel volume
    faders or the crossfader to either jump from one drop to
    another or blend the two drops together") and DJ.Studio's
    method 8, "Cutting and Switching" ("the DJ flicks the volume
    crossfader between the tracks... parts of new songs are
    quickly cut in and out... a cool way to tease elements of the
    new track"). Rendered at drop scale: after `land_bars` bars of
    both drops together (the double-drop landing), ownership
    alternates every `chop_bars` bars — A, B, A, B — for `rounds`
    full cycles, with the silent side killed outright (3 ms
    smoothed edges, never a blend). The chop IS the single-sub
    rule performed: exactly one bassline exists at any instant, so
    two full drops can occupy one passage without ever summing.
    After the last alternation the mix commits to B.

    Parameters
    ----------
    a, b : phrase-aligned DROP segments (mono float64), equal
        treatment — the shorter is zero-padded. Caller aligns the
        two drops' downbeats.
    sr : sample rate, Hz.
    bar_s : seconds per bar (the chop grid).
    chop_bars : bars per ownership window (default 2; 1 = the
        riddim quick-chop, 4 = the long DnB trade).
    rounds : full A+B alternation cycles after the landing
        (default 2).
    land_bars : bars both drops play together before the chop
        starts (default 1 — the landing must register as a double
        drop before it starts trading).

    Why it works: a double drop held static spends its surprise in
    one bar; chopping converts it into a conversation — each
    window is a reminder that both tracks are present, and each
    cut is a downbeat-level event the floor can anticipate and
    ride. Distinct from rhythmic_fader_chops (GAP-15: a 16th-note
    gate on an EXITING A while B fades in beneath — an entry
    gesture with a bar-5 deadline; here both tracks are already
    the main event, the period is bars not subdivisions, and
    neither side is fading anywhere) and from double_drop
    (T-024: both drops held under one enforced sub, then a bass
    swap — the chop replaces the hold with alternation).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n = max(len(a), len(b))
    if len(a) < n:
        a = np.pad(a, (0, n - len(a)))
    if len(b) < n:
        b = np.pad(b, (0, n - len(b)))
    bar_n = int(round(bar_s * sr))
    a_env = np.ones(n)
    b_env = np.ones(n)
    t0 = int(land_bars) * bar_n
    win = int(chop_bars) * bar_n
    n_alt = int(rounds) * 2
    for i in range(n_alt):
        w0 = t0 + i * win
        if w0 >= n:
            break
        w1 = min(n, w0 + win)
        if i % 2 == 0:
            b_env[w0:w1] = 0.0   # A owns this window
        else:
            a_env[w0:w1] = 0.0   # B owns this window
    commit = t0 + n_alt * win
    if commit < n:
        a_env[commit:] = 0.0     # the mix commits to B
    sm = max(1, int(0.003 * sr))
    if sm > 1:
        kernel = np.ones(sm) / sm
        for env in (a_env, b_env):
            smoothed = np.convolve(np.pad(env, (sm, sm), mode="edge"),
                                   kernel, mode="same")[sm:-sm]
            env[:] = smoothed
    return a * a_env + b * b_env


# ----------------------------------------------------------------------------
# WEB-21 — Drop insert (Phase 23, genre traditions tranche A: DnB / dubstep)
# ----------------------------------------------------------------------------

def drop_insert(a, b, sr, bar_s, insert_bars=1, drop_bar=8):
    """Drop insert: at A's drop downbeat, B's drop plays for
    `insert_bars` bars INSTEAD — then A's drop resumes.

    From the same note.com taxonomy's variety section ("Surprising
    spreading out from Buildup to Drop... when I move from the
    familiar build-up to the drop, I will insert a bar of another
    track to make it unexpected, and then return to the original
    track. It's just very difficult.") — and it is the shortest
    performed form of the dubstep switch: the crowd has been sold
    A's drop by A's build, a foreign drop fires for one bar, and
    then the promised drop arrives anyway, doubled in impact for
    having been withheld. A keeps running underneath while muted
    (the booth reality: the deck never stops), so A's drop resumes
    at the position it would have reached — the insert is a
    substitution window in A's timeline, not a pause in it.

    Parameters
    ----------
    a, b : segments (mono float64). `a` contains its build AND
        its drop; the drop's first downbeat is at bar `drop_bar`
        (caller aligns). `b` STARTS at its drop.
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    insert_bars : the substitution window (default 1 — the
        source's bar; 2 = a statement, 4 = the full dubstep switch,
        A's drop withheld for a whole phrase).
    drop_bar : bar index (0-based) of A's drop inside `a`.

    Why it works: expectation is the currency — the move spends
    one bar of it and repays with interest when the real drop
    lands mid-phrase, already in progress, as if it had never been
    interrupted. Distinct from fake_drop (T-029: the rug-pull is a
    VOID — nothing plays; here a whole foreign drop plays), from
    hotcue_drop_swap (T-014: the replacement is permanent; here A
    returns), from same_song_switchup (GAP-13: two arrangements of
    ONE track; here the guest is a different track), and from
    hook_drop_handoff (T-038: A exits for good on its hook). A
    human-triggered weapon like T-029 — it only reads on a
    well-known A whose drop the crowd can predict.
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    i0 = int(drop_bar) * bar_n
    i1 = min(len(a), i0 + int(insert_bars) * bar_n)
    out = a.copy()
    if i0 < len(a) and i1 > i0:
        seg = b[:i1 - i0]
        if len(seg) < i1 - i0:
            seg = np.pad(seg, (0, i1 - i0 - len(seg)))
        g = max(1, int(0.002 * sr))
        if 2 * g < len(seg):
            seg = seg.copy()
            seg[:g] *= 0.5 - 0.5 * np.cos(np.pi * np.linspace(0, 1, g))
            seg[-g:] *= 0.5 + 0.5 * np.cos(np.pi * np.linspace(0, 1, g))
        out[i0:i1] = seg
    return out


# ----------------------------------------------------------------------------
# Metadata registry (FRAMEWORK.md §3) — merged by engine/meta.py
# ----------------------------------------------------------------------------

_PEST = {"type": "cookbook",
         "ref": "Pestrela DJ Knowledge Base — Effects (DJM Beat FX / "
                "Colour FX taxonomy)",
         "url": "https://pestrela.github.io/dj_kb/effects/",
         "date": "2026-10-21"}

META = {
    "spiral_echo": {
        "title": "Spiral Echo (Pitch-Riding Feedback Delay)",
        "bank": "WEB-01", "family": "SPACE", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 10.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "breakdown", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "camelot>=2", "weight": 2,
             "reason": "the tail leaves A's pitch center — key distance "
                       "is forgiven"},
            {"when": "phrase_a==outro", "weight": 1,
             "reason": "a thrown final fragment is the classic spiral "
                       "exit"},
        ],
        "energy": {"delta": 0, "tension": "falling"},
        "exit": "tail", "clash_risk": "none",
        "params": {
            "delay_beats": {"type": "float", "range": [0.25, 1.5],
                            "default": 0.75, "unit": "beats",
                            "presets": {"quarter": 0.25, "dotted": 0.75,
                                        "beat": 1.0}},
            "shift_semitones": {"type": "float", "range": [-6.0, 6.0],
                                "default": 2.0, "unit": "semitones",
                                "presets": {"up2": 2.0, "up4": 4.0,
                                            "down2": -2.0, "down4": -4.0}},
            "repeats": {"type": "int", "range": [2, 16], "default": 8,
                        "unit": "repeats"},
            "feedback": {"type": "float", "range": [0.0, 0.85],
                         "default": 0.62, "unit": "ratio"},
            "fade_bars": {"type": "float", "range": [0.5, 8.0],
                          "default": 2.0, "unit": "bars"},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Pioneer DJM-450 manual — SPIRAL beat FX: pitch "
                    "changes simultaneously with delay time; LEVEL/DEPTH "
                    "sets feedback",
             "url": "https://www.manua.ls/pioneer/djm-450/manual?p=12",
             "date": "2026-10-21"},
            dict(_PEST),
        ],
        "composed_of": ["echo_out"],
    },
    "flanger_sweep": {
        "title": "Flanger Sweep (Jet Comb Build/Exit)",
        "bank": "WEB-02", "family": "FREQ", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "build", "drop", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta>=1", "weight": 2,
             "reason": "B's dry fullness contrasts the thinned A — "
                       "better when B is the bigger record"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "sweep_bars": {"type": "int", "range": [2, 16], "default": 8,
                           "unit": "bars",
                           "presets": {"tight": 4, "standard": 8,
                                       "long": 16}},
            "depth_ms": {"type": "float", "range": [0.5, 5.0],
                         "default": 2.2, "unit": "ms",
                         "presets": {"subtle": 1.2, "jet": 2.2,
                                     "deep": 3.8}},
            "cycles": {"type": "float", "range": [0.5, 8.0],
                       "default": 2.0, "unit": "cycles"},
            "mix": {"type": "float", "range": [0.0, 1.0],
                    "default": 0.85, "unit": "ratio"},
        },
        "evidence": [
            dict(_PEST),
            {"type": "course",
             "ref": "Engine DJ transition techniques — modulation "
                    "effects (flanger/phaser) for transition movement",
             "url": "https://app.studyraid.com/en/read/5035/107802/"
                    "layering-and-transition-techniques",
             "date": "2026-10-21"},
        ],
        "composed_of": [],
    },
    "reverse_roll": {
        "title": "Reverse Roll (Reversed Loop-Sampler Build)",
        "bank": "WEB-03", "family": "TIME", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 5.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "build", "drop"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta>=1", "weight": 2,
             "reason": "the inhalation build pays off into a bigger B"},
            {"when": "bpm_delta_pct<=1", "weight": 1,
             "reason": "grid-locked release — matched tempos keep the "
                       "roll honest"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "roll_bars": {"type": "int", "range": [1, 4], "default": 2,
                          "unit": "bars",
                          "presets": {"quick": 1, "standard": 2,
                                      "long": 4}},
        },
        "evidence": [dict(_PEST)],
        "composed_of": ["loop_roll_build"],
    },
    "crush_degrade": {
        "title": "Crush Degrade (Bit-Reduction Exit)",
        "bank": "WEB-04", "family": "DYN", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "verse", "chorus", "drop"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "genre_pair==leap", "weight": 2,
             "reason": "no pitch/tempo negotiation — the fidelity "
                       "contrast carries genre leaps"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "bits_end": {"type": "float", "range": [3.0, 10.0],
                         "default": 5.0, "unit": "bits",
                         "presets": {"lofi": 7.0, "crushed": 5.0,
                                     "destroyed": 3.5}},
            "bars": {"type": "int", "range": [2, 8], "default": 4,
                     "unit": "bars",
                     "presets": {"short": 2, "standard": 4, "long": 8}},
            "rate_end": {"type": "float", "range": [0.1, 0.75],
                         "default": 0.25, "unit": "ratio"},
            "fade_bars": {"type": "float", "range": [0.25, 4.0],
                          "default": 1.0, "unit": "bars"},
        },
        "evidence": [dict(_PEST)],
        "composed_of": [],
    },
    "shepard_riser": {
        "title": "Shepard Riser (Endless-Rise Build Layer)",
        "bank": "WEB-05", "family": "SYNTH", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "build", "drop", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta>=2", "weight": 2,
             "reason": "unresolved rising tension wants a much bigger "
                       "B to resolve into"},
            {"when": "phrase_a==build", "weight": 1,
             "reason": "the layer doubles a build that is already "
                       "rising"},
        ],
        "energy": {"delta": 2, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "direction": {"type": "int", "range": [-1, 1], "default": 1,
                          "unit": "sign",
                          "presets": {"up": 1, "down": -1}},
            "bars": {"type": "int", "range": [4, 16], "default": 8,
                     "unit": "bars",
                     "presets": {"short": 4, "standard": 8, "long": 16}},
            "level_db": {"type": "float", "range": [-24.0, -3.0],
                         "default": -9.0, "unit": "dB"},
            "partials": {"type": "int", "range": [4, 10], "default": 7,
                         "unit": "partials"},
        },
        "evidence": [
            dict(_PEST),
            {"type": "tutorial",
             "ref": "Sound on Sound — iZotope Mobius Filter review: "
                    "Shepard-tone construction (octave sine stack under "
                    "a level envelope) as perpetual-motion build",
             "url": "https://www.soundonsound.com/reviews/"
                    "izotope-mobius-filter",
             "date": "2026-10-21"},
        ],
        "composed_of": ["noise_echo_buildup"],
    },
    "granular_freeze": {
        "title": "Granular Freeze (Frozen-Moment Cloud Handoff)",
        "bank": "WEB-06", "family": "SPACE", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "breakdown", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "genre_pair==leap", "weight": 2,
             "reason": "the cloud owes no key/tempo allegiance — it "
                       "bridges leaps"},
            {"when": "phrase_a==breakdown", "weight": 1,
             "reason": "a sparse A freezes into a richer cloud than a "
                       "dense one"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "tail", "clash_risk": "none",
        "params": {
            "grain_ms": {"type": "float", "range": [25.0, 150.0],
                         "default": 70.0, "unit": "ms",
                         "presets": {"fine": 35.0, "standard": 70.0,
                                     "coarse": 120.0}},
            "cloud_bars": {"type": "int", "range": [2, 8], "default": 4,
                           "unit": "bars",
                           "presets": {"short": 2, "standard": 4,
                                       "long": 8}},
            "capture_ms": {"type": "float", "range": [80.0, 250.0],
                           "default": 150.0, "unit": "ms"},
            "density": {"type": "float", "range": [10.0, 90.0],
                        "default": 45.0, "unit": "grains/s"},
            "drift": {"type": "float", "range": [0.0, 1.0],
                      "default": 0.7, "unit": "fraction"},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Amazing Noises Grain Freezer — captures a ~150 ms "
                    "fragment and sustains it as a cloud of overlapping "
                    "grains (Rekkerd, 2026-10-21)",
             "url": "https://rekkerd.org/free-grain-freezer-granular-"
                    "effect-plugin-by-amazing-noises-vst3-au/",
             "date": "2026-10-21"},
            {"type": "tutorial",
             "ref": "Sound on Sound — Granular Synthesis: A Practical "
                    "Introduction (size/density/position; smeared and "
                    "frozen textures)",
             "url": "https://www.soundonsound.com/techniques/"
                    "granular-synthesis-practical-introduction",
             "date": "2026-10-21"},
        ],
        "composed_of": ["reverb_freeze"],
    },
    "helix_catch": {
        "title": "Helix Catch (Loop-Sampler Pitch-Ramp Hold & Release)",
        "bank": "WEB-07", "family": "TIME", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both",
                                  "neither"],
                     "phrase_a_ok": ["outro", "build", "drop", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta>=1", "weight": 2,
             "reason": "the release lands hardest when B is the "
                       "bigger record"},
            {"when": "phrase_a==drop", "weight": 1,
             "reason": "catching a drop's last beat is the hardware "
                       "move"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "capture_beats": {"type": "float", "range": [0.5, 4.0],
                              "default": 1.0, "unit": "beats",
                              "presets": {"half": 0.5, "beat": 1.0,
                                          "bar": 4.0}},
            "hold_bars": {"type": "int", "range": [1, 4],
                          "default": 2, "unit": "bars",
                          "presets": {"one": 1, "two": 2, "four": 4}},
            "ramp_semitones": {"type": "float",
                               "range": [-12.0, 12.0],
                               "default": 12.0, "unit": "semitones",
                               "presets": {"up_octave": 12.0,
                                           "up_fifth": 7.0,
                                           "down_octave": -12.0,
                                           "fixed": 0.0}},
            "fade_bars": {"type": "float", "range": [0.25, 4.0],
                          "default": 0.5, "unit": "bars"},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Pioneer DJM-900NXS2 manual p.17 via Pioneer "
                    "official forum (HELIX/FREEZE thread): engaging "
                    "HELIX loops the sound, releasing returns the "
                    "pitch to the engage point, LEVEL/DEPTH fully "
                    "right fixes the output pitch",
             "url": "https://forums.pioneerdj.com/hc/en-us/"
                    "community/posts/205498726-HELIX-FREEZE-ON-DJM-"
                    "900NXS2",
             "date": "2026-10-21"},
            dict(_PEST),
        ],
        "composed_of": ["loop_roll_build"],
    },
    "beatslicer_shuffle": {
        "title": "BeatSlicer Shuffle (Buffer Slice-Permutation Build)",
        "bank": "WEB-08", "family": "TIME", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both",
                                  "neither"],
                     "phrase_a_ok": ["outro", "build", "drop", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta>=1", "weight": 2,
             "reason": "the shuffled bar reads as a build — B "
                       "should cash it"},
            {"when": "phrase_a==chorus", "weight": 1,
             "reason": "a hook the floor knows, re-dealt, is the "
                       "strongest permutation material"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "pattern": {"type": "str", "range": None,
                        "default": "stride", "unit": "pattern",
                        "presets": {"stride": "stride",
                                    "reverse": "reverse",
                                    "bookends": "bookends",
                                    "swap_pairs": "swap_pairs",
                                    "halves": "halves",
                                    "inside_out": "inside_out"}},
            "buffer_bars": {"type": "int", "range": [1, 2],
                            "default": 1, "unit": "bars",
                            "presets": {"one": 1, "two": 2}},
            "buzz": {"type": "int", "range": [0, 1], "default": 1,
                     "unit": "flag",
                     "presets": {"off": 0, "on": 1}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Native Instruments Traktor 2 manual §14.4.29 "
                    "BeatSlicer Buffer: samples 2 bars, subdivides "
                    "into chunks, replays them in a different "
                    "sequence; 20 patterns in 5 styles",
             "url": "https://www.manua.ls/native-instruments/"
                    "traktor-2/manual?p=248",
             "date": "2026-10-21"},
        ],
        "composed_of": ["loop_roll_build", "stutter_transition"],
    },
    "downlifter_exit": {
        "title": "Downlifter Exit (Descending Sweep Seam Mask)",
        "bank": "WEB-09", "family": "SYNTH", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both",
                                  "neither"],
                     "phrase_a_ok": ["outro", "build", "drop", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "genre_pair==leap", "weight": 2,
             "reason": "the sweep licenses hard changes underneath "
                       "it"},
            {"when": "phrase_a==drop", "weight": 1,
             "reason": "a downer is the standard drop-exit "
                       "punctuation in EDM arrangement"},
        ],
        "energy": {"delta": 0, "tension": "falling"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "sweep_bars": {"type": "float", "range": [0.5, 2.0],
                           "default": 1.0, "unit": "bars",
                           "presets": {"half": 0.5, "one": 1.0,
                                       "two": 2.0}},
            "f_end": {"type": "float", "range": [80.0, 1500.0],
                      "default": 300.0, "unit": "Hz",
                      "presets": {"sub": 120.0, "low": 300.0,
                                  "mid": 800.0}},
            "f_start": {"type": "float", "range": [4000.0, 16000.0],
                        "default": 12000.0, "unit": "Hz"},
            "level_db": {"type": "float", "range": [-18.0, -3.0],
                         "default": -9.0, "unit": "dB",
                         "presets": {"under": -12.0,
                                     "standard": -9.0, "loud": -6.0}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "MusicRadar — How to make synth sweep FX for "
                    "EDM drops: risers build before a change, "
                    "'downers' are equally commonplace; noise through "
                    "a low-pass with automated cutoff",
             "url": "http://nghialong.com/synth-sweep-fx.html",
             "date": "2026-10-21"},
            {"type": "tutorial",
             "ref": "sonical.ly — How to Create Epic Risers and "
                    "Transition Effects for Electronic Music "
                    "(transition FX taxonomy)",
             "url": "https://sonical.ly/how-to-create-epic-risers-"
                    "and-transition-effects-for-electronic-music-a-"
                    "complete-guide/",
             "date": "2026-10-21"},
        ],
        "composed_of": ["noise_echo_buildup"],
    },
    "shimmer_wash": {
        "title": "Shimmer Wash (Octave-Climbing Reverb Exit)",
        "bank": "WEB-10", "family": "SPACE", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both",
                                  "neither"],
                     "phrase_a_ok": ["outro", "breakdown", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "camelot>=2", "weight": 2,
             "reason": "the tail climbs out of A's key — key "
                       "distance is forgiven"},
            {"when": "phrase_a==outro", "weight": 1,
             "reason": "a dissolving outro is the classic shimmer "
                       "exit"},
        ],
        "energy": {"delta": 0, "tension": "falling"},
        "exit": "tail", "clash_risk": "none",
        "params": {
            "shift_semitones": {"type": "float", "range": [5.0, 12.0],
                                "default": 12.0, "unit": "semitones",
                                "presets": {"octave": 12.0,
                                            "fifth": 7.0,
                                            "fourth": 5.0}},
            "swell_bars": {"type": "int", "range": [2, 8],
                           "default": 4, "unit": "bars",
                           "presets": {"short": 2, "standard": 4,
                                       "long": 8}},
            "level_db": {"type": "float", "range": [-24.0, -6.0],
                         "default": -12.0, "unit": "dB",
                         "presets": {"ghost": -18.0,
                                     "standard": -12.0,
                                     "present": -8.0}},
            "decay_s": {"type": "float", "range": [2.0, 12.0],
                        "default": 6.0, "unit": "s"},
            "fade_bars": {"type": "float", "range": [0.5, 8.0],
                          "default": 2.0, "unit": "bars"},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Pioneer RMX-1000 manual via Pestrela KB — "
                    "Reverb Up: adds reverberation and raises the "
                    "pitch of the echo as time passes (Reverb Down "
                    "lowers it)",
             "url": "https://pestrela.github.io/dj_kb/effects/",
             "date": "2026-10-21"},
            {"type": "tutorial",
             "ref": "Production Expert — How To Create Two "
                    "Specialist Reverbs: shimmer = pitch shift "
                    "(usually +12 semitones) before the reverb",
             "url": "https://www.production-expert.com/production-"
                    "expert-1/how-to-create-shimmer-reverb-and-the-"
                    "original-blackhole-reverb-in-pro-tools",
             "date": "2026-10-21"},
        ],
        "composed_of": ["reverb_wash"],
    },
    "infinity_filter": {
        "title": "Infinity Filter (Endless Barber-Pole Sweep Exit)",
        "bank": "WEB-11", "family": "FREQ", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both",
                                  "neither"],
                     "phrase_a_ok": ["outro", "build", "drop", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "camelot>=2", "weight": 2,
             "reason": "the peak stack never stops leaving A's pitch "
                       "center — key distance is forgiven"},
            {"when": "phrase_a==outro", "weight": 1,
             "reason": "an outro in permanent departure is the "
                       "classic infinity-sweep exit"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "direction": {"type": "int", "range": [-1, 1],
                          "default": 1, "unit": "sign",
                          "presets": {"up": 1, "down": -1}},
            "cycles": {"type": "float", "range": [0.5, 4.0],
                       "default": 2.0, "unit": "wraps",
                       "presets": {"one": 1.0, "two": 2.0,
                                   "three": 3.0}},
            "sweep_bars": {"type": "int", "range": [2, 8],
                           "default": 4, "unit": "bars",
                           "presets": {"short": 2, "standard": 4,
                                       "long": 8}},
            "mix": {"type": "float", "range": [0.5, 1.0],
                    "default": 0.85, "unit": "ratio"},
            "fade_bars": {"type": "float", "range": [0.25, 4.0],
                          "default": 0.5, "unit": "bars"},
        },
        "evidence": [
            {"type": "manual",
             "ref": "Serato Support — DJ-FX & Channel FX list "
                    "(Serato DJ Pro 3.2+): Infinity Filter and "
                    "Infinity Flanger among the Advanced FX; legacy "
                    "packs named the same idea Shepard Filter",
             "url": "https://support.serato.com/hc/en-us/articles/"
                    "10271055029263-DJ-FX-Channel-FX-list",
             "date": "2026-10-21"},
            {"type": "tutorial",
             "ref": "Serato Hex FX — Filters: the Infinity Filter "
                    "has \"endless sweeping peaks for evolving, "
                    "dramatic soundscapes\"; Infinity Flanger "
                    "\"rises or falls infinitely\"",
             "url": "http://serato.com/hex-fx",
             "date": "2026-10-21"},
            dict(_PEST),
        ],
        "composed_of": ["filter_sweep"],
    },
    "pattern_layer_bridge": {
        "title": "Pattern Layer Bridge (Pattern Player Seam Layer)",
        "bank": "WEB-12", "family": "SYNTH", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 6.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both",
                                  "neither"],
                     "phrase_a_ok": ["breakdown", "outro", "build",
                                     "drop"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "phrase_a==breakdown", "weight": 2,
             "reason": "NI's recipe starts the pattern in A's "
                       "breakdown, where neither track owns the "
                       "groove"},
            {"when": "energy_delta>=1", "weight": 1,
             "reason": "the pattern's activity arc builds into a "
                       "bigger B"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "seamless", "clash_risk": "none",
        "params": {
            "pattern": {"type": "str", "range": None,
                        "default": "groove", "unit": "pattern",
                        "presets": {"foundation": "foundation",
                                    "groove": "groove",
                                    "build": "build",
                                    "roll": "roll"}},
            "kit": {"type": "str", "range": None,
                    "default": "kit909", "unit": "kit",
                    "presets": {"kit808": "kit808",
                                "kit909": "kit909"}},
            "bars": {"type": "int", "range": [4, 16], "default": 8,
                     "unit": "bars",
                     "presets": {"short": 4, "standard": 8,
                                 "long": 16}},
            "level_db": {"type": "float", "range": [-18.0, -3.0],
                         "default": -9.0, "unit": "dB"},
            "duck_db": {"type": "float", "range": [0.0, 12.0],
                        "default": 0.0, "unit": "dB"},
            "duck_release_ms": {"type": "float",
                                "range": [200.0, 500.0],
                                "default": 300.0, "unit": "ms"},
        },
        "evidence": [
            {"type": "manual",
             "ref": "Native Instruments Traktor Pro 4 manual — "
                    "Pattern Player: an FX-unit mode playing "
                    "rhythmic one-shot patterns in sync with the "
                    "master clock; Volume/Kit/Pattern/Pitch/Decay "
                    "controls; ducking sidechains the deck to the "
                    "pattern, duck release 200-500 ms set by Decay",
             "url": "https://www.manua.ls/native-instruments/"
                    "traktor-pro-4/manual?p=25",
             "date": "2026-10-21"},
            {"type": "tutorial",
             "ref": "Native Instruments Blog — Beyond "
                    "four-on-the-floor: mixing with the Pattern "
                    "Player in Traktor Pro 4 (transitions and "
                    "builds: pattern over A's breakdown, raise "
                    "activity, drop B, swap the bass under the "
                    "pattern, fade A out, dial the pattern back)",
             "url": "https://blog.native-instruments.com/"
                    "pattern-player-traktor-pro/",
             "date": "2026-10-21"},
        ],
        "composed_of": ["drum_bridge"],
    },
    "pumper_exit": {
        "title": "Pumper Exit (Downbeat Duck Pump Exit)",
        "bank": "WEB-13", "family": "DYN", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 10.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both",
                                  "neither"],
                     "phrase_a_ok": ["chorus", "verse", "build",
                                     "drop"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta>=1", "weight": 1,
             "reason": "the withheld final recovery makes B's "
                       "entrance feel bigger — the hole is the "
                       "drop"},
            {"when": "phrase_a==chorus", "weight": 1,
             "reason": "downbeat-strong material pumps cleanest; "
                       "the duck grid reads on a full groove"},
        ],
        "energy": {"delta": 1, "tension": "build"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "duck_db": {"type": "float", "range": [-20.0, -2.0],
                        "default": -10.0, "unit": "dB",
                        "presets": {"light": -6.0,
                                    "standard": -10.0,
                                    "deep": -16.0}},
            "offset_beats": {"type": "float",
                             "range": [-0.5, 0.0],
                             "default": -0.25, "unit": "beats",
                             "presets": {"on_grid": 0.0,
                                         "early16": -0.0625,
                                         "early8": -0.125,
                                         "early4": -0.25}},
            "rate_beats": {"type": "float", "range": [0.5, 2.0],
                           "default": 1.0, "unit": "beats"},
            "pump_bars": {"type": "int", "range": [2, 8],
                          "default": 4, "unit": "bars",
                          "presets": {"short": 2, "standard": 4,
                                      "long": 8}},
        },
        "evidence": [
            {"type": "manual",
             "ref": "Denon DJ X1850 PRIME User Guide — Effects "
                    "chapter: Pumper 'attenuates or ducks audio "
                    "on the downbeat, similar to a sidechain "
                    "compressor'; Duck -2..-20 dB, Offset "
                    "-1/16..-1/2 beats",
             "url": "https://cdn.inmusicbrands.com/denondj/"
                    "X1850Prime/_abcd321_X1850_PRIME-UserGuide"
                    "-v1_1.pdf",
             "date": "2026-10-21"},
            {"type": "manual",
             "ref": "rekordbox DDJ-RZX / XDJ-RX3 manuals — "
                    "Release FX DUCKING pad: 'changes the volume "
                    "according to the beat and fades out the "
                    "sound by adding a ducking-like effect' "
                    "(second vendor, exit form)",
             "url": "https://rekordbox.com",
             "date": "2026-10-21"},
        ],
        "composed_of": ["riser_ducking_overlay"],
    },
    "scale_down_exit": {
        "title": "Scale Down Exit (Beat-Stepped Pitch Descent)",
        "bank": "WEB-14", "family": "TIME", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 10.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both",
                                  "neither"],
                     "phrase_a_ok": ["outro", "breakdown", "verse",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "camelot>=2", "weight": 2,
             "reason": "every replay leaves A's pitch center "
                       "further behind — the descent is clash-safe "
                       "exactly where a held tail would fight B"},
            {"when": "phrase_a==outro", "weight": 1,
             "reason": "a captured beat walking downstairs is an "
                       "outro gesture — it needs A's tail, not "
                       "its peak"},
        ],
        "energy": {"delta": 0, "tension": "falling"},
        "exit": "tail", "clash_risk": "none",
        "params": {
            "scale": {"type": "str", "range": None,
                      "default": "major", "unit": "scale",
                      "presets": {"major": "major",
                                  "minor": "minor",
                                  "major_pent": "major_pent",
                                  "minor_pent": "minor_pent",
                                  "chromatic": "chromatic"}},
            "steps": {"type": "int", "range": [2, 8],
                      "default": 4, "unit": "steps",
                      "presets": {"few": 3, "standard": 4,
                                  "deep": 6}},
            "capture_beats": {"type": "float",
                              "range": [0.5, 2.0], "default": 1.0,
                              "unit": "beats"},
            "step_beats": {"type": "float", "range": [0.5, 2.0],
                           "default": 1.0, "unit": "beats"},
            "fade_bars": {"type": "float", "range": [0.0, 4.0],
                          "default": 2.0, "unit": "bars"},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "Engine DJ v3.1.0 release article — Main FX "
                    "one-liners: Pitch Down 'chromatically "
                    "pitches down the captured audio in time "
                    "with the beat'; Scale Down 'similar to "
                    "Pitch Down, using four different scales to "
                    "add color to a transition'",
             "url": "https://enginedj.com/news/articles/engine"
                    "-dj-v3-1-0-now-available-touch-fx-25-new-"
                    "and-enhanced-main-fx",
             "date": "2026-10-21"},
            {"type": "tutorial",
             "ref": "Engine DJ 3.1 Release Notes (inMusic "
                    "Support) — the 26-effect Main FX roster, "
                    "Pitch Down / Scale Down among the new "
                    "effects",
             "url": "https://inmusicsupport.freshdesk.com/en/"
                    "support/solutions/articles/69000839161-"
                    "engine-dj-3-1-release-notes",
             "date": "2026-10-21"},
        ],
        "composed_of": ["spiral_echo"],
    },
    "fader_synth": {
        "title": "Fader Synth (Source-Replacing Fader Oscillator)",
        "bank": "WEB-15", "family": "SYNTH", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 6.0, "camelot_max": 3,
                     "vocal_ok": ["a_only", "b_only", "both",
                                  "neither"],
                     "phrase_a_ok": ["breakdown", "build", "drop",
                                     "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "phrase_a==breakdown", "weight": 2,
             "reason": "the fader ride needs a sparse seam — "
                       "where the record thins, the synth line "
                       "owns the space it replaces"},
            {"when": "energy_delta>=1", "weight": 1,
             "reason": "the ride's climb is directed energy B "
                       "inherits at the seam"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "seamless", "clash_risk": "key",
        "params": {
            "waveform": {"type": "str", "range": None,
                         "default": "saw", "unit": "waveform",
                         "presets": {"sine": "sine", "saw": "saw",
                                     "square": "square"}},
            "ride": {"type": "str", "range": None,
                     "default": "steps", "unit": "ride",
                     "presets": {"steps": "steps",
                                 "glide": "glide",
                                 "arp": "arp",
                                 "hold": "hold"}},
            "scale": {"type": "str", "range": None,
                      "default": "major", "unit": "scale",
                      "presets": {"major": "major",
                                  "minor": "minor",
                                  "minor_h": "minor_h",
                                  "japanese": "japanese"}},
            "root_hz": {"type": "float", "range": [55.0, 220.0],
                        "default": 110.0, "unit": "Hz"},
            "base_octave": {"type": "int", "range": [-3, 3],
                            "default": 0, "unit": "octaves",
                            "presets": {"down": -1, "base": 0,
                                        "up": 1}},
            "zone_bars": {"type": "int", "range": [2, 8],
                          "default": 4, "unit": "bars",
                          "presets": {"short": 2, "standard": 4,
                                      "long": 8}},
            "level_db": {"type": "float", "range": [-12.0, -3.0],
                         "default": -6.0, "unit": "dB"},
        },
        "evidence": [
            {"type": "manual",
             "ref": "Pioneer DJM-S11 manual — Beat FX types and "
                    "settings, FADER SYNTH (SINE/SAW/SQUARE) "
                    "p.61: 'outputs the synth sound as the audio "
                    "source of the base oscillation frequency'; "
                    "base frequency level -3..+3; scale sub "
                    "parameter (AUTO SCALE, MAJOR, MINOR, "
                    "MINOR H, JAPANESE, ...); FADER PITCH p.60",
             "url": "https://www.manua.ls/pioneer/djm-s11/"
                    "manual?p=61",
             "date": "2026-10-21"},
        ],
        "composed_of": ["cdj_synth_lead"],
    },
    "ring_mod_dissolve": {
        "title": "Ring Mod Dissolve (Carrier-Multiplication Exit)",
        "bank": "WEB-16", "family": "FREQ", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both",
                                  "neither"],
                     "phrase_a_ok": ["outro", "build", "drop",
                                     "verse", "chorus", "breakdown"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta>=1", "weight": 1,
             "reason": "the rising carrier is directed tension "
                       "that resolves when B lands dry"},
            {"when": "genre_pair==leap", "weight": 1,
             "reason": "multiplication erases A's pitch identity "
                       "— legal across a leap where blends are "
                       "not"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "carrier_start_hz": {"type": "float",
                                 "range": [40.0, 1000.0],
                                 "default": 100.0, "unit": "Hz",
                                 "presets": {"low": 60.0,
                                             "manual_min": 100.0,
                                             "mid": 240.0}},
            "carrier_end_hz": {"type": "float",
                               "range": [400.0, 8371.0],
                               "default": 2800.0, "unit": "Hz",
                               "presets": {"soft": 1200.0,
                                           "standard": 2800.0,
                                           "manual_max": 8371.0}},
            "morph": {"type": "float", "range": [0.0, 1.0],
                      "default": 1.0, "unit": "AM..RM",
                      "presets": {"am": 0.0, "half": 0.5,
                                  "rm": 1.0}},
            "raw": {"type": "str", "range": None,
                    "default": "sine", "unit": "carrier",
                    "presets": {"sine": "sine", "raw": "square"}},
            "zone_bars": {"type": "int", "range": [2, 8],
                          "default": 4, "unit": "bars",
                          "presets": {"short": 2, "standard": 4,
                                      "long": 8}},
            "fade_bars": {"type": "float", "range": [0.25, 1.0],
                          "default": 0.5, "unit": "bars",
                          "presets": {"tight": 0.25,
                                      "standard": 0.5}},
        },
        "evidence": [
            {"type": "manual",
             "ref": "Native Instruments Traktor 2 manual — The "
                    "Effects in Detail, §14.4.25 Ring Modulator "
                    "(p.245): 'modulates the tracks by multiplying "
                    "the high frequency signal onto the audio "
                    "material'; oscillator 100 Hz-8371 Hz; AM-RM "
                    "morph; RAW sine -> filtered square carrier",
             "url": "https://www.manua.ls/native-instruments/"
                    "traktor-2/manual?p=245",
             "date": "2026-10-21"},
        ],
        "composed_of": [],
    },
    "formant_morph_exit": {
        "title": "Formant Morph Exit (Vowel-Series Spectral Morph)",
        "bank": "WEB-17", "family": "FREQ", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both",
                                  "neither"],
                     "phrase_a_ok": ["outro", "build", "drop",
                                     "verse", "chorus", "breakdown"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "vocal_pair==a_only", "weight": 2,
             "reason": "on a vocal A the morph re-articulates the "
                       "singer's own vowels — the talker effect "
                       "doubles"},
            {"when": "phrase_a==breakdown", "weight": 1,
             "reason": "sparse sections let individual vowels "
                       "read as events"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "path": {"type": "str", "range": None,
                     "default": "aeiou", "unit": "vowels",
                     "presets": {"aeiou": "aeiou",
                                 "ouiea": "ouiea", "ai": "ai",
                                 "ou": "ou"}},
            "table": {"type": "str", "range": None,
                      "default": "english", "unit": "formants",
                      "presets": {"english": "english",
                                  "german": "german"}},
            "sharp": {"type": "float", "range": [0.5, 2.0],
                      "default": 1.0, "unit": "presence",
                      "presets": {"soft": 0.6, "standard": 1.0,
                                  "present": 1.8}},
            "zone_bars": {"type": "int", "range": [2, 8],
                          "default": 4, "unit": "bars",
                          "presets": {"short": 2, "standard": 4,
                                      "long": 8}},
            "mix": {"type": "float", "range": [0.5, 1.0],
                    "default": 0.9, "unit": "wet",
                    "presets": {"light": 0.7, "standard": 0.9,
                                "total": 1.0}},
            "fade_bars": {"type": "float", "range": [0.25, 1.0],
                          "default": 0.5, "unit": "bars",
                          "presets": {"tight": 0.25,
                                      "standard": 0.5}},
        },
        "evidence": [
            {"type": "manual",
             "ref": "Native Instruments Traktor 2 manual — The "
                    "Effects in Detail, §14.4.30 Formant Filter "
                    "(p.249): 'imitates the sound of spoken "
                    "vowels by morphing three bandpass filters "
                    "into each other'; TALK morphs the a-e-i-o-u "
                    "formants; SHARP presence; TYP German/English",
             "url": "https://www.manua.ls/native-instruments/"
                    "traktor-2/manual?p=249",
             "date": "2026-10-21"},
        ],
        "composed_of": [],
    },
    "resonator_tail": {
        "title": "Resonator Tail (Tuned Resonator-Bank Ring-Out)",
        "bank": "WEB-18", "family": "SPACE", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": 2,
                     "vocal_ok": ["a_only", "b_only", "both",
                                  "neither"],
                     "phrase_a_ok": ["outro", "build", "drop",
                                     "verse", "chorus", "breakdown"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "camelot<=1", "weight": 2,
             "reason": "the ring is tuned to B's chord — the "
                       "closer the pair, the more literally the "
                       "tail lands as B's harmony"},
            {"when": "phrase_a==breakdown", "weight": 1,
             "reason": "sparse excitation reads as distinct "
                       "plucked-string gestures in the bank"},
            {"when": "energy_delta<=0", "weight": 1,
             "reason": "a decaying string tail is a falling-"
                       "tension exit; it spends energy, it does "
                       "not build it"},
        ],
        "energy": {"delta": 0, "tension": "falling"},
        "exit": "tail", "clash_risk": "low",
        "params": {
            "chord": {"type": "str", "range": None,
                      "default": "major", "unit": "voicing",
                      "presets": {"major": "major",
                                  "minor": "minor",
                                  "power": "power",
                                  "octave": "octave"}},
            "decay_s": {"type": "float", "range": [0.8, 6.0],
                        "default": 2.5, "unit": "s",
                        "presets": {"short": 1.2,
                                    "standard": 2.5,
                                    "long": 4.5}},
            "color": {"type": "float", "range": [0.0, 1.0],
                      "default": 0.5, "unit": "brightness",
                      "presets": {"dark": 0.2,
                                  "standard": 0.5,
                                  "bright": 0.85}},
            "root_midi": {"type": "int", "range": [36, 60],
                          "default": 45, "unit": "MIDI note",
                          "presets": {"low": 36,
                                      "standard": 45,
                                      "high": 57}},
            "zone_bars": {"type": "int", "range": [1, 4],
                          "default": 2, "unit": "bars",
                          "presets": {"short": 1,
                                      "standard": 2,
                                      "long": 4}},
            "ring_level": {"type": "float", "range": [0.3, 1.0],
                           "default": 0.85, "unit": "wet",
                           "presets": {"soft": 0.55,
                                       "standard": 0.85,
                                       "full": 1.0}},
            "fade_bars": {"type": "float", "range": [0.25, 2.0],
                          "default": 1.0, "unit": "bars",
                          "presets": {"tight": 0.5,
                                      "standard": 1.0,
                                      "slow": 2.0}},
        },
        "evidence": [
            {"type": "manual",
             "ref": "Ableton Live 12 manual — Live Audio Effect "
                    "Reference, Resonators: 'five parallel "
                    "resonators that add a tonal character to "
                    "the input signal and can be tuned in "
                    "semitones or scale degrees'; Decay = time "
                    "for the resonators 'to be silent after "
                    "getting an input signal... similar to the "
                    "behavior of an undamped piano string', "
                    "pitch-dependent; Color = brightness; "
                    "Resonator I Note sets the root, II-V "
                    "tuned relative in intervals, ±24 semitones",
             "url": "https://www.ableton.com/en/manual/"
                    "live-audio-effect-reference/",
             "date": "2026-10-21"},
            {"type": "manual",
             "ref": "Same reference, Spectral Resonator: the "
                    "spectral sibling — 'applying tuned "
                    "resonances to its spectrum... highlight "
                    "chosen frequencies of the resonating "
                    "partials and alter their decay', harmonics "
                    "quantizable to the active scale; banked "
                    "as the same family's second device, not "
                    "a second base",
             "url": "https://www.ableton.com/en/manual/"
                    "live-audio-effect-reference/",
             "date": "2026-10-21"},
        ],
        "composed_of": [],
    },
    # ------------------------------------------------------------- WEB-19
    "continuous_drop": {
        "title": "Continuous Drop (Drop-to-Drop Relay)",
        "bank": "WEB-19", "family": "STRUCT", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 3.0, "camelot_max": 2,
                     "vocal_ok": ["a_only", "b_only", "neither"],
                     "phrase_a_ok": ["drop"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": ["drop_pair", "b_build"]},
        "prefers": [
            {"when": "phrase_a==drop", "weight": 3,
             "reason": "A is in its drop — the staging window lives inside it"},
            {"when": "energy_delta>=0", "weight": 2,
             "reason": "the relay only runs forward — B's drop holds or raises the floor"},
            {"when": "camelot<=1", "weight": 1,
             "reason": "the staged cell rides A's tail — keys must not fight at pressure level"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "snap", "clash_risk": "bass",
        "params": {
            "stage_bars": {"type": "int", "range": [4, 16],
                           "default": 8, "unit": "bars",
                           "presets": {"4bar": 4, "8bar": 8,
                                       "16bar": 16}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "kohadachan, 'A Personal Drum and Bass DJ how to' (note.com, 2024) — transition-pattern taxonomy: 'Continuous Drop: the end of the previous track's drop -> the start of the next track's drop (start from 8 bars before the previous track drop's end)'",
             "url": "https://note.com/kohadachan/n/na667cfa0b9e9",
             "date": "2026-10-22"},
            {"type": "tutorial",
             "ref": "DJ.Studio, 'How To Mix Drum And Bass' (2024) — the drop-respecting method family (double drops, breakdown switch, intro over outro) the relay belongs to",
             "url": "https://dj.studio/blog/mix-drum-and-bass",
             "date": "2026-10-22"},
        ],
        "composed_of": [],
    },
    # ------------------------------------------------------------- WEB-20
    "drop_chop": {
        "title": "Drop Chop (Alternating Drop Ownership)",
        "bank": "WEB-20", "family": "STRUCT", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 3.0, "camelot_max": 2,
                     "vocal_ok": ["a_only", "b_only", "neither"],
                     "phrase_a_ok": ["drop"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": ["drop_pair"]},
        "prefers": [
            {"when": "energy_delta_abs<=1", "weight": 2,
             "reason": "the trades read as equals — a hotter B ends the conversation early"},
            {"when": "phrase_a==drop", "weight": 3,
             "reason": "both drops are live — the chop sustains a landed double drop"},
        ],
        "energy": {"delta": 0, "tension": "build"},
        "exit": "snap", "clash_risk": "bass",
        "params": {
            "chop_bars": {"type": "int", "range": [1, 4],
                          "default": 2, "unit": "bars",
                          "presets": {"1bar": 1, "2bar": 2,
                                      "4bar": 4}},
            "rounds": {"type": "int", "range": [1, 4],
                       "default": 2, "unit": "cycles",
                       "presets": {"x1": 1, "x2": 2, "x4": 4}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "DJGear2K, 'What Is A Double Drop?' (2023) — step 4: with both drops playing, 'use the channel volume faders or the crossfader to either jump from one drop to another or blend the two drops together'",
             "url": "https://djgear2k.com/double-drop-mixing-guide/",
             "date": "2026-10-22"},
            {"type": "tutorial",
             "ref": "DJ.Studio, 'How To Mix Drum And Bass' (2024) — method 8, 'Cutting and Switching': flicking the crossfader between tracks to tease elements of the new track and create sudden transitions",
             "url": "https://dj.studio/blog/mix-drum-and-bass",
             "date": "2026-10-22"},
        ],
        "composed_of": ["double_drop"],
    },
    # ------------------------------------------------------------- WEB-21
    "drop_insert": {
        "title": "Drop Insert (Guest-Bar Drop Substitution)",
        "bank": "WEB-21", "family": "STRUCT", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 3.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "neither"],
                     "phrase_a_ok": ["build"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": ["drop_pair"]},
        "prefers": [
            {"when": "energy_delta>=1", "weight": 1,
             "reason": "human-triggered weapon — the guest bar must hit at least as hard as the drop it replaces"},
            {"when": "iconic_a", "weight": 2,
             "reason": "the move only reads on a well-known A whose drop the crowd can predict"},
        ],
        "energy": {"delta": 1, "tension": "build"},
        "exit": "snap", "clash_risk": "none",
        "params": {
            "insert_bars": {"type": "int", "range": [1, 4],
                            "default": 1, "unit": "bars",
                            "presets": {"1bar": 1, "2bar": 2,
                                        "4bar": 4}},
        },
        "evidence": [
            {"type": "tutorial",
             "ref": "kohadachan, 'A Personal Drum and Bass DJ how to' (note.com, 2024) — 'when I move from the familiar build-up to the drop, I will insert a bar of another track to make it unexpected, and then return to the original track'",
             "url": "https://note.com/kohadachan/n/na667cfa0b9e9",
             "date": "2026-10-22"},
            {"type": "tutorial",
             "ref": "Pioneer DJ, DDJ-400 technique tutorials (2019) — the drop swap named 'a staple of trap and dubstep music': the performed fake-out family this insert is the shortest form of",
             "url": "https://www.pioneerdj.com/en/news/2019/ddj-400-dj-controller-mixing-technique-tutorials/",
             "date": "2026-10-22"},
        ],
        "composed_of": [],
    },
}


# Plan-renderer exports (FRAMEWORK.md §7): fn(a, b, sr, **kwargs).
TECHNIQUE_FUNCS = {
    "spiral_echo": spiral_echo,
    "flanger_sweep": flanger_sweep,
    "reverse_roll": reverse_roll,
    "crush_degrade": crush_degrade,
    "shepard_riser": shepard_riser,
    "granular_freeze": granular_freeze,
    "helix_catch": helix_catch,
    "beatslicer_shuffle": beatslicer_shuffle,
    "downlifter_exit": downlifter_exit,
    "shimmer_wash": shimmer_wash,
    "infinity_filter": infinity_filter,
    "pattern_layer_bridge": pattern_layer_bridge,
    "pumper_exit": pumper_exit,
    "scale_down_exit": scale_down_exit,
    "fader_synth": fader_synth,
    "ring_mod_dissolve": ring_mod_dissolve,
    "formant_morph_exit": formant_morph_exit,
    "resonator_tail": resonator_tail,
    "continuous_drop": continuous_drop,
    "drop_chop": drop_chop,
    "drop_insert": drop_insert,
}
