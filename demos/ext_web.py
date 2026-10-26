"""
open-transitions — demo specs for the web-mined domain module
(FRAMEWORK.md §7).

Registers demos for engine/web_techniques.py (WEB-01..WEB-18, mined
2026-10-21; WEB-19..WEB-21 added Phase 23, 2026-10-22; WEB-34..WEB-38
added Phase 28, 2026-10-25, short-form technique-term mining). Merged
automatically by demos/make_demos.py
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

    # WEB-11 infinity_filter: A's final 4 bars pass through the
    # endless peak stack (2 wraps up); B enters dry at the seam.
    specs["infinity_filter"] = (
        lambda: web.infinity_filter(bars(A, 8), bars(B, 8), SR, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-12 pattern_layer_bridge: the synthesized 909 pattern plays
    # across the seam zone (A's last 4 bars + B's first 4 bars);
    # B is established as the pattern stops at bar 12.
    specs["pattern_layer_bridge"] = (
        lambda: web.pattern_layer_bridge(bars(A, 8), bars(B, 8), SR,
                                         BPM, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-13 pumper_exit: A's last 4 bars duck on the downbeat grid,
    # deepening to -10 dB; the final recovery is withheld and B
    # enters dry in the hole at the seam (the last beat of A is the
    # hole — declared allowed silence, as with the brake/power-down
    # demos).
    specs["pumper_exit"] = (
        lambda: web.pumper_exit(bars(A, 8), bars(B, 8), SR, BPM,
                                BAR_S),
        lambda m: 8 * BAR_S,
        lambda m: [(8 * BAR_S - BEAT_S, 8 * BAR_S + 0.25)],
    )

    # WEB-14 scale_down_exit: A's final beat is captured and replayed
    # 4 times across B's fade-in, stepping down the major scale.
    specs["scale_down_exit"] = (
        lambda: web.scale_down_exit(last_bars(A, 8), bars(B, 8), SR,
                                     BPM, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-15 fader_synth: A is replaced across the seam zone (bars
    # 7-10) by a saw line riding scale steps from the root; B fades
    # in under the line and is established as the synth cuts.
    specs["fader_synth"] = (
        lambda: web.fader_synth(bars(A, 8), bars(B, 8), SR, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-16 ring_mod_dissolve: A's last 4 bars crossfade into full
    # ring modulation while the carrier sweeps 100 Hz -> 2.8 kHz;
    # the dissolved shimmer cuts at the seam and B enters dry.
    specs["ring_mod_dissolve"] = (
        lambda: web.ring_mod_dissolve(bars(A, 8), bars(B, 8), SR,
                                      BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-17 formant_morph_exit: A's last 4 bars morph through the
    # a-e-i-o-u formant series at 90% wet; the last vowel cuts at
    # the seam and B enters dry.
    specs["formant_morph_exit"] = (
        lambda: web.formant_morph_exit(bars(A, 8), bars(B, 8), SR,
                                       BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-18 resonator_tail: A's last 2 bars crossfade into a
    # five-resonator ring tuned to a major voicing on A2; the
    # dry is gone at the seam and the ring decays across B's
    # 1-bar fade-in.
    specs["resonator_tail"] = (
        lambda: web.resonator_tail(bars(A, 8), bars(B, 8), SR,
                                   BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-19 continuous_drop: A plays 16 bars (its "drop"); B's
    # first bar is staged, lows killed, under A's final 8 bars;
    # B lands at full level on the seam — handoff at bar 16.
    specs["continuous_drop"] = (
        lambda: web.continuous_drop(bars(A, 16), bars(B, 8), SR,
                                    BAR_S),
        lambda m: 16 * BAR_S,
        None,
    )

    # WEB-20 drop_chop: 1 landing bar of both drops, then 2-bar
    # ownership trades x2 rounds (bars 1-8), commit to B from
    # bar 9 — handoff at the commit point, bar 9 (8 bars in).
    specs["drop_chop"] = (
        lambda: web.drop_chop(bars(A, 12), bars(B, 12), SR, BAR_S),
        lambda m: 9 * BAR_S,
        None,
    )

    # WEB-21 drop_insert: A's drop is due at bar 8; B's drop
    # substitutes for 1 bar, then A's drop resumes — handoff at
    # the insert point, bar 8.
    specs["drop_insert"] = (
        lambda: web.drop_insert(bars(A, 16), bars(B, 8), SR, BAR_S),
        lambda m: 8 * BAR_S,
        None,
    )

    # WEB-34 stepped_element_tease: B's HF layer ladders
    # 25/50/75/100% over 4 beats each (4 bars); at the ladder's
    # end B takes over full from bar 4 onward. Handoff = bar 4.
    specs["stepped_element_tease"] = (
        lambda: web.stepped_element_tease(
            bars(A, 8), bars(B, 8), SR, BAR_S),
        lambda m: 4 * BAR_S,
        None,
    )

    # WEB-35 loop_click_bridge: B's 150 ms head slice tiles
    # back-to-back (a loop cycles continuously) across 4 bars
    # while A fades out; the loop switches off and B continues
    # past the slice. Handoff = bar 4.
    specs["loop_click_bridge"] = (
        lambda: web.loop_click_bridge(
            bars(A, 8), bars(B, 8), SR, BAR_S),
        lambda m: 4 * BAR_S,
        None,
    )

    # WEB-36 cue_tap_walk: B's first beat tapped 4x at A's tempo
    # while A fades, then 4 decelerating taps (x1.2 intervals),
    # then B plays full from the cue. Handoff = B's entrance at
    # 4 beats + walk length (6.368 beats) = 10.368 beats.
    # Allowed silence: the walk's inter-tap gaps — the taps are
    # discrete restarts, so the gaps between them are the
    # technique, not a render defect. The tap section itself
    # (cue tiled back-to-back over the fading A) stays gated.
    _tap_beats = 4.0
    _walk_beats = 1.0 + 1.2 + 1.44 + 1.728 + 1.0
    specs["cue_tap_walk"] = (
        lambda: web.cue_tap_walk(
            bars(A, 8), bars(B, 8), SR, BAR_S, BPM),
        lambda m: (_tap_beats + _walk_beats) * BEAT_S,
        lambda m: [(_tap_beats * BEAT_S,
                    (_tap_beats + _walk_beats) * BEAT_S)],
    )

    # WEB-37 brake_tempo_land: A 8 bars, its last 2 beats brake
    # 1.0 -> 0.8 (output 2/0.9 beats long); B starts full on the
    # 1 after the braked window. Handoff = 8 bars + the brake
    # stretch (2/0.9 - 2 beats).
    specs["brake_tempo_land"] = (
        lambda: web.brake_tempo_land(
            bars(A, 8), bars(B, 8), SR, BPM),
        lambda m: 8 * BAR_S + (2.0 / 0.9 - 2.0) * BEAT_S,
        None,
    )

    # WEB-38 delay_drum_roll: A 8 bars, its last 4 beats carry
    # the 1/2-beat delay send ramping to 0.6, slammed shut as B
    # drops full on the beat. Handoff = bar 8.
    specs["delay_drum_roll"] = (
        lambda: web.delay_drum_roll(
            bars(A, 8), bars(B, 8), SR, BAR_S, BPM),
        lambda m: 8 * BAR_S,
        None,
    )

    return specs
