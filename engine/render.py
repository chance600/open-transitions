"""
open-transitions engine — transition clip renderer.

Reads a track analysis file (BPM, bar length per track), cuts the configured
mix zones, applies the chosen technique, normalizes, and writes the clip.

Usage:
    python render.py --analysis analysis.json --audio-dir ./audio \
        --out-dir ./clips --plan plan.json

plan.json: list of transition specs, e.g.
    [{"id": "01-stay-high-to-anchor-point",
      "out": {"file": "stay.wav", "t0": 193.2, "bars": 32},
      "in":  {"file": "anchor.wav", "t0": 0.0, "bars": 32},
      "technique": "eq_blend", "technique_args": {"blend_bars": 32},
      "handoff_s": 33.2}]

No hardcoded local paths: everything comes from argv / the plan file.
"""

import argparse
import json
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy import signal as sig

from . import dsp, techniques, verify


TECHNIQUES = {
    "eq_blend": techniques.eq_blend,
    "echo_out": techniques.echo_out,
    "echo_out_blend": techniques.echo_out_blend,
    "layered_emergence": techniques.layered_emergence,
    "filter_sweep": techniques.filter_sweep,
    "reverb_wash": techniques.reverb_wash,
    "riser_drop": techniques.riser_drop,
    "bass_swap": techniques.bass_swap,
    "hook_drop_handoff": techniques.hook_drop_handoff,
    "hard_cut": techniques.hard_cut,
    "brake_stop": techniques.brake_stop,
    "power_down": techniques.power_down,
    "backspin": techniques.backspin,
    "vocal_punchline_snap": techniques.vocal_punchline_snap,
    "fake_drop": techniques.fake_drop,
    "loop_roll_build": techniques.loop_roll_build,
    "stutter_transition": techniques.stutter_transition,
    "vocal_chop_build": techniques.vocal_chop_build,
    "noise_echo_buildup": techniques.noise_echo_buildup,
    "hotcue_drop_swap": techniques.hotcue_drop_swap,
    "double_drop": techniques.double_drop,
    "loop_transition": techniques.loop_transition,
    "layered_fx_stack": techniques.layered_fx_stack,
    "reverb_freeze": techniques.reverb_freeze,
    "tempo_bridge": techniques.tempo_bridge,
    "drum_bridge": techniques.drum_bridge,
    "breakdown_transition": techniques.breakdown_transition,
    "genre_bridge": techniques.genre_bridge,
    "loop_juggle_replace": techniques.loop_juggle_replace,
    "acapella_overlay": techniques.acapella_overlay,
    "wordplay": techniques.wordplay,
    "build_to_drop": techniques.build_to_drop,
    "three_deck_layer": techniques.three_deck_layer,
    "beat_jump_transition": techniques.beat_jump_transition,
    "pitch_play": techniques.pitch_play,
    "screwed_treatment": techniques.screwed_treatment,
}

# Domain modules (FRAMEWORK.md §7): merge their TECHNIQUE_FUNCS so the
# plan-file renderer sees the full library. Import failures are ignored —
# a domain module simply isn't present yet.
import importlib as _importlib

for _modname in ("dm_techniques", "gap_struct", "gap_rest", "performer",
                 "web_techniques", "compounds", "hw_techniques",
                 "genre_techniques"):
    try:
        _m = _importlib.import_module(f".{_modname}", __package__)
    except ImportError:
        continue
    for _tid, _fn in getattr(_m, "TECHNIQUE_FUNCS", {}).items():
        if _tid in TECHNIQUES:
            raise ValueError(f"technique id collision: {_tid}")
        TECHNIQUES[_tid] = _fn


