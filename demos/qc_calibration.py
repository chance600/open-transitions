#!/usr/bin/env python3
"""QC calibration — does engine/qc.py rank renders the way his ears did?

Runs the cleanliness suite on the six Set-1 (batch-05-setlist) renders
that carry first-person verdicts from 2026-10-20:

  link02 v2 reverb wash   "extremely clean"          -> must rank top
  link04 v1 bass swap     "cleanest so far"          -> high
  link03 v2 fader chops   partial / "not as good"    -> mid
  link01 v1 bass swap     "not very clean"           -> low
  link01 v2 filter sweep  "doesn't fade cleanly"     -> low
  link02 v1 bass swap     "not very clean"           -> low

Sides are reconstructed with the builds' OWN machinery — this matters:
the original harness cut excerpts with naive (bar-1) x bar_len slicing
of ffmpeg-decoded audio, while every build decoded with librosa
(B1.load44) and cut on the beat-snapped detected grid
(B1.cut_grid_aligned over analysis beat_times), then stretched and
kick-aligned the incoming side. The naive slices sat up to a beat away
from the audio actually rendered, which scrambled every
content-sensitive check (phantom grid offsets, vocal "collisions" on
by-construction sequential swaps). Here:

  v1 links   — links2's exact path: A cut 16 bars grid-aligned; B cut
               with spare bars, B1.stretch_to, L2.align_b_to_a_spare.
  v2 links   — build_setlist_v2's prep_b (copied verbatim below):
               spare cut + stretch + align_long.
  link03 v2  — its build script's exact segment recipe (naive seg()
               cuts, techniques.tempo_bridge ramp + gain comp, the
               four-stab chop bar), B = kombucha bars 105-120.

Placed sides are gain-matched to the render via the A-solo head (the
A head is unprocessed in all six builds; renders are peak-normalized).
Grid offsets in the specs come from the build records (all six builds
aligned B to A's grid, grid_shift_ms = 0.0); link03 is a tempo bridge
— its sides' grids are not commensurable, so its spec omits grid
offsets and beat_phase rests on the B-tail audio check.

Writes demos/out/qc-calibration.json and prints the ranking table.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
WS = os.path.expanduser("~/workspace/goals/dj-career-launch-alec")
WORK = os.path.join(WS, "mixing-lane/work")
AUDIO = os.path.join(WORK, "sweep-audio")
RENDERS = os.path.join(WS, "mixing-lane/blends/batch-05-setlist")
sys.path.insert(0, REPO)
sys.path.insert(0, WORK)

from engine import qc, techniques               # noqa: E402
from engine.render import load_mono             # noqa: E402
import build_setlist_links as B1                # noqa: E402
import build_setlist_links2 as L2               # noqa: E402

SR = 44100
AN = json.load(open(os.path.join(WORK, "setlist-analysis2.json")))
FILES = {"izindlu": "izindlu.mp3", "stay_high": "stay_high.wav",
         "rapture_piii": "rapture_piii.mp3",
         "kombucha_1": "kombucha_1.mp3", "lifetime": "lifetime.mp3"}


def load(slug):
    _, x = B1.load44(os.path.join(AUDIO, FILES[slug]))
    return x


def place(seg, offset_s, total):
    out = np.zeros(total)
    i0 = int(round(offset_s * SR))
    n = min(len(seg), total - i0)
    if n > 0:
        out[i0:i0 + n] = seg[:n]
    return out


# --- build_setlist_v2.prep_b / align_long, verbatim -------------------------

def align_long(b_long, sr, a_bar_len, max_shift_s=0.10):
    """align_b_to_a_spare logic, but returns the FULL aligned buffer
    (v2 builds need B bars past the 16-bar handoff for the solo tail)."""
    probe = b_long[:int(2 * a_bar_len * sr)]
    kicks = B1.lowband_kick_times(probe, sr)
    if len(kicks) < 2:
        print("    WARN: no kick grid in B probe; no shift applied",
              flush=True)
        return b_long, 0.0
    beat = a_bar_len / 4.0
    shift_s = round(kicks[0] / beat) * beat - kicks[0]
    if abs(shift_s) > max_shift_s:
        print(f"    WARN: kick shift {shift_s * 1000:.0f}ms > cap; "
              f"distrusted, no shift applied", flush=True)
        return b_long, 0.0
    shift_n = int(round(shift_s * sr))
    if shift_n < 0:
        b2 = b_long[-shift_n:]
    elif shift_n > 0:
        b2 = np.concatenate([np.zeros(shift_n), b_long])
    else:
        b2 = b_long
    return b2, shift_s


def prep_b(b_slug, b_start, a_an, want_bars):
    """Cut B with spare bars, stretch to A's tempo, grid-align.
    Returns (aligned_long_buffer, rate, shift_s) at A's bar grid."""
    b_an = AN[b_slug]
    b_full = load(b_slug)
    rate_pre = b_an["bpm"] / a_an["bpm"]
    cut_bars = int(np.ceil(want_bars / rate_pre)) + 2
    b_ex, _ = B1.cut_grid_aligned(b_full, SR, B1.span_t0(b_an, b_start),
                                  cut_bars, b_an["bar_len_s"],
                                  b_an["beat_times"])
    b_ex, rate = B1.stretch_to(b_ex, SR, b_an["bpm"], a_an["bpm"])
    b_al, shift = align_long(b_ex, SR, a_an["bar_len_s"])
    return b_al, rate, shift


