# BUILD-LOG — open-transitions active build track

The DJ-skills-for-LLMs library, under construction. Local build only — nothing
pushed to any remote (publishing is a per-item call).

## Session 2026-10-18/19 — engine build-out (32 techniques)

### Implemented (engine/techniques.py)
Batch 1 — cuts, stops, drops:
- `hook_drop_handoff` (T-038) — signature vocal hook is the final event; 60–80 ms protective cosine exit fade to hard zero; incoming blooms in as texture AT the drop with a fast-attack sqrt curve (never cosine — v17 lesson: cosine reads as dead air). Banked rule: the blend lives in the entrance, the drop lives in the exit.
- `hard_cut` (T-030) — concat with 2 ms click guards.
- `brake_stop` (T-006) — pitch+tempo dive 1→0 over 0.25 beats (exp curve), tail pad.
- `power_down` (T-013) — manual pitch-fader drag over 1.5 beats (linear).
- `backspin` (T-007) — reversed tail with exp decay to −60 dB over exactly 1 beat.
- `vocal_punchline_snap` (T-025) — beat-3 low kill → beat-4 midpass vocal isolate → 175 ms digital void → drop at unity.
- `fake_drop` (T-029) — build, 3-beat void, real drop (optional interlude one-shot).

Batch 2 — builds, rolls, stacks:
- `loop_roll_build` (T-008) — 1/2→1/4→1/8→1/16 rolls across the final bar + HPF sweep to 6 kHz.
- `stutter_transition` (T-019) — hot-cue taps on 3, 3-and, 4, 4-and (low-killed), A dies on the last tap, B releases full.
- `vocal_chop_build` (T-033) — chop-density ladder 1/4→1/8→1/16 + band-pass sweep 500 Hz→5 kHz → hard cut.
- `noise_echo_buildup` (T-018) — empty-channel noise + 1/2-beat echo, raised over 8 bars, killed dead on the drop.
- `hotcue_drop_swap` (T-014) — equal-power volume cross-swap over the 4-beat run-up.
- `double_drop` (T-024) — dual builds, single-sub-bass rule (B's lows killed through the drop, bass swap after).
- `loop_transition` (T-027) — bounded 2-cycle loop tiled + T-001 EQ blend (composes `eq_blend`).
- `layered_fx_stack` (T-017) — echo from −8 bars, HPF sweep from −4, reverb send from −2, fader kill on the 1; B enters with mirror filter opening.

Batch 3 — freezes, bridges, juggles, decision functions:
- `reverb_freeze` (T-034) — 100%-wet long-decay tail excited pre-freeze, dry crossfaded out, B launches inside the tail, freeze releases over 4 bars.
- `tempo_bridge` (T-021) — one continuous phase-vocoder pass with a per-frame rate envelope (~1 BPM/bar ramp), or half/double passthrough.
- `drum_bridge` (T-022) — HPF ramp 30→400 Hz + mid kill over 4 bars (full-mix strip approximation; stems are exact), 12-bar interlude, B blends in with lows held.
- `breakdown_transition` (T-023) — equal-power blend inside A's breakdown + optional pitch-preserving BPM slide.
- `genre_bridge` (T-026) — vocal anchor looped in a reverb wash, B builds under HPF, wash cuts dead and B snaps full on the drop.
- `loop_juggle_replace` (T-031) — The Replace: A plays beats 1–3, B's loop-start steals beat 4, ×N cycles, then B from its first kick.
- `acapella_overlay` (T-010) — low-kill/high-tame EQ preset + overlay window with phrase-window fader riding.
- `harmonic_mix` (T-015) — pure Camelot decision function (same / ±1 / relative / +2 / clash, 12↔1 wraparound).
- `select_technique` (T-037) — pure decision brain: rejection rules prune first, decision table picks among survivors, priority-ordered; returns technique + reasons + rejected map.

Pre-existing (regression-demoed, untouched logic): `eq_blend`, `bass_swap`,
`filter_sweep`, `echo_out`, `echo_out_blend`, `layered_emergence`,
`reverb_wash`, `riser_drop`.

### DSP added (engine/dsp.py)
- `warp_resample` — time-varying playback rate (pitch-coupled, vinyl physics).
- `pitch_dive` — tape-stop dive, linear or exp curve.
- `phase_vocoder_stretch` — STFT phase vocoder, scalar or per-frame rate array; OLA edge hygiene (low-overlap zeroing + 5 ms edge fades).
- `bandpass_sweep` — HP+LP cascade for the chop brightness ladder.
- `synth_riser` upgraded (T-035): `duck_bpm`/`duck_db`/`duck_bars` sidechain-style pumping, `hp_hz`/`lp_hz` placement filters.

### Bugs found and fixed during the build
1. `eq_blend` hardcoded 32-bar breakpoints (bars 17/24) — crashed for shorter blends. Breakpoints are now fractions of `blend_bars` (identical behavior at 32).
2. `loop_roll_build` tiling assumed beat length divisible by roll division — pad instead of clip.
3. `phase_vocoder_stretch` OLA edge: dividing by near-zero window edges amplified numerical noise into a 158× spike (invisible in RMS, fatal for peak normalization). Fixed with low-overlap zeroing + edge fades.
4. `tempo_bridge` chunked the ramp into 1-bar constant-rate pieces — each chunk's STFT fade-in read as a periodic gap. Rebuilt as one continuous per-frame-rate pass.
5. Test-track fidelity (not technique bugs): sparse sketch tripped the silence gate (added continuous bed + 16th hats); detuned bed pair beat-cancelled into momentary dropouts (harmonic series instead); diff-noise hats carried energy to Nyquist (10 kHz lowpass).

### Tested
- `demos/make_demos.py`: 30/30 demos rendered + verified clean (silence_ok, headroom_ok, peak −1.0 dBFS). `demos/out/verification.json` + per-clip PNGs are the receipts.
- `harmonic_mix` + `select_technique`: assertion-checked (same/±1/relative/wraparound/clash; eq_blend for lateral, hook_drop_handoff for iconic-vocal-A, eq_blend pruned at 12% BPM gap).
- Audio spot-checks: hook_drop_handoff hits digital zero at the drop with bloom rising after; vocal_punchline_snap has an exact 175 ms void; fake_drop void is exact; brake_stop centroid dives 1588→70 Hz; tempo_bridge 128→132 grows 15.00→15.23 s with pitch preserved (220 Hz test tone stays 220 Hz).
- `render.py` TECHNIQUES registry updated (30 renderable entries; the 2 pure functions are not render targets).
- `techniques/` — 32 spec docs + INDEX.md generated from docstrings (`demos/gen_technique_docs.py`).

### Deferred (with reasons)
- T-009 build-to-drop layering — needs build-start/length detection (unsolved perception); choreography is specified in the bank, engine renders it once boundaries are known.
- T-011 wordplay — needs word-level lyric timestamps (WhisperX-class alignment); trigger timing is scriptable, discovery is not.
- T-012 tone play — SKIP as a transition (per-track improvisation, no generalizable recipe).
- T-016 energy planning — partial; the decision table lives in T-037, energy scoring per track/section is future work.
- T-020 3-deck layering — composes from existing primitives; needs a worked example (queued).
- T-023/T-026 advanced variants — basic choreography implemented; curatorial choices remain human.
- T-032 key-shift/pitch-play — needs formant-preserved pitch shifting (±2 semitones); DSP gap, noted for the next DSP batch.
- T-036 siren/horn — SKIP (human hype decision, never auto-deployed).
- `examples/` — still empty; queued: worked spec→automation examples (T-020 3-deck, T-009 dual-build).

### Next batch (queued)
1. `examples/`: 2–3 worked examples (technique spec next to the automation it produces).
2. DSP: formant-preserving pitch shift (T-032), onset/vocal-activity detection helpers (T-019/T-025 cue placement).
3. `render.py`: plan-file examples + analysis.json schema doc.
4. Engine versioning: CHANGELOG.md once the repo has a remote (his call).
5. Field-testing: render shortlisted techniques against real sketch audio; his ears are the gate.

## Phase 2 — GAP-A + GAP-B closed (2026-10-18)

Palette now covers all 105 catalog links (98 were covered; the 7 gaps are closed).

### Implemented in engine/techniques.py (+ demos, all verified clean)
- `wordplay` (T-011): shared-word onset alignment (caller-supplied word timestamps — the ADAPT caveat stands), rhythmic-unison trigger, hard_cut/echo_out exits.
- `build_to_drop` (T-009): dual-build layering — b's build at 100% fader with lows killed (bars 1–8), HPF wash on a (bars 9–16), step-cut pre-drop, b's drop at full. Build-boundary detection remains the caller's job.
- `three_deck_layer` (T-020): glue layer with tri-partite frequency slotting (a=lows, b=mids, glue=highs@75%), bass-swap handoff, glue rides 16 bars post-swap.
- `beat_jump` (T-028): pure playhead arithmetic `(b_full, cue_t, jump_beats) -> start_sample`; warns unless jump is a multiple of 8 bars. `beat_jump_transition` renders the repair.
- `pitch_play` (T-032): integer-semitone vocal shift into the backing key + T-010 overlay EQ; |semitones|<=2 enforced (raises beyond). New `dsp.pitch_shift` (phase-vocoder stretch + resample; NOT formant-preserving — documented).
- `screwed_treatment` (T-039, NEW bank entry): rate 0.6–2.0, pitch-coupled (vinyl/Screw) or pitch-held (slowed+reverb), chop/retrigger patterns.

### Deferred items retired from the old list
- T-009, T-011, T-020, T-032 are now IMPLEMENTED (their perception-side caveats — build detection, lyric timestamps, glue selection — remain caller-side, as the bank specifies).

### Infra
- `dsp.pitch_shift` added. `verify.py` plots optional (matplotlib/numpy2 env incompatibility — numerics always run). `render.py` registry: 36 renderable. `techniques/`: 39 spec docs + INDEX.md. README catalog updated (38 techniques, 36 demos).
- Full demo suite: 36/36 rendered + verified clean, no regressions.

### Remaining deferred (with reasons)
- T-012 tone play — SKIP (per-track improvisation). T-016 energy planning — partial (decision table in T-037). T-036 siren/horn — SKIP (human hype). Formant-preserving pitch shift — DSP gap for a future batch (current impl is fine within ±2).

## Phase 3 — Framework + open-source publish (2026-10-20)

Framework first, per his "experimental but needs a framework for real utility" directive.

1. **`FRAMEWORK.md`** — the architecture contract: 10-family taxonomy (incl. ROUTING for stem routing), technique metadata schema (requires/prefers/params/energy/exit/evidence), Song schema + pair-feature derivation, selection design, evidence layer (no orphan techniques), extension grammar (variants/overlays/chains/compounds), module contracts, verification gates, counting rules (techniques vs variants vs knowledge entries — reported separately, no layer inflates another), deliberate exclusions (T-012 toneplay, holding-pattern loop, T-036 siren/horn — registered in EXCLUSIONS so selection can explain their absence).
2. **`engine/meta.py`** — 39 registry entries (all 38 core techniques + select_technique), every one with ≥1 real-world evidence reference; aggregates domain-module META dicts (core wins).
3. **`engine/select.py`** — selection engine v1: `select(a, b)` → ranked candidates with scores + reasons, full "why not" map, pair features. Genre-norm bonuses (bank GAPS.md #10). Deterministic. `check_select()` asserts agreement with T-037 on its canonical cases (lateral → eq_blend; iconic A → hook_drop_handoff; 12% BPM + clash + leap → echo_out-class answer, eq_blend rejected naming the BPM rule; shared lyric → wordplay top-3) and is wired into the demo suite.
4. **Domain-module contracts** — `demos/make_demos.py` auto-merges `demos/ext_*.py` (ctx injection: tracks, stems, helpers), `engine/render.py` auto-merges domain `TECHNIQUE_FUNCS`, `engine/meta.py` auto-merges domain `META`. New lanes = drop in files, no shared-file edits. `build_track_stems()` added for ROUTING-family demos.
5. **Publish** — `github.com/chance600/open-transitions` (public, MIT), first push: framework + full current library.

Verification: 36/36 demos clean, select checks green, README catalog verified.
