# open-transitions

An open library of named, parameterizable DJ transition techniques — plus an engine that renders them. MIT licensed.

## The problem

Every DJ tutorial teaches the same transitions: the long harmonic EQ blend, the echo-out, the filter-sweep build, the brake, the backspin, the wordplay drop. But the knowledge lives in YouTube videos and forum posts as prose — "bring the bass in slowly, sweep the filter" — never as parameters a machine can execute. Auto-DJ tools do one thing: the crossfade. The creative vocabulary of real DJing has no open, code-readable home.

## What this is

1. **`techniques/`** — 82 technique specs, each a parameter-level recipe: the exact moves (EQ positions, filter automation curves, FX type + values, timing in bars/beats), parameters with units and defaults, why it works, when to use/avoid it, and provenance (bank T-001–T-039, gap-report GAP-01–GAP-18, DM-clip DM-Axx, performer PERF-ZAB, web-mined WEB-01–WEB-18). Prose is documentation; the parameters are the product.
2. **`engine/`** — deterministic DSP (numpy + scipy only) that renders the techniques on real audio: `dsp.py` (building blocks), `techniques.py` (the 32 named techniques), `render.py` (plan-file batch renderer), `verify.py` (silence/headroom/timbre gates).
3. **`demos/`** — `make_demos.py` synthesizes two deterministic test tracks (no copyrighted audio) and renders + verifies a demo clip per technique into `demos/out/`.
4. **The framework** ([FRAMEWORK.md](FRAMEWORK.md)) — what makes this a system instead of a pile of recipes: every technique is registered in a **metadata registry** (`engine/meta.py`) with hard preconditions, soft preference rules, parameter families, an energy/exit profile, and ≥1 real-world evidence reference (no orphan techniques). A **selection engine** (`engine/select.py`) takes structured info about two songs — tempo, key, energy, sections, vocals, genre — evaluates every technique's preconditions, and returns ranked candidates with reasons *plus* a "why not" list for the rejects. An **extension grammar** (variants × parameter grids, overlays, chains, compounds) grows the library mechanically toward hundreds of renderable entries.
5. **`knowledge/`** — documented production/mixing/set craft with full provenance that informs selection but isn't itself a renderable transition.

## What this is not

- Not a crossfader. Crossfades are one technique among dozens.
- Not a source of copyrighted audio. **This repo ships techniques and code only — never copyrighted music.** All development audio is synthesized sketch material. If you build on this, bring your own legally-obtained tracks.

## Technique catalog

