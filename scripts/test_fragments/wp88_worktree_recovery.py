# -*- coding: utf-8 -*-
"""Positive recovery evidence for wp88 rows 1, 46, and 90."""

TEST_ID = "wp88_worktree_recovery"


def run(tl_module):
    import hashlib
    import importlib
    import os
    from pathlib import Path
    import subprocess
    import tempfile

    root = Path(__file__).resolve().parents[2]
    expected_docs = {
        "docs/research/2026-08-04-kiem-chung-auth-fail-close-codex-claude.md":
            "9db028636b77d6e93c82ccc27ddcec12cb9e8c9d51b4f0f0691313697e1b969d",
        "docs/research/2026-08-04-kiem-chung-phuong-an-subscription-codex-claude.md":
            "90bc4509ee829157bae5612c6c470c1369a700ad9b98ef1841eefe89ca559f6f",
        "docs/research/2026-08-04-lua-chon-orchestrator-da-model-codex-claude.md":
            "0d92c0ba751e54be1357a9709ee4bff7463086290e229b1f837c99675a2a7eec",
        "docs/research/2026-08-04-so-sanh-gh-aw-bernstein-agent-orchestrator-metaswarm.md":
            "9c1a3bd4bf826991d8a220f1356b940bdc13fa8db0f88df7c474f1273b70062b",
        "docs/research/2026-08-05-kiem-chung-claude-bare-va-auth-gate.md":
            "d782436174b01e3dc5843a335cf6e2539107f9ef4c2c0c10a21371b8cfdc5d22",
    }
    present_docs = [rel for rel in expected_docs if (root / rel).is_file()]
    if present_docs and len(present_docs) != len(expected_docs):
        return False
    if any(hashlib.sha256((root / rel).read_bytes()).hexdigest() != expected_docs[rel]
           for rel in present_docs):
        return False

    loader = importlib.import_module("tl_core.test_fragments")
    source_ids = set(loader.discover_harness_test_ids(root / "scripts" / "tl_selftest.py"))
    superseded_ids = {
        "wp41_fragment_loader_zero",
        "wp41_fragment_loader_one",
        "wp41_fragment_loader_many_deterministic",
        "wp41_fragment_duplicate_path_rejected",
        "wp41_fragment_duplicate_wp_id_rejected",
        "wp41_fragment_grandfather_exact_only",
        "wp41_fragment_malformed_contract_rejected",
        "wp41_fragment_syntax_error_diagnosable",
        "wp41_fragment_import_error_diagnosable",
        "wp41_fragment_path_traversal_rejected",
        "wp41_fragment_invalid_path_rejected",
        "wp41_fragment_path_id_mismatch_rejected",
        "wp41_fragment_cwd_independent",
        "wp41_fragment_discovery_adapter",
        "wp41_fragment_read_error_diagnosable",
    }
    if not superseded_ids.issubset(source_ids):
        return False

    with tempfile.TemporaryDirectory() as tmp:
        fragment_root = Path(tmp)
        for test_id in ("wp88_loader_zulu", "wp88_loader_alpha"):
            (fragment_root / f"{test_id}.py").write_text(
                f'TEST_ID = "{test_id}"\n\ndef run(tl_module):\n    return True\n',
                encoding="utf-8", newline="\n")
        cases = loader.load_fragment_cases(fragment_root)
        if ([case.test_id for case in cases]
                != ["wp88_loader_alpha", "wp88_loader_zulu"]):
            return False
        if not all(case.run(tl_module) for case in cases):
            return False

    with tempfile.TemporaryDirectory() as tmp:
        parent = Path(tmp)
        physical_root = parent / "physical"
        linked_root = parent / "linked"
        physical_root.mkdir()
        if os.name == "nt":
            made = subprocess.run(
                [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/c", "mklink", "/J",
                 str(linked_root), str(physical_root)],
                capture_output=True, text=True, encoding="utf-8", errors="replace")
            if made.returncode != 0:
                return False
        else:
            try:
                linked_root.symlink_to(physical_root, target_is_directory=True)
            except OSError:
                return False
        try:
            target = linked_root / "wp88_read_error.py"
            target.write_text(
                'TEST_ID = "wp88_read_error"\n\ndef run(tl_module):\n    return True\n',
                encoding="utf-8", newline="\n")
            if target == target.resolve(strict=True):
                return False
            original_read_text = Path.read_text

            def blocked_read_text(path, *args, **kwargs):
                if path.name == "wp88_read_error.py":
                    raise OSError("wp88 fixture read blocked")
                return original_read_text(path, *args, **kwargs)

            Path.read_text = blocked_read_text
            try:
                try:
                    loader.load_fragment_cases(linked_root)
                except loader.FragmentError as exc:
                    read_error_ok = exc.code == "FRAGMENT_READ"
                else:
                    read_error_ok = False
            finally:
                Path.read_text = original_read_text
        finally:
            if os.name == "nt":
                linked_root.rmdir()
            else:
                linked_root.unlink()
    return read_error_ok
