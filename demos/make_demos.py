"""
open-transitions — technique demo renderer + verifier.

Synthesizes two deterministic test tracks (no copyrighted audio) and renders
a demo clip for every implemented engine technique, running verify.verify_clip
on each. Output: demos/out/<technique>.wav, <technique>-verify.png,
verification.json.

Usage:
    python3 demos/make_demos.py [--out-dir demos/out] [--only hook_drop_handoff]
"""

import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import dsp, techniques, verify

SR = 44100
BPM = 128.0
BEAT_S = 60.0 / BPM
BAR_S = 4 * BEAT_S


# ----------------------------------------------------------------------------
# Deterministic test-track synthesis (sketch material only)
# ----------------------------------------------------------------------------

def _kick(sr, n):
    t = np.arange(n) / sr
    f = 55 * np.exp(-t * 30) + 38
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 18)


def _hat(sr, n, decay=60.0):
    from scipy import signal as _sig
    rng = np.random.default_rng(3)
    t = np.arange(n) / sr
    nz = rng.standard_normal(n)
    # crude highpass via diff, then a real 10 kHz lowpass — real hats roll
    # off; unfiltered diff-noise carries energy to Nyquist that yanks the
    # spectral centroid in sparse windows (diagnostic noise, not music)
    hp = np.diff(nz, prepend=0)
    hp = 0.5 * (hp + np.roll(hp, 1))
    sos = _sig.butter(4, 10000.0, btype="lowpass", fs=sr, output="sos")
    hp = _sig.sosfilt(sos, hp)
    return hp * np.exp(-t * decay)


def _bass(sr, n, f0):
    t = np.arange(n) / sr
    # subby square-ish: sine + 3rd harmonic
    return (np.sin(2 * np.pi * f0 * t) + 0.25 * np.sin(2 * np.pi * 3 * f0 * t)) \
        * np.exp(-t * 6)


def _stab(sr, n, freqs):
    t = np.arange(n) / sr
    s = sum(np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)
    return s * np.exp(-t * 8)


def _vocal_hook(sr, n, f0=196.0):
    """Formant-ish 'oh' hook: harmonic stack with vibrato + syllable pump."""
    t = np.arange(n) / sr
    vib = 1.0 + 0.01 * np.sin(2 * np.pi * 5.5 * t)
    harm = np.zeros(n)
    for h, amp in [(1, 1.0), (2, 0.5), (3, 0.28), (4, 0.16), (5, 0.1)]:
        harm += amp * np.sin(2 * np.pi * f0 * h * np.cumsum(vib) / sr)
    # formant emphasis around 800 Hz and 2400 Hz (crude, static)
    harm = harm / (np.max(np.abs(harm)) + 1e-9)
    # two-syllable pump: "oh ... OH"
    beats = n / sr / BEAT_S
    u = np.linspace(0, 1, n)
    pump = 0.55 + 0.45 * np.sin(np.pi * np.clip(u * 2, 0, 1)) ** 2
    return harm * pump * 0.7


