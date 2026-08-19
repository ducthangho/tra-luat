#!/usr/bin/env python3
"""validate_note.py — Validate a ChatGPT Pro review note against a review bundle and repo state.

Assurance: advisory_review
Receipt Schema: chatgpt_review_validation_receipt.v1
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

VALIDATOR_VERSION = "1.0.0"
HEX_40_RE = re.compile(r"^[0-9a-f]{40}$")
KEBAB_CASE_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ALLOWED_VERDICTS = {"approve", "changes_requested", "blocked"}
ALLOWED_SEVERITIES = {"P0", "P1", "P2", "P3"}
ALLOWED_ACCOUNT_PLANS = {"pro", "plus", "team", "enterprise"}


class NoteValidationError(Exception):
    """Raised when review note fails validation rules."""


class DuplicateKeyError(NoteValidationError):
    """Raised when duplicate keys are found in YAML mapping."""


class UniqueKeyYamlLoader(yaml.SafeLoader):
    """Custom SafeLoader enforcing no duplicate keys in YAML mappings."""

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> Dict[Any, Any]:
        mapping: Dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                raise DuplicateKeyError(f"Duplicate key '{key}' phat hien trong YAML review note tai dong {key_node.start_mark.line + 1}")
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def _sha256_file(path: Path) -> str:
    """Calculate SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def _sha256_bytes(data: bytes) -> str:
    """Calculate SHA256 of bytes."""
    return hashlib.sha256(data).hexdigest()


def parse_yaml_strict(text: str) -> Dict[str, Any]:
    """Parse YAML string with strict duplicate key prevention."""
    try:
        data = yaml.load(text, Loader=UniqueKeyYamlLoader)
    except DuplicateKeyError as exc:
        raise exc
    except Exception as exc:
        raise NoteValidationError(f"Khong the parse YAML: {exc}") from exc

    if not isinstance(data, dict):
        raise NoteValidationError(f"Root cua review note phai la YAML mapping/dict, nhan duoc: {type(data).__name__}")
    return data


