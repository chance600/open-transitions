# VARIANTS — generated variant catalog

Variants are base techniques x named presets on their declared
discrete parameter axes (FRAMEWORK.md §6, operator 1; axes are
the `"presets"` maps in each technique's `params`, §3). The
registry lives in `engine/variants.py` and is **generated,
never hand-listed**: `VARIANTS = build_variants()` enumerates
`meta.all_meta()` at import time.

**Snapshot: 127 variants across 36 base techniques** (108 variants across 29 core-bank bases; the rest arrive via domain modules, FRAMEWORK.md §7).
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

### double_drop — Double Drop (Dual-Build Collision) (2 variants)

| variant | params |
|---|---|
| `double_drop__16bar` | drop_at_bar=16 |
| `double_drop__8bar` | drop_at_bar=8 |

### drum_bridge — Drum Bridge (Atonal Neutral Zone) (3 variants)

| variant | params |
|---|---|
| `drum_bridge__12bar` | interlude_bars=12 |
| `drum_bridge__16bar` | interlude_bars=16 |
| `drum_bridge__8bar` | interlude_bars=8 |

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

### rhythmic_fader_chops — Rhythmic Fader Chops (Transformer) (3 variants)

| variant | params |
|---|---|
| `rhythmic_fader_chops__2beat` | chop_beats=2 |
| `rhythmic_fader_chops__4beat` | chop_beats=4 |
| `rhythmic_fader_chops__8beat` | chop_beats=8 |

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

### slip_mode_flourish — Slip-Mode Flourish (3 variants)

| variant | params |
|---|---|
| `slip_mode_flourish__half` | flourish_beats=0.5 |
| `slip_mode_flourish__one` | flourish_beats=1.0 |
| `slip_mode_flourish__two` | flourish_beats=2.0 |

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