# --- per-build side reconstruction ------------------------------------------

def v1_sides(a_slug, a_start, b_slug, b_start):
    """links2 bass_swap path: A 16 bars grid-aligned; B spare-cut,
    stretched to A's tempo, kick-aligned; B enters at the 8-bar
    handoff. Returns (a_ex, b_ex, b_off_s, align_shift_s)."""
    a_an, b_an = AN[a_slug], AN[b_slug]
    a_bar = a_an["bar_len_s"]
    a_ex, _ = B1.cut_grid_aligned(load(a_slug), SR,
                                  B1.span_t0(a_an, a_start), 16, a_bar,
                                  a_an["beat_times"])
    rate_pre = b_an["bpm"] / a_an["bpm"]
    cut_bars = int(np.ceil(16 / rate_pre)) + 2
    b_long, _ = B1.cut_grid_aligned(load(b_slug), SR,
                                    B1.span_t0(b_an, b_start), cut_bars,
                                    b_an["bar_len_s"], b_an["beat_times"])
    b_st, _rate = B1.stretch_to(b_long, SR, b_an["bpm"], a_an["bpm"])
    n16 = int(round(16 * a_bar * SR))
    b_ex, shift = L2.align_b_to_a_spare(b_st, SR, a_bar, n16)
    return a_ex, b_ex, 8 * a_bar, shift


def v2_link01_sides():
    a_an = AN["izindlu"]
    bar = a_an["bar_len_s"]
    a_long, _ = B1.cut_grid_aligned(load("izindlu"), SR,
                                    B1.span_t0(a_an, 81), 24, bar,
                                    a_an["beat_times"])
    b_al, _rate, shift = prep_b("stay_high", 33, a_an, 24)
    return a_long, b_al[:int(round(24 * bar * SR))], 8 * bar, shift


def v2_link02_sides():
    a_an = AN["stay_high"]
    bar = a_an["bar_len_s"]
    a_seg, _ = B1.cut_grid_aligned(load("stay_high"), SR,
                                   B1.span_t0(a_an, 25), 24, bar,
                                   a_an["beat_times"])
    b_al, _rate, shift = prep_b("rapture_piii", 177, a_an, 16)
    return a_seg, b_al[:int(round(16 * bar * SR))], 18 * bar, shift