def validate_review_note(
    note_path: Path,
    bundle_manifest_path: Path,
    repo_dir: Optional[Path] = None,
    pr_number: Optional[int] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Validate review note against bundle manifest and git repo state.

    Returns (receipt_dict, parsed_note_dict).
    """
    if not note_path.exists():
        raise NoteValidationError(f"Tep review note khong ton tai: {note_path}")
    if not bundle_manifest_path.exists():
        raise NoteValidationError(f"Tep bundle manifest khong ton tai: {bundle_manifest_path}")

    # 1. Read and parse YAML strictly
    note_bytes = note_path.read_bytes()
    note_sha256 = _sha256_bytes(note_bytes)
    note_text = note_bytes.decode("utf-8", errors="replace")
    note = parse_yaml_strict(note_text)

    # 2. Read and parse bundle manifest
    try:
        manifest_raw = bundle_manifest_path.read_text(encoding="utf-8")
        manifest = json.loads(manifest_raw)
    except Exception as exc:
        raise NoteValidationError(f"Khong the doc hoac parse bundle manifest {bundle_manifest_path}: {exc}") from exc

    bundle_dir = bundle_manifest_path.parent
    bundle_manifest_sha256 = _sha256_file(bundle_manifest_path)

    # 3. Check format
    if note.get("format") != "temporary_chatgpt_review_note.v0":
        raise NoteValidationError(
            f"format khong hop le: '{note.get('format')}', ky vong 'temporary_chatgpt_review_note.v0'"
        )

    # 4. Check provider, execution_surface, transport, account_plan
    provider = note.get("provider")
    if provider != "openai_chatgpt":
        raise NoteValidationError(f"provider khong hop le: '{provider}', ky vong 'openai_chatgpt'")

    surface = note.get("execution_surface")
    if surface != "chatgpt_web":
        raise NoteValidationError(f"execution_surface khong hop le: '{surface}', ky vong 'chatgpt_web'")

    transport = note.get("transport")
    if transport != "human_mediated":
        raise NoteValidationError(f"transport khong hop le: '{transport}', ky vong 'human_mediated'")

    plan = note.get("account_plan")
    if plan not in ALLOWED_ACCOUNT_PLANS:
        raise NoteValidationError(f"account_plan khong hop le: '{plan}', cho phep: {sorted(ALLOWED_ACCOUNT_PLANS)}")

    # 5. Check reviewed_sha and reviewed_tree
    reviewed_sha = str(note.get("reviewed_sha", "")).strip().lower()
    reviewed_tree = str(note.get("reviewed_tree", "")).strip().lower()

    if not HEX_40_RE.match(reviewed_sha):
        raise NoteValidationError(f"reviewed_sha khong du 40 ky tu hex thuong: '{reviewed_sha}'")
    if not HEX_40_RE.match(reviewed_tree):
        raise NoteValidationError(f"reviewed_tree khong du 40 ky tu hex thuong: '{reviewed_tree}'")

    # 6. Check match against bundle manifest
    if manifest.get("schema") != "chatgpt_review_bundle.v1":
        raise NoteValidationError(f"bundle manifest schema khong hop le: '{manifest.get('schema')}'")

    expected_bundle_id = manifest.get("bundle_id")
    note_bundle_id = note.get("bundle_id")
    if note_bundle_id != expected_bundle_id:
        raise NoteValidationError(
            f"bundle_id trong note ('{note_bundle_id}') khong khop voi manifest ('{expected_bundle_id}')"
        )

    manifest_head_sha = str(manifest.get("head_sha", "")).strip().lower()
    manifest_tree_sha = str(manifest.get("tree_sha", "")).strip().lower()

    if reviewed_sha != manifest_head_sha:
        raise NoteValidationError(
            f"reviewed_sha trong note ('{reviewed_sha}') khong khop voi bundle manifest ('{manifest_head_sha}')"
        )
    if reviewed_tree != manifest_tree_sha:
        raise NoteValidationError(
            f"reviewed_tree trong note ('{reviewed_tree}') khong khop voi bundle manifest ('{manifest_tree_sha}')"
        )

    # 7. Check bundle file hashes on disk
    manifest_files = manifest.get("files", [])
    if not manifest_files:
        raise NoteValidationError("Bundle manifest khong co danh sach files")

    for f_entry in manifest_files:
        f_rel = f_entry.get("path")
        f_expected_sha = f_entry.get("sha256")
        f_path = bundle_dir / f_rel
        if not f_path.exists():
            raise NoteValidationError(f"Tep trong bundle khong ton tai tren dia: {f_path}")
        f_actual_sha = _sha256_file(f_path)
        if f_actual_sha != f_expected_sha:
            raise NoteValidationError(
                f"Bundle file '{f_rel}' bi sua doi! SHA256 thuc te '{f_actual_sha}' != manifest '{f_expected_sha}'"
            )

    # 8. Check verdict
    verdict = note.get("verdict")
    if verdict not in ALLOWED_VERDICTS:
        raise NoteValidationError(f"verdict khong hop le: '{verdict}', cho phep: {sorted(ALLOWED_VERDICTS)}")

    # 9. Check findings
    findings = note.get("findings")
    if not isinstance(findings, list):
        raise NoteValidationError("findings phai la danh sach (list)")

    seen_finding_ids: Set[str] = set()
    for idx, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise NoteValidationError(f"Finding thu {idx+1} khong phai dict")

        f_id = finding.get("finding_id")
        if not f_id or not isinstance(f_id, str) or not KEBAB_CASE_RE.match(f_id):
            raise NoteValidationError(
                f"finding_id '{f_id}' khong dung format kebab-case (vd: 'stale-sha-detected')"
            )
        if f_id in seen_finding_ids:
            raise NoteValidationError(f"Trung lap finding_id: '{f_id}'")
        seen_finding_ids.add(f_id)

        sev = finding.get("severity")
        if sev not in ALLOWED_SEVERITIES:
            raise NoteValidationError(f"Finding '{f_id}' co severity khong hop le: '{sev}', cho phep: {sorted(ALLOWED_SEVERITIES)}")

        # Path check (repo-relative, no traversal, not absolute)
        f_path = finding.get("path")
        if f_path is not None and isinstance(f_path, str) and f_path.strip():
            f_path_norm = f_path.strip().replace("\\", "/")
            if f_path_norm.startswith("/") or re.match(r"^[a-zA-Z]:", f_path_norm):
                raise NoteValidationError(f"Finding '{f_id}' co path tuyet doi khong hop le: '{f_path}'")
            if ".." in f_path_norm.split("/"):
                raise NoteValidationError(f"Finding '{f_id}' chua path traversal '..': '{f_path}'")

        if not finding.get("evidence"):
            raise NoteValidationError(f"Finding '{f_id}' thieu truong 'evidence'")
        if not finding.get("recommendation"):
            raise NoteValidationError(f"Finding '{f_id}' thieu truong 'recommendation'")

    # 10. Check tests
    tests_block = note.get("tests")
    if not isinstance(tests_block, dict):
        raise NoteValidationError("Truong 'tests' phai la dictionary")
    if tests_block.get("independently_run") is not False:
        raise NoteValidationError(
            "tests.independently_run phai la false (ChatGPT Web khong duoc phep khai da chay test doc lap)"
        )

    # 11. Check limitations
    limitations = note.get("limitations")
    if not isinstance(limitations, list) or len(limitations) == 0:
        raise NoteValidationError("Truong 'limitations' phai la danh sach khong rong")

    # 12. Check assurance
    assurance = note.get("assurance")
    if assurance != "advisory_review":
        raise NoteValidationError(
            f"assurance khong hop le: '{assurance}', ChatGPT Web bat buoc phai mang 'advisory_review'"
        )

    # 13. Local git head check
    local_head_matches = True
    if repo_dir is not None:
        try:
            local_head = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=True,
            ).stdout.strip().lower()
            local_head_matches = (local_head == reviewed_sha)
        except Exception:
            local_head_matches = False

    # 14. GitHub PR head check if requested
    github_pr_head_matches: Any = "unavailable"
    if pr_number is not None:
        try:
            pr_out = subprocess.run(
                ["gh", "pr", "view", str(pr_number), "--json", "headRefOid"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            if pr_out.returncode == 0:
                pr_data = json.loads(pr_out.stdout)
                remote_head = pr_data.get("headRefOid", "").strip().lower()
                github_pr_head_matches = (remote_head == reviewed_sha)
                if not github_pr_head_matches:
                    raise NoteValidationError(
                        f"Remote PR #{pr_number} head ('{remote_head}') khong khop reviewed_sha ('{reviewed_sha}')"
                    )
            else:
                github_pr_head_matches = "unavailable"
        except Exception as exc:
            if isinstance(exc, NoteValidationError):
                raise exc
            github_pr_head_matches = "unavailable"

    # Construct validation receipt
    receipt: Dict[str, Any] = {
        "format": "chatgpt_review_validation_receipt.v1",
        "review_note_sha256": note_sha256,
        "bundle_id": expected_bundle_id,
        "bundle_sha256": bundle_manifest_sha256,
        "schema_valid": True,
        "bundle_valid": True,
        "reviewed_sha_matches_bundle": True,
        "reviewed_tree_matches_bundle": True,
        "local_head_matches": local_head_matches,
        "github_pr_head_matches": github_pr_head_matches,
        "provider_claim_valid": True,
        "transport_claim_valid": True,
        "finding_ids_valid": True,
        "model_identity_verified": False,
        "session_identity_verified": False,
        "authoritative_assurance": "review_deferred",
        "advisory_assurance": "advisory_review",
        "validator_version": VALIDATOR_VERSION,
        "validated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    return receipt, note


def render_markdown_comment(receipt: Dict[str, Any], note: Dict[str, Any]) -> str:
    """Render a markdown summary with embedded YAML review note and receipt for GitHub PR comment."""
    verdict = note.get("verdict", "unknown")
    verdict_emoji = "✅ APPROVE (ADVISORY)" if verdict == "approve" else ("⚠️ CHANGES REQUESTED" if verdict == "changes_requested" else "⛔ BLOCKED")
    findings_count = len(note.get("findings", []))

    lines = [
        f"### ChatGPT Pro Advisory Review Verdict: {verdict_emoji}",
        "",
        f"- **Reviewed SHA**: `{note.get('reviewed_sha')}`",
        f"- **Bundle ID**: `{receipt.get('bundle_id')}`",
        f"- **Bundle SHA256**: `{receipt.get('bundle_sha256')}`",
        f"- **Findings**: `{findings_count}` finding(s)",
        f"- **Assurance**: `advisory_review` (validated locally via `validate_note.py`)",
        "",
        "```yaml",
        yaml.dump(note, sort_keys=False, allow_unicode=True).strip(),
        "```",
        "",
        "<details>",
        "<summary>Validation Receipt (chatgpt_review_validation_receipt.v1)</summary>",
        "",
        "```yaml",
        yaml.dump(receipt, sort_keys=False, allow_unicode=True).strip(),
        "```",
        "",
        "</details>",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ChatGPT Pro review note against bundle")
    parser.add_argument("--note", required=True, type=Path, help="Path to ChatGPT review note YAML")
    parser.add_argument("--bundle", required=True, type=Path, help="Path to 00_BUNDLE_MANIFEST.json")
    parser.add_argument("--repo", type=Path, default=None, help="Repository root directory")
    parser.add_argument("--pr", type=int, default=None, help="Optional GitHub PR number to verify headRefOid")
    parser.add_argument("--receipt-out", type=Path, default=None, help="Path to save validation receipt YAML")
    parser.add_argument("--render-out", type=Path, default=None, help="Path to save rendered PR comment markdown")
    parser.add_argument("--json", action="store_true", help="Output JSON receipt on stdout")

    args = parser.parse_args()

    try:
        receipt, note = validate_review_note(
            note_path=args.note,
            bundle_manifest_path=args.bundle,
            repo_dir=args.repo,
            pr_number=args.pr,
        )

        # Write receipt if requested
        if args.receipt_out:
            args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
            args.receipt_out.write_text(
                yaml.dump(receipt, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
                newline="\n",
            )

        # Write rendered markdown if requested
        if args.render_out:
            args.render_out.parent.mkdir(parents=True, exist_ok=True)
            args.render_out.write_text(
                render_markdown_comment(receipt, note),
                encoding="utf-8",
                newline="\n",
            )

        if args.json:
            print(json.dumps(receipt, indent=2, ensure_ascii=False))
        else:
            print(f"VALIDATION PASSED (verdict={note.get('verdict')})")
            print(f"Receipt SHA256: {receipt['review_note_sha256']}")
        return 0
    except Exception as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, indent=2, ensure_ascii=False))
        else:
            print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
