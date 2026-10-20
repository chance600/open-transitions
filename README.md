# open-transitions

An open library of named, parameterizable DJ transition techniques — plus an engine that renders them. MIT licensed.

## The problem

Every DJ tutorial teaches the same transitions: the long harmonic EQ blend, the echo-out, the filter-sweep build, the brake, the backspin, the wordplay drop. But the knowledge lives in YouTube videos and forum posts as prose — "bring the bass in slowly, sweep the filter" — never as parameters a machine can execute. Auto-DJ tools do one thing: the crossfade. The creative vocabulary of real DJing has no open, code-readable home.

## What this is

1. **`techniques/`** — 32 technique specs, each a parameter-level recipe: the exact moves (EQ positions, filter automation curves, FX type + values, timing in bars/beats), parameters with units and defaults, why it works, when to use/avoid it, and bank provenance (T-001–T-038). Prose is documentation; the parameters are the product.
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
  techniques.py   the 32 named techniques (parameterized, docstringed)
  meta.py         technique metadata registry (preconditions, preferences,
                  parameter families, evidence) — read by the selector
  select.py       selection engine v1: two songs in → ranked techniques
                  with reasons + a "why not" list (generalizes T-037)
  render.py       plan-file batch renderer (TECHNIQUES registry)
  verify.py       silence / headroom / centroid gates + plots
techniques/       per-technique spec docs (generated from docstrings:
                  demos/gen_technique_docs.py)
knowledge/        production / mixing / set craft with provenance
demos/
  make_demos.py   synthesized test tracks + demos + verification
                  (auto-merges demos/ext_*.py domain modules)
  out/            rendered WAVs, verify PNGs, verification.json
examples/         (worked technique-spec → automation examples; next)
BUILD-LOG.md      what was built, tested, and what's next
```

## Status

Active build. 38 techniques implemented, 36 demos rendered + verified, 2 pure functions assertion-checked. Phase 2 (2026-10-18): closed GAP-A (T-009 build_to_drop, T-011 wordplay, T-020 three_deck_layer, T-028 beat_jump, T-032 pitch_play) and GAP-B (T-039 screwed_treatment, new bank entry); added dsp.pitch_shift; verify.py plots now optional (matplotlib/numpy2 env). Framework phase (2026-10-20): FRAMEWORK.md + metadata registry (39 entries, all with evidence) + selection engine v1 (`engine/select.py`, agrees with T-037 on its canonical cases, asserted in the demo suite) + domain-module contracts so new technique lanes merge without shared-file edits. See [BUILD-LOG.md](BUILD-LOG.md) for the session log and the queued next batch.

## License

MIT — see [LICENSE](LICENSE).
