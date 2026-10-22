"""
open-transitions — demo registrations for the gap-rest domain module
(engine/gap_rest.py): GAP-01/02/04/05/07/17 + the Zabiela PERF moves +
the Phase 22 performer pair (transform gate loop, dual-loop composite).

Merged automatically by demos/make_demos.py (FRAMEWORK.md §7). Each demo
renders on the deterministic sketch tracks and must pass
engine.verify.verify_clip — allowed is () throughout except the
transform gate, whose gate window is declared intentional silence.
"""

from engine import gap_rest as gr


def demo_specs(ctx):
    SR = ctx["SR"]
    BPM = ctx["BPM"]
    BAR_S = ctx["BAR_S"]
    BEAT_S = ctx["BEAT_S"]
    get_tracks = ctx["get_tracks"]
    bars = ctx["bars"]
    last_bars = ctx["last_bars"]  # noqa: F841 (ctx contract; kept for parity)

    T = get_tracks()
    A, B = T["A"], T["B"]
    specs = {}

    def reg(name, fn, handoff=None, allowed=()):
        specs[name] = (fn, handoff, allowed)

    hit_t = 4 * BAR_S
    reg("sample_connection",
        lambda: gr.sample_connection(
            bars(A, 8), bars(B, 8), SR, BPM, hit_t, hit_len_s=0.5),
        handoff=lambda m: hit_t + 2 * 0.5)

    reg("loop_tightening_build",
        lambda: gr.loop_tightening_build(
            bars(T["vox"], 4), bars(B, 8), SR, BAR_S, BPM))

    reg("polyrhythmic_loops",
        lambda: gr.polyrhythmic_loops(
            bars(A, 8), bars(B, 8), SR, BAR_S),
        handoff=lambda m: 4 * BAR_S + 3 * BAR_S)

    reg("slip_mode_flourish",
        lambda: gr.slip_mode_flourish(
            bars(A, 8), SR, BPM, flourish_beats=1.0))

    reg("premade_tempo_bridge_edit",
        lambda: gr.premade_tempo_bridge_edit(
            bars(A, 8), bars(B, 8), SR, 100.0, 128.0, BAR_S, edit_bars=8),
        handoff=lambda m: 8 * BAR_S + gr.bridge_edit_seconds(
            100.0, 128.0, 8))

    reg("sampler_one_shot_mask",
        lambda: gr.sampler_one_shot_mask(
            bars(A, 8), bars(B, 8), SR, one_shot_db=-3.0),
        handoff=lambda m: 8 * BAR_S)

    reg("feedback_loop_build",
        lambda: gr.feedback_loop_build(
            bars(A, 8), bars(B, 8), SR, BPM, BAR_S, build_bars=8),
        handoff=lambda m: 8 * BAR_S)

    reg("metric_loop_pivot",
        lambda: gr.metric_loop_pivot(
            bars(A, 8), bars(B, 8), SR, BAR_S,
            cycle_beats=3, total_beats=12),
        handoff=lambda m: 4 * BAR_S + 12 * BEAT_S)

    # Phase 22 (performer tranche A). The transform gate's off-phases
    # are intentional rhythmic silence inside the gate window
    # (bars 5-8), declared as an allowed span per FRAMEWORK.md §7.
    reg("transform_gate_loop",
        lambda: gr.transform_gate_loop(
            bars(A, 8), bars(B, 8), SR, BPM, BAR_S, gate_bars=4),
        handoff=lambda m: 8 * BAR_S,
        allowed=lambda m: [(4 * BAR_S, 8 * BAR_S)])

    reg("dual_loop_composite",
        lambda: gr.dual_loop_composite(
            bars(A, 8), bars(B, 8), SR, BAR_S,
            comp_bars=4, role_split_hz=250.0),
        handoff=lambda m: 8 * BAR_S)

    return specs
