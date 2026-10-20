# FRAMEWORK — how open-transitions is organized, selected, and extended

This document is the architecture contract for the library. Everything else
(specs, engine code, demos) conforms to it. It exists so that **any LLM or
human can (a) pick the right technique for two given songs, and (b) add new
techniques mechanically** — the difference between a pile of recipes and a
system with real utility.

---

## 1. The three layers

| Layer | What it is | Where it lives |
|---|---|---|
| **Techniques** | Named, parameterized, executable moves. Each has a function, a spec doc, a demo render + verification, and ≥1 real-world evidence reference. | `engine/*.py`, `techniques/*.md` |
| **Selection** | A decision engine: given structured info about two songs, it evaluates every technique's preconditions, ranks the survivors with reasons, and explains the rejects. | `engine/select.py` over `engine/meta.py` |
| **Knowledge** | Documented tips, workflows, and craft that inform selection or production but are not themselves renderable transitions (DAW tricks, prep workflows, set philosophy). Each carries provenance. | `knowledge/*.md` |

**Counting rules (honesty contract).** Reported numbers always separate:
*techniques* (executable, spec'd, demo-verified), *variants* (named parameter
presets, renderable through the variant registry), and *knowledge entries*
(documented, provenance-carrying, not transitions). No layer inflates another.

---

## 2. Taxonomy (families)

Adapted from the bank's 9-cell taxonomy v2, plus the ROUTING family the v4
research plan added (stem routing had no home in v2 — the gap report's
STRUCT residual-bucket problem).

| Family | Meaning |
|---|---|
| `FREQ` | Frequency-selective processing: EQ, filters, isolators |
| `TIME` | Repetition & playhead manipulation: loops, rolls, cue retriggering, beat-jump, slip |
| `SPACE` | Reverb / delay / spatial tails and dissolves |
| `DYN` | Pitch / rate transformation |
| `STRUCT` | Arrangement-level structure: overlays, handoffs, bridges, drop collisions |
| `ROUTING` | Stem-level routing: element-by-element handover, stem muting, spare-deck elements |
| `PERF` | Performance / execution gestures: scratch, fader chops, live hardware moves |
| `SYNTH` | DJ-injected signals: risers, noise, one-shots, synthesized leads |
| `COMP` | Compounds of 2+ atoms (named in `composed_of`) |
| `SET` | Set context & endpoints: planning, opening/closing, recovery, hosting |

A technique has exactly one primary family. Compounds additionally list their
atoms in `composed_of`.

---

## 3. Technique metadata schema

Every technique is registered in a `META` dict (in `engine/meta.py` for the
core bank, or in its own domain module — see §7). The registry is the single
source of truth the selection engine reads.

```python
META["eq_blend"] = {
    "title": "EQ Blend (3-Band Frequency Replacement)",
    "bank": "T-001",                 # bank id | "DM-A14" | "GAP-08" | "PERF-…" | None
    "family": "COMP",
    "kind": "render",                # render | decision | planning | overlay
    "verdict": "ADOPT",              # ADOPT | ADAPT | SKIP (SKIP = documented exclusion)
    "confidence": "high",            # high | medium | field-tested | low
    "requires": {                    # HARD preconditions on PairFeatures (§4)
        "bpm_delta_pct_max": 10.0,
        "camelot_max": 3,
        "vocal_ok": ["a_only", "b_only", "neither"],
        "phrase_a_ok": ["outro", "verse", "chorus"],
        "genre_pair_ok": ["same", "neighbor"],
        "needs": [],                 # feature flags: b_build, a_breakdown,
                                     # iconic_a, iconic_b, drop_pair, stems,
                                     # glue, shared_lyric, anchor_vocal, third_deck
    },
    "prefers": [                     # SOFT scoring rules
        {"when": "energy_delta_abs<=1", "weight": 3,
         "reason": "lateral energy — invisible handoff"},
    ],
    "energy": {"delta": 0, "tension": "flat"},   # typical outcome
    "exit": "seamless",              # seamless | snap | tail | void | loop
    "clash_risk": "bass",            # none | vocal | bass | key
    "params": {                      # parameter families
        "blend_bars": {"type": "int", "range": [4, 64], "default": 32,
                       "unit": "bars"},
    },
    "evidence": [                    # ≥1 REQUIRED — no orphan techniques
        {"type": "cookbook", "ref": "null-set-ai-dj Transition Cookbook (MIT)",
         "url": None, "date": None},
    ],
    "composed_of": [],               # atom ids for COMP family
}
```

