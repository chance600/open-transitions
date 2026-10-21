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

## Phase 4 — Expansion wave (2026-10-20)

Six domain lanes landed in parallel under the §7 contracts (each lane: engine module + ext demos + spec docs; zero shared-file edits), then one merge pass wired the public surface.

1. **DM-clip lane** (`engine/dm_techniques.py`, +6): live_loop_mix (DM-A14), cdj_synth_lead (DM-A15), tempo_double_trick (DM-A21), reverse_vocal_ambience (DM-A23), whoa_reverb_wobble (DM-A39), vocal_tremolo_gate (DM-A44) — the DJ-applicable subset of the 44 DM-clip candidates, each with the source clip URL + creator + save date as evidence. The remaining producing/mixing candidates went to `knowledge/` (below).
2. **STRUCT gaps** (`engine/gap_struct.py`, +7): stem_element_crossfade (GAP-08, incl. bass-stem-only entry), strip_down_buildup (GAP-09), flying_solo_acapella (GAP-10), beat_switch_under_acapella (GAP-11), accidental_duet (GAP-12), same_song_switchup (GAP-13), mic_talkover_reset (GAP-18, planning kind). Stem demos use the new stem-separated sketch tracks.
3. **TIME/DYN/SYNTH gaps + Zabiela** (`engine/gap_rest.py`, +8): sample_connection (GAP-01), loop_tightening_build (GAP-02, Hype Loops), polyrhythmic_loops (GAP-04), slip_mode_flourish (GAP-05), premade_tempo_bridge_edit (GAP-07), sampler_one_shot_mask (GAP-17), feedback_loop_build + metric_loop_pivot (PERF-ZAB, edu-survey-G §4).
4. **PERF gaps + T-035** (`engine/performer.py`, +4): scratch_in (GAP-14), rhythmic_fader_chops (GAP-15), spare_deck_element_firing (GAP-16), riser_ducking_overlay (T-035 — first parameterized software recipe; kind "overlay").
5. **Variants** (`engine/variants.py`): generator over the registry's declared preset axes — **127 named variants / 36 bases**, all renderable via `render_variant`; 30 sampled through the demo pipeline, all clean. (backspin / vocal_punchline_snap variants are registered and renderable but excluded from the *sample* — their intentional silence spans need declared allowances, the §7 mechanism; the core demos cover both.)
6. **Knowledge tree** (`knowledge/`, 81 entries): producing (36), mixing (18), setcraft (11 — incl. T-016 energy planning + the documented exclusions), workflows (7 — incl. the Mixed In Key → Rekordbox pipeline), performers (9 — Zabiela/Hype/EZ craft + the S0–S11 extraction pipeline + L0–L4 confidence ladder). Every entry carries provenance.

**Counts now:** 64 registry entries (62 executable techniques + T-037 + 1 planning), 48 plan-renderable, 127 variants, 81 knowledge entries, 3 registered exclusions (toneplay, holding-pattern loop, siren/horn). Selection smoke tests pass: stem techniques rank when stems exist, reject with named reasons when they don't; planning entries never rank.

