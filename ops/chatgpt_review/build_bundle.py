#!/usr/bin/env python3
"""build_bundle.py — Build a frozen review bundle for ChatGPT Pro Web review.

Assurance: advisory_review
Schema: chatgpt_review_bundle.v1
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
from typing import Any, Dict, List, Optional, Set

BUILDER_VERSION = "1.0.0"
HEX_40_RE = re.compile(r"^[0-9a-f]{40}$")

FORBIDDEN_PATH_PATTERNS = [
    re.compile(r"(^|/)\.env.*$", re.IGNORECASE),
    re.compile(r"(^|/)id_rsa.*$", re.IGNORECASE),
    re.compile(r".*\.(key|pem|p12|pfx|pkcs12)$", re.IGNORECASE),
    re.compile(r".*credential.*", re.IGNORECASE),
    re.compile(r".*secret.*", re.IGNORECASE),
    re.compile(r".*token.*", re.IGNORECASE),
    re.compile(r"(^|/)\.git/.*"),
]


class BundleBuildError(Exception):
    """Raised when bundle building fails validation."""


def _chay_git(args: List[str], cwd: Path) -> str:
    """Run a git command safely with utf-8 encoding."""
    cmd = ["git"] + args
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except Exception as exc:
        raise BundleBuildError(f"Khong the thuc thi git command {cmd}: {exc}") from exc

    if proc.returncode != 0:
        raise BundleBuildError(
            f"Git command {cmd} that bai (rc={proc.returncode}): {proc.stderr.strip()}"
        )
    return proc.stdout


def _sha256_file(path: Path) -> str:
    """Calculate SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def _is_path_forbidden(rel_path: str) -> bool:
    """Check if a path matches forbidden secret/sensitive patterns."""
    norm = rel_path.replace("\\", "/").strip()
    return any(pat.search(norm) for pat in FORBIDDEN_PATH_PATTERNS)


def _parse_spec_metadata(spec_content: str, fallback_packet_id: str) -> Dict[str, Any]:
    """Parse packet metadata (packet_id, write_set, review_class) from spec markdown."""
    packet_id = fallback_packet_id
    write_set: List[str] = []
    review_class = "systemic"

    # Match packet_id / Packet ID / Packet: <id>
    m_id = re.search(r"(?:Packet\s*(?:ID)?|packet_id)\s*[:=]\s*([A-Za-z0-9._-]+)", spec_content, re.IGNORECASE)
    if m_id:
        packet_id = m_id.group(1).strip()

    # Match review_class: routine | systemic | sensitive
    m_rc = re.search(r"review_class\s*[:=]\s*(routine|systemic|sensitive)", spec_content, re.IGNORECASE)
    if m_rc:
        review_class = m_rc.group(1).strip().lower()

    # Match write_set YAML-like block or list
    m_ws = re.search(r"write_set\s*:\s*\n((?:\s*-\s*.+\n)+)", spec_content, re.IGNORECASE)
    if m_ws:
        for line in m_ws.group(1).splitlines():
            item = line.strip()
            if item.startswith("-"):
                item_val = item.lstrip("-").strip().strip('"').strip("'")
                if item_val:
                    write_set.append(item_val)

    return {
        "packet_id": packet_id,
        "review_class": review_class,
        "write_set": write_set,
    }


