"""
open-transitions engine — compounds domain module (Phase 24).

Cross-base compounds promoted to bases by the combinatorial
enumeration pass (ENUMERATION.md, V2 queue item 3): pairs from the
registry's own atom set whose fusion is a distinct mechanism, not
a parallel stack. The enumeration's accounting is the provenance:
of 3,003 unordered render pairs, exactly one fusion passed the
admission bar as a previously unbuilt mechanism.

  CMP-01 aging_echo   echo throw whose feedback loop carries a
                      lowpass, so every repeat is darker than the
                      last — the dub tradition's delay (Phase 24)

Conventions follow engine/techniques.py: numpy mono float64
in/out, timing in bars/beats, the docstring IS the spec source
(techniques/*.md mirror it). Synthesized sketch audio only.
"""

import numpy as np
from scipy import signal

from . import dsp

KILL_DB = -60.0  # mirrors engine/techniques.py convention


# ----------------------------------------------------------------------------
# CMP-01 — Aging echo (dub feedback-tone echo)
# ----------------------------------------------------------------------------

def aging_echo(a, b, sr, bpm, bar_s, beat_div=0.5, feedback=0.55,
               wet=0.6, cutoff_hz=4500.0, tail_beats=4):
    """Echo throw whose repeats darken — a lowpass inside the loop.

    Parameters
    ----------
    a : outgoing track segment (mono float64); the throw is its
        final beat, exactly as in `echo_out` (T-004): lows killed
        over the throw beat, input gated at the throw, post-fader
        tail.
    b : incoming track segment (mono float64) — enters at full
        level under the ringing tail.
    sr : sample rate (Hz).
    bpm : tempo (beats/min) — sets the delay grid.
    bar_s : seconds per bar (signature parity with the SPACE
        family; the grid here runs on beats).
    beat_div : delay time in beats (default 0.5).
    feedback : loop gain per repeat (default 0.55).
    wet : echo level in the mix (default 0.6).
    cutoff_hz : the loop lowpass (default 4500 Hz). Each repeat
        passes it once more, so repeat k is the throw filtered
        k times — brightness decays with level, repeat spectra
        descend measurably.
    tail_beats : pure-tail length appended past A's end, ringing
        over B's entrance (default 4 beats).

    Returns
    -------
    Mono float64 mix of length len(a) + len(b): A with the throw,
    then B entering under the aging tail (the tail overlaps B's
    head and decays inside it).

    Why it works
    ------------
    The dub tradition's delay (King Tubby's and Scientist's
    feedback echo, carried into dub techno): the tone loss lives
    INSIDE the recurrence, so the tail does not just get quieter,
    it gets older — high content is spent first, and what is left
    ringing over B is a dull, low residue that cannot fight B's
    fresh top end. The registry's `dsp.feedback_delay` is a pure
    geometric series (every repeat an equally bright copy), and
    its two standing compounds with a filter atom —
    `layered_fx_stack`, `layered_emergence` — run the filter in
    PARALLEL on the mix. This is the serial topology neither
    implements. Precedent for a loop modification earning a base:
    `spiral_echo` (WEB-01) put pitch inside the same loop. The
    vendor name "Dub Echo" was resolved in the bank (Phases 6/8)
    as a knob form of T-004; this entry is the tradition
    mechanism that name points at, named for the mechanism so the
    records do not collide. Feed conditioning as doctrine:
    knowledge/mixing (iZotope, Phase 18).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    sr = float(sr)
    beat_s = 60.0 / bpm
    n = len(a)
    throw_n = int(beat_s * sr)  # last beat is the throw
    throw_start = max(0, n - throw_n)

    # Kill lows over the throw beat (echo_out's throw hygiene).
    lo_db = np.zeros(n)
    lo_db[throw_start:] = KILL_DB
    a_eq = dsp.apply_3band_eq(a, sr, lo_db, 0.0, 0.0)

    # Post-fader gate: input stops at the throw start.
    gate = np.ones(n)
    gate[throw_start:] = 0.0
    x = a_eq * gate

    # Extend with silence so the loop rings out as a pure tail.
    tail_n = int(tail_beats * beat_s * sr)
    x_ext = np.concatenate([x, np.zeros(tail_n)])
    n_ext = len(x_ext)

    # The aging series: y = sum_k feedback^k * shift^k(LP^k(x)).
    # Iterating the lowpass on the whole buffer per repeat IS the
    # physical loop — the circulating signal is filtered once per
    # circulation.
    d = max(1, int(round(beat_div * beat_s * sr)))
    sos = signal.butter(2, min(cutoff_hz, 0.45 * sr), btype="lowpass",
                        fs=sr, output="sos")
    y = x_ext.copy()
    cur = x_ext
    fbp = float(feedback)
    k = 1
    while fbp > 1e-4 and k * d < n_ext:
        cur = signal.sosfilt(sos, cur)
        y[k * d:] += fbp * cur[:-k * d]
        fbp *= feedback
        k += 1
    aged = (1.0 - wet) * x_ext + wet * y

    # B enters at A's end; the tail overlaps B's head.
    out = np.zeros(n + len(b))
    m = min(n_ext, len(out))
    out[:m] += aged[:m]
    out[n:n + len(b)] += b
    return out


# ----------------------------------------------------------------------------
# Registry
# ----------------------------------------------------------------------------

META = {
    "aging_echo": {
        "title": "Aging Echo (Dub Feedback-Tone Echo)",
        "bank": "CMP-01",
        "family": "SPACE",
        "kind": "render",
        "verdict": "ADAPT",
        "confidence": "high",
        "requires": {
            "bpm_delta_pct_max": 10.0,
            "camelot_max": None,
            "vocal_ok": ["a_only", "b_only", "both", "neither"],
            "phrase_a_ok": ["outro", "breakdown", "verse", "chorus"],
            "genre_pair_ok": ["same", "neighbor", "leap"],
            "needs": [],
        },
        "prefers": [
            {"when": "energy_delta<=0", "weight": 2,
             "reason": "the aging tail decays in level AND brightness "
                       "— a double decay under a falling or lateral exit"},
            {"when": "camelot>=4", "weight": 2,
             "reason": "darkened repeats shed A's key residue — the "
                       "canvas resets dull, not bright"},
            {"when": "genre_pair==leap", "weight": 1,
             "reason": "genre independence — the spent tail lets B "
                       "arrive from another world"},
        ],
        "energy": {"delta": -1, "tension": "falling"},
        "exit": "tail",
        "clash_risk": "none",
        "params": {
            "beat_div": {"type": "float", "range": [0.25, 1.0],
                         "default": 0.5, "unit": "beats",
                         "presets": {"quarter": 0.25, "dotted": 0.75,
                                     "full": 1.0}},  # the half-note
                         # default staging is the base itself —
                         # unnamed as a preset per the Phase 24 bar
            "cutoff_hz": {"type": "float", "range": [1200.0, 12000.0],
                          "default": 4500.0, "unit": "hz",
                          "presets": {"bright": 8000.0,
                                      "dark": 2000.0}},  # the 4500
                         # Hz default likewise stays the base itself
            "feedback": {"type": "float", "range": [0.0, 0.9],
                         "default": 0.55, "unit": "gain"},
            "wet": {"type": "float", "range": [0.0, 1.0],
                    "default": 0.6, "unit": "wet"},
            "tail_beats": {"type": "int", "range": [2, 8],
                           "default": 4, "unit": "beats"},
        },
        "evidence": [
            {"type": "set",
             "ref": "Dub delay canon — King Tubby / Scientist: "
                    "feedback echo with per-repeat tone loss as the "
                    "tradition's signature tail, carried into dub "
                    "techno (Basic Channel / Rhythm & Sound)",
             "url": None, "date": None},
            {"type": "cookbook",
             "ref": "Registry-internal: Phase 24 enumeration "
                    "(ENUMERATION.md Part B) — the serial "
                    "feedback-conditioning topology distinguished "
                    "from the parallel filter atoms of "
                    "layered_fx_stack / layered_emergence; feed "
                    "conditioning doctrine in knowledge/mixing "
                    "(iZotope Learn, Phase 18)",
             "url": None, "date": "2026-10-22"},
        ],
        "composed_of": ["echo_out"],
    },
}

TECHNIQUE_FUNCS = {
    "aging_echo": aging_echo,
}
