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

## Phase 12 — Educationals study program: tranche 7 (2026-10-21)

Seventh tranche, worked the NEXT QUEUE top-down, items
1–5: (1) the Traktor Pro 4 manual's non-FX chapters,
(2) Making Music (DeSantis), (3) James Hype, (4) DJ Phil
Harris, (5) Laidback Luke. Yield: **zero new bases**, six
knowledge entries, four axes/records — the tranche the
Phase 11 queue refresh predicted for the educator canon,
worked to depth. All banked in TECHNIQUES (Phase 12
section).

- **Traktor Pro 4, non-FX chapters — zero new bases,
  two knowledge entries.** The manual's Overview, Global
  Concepts, both tutorial chapters, and Cruise Mode read
  first-hand (manua.ls body). Flux Mode is the slip
  playhead model's second first-party statement (after
  rekordbox's Slip, Phase 8) and its crispest definition
  ("without losing the phrasing of your tracks... a
  second, virtual playhead continues forward"); Reverse
  Mode is the excursion run backwards on the same
  transport. QUANT/SNAP state the cue/loop bases'
  alignment layer as two halves (land on-grid / set
  on-grid). The Stem Deck is GAP-08's vendor control
  surface ("transitions between elements Stem by Stem";
  per-stem volume/filter/FX-send), and Traktor now
  *generates* stems in-app — GAP-08's `needs: stems`
  gate stands, its offline-prep assumption retired. The
  Loop Recorder (capture the mix output itself as an
  overdub-able loop) is `live_loop_mix`'s capture form;
  the Remix Deck is the WEB-12 layer family's sample
  surface. Two knowledge entries: **Tempo Master
  succession** (setcraft — AUTO mode's handover rule:
  master ends → the synced deck succeeds → the Master
  Clock stands behind both) and the **fade-marker pair**
  (workflows — Fade Out/Fade In cue points as
  declarative transition authoring, Flip's second
  vendor form, performed by Cruise Mode).
- **Making Music — PARTIAL by edition, two knowledge
  entries.** The free web edition publishes 24 of 74
  chapters; its transition-relevant chapters were read
  first-hand on the official site. **Fuzzy Boundaries**
  (producing) — the staggered seam: extend/retract/
  delete per track so the boundary goes jagged, which
  is GAP-08's staging stated for arrangement; its fine
  moves name the **fill-timing axis** (anticipation —
  peak before the downbeat; hesitation — overrun it).
  **Unique Events** (producing) — single events /
  musical gestures / processing gestures as one-time
  seam punctuation, with the restraint rule. The
  Asynchronous/Polyrhythmic Loops chapter corroborates
  the Phase 10 fractional-length axis from the producer
  side. "Foreground, Middle Ground, and Background" and
  "Short Loops as Endings" are NOT among the free 24 —
  named from the published TOC only, text unread; the
  full book is $30, his per-item call. No claim rests on
  them or on any unofficial copy.
- **James Hype — zero new bases.** Pioneer DJ's "How I
  DJ" episode (description/timeline first-hand; spoken
  content at published-summary weight, flagged) + his
  verbatim course-page doctrines. **Acapellas as "the
  glue"** confirms the T-010 × GAP-11 compound with its
  named practitioner and completes the vocal-led
  staging Carlo's Phase 10 note opened: vocal solo →
  loop → next backing filtered up underneath (the Phase
  11 DDJT sighting, now artist-confirmed). The "track
  elements" doctrine states GAP-08's premise in the
  artist's words. **"Hype Loops"** banked as a named
  compound — its engine link (GAP-02
  `loop_tightening_build`) predates the program; the
  course module confirms the extraction.
- **DJ Phil Harris — zero new bases, the Carlo-model
  caveat.** The transcript host rate-limited the full
  pages (HTTP 429, not retried); all banked claims are
  verbatim transcript text via the search index. Yield:
  the **Levels stack** — five passes over one pair,
  escalating; Level 1 (EQ + phrasing) is the whole
  foundation ("no point adding anything else... if the
  EQing and phrasing isn't taken care of first") and
  Level 2's effects are framed as *cleanup* ("help
  clean up the mix in or mix out") — the registry's
  implicit layering order stated as teaching doctrine —
  and phrase mixing's staging rule (B's intro starts
  halfway through A's outro; A's low EQ surrenders as B
  rises).
- **Laidback Luke — zero new bases, one axis, two
  knowledge entries.** His DDJT course curriculum (paid,
  unmined) is his named-mix taxonomy: "Bait & Switch" →
  `fake_drop`'s performer name; "Scratch Drop" → the
  T-014 compound; wordplay → T-020 with Luke as second
  named practitioner; "Delay Doubles" recorded
  name-only (mechanism unpublished in free text, the
  "sick beat" handling). **"Element Matching"** banked
  as `genre_bridge`'s staging axis — a shared element,
  not a ramp, licenses the leap (workshop-corroborated:
  "looking for similarities between songs").
  **Tempo ≠ energy** (setcraft) — the Tempo
  Rollercoaster doctrine: tempo and energy scored
  separately, each spendable while the other holds.
  Performers entry (performers): 60-tracks-an-hour
  quick-mix density, manipulation as the style, scratch
  competence as recovery insurance (verbatim).

Selection smoke: `check_select()` green (incl. the
P1–P3 guard Cases 6–8). Probe: a wide leap pair (128 →
150 BPM, key distance 5, house → hardstyle) ranks the
void/reset class on top (echo_out 8.0, hard_cut,
infinity_filter) — the element-bridge/reset doctrine
the Element Matching axis describes, behaving as
encoded. No engine changes this phase.

Counts (recounted from artifacts): registry **82**
(unchanged — 81 executable + 1 planning; 66
plan-renderable), variants **332** across **54** bases
(unchanged), knowledge 88 → **94** (+2 setcraft, +2
producing, +1 workflows, +1 performers), verdicts
unchanged: ADOPT 60 / ADAPT 22. Demo suite: **108/108
rendered + verified clean** (`demos/out/
verification.json` — no new demos; no engine or spec
changes). NEXT QUEUE refreshed in
EDUCATIONAL-SOURCES.md: DJ TechTools' remainder now
leads; the Reddit revisit stays at the tail.

## Phase 13 — Educationals study program: tranche 8 (2026-10-21)