def build_bundle(
    packet_spec_path: Path,
    base_sha: str,
    head_sha: str,
    test_evidence_path: Path,
    out_dir: Path,
    repo_dir: Optional[Path] = None,
    packet_id: Optional[str] = None,
    review_class: Optional[str] = None,
    write_set: Optional[List[str]] = None,
    allow_dirty: bool = False,
) -> Dict[str, Any]:
    """Build a frozen ChatGPT Pro review bundle in out_dir."""
    if repo_dir is None:
        repo_dir = Path.cwd()
    repo_dir = repo_dir.resolve()

    # 1. Validate full 40-char lowercase hex SHAs
    base_sha = base_sha.strip().lower()
    head_sha = head_sha.strip().lower()

    if not HEX_40_RE.match(base_sha):
        raise BundleBuildError(f"base_sha khong hop le (phai du 40 ky tu hex thuong): {base_sha}")
    if not HEX_40_RE.match(head_sha):
        raise BundleBuildError(f"head_sha khong hop le (phai du 40 ky tu hex thuong): {head_sha}")

    # 2. Validate tree_sha
    tree_out = _chay_git(["rev-parse", f"{head_sha}^{{tree}}"], cwd=repo_dir).strip().lower()
    if not HEX_40_RE.match(tree_out):
        raise BundleBuildError(f"Khong the trich xuat tree_sha hop le tu head_sha {head_sha}: {tree_out}")
    tree_sha = tree_out

    # 3. Check dirty worktree unless allow_dirty is true
    if not allow_dirty:
        status_out = _chay_git(["status", "--porcelain"], cwd=repo_dir).strip()
        if status_out:
            lines = [l for l in status_out.splitlines() if not l.startswith("?? work/reviews")]
            if lines:
                raise BundleBuildError(
                    f"Worktree khong sach. Yeu cau commit hoac stash truoc khi dong bang bundle: {lines[:3]}"
                )

    # 4. Read packet spec
    if not packet_spec_path.exists():
        raise BundleBuildError(f"Tep packet spec khong ton tai: {packet_spec_path}")
    try:
        spec_content = packet_spec_path.read_text(encoding="utf-8")
    except Exception as exc:
        raise BundleBuildError(f"Khong the doc packet spec {packet_spec_path}: {exc}") from exc

    # Fallback packet_id from filename stem
    stem_id = packet_spec_path.stem
    spec_meta = _parse_spec_metadata(spec_content, fallback_packet_id=stem_id)

    effective_packet_id = packet_id or spec_meta["packet_id"]
    effective_review_class = review_class or spec_meta["review_class"]
    effective_write_set = write_set if write_set is not None else spec_meta["write_set"]

    if effective_review_class not in ("routine", "systemic", "sensitive"):
        raise BundleBuildError(f"review_class khong hop le: {effective_review_class}")

    # 5. Read test evidence
    if not test_evidence_path.exists():
        raise BundleBuildError(f"Tep test evidence khong ton tai: {test_evidence_path}")
    try:
        test_evidence_raw = test_evidence_path.read_text(encoding="utf-8")
        test_evidence_json = json.loads(test_evidence_raw)
    except Exception as exc:
        raise BundleBuildError(f"Tep test evidence khong hop le hoac khong parse duoc JSON: {exc}") from exc

    # 6. Extract diff, changed paths, numstat
    diff_text = _chay_git(["diff", base_sha, head_sha], cwd=repo_dir)
    changed_paths_raw = _chay_git(["diff", "--name-only", base_sha, head_sha], cwd=repo_dir)
    numstat_text = _chay_git(["diff", "--numstat", base_sha, head_sha], cwd=repo_dir)

    changed_paths = [p.strip() for p in changed_paths_raw.splitlines() if p.strip()]

    # 7. Validate forbidden paths
    for p in changed_paths:
        if _is_path_forbidden(p):
            raise BundleBuildError(f"Phat hien duong dan cam/nhay cam trong diff: {p}")

    # 8. Validate write-set if declared
    if effective_write_set:
        declared_set = set(effective_write_set)
        for p in changed_paths:
            # Check direct match or directory match
            if p not in declared_set and not any(p.startswith(d.rstrip("/") + "/") for d in declared_set if d.endswith("/")):
                raise BundleBuildError(
                    f"Duong dan thay doi '{p}' nam ngoai write-set duoc khai bao: {sorted(declared_set)}"
                )

    # 9. Read review prompt template
    prompt_file = repo_dir / "ops" / "chatgpt_review" / "REVIEW_PROMPT.md"
    if prompt_file.exists():
        instructions_text = prompt_file.read_text(encoding="utf-8")
    else:
        instructions_text = (
            "Ban la Reviewer read-only cho repository tra-luat.\n"
            "Chi su dung cac tep trong review bundle duoc tai len.\n"
            "Kiem tra hai truc: Spec va Standards/Security.\n"
        )

    # 10. Prepare out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    bundle_id = f"{effective_packet_id}_{head_sha[:8]}"

    # Template content with prepopulated exact reviewed SHA/tree
    note_template_text = f"""format: temporary_chatgpt_review_note.v0
provider: openai_chatgpt
execution_surface: chatgpt_web
transport: human_mediated
account_plan: pro
bundle_id: {bundle_id}
bundle_sha256: <FILL_FROM_VALIDATION_RECEIPT_OR_MANIFEST>
reviewed_sha: {head_sha}
reviewed_tree: {tree_sha}
verdict: approve # approve | changes_requested | blocked
review_axes:
  - spec
  - standards_security
findings: []
  # - finding_id: stable-kebab-slug
  #   severity: P1 # P0 | P1 | P2 | P3
  #   path: relative/path/to/file.py # or null
  #   line: 100 # or null
  #   evidence: "Description of issue"
  #   recommendation: "Suggested fix"
tests:
  independently_run: false
  evidence_reviewed: []
limitations:
  - human_mediated_transport
  - model_identity_not_machine_verified
  - tests_not_run_by_chatgpt
assurance: advisory_review
"""

    bundle_files_to_write = {
        "01_PACKET_SPEC.md": spec_content,
        "02_REVIEW_INSTRUCTIONS.md": instructions_text,
        "03_DIFF.patch.txt": diff_text,
        "04_CHANGED_PATHS.txt": "\n".join(changed_paths) + ("\n" if changed_paths else ""),
        "05_NUMSTAT.txt": numstat_text,
        "06_TEST_EVIDENCE.json": json.dumps(test_evidence_json, indent=2, ensure_ascii=False) + "\n",
        "07_REVIEW_NOTE_TEMPLATE.yaml": note_template_text,
    }

    # Write the 7 files
    for fname, content in bundle_files_to_write.items():
        fpath = out_dir / fname
        fpath.write_text(content, encoding="utf-8", newline="\n")

    # Hash the 7 files
    files_entries: List[Dict[str, Any]] = []
    for fname in sorted(bundle_files_to_write.keys()):
        fpath = out_dir / fname
        files_entries.append({
            "path": fname,
            "sha256": _sha256_file(fpath),
            "size": fpath.stat().st_size,
        })

    manifest: Dict[str, Any] = {
        "schema": "chatgpt_review_bundle.v1",
        "bundle_id": bundle_id,
        "packet_id": effective_packet_id,
        "base_sha": base_sha,
        "head_sha": head_sha,
        "tree_sha": tree_sha,
        "write_set": effective_write_set,
        "review_class": effective_review_class,
        "files": files_entries,
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "builder_version": BUILDER_VERSION,
    }

    manifest_path = out_dir / "00_BUNDLE_MANIFEST.json"
    manifest_content = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    manifest_path.write_text(manifest_content, encoding="utf-8", newline="\n")

    manifest_sha256 = _sha256_file(manifest_path)

    return {
        "ok": True,
        "bundle_id": bundle_id,
        "bundle_dir": str(out_dir),
        "manifest_path": str(manifest_path),
        "manifest_sha256": manifest_sha256,
        "head_sha": head_sha,
        "tree_sha": tree_sha,
        "file_count": len(files_entries) + 1,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a review bundle for ChatGPT Pro Web")
    parser.add_argument("--packet-spec", required=True, type=Path, help="Path to Packet Spec markdown")
    parser.add_argument("--base-sha", required=True, type=str, help="40-char base Git SHA")
    parser.add_argument("--head-sha", required=True, type=str, help="40-char head Git SHA")
    parser.add_argument("--test-evidence", required=True, type=Path, help="Path to test evidence JSON")
    parser.add_argument("--out", required=True, type=Path, help="Output directory for bundle")
    parser.add_argument("--repo", type=Path, default=None, help="Repository root directory")
    parser.add_argument("--packet-id", type=str, default=None, help="Packet identifier")
    parser.add_argument("--review-class", type=str, choices=["routine", "systemic", "sensitive"], default=None)
    parser.add_argument("--write-set", type=str, default=None, help="Comma-separated write set paths")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow dirty worktree (test only)")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")

    args = parser.parse_args()

    write_set_list = None
    if args.write_set:
        write_set_list = [p.strip() for p in args.write_set.split(",") if p.strip()]

    try:
        result = build_bundle(
            packet_spec_path=args.packet_spec,
            base_sha=args.base_sha,
            head_sha=args.head_sha,
            test_evidence_path=args.test_evidence,
            out_dir=args.out,
            repo_dir=args.repo,
            packet_id=args.packet_id,
            review_class=args.review_class,
            write_set=write_set_list,
            allow_dirty=args.allow_dirty,
        )
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Bundle {result['bundle_id']} tao thanh cong tai: {result['bundle_dir']}")
            print(f"Manifest SHA256: {result['manifest_sha256']}")
        return 0
    except Exception as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, indent=2, ensure_ascii=False))
        else:
            print(f"Loi build bundle: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
