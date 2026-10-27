"""One learning pass: ingest -> propose -> measure -> report.

A pass never merges, never commits, never promotes. It writes spec
drafts for newly claimed queue items and prints a report of promotion
gates (which a human then acts on). Run it from the repo root:

    python -m learning.loop --queue learning/queue.json \
        --verdicts learning/verdicts.jsonl --drafts learning/drafts

The queue and verdict files are caller-supplied: the repo ships none,
so a fresh checkout starts empty and invents nothing.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from learning.gates import demo_verify_gate
from learning.ingest import Queue, Source, SourceRegistry
from learning.propose import propose_draft
from learning.verdicts import load_verdicts, promotion_gate


def load_registry(path: str | Path) -> SourceRegistry:
    """Load a human-registered sources file (JSON list of Source dicts).

    Registration is a human act: every entry asserts free/public
    reachability, confirmed by a human, never inferred by the loop.
    """
    rows = json.loads(Path(path).read_text())
    return SourceRegistry([Source(**row) for row in rows])


def run_pass(
    queue_path: str | Path,
    verdicts_path: str | Path | None,
    drafts_dir: str | Path,
    registry: SourceRegistry,
    worker: str = "learning-loop",
) -> dict:
    """Run one pass. Returns the report dict (also printed as JSON)."""
    report: dict = {"drafts_written": [], "promotion_gates": {}, "notes": []}
    queue = Queue(queue_path, registry)
    candidate = queue.next_unclaimed()
    if candidate is None:
        report["notes"].append("queue empty or all items claimed; nothing proposed")
    else:
        queue.claim(candidate, worker)
        path = propose_draft(candidate, drafts_dir)
        queue.release(candidate, "proposed")
        queue.save()
        report["drafts_written"].append(str(path))
    if verdicts_path and Path(verdicts_path).exists():
        verdicts = load_verdicts(verdicts_path)
        techniques = sorted({v.technique for v in verdicts})
        for technique in techniques:
            ok, reason = promotion_gate(technique, verdicts)
            report["promotion_gates"][technique] = {"promotable": ok, "reason": reason}
    else:
        report["notes"].append("no verdicts file; promotion gates not evaluated")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one learning pass.")
    parser.add_argument("--queue", required=True)
    parser.add_argument("--verdicts", default=None)
    parser.add_argument("--drafts", required=True)
    parser.add_argument("--sources", default="learning/sources.json")
    parser.add_argument("--worker", default="learning-loop")
    args = parser.parse_args()
    registry = (
        load_registry(args.sources)
        if args.sources and Path(args.sources).exists()
        else SourceRegistry()
    )
    report = run_pass(args.queue, args.verdicts, args.drafts, registry, args.worker)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