def link03_sides():
    """build_setlink03_v2.py's exact recipe. Returns
    (a_placed_seg, b_seg, t_b_entry, t_ramp_start)."""
    a = load("rapture_piii")
    b = load("kombucha_1")
    bpm_a, bpm_b = 117.5, 123.0
    bar_a, bar_b = 240.0 / bpm_a, 240.0 / bpm_b

    def seg(x, bar_start_1idx, n_bars, bar_len):
        i0 = int(round((bar_start_1idx - 1) * bar_len * SR))
        i1 = int(round((bar_start_1idx - 1 + n_bars) * bar_len * SR))
        return x[i0:i1]

    a_solo = seg(a, 177, 8, bar_a)
    a_ramp_in = seg(a, 185, 8, bar_a)
    a_ramped, _ = techniques.tempo_bridge(a_ramp_in, SR, bpm_a, bpm_b,
                                          bar_a, ramp_bars=8,
                                          method="ramp")
    comp = float(np.sqrt(np.mean(a_ramp_in ** 2))
                 / np.sqrt(np.mean(a_ramped ** 2)))
    a_ramped = a_ramped * comp
    beat_b = 60.0 / bpm_b
    hit = seg(a, 193, 1, bar_a)[:int(beat_b * SR)]
    beat_n = int(round(beat_b * SR))
    stab = np.zeros(beat_n)
    n_hit = min(len(hit), beat_n)
    stab[:n_hit] = hit[:n_hit]
    env = np.ones(beat_n)
    f0, f1 = int(0.55 * beat_n), int(0.78 * beat_n)
    env[f0:f1] = 0.5 * (1 + np.cos(np.linspace(0, np.pi, f1 - f0)))
    env[f1:] = 0.0
    chop_bar = np.concatenate([stab * env] * 4)
    a_seg = np.concatenate([a_solo, a_ramped, chop_bar])
    b_seg = seg(b, 105, 16, bar_b)
    t_ramp = len(a_solo) / SR
    t_b = (len(a_solo) + len(a_ramped) + len(chop_bar)) / SR
    return a_seg, b_seg, t_b, t_ramp


# --- cases --------------------------------------------------------------------

def _spec(a_slug, w_bars, lows, grids=True):
    an = AN[a_slug]
    bar = an["bar_len_s"]
    spec = {"window_s": (w_bars[0] * bar, w_bars[1] * bar),
            "bpm": an["bpm"], "bar_s": bar, "beat_offset_s": 0.0,
            "lows_contract": lows}
    if grids:
        spec["a_grid_offset_s"] = 0.0
        spec["b_grid_offset_s"] = 0.0
    return spec


def case_link02_v2():
    a, b, off, shift = v2_link02_sides()
    return a, b, off, shift, _spec("stay_high", (16, 24), "free")


def case_link04_v1():
    a, b, off, shift = v1_sides("kombucha_1", 105, "lifetime", 33)
    return a, b, off, shift, _spec("kombucha_1", (8, 16), "continuous")


def case_link03_v2():
    a, b, t_b, t_ramp = link03_sides()
    bar_b = 240.0 / 123.0
    spec = {"window_s": (t_ramp, t_b), "bpm": 123.0, "bar_s": bar_b,
            "beat_offset_s": t_b % bar_b, "lows_contract": "free"}
    return a, b, t_b, 0.0, spec


def case_link01_v1():
    a, b, off, shift = v1_sides("izindlu", 89, "stay_high", 33)
    return a, b, off, shift, _spec("izindlu", (8, 16), "continuous")


def case_link01_v2():
    a, b, off, shift = v2_link01_sides()
    return a, b, off, shift, _spec("izindlu", (8, 24), "free")


def case_link02_v1():
    a, b, off, shift = v1_sides("stay_high", 33, "rapture_piii", 177)
    return a, b, off, shift, _spec("stay_high", (8, 16), "continuous")


