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
# Phase 9 proposal P1 landed Phase 10: the ladder's clash class is no
# longer flat for cross-letter pairs — see the diagonal rule below.
# ----------------------------------------------------------------------------

def _parse_camelot(k: str):
    k = k.strip().upper()
    return int(k[:-1]), k[-1]


def camelot_distance(ka: str, kb: str) -> int:
    na, la = _parse_camelot(ka)
    nb, lb = _parse_camelot(kb)
    if na == nb and la == lb:
        return 0
    if na == nb:
        return 1  # relative major/minor
    step = min((nb - na) % 12, (na - nb) % 12)
    if la != lb:
        # MIK diagonal asymmetry (knowledge/setcraft.md, Phase 9): the
        # diagonal whose minor sits one wheel-step clockwise of the
        # major (8B->9A, 9A->8B) shares six of seven scale notes and
        # works — score 2, the workable band. The reverse diagonal
        # (8B->7A, 7A->8B) holds dissonant intervals — stays 4.
        if step == 1:
            n_major = na if la == "B" else nb
            n_minor = nb if la == "B" else na
            if (n_minor - n_major) % 12 == 1:
                return 2
        return 4  # different mode at a different wheel position — clash-prone
    return min(step, 4)


def _tonic_pc(key: str) -> int:
    """Tonic pitch class of a Camelot code (C = 0). The wheel is the
    circle of fifths anchored at 8B = C major; the A ring holds the
    relative minors, a minor third below the same-number major."""
    n, letter = _parse_camelot(key)
    pc = (7 * (n - 8)) % 12
    if letter == "A":
        pc = (pc - 3) % 12
    return pc


