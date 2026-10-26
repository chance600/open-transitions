"""Verification gates: pure functions over already-computed evidence.

These gates MEASURE; they never promote. A technique passes the demo
gate only when it is actually registered (META entry) AND its demo
verification entry is fully clean. The demo gate is one input to a
human promotion decision, never a substitute for it (see verdicts.py:
a loop cannot hear, and QC-clean renders have been rejected by ear).
"""

from __future__ import annotations


def demo_verify_gate(
    technique: str,
    meta: dict,
    verification: list[dict],
) -> tuple[bool, str]:
    """Check a technique's demo evidence. Returns (ok, reason)."""
    if technique not in meta:
        return False, f"{technique!r} has no META registry entry"
    entries = [e for e in verification if e.get("technique") == technique]
    if not entries:
        return False, f"{technique!r} has no demo verification entry"
    entry = entries[0]
    failed = [
        key
        for key in ("render_ok", "silence_ok", "headroom_ok")
        if not entry.get(key)
    ]
    if failed:
        return False, f"demo verification failed on: {', '.join(failed)}"
    return True, "META entry + fully clean demo verification"


def registry_counts(meta: dict, variants: dict, knowledge: int, demos: int) -> dict:
    """Snapshot counts in the same units the workspace knowledge pass uses."""
    return {
        "bases": len(meta),
        "variants": len(variants),
        "knowledge": knowledge,
        "demos": demos,
    }
