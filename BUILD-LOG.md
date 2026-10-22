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

## Phase 7 — Educationals study program: tranche 2 (2026-10-21)

Second tranche of the standing study program, worked from the top
of the Phase 6 NEXT QUEUE, items 1–4 in order and to depth:
(1) the DJM-A9 manual body — Sound Color FX types (pp.40–41),
Beat FX types and settings (pp.52–56), FX FREQUENCY usage
(pp.47–50); (2) Serato's official FX + Flip documentation
(Serato Support: Using DJ-FX in both editions, the 3.2.0 DJ-FX &
Channel FX FAQ, the full DJ-FX & Channel FX list, the Flip User
Guide); (3) the Traktor Pro 4 manual's FX chapters — Pattern
Player controls (p.25) and FX-unit mode (p.78), the 9-piece
Mixer FX set — plus NI's Pattern Player blog; (4) the DJ
TechTools compounds pass — the Fader FX Theory article (2008)
and the chain lists preserved on the Pestrela effects page.

Two techniques cleared the evidence + executability bar — banked
first as WEB-11/WEB-12 in `technique-bank/TECHNIQUES.md` with
provenance, then built into the existing web lane
(`engine/web_techniques.py` + `demos/ext_web.py`; no new merge
points):

- `infinity_filter` (WEB-11, FREQ) — Serato's Infinity Filter
  (legacy name: Shepard Filter): the Shepard construction
  transposed to filters — an octave-spaced stack of narrow
  resonant peaks sweeps A's final bars endlessly under a Gaussian
  log-frequency window, so the exit never arrives; B enters dry
  (Serato Support DJ-FX & Channel FX list; Serato Hex FX:
  "endless sweeping peaks"; Pestrela's Mobius = Shepard Tone
  decomposition).
