"""
keeper-shape demos (Phase 30, FRAMEWORK.md §7).

Registers demos for engine/keeper_shapes.py (KEEP-01..KEEP-04), the
four lane shapes promoted from gap-flagged custom recommendations to
first-class registry entries. All material is the suite's synthesized
sketch audio (ctx tracks) — no copyrighted audio.

Sketch caveats (honest): the harness synthesizes stemsB WITHOUT a
hook, so stemsB["vocal"] is digital silence. The underlap demo
therefore demonstrates the emergence curve + vocal-hold timing
structurally, not an audible B vocal re-entry; the wera_weave demo
demonstrates the lead-vocal-over-groove choreography with A's hook
vocal (stemsA IS synthesized with a hook) and B's groove, with B's
closing chant span structurally present but silent in sketch
material. The wub_runway demo uses stemsB["melody"] as the signature
figure, which the harness does synthesize. The ooh_tail_pickup demo
uses mono sketch tracks; the "motif" is A's last phrase region,
caller-nominated in real use. Demos prove shape, not feel.
"""

from engine import keeper_shapes as keep


def demo_specs(ctx):
    SR, BAR_S = ctx["SR"], ctx["BAR_S"]
    bars, last_bars = ctx["bars"], ctx["last_bars"]
    T = ctx["get_tracks"]()
    A, B = T["A"], T["B"]
    sA, sB = T["stemsA"], T["stemsB"]

    specs = {}

    # KEEP-01: A dry 8 bars; motif completes; B picks up straight at
    # full level with the HP-filtered decaying tail under its entrance.
    specs["ooh_tail_pickup"] = (
        lambda: keep.ooh_tail_pickup(last_bars(A, 8), bars(B, 8),
                                     SR, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # KEEP-02: 12-bar emergence zone; B whisper -> parity -> full,
    # B vocal withheld until the final (re-entry) bar.
    specs["underlap"] = (
        lambda: keep.underlap(sA, sB, SR, BAR_S),
        lambda m: 12 * BAR_S,
        None,
    )

    # KEEP-03: 4 bars A full, 6-bar runway (A drums cut, vocal
    # excluded, figure play-staged), then 4 bars B proper.
    specs["wub_runway"] = (
        lambda: keep.wub_runway(sA, sB, SR, BAR_S),
        lambda m: 10 * BAR_S,
        None,
    )

    # KEEP-04: 4 bars A full, 8-bar vocal-lead weave over B groove,
    # 1-bar vocal exit, 2-bar recognition groove, 2-bar B chant last.
    specs["wera_weave"] = (
        lambda: keep.wera_weave(sA, sB, SR, BAR_S),
        lambda m: 4 * BAR_S,
        None,
    )

    return specs
