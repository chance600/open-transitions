"""
open-transitions — demo specs for the DM-clip domain module (FRAMEWORK.md §7).

Registers demos for engine/dm_techniques.py. Merged automatically by
demos/make_demos.py (load_ext_specs). All material is the suite's
synthesized sketch audio (ctx tracks) — no copyrighted audio.
"""

import numpy as np

from engine import dm_techniques as dm


def demo_specs(ctx):
    SR, BPM, BAR_S, BEAT_S = ctx["SR"], ctx["BPM"], ctx["BAR_S"], ctx["BEAT_S"]
    get_tracks, bars, last_bars = (ctx["get_tracks"], ctx["bars"],
                                   ctx["last_bars"])
    T = get_tracks()
    A, B, VOX = T["A"], T["B"], T["vox"]

    specs = {}

    # DM-A14: A's last 8 bars; the final 2 bars auto-loop under the TRANS
    # gate while B's fader comes up over 8 beats (2 bars). Output = B's
    # 8 bars; handoff at the end of the fader move.
    specs["live_loop_mix"] = (
        lambda: dm.live_loop_mix(last_bars(A, 8), bars(B, 8), SR, BPM, BAR_S),
        lambda m: 8 * BEAT_S,
        None,
    )

    # DM-A15: lead layer synthesized from B's own first beat, laid over
    # B's groove (the layer is the track, re-pitched — that is the trick).
    def _cdj_demo():
        groove = bars(B, 8)
        lead = dm.cdj_synth_lead(groove, SR, BAR_S)
        return groove * 0.85 + lead

    specs["cdj_synth_lead"] = (_cdj_demo, lambda m: 4 * BAR_S, None)

    # DM-A21: A's last 12 bars — 8 play straight, the final 4 ramp
    # 1x -> 2x (consuming 4/1.5 bars of time), then B enters full at the
    # alignment point.
    _ramp_out_s = 4 * BAR_S / 1.5
    specs["tempo_double_trick"] = (
        lambda: dm.tempo_double_trick(last_bars(A, 12), bars(B, 8), SR, BAR_S),
        lambda m: 8 * BAR_S + _ramp_out_s,
        None,
    )

    # DM-A23: 4 bars of sketch vocal preceded by its own reversed
    # reverb/delay swell (swell_s = 1.5 s). The swell fades in from
    # silence BY DESIGN — declared as allowed, gate not weakened.
    specs["reverse_vocal_ambience"] = (
        lambda: dm.reverse_vocal_ambience(bars(VOX, 4), SR),
        lambda m: 1.5,
        lambda m: [(0.0, 1.6)],
    )

    # DM-A39: a 2-bar vocal hit drowned in reverb; the appended tail
    # wobbles with an accelerating tremolo.
    specs["whoa_reverb_wobble"] = (
        lambda: dm.whoa_reverb_wobble(bars(VOX, 2), SR),
        lambda m: 2 * BAR_S,
        None,
    )

    # DM-A44: 8 bars of sketch vocal; the 1/16 tremolo amount ramps up
    # over the second half and fully gates the final bars.
    specs["vocal_tremolo_gate"] = (
        lambda: dm.vocal_tremolo_gate(bars(VOX, 8), SR, BPM),
        lambda m: 4 * BAR_S,
        None,
    )

    return specs