- `pattern_layer_bridge` (WEB-12, SYNTH) — Traktor Pro 4's
  Pattern Player as a transition: a synthesized one-shot pattern
  layer (parametric 808/909-style voices on a 16-step grid, named
  density patterns in the manual's increasing-activity order,
  optional kick ducking with the manual's 200–500 ms release)
  carries the seam zone while A exits and B establishes (Traktor
  Pro 4 manual pp.25/78; NI blog's transitions-and-builds
  recipe).

One authoring model went to the knowledge layer: **Serato Flip**
— recorded hot-cue/censor automation saved into the track's
metadata and replayed as an edit — banked in
`knowledge/workflows.md` (knowledge 81 → **82**), the model
behind the premade-edit family (T-028/T-014/GAP-07), not a
renderer.

**Everything else was overlap-resolved in the bank with
pointers, deliberately not rebuilt:** the full A9 catalog
against its manual body (MOBIUS → `shepard_riser` — the body's
signed beat fractions are its direction axis; SPACE →
`reverb_wash` band-pair axis; TRIPLET FILTER/ROLL → timing axes
— Phase 6's resolutions *confirmed* by the body; FX FREQUENCY →
a routing-axis note over the existing band machinery); 40+
Serato DJ-FX names across the 3.2 list and the legacy iZotope
packs (echo/brake/roll/gate/crush/reverb family voicings;
Pitch Looper → `helix_catch`; Particle Delay → a
`granular_freeze` feed axis; Pan Delay → the mono T-004
disposition), with three **named unknowns banked-not-built** —
Infinity Tone, Space Invader, U.F.O: no mechanism published in
any source read (the French Candy disposition); Traktor's 9
Mixer FX — every one decomposes as an effect + bipolar filter
(Barber Pole → `shepard_riser`, Dotted Delay → a T-004 timing
axis, Crush → `crush_degrade`, its "no pitch increase" note
being exactly the DJM distinction) — plus Delay T3 / Free Run
and Flux Mode as axes/planning notes on existing entries; and
the DJTT compounds pass proper: Fader FX's three-slot grammar
(repeating → shaping → dimensional) is FRAMEWORK §6's chain
operator with named slot roles, and every named chain — JogFX
(Detox, Build, Swirl), MacroFX (Wormhole, PolarWind,
FlightTest, LaserSlicer, DarkMatter, Zzzurp, EventHorizon,
Bass-o-Matic, Strrretch, GranuPhase), the Koolis combos —
decomposes into registry bases with **zero new primitives**
(the ring modulator appears only as a compound ingredient and
is banked-not-built as a base; Bass-o-Matic's "triplets slicer"
is a third vendor confirming triplet timing as an axis). The
NEXT QUEUE in `technique-bank/EDUCATIONAL-SOURCES.md` is
refreshed — Denon Engine DJ tops it now.

**Counts now:** registry 74 → **76** (67 render + 3 decision +
5 overlay + 1 planning; 75 executable), plan-renderable 58 →
**60**, variants 237 → **257** (+20 across the 2 new bases;
VARIANTS.md regenerated), knowledge 81 → **82**, demos 100 →
**102** (suite: 102/102 rendered + verified clean). Verdicts:
ADOPT 54 / ADAPT 22. Selection: `check_select()` green (T-037
agreement); probes rank the new techniques on-design —
`pattern_layer_bridge` #1 on a breakdown → bigger-B pair with
both preference reasons firing, `infinity_filter` #3 on a
key-clash pair (both prefers firing) and #5 on a generic matched
pair, eligible-but-unremarkable where its preferences don't
apply; all 20 new variants render finite output via
`render_variant`. Two render bugs were caught and fixed during
smoke (bandpass state-vector length in the peak bank; a zone
slice running past the seam).

## Phase 8 — Educationals study program: tranche 3 (2026-10-21)

Third tranche of the standing study program, worked from the top
of the Phase 7 NEXT QUEUE, items 1–4 in order and to depth:
(1) the Denon Engine DJ documentation — X1850 PRIME User Guide
(BPM FX and Sweep FX chapters), Prime GO manual Touch FX (p.59),
Prime 4+/G2 FAQ, and the Engine DJ v3.1 release article with its
26-effect Main FX list (+ the 3.1 Release Notes); (2) the
Pestrela DJ Knowledge Base's Mappings & Controllers remainder,
read in full; (3) the rekordbox manuals — DDJ-RZX ("Using the
release FX"), XDJ-RX3 (Release FX pad assignments), and the
software manual's slip mode chapter (pp.134–135); (4) the DJM-S11
manual body — Sound Color FX (p.52), Beat FX types and settings
(pp.55–61), Touch FX (p.62) — plus Smooth Echo from Pioneer's
product copy. The tranche's first pass died in a daemon restart
after its bank prose landed in `technique-bank/TECHNIQUES.md`;
this phase was completed in a recovery pass that audited that
prose against the sources first-hand, then built what it banked.

Three techniques cleared the evidence + executability bar —
banked as WEB-13/WEB-14/WEB-15 in `technique-bank/TECHNIQUES.md`
with provenance, then built into the existing web lane
(`engine/web_techniques.py` + `demos/ext_web.py`; no new merge
points):

- `pumper_exit` (WEB-13, DYN) — Denon's Pumper as a transition
  exit: audio ducks on the downbeat grid (manual: Duck −2…−20 dB,
  Offset to −1/2 beat) across A's final bars, the depth ramping
  cycle by cycle; the final cycle's recovery is withheld and B
  enters dry at full level in the hole (X1850 PRIME User Guide;
  rekordbox's Release FX DUCKING is the second vendor).
- `scale_down_exit` (WEB-14, TIME) — Engine DJ 3.1's Scale Down:
  A's captured fragment replays over B's entrance, each replay
  stepping down the scale in beat-locked steps (the Pitch Down
  chromatic form is an axis). Engine names "four different
  scales" without enumerating them; the render adopts the
  standard four (major, natural minor, major and minor
  pentatonic), disclosed in the bank entry (Engine DJ v3.1
  article; Engine DJ 3.1 Release Notes).
- `fader_synth` (WEB-15, SYNTH) — the DJM-S11's FADER SYNTH as a
  seam: A's channel is *replaced* by an oscillator (SINE/SAW/
  SQUARE, base octave −3…+3) whose pitch the fader plays, in
  named scale quantizations; the line rides across the seam
  zone while B fades in beneath it, then cuts — B inherits the
  key and the energy (DJM-S11 manual, p.61).

Two authoring models went to the knowledge layer
(`knowledge/workflows.md`, knowledge 82 → **84**): **Release FX**
— rekordbox's chain-terminator operator (FRAMEWORK §6: whatever
chain is running, the release FX is how it ends; every member
resolves to a registry base, DUCKING → WEB-13's mechanism in exit
form), and **Smooth Echo** — trigger-coupled echo tails, a
trigger-semantics layer over T-004/WEB-01 (the tail is fired by
the cut gesture itself).

**Everything else was overlap-resolved in the bank with
pointers, deliberately not rebuilt:** Denon's Sweep FX set
(ECHO/FLANGER/PHASER sweeps, WASH OUT → `shimmer_wash`'s knob
form, NOISE GATE confirmed as `vocal_tremolo_gate`'s other
vendor) and Touch FX set (every member a registry base, a
gesture, a chain-order note, or a sequencer); the full 26 Main
FX list (incl. the Phase 5/6 names re-confirmed — HELIX →
`helix_catch`, MOBIUS TONE → `shepard_riser` — and the four
simple locks BRK/ECHO/DUCK/ROLL BS); Pestrela's Controllers
remainder — read in full, **zero new mechanisms** (gate
compressors and dual-deck pagers banked as the page's two
engineering footnotes); rekordbox slip mode, a second-vendor
verbatim confirmation of the T-028/GAP-05 playhead model; and
the S11's Beat FX body — every entry a registry base or a
composition, with its new axes recorded where they belong
(FADER PITCH's scale list → T-032; DUCKING ECHO's tail-coupling
parameter; DELAY's Swing sub-parameter; KILL's attenuation
time+curve pair; ROLL's dry-mute amount; the WIDE FILTER's
extended travel; the cyclic vs one-shot split across the FX
catalogs). One named unknown stays banked-not-built: the Sweep
FX voice named "Gender" publishes no mechanism in any source
read (the French Candy disposition). The README catalog table —
carried since Phase 5 stopping at WEB-06 — now runs through
WEB-15. The NEXT QUEUE in
`technique-bank/EDUCATIONAL-SOURCES.md` is refreshed — the
RMX-1000 manual body tops it now.

**Counts now:** registry 76 → **79** (70 render + 3 decision +
5 overlay + 1 planning; 78 executable), plan-renderable 60 →
**63** (the plan renderer's merged technique map), variants
257 → **295** (+38 across the 3 new bases; VARIANTS.md
regenerated), knowledge 82 → **84**, demos 102 → **105** (suite:
105/105 rendered + verified clean). Verdicts: ADOPT 57 /
ADAPT 22. Selection: `check_select()` green (T-037 agreement);
probes rank the new techniques on-design — `fader_synth` #1 on a
breakdown → bigger-B pair with both preference reasons firing
(`pattern_layer_bridge` #2 alongside), `scale_down_exit` #5 on a
key-clash outro pair with both prefers firing (`spiral_echo` #7
with the same), `pumper_exit` eligible with both preferences
firing (score 3.0, in a six-way tie cluster) on a chorus →
bigger-B pair; on a generic outro pair `pumper_exit` and
`fader_synth` are rejected by their phrase gates — by design —
and `scale_down_exit` is eligible below the cut; all 38 new
variants render finite output via `render_variant`. One demo
fix during the run: `pumper_exit`'s withheld-recovery hole —
the technique's signature silence — is declared as allowed
silence in its demo spec, the brake/power-down pattern, after
the verifier flagged the final beat.

## Phase 9 — Educationals study program: tranche 4 (2026-10-21)

Fourth tranche of the standing study program, worked from the
top of the Phase 8 NEXT QUEUE, items 1–4 in order and to depth:
(1) the Pioneer RMX-1000 manual body — "Types of effects"
(pp.15–17) and the RELEASE FX / FX SOURCE operation pages
(p.14), read first-hand on manua.ls; (2) the Traktor 2 manual's
"The Effects in Detail" chapter (§14.4.1–14.4.35, manua.ls
pp.226–253) read to completion — Phase 6 had read only
BeatSlicer and Iceverb; (3) the VirtualDJ native effects list
(manual Mixer > Audio and Decks > Effects pages first-hand;
the appendix roster page renders in JavaScript and is not
text-readable, so staff/changelog confirmations carry the
deck-FX remainder — the caveat is recorded in the bank);
(4) Mixed In Key's harmonic/energy research — the book chapter
"Use Advanced Harmonic Mixing Techniques," the current
"Harmonic Mixing Explained" wiki page and its "Change DJ Set
Energy With the Camelot Wheel" workflow, and the founder's
energy-scale anchors (1001tracklists interview).

**Built (2):** `ring_mod_dissolve` (WEB-16, FREQ, ADOPT) —
Traktor's Ring Modulator (§14.4.25) rendered as a dissolve
exit: A's final bars crossfade into full carrier
multiplication while the carrier sweeps logarithmically
(100 Hz default start, the manual's range floor; 8371 Hz
ceiling available as a preset), the AM–RM morph and RAW
filtered-square carrier carried as parameters. Phase 7 had
banked ring modulation as a compound ingredient only; the
first-party manual's standalone mechanism revises that
disposition. `formant_morph_exit` (WEB-17, FREQ, ADOPT) —
the Formant Filter (§14.4.30): three bandpass formants morph
through the vowel series (path / TYP table / SHARP carried as
parameters; formant targets are classic Peterson &
Barney-style published averages, the German table a flagged
approximation). Both are mechanisms no registry base performs
— multiplication and spectral-shape morphing — not re-voicings
of existing bases.

**Item 1 (RMX-1000) — resolutions, no builds:** the complete
Scene FX roster (10 effects, two banks) resolves to registry
bases, with WEB-01/WEB-10's evidence upgraded to manual-grade.
**Zip is settled**: it is not an RMX-1000 effect at all — it
is the RMX-500's breakdown pitch shifter (djworx review),
i.e. T-032 `pitch_play`'s family; Phase 6's "performance
gesture" hedge is retired. **Sub Parameter is settled** as a
per-effect control layer, not a mechanism. TRANS/ROLL's
independent per-band beat cycles banked as a band-cycle axis
of T-008/T-019; the RELEASE FX lever's FX-clearing semantics
give the knowledge layer's chain-terminator entry its
second-hardware confirmation (amended in
`knowledge/workflows.md`).

**Item 2 (Traktor) — the chapter's systematic yield:** beyond
the two builds, four "Pulse" variants (Flanger/Filter/
Filter:92/Phaser Pulse) expose **peak-triggered modulation**
as a cross-effect modulation-source axis — movement locked to
the signal's own peaks, self-developing "best in empty parts
of the music" — banked in TECHNIQUES against T-003/WEB-02.
Thirty-one further sections overlap-resolved with axes banked
(rate-glide DURATION on T-004, inverted-feedback FB−,
Filter:92's Band Reject mode, Transpose Stretch's
stretch-to-a-single-grain path into WEB-06's frozen moment,
Bouncer's pattern-progress transposition, Digital LoFi as
WEB-04's second vendor). Macro FX do not appear in this
manual body; Phase 7's DJTT record stands. Entry 26 is fully
mined — the Traktor catalog is closed.

**Item 3 (VirtualDJ) — complete overlap:** the manual's
verbatim Color FX set (10) and Mix FX set (6), plus
staff/changelog-confirmed deck FX (Beat Grid, Slicer, WahWah,
Backspin, BrakeStart, Loop Out), all resolve to built
families — zero new bases, zero new primitives. Two framings
banked: **Mix FX** (effects bound to the crossfader itself —
the blend gesture is the effect's envelope; the crossfader-
coupled form of Phase 7's fader-coupling) and **Stem FX
routing** (per-stem effect application). Four independent FX
taxonomies now converge on the registry's mechanism set;
FlippinDoubles is banked-not-built on thin (forum-only)
evidence.

**Item 4 (Mixed In Key) — selection-layer yield:** two
knowledge entries in `knowledge/setcraft.md` (Energy Boost
Mixing — key movement as an energy event: +2 same-letter as
the standard boost, +7/−5 as the semitone boost, the quick-mix
rule, the −2 wind-down mirror; Camelot diagonals and the +4 —
the diagonal asymmetry and Guetta's simple-melody far move),
plus the founder's anchors calibrating the Energy planning
entry (6 = the danceability threshold; 9–10 = anthems).
Power Block Mixing: named by MIK, no mechanism published —
French Candy disposition.

**Proposals — recorded, NOT implemented** (this tranche's
brief: selection behavior changes are flagged, never silently
landed). MIK's doctrine exposes three places where
`engine/select.py` is coarser than the evidence:
(P1) `camelot_distance` scores every different-letter /
different-number pair 4 (clash), but the working diagonals
(8B→9A, 9A→8B) share notes — refine so the note-sharing
diagonals score 2 while the dissonant diagonal (8B→7A) stays
4. (P2) Distance is symmetric, but key movement is
directional: add a signed `key_move` feature (semitone delta)
and let short/FX exits *prefer* +1/+2-semitone moves when
`energy_delta >= 0` (the Energy Boost), while long-blend
techniques keep excluding them (the quick-mix rule).
(P3) The +4 same-letter move works "with simple melodies" —
gate a far-move allowance on melodic simplicity; `vocal_pair`
is the interim proxy until a melodic-density feature exists.
Each proposal needs check_select cases before it lands; they
are item 8 of the refreshed NEXT QUEUE.

**Counts now:** registry 79 → **81** (72 render + 3 decision +
5 overlay + 1 planning; 80 executable), plan-renderable 63 →
**65**, variants 295 → **319** (+24 across the 2 new bases,
53 bases; VARIANTS.md regenerated), knowledge 84 → **86**,
demos 105 → **107** (suite: 107/107 rendered + verified
clean). Verdicts: ADOPT 57 → **59** / ADAPT 22. Selection:
`check_select()` green (T-037 agreement); probes rank the new
techniques on-design — `formant_morph_exit` #1 (5.0, tied,
alphabetical first) on a vocal-A breakdown pair with both
preference reasons firing, `ring_mod_dissolve` at 4.0 with
both reasons on a true genre-leap + energy-rise pair; both
unrejected on lateral pairs; all 24 new variants render
finite output via `render_variant`. One fix during the run:
both new META entries initially omitted `breakdown` from
`phrase_a_ok`, contradicting the formant entry's own
breakdown preference — caught by the selection probes and
corrected (the demo suite does not exercise META gates). The NEXT QUEUE in
`technique-bank/EDUCATIONAL-SOURCES.md` is refreshed — the
structured catalogs are exhausted, so Crossfader's named
transition techniques top it now.

## Phase 10 — Educationals study program: tranche 5 (2026-10-21)

Fifth tranche, two workstreams. Workstream A worked the NEXT
QUEUE top-down: (1) Crossfader's named transition techniques —
the channel's canonical "12 High-Energy DJ Transitions" set,
mined from Crossfader's own step-by-step walkthrough text
(wearecrossfader.co.uk) plus the full transcript of "5 Ways To
Stop Your DJ Mixes Sounding Boring"; (2) Club Ready DJ School
+ DJ Carlo routine/mashup breakdowns — Club Ready's written
harmonic-mixing guide (Tribe Talk blog) and Carlo's flagship
"10 MUST KNOW DJ Mixing Techniques," all read first-hand.
Workstream B discharged the queue's engineering debt: the
three select.py proposals recorded in Phase 9.

**Workstream A — zero new bases, the pattern holds.** Five
educator canons and four vendor taxonomies have now been
absorbed without a registry gap since Phase 9. The yield is
axes, framings, and selection knowledge, all banked in
TECHNIQUES (Phase 10 section):
- Crossfader: 8 of the 12 names were already bank-cited and
  are mechanism-confirmed by the walkthrough text. The 4
  unmined names resolve as: **Same Song Switch Up** — a
  pairing framing (same-composition pairs license full-phrase
  simultaneous playback; the audio ops are T-003 × T-002);
  **Polyrhythmic Looping** — a fractional loop-length axis of
  T-008 (3/2, 3/4 lengths precessing against the host grid;
  the triplet precedent governs: axis, not base), with its
  tempo-mediation use recorded against T-021; **Sample Switch
  Up + Wide Syncing** — one shared axis of T-021: the tempo
  ramp applied to the *sync-locked pair* rather than the
  outgoing stream alone (104→126 BPM over 16 bars in the
  moderate instance; 125→~183 wide-range in the extreme), the
  sample-genealogy pairing recorded as its selection context.
  The second video contributes **Gate Cue** — Serato's
  momentary cue mode ("once you release that performance pad
  it's going to stop instantly") banked as T-019's
  trigger-mode axis (latched / gated), with the
  loop→performed-pattern swap as its staging form.
- Club Ready: the compatibility-vs-modulation framing banked
  in `knowledge/setcraft.md` (+1 entry); their +4 caution
  corroborates the simplicity gate's premise; their +9 note
  is recorded as a set-level color and explicitly NOT adopted
  into the ladder (single-source personal preference).
  Curriculum titles state no mechanisms — nothing banked from
  titles.
- DJ Carlo: the pro EQ blend stated as doctrine (T-001/T-002);
  the named Buildup Loop Transition confirms T-008's ladder;
  stems mashup mixing resolves to GAP-08
  `stem_element_crossfade` with a **vocal-led order axis**
  (his staging leads with the vocal; GAP-08's default order
  leads with the bass). Coverage caveat: the transcript host
  rate-limited the full page; every banked claim is verbatim
  transcript text surfaced via the search index, and none
  rest on the unexcerpted middle segments.

**Workstream B — P1–P3 all implemented** in
`engine/select.py`, each behind before/after probe evidence
(pairs exercising the change; harness preserved with the
tranche's working papers). The bar held: `check_select()`
green throughout with three new guard cases; no existing
gate loosened except where a proposal names it.
- **P1 — diagonal refinement.** `camelot_distance`: a
  cross-letter wheel-adjacent pair (step 1) scores **2** when
  the minor's number ≡ the major's number + 1 (mod 12) — the
  note-sharing diagonal — and stays **4** otherwise. Probe:
  before, all four diagonal directions scored 4 and DIAG-WORK
  (8B→9A) was clash-rejected by every blend family; after,
  8B→9A = 9A→8B = 2 with eq_blend/bass_swap admitted (6.0),
  while DIAG-DISS (8B→7A) stays 4 and rejected. Case 6.
- **P2 — signed key_move + boost preference.** New
  `_tonic_pc`/`key_move` (semitone delta −6..+5, circle of
  fifths anchored 8B = C) and an `energy_boost` feature
  (key_move ∈ {+1, +2} with energy_delta ≥ 0). `_boost_bonus`
  adds **+1.0 with a stated MIK reason to snap/void-class
  exits only** — seamless and tail scores are bit-identical,
  and no camelot_max gate moves: the quick-mix rule as
  scoring. Probe: before, BOOST+2 (8A→10A) and its mirror
  MIRROR-2 (8A→6A) produced *identical* selection output —
  direction was invisible; after, hard_cut scores 2.0 on the
  boost pair with the reason vs absent on the mirror,
  eq_blend identical (6.0) in both directions, the semitone
  route (8A→3A, the +7/−5 move) earns the same +1.0 against
  its downward control (8A→1A), and a falling-energy boost
  pair earns nothing (energy_boost False — MIK's
  support-with-energy condition enforced). Case 7. Observed
  interaction, recorded not hidden: DIAG-DISS (8B→7A) has
  key_move +2, so its snap exits earn the boost preference
  even though blends stay clash-rejected there — coherent,
  since the boost keys on tonic pitch motion, independent of
  the compatibility ladder.
- **P3 — the +4 simplicity gate.** In `derive_features`: an
  upward same-letter +4 move on a vocal-free pair
  (`vocal_pair == "neither"`, the interim simplicity proxy)
  reads an effective camelot of **3** — the top of the
  workable band — with the raw ladder preserved as
  `camelot_raw`. Probe: PLUS4-SIMPLE (8B→12B) moves from
  clash-class (all blends rejected) to eq_blend admitted
  (6.0), while double_drop stays Camelot-rejected (3 > 2) —
  camelot_max ≤ 2 techniques remain closed to gated pairs;
  PLUS4-VOCAL (both-vocal) and PLUS4-DOWN (the downward far
  move) stay 4 and rejected. Case 8.
Both MIK setcraft entries carry "Implemented (Phase 10)"
notes; entry 36 of the sources list records the discharge.

**Counts now:** registry **81** (unchanged — no new bases),
variants **319** (unchanged), knowledge 86 → **87** (+1
Club Ready entry), demos **107** (suite: 107/107 rendered +
verified clean). Verdicts
unchanged: ADOPT 59 / ADAPT 22. Selection: `check_select()`
green — "T-037 agreement + ranking sanity OK" — now including
Cases 6–8 (diagonal distance + admission split; key_move
signs + the exact +1.0 boost differential + the
falling-energy exclusion; the +4 gate's admission/rejection
split). The NEXT QUEUE in
`technique-bank/EDUCATIONAL-SOURCES.md` is refreshed —
Digital DJ Tips tops it; the proposals item is discharged
and off the queue.

## Phase 11 — Educationals study program: tranche 6 (2026-10-21)

Sixth tranche, worked the NEXT QUEUE top-down, items 1–4:
(1) Digital DJ Tips' transition coverage, (2) r/Beatmatch +
r/DJs, (3) the Sound on Sound remainder, (4) the Ableton
Live audio effect reference — the producer-side mirror of
the DJ catalogs. Yield: **one new base** (the first since
Phase 9 — and it was hiding exactly where the Phase 10
queue refresh predicted: producer-side semantics), three
axes, the community failure-mode set, and one knowledge
entry. All banked in TECHNIQUES (Phase 11 section).

- **Digital DJ Tips — zero new bases.** Their half/double-
  time article confirms T-021 Method A in full bar math
  (with the BYNX 85-over-170 compound as T-010 × T-021);
  the Tempo Trap contributes the **percussion-loop
  ferryman** as a staging axis of T-021 (the ramp target
  becomes a neutral loop, not a track — the render vehicle
  is the WEB-12 × T-021 compound) plus its floor-risk
  caveat on Method A; the timing "big cheat" resolves to
  T-004/T-005 with a tail-window entry axis; the acapella
  bridge resolves to the T-010 × GAP-11 × GAP-10 compound
  family; the Acapellas & Stems course's "sick beat"
  genre-change transition got the **French Candy
  disposition** (module title only — no mechanism in any
  free text). Course curricula state titles, not
  mechanisms; the paid school stays unmined.
- **r/Beatmatch + r/DJs — PARTIAL, evidence-limited (the
  Phase 10 Carlo model).** Reddit's hosts refuse the fetch
  in this environment; no account was created and nothing
  was posted. The item was worked from the readable
  practitioner community layer (DJ TechTools + Serato forum
  threads, DDJT reader threads — all read first-hand):
  a **stepped-tease gain axis** on `layered_emergence`
  (25/50/75/100% fader steps, four beats each), the
  **cue-tap telegraph** confirmed against T-019, the
  loop-buzz-pitch-slam resolved to the T-008 × T-032
  compound, and the **failure-mode set** — two vocals, two
  basslines, two melodies, hat brittleness, and one the
  catalogs never state: **kick-peak misalignment**
  ("not all kicks peak on the beat, and correcting it can
  cause your hi-hats and snare to fall out of time"),
  recorded against the beat-aligned bases and the QC
  gate's beat_phase check. DDJT's trainwreck-salvage
  repertoire went to `knowledge/setcraft.md` (+1 entry):
  the cut is every blend's abort state, which is why
  hard-cut-class exits carry no clash risk in selection.
  Entries 37/38 stand partial, the caveat stated in place.
- **Sound on Sound remainder — zero new bases.** Reverse
  reverb is a fourth independent source for DM-A23
  (already built); gated/level-keyed reverb is a
  send-gating axis on the reverb family; the ducked FX
  return is recorded against T-004/T-005 as the discipline
  that keeps exits intelligible under a vocal A; the
  **pre-entry dry-up** (dry the source before the entry so
  the entry lands bigger) is the send-riding axis's
  downward direction. Entry 58 stands mined.
- **Ableton Live reference — WEB-18 built.** *Resonators*
  is a genuinely new primitive: five parallel resonators
  tuned in semitones, decay pitch-dependent "similar to
  the behavior of an undamped piano string." Built as
  **`resonator_tail`** — A's final bars excite a five-comb
  bank voiced as a chord (major/minor/power/octave) on a
  root selection passes from B's tonic; the dry crossfades
  into the ring across the zone, and the ring decays under
  B's entrance. Every other tail carries A's pitch content
  forward (echo repeats it, reverb diffuses it, shimmer
  transposes it by a fixed interval); the bank replaces
  it — the tail keeps A's rhythm, its pitch becomes B's
  chord. *Spectral Resonator* banked as the same family's
  spectral sibling, not a second base. The tranche's
  sharpest dedupe: **Shifter's Pitch-mode + feedback
  Delay** — the planned second build — is Pioneer's
  SPIRAL mechanism and resolved onto **WEB-01
  `spiral_echo`** (second vendor); Beat Repeat's Pitch
  Decay is the same ladder in slice topology (T-008 axis)
  and Spectral Time's per-echo Shift is its third Ableton
  statement. Shifter's Freq mode (single-sideband) became
  a **mode axis of WEB-16** (Ring keeps both sidebands);
  Grain Delay → WEB-06 family; Hybrid Reverb's Shimmer
  algorithm is a second vendor statement of WEB-10's exact
  mechanism; the remaining roster (Chorus-Ensemble, Auto
  Filter, Echo/Delay, Vocoder, degradation and saturation
  rosters) overlap-resolved in full.

Selection smoke: `check_select()` green throughout
(incl. the P1–P3 guard Cases 6–8). Probes:
`resonator_tail` surfaces for a close-key pair (8A→8A, A
in breakdown — all three prefers fire, score 5.0) and is
gated out at Camelot distance 4 > its `camelot_max` 2.
One authoring catch, fixed before commit: the first
prefer named a non-existent feature (`camelot_distance`)
and silently never fired — the probe caught it; the
feature is `camelot`.

Counts (recounted from artifacts): registry 81 → **82**
(81 executable + 1 planning; 66 plan-renderable),
variants 319 → **332** across 53 → **54** bases,
knowledge 87 → **88**, verdicts ADOPT 59 → **60** /
ADAPT 22. Demo suite: **108/108 rendered + verified clean**
(`demos/out/verification.json`; resonator_tail record:
render_ok, silence_ok, headroom_ok all true). NEXT QUEUE refreshed in EDUCATIONAL-SOURCES.md:
Traktor Pro 4 non-FX chapters now lead; the Reddit
revisit sits at the tail, honestly conditional on a fetch
route opening.
