"""
open-transitions engine — STRUCT/ROUTING gap techniques (domain module).

Covers Transition Gap Report 2026-10-19, STRUCT residual bucket
(gaps 8-13) + SET gap 18: element-level stem handovers, vocal-forward
structure moves, the same-song switch-up, and the mic talk-over plan.

  stem_element_crossfade    GAP-08 element-by-element stem crossfade
  strip_down_buildup        GAP-09 progressive element-removal build
  flying_solo_acapella      GAP-10 naked-vocal reset + filtered rise
  beat_switch_under_acapella GAP-11 beat swap under a looping vocal
  accidental_duet           GAP-12 two isolated vocals reading as a duet
  same_song_switchup        GAP-13 full <-> drums-only flip of one track
  mic_talkover_reset        GAP-18 mic talk-over (planning, not renderable)

Stem functions take stem dicts {"drums","bass","melody","vocal"} (mono
float64 arrays, per FRAMEWORK.md §7) + sr, and return a mono float64 mix.
Missing stems are treated as silence. Non-stem functions take full-track
arrays `a`/`b`.

TECHNIQUE_FUNCS exports only the functions the plan renderer can call as
fn(a, b, sr, **kwargs) (engine/render.py): the stem functions take dicts,
which the renderer cannot cut from a file, so they stay out of the
renderer and are demo + META + spec only. flying_solo_acapella's first
argument is a stem dict, so it does not qualify either. same_song_switchup
takes two plain audio arrays (two arrangements of one track) and DOES
qualify.
"""

import numpy as np

from . import dsp


def _fit(x, n):
    """Pad/truncate a mono array to exactly n samples (float64)."""
    x = np.asarray(x, dtype=np.float64)
    if len(x) == n:
        return x
    if len(x) > n:
        return x[:n]
    return np.pad(x, (0, n - len(x)))


def _stem(stems, name, n):
    """Fetch one stem fitted to n samples; missing stems are silence."""
    if stems is None or name not in stems:
        return np.zeros(n)
    return _fit(stems[name], n)


def _sum_stems(stems, names, n):
    out = np.zeros(n)
    for name in names:
        out += _stem(stems, name, n)
    return out


# ----------------------------------------------------------------------------
# GAP-08 — Element-by-Element Stem Crossfade (ROUTING)
# ----------------------------------------------------------------------------

def stem_element_crossfade(a_stems, b_stems, sr, bar_s,
                           order=("bass", "drums", "melody", "vocal"),
                           bars_per=4, intro_bars=4):
    """Hand the track over one stem at a time. A plays full for the intro;
    then per stage block, B's next stem enters at unity while A's
    corresponding stem mutes with a 1-beat equal-power crossfade.

    THE signature move is the first stage (bars 5-8): B's isolated
    bassline enters UNDER A's intact drums/melody/vocal — a bass entry
    with no kick attached. EQ tools cannot do this: opening B's low band
    always brings B's kick with it; only a stem gives bass without kick.

    Parameters
    ----------
    a_stems, b_stems : dict {"drums","bass","melody","vocal"}, mono arrays.
    sr : sample rate (Hz).
    bar_s : seconds per bar (float).
    order : sequence of stem names handed over, in stage order.
        Default ("bass","drums","melody","vocal"): 16-bar handover.
    bars_per : bars per stage (default 4).
    intro_bars : bars of A playing full before the first stage (default 4).

    Returns a mono float64 mix of intro_bars + len(order)*bars_per bars.
    Stems not listed in `order` stay with A for the whole mix.
    """
    bar_n = int(round(bar_s * sr))
    beat_n = int(round(bar_s / 4.0 * sr))
    n = (intro_bars + len(order) * bars_per) * bar_n
    mix = np.zeros(n)
    for name in dict.fromkeys(list(a_stems or {}) + list(b_stems or {})):
        a = _stem(a_stems, name, n)
        b = _stem(b_stems, name, n)
        if name in order:
            i = order.index(name)
            s0 = (intro_bars + i * bars_per) * bar_n
            ga = np.ones(n)
            gb = np.zeros(n)
            xf = min(max(beat_n, 1), n - s0)
            u = np.linspace(0.0, 1.0, xf)
            ga[s0:s0 + xf] = np.cos(0.5 * np.pi * u)
            gb[s0:s0 + xf] = np.sin(0.5 * np.pi * u)
            ga[s0 + xf:] = 0.0
            gb[s0 + xf:] = 1.0
            mix += a * ga + b * gb
        else:
            mix += a  # stems outside the order stay with A
    return mix


