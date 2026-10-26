"""
open-transitions engine — keeper-shape domain module (Phase 30).

The four lane shapes that won settled keepers in the mixing lane but had
no registry entry, so engine/fit_select.py could only surface them as
gap-flagged custom-shape recommendations. Each function below renders the
GENERIC mechanism distilled from its keeper — what transfers to a new
pair — not the keeper itself. The keepers are pair-specific, stem-based,
multi-stage constructions (solved gain curves, zone fits, stem surgery);
no sketch render reproduces them, and nothing here claims otherwise.

  KEEP-01 ooh_tail_pickup  A plays dry at unity through a short tail
                            motif; the motif completes, B enters
                            straight at full level, and only a
                            low-stripped decaying tail of A's last
                            phrase rides under B's entrance.
                            Keeper: Stay High -> Rapture v4 (row 39).
  KEEP-02 underlap         B emerges slowly under A on a smootherstep
                            gain curve (whisper -> parity at the
                            handover anchor -> full only after A is
                            done) while B's vocal is withheld until
                            the re-entry bar. Keeper: Rapture ->
                            Kombucha v16a (rows 76, 94).
  KEEP-03 wub_runway       B's signature melodic figure previews on a
                            runway while A eases out attenuation-only
                            (A drums cut at the runway start, A vocal
                            excluded from the tail), the figure
                            play-staged up to level, then B proper.
                            Keeper: Balkans -> Cola v11-solo / v10b
                            (rows 103, 120).
  KEEP-04 wera_weave       A's hook vocal leads over B's groove
                            (B vocal withheld) for a weave zone, exits,
                            B's groove carries a recognition span, and
                            B's own vocal/chant enters last. Zero
                            performed-vocal coexistence by
                            construction: the A-vocal and B-vocal
                            slices are disjoint in the output
                            timeline. Keeper: Tuk Tuk -> Tunapewa v3c
                            (row 93).

Conventions follow engine/gap_struct.py: numpy mono float64 in/out,
timing in bars, the docstring IS the spec source (techniques/*.md
mirror it). Stem functions take dicts {\"drums\",\"bass\",\"melody\",
\"vocal\"}; missing stems are silence. Sketch caveat (honest): the
demo harness synthesizes stemsB WITHOUT a hook, so stemsB[\"vocal\"]
is digital silence — the underlap and wera_weave demos therefore
demonstrate the vocal-hold choreography structurally (the hold /
re-entry timing), not an audible B vocal. The wub_runway demo uses
stemsB[\"melody\"] as the signature figure, which the harness does
synthesize. The ooh_tail_pickup demo uses mono sketch tracks; the
\"motif\" is A's last phrase region, caller-nominated in real use.
"""

import numpy as np
from scipy import signal

KILL_DB = -60.0  # mirrors engine/techniques.py convention


def _fit(x, n):
    """Fit array x to length n (truncate or zero-pad)."""
    x = np.asarray(x, dtype=np.float64)
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


def _bar_slice(stems, names, bar_s, sr, start_bar, n_bars):
    """Sum of `names` stems over [start_bar, start_bar + n_bars)."""
    bar_n = int(round(bar_s * sr))
    n = int(n_bars * bar_n)
    full = _sum_stems(stems, names, int((start_bar + n_bars) * bar_n))
    return full[int(start_bar * bar_n):int(start_bar * bar_n) + n]


def _smootherstep(u):
    """C1-smooth 0 -> 1 ramp (3u^2 - 2u^3), clipped to [0, 1]."""
    u = np.clip(np.asarray(u, dtype=np.float64), 0.0, 1.0)
    return u * u * (3.0 - 2.0 * u)


def _db_to_lin(db):
    return 10.0 ** (np.asarray(db, dtype=np.float64) / 20.0)


# ----------------------------------------------------------------------------
# KEEP-01 — Tail-Motif Pickup (STRUCT)
# ----------------------------------------------------------------------------

