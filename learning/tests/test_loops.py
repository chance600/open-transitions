"""Tests for the learning loops. Stdlib only, offline, fast.

Run from the repo root: python -m unittest discover -s learning/tests -v
"""

import json
import tempfile
import unittest
from pathlib import Path

from learning.gates import demo_verify_gate
from learning.ingest import (
    Candidate,
    FileSourceAdapter,
    IngestError,
    Queue,
    Source,
    SourceRegistry,
)
from learning.propose import propose_draft
from learning.verdicts import Verdict, promotion_gate


def registry() -> SourceRegistry:
    return SourceRegistry(
        [
            Source(
                name="cookbook",
                url="https://example.org/cookbook",
                kind="repo",
                free_public=True,
                license_note="MIT",
            )
        ]
    )


def candidate() -> Candidate:
    return Candidate(
        name="merge_hold_handover",
        source_name="cookbook",
        source_url="https://example.org/cookbook#merge",
        summary="Merge, hold, hand over.",
        license_note="MIT",
    )


class TestIngest(unittest.TestCase):
    def test_paid_source_refused(self):
        with self.assertRaises(IngestError):
            SourceRegistry(
                [Source(name="paid", url="https://example.org/p", kind="course", free_public=False)]
            )

    def test_unregistered_source_refused(self):
        with self.assertRaises(IngestError):
            candidate().validate(SourceRegistry())

    def test_missing_provenance_refused(self):
        bad = candidate()
        bad.license_note = ""
        with self.assertRaises(IngestError):
            bad.validate(registry())

    def test_claim_blocks_double_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = Queue(Path(tmp) / "q.json", registry())
            queue.add(candidate())
            first = queue.next_unclaimed()
            queue.claim(first, "worker-a")
            self.assertIsNone(queue.next_unclaimed())
            queue.release(first, "proposed")
            self.assertIsNone(queue.next_unclaimed())

    def test_stale_claim_releasable(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = Queue(Path(tmp) / "q.json", registry())
            queue.add(candidate())
            item = queue.next_unclaimed()
            queue.claim(item, "worker-a", now=1000.0)
            # 25h later: claim expired, item returns to the queue.
            self.assertIsNotNone(queue.next_unclaimed(now=1000.0 + 25 * 3600))

    def test_file_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "notes.jsonl"
            path.write_text(json.dumps(candidate().__dict__) + "\n")
            rows = FileSourceAdapter(registry()).read(path)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0].name, "merge_hold_handover")


class TestPropose(unittest.TestCase):
    def test_draft_written_and_not_clobbered(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = propose_draft(candidate(), tmp)
            self.assertTrue(path.exists())
            self.assertIn("DRAFT", path.read_text())
            with self.assertRaises(FileExistsError):
                propose_draft(candidate(), tmp)


class TestVerdicts(unittest.TestCase):
    def test_machine_only_never_promotes(self):
        verdicts = [
            Verdict("A x B", "t1", "pass", "machine"),
            Verdict("A x B", "t1", "pass", "machine"),
        ]
        self.assertFalse(promotion_gate("t1", verdicts)[0])

    def test_no_verdict_never_promotes(self):
        self.assertFalse(promotion_gate("t1", [])[0])

    def test_human_pass_promotes(self):
        verdicts = [Verdict("A x B", "t1", "pass", "human", heart=True)]
        ok, _ = promotion_gate("t1", verdicts)
        self.assertTrue(ok)

    def test_later_human_reject_blocks(self):
        verdicts = [
            Verdict("A x B", "t1", "pass", "human"),
            Verdict("A x B", "t1", "reject", "human"),
        ]
        self.assertFalse(promotion_gate("t1", verdicts)[0])

    def test_partial_alone_never_promotes(self):
        verdicts = [Verdict("A x B", "t1", "partial", "human")]
        self.assertFalse(promotion_gate("t1", verdicts)[0])


class TestGates(unittest.TestCase):
    def test_demo_gate_requires_meta_and_clean_verification(self):
        meta = {"t1": {"title": "T1"}}
        clean = [{"technique": "t1", "render_ok": True, "silence_ok": True, "headroom_ok": True}]
        self.assertTrue(demo_verify_gate("t1", meta, clean)[0])
        self.assertFalse(demo_verify_gate("missing", meta, clean)[0])
        dirty = [{"technique": "t1", "render_ok": True, "silence_ok": False, "headroom_ok": True}]
        self.assertFalse(demo_verify_gate("t1", meta, dirty)[0])


if __name__ == "__main__":
    unittest.main()
