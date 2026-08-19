#!/usr/bin/env python3
"""test_chatgpt_review.py — Unit and integration tests for ChatGPT review tools."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

# Add project root to sys.path
REPO_ROOT = Path(__file__).resolve().parents[3]

from ops.chatgpt_review.build_bundle import (
    BUILDER_VERSION,
    BundleBuildError,
    _is_path_forbidden,
    _parse_spec_metadata,
    _sha256_file,
    build_bundle,
)


class TestChatGPTReviewBundleBuilder(unittest.TestCase):
    """Test suite for review bundle builder."""

    def setUp(self) -> None:
        self.tmp_dir = Path(tempfile.mkdtemp(prefix="test_cg_bundle_"))
        self.spec_file = self.tmp_dir / "SPEC_TEST.md"
        self.evidence_file = self.tmp_dir / "evidence.json"
        self.out_dir = self.tmp_dir / "bundle_out"

        self.spec_file.write_text(
            """# Packet Test Spec
Packet ID: CG-TEST-01
review_class: systemic
write_set:
  - ops/chatgpt_review/build_bundle.py
  - ops/chatgpt_review/schemas/chatgpt_review_bundle.v1.schema.json

## Objective
Test objective description.
""",
            encoding="utf-8",
        )

        self.evidence_file.write_text(
            json.dumps({"test_run": "PASS", "passed": 10, "failed": 0}, indent=2),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_parse_spec_metadata(self) -> None:
        content = """# Spec
Packet ID: MY-PACKET-01
review_class: sensitive
write_set:
  - foo/bar.py
  - "baz/qux.txt"
"""
        meta = _parse_spec_metadata(content, fallback_packet_id="fallback")
        self.assertEqual(meta["packet_id"], "MY-PACKET-01")
        self.assertEqual(meta["review_class"], "sensitive")
        self.assertEqual(meta["write_set"], ["foo/bar.py", "baz/qux.txt"])

    def test_forbidden_path_detection(self) -> None:
        self.assertTrue(_is_path_forbidden(".env"))
        self.assertTrue(_is_path_forbidden("config/.env.local"))
        self.assertTrue(_is_path_forbidden("secret.key"))
        self.assertTrue(_is_path_forbidden("certs/server.pem"))
        self.assertTrue(_is_path_forbidden("credentials.json"))
        self.assertTrue(_is_path_forbidden(".git/config"))

        self.assertFalse(_is_path_forbidden("scripts/tl.py"))
        self.assertFalse(_is_path_forbidden("ops/chatgpt_review/README.md"))
        self.assertFalse(_is_path_forbidden("RELEASE_MANIFEST.json"))

    def test_invalid_sha_raises_error(self) -> None:
        with self.assertRaises(BundleBuildError) as ctx:
            build_bundle(
                packet_spec_path=self.spec_file,
                base_sha="shortsha123",
                head_sha="a" * 40,
                test_evidence_path=self.evidence_file,
                out_dir=self.out_dir,
                repo_dir=REPO_ROOT,
                allow_dirty=True,
            )
        self.assertIn("base_sha khong hop le", str(ctx.exception))

    def test_invalid_test_evidence_json(self) -> None:
        bad_evidence = self.tmp_dir / "bad_evidence.txt"
        bad_evidence.write_text("NOT JSON DATA", encoding="utf-8")

        base_sha = "3b7c83694b7b15e8f80cfd358c57c336d751120b"
        head_sha = "f926835b3c45dd5d17f7c7fa0342bf8fb65de021"

        with self.assertRaises(BundleBuildError) as ctx:
            build_bundle(
                packet_spec_path=self.spec_file,
                base_sha=base_sha,
                head_sha=head_sha,
                test_evidence_path=bad_evidence,
                out_dir=self.out_dir,
                repo_dir=REPO_ROOT,
                allow_dirty=True,
            )
        self.assertIn("test evidence khong hop le", str(ctx.exception))

    def test_successful_bundle_build_on_repo_commit(self) -> None:
        # Use actual commits from repo
        base_sha = "3b7c83694b7b15e8f80cfd358c57c336d751120b"
        head_sha = "f926835b3c45dd5d17f7c7fa0342bf8fb65de021"

        spec_file = self.tmp_dir / "SPEC_MP_T0_01.md"
        spec_file.write_text(
            """# Packet MP-T0-01
Packet ID: MP-T0-01
review_class: systemic
write_set:
  - AGENTS.md
  - ops/KE_HOACH_THI_CONG_DA_PROVIDER.md
  - ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md
  - ops/chatgpt_review/README.md
  - ops/chatgpt_review/REVIEW_PROMPT.md
  - ops/chatgpt_review/REVIEW_NOTE_TEMPLATE.yaml
  - RELEASE_MANIFEST.json