# ----------------------------------------------------------------------------
# GAP-09 — Strip-Down Buildup (ROUTING)
# ----------------------------------------------------------------------------

def strip_down_buildup(a_stems, b, sr, bar_s, guard_ms=5.0):
    """The build is progressive element REMOVAL on the outgoing track.

    Bars 1-4:   A full (drums+bass+melody+vocal).
    Bars 5-8:   A's drums stem muted (the groove hollows).
    Bars 9-12:  A's bass stem muted too — only vocal+melody exposed,
                hanging over the groove's ghost.
    Bar 13, beat 1: B's full drums+bass slam in at unity. A is gone.

    The inverse of T-022 (which strips TO drums): here the energy drains
    out of the low end so the slam lands relative to near-silence down
    low, not relative to A's kick.

    Parameters
    ----------
    a_stems : dict {"drums","bass","melody","vocal"}, mono arrays.
    b : incoming full-track segment, mono array (enters at its own downbeat).
    sr : sample rate (Hz).
    bar_s : seconds per bar (float).
    guard_ms : click guard at the mute steps and the slam (default 5.0 ms;
        inaudible, avoids digital clicks on the stepped mutes).

    Returns 12 bars of A-strip followed by b.
    """
    bar_n = int(round(bar_s * sr))
    n_strip = 12 * bar_n
    g = max(1, int(guard_ms / 1000.0 * sr))

    def mute_env(mute_bar):
        """Gain 1 until mute_bar, cosine guard down over the preceding g
        samples, 0 after."""
        env = np.ones(n_strip)
        bnd = mute_bar * bar_n
        s0 = max(0, bnd - g)
        if s0 < bnd:
            env[s0:bnd] = 0.5 + 0.5 * np.cos(
                np.pi * np.linspace(0.0, 1.0, bnd - s0))
        env[bnd:] = 0.0
        return env

    drums = _stem(a_stems, "drums", n_strip) * mute_env(4)
    bass = _stem(a_stems, "bass", n_strip) * mute_env(8)
    mel = _stem(a_stems, "melody", n_strip)
    vox = _stem(a_stems, "vocal", n_strip)
    strip = drums + bass + mel + vox
    # A cut at the slam (guard, click only)
    strip[-g:] *= 0.5 + 0.5 * np.cos(np.pi * np.linspace(0.0, 1.0, g))

    b = np.asarray(b, dtype=np.float64)
    b_out = b.copy()
    b_out[:g] *= 0.5 - 0.5 * np.cos(np.pi * np.linspace(0.0, 1.0, min(g, len(b))))
    return np.concatenate([strip, b_out])


# ----------------------------------------------------------------------------
# GAP-10 — Flying-Solo Acapella Bridge (STRUCT)
# ----------------------------------------------------------------------------

