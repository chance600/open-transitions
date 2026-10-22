# VARIANTS — generated variant catalog

Variants are base techniques x named presets on their declared
discrete parameter axes (FRAMEWORK.md §6, operator 1; axes are
the `"presets"` maps in each technique's `params`, §3). The
registry lives in `engine/variants.py` and is **generated,
never hand-listed**: `VARIANTS = build_variants()` enumerates
`meta.all_meta()` at import time.

**Snapshot: 356 variants across 56 base techniques** (108 variants across 29 core-bank bases; the rest arrive via domain modules, FRAMEWORK.md §7).
This file is a snapshot of one generation run — see
*Regenerating* below.

## Naming scheme

- **Single-axis:** `<base>__<preset>` — one variant per preset
  on the base's FIRST preset axis.
  e.g. `eq_blend__16bar` = eq_blend with `blend_bars=16`.
- **Pairwise:** `<base>__<p1>_<p2>` — combinations of the first
  two preset axes, capped at 9 combos per technique.
  e.g. `brake_stop__long_exp` = `stop_beats=2.0, curve='exp'`.

Render any variant with `variants.render_variant(name, a, b, sr, **ctx)`;
resolve without rendering via `variants.get_variant(name)`,
which returns `(fn, preset_kwargs)` and raises `KeyError` on
unknown ids. Every variant inherits its base technique's
evidence, recorded as `"inherited from <base>"`.

Demo coverage: `demos/ext_variants.py` registers a representative
sample (first single-axis variant + first pairwise combo per
core base, capped at 40) through the standard demo pipeline.

## Catalog

### acapella_overlay — Acapella Overlay (Live Mashup) (3 variants)

| variant | params |
|---|---|
| `acapella_overlay__16bar` | overlay_bars=16 |
| `acapella_overlay__32bar` | overlay_bars=32 |
| `acapella_overlay__8bar` | overlay_bars=8 |

### backspin — Backspin (Spinback) (3 variants)

| variant | params |
|---|---|
| `backspin__half` | spin_beats=0.5 |
| `backspin__one` | spin_beats=1.0 |
| `backspin__two` | spin_beats=2.0 |

### beatslicer_shuffle — BeatSlicer Shuffle (Buffer Slice-Permutation Build) (15 variants)

| variant | params |
|---|---|
| `beatslicer_shuffle__bookends` | pattern='bookends' |
| `beatslicer_shuffle__bookends_one` | pattern='bookends', buffer_bars=1 |
| `beatslicer_shuffle__bookends_two` | pattern='bookends', buffer_bars=2 |
| `beatslicer_shuffle__halves` | pattern='halves' |
| `beatslicer_shuffle__halves_one` | pattern='halves', buffer_bars=1 |
| `beatslicer_shuffle__halves_two` | pattern='halves', buffer_bars=2 |
| `beatslicer_shuffle__inside_out` | pattern='inside_out' |
| `beatslicer_shuffle__inside_out_one` | pattern='inside_out', buffer_bars=1 |
| `beatslicer_shuffle__inside_out_two` | pattern='inside_out', buffer_bars=2 |
| `beatslicer_shuffle__reverse` | pattern='reverse' |
| `beatslicer_shuffle__reverse_one` | pattern='reverse', buffer_bars=1 |
| `beatslicer_shuffle__reverse_two` | pattern='reverse', buffer_bars=2 |
| `beatslicer_shuffle__stride` | pattern='stride' |
| `beatslicer_shuffle__stride_one` | pattern='stride', buffer_bars=1 |
| `beatslicer_shuffle__swap_pairs` | pattern='swap_pairs' |

### brake_stop — Brake / Tape Stop (12 variants)

| variant | params |
|---|---|
| `brake_stop__long` | stop_beats=2.0 |
| `brake_stop__long_exp` | stop_beats=2.0, curve='exp' |
| `brake_stop__long_linear` | stop_beats=2.0, curve='linear' |
| `brake_stop__long_s_curve` | stop_beats=2.0, curve='s' |
| `brake_stop__snap` | stop_beats=0.25 |
| `brake_stop__snap_exp` | stop_beats=0.25, curve='exp' |
| `brake_stop__snap_linear` | stop_beats=0.25, curve='linear' |
| `brake_stop__snap_s_curve` | stop_beats=0.25, curve='s' |
| `brake_stop__standard` | stop_beats=1.0 |
| `brake_stop__standard_exp` | stop_beats=1.0, curve='exp' |
| `brake_stop__standard_linear` | stop_beats=1.0, curve='linear' |
| `brake_stop__standard_s_curve` | stop_beats=1.0, curve='s' |

### build_to_drop — Build-to-Drop (Dual-Build Layering) (3 variants)

| variant | params |
|---|---|
| `build_to_drop__16bar` | build_bars=16 |
| `build_to_drop__32bar` | build_bars=32 |
| `build_to_drop__8bar` | build_bars=8 |

### crush_degrade — Crush Degrade (Bit-Reduction Exit) (12 variants)

| variant | params |
|---|---|
| `crush_degrade__crushed` | bits_end=5.0 |
| `crush_degrade__crushed_long` | bits_end=5.0, bars=8 |
| `crush_degrade__crushed_short` | bits_end=5.0, bars=2 |
| `crush_degrade__crushed_standard` | bits_end=5.0, bars=4 |
| `crush_degrade__destroyed` | bits_end=3.5 |
| `crush_degrade__destroyed_long` | bits_end=3.5, bars=8 |
| `crush_degrade__destroyed_short` | bits_end=3.5, bars=2 |
| `crush_degrade__destroyed_standard` | bits_end=3.5, bars=4 |
| `crush_degrade__lofi` | bits_end=7.0 |
| `crush_degrade__lofi_long` | bits_end=7.0, bars=8 |
| `crush_degrade__lofi_short` | bits_end=7.0, bars=2 |
| `crush_degrade__lofi_standard` | bits_end=7.0, bars=4 |

### double_drop — Double Drop (Dual-Build Collision) (2 variants)

| variant | params |
|---|---|
| `double_drop__16bar` | drop_at_bar=16 |
| `double_drop__8bar` | drop_at_bar=8 |

### downlifter_exit — Downlifter Exit (Descending Sweep Seam Mask) (12 variants)

| variant | params |
|---|---|
| `downlifter_exit__half` | sweep_bars=0.5 |
| `downlifter_exit__half_low` | sweep_bars=0.5, f_end=300.0 |
| `downlifter_exit__half_mid` | sweep_bars=0.5, f_end=800.0 |
| `downlifter_exit__half_sub` | sweep_bars=0.5, f_end=120.0 |
| `downlifter_exit__one` | sweep_bars=1.0 |
| `downlifter_exit__one_low` | sweep_bars=1.0, f_end=300.0 |
| `downlifter_exit__one_mid` | sweep_bars=1.0, f_end=800.0 |
| `downlifter_exit__one_sub` | sweep_bars=1.0, f_end=120.0 |
| `downlifter_exit__two` | sweep_bars=2.0 |
| `downlifter_exit__two_low` | sweep_bars=2.0, f_end=300.0 |
| `downlifter_exit__two_mid` | sweep_bars=2.0, f_end=800.0 |
| `downlifter_exit__two_sub` | sweep_bars=2.0, f_end=120.0 |

### drum_bridge — Drum Bridge (Atonal Neutral Zone) (3 variants)

| variant | params |
|---|---|
| `drum_bridge__12bar` | interlude_bars=12 |
| `drum_bridge__16bar` | interlude_bars=16 |
| `drum_bridge__8bar` | interlude_bars=8 |

### dual_loop_composite — Dual-Loop Composite (EZ Loop-as-Instrument) (12 variants)

| variant | params |
|---|---|
| `dual_loop_composite__2bar` | comp_bars=2 |
| `dual_loop_composite__2bar_high` | comp_bars=2, role_split_hz=350 |
| `dual_loop_composite__2bar_low` | comp_bars=2, role_split_hz=150 |
| `dual_loop_composite__2bar_mid` | comp_bars=2, role_split_hz=250 |
| `dual_loop_composite__4bar` | comp_bars=4 |
| `dual_loop_composite__4bar_high` | comp_bars=4, role_split_hz=350 |
| `dual_loop_composite__4bar_low` | comp_bars=4, role_split_hz=150 |
| `dual_loop_composite__4bar_mid` | comp_bars=4, role_split_hz=250 |
| `dual_loop_composite__8bar` | comp_bars=8 |
| `dual_loop_composite__8bar_high` | comp_bars=8, role_split_hz=350 |
| `dual_loop_composite__8bar_low` | comp_bars=8, role_split_hz=150 |
| `dual_loop_composite__8bar_mid` | comp_bars=8, role_split_hz=250 |

### echo_out — Echo Out (4 variants)

| variant | params |
|---|---|
| `echo_out__dotted` | beat_div=0.75 |
| `echo_out__full` | beat_div=1.0 |
| `echo_out__half` | beat_div=0.5 |
| `echo_out__quarter` | beat_div=0.25 |

### echo_out_blend — Echo Out Blend (3 variants)

| variant | params |
|---|---|
| `echo_out_blend__dotted` | beat_div=0.75 |
| `echo_out_blend__full` | beat_div=1.0 |
| `echo_out_blend__half` | beat_div=0.5 |

### eq_blend — EQ Blend (3-Band Frequency Replacement) (4 variants)

| variant | params |
|---|---|
| `eq_blend__16bar` | blend_bars=16 |
| `eq_blend__32bar` | blend_bars=32 |
| `eq_blend__64bar` | blend_bars=64 |
| `eq_blend__8bar` | blend_bars=8 |

### fader_synth — Fader Synth (Source-Replacing Fader Oscillator) (12 variants)

| variant | params |
|---|---|
| `fader_synth__saw` | waveform='saw' |
| `fader_synth__saw_arp` | waveform='saw', ride='arp' |
| `fader_synth__saw_glide` | waveform='saw', ride='glide' |
| `fader_synth__saw_hold` | waveform='saw', ride='hold' |
| `fader_synth__saw_steps` | waveform='saw', ride='steps' |
| `fader_synth__sine` | waveform='sine' |
| `fader_synth__sine_arp` | waveform='sine', ride='arp' |
| `fader_synth__sine_glide` | waveform='sine', ride='glide' |
| `fader_synth__sine_hold` | waveform='sine', ride='hold' |
| `fader_synth__sine_steps` | waveform='sine', ride='steps' |
| `fader_synth__square` | waveform='square' |
| `fader_synth__square_arp` | waveform='square', ride='arp' |

### fake_drop — Fake Drop (Rug Pull) (3 variants)

| variant | params |
|---|---|
| `fake_drop__2beat` | void_beats=2.0 |
| `fake_drop__3beat` | void_beats=3.0 |
| `fake_drop__4beat` | void_beats=4.0 |

### feedback_loop_build — Feedback-Loop Build (Zabiela EFX-1000) (2 variants)

| variant | params |
|---|---|
| `feedback_loop_build__4bar` | build_bars=4 |
| `feedback_loop_build__8bar` | build_bars=8 |

### filter_sweep — Filter Sweep Transition (HPF/LPF) (3 variants)

| variant | params |
|---|---|
| `filter_sweep__long` | sweep_bars=12 |
| `filter_sweep__quick` | sweep_bars=4 |
| `filter_sweep__standard` | sweep_bars=7 |

### flanger_sweep — Flanger Sweep (Jet Comb Build/Exit) (12 variants)

| variant | params |
|---|---|
| `flanger_sweep__long` | sweep_bars=16 |
| `flanger_sweep__long_deep` | sweep_bars=16, depth_ms=3.8 |
| `flanger_sweep__long_jet` | sweep_bars=16, depth_ms=2.2 |
| `flanger_sweep__long_subtle` | sweep_bars=16, depth_ms=1.2 |
| `flanger_sweep__standard` | sweep_bars=8 |
| `flanger_sweep__standard_deep` | sweep_bars=8, depth_ms=3.8 |
| `flanger_sweep__standard_jet` | sweep_bars=8, depth_ms=2.2 |
| `flanger_sweep__standard_subtle` | sweep_bars=8, depth_ms=1.2 |
| `flanger_sweep__tight` | sweep_bars=4 |
| `flanger_sweep__tight_deep` | sweep_bars=4, depth_ms=3.8 |
| `flanger_sweep__tight_jet` | sweep_bars=4, depth_ms=2.2 |
| `flanger_sweep__tight_subtle` | sweep_bars=4, depth_ms=1.2 |

### formant_morph_exit — Formant Morph Exit (Vowel-Series Spectral Morph) (12 variants)

| variant | params |
|---|---|
| `formant_morph_exit__aeiou` | path='aeiou' |
| `formant_morph_exit__aeiou_english` | path='aeiou', table='english' |
| `formant_morph_exit__aeiou_german` | path='aeiou', table='german' |
| `formant_morph_exit__ai` | path='ai' |
| `formant_morph_exit__ai_english` | path='ai', table='english' |
| `formant_morph_exit__ai_german` | path='ai', table='german' |
| `formant_morph_exit__ou` | path='ou' |
| `formant_morph_exit__ou_english` | path='ou', table='english' |
| `formant_morph_exit__ou_german` | path='ou', table='german' |
| `formant_morph_exit__ouiea` | path='ouiea' |
| `formant_morph_exit__ouiea_english` | path='ouiea', table='english' |
| `formant_morph_exit__ouiea_german` | path='ouiea', table='german' |

### granular_freeze — Granular Freeze (Frozen-Moment Cloud Handoff) (12 variants)

| variant | params |
|---|---|
| `granular_freeze__coarse` | grain_ms=120.0 |
| `granular_freeze__coarse_long` | grain_ms=120.0, cloud_bars=8 |
| `granular_freeze__coarse_short` | grain_ms=120.0, cloud_bars=2 |
| `granular_freeze__coarse_standard` | grain_ms=120.0, cloud_bars=4 |
| `granular_freeze__fine` | grain_ms=35.0 |
| `granular_freeze__fine_long` | grain_ms=35.0, cloud_bars=8 |
| `granular_freeze__fine_short` | grain_ms=35.0, cloud_bars=2 |
| `granular_freeze__fine_standard` | grain_ms=35.0, cloud_bars=4 |
| `granular_freeze__standard` | grain_ms=70.0 |
| `granular_freeze__standard_long` | grain_ms=70.0, cloud_bars=8 |
| `granular_freeze__standard_short` | grain_ms=70.0, cloud_bars=2 |
| `granular_freeze__standard_standard` | grain_ms=70.0, cloud_bars=4 |

### helix_catch — Helix Catch (Loop-Sampler Pitch-Ramp Hold & Release) (12 variants)

| variant | params |
|---|---|
| `helix_catch__bar` | capture_beats=4.0 |
| `helix_catch__bar_four` | capture_beats=4.0, hold_bars=4 |
| `helix_catch__bar_one` | capture_beats=4.0, hold_bars=1 |
| `helix_catch__bar_two` | capture_beats=4.0, hold_bars=2 |
| `helix_catch__beat` | capture_beats=1.0 |
| `helix_catch__beat_four` | capture_beats=1.0, hold_bars=4 |
| `helix_catch__beat_one` | capture_beats=1.0, hold_bars=1 |
| `helix_catch__beat_two` | capture_beats=1.0, hold_bars=2 |
| `helix_catch__half` | capture_beats=0.5 |
| `helix_catch__half_four` | capture_beats=0.5, hold_bars=4 |
| `helix_catch__half_one` | capture_beats=0.5, hold_bars=1 |
| `helix_catch__half_two` | capture_beats=0.5, hold_bars=2 |

### hook_drop_handoff — Hook-Drop Handoff (12 variants)

| variant | params |
|---|---|
| `hook_drop_handoff__60ms` | exit_fade_ms=60.0 |
| `hook_drop_handoff__60ms_2bar` | exit_fade_ms=60.0, bloom_bars=2 |
| `hook_drop_handoff__60ms_3bar` | exit_fade_ms=60.0, bloom_bars=3 |
| `hook_drop_handoff__60ms_4bar` | exit_fade_ms=60.0, bloom_bars=4 |
| `hook_drop_handoff__70ms` | exit_fade_ms=70.0 |
| `hook_drop_handoff__70ms_2bar` | exit_fade_ms=70.0, bloom_bars=2 |
| `hook_drop_handoff__70ms_3bar` | exit_fade_ms=70.0, bloom_bars=3 |
| `hook_drop_handoff__70ms_4bar` | exit_fade_ms=70.0, bloom_bars=4 |
| `hook_drop_handoff__80ms` | exit_fade_ms=80.0 |
| `hook_drop_handoff__80ms_2bar` | exit_fade_ms=80.0, bloom_bars=2 |
| `hook_drop_handoff__80ms_3bar` | exit_fade_ms=80.0, bloom_bars=3 |
| `hook_drop_handoff__80ms_4bar` | exit_fade_ms=80.0, bloom_bars=4 |

### hotcue_drop_swap — Hot-Cue Drop Swap (Drop Juggling) (3 variants)

| variant | params |
|---|---|
| `hotcue_drop_swap__2beat` | xfade_beats=2 |
| `hotcue_drop_swap__4beat` | xfade_beats=4 |
| `hotcue_drop_swap__8beat` | xfade_beats=8 |

### infinity_filter — Infinity Filter (Endless Barber-Pole Sweep Exit) (8 variants)

| variant | params |
|---|---|
| `infinity_filter__down` | direction=-1 |
| `infinity_filter__down_one` | direction=-1, cycles=1.0 |
| `infinity_filter__down_three` | direction=-1, cycles=3.0 |
| `infinity_filter__down_two` | direction=-1, cycles=2.0 |
| `infinity_filter__up` | direction=1 |
| `infinity_filter__up_one` | direction=1, cycles=1.0 |
| `infinity_filter__up_three` | direction=1, cycles=3.0 |
| `infinity_filter__up_two` | direction=1, cycles=2.0 |

### layered_fx_stack — Layered FX Stack (Echo + Filter + Reverb) (2 variants)

| variant | params |
|---|---|
| `layered_fx_stack__4bar` | echo_bars=4 |
| `layered_fx_stack__8bar` | echo_bars=8 |

### loop_juggle_replace — Loop-Juggle Replace (2 variants)

| variant | params |
|---|---|
| `loop_juggle_replace__2cycle` | cycles=2 |
| `loop_juggle_replace__4cycle` | cycles=4 |

### loop_roll_build — Loop Roll Build (2 variants)

| variant | params |
|---|---|
| `loop_roll_build__one` | roll_bars=1 |
| `loop_roll_build__two` | roll_bars=2 |

### loop_transition — Loop Transition (Bounded Loop Handoff) (2 variants)

| variant | params |
|---|---|
| `loop_transition__4bar` | loop_bars=4 |
| `loop_transition__8bar` | loop_bars=8 |

### metric_loop_pivot — Metric Loop Pivot (3:4 Tempo Modulation) (2 variants)

| variant | params |
|---|---|
| `metric_loop_pivot__3beat` | cycle_beats=3 |
| `metric_loop_pivot__3beat_12beat` | cycle_beats=3, total_beats=12 |

### noise_echo_buildup — Noise + Echo Buildup (Empty-Channel Riser) (3 variants)

| variant | params |
|---|---|
| `noise_echo_buildup__16bar` | build_bars=16 |
| `noise_echo_buildup__4bar` | build_bars=4 |
| `noise_echo_buildup__8bar` | build_bars=8 |

### pattern_layer_bridge — Pattern Layer Bridge (Pattern Player Seam Layer) (12 variants)

| variant | params |
|---|---|
| `pattern_layer_bridge__build` | pattern='build' |
| `pattern_layer_bridge__build_kit808` | pattern='build', kit='kit808' |
| `pattern_layer_bridge__build_kit909` | pattern='build', kit='kit909' |
| `pattern_layer_bridge__foundation` | pattern='foundation' |
| `pattern_layer_bridge__foundation_kit808` | pattern='foundation', kit='kit808' |
| `pattern_layer_bridge__foundation_kit909` | pattern='foundation', kit='kit909' |
| `pattern_layer_bridge__groove` | pattern='groove' |
| `pattern_layer_bridge__groove_kit808` | pattern='groove', kit='kit808' |
| `pattern_layer_bridge__groove_kit909` | pattern='groove', kit='kit909' |
| `pattern_layer_bridge__roll` | pattern='roll' |
| `pattern_layer_bridge__roll_kit808` | pattern='roll', kit='kit808' |
| `pattern_layer_bridge__roll_kit909` | pattern='roll', kit='kit909' |

### pitch_play — Pitch Play (Key-Shifted Vocal Overlay) (4 variants)

| variant | params |
|---|---|
| `pitch_play__down1` | semitones=-1 |
| `pitch_play__down2` | semitones=-2 |
| `pitch_play__up1` | semitones=1 |
| `pitch_play__up2` | semitones=2 |

### power_down — Power-Down (3 variants)

| variant | params |
|---|---|
| `power_down__long` | down_beats=3.0 |
| `power_down__quick` | down_beats=1.0 |
| `power_down__standard` | down_beats=1.5 |

### premade_tempo_bridge_edit — Pre-Made Tempo-Bridge Edit (Transition Track) (3 variants)

| variant | params |
|---|---|
| `premade_tempo_bridge_edit__16bar` | edit_bars=16 |
| `premade_tempo_bridge_edit__4bar` | edit_bars=4 |
| `premade_tempo_bridge_edit__8bar` | edit_bars=8 |

### pumper_exit — Pumper Exit (Downbeat Duck Pump Exit) (12 variants)

| variant | params |
|---|---|
| `pumper_exit__deep` | duck_db=-16.0 |
| `pumper_exit__deep_early16` | duck_db=-16.0, offset_beats=-0.0625 |
| `pumper_exit__deep_early4` | duck_db=-16.0, offset_beats=-0.25 |
| `pumper_exit__deep_early8` | duck_db=-16.0, offset_beats=-0.125 |
| `pumper_exit__deep_on_grid` | duck_db=-16.0, offset_beats=0.0 |
| `pumper_exit__light` | duck_db=-6.0 |
| `pumper_exit__light_early16` | duck_db=-6.0, offset_beats=-0.0625 |
| `pumper_exit__light_early4` | duck_db=-6.0, offset_beats=-0.25 |
| `pumper_exit__light_early8` | duck_db=-6.0, offset_beats=-0.125 |
| `pumper_exit__light_on_grid` | duck_db=-6.0, offset_beats=0.0 |
| `pumper_exit__standard` | duck_db=-10.0 |
| `pumper_exit__standard_early16` | duck_db=-10.0, offset_beats=-0.0625 |

### resonator_tail — Resonator Tail (Tuned Resonator-Bank Ring-Out) (13 variants)

| variant | params |
|---|---|
| `resonator_tail__major` | chord='major' |
| `resonator_tail__major_long` | chord='major', decay_s=4.5 |
| `resonator_tail__major_short` | chord='major', decay_s=1.2 |
| `resonator_tail__major_standard` | chord='major', decay_s=2.5 |
| `resonator_tail__minor` | chord='minor' |
| `resonator_tail__minor_long` | chord='minor', decay_s=4.5 |
| `resonator_tail__minor_short` | chord='minor', decay_s=1.2 |
| `resonator_tail__minor_standard` | chord='minor', decay_s=2.5 |
| `resonator_tail__octave` | chord='octave' |
| `resonator_tail__octave_long` | chord='octave', decay_s=4.5 |
| `resonator_tail__octave_short` | chord='octave', decay_s=1.2 |
| `resonator_tail__octave_standard` | chord='octave', decay_s=2.5 |
| `resonator_tail__power` | chord='power' |

### reverb_freeze — Reverb Freeze (3 variants)

| variant | params |
|---|---|
| `reverb_freeze__1bar` | freeze_bars=1 |
| `reverb_freeze__2bar` | freeze_bars=2 |
| `reverb_freeze__4bar` | freeze_bars=4 |

### reverb_wash — Reverb Wash (3 variants)

| variant | params |
|---|---|
| `reverb_wash__early` | wash_start_bar=2 |
| `reverb_wash__late` | wash_start_bar=8 |
| `reverb_wash__standard` | wash_start_bar=4 |

### reverse_roll — Reverse Roll (Reversed Loop-Sampler Build) (3 variants)

| variant | params |
|---|---|
| `reverse_roll__long` | roll_bars=4 |
| `reverse_roll__quick` | roll_bars=1 |
| `reverse_roll__standard` | roll_bars=2 |

### rhythmic_fader_chops — Rhythmic Fader Chops (Transformer) (3 variants)

| variant | params |
|---|---|
| `rhythmic_fader_chops__2beat` | chop_beats=2 |
| `rhythmic_fader_chops__4beat` | chop_beats=4 |
| `rhythmic_fader_chops__8beat` | chop_beats=8 |

### ring_mod_dissolve — Ring Mod Dissolve (Carrier-Multiplication Exit) (12 variants)

| variant | params |
|---|---|
| `ring_mod_dissolve__low` | carrier_start_hz=60.0 |
| `ring_mod_dissolve__low_manual_max` | carrier_start_hz=60.0, carrier_end_hz=8371.0 |
| `ring_mod_dissolve__low_soft` | carrier_start_hz=60.0, carrier_end_hz=1200.0 |
| `ring_mod_dissolve__low_standard` | carrier_start_hz=60.0, carrier_end_hz=2800.0 |
| `ring_mod_dissolve__manual_min` | carrier_start_hz=100.0 |
| `ring_mod_dissolve__manual_min_manual_max` | carrier_start_hz=100.0, carrier_end_hz=8371.0 |
| `ring_mod_dissolve__manual_min_soft` | carrier_start_hz=100.0, carrier_end_hz=1200.0 |
| `ring_mod_dissolve__manual_min_standard` | carrier_start_hz=100.0, carrier_end_hz=2800.0 |
| `ring_mod_dissolve__mid` | carrier_start_hz=240.0 |
| `ring_mod_dissolve__mid_manual_max` | carrier_start_hz=240.0, carrier_end_hz=8371.0 |
| `ring_mod_dissolve__mid_soft` | carrier_start_hz=240.0, carrier_end_hz=1200.0 |
| `ring_mod_dissolve__mid_standard` | carrier_start_hz=240.0, carrier_end_hz=2800.0 |

### riser_drop — Riser Drop (2 variants)

| variant | params |
|---|---|
| `riser_drop__4bar` | riser_bars=4 |
| `riser_drop__8bar` | riser_bars=8 |

### riser_ducking_overlay — Riser Ducking & Placement (Overlay) (3 variants)

| variant | params |
|---|---|
| `riser_ducking_overlay__16bar` | pre_drop_bars=16 |
| `riser_ducking_overlay__4bar` | pre_drop_bars=4 |
| `riser_ducking_overlay__8bar` | pre_drop_bars=8 |

### scale_down_exit — Scale Down Exit (Beat-Stepped Pitch Descent) (14 variants)

| variant | params |
|---|---|
| `scale_down_exit__chromatic` | scale='chromatic' |
| `scale_down_exit__chromatic_deep` | scale='chromatic', steps=6 |
| `scale_down_exit__chromatic_few` | scale='chromatic', steps=3 |
| `scale_down_exit__chromatic_standard` | scale='chromatic', steps=4 |
| `scale_down_exit__major` | scale='major' |
| `scale_down_exit__major_deep` | scale='major', steps=6 |
| `scale_down_exit__major_few` | scale='major', steps=3 |
| `scale_down_exit__major_pent` | scale='major_pent' |
| `scale_down_exit__major_pent_deep` | scale='major_pent', steps=6 |
| `scale_down_exit__major_pent_few` | scale='major_pent', steps=3 |
| `scale_down_exit__major_pent_standard` | scale='major_pent', steps=4 |
| `scale_down_exit__major_standard` | scale='major', steps=4 |
| `scale_down_exit__minor` | scale='minor' |
| `scale_down_exit__minor_pent` | scale='minor_pent' |

### scratch_in — Scratch-In / Scratch Drop (3 variants)

| variant | params |
|---|---|
| `scratch_in__half` | scratch_beats=0.5 |
| `scratch_in__one` | scratch_beats=1.0 |
| `scratch_in__two` | scratch_beats=2.0 |

### screwed_treatment — Screwed Treatment (Chopped & Screwed / Slowed) (12 variants)

| variant | params |
|---|---|
| `screwed_treatment__chipmunk` | rate=1.5 |
| `screwed_treatment__chipmunk_coupled` | rate=1.5, pitch_coupled=True |
| `screwed_treatment__chipmunk_held` | rate=1.5, pitch_coupled=False |
| `screwed_treatment__deep` | rate=0.6 |
| `screwed_treatment__deep_coupled` | rate=0.6, pitch_coupled=True |
| `screwed_treatment__deep_held` | rate=0.6, pitch_coupled=False |
| `screwed_treatment__double` | rate=2.0 |
| `screwed_treatment__double_coupled` | rate=2.0, pitch_coupled=True |
| `screwed_treatment__double_held` | rate=2.0, pitch_coupled=False |
| `screwed_treatment__screw` | rate=0.7 |
| `screwed_treatment__screw_coupled` | rate=0.7, pitch_coupled=True |
| `screwed_treatment__screw_held` | rate=0.7, pitch_coupled=False |

### shepard_riser — Shepard Riser (Endless-Rise Build Layer) (8 variants)

| variant | params |
|---|---|
| `shepard_riser__down` | direction=-1 |
| `shepard_riser__down_long` | direction=-1, bars=16 |
| `shepard_riser__down_short` | direction=-1, bars=4 |
| `shepard_riser__down_standard` | direction=-1, bars=8 |
| `shepard_riser__up` | direction=1 |
| `shepard_riser__up_long` | direction=1, bars=16 |
| `shepard_riser__up_short` | direction=1, bars=4 |
| `shepard_riser__up_standard` | direction=1, bars=8 |

### shimmer_wash — Shimmer Wash (Octave-Climbing Reverb Exit) (12 variants)

| variant | params |
|---|---|
| `shimmer_wash__fifth` | shift_semitones=7.0 |
| `shimmer_wash__fifth_long` | shift_semitones=7.0, swell_bars=8 |
| `shimmer_wash__fifth_short` | shift_semitones=7.0, swell_bars=2 |
| `shimmer_wash__fifth_standard` | shift_semitones=7.0, swell_bars=4 |
| `shimmer_wash__fourth` | shift_semitones=5.0 |
| `shimmer_wash__fourth_long` | shift_semitones=5.0, swell_bars=8 |
| `shimmer_wash__fourth_short` | shift_semitones=5.0, swell_bars=2 |
| `shimmer_wash__fourth_standard` | shift_semitones=5.0, swell_bars=4 |
| `shimmer_wash__octave` | shift_semitones=12.0 |
| `shimmer_wash__octave_long` | shift_semitones=12.0, swell_bars=8 |
| `shimmer_wash__octave_short` | shift_semitones=12.0, swell_bars=2 |
| `shimmer_wash__octave_standard` | shift_semitones=12.0, swell_bars=4 |

### slip_mode_flourish — Slip-Mode Flourish (3 variants)

| variant | params |
|---|---|
| `slip_mode_flourish__half` | flourish_beats=0.5 |
| `slip_mode_flourish__one` | flourish_beats=1.0 |
| `slip_mode_flourish__two` | flourish_beats=2.0 |

### spiral_echo — Spiral Echo (Pitch-Riding Feedback Delay) (12 variants)

| variant | params |
|---|---|
| `spiral_echo__beat` | delay_beats=1.0 |
| `spiral_echo__beat_down2` | delay_beats=1.0, shift_semitones=-2.0 |
| `spiral_echo__beat_down4` | delay_beats=1.0, shift_semitones=-4.0 |
| `spiral_echo__beat_up2` | delay_beats=1.0, shift_semitones=2.0 |
| `spiral_echo__beat_up4` | delay_beats=1.0, shift_semitones=4.0 |
| `spiral_echo__dotted` | delay_beats=0.75 |
| `spiral_echo__dotted_down2` | delay_beats=0.75, shift_semitones=-2.0 |
| `spiral_echo__dotted_down4` | delay_beats=0.75, shift_semitones=-4.0 |
| `spiral_echo__dotted_up2` | delay_beats=0.75, shift_semitones=2.0 |
| `spiral_echo__dotted_up4` | delay_beats=0.75, shift_semitones=4.0 |
| `spiral_echo__quarter` | delay_beats=0.25 |
| `spiral_echo__quarter_down2` | delay_beats=0.25, shift_semitones=-2.0 |

### tempo_bridge — Tempo Bridge (BPM Ramp / Half-Double) (3 variants)

| variant | params |
|---|---|
| `tempo_bridge__12bar` | ramp_bars=12 |
| `tempo_bridge__24bar` | ramp_bars=24 |
| `tempo_bridge__8bar` | ramp_bars=8 |

### three_deck_layer — 3-Deck Layering (Glue Layer) (2 variants)

| variant | params |
|---|---|
| `three_deck_layer__12bar` | swap_bar=12 |
| `three_deck_layer__16bar` | swap_bar=16 |

### transform_gate_loop — Transform Gate Loop (Zabiela EFX Transform) (12 variants)

| variant | params |
|---|---|
| `transform_gate_loop__2bar` | gate_bars=2 |
| `transform_gate_loop__2bar_half` | gate_bars=2, duty_cycle=0.5 |
| `transform_gate_loop__2bar_open` | gate_bars=2, duty_cycle=0.65 |
| `transform_gate_loop__2bar_tight` | gate_bars=2, duty_cycle=0.35 |
| `transform_gate_loop__4bar` | gate_bars=4 |
| `transform_gate_loop__4bar_half` | gate_bars=4, duty_cycle=0.5 |
| `transform_gate_loop__4bar_open` | gate_bars=4, duty_cycle=0.65 |
| `transform_gate_loop__4bar_tight` | gate_bars=4, duty_cycle=0.35 |
| `transform_gate_loop__8bar` | gate_bars=8 |
| `transform_gate_loop__8bar_half` | gate_bars=8, duty_cycle=0.5 |
| `transform_gate_loop__8bar_open` | gate_bars=8, duty_cycle=0.65 |
| `transform_gate_loop__8bar_tight` | gate_bars=8, duty_cycle=0.35 |

### vocal_chop_build — Vocal-Chop Build (2 variants)

| variant | params |
|---|---|
| `vocal_chop_build__4bar` | build_bars=4 |
| `vocal_chop_build__8bar` | build_bars=8 |

### vocal_punchline_snap — Vocal Punchline Drop Snap (3 variants)

| variant | params |
|---|---|
| `vocal_punchline_snap__standard` | void_ms=175.0 |
| `vocal_punchline_snap__tight` | void_ms=150.0 |
| `vocal_punchline_snap__wide` | void_ms=200.0 |

### wordplay — Wordplay (2 variants)

| variant | params |
|---|---|
| `wordplay__echo_out` | exit='echo_out' |
| `wordplay__hard_cut` | exit='hard_cut' |

## Registered but not directly renderable

These bases carry preset axes (so variants are generated)
but have no function in the merged technique map — e.g.
`kind: "overlay"` entries, which compose pre/post a base
render (§6, operator 2) instead of rendering directly.
`get_variant` raises `KeyError` for them:

- `riser_ducking_overlay`
- `slip_mode_flourish`

## Regenerating

This catalog regenerates from the live registry. A merge pass
re-runs `build_variants()` once all domain modules have landed
and rewrites this file with the same generator (run from the
repo root):

```bash
cat > /tmp/gen_variants_md.py <<'PY'
import sys
from collections import Counter

sys.path.insert(0, ".")
from engine import meta, variants

all_meta = meta.all_meta()
reg = variants.build_variants()
per_base = Counter(v["base"] for v in reg.values())
core_n = sum(n for b, n in per_base.items() if b in meta.CORE_META)
core_b = sum(1 for b in per_base if b in meta.CORE_META)
no_fn = sorted(b for b in per_base if b not in variants._FUNCS)

out = []
out.append("# VARIANTS — generated variant catalog")
out.append("")
out.append("Variants are base techniques x named presets on their declared")
out.append("discrete parameter axes (FRAMEWORK.md §6, operator 1; axes are")
out.append('the `"presets"` maps in each technique\'s `params`, §3). The')
out.append("registry lives in `engine/variants.py` and is **generated,")
out.append("never hand-listed**: `VARIANTS = build_variants()` enumerates")
out.append("`meta.all_meta()` at import time.")
out.append("")
out.append(f"**Snapshot: {len(reg)} variants across {len(per_base)} base "
           f"techniques** ({core_n} variants across {core_b} core-bank "
           "bases; the rest arrive via domain modules, FRAMEWORK.md §7).")
out.append("This file is a snapshot of one generation run — see")
out.append("*Regenerating* below.")
out.append("")
out.append("## Naming scheme")
out.append("")
out.append("- **Single-axis:** `<base>__<preset>` — one variant per preset")
out.append("  on the base's FIRST preset axis.")
out.append("  e.g. `eq_blend__16bar` = eq_blend with `blend_bars=16`.")
out.append("- **Pairwise:** `<base>__<p1>_<p2>` — combinations of the first")
out.append("  two preset axes, capped at 9 combos per technique.")
out.append("  e.g. `brake_stop__long_exp` = `stop_beats=2.0, curve='exp'`.")
out.append("")
out.append("Render any variant with "
           "`variants.render_variant(name, a, b, sr, **ctx)`;")
out.append("resolve without rendering via `variants.get_variant(name)`,")
out.append("which returns `(fn, preset_kwargs)` and raises `KeyError` on")
out.append("unknown ids. Every variant inherits its base technique's")
out.append('evidence, recorded as `"inherited from <base>"`.')
out.append("")
out.append("Demo coverage: `demos/ext_variants.py` registers a "
           "representative")
out.append("sample (first single-axis variant + first pairwise combo per")
out.append("core base, capped at 40) through the standard demo pipeline.")
out.append("")
out.append("## Catalog")
for base in sorted(per_base):
    title = all_meta.get(base, {}).get("title", base)
    out.append("")
    out.append(f"### {base} — {title} ({per_base[base]} variants)")
    out.append("")
    out.append("| variant | params |")
    out.append("|---|---|")
    for vid in sorted(v for v in reg if reg[v]["base"] == base):
        params = ", ".join(f"{k}={v!r}"
                           for k, v in reg[vid]["params"].items())
        out.append(f"| `{vid}` | {params} |")
if no_fn:
    out.append("")
    out.append("## Registered but not directly renderable")
    out.append("")
    out.append("These bases carry preset axes (so variants are generated)")
    out.append("but have no function in the merged technique map — e.g.")
    out.append("`kind: \"overlay\"` entries, which compose pre/post a base")
    out.append("render (§6, operator 2) instead of rendering directly.")
    out.append("`get_variant` raises `KeyError` for them:")
    out.append("")
    for b in no_fn:
        out.append(f"- `{b}`")
out.append("")
out.append("## Regenerating")
out.append("")
out.append("This catalog regenerates from the live registry. A merge pass")
out.append("re-runs `build_variants()` once all domain modules have landed")
out.append("and rewrites this file with the same generator (run from the")
out.append("repo root):")
out.append("")
out.append("```bash")
out.append("cat > /tmp/gen_variants_md.py <<'PY'")
out.append(open(__file__).read().rstrip())
out.append("PY")
out.append("python3 /tmp/gen_variants_md.py > VARIANTS.md")
out.append("```")
print("\n".join(out))
PY
python3 /tmp/gen_variants_md.py > VARIANTS.md
```