""",
            encoding="utf-8",
        )

        result = build_bundle(
            packet_spec_path=spec_file,
            base_sha=base_sha,
            head_sha=head_sha,
            test_evidence_path=self.evidence_file,
            out_dir=self.out_dir,
            repo_dir=REPO_ROOT,
            allow_dirty=True,
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["bundle_id"], f"MP-T0-01_{head_sha[:8]}")

        # Check all 8 bundle files exist
        expected_files = [
            "00_BUNDLE_MANIFEST.json",
            "01_PACKET_SPEC.md",
            "02_REVIEW_INSTRUCTIONS.md",
            "03_DIFF.patch.txt",
            "04_CHANGED_PATHS.txt",
            "05_NUMSTAT.txt",
            "06_TEST_EVIDENCE.json",
            "07_REVIEW_NOTE_TEMPLATE.yaml",
        ]
        for fname in expected_files:
            fpath = self.out_dir / fname
            self.assertTrue(fpath.exists(), f"Missing bundle file: {fname}")

        # Validate manifest content
        manifest_path = self.out_dir / "00_BUNDLE_MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual(manifest["schema"], "chatgpt_review_bundle.v1")
        self.assertEqual(manifest["base_sha"], base_sha)
        self.assertEqual(manifest["head_sha"], head_sha)
        self.assertEqual(manifest["packet_id"], "MP-T0-01")
        self.assertEqual(manifest["review_class"], "systemic")
        self.assertEqual(manifest["builder_version"], BUILDER_VERSION)
        self.assertEqual(len(manifest["files"]), 7)

        # Check manifest schema file validity
        schema_path = REPO_ROOT / "ops" / "chatgpt_review" / "schemas" / "chatgpt_review_bundle.v1.schema.json"
        self.assertTrue(schema_path.exists())
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(schema["title"], "ChatGPTReviewBundleManifestV1")

    def test_bundle_determinism_and_mutation_detection(self) -> None:
        base_sha = "3b7c83694b7b15e8f80cfd358c57c336d751120b"
        head_sha = "f926835b3c45dd5d17f7c7fa0342bf8fb65de021"

        out_dir_1 = self.tmp_dir / "bundle_1"
        out_dir_2 = self.tmp_dir / "bundle_2"

        spec_file = self.tmp_dir / "SPEC_DET.md"
        spec_file.write_text(
            """# Spec
Packet ID: DET-TEST
review_class: systemic
write_set:
  - AGENTS.md
  - ops/KE_HOACH_THI_CONG_DA_PROVIDER.md
  - ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md
  - ops/chatgpt_review/README.md
  - ops/chatgpt_review/REVIEW_PROMPT.md
  - ops/chatgpt_review/REVIEW_NOTE_TEMPLATE.yaml
  - RELEASE_MANIFEST.json
""",
            encoding="utf-8",
        )

        res1 = build_bundle(
            packet_spec_path=spec_file,
            base_sha=base_sha,
            head_sha=head_sha,
            test_evidence_path=self.evidence_file,
            out_dir=out_dir_1,
            repo_dir=REPO_ROOT,
            allow_dirty=True,
            packet_id="DET-TEST",
        )

        res2 = build_bundle(
            packet_spec_path=spec_file,
            base_sha=base_sha,
            head_sha=head_sha,
            test_evidence_path=self.evidence_file,
            out_dir=out_dir_2,
            repo_dir=REPO_ROOT,
            allow_dirty=True,
            packet_id="DET-TEST",
        )

        manifest1 = json.loads((out_dir_1 / "00_BUNDLE_MANIFEST.json").read_text(encoding="utf-8"))
        manifest2 = json.loads((out_dir_2 / "00_BUNDLE_MANIFEST.json").read_text(encoding="utf-8"))

        # Check all 7 bundle files have identical content and sha256
        for f1, f2 in zip(manifest1["files"], manifest2["files"]):
            self.assertEqual(f1["path"], f2["path"])
            self.assertEqual(f1["sha256"], f2["sha256"])
            self.assertEqual(f1["size"], f2["size"])

        # Mutation check: mutate 03_DIFF.patch.txt in bundle_1
        diff_file = out_dir_1 / "03_DIFF.patch.txt"
        original_hash = _sha256_file(diff_file)
        diff_file.write_text("MUTATED CONTENT", encoding="utf-8")
        mutated_hash = _sha256_file(diff_file)
        self.assertNotEqual(original_hash, mutated_hash)

    def test_missing_spec_or_evidence_file(self) -> None:
        base_sha = "3b7c83694b7b15e8f80cfd358c57c336d751120b"
        head_sha = "f926835b3c45dd5d17f7c7fa0342bf8fb65de021"

        missing_path = self.tmp_dir / "non_existent_file.md"

        with self.assertRaises(BundleBuildError) as ctx1:
            build_bundle(
                packet_spec_path=missing_path,
                base_sha=base_sha,
                head_sha=head_sha,
                test_evidence_path=self.evidence_file,
                out_dir=self.out_dir,
                repo_dir=REPO_ROOT,
                allow_dirty=True,
            )
        self.assertIn("spec khong ton tai", str(ctx1.exception))

        with self.assertRaises(BundleBuildError) as ctx2:
            build_bundle(
                packet_spec_path=self.spec_file,
                base_sha=base_sha,
                head_sha=head_sha,
                test_evidence_path=missing_path,
                out_dir=self.out_dir,
                repo_dir=REPO_ROOT,
                allow_dirty=True,
            )
    def test_write_set_violation_fails(self) -> None:
        base_sha = "3b7c83694b7b15e8f80cfd358c57c336d751120b"
        head_sha = "f926835b3c45dd5d17f7c7fa0342bf8fb65de021"

        spec_file = self.tmp_dir / "SPEC_TINY_WRITE_SET.md"
        spec_file.write_text(
            """# Spec
Packet ID: TINY-SET
review_class: routine
write_set:
  - only_this_file.py
""",
            encoding="utf-8",
        )

        with self.assertRaises(BundleBuildError) as ctx:
            build_bundle(
                packet_spec_path=spec_file,
                base_sha=base_sha,
                head_sha=head_sha,
                test_evidence_path=self.evidence_file,
                out_dir=self.out_dir,
                repo_dir=REPO_ROOT,
                allow_dirty=True,
            )
        self.assertIn("nam ngoai write-set", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
