# VARIANTS — generated variant catalog

Variants are base techniques x named presets on their declared
discrete parameter axes (FRAMEWORK.md §6, operator 1; axes are
the `"presets"` maps in each technique's `params`, §3). The
registry lives in `engine/variants.py` and is **generated,
never hand-listed**: `VARIANTS = build_variants()` enumerates
`meta.all_meta()` at import time.

**Snapshot: 986 variants across 82 base techniques** (117 variants across 29 core-bank bases; the rest arrive via domain modules, FRAMEWORK.md §7).
This file is a snapshot of one generation run — see
*Regenerating* below.

## Naming scheme

- **Single-axis:** `<base>__<preset>` — one variant per preset
  on the base's FIRST preset axis.
  e.g. `eq_blend__16bar` = eq_blend with `blend_bars=16`.
- **Pairwise:** `<base>__<p1>_<p2>` — combinations of the first
  two preset axes, capped at 9 combos per technique.
  e.g. `brake_stop__long_exp` = `stop_beats=2.0, curve='exp'`.

Phase 24 (ENUMERATION.md) extended the walk past the first two
axes: singles on every axis and combos on every axis pair are
admitted when the id is nameable (exactly one parameter set
claims it) and every preset set is non-default — a default leg
renders as its single, so default-legged combos are parameter
notes, not variants. The legacy surface above is generated
exactly as before and never delisted.

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

### aging_echo — Aging Echo (Dub Feedback-Tone Echo) (11 variants)

| variant | params |
|---|---|
| `aging_echo__bright` | cutoff_hz=8000.0 |
| `aging_echo__dark` | cutoff_hz=2000.0 |
| `aging_echo__dotted` | beat_div=0.75 |
| `aging_echo__dotted_bright` | beat_div=0.75, cutoff_hz=8000.0 |
| `aging_echo__dotted_dark` | beat_div=0.75, cutoff_hz=2000.0 |
| `aging_echo__full` | beat_div=1.0 |
| `aging_echo__full_bright` | beat_div=1.0, cutoff_hz=8000.0 |
| `aging_echo__full_dark` | beat_div=1.0, cutoff_hz=2000.0 |
| `aging_echo__quarter` | beat_div=0.25 |
| `aging_echo__quarter_bright` | beat_div=0.25, cutoff_hz=8000.0 |
| `aging_echo__quarter_dark` | beat_div=0.25, cutoff_hz=2000.0 |

### backspin — Backspin (Spinback) (3 variants)

| variant | params |
|---|---|
| `backspin__half` | spin_beats=0.5 |
| `backspin__one` | spin_beats=1.0 |
| `backspin__two` | spin_beats=2.0 |

### beatslicer_shuffle — BeatSlicer Shuffle (Buffer Slice-Permutation Build) (24 variants)

| variant | params |
|---|---|
| `beatslicer_shuffle__bookends` | pattern='bookends' |
| `beatslicer_shuffle__bookends_off` | pattern='bookends', buzz=0 |
| `beatslicer_shuffle__bookends_one` | pattern='bookends', buffer_bars=1 |
| `beatslicer_shuffle__bookends_two` | pattern='bookends', buffer_bars=2 |
| `beatslicer_shuffle__halves` | pattern='halves' |
| `beatslicer_shuffle__halves_off` | pattern='halves', buzz=0 |
| `beatslicer_shuffle__halves_one` | pattern='halves', buffer_bars=1 |
| `beatslicer_shuffle__halves_two` | pattern='halves', buffer_bars=2 |
| `beatslicer_shuffle__inside_out` | pattern='inside_out' |
| `beatslicer_shuffle__inside_out_off` | pattern='inside_out', buzz=0 |
| `beatslicer_shuffle__inside_out_one` | pattern='inside_out', buffer_bars=1 |
| `beatslicer_shuffle__inside_out_two` | pattern='inside_out', buffer_bars=2 |
| `beatslicer_shuffle__off` | buzz=0 |
| `beatslicer_shuffle__reverse` | pattern='reverse' |
| `beatslicer_shuffle__reverse_off` | pattern='reverse', buzz=0 |
| `beatslicer_shuffle__reverse_one` | pattern='reverse', buffer_bars=1 |
| `beatslicer_shuffle__reverse_two` | pattern='reverse', buffer_bars=2 |
| `beatslicer_shuffle__stride` | pattern='stride' |
| `beatslicer_shuffle__stride_one` | pattern='stride', buffer_bars=1 |
| `beatslicer_shuffle__swap_pairs` | pattern='swap_pairs' |
| `beatslicer_shuffle__swap_pairs_off` | pattern='swap_pairs', buzz=0 |
| `beatslicer_shuffle__swap_pairs_two` | pattern='swap_pairs', buffer_bars=2 |
| `beatslicer_shuffle__two` | buffer_bars=2 |
| `beatslicer_shuffle__two_off` | buffer_bars=2, buzz=0 |

### bed_tempo_switch — Bed Tempo Switch (Ambient Third-Deck Cover) (3 variants)

| variant | params |
|---|---|
| `bed_tempo_switch__2bar` | bed_bars=2 |
| `bed_tempo_switch__4bar` | bed_bars=4 |
| `bed_tempo_switch__8bar` | bed_bars=8 |

### brake_stop — Brake / Tape Stop (13 variants)

| variant | params |
|---|---|
| `brake_stop__linear` | curve='linear' |
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

### brake_tempo_land — Brake Tempo Land (Metered Brake to Target Tempo) (10 variants)

| variant | params |
|---|---|
| `brake_tempo_land__deep` | target_ratio=0.7 |
| `brake_tempo_land__dramatic` | land_beats=4 |
| `brake_tempo_land__dramatic_deep` | land_beats=4, target_ratio=0.7 |
| `brake_tempo_land__dramatic_gentle` | land_beats=4, target_ratio=0.9 |
| `brake_tempo_land__dramatic_standard` | land_beats=4, target_ratio=0.8 |
| `brake_tempo_land__gentle` | target_ratio=0.9 |
| `brake_tempo_land__quick` | land_beats=2 |
| `brake_tempo_land__quick_deep` | land_beats=2, target_ratio=0.7 |
| `brake_tempo_land__quick_gentle` | land_beats=2, target_ratio=0.9 |
| `brake_tempo_land__quick_standard` | land_beats=2, target_ratio=0.8 |

### breakdown_swap — Breakdown Swap (Beat Entry Under Open Space) (2 variants)

| variant | params |
|---|---|
| `breakdown_swap__16bar` | swap_bars=16 |
| `breakdown_swap__8bar` | swap_bars=8 |

### build_to_drop — Build-to-Drop (Dual-Build Layering) (3 variants)

| variant | params |
|---|---|
| `build_to_drop__16bar` | build_bars=16 |
| `build_to_drop__32bar` | build_bars=32 |
| `build_to_drop__8bar` | build_bars=8 |

### continuous_drop — Continuous Drop (Drop-to-Drop Relay) (3 variants)

| variant | params |
|---|---|
| `continuous_drop__16bar` | stage_bars=16 |
| `continuous_drop__4bar` | stage_bars=4 |
| `continuous_drop__8bar` | stage_bars=8 |

### crush_degrade — Crush Degrade (Bit-Reduction Exit) (14 variants)

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
| `crush_degrade__long` | bars=8 |
| `crush_degrade__short` | bars=2 |

### cue_tap_walk — Cue Tap Walk (Decelerating Cue Taps) (13 variants)

| variant | params |
|---|---|
| `cue_tap_walk__double` | taps=2 |
| `cue_tap_walk__double_long` | taps=2, walk_beats=8 |
| `cue_tap_walk__double_quick` | taps=2, walk_beats=2 |
| `cue_tap_walk__double_standard` | taps=2, walk_beats=4 |
| `cue_tap_walk__long` | taps=8 |
| `cue_tap_walk__long_long` | taps=8, walk_beats=8 |
| `cue_tap_walk__long_quick` | taps=8, walk_beats=2 |
| `cue_tap_walk__long_standard` | taps=8, walk_beats=4 |
| `cue_tap_walk__quick` | walk_beats=2 |
| `cue_tap_walk__standard` | taps=4 |
| `cue_tap_walk__standard_long` | taps=4, walk_beats=8 |
| `cue_tap_walk__standard_quick` | taps=4, walk_beats=2 |
| `cue_tap_walk__standard_standard` | taps=4, walk_beats=4 |

### cyclic_speed_dip — Cyclic Speed Dip (Downer) (18 variants)

| variant | params |
|---|---|
| `cyclic_speed_dip__16bar` | dip_bars=16 |
| `cyclic_speed_dip__4bar` | dip_bars=4 |
| `cyclic_speed_dip__deep` | depth=0.7 |
| `cyclic_speed_dip__deep_16bar` | depth=0.7, dip_bars=16 |
| `cyclic_speed_dip__deep_4bar` | depth=0.7, dip_bars=4 |
| `cyclic_speed_dip__half_bar` | rate_beats=2.0 |
| `cyclic_speed_dip__half_bar_16bar` | rate_beats=2.0, dip_bars=16 |
| `cyclic_speed_dip__half_bar_4bar` | rate_beats=2.0, dip_bars=4 |
| `cyclic_speed_dip__half_bar_deep` | rate_beats=2.0, depth=0.7 |
| `cyclic_speed_dip__half_bar_shallow` | rate_beats=2.0, depth=0.25 |
| `cyclic_speed_dip__shallow` | depth=0.25 |
| `cyclic_speed_dip__shallow_16bar` | depth=0.25, dip_bars=16 |
| `cyclic_speed_dip__shallow_4bar` | depth=0.25, dip_bars=4 |
| `cyclic_speed_dip__two_bar` | rate_beats=8.0 |
| `cyclic_speed_dip__two_bar_16bar` | rate_beats=8.0, dip_bars=16 |
| `cyclic_speed_dip__two_bar_4bar` | rate_beats=8.0, dip_bars=4 |
| `cyclic_speed_dip__two_bar_deep` | rate_beats=8.0, depth=0.7 |
| `cyclic_speed_dip__two_bar_shallow` | rate_beats=8.0, depth=0.25 |

### delay_drum_roll — Delay Drum Roll (Wet-Slam Roll Illusion) (7 variants)

| variant | params |
|---|---|
| `delay_drum_roll__quarter` | delay_beats=0.25 |
| `delay_drum_roll__short` | roll_beats=2 |
| `delay_drum_roll__short_half` | roll_beats=2, delay_beats=0.5 |
| `delay_drum_roll__short_quarter` | roll_beats=2, delay_beats=0.25 |
| `delay_drum_roll__standard` | roll_beats=4 |
| `delay_drum_roll__standard_half` | roll_beats=4, delay_beats=0.5 |
| `delay_drum_roll__standard_quarter` | roll_beats=4, delay_beats=0.25 |

### djfx_microloop — DJFX Microloop (Free-Time Grain Loop) (18 variants)

| variant | params |
|---|---|
| `djfx_microloop__1bar` | loop_bars=1 |
| `djfx_microloop__4bar` | loop_bars=4 |
| `djfx_microloop__hold` | mode='hold' |
| `djfx_microloop__hold_1bar` | mode='hold', loop_bars=1 |
| `djfx_microloop__hold_4bar` | mode='hold', loop_bars=4 |
| `djfx_microloop__stop` | mode='stop' |
| `djfx_microloop__stop_1bar` | mode='stop', loop_bars=1 |
| `djfx_microloop__stop_4bar` | mode='stop', loop_bars=4 |
| `djfx_microloop__tight` | length_ms=30.0 |
| `djfx_microloop__tight_1bar` | length_ms=30.0, loop_bars=1 |
| `djfx_microloop__tight_4bar` | length_ms=30.0, loop_bars=4 |
| `djfx_microloop__tight_hold` | length_ms=30.0, mode='hold' |
| `djfx_microloop__tight_stop` | length_ms=30.0, mode='stop' |
| `djfx_microloop__wide` | length_ms=230.0 |
| `djfx_microloop__wide_1bar` | length_ms=230.0, loop_bars=1 |
| `djfx_microloop__wide_4bar` | length_ms=230.0, loop_bars=4 |
| `djfx_microloop__wide_hold` | length_ms=230.0, mode='hold' |
| `djfx_microloop__wide_stop` | length_ms=230.0, mode='stop' |

### double_drop — Double Drop (Dual-Build Collision) (2 variants)

| variant | params |
|---|---|
| `double_drop__16bar` | drop_at_bar=16 |
| `double_drop__8bar` | drop_at_bar=8 |

### downlifter_exit — Downlifter Exit (Descending Sweep Seam Mask) (24 variants)

| variant | params |
|---|---|
| `downlifter_exit__half` | sweep_bars=0.5 |
| `downlifter_exit__half_loud` | sweep_bars=0.5, level_db=-6.0 |
| `downlifter_exit__half_low` | sweep_bars=0.5, f_end=300.0 |
| `downlifter_exit__half_mid` | sweep_bars=0.5, f_end=800.0 |
| `downlifter_exit__half_sub` | sweep_bars=0.5, f_end=120.0 |
| `downlifter_exit__half_under` | sweep_bars=0.5, level_db=-12.0 |
| `downlifter_exit__loud` | level_db=-6.0 |
| `downlifter_exit__mid` | f_end=800.0 |
| `downlifter_exit__mid_loud` | f_end=800.0, level_db=-6.0 |
| `downlifter_exit__mid_under` | f_end=800.0, level_db=-12.0 |
| `downlifter_exit__one` | sweep_bars=1.0 |
| `downlifter_exit__one_low` | sweep_bars=1.0, f_end=300.0 |
| `downlifter_exit__one_mid` | sweep_bars=1.0, f_end=800.0 |
| `downlifter_exit__one_sub` | sweep_bars=1.0, f_end=120.0 |
| `downlifter_exit__sub` | f_end=120.0 |
| `downlifter_exit__sub_loud` | f_end=120.0, level_db=-6.0 |
| `downlifter_exit__sub_under` | f_end=120.0, level_db=-12.0 |
| `downlifter_exit__two` | sweep_bars=2.0 |
| `downlifter_exit__two_loud` | sweep_bars=2.0, level_db=-6.0 |
| `downlifter_exit__two_low` | sweep_bars=2.0, f_end=300.0 |
| `downlifter_exit__two_mid` | sweep_bars=2.0, f_end=800.0 |
| `downlifter_exit__two_sub` | sweep_bars=2.0, f_end=120.0 |
| `downlifter_exit__two_under` | sweep_bars=2.0, level_db=-12.0 |
| `downlifter_exit__under` | level_db=-12.0 |

### drop_chop — Drop Chop (Alternating Drop Ownership) (14 variants)

| variant | params |
|---|---|
| `drop_chop__1bar` | chop_bars=1 |
| `drop_chop__1bar_x1` | chop_bars=1, rounds=1 |
| `drop_chop__1bar_x2` | chop_bars=1, rounds=2 |
| `drop_chop__1bar_x4` | chop_bars=1, rounds=4 |
| `drop_chop__2bar` | chop_bars=2 |
| `drop_chop__2bar_x1` | chop_bars=2, rounds=1 |
| `drop_chop__2bar_x2` | chop_bars=2, rounds=2 |
| `drop_chop__2bar_x4` | chop_bars=2, rounds=4 |
| `drop_chop__4bar` | chop_bars=4 |
| `drop_chop__4bar_x1` | chop_bars=4, rounds=1 |
| `drop_chop__4bar_x2` | chop_bars=4, rounds=2 |
| `drop_chop__4bar_x4` | chop_bars=4, rounds=4 |
| `drop_chop__x1` | rounds=1 |
| `drop_chop__x4` | rounds=4 |

### drop_insert — Drop Insert (Guest-Bar Drop Substitution) (3 variants)

| variant | params |
|---|---|
| `drop_insert__1bar` | insert_bars=1 |
| `drop_insert__2bar` | insert_bars=2 |
| `drop_insert__4bar` | insert_bars=4 |

### drum_bridge — Drum Bridge (Atonal Neutral Zone) (3 variants)

| variant | params |
|---|---|
| `drum_bridge__12bar` | interlude_bars=12 |
| `drum_bridge__16bar` | interlude_bars=16 |
| `drum_bridge__8bar` | interlude_bars=8 |

### dual_loop_composite — Dual-Loop Composite (EZ Loop-as-Instrument) (14 variants)

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
| `dual_loop_composite__high` | role_split_hz=350 |
| `dual_loop_composite__low` | role_split_hz=150 |

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

### echo_out_reset — Echo Out Reset (Metronome Reset, Any-BPM Drop) (10 variants)

| variant | params |
|---|---|
| `echo_out_reset__1bar` | tail_bars=1 |
| `echo_out_reset__1bar_dotted` | tail_bars=1, beat_div=0.75 |
| `echo_out_reset__1bar_half` | tail_bars=1, beat_div=0.5 |
| `echo_out_reset__2bar` | tail_bars=2 |
| `echo_out_reset__2bar_dotted` | tail_bars=2, beat_div=0.75 |
| `echo_out_reset__2bar_half` | tail_bars=2, beat_div=0.5 |
| `echo_out_reset__4bar` | tail_bars=4 |
| `echo_out_reset__4bar_dotted` | tail_bars=4, beat_div=0.75 |
| `echo_out_reset__4bar_half` | tail_bars=4, beat_div=0.5 |
| `echo_out_reset__dotted` | beat_div=0.75 |

### echo_tempo_lift — Echo Tempo Lift (3/4-Beat Echo Grid Lift) (7 variants)

| variant | params |
|---|---|
| `echo_tempo_lift__half` | delay_beats=0.5 |
| `echo_tempo_lift__short` | tail_repeats=4 |
| `echo_tempo_lift__short_half` | tail_repeats=4, delay_beats=0.5 |
| `echo_tempo_lift__short_three_quarter` | tail_repeats=4, delay_beats=0.75 |
| `echo_tempo_lift__standard` | tail_repeats=8 |
| `echo_tempo_lift__standard_half` | tail_repeats=8, delay_beats=0.5 |
| `echo_tempo_lift__standard_three_quarter` | tail_repeats=8, delay_beats=0.75 |

### eq_blend — EQ Blend (3-Band Frequency Replacement) (4 variants)

| variant | params |
|---|---|
| `eq_blend__16bar` | blend_bars=16 |
| `eq_blend__32bar` | blend_bars=32 |
| `eq_blend__64bar` | blend_bars=64 |
| `eq_blend__8bar` | blend_bars=8 |

### fader_synth — Fader Synth (Source-Replacing Fader Oscillator) (68 variants)

| variant | params |
|---|---|
| `fader_synth__arp` | ride='arp' |
| `fader_synth__arp_down` | ride='arp', base_octave=-1 |
| `fader_synth__arp_japanese` | ride='arp', scale='japanese' |
| `fader_synth__arp_long` | ride='arp', zone_bars=8 |
| `fader_synth__arp_minor` | ride='arp', scale='minor' |
| `fader_synth__arp_short` | ride='arp', zone_bars=2 |
| `fader_synth__arp_up` | ride='arp', base_octave=1 |
| `fader_synth__down` | base_octave=-1 |
| `fader_synth__down_long` | base_octave=-1, zone_bars=8 |
| `fader_synth__down_short` | base_octave=-1, zone_bars=2 |
| `fader_synth__glide` | ride='glide' |
| `fader_synth__glide_down` | ride='glide', base_octave=-1 |
| `fader_synth__glide_long` | ride='glide', zone_bars=8 |
| `fader_synth__glide_short` | ride='glide', zone_bars=2 |
| `fader_synth__glide_up` | ride='glide', base_octave=1 |
| `fader_synth__hold` | ride='hold' |
| `fader_synth__hold_down` | ride='hold', base_octave=-1 |
| `fader_synth__hold_long` | ride='hold', zone_bars=8 |
| `fader_synth__hold_short` | ride='hold', zone_bars=2 |
| `fader_synth__hold_up` | ride='hold', base_octave=1 |
| `fader_synth__japanese` | scale='japanese' |
| `fader_synth__japanese_down` | scale='japanese', base_octave=-1 |
| `fader_synth__japanese_long` | scale='japanese', zone_bars=8 |
| `fader_synth__japanese_short` | scale='japanese', zone_bars=2 |
| `fader_synth__japanese_up` | scale='japanese', base_octave=1 |
| `fader_synth__long` | zone_bars=8 |
| `fader_synth__minor` | scale='minor' |
| `fader_synth__minor_down` | scale='minor', base_octave=-1 |
| `fader_synth__minor_h` | scale='minor_h' |
| `fader_synth__minor_h_down` | scale='minor_h', base_octave=-1 |
| `fader_synth__minor_h_long` | scale='minor_h', zone_bars=8 |
| `fader_synth__minor_h_short` | scale='minor_h', zone_bars=2 |
| `fader_synth__minor_h_up` | scale='minor_h', base_octave=1 |
| `fader_synth__minor_long` | scale='minor', zone_bars=8 |
| `fader_synth__minor_short` | scale='minor', zone_bars=2 |
| `fader_synth__minor_up` | scale='minor', base_octave=1 |
| `fader_synth__saw` | waveform='saw' |
| `fader_synth__saw_arp` | waveform='saw', ride='arp' |
| `fader_synth__saw_glide` | waveform='saw', ride='glide' |
| `fader_synth__saw_hold` | waveform='saw', ride='hold' |
| `fader_synth__saw_steps` | waveform='saw', ride='steps' |
| `fader_synth__short` | zone_bars=2 |
| `fader_synth__sine` | waveform='sine' |
| `fader_synth__sine_arp` | waveform='sine', ride='arp' |
| `fader_synth__sine_down` | waveform='sine', base_octave=-1 |
| `fader_synth__sine_glide` | waveform='sine', ride='glide' |
| `fader_synth__sine_hold` | waveform='sine', ride='hold' |
| `fader_synth__sine_japanese` | waveform='sine', scale='japanese' |
| `fader_synth__sine_long` | waveform='sine', zone_bars=8 |
| `fader_synth__sine_minor` | waveform='sine', scale='minor' |
| `fader_synth__sine_minor_h` | waveform='sine', scale='minor_h' |
| `fader_synth__sine_short` | waveform='sine', zone_bars=2 |
| `fader_synth__sine_steps` | waveform='sine', ride='steps' |
| `fader_synth__sine_up` | waveform='sine', base_octave=1 |
| `fader_synth__square` | waveform='square' |
| `fader_synth__square_arp` | waveform='square', ride='arp' |
| `fader_synth__square_down` | waveform='square', base_octave=-1 |
| `fader_synth__square_glide` | waveform='square', ride='glide' |
| `fader_synth__square_hold` | waveform='square', ride='hold' |
| `fader_synth__square_japanese` | waveform='square', scale='japanese' |
| `fader_synth__square_long` | waveform='square', zone_bars=8 |
| `fader_synth__square_minor` | waveform='square', scale='minor' |
| `fader_synth__square_minor_h` | waveform='square', scale='minor_h' |
| `fader_synth__square_short` | waveform='square', zone_bars=2 |
| `fader_synth__square_up` | waveform='square', base_octave=1 |
| `fader_synth__up` | base_octave=1 |
| `fader_synth__up_long` | base_octave=1, zone_bars=8 |
| `fader_synth__up_short` | base_octave=1, zone_bars=2 |

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

### flanger_sweep — Flanger Sweep (Jet Comb Build/Exit) (14 variants)

| variant | params |
|---|---|
| `flanger_sweep__deep` | depth_ms=3.8 |
| `flanger_sweep__long` | sweep_bars=16 |
| `flanger_sweep__long_deep` | sweep_bars=16, depth_ms=3.8 |
| `flanger_sweep__long_jet` | sweep_bars=16, depth_ms=2.2 |
| `flanger_sweep__long_subtle` | sweep_bars=16, depth_ms=1.2 |
| `flanger_sweep__standard` | sweep_bars=8 |
| `flanger_sweep__standard_deep` | sweep_bars=8, depth_ms=3.8 |
| `flanger_sweep__standard_jet` | sweep_bars=8, depth_ms=2.2 |
| `flanger_sweep__standard_subtle` | sweep_bars=8, depth_ms=1.2 |
| `flanger_sweep__subtle` | depth_ms=1.2 |
| `flanger_sweep__tight` | sweep_bars=4 |
| `flanger_sweep__tight_deep` | sweep_bars=4, depth_ms=3.8 |
| `flanger_sweep__tight_jet` | sweep_bars=4, depth_ms=2.2 |
| `flanger_sweep__tight_subtle` | sweep_bars=4, depth_ms=1.2 |

### formant_morph_exit — Formant Morph Exit (Vowel-Series Spectral Morph) (66 variants)

| variant | params |
|---|---|
| `formant_morph_exit__aeiou` | path='aeiou' |
| `formant_morph_exit__aeiou_english` | path='aeiou', table='english' |
| `formant_morph_exit__aeiou_german` | path='aeiou', table='german' |
| `formant_morph_exit__ai` | path='ai' |
| `formant_morph_exit__ai_english` | path='ai', table='english' |
| `formant_morph_exit__ai_german` | path='ai', table='german' |
| `formant_morph_exit__ai_light` | path='ai', mix=0.7 |
| `formant_morph_exit__ai_long` | path='ai', zone_bars=8 |
| `formant_morph_exit__ai_present` | path='ai', sharp=1.8 |
| `formant_morph_exit__ai_short` | path='ai', zone_bars=2 |
| `formant_morph_exit__ai_soft` | path='ai', sharp=0.6 |
| `formant_morph_exit__ai_tight` | path='ai', fade_bars=0.25 |
| `formant_morph_exit__ai_total` | path='ai', mix=1.0 |
| `formant_morph_exit__german` | table='german' |
| `formant_morph_exit__german_light` | table='german', mix=0.7 |
| `formant_morph_exit__german_long` | table='german', zone_bars=8 |
| `formant_morph_exit__german_present` | table='german', sharp=1.8 |
| `formant_morph_exit__german_short` | table='german', zone_bars=2 |
| `formant_morph_exit__german_soft` | table='german', sharp=0.6 |
| `formant_morph_exit__german_tight` | table='german', fade_bars=0.25 |
| `formant_morph_exit__german_total` | table='german', mix=1.0 |
| `formant_morph_exit__light` | mix=0.7 |
| `formant_morph_exit__light_tight` | mix=0.7, fade_bars=0.25 |
| `formant_morph_exit__long` | zone_bars=8 |
| `formant_morph_exit__long_light` | zone_bars=8, mix=0.7 |
| `formant_morph_exit__long_tight` | zone_bars=8, fade_bars=0.25 |
| `formant_morph_exit__long_total` | zone_bars=8, mix=1.0 |
| `formant_morph_exit__ou` | path='ou' |
| `formant_morph_exit__ou_english` | path='ou', table='english' |
| `formant_morph_exit__ou_german` | path='ou', table='german' |
| `formant_morph_exit__ou_light` | path='ou', mix=0.7 |
| `formant_morph_exit__ou_long` | path='ou', zone_bars=8 |
| `formant_morph_exit__ou_present` | path='ou', sharp=1.8 |
| `formant_morph_exit__ou_short` | path='ou', zone_bars=2 |
| `formant_morph_exit__ou_soft` | path='ou', sharp=0.6 |
| `formant_morph_exit__ou_tight` | path='ou', fade_bars=0.25 |
| `formant_morph_exit__ou_total` | path='ou', mix=1.0 |
| `formant_morph_exit__ouiea` | path='ouiea' |
| `formant_morph_exit__ouiea_english` | path='ouiea', table='english' |
| `formant_morph_exit__ouiea_german` | path='ouiea', table='german' |
| `formant_morph_exit__ouiea_light` | path='ouiea', mix=0.7 |
| `formant_morph_exit__ouiea_long` | path='ouiea', zone_bars=8 |
| `formant_morph_exit__ouiea_present` | path='ouiea', sharp=1.8 |
| `formant_morph_exit__ouiea_short` | path='ouiea', zone_bars=2 |
| `formant_morph_exit__ouiea_soft` | path='ouiea', sharp=0.6 |
| `formant_morph_exit__ouiea_tight` | path='ouiea', fade_bars=0.25 |
| `formant_morph_exit__ouiea_total` | path='ouiea', mix=1.0 |
| `formant_morph_exit__present` | sharp=1.8 |
| `formant_morph_exit__present_light` | sharp=1.8, mix=0.7 |
| `formant_morph_exit__present_long` | sharp=1.8, zone_bars=8 |
| `formant_morph_exit__present_short` | sharp=1.8, zone_bars=2 |
| `formant_morph_exit__present_tight` | sharp=1.8, fade_bars=0.25 |
| `formant_morph_exit__present_total` | sharp=1.8, mix=1.0 |
| `formant_morph_exit__short` | zone_bars=2 |
| `formant_morph_exit__short_light` | zone_bars=2, mix=0.7 |
| `formant_morph_exit__short_tight` | zone_bars=2, fade_bars=0.25 |
| `formant_morph_exit__short_total` | zone_bars=2, mix=1.0 |
| `formant_morph_exit__soft` | sharp=0.6 |
| `formant_morph_exit__soft_light` | sharp=0.6, mix=0.7 |
| `formant_morph_exit__soft_long` | sharp=0.6, zone_bars=8 |
| `formant_morph_exit__soft_short` | sharp=0.6, zone_bars=2 |
| `formant_morph_exit__soft_tight` | sharp=0.6, fade_bars=0.25 |
| `formant_morph_exit__soft_total` | sharp=0.6, mix=1.0 |
| `formant_morph_exit__tight` | fade_bars=0.25 |
| `formant_morph_exit__total` | mix=1.0 |
| `formant_morph_exit__total_tight` | mix=1.0, fade_bars=0.25 |

### granular_freeze — Granular Freeze (Frozen-Moment Cloud Handoff) (14 variants)

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
| `granular_freeze__long` | cloud_bars=8 |
| `granular_freeze__short` | cloud_bars=2 |
| `granular_freeze__standard` | grain_ms=70.0 |
| `granular_freeze__standard_long` | grain_ms=70.0, cloud_bars=8 |
| `granular_freeze__standard_short` | grain_ms=70.0, cloud_bars=2 |
| `granular_freeze__standard_standard` | grain_ms=70.0, cloud_bars=4 |

### helix_catch — Helix Catch (Loop-Sampler Pitch-Ramp Hold & Release) (29 variants)

| variant | params |
|---|---|
| `helix_catch__bar` | capture_beats=4.0 |
| `helix_catch__bar_down_octave` | capture_beats=4.0, ramp_semitones=-12.0 |
| `helix_catch__bar_fixed` | capture_beats=4.0, ramp_semitones=0.0 |
| `helix_catch__bar_four` | capture_beats=4.0, hold_bars=4 |
| `helix_catch__bar_one` | capture_beats=4.0, hold_bars=1 |
| `helix_catch__bar_two` | capture_beats=4.0, hold_bars=2 |
| `helix_catch__bar_up_fifth` | capture_beats=4.0, ramp_semitones=7.0 |
| `helix_catch__beat` | capture_beats=1.0 |
| `helix_catch__beat_four` | capture_beats=1.0, hold_bars=4 |
| `helix_catch__beat_one` | capture_beats=1.0, hold_bars=1 |
| `helix_catch__beat_two` | capture_beats=1.0, hold_bars=2 |
| `helix_catch__down_octave` | ramp_semitones=-12.0 |
| `helix_catch__fixed` | ramp_semitones=0.0 |
| `helix_catch__four` | hold_bars=4 |
| `helix_catch__four_down_octave` | hold_bars=4, ramp_semitones=-12.0 |
| `helix_catch__four_fixed` | hold_bars=4, ramp_semitones=0.0 |
| `helix_catch__four_up_fifth` | hold_bars=4, ramp_semitones=7.0 |
| `helix_catch__half` | capture_beats=0.5 |
| `helix_catch__half_down_octave` | capture_beats=0.5, ramp_semitones=-12.0 |
| `helix_catch__half_fixed` | capture_beats=0.5, ramp_semitones=0.0 |
| `helix_catch__half_four` | capture_beats=0.5, hold_bars=4 |
| `helix_catch__half_one` | capture_beats=0.5, hold_bars=1 |
| `helix_catch__half_two` | capture_beats=0.5, hold_bars=2 |
| `helix_catch__half_up_fifth` | capture_beats=0.5, ramp_semitones=7.0 |
| `helix_catch__one` | hold_bars=1 |
| `helix_catch__one_down_octave` | hold_bars=1, ramp_semitones=-12.0 |
| `helix_catch__one_fixed` | hold_bars=1, ramp_semitones=0.0 |
| `helix_catch__one_up_fifth` | hold_bars=1, ramp_semitones=7.0 |
| `helix_catch__up_fifth` | ramp_semitones=7.0 |

### hook_drop_handoff — Hook-Drop Handoff (19 variants)

| variant | params |
|---|---|
| `hook_drop_handoff__2bar` | bloom_bars=2 |
| `hook_drop_handoff__2bar_linear` | bloom_bars=2, bloom_curve='linear' |
| `hook_drop_handoff__4bar` | bloom_bars=4 |
| `hook_drop_handoff__4bar_linear` | bloom_bars=4, bloom_curve='linear' |
| `hook_drop_handoff__60ms` | exit_fade_ms=60.0 |
| `hook_drop_handoff__60ms_2bar` | exit_fade_ms=60.0, bloom_bars=2 |
| `hook_drop_handoff__60ms_3bar` | exit_fade_ms=60.0, bloom_bars=3 |
| `hook_drop_handoff__60ms_4bar` | exit_fade_ms=60.0, bloom_bars=4 |
| `hook_drop_handoff__60ms_linear` | exit_fade_ms=60.0, bloom_curve='linear' |
| `hook_drop_handoff__70ms` | exit_fade_ms=70.0 |
| `hook_drop_handoff__70ms_2bar` | exit_fade_ms=70.0, bloom_bars=2 |
| `hook_drop_handoff__70ms_3bar` | exit_fade_ms=70.0, bloom_bars=3 |
| `hook_drop_handoff__70ms_4bar` | exit_fade_ms=70.0, bloom_bars=4 |
| `hook_drop_handoff__80ms` | exit_fade_ms=80.0 |
| `hook_drop_handoff__80ms_2bar` | exit_fade_ms=80.0, bloom_bars=2 |
| `hook_drop_handoff__80ms_3bar` | exit_fade_ms=80.0, bloom_bars=3 |
| `hook_drop_handoff__80ms_4bar` | exit_fade_ms=80.0, bloom_bars=4 |
| `hook_drop_handoff__80ms_linear` | exit_fade_ms=80.0, bloom_curve='linear' |
| `hook_drop_handoff__linear` | bloom_curve='linear' |

### hotcue_drop_swap — Hot-Cue Drop Swap (Drop Juggling) (3 variants)

| variant | params |
|---|---|
| `hotcue_drop_swap__2beat` | xfade_beats=2 |
| `hotcue_drop_swap__4beat` | xfade_beats=4 |
| `hotcue_drop_swap__8beat` | xfade_beats=8 |

### infinity_filter — Infinity Filter (Endless Barber-Pole Sweep Exit) (18 variants)

| variant | params |
|---|---|
| `infinity_filter__down` | direction=-1 |
| `infinity_filter__down_long` | direction=-1, sweep_bars=8 |
| `infinity_filter__down_one` | direction=-1, cycles=1.0 |
| `infinity_filter__down_short` | direction=-1, sweep_bars=2 |
| `infinity_filter__down_three` | direction=-1, cycles=3.0 |
| `infinity_filter__down_two` | direction=-1, cycles=2.0 |
| `infinity_filter__long` | sweep_bars=8 |
| `infinity_filter__one` | cycles=1.0 |
| `infinity_filter__one_long` | cycles=1.0, sweep_bars=8 |
| `infinity_filter__one_short` | cycles=1.0, sweep_bars=2 |
| `infinity_filter__short` | sweep_bars=2 |
| `infinity_filter__three` | cycles=3.0 |
| `infinity_filter__three_long` | cycles=3.0, sweep_bars=8 |
| `infinity_filter__three_short` | cycles=3.0, sweep_bars=2 |
| `infinity_filter__up` | direction=1 |
| `infinity_filter__up_one` | direction=1, cycles=1.0 |
| `infinity_filter__up_three` | direction=1, cycles=3.0 |
| `infinity_filter__up_two` | direction=1, cycles=2.0 |

### instant_double_stutter — Instant Double Stutter (Half-Beat Dual-Stream Splice) (3 variants)

| variant | params |
|---|---|
| `instant_double_stutter__1bar` | stutter_bars=1 |
| `instant_double_stutter__2bar` | stutter_bars=2 |
| `instant_double_stutter__4bar` | stutter_bars=4 |

### layered_fx_stack — Layered FX Stack (Echo + Filter + Reverb) (2 variants)

| variant | params |
|---|---|
| `layered_fx_stack__4bar` | echo_bars=4 |
| `layered_fx_stack__8bar` | echo_bars=8 |

### loop_click_bridge — Loop Click Bridge (Micro-Loop Metronome) (13 variants)

| variant | params |
|---|---|
| `loop_click_bridge__long` | click_ms=250 |
| `loop_click_bridge__long_long` | click_ms=250, click_bars=8 |
| `loop_click_bridge__long_standard` | click_ms=250, click_bars=4 |
| `loop_click_bridge__long_tight` | click_ms=250, click_bars=2 |
| `loop_click_bridge__short` | click_ms=100 |
| `loop_click_bridge__short_long` | click_ms=100, click_bars=8 |
| `loop_click_bridge__short_standard` | click_ms=100, click_bars=4 |
| `loop_click_bridge__short_tight` | click_ms=100, click_bars=2 |
| `loop_click_bridge__standard` | click_ms=150 |
| `loop_click_bridge__standard_long` | click_ms=150, click_bars=8 |
| `loop_click_bridge__standard_standard` | click_ms=150, click_bars=4 |
| `loop_click_bridge__standard_tight` | click_ms=150, click_bars=2 |
| `loop_click_bridge__tight` | click_bars=2 |

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

### notch_carve_sweep — Notch Carve Sweep (Dual State-Variable VCF) (8 variants)

| variant | params |
|---|---|
| `notch_carve_sweep__long` | sweep_bars=8 |
| `notch_carve_sweep__long_needle` | sweep_bars=8, q=24.0 |
| `notch_carve_sweep__long_wide` | sweep_bars=8, q=2.0 |
| `notch_carve_sweep__needle` | q=24.0 |
| `notch_carve_sweep__quick` | sweep_bars=2 |
| `notch_carve_sweep__quick_needle` | sweep_bars=2, q=24.0 |
| `notch_carve_sweep__quick_wide` | sweep_bars=2, q=2.0 |
| `notch_carve_sweep__wide` | q=2.0 |

### ooh_tail_pickup — Tail-Motif Pickup (14 variants)

| variant | params |
|---|---|
| `ooh_tail_pickup__long` | tail_bars=4 |
| `ooh_tail_pickup__long_present` | tail_bars=4, tail_level=0.65 |
| `ooh_tail_pickup__long_soft` | tail_bars=4, tail_level=0.35 |
| `ooh_tail_pickup__long_standard` | tail_bars=4, tail_level=0.5 |
| `ooh_tail_pickup__present` | tail_level=0.65 |
| `ooh_tail_pickup__short` | tail_bars=1 |
| `ooh_tail_pickup__short_present` | tail_bars=1, tail_level=0.65 |
| `ooh_tail_pickup__short_soft` | tail_bars=1, tail_level=0.35 |
| `ooh_tail_pickup__short_standard` | tail_bars=1, tail_level=0.5 |
| `ooh_tail_pickup__soft` | tail_level=0.35 |
| `ooh_tail_pickup__standard` | tail_bars=2 |
| `ooh_tail_pickup__standard_present` | tail_bars=2, tail_level=0.65 |
| `ooh_tail_pickup__standard_soft` | tail_bars=2, tail_level=0.35 |
| `ooh_tail_pickup__standard_standard` | tail_bars=2, tail_level=0.5 |

### pattern_gate_slicer — Pattern Gate Slicer (16-Step Gate Pattern) (31 variants)

| variant | params |
|---|---|
| `pattern_gate_slicer__2bar` | gate_bars=2 |
| `pattern_gate_slicer__8bar` | gate_bars=8 |
| `pattern_gate_slicer__8th` | step_beats=0.5 |
| `pattern_gate_slicer__8th_2bar` | step_beats=0.5, gate_bars=2 |
| `pattern_gate_slicer__8th_8bar` | step_beats=0.5, gate_bars=8 |
| `pattern_gate_slicer__8th_legato` | step_beats=0.5, mode='legato' |
| `pattern_gate_slicer__cascade` | pattern='cascade' |
| `pattern_gate_slicer__cascade_2bar` | pattern='cascade', gate_bars=2 |
| `pattern_gate_slicer__cascade_8bar` | pattern='cascade', gate_bars=8 |
| `pattern_gate_slicer__cascade_8th` | pattern='cascade', step_beats=0.5 |
| `pattern_gate_slicer__cascade_legato` | pattern='cascade', mode='legato' |
| `pattern_gate_slicer__cascade_quarter` | pattern='cascade', step_beats=1.0 |
| `pattern_gate_slicer__legato` | mode='legato' |
| `pattern_gate_slicer__legato_2bar` | mode='legato', gate_bars=2 |
| `pattern_gate_slicer__legato_8bar` | mode='legato', gate_bars=8 |
| `pattern_gate_slicer__pulse` | pattern='pulse' |
| `pattern_gate_slicer__pulse_2bar` | pattern='pulse', gate_bars=2 |
| `pattern_gate_slicer__pulse_8bar` | pattern='pulse', gate_bars=8 |
| `pattern_gate_slicer__pulse_8th` | pattern='pulse', step_beats=0.5 |
| `pattern_gate_slicer__pulse_legato` | pattern='pulse', mode='legato' |
| `pattern_gate_slicer__pulse_quarter` | pattern='pulse', step_beats=1.0 |
| `pattern_gate_slicer__quarter` | step_beats=1.0 |
| `pattern_gate_slicer__quarter_2bar` | step_beats=1.0, gate_bars=2 |
| `pattern_gate_slicer__quarter_8bar` | step_beats=1.0, gate_bars=8 |
| `pattern_gate_slicer__quarter_legato` | step_beats=1.0, mode='legato' |
| `pattern_gate_slicer__stutter` | pattern='stutter' |
| `pattern_gate_slicer__stutter_2bar` | pattern='stutter', gate_bars=2 |
| `pattern_gate_slicer__stutter_8bar` | pattern='stutter', gate_bars=8 |
| `pattern_gate_slicer__stutter_8th` | pattern='stutter', step_beats=0.5 |
| `pattern_gate_slicer__stutter_legato` | pattern='stutter', mode='legato' |
| `pattern_gate_slicer__stutter_quarter` | pattern='stutter', step_beats=1.0 |

### pattern_layer_bridge — Pattern Layer Bridge (Pattern Player Seam Layer) (23 variants)

| variant | params |
|---|---|
| `pattern_layer_bridge__build` | pattern='build' |
| `pattern_layer_bridge__build_kit808` | pattern='build', kit='kit808' |
| `pattern_layer_bridge__build_kit909` | pattern='build', kit='kit909' |
| `pattern_layer_bridge__build_long` | pattern='build', bars=16 |
| `pattern_layer_bridge__build_short` | pattern='build', bars=4 |
| `pattern_layer_bridge__foundation` | pattern='foundation' |
| `pattern_layer_bridge__foundation_kit808` | pattern='foundation', kit='kit808' |
| `pattern_layer_bridge__foundation_kit909` | pattern='foundation', kit='kit909' |
| `pattern_layer_bridge__foundation_long` | pattern='foundation', bars=16 |
| `pattern_layer_bridge__foundation_short` | pattern='foundation', bars=4 |
| `pattern_layer_bridge__groove` | pattern='groove' |
| `pattern_layer_bridge__groove_kit808` | pattern='groove', kit='kit808' |
| `pattern_layer_bridge__groove_kit909` | pattern='groove', kit='kit909' |
| `pattern_layer_bridge__kit808` | kit='kit808' |
| `pattern_layer_bridge__kit808_long` | kit='kit808', bars=16 |
| `pattern_layer_bridge__kit808_short` | kit='kit808', bars=4 |
| `pattern_layer_bridge__long` | bars=16 |
| `pattern_layer_bridge__roll` | pattern='roll' |
| `pattern_layer_bridge__roll_kit808` | pattern='roll', kit='kit808' |
| `pattern_layer_bridge__roll_kit909` | pattern='roll', kit='kit909' |
| `pattern_layer_bridge__roll_long` | pattern='roll', bars=16 |
| `pattern_layer_bridge__roll_short` | pattern='roll', bars=4 |
| `pattern_layer_bridge__short` | bars=4 |

### phaser_sweep — Phaser Sweep (Allpass Cascade) (18 variants)

| variant | params |
|---|---|
| `phaser_sweep__deep` | stages=6 |
| `phaser_sweep__duo` | stages=2 |
| `phaser_sweep__fast` | rate_bars=0.5 |
| `phaser_sweep__fast_deep` | rate_bars=0.5, stages=6 |
| `phaser_sweep__fast_duo` | rate_bars=0.5, stages=2 |
| `phaser_sweep__long` | sweep_bars=8 |
| `phaser_sweep__long_deep` | sweep_bars=8, stages=6 |
| `phaser_sweep__long_duo` | sweep_bars=8, stages=2 |
| `phaser_sweep__long_fast` | sweep_bars=8, rate_bars=0.5 |
| `phaser_sweep__long_slow` | sweep_bars=8, rate_bars=2.0 |
| `phaser_sweep__quick` | sweep_bars=2 |
| `phaser_sweep__quick_deep` | sweep_bars=2, stages=6 |
| `phaser_sweep__quick_duo` | sweep_bars=2, stages=2 |
| `phaser_sweep__quick_fast` | sweep_bars=2, rate_bars=0.5 |
| `phaser_sweep__quick_slow` | sweep_bars=2, rate_bars=2.0 |
| `phaser_sweep__slow` | rate_bars=2.0 |
| `phaser_sweep__slow_deep` | rate_bars=2.0, stages=6 |
| `phaser_sweep__slow_duo` | rate_bars=2.0, stages=2 |

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

### pre_filtered_echo — Pre-Filtered Echo (Dry+Wet Send Conditioning) (11 variants)

| variant | params |
|---|---|
| `pre_filtered_echo__dotted` | beat_div=0.75 |
| `pre_filtered_echo__dotted_open` | beat_div=0.75, cutoff_hz=1200.0 |
| `pre_filtered_echo__dotted_sub_only` | beat_div=0.75, cutoff_hz=120.0 |
| `pre_filtered_echo__full` | beat_div=1.0 |
| `pre_filtered_echo__full_open` | beat_div=1.0, cutoff_hz=1200.0 |
| `pre_filtered_echo__full_sub_only` | beat_div=1.0, cutoff_hz=120.0 |
| `pre_filtered_echo__open` | cutoff_hz=1200.0 |
| `pre_filtered_echo__quarter` | beat_div=0.25 |
| `pre_filtered_echo__quarter_open` | beat_div=0.25, cutoff_hz=1200.0 |
| `pre_filtered_echo__quarter_sub_only` | beat_div=0.25, cutoff_hz=120.0 |
| `pre_filtered_echo__sub_only` | cutoff_hz=120.0 |

### premade_tempo_bridge_edit — Pre-Made Tempo-Bridge Edit (Transition Track) (3 variants)

| variant | params |
|---|---|
| `premade_tempo_bridge_edit__16bar` | edit_bars=16 |
| `premade_tempo_bridge_edit__4bar` | edit_bars=4 |
| `premade_tempo_bridge_edit__8bar` | edit_bars=8 |

### pumper_exit — Pumper Exit (Downbeat Duck Pump Exit) (27 variants)

| variant | params |
|---|---|
| `pumper_exit__deep` | duck_db=-16.0 |
| `pumper_exit__deep_early16` | duck_db=-16.0, offset_beats=-0.0625 |
| `pumper_exit__deep_early4` | duck_db=-16.0, offset_beats=-0.25 |
| `pumper_exit__deep_early8` | duck_db=-16.0, offset_beats=-0.125 |
| `pumper_exit__deep_long` | duck_db=-16.0, pump_bars=8 |
| `pumper_exit__deep_on_grid` | duck_db=-16.0, offset_beats=0.0 |
| `pumper_exit__deep_short` | duck_db=-16.0, pump_bars=2 |
| `pumper_exit__early16` | offset_beats=-0.0625 |
| `pumper_exit__early16_long` | offset_beats=-0.0625, pump_bars=8 |
| `pumper_exit__early16_short` | offset_beats=-0.0625, pump_bars=2 |
| `pumper_exit__early8` | offset_beats=-0.125 |
| `pumper_exit__early8_long` | offset_beats=-0.125, pump_bars=8 |
| `pumper_exit__early8_short` | offset_beats=-0.125, pump_bars=2 |
| `pumper_exit__light` | duck_db=-6.0 |
| `pumper_exit__light_early16` | duck_db=-6.0, offset_beats=-0.0625 |
| `pumper_exit__light_early4` | duck_db=-6.0, offset_beats=-0.25 |
| `pumper_exit__light_early8` | duck_db=-6.0, offset_beats=-0.125 |
| `pumper_exit__light_long` | duck_db=-6.0, pump_bars=8 |
| `pumper_exit__light_on_grid` | duck_db=-6.0, offset_beats=0.0 |
| `pumper_exit__light_short` | duck_db=-6.0, pump_bars=2 |
| `pumper_exit__long` | pump_bars=8 |
| `pumper_exit__on_grid` | offset_beats=0.0 |
| `pumper_exit__on_grid_long` | offset_beats=0.0, pump_bars=8 |
| `pumper_exit__on_grid_short` | offset_beats=0.0, pump_bars=2 |
| `pumper_exit__short` | pump_bars=2 |
| `pumper_exit__standard` | duck_db=-10.0 |
| `pumper_exit__standard_early16` | duck_db=-10.0, offset_beats=-0.0625 |

### resonator_tail — Resonator Tail (Tuned Resonator-Bank Ring-Out) (89 variants)

| variant | params |
|---|---|
| `resonator_tail__bright` | color=0.85 |
| `resonator_tail__bright_full` | color=0.85, ring_level=1.0 |
| `resonator_tail__bright_high` | color=0.85, root_midi=57 |
| `resonator_tail__bright_long` | color=0.85, zone_bars=4 |
| `resonator_tail__bright_low` | color=0.85, root_midi=36 |
| `resonator_tail__bright_short` | color=0.85, zone_bars=1 |
| `resonator_tail__bright_slow` | color=0.85, fade_bars=2.0 |
| `resonator_tail__bright_soft` | color=0.85, ring_level=0.55 |
| `resonator_tail__bright_tight` | color=0.85, fade_bars=0.5 |
| `resonator_tail__dark` | color=0.2 |
| `resonator_tail__dark_full` | color=0.2, ring_level=1.0 |
| `resonator_tail__dark_high` | color=0.2, root_midi=57 |
| `resonator_tail__dark_long` | color=0.2, zone_bars=4 |
| `resonator_tail__dark_low` | color=0.2, root_midi=36 |
| `resonator_tail__dark_short` | color=0.2, zone_bars=1 |
| `resonator_tail__dark_slow` | color=0.2, fade_bars=2.0 |
| `resonator_tail__dark_soft` | color=0.2, ring_level=0.55 |
| `resonator_tail__dark_tight` | color=0.2, fade_bars=0.5 |
| `resonator_tail__full` | ring_level=1.0 |
| `resonator_tail__full_slow` | ring_level=1.0, fade_bars=2.0 |
| `resonator_tail__full_tight` | ring_level=1.0, fade_bars=0.5 |
| `resonator_tail__high` | root_midi=57 |
| `resonator_tail__high_full` | root_midi=57, ring_level=1.0 |
| `resonator_tail__high_long` | root_midi=57, zone_bars=4 |
| `resonator_tail__high_short` | root_midi=57, zone_bars=1 |
| `resonator_tail__high_slow` | root_midi=57, fade_bars=2.0 |
| `resonator_tail__high_soft` | root_midi=57, ring_level=0.55 |
| `resonator_tail__high_tight` | root_midi=57, fade_bars=0.5 |
| `resonator_tail__long_bright` | decay_s=4.5, color=0.85 |
| `resonator_tail__long_dark` | decay_s=4.5, color=0.2 |
| `resonator_tail__long_high` | decay_s=4.5, root_midi=57 |
| `resonator_tail__long_long` | decay_s=4.5, zone_bars=4 |
| `resonator_tail__long_low` | decay_s=4.5, root_midi=36 |
| `resonator_tail__long_short` | decay_s=4.5, zone_bars=1 |
| `resonator_tail__low` | root_midi=36 |
| `resonator_tail__low_full` | root_midi=36, ring_level=1.0 |
| `resonator_tail__low_long` | root_midi=36, zone_bars=4 |
| `resonator_tail__low_short` | root_midi=36, zone_bars=1 |
| `resonator_tail__low_slow` | root_midi=36, fade_bars=2.0 |
| `resonator_tail__low_soft` | root_midi=36, ring_level=0.55 |
| `resonator_tail__low_tight` | root_midi=36, fade_bars=0.5 |
| `resonator_tail__major` | chord='major' |
| `resonator_tail__major_long` | chord='major', decay_s=4.5 |
| `resonator_tail__major_short` | chord='major', decay_s=1.2 |
| `resonator_tail__major_standard` | chord='major', decay_s=2.5 |
| `resonator_tail__minor` | chord='minor' |
| `resonator_tail__minor_bright` | chord='minor', color=0.85 |
| `resonator_tail__minor_dark` | chord='minor', color=0.2 |
| `resonator_tail__minor_full` | chord='minor', ring_level=1.0 |
| `resonator_tail__minor_high` | chord='minor', root_midi=57 |
| `resonator_tail__minor_long` | chord='minor', decay_s=4.5 |
| `resonator_tail__minor_low` | chord='minor', root_midi=36 |
| `resonator_tail__minor_short` | chord='minor', decay_s=1.2 |
| `resonator_tail__minor_slow` | chord='minor', fade_bars=2.0 |
| `resonator_tail__minor_soft` | chord='minor', ring_level=0.55 |
| `resonator_tail__minor_standard` | chord='minor', decay_s=2.5 |
| `resonator_tail__minor_tight` | chord='minor', fade_bars=0.5 |
| `resonator_tail__octave` | chord='octave' |
| `resonator_tail__octave_bright` | chord='octave', color=0.85 |
| `resonator_tail__octave_dark` | chord='octave', color=0.2 |
| `resonator_tail__octave_full` | chord='octave', ring_level=1.0 |
| `resonator_tail__octave_high` | chord='octave', root_midi=57 |
| `resonator_tail__octave_long` | chord='octave', decay_s=4.5 |
| `resonator_tail__octave_low` | chord='octave', root_midi=36 |
| `resonator_tail__octave_short` | chord='octave', decay_s=1.2 |
| `resonator_tail__octave_slow` | chord='octave', fade_bars=2.0 |
| `resonator_tail__octave_soft` | chord='octave', ring_level=0.55 |
| `resonator_tail__octave_standard` | chord='octave', decay_s=2.5 |
| `resonator_tail__octave_tight` | chord='octave', fade_bars=0.5 |
| `resonator_tail__power` | chord='power' |
| `resonator_tail__power_bright` | chord='power', color=0.85 |
| `resonator_tail__power_dark` | chord='power', color=0.2 |
| `resonator_tail__power_full` | chord='power', ring_level=1.0 |
| `resonator_tail__power_high` | chord='power', root_midi=57 |
| `resonator_tail__power_low` | chord='power', root_midi=36 |
| `resonator_tail__power_slow` | chord='power', fade_bars=2.0 |
| `resonator_tail__power_soft` | chord='power', ring_level=0.55 |
| `resonator_tail__power_tight` | chord='power', fade_bars=0.5 |
| `resonator_tail__short_bright` | decay_s=1.2, color=0.85 |
| `resonator_tail__short_dark` | decay_s=1.2, color=0.2 |
| `resonator_tail__short_high` | decay_s=1.2, root_midi=57 |
| `resonator_tail__short_long` | decay_s=1.2, zone_bars=4 |
| `resonator_tail__short_low` | decay_s=1.2, root_midi=36 |
| `resonator_tail__short_short` | decay_s=1.2, zone_bars=1 |
| `resonator_tail__slow` | fade_bars=2.0 |
| `resonator_tail__soft` | ring_level=0.55 |
| `resonator_tail__soft_slow` | ring_level=0.55, fade_bars=2.0 |
| `resonator_tail__soft_tight` | ring_level=0.55, fade_bars=0.5 |
| `resonator_tail__tight` | fade_bars=0.5 |

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

### ring_mod_dissolve — Ring Mod Dissolve (Carrier-Multiplication Exit) (57 variants)

| variant | params |
|---|---|
| `ring_mod_dissolve__am` | morph=0.0 |
| `ring_mod_dissolve__am_long` | morph=0.0, zone_bars=8 |
| `ring_mod_dissolve__am_raw` | morph=0.0, raw='square' |
| `ring_mod_dissolve__am_short` | morph=0.0, zone_bars=2 |
| `ring_mod_dissolve__am_tight` | morph=0.0, fade_bars=0.25 |
| `ring_mod_dissolve__half` | morph=0.5 |
| `ring_mod_dissolve__half_long` | morph=0.5, zone_bars=8 |
| `ring_mod_dissolve__half_raw` | morph=0.5, raw='square' |
| `ring_mod_dissolve__half_short` | morph=0.5, zone_bars=2 |
| `ring_mod_dissolve__half_tight` | morph=0.5, fade_bars=0.25 |
| `ring_mod_dissolve__long` | zone_bars=8 |
| `ring_mod_dissolve__long_tight` | zone_bars=8, fade_bars=0.25 |
| `ring_mod_dissolve__low` | carrier_start_hz=60.0 |
| `ring_mod_dissolve__low_am` | carrier_start_hz=60.0, morph=0.0 |
| `ring_mod_dissolve__low_half` | carrier_start_hz=60.0, morph=0.5 |
| `ring_mod_dissolve__low_long` | carrier_start_hz=60.0, zone_bars=8 |
| `ring_mod_dissolve__low_manual_max` | carrier_start_hz=60.0, carrier_end_hz=8371.0 |
| `ring_mod_dissolve__low_raw` | carrier_start_hz=60.0, raw='square' |
| `ring_mod_dissolve__low_short` | carrier_start_hz=60.0, zone_bars=2 |
| `ring_mod_dissolve__low_soft` | carrier_start_hz=60.0, carrier_end_hz=1200.0 |
| `ring_mod_dissolve__low_standard` | carrier_start_hz=60.0, carrier_end_hz=2800.0 |
| `ring_mod_dissolve__low_tight` | carrier_start_hz=60.0, fade_bars=0.25 |
| `ring_mod_dissolve__manual_max` | carrier_end_hz=8371.0 |
| `ring_mod_dissolve__manual_max_am` | carrier_end_hz=8371.0, morph=0.0 |
| `ring_mod_dissolve__manual_max_half` | carrier_end_hz=8371.0, morph=0.5 |
| `ring_mod_dissolve__manual_max_long` | carrier_end_hz=8371.0, zone_bars=8 |
| `ring_mod_dissolve__manual_max_raw` | carrier_end_hz=8371.0, raw='square' |
| `ring_mod_dissolve__manual_max_short` | carrier_end_hz=8371.0, zone_bars=2 |
| `ring_mod_dissolve__manual_max_tight` | carrier_end_hz=8371.0, fade_bars=0.25 |
| `ring_mod_dissolve__manual_min` | carrier_start_hz=100.0 |
| `ring_mod_dissolve__manual_min_manual_max` | carrier_start_hz=100.0, carrier_end_hz=8371.0 |
| `ring_mod_dissolve__manual_min_soft` | carrier_start_hz=100.0, carrier_end_hz=1200.0 |
| `ring_mod_dissolve__manual_min_standard` | carrier_start_hz=100.0, carrier_end_hz=2800.0 |
| `ring_mod_dissolve__mid` | carrier_start_hz=240.0 |
| `ring_mod_dissolve__mid_am` | carrier_start_hz=240.0, morph=0.0 |
| `ring_mod_dissolve__mid_half` | carrier_start_hz=240.0, morph=0.5 |
| `ring_mod_dissolve__mid_long` | carrier_start_hz=240.0, zone_bars=8 |
| `ring_mod_dissolve__mid_manual_max` | carrier_start_hz=240.0, carrier_end_hz=8371.0 |
| `ring_mod_dissolve__mid_raw` | carrier_start_hz=240.0, raw='square' |
| `ring_mod_dissolve__mid_short` | carrier_start_hz=240.0, zone_bars=2 |
| `ring_mod_dissolve__mid_soft` | carrier_start_hz=240.0, carrier_end_hz=1200.0 |
| `ring_mod_dissolve__mid_standard` | carrier_start_hz=240.0, carrier_end_hz=2800.0 |
| `ring_mod_dissolve__mid_tight` | carrier_start_hz=240.0, fade_bars=0.25 |
| `ring_mod_dissolve__raw` | raw='square' |
| `ring_mod_dissolve__raw_long` | raw='square', zone_bars=8 |
| `ring_mod_dissolve__raw_short` | raw='square', zone_bars=2 |
| `ring_mod_dissolve__raw_tight` | raw='square', fade_bars=0.25 |
| `ring_mod_dissolve__short` | zone_bars=2 |
| `ring_mod_dissolve__short_tight` | zone_bars=2, fade_bars=0.25 |
| `ring_mod_dissolve__soft` | carrier_end_hz=1200.0 |
| `ring_mod_dissolve__soft_am` | carrier_end_hz=1200.0, morph=0.0 |
| `ring_mod_dissolve__soft_half` | carrier_end_hz=1200.0, morph=0.5 |
| `ring_mod_dissolve__soft_long` | carrier_end_hz=1200.0, zone_bars=8 |
| `ring_mod_dissolve__soft_raw` | carrier_end_hz=1200.0, raw='square' |
| `ring_mod_dissolve__soft_short` | carrier_end_hz=1200.0, zone_bars=2 |
| `ring_mod_dissolve__soft_tight` | carrier_end_hz=1200.0, fade_bars=0.25 |
| `ring_mod_dissolve__tight` | fade_bars=0.25 |

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

### scale_down_exit — Scale Down Exit (Beat-Stepped Pitch Descent) (20 variants)

| variant | params |
|---|---|
| `scale_down_exit__chromatic` | scale='chromatic' |
| `scale_down_exit__chromatic_deep` | scale='chromatic', steps=6 |
| `scale_down_exit__chromatic_few` | scale='chromatic', steps=3 |
| `scale_down_exit__chromatic_standard` | scale='chromatic', steps=4 |
| `scale_down_exit__deep` | steps=6 |
| `scale_down_exit__few` | steps=3 |
| `scale_down_exit__major` | scale='major' |
| `scale_down_exit__major_deep` | scale='major', steps=6 |
| `scale_down_exit__major_few` | scale='major', steps=3 |
| `scale_down_exit__major_pent` | scale='major_pent' |
| `scale_down_exit__major_pent_deep` | scale='major_pent', steps=6 |
| `scale_down_exit__major_pent_few` | scale='major_pent', steps=3 |
| `scale_down_exit__major_pent_standard` | scale='major_pent', steps=4 |
| `scale_down_exit__major_standard` | scale='major', steps=4 |
| `scale_down_exit__minor` | scale='minor' |
| `scale_down_exit__minor_deep` | scale='minor', steps=6 |
| `scale_down_exit__minor_few` | scale='minor', steps=3 |
| `scale_down_exit__minor_pent` | scale='minor_pent' |
| `scale_down_exit__minor_pent_deep` | scale='minor_pent', steps=6 |
| `scale_down_exit__minor_pent_few` | scale='minor_pent', steps=3 |

### scratch_in — Scratch-In / Scratch Drop (3 variants)

| variant | params |
|---|---|
| `scratch_in__half` | scratch_beats=0.5 |
| `scratch_in__one` | scratch_beats=1.0 |
| `scratch_in__two` | scratch_beats=2.0 |

### screwed_treatment — Screwed Treatment (Chopped & Screwed / Slowed) (13 variants)

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
| `screwed_treatment__held` | pitch_coupled=False |
| `screwed_treatment__screw` | rate=0.7 |
| `screwed_treatment__screw_coupled` | rate=0.7, pitch_coupled=True |
| `screwed_treatment__screw_held` | rate=0.7, pitch_coupled=False |

### shepard_riser — Shepard Riser (Endless-Rise Build Layer) (10 variants)

| variant | params |
|---|---|
| `shepard_riser__down` | direction=-1 |
| `shepard_riser__down_long` | direction=-1, bars=16 |
| `shepard_riser__down_short` | direction=-1, bars=4 |
| `shepard_riser__down_standard` | direction=-1, bars=8 |
| `shepard_riser__long` | bars=16 |
| `shepard_riser__short` | bars=4 |
| `shepard_riser__up` | direction=1 |
| `shepard_riser__up_long` | direction=1, bars=16 |
| `shepard_riser__up_short` | direction=1, bars=4 |
| `shepard_riser__up_standard` | direction=1, bars=8 |

### shimmer_wash — Shimmer Wash (Octave-Climbing Reverb Exit) (24 variants)

| variant | params |
|---|---|
| `shimmer_wash__fifth` | shift_semitones=7.0 |
| `shimmer_wash__fifth_ghost` | shift_semitones=7.0, level_db=-18.0 |
| `shimmer_wash__fifth_long` | shift_semitones=7.0, swell_bars=8 |
| `shimmer_wash__fifth_present` | shift_semitones=7.0, level_db=-8.0 |
| `shimmer_wash__fifth_short` | shift_semitones=7.0, swell_bars=2 |
| `shimmer_wash__fifth_standard` | shift_semitones=7.0, swell_bars=4 |
| `shimmer_wash__fourth` | shift_semitones=5.0 |
| `shimmer_wash__fourth_ghost` | shift_semitones=5.0, level_db=-18.0 |
| `shimmer_wash__fourth_long` | shift_semitones=5.0, swell_bars=8 |
| `shimmer_wash__fourth_present` | shift_semitones=5.0, level_db=-8.0 |
| `shimmer_wash__fourth_short` | shift_semitones=5.0, swell_bars=2 |
| `shimmer_wash__fourth_standard` | shift_semitones=5.0, swell_bars=4 |
| `shimmer_wash__ghost` | level_db=-18.0 |
| `shimmer_wash__long` | swell_bars=8 |
| `shimmer_wash__long_ghost` | swell_bars=8, level_db=-18.0 |
| `shimmer_wash__long_present` | swell_bars=8, level_db=-8.0 |
| `shimmer_wash__octave` | shift_semitones=12.0 |
| `shimmer_wash__octave_long` | shift_semitones=12.0, swell_bars=8 |
| `shimmer_wash__octave_short` | shift_semitones=12.0, swell_bars=2 |
| `shimmer_wash__octave_standard` | shift_semitones=12.0, swell_bars=4 |
| `shimmer_wash__present` | level_db=-8.0 |
| `shimmer_wash__short` | swell_bars=2 |
| `shimmer_wash__short_ghost` | swell_bars=2, level_db=-18.0 |
| `shimmer_wash__short_present` | swell_bars=2, level_db=-8.0 |

### sideband_comb_filter — Sideband Comb Filter (SBF) (23 variants)

| variant | params |
|---|---|
| `sideband_comb_filter__2bar` | zone_bars=2 |
| `sideband_comb_filter__8bar` | zone_bars=8 |
| `sideband_comb_filter__high` | base_hz=440.0 |
| `sideband_comb_filter__high_2bar` | base_hz=440.0, zone_bars=2 |
| `sideband_comb_filter__high_8bar` | base_hz=440.0, zone_bars=8 |
| `sideband_comb_filter__high_tight` | base_hz=440.0, interval=0.25 |
| `sideband_comb_filter__high_wide` | base_hz=440.0, interval=1.0 |
| `sideband_comb_filter__mid` | base_hz=220.0 |
| `sideband_comb_filter__mid_2bar` | base_hz=220.0, zone_bars=2 |
| `sideband_comb_filter__mid_8bar` | base_hz=220.0, zone_bars=8 |
| `sideband_comb_filter__mid_tight` | base_hz=220.0, interval=0.25 |
| `sideband_comb_filter__mid_wide` | base_hz=220.0, interval=1.0 |
| `sideband_comb_filter__sub` | base_hz=55.0 |
| `sideband_comb_filter__sub_2bar` | base_hz=55.0, zone_bars=2 |
| `sideband_comb_filter__sub_8bar` | base_hz=55.0, zone_bars=8 |
| `sideband_comb_filter__sub_tight` | base_hz=55.0, interval=0.25 |
| `sideband_comb_filter__sub_wide` | base_hz=55.0, interval=1.0 |
| `sideband_comb_filter__tight` | interval=0.25 |
| `sideband_comb_filter__tight_2bar` | interval=0.25, zone_bars=2 |
| `sideband_comb_filter__tight_8bar` | interval=0.25, zone_bars=8 |
| `sideband_comb_filter__wide` | interval=1.0 |
| `sideband_comb_filter__wide_2bar` | interval=1.0, zone_bars=2 |
| `sideband_comb_filter__wide_8bar` | interval=1.0, zone_bars=8 |

### slip_mode_flourish — Slip-Mode Flourish (3 variants)

| variant | params |
|---|---|
| `slip_mode_flourish__half` | flourish_beats=0.5 |
| `slip_mode_flourish__one` | flourish_beats=1.0 |
| `slip_mode_flourish__two` | flourish_beats=2.0 |

### spiral_echo — Spiral Echo (Pitch-Riding Feedback Delay) (17 variants)

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
| `spiral_echo__down2` | shift_semitones=-2.0 |
| `spiral_echo__down4` | shift_semitones=-4.0 |
| `spiral_echo__quarter` | delay_beats=0.25 |
| `spiral_echo__quarter_down2` | delay_beats=0.25, shift_semitones=-2.0 |
| `spiral_echo__quarter_down4` | delay_beats=0.25, shift_semitones=-4.0 |
| `spiral_echo__quarter_up4` | delay_beats=0.25, shift_semitones=4.0 |
| `spiral_echo__up4` | shift_semitones=4.0 |

### stem_swap_replace — Stem Swap Replace (Captured-Loop Stem Substitution) (7 variants)

| variant | params |
|---|---|
| `stem_swap_replace__16bar` | swap_bars=16 |
| `stem_swap_replace__1bar` | loop_bars=1 |
| `stem_swap_replace__1bar_16bar` | loop_bars=1, swap_bars=16 |
| `stem_swap_replace__1bar_4bar` | loop_bars=1, swap_bars=4 |
| `stem_swap_replace__4bar` | loop_bars=4 |
| `stem_swap_replace__4bar_16bar` | loop_bars=4, swap_bars=16 |
| `stem_swap_replace__4bar_4bar` | loop_bars=4, swap_bars=4 |

### stepped_element_tease — Stepped Element Tease (25/50/75/100% Ladder) (3 variants)

| variant | params |
|---|---|
| `stepped_element_tease__long` | step_beats=8 |
| `stepped_element_tease__standard` | step_beats=4 |
| `stepped_element_tease__tight` | step_beats=2 |

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

### transform_gate_loop — Transform Gate Loop (Zabiela EFX Transform) (14 variants)

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
| `transform_gate_loop__open` | duty_cycle=0.65 |
| `transform_gate_loop__tight` | duty_cycle=0.35 |

### underlap — Underlap (Slow Emergence, Vocal Held) (14 variants)

| variant | params |
|---|---|
| `underlap__audible` | entry_db=-14.0 |
| `underlap__long` | zone_bars=16 |
| `underlap__long_audible` | zone_bars=16, entry_db=-14.0 |
| `underlap__long_quiet` | zone_bars=16, entry_db=-20.0 |
| `underlap__long_whisper` | zone_bars=16, entry_db=-26.0 |
| `underlap__quiet` | entry_db=-20.0 |
| `underlap__short` | zone_bars=8 |
| `underlap__short_audible` | zone_bars=8, entry_db=-14.0 |
| `underlap__short_quiet` | zone_bars=8, entry_db=-20.0 |
| `underlap__short_whisper` | zone_bars=8, entry_db=-26.0 |
| `underlap__standard` | zone_bars=12 |
| `underlap__standard_audible` | zone_bars=12, entry_db=-14.0 |
| `underlap__standard_quiet` | zone_bars=12, entry_db=-20.0 |
| `underlap__standard_whisper` | zone_bars=12, entry_db=-26.0 |

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

### wera_weave — Hook-Vocal Weave (Vocal Leads, Chant Last) (14 variants)

| variant | params |
|---|---|
| `wera_weave__brief` | chant_bars=1 |
| `wera_weave__extended` | chant_bars=4 |
| `wera_weave__long` | weave_bars=12 |
| `wera_weave__long_brief` | weave_bars=12, chant_bars=1 |
| `wera_weave__long_extended` | weave_bars=12, chant_bars=4 |
| `wera_weave__long_standard` | weave_bars=12, chant_bars=2 |
| `wera_weave__short` | weave_bars=4 |
| `wera_weave__short_brief` | weave_bars=4, chant_bars=1 |
| `wera_weave__short_extended` | weave_bars=4, chant_bars=4 |
| `wera_weave__short_standard` | weave_bars=4, chant_bars=2 |
| `wera_weave__standard` | weave_bars=8 |
| `wera_weave__standard_brief` | weave_bars=8, chant_bars=1 |
| `wera_weave__standard_extended` | weave_bars=8, chant_bars=4 |
| `wera_weave__standard_standard` | weave_bars=8, chant_bars=2 |

### wordplay — Wordplay (2 variants)

| variant | params |
|---|---|
| `wordplay__echo_out` | exit='echo_out' |
| `wordplay__hard_cut` | exit='hard_cut' |

### wub_runway — Signature-Figure Runway (Drums Excluded) (3 variants)

| variant | params |
|---|---|
| `wub_runway__long` | runway_bars=8 |
| `wub_runway__short` | runway_bars=4 |
| `wub_runway__standard` | runway_bars=6 |

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
out.append("Phase 24 (ENUMERATION.md) extended the walk past the first two")
out.append("axes: singles on every axis and combos on every axis pair are")
out.append("admitted when the id is nameable (exactly one parameter set")
out.append("claims it) and every preset set is non-default — a default leg")
out.append("renders as its single, so default-legged combos are parameter")
out.append("notes, not variants. The legacy surface above is generated")
out.append("exactly as before and never delisted.")
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