Rules:
- **`requires` are hard.** A technique that fails a hard precondition is
  rejected *with the reason recorded* — the "why not" list is a first-class
  output, because most trainwrecks come from blending where a cut was
  required (T-037's founding insight).
- **`prefers` are soft.** Each match adds its weight and appends its reason.
- **`evidence` is mandatory.** Types: `tutorial`, `cookbook`, `course`,
  `set`, `clip`, `paper`, `field-test`. A technique with no evidence does
  not enter the registry.
- **`params`** declare the continuous ranges + the discrete preset axes the
  variant generator (§6) may enumerate.

---

## 4. Song schema and pair features

Selection never sees audio — it sees structured song info. An LLM caller
(or an analysis pipeline) fills this in:

```python
@dataclass
class Song:
    bpm: float
    key: str                    # Camelot code, e.g. "8A"
    energy: float               # 1–10 (bank scale: warm-up 3–6, peak 6±3.5)
    genre: str                  # free label; relations via GENRE_GRAPH
    intro_bars: int = 16        # usable intro length
    outro_bars: int = 16
    has_build: bool = False
    has_breakdown: bool = False
    has_drop: bool = True
    phrase: str = "outro"       # section being mixed FROM (for A):
                                # breakdown|outro|build|drop|verse|chorus
    vocal: str = "none"         # none|background|hook|iconic
    iconic_vocal: bool = False  # signature hook available for T-038/T-025
    stems_available: bool = False
    shared_lyric: str | None = None   # word/phrase shared with the partner
    sample_link: bool = False         # B samples A (or vice versa)
    era: str | None = None
```

From a pair (A outgoing, B incoming) the engine derives `PairFeatures`:
`bpm_delta_pct`, `half_double_ok` (exact 2:1 / 1:2 within 1%),
`camelot_distance` (0 same · 1 ±1/relative · 2–3 · 4+ clash, via the
`harmonic_mix` rule), `energy_delta`, `vocal_pair`
(a_only/b_only/both/neither), `genre_pair` (same/neighbor/leap via
`GENRE_GRAPH`), plus the boolean `needs` flags unioned from both songs.

---

## 5. Selection engine (`engine/select.py`)

```
select(a: Song, b: Song, top_n=5) -> {
  "ranked":   [{"technique": id, "score": float,
                "reasons": [str, ...], "params_hint": {...}}, ...],
  "rejected": {id: "why not", ...},        # every hard-fail, with reason
  "features": PairFeatures,                # what the decision saw
}
```

Algorithm: (1) derive pair features; (2) evaluate every registered
technique's `requires` — failures go to `rejected` with the specific failed
rule; (3) score survivors: base 1.0 + Σ matched `prefers` weights +
family/genre-norm bonus (hip-hop/open-format favors quick cuts & wordplay;
house/techno favors long FREQ blends; DnB/dubstep favors drop collisions —
bank GAPS.md #10); (4) sort, return top N. Deterministic: same input, same
ranking, always.

`techniques.select_technique` (T-037) remains as the legacy hand-tuned
decision table; `select.py` is the registry-driven generalization and must
agree with T-037 on its canonical cases (asserted in the demo suite).

---

## 6. Extension grammar — how hundreds become thousands, mechanically

Four composition operators. Every generated entry is still renderable and
still carries its base technique's evidence (inherited, noted as inherited).

1. **Variant** — a base technique × a named preset on its declared discrete
   parameter axes. ID: `<base>__<preset>` (e.g. `eq_blend__16bar`,
   `echo_out__dotted`). Variants live in `engine/variants.py`'s registry,
   generated from `params` axes in the metadata — never hand-listed.
   Renderable via `variants.render_variant(name, a, b, sr, **ctx)`.
2. **Overlay** — a decoration applied before/after a base render
   (`kind: "overlay"` techniques, e.g. riser ducking under a build).
   Declared as `{"overlay": id, "position": "pre"|"post"}` in a chain spec.
3. **Sequence (chain)** — ordered techniques across a multi-stage move
   (e.g. `screwed_treatment → hook_drop_handoff`). A chain spec is a list of
   `{technique, params}` steps with the rule that each step's exit feeds the
   next step's entrance; chains are SET/STRUCT-level plans, rendered
   step-wise by the caller.
4. **Compound** — a named technique whose implementation *is* a composition
   (family `COMP`, atoms in `composed_of`). Compounds are first-class
   techniques, not variants.

Growth path: base techniques grow by research (bank, gap reports, performer
reverse-engineering, field work); variants grow combinatorially from the
parameter axes; knowledge grows by study. All three are reported separately.

---

## 7. Module contracts (how to add a technique)

New techniques land in **domain modules**, one file per source lane, so work
never collides:

```
engine/<domain>.py        # functions + META dict + TECHNIQUE_FUNCS dict
demos/ext_<domain>.py     # demo_specs(ctx) -> {name: (fn, handoff_fn, allowed_fn)}
techniques/<name>.md      # spec doc, same format as the core specs
```

- `<domain>.py` functions take audio arrays + `sr` (+ `bar_s`/`bpm` as
  needed), return a mono float64 mix array, and carry a full docstring
  (the docstring IS the spec source; the .md mirrors it).
- `META` entries follow §3 exactly, including ≥1 evidence item.
- `demos/ext_<domain>.py` receives `ctx` = {`SR`, `BPM`, `BAR_S`, `BEAT_S`,
  `get_tracks()`, `bars()`, `last_bars()`} from
  `demos/make_demos.py` and returns demo registrations in the core format.
  Demos must pass `verify.verify_clip` (silence/headroom gates) — intentional
  silence is declared via `allowed_fn`, never by weakening the gate.
- `engine/meta.py` and `engine/render.py` auto-merge domain modules
  (try-import); `demos/make_demos.py` auto-merges `ext_*` demo modules.
  Adding a domain = dropping in files, no shared-file edits.
- Stem techniques use the stem-separated sketch tracks in demos:
  `ctx["get_tracks"]()["stemsA"]` / `["stemsB"]` — tracks synthesized as
  separate `drums`/`bass`/`melody`/`vocal` arrays so element-level moves are
  honestly demonstrable on sketch audio.

## 8. Verification gates

1. Every render technique: demo renders + passes silence/headroom gates
   (`demos/out/verification.json` is the receipt).
2. Every decision/planning entry: assertion-checked in the demo suite.
3. `select.py`: self-test must agree with T-037 on canonical cases.
4. Specs: every registry entry has a `techniques/<id>.md` or a
   `knowledge/<id>.md`; every spec names its evidence.
5. Nothing ships without the full suite green: `python3 demos/make_demos.py`.

## 9. Deliberate exclusions (documented, not missing)

- **Toneplay (T-012)** — per-track improvisation; no generalizable recipe
  exists by definition (bank verdict SKIP). Listed in the registry with
  `verdict: SKIP` so selection can explain its absence.
- **Holding-pattern loop** — the bank's T-027 discipline caps transition
  loops at 2 cycles; the indefinite set-tool loop is a SET-level recovery
  plan, documented in `knowledge/`, not a transition technique.
- **Siren/horn (T-036)** — human hype decision with a hard once-per-set
  quota; never auto-deployed. Documented in `knowledge/`.
