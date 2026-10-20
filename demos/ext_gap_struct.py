"""gap_struct demos (STRUCT/ROUTING gap techniques) — FRAMEWORK.md §7.

Stems come from ctx["get_tracks()"]["stemsA"] / ["stemsB"]: dicts of
drums/bass/melody/vocal arrays (24 bars each).

Sketch caveat (honest): the harness synthesizes stemsB WITHOUT a hook
(hook=False), so stemsB["vocal"] is digital silence. stem_element_crossfade
uses the stems as-is — B's vocal stage mutes A's vocal and B's (silent)
vocal stem takes its slot; the other three element handoffs are fully
audible. For accidental_duet — a move that IS two vocals — B's vocal stem
is the harness's vocal-only sketch track ("vox"), so the demo actually
contains a duet.

same_song_switchup declares allowed spans over its two drums-only
sections: the harness's drums stem is kick + fast-decaying hats with no
bed, so isolated 50 ms windows between hits decay below the -60 dBFS
floor. That is sketch-material sparseness, not silence in the move (the
core breakdown_transition demo declares the same artifact class).
"""

from engine import gap_struct


def demo_specs(ctx):
    SR, BPM, BAR_S = ctx["SR"], ctx["BPM"], ctx["BAR_S"]
    bars, last_bars = ctx["bars"], ctx["last_bars"]
    T = ctx["get_tracks"]()
    sA, sB = T["stemsA"], T["stemsB"]
    A, B = T["A"], T["B"]

    specs = {}

    def reg(name, fn, handoff=None, allowed=None):
        specs[name] = (fn,
                       (lambda m, h=handoff: h) if handoff is not None else None,
                       allowed if allowed is not None else (lambda m: ()))

    # GAP-08: 4 bars A full, then bass -> drums -> melody -> vocal
    reg("stem_element_crossfade",
        lambda: gap_struct.stem_element_crossfade(sA, sB, SR, BAR_S),
        handoff=4 * BAR_S)  # the signature bass-stem-only entry

    # GAP-09: 12-bar strip (drums out @5, bass out @9), B slams at bar 13
    reg("strip_down_buildup",
        lambda: gap_struct.strip_down_buildup(sA, bars(B, 8), SR, BAR_S),
        handoff=12 * BAR_S)

    # GAP-10: naked vocal 2 bars, filtered rise 4 bars, drop at bar 7
    reg("flying_solo_acapella",
        lambda: gap_struct.flying_solo_acapella(
            sA, bars(B, 12), SR, BAR_S, BPM),
        handoff=6 * BAR_S)  # the drop

    # GAP-11: looping A vocal, bed swaps A->B drums+bass at bar 5
    reg("beat_switch_under_acapella",
        lambda: gap_struct.beat_switch_under_acapella(sA, sB, SR, BAR_S),
        handoff=4 * BAR_S)

    # GAP-12: two vocals, A melody pad at 0.5, B drums on the grid
    sB_duet = {"drums": sB["drums"], "bass": sB["bass"],
               "melody": sB["melody"], "vocal": bars(T["vox"], 8)}
    reg("accidental_duet",
        lambda: gap_struct.accidental_duet(sA, sB_duet, SR, BPM, BAR_S),
        handoff=4 * BAR_S)

    # GAP-13: track A full vs its own drums-only arrangement (stemsA drums)
    reg("same_song_switchup",
        lambda: gap_struct.same_song_switchup(
            bars(A, 8), bars(sA["drums"], 8), SR, BAR_S),
        handoff=2 * BAR_S,  # first flip
        allowed=lambda m: [(2 * BAR_S, 4 * BAR_S), (6 * BAR_S, 8 * BAR_S)])

    return specs