CASES = [
    dict(id="link02-v2-reverb-wash", tier="top",
         his="extremely clean",
         render="setlink02-stay-high-x-rapture-piii-eq_blend-v2.wav",
         build=case_link02_v2),
    dict(id="link04-v1-bass-swap", tier="high",
         his="cleanest so far (accepted)",
         render="setlink04-kombucha-x-lifetime-bass_swap.wav",
         build=case_link04_v1),
    dict(id="link03-v2-fader-chops", tier="mid",
         his="partial — effect present, below reference standard",
         render="setlink03-rapture-piii-x-kombucha-rhythmic_fader_chops"
                "-v2.wav",
         build=case_link03_v2),
    dict(id="link01-v1-bass-swap", tier="low",
         his="not very clean",
         render="setlink01-izindlu-x-stay-high-bass_swap.wav",
         build=case_link01_v1),
    dict(id="link01-v2-filter-sweep", tier="low",
         his="doesn't fade cleanly into stay high",
         render="setlink01-izindlu-x-stay-high-eq_blend-v2.wav",
         build=case_link01_v2),
    dict(id="link02-v1-bass-swap", tier="low",
         his="not very clean — slower fade needed",
         render="setlink02-stay-high-x-rapture-piii-bass_swap.wav",
         build=case_link02_v1),
]


def run_case(case):
    sr, render = load_mono(os.path.join(RENDERS, case["render"]))
    assert sr == SR
    total = len(render)
    a_seg, b_seg, b_off, shift, spec = case["build"]()
    a = place(a_seg, 0.0, total)
    b = place(b_seg, b_off, total)
    # gain-match sides to the render via the (unprocessed) A-solo head
    head = int(4 * spec["bar_s"] * SR)
    g = float(np.sqrt(np.mean(render[:head] ** 2))
              / (np.sqrt(np.mean(a[:head] ** 2)) + 1e-12))
    a, b = a * g, b * g
    print(f"=== {case['id']} (his: {case['his']}) "
          f"b_off {b_off:.2f} align_shift {shift * 1000:+.0f} ms "
          f"gain {g:.3f}", flush=True)
    rec = qc.qc_render(render, SR, spec, a, b, clip_id=case["id"])
    rec["his_verdict"] = case["his"]
    rec["his_tier"] = case["tier"]
    rec["alignment"] = {"a_offset_s": 0.0, "b_offset_s": round(b_off, 3),
                        "b_align_shift_ms": round(shift * 1000, 1),
                        "side_gain": round(g, 3),
                        "method": "build-machinery replication "
                                  "(grid-aligned cuts, builder stretch "
                                  "+ kick align)"}
    return rec


def main():
    receipts = [run_case(c) for c in CASES]
    order = {"top": 0, "high": 1, "mid": 2, "low": 3}
    ranked = sorted(receipts,
                    key=lambda r: -(r["cleanliness_score"] or -1))
    print("\n=== QC ranking vs his ears ===")
    print(f"{'render':28s} {'tier':5s} {'QC':>6s}  verdict  checks")
    for r in ranked:
        per = " ".join(
            f"{c['name'].replace('_collision', '').replace('_hygiene', '')}"
            f"={c['score']:.0f}" if c["score"] is not None
            else f"{c['name']}=n/a" for c in r["checks"])
        print(f"{r['clip']:28s} {r['his_tier']:5s} "
              f"{r['cleanliness_score']:6.1f}  {r['verdict']:7s} {per}")
    tiers = [order[r["his_tier"]] for r in ranked]
    inversions = sum(1 for i in range(len(tiers))
                     for j in range(i + 1, len(tiers))
                     if tiers[i] > tiers[j])
    print(f"\ntier inversions vs his ranking: {inversions} "
          f"(0 = perfect tier order)")
    out = os.path.join(HERE, "out", "qc-calibration.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(receipts, f, indent=2)
    print(f"receipts -> {out}")


if __name__ == "__main__":
    main()