def build_track(sr, bpm, bars, seed, root=55.0, hook_bars=0,
                drums=True, bass=True, stabs=True):
    """Deterministic groove sketch. hook_bars: vocal hook over the last N bars."""
    rng = np.random.default_rng(seed)
    n = int(bars * BAR_S * sr)
    x = np.zeros(n)
    beat_n = int(BEAT_S * sr)

    kick = _kick(sr, beat_n)
    hat = _hat(sr, beat_n // 2)
    hat16 = _hat(sr, beat_n // 4, decay=90.0)
    for b in range(bars * 4):
        i = b * beat_n
        if drums and b % 4 == 0 and i + beat_n <= n:
            x[i:i + beat_n] += kick * 0.9
        # continuous 16th-note hats: the groove's HF anchor (no sparse windows)
        for s in range(4):
            j = i + s * beat_n // 4
            k = beat_n // 4
            if drums and j + k <= n:
                x[j:j + k] += hat16[:k] * 0.13
        if drums and b % 2 == 1 and i + beat_n // 2 <= n:
            x[i + beat_n // 4:i + beat_n // 4 + beat_n // 2] += hat[:beat_n // 2] * 0.22
        if bass and b % 4 in (0, 1, 3) and i + beat_n <= n:
            bn = _bass(sr, beat_n, root * (1.5 if b % 8 == 6 else 1.0))
            x[i:i + beat_n] += bn[:beat_n] * 0.5
    if stabs:
        for bar in range(0, bars, 2):
            i = bar * int(BAR_S * sr)
            st = _stab(sr, int(BAR_S * sr), [220.0, 261.6, 329.6])
            k = min(len(st), n - i)
            x[i:i + k] += st[:k] * 0.25
    if hook_bars:
        hn = int(hook_bars * BAR_S * sr)
        hk = _vocal_hook(sr, hn)
        x[n - hn:] += hk * 0.8
    # continuous low bed: keeps the sketch above the silence floor between
    # drum hits (the verify gate flags >50 ms below -60 dBFS). Harmonic
    # series — no detuned pairs (their beat-frequency cancellation creates
    # momentary dropouts that read as gaps).
    t = np.arange(n) / sr
    bed = (np.sin(2 * np.pi * root * 4 * t)
           + 0.4 * np.sin(2 * np.pi * root * 6 * t)
           + 0.25 * np.sin(2 * np.pi * root * 8 * t))
    bed = bed / (np.max(np.abs(bed)) + 1e-9)
    lfo = 0.7 + 0.3 * np.sin(2 * np.pi * 0.125 * t)
    x = x + bed * lfo * 0.06
    # gentle master glue
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.85
    return x


def build_breakdown(sr, bpm, bars, seed):
    """Drumless breakdown sketch: pads + hook, no kick."""
    n = int(bars * BAR_S * sr)
    t = np.arange(n) / sr
    pad = sum(np.sin(2 * np.pi * f * t + 0.5) for f in [110.0, 138.6, 164.8])
    pad = pad / (np.max(np.abs(pad)) + 1e-9)
    env = 0.6 + 0.4 * np.sin(np.pi * np.linspace(0, 1, n))
    hk = _vocal_hook(sr, n, f0=174.0)
    x = pad * env * 0.4 + hk * 0.5
    return x / (np.max(np.abs(x)) + 1e-9) * 0.8


def build_vocal_only(sr, bpm, bars, seed):
    n = int(bars * BAR_S * sr)
    hk = _vocal_hook(sr, n, f0=196.0)
    return hk / (np.max(np.abs(hk)) + 1e-9) * 0.8


TRACKS = {}


def build_track_stems(sr, bpm, bars_n, seed, root=55.0, hook=False,
                      drums=True, bass=True, stabs=True):
    """Stem-separated sketch track: drums / bass / melody / vocal as
    separate arrays (sums to a full track). Used by ROUTING-family demos
    that hand over elements, not bands."""
    n = int(bars_n * BAR_S * sr)
    dr = np.zeros(n)
    bs = np.zeros(n)
    mel = np.zeros(n)
    beat_n = int(BEAT_S * sr)

    kick = _kick(sr, beat_n)
    hat = _hat(sr, beat_n // 2)
    hat16 = _hat(sr, beat_n // 4, decay=90.0)
    for b in range(bars_n * 4):
        i = b * beat_n
        if drums and b % 4 == 0 and i + beat_n <= n:
            dr[i:i + beat_n] += kick * 0.9
        for s in range(4):
            j = i + s * beat_n // 4
            k = beat_n // 4
            if drums and j + k <= n:
                dr[j:j + k] += hat16[:k] * 0.13
        if drums and b % 2 == 1 and i + beat_n // 2 <= n:
            dr[i + beat_n // 4:i + beat_n // 4 + beat_n // 2] += hat[:beat_n // 2] * 0.22
        if bass and b % 4 in (0, 1, 3) and i + beat_n <= n:
            bn = _bass(sr, beat_n, root * (1.5 if b % 8 == 6 else 1.0))
            bs[i:i + beat_n] += bn[:beat_n] * 0.5
    if stabs:
        for bar in range(0, bars_n, 2):
            i = bar * int(BAR_S * sr)
            st = _stab(sr, int(BAR_S * sr), [220.0, 261.6, 329.6])
            k = min(len(st), n - i)
            mel[i:i + k] += st[:k] * 0.25
    t = np.arange(n) / sr
    bed = (np.sin(2 * np.pi * root * 4 * t)
           + 0.4 * np.sin(2 * np.pi * root * 6 * t)
           + 0.25 * np.sin(2 * np.pi * root * 8 * t))
    bed = bed / (np.max(np.abs(bed)) + 1e-9)
    lfo = 0.7 + 0.3 * np.sin(2 * np.pi * 0.125 * t)
    mel = mel + bed * lfo * 0.06
    vox = np.zeros(n)
    if hook:
        hk = _vocal_hook(sr, n)
        vox[:] = hk * 0.5
    for x in (dr, bs, mel, vox):
        x[:] = x / (np.max(np.abs(x)) + 1e-9) * 0.85
    return {"drums": dr, "bass": bs, "melody": mel, "vocal": vox}


def get_tracks():
    if not TRACKS:
        TRACKS["A"] = build_track(SR, BPM, 24, seed=1, root=55.0, hook_bars=4)
        TRACKS["B"] = build_track(SR, BPM, 24, seed=2, root=49.0, hook_bars=0)
        TRACKS["Bhook"] = build_track(SR, BPM, 16, seed=2, root=49.0,
                                       hook_bars=16)
        TRACKS["break"] = build_breakdown(SR, BPM, 16, seed=5)
        TRACKS["vox"] = build_vocal_only(SR, BPM, 16, seed=6)
        TRACKS["stemsA"] = build_track_stems(SR, BPM, 24, seed=1, root=55.0,
                                             hook=True)
        TRACKS["stemsB"] = build_track_stems(SR, BPM, 24, seed=2, root=49.0,
                                             hook=False)
    return TRACKS


def bars(x, n):
    i = int(n * BAR_S * SR)
    return x[:i] if len(x) >= i else np.pad(x, (0, i - len(x)))


def last_bars(x, n):
    i = int(n * BAR_S * SR)
    return x[-i:] if len(x) >= i else x


def _echo_out_demo():
    """echo_out returns a + tail; b slams on the downbeat after a ends."""
    T = get_tracks()
    a = bars(T["A"], 8)
    b = bars(T["B"], 8)
    echoed = techniques.echo_out(a, SR, BPM)
    drop_at = len(a)
    total = max(len(echoed), drop_at + len(b))
    mix = np.zeros(total)
    mix[:len(echoed)] += echoed
    mix[drop_at:drop_at + len(b)] += b
    return mix


# ----------------------------------------------------------------------------
# Demo specs: technique -> (render_fn, handoff_s_fn, allowed_silence_fn)
# ----------------------------------------------------------------------------

def demo_specs():
    T = get_tracks()
    A, B = T["A"], T["B"]
    specs = {}

    def reg(name, fn, handoff=None, allowed=()):
        specs[name] = (fn, handoff, allowed)

    reg("hook_drop_handoff",
        lambda: techniques.hook_drop_handoff(
            last_bars(A, 8), bars(B, 8), SR, BAR_S),
        handoff=lambda m: 8 * BAR_S)
    reg("hard_cut",
        lambda: techniques.hard_cut(bars(A, 8), bars(B, 8), SR),
        handoff=lambda m: 8 * BAR_S)
    reg("brake_stop",
        lambda: techniques.brake_stop(bars(A, 8), SR, BPM) ,
        allowed=lambda m: [(8 * BAR_S - 0.05, 8 * BAR_S + 0.6)])
    reg("power_down",
        lambda: techniques.power_down(bars(A, 8), SR, BPM),
        allowed=lambda m: [(8 * BAR_S - 0.05, 8 * BAR_S + 1.2)])
    reg("backspin",
        lambda: techniques.backspin(bars(A, 8), bars(B, 4), SR, BPM),
        handoff=lambda m: 8 * BAR_S + BEAT_S,
        # the spin decays to -60 dBFS right before the slam — intentional
        allowed=lambda m: [(8 * BAR_S + BEAT_S - 0.3,
                            8 * BAR_S + BEAT_S + 0.05)])
    reg("vocal_punchline_snap",
        lambda: techniques.vocal_punchline_snap(
            bars(T["Bhook"], 4), bars(B, 4), SR, BPM),
        handoff=lambda m: 4 * BAR_S,
        allowed=lambda m: [(4 * BAR_S - 0.25, 4 * BAR_S)])
    reg("fake_drop",
        lambda: techniques.fake_drop(bars(A, 8), bars(B, 4), SR, BPM),
        allowed=lambda m: [(8 * BAR_S, 8 * BAR_S + 3 * BEAT_S)])
    reg("loop_roll_build",
        lambda: techniques.loop_roll_build(bars(A, 8), bars(B, 4), SR, BPM),
        handoff=lambda m: 8 * BAR_S)
    reg("stutter_transition",
        lambda: techniques.stutter_transition(
            bars(A, 4), T["Bhook"], SR, BPM, cue_t=0.1),
        handoff=lambda m: 4 * BAR_S)
    reg("vocal_chop_build",
        lambda: techniques.vocal_chop_build(
            bars(A, 8), bars(B, 4), SR, BAR_S,
            chop_t=4 * BAR_S, chop_len_s=1.0, build_bars=4),
        handoff=lambda m: 4 * BAR_S)
    reg("noise_echo_buildup",
        lambda: techniques.noise_echo_buildup(
            bars(A, 8), bars(B, 4), SR, BAR_S, BPM),
        handoff=lambda m: 8 * BAR_S)
    reg("hotcue_drop_swap",
        lambda: techniques.hotcue_drop_swap(
            bars(A, 8), bars(B, 8), SR, BPM),
        handoff=lambda m: 8 * BAR_S)
    reg("double_drop",
        lambda: techniques.double_drop(
            bars(A, 8), bars(B, 8), SR, BAR_S,
            drop_at_bar=4, drop_bars=4),
        handoff=lambda m: 4 * BAR_S)
    reg("loop_transition",
        lambda: techniques.loop_transition(
            bars(A, 8), bars(B, 16), SR, BAR_S),
        handoff=lambda m: 8 * BAR_S)
    reg("layered_fx_stack",
        lambda: techniques.layered_fx_stack(
            bars(A, 12), bars(B, 8), SR, BAR_S, BPM),
        handoff=lambda m: 12 * BAR_S)
    reg("reverb_freeze",
        lambda: techniques.reverb_freeze(
            bars(A, 8), bars(B, 8), SR, BAR_S, BPM),
        handoff=lambda m: 8 * BAR_S)
    reg("tempo_bridge",
        lambda: techniques.tempo_bridge(
            bars(A, 8), SR, 128.0, 132.0, BAR_S)[0])
    reg("drum_bridge",
        lambda: techniques.drum_bridge(
            bars(A, 16), bars(B, 8), SR, BAR_S),
        handoff=lambda m: 12 * BAR_S)
    reg("breakdown_transition",
        lambda: techniques.breakdown_transition(
            T["break"], bars(B, 8), SR, BAR_S,
            bpm_from=128.0, bpm_to=132.0),
        handoff=lambda m: 8 * BAR_S,
        # A's fade-out tail dips below the floor in its last ~150 ms
        allowed=lambda m: [(len(m) / SR - 0.5, len(m) / SR)])
    reg("genre_bridge",
        lambda: techniques.genre_bridge(
            bars(A, 8), bars(B, 8), SR, BAR_S, BPM,
            anchor_t=4 * BAR_S, anchor_len_s=2 * BAR_S, anchor_cycles=2),
        handoff=lambda m: 2 * 2 * BAR_S)
    reg("loop_juggle_replace",
        lambda: techniques.loop_juggle_replace(
            bars(A, 1), bars(B, 1), bars(B, 4), SR, BPM, cycles=2),
        handoff=lambda m: 2 * BAR_S)
    reg("acapella_overlay",
        lambda: techniques.acapella_overlay(
            bars(A, 16), T["vox"], SR, BAR_S))
    # Phase-2 techniques (GAP-A + T-039)
    reg("wordplay",
        lambda: techniques.wordplay(
            bars(T["vox"], 8), bars(T["Bhook"], 8), SR, BPM,
            a_word_t=1.0, b_word_t=0.5, word_len_s=0.5,
            exit="hard_cut"),
        handoff=lambda m: 1.0)
    reg("build_to_drop",
        lambda: techniques.build_to_drop(
            bars(A, 16), bars(B, 20), SR, BAR_S, build_bars=16),
        handoff=lambda m: 16 * BAR_S)
    reg("three_deck_layer",
        lambda: techniques.three_deck_layer(
            bars(A, 16), bars(B, 24), bars(A, 24), SR, BAR_S,
            swap_bar=12, glue_in_bars=12, glue_out_bars=8),
        handoff=lambda m: 12 * BAR_S)
    reg("beat_jump_transition",
        lambda: techniques.beat_jump_transition(
            bars(A, 8), T["B"], SR, BPM, BAR_S, cue_t=0.0,
            jump_beats=32, play_bars=8),
        handoff=lambda m: 8 * BAR_S)
    reg("pitch_play",
        lambda: techniques.pitch_play(
            bars(T["vox"], 8), bars(A, 8), SR, BAR_S,
            semitones=1, overlay_bars=8))
    reg("screwed_treatment",
        lambda: techniques.screwed_treatment(
            bars(A, 8), SR, bpm=BPM, rate=0.7, pitch_coupled=True,
            chop_every_beats=4, chop_repeats=2))
    # pre-existing engine techniques (regression demos)
    reg("echo_out",
        lambda: _echo_out_demo(),
        handoff=lambda m: 8 * BAR_S)
    reg("layered_emergence",
        lambda: techniques.layered_emergence(
            bars(A, 12), bars(B, 12), SR, BPM, BAR_S),
        handoff=lambda m: 12 * BAR_S - BEAT_S)
    reg("eq_blend",
        lambda: techniques.eq_blend(bars(A, 16), bars(B, 16), SR, BAR_S,
                                    blend_bars=16),
        handoff=lambda m: 8 * BAR_S)
    reg("bass_swap",
        lambda: techniques.bass_swap(bars(A, 4), bars(B, 4), SR),
        handoff=lambda m: 0.0)
    reg("filter_sweep",
        lambda: techniques.filter_sweep(bars(A, 16), bars(B, 16), SR, BAR_S),
        handoff=lambda m: 15 * BAR_S)
    reg("reverb_wash",
        lambda: techniques.reverb_wash(bars(A, 12), bars(B, 8), SR, BAR_S),
        handoff=lambda m: 6 * BAR_S)
    reg("echo_out_blend",
        lambda: techniques.echo_out_blend(
            bars(A, 8), bars(B, 12), SR, BPM, BAR_S),
        handoff=lambda m: 8 * BAR_S - BEAT_S)
    reg("riser_drop",
        lambda: techniques.riser_drop(bars(A, 8), bars(B, 4), SR, BAR_S),
        handoff=lambda m: 8 * BAR_S)
    return specs


# ----------------------------------------------------------------------------
# Pure-function checks (no audio)
# ----------------------------------------------------------------------------

def check_pure_functions():
    r = techniques.harmonic_mix("8A", "8A")
    assert r["compatible"] and r["move"] == "same key", r
    r = techniques.harmonic_mix("8A", "9A")
    assert r["compatible"] and "+1" in r["move"], r
    r = techniques.harmonic_mix("8A", "8B")
    assert r["compatible"] and "relative" in r["move"], r
    r = techniques.harmonic_mix("12A", "1A")
    assert r["compatible"], r  # wraparound
    r = techniques.harmonic_mix("8A", "3B")
    assert not r["compatible"], r

    s = techniques.select_technique({
        "bpm_delta_pct": 1.0, "half_double_ok": False,
        "camelot_distance": 0, "energy_delta": 0.0,
        "phrase_a": "outro", "vocal": "neither", "genre_pair": "same",
        "b_has_build": False, "a_has_breakdown": False,
        "iconic_vocal": None, "b_intro_bars": 16, "drop_pair_ok": False,
    })
    assert s["technique"] == "eq_blend", s

    s = techniques.select_technique({
        "bpm_delta_pct": 1.0, "half_double_ok": False,
        "camelot_distance": 0, "energy_delta": 0.0,
        "phrase_a": "outro", "vocal": "neither", "genre_pair": "same",
        "b_has_build": False, "a_has_breakdown": False,
        "iconic_vocal": "a", "b_intro_bars": 16, "drop_pair_ok": False,
    })
    assert s["technique"] == "hook_drop_handoff", s

    s = techniques.select_technique({
        "bpm_delta_pct": 12.0, "half_double_ok": False,
        "camelot_distance": 4, "energy_delta": 0.0,
        "phrase_a": "outro", "vocal": "neither", "genre_pair": "leap",
        "b_has_build": False, "a_has_breakdown": False,
        "iconic_vocal": None, "b_intro_bars": 16, "drop_pair_ok": False,
    })
    assert "eq_blend" in s["rejected"], s  # pruned by rejection rules
    assert s["technique"] in ("echo_out", "drum_bridge", "tempo_bridge",
                              "breakdown_transition", "hard_cut",
                              "genre_bridge"), s
    print("pure-function checks: harmonic_mix + select_technique OK")
    from engine.select import check_select
    check_select()


# ----------------------------------------------------------------------------
# Domain extension modules (FRAMEWORK.md §7)
# ----------------------------------------------------------------------------

def _demo_ctx():
    return {"SR": SR, "BPM": BPM, "BAR_S": BAR_S, "BEAT_S": BEAT_S,
            "get_tracks": get_tracks, "bars": bars, "last_bars": last_bars}


def load_ext_specs(specs):
    """Merge demo_specs(ctx) from any demos/ext_*.py domain module."""
    import importlib
    ctx = _demo_ctx()
    for modname in ("ext_dm", "ext_gap_struct", "ext_gap_rest",
                    "ext_performer", "ext_variants", "ext_web"):
        try:
            mod = importlib.import_module(modname)
        except ImportError:
            continue
        for name, entry in mod.demo_specs(ctx).items():
            assert name not in specs, f"demo name collision: {name}"
            specs[name] = entry
    return specs


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="demos/out")
    ap.add_argument("--only", default=None)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    check_pure_functions()

    specs = demo_specs()
    specs = load_ext_specs(specs)
    if args.only:
        specs = {k: v for k, v in specs.items() if k == args.only}
        assert specs, f"unknown technique {args.only}"

    from scipy.io import wavfile
    results = []
    for name, (fn, handoff_fn, allowed_fn) in specs.items():
        print(f"--- demo: {name} ---", flush=True)
        try:
            mix = np.asarray(fn(), dtype=np.float64)
        except Exception as e:
            print(f"    RENDER FAILED: {type(e).__name__}: {e}")
            results.append({"technique": name, "render_ok": False,
                            "error": f"{type(e).__name__}: {e}"})
            continue
        mix, applied = dsp.normalize_peak(mix, target_db=-1.0)
        out_path = os.path.join(args.out_dir, name + ".wav")
        stereo = np.stack([mix, mix], axis=1)
        wavfile.write(out_path, SR,
                      (np.clip(stereo, -1, 1) * 32767).astype(np.int16))
        handoff = handoff_fn(mix) if handoff_fn else None
        allowed = allowed_fn(mix) if allowed_fn else ()
        rep = verify.verify_clip(
            mix, SR, handoff_s=handoff, allowed_silence=allowed,
            plot_path=os.path.join(args.out_dir, name + "-verify.png"),
            clip_id=name)
        rep["technique"] = name
        rep["render_ok"] = True
        rep["normalize_db"] = round(applied, 2)
        rep["path"] = out_path
        results.append(rep)

    with open(os.path.join(args.out_dir, "verification.json"), "w") as f:
        json.dump(results, f, indent=2)

    ok = sum(1 for r in results
             if r.get("render_ok") and r.get("silence_ok")
             and r.get("headroom_ok"))
    print(f"\ndone: {ok}/{len(results)} demos rendered + verified clean.")
    for r in results:
        if not (r.get("render_ok") and r.get("silence_ok")
                and r.get("headroom_ok")):
            print(f"  NEEDS ATTENTION: {r['technique']}: "
                  f"{r.get('error', '')} gaps={r.get('silence_gaps_s')} "
                  f"headroom_ok={r.get('headroom_ok')}")


if __name__ == "__main__":
    main()
