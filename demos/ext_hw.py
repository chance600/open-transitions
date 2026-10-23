"""
open-transitions — demo specs for the hardware/software domain
module (FRAMEWORK.md §7).

Registers demos for engine/hw_techniques.py (WEB-22..WEB-29,
Phase 26 expansion tranche 5: Mixxx / djay / VirtualDJ / SP-404MKII
/ Xone:96 / DJM-V10 documentation mining, 2026-10-23). Merged
automatically by demos/make_demos.py (load_ext_specs). All material
is the suite's synthesized sketch audio (ctx tracks) — no
copyrighted audio.

Sketch caveat (honest): the harness synthesizes stemsB WITHOUT a
hook (hook=False), so stemsB["vocal"] is digital silence. The
stem_swap_replace demo swaps the DRUMS stem, which is fully audible
on both sides; vocal/melody swaps would rest on the same silence
the stem_element_crossfade demo already documents.
"""

from engine import hw_techniques as hw


def demo_specs(ctx):
    SR, BPM, BAR_S = ctx["SR"], ctx["BPM"], ctx["BAR_S"]
    get_tracks, bars, last_bars = (ctx["get_tracks"], ctx["bars"],
                                   ctx["last_bars"])
    T = get_tracks()
    A, B = T["A"], T["B"]
    sA, sB = T["stemsA"], T["stemsB"]

    specs = {}

    # WEB-22 pre_filtered_echo: A's last 8 bars dry at full level;
    # the final beat is thrown through the 300 Hz send filter and
    # the bass-less repeats ring over B's entrance.
    specs["pre_filtered_echo"] = (
        lambda: hw.pre_filtered_echo(last_bars(A, 8), bars(B, 8),
                                     SR, BPM, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-23 notch_carve_sweep: the notch log-ramps 60 Hz -> 15 kHz
    # across A's last 4 bars; B crossfades over the final bar, so
    # the handoff centre sits at 7.5 bars.
    specs["notch_carve_sweep"] = (
        lambda: hw.notch_carve_sweep(bars(A, 8), bars(B, 8),
                                     SR, BPM, BAR_S),
        lambda m: 7.5 * BAR_S,
        None,
    )

    # WEB-24 phaser_sweep: A's last 4 bars run through the allpass
    # cascade (1-bar LFO); B crossfades over the final bar.
    specs["phaser_sweep"] = (
        lambda: hw.phaser_sweep(bars(A, 8), bars(B, 8), SR, BPM,
                                BAR_S),
        lambda m: 7.5 * BAR_S,
        None,
    )

    # WEB-25 stem_swap_replace: B plays 4 bars, then A's captured
    # 2-bar drums loop replaces B's drums for 8 bars while the rest
    # of B continues; B's own drums return for the 4-bar tail.
    specs["stem_swap_replace"] = (
        lambda: hw.stem_swap_replace(sA, sB, SR, BAR_S),
        lambda m: 4 * BAR_S,
        None,
    )

    # WEB-26 djfx_microloop: A's final 2 bars are replaced by the
    # 120 ms grain sweeping +1 -> -1 (reverse mode); B enters at
    # the 8-bar line.
    specs["djfx_microloop"] = (
        lambda: hw.djfx_microloop(last_bars(A, 8), bars(B, 8),
                                  SR, BPM, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-27 cyclic_speed_dip: A's first 8 bars dry, final 8 bars
    # dipped (period 4 beats, depth 0.45) — the dipped half
    # lengthens by 1/(1-0.45/2) = 1.29x to ~10.32 bars, and B
    # crossfades over the last bar of it: handoff centre =
    # 8 + 10.32 - 0.5 = 17.82 bars.
    specs["cyclic_speed_dip"] = (
        lambda: hw.cyclic_speed_dip(last_bars(A, 16), bars(B, 8),
                                    SR, BPM, BAR_S),
        lambda m: (8 + 8 / (1 - 0.45 / 2) - 0.5) * BAR_S,
        None,
    )

    # WEB-28 pattern_gate_slicer: A's last 4 bars run under the
    # offbeat 16-step pattern (16th grid, slash mode); B enters at
    # the 8-bar line with a 2-beat head fade. Staged on last_bars
    # (the standard exit-demo staging): the first-8-bars sketch
    # decays into a sparse tail (-45 dB RMS) where the pattern's
    # 0.15 steps would push isolated windows under the -60 dBFS
    # floor — sketch sparseness, not silence in the move.
    specs["pattern_gate_slicer"] = (
        lambda: hw.pattern_gate_slicer(last_bars(A, 8), bars(B, 8),
                                       SR, BPM, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-29 sideband_comb_filter: A's last 4 bars dissolve dry ->
    # comb skeleton; B crossfades over the final bar.
    specs["sideband_comb_filter"] = (
        lambda: hw.sideband_comb_filter(bars(A, 8), bars(B, 8),
                                        SR, BPM, BAR_S),
        lambda m: 7.5 * BAR_S,
        None,
    )

    return specs
