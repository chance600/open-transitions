"""Learning loops for open-transitions.

The loops propose and measure. A human disposes. Nothing in this
package promotes a technique into the registry on machine metrics
alone: promotion requires a human PASS/heart verdict row, and
silence never approves. See learning/README.md for the full rules.
"""

from learning.ingest import Candidate, Queue, SourceRegistry
from learning.propose import propose_draft
from learning.verdicts import Verdict, load_verdicts, promotion_gate
from learning.gates import demo_verify_gate

__all__ = [
    "Candidate",
    "Queue",
    "SourceRegistry",
    "propose_draft",
    "Verdict",
    "load_verdicts",
    "promotion_gate",
    "demo_verify_gate",
]
