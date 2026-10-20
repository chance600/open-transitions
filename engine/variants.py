"""open-transitions — variant registry (FRAMEWORK.md §6, operator 1).

A variant is a base technique x a named preset on one of its declared
discrete parameter axes (the ``"presets"`` maps in the metadata, §3).
This module is a GENERATOR, not a hand list: the registry is a pure
function of ``meta.all_meta()``, rebuilt at import (and re-buildable at
any time via ``build_variants()``). When new domain modules land
(FRAMEWORK.md §7), their preset axes expand this registry automatically
on the next import — no edits here.

Naming: ``<base>__<preset>`` for single-axis variants,
``<base>__<p1>_<p2>`` for pairwise combos of the first two axes
(capped at ``PAIRWISE_CAP`` combos per technique).

Every variant inherits its base technique's evidence, recorded as
``"inherited from <base>"`` (§6: generated entries are renderable and
carry the base's evidence, noted as inherited).
"""

import importlib
import inspect

import numpy as np

from . import meta, techniques

# Domain modules merged exactly the way engine/render.py merges them
# (FRAMEWORK.md §7): a module that isn't present yet is simply skipped.
_DOMAIN_MODULES = ("dm_techniques", "gap_struct", "gap_rest", "performer")

PAIRWISE_CAP = 9

# Positional audio-argument names used across the technique functions.
# Anything not listed here must arrive via kwargs (variant params, caller
# ctx, a default, or _fallback) — never guessed positionally.
_AUDIO_A = {"a", "a_bar", "a_build", "x", "vocal", "glue"}
_AUDIO_B = {"b", "b_bar", "b_build", "b_full", "b_vocal", "backing"}


# ----------------------------------------------------------------------------
# Registry generation
# ----------------------------------------------------------------------------

def _preset_axes(entry):
    """[(param_name, presets)] for params carrying a "presets" map,
    in metadata declaration order."""
    axes = []
    for pname, spec in (entry.get("params") or {}).items():
        presets = spec.get("presets") if isinstance(spec, dict) else None
        if presets:
            axes.append((pname, presets))
    return axes


def build_variants():
    """Enumerate the full variant registry from meta.all_meta().

    For each technique with >= 1 discrete preset axis: one variant per
    preset on the FIRST axis, plus pairwise combos of the first two
    axes (capped at PAIRWISE_CAP per technique). Deterministic: bases,
    preset names, and the returned dict's keys are all sorted.
    """
    registry = {}
    all_meta = meta.all_meta()
    for tid in sorted(all_meta):
        entry = all_meta[tid]
        axes = _preset_axes(entry)
        if not axes:
            continue
        title = entry.get("title", tid)
        axis1, presets1 = axes[0]
        for pname in sorted(presets1):
            registry[f"{tid}__{pname}"] = {
                "base": tid,
                "params": {axis1: presets1[pname]},
                "evidence": f"inherited from {tid}",
                "title": f"{title} [{pname}]",
            }
        if len(axes) >= 2:
            axis2, presets2 = axes[1]
            combos = [(p1, p2) for p1 in sorted(presets1)
                      for p2 in sorted(presets2)]
            for p1, p2 in combos[:PAIRWISE_CAP]:
                registry[f"{tid}__{p1}_{p2}"] = {
                    "base": tid,
                    "params": {axis1: presets1[p1], axis2: presets2[p2]},
                    "evidence": f"inherited from {tid}",
                    "title": f"{title} [{p1} + {p2}]",
                }
    return dict(sorted(registry.items()))


VARIANTS = build_variants()


def count():
    """Total number of registered variants."""
    return len(VARIANTS)


# ----------------------------------------------------------------------------
# Function resolution
# ----------------------------------------------------------------------------

