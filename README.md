# open-transitions

An open library of named, parameterizable DJ transition techniques — plus an engine that renders them. MIT licensed.

## The problem

Every DJ tutorial teaches the same transitions: the long harmonic EQ blend, the echo-out, the filter-sweep build, the brake, the backspin, the wordplay drop. But the knowledge lives in YouTube videos and forum posts as prose — "bring the bass in slowly, sweep the filter" — never as parameters a machine can execute. Auto-DJ tools do one thing: the crossfade. The creative vocabulary of real DJing has no open, code-readable home.

## What this is

1. **`techniques/`** — 64 technique specs, each a parameter-level recipe: the exact moves (EQ positions, filter automation curves, FX type + values, timing in bars/beats), parameters with units and defaults, why it works, when to use/avoid it, and provenance (bank T-001–T-039, gap-report GAP-01–GAP-18, DM-clip DM-Axx, performer PERF-ZAB). Prose is documentation; the parameters are the product.
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
                  performer.py  PERF gaps + T-035 overlay
  meta.py         technique metadata registry (preconditions, preferences,
                  parameter families, evidence) — read by the selector
  select.py       selection engine v1: two songs in → ranked techniques
                  with reasons + a "why not" list (generalizes T-037)
  variants.py     variant generator: base × named parameter presets
                  (127 variants, see VARIANTS.md)
  render.py       plan-file batch renderer (TECHNIQUES registry)
  verify.py       silence / headroom / centroid gates + plots
techniques/       per-technique spec docs (core generated from docstrings:
                  demos/gen_technique_docs.py; domains ship theirs)
knowledge/        production / mixing / set craft with provenance
                  (81 entries: producing, mixing, setcraft, workflows,
                  performers)
demos/
  make_demos.py   synthesized test tracks + demos + verification
                  (auto-merges demos/ext_*.py domain modules)
  out/            rendered WAVs, verify PNGs, verification.json
examples/         (worked technique-spec → automation examples; next)
BUILD-LOG.md      what was built, tested, and what's next
```

## Status

Active build. **64 registry entries: 62 executable techniques + the T-037 decision brain + 1 planning entry; 127 named variants renderable via `engine/variants.py`; 81 knowledge entries.** Phase 4 (2026-10-20): the expansion wave — gap report's 16 actionable gaps all implemented (incl. element-by-element stem crossfade with the bass-stem-only entry), 6 DM-clip DJ techniques, Zabiela's feedback-loop + metric-pivot moves, T-035 riser ducking as an overlay, and the variant generator. Selection smoke tests: stem techniques surface only when stems exist and reject with the named reason otherwise. See [BUILD-LOG.md](BUILD-LOG.md) and [VARIANTS.md](VARIANTS.md).

## License

MIT — see [LICENSE](LICENSE).
