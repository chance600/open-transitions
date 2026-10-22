# ENUMERATION — Phase 24 combinatorial pass (Class 3)

The enumeration record for the V2 queue item 3:
Class 3's full axis walk across the registry's
bases + cross-base pairwise compounds and
sequences, deduped at the registry's admission
bar (FRAMEWORK.md §6). This file is the audit
trail: every cell of the walked space is
counted in exactly one bucket, with the rule
that put it there stated. Numbers are
recounted from artifacts at phase close; the
generator and catalog are `engine/variants.py`
and `VARIANTS.md`.

## Method (fixed before counting)

**Part A — axis walk (variants).** For every
base with ≥1 declared preset axis (the
`"presets"` maps in `params`, FRAMEWORK §3):
singles = every preset on every axis; pairs =
every preset combination on every axis pair.
A candidate's natural id follows the standing
scheme (`<base>__<preset>`,
`<base>__<p1>_<p2>`, presets in axis
declaration order). Admission rules, applied
in order:

1. **Nameability.** The id must denote exactly
   one parameter set — across the candidate
   space and the existing registry. Preset
   vocabularies repeat across axes ("one",
   "low", "short"…), so beyond the first two
   axes the scheme collides; colliding cells
   are rejected and counted, not renamed
   (a scheme change is a framework decision,
   recorded as white space, not improvised
   mid-tranche).
2. **Effectiveness.** Every axis a candidate
   sets must be consumed by the base's render
   path (checked against the function; an
   unconsumed axis makes the candidate
   render-identical to its other leg).
3. **Audible distinction (new admissions).**
   A pair with a default-valued leg renders
   identically to that leg's single; a single
   whose value is the default renders as the
   base. Such cells are render-duplicates —
   parameter notes, not variants (Class 3:
   "only pairs that change something audible
   count"). The legacy surface (first-axis
   singles + first-two-axes pairs under the
   cap) predates this bar and is NOT delisted;
   the asymmetry is deliberate and stated
   here, not hidden.
4. **Axis-pair coherence (judgment).** Each
   surviving (base, axis-pair) is read by
   hand: two axes that are one dimension
   declared twice, or whose presets
   contradict, are rejected with the reason
   recorded per pair.

**Part B — cross-base compounds + sequences.**
Unordered pairs of render bases (compounds,
§6 operator 4) and ordered pairs (sequences,
§6 operator 3), classified by rules over the
registry's own fields (family, kind, exit,
clash_risk, composed_of) before any hand
judgment; the surviving shortlist is judged
per pair at the admission bar: a compound
earns a base only if it is a distinct
mechanism a DJ would name and reuse.
Sequences whose composition is "do X, then
Y" with no fusion bank as knowledge with
their composition stated, per the phase
brief.

## Part A — axis walk: accounting

Cells walked: **1,181** (313 singles + 868
pairs) across the 59 bases that declare preset
axes (87 registry bases; 28 declare none).
Meta-declared defaults were verified equal to
the render functions' own defaults for every
axis (0 mismatches) before any default-based
rule was applied.

| Bucket | Singles | Pairs | Total |
|---|---|---|---|
| Already registered (legacy surface) | 175 | 199 | 374 |
| Rejected — id taken in registry, different params | 2 | 30 | 32 |
| Rejected — id ambiguous in the candidate space | 19 | 163 | 182 |
| Rejected — default-valued single (renders as the base) | 31 | — | 31 |
| Rejected — pair with a default leg (renders as that leg's single) | — | 203 | 203 |
| Rejected — aliased preset value | 1 | 0 | 1 |
| Rejected — conditionally inert leg (at validation) | — | 7 | 7 |
| Rejected — incoherent axis pair (judgment) | — | 0 | 0 |
| **Admitted** | **85** | **266** | **351** |

**Nameability is the walk's binding
constraint** (214 cells): preset vocabularies
repeat across axes (`one`, `low`, `short`,
`standard`…), and the standing id scheme does
not say which axis a preset belongs to. Past
the first two axes the scheme cannot name
what the mechanisms can do — counted here as
rejections, proposed as a scheme question in
the white space, not improvised around.

**Effectiveness, measured not assumed.** Every
axis appearing in an admitted candidate (61)
was render-tested on the sketch tracks: two
preset values at the default background (and a
second background where the first read
inert). 60 axes change the render outright.
One finding: `brake_stop`'s `curve` axis is
effective (exp ≠ linear) but its `s_curve`
preset maps to the value `"s"`, which
`dsp.pitch_dive` does not implement — it
falls through to the linear branch, so
`brake_stop__s_curve` would render identically
to `brake_stop__linear` and is rejected as an
alias. (The legacy registry already carries
`*_s_curve` pairs from the first-two-axes
surface; they stand as history, and the
aliasing is recorded here and in the white
space.) A second scare — `drop_chop`'s
`rounds` x2 ≡ x4 — proved to be a harness
artifact (8-bar test segments are too short
for four rounds to fit); at 16 bars the
values differ, and the axis stands.

**Coherence judgment.** The 273 pairs that
passed the mechanical filters fall in 72
(base, axis-pair) groups;
each was read by hand. All couple independent
audible dimensions (voicing × register,
pattern × length, sweep-start × sweep-end,
density × staging…). The two hardest calls:
ring-mod's carrier start × end (endpoints of
one sweep — independent coordinates, a pair
names a sweep *shape* neither single can);
resonator decay × zone length (the source's
ring constant vs the excitation window —
different controls, set independently in
performance). Zero groups rejected: the
mechanical filters had already removed the
junk, and the module authors declared their
axes as independent dimensions.

