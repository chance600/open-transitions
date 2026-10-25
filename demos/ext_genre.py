"""
open-transitions — demo specs for the genre traditions tranche B
domain module (FRAMEWORK.md §7).

Registers demos for engine/genre_techniques.py (WEB-30..WEB-33,
Phase 27 expansion tranche 6: techno multi-deck doctrine, trance /
harmonic traditions, open-format tables, 2026-10-24). Merged
automatically by demos/make_demos.py (load_ext_specs). All material
is the suite's synthesized sketch audio (ctx tracks) — no
copyrighted audio.

Sketch caveats (honest):
* breakdown_swap stages on the suite's drumless breakdown sketch
  (pads + hook, no kick) with stemsB's drums stem as the entering
  beat — the mechanism (drums under open space) is exactly what
  renders; the breakdown's own melodic content is the sketch's.
* bed_tempo_switch's demo uses the function's neutral synthesized
  pad as the bed, and the sketch runs at one fixed BPM — so the
  demo proves the bed STRUCTURE (A -> bed -> B drop), not the
  tempo discontinuity itself, which is caller context.
* stemsB carries no vocal hook (hook=False), so no demo here
  exercises a vocal bed; the stutter demo's vocal content is
  A's own hook bars.
"""

from engine import genre_techniques as gg


def demo_specs(ctx):
    SR, BPM, BAR_S = ctx["SR"], ctx["BPM"], ctx["BAR_S"]
    get_tracks, bars, last_bars = (ctx["get_tracks"], ctx["bars"],
                                   ctx["last_bars"])
    T = get_tracks()
    A, B = T["A"], T["B"]
    sB = T["stemsB"]
    brk = T["break"]

    specs = {}

    # WEB-30 breakdown_swap: A's 8-bar drumless breakdown with
    # B's drums fading in across the window on a smootherstep;
    # B plays full from bar 8 onward. Handoff = breakdown
    # resolution at 8 bars.
    specs["breakdown_swap"] = (
        lambda: gg.breakdown_swap(
            bars(brk, 8), bars(B, 16), SR, BAR_S,
            b_drums=bars(sB["drums"], 8)),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-31 echo_out_reset: A 8 bars, 2-bar echo tail standing
    # alone, B drops dry on the next downbeat. Handoff = the
    # drop at 10 bars.
    # Allowed silence: the tail's decayed portion. The tail
    # decays 5.19 dB per 0.234 s repeat (feedback 0.55), so from
    # a ~-32 dBFS throw it crosses -60 dBFS ~1.3 s into the
    # tail and stays below it until B drops — that decay to
    # inaudibility IS the reset mechanism (the room's metronome
    # erased), not a render defect. The tail's first second
    # stays gated: a tail silent from the start still fails.
    specs["echo_out_reset"] = (
        lambda: gg.echo_out_reset(
            bars(A, 8), bars(B, 8), SR, BAR_S, BPM),
        lambda m: 10 * BAR_S,
        lambda m: [(8 * BAR_S + 1.0, 10 * BAR_S)],
    )

    # WEB-32 bed_tempo_switch: A 8 bars crossfading into the
    # neutral pad bed over its final 2 bars; bed sustains 4
    # bars total; B drops at 10 bars. Fixed sketch BPM: the
    # demo proves structure, not the discontinuity (see module
    # docstring).
    specs["bed_tempo_switch"] = (
        lambda: gg.bed_tempo_switch(
            bars(A, 8), bars(B, 8), SR, BAR_S, bed=None),
        lambda m: 10 * BAR_S,
        None,
    )

    # WEB-33 instant_double_stutter: A's final 2 bars replaced
    # by the half-beat dual-stream splice (each even half-beat
    # doubled); B enters full at 8 bars.
    specs["instant_double_stutter"] = (
        lambda: gg.instant_double_stutter(
            bars(A, 8), bars(B, 8), SR, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    return specs
