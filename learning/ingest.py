"""Mining loop: sources registry, candidate validation, and queue.

Rules carried over from the workspace crawl engine:
- Free/public sources ONLY. A source that is paid, login-walled, or
  otherwise non-public is rejected at registration, never at use.
- Zero spend. Nothing in this module spends money or calls a paid API.
- Provenance on every candidate: a candidate without a source URL
  and a license note is invalid, full stop.
- Claim protocol: a worker claims a queue item before working it and
  releases it only after the work verifies. A live claim (< 24h old)
  means the next worker takes the next UNCLAIMED item, never a
  double run.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

CLAIM_TTL_S = 24 * 3600


class IngestError(ValueError):
    """Raised when a source, candidate, or queue operation is invalid."""


@dataclass(frozen=True)
class Source:
    """One mining source. `free_public` is a human assertion, not a guess.

    Register a source only after a human has confirmed it is free and
    publicly reachable without login or payment. The flag is never
    inferred from a URL.
    """

    name: str
    url: str
    kind: str  # e.g. "repo", "paper", "docs", "manual"
    free_public: bool
    license_note: str = ""

    def validate(self) -> None:
        if not self.name or not self.url:
            raise IngestError("source needs a name and a url")
        if not self.url.startswith(("http://", "https://")):
            raise IngestError(f"source url must be http(s): {self.url!r}")
        if not self.free_public:
            raise IngestError(
                f"source {self.name!r} is not confirmed free/public; "
                "refusing to register (zero-spend rule)"
            )


class SourceRegistry:
    """The allow-list for mining. Anything unregistered is unminable."""

    def __init__(self, sources: list[Source] | None = None) -> None:
        self._sources: dict[str, Source] = {}
        for source in sources or []:
            self.register(source)

    def register(self, source: Source) -> None:
        source.validate()
        self._sources[source.name] = source

    def get(self, name: str) -> Source:
        try:
            return self._sources[name]
        except KeyError as exc:
            raise IngestError(
                f"source {name!r} is not registered; register it (with a "
                "human free/public confirmation) before mining it"
            ) from exc

    def names(self) -> list[str]:
        return sorted(self._sources)


@dataclass
class Candidate:
    """One mined technique idea, before any spec is written."""

    name: str
    source_name: str
    source_url: str
    summary: str
    license_note: str = ""
    claimed_by: str | None = None
    claimed_at: float | None = None
    status: str = "queued"  # queued | claimed | proposed | parked

    def validate(self, registry: SourceRegistry) -> None:
        if not self.name or not self.summary:
            raise IngestError("candidate needs a name and a summary")
        source = registry.get(self.source_name)
        if source.url not in self.source_url:
            raise IngestError(
                f"candidate {self.name!r} url does not match registered "
                f"source {source.name!r}"
            )
        if not self.license_note:
            raise IngestError(
                f"candidate {self.name!r} has no license note; "
                "provenance is required"
            )

    def claim_live(self, now: float | None = None) -> bool:
        if self.status != "claimed" or self.claimed_at is None:
            return False
        return (now or time.time()) - self.claimed_at < CLAIM_TTL_S


class Queue:
    """A JSON-file queue with claim/release semantics.

    File format: {"candidates": [Candidate-as-dict, ...]}. The queue
    never invents items: entries arrive only via add() or a source
    adapter's explicit output.
    """

    def __init__(self, path: str | Path, registry: SourceRegistry) -> None:
        self.path = Path(path)
        self.registry = registry
        self.candidates: list[Candidate] = []
        if self.path.exists():
            data = json.loads(self.path.read_text())
            self.candidates = [Candidate(**row) for row in data.get("candidates", [])]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        rows = [c.__dict__ for c in self.candidates]
        self.path.write_text(json.dumps({"candidates": rows}, indent=2) + "\n")

    def add(self, candidate: Candidate) -> None:
        candidate.validate(self.registry)
        if any(c.name == candidate.name for c in self.candidates):
            raise IngestError(f"candidate {candidate.name!r} already queued")
        self.candidates.append(candidate)

    def next_unclaimed(self, now: float | None = None) -> Candidate | None:
        for candidate in self.candidates:
            if candidate.status == "queued":
                return candidate
            if candidate.status == "claimed" and not candidate.claim_live(now):
                # Stale claim (> 24h): releasable, never silently dropped.
                candidate.status = "queued"
                candidate.claimed_by = None
                candidate.claimed_at = None
                return candidate
        return None

    def claim(self, candidate: Candidate, worker: str, now: float | None = None) -> None:
        if candidate.claim_live(now):
            raise IngestError(f"candidate {candidate.name!r} already claimed")
        candidate.status = "claimed"
        candidate.claimed_by = worker
        candidate.claimed_at = now or time.time()

    def release(self, candidate: Candidate, status: str) -> None:
        if status not in ("queued", "proposed", "parked"):
            raise IngestError(f"cannot release to status {status!r}")
        candidate.status = status
        candidate.claimed_by = None
        candidate.claimed_at = None


class FileSourceAdapter:
    """Turn a local JSONL file of mined notes into validated candidates.

    This is the only adapter shipped: it proves the ingest interface
    without any network fetching. Each line must be a JSON object with
    name, source_name, source_url, summary, and license_note. Web
    fetchers are a later, separately approved addition — they are not
    stubbed here, so nothing silently pretends to fetch.
    """

    def __init__(self, registry: SourceRegistry) -> None:
        self.registry = registry

    def read(self, path: str | Path) -> list[Candidate]:
        candidates = []
        for line in Path(path).read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            candidate = Candidate(
                name=row["name"],
                source_name=row["source_name"],
                source_url=row["source_url"],
                summary=row["summary"],
                license_note=row.get("license_note", ""),
            )
            candidate.validate(self.registry)
            candidates.append(candidate)
        return candidates
