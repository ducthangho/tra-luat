# -*- coding: utf-8 -*-
"""Executable two-way counter-proofs for packet_scope_check.py."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


CHECK = Path(__file__).with_name("packet_scope_check.py")


BASE = {
    "packet_id": "wp999",
    "revision": 1,
    "spec_hash": "0" * 64,
    "objective": "scope counter-proof",
    "write_set": [{"type": "exact", "path": "docs/a.md"}],
    "ref_set": [{"type": "exact", "ref": "refs/heads/codex/wp999"}],
    "depends_on": [],
    "executor": "codex",
    "environment": "local",
    "risk": "normal",
    "acceptance_criteria": ["counter-proof"],
}


def _run(tmp: Path, spec, changes, *, raw_spec=None):
    spec_path = tmp / "packet.yaml"
    changes_path = tmp / "changes.json"
    spec_path.write_text(raw_spec if raw_spec is not None else json.dumps(spec), encoding="utf-8")
    changes_path.write_text(json.dumps(changes), encoding="utf-8")
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    proc = subprocess.run(
        [sys.executable, str(CHECK), "--spec", str(spec_path), "--changes", str(changes_path), "--json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        payload = {"ok": False, "error": "NON_JSON", "raw": proc.stdout.decode("utf-8", "replace")}
    return proc.returncode, payload


def main():
    cases = []
    with tempfile.TemporaryDirectory(prefix="wp84_scope_") as name:
        tmp = Path(name)

        def case(label, want_rc, spec=BASE, changes=None, raw_spec=None, want_error=None):
            if changes is None:
                changes = {"files": [], "refs": []}
            rc, payload = _run(tmp, spec, changes, raw_spec=raw_spec)
            ok = (rc == want_rc and bool(payload.get("ok")) == (want_rc == 0))
            if want_error is not None:
                ok = ok and payload.get("error") == want_error
            cases.append((label, ok, rc, payload))

        # The six acceptance cases, with real return-code reads.
        case("file_in_write_set_passes", 0, changes={"files": ["docs/a.md"], "refs": []})
        case("file_outside_write_set_fails", 1, changes={"files": ["docs/b.md"], "refs": []},
             want_error="OUT_OF_SCOPE")
        case("ref_in_ref_set_passes", 0, changes={"files": [], "refs": ["refs/heads/codex/wp999"]})
        case("ref_outside_ref_set_fails", 1, changes={"files": [], "refs": ["refs/heads/master"]},
             want_error="OUT_OF_SCOPE")
        missing = dict(BASE)
        missing.pop("ref_set")
        case("missing_required_field_fails", 1, spec=missing, want_error="SPEC_MISSING_FIELD")
        case("broken_spec_fails", 1, raw_spec="packet_id: [unterminated", want_error="SPEC_MISSING_FIELD")

        # YAML and prefix behavior ensure both advertised input formats and both scope types run.
        yaml_spec = """packet_id: wp999
revision: 1
spec_hash: "0000000000000000000000000000000000000000000000000000000000000000"
objective: yaml counter-proof
write_set:
  - type: prefix
    path: docs/sub
ref_set:
  - type: prefix
    ref: refs/heads/codex/wp999
depends_on: []
executor: codex
environment: local
risk: normal
acceptance_criteria:
  - counter-proof
"""
        case("yaml_prefixes_pass", 0, raw_spec=yaml_spec,
             changes={"files": ["docs/sub/x.md"], "refs": ["refs/heads/codex/wp999/topic"]})
        case("malformed_changes_fail", 1, changes={"files": []}, want_error="CHANGES_PARSE_ERROR")

    passed = sum(1 for _, ok, _, _ in cases if ok)
    for label, ok, rc, payload in cases:
        print("[%s] %s rc=%s error=%s" % ("OK" if ok else "FAIL", label, rc, payload.get("error")))
    print("packet_scope_check_test: %d/%d" % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