| Technique | Bank | Verdict | Confidence | What it does |
|---|---|---|---|---|
| `hook_drop_handoff` | T-038 | ADOPT | field-tested | Signature vocal hook is the final event; incoming blooms in as texture at the drop |
| `screwed_treatment` | T-039 | ADOPT | high | Chopped & screwed / slowed / 2x-speed pre-transition treatment |
| `wordplay` | T-011 | ADAPT | high | Shared-lyric word answered by the incoming track in rhythmic unison |
| `build_to_drop` | T-009 | ADAPT | high | Dual-build layering: two builds fuse, incoming drops |
| `three_deck_layer` | T-020 | ADAPT | medium | Glue layer: tri-partite frequency slotting, energy floor never dips |
| `beat_jump` | T-028 | ADOPT | high | Phrase-realignment playhead arithmetic (planning primitive) |
| `pitch_play` | T-032 | ADOPT | high | Key-shifted vocal overlay (±2 semitones max) |
| `eq_blend` | T-001 | ADOPT | high | 3-band frequency-replacement long blend (breakpoints scale with blend length) |
| `bass_swap` | T-002 | ADOPT | high | Instantaneous low-band handover on the downbeat |
| `filter_sweep` | T-003 | ADOPT | high | HPF/LPF opposing sweep, snap open on the 1 |
| `echo_out` | T-004 | ADOPT | high | Echo throw + fader kill; slam the next track on the downbeat |
| `echo_out_blend` | T-004b | ADOPT | high | Echo throw with the incoming track emerging under a diffused tail |
| `layered_emergence` | T-004c | ADOPT | high | Stacked: thinning sweep + riser + echo throw + wash bloom + HP entrance |
| `reverb_wash` | T-005 | ADOPT | high | Dissolve outgoing into reverb; incoming emerges from the fog |
| `brake_stop` | T-006 | ADOPT | high | Vinyl brake / tape stop (pitch+tempo dive to a halt) |
| `backspin` | T-007 | ADAPT | medium | Spinback rewind over 1 beat, slam on the downbeat |
| `loop_roll_build` | T-008 | ADOPT | high | 1/2→1/4→1/8→1/16 roll build with HPF thinning |
| `acapella_overlay` | T-010 | ADAPT | medium | Vocal over instrumental (low-kill EQ preset + overlay window) |
| `power_down` | T-013 | ADOPT | high | Pitch-fader drag 0→−100%: the track runs out of life |
| `hotcue_drop_swap` | T-014 | ADOPT | high | Replace A's drop with B's over the 4-beat run-up |
| `harmonic_mix` | T-015 | ADOPT | high | Camelot compatibility decision function (pure) |
| `layered_fx_stack` | T-017 | ADOPT | high | Echo (time) + HPF (frequency) + reverb (space) stacked on the outgoing |
| `noise_echo_buildup` | T-018 | ADOPT | high | Empty-channel noise riser with 1/2-beat echo |
| `stutter_transition` | T-019 | ADAPT | medium | Hot-cue vocal stutter taps (3, 3-and, 4, 4-and), then release |
| `tempo_bridge` | T-021 | ADOPT | high | Pitch-preserving BPM ramp (phase vocoder) or half/double metric shift |
| `drum_bridge` | T-022 | ADOPT | high | Strip to drums (key-neutral zone), blend B in |
| `breakdown_transition` | T-023 | ADOPT | high | Whole transition inside A's breakdown (BPM/key/genre can all change) |
| `double_drop` | T-024 | ADAPT | medium | Two builds, one downbeat, one sub-bass (single-sub rule enforced) |
| `vocal_punchline_snap` | T-025 | ADOPT | high | Low-kill → vocal isolate → 150–200 ms void → drop at unity |
| `genre_bridge` | T-026 | ADAPT | medium | Pivot genres on a looping vocal anchor in a reverb wash |
| `loop_transition` | T-027 | ADOPT | high | Bounded 2-cycle loop handoff + EQ blend (never a third cycle) |
| `fake_drop` | T-029 | ADAPT | medium | Build, 2–4 beat void, real drop (human-triggered weapon) |
| `hard_cut` | T-030 | ADOPT | high | No blend, no FX — the cut, with total commitment |
| `loop_juggle_replace` | T-031 | ADAPT | medium | Steal the groove hit by hit (The Replace) |
| `vocal_chop_build` | T-033 | ADOPT | high | Chop-density ladder (1/4→1/8→1/16) + band-pass sweep → drop |
| `reverb_freeze` | T-034 | ADOPT | high | Frozen reverb tail; B launches inside it, freeze releases |
| `riser_drop` | — | ADOPT | medium | Riser + HP thinning into a tempo-jump drop |
| `select_technique` | T-037 | ADOPT | high | Decision brain: musical features → technique + rejection reasons (pure) |
| `stem_element_crossfade` | GAP-08 | ADOPT | medium | 16-bar handover one stem at a time — incl. the bass-stem-only entry |
| `strip_down_buildup` | GAP-09 | ADOPT | medium | The build is progressive element *removal*; B's full kit slams in |
| `flying_solo_acapella` | GAP-10 | ADAPT | medium | Naked-vocal reset: soloed acapella alone, B filters up underneath |
| `beat_switch_under_acapella` | GAP-11 | ADOPT | medium | One continuous acapella; the instrumentals rotate underneath |
| `accidental_duet` | GAP-12 | ADAPT | medium | Two isolated vocals in key/tempo sync read as a duet |
| `same_song_switchup` | GAP-13 | ADAPT | medium | Two arrangements of the same song alternated via cue flips |
| `sample_connection` | GAP-01 | ADAPT | medium | Cue swap into the track that samples A, exactly on the shared element |
| `loop_tightening_build` | GAP-02 | ADOPT | medium | Hype Loops: grabbed loop halved (4→2→1→½) over B's build |
| `polyrhythmic_loops` | GAP-04 | ADAPT | medium | 4-beat vs 3-beat loops layered as an evolving transition bed |
| `slip_mode_flourish` | GAP-05 | ADAPT | medium | Live flourish over a playhead that never stops (slip safety net) |
| `premade_tempo_bridge_edit` | GAP-07 | ADOPT | medium | A produced edit that itself ramps BPM carries the bridge — no live pitch work |
| `sampler_one_shot_mask` | GAP-17 | ADOPT | medium | One-shot fired exactly on the cut masks the join |
| `feedback_loop_build` | PERF-ZAB | ADOPT | medium | Zabiela: feedback delay ramped 0.5→0.95, then the loop cuts |
| `metric_loop_pivot` | PERF-ZAB | ADAPT | medium | 3-beat loop cycles pivot tempo at the 12-beat alignment (Zabiela 2020) |
| `scratch_in` | GAP-14 | ADAPT | medium | B's first beat baby-scratched in rhythm, released on the downbeat |
| `rhythmic_fader_chops` | GAP-15 | ADOPT | high | Transformer-style fader chops as the transition gesture itself |
| `spare_deck_element_firing` | GAP-16 | ADAPT | medium | Spare-deck elements (riser loop, vocal hit) fired like orchestra sections |
| `riser_ducking_overlay` | T-035 | ADOPT | high | Overlay: kick-ducked riser at −6 dB under the mix, hard cut + downlifter |
| `live_loop_mix` | DM-A14 | ADAPT | medium | 2-bar loop + ¼-beat TRANS gate while B's fader rises (French Candy) |
| `cdj_synth_lead` | DM-A15 | ADOPT | medium | Single-cycle synthesis: a loop grab becomes a playable lead |
| `tempo_double_trick` | DM-A21 | ADAPT | medium | Metric doubling: pitch-ramp to 2× as B enters (French Candy) |
| `reverse_vocal_ambience` | DM-A23 | ADOPT | medium | Reverse → delay/reverb → reverse back: a swelling entrance texture |
| `whoa_reverb_wobble` | DM-A39 | ADOPT | medium | Skrillex "whoa": big reverb tail + accelerating tremolo wobble |
| `vocal_tremolo_gate` | DM-A44 | ADOPT | medium | 1/16 tremolo gate, amount automated up on the note (mono Auto-Pan) |
| `mic_talkover_reset` | GAP-18 | ADAPT | medium | Planning entry: mic over the outro resets the room; next track cold |
| `spiral_echo` | WEB-01 | ADOPT | medium | Feedback delay whose repeats pitch-shift: A's last fragment spirals away over B's entrance (DJM SPIRAL, rendered) |
| `flanger_sweep` | WEB-02 | ADOPT | medium | Jet comb sweep thins A's final bars; B enters dry and full-bodied on the downbeat |
| `reverse_roll` | WEB-03 | ADOPT | medium | A's last beat loops backwards in halving tiles (REV ROLL) — an inhalation build; B releases beat-locked |
| `crush_degrade` | WEB-04 | ADOPT | medium | Bit depth + sample rate collapse over A's final bars; B arrives at full fidelity — the contrast is the drop |
| `shepard_riser` | WEB-05 | ADOPT | medium | Shepard-Risset endless-rise layer under A's final bars; cuts dead, B inherits the tension |
| `granular_freeze` | WEB-06 | ADOPT | medium | A's last ~150 ms sustained as a grain cloud; B fades up inside it, owing no key or tempo |
| `helix_catch` | WEB-07 | ADOPT | medium | A's last fragment is caught in a loop, pitch-ramps during the hold, and releases snapped home into B (DJM HELIX) |
| `beatslicer_shuffle` | WEB-08 | ADOPT | medium | A's final bar(s) sliced 8-per-bar and replayed in named permutations, BUZZ on the final beat (Traktor BeatSlicer) |
| `downlifter_exit` | WEB-09 | ADOPT | medium | Descending synth sweep across the seam masks a hard cut — the riser's mirror image |
| `shimmer_wash` | WEB-10 | ADOPT | medium | A's tail pitched +12 st into a long reverb; B enters under the climbing shimmer (RMX-1000 Reverb Up principle) |
| `infinity_filter` | WEB-11 | ADOPT | medium | Endless barber-pole resonant sweep: A's own spectrum climbs forever and never arrives; B enters dry (Serato Infinity Filter) |
| `pattern_layer_bridge` | WEB-12 | ADOPT | medium | A synthesized 808/909-style pattern layer carries the seam zone while A exits and B establishes (Traktor Pattern Player) |
| `pumper_exit` | WEB-13 | ADOPT | medium | Beat-synced ducking deepens across A's final bars; the last recovery is withheld and B fills the hole (Denon Pumper) |
| `scale_down_exit` | WEB-14 | ADOPT | medium | A's captured beat replays down a musical scale, one beat-locked step at a time, across B's entrance (Engine Scale Down) |
| `fader_synth` | WEB-15 | ADOPT | medium | A's channel is replaced by a fader-played oscillator line riding a scale across the seam; B inherits it (DJM-S11 FADER SYNTH) |
| `ring_mod_dissolve` | WEB-16 | ADOPT | medium | A's final bars are multiplied by a rising carrier (100 Hz → kHz) until the track dissolves into inharmonic sidebands; B enters dry (Traktor Ring Modulator) |
| `formant_morph_exit` | WEB-17 | ADOPT | medium | A's final bars morph through the a-e-i-o-u vowel formant series — the track talks its way out; B enters dry (Traktor Formant Filter) |