Honest residuals: stem-signature techniques are demo+registry only (the plan renderer can't cut stems from a file — stem plan support is future work); `premade_tempo_bridge_edit` variants need their lane's staging scene; the full-suite verification receipt is regenerated on every merge run.

## Phase 5 — Backlog audit + web-mined tranche (2026-10-21)

Two workstreams, in order: (1) audit the banked backlog against the
registry, build anything qualifying that isn't built; (2) mine fresh
techniques from DJ literature outside the bank, bank them first, then
build to the same bar.

1. **Backlog audit — zero buildable leftovers.** The DM clip study's
   44 candidates: 6 already built in Phase 4 (A-14, A-15, A-21, A-23,
   A-39, A-44), 33 are knowledge-class (producing/mixing/workflows/
   business — they live in `knowledge/`, where they belong), 5 were
   overlap-resolved into existing entries (A-09/A-33/A-34 → vocal-chop
   family; A-28 → T-035/T-019 primitives; A-30 is an in-track fill,
   not a transition). TECHNIQUES.md's gap entries: all 16 actionable
   gaps were implemented in Phase 4; the remaining bank entries are
   the documented exclusions (T-012 toneplay, T-036 siren/horn) and
   T-016 energy planning (knowledge-class, in T-037/setcraft). GAP-03
   and GAP-06 exist in no bank or repo record — numbering skips, not
   lost techniques. The full audit with per-candidate reasons is
   recorded in `technique-bank/TECHNIQUES.md` ("Backlog audit —
   2026-10-21"). **Nothing was force-built to inflate the count.**
2. **Web-mined lane** (`engine/web_techniques.py`, +6 render
   techniques, banked first as WEB-01…WEB-06 in TECHNIQUES.md with
   per-technique sources):
   - `spiral_echo` (WEB-01, SPACE) — Pioneer DJM SPIRAL beat FX
     rendered: a feedback delay whose repeats pitch-shift per return
     (DJM-450 manual; Pestrela DJ Knowledge Base).
   - `flanger_sweep` (WEB-02, FREQ) — DJM Colour FX "Jet": a swept
     comb thins A's final bars; B enters dry (Pestrela KB; Engine DJ
     course).
   - `reverse_roll` (WEB-03, TIME) — REV ROLL reversed loop sampler
     as an exit build: A's last beat tiles backwards, halving
     (Pestrela KB).
   - `crush_degrade` (WEB-04, DYN) — DJM Crush extended: bit depth,
     sample rate, and low-pass all collapse over A's final bars;
     B arrives at full fidelity (Pestrela KB).
   - `shepard_riser` (WEB-05, SYNTH) — Shepard-Risset endless-rise
     layer (the DJM Mobius illusion, synthesized): octave sine stack
     under a Gaussian log-frequency envelope (Pestrela KB; Sound on
     Sound, iZotope Möbius Filter review).
   - `granular_freeze` (WEB-06, SPACE) — A's last ~150 ms sustained
     as a Hann-grain cloud while B fades up inside it (Amazing Noises
     Grain Freezer recipe via Rekkerd; Sound on Sound granular
     synthesis primer). Distinct from T-034 reverb_freeze, which
     freezes the room's tail — this freezes the source.
   Each ships with META (requires/prefers/params/evidence), spec doc,
   demo (`demos/ext_web.py`), and variants from its preset axes.
   Deliberately left banked, not built: the French Candy "washing
   machine" effect (Part B of the DM study) — named in one clip but
   never explained in text; it fails the evidence standard until a
   source describes the mechanism. A-42 stereo automation stays
   knowledge-class (a produced-track technique, not a transition).

**Counts now:** registry 64 → **70** (61 render + 3 decision + 5
overlay + 1 planning; 69 executable), plan-renderable 48 → **54**,
variants 127 → **186** (+59 across the 6 new bases; VARIANTS.md
regenerated), knowledge **81** (unchanged — this tranche added no
knowledge entries), exclusions unchanged (3). Verdicts: ADOPT 48 /
ADAPT 22.

**Verification:** full demo suite `python3 demos/make_demos.py` —
**96/96 demos rendered + verified clean** (90 baseline + 6 new;
silence/headroom/centroid gates, QC-gate self-test included);
`check_select()` T-037 canonical agreement still green; selection
smoke: crush_degrade + granular_freeze rank on a genre-leap pair,
reverse_roll + shepard_riser + flanger_sweep rank on a build pair,
spiral_echo ranks #6/30 on a key-clash pair (eligible, prefers fire,
no canonical displacement); all 59 new variants render finite output
via `render_variant`.

## Phase 6 — Educationals study program: source list + tranche 1 (2026-10-21)

