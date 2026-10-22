"""
open-transitions — compounds-lane demo registrations (FRAMEWORK.md §7).

Merged by demos/make_demos.py's load_ext_specs(). Each entry is
(name -> (render_fn, handoff_fn, allowed_fn)) in the core format.
"""

from engine import compounds


def demo_specs(ctx):
    SR, BPM = ctx["SR"], ctx["BPM"]
    BAR_S = ctx["BAR_S"]
    get_tracks, bars, last_bars = (ctx["get_tracks"], ctx["bars"],
                                   ctx["last_bars"])
    T = get_tracks()
    A, B = T["A"], T["B"]
    specs = {}

    # CMP-01 aging_echo: A's last 8 bars play; the throw on the
    # final beat rings an aging tail over B's entrance — handoff
    # is the bar-8 boundary.
    specs["aging_echo"] = (
        lambda: compounds.aging_echo(last_bars(A, 8), bars(B, 8),
                                     SR, BPM, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )
    return specs
