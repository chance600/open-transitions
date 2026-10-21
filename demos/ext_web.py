"""
open-transitions — demo specs for the web-mined domain module
(FRAMEWORK.md §7).

Registers demos for engine/web_techniques.py (WEB-01..WEB-10, mined
2026-10-21). Merged automatically by demos/make_demos.py
(load_ext_specs). All material is the suite's synthesized sketch audio
(ctx tracks) — no copyrighted audio.
"""

import numpy as np

from engine import web_techniques as web


def demo_specs(ctx):
    SR, BPM, BAR_S, BEAT_S = ctx["SR"], ctx["BPM"], ctx["BAR_S"], ctx["BEAT_S"]
    get_tracks, bars, last_bars = (ctx["get_tracks"], ctx["bars"],
                                   ctx["last_bars"])
    T = get_tracks()
    A, B = T["A"], T["B"]

    specs = {}

    # WEB-01 spiral_echo: A's last 8 bars play dry; the final 3/4-beat
    # fragment spirals up (+2 st/repeat) across B's 2-bar fade-in.
    specs["spiral_echo"] = (
        lambda: web.spiral_echo(last_bars(A, 8), bars(B, 8), SR, BPM, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-02 flanger_sweep: the whole 8-bar A segment is the sweep zone
    # (2 cycles, jet depth); B enters dry on the downbeat.
    specs["flanger_sweep"] = (
        lambda: web.flanger_sweep(bars(A, 8), bars(B, 8), SR, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-03 reverse_roll: A's last 2 bars are the reversed-tile roll
    # (1 -> 1/2 -> 1/4 -> 1/8 beat); B releases at the downbeat.
    specs["reverse_roll"] = (
        lambda: web.reverse_roll(last_bars(A, 8), bars(B, 8), SR, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-04 crush_degrade: bars 5-8 of A crush 16 -> 5 bits with the
    # rate fold; B crossfades in clean across the final bar, so the
    # handoff center sits at 7.5 bars.
    specs["crush_degrade"] = (
        lambda: web.crush_degrade(bars(A, 8), bars(B, 8), SR, BAR_S),
        lambda m: 7.5 * BAR_S,
        None,
    )

    # WEB-05 shepard_riser: the endless-rise layer rides A's last 8
    # bars at -9 dB and cuts dead; B drops at the seam.
    specs["shepard_riser"] = (
        lambda: web.shepard_riser(bars(A, 8), bars(B, 4), SR, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-06 granular_freeze: A freezes at bar 4 into a 4-bar grain
    # cloud (150 ms capture, 70 ms grains); B fades up inside the cloud
    # and owns the mix from bar 8.
    specs["granular_freeze"] = (
        lambda: web.granular_freeze(bars(A, 8), bars(B, 8), SR, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-07 helix_catch: A's final beat (of the 8-bar segment) is
    # caught and looped for 2 bars while its pitch ramps +12 st; the
    # release lands B at natural pitch — handoff = 7 bars + 3 beats
    # of dry A, then the 2-bar hold.
    specs["helix_catch"] = (
        lambda: web.helix_catch(last_bars(A, 8), bars(B, 8), SR, BPM,
                                BAR_S),
        lambda m: 10 * BAR_S - BEAT_S,
        None,
    )

    # WEB-08 beatslicer_shuffle: A plays 7 bars clean; its final bar
    # is re-dealt in the stride permutation (with BUZZ); B releases
    # on the downbeat at bar 8.
    specs["beatslicer_shuffle"] = (
        lambda: web.beatslicer_shuffle(bars(A, 8), bars(B, 8), SR,
                                       BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-09 downlifter_exit: A hands to B at bar 8 under a 1-bar
    # descending sweep (12 kHz -> 300 Hz) centered on the seam.
    specs["downlifter_exit"] = (
        lambda: web.downlifter_exit(bars(A, 8), bars(B, 8), SR,
                                     BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-10 shimmer_wash: A's last 4 bars feed the +12 st shimmer
    # layer; A ends at bar 8 and B fades in under the climbing tail.
    specs["shimmer_wash"] = (
        lambda: web.shimmer_wash(bars(A, 8), bars(B, 8), SR, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    return specs