Verdict key: **ADOPT** = fully scriptable parameter automation · **ADAPT** = automatable, needs human-feel choices (noted per technique) · field-tested = rendered and approved by ear on real mixes.

## Quickstart

```bash
pip install numpy scipy matplotlib
# render + verify every technique demo (synthesized audio, ~1 min)
python3 demos/make_demos.py
# just one
python3 demos/make_demos.py --only hook_drop_handoff
```

Use it in code:

```python
from engine import techniques, dsp

# pick the technique from the musical situation (T-037)
choice = techniques.select_technique({
    "bpm_delta_pct": 1.0, "half_double_ok": False,
    "camelot_distance": 0, "energy_delta": 0.0,
    "phrase_a": "outro", "vocal": "neither", "genre_pair": "same",
    "b_has_build": False, "a_has_breakdown": False,
    "iconic_vocal": "a", "b_intro_bars": 16, "drop_pair_ok": False,
})
print(choice["technique"], choice["reasons"])   # hook_drop_handoff [...]

# render it (a, b: mono float arrays; bar_s: seconds per bar)
mix = techniques.hook_drop_handoff(a, b, sr, bar_s,
                                   exit_fade_ms=70.0, bloom_bars=3)
mix, _ = dsp.normalize_peak(mix, target_db=-1.0)
```