def flying_solo_acapella(a_stems, b, sr, bar_s, bpm, solo_beats=4,
                         rise_bars=4, lp_lo_hz=400.0, lp_hi_hz=16000.0):
    """All music drops out; a soloed acapella hangs alone for solo_beats,
    loops once more (the naked-vocal reset — the defining move), then B
    filters up from a low-pass UNDERNEATH the still-looping vocal into the
    drop, where the vocal exits and B is full and open.

    Parameters
    ----------
    a_stems : dict with a "vocal" stem (mono array) — the acapella source.
    b : incoming full-track segment, mono array (enters under the vocal).
    sr : sample rate (Hz).
    bar_s : seconds per bar (float).
    bpm : track tempo (the vocal solo length is counted in beats).
    solo_beats : beats of soloed vocal per loop pass (default 4 = 1 bar).
    rise_bars : bars of B rising under the vocal (default 4).
    lp_lo_hz : B's low-pass cutoff at rise start (default 400.0 Hz).
    lp_hi_hz : B's low-pass cutoff at the drop (default 16000.0 Hz,
        exponential sweep, fully open).

    Returns: naked vocal (2 passes) + B rising under the vocal loop
    (vocal fades out in the final 100 ms before the drop) + the rest of b.
    """
    beat_n = int(round(60.0 / bpm * sr))
    bar_n = int(round(bar_s * sr))
    solo_n = max(beat_n, solo_beats * beat_n)

    solo = _stem(a_stems, "vocal", solo_n)
    naked = np.tile(solo, 2)  # the loop — the naked-vocal reset

    b = np.asarray(b, dtype=np.float64)
    rise_n = min(rise_bars * bar_n, len(b))
    u = np.linspace(0.0, 1.0, rise_n)
    cut = lp_lo_hz * (lp_hi_hz / lp_lo_hz) ** u
    b_rise = dsp.sweep_filter(b[:rise_n], sr, cut, ftype="lowpass",
                              block=2048)

    # Vocal keeps looping over the rise; fades out in the last 100 ms so
    # the drop owns beat 1 (guard, click only).
    vox_rise = np.tile(solo, int(np.ceil(rise_n / solo_n)))[:rise_n]
    f = min(int(0.1 * sr), rise_n)
    vox_rise[-f:] *= 0.5 + 0.5 * np.cos(np.pi * np.linspace(0.0, 1.0, f))

    rise = b_rise + vox_rise
    rest = b[rise_n:]
    return np.concatenate([naked, rise, rest])


# ----------------------------------------------------------------------------
# GAP-11 — Beat Switch Under a Continuous Acapella (STRUCT)
# ----------------------------------------------------------------------------