def ooh_tail_pickup(a, b, sr, bar_s, tail_bars=2, tail_level=0.5,
                    tail_decay_bars=2.5):
    """A dry at unity through its tail motif; B picks up straight.

    A plays at unity, unprocessed, for its full length — no wash, no
    duck, no master fade. The device is what happens AT the seam: the
    motif completes, and B enters at full level (a 15 ms raised-cosine
    anti-click ramp only — that is click protection, not a fade-in).
    The only addition is a tail generated from A's last phrase region
    (its final `tail_bars`): high-passed at 180 Hz (lows stripped),
    scaled so its RMS equals `tail_level` x A's RMS, and decayed to
    exactly zero over `tail_decay_bars` under B's entrance.

    The motif itself is caller context: in real use the caller places
    A's segment so it ends on the tail motif (the keeper's 'ooh');
    the function does not detect motifs. What transfers is the
    pickup grammar — dry A, straight B entry, decaying tail — not
    the keeper's re-picked B passage or its +7 dB entry gain ride.

    Parameters
    ----------
    a, b : mono float64 segments (outgoing, incoming).
    sr : sample rate (Hz). bar_s : seconds per bar (float).
    tail_bars : bars of A taken as the tail source (default 2).
    tail_level : tail RMS as a fraction of A's RMS (default 0.5).
    tail_decay_bars : bars over which the tail decays to zero
        under B's entrance (default 2.5); clamped to the tail
        source's length, so the tail always reaches exactly zero
        within its own material rather than running past it.

    Returns a mono float64 mix of len(a) + len(b).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bar_n = int(round(bar_s * sr))
    mix = np.concatenate([a, b.copy()])
    # B entry: anti-click only.
    click_n = min(int(round(0.015 * sr)), len(b))
    if click_n > 1:
        ramp = 0.5 - 0.5 * np.cos(np.linspace(0.0, np.pi, click_n))
        mix[len(a):len(a) + click_n] *= ramp
    # Tail: HP-filtered last phrase of A, RMS-matched, decayed to zero.
    tail_n = int(tail_bars * bar_n)
    tail_src = a[-tail_n:] if len(a) >= tail_n else a
    if len(tail_src) and np.max(np.abs(tail_src)) > 0:
        sos = signal.butter(4, 180.0, btype="highpass", fs=sr, output="sos")
        tail = signal.sosfilt(sos, tail_src)
        rms_a = float(np.sqrt(np.mean(a ** 2))) if len(a) else 0.0
        rms_t = float(np.sqrt(np.mean(tail ** 2))) if len(tail) else 0.0
        if rms_a > 0 and rms_t > 0:
            tail = tail * (tail_level * rms_a / rms_t)
            decay_n = min(int(tail_decay_bars * bar_n), len(tail), len(b))
            u = np.linspace(0.0, 1.0, decay_n)
            mix[len(a):len(a) + decay_n] += tail[:decay_n] * (
                1.0 - _smootherstep(u))
    return mix


# ----------------------------------------------------------------------------
# KEEP-02 — Underlap (ROUTING)
# ----------------------------------------------------------------------------

def underlap(a_stems, b_stems, sr, bar_s, zone_bars=12, entry_db=-26.0,
             parity_db=-10.8):
    """B emerges slowly under A; B's vocal is held until re-entry.

    Over a `zone_bars` zone: B's non-vocal stems enter at `entry_db`
    (a whisper) and rise on two C1-smooth smootherstep segments —
    entry -> parity (`parity_db`, the handover anchor, at 2/3 of the
    zone) -> full (0 dB, at the zone end). A plays at unity until the
    final two bars, then dissolves to exactly zero at the zone end.
    B's vocal stem is withheld for the whole zone except its final
    bar (the re-entry bar), so the first B vocal heard is the
    re-entry, never a chant leaking under A's exit.

    The keeper's parity (-10.77 dB) was solved from its measured
    components; the generic form fixes parity at -10.8 dB and lets
    the caller override it. The keeper's stem surgery (zeroing one
    excerpt bar's stem) is NOT reproduced — the generic move is the
    emergence curve plus the vocal hold, which is what a new pair
    can reuse without the keeper's forensic record.

    Parameters
    ----------
    a_stems, b_stems : dict {\"drums\",\"bass\",\"melody\",\"vocal\"}.
    sr : sample rate (Hz). bar_s : seconds per bar (float).
    zone_bars : emergence zone length in bars (default 12).
    entry_db : B's entry level in dB (default -26.0, a whisper).
    parity_db : B's level at the handover anchor (default -10.8).

    Returns a mono float64 mix of zone_bars bars. A is fully done
    at the zone end; B is at full level there.
    """
    bar_n = int(round(bar_s * sr))
    n = int(zone_bars * bar_n)
    parity_bar = int(round(zone_bars * 2.0 / 3.0))
    # B non-vocal emergence curve: entry -> parity -> full.
    t = np.arange(n)
    gb = np.zeros(n)
    p0 = 0
    p1 = parity_bar * bar_n
    p2 = n
    if p1 > p0:
        gb[p0:p1] = _db_to_lin(entry_db + (parity_db - entry_db)
                               * _smootherstep(
                                   np.linspace(0.0, 1.0, p1 - p0)))
    if p2 > p1:
        gb[p1:p2] = _db_to_lin(parity_db + (0.0 - parity_db)
                               * _smootherstep(
                                   np.linspace(0.0, 1.0, p2 - p1)))
    # A dissolve: unity until the final two bars, then to zero.
    ga = np.ones(n)
    d0 = max(0, (zone_bars - 2) * bar_n)
    if n > d0:
        ga[d0:] = 1.0 - _smootherstep(np.linspace(0.0, 1.0, n - d0))
    mix = _sum_stems(a_stems, ["drums", "bass", "melody", "vocal"], n) * ga
    mix += _sum_stems(b_stems, ["drums", "bass", "melody"], n) * gb
    # B vocal: withheld until the re-entry bar (final bar of the zone).
    b_vocal = _stem(b_stems, "vocal", n)
    r0 = (zone_bars - 1) * bar_n
    mix[r0:] += b_vocal[r0:]
    return mix


# ----------------------------------------------------------------------------
# KEEP-03 — Signature-Figure Runway (ROUTING)
# ----------------------------------------------------------------------------

def wub_runway(a_stems, b_stems, sr, bar_s, runway_bars=6,
               figure="melody", intro_bars=4, tail_bars=4):
    """B's signature figure previews on a runway; A eases out.

    Intro: A plays full for `intro_bars`. Runway: A's drums are cut
    at the runway start and A's vocal is excluded from the tail;
    A's remaining stems (bass + melody) ease out attenuation-only
    on a smootherstep dB curve (0 dB -> -60 dB) reaching exactly
    zero at the runway end. Meanwhile B's signature figure
    (`figure` stem, default melody) tiles across the runway in
    plays, play-staged: play 1 ramps -1.0 -> -0.5 dB, play 2 ramps
    -0.5 -> 0 dB, play 3+ sits at 0 dB. After the runway, B proper
    continues from where the figure's first play left off.

    The keeper's runway curve was a per-bar PCHIP solve from its
    components; the generic form is the smootherstep dB curve,
    which preserves the properties that matter (attenuation-only,
    exact zero at the runway end) without the keeper's numbers.
    The figure is caller-nominated: the caller passes the stem
    that IS the signature figure for the pair.

    Parameters
    ----------
    a_stems, b_stems : dict {\"drums\",\"bass\",\"melody\",\"vocal\"}.
    sr : sample rate (Hz). bar_s : seconds per bar (float).
    runway_bars : runway length in bars (default 6).
    figure : B stem name used as the signature figure (default
        \"melody\").
    intro_bars : bars of A full before the runway (default 4).
    tail_bars : bars of B proper after the runway (default 4).

    Returns a mono float64 mix of intro + runway + tail bars.
    """
    bar_n = int(round(bar_s * sr))
    intro_n = int(intro_bars * bar_n)
    runway_n = int(runway_bars * bar_n)
    tail_n = int(tail_bars * bar_n)
    total = intro_n + runway_n + tail_n
    mix = np.zeros(total)
    # Intro: A full.
    mix[:intro_n] += _sum_stems(
        a_stems, ["drums", "bass", "melody", "vocal"], intro_n)
    # Runway: A bass+melody easing out, drums cut, vocal excluded.
    a_run = _bar_slice(a_stems, ["bass", "melody"], bar_s, sr,
                       intro_bars, runway_bars)
    u = np.linspace(0.0, 1.0, runway_n)
    ga_db = -60.0 * _smootherstep(u)
    ga = _db_to_lin(ga_db)
    ga[-1] = 0.0  # exact zero at the runway end
    mix[intro_n:intro_n + runway_n] += a_run * ga
    # Runway: B figure tiled in plays, play-staged up to level.
    play_bars = max(1, int(runway_bars) // 3)
    play_n = int(play_bars * bar_n)
    figure_seg = _bar_slice(b_stems, [figure], bar_s, sr, 0, play_bars)
    n_plays = int(np.ceil(runway_n / play_n)) if play_n else 0
    stages = [(-1.0, -0.5), (-0.5, 0.0)]
    for k in range(n_plays):
        s0 = intro_n + k * play_n
        s1 = min(s0 + play_n, intro_n + runway_n)
        if s1 <= s0:
            break
        lo, hi = stages[k] if k < len(stages) else (0.0, 0.0)
        ramp = _db_to_lin(np.linspace(lo, hi, s1 - s0))
        mix[s0:s1] += figure_seg[:s1 - s0] * ramp
    # Tail: B proper continues from where the figure's first play
    # left off (bar play_bars of B's timeline).
    b_tail = _bar_slice(b_stems, ["drums", "bass", "melody", "vocal"],
                        bar_s, sr, play_bars, tail_bars)
    mix[intro_n + runway_n:] += b_tail
    return mix


# ----------------------------------------------------------------------------
# KEEP-04 — Hook-Vocal Weave (STRUCT)
# ----------------------------------------------------------------------------

def wera_weave(a_stems, b_stems, sr, bar_s, weave_bars=8, chant_bars=2,
               intro_bars=4, exit_bars=1, recognition_bars=2):
    """A's hook vocal leads over B's groove; B's chant enters last.

    Intro: A plays full for `intro_bars`. Weave: A's vocal stem
    leads over B's groove (drums + bass + melody) for `weave_bars`
    — A's other stems are out, B's vocal is withheld. Exit: A's
    vocal fades to zero over `exit_bars` while B's groove
    continues. Recognition: B's groove alone for
    `recognition_bars` — the listener recognizes B before its
    vocal arrives (D10). Chant: B full, vocal included, for
    `chant_bars`. A-vocal and B-vocal never coexist: the slices
    are disjoint in the output timeline by construction.

    The keeper's weave was tempo-matched by a diagnosis-led repair
    (true-rate phase-vocoder stretch, single kick-pairing fit);
    tempo matching is caller context here, not part of the move.
    What transfers is the choreography: lead vocal, staged exit,
    recognition span, chant last.

    Parameters
    ----------
    a_stems, b_stems : dict {\"drums\",\"bass\",\"melody\",\"vocal\"}.
    sr : sample rate (Hz). bar_s : seconds per bar (float).
    weave_bars : vocal-lead zone in bars (default 8).
    chant_bars : closing B-full span in bars (default 2).
    intro_bars : bars of A full before the weave (default 4).
    exit_bars : bars over which A's vocal exits (default 1).
    recognition_bars : B-groove-alone span in bars (default 2).

    Returns a mono float64 mix of
    intro + weave + exit + recognition + chant bars.
    """
    bar_n = int(round(bar_s * sr))

    def seg(stems, names, start, nbars):
        return _bar_slice(stems, names, bar_s, sr, start, nbars)

    parts = []
    # Intro: A full.
    parts.append(seg(a_stems, ["drums", "bass", "melody", "vocal"],
                     0, intro_bars))
    # Weave: A vocal over B groove (B vocal withheld).
    parts.append(seg(a_stems, ["vocal"], intro_bars, weave_bars)
                 + seg(b_stems, ["drums", "bass", "melody"], 0, weave_bars))
    # Exit: A vocal fades out over exit_bars; B groove continues.
    a_exit = seg(a_stems, ["vocal"], intro_bars + weave_bars, exit_bars)
    n_exit = len(a_exit)
    if n_exit:
        a_exit = a_exit * (1.0 - np.linspace(0.0, 1.0, n_exit))
    parts.append(a_exit + seg(b_stems, ["drums", "bass", "melody"],
                              weave_bars, exit_bars))
    # Recognition: B groove alone.
    parts.append(seg(b_stems, ["drums", "bass", "melody"],
                     weave_bars + exit_bars, recognition_bars))
    # Chant: B full, vocal included, last.
    parts.append(seg(b_stems, ["drums", "bass", "melody", "vocal"],
                     weave_bars + exit_bars + recognition_bars, chant_bars))
    return np.concatenate(parts)


TECHNIQUE_FUNCS = {
    "ooh_tail_pickup": ooh_tail_pickup,
    "underlap": underlap,
    "wub_runway": wub_runway,
    "wera_weave": wera_weave,
}

META = {
    "ooh_tail_pickup": {
        "title": "Tail-Motif Pickup",
        "bank": "KEEP-01", "family": "STRUCT", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": None, "camelot_max": None,
                     "vocal_ok": ["a_only", "both"],
                     "phrase_a_ok": ["outro", "chorus", "verse", "build"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": []},
        "prefers": [
            {"when": "a_motif", "weight": 2,
             "reason": "A carries a short distinctive vocal tail motif "
                       "to pick up as the device"},
            {"when": "genre_pair==same", "weight": 1,
             "reason": "same-genre pair — the pickup needs no genre "
                       "work, only the motif"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "snap", "clash_risk": "key",
        "params": {"tail_bars": {"type": "int", "range": [1, 4],
                                 "default": 2, "unit": "bars",
                                 "presets": {"short": 1, "standard": 2,
                                             "long": 4}},
                   "tail_level": {"type": "float", "range": [0.2, 0.8],
                                  "default": 0.5, "unit": "fraction",
                                  "presets": {"soft": 0.35,
                                              "standard": 0.5,
                                              "present": 0.65}}},
        "evidence": [
            {"type": "field-test",
             "ref": "Lane keeper: Stay High -> Rapture ooh_tail_pickup v4, "
                    "heart PASS ('SO GOOD', verdict-dataset row 39, "
                    "2026-10-20) — A dry at unity, motif completes, "
                    "B piano picks up straight",
             "url": None, "date": "2026-10-20"},
        ],
        "composed_of": [],
    },
    "underlap": {
        "title": "Underlap (Slow Emergence, Vocal Held)",
        "bank": "KEEP-02", "family": "ROUTING", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 10.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "verse", "chorus", "build"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": ["stems"]},
        "prefers": [
            {"when": "b_entry_mode==groove", "weight": 2,
             "reason": "B enters as groove, not vocal — emergence has "
                       "room without a vocal collision"},
            {"when": "bpm_delta_pct>=3", "weight": 1,
             "reason": "gap bridged by emergence rather than a blend "
                       "(keeper gap 5.5%)"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "seamless", "clash_risk": "vocal",
        "params": {"zone_bars": {"type": "int", "range": [4, 20],
                                 "default": 12, "unit": "bars",
                                 "presets": {"short": 8, "standard": 12,
                                             "long": 16}},
                   "entry_db": {"type": "float", "range": [-30.0, -10.0],
                                "default": -26.0, "unit": "dB",
                                "presets": {"whisper": -26.0,
                                            "quiet": -20.0,
                                            "audible": -14.0}}},
        "evidence": [
            {"type": "field-test",
             "ref": "Lane keeper: Rapture -> Kombucha underlap_carry "
                    "v16a, heart PASS (verdict-dataset rows 76, 94, "
                    "2026-10-21) — smootherstep emergence, chant "
                    "removed, vocal re-entry first heard at 59.63 s",
             "url": None, "date": "2026-10-21"},
        ],
        "composed_of": [],
    },
    "wub_runway": {
        "title": "Signature-Figure Runway (Drums Excluded)",
        "bank": "KEEP-03", "family": "ROUTING", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 5.0, "camelot_max": None,
                     "vocal_ok": ["a_only", "b_only", "both", "neither"],
                     "phrase_a_ok": ["outro", "chorus"],
                     "genre_pair_ok": ["same", "neighbor", "leap"],
                     "needs": ["stems"]},
        "prefers": [
            {"when": "b_motif", "weight": 2,
             "reason": "B has a signature melodic figure to feature "
                       "on the runway"},
            {"when": "bpm_delta_pct<=1", "weight": 1,
             "reason": "Delta~0% — the runway needs no tempo work, "
                       "only staging (keeper gap 0%)"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "seamless", "clash_risk": "key",
        "params": {"runway_bars": {"type": "int", "range": [2, 12],
                                  "default": 6, "unit": "bars",
                                  "presets": {"short": 4, "standard": 6,
                                              "long": 8}}},
        "evidence": [
            {"type": "field-test",
             "ref": "Lane keepers: Balkans -> Cola wub_runway v11-solo, "
                    "heart PASS, and v10b-with-drums, PASS "
                    "(verdict-dataset rows 103, 120, 2026-10-21/22) — "
                    "six-bar continuous-identity runway, drums cut, "
                    "vocal excluded, figure play-staged",
             "url": None, "date": "2026-10-21"},
        ],
        "composed_of": [],
    },
    "wera_weave": {
        "title": "Hook-Vocal Weave (Vocal Leads, Chant Last)",
        "bank": "KEEP-04", "family": "STRUCT", "kind": "render",
        "verdict": "ADOPT", "confidence": "medium",
        "requires": {"bpm_delta_pct_max": 5.0, "camelot_max": 3,
                     "vocal_ok": ["a_only", "both"],
                     "phrase_a_ok": ["outro", "chorus", "verse"],
                     "genre_pair_ok": ["same", "neighbor"],
                     "needs": ["stems"]},
        "prefers": [
            {"when": "a_motif", "weight": 2,
             "reason": "A hook vocal leads the weave over B's groove"},
            {"when": "b_entry_mode==groove", "weight": 1,
             "reason": "B groove carries the weave while its vocal is "
                       "withheld"},
        ],
        "energy": {"delta": 0, "tension": "flat"},
        "exit": "seamless", "clash_risk": "vocal",
        "params": {"weave_bars": {"type": "int", "range": [2, 16],
                                  "default": 8, "unit": "bars",
                                  "presets": {"short": 4, "standard": 8,
                                              "long": 12}},
                   "chant_bars": {"type": "int", "range": [1, 6],
                                  "default": 2, "unit": "bars",
                                  "presets": {"brief": 1, "standard": 2,
                                              "extended": 4}}},
        "evidence": [
            {"type": "field-test",
             "ref": "Lane keeper: Tuk Tuk -> Tunapewa wera_weave v3c, "
                    "heart PASS (verdict-dataset row 93, 2026-10-21) — "
                    "wera line leads over the drum weave, exit, "
                    "recognition, B chant last, zero vocal coexistence",
             "url": None, "date": "2026-10-21"},
        ],
        "composed_of": [],
    },
}