Standing program kickoff (his directive: "Keep studying other DJ and
producer educationals. Assemble a large list if needed first."). Two
deliverables, in order: (1) the bibliography that outlives the run;
(2) the first mining tranche drawn from it.

1. **The source list** — `technique-bank/EDUCATIONAL-SOURCES.md` (goal
   workspace; the registry's companion reading list): **85 sources**
   in 5 classes — DJ educators/channels 20, official gear/software
   documentation 14, knowledge bases/blogs/forums 13, producer
   educationals 31, books 7. Each entry carries a URL, what it's
   good for, access (free / free-with-signup / paid), and a mining
   status. Every URL was verified resolving (redirects followed):
   four wrong URLs were corrected to their verified forms, two
   entries whose listed homes are gone were replaced in place, and
   the exceptions (two 403 bot walls, one dead domain) are noted
   inline — nothing silently kept. Paid sources are marked "paid —
   his per-item call"; nothing was purchased and no accounts were
   created. The file ends with a ranked **NEXT QUEUE** (10 sources),
   re-ranked at the end of every future tranche.
2. **Tranche 1 — the effect catalogs.** Mined the full DJM Beat FX /
   Colour FX catalogs (900NXS2 definitions + the A9 list), the
   Traktor FX catalog (Traktor 2 manual, Effects in Detail), the
   RMX-1000 Scene FX descriptions, and the producer riser/downer
   literature. Four techniques cleared the evidence + executability
   bar — banked first as WEB-07…WEB-10 in `technique-bank/
   TECHNIQUES.md` with provenance, then built into the existing web
   lane (`engine/web_techniques.py` + `demos/ext_web.py`; no new
   merge points):
   - `helix_catch` (WEB-07, TIME) — DJM HELIX: A's last fragment is
     caught into a loop whose pitch ramps during the hold; the
     release snaps home into B (DJM-900NXS2 manual p.17 via the
     Pioneer official forum; Pestrela KB).
   - `beatslicer_shuffle` (WEB-08, TIME) — Traktor BeatSlicer: A's
     final bar(s) are sliced (8 per bar) and replayed in a named
     permutation as a build, BUZZ on the final beat (Traktor 2
     manual §14.4.29).
   - `downlifter_exit` (WEB-09, SYNTH) — the producer's "downer": a
     descending low-passed-noise sweep spans the seam and masks a
     hard cut (MusicRadar synth-sweep tutorial; bank T-035's
     documented usage).
   - `shimmer_wash` (WEB-10, SPACE) — RMX-1000 Reverb Up / the
     shimmer principle: A's tail pitch-shifted +12 st into a long
     reverb swells as dry A exits; B enters under the climbing tail
     (RMX-1000 manual via Pestrela KB; Production Expert). The
     render is the feed-forward approximation of the feedback
     original, disclosed in the spec (the WEB-02 convention).
   **22 further catalog items were overlap-resolved**, banked in
   TECHNIQUES.md with pointers, and deliberately not rebuilt:
   phaser → `flanger_sweep`; dub echo / ping pong / low-cut echo /
   multi-tap → the T-004 echo family; trans / time gater →
   T-019/GAP-15/DM-A44 gate family; triplet filter/roll → timing
   axes of T-003/T-008; roll/slip roll/vinyl brake/pitch FX →
   T-008/GAP-05/T-006/T-032; melodic → DM-A15; Iceverb → the
   T-005/T-034 reverb family (its manual mechanism is resonant-
   filter color, not pitch shimmer); beatmasher → T-008/T-019;
   barber pole → `shepard_riser`; Enigma Jet → a WEB-05+WEB-02
   compound; Traktor MacroFX + DJTT chains → FRAMEWORK §6
   compounds, knowledge-class; reverse reverb → DM-A23 (already
   built). Nothing was force-built to inflate the count.

**Counts now:** registry 70 → **74** (65 render + 3 decision + 5
overlay + 1 planning; 73 executable), plan-renderable 54 → **58**,
variants 186 → **237** (+51 across the 4 new bases; VARIANTS.md
regenerated), knowledge **81** (unchanged), demos 96 → **100**
(suite: 100/100 rendered + verified clean). Verdicts: ADOPT 52 /
ADAPT 22. Selection: `check_select()` green (T-037 agreement +
ranking sanity); probe pairs rank the new techniques sensibly —
`shimmer_wash` surfaces #4 with both preference reasons firing on a
key-clash pair, the rest are eligible and sit below the top-5 cut on
a generic pair, the same behavior as WEB-01…WEB-06.
