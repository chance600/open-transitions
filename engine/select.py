"""open-transitions — selection engine v1 (FRAMEWORK.md §5).

Takes structured info about two songs (outgoing A, incoming B) and returns
ranked candidate techniques with scores + reasons, plus a "why not" list of
every rejected technique and the failed rule. Deterministic: same input,
same ranking, always.

Supersedes techniques.select_technique (T-037) as the primary selector;
agreement with T-037's canonical cases is asserted in check_select().
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from . import meta


# ----------------------------------------------------------------------------
# Song schema (FRAMEWORK.md §4)
# ----------------------------------------------------------------------------

@dataclass
class Song:
    bpm: float
    key: str                      # Camelot code, e.g. "8A"
    energy: float                 # 1–10 bank scale
    genre: str                    # free label
    intro_bars: int = 16
    outro_bars: int = 16
    has_build: bool = False
    has_breakdown: bool = False
    has_drop: bool = True
    phrase: str = "outro"         # breakdown|outro|build|drop|verse|chorus
    vocal: str = "none"           # none|background|hook|iconic
    iconic_vocal: bool = False
    stems_available: bool = False
    shared_lyric: Optional[str] = None
    sample_link: bool = False
    flags: dict = field(default_factory=dict)   # ad-hoc ctx: drop_pair,
                                                # glue, third_deck,
                                                # anchor_vocal, ...


# ----------------------------------------------------------------------------
# Genre graph (bank GAPS.md #10 — genre norms steer scoring)
# ----------------------------------------------------------------------------

_GENRE_SCENES = {
    "house": {"house", "tech house", "deep house", "melodic house",
              "progressive house", "edm", "techno", "afro house"},
    "hiphop": {"hip-hop", "hiphop", "rap", "trap", "drill", "rnb"},
    "bass": {"dubstep", "dnb", "drum and bass", "uk garage", "garage",
             "bassline", "bass music"},
    "trance": {"trance", "big room", "hardstyle"},
    "pop": {"pop", "dance pop", "indie", "indie dance", "disco"},
    "openformat": {"open format", "top 40", "mashup"},
}


def _norm_genre(g: str) -> str:
    g = (g or "").strip().lower()
    return g


def genre_pair(ga: str, gb: str) -> str:
    ga, gb = _norm_genre(ga), _norm_genre(gb)
    if ga == gb:
        return "same"
    for scene, members in _GENRE_SCENES.items():
        if ga in members and gb in members:
            return "same"
    # the dominant open-format pairing is treated as adjacent, not a leap
    scenes_a = {s for s, m in _GENRE_SCENES.items() if ga in m}
    scenes_b = {s for s, m in _GENRE_SCENES.items() if gb in m}
    if scenes_a and scenes_b:
        if scenes_a & scenes_b:
            return "neighbor"
        if {("house", "hiphop"), ("hiphop", "house")} and (
                (scenes_a == {"house"} and scenes_b == {"hiphop"})
                or (scenes_a == {"hiphop"} and scenes_b == {"house"})):
            return "neighbor"
        if (("openformat" in scenes_a) or ("openformat" in scenes_b)):
            return "neighbor"
    return "leap"


def genre_scene(g: str) -> Optional[str]:
    g = _norm_genre(g)
    for scene, members in _GENRE_SCENES.items():
        if g in members:
            return scene
    return None


# ----------------------------------------------------------------------------
# Camelot distance (T-037 ladder: 0 same · 1 ±1/relative · 2–3 · 4+ clash)
# ----------------------------------------------------------------------------

def camelot_distance(ka: str, kb: str) -> int:
    def parse(k):
        k = k.strip().upper()
        return int(k[:-1]), k[-1]

    na, la = parse(ka)
    nb, lb = parse(kb)
    if na == nb and la == lb:
        return 0
    if na == nb:
        return 1  # relative major/minor
    step = min((nb - na) % 12, (na - nb) % 12)
    if la != lb:
        return 4  # different mode at a different wheel position — clash-prone
    return min(step, 4)


# ----------------------------------------------------------------------------
# Pair features
# ----------------------------------------------------------------------------

def _vocal_pair(a: Song, b: Song) -> str:
    va = a.vocal != "none"
    vb = b.vocal != "none"
    if va and vb:
        return "both"
    if va:
        return "a_only"
    if vb:
        return "b_only"
    return "neither"


def derive_features(a: Song, b: Song) -> dict:
    bpm_delta_pct = abs(b.bpm - a.bpm) / a.bpm * 100.0 if a.bpm else 0.0
    ratio = b.bpm / a.bpm if a.bpm else 1.0
    half_double_ok = abs(ratio - 2.0) < 0.01 or abs(ratio - 0.5) < 0.01
    dE = b.energy - a.energy
    feats = {
        "bpm_delta_pct": bpm_delta_pct,
        "half_double_ok": half_double_ok,
        "camelot": camelot_distance(a.key, b.key),
        "energy_delta": dE,
        "energy_delta_abs": abs(dE),
        "energy_a": a.energy, "energy_b": b.energy,
        "phrase_a": a.phrase,
        "vocal_pair": _vocal_pair(a, b),
        "genre_pair": genre_pair(a.genre, b.genre),
        "genre_a": _norm_genre(a.genre), "genre_b": _norm_genre(b.genre),
        "scene_a": genre_scene(a.genre), "scene_b": genre_scene(b.genre),
        "b_intro_bars": b.intro_bars,
        "iconic_a": a.iconic_vocal, "iconic_b": b.iconic_vocal,
        "a_breakdown": a.has_breakdown, "b_build": b.has_build,
        "stems": a.stems_available and b.stems_available,
        "shared_lyric": bool(a.shared_lyric or b.shared_lyric),
        "sample_link": a.sample_link or b.sample_link,
        "anchor_vocal": bool(a.flags.get("anchor_vocal")
                             or b.flags.get("anchor_vocal")),
        "drop_pair": bool(a.flags.get("drop_pair")
                          or b.flags.get("drop_pair")),
        "glue": bool(a.flags.get("glue") or b.flags.get("glue")),
        "third_deck": bool(a.flags.get("third_deck")
                           or b.flags.get("third_deck")),
    }
    return feats


# ----------------------------------------------------------------------------
# Requires / prefers evaluation
# ----------------------------------------------------------------------------

def _eval_requires(tid: str, req: dict, f: dict):
    """Returns (ok: bool, failed_reason: str|None)."""
    if not req:
        return True, None
    bmax = req.get("bpm_delta_pct_max")
    if bmax is not None and f["bpm_delta_pct"] > bmax:
        return False, f"BPM delta {f['bpm_delta_pct']:.1f}% > {bmax}% max"
    cmax = req.get("camelot_max")
    if cmax is not None and f["camelot"] > cmax:
        return False, (f"Camelot distance {f['camelot']} > {cmax} max "
                       f"— keys would clash under a blend")
    vocal_ok = req.get("vocal_ok")
    if vocal_ok is not None and f["vocal_pair"] not in vocal_ok:
        return False, f"vocal state '{f['vocal_pair']}' not allowed here"
    phrase_ok = req.get("phrase_a_ok")
    if phrase_ok is not None and f["phrase_a"] not in phrase_ok:
        return False, f"A is in '{f['phrase_a']}' — wrong section for this move"
    gp_ok = req.get("genre_pair_ok")
    if gp_ok is not None and f["genre_pair"] not in gp_ok:
        return False, f"genre pair '{f['genre_pair']}' too far for this move"
    for need in req.get("needs", []):
        if not f.get(need):
            return False, f"missing required context: '{need}'"
    return True, None


def _eval_when(when: str, f: dict):
    """Tiny rule language: 'energy_delta_abs<=1', 'iconic_b', 'genre_pair==leap'."""
    w = when.strip()
    for op in (">=", "<=", "==", "!=", ">", "<"):
        if op in w:
            left, right = w.split(op, 1)
            left, right = left.strip(), right.strip()
            val = f.get(left)
            try:
                rval = float(right)
            except ValueError:
                rval = right.strip("'\"")
            if op == ">=":
                return val is not None and val >= rval
            if op == "<=":
                return val is not None and val <= rval
            if op == "==":
                return val is not None and val == rval
            if op == "!=":
                return val is not None and val != rval
            if op == ">":
                return val is not None and val > rval
            if op == "<":
                return val is not None and val < rval
    return bool(f.get(w))


def _score_prefers(prefers: list, f: dict):
    points, reasons = 0.0, []
    for p in prefers:
        if _eval_when(p["when"], f):
            points += p.get("weight", 1)
            reasons.append(p.get("reason", p["when"]))
    return points, reasons


# Genre-norm bonus (bank GAPS.md #10): the scene steers the vocabulary.
def _genre_bonus(tid: str, entry: dict, f: dict):
    fam = entry.get("family")
    reasons = []
    pts = 0.0
    if f["scene_a"] == "hiphop" or f["scene_b"] == "hiphop":
        if fam == "PERF" or tid in ("stutter_transition", "wordplay",
                                    "bass_swap", "backspin", "hard_cut",
                                    "screwed_treatment"):
            pts += 1.0
            reasons.append("hip-hop/open-format norm: quick cuts, "
                           "stutter, wordplay")
    if f["scene_a"] in ("house", "trance", "pop") or \
            f["scene_b"] in ("house", "trance", "pop"):
        if fam == "FREQ" or tid in ("eq_blend", "filter_sweep",
                                    "layered_fx_stack", "reverb_wash"):
            pts += 1.0
            reasons.append("house/techno norm: long blends, sweeps, washes")
    if f["scene_a"] == "bass" or f["scene_b"] == "bass":
        if tid in ("double_drop", "hotcue_drop_swap", "bass_swap",
                   "vocal_punchline_snap"):
            pts += 1.0
            reasons.append("DnB/dubstep norm: drop collisions, drop swaps")
    return pts, reasons


# ----------------------------------------------------------------------------
# Main entry point
# ----------------------------------------------------------------------------

def select(a: Song, b: Song, top_n: int = 5) -> dict:
    f = derive_features(a, b)
    registry = meta.all_meta()
    rejected, scored = {}, []
    for tid, entry in registry.items():
        if entry.get("kind") not in ("render", "decision"):
            continue
        if tid in ("select_technique", "beat_jump", "harmonic_mix"):
            # pure decision/planning primitives, not transitions
            continue
        ok, why = _eval_requires(tid, entry.get("requires", {}), f)
        if not ok:
            rejected[tid] = why
            continue
        pts, reasons = _score_prefers(entry.get("prefers", []), f)
        bpts, breasons = _genre_bonus(tid, entry, f)
        total = 1.0 + pts + bpts
        params_hint = {k: v.get("default") for k, v in
                       entry.get("params", {}).items()}
        scored.append({"technique": tid, "score": round(total, 2),
                       "reasons": reasons + breasons,
                       "energy": entry.get("energy"),
                       "exit": entry.get("exit"),
                       "params_hint": params_hint})
    scored.sort(key=lambda r: (-r["score"], r["technique"]))
    # determinism guard: ties broken alphabetically, same input → same order
    return {"ranked": scored[:top_n], "rejected": rejected, "features": f}


# ----------------------------------------------------------------------------
# Self-test: agreement with T-037's canonical cases
# ----------------------------------------------------------------------------

def check_select():
    def songs(**kw):
        base = dict(bpm=128.0, key="8A", energy=7.0, genre="house")
        base.update(kw)
        return Song(**base)

    # Case 1 — lateral: same BPM/key/energy → eq_blend must rank #1, unrejected
    r = select(songs(), songs())
    assert "eq_blend" not in r["rejected"], r["rejected"]
    assert r["ranked"][0]["technique"] == "eq_blend", r["ranked"][0]
    assert "hook_drop_handoff" in r["rejected"], "iconic_a missing must reject hook"

    # Case 2 — A's signature hook → hook_drop_handoff must rank #1
    r = select(songs(vocal="iconic", iconic_vocal=True), songs())
    assert r["ranked"][0]["technique"] == "hook_drop_handoff", r["ranked"][:3]

    # Case 3 — wide BPM gap + key clash + genre leap → blends rejected,
    # top must be one of T-037's own canonical answers
    a = songs()
    b = songs(bpm=143.4, key="3B", energy=6.0, genre="trap")
    r = select(a, b)
    assert "eq_blend" in r["rejected"], "eq_blend must be pruned at 12% BPM"
    allowed = {"echo_out", "drum_bridge", "tempo_bridge",
               "breakdown_transition", "hard_cut", "genre_bridge",
               "reverb_freeze", "filter_sweep"}
    assert r["ranked"][0]["technique"] in allowed, r["ranked"][0]

    # Case 4 — shared lyric → wordplay must be in the top 3 with its reason
    a = songs(vocal="hook", energy=7.0)
    b = songs(vocal="hook", shared_lyric="midnight", energy=7.0)
    r = select(a, b)
    top3 = [x["technique"] for x in r["ranked"][:3]]
    assert "wordplay" in top3, top3

    # Case 5 — rejection reasons must name the failed rule (recompute case 3)
    r3 = select(songs(), songs(bpm=143.4, key="3B", energy=6.0,
                                genre="trap"))
    assert "eq_blend" in r3["rejected"]
    assert "BPM" in r3["rejected"]["eq_blend"], r3["rejected"]["eq_blend"]
    print("select.py checks: T-037 agreement + ranking sanity OK")