Eighth tranche, worked the NEXT QUEUE top-down, items
1–5: (1) DJ TechTools, remainder, (2) Serato
documentation, remainder (Pitch 'n Time + Stems),
(3) DJ TLM, (4) DJ Angelo, (5) Engine DJ, remainder.
Yield: **zero new bases**, four knowledge entries, and
a run of axes/premises — the tranche the Phase 12
refresh predicted for the worked-over canon: what
remains is confirmation with sharper edges, and the
edges here were real. All banked in TECHNIQUES
(Phase 13 section).

- **DJ TechTools, remainder — zero new bases, one
  knowledge entry.** Seven archive articles read
  first-hand (2008–2016). Cue Point Juggling (2008)
  is the cue family's origin statement: direct play
  vs sample play ("sample and hold" — the gated
  trigger mode Phase 10 banked on T-019, at its
  origin), and its durable content is a prep rule,
  banked to knowledge/workflows: the **five-cue
  layout** (kick / snare / hat / fill / section, same
  roles on every track). The Advanced Cue Point
  Scratch resolves to a T-019 × T-017 compound with
  its fixed chain decomposed (lo-fi > Filter LFO 92
  > reverb > peak filter); Controltablism (John
  Type, 2016) banks T-019's trigger-source axis
  (finger / gated / sequenced — cues as programmable
  patterns). The 2014 transition chains decompose
  (T-008 × T-003 × T-005; gate × T-003 × T-005) with
  their harmonic-thinning rationale recorded against
  T-004; EQ Mixing (2012) completes T-001's named
  modes with **Tone Matching** (the pair's shared
  timbre as the blend's EQ target); Advanced Key
  Mixing (2013) corroborates the selection layer
  three ways (Energy Swap = the P1 diagonal;
  Absolute Major/Minor = the parallel move; the
  Energy Boost arithmetic = MIK's, independently
  stated) and names the loop family's harmonic-
  ferryman staging; Value-Added Mixing contributes
  the Bridge-the-Mix material constraint on WEB-12 /
  GAP-16, a divergent +3 Camelot lift recorded but
  not adopted (MIK governs), and a restraint
  corroboration.
- **Serato, remainder — zero new bases, one axis.**
  The Stems articles are GAP-08's second vendor
  control surface (four stems + Acapella/Instrumental
  one-button groups, real-time separation). **Stem
  Pad FX** bank GAP-08's **FX-scope axis**: FX Vocal
  Echo / FX Instrumental Echo / FX Drums Echo /
  Instrumental Braker are T-004 and T-006 with their
  scope narrowed to a stem group at the seam —
  Traktor's per-stem sends were the continuous form;
  Serato's is the pad-fired exit throw. Pitch 'n
  Time DJ (the support article + three quickstart
  Key Shift sections, identical across devices) is
  the key-shift capability provenance under T-015 /
  T-032: semitone pad ranges, Key Sync, Pitch Play —
  the control the selection layer's key_move
  arithmetic presumes.
- **DJ TLM — zero new bases, one knowledge entry,
  the evidence shape stated in the bank.** His deep
  canon is the paid DJ Courses Online subscription
  (unmined; his per-item call). The free footprint:
  his school's blog read first-hand (Bartmann
  bylines) + podcast topics at title weight. Yield:
  the **post-fader premise** under T-004/T-005 (the
  tail outlives the cut because the send is
  post-fader; reverb 50% wet / ~10 s decay is the
  worked example), the **reset** doctrine (FX in a
  phrase's last 2–4 bars, cut at the boundary — the
  exit family run as intra-track punctuation), the
  **throwback** (knowledge/setcraft: the layer
  family's source axis set to *previously played*),
  and corroborations (Hard Swap, anticipation
  arithmetic, the glue track).
- **DJ Angelo — zero new bases, one knowledge
  entry.** Worked from his published canons (the
  Turntable Tutorial Collection's episode list; the
  full Tricks & Transitions curriculum) at the Luke
  precedent's weight. The scratch canon banks as
  **GAP-14's pattern axis** — tear (faderless) /
  stab / transformer / chirp / flare-n-click / crab,
  in his teaching order: a rendered scratch-in now
  names its pattern. Beat juggling resolves to
  T-031's manual form + its loops/pauses variants;
  his course's named forms resolve to compounds
  (acapella switch → GAP-13 × GAP-10; acapella
  bridge → T-010 × GAP-11, third named practitioner;
  tone/pitch play direction + sliding axes on T-032;
  tone play × key shift as a stated compound).
  Beat chasing recorded name-only (no mechanism in
  his free text; DM-A21 noted as candidate, not
  asserted); Autobahn / Boomerang name-only (the
  "Delay Doubles" handling). Knowledge: performers
  (Angelo — the turntablist as transitionist; 4PLAY
  as the deck-count extreme performed with
  restraint).
- **Engine DJ, remainder — zero new bases, one
  knowledge entry.** The 3.2 + 4.1 release articles,
  the Prime GO manual's Pad Modes/Stems sections,
  and the X1850 mic settings, read first-hand.
  Engine OS Stems are GAP-08's **third vendor
  surface** with the prep divergence stated plainly:
  stems are created in the desktop software and
  *packed to a drive* — Serato separates in real
  time, Traktor generates in-app, Engine pre-renders;
  the gate's satisfiability is vendor-shaped, the
  crossfade identical. **Fuzzy Key Sync** →
  knowledge/setcraft (Strict = same key, Fuzzy =
  closest compatible key — the sync target as a
  compatibility set, the third first-party anchor
  for the model select.py scores). Flex Gate banks
  the gate family's pattern axis (patterns
  synchronize to the track's phase; the X1850's
  16-pattern Beat Break Edit is the storage end).
  Slip on Prime GO is GAP-05's third vendor
  statement; Active Loops bank the loop family's
  position-armed trigger (the fade-marker authoring
  model applied to loops); the X1850 talkover
  settings give GAP-18 its parameter set (level
  −40…−20 dB, resume Normal/Fast, gate threshold);
  Instant Doubles is DM-A21's Denon surface.

Selection smoke: `check_select()` green (incl. the
P1–P3 guard Cases 6–8). Probes: a stems-available
house pair co-leads `stem_element_crossfade` at 8.0
alongside `eq_blend` (the GAP-08 material behaving as
banked); an open-format hip-hop pair ranks
`scratch_in` with its snap exit and the open-format
norm reason. No engine changes this phase.

Counts (recounted from artifacts): registry **82**
(unchanged — 81 executable + 1 planning; 66
plan-renderable), variants **332** across **54**
bases (unchanged), knowledge 94 → **98** (+1
workflows, +2 setcraft, +1 performers), verdicts
unchanged: ADOPT 60 / ADAPT 22. Demo suite: **108/108
rendered + verified clean** (`demos/out/
verification.json` — no new demos; no engine or spec
changes). NEXT QUEUE refreshed in
EDUCATIONAL-SOURCES.md: the rekordbox manuals'
remainder now leads; the Reddit revisit stays at the
tail.

## Phase 14 — Educationals study program: tranche 9 (2026-10-21)

Ninth tranche, worked the NEXT QUEUE top-down, items
1–5: (1) rekordbox manuals, remainder, (2) A-Trak,
(3) Passionate DJ, (4) EDMProd, (5) Rob Swift. Yield:
**zero new bases**, five knowledge entries, and the
tranche's real product — genealogy: the practitioners
themselves stating which families descend from which.
All banked in TECHNIQUES (Phase 14 section).

- **rekordbox manuals, remainder — zero new bases,
  one knowledge entry.** The rekordbox 7 FAQ + plan
  pages, the MIX POINT LINK FAQ, the Instruction
  Manual's KEY chapter, and the DDJ-FLX10 manual's
  Mix Point Link pages, read first-hand. **STEMS**
  are GAP-08's **fourth vendor surface** — real-time
  separation (like Serato's), with ACTIVE STEM
  mute/solo toggles, STEM ISO per-stem volume knobs,
  and STEM FX — completing the cross-vendor
  comparison (Traktor in-app generation, Serato
  real-time + pad throws, Engine desktop pre-render,
  rekordbox real-time + ISO), and adding the
  **stem-granularity axis** (3 stems folds BASS into
  INST; at 4, the bass hand-off can run inside the
  surface) plus the mute axis's solo form. **KEY
  SYNC** is the exact-target pole of the sync-target
  question (against Engine's Fuzzy set, Phase 13);
  KEY SHIFT (±12 pad mode) and KEYBOARD (cue-bound
  pitch play) complete Pioneer's key-shift
  provenance under T-015/T-032. **MIX POINT LINK**
  → knowledge/workflows: paired-point cross-deck
  authoring whose SILENT form pre-rolls the incoming
  track *muted* under the outgoing one — the seam as
  a level event, not a start event — with the FLX10
  manual's cancel/relink state semantics. **GROOVE
  CIRCUIT** is drum replacement's Pioneer surface:
  the drums stem's axis gains its **replace** value.
- **A-Trak — zero new bases, one knowledge entry.**
  Three interviews read first-hand (DJ Times 2007,
  Fusicology 2010, the 2014 #RealDJing post). The
  **notation method** (his coinage, first-person) is
  GAP-14's composability premise: scratch patterns
  are discrete enough to write, so routines are
  scores. **Transformer on the acapella** ("I'd grab
  the a cappella and transform the singing part…
  in question-and-answer style with our background
  singer") banks as a named GAP-14 × GAP-10/11
  compound — the chop scoped to the vocal over a
  clean re-played beat. **Staged element entry**
  (acapella chorus first, drums entering a verse
  later on the other deck) corroborates the layer
  family's vocal-led order axis with its second
  named practitioner. Knowledge: performers — risk
  as obligation, legibility as the routine's
  constraint.
- **Passionate DJ — zero new bases, one knowledge
  entry.** "The Art of EQing" (2013) and "Restraint
  & Patience" (2017) read first-hand. The EQ essay
  banks **T-003's off-key entry form**: lead an
  off-key track in on "just the very tip-top of the
  audio spectrum" — hats and a touch of vocal carry
  rhythm with no pitch commitment while the
  outgoing track owns the harmony — and corroborates
  Tone Matching from the record-box side. The
  restraint essay → knowledge/setcraft: energy
  headroom as a budgeted set-level resource, density
  moves named as value-subtractors. Caveat recorded
  in the bank: "It's OK to Let It Play" failed to
  load in this environment and stands unread.
- **EDMProd — zero new bases, one knowledge entry.**
  "The Art of Turnarounds" (2023) and the build-up
  guide read first-hand. The **nine turnarounds**
  resolve onto the registry (silence + pickup, drum
  fill, DIY sweeps, filter scopes, reversal + its
  pickup form, character delay, pitch punctuation,
  clap build) under the source's own frame — a
  turnaround is the producer's name for the phrase-
  end seam. **Render and Process** → knowledge/
  producing: the seam manufactured offline from the
  track's own rendered tail is GAP-07's producer
  form. The **Filter Master** completes T-003's
  scope axis with master-with-exemption (the whole
  bus low-passed, one vocal left unaffected to carry
  the seam). The build-up guide states T-018's
  pitched forms as craft (pitch-automated snare
  rolls; bounced reverb tails, pitched).
- **Rob Swift — zero new bases, one knowledge
  entry.** His own teaching texts (the backspinning
  guide, "Don't Think, Feel", the Cardinal Rules)
  and DJTT's lessons roundup, read first-hand. The
  **backspin → juggle lineage** is stated by the
  lineage source himself: backspinning on doubles,
  "start off linear, then expand the order of your
  Juggles… a new cycle… then a new cycle after
  that" — T-031 descends from T-007 by the **cycle
  axis**, on the material condition of the doubles
  pair. The **Single Paradiddle** banks as GAP-14's
  rudiment level (patterns as stroke sequences over
  a Forward/Back alphabet), and stab primacy
  corroborates the axis ordering. His **patterns-
  exist-in-the-record** doctrine is recorded as the
  discovery pole against A-Trak's notation — the
  two poles of one family, both banked. Knowledge:
  performers — Scratch Synchronicity, the scratch
  family's ensemble constraint.

Selection smoke: `check_select()` green (incl. the
P1–P3 guard Cases 6–8). Probes: a stems-available
house pair co-leads `stem_element_crossfade` at 8.0
alongside `eq_blend` (the GAP-08 material, now with
its four vendor surfaces banked); an off-key pair
(8A → 3A) clash-rejects `eq_blend` and tops out on
the filter family (`filter_sweep` / `infinity_filter`
at 6.0) — the off-key entry behavior the Passionate
DJ essay describes, as encoded. No engine changes
this phase.

Counts (recounted from artifacts): registry **82**
(unchanged — 81 executable + 1 planning; 66
plan-renderable), variants **332** across **54**
bases (unchanged), knowledge 98 → **103** (+1
workflows, +2 performers, +1 setcraft, +1
producing), verdicts unchanged: ADOPT 60 / ADAPT 22.
Demo suite: **108/108 rendered + verified clean**
(`demos/out/verification.json` — no new demos; no
engine or spec changes). NEXT QUEUE refreshed in
EDUCATIONAL-SOURCES.md: the Denon Prime manual bodies
now lead; the conditional items (educator revisits,
Cambridge, the Reddit revisit) hold their places at
the tail.

## Phase 15 — Educationals study program: tranche 10 (2026-10-21–22)

Worked the Phase 14 NEXT QUEUE top-down: (1) the
Denon Prime manuals' remainder, (2) DJ Jazzy Jeff,
(3) Ean Golden / DJ TechTools (YouTube), (4) In The
Mix, (5) Multiplier. **Zero new bases.** Knowledge
103 → **107**. Two items land as honest partials —
the tranche's yield is concentrated in the device
manual body and the performer/controllerist record,
and its tail is now explicit about which of the
list's promises were environment-shaped rather than
real.

Item 1 (Denon Prime manuals, remainder): the
current-generation Engine OS manual body (109 pp.,
shared PRIME 4 / 2 / GO / SC LIVE) read first-hand
beyond the FAQ and GO passes of Phases 8/13. The
**Stems Mode body completes GAP-08's Engine
surface**: pads isolate Vocal / Melody / Bass /
Drums as mute toggles; the **Parameter buttons are
one-press group isolations** (◀ Acapella, ▶
Instrumental; absent on PRIME GO); the access model
splits by generation — automatic on PRIME 4+, a
one-time license on every other Engine OS device —
and the desktop-create + pack-to-drive prep model is
restated verbatim, so the four-surface comparison
(Traktor in-app, Serato real-time, rekordbox
real-time, Engine pre-render + pack + license) now
stands at manual depth throughout. **Fader Echo**
(Control Center / Toolbar body, verbatim) banks as
T-004's gesture-triggered trigger-form: the exit
gesture itself fires the echo tail — the operator
Pioneer ships as Smooth Echo, stated by a second
vendor, on standalone hardware, as a global deck
behavior. Knowledge: workflows — **Playlist Deck**
(the automated-crossfade deck: one global crossfade
time over a list; the authoring spectrum's
automation pole against Cruise Mode's fade markers
and MIX POINT LINK's paired points) and **Ableton
Link** (sync as federation — beat/phase/tempo held
in common over a network, lead tempo adjustable from
any peer — against Traktor's Tempo Master
succession). Corroborations at body depth: Slip /
Censor bodies, Key Sync long-press + the Key Change
Menu, Auto Loop 1/32–64, flexible beat grids (Insert
Anchor), Stop Time, X Fader Contour — and the
**Sampler Mode body supersedes Phase 13's FAQ-era
"16 slots on Prime 4+" with eight slots** (Roll
pressed twice; second bank on GO / SC LIVE 2).

Item 2 (DJ Jazzy Jeff): a 1988 first-person
interview (Phaze 1, via muzines), the Serato Icon
film's coverage (DJWORX / MN2S / DDJT), and the
biographical record (PBS's Art of Turntablism;
encyclopedia.com; The Skinny, 2007), all first-hand.
Zero new bases. **Transformer** gains its provenance
on GAP-14's pattern axis — Philadelphia, mid-1980s,
Spinbad / Cash Money / Jeff, invention banked as
contested (PBS co-invention; the 1988 interview
Jeff's claim; encyclopedia.com: some credit Cash
Money, Jeff first to record) — plus its hardware
consequence: the pattern demanded a crisper fader
cutoff than stock mixers had and pushed the modern
crossfader's redesign. **Chirp** is Jeff's outright
(The Skinny: "his own invention," debuted on "The
Magnificent Jazzy Jeff," 1987) — two of the axis's
six named patterns now trace to one Philadelphia
lineage, and both names are onomatopoeia. The 1988
interview's **decoupling layer** (mats off; 45s, wax
paper, cut-up album covers between record and deck)
banks as the scratch family's material premise — the
slipmat's improvised ancestor — and its first-person
**drop** dates the pre-beatmatch transition default.
The **Peter Piper routine's** published structure
(MN2S's account of the 2015 film: acapella fore →
synth stab scratched into a new rhythm → vocals +
instrumental combine over dropped-in drumbeat
moments → the vocal tag) is the vocal-led order
axis's third practitioner, banked at summary weight.
Knowledge: performers — his two-phase doctrine
("The turntables are mastered. Now it's just a
process of making up new techniques") and study
method ("Examine everybody else's techniques and
learn from them… but use them in your own way").
Caveats: his DDJT courses (How To DJ Right; Scratch
Skills Masterclass) are paid — unmined, his
per-item call; the Rolling Stone Playlist Retreat
feature is blocked in this environment and stands
unread, recorded at headline weight.

Item 3 (Ean Golden / DJ TechTools, YouTube): the
channel's mechanism text layer (DJTT's Instant
Gratification demystification, 2014; Twisted
Gratification, 2016, Golden first-person; the
one-button-builds article, 2014; the VCI-400 Ean
Golden edition statement, 2012; the Midi Fighter
maps pages) — the Angelo standard: mechanisms bank
from the texts that state them. Zero new bases.
**Instant Gratification** resolves as T-017's
performed form — *atomic total state recall*:
≥7 mapping commands per press (selector, parameters,
dry/wet, routing on for the target deck and off for
all others, unit mode) so "one magic button *always*
work[s]"; banked to knowledge/workflows as total
state recall, the authoring rule the registry's own
specs obey. The demystification's **rate-row
press-count hold** (a modifier counts held Beatmasher
rate buttons 0–7; the effect dies only at count 0)
is the gate family's performed wiring — rates played
as a keyboard over one continuously gated masher.
**One-button builds** are T-018's held-gesture form:
snap-to-start, auto-repeat ramp while held,
release-with-tail. **Fader effects** complete the
gesture-coupling genealogy across three layers —
mapping (Golden, 2008–2011: fader travel zoned, cut
first, FX depth after) → mixer feature (Pioneer
Smooth Echo) → device behavior (Denon Fader Echo,
item 1) — each layer coarsening the coupling as it
hardens. **Twisted Gratification** banks the
macro-knob form (one knob, a three-FX chain along
pre-tuned ranges) and the designed exit (Release FX:
press = echo freeze + kill all FX; hold = filter the
freeze); **Midi Fighter 3D motion** records attitude
as a modulation source against Phase 9's
modulation-source layer. Knowledge: workflows +1
(total state recall carries the Twisted forms).

Item 4 (In The Mix): **PARTIAL — episode level
unevidenced in this environment; nothing banked.**
Michael Wynne's channel identity and scope confirmed
first-hand (channel page; Wikitubia history — first
video April 2017, a sidechain tutorial; gearnews),
but eight targeted searches surfaced no transition
episode by name, the channel listing is JS-gated to
the text fetcher, and the Mastering The Mix blog
carries no transition article. Two attribution traps
were opened and **rejected**: a transition-dense FL
Studio course transcript in the same results is
Miguel's (Mad Miguel), and an arrangement
masterclass naming "the turnaround and the marker"
is Underdog's Oscar (Triangle Method) — neither
banks under this entry. Entry 50 stays open at the
queue tail, conditional on a readable video-ID
source (the transcript host itself is reachable; IDs
are the missing piece).

Item 5 (Multiplier): **PARTIAL — the canon is paid;
the free channel is evidenced at listing weight
only; nothing banked.** Adam Pollard's identity
confirmed across the Ask.Video listings, Blue Cat's
tutorial index, and Point Blank's channel roundup.
His mechanism canon is the paid Ask.Video /
macProVideo series — *Dance Music Styles 102:
Dubstep*, the *Dance Sound Design* set (Bass, Lead
Synths, Pads, Vocals), *Advanced Vocals for Sound
Design* (resampling, FM vocal conversion,
interpolation settings, bespoke wavetables) —
listings name topics, not mechanisms, and are banked
at that weight; unmined, his per-item call. Point
Blank's roundup characterizes the free channel
(concept-forward: "how a limiter actually listens to
your audio," wavetables into an analog synth,
chord-writing approaches) and names one video
(rq6NCdxk_4E, workflow tips) whose transcript fetch
returned the host's 429 — the Carlo caveat verbatim;
no transition episode was evidenced at transcript
weight. Entry 51 stays open at the queue tail on
either condition: the 429 clearing, or his call on
the paid canon.

Selection smoke: `check_select()` green (incl. the
P1–P3 guard Cases 6–8). No engine or spec changes
this phase — the recount below was verified against
the live engine (`variants` regenerates to 332;
meta verdicts tally ADOPT 60 / ADAPT 22).

Counts (recounted from artifacts): registry **82**
(unchanged — 81 executable + 1 planning; 66
plan-renderable), variants **332** across **54**
bases (unchanged), knowledge 103 → **107** (+3
workflows, +1 performers), verdicts unchanged:
ADOPT 60 / ADAPT 22. Demo suite: **108/108 rendered
+ verified clean** (`demos/out/verification.json` —
no new demos; no engine or spec changes). NEXT
QUEUE refreshed in EDUCATIONAL-SOURCES.md: Alex Rome
and Zen World now lead the producer class; Underdog
(entry 73) is promoted on evidence found this
tranche — its arrangement masterclass transcript was
read first-hand during item 4's attribution check and
carries bankable turnaround/marker material, queued
rather than banked out of turn; entries 50/51 hold
their conditional places at the tail.

## Phase 16 — Educationals study program: tranche 11 (2026-10-22)

Tranche 11 worked the Phase 15 NEXT QUEUE top-down:
the producer-YouTube class — (1) Alex Rome,
(2) Zen World, (3) Underdog Electronic Music
School, (4) Hyperbits (free surface only),
(5) Bound to Divide. Zero new bases; the yield is
six knowledge entries, all in the producing layer,
and two honest partials. The tranche ran under
tranche 10's attribution discipline throughout:
open the material, name the presenter, then bank.

Item 1 (Alex Rome): his named doctrine, the **Two
Loop Rule**, banks to knowledge/producing as the
arrangement-cadence law — the arrangement changes
every two loops of the chords/main elements (two
loops = 8 bars at the common 4-bar loop), from a
small change vocabulary (add/remove an instrument,
add/remove expression, MIDI transfer to another
instrument, rhythm change), with seams worked
(entry-point effects; full cut → drum fill + crash
at the drop; the lead transferred to a pad and
rested through the build). Evidence weight recorded
in place: summary + trade press (MusicTech's
account; the Woovebox manual's independent adoption
restating the 8-bar equivalence) — the video's
verbatim transcript was not read in this
environment. His transitions canon proper is the
paid Teachable course *EDM Fundamentals* ("Building
Transitions and FX"; "Using Automation to Create
Tension") — curriculum level only, unmined, his
per-item call.

Item 2 (Zen World): **PARTIAL** — identity and
method confirmed first-hand from the Boomcast
interview (full timestamped transcript read); his
doctrine banks to knowledge/producing as **use over
sound**: identity lives in the processing gesture
applied to known material (a stock saw + a gate = a
signature), learned by reverse-engineering presets.
No transition/FX-build episode was evidenced at
transcript weight (the transcript index returned
none of his tutorials), and his current output
(EvoSounds) is Patreon-first, member-gated past the
introduction. Nothing banked from titles or teasers;
the entry stays open on the producer-partial
conditions.

Item 3 (Underdog): the tranche's richest yield,
both videos read in full at transcript weight.
**Turnaround and marker** bank to
knowledge/producing as the producer seam's two-part
anatomy: the turnaround signals the ending (lows
energy removed, reversed reverb swell, noise
riser); the marker is the splash on the transition
itself — including the **marker by subtraction**
(the false drop's absent first hit *is* the placed
event), markers manufactured from the track's own
timbres, and the seam-pronunciation dial (explicit
vs hypnotic edges). The **trilogy break** banks as
a named staging compound (sparse → build ×3 →
silence → drop), decomposed onto existing families,
at reference weight. The **four levels of
arrangement** and the **element-inventory study
method** complete the item (+3 knowledge in all).
Zero new bases — everything decomposes.

Item 4 (Hyperbits, free surface): the **mono-build
trick** banks to knowledge/producing at full
parameter spec — stereo image automated toward
mono across the build (4–8 bars, capped 40–60%) so
the drop's width lands by contrast — knowledge-
class under the standing mono-engine precedent
(stereo automation, A-42), recorded whole so the
spec survives a future stereo engine. The build-ups
article's **master-bus automation** (level dip
1–2 dB + low-cut/resonance + reverb across the
build) is recorded on T-003's scope axis as its
practitioner statement and level form; entrance
doctrine corroborated (a third statement, after
Oscar and Zen World, that the presentation of a
sound outranks the sound). The masterclass is paid
and untouched.

Item 5 (Bound to Divide): **PARTIAL** — identity
confirmed (Julian van Straten; Basic Wavez
founder); his arrangement/transitions teaching sits
inside paid courses (Basic Wavez, Sonic Academy,
PML) at curriculum weight, unmined, his per-item
call (pirate mirrors surfaced by the searches are
never a route). The one transcript indexed under
his name is a PML multi-tutor compilation whose two
transition mechanisms (a standing return-chain
transition bus; a freeze-and-reverse vocal riser)
are individually unattributed — **rejected under
this entry** by the attribution discipline, and
recorded in the bank against entry 77's surface to
be attribution-checked when Production Music Live
is worked.

Selection smoke: `check_select()` green (incl. the
P1–P3 guard Cases 6–8). Probe: a same-key house
pair whose B carries a build into a drop ranks
`eq_blend` top with the build family
(`loop_roll_build`, `loop_tightening_build`,
`layered_fx_stack`) in the leading group at 4.0 —
the build family behaving as banked in a tranche
that banked three producer statements of build
doctrine. No engine or spec changes this phase.

Counts (recounted from artifacts): registry **82**
(unchanged — 81 executable + 1 planning; 66
plan-renderable), variants **332** across **54**
bases (unchanged — `variants.count()` re-run),
knowledge 107 → **113** (+6, all producing —
verified by the `### ` count across knowledge/*.md:
113, with each new entry physically in
knowledge/producing.md per the Phase 15 lesson),
verdicts unchanged: ADOPT 60 / ADAPT 22 (tallied
from engine meta). Demo suite: **108/108 rendered
+ verified clean** (`demos/out/verification.json`
re-read: 108 records, render/silence/headroom all
true — no new demos; no engine or spec changes).
NEXT QUEUE refreshed in EDUCATIONAL-SOURCES.md:
Production Music Live leads (its surface now also
carries the attribution check owed from item 5),
then the rekordbox controller bodies and Point
Blank, with the two conditional clusters held at
the tail.

## Phase 17 — 2026-10-22 (EDUCATIONAL TRANCHE 12)

Queue items 1-5 of the Phase 16 NEXT QUEUE, worked
to depth. Yield: zero new registry bases (82 stays:
81 executable + 1 planning, 66 plan-renderable),
zero new variants (332 / 54 bases), +2 knowledge
(113 → 115; producing 45 → 46, setcraft 20 → 21),
no engine or spec changes, no new demos (suite
108/108 rendered + verified clean, unchanged).
Every item was dispositioned into the bank and the
sources list incrementally as it closed.

Item 1 — Production Music Live (77), the
attribution debt from Phase 16 discharged. The
"7 Melodic House Tips" compilation was re-read in
full at transcript weight: the source page names
PML as author, the tips run in PML's voice with no
per-tip attribution (one teaches PML's own
Spacemaker), and the closing program promo maps
tutors to program steps — none of them a
transition step. The Phase 16 rejection of both
mechanisms under Bound to Divide therefore
stands, and both bank under PML at publisher
weight: the standing transition bus (return
track, full-decay reverb high-passed, drum-bus
send automated at every transition, optional
sidechain at the chain end) joins
knowledge/producing as the T-004/T-005 throw's
template form — Rome's entry-point effects and a
premade band bus are its partial kin — and the
freeze-and-reverse vocal riser (freeze the wet
vocal, reverse the tail, lay it before the dry,
ping-pong to smooth) is DM-A23's manufacture
axis, GAP-07's render-and-process family. The
Spacemaker is recorded as ducking's
frequency-selective instrument, briefly. A PML
article on arrangement corroborates (three
introduction automations; the outro strips to
main drums for the DJ mix-out); the paid course
catalogue stays at curriculum weight, its two
named transition lessons recorded.

Item 2 — the rekordbox controller bodies (32,
partial remainder). The CDJ-3000 manual body,
read first-hand, states Key Sync's candidate set
verbatim: "the key … with the least change among"
the same key, dominant, subdominant, relative,
and the relatives of both fifth-neighbors — the
refined-distance neighborhood exactly, the
compatibility model's fourth first-party anchor
and its first from player hardware; banked in
knowledge/setcraft (the second setcraft entry of
Phase 14's rule, now at hardware weight). The
DDJ-REV5 manual gives T-021 its one-button device
form — Auto BPM Transition (ramp over 1/2/4/8
bars, three selectable targets) — with a stem
pre-mute coupling that enters GAP-08's family as
the pre-mute axis, plus preselectable Key Lock
and Auto Loop states; the REV7 adds Instant
Scratch (hardware-resident samples, T-019's
trigger source) and two Beat FX decomposed as
compounds of standing bases (Duck Down =
T-008 × tapestop; Fill Out = T-008 × T-004), with
Helix Out recorded as WEB-07's vendor sibling
(fade term in tow); the REV1 gives GAP-14 its
device-automation form, Tracking Scratch. The
XDJ line closed at feature-list weight, stated as
such.

Item 3 — Point Blank Music School (16). Worked
from the school's own site: Oakenfull's
arrangement lecture read in full at transcript
weight, deconstruction pages at article weight.
Zero new bases, no knowledge: the withheld beat
(Harris's chorus that stages and holds back until
the true chorus; Armin's beat held past the
chorus boundary) is recorded as the build
family's section-scale form and the second-verse
release (drums out 4–8 bars post-chorus, or a
counted new element) as the layer family's
section form; the tempo-synced-reference study
method corroborates Oscar's element inventory at
section scale (already standing in
knowledge/producing); the Pjanoo deconstruction's
closing acapella mashup is a T-010 practitioner
statement. Paid courses untouched.

Item 4 — Produce Like A Pro (55). Zero new
bases, no knowledge. Marc Daniel Nelson's vocal
template, read first-hand on the school's own
site: the ducked FX return's full named form —
delay return sidechain-ducked under the dry vocal
so no repeat sounds during the phrase, the bloom
arriving into the reverb at phrase ends, template
not automation — completing Phase 11's one-line
Sound on Sound record against T-004/T-005. Warren
Huart's one-reverb staged pre-delays (vocal
0 ms / piano ~20 / bass ~40 / drums ~60 into one
shared reverb, feed high-passed ~300–400 Hz)
banked as T-005's depth axis at vendor-quoted
weight. The wider mixing canon evidenced is mix
craft without seam content; the paid academy
untouched.

Item 5 — Pensado's Place (56). Worked from his
published interview text (verbatim, first-hand)
and Lair-episode summaries, for the assigned tail
and level craft. Zero new bases. Banked: the
vocal-fill delay at bars 8/16 as the throw
family's signal form ("the 'here comes the
chorus' cue" — the throw as the marker Oscar
named); the gated reverb keyed to its own source
(the gate's key is the dry vocal; the tail's
lifetime is the phrase's) with his silence
doctrine recorded as the tail-hygiene principle's
practitioner statement, and the octave-harmonizer
reverb feed as WEB-10's feed-side form; imperfect
(off-grid) delays as the delay family's timing
axis, recorded at forum-report weight with the
caveat in place; the Herbert effect — FX returns
darkened — as the tail family's top-side spectral
hygiene, at summary weight.

Selection smoke: check_select() green including
the P1–P3 guard cases. Probes: a diagonal
8B → 9A house pair measures camelot distance 2
(the CDJ candidate set's own diagonal) — bass_swap
leads the ranking at 6.0 while eq_blend is vetoed
by this pair's coexisting vocals, the distance
admitting the family and the vocal gate doing its
own job; a same-key 120 → 140 pair (16.7%) lifts
the tempo-bridge family to co-lead (tempo_bridge
+ premade_tempo_bridge_edit at 4.0 — "wide BPM
gap — ramp it or shift the metric"), the family
item 2 just gave a one-button device form.

Counts recounted from artifacts: registry 82
(techniques/*.md = 83 with INDEX), variants
332 / 54 bases, knowledge 115 (mixing 18,
performers 14, producing 46, setcraft 21,
workflows 16), verdicts ADOPT 60 / ADAPT 22
(tallied from engine meta), demos 108 records —
all render_ok / silence_ok / headroom_ok.

The NEXT QUEUE at the end of EDUCATIONAL-SOURCES.md
was refreshed at the end of this phase: Mr. Bill
(71), Ned Rush (72), and iZotope Learn (76) carry
over to the top; MusicRadar's remainder (59) and
Attack Magazine (60) follow; the producer-YouTube
remainder (61–70, 74) is ranked behind them; the
conditional clusters (transcript-gated revisits;
fetch-route conditionals) are unchanged.

## Phase 18 — 2026-10-22 (EDUCATIONAL TRANCHE 13)

Queue items 1-5 of the Phase 17 NEXT QUEUE, worked
to depth. Yield: zero new registry bases (82 stays:
81 executable + 1 planning, 66 plan-renderable),
zero new variants (332 / 54 bases), +4 knowledge
(115 → 119; producing 46 → 48, workflows 16 → 17,
mixing 18 → 19), no engine or spec changes, no new
demos (suite 108/108 rendered + verified clean,
unchanged). Every item was dispositioned into the
bank and the sources list incrementally as it
closed.

Item 1 — Mr. Bill (71). The granular / beat-repeat
family's practitioner depth resolves entirely onto
the render-and-process family (GAP-07) and the
slicer family (WEB-08): his seam craft is
manufacture — transition material rendered from
the track's own audio before the seam is placed.
His free tutorial's reverb-artifact amplification
(reverb → duplicated gain/tool stages magnify the
tail's artifacts into glitch timbre, limiter last;
bounce, onset-slice, shorten tails → glitch
percussion) banks as GAP-07's artifact form, at
recreation-transcript weight (Polarity's Bitwig
walkthrough of the tutorials, full transcript
read); the same source gives the all-pass /
splitter phase stack as the crush family's phase
form. Third-party notes on his start-to-finish
series (summary weight — the series is his paid
course surface) give master-bus resampling:
resampler passes on the master channel yield
glitch material related to the arrangement, placed
to lead into the drop; banked in
knowledge/producing as the resample-the-mix
entry, with the stop-the-world quarter-note
offset as a placement corollary. The DJTT
performance walkthrough (article weight) banks
his Simpler slice + Follow Actions + Chain
Selector template as WEB-08 performed. His
template and courses are paid — unmined.

Item 2 — Ned Rush (72). The beat-repeat family's
device-semantics remainder. His Follow Actions
method (Seed to Stage's write-up of his video,
article weight): Session clips edited at clip
level (start/length/warp/pitch), Legato launch,
Follow Action Any/Other chaining fragments at
random within their block, the stream recorded
and selected — banked as WEB-08's generative
form, T-019's probability-chain trigger, and
knowledge/workflows' generate-and-select entry
(probability proposes, the ear disposes). His
packs at product-description weight (the packs
are paid; descriptions state the mechanisms):
MashUp = T-008's per-effect probability panel;
Scrubber = GAP-05's buffer device form (MIDI
scrub playhead, auto-scrub, gating); the
Function Suite = the drawn breakpoint function
as the repeat/granular families' third
modulation source (LFO / sample-and-hold /
drawn function), Function Scrub aiming it at
buffer start position; Psychedelay = WEB-01's
buffer logic stated as a delay device. The
Granulator III tutorial stands at title weight.

Item 3 — iZotope Learn (76). The SPACE family's
knowledge-class remainder, two articles read in
full. Tempo-synced tails join knowledge/mixing:
pre-delay and decay set to beat values (1/64 =
52 ms at 71 BPM; decay = one half note, 1.69 s)
so the wash ends on the grid — the tail budget
authored in beats. Retriggered reverb (bypass
automation restarts the wash per chord) banks
as T-005's accumulation axis; feed conditioning
banks as its feed axis — the ghost-trigger
transient carve (the reverb reacts only to the
tonal part) and the Abbey Road input EQ
(band-limit the feed, completing the triangle
with PML's in-chain high-pass and Pensado's
darkened returns, Phases 17); gate-before-delay
("10 Common Delay Mistakes" #4) is the
send-gating axis's delay-side statement, and
the delay-timing caution corroborates the
timing axis at curriculum weight.

Item 4 — MusicRadar (59), partial remainder
closed at the index weight the queue assigned.
The synth-sweep tutorial (full text read via a
mirror of the MusicRadar piece): noise
oscillator → low-pass with a resonance bump,
cutoff automated — T-018's patch form, with
its space-consistency term (the sweep is sent
to the track's existing aux returns, so the
transition sound lives in the track's own
space). The drum-mix column's rhythmic-predelay
note corroborates item 3's tempo-synced tail
from the magazine side; its sidechain note is
T-035's mix-scale form, already standing. The
archive's bulk is gear/mix craft, recorded as
worked at index weight.

Item 5 — Attack Magazine (60). The Deconstructed
series read at depth ('No UFO's' in full):
the recurring transition sound joins
knowledge/producing — one synth crash at every
section head (and midpoint) as the marker's
standing form, with the energy-carry corollary
(a looped vocal + the crashes carry energy
from chorus into breakdown — the ferryman at
arrangement scale) and the austerity bound (no
fills, no dropouts; energy carried by mixer
mute changeovers alone, halfway pattern swaps
as the mid-section term — Rome's two-loop
cadence's ancestor). The easing-off chorus is
the restraint doctrine's historical instance.
Beat Dissected is drum-programming craft,
nothing banked. Their books are paid — unmined.

Selection smoke: check_select() green including
the P1–P3 guard cases. Probes: a same-key,
same-tempo bass pair ranks eq_blend top (7.0)
with live_loop_mix second — the plain pair
correctly earns no glitch-family preference;
a stems-available house pair co-leads
stem_element_crossfade with eq_blend at 8.0
(GAP-08 behaving as banked through four vendor
surfaces and two practitioner tranches); a
drop → breakdown pair tops out on
resonator_tail (4.0) with beatslicer_shuffle
present but low (1.0) — its prefers want
features this pair does not declare, reported
as measured.

Counts recounted from artifacts: registry 82
(techniques/*.md = 83 with INDEX), variants
332 / 54 bases, knowledge 119 (mixing 19,
performers 14, producing 48, setcraft 21,
workflows 17 — each new entry verified
physically present in its repo file by the
### count convention), verdicts ADOPT 60 /
ADAPT 22 (tallied from engine meta), demos 108
records — all render_ok / silence_ok /
headroom_ok.

The NEXT QUEUE at the end of EDUCATIONAL-SOURCES.md
was refreshed at the end of this phase: the
producer-YouTube remainder sweep (61–70, 74)
now leads; the two conditional clusters
(transcript-gated revisits; fetch-route
conditionals) follow. The written
first-party and practitioner surfaces are nearly
exhausted — what remains is the YouTube long
tail and the gated revisits.

## Phase 19 — 2026-10-22 (EDUCATIONAL TRANCHE 14)

Queue item 1 of the Phase 18 NEXT QUEUE — the
producer-YouTube remainder sweep (entries 61–70,
74) — worked as one sweep, per-channel depth as
the evidence earned it. Yield: zero new registry
bases (82 stays: 81 executable + 1 planning, 66
plan-renderable), zero new variants (332 / 54
bases), +1 knowledge (119 → 120; setcraft 21 →
22), no engine or spec changes, no new demos
(suite 108/108 rendered + verified clean,
unchanged). Every channel was dispositioned
into the bank and the sources list incrementally
as it closed. The sweep behaved as the queue
predicted: corroboration, parameters and
doctrine statements, no new mechanisms — the
registry's mechanism set stands unrefuted by
eleven more channels.

Item 1 — Ableton Learning Music (61). The
interactive fundamentals site read at its text
weight (Get started; Play with song structures):
sections are patterns combined in multiples of
four, eight, or 16 bars, arranging is putting
the sections together, and the site's opening
premise is combination itself. Recorded as
corroboration of the grammar the producing
entries assume — the knowledge-class grounding
the entry promised, delivered at exactly that
weight. Nothing banks.

Item 2 — Big Z (62). PARTIAL. Identity and
current teaching surface confirmed first-party
(Big Z Studios): a mixing/mastering practice
whose course surface is the paid Mixing Academy
— no transition module named at listing weight.
The free channel this entry listed could not be
evidenced at transcript weight in this
environment (searches surfaced the paid surface
and pirate mirrors, never used). No mechanism
banked; the entry joins the
transcript-conditionals cluster.

Item 3 — SeamlessR (63). Resolved at interview
weight: Image-Line's artist interview (his own
account — Harmor as "the biggest game changer")
and CreativeLive's instructor page. His
resynthesis doctrine banks as GAP-07's
instrument form: where render-and-process
renders a passage for the seam, his renders
the source sound itself — the render is the
instrument, and the edit craft downstream is
the slicer family's, already banked. His
CreativeLive courses are paid — unmined.

Item 4 — Slynk (64). Resolved: Ableton's own
blog on his Grain Scanner vocal work (article
weight) is WEB-06's granular family performed
on the vocal, already banked; EDMProd's
interview at show-notes weight states the
groove doctrine — performance quality, not a
seam mechanism — recorded in the bank rather
than banked as knowledge. Nothing new.

Item 5 — EDM Tips (65). The sweep's one
knowledge yield. Will Darling's arrangement
guide read in full first-hand: one micro
progression carries the track, energy comes
from melody, automation and element
arrangement, and a second progression — if
used at all — stays in the same key, reuses
the main chords, and stays short. Banked to
knowledge/setcraft as key stability: no key
move is the unmarked default and the move is
the bounded, priced exception — the
producer-side premise under Club Ready's
compatibility mode and select.py's P3 gate.
His loop-to-song method is the layer family's
compositional form, already standing.

Item 6 — Reid Stefan (66). Resolved at index
weight: first-party MyMixLab listings state a
vocal-production and mix/master canon (vocal
FX as reverb/delay space, width, tails and
rhythmic FX) — the SPACE family's mix
application at generic weight, tails as polish
rather than seam craft. No transition
mechanism named in the readable surface; the
full-length canon is paid-platform — unmined.

Item 7 — Andrew Huang (67). Resolved at
product-description weight (his Baby Audio
interview, first-party, plus published product
descriptions; the plugin is a commercial
product, not mined as a course). Transit
chains 18 effect modules across seven slots
under one macro transition controller whose
span is set in bars/divisions — banked as
T-017's (Layered FX Stack) macro form: the
stack bound to a single controller, its span
the timing parameter; randomize-with-locks is
generate-and-select at device weight. Transit
2's Loop and Reverser modules are in-macro
compounds of the slicer and reverse families,
and its Follower/Sidechain modes bank as the
modulation-source axis's fourth term —
signal-derived, after LFO, sample-and-hold,
and Ned Rush's drawn function.

Item 8 — Rick Beato (68). Resolved as
knowledge-class corroboration, as the entry
promised: the analysis canon (stem breakdowns
naming key changes, modal interchange,
borrowed chords) and his public advocacy of
the key change as an energy event are the
theory-side statement of the lift P2 scores.
His course's modulation module stands at
curriculum weight (paid — unmined); the
mechanisms are standard theory already
assumed. One widely indexed key-change
summary is another educator's video —
attribution rejected, not banked here.

Item 9 — Busy Works Beats (69). Resolved at
index weight: the rap-side FL educator's seam
craft as evidenced is sample placement — his
template bundle's "Chants & SFX — ear candy
and transition effects" folder
(product-description weight) is the marker
family's sample form. A generic FL course
transcript indexed near his name is
unattributed — rejected. His courses are
paid — curriculum weight.

Item 10 — Virtual Riot (70). Resolved at
workshop-report weight (Slam Academy's
masterclass recap; UKF on his Studio Time
series). "A saw-wave pitched down becomes
rhythm" — the intervals landing on 2:3 and
3:4 ratios — banks as the pitch/rhythm-
continuum statement under T-008's fractional
loop-length axis; his randomization doctrine
(locked pitch, save the gems) corroborates
generate-and-select. His Slam Academy course
is paid — unmined; his growl chains are
timbre craft, recorded as worked.

Item 11 — Alice Efe (74). PARTIAL at title
weight: identity stands as verified at the
2026-10-21 list verification, but no tutorial
text of hers could be read in this environment
(search surfaced only generic looper material,
none of it hers). Live-looping seam craft
would resolve onto live_loop_mix's performed
form if evidenced; nothing is asserted without
the text. Held with the fetch-route
conditionals.

Selection smoke: check_select() green including
the P1–P3 guard cases (Cases 6–8). Probes, as
measured: a stems-available house pair co-leads
stem_element_crossfade with eq_blend at 8.0
(GAP-08 behaving as banked); an off-key pair
(8A → 3A) rejects eq_blend and tops out on the
filter family (filter_sweep / infinity_filter
at 6.0) — the off-key behavior the key-stability
entry prices; a vocal-free +4 pair (8B → 12B)
measures effective camelot 3 with eq_blend
admitted — the P3 gate live, unchanged.

Counts recounted from artifacts: registry 82
(techniques/*.md = 83 with INDEX; meta kinds
73 render / 5 overlay / 3 decision / 1
planning), variants 332 / 54 bases, knowledge
120 (mixing 19, performers 14, producing 48,
setcraft 22, workflows 17 — the new entry
verified physically present in
knowledge/setcraft.md by the ### count
convention), verdicts ADOPT 60 / ADAPT 22
(tallied from engine meta), demos 108 records —
all render_ok / silence_ok / headroom_ok.

The NEXT QUEUE at the end of
EDUCATIONAL-SOURCES.md was refreshed at the end
of this phase: MixbusTv (57) — the last unmined
free entry in class 4 — now leads, followed by
the two conditional clusters (transcript-gated
revisits, now including Big Z's free canon;
fetch-route conditionals, now including Alice
Efe). The open free surfaces are otherwise
exhausted; the paid canons remain his per-item
call.
## Phase 20 — 2026-10-22 (EDUCATIONAL TRANCHE 15 — MINING PHASE CLOSES)

Queue item 1 of the Phase 19 NEXT QUEUE —
MixbusTv (57), the last unmined free entry in
class 4 — worked at the depth the evidence
supports, then the program accounting audit
that closes the mining phase. Yield: zero new
registry bases (82 stays: 81 executable + 1
planning, 66 plan-renderable), zero new
variants (332 / 54 bases), zero knowledge
(120 stays), no engine or spec changes, no
new demos (suite 108/108 rendered + verified
clean, unchanged).

Item 1 — MixbusTv (57). Resolved at index
weight. Identity and canon confirmed
first-hand: David Gnozzi, platinum
mix/mastering engineer (MC Solaar's
*Geopoetique*), the MixbusTv channel
(2014– ), Pro Mix Academy tutor — the
Produce Like A Pro profile of him (entry
55's own site), the Recording Studio
Rockstars session notes, and his own site's
blog index (news, presets, course
announcements; no technique articles) read
first-hand. The canon as evidenced is
mixing/mastering craft: mix-bus chains,
vocal mixing, gear reviews at technical
depth. His vocal-FX teaching, at summary
weight (a third-party summary of "How To
Mix Vocals Like A Pro"): sends-based
reverb/delay returns, ducked out of the
vocal's way, decay and pre-delay calculated
from the project BPM, the effected track
EQ'd — the T-004/T-005 SPACE family's send
craft entire, already banked at higher
weight (the ducked return's full named
form, Phase 17; tempo-synced tails, Phase
18). His one named doctrine point — keying
the mixbus compressor from a partial signal
(the bass, or the vocals) rather than the
full mix, so the bus breathes with a chosen
element — recorded in the bank at
practitioner-report weight (Gearspace
discussion of his clip): a dynamics
key-source practice, mix craft rather than
a seam mechanism; recorded, not banked, on
the Phase 19 Slynk precedent. No transition
mechanism surfaces at readable weight — the
queue's expectation (SPACE-family tail craft
at best) is met and exhausted by the
higher-weight entries standing. His courses
(three ProMix Academy titles; his own
store's courses) are paid — unmined, his
per-item call. Bank: TECHNIQUES Phase 20
section.

Item 2 — the program accounting audit (the
mining phase's closing state; the full table
stands as the PROGRAM-STATUS section at the
head of EDUCATIONAL-SOURCES.md). Every one
of the 85 sources on the list is accounted
by final state, **recounted from the list's
own Status fields**, not carried from any
tranche summary:

- **Mined — 53:** entries 1–14, 16 · 22,
  24–27, 29–34 · 35, 36, 44 · 48, 52,
  54–56, 57, 58–61, 63–73, 76, 77 · 85.
  (Five carry recorded coverage caveats
  inside their entries — 5, 6, 11, 13, 52 —
  which stand as written.)
- **Mined-partial — 13:** 21, 23, 28
  (catalog remainders deduped, bodies not
  re-read) · 37, 38 (community layer worked;
  the subreddits proper unfetchable here) ·
  47 (HELIX threads only) · 50, 51 (identity
  confirmed; no episode evidenced at
  transcript weight) · 53 (method banked;
  tutorials member-gated / untranscribed) ·
  62 (paid surface confirmed; free canon
  unevidenced) · 74 (no readable text
  route) · 75 (teaching inside paid
  courses) · 82 (Making Music — free web
  edition's 24 of 74 chapters; full book
  paid).
- **Conditional-parked, unworked — 1:**
  83 (Mixing Secrets / Cambridge Music
  Technology), bot-walled companion site;
  its gate is a fetch route opening.
- **Paid-canon unmined — 8:** 17 (Toolroom
  Academy), 20 (Scratch DJ Academy), 49
  (Sonic Academy), and five of the seven
  class-5 books (78, 79, 80, 81, 84). His
  per-item call; nothing purchased, ever.
- **Free, unmined, never queued — 10:** the
  residual queue below.

**Sum check: 53 + 13 + 1 + 8 + 10 = 85** —
the list total. ✓

Two audit findings, recorded rather than
smoothed. (1) **File integrity:** the entry
bodies for 78–85 do not exist in
EDUCATIONAL-SOURCES.md. The header count
(84 at assembly; 85 with Production Expert
added in Phase 6), this log's phase records,
and the file's own queue history attest all
eight — Making Music (82), Mixing Secrets /
Cambridge (83), Production Expert (85, its
shimmer article mined as WEB-10 evidence in
Phase 6) — but the five remaining books'
titles survive in no program file. They are
accounted under their standing class-5
disposition (paid / summary-weight only) in
the paid-canon bucket; nothing about them
is reconstructed beyond what the records
state. (2) **Hygiene:** entry 31's status
token still read "partial" although its
remainder completed in Phase 15 — corrected
at this audit, noted in the entry. The old
tail queue's parenthetical cross-references
likewise matched no current entries; the
refreshed queue below uses numbers verified
against the file.

**Conditional overlay** (remainders parked;
the entries are counted above — the gate is
on their remainders, and per standing
instruction no attempts were burned on them
this tranche): transcript-host 429 or a
readable transcript route — 5, 6, 50, 51,
53, 62, 75; fetch route — 37, 38, 74; bot
wall — 83.

**Residual queue** (the NEXT QUEUE at the
end of EDUCATIONAL-SOURCES.md, refreshed):
the only sources actionable without new
external conditions are the ten never-queued
free entries — DJWORX YouTube (15), DJcity
(18), BPM Supreme (19), r/Serato (39),
r/Traktor (40), Serato Forum (41), DJWORX
site (42), Magnetic Magazine (43), Native
Instruments Blog (45), Wikipedia — DJ mix
(46). All are community / gear-explainer
surfaces of classes the program repeatedly
found corroborative rather than
mechanism-bearing, and none was ever ranked
into a tranche's items; the two subreddits
(39, 40) are untried routes whose hosts
refused the sibling fetches (37, 38), so
theirs may refuse identically. Everything
else on the list waits on a gate lifting
(the conditional clusters) or his per-item
call (the paid canons, the Making Music
full book, the DDT school). With this
accounting, the mining phase is closed:
the registry's mechanism set stands
complete against the free evidence.

Selection smoke: check_select() green,
including the P1–P3 guard cases (Cases
6–8), re-run at the audit. Probes, as
measured (unchanged behavior, re-verified):
a stems-available house pair co-leads
stem_element_crossfade with eq_blend at
8.0; an off-key pair (8A → 3A) rejects
eq_blend and tops out on the filter family
at 6.0; a vocal-free +4 pair (8B → 12B)
measures effective camelot 3 with eq_blend
admitted — the P3 gate live.

Counts recounted from artifacts: registry
82 (techniques/*.md = 83 with INDEX; meta
kinds 73 render / 5 overlay / 3 decision /
1 planning; 81 executable; 66
plan-renderable by the render module's
function registry), variants 332 / 54
bases, knowledge 120 (mixing 19, performers
14, producing 48, setcraft 22, workflows
17 — the ### count across knowledge/*.md),
verdicts ADOPT 60 / ADAPT 22 (tallied from
engine meta), demos 108 records — all
render_ok / silence_ok / headroom_ok. Repo
phases 1–20; this commit is the repo's
19th.

## Phase 21 — 2026-10-22 (EDUCATIONAL TRANCHE 16 — THE RESIDUAL SWEEP; FREE LIST EXHAUSTED)

The residual queue named by the Phase 20
audit — the ten free sources listed but
never queued (entries 15, 18, 19, 39, 40,
41, 42, 43, 45, 46) — worked in order at
the depth the evidence supports. Yield:
zero new registry bases (82 stays: 81
executable + 1 planning, 66
plan-renderable), zero new variants
(332 / 54 bases), zero knowledge (120
stays), no engine or spec changes, no new
demos (suite 108/108 rendered + verified
clean, unchanged).

At index weight (channel / site surfaces
read first-hand; technique content is
corroboration of what stands banked at
higher weight): DJWORX YouTube (15) — the
channel is gear first-looks/reviews,
event/set footage and heritage pieces; no
tutorial canon stands on it, and Mojaxx's
review-demonstrated FX behaviour is the
gear's own documented behaviour from the
class-2 passes. DJcity (18) — djcity.com
is a record-pool storefront with no
education-blog surface standing; DJcity TV
is routine/performance video plus the same
gear reviews. Attribution guard recorded:
the "DJ City" education blog at
djcity.com.au is an Australian retailer
namesake, not this entry, and was not
mined under it. BPM Supreme (19) — the
pool's education surface is BPM Academy,
bundled into subscription plans inside the
subscriber app (title-weight only; no
account created); its one free public
technique surface, the 2021 Mix
Breakdowns, was a Crossfader co-production
whose techniques (tone play, wordplay,
sample switch up) are entry 2's Phase 10
banked set entire. DJWORX site (42) — the
tutorial hub's technique doctrine is
structural cue placement, phrase-boundary
mixing and energy matching, all banked at
higher weight. Magnetic Magazine (43) —
its DJCity conversation, read in full,
states the preparation-as-improvisation
doctrine; recorded as corroboration of the
prep/setcraft entries, not duplicated
(the Phase 17 precedent).

Mined, corroboration only (read
first-hand; no mechanism the registry
lacks): Serato Forum (41) — the forum
proper is readable here, and its
Scratch Live-era technique threads state
the registry's core set in practitioner
words (the bass cross as advice, the
vocal-over-instrumental exit, spinback
exits, the acapella ride-through,
manufactured tempo-transition tracks as
T-021's material form). This closes the
loop opened in Phase 11, where the
community layer was worked from indexed
threads. Native Instruments Blog (45) —
the vendor's tutorial surface restates
entry 27's manual content as recipes (the
Pattern Player drum layer inside a
stem-staged live remix = WEB-12 × GAP-08;
loops holding an incoming track;
deliberate key changes for energy).
Wikipedia — DJ mix (46) — the article's
Technique taxonomy maps entire onto the
registry, including its one distinctive
line (Goa DJs mixing in the break over
synth washes = T-023's encyclopedic
statement); the neutral outside check the
entry promised, passed.

Attempted and refused: r/Serato (39) and
r/Traktor (40). One honest fetch attempt
was made on r/Serato via the program's
normal route: reddit.com is blocked at the
fetch layer in this environment — the
same domain-level refusal entries 37/38
met in Phase 11. r/Traktor's refusal is
recorded against the identical gate rather
than burned as a second identical request.
No bypass route, no account, no posting.
Both entries move to the fetch-route
conditional cluster, content never read,
nothing asserted.

Close-out accounting, recounted from
EDUCATIONAL-SOURCES.md's own Status fields
(the PROGRAM-STATUS section at its head is
updated to match): **mined 61 ·
mined-partial 13 · conditional-parked
unworked 3 (39, 40, 83) · paid-canon
unmined 8 · free-unmined 0 — sum 61 + 13
+ 3 + 8 + 0 = 85 ✓**, the list total. The
free list is genuinely exhausted: every
free source has been read, or its reading
honestly attempted and its gate recorded.
The sweep surfaced nothing new and freely
reachable beyond the ten, so the residual
queue's final form (end of
EDUCATIONAL-SOURCES.md) is empty of
freely-actionable items — what remains is
the conditional clusters with their gates
(transcript host: 5, 6, 50, 51, 53, 62,
75; fetch route: 37, 38, 39, 40, 74; bot
wall: 83) and the paid canons on his
per-item call.

Selection smoke: check_select() green,
including the P1–P3 guard cases (Cases
6–8), re-run at the close-out. Probes, as
measured (unchanged behavior, re-verified):
a stems-available house pair co-leads
stem_element_crossfade with eq_blend at
8.0; an off-key pair (8A → 3A) rejects
eq_blend and tops out on the filter family
at 6.0; a vocal-free +4 pair (8B → 12B)
measures effective camelot 3 with eq_blend
admitted — the P3 gate live.

Counts recounted from artifacts: registry
82 (techniques/*.md = 83 with INDEX; meta
kinds 73 render / 5 overlay / 3 decision /
1 planning; 81 executable; 66
plan-renderable by the render module's
function registry), variants 332 / 54
bases, knowledge 120 (mixing 19, performers
14, producing 48, setcraft 22, workflows
17 — the ### count across knowledge/*.md),
verdicts ADOPT 60 / ADAPT 22 (tallied from
engine meta), demos 108 records — all
render_ok / silence_ok / headroom_ok. Repo
phases 1–21; this commit is the repo's
20th.

## Phase 22 — 2026-10-22 (expansion tranche 1: performer corpus, tranche A)

The study program REOPENS under the user's
expansion mandate ("82 transitions is like
still a very small fraction. Go get more.").
The V1 closure's framing error is owned in
the bank: the 85-source list was a seed,
not the map. The map is now
EDUCATIONAL-SOURCES-V2.md (192 entries, 7
classes, cartography 2026-10-22), and this
phase works its ranked queue item 1 —
performer corpus tranche A, the R2 attack
order: Zabiela → Hype → EZ, then the HÖR
Berlin / Boiler Room corpus route via
1001tracklists. S0–S11 were run per item
at the level the reachable evidence
carries; where full S2 audio alignment was
infeasible from here, entries bank at
their evidenced confidence with the
limitation recorded in place. Yield: 2 new
bases, 4 named axes, 4 knowledge entries,
3 performer entries extended.

Zabiela (the attack order's #1) was mined
from his own teaching: the "How To DJ"
Episode 3 series (DJdownload / Ministry of
Sound, 2009), all eight parts read at
episode-description weight first-hand, plus
Balance 029's full Act 1/Act 2 tracklists.
One new base: transform_gate_loop
(PERF-ZAB, ADAPT, confidence high — the
source is L4-grade, the performer teaching
his own move) — the EFX-1000 transform
effect gating a held loop (his: a loop of
his own scratching), beat-select patterns
switched live; engine form doubles the
gate subdivision per bar over a gate_bars
window and cuts into B. Deduped in place
against GAP-15 (manual fader between two
sources), T-019 (retrigger, not gating),
and the tremolo gate (LFO on an overlay).
Three axes banked from the same pass:
loop_length_modulation on
feedback_loop_build (BPM-halving to change
a feedback loop's length; spinback fills
inside the hold), capture_source: live mic
on live_loop_mix DM-A14 (headphones into
the mic input — his "thank you" vocal
mashup, Part 4), and a beat-roll-as-sampler
use-note on T-008/WEB-03. Balance 029 banks
as setcraft (composite-track staging: one
perceived track, elements of three or four
sources; the tape-exhaustion halt as a
set-level ending), with the produced-mix
caveat stated — composites evidence the
doctrine, not live density.

James Hype was re-mined and yields ZERO
new bases — the Phase 12 verdict stands,
now corroborated at three independent
weights (Pioneer "How I DJ" episode
summary; DJ Carlo's flagship transcript at
verbatim weight for the buildup-loop
section; Digital DJ Tips' timestamped
Flying Solo instance). The yield is real
but axis-class: out_point_creep on GAP-02
(the sub-beat tightening stage after the
halving ladder — re-press Out, jog the
loop end inside the beat), echo_assignment:
per-deck on the echo family, the GAP-10
performed instance, and his EQ doctrine
(boost EQ over gain; strip acapella lows)
in the performers entry. His paid Mixing
Skills course remains the unmined
ground-truth surface — the user's per-item
call, unchanged by this phase.

DJ EZ yields the tranche's second base:
dual_loop_composite (PERF-EZ, ADAPT,
confidence medium / L1) — the Boiler Room
x RBMA set's minute-~14 construction,
documented by timestamped watcher anatomy
(Line Noise): a tiny loop of Wookie's
"Battle" as the bass drum, Cleptomaniacs'
"All I Do" dub as percussive stutter, both
role-stripped into a third groove. This
closes the extraction target performers.md
named in 2026-10-17. Deduped against T-031,
T-020, GAP-16, WEB-12 in the spec. Set-level
yield: the two-mode density doctrine
(31 cuts/45 min Boiler Room vs FABRICLIVE
71's 32 tracks/75.5 min with long-hold
blends — knowledge/setcraft) and the
Recess archive's two-copy offset jerk +
sampler-carry handoff (knowledge/mixing).

The HÖR Berlin / Boiler Room corpus route
was verified, not exhausted: 1001tracklists
fetches cleanly with w/ layering notation
intact (proof item: Nitepunk @ HÖR Berlin
2026-10-15 — 22 positions, 2 w/ layer
events, 6 ID–ID). No S2 alignment was run
on any set this phase; EZ's 2012 set has
no reachable full timestamped tracklist, so
no timing statistics are claimed for it.
The corpus is staged behind queue item 2
(genre traditions tranche A), which gives
the extraction its genre-native labels;
the V2 queue now leaves item 2 at the top.

Selection smoke: check_select() green,
including the P1–P3 guard cases, re-run
this phase. Probes, as measured: on a
melodic-house build→drop pair (124→126,
energy 6→8) transform_gate_loop ranks at
3.0 with its prefers reason firing; on a
UKG outro→drop pair (132→134, inside its
3% tempo gate) dual_loop_composite ranks
at 3.0 with its reason firing, and it
stays out of the build-phrase pair its
requires exclude.

Counts recounted from artifacts: registry
84 (techniques/*.md = 85 with INDEX; meta
kinds 75 render / 5 overlay / 3 decision /
1 planning; 83 executable; 68
plan-renderable by the render module's
function registry), variants 356 / 56
bases (VARIANTS.md regenerated), knowledge
124 (mixing 21, performers 14, producing
48, setcraft 24, workflows 17 — the ###
count across knowledge/*.md), verdicts
ADOPT 60 / ADAPT 24 (tallied from engine
meta), demos 110 records — all render_ok /
silence_ok / headroom_ok (110/110 verified
clean; the transform gate's gate window is
a declared allowed-silence span). Repo
phases 1–22.

WHITE SPACE — what this tranche revealed
that is NOT on the V2 list:
(1) The DJdownload "How To DJ" series
itself: Zabiela's Episode 3 is one episode
of a multi-performer taught series — the
other episodes' performers are unlisted
anywhere on the map, and taught-series
episodes are L4-grade ore wherever they
survive (Listen Notes carries the catalog
with descriptions).
(2) The Recess.co.uk technique archive —
a practitioner-written UK text corpus
(mix walkthroughs with exact choreography,
reader-contributed named tricks) that
appears on neither the V1 nor V2 lists; it
surfaced via EZ and immediately yielded
two banked moves. A classic-text stratum
(Recess, the old DJ Forums / about.com
era pages) is missing from the map's
classes entirely.
(3) The watcher-anatomy genre: long-form
critical writing that timestamps and
anatomizes single gestures (Line Noise on
EZ; the BCR001 mixography format) — a
source class between review and tutorial
that the map's Class 4 does not name, and
the only free surface that produced a
timestamped gesture claim this tranche.
(4) Produced-mix archaeology: Balance 029
was built in a DDJ-RZ + Ableton
back-and-forth over a year — the
commercial mix-CD back-catalogs (Balance,
Renaissance, Global Underground) are a
documented-composite corpus with full
tracklists, unlisted as a class; their
evidence weight (studio composites) needs
its own ladder rung between L1 and L2.
(5) EZ's minute-14 composite suggests a
mechanism family the map has no name for:
role-assigned loop construction (fragments
reduced to drum roles and recombined) —
the breaks/juggling traditions likely hold
more instances (the map's Class 2C names
jungle choppage of *source material*, not
loop-role construction from *two* records).

## Phase 23 — 2026-10-22 (expansion tranche 2: genre traditions, tranche A — DnB + dubstep + UKG texts)

Queue item 2 of the V2 map: Class 2A/2B/2E
texts mined for named vocabularies and
bounds, so the staged S2-alignment corpus
(HÖR/Boiler Room, Phase 22) has
genre-native labels when it re-enters.
All eleven text entries were fetched
first-hand in full in this environment;
the two video items stand as listed (the
EZ masterclass — performed corpus mined
in Phase 22; the STRANJAH Transmission
page — a video landing page, worked at
its six-technique outline weight).

Three new bases, all from the DnB texts.
continuous_drop (WEB-19) is the lead
pattern of kohadachan's note.com
taxonomy — a working DJ's own named
patterns: A's drop plays out with B's
first bar staged beneath its final 8
bars (lows killed, −14 -> −6 dB), and
B's drop lands on the exact downbeat
A's ends. drop_chop (WEB-20) renders
DJGear2K's step-4 chop and DJ.Studio's
"Cutting and Switching": two drops land
together, then full-level ownership
alternates on a bar grid (1/2/4 bars x
rounds) before committing to B — the
single-sub rule performed, deduped
against GAP-15's 16th-note entry gate
and T-024's held collision. drop_insert
(WEB-21) is the taxonomy's variety move
verbatim ("insert a bar of another
track... then return to the original
track"): B's drop substitutes for
insert_bars at A's drop downbeat while
A keeps running muted, then A's drop
resumes mid-course — a human-triggered
weapon whose selector prefer prices the
well-known-A precondition (iconic_a).

Four axes banked on existing bases: the
converge exit (the mountain pattern's
second outcome) and triple-drop staging
(deck_count = 3; the taxonomy's Andy C
case study) on double_drop; Pioneer's
official dual-build staging (DDJ-400
tutorials: both build-ups played
simultaneously, swap before the drop)
on hotcue_drop_swap; periodic bass
alternation (~8-bar ownership trades
inside a long blend, DJTT forum) on
bass_swap. Eight knowledge entries:
mixing x4 (the pattern taxonomy itself,
incl. the cut-in cueing rule and the
1/4-bar pre-drop dip; the long-layer EQ
doctrine — total bass constant, staged
faders, the break+intro two-lows
exception; LowCut Echo as the echo
family's band axis; the DnB key moves
+2 / +6 "back code" / −3, priced by
coexistence duration), setcraft x2 (DnB
dwell arithmetic — 44/66/88-second
quanta and the five-part hour; the NUKG
short-blend doctrine from RA's Conducta
review — blends "normally just a few
bars long," peak picture over
narrative), producing x2 (Stranjah's
break-choppage as role material —
jungle + deep-140, the single-source
studio form of dual_loop_composite's
two-record gesture; EDM Templates'
arrangement bounds — 8-bar change rule,
second-drop switch-up, pre-drop
silence, the standard bass-music
structure).

Resolved without builds: DJ.Studio's
other seven methods are the registry's
core set under DnB bounds — the genre's
*vocabulary* was the gap, not its
mechanisms; Benztown's worked double
drop corroborates T-024 (its phrase
arithmetic joins the taxonomy entry);
4D4M's dubstep↔hardstyle guide is
generic cross-tempo advice already
inside T-021/T-026 bounds. Two map
corrections stand in V2 in place: the
4D4M riddim guide and the ADSR
deep-dubstep page are production texts
whose [S]-grade summaries overstated
their DJ content — fetched in full,
banked at production weight, never
quietly upgraded. The UKG cell closes
honestly: no UKG transition text
educator exists; the EZ masterclass
video stands for the performed corpus.

Selection smoke: check_select() green,
including the P1–P3 guard cases, re-run
this phase. Probes, as measured: on a
DnB drop pair (174 BPM, same key,
drop_pair flagged) continuous_drop
ranks at 7.0 with all three prefers
reasons firing and drop_chop at 6.0
with both of its reasons; on a build
pair with an iconic A, drop_insert
ranks at 4.0 with its weapon + iconic
reasons firing; without the drop_pair
flag all three reject with the named
missing-context reason. Behavioral
render checks: the insert window is
sample-equal to B and everything
outside it to A; chop windows are
sample-equal to their owner, the
landing bar to A+B, the commit tail
to B; variant renders smoke-clean
(continuous_drop__4bar/16bar,
drop_chop__1bar/1bar_x4/4bar_x1,
drop_insert__1bar/4bar).

Counts recounted from artifacts:
registry 87 (techniques/*.md = 88 with
INDEX; meta kinds 78 render / 5 overlay
/ 3 decision / 1 planning; 86
executable; 71 plan-renderable by the
render module's function registry),
variants 374 / 59 bases (VARIANTS.md
regenerated), knowledge 132 (mixing 25,
performers 14, producing 50, setcraft
26, workflows 17 — the ### count across
knowledge/*.md), verdicts ADOPT 60 /
ADAPT 27 (tallied from engine meta),
demos 113 records — all render_ok /
silence_ok / headroom_ok (113/113
verified clean). Repo phases 1–23.

WHITE SPACE — what this tranche
revealed that is NOT on the V2 list:
(1) The [S]-grade summary risk is
quantified now: 2 of 11 fetched texts
materially misdescribed their content
(both production texts in DJ dress, both
in the same genre cell). Class 2's
remaining cells (2C–2M) are [S]-grade
throughout — tranche B should budget a
fetch-correction rate of roughly 1 in 5
and treat every yield figure as
unverified until fetched, exactly as
the class header warns.
(2) The non-English practitioner-text
stratum is bigger than one note.com
article: kohadachan's taxonomy links a
Japanese DnB scene with its own labels,
festivals, and DJ-course culture, and
his pattern names (valley, mountain)
exist in no English source the map
holds. A deliberate non-English sweep
(Japanese, German, Spanish, Korean DJ
text) is a source class the map's seven
classes do not name.
(3) The DAW-construction literature for
performed moves (Benztown's Pro Tools
double drop; the DAW-built mixshow
craft in Class 2L) is a bridge genre:
moves documented as *edits* with exact
parameters, at higher precision than
any tutorial — a mining surface between
Class 2 and Class 6 that neither names.
(4) Riddim's performed vocabulary
(chopping doubles, fake-out switches at
set scale) exists — Phase 23 verified
its textual surface is nearly empty
(the 4D4M correction), which moves the
vein's real home: it is a Class 1
performed-corpus item (Skrillex/Excision
sets) and should be re-queued there
rather than chased in text again.
(5) Track titles as technique evidence:
a UKG tracklist carrying a tune named
"Wheel Up" is doctrine data — repertoire
named after gestures (wheel-up, gun
fingers) is an unlisted signal source
for which gestures a tradition considers
load-bearing.

## Phase 24 — 2026-10-22 (expansion
tranche 3: the combinatorial enumeration
pass — V2 queue item 3, Class 3)

Enumeration, not mining: the full axis
walk + cross-base compounds/sequences
over the registry as it stood, deduped
at the admission bar. The complete audit
trail — every cell counted in exactly one
bucket — lives in ENUMERATION.md (new,
repo root); this entry is its summary.

**Part A — the axis walk.** 1,181 cells
(313 singles + 868 pairs) across the 59
bases declaring preset axes; meta
defaults verified == fn defaults first
(0 mismatches). Buckets: 374 already
registered · 351 admitted (85 singles on
axes 2–7 + 266 pairs on every axis pair)
· 456 rejected — 214 unnameable, 234
default-legged (render as their single
or the base), 32 id-collisions with the
registry, 182 id-ambiguous in the space,
1 aliased preset, 7 conditionally inert
legs found at validation. Nameability
is the binding constraint: preset
vocabularies repeat across axes and the
id scheme does not encode the axis.
Effectiveness was measured, not assumed
— 61 axes render-tested, 60 effective;
the 61st (brake_stop's curve) is
effective but its s_curve value falls
through dsp.pitch_dive to linear (no
S-curve exists in the engine), so the
alias is rejected and encoded in the
generator's measured tables. The
generator (engine/variants.py) now
implements the bar exactly: legacy
surface generated as before and never
delisted (verified id-for-id against
HEAD), expansion admitted only when
nameable + non-default-legged +
non-aliased + non-inert, computed over
the full candidate space.

**Validation.** All admitted variants
rendered on sketch segments and checked
vs base default, vs constituent singles,
vs same-base siblings (375 renders).
32 identity flags, two root causes:
fader_synth's scale axis is conditionally
inert (glide/hold rides never read it;
the arp ride reads only degrees 0/2/4,
where minor and harmonic-minor agree) —
7 pairs rejected, condition encoded as
_CONDITIONAL_INERT; and the new base's
axes named their own defaults — fixed at
the source. Post-fix revalidation of the
affected bases: 67 variants, 0 problems.

**Part B — compounds + sequences.** Of
3,003 unordered render pairs: 40 already
bases · 371 same-family collisions · 83
clash collisions · 158 dual-architecture
· 158 empty requires conjunctions · and
of 2,185 structural survivors, 1,912 are
additive stacks the overlay/layered
machinery already expresses, 196 are
stem-scoped axis applications (GAP-08),
69 the FX-return pattern (banked as one
knowledge entry), 8 gesture-triggered
echo (already dispositioned at knowledge
weight, not re-litigated). ONE new base
clears the bar: **aging_echo** (CMP-01,
ADAPT, high) — the dub tradition's
feedback delay with a lowpass INSIDE the
loop; repeat k is filtered k times, so
the tail decays in brightness as well
as level (demo centroids descend
649→471 Hz across repeats where
echo_out's stay flat at 4145 Hz). Its
atom pair existed only as parallel atoms
(layered_fx_stack / layered_emergence);
the serial in-loop topology is the new
mechanism, under the spiral_echo
precedent. New domain module
engine/compounds.py + demos/ext_compounds
.py; spec + INDEX; selection ranks it
first (5.0) on its home pair and
hard-rejects past its tempo gate.
Sequences: 6,006 ordered pairs under
same-seam scoping, 5,227 compatible —
six chains pass the naming bar and bank
as knowledge with compositions stated
(spinback→drop-swap, brake→drop,
echo→rewind, tease→bass-swap,
fake-out→double-drop, tighten→swap).

**Correction to the map, in the open.**
Class 3 estimated 40–80 compound bases;
the bar returned 1. 23 phases had
already mined the fusion grammar's
named instances (28 composed_of
relations); the residual pair space is
addition, not interaction. The variant
estimate (250–450) landed: 351 admitted
(736 total, ≈2.0×).

Counts recounted from artifacts:
registry 88 (techniques/*.md = 89 with
INDEX; meta kinds 79 render / 5 overlay
/ 3 decision / 1 planning; 87
executable; 72 plan-renderable by the
render module's function registry),
variants 736 / 60 bases (VARIANTS.md
regenerated), knowledge 138 (mixing 31,
performers 14, producing 50, setcraft 26,
workflows 17 — the ### count across
knowledge/*.md), verdicts ADOPT 60 /
ADAPT 28 (tallied from engine meta),
demos 114 records — all render_ok /
silence_ok / headroom_ok (114/114
verified clean). Repo phases 1–24.

WHITE SPACE — what the enumeration
revealed that neither map names:
(1) the namespace is smaller than the
mechanism space — 214 real stagings are
unnameable under the standing id scheme;
an axis-qualified scheme is a framework
decision owed, not improvised. (2) Axes
can be conditionally inert (fader_synth)
— the meta schema cannot declare
applicability conditions; conditional
structure is discoverable only by
rendering. (3) dsp.pitch_dive lacks the
S-curve its preset promises — the legacy
brake_stop *_s_curve pairs render as
their *_linear siblings; implementing
the curve changes shipped renders, a
deliberate future fix. (4) The compound
frontier is atom-bound: it moves when
new atoms arrive (Classes 1/2/5 — the
macro/chain systems especially), not
when old atoms are re-paired. (5)
Chains have no selection layer —
select.py scores single techniques; a
chain scorer is unbuilt, unnamed work.
(6) Genre is not an axis: Class 3's
step 5 (genre re-stagings) cannot be
walked combinatorially while genre lives
in requires windows. (7) Distinctness is
length-relative (drop_chop rounds: x2≡x4
at 8 bars, distinct at 16) — performance-
length spot checks on high-axis bases are
owed before a variant drives a set
decision. Queue as left: item 4
(software/hardware tranche A) tops the
ranked queue after the staged HÖR /
Boiler Room S2 corpus tranche, which
re-enters next per its own note.

## Phase 25 — 2026-10-22 (expansion tranche 4: the staged S2 mix-to-track alignment tranche)

The staged HÖR Berlin / Boiler Room S2
alignment tranche (queue item 3's note;
the landscape's S0–S11 pipeline run for
the first time). Authoritative record:
ALIGNMENT.md in this repo (sets, method
as run, per-track table, findings).
Scratch artifacts (audio, features, DTW
paths, alignment.json) retained at
~/workspace/scratch/s2-alignment/ —
nothing audio is committed.

Sets attempted 3 / aligned 1. Nitepunk @
HÖR Berlin and Andy C @ Rampage Open Air
failed at S1 acquisition: YouTube media
download is walled from both egress
points (all yt-dlp clients probed:
SABR-only / bot sign-in), neither set has
an alternate public audio source, and no
bypass was attempted. Substitute
primary, John Digweed — Transitions
1150 (Guerilla Records Special), aligned
from the artist's official SoundCloud
upload: 21 positions, 12 source tracks
acquired, 9 DTW-aligned (5 solid /
3 flagged proxies / 1 identity-excluded),
2 adjacent-pair transition records,
1 fully measured blend.

Banked: 3 knowledge entries (setcraft:
Digweed alignment calibration + the
crossfader-class opener / same-song
blind spot; workflows: acquisition
routes). New bases 0, axes/variants 0 —
the measured gesture (01→02: 9.2 s
overlap, band crossovers spread 1.8 s,
crossfader-class, residual mid 0.011 /
high 0.009) belongs to an existing
family, and one instance re-stages
nothing. Calibration agreements vs Kim
et al.: tempo adjustments 5/5 <5 %
(+1.65 / −0.50 / −0.02 / −1.85 / +3.66 %,
constant per-half slopes); vs Kim/Yang/
Nam: the opener lands in the 28 %
crossfader minority of the 28/72 split.
Calibration disagreement of a different
kind: the artist's published timestamps
deviate from measured starts by up to
38.6 s (RMS ≈26 s) — listing-grade, not
alignment-grade, data.

Counts: registry 88 → 88; variants
736/60 bases (unchanged); knowledge
138 → 141; demos 114/114 (unchanged);
verdicts ADOPT 60 / ADAPT 28 (unchanged).
No engine/technique/selection surface
touched, so check_select() and the demo
battery were not re-run — stated, not
skipped silently. Method deviations
recorded in ALIGNMENT.md: STFT chroma
for CQT (2 h CQT OOM-killed), chunked
feature extraction, cosine-metric NaN
sanitisation.

WHITE SPACE. (1) The corpus the map
ranks highest for alignment (HÖR /
Boiler Room, YouTube-only) is precisely
the corpus acquisition cannot reach;
this tranche's evidence is one
long-blend radio set, and S6/S7 gesture
extraction on high-rate performed
material is still unproven. (2) The
binding constraint was source-track
supply — DRM-flagged official uploads
(Spooky, Chameleon Project) and absent
full-length uploads left 9 of 21
positions unalignable; purchase routes
exist for parts of this catalogue but
are his per-item call, untouched here.
(3) Track 06's fetched file is an
unresolved identity failure (DTW
optimum inside position 08's window);
whether the upload is mislabelled or
the matcher was fooled by same-family
loops is undecided on current evidence.
(4) The Gargantuan-album extraction for
position 04 was fetched, not run — it
buys an isolated track, no transition.
(5) Queue as left: item 4
(software/hardware tranche A — Mixxx,
djay Neural Mix, SP-404MKII DJ mode,
MODEL 1 + Xone) tops the ranked queue,
unqualified; item 7's academic pass
carries Phase 25's early partial
delivery in its note.

## Phase 26 — 2026-10-23 (expansion tranche 5: software/hardware tranche A — Mixxx, djay, VirtualDJ, SP-404MKII, Xone:96, DJM-V10)

The V2 queue's item 4, worked as six
parallel source-mining passes, one per
doc body, each fetched first-hand in
full: Mixxx 2.5 Manual Ch. 11 (Effects);
Algoriddim djay Pro help (16 Neural Mix /
mixer / automix pages — no standalone
Mac Neural Mix EQ page exists; the EQ
facts assemble from three pages that
disagree in presentation); VirtualDJ
Manual Stems 2.0 cluster (six pages);
Roland SP-404MKII Reference v5.5 (80
pages: the complete BUS FX cluster, all
46 individual MFX pages, the complete
DJ Mode cluster — the official
reference carries DJ Mode in full, so
the map's manualsdir mirror was not
needed); Allen & Heath Xone:96 User
Guide (the official support HTML is the
complete guide, 874 lines, read
end-to-end); Pioneer DJM-V10 manual via
the manua.ls mirror (pp26–66 + specs —
the official Pioneer PDF is login-walled;
recorded as a named gap, not bypassed;
every V10 fact is labelled
mirror-sourced). Mining briefs and raw
fetches retained at
~/workspace/scratch/sw-tranche/.

Eight new bases, all in the new domain
module engine/hw_techniques.py (wired
into meta/render/variants + demos via
ext_hw.py, FRAMEWORK.md §7), each with
spec doc, demo, variants and selection
metadata: WEB-22 `pre_filtered_echo`
(Mixxx: the echo send band-shaped
*outside* the loop, dry pinned at full —
the send-side complement of CMP-01's
in-loop topology; the manual's own
worked example); WEB-23
`notch_carve_sweep` (Xone:96: HPF+LPF
summed from the simultaneous
state-variable outputs = one travelling
rejection band); WEB-24 `phaser_sweep`
(SP-404 Phaser + the 96's all-pass sum:
an allpass cascade, magnitude-flat —
distinct DSP from WEB-02's delay comb);
WEB-25 `stem_swap_replace` (VirtualDJ
StemSwap: a captured stem loop mutes
and replaces the host's corresponding
stem, trigger-gated — not GAP-08's
linear handover); WEB-26
`djfx_microloop` (DJFX Looper: a
12–230 ms free-time grain performed at
varispeed through zero — forward, stop,
backward); WEB-27 `cyclic_speed_dip`
(Downer: a tempo-period rate LFO with
HF tracking and a pitch-corrected
form); WEB-28 `pattern_gate_slicer`
(Slicer: a preset 16-step gain table
with swing and SLASH/LEGATO modes; the
V10 TRANS duty form banked as its
staging); WEB-29 `sideband_comb_filter`
(SBF: a geometric comb of narrow
passbands, dissolving A into its
spectral skeleton).

24 named axes written into 16 parent
specs (the Phase 23 headed-section
pattern): five on GAP-08 (ModernEQ's
coupled morph law, the kick/hihat
sub-split, EZRemix's right-isolate law,
djay's parallel stem crossfader bank,
djay's automix handover); damping
tables + the Mute FX stem-mute tail on
T-004; dual-VCF counter-sweep, CRUNCH
and WILD on T-003 (plus V10 global/LFO
forms and Roland's filter stagings);
both flagships' four-band laws + the
V10 master isolator on T-001;
Tempo Blend's dual-converge on T-021;
the Mute Bus tails-only break on
T-034; HELIX overlay + plain roll on
WEB-07; Scatter + stem-scoped Beat
Grid on WEB-08; Tape Echo heads on
CMP-01; Cloud Delay on WEB-01; the
Resonator chord-bank + Hyper-Reso on
WEB-18; Lo-fi + Cassette Sat on WEB-04;
VINYL BRAKE as a staging (duplicate
ruling) on T-006; Back Spin ground
truth on T-007; stored markers on
T-028; Chromatic PS + DJ Bend on
T-032. 10 knowledge entries (mixing
+7: the Dry+Wet law, stem-scoped FX
doctrine, stem taxonomy + bleed, the
tails-only break, FX returns as full
channels + the V10 SEND bounds + the
COMP negative ruling, band-selective
FX, crunch≠crush + the 96 corrections;
workflows +3: the scheme-gap
collection, SP-404 routing/DJ-mode
doctrine, djay configuration
doctrine).

Adjudications worth the record: the
V10's HELIX is a DUPLICATE of WEB-07
(the same Pioneer effect, second
manual — its overlay/freeze laws are
the axis); Roland's Resonator is an
AXIS on WEB-18 (WEB-18 already renders
feedback combs with in-loop damping);
djay's Tempo Blend is an AXIS on
T-021 (the tempo-convergence family is
T-021's; the dual-sided fader coupling
is the staging); the Mute Bus break is
an AXIS on T-034 (the void family,
decaying where the freeze sustains);
Pioneer's TRANS and Roland's Slicer
are ONE base (the preset-table form is
the richer mechanism; duty is its
staging); the Xone all-pass and the
SP-404 Phaser are ONE base (one
topology, two attestations).

Validation, mirroring Phases 22–24:
check_pure_functions green at import
(harmonic mix + the select_technique
assert table, canonical cases unmoved —
eq_blend still ranks #1 on the lateral
pair, hook_drop_handoff #1 with an
iconic A); meta defaults == function
defaults for all eight bases; selection
probes rank every new base in its home
pair with its own prefers reasons
firing (pre_filtered_echo #6,
notch_carve_sweep #5, phaser_sweep #5,
stem_swap_replace #9, djfx_microloop
#6, cyclic_speed_dip #1 on the
wide-tempo pair, pattern_gate_slicer
#4, sideband_comb_filter #3); all 134
new variants smoke-render and none
renders identical to its base; the
demo battery is 122/122 clean (114 +
8 new). One staging fix inside the
tranche: the pattern_gate_slicer demo
initially gated the sketch's sparse
first-8-bars tail (raw −45 dB RMS; the
pattern's 0.15 steps pushed a 50 ms
window under the −60 dBFS floor) — the
demo now stages on last_bars like the
other exit demos; the gate and the
base were not touched, and no allowed
span was declared.

Counts: registry 88 → 96 (87 render /
5 overlay / 3 decision / 1 planning);
variants 736 → 870 across 68 bases
(+134: the new bases carry 11/8/18/7/
18/18/31/23); knowledge 141 → 151
(mixing 38, performers 14, producing
50, setcraft 28, workflows 21);
verdicts ADOPT 60 / ADAPT 28 → 36;
demos 114 → 122, all clean. VARIANTS.md
regenerated with its embedded
generator; ENUMERATION.md carries a
growth addendum (no new walk); the V2
map's queue item 4 is marked DONE and
its Class 5 corrections stand in place.

WHITE SPACE. (1) The map's yield
estimates for Class 5 were catalogue
counts, and catalogues lie by naming:
most of what six flagship products call
effects were already bases here under
other vendors' names — the tranche's
real yield is eight mechanisms plus
ground truth, and any second
software/hardware pass (tranche B)
should be priced as an axes-and-
knowledge exercise from the start, not
a base hunt. (2) Two of the eight bases
rest on a single vendor page each
(WEB-23 on the 96's guide, WEB-25 on
VDJ's sampler pages) — no second
attestation was findable in the free
corpus this pass; both are ADAPT/medium
for exactly that reason. (3) The V10
record is mirror-grade: manua.ls OCR
garbles the SEND block diagrams, and
the manual withholds every crossover
frequency, every SEND range, and the
COMP law — the official PDF stays
login-walled and unbypassed, so the
V10's numbers bank as knob semantics,
not measurements. (4) Roland publishes
neither the Slicer's 32 pattern tables
nor Scatter's 10 TYPE permutations:
WEB-28 renders the documented mechanism
with the registry's own tables, and any
future claim of "the hardware's
patterns" would be invention. (5) The
unnameable five (Mixxx metaknob
trajectories, djay's held mashup state,
the 96's B2B dual-cue changeover,
Zan-Zou's stereo-only phase delay,
SP-404's two-stream sidechain and
FAVOURITE chain pairs) mark the ID
scheme's real frontier — trajectory
modifiers, state objects, chain
syntax — the same wall Phase 24's
enumeration hit from the other side
(214 stagings). A scheme extension is
a design project of its own; this
tranche records the pressure, it does
not relieve it. (6) djay's Neural Mix
EQ boost/kill figures exist only in a
staff forum post; the manual states no
dB range and no kill — the axis banks
the centre=unity law and leaves the
numbers forum-grade. (7) MODEL 1
(PLAYdifferently) was named in queue
item 4's text but was not in this
tranche's target list and no MODEL 1
source was fetched — it stands
unworked for tranche B, alongside the
class's unworked remainder (Xone:92 /
PX5 via mirrors, the Mixxx developer
sources, VDJScript). (8) Nothing in
this tranche was heard: the eight
bases are validated by the battery and
selection probes, not by ears — the
sketch demos prove shape, not feel,
and the first real-track staging of
each remains the test that counts.
(9) Queue as left: item 5 (genre
traditions tranche B — techno
multi-deck doctrine + trance/harmonic
+ open-format tables) tops the ranked
queue; item 7's academic pass carries
Phase 25's early partial delivery;
the conditional clusters stay parked
with their gates.