def beat_switch_under_acapella(a_stems, b_stems, sr, bar_s, total_bars=8,
                               switch_bar=4, vocal_loop_bars=4, guard_ms=5.0):
    """One acapella runs uninterrupted while the instrumental underneath it
    is swapped at switch_bar (default bar 4): A drums+bass -> B drums+bass.
    The vocal is the constant, the beats rotate. Inverted sibling of T-010
    (which ends with the vocal — here the vocal never stops).

    Parameters
    ----------
    a_stems, b_stems : dicts with "drums","bass","vocal", mono arrays.
    sr : sample rate (Hz).
    bar_s : seconds per bar (float).
    total_bars : mix length in bars (default 8).
    switch_bar : 0-based bar index where A drums+bass hand to B drums+bass
        (default 4).
    vocal_loop_bars : bars of A's vocal looped for the whole mix (default 4).
    guard_ms : crossfade guard straddling the switch (default 5.0 ms).

    Returns total_bars of looping vocal over the switching beat bed.
    """
    bar_n = int(round(bar_s * sr))
    n = total_bars * bar_n
    g = max(2, int(guard_ms / 1000.0 * sr))

    vox_src = _stem(a_stems, "vocal", vocal_loop_bars * bar_n)
    vocal = np.tile(vox_src, int(np.ceil(n / len(vox_src))))[:n]

    a_bed = _sum_stems(a_stems, ("drums", "bass"), n)
    b_bed = _sum_stems(b_stems, ("drums", "bass"), n)

    sw = switch_bar * bar_n
    bed = a_bed.copy()
    bed[sw:] = b_bed[sw:]
    # short cosine crossfade straddling the switch (guard, click only)
    lo, hi = max(0, sw - g // 2), min(n, sw + g // 2)
    if hi > lo:
        w = np.linspace(0.0, 1.0, hi - lo)
        bed[lo:hi] = a_bed[lo:hi] * (0.5 + 0.5 * np.cos(np.pi * w)) \
            + b_bed[lo:hi] * (0.5 - 0.5 * np.cos(np.pi * w))
    return vocal + bed


# ----------------------------------------------------------------------------
# GAP-12 — Accidental Duet (STRUCT)
# ----------------------------------------------------------------------------

def accidental_duet(a_stems, b_stems, sr, bpm, bar_s, duet_bars=8,
                    pad_gain=0.5):
    """Two isolated vocals run simultaneously, tempo/key-synced, reading as
    a duet for a section. A's instrumental thins to a pad (its melody stem
    at pad_gain); B's drums hold the grid. A's drums and bass stay out.

    Parameters
    ----------
    a_stems, b_stems : dicts with "drums","melody","vocal", mono arrays.
    sr : sample rate (Hz).
    bpm : track tempo (used for the 2-beat section edge fades).
    bar_s : seconds per bar (float).
    duet_bars : duet section length in bars (default 8).
    pad_gain : gain of A's thinned melody stem (default 0.5).

    Returns duet_bars with 2-beat raised-cosine edge fades (the duet is a
    bounded section, not an infinite overlay).
    """
    bar_n = int(round(bar_s * sr))
    beat_n = int(round(60.0 / bpm * sr))
    n = duet_bars * bar_n

    mix = (_stem(a_stems, "vocal", n) + _stem(b_stems, "vocal", n)
           + pad_gain * _stem(a_stems, "melody", n)
           + _stem(b_stems, "drums", n))

    f = min(2 * beat_n, n // 2)
    if f > 1:
        # Edge fades bottom out at 0.25: in real use the section is cut
        # into a playing floor, so it swells in — it never fades from
        # digital silence.
        env = np.ones(n)
        env[:f] = 0.25 + 0.75 * dsp.raised_cosine(f, up=True)
        env[-f:] = 0.25 + 0.75 * dsp.raised_cosine(f, up=False)
        mix = mix * env
    return mix


# ----------------------------------------------------------------------------
# GAP-13 — Same-Song Switch-Up (STRUCT)
# ----------------------------------------------------------------------------

def same_song_switchup(a_full, a_alt, sr, bar_s, section_bars=2,
                       total_bars=8, guard_ms=50.0):
    """Two arrangements of the SAME track alternated live: section_bars of
    full, section_bars of the alternate (drums-only) arrangement, for
    total_bars — the hot-cue flip feel. Familiarity is constant; only the
    arrangement changes mid-track.

    Parameters
    ----------
    a_full : full-arrangement segment, mono array.
    a_alt : alternate (e.g. drums-only) arrangement of the same track, mono
        array. Same length/tempo/key as a_full — caller's prep domain.
    sr : sample rate (Hz).
    bar_s : seconds per bar (float).
    section_bars : bars per arrangement section (default 2).
    total_bars : total mix length in bars (default 8).
    guard_ms : cosine crossfade guard at each flip, straddling the boundary
        (default 50.0 ms — the protective, inaudible part of the flip).

    Returns total_bars of alternating arrangements.
    """
    bar_n = int(round(bar_s * sr))
    n = total_bars * bar_n
    full = _fit(a_full, n)
    alt = _fit(a_alt, n)

    sec_n = section_bars * bar_n
    g = max(2, int(guard_ms / 1000.0 * sr))
    idx = np.arange(n)
    gain = (idx // sec_n % 2 == 0).astype(np.float64)  # full on even sections
    for k in range(1, (n + sec_n - 1) // sec_n):
        bnd = k * sec_n
        start = 1.0 if k % 2 == 1 else 0.0  # gain value BEFORE the boundary
        lo, hi = max(0, bnd - g // 2), min(n, bnd + g // 2)
        if hi > lo:
            u = np.linspace(0.0, 1.0, hi - lo)
            # same track, correlated material -> linear complementary gains
            # under a cosine profile
            gain[lo:hi] = (start + (1.0 - 2.0 * start)
                           * (0.5 - 0.5 * np.cos(np.pi * u)))
    return full * gain + alt * (1.0 - gain)


# ============================================================================
# Metadata registry (FRAMEWORK.md §3) — merged by engine/meta.py all_meta()
# ============================================================================

META = {
    "stem_element_crossfade": {
        "title": "Element-by-Element Stem Crossfade",
        "bank": "GAP-08", "family": "ROUTING", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 3.0, "camelot_max": 2,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "verse", "chorus"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": ["stems"]},
        "prefers": [
            {"when": "b_intro_bars>=16", "weight": 3,
             "reason": "a 16-bar handover needs room on B's side"},
            {"when": "energy_delta_abs<=1", "weight": 2,
             "reason": "lateral energy — the elements do the work"},
            {"when": "camelot<=1", "weight": 2,
             "reason": "B's isolated bass under A's melody is key-sensitive"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "seamless", "clash_risk": "key",
        "params": {"bars_per": {"type": "int", "range": [2, 8], "default": 4,
                                "unit": "bars"},
                   "order": {"type": "list", "default": ["bass", "drums",
                                                        "melody", "vocal"],
                             "unit": "stem names"}},
        "evidence": [
            {"type": "set", "ref": "James Hype / stems-first method "
             "(Hype/stems) — 16-bar element-by-element stem crossfade incl. "
             "the bass-stem-only entry; Transition Gap Report 2026-10-19, "
             "GAP-08", "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    "strip_down_buildup": {
        "title": "Strip-Down Buildup",
        "bank": "GAP-09", "family": "ROUTING", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 3.0, "camelot_max": 4,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["build", "outro"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": ["stems"]},
        "prefers": [
            {"when": "vocal_pair==a_only", "weight": 2,
             "reason": "an exposed vocal over the hollowed groove is the "
                       "payoff image"},
            {"when": "energy_a>=6", "weight": 2,
             "reason": "removal only reads as a build against a dense A"},
        ],
        "energy": {"delta": 1, "tension": "rising"},
        "exit": "snap", "clash_risk": "none",
        "params": {},
        "evidence": [
            {"type": "set", "ref": "James Hype / stems-first method "
             "(Hype/stems) — progressive element removal on the outgoing "
             "track (drums, then bass) before the incoming slam; Transition "
             "Gap Report 2026-10-19, GAP-09", "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    "flying_solo_acapella": {
        "title": "Flying-Solo Acapella Bridge",
        "bank": "GAP-10", "family": "STRUCT", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 5.0, "camelot_max": 2,
                     "vocal_ok": ["a_only", "both"],
                     "phrase_a_ok": ["breakdown", "outro", "verse"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": ["stems", "anchor_vocal"]},
        "prefers": [
            {"when": "energy_a>=6", "weight": 2,
             "reason": "the naked-vocal reset hits hardest after peak "
                       "energy — it resets the room"},
            {"when": "b_has_build", "weight": 2,
             "reason": "B needs a rise worth filtering up under the vocal"},
        ],
        "energy": {"delta": -1, "tension": "reset"},
        "exit": "void", "clash_risk": "vocal",
        "params": {"solo_beats": {"type": "int", "range": [2, 8],
                                  "default": 4, "unit": "beats"},
                   "rise_bars": {"type": "int", "range": [2, 8], "default": 4,
                                 "unit": "bars"}},
        "evidence": [
            {"type": "tutorial", "ref": "Hype/DDT — flying-solo acapella "
             "bridge: music drops out, acapella hangs alone and loops, next "
             "track filters up underneath into the drop; Transition Gap "
             "Report 2026-10-19, GAP-10", "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    "beat_switch_under_acapella": {
        "title": "Beat Switch Under a Continuous Acapella",
        "bank": "GAP-11", "family": "STRUCT", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 1.5, "camelot_max": 2,
                     "vocal_ok": ["a_only", "both"],
                     "phrase_a_ok": ["verse", "chorus", "outro"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": ["stems", "anchor_vocal"]},
        "prefers": [
            {"when": "energy_delta_abs<=1", "weight": 2,
             "reason": "the vocal is the constant — beats rotate laterally"},
            {"when": "genre_pair==leap", "weight": 2,
             "reason": "a continuous vocal is the smoothest genre pivot in "
                       "the library"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "loop", "clash_risk": "key",
        "params": {"switch_bar": {"type": "int", "range": [2, 6],
                                  "default": 4, "unit": "bar index"},
                   "total_bars": {"type": "int", "range": [4, 16],
                                  "default": 8, "unit": "bars"}},
        "evidence": [
            {"type": "tutorial", "ref": "open-format toolkit — beat-switch "
             "under a continuous acapella: one vocal, swapping instrumentals "
             "underneath; Transition Gap Report 2026-10-19, GAP-11",
             "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    "accidental_duet": {
        "title": "Accidental Duet (Two-Vocal Overlay)",
        "bank": "GAP-12", "family": "STRUCT", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 1.0, "camelot_max": 1,
                     "vocal_ok": ["both"],
                     "phrase_a_ok": ["verse", "chorus", "breakdown"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": ["stems"]},
        "prefers": [
            {"when": "camelot<=1", "weight": 3,
             "reason": "two simultaneous vocals live or die on key distance"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "seamless", "clash_risk": "vocal",
        "params": {"duet_bars": {"type": "int", "range": [4, 16],
                                 "default": 8, "unit": "bars"},
                   "pad_gain": {"type": "float", "range": [0.0, 1.0],
                                "default": 0.5, "unit": "linear gain"}},
        "evidence": [
            {"type": "course", "ref": "Digital DJ Tips (DDT) — accidental "
             "duet: two isolated vocals in key/tempo sync reading as a "
             "duet; Transition Gap Report 2026-10-19, GAP-12",
             "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    "same_song_switchup": {
        "title": "Same-Song Switch-Up",
        "bank": "GAP-13", "family": "STRUCT", "kind": "render",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 0.0, "camelot_max": 0,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["drop", "chorus"],
                     "genre_pair_ok": ["same"],
                     "needs": []},
        "prefers": [
            {"when": "energy_a>=6", "weight": 2,
             "reason": "arrangement flips are a peak-time move"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "snap", "clash_risk": "none",
        "params": {"section_bars": {"type": "int", "range": [1, 4],
                                    "default": 2, "unit": "bars"},
                   "total_bars": {"type": "int", "range": [4, 16],
                                  "default": 8, "unit": "bars"},
                   "guard_ms": {"type": "float", "range": [10, 200],
                                "default": 50.0, "unit": "ms"}},
        "evidence": [
            {"type": "tutorial", "ref": "open-format toolkit — same-song "
             "switch-up: two arrangements of one track alternated live via "
             "hot-cue flips; Transition Gap Report 2026-10-19, GAP-13",
             "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
    "mic_talkover_reset": {
        "title": "Mic Talk-Over Reset",
        "bank": "GAP-18", "family": "SET", "kind": "planning",
        "verdict": "ADAPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 100.0, "camelot_max": 4,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "energy_delta_abs>=3", "weight": 3,
             "reason": "a human voice bridges a jump the music can't"},
        ],
        "energy": {"delta": 0, "tension": "reset"},
        "exit": "snap", "clash_risk": "none",
        "params": {"talkover_bars": {"type": "int", "range": [4, 16],
                                     "default": 8, "unit": "bars"},
                   "duck_db": {"type": "float", "range": [3, 12],
                               "default": 6.0, "unit": "dB"}},
        "evidence": [
            {"type": "tutorial", "ref": "open-format source — mic talk-over "
             "as a named transition tool (hosting move: talk over the "
             "outgoing outro to reset the room, drop the next track cold); "
             "Transition Gap Report 2026-10-19, GAP-18",
             "url": None, "date": "2026-10-19"},
        ],
        "composed_of": [],
    },
}


# Renderer-compatible subset: only functions with signature
# fn(a, b, sr, **kwargs) where a and b are plain audio arrays.
# The stem-signature functions take dicts and the plan renderer cuts arrays
# from files, so they are META + demo + spec only. flying_solo_acapella's
# first argument is a stem dict — not renderer-compatible either.
TECHNIQUE_FUNCS = {
    "same_song_switchup": same_song_switchup,
}