Admitted shape: singles land on axes 2–7
(43 / 24 / 7 / 6 / 4 / 2 by axis index);
pairs land on every axis pair — 9 are
beyond-cap combos of the legacy (1,2) pair,
264 are on axis pairs the old generator
never walked. The generator
(`engine/variants.py`) now implements
exactly this bar: the legacy surface is
generated as before and never delisted;
expansion candidates are admitted only
under rules 1–4 above, computed over the
full candidate space so the registry and
this record agree by construction.

**Render validation.** Every admitted
variant was rendered on sketch segments
(8 bars; 16 for `drop_chop`, whose rounds
axis needs the length) and checked three
ways: it differs from its base's default
render; a pair differs from each of its
constituent singles; no two new variants of
one base render identically. 375 renders
checked (the 358 pre-validation admissions
+ the new base's 17). 32 identity flags,
two root causes:

1. `aging_echo`'s own axes named their
defaults (`half`, `standard`) — the legacy
surface convention, harmless on
grandfathered bases, wrong for a base born
under this bar. Fixed at the source: its
preset maps no longer name defaults, and
the base carries 11 variants, all distinct.
2. `fader_synth`'s `scale` axis is
conditionally inert: the glide and hold
rides never read it, and the arp ride reads
only degrees 0/2/4 — where the minor and
harmonic-minor tables agree (they differ at
degree 6). 7 pairs rejected here (counted
in the table above) and encoded in the
generator's measured `_CONDITIONAL_INERT`
table. The scale singles stand — under the
default steps ride every degree sounds.

Post-fix, the affected bases re-validated:
67 variants, 0 problems. Scope note,
stated plainly: the checks compare against
the base default, the constituent singles
and same-base siblings; a new pair
rendering identically to an unrelated
legacy variant on a third axis was not
searched for — no evidence of that class
appeared anywhere in the pass.

## Part B — compounds + sequences: accounting

Compound space: **3,003** unordered pairs of
the 78 render bases. (Outside the space: the
5 overlay-kind bases pair with every render
base through §6 operator 2 — 390 applications,
expressible today, no bases; the 4
decision/planning entries render nothing —
318 pairs excluded.)

| Bucket | Pairs |
|---|---|
| Already a base (an entry's `composed_of` covers the pair) | 40 |
| Same-family role collision | 371 |
| Clash collision (both claim bass / vocal / key at full level) | 83 |
| Event × event (drop family — sequence-class, below) | 8 |
| Dual architecture (two seam-owning stagings = a plan, not a move) | 158 |
| Requires conjunction empty (vocal / phrase / genre windows disjoint) | 158 |
| Survived structure — failed the naming bar (below) | 2,185 |

The 2,185 by what they actually are:
**1,912 additive** (the two mechanisms run in
parallel with no interaction term — the
layered-stack and overlay machinery already
expresses them), **196 stem-scoped** (a
process applied to one stem of a routing
base — the FX-scope axis banked on GAP-08 in
Phase 13), **69 FX-return** (a tail's output
processed — gated / ducked / filtered /
morphed return; banked as one knowledge
entry with its instances), **8
gesture-trigger** (a scratch / spin / brake /
flourish gesture firing an echo tail —
already dispositioned at knowledge weight by
the bank: Pioneer's Smooth Echo operator
note and Engine's Fader Echo, "the exit
gesture fires the tail"; not re-litigated).

**One new base: `aging_echo`.** Its atom pair
(echo_out × filter) already exists — as
*parallel* atoms inside `layered_fx_stack`
and `layered_emergence`, where the filter
sweeps the mix and the repeats stay bright.
The built mechanism is the other topology:
the lowpass sits *inside* the feedback loop,
so repeat k is filtered k times and the tail
audibly ages — the dub tradition's delay,
measurable as descending repeat spectra, and
absent from the engine (`dsp.feedback_delay`
is a pure geometric series; every repeat is
an equally bright copy). The precedent is
the registry's own: `spiral_echo` earned its
base for putting pitch inside the same loop.
The vendor name "Dub Echo" was resolved
three times in the bank as a *knob form* of
T-004; this build is the tradition mechanism
that name points at, named for the mechanism
so the two records don't collide.

Sequences: **6,006** ordered pairs under
same-seam scoping (the second move begins
inside the first's exit gesture; exit/entry
compatibility from `exit` and entry class) —
5,227 compatible, 779 incompatible. The
compatible mass is ordinary set-scale
succession, not seam craft. Six chains pass
the naming bar and bank as knowledge with
their compositions stated: spinback →
drop-swap, brake → drop, echo → rewind,
tease → bass-swap, fake-out → double-drop,
tighten → swap.

**Against the Class 3 estimate** (40–80
compound bases): the bar returned 1. The
reason is in the buckets — 23 phases had
already mined the fusion grammar's named
instances (28 `composed_of` relations stand
in the registry), and the pair space over
the *existing* atoms is overwhelmingly
additive. The compound frontier is not a
pair-enumeration problem; it moves when new
atoms arrive (Classes 1, 2, 5), not when old
atoms are re-paired. Recorded as a
correction to the map's arithmetic, in the
open.

## Close-out — counts after this pass

Recounted from artifacts: registry **88**
bases (79 render / 5 overlay / 3 decision /
1 planning; 87 executable; 72
plan-renderable by the render module's
function registry), variants **736 across
60 bases** (374 legacy + 351 admitted here
+ 11 on the new base), knowledge **138**,
verdicts ADOPT 60 / ADAPT 28, demos 114/114
verified clean (the new base's demo among
them). The enumeration space was bounded by
the registry's current axis definitions and
the 87 bases that existed when the walk
began — that bound is the finding the white
space below is about.

## WHITE SPACE — what the enumeration
revealed that neither map names

1. **The namespace is smaller than the
mechanism space.** 214 walked cells are
real, distinct stagings the standing id
scheme cannot name (it does not say which
axis a preset belongs to, and preset
vocabularies repeat across axes). An
axis-qualified id scheme (`base__axis:preset`)
would unlock them; it is a framework
decision, not an enumeration fix, and no
ids were improvised here.
2. **Axes are not always independent.**
`fader_synth`'s scale is conditionally
inert — read only under some values of the
ride axis. The meta schema has no way to
declare applicability ("axis B applies
only when axis A ∈ {…}"), so conditional
structure is currently discoverable only
by rendering. A schema field for it
belongs to a future framework pass.
3. **An engine gap found by enumeration,
not mining:** `dsp.pitch_dive` has no true
S-curve, so the legacy `brake_stop`
`*_s_curve` pairs render as their
`*_linear` siblings. Implementing the
curve changes shipped renders — a
deliberate future fix, flagged, not done.
4. **The compound frontier is atom-bound.**
Part B's correction generalizes: pairwise
enumeration over existing atoms yields
addition, not interaction. The next
compounds will arrive WITH new atoms —
Class 5's macro/chain systems (Metaknob,
Hex dial, chain FX) are interaction-rich
by design and are the frontier's likely
source.
5. **Chains lack a selection layer.** The
sequence graph says ~87% of ordered pairs
are mechanically compatible — what binds
real chains is dramaturgy (energy,
attention), and `select.py` scores single
techniques only. A chain scorer is
unbuilt, unnamed work.
6. **Genre is not an axis.** Class 3's
step 5 (genre re-stagings) could not be
walked as combinatorics: genre lives in
`requires` windows, not preset axes. Until
genre is a declared axis, re-stagings are
reachable only by mining (Class 2), never
by enumeration.
7. **Distinctness is length-relative.** The
`drop_chop` rounds lesson (x2 ≡ x4 at 8
bars, distinct at 16) means every
render-equality claim in this record is
scoped to its test length; performance-
length spot checks on high-axis bases are
owed before any variant drives a real set
decision.
