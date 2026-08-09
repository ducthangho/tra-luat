# -*- coding: utf-8 -*-
"""WP68 — nested repository copies must not contaminate release artifacts.

The regression uses the release manifest/verify seam on real temporary trees. Two
independent safety layers are exercised separately:

* a copy is ignored only when all three repository markers are present; and
* excluding a path already named by the current manifest always fails closed.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path


TEST_ID = "wp68_release_exclude_nested_repo"


_MARKERS = ("SKILL.md", "VERSION", "scripts/tl.py")
_MANIFESTED_SENTINEL = "agents/openai.yaml"


def _source_root(tl_module):
    return Path(tl_module.__file__).resolve().parent.parent


def _write(root, rel, data=None):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = data if data is not None else ("fixture:" + rel + "\n").encode("utf-8")
    path.write_bytes(payload)


def _baseline(tl_module, root):
    source = json.loads((_source_root(tl_module) / "RELEASE_MANIFEST.json").read_text(encoding="utf-8"))
    for record in source.get("files", []):
        rel = str(record.get("path") or "")
        if rel:
            _write(root, rel)
    # WP68-R2-CODEX-01: this file is intentionally inside the directory where
    # marker collisions are planted, and therefore belongs to the baseline.
    _write(root, _MANIFESTED_SENTINEL)
    manifest = tl_module._build_release_manifest(root)
    if not manifest.get("ok"):
        return None
    return manifest


def _plant_markers(root, rel, count=3):
    for marker in _MARKERS[:count]:
        _write(root / rel, marker)


def _verify(tl_module, root, manifest):
    return tl_module._verify_release_manifest(root, manifest, strict=True)


def _full_copy_is_ignored(tl_module):
    with tempfile.TemporaryDirectory(prefix="wp68_full_") as temp:
        root = Path(temp)
        manifest = _baseline(tl_module, root)
        if manifest is None:
            return False
        _plant_markers(root, "sandbox/full", 3)
        _write(root / "sandbox/full", "payload.txt")
        result = _verify(tl_module, root, manifest)
        current = tl_module._build_release_manifest(root)
        return bool(
            result.get("ok") is True
            and result.get("extra_files") == []
            and result.get("missing_from_current_manifest") == []
            and current.get("file_count") == manifest.get("file_count")
            and current.get("package_hash") == manifest.get("package_hash")
        )


def _partial_copies_remain_visible(tl_module):
    cases = (
        ("sandbox/two-markers", 2, {"sandbox/two-markers/SKILL.md", "sandbox/two-markers/VERSION"}),
        ("sandbox/scripts-only", 0, {"sandbox/scripts-only/scripts/tl.py"}),
    )
    for rel, marker_count, expected_extra in cases:
        with tempfile.TemporaryDirectory(prefix="wp68_partial_") as temp:
            root = Path(temp)
            manifest = _baseline(tl_module, root)
            if manifest is None:
                return False
            if marker_count:
                _plant_markers(root, rel, marker_count)
            else:
                _write(root / rel, "scripts/tl.py")
            result = _verify(tl_module, root, manifest)
            if not (
                result.get("ok") is False
                and set(result.get("extra_files") or []) == expected_extra
                and result.get("missing_from_current_manifest") == []
            ):
                return False
    return True


def _manifested_path_exclusion_fails_closed(tl_module):
    with tempfile.TemporaryDirectory(prefix="wp68_counterexample_") as temp:
        root = Path(temp)
        manifest = _baseline(tl_module, root)
        if manifest is None:
            return False
        _plant_markers(root, "agents", 3)
        result = _verify(tl_module, root, manifest)
        missing = set(result.get("missing_from_current_manifest") or [])
        # No extra-file signal remains after marker-based exclusion. The red
        # verdict therefore comes solely from the current-manifest safety layer.
        return bool(
            result.get("ok") is False
            and result.get("extra_files") == []
            and _MANIFESTED_SENTINEL in missing
            and not result.get("failed")
        )


def _root_is_not_self_excluded(tl_module):
    with tempfile.TemporaryDirectory(prefix="wp68_root_") as temp:
        root = Path(temp)
        manifest = _baseline(tl_module, root)
        if manifest is None:
            return False
        paths = {record.get("path") for record in manifest.get("files", [])}
        return all(marker in paths for marker in _MARKERS)


def run(tl_module):
    return bool(
        _full_copy_is_ignored(tl_module)
        and _partial_copies_remain_visible(tl_module)
        and _manifested_path_exclusion_fails_closed(tl_module)
        and _root_is_not_self_excluded(tl_module)
    )
