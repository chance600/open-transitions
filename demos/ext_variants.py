"""open-transitions — variant demos (FRAMEWORK.md §6/§7).

Registers a REPRESENTATIVE sample of the generated variant registry
(engine/variants.py) through the standard demo pipeline: for each
CORE-bank base technique with variants, its first single-axis variant
plus its first pairwise combo when one exists (variant ids in sorted
order), capped at 40 demos total. Variant selection is derived from
the registry at call time — nothing here is a hand list of variants.
Domain-module bases are staged by their own demos/ext_<domain>.py
modules (FRAMEWORK.md §7), not by this core sample.

All demos register with handoff None and no allowed-silence spans.
Scene notes:

* The per-base scenes below are demo staging only (which sketch tracks,
  how many bars, production ctx like cue times) — the same role the
  hand-written registrations in make_demos.py play for core techniques.
* Techniques whose function returns only the outgoing side (echo_out,
  brake_stop, power_down — their docstrings say the caller drops the
  next track) are completed by dropping B on the downbeat where A ends,
  the composition make_demos.py itself uses for echo_out.
* fake_drop's void is filled with the function's own documented
  `interlude` one-shot (a vocal quip from the vox sketch track).
* Bases whose render carries intentional in-render silence by design
  (backspin's decay-to-silence spin tail; vocal_punchline_snap's
  pre-drop void) cannot pass the silence gate without a declared
  allowed span, so they are excluded from this allowed-() sample; the
  core demo suite covers both with declared spans (FRAMEWORK.md §7).
"""

import numpy as np

from engine import meta as _meta
from engine.variants import VARIANTS, render_variant

MAX_DEMOS = 40

# Bases excluded from the sample: intentional in-render silence (see
# module docstring). Their variants remain in the registry and are
# renderable via variants.render_variant.
_EXCLUDED_BASES = ("backspin", "vocal_punchline_snap")


def _scene(base, ctx):
    """(a, b, extra_ctx, overlay_b) staging for one base technique."""
    T = ctx["get_tracks"]()
    bars, last_bars = ctx["bars"], ctx["last_bars"]
    A, B = T["A"], T["B"]
    extra = {"bpm": ctx["BPM"], "bar_s": ctx["BAR_S"]}
    a, b, overlay = bars(A, 8), bars(B, 8), False

    if base == "eq_blend":
        a, b = bars(A, 16), bars(B, 16)
    elif base == "filter_sweep":
        # fn timeline is tease+sweep+1 bars and zero-pads short inputs —
        # keep it inside the 16-bar tracks for every sweep preset
        a, b = bars(A, 16), bars(B, 16)
        extra.update(tease_bars=3)
    elif base in ("echo_out", "brake_stop", "power_down"):
        overlay = True  # fn returns A's ending; B drops at len(a)
    elif base == "echo_out_blend":
        a, b = bars(A, 8), bars(B, 12)
    elif base == "reverb_wash":
        a, b = bars(A, 12), bars(B, 8)
    elif base == "layered_fx_stack":
        a, b = bars(A, 12), bars(B, 8)
    elif base == "noise_echo_buildup":
        a, b = bars(A, 16), bars(B, 4)
    elif base == "build_to_drop":
        a, b = bars(A, 16), bars(B, 20)
    elif base == "double_drop":
        # sketch tracks are 24 bars; drop_bars=8 lands the bass swap
        # exactly at the end of the audio for the 16-bar drop preset
        a, b = bars(A, 24), bars(B, 24)
        extra.update(drop_bars=8)
    elif base == "drum_bridge":
        a, b = bars(A, 16), bars(B, 8)
    elif base == "acapella_overlay":
        a, b = bars(A, 16), T["vox"]
    elif base == "wordplay":
        a, b = bars(T["vox"], 8), bars(T["Bhook"], 8)
        extra.update(a_word_t=1.0, b_word_t=0.5, word_len_s=0.5)
    elif base == "vocal_chop_build":
        a, b = bars(A, 8), bars(B, 4)
        extra.update(chop_t=4 * ctx["BAR_S"], chop_len_s=1.0)
    elif base == "fake_drop":
        a, b = bars(A, 8), bars(B, 4)
        extra.update(interlude=bars(T["vox"], 1))
    elif base in ("loop_roll_build", "riser_drop"):
        a, b = bars(A, 8), bars(B, 4)
    elif base == "loop_transition":
        a, b = bars(A, 8), bars(B, 16)
    elif base == "loop_juggle_replace":
        a, b = bars(A, 4), bars(B, 4)
    elif base == "three_deck_layer":
        a, b = bars(A, 24), bars(B, 24)
        extra.update(glue_out_bars=8)
    elif base == "tempo_bridge":
        extra.update(bpm_from=ctx["BPM"], bpm_to=132.0)
    elif base == "hook_drop_handoff":
        a, b = last_bars(A, 8), bars(B, 8)
    elif base == "pitch_play":
        a, b = bars(T["vox"], 8), bars(A, 8)
    elif base == "screwed_treatment":
        extra.update(chop_every_beats=4, chop_repeats=2)
    elif base == "breakdown_swap":
        # breakdown stem base: a is A's drumless breakdown sketch,
        # b_drums the entering beat (caller-supplied, like cue times)
        a, b = bars(T["break"], 8), bars(B, 16)
        extra.update(b_drums=bars(T["stemsB"]["drums"], 8))
    return a, b, extra, overlay


def _make_fn(variant_id, base, ctx):
    def fn():
        a, b, extra, overlay = _scene(base, ctx)
        mix = render_variant(variant_id, a, b, ctx["SR"], **extra)
        if overlay:
            total = max(len(mix), len(a) + len(b))
            out = np.zeros(total)
            out[:len(mix)] += mix
            out[len(a):len(a) + len(b)] += b
            return out
        return mix

    return fn


def _sample_ids():
    """First single-axis variant per base (all bases, sorted), then the
    first pairwise combo per base — capped at MAX_DEMOS."""
    by_base = {}
    for vid in sorted(VARIANTS):
        by_base.setdefault(VARIANTS[vid]["base"], []).append(vid)

    def first_with(base, n_params):
        for vid in by_base.get(base, []):
            if len(VARIANTS[vid]["params"]) == n_params:
                return vid
        return None

    bases = [b for b in sorted(by_base)
             if b in _meta.CORE_META and b not in _EXCLUDED_BASES]
    picks = [v for v in (first_with(b, 1) for b in bases) if v]
    picks += [v for v in (first_with(b, 2) for b in bases) if v]
    return picks[:MAX_DEMOS]


def demo_specs(ctx):
    specs = {}
    for vid in _sample_ids():
        specs[vid] = (_make_fn(vid, VARIANTS[vid]["base"], ctx),
                      None, lambda m: ())
    return specs