def _technique_funcs():
    """Merged technique function map: core functions from
    engine.techniques (looked up by technique id), plus each domain
    module's TECHNIQUE_FUNCS — the same merge engine/render.py performs.
    Core wins on conflict, matching meta.all_meta()."""
    funcs = {}
    for tid in meta.all_meta():
        fn = getattr(techniques, tid, None)
        if callable(fn):
            funcs[tid] = fn
    for name in _DOMAIN_MODULES:
        try:
            mod = importlib.import_module(f".{name}", __package__)
        except ImportError:
            continue
        for tid, fn in getattr(mod, "TECHNIQUE_FUNCS", {}).items():
            funcs.setdefault(tid, fn)
    return funcs


_FUNCS = _technique_funcs()


def get_variant(name):
    """Resolve a variant id to (technique_fn, preset_kwargs).

    Raises KeyError on an unknown variant id, or on a variant whose base
    technique has no render function in the merged map.
    """
    if name not in VARIANTS:
        raise KeyError(f"unknown variant: {name}")
    entry = VARIANTS[name]
    fn = _FUNCS.get(entry["base"])
    if fn is None:
        raise KeyError(
            f"variant {name}: no function for base {entry['base']!r}")
    return fn, dict(entry["params"])


# ----------------------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------------------

_MISSING = object()


def _fallback(pname, merged):
    """Last-resort values for required parameters that are neither
    variant params nor caller ctx. Only well-defined production values:
    cue/anchor times default to the segment start; tempo endpoints
    default to the caller's bpm (or the bpm implied by bar_s)."""
    if pname in ("cue_t", "chop_t", "anchor_t", "a_word_t", "b_word_t"):
        return 0.0
    bpm = merged.get("bpm")
    if bpm is None and merged.get("bar_s"):
        bpm = 240.0 / merged["bar_s"]  # 4 beats per bar
    if pname in ("bpm", "bpm_from", "bpm_to"):
        return bpm if bpm is not None else _MISSING
    if pname == "bar_s" and merged.get("bpm"):
        return 240.0 / merged["bpm"]
    return _MISSING


def render_variant(name, a, b, sr, **ctx):
    """Render variant `name` over tracks a -> b at sample rate sr.

    Calls the base technique as fn(a, b, sr, **{**params, **ctx}) with
    two adaptations for the library's heterogeneous signatures
    (FRAMEWORK.md §7 predates a single call shape):

    * ctx is filtered to the kwargs the function actually accepts
      (inspect.signature), so callers may pass a shared ctx (bpm,
      bar_s, cue times, ...) to every variant.
    * Positional parameters are bound by name: the audio arguments
      (a / b and their aliases — x, vocal, b_full, glue, ...) receive
      a / b, and `sr` receives sr, wherever they sit in the signature.
      Functions returning a tuple (tempo_bridge -> (audio, bpm_to))
      yield their audio element.
    """
    fn, params = get_variant(name)
    merged = dict(params)
    merged.update(ctx)
    sig = inspect.signature(fn)

    args, kwargs, used = [], {}, set()
    for pname, p in sig.parameters.items():
        if p.kind is inspect.Parameter.VAR_POSITIONAL:
            continue
        if p.kind is inspect.Parameter.VAR_KEYWORD:
            for k, v in merged.items():
                if k not in used:
                    kwargs[k] = v
            continue
        if pname in merged:
            kwargs[pname] = merged[pname]
            used.add(pname)
        elif pname == "sr":
            args.append(sr)
        elif pname in _AUDIO_A:
            args.append(a)
        elif pname in _AUDIO_B:
            args.append(b)
        elif p.default is not inspect.Parameter.empty:
            continue  # function's own default stands
        else:
            fb = _fallback(pname, merged)
            if fb is _MISSING:
                raise TypeError(
                    f"render_variant({name!r}): cannot supply required "
                    f"parameter {pname!r} of "
                    f"{getattr(fn, '__name__', fn)} — pass it via ctx")
            kwargs[pname] = fb

    out = fn(*args, **kwargs)
    if isinstance(out, tuple):
        out = out[0]
    return np.asarray(out, dtype=np.float64)