Batch-render real tracks from a plan file:

```bash
python3 -m engine.render --analysis analysis.json --audio-dir ./audio \
    --out-dir ./clips --plan plan.json
```

`plan.json` entries: `{"id": ..., "out": {"file", "t0", "bars", "bar_s", "bpm"}, "in": {...}, "technique": "eq_blend", "technique_args": {"blend_bars": 32}, "handoff_s": ...}`.

## Verification

Every demo render passes `engine/verify.py`:

- **(a) silence gaps** — no digital silence (>50 ms below −60 dBFS) except where the technique intentionally has it (declared per-demo: drop voids, spin decays, fade tails);
- **(b) headroom** — peak < 0 dBFS (renders normalize to −1 dBFS);
- **(c) timbre continuity** — spectral-centroid track ±2 s around the handoff; brick-wall jumps reported (some techniques are *supposed* to snap).

`demos/out/verification.json` + per-clip PNGs are the receipts. Pure decision functions (`harmonic_mix`, `select_technique`) are covered by assertions in `make_demos.py`.

## Layout

```
FRAMEWORK.md      the architecture contract: metadata schema, song schema,
                  selection design, evidence layer, extension grammar
engine/
  dsp.py          DSP primitives: 3-band EQ, sweep filters, feedback delay,
                  Schroeder reverb (+freeze), riser synth (T-035 ducking),
                  warp resample (brake/power-down), phase-vocoder stretch
  techniques.py   the core bank techniques (parameterized, docstringed)
  dm_techniques.py  DM-clip lane (DM-A14…A44) · gap_struct.py  stem/routing
                  gaps · gap_rest.py  TIME/DYN/SYNTH gaps + Zabiela ·
                  performer.py  PERF gaps + T-035 overlay ·
                  web_techniques.py  web-mined lane (WEB-01…WEB-17)
  meta.py         technique metadata registry (preconditions, preferences,
                  parameter families, evidence) — read by the selector
  select.py       selection engine v1: two songs in → ranked techniques
                  with reasons + a "why not" list (generalizes T-037)
  variants.py     variant generator: base × named parameter presets
                  (257 variants, see VARIANTS.md)
  render.py       plan-file batch renderer (TECHNIQUES registry)
  verify.py       silence / headroom / centroid gates + plots
techniques/       per-technique spec docs (core generated from docstrings:
                  demos/gen_technique_docs.py; domains ship theirs)
knowledge/        production / mixing / set craft with provenance
                  (82 entries: producing, mixing, setcraft, workflows,
                  performers)
demos/
  make_demos.py   synthesized test tracks + demos + verification
                  (auto-merges demos/ext_*.py domain modules)
  out/            rendered WAVs, verify PNGs, verification.json
examples/         (worked technique-spec → automation examples; next)
BUILD-LOG.md      what was built, tested, and what's next
```