def load_mono(path):
    sr, x = wavfile.read(path)
    orig_dtype = np.asarray(x).dtype
    x = np.asarray(x, dtype=np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    if np.issubdtype(orig_dtype, np.integer):
        # int16 stereo was silently skipping this (dtype became float64
        # after the channel mean, so the integer check failed) — the whole
        # mix then ran at x32768 scale. Normalization hid it, but every
        # diagnostic print was nonsense. Normalize off the ORIGINAL dtype.
        x = x / float(np.iinfo(orig_dtype).max)
    return sr, x


def cut(x, sr, t0, seconds):
    i0 = int(t0 * sr)
    i1 = int((t0 + seconds) * sr)
    seg = x[i0:i1]
    if len(seg) < i1 - i0:
        seg = np.pad(seg, (0, i1 - i0 - len(seg)))
    return seg


def to_stereo_44k(x, sr_in, sr_out=44100):
    """Dual-mono stereo at 44.1 kHz for delivery."""
    if sr_in != sr_out:
        n_out = int(len(x) * sr_out / sr_in)
        x = sig.resample_poly(x, sr_out, sr_in)
        # resample_poly with up/down may not hit exact length; trim/pad
        if len(x) < n_out:
            x = np.pad(x, (0, n_out - len(x)))
        x = x[:n_out]
    stereo = np.stack([x, x], axis=1)
    # int16
    stereo = np.clip(stereo, -1.0, 1.0)
    return (stereo * 32767).astype(np.int16)


def render_transition(spec, analysis, audio_dir):
    tid = spec["id"]
    print(f"--- {tid} [{spec['technique']}] ---", flush=True)

    out_f = os.path.join(audio_dir, spec["out"]["file"])
    in_f = os.path.join(audio_dir, spec["in"]["file"])
    sr_o, a_full = load_mono(out_f)
    sr_i, b_full = load_mono(in_f)
    assert sr_o == sr_i, "sample rate mismatch between tracks"
    sr = sr_o

    a = cut(a_full, sr, spec["out"]["t0"], spec["out"]["bars"] * spec["out"]["bar_s"])
    b = cut(b_full, sr, spec["in"]["t0"], spec["in"]["bars"] * spec["in"]["bar_s"])
    print(f"    a: {len(a)/sr:.1f}s  b: {len(b)/sr:.1f}s @ {sr} Hz", flush=True)

    fn = TECHNIQUES[spec["technique"]]
    args = dict(spec.get("technique_args", {}))
    # inject common timing args for techniques that accept them
    import inspect as _inspect
    params = _inspect.signature(fn).parameters
    if "bar_s" in params:
        args.setdefault("bar_s", spec["out"]["bar_s"])
    if "bpm" in params:
        args.setdefault("bpm", spec["out"]["bpm"])

    mix = fn(a, b, sr, **args) if spec["technique"] != "echo_out" else None

    if spec["technique"] == "echo_out":
        # echo_out returns a + tail; overlay b starting at the drop point
        echoed = fn(a, sr, **args)
        drop_at = len(a)  # b slams on the next downbeat after a ends
        total = max(len(echoed), drop_at + len(b))
        mix = np.zeros(total)
        mix[:len(echoed)] += echoed
        mix[drop_at:drop_at + len(b)] += b

    # Normalize to -1 dBFS peak (sketch listening level, no clipping)
    mix, applied = dsp.normalize_peak(mix, target_db=-1.0)
    print(f"    rendered {len(mix)/sr:.1f}s, normalize {applied:+.1f} dB", flush=True)
    return sr, mix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--audio-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--skip-verify", action="store_true")
    args = ap.parse_args()

    with open(args.analysis) as f:
        analysis = json.load(f)
    with open(args.plan) as f:
        plan = json.load(f)

    os.makedirs(args.out_dir, exist_ok=True)
    results = []
    for spec in plan:
        sr, mix = render_transition(spec, analysis, args.audio_dir)
        out_path = os.path.join(args.out_dir, spec["id"] + ".wav")
        wavfile.write(out_path, 44100, to_stereo_44k(mix, sr))
        print(f"    wrote {out_path}", flush=True)

        rep = {"id": spec["id"], "path": out_path,
               "duration_s": round(len(mix) / sr, 2)}
        if not args.skip_verify:
            handoff = spec.get("handoff_s")
            rep["verification"] = verify.verify_clip(
                mix, sr, handoff_s=handoff,
                plot_path=os.path.join(args.out_dir, spec["id"] + "-verify.png"),
                clip_id=spec["id"])
        results.append(rep)

    with open(os.path.join(args.out_dir, "verification.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("done.", flush=True)


if __name__ == "__main__":
    main()