def key_move(ka: str, kb: str) -> int:
    """Signed semitone move from A's tonic to B's tonic, -6..+5
    (shortest signed path; the tritone folds to -6). Directional —
    the quantity the symmetric camelot_distance cannot express
    (Phase 9 proposal P2, landed Phase 10). Wheel checks: +2
    same-letter = +2 semitones; +7 (or -5) same-letter = +1."""
    d = (_tonic_pc(kb) - _tonic_pc(ka)) % 12
    return d - 12 if d >= 6 else d


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
    km = key_move(a.key, b.key)
    cam_raw = camelot_distance(a.key, b.key)
    cam = cam_raw
    # MIK +4 simplicity gate (Phase 9 proposal P3, landed Phase 10): a
    # same-letter +4 wheel move (10B->2B) is clash-class on the raw
    # ladder but works on melodically simple pairs (Guetta via MIK).
    # Interim simplicity proxy: vocal_pair — "neither" (no sung melody
    # on either side) is the least melodic density the schema can see,
    # until a melodic-density feature exists. Gated pairs read 3, the
    # top of the workable band: camelot_max<=2 techniques stay closed,
    # and the raw ladder value is preserved in camelot_raw.
    if cam_raw == 4:
        na, la = _parse_camelot(a.key)
        nb, lb = _parse_camelot(b.key)
        if la == lb and (nb - na) % 12 == 4 \
                and _vocal_pair(a, b) == "neither":
            cam = 3
    feats = {
        "bpm_delta_pct": bpm_delta_pct,
        "half_double_ok": half_double_ok,
        "camelot": cam,
        "camelot_raw": cam_raw,
        "key_move": km,
        # Energy Boost (MIK): a +1/+2-semitone key lift is an energy
        # event when the energy does not fall to meet it (P2).
        "energy_boost": km in (1, 2) and dE >= 0,
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


# Energy-boost bonus (MIK doctrine, knowledge/setcraft.md; Phase 9
# proposal P2, landed Phase 10): a +1/+2-semitone key lift on
# non-falling energy lifts the floor by itself — but the keys are
# incompatible, so only quick exits can carry it (the quick-mix rule).
# Snap/void exits (cuts, brakes, freezes, drop collisions) earn the
# preference; seamless/tail exits earn nothing, and their camelot_max
# gates keep excluding semitone moves exactly as before.
def _boost_bonus(tid: str, entry: dict, f: dict):
    if f.get("energy_boost") and entry.get("exit") in ("snap", "void"):
        return 1.0, ["energy boost: +1/+2 semitone key lift on "
                      "non-falling energy — a quick exit carries it (MIK)"]
    return 0.0, []


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
        xpts, xreasons = _boost_bonus(tid, entry, f)
        total = 1.0 + pts + bpts + xpts
        params_hint = {k: v.get("default") for k, v in
                       entry.get("params", {}).items()}
        scored.append({"technique": tid, "score": round(total, 2),
                       "reasons": reasons + breasons + xreasons,
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

    # Case 6 — MIK diagonals (Phase 9 proposal P1, landed Phase 10):
    # the note-sharing diagonal scores 2 and admits blend-class
    # techniques; the dissonant diagonal stays clash 4
    assert camelot_distance("8B", "9A") == 2
    assert camelot_distance("9A", "8B") == 2
    assert camelot_distance("8B", "7A") == 4
    assert camelot_distance("7A", "8B") == 4
    rw = select(songs(key="8B"), songs(key="9A"), top_n=100)
    rd = select(songs(key="8B"), songs(key="7A"), top_n=100)
    assert rw["features"]["camelot"] == 2, rw["features"]
    assert rd["features"]["camelot"] == 4, rd["features"]
    assert "eq_blend" not in rw["rejected"], rw["rejected"].get("eq_blend")
    assert "eq_blend" in rd["rejected"]
    assert "Camelot" in rd["rejected"]["eq_blend"]

    # Case 7 — energy boost (P2): signed key_move; snap exits prefer
    # the upward move; the mirror move, the falling-energy move, and
    # seamless/tail exits earn nothing
    assert key_move("8A", "10A") == 2 and key_move("8A", "6A") == -2
    assert key_move("8A", "3A") == 1 and key_move("8A", "1A") == -1

    def entry(r, tid):
        return next(x for x in r["ranked"] if x["technique"] == tid)

    up = select(songs(), songs(key="10A", energy=8.0), top_n=100)
    dn = select(songs(), songs(key="6A", energy=8.0), top_n=100)
    assert up["features"]["energy_boost"] is True
    assert dn["features"]["energy_boost"] is False
    assert entry(up, "hard_cut")["score"] == \
        entry(dn, "hard_cut")["score"] + 1.0
    assert any("energy boost" in s
               for s in entry(up, "hard_cut")["reasons"])
    assert not any("energy boost" in s
                   for s in entry(dn, "hard_cut")["reasons"])
    assert entry(up, "eq_blend")["score"] == \
        entry(dn, "eq_blend")["score"]
    flat = select(songs(), songs(key="10A", energy=6.0), top_n=100)
    assert flat["features"]["energy_boost"] is False
    semi = select(songs(), songs(key="3A", energy=8.0), top_n=100)
    smdn = select(songs(), songs(key="1A", energy=8.0), top_n=100)
    assert semi["features"]["key_move"] == 1
    assert entry(semi, "hard_cut")["score"] == \
        entry(smdn, "hard_cut")["score"] + 1.0
    assert entry(semi, "echo_out")["score"] == \
        entry(smdn, "echo_out")["score"]

    # Case 8 — +4 simplicity gate (P3): an upward same-letter +4 move
    # on a vocal-free pair reads 3 (raw ladder preserved at 4), admits
    # camelot_max=3 techniques and keeps camelot_max<=2 closed; any
    # sung melody, or the downward far move, keeps the clash score
    g = select(songs(key="8B"), songs(key="12B"), top_n=100)
    assert g["features"]["camelot_raw"] == 4, g["features"]
    assert g["features"]["camelot"] == 3, g["features"]
    assert "eq_blend" not in g["rejected"], g["rejected"].get("eq_blend")
    assert "Camelot" in g["rejected"]["double_drop"]
    gv = select(songs(key="8B", vocal="hook"),
                songs(key="12B", vocal="hook"), top_n=100)
    assert gv["features"]["camelot"] == 4, gv["features"]
    assert "eq_blend" in gv["rejected"]
    gd = select(songs(key="12B"), songs(key="8B"), top_n=100)
    assert gd["features"]["camelot"] == 4, gd["features"]
    assert "eq_blend" in gd["rejected"]
    print("select.py checks: T-037 agreement + ranking sanity OK")