## Status

Active build. **82 registry entries: 81 executable techniques + 1 planning entry; 332 named variants renderable via `engine/variants.py`; 94 knowledge entries.** Phase 4 (2026-10-20): the expansion wave — gap report's 16 actionable gaps all implemented (incl. element-by-element stem crossfade with the bass-stem-only entry), 6 DM-clip DJ techniques, Zabiela's feedback-loop + metric-pivot moves, T-035 riser ducking as an overlay, and the variant generator. Selection smoke tests: stem techniques surface only when stems exist and reject with the named reason otherwise. Web-mined tranche (2026-10-21): a full backlog audit (zero buildable leftovers — every qualifying DM/gap candidate was already built; the rest are knowledge-class or documented skips) plus six fresh techniques mined from DJ literature (Pioneer DJM effect taxonomy, Shepard-tone and granular-synthesis sources) — spiral echo, flanger sweep, reverse roll, crush degrade, Shepard riser, granular freeze — each with registry entry, variants, spec doc, and a verified demo (suite: 96/96 clean). Phase 6 (2026-10-21): the educationals study program opened — an 85-source bibliography of DJ/producer educational sources (in the goal workspace's technique-bank, with a ranked next-mining queue), and tranche 1 mined the first-party effect catalogs (DJM Beat FX/Colour FX, Traktor FX, RMX-1000) for four more techniques: helix catch, beatslicer shuffle, downlifter exit, shimmer wash — 22 further catalog items were overlap-resolved into existing entries, not rebuilt (suite: 100/100 clean). Phase 7 (2026-10-21): tranche 2 of the study program worked the source list's queue top-down — the DJM-A9 manual body, Serato's FX + Flip documentation, Traktor Pro 4's FX chapters, and the DJ TechTools compounds pass — for two more techniques: infinity filter (Serato's endless barber-pole sweep, rendered as a Shepard peak stack) and pattern layer bridge (Traktor's Pattern Player as a synthesized seam layer) — Serato Flip went to the knowledge layer as an authoring model, and everything else (the full A9 catalog against its manual body, 40+ Serato FX names, Traktor's 9 Mixer FX, every named DJTT/MacroFX chain) was overlap-resolved into existing entries, not rebuilt (suite: 102/102 clean). Phase 8 (2026-10-21): tranche 3 worked the queue's next four — the Denon Engine DJ documentation (X1850 BPM/Sweep FX, Prime Touch FX, the 26 Main FX), the Pestrela KB's Controllers remainder, the rekordbox manuals (Release FX, Slip mode), and the DJM-S11 manual body — for three more techniques: pumper exit (Denon's downbeat duck, with rekordbox's DUCKING as second vendor), scale down exit (Engine's beat-stepped pitch descent through four scales), and fader synth (the S11's source-replacing fader oscillator) — rekordbox's Release FX operator and Pioneer's Smooth Echo went to the knowledge layer as operator models, and the remaining catalogs (Denon's Sweep/Touch/BPM FX sets, the S11's Beat FX axes, Pestrela's mapping craft) were overlap-resolved into existing entries, not rebuilt (suite: 105/105 clean). Phase 9 (2026-10-21): tranche 4 closed the structured vendor catalogs — the RMX-1000 manual body (Zip settled as the RMX-500's pitch shifter, Sub Parameter settled as a control layer), the Traktor 2 manual's full "Effects in Detail" chapter read to completion, the VirtualDJ native effects list (a fourth taxonomy, complete overlap), and Mixed In Key's harmonic/energy research for the selection layer — for two more techniques, both from the Traktor chapter's last unread pages: ring mod dissolve (the Ring Modulator's carrier multiplication, §14.4.25) and formant morph exit (the Formant Filter's vowel-series morph, §14.4.30); the chapter's Pulse family was banked as a peak-trigger modulation-source axis, Mixed In Key yielded two setcraft entries plus three `select.py` proposals recorded in BUILD-LOG (not implemented), and everything else was overlap-resolved into existing entries, not rebuilt (suite: 107/107 clean). Phase 10 (2026-10-21): tranche 5 worked the educator canons — Crossfader's canonical 12 named transitions (from the channel's own walkthrough text) plus a second-video transcript, Club Ready DJ School's written harmonic-mixing guide, and DJ Carlo's flagship techniques video — for zero new bases: the unmined Crossfader names resolved as a pairing framing (same-song switch up), a fractional loop-length axis on the loop roll (polyrhythmic looping), a sync-locked pair-ramp axis on the tempo bridge (sample switch up / wide syncing), and a gated trigger-mode axis on the gate cut (Serato Gate Cue); Club Ready contributed the compatibility-vs-modulation framing to the knowledge layer, and Carlo's stems mashup staging added a vocal-led order axis to the stem crossfade. The same phase discharged the selection layer's engineering debt: all three Phase 9 `select.py` proposals are implemented — the note-sharing Camelot diagonal scores 2 in `camelot_distance`, a signed `key_move` feature lets snap/void exits prefer +1/+2-semitone energy boosts (the quick-mix rule as scoring; seamless/tail gates untouched), and the +4 far move is gated on a vocal-free pair — each with before/after probe evidence and new `check_select()` guard cases (suite: 107/107 clean). See [BUILD-LOG.md](BUILD-LOG.md) and [VARIANTS.md](VARIANTS.md). Phase 11 (2026-10-21): tranche 6 worked the queue top-down — Digital DJ Tips' transition coverage, the r/Beatmatch + r/DJs community layer, the Sound on Sound remainder, and the Ableton Live audio effect reference — for one new technique: resonator tail (Ableton's Resonators — A's final bars excite a five-resonator bank voiced as B's chord and ring away under B's entrance, the first new base since Phase 9, found in producer-side semantics as the Phase 10 queue refresh predicted). Shifter's pitch-feedback delay deduplicated onto spiral echo (Pioneer's SPIRAL is the same mechanism); Digital DJ Tips and Sound on Sound resolved entirely to confirmations, axes, and craft (incl. the pre-entry dry-up and the ducked FX return); the community item stands partial — Reddit's hosts refuse the fetch in this environment, so it was worked from readable forum threads, yielding a stepped-tease axis, the failure-mode set (incl. the kick-peak alignment caveat), and a trainwreck-salvage knowledge entry (suite: 108/108 clean). Phase 12 (2026-10-21): tranche 7 worked the queue's next five — the Traktor Pro 4 manual's non-FX chapters, DeSantis's *Making Music* (the free web edition's transition-relevant chapters), James Hype, DJ Phil Harris, and Laidback Luke — for zero new bases and six knowledge entries: Flux Mode is the slip playhead model's second first-party statement ("without losing the phrasing"), the Stem Deck semantics land on the stem crossfade, Tempo Master succession and the fade-marker pair join the setcraft/workflows layers, Fuzzy Boundaries and Unique Events give the staggered seam and one-time seam punctuation their producer-canon names, Hype's acapella-as-glue confirms the beat-switch-under-acapella compound's vocal-led staging, Harris's Levels stack states the layering order (FX as a second layer over a sound blend), and Luke contributes the Element Matching genre-bridge axis plus the tempo ≠ energy doctrine (suite: 108/108 clean; selection smoke green).

## License

MIT — see [LICENSE](LICENSE).
