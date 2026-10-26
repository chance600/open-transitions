"""Verdict -> selector loop: the verdict schema and the promotion gate.

This is the anti-self-grading module. The loop may MEASURE (backtests,
demo gates, counts), but it may never PROMOTE on its own measurements.
Promotion into the registry requires a human verdict, and silence is
never approval.

Verdict outcomes mirror the workspace verdict dataset:
  pass, pass-reserve, positive, partial, negative, reject, rejected
Only "pass" (including a heart, recorded as pass with heart=True)
promotes. A later human reject after the latest human pass blocks
promotion until a newer human pass supersedes it. Machine verdicts
(verifier_type="machine") are recorded for measurement only and can
never promote, however many there are.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

HUMAN_PROMOTING_OUTCOMES = {"pass"}
HUMAN_BLOCKING_OUTCOMES = {"reject", "rejected"}


class VerdictError(ValueError):
    """Raised when a verdict row is malformed or unusable."""


@dataclass(frozen=True)
class Verdict:
    pair: str
    technique: str
    outcome: str
    verifier_type: str  # "human" or "machine"
    date: str = ""
    heart: bool = False
    source: str = ""  # e.g. dataset row id, chat reference

    def validate(self) -> None:
        if not self.pair or not self.technique or not self.outcome:
            raise VerdictError("verdict needs pair, technique, and outcome")
        if self.verifier_type not in ("human", "machine"):
            raise VerdictError(
                f"verifier_type must be 'human' or 'machine', got "
                f"{self.verifier_type!r}"
            )


def load_verdicts(path: str | Path) -> list[Verdict]:
    """Load a JSONL verdict file. Malformed rows fail loudly, never skipped."""
    verdicts = []
    for i, line in enumerate(Path(path).read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            verdict = Verdict(**row)
        except (json.JSONDecodeError, TypeError) as exc:
            raise VerdictError(f"{path}:{i}: malformed verdict row: {exc}") from exc
        verdict.validate()
        verdicts.append(verdict)
    return verdicts


def append_verdict(path: str | Path, verdict: Verdict) -> None:
    verdict.validate()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(verdict.__dict__) + "\n")


def promotion_gate(technique: str, verdicts: list[Verdict]) -> tuple[bool, str]:
    """Decide whether a technique may be promoted. Returns (ok, reason).

    Rules, in order:
    1. No human verdicts at all -> not promotable (silence never approves).
    2. A human reject/rejected AFTER the latest human pass -> blocked.
    3. At least one human pass (heart or plain) with no later human
       block -> promotable.
    Machine verdicts are ignored by this gate entirely.
    """
    human = [v for v in verdicts if v.technique == technique and v.verifier_type == "human"]
    if not human:
        return False, "no human verdicts; silence never approves"
    latest_pass = max(
        (i for i, v in enumerate(human) if v.outcome in HUMAN_PROMOTING_OUTCOMES),
        default=None,
    )
    latest_block = max(
        (i for i, v in enumerate(human) if v.outcome in HUMAN_BLOCKING_OUTCOMES),
        default=None,
    )
    if latest_pass is None:
        return False, "no human pass; partial/positive alone never promotes"
    if latest_block is not None and latest_block > latest_pass:
        return False, "human reject after latest human pass blocks promotion"
    return True, "human pass on file with no later human block"
