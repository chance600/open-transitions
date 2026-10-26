"""open-transitions — characteristic-driven technique selector (D18).

Extends engine/select.py: same registry, same genre graph, same Camelot
ladder — but selection is driven by the two songs' characteristics PLUS
mined fit evidence from the lane's verdict dataset (163 rows), with
three-state gate logic for fields the lane does not yet capture.

Why this module exists instead of editing select.py in place:
select.py assumes a complete Song (bpm, key, energy all present) and
scores registry prefers only. Lane records routinely lack key and energy,
and registry prefers alone bury proven techniques (stem_element_crossfade
has no prefers that fire without a known key/energy, yet it is 2/2 on
keeper pairs). This module (a) treats unknown fields as UNVERIFIED rather
than failing or assuming them, and (b) adds an evidence layer mined from
verdicts. Phase 30 promoted the four keeper shapes (ooh_tail_pickup,
wub_runway, wera_weave, underlap) from gap-flagged custom-shape
recommendations to first-class registry entries (KEEP-01..KEEP-04,
engine/keeper_shapes.py); they now rank in select_fit like any render
technique, and select_fit's "custom_shapes" output is retained empty
for backward compatibility.

Deterministic: same inputs, same ranking. No randomness anywhere.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from . import meta
from .select import (
    _boost_bonus,
    _genre_bonus,
    _score_prefers,
    camelot_distance,
    genre_pair as _genre_pair,
    genre_scene,
    key_move,
)

# ----------------------------------------------------------------------------
# Lane song schema (D18). Every field carries provenance in `prov`:
# "record" (a lane record states it), "inferred" (derived from artist/
# construction records, flagged as such), "unknown" (not captured).
# ----------------------------------------------------------------------------

VOCAL_STATES = ("none", "background", "hook", "iconic", "unknown")
ENTRY_MODES = ("drums_first", "groove", "melody", "vocal", "full", "unknown")


@dataclass
class LaneSong:
    bpm: Optional[float] = None
    genre: str = "unknown"           # scene-level label when known
    key: Optional[str] = None        # Camelot code, e.g. "8A"
    energy: Optional[float] = None   # 1-10 bank scale
    energy_contour: Optional[str] = None  # rise|fall|flat|peak|unknown
    phrase: str = "outro"            # section A is taken from
    vocal: str = "unknown"           # none|background|hook|iconic|unknown
    vocal_detail: Optional[str] = None    # e.g. "short ooh tail", "chant"
    signature_motif: Optional[str] = None  # short distinctive motif usable
                                      # as a device, e.g. "wub loop figure"
    b_entry_mode: str = "unknown"    # how B should enter (D7: drums first)
    b_vocal_in_bridge: Optional[bool] = None  # False = lyrics-out bridge
    # Tri-state on purpose: None = unknown (NOT "unavailable"). A False
    # here gates stem techniques; a None only flags them unverified.
    stems_available: Optional[bool] = None
    intro_bars: Optional[int] = None
    outro_bars: Optional[int] = None
    groove_density: Optional[str] = None  # sparse|driving|dense|syncopated
    era: Optional[str] = None        # release year when known
    iconic_vocal: bool = False
    shared_lyric: Optional[str] = None
    sample_link: bool = False
    anchor_vocal: bool = False
    prov: dict = field(default_factory=dict)


# ----------------------------------------------------------------------------
# Fit evidence mined from mixing-lane/verdict-dataset.jsonl (163 rows).
# Method: rows normalized to (technique family, pair); a pair's terminal
# outcome is POS if any row on that pair is pass/positive/pass-reserve,
# else NEG if its last row is negative/reject/rejected, else OPEN.
# Row counts alone would lie: drum_bridge has 40 rows on 3 pairs (one
# pair iterated 19 times), so the table counts PAIRS, not rows.
# "keeper" = the pair's version-of-record technique (binding verdict).
# ----------------------------------------------------------------------------

FIT_EVIDENCE = {
    "bass_swap": {
        "bank": "T-002", "pairs_tried": 11, "keeper_pairs": 2,
        "negative_pairs": 8, "open_pairs": 1,
        "keeper_rows": [28, 57], "negative_rows": [1, 3, 5, 49, 50, 59, 121, 152, 161],
        "fit": "kick-driven handover where A holds an energy floor; won on "
               "blend02 (O'Flynn -> What A Life) and setlink04 (Kombucha -> "
               "Lifetime, with a stem vocal return).",
        "anti": "8 first-try NEGs on pairs that later settled on other techniques "
                "(setlink02/03/06/08/10, setlink12, setlink29). Evidence "
                "AGAINST bass_swap as a default: it is a probe, not a plan.",
    },
    "eq_blend": {
        "bank": "T-001", "pairs_tried": 6, "keeper_pairs": 3,
        "negative_pairs": 1, "open_pairs": 2,
        "keeper_rows": [29, 51, 150], "negative_rows": [52],
        "fit": "Delta~0% + same/neighbor genre (setlink09, blend03), OR a wide "
               "gap handled by slowing A + a lyrics-out bridge (setlink21: "
               "130->119, -8.5%, B vocal stem absent from the bridge).",
        "anti": "setlink07 v1 (frequency replacement) NEG; the pair settled on "
                "stem_element_crossfade instead.",
    },
    "drum_bridge": {
        "bank": "T-022", "pairs_tried": 3, "keeper_pairs": 2,
        "negative_pairs": 0, "open_pairs": 1,
        "keeper_rows": [125, 140], "negative_rows": [],
        "fit": "B's groove/drum identity is the feature (D7 drums-first). Both "
               "keepers sit at Delta~-4.5% (setlink10 123->117.5, setlink11 "
               "123->117.5). The setlink06 drum line went OPEN/superseded "
               "by wub_runway, not negative.",
        "anti": "none recorded.",
    },
    "stem_element_crossfade": {
        "bank": "GAP-08", "pairs_tried": 2, "keeper_pairs": 2,
        "negative_pairs": 0, "open_pairs": 0,
        "keeper_rows": [53, 60], "negative_rows": [],
        "fit": "Delta~0% + same/neighbor genre + stems available (setlink07, "
               "setlink08). Clean but THIN: n=2 pairs.",
        "anti": "none recorded.",
    },
    "underlap": {
        "bank": "KEEP-02", "pairs_tried": 1, "keeper_pairs": 1,
        "negative_pairs": 0, "open_pairs": 0,
        "keeper_rows": [76, 94], "negative_rows": [],
        "fit": "B slow emergence + muted chant over a long tide (setlink03, "
               "117.5->124, +5.5%). Registry entry since Phase 30.",
        "anti": "none recorded.",
    },
    "wub_runway": {
        "bank": "KEEP-03", "pairs_tried": 1, "keeper_pairs": 1,
        "negative_pairs": 0, "open_pairs": 0,
        "keeper_rows": [103, 120], "negative_rows": [],
        "fit": "B enters on its signature melodic figure with drums excluded "
               "and A easing out across a runway (setlink06, Delta 0%). "
               "Registry entry since Phase 30.",
        "anti": "none recorded.",
    },
    "wera_weave": {
        "bank": "KEEP-04", "pairs_tried": 1, "keeper_pairs": 1,
        "negative_pairs": 0, "open_pairs": 0,
        "keeper_rows": [93], "negative_rows": [],
        "fit": "A hook-vocal leads over a zone-fitted B (setlink10, 123->117.5). "
               "Registry entry since Phase 30.",
        "anti": "none recorded.",
    },
    "ooh_tail_pickup": {
        "bank": "KEEP-01", "pairs_tried": 1, "keeper_pairs": 1,
        "negative_pairs": 0, "open_pairs": 0,
        "keeper_rows": [39], "negative_rows": [],
        "fit": "A has a short distinctive vocal tail motif picked up as the "
               "device (setlink02, 123->117.5). Registry entry since "
               "Phase 30.",
        "anti": "none recorded.",
    },
    "hook_drop_handoff": {
        "bank": "T-038", "pairs_tried": 1, "keeper_pairs": 1,
        "negative_pairs": 0, "open_pairs": 0,
        "keeper_rows": [19, 20, 22, 25, 27], "negative_rows": [],
        "fit": "A iconic hook -> B drop across a genre leap (blend01, rap -> "
               "house). One pair, 19 rows, 5 keepers.",
        "anti": "none recorded.",
    },
    "reverb_wash": {
        "bank": "T-005", "pairs_tried": 1, "keeper_pairs": 0,
        "negative_pairs": 0, "open_pairs": 1,
        "keeper_rows": [], "negative_rows": [],
        "fit": "Positive-leaning on setlink02 (rows 4, 31) but SUPERSEDED by "
               "ooh_tail_pickup v4 — not keeper evidence.",
        "anti": "none recorded.",
    },
    "genre_bridge": {
        "bank": "T-026", "pairs_tried": 2, "keeper_pairs": 0,
        "negative_pairs": 2, "open_pairs": 0,
        "keeper_rows": [], "negative_rows": [153, 162],
        "fit": "NO CLEAN TRIALS. Both NEGs are identity-confounded: row 153 "
               "(Juicy file, not Luna) and row 162 (Ibeyi file, not "
               "Korolova). Zero usable technique evidence either way.",
        "anti": "none usable (see fit).",
    },
    "loop_roll_build": {
        "bank": "T-008", "pairs_tried": 1, "keeper_pairs": 0,
        "negative_pairs": 1, "open_pairs": 0,
        "keeper_rows": [], "negative_rows": [154, 155, 156, 157, 158],
        "fit": "none recorded.",
        "anti": "SCOPED negative: vocal-loop device hated on setlink05's "
               "lyric-forward bridge (placement fault + device hate). "
               "Lane scope is that bridge, not all loop-rolls.",
    },
    "hard_cut": {
        "bank": "T-030", "pairs_tried": 1, "keeper_pairs": 0,
        "negative_pairs": 1, "open_pairs": 0,
        "keeper_rows": [], "negative_rows": [38, 42, 45, 46, 122],
        "fit": "none recorded.",
        "anti": "Technique class rejected on setlink04 (link 5b); the pair "
               "itself was NOT killed and continued as eq_blend.",
    },
    "echo_out": {
        "bank": "T-004", "pairs_tried": 1, "keeper_pairs": 0,
        "negative_pairs": 1, "open_pairs": 0,
        "keeper_rows": [], "negative_rows": [37],
        "fit": "none recorded.",
        "anti": "one early NEG on setlink04 (link 5b).",
    },
    "filter_sweep": {
        "bank": "T-003", "pairs_tried": 1, "keeper_pairs": 0,
        "negative_pairs": 1, "open_pairs": 0,
        "keeper_rows": [], "negative_rows": [2],
        "fit": "none recorded.",
        "anti": "one NEG on setlink01 (fit-doubted pair).",
    },
    "tempo_bridge": {
        "bank": "T-021", "pairs_tried": 1, "keeper_pairs": 0,
        "negative_pairs": 1, "open_pairs": 0,
        "keeper_rows": [], "negative_rows": [163],
        "fit": "none recorded.",
        "anti": "one NEG: stale pre-doctrine sweep render (idea37).",
    },
    "rhythmic_fader_chops": {
        "bank": "GAP-15", "pairs_tried": 1, "keeper_pairs": 0,
        "negative_pairs": 0, "open_pairs": 1,
        "keeper_rows": [], "negative_rows": [],
        "fit": "setlink03 choppy line closed at v14c as standing best "
               "PARTIAL, never a keeper.",
        "anti": "none terminal.",
    },
    "layered_emergence": {
        "bank": "T-004c", "pairs_tried": 1, "keeper_pairs": 0,
        "negative_pairs": 1, "open_pairs": 0,
        "keeper_rows": [], "negative_rows": [62, 65],
        "fit": "none recorded.",
        "anti": "early NEGs on setlink06; the pair settled on wub_runway.",
    },
}

# Custom shapes, retired in Phase 30: the four keeper shapes above are
# now registry entries (KEEP-01..KEEP-04) and rank in select_fit through
# the normal path. The "custom_shapes" key is kept in select_fit's
# output, empty, so existing callers (including the backtest's custom
# branch) keep working without a special case.
CUSTOM_SHAPES = {}


# ----------------------------------------------------------------------------
# Pair features (three-state: None/unknown means "gate skipped, flagged")
# ----------------------------------------------------------------------------

def _vocal_pair(a: LaneSong, b: LaneSong) -> str:
    if a.vocal == "unknown" or b.vocal == "unknown":
        return "unknown"
    va, vb = a.vocal != "none", b.vocal != "none"
    if va and vb:
        return "both"
    if va:
        return "a_only"
    if vb:
        return "b_only"
    return "neither"


def derive_lane_features(a: LaneSong, b: LaneSong) -> dict:
    if a.bpm and b.bpm:
        bpm_delta_pct = abs(b.bpm - a.bpm) / a.bpm * 100.0
        ratio = b.bpm / a.bpm
    else:
        bpm_delta_pct, ratio = None, None
    half_double_ok = ratio is not None and (
        abs(ratio - 2.0) < 0.01 or abs(ratio - 0.5) < 0.01)
    if a.key and b.key:
        cam = camelot_distance(a.key, b.key)
        km = key_move(a.key, b.key)
    else:
        cam, km = None, None
    if a.energy is not None and b.energy is not None:
        dE = b.energy - a.energy
    else:
        dE = None
    gp = "unknown" if a.genre == "unknown" or b.genre == "unknown" \
        else _genre_pair(a.genre, b.genre)
    return {
        "bpm_delta_pct": bpm_delta_pct,
        "bpm_ratio": ratio,
        "half_double_ok": half_double_ok,
        "camelot": cam,
        "key_move": km,
        "key_verified": cam is not None,
        "energy_delta": dE,
        "energy_delta_abs": abs(dE) if dE is not None else None,
        "energy_a": a.energy, "energy_b": b.energy,
        "energy_verified": dE is not None,
        "phrase_a": a.phrase,
        "vocal_pair": _vocal_pair(a, b),
        "genre_pair": gp,
        "genre_a": a.genre, "genre_b": b.genre,
        "scene_a": genre_scene(a.genre) if a.genre != "unknown" else None,
        "scene_b": genre_scene(b.genre) if b.genre != "unknown" else None,
        "b_intro_bars": b.intro_bars,
        "iconic_a": a.iconic_vocal,
        "a_breakdown": False, "b_build": False,
        # Tri-state: True only if both known-True; False if either
        # known-False; None if unknown on either side.
        "stems": (True if (a.stems_available and b.stems_available)
                 else (False if (a.stems_available is False
                                 or b.stems_available is False)
                       else None)),
        "shared_lyric": bool(a.shared_lyric or b.shared_lyric),
        "sample_link": a.sample_link or b.sample_link,
        "anchor_vocal": a.anchor_vocal or b.anchor_vocal,
        "drop_pair": False, "glue": False, "third_deck": False,
        "b_vocal_in_bridge": b.b_vocal_in_bridge,
        "a_vocal_detail": a.vocal_detail, "b_vocal_detail": b.vocal_detail,
        "a_motif": a.signature_motif, "b_motif": b.signature_motif,
        "b_entry_mode": b.b_entry_mode,
        "energy_boost": (km in (1, 2) and dE is not None and dE >= 0),
    }


# ----------------------------------------------------------------------------
# Three-state requires evaluation
# ----------------------------------------------------------------------------

def _eval_requires_lane(req: dict, f: dict):
    """Returns (status, reason): status in {'pass','gated','unverified'}.
    ALL gates are evaluated (a first-unverified-gate early return would
    hide a later KNOWN failure — fixed 2026-10-25 when it masked a
    missing-stems gate behind an unknown-key gate on link5). Precedence:
    any known-field failure -> 'gated'; else any unknown-field gate ->
    'unverified'; else 'pass'."""
    if not req:
        return "pass", None
    failed, unverified = [], []
    bmax = req.get("bpm_delta_pct_max")
    if bmax is not None:
        if f["bpm_delta_pct"] is None:
            unverified.append("BPM delta unknown — bpm gate skipped")
        elif f["bpm_delta_pct"] > bmax:
            failed.append(f"BPM delta {f['bpm_delta_pct']:.1f}% > {bmax}% max")
    cmax = req.get("camelot_max")
    if cmax is not None:
        if f["camelot"] is None:
            unverified.append("key unknown — camelot gate skipped")
        elif f["camelot"] > cmax:
            failed.append(f"Camelot distance {f['camelot']} > {cmax} max "
                          f"— keys would clash under a blend")
    vocal_ok = req.get("vocal_ok")
    if vocal_ok is not None:
        if f["vocal_pair"] == "unknown":
            unverified.append("vocal state unknown — vocal gate skipped")
        elif f["vocal_pair"] not in vocal_ok:
            failed.append(f"vocal state '{f['vocal_pair']}' not allowed here")
    phrase_ok = req.get("phrase_a_ok")
    if phrase_ok is not None and f["phrase_a"] not in phrase_ok:
        failed.append(f"A is in '{f['phrase_a']}' — wrong section for this move")
    gp_ok = req.get("genre_pair_ok")
    if gp_ok is not None:
        if f["genre_pair"] == "unknown":
            unverified.append("genre unknown — genre gate skipped")
        elif f["genre_pair"] not in gp_ok:
            failed.append(f"genre pair '{f['genre_pair']}' too far for this move")
    for need in req.get("needs", []):
        val = f.get(need)
        if val is False:
            failed.append(f"missing required context: '{need}'")
        elif val is None:
            unverified.append(f"required context unknown: '{need}'")
    if failed:
        return "gated", "; ".join(failed)
    if unverified:
        return "unverified", "; ".join(unverified)
    return "pass", None


# ----------------------------------------------------------------------------
# Evidence adjustment
# ----------------------------------------------------------------------------

def _evidence_adjustment(tid: str, f: dict) -> tuple:
    """Returns (points, [reason strings], [flags]). Conservative by
    design: keeper-rate bonuses are small, thin evidence is flagged,
    and negative matching uses coarse buckets only."""
    ev = FIT_EVIDENCE.get(tid)
    if not ev:
        return 0.0, [], ["no lane evidence — registry reasoning only"]
    pts, reasons, flags = 0.0, [], []
    tried, keepers = ev["pairs_tried"], ev["keeper_pairs"]
    if keepers:
        rate = keepers / tried
        if tried >= 2:
            pts += 2.0 * rate
            reasons.append(f"lane evidence: {keepers}/{tried} pairs kept "
                           f"(rows {ev['keeper_rows']})")
        else:
            pts += 1.0
            reasons.append(f"lane evidence (THIN n=1): keeper on "
                           f"{keepers}/{tried} pair (rows {ev['keeper_rows']})")
            flags.append("thin evidence n=1")
    if ev["negative_pairs"] and tid == "bass_swap":
        # The lane's most repeated lesson, stated as a reason but NOT
        # double-counted in points: the 8 first-try NEGs already dilute
        # the keeper rate above (2/11). Subtracting again would punish
        # the same history twice (fixed 2026-10-25 after the backtest
        # showed bass_swap buried at rank 20 on both its keeper pairs).
        reasons.append("lane evidence: 8 first-try NEGs on pairs that "
                       "settled elsewhere — never the default (rows "
                       f"{ev['negative_rows']})")
    if tid == "genre_bridge":
        flags.append("no clean trials — both NEGs identity-confounded "
                     "(rows 153, 162); rank rests on registry gates only")
    # Mined feature-fit bonuses (keeper signatures, coarse buckets).
    d = f["bpm_delta_pct"]
    if tid == "drum_bridge":
        if f["b_entry_mode"] == "drums_first":
            pts += 2.0
            reasons.append("fit: B enters drums-first (D7) — both "
                           "drum_bridge keepers share this")
        elif d is not None and 3.0 <= d <= 6.0:
            pts += 1.0
            reasons.append("fit: BPM gap 3-6% matches both drum_bridge "
                           "keepers (-4.4%, -4.5%)")
    if tid == "eq_blend":
        if d is not None and d <= 1.0 and f["genre_pair"] in ("same", "neighbor"):
            pts += 2.0
            reasons.append("fit: Delta~0% + same/neighbor genre — "
                           "eq_blend keeper signature (rows 29, 51)")
        if f["b_vocal_in_bridge"] is False and d is not None and d >= 8.0:
            pts += 1.5
            reasons.append("fit: wide gap + lyrics-out bridge — setlink21 "
                           "keeper pattern (row 150)")
    if tid == "stem_element_crossfade":
        if f["stems"] and d is not None and d <= 3.0 \
                and f["genre_pair"] in ("same", "neighbor"):
            pts += 2.0
            reasons.append("fit: stems + Delta<=3% + same/neighbor — "
                           "stem_element_crossfade keeper signature "
                           "(rows 53, 60)")
    if tid == "hook_drop_handoff":
        if f["iconic_a"] and f["genre_pair"] == "leap":
            pts += 1.0
            reasons.append("fit: iconic A hook across a genre leap — "
                           "blend01 keeper pattern")
    # Keeper-shape motif-role disambiguation (Phase 30): ooh_tail_pickup
    # and wera_weave both key on "A hook vocal" in the abstract, but
    # they are different devices — a short tail fragment picked up
    # vs a lead line woven over B's groove. Where the profile states
    # the role in vocal_detail, only the matching shape earns this
    # bonus; where it does not, both rank on the motif prefers and
    # the overlap is flagged by the caller, not papered over.
    a_det = (f.get("a_vocal_detail") or "").lower()
    b_det = (f.get("b_vocal_detail") or "").lower()
    if tid == "ooh_tail_pickup" and "tail" in a_det:
        pts += 1.0
        reasons.append("fit: motif-role is a tail fragment "
                       "(vocal_detail) — the pickup device, not a lead")
    if tid == "wera_weave" and "hook" in a_det:
        pts += 1.0
        reasons.append("fit: motif-role is a lead hook line "
                       "(vocal_detail) — the weave device, not a tail")
    if tid == "underlap" and "mut" in b_det:
        pts += 1.0
        reasons.append("fit: B vocal muted for the entry bars "
                       "(vocal_detail) — the underlap signature")
    if tid == "wub_runway" and f.get("b_motif") \
            and f.get("b_entry_mode") in ("groove", "melody"):
        pts += 1.0
        reasons.append("fit: B signature figure carries the entrance "
                       "with drums excluded — the runway staging")
    return pts, reasons, flags


def _custom_shape_hits(a: LaneSong, b: LaneSong) -> list:
    """Retired in Phase 30 — the keeper shapes now rank, not fire.

    Kept as a function (returning no hits) so select_fit's output
    shape is unchanged for existing callers.
    """
    return []


# ----------------------------------------------------------------------------
# Main entry point
# ----------------------------------------------------------------------------

def select_fit(a: LaneSong, b: LaneSong, top_n: int = 5) -> dict:
    f = derive_lane_features(a, b)
    registry = meta.all_meta()
    ranked, gated, unverified = [], {}, {}
    for tid, entry in registry.items():
        if entry.get("kind") not in ("render", "decision"):
            continue
        if tid in ("select_technique", "beat_jump", "harmonic_mix"):
            continue
        status, why = _eval_requires_lane(entry.get("requires", {}), f)
        if status == "gated":
            gated[tid] = why
            continue
        pts, reasons = _score_prefers(entry.get("prefers", []), f)
        bpts, breasons = _genre_bonus(tid, entry, f)
        xpts, xreasons = _boost_bonus(tid, entry, f)
        epts, ereasons, eflags = _evidence_adjustment(tid, f)
        total = 1.0 + pts + bpts + xpts + epts
        flags = list(eflags)
        if status == "unverified":
            unverified[tid] = why
            flags.append("unverified gate: " + why)
        ranked.append({"technique": tid, "score": round(total, 2),
                       "reasons": reasons + breasons + xreasons + ereasons,
                       "flags": flags,
                       "bank": entry.get("bank"),
                       "energy": entry.get("energy"),
                       "exit": entry.get("exit")})
    # Tie-break: equal scores rank techniques WITH lane evidence above
    # techniques with none (a generic genre-bonus-only technique must
    # not outrank a technique with actual keeper evidence), then
    # alphabetically. Deterministic.
    ranked.sort(key=lambda r: (-r["score"],
                               0 if r["technique"] in FIT_EVIDENCE else 1,
                               r["technique"]))
    return {"ranked": ranked[:top_n], "ranked_all": ranked,
            "gated": gated, "unverified": unverified,
            "custom_shapes": _custom_shape_hits(a, b),
            "features": f}
