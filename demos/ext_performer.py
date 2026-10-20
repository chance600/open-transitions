"""
open-transitions — performer-lane demo registrations (FRAMEWORK.md §7).

Merged by demos/make_demos.py's load_ext_specs(). Each entry is
(name -> (render_fn, handoff_fn, allowed_fn)) in the core format.
No demo needs an allowed-silence declaration: every gesture here plays
OVER a continuous bed by design, so the verify gate runs unweakened.
"""

import numpy as np

from engine import performer


def demo_specs(ctx):
    SR, BPM = ctx["SR"], ctx["BPM"]
    BAR_S, BEAT_S = ctx["BAR_S"], ctx["BEAT_S"]
    get_tracks, bars, last_bars = (ctx["get_tracks"], ctx["bars"],
                                   ctx["last_bars"])
    T = get_tracks()
    A, B = T["A"], T["B"]
    specs = {}

    # GAP-14: gesture over A's final beat of the 8-bar segment, hard cut,
    # B plays full — handoff is the cut at bar 8's end.
    specs["scratch_in"] = (
        lambda: performer.scratch_in(bars(A, 8), bars(B, 8), SR, BPM),
        lambda m: 8 * BAR_S,
        None,
    )

    # GAP-15: overlapping 8-bar segments; chops in bar 1, A fully out by
    # bar 5 — handoff is the bar-5 boundary (4 bars in).
    specs["rhythmic_fader_chops"] = (
        lambda: performer.rhythmic_fader_chops(
            bars(A, 8), bars(B, 8), SR, BPM, BAR_S),
        lambda m: 4 * BAR_S,
        None,
    )

    # GAP-16: 16-bar bed; riser fires at bar 8, one-shot at bar 12 —
    # handoff is the bass swap on bar 9 (8 bars in).
    specs["spare_deck_element_firing"] = (
        lambda: performer.spare_deck_element_firing(
            bars(A, 16), bars(B, 16), SR, BAR_S, BPM),
        lambda m: 8 * BAR_S,
        None,
    )

    def _riser_demo():
        # T-035 overlay: A's final 8-bar phrase ends exactly on the
        # drop point. The overlay returns phrase+riser (hard-cut at the
        # drop) + a 2-beat downlifter tail; per the bank's exit rule the
        # tail is overlapped onto beats 1-2 of B's drop bar.
        pre = last_bars(A, 8)
        raw = performer.riser_ducking_overlay(pre, SR, BAR_S, BPM,
                                              pre_drop_bars=8)
        body, tail = raw[:len(pre)], raw[len(pre):]
        drop = bars(B, 8).copy()
        k = min(len(tail), len(drop))
        drop[:k] += tail[:k]
        return np.concatenate([body, drop])

    specs["riser_ducking_overlay"] = (
        _riser_demo,
        lambda m: 8 * BAR_S,
        None,
    )
    return specs
