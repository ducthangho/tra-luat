#!/usr/bin/env python3
"""Stdlib inventory shared by Linux and real Windows.

All telemetry, grants and human decisions below are SYNTHETIC TEST FIXTURES.
No real receipt is emitted. CLI tests execute a pinned canonical Git verifier;
API tests pass an explicitly trusted Snapshot and measure semantic controls.
Run: python -B ops/codex_routing_test.py [-v]
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE = Path(os.environ.get("TL_ROUTING_TEST_MODULE", str(HERE / "codex_routing.py")))
spec = importlib.util.spec_from_file_location("routing_under_test", MODULE)
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)
NOW = "2026-11-03T16:30:00Z"
OUTPUT = b"TEST ONLY synthetic native CLI telemetry\nKET_LUAN: approve\n"
REPORT = b"TEST ONLY synthetic report, no real human audit\n"
MUTANTS_KILLED = 0


def fixture():
    b = dict(grant_id="test-grant", mission=1172, revision=1, plan_hash="a" * 64, packet=1173,
             spec_hash="b" * 64, generation=1, base_sha="c" * 40, head_sha="d" * 40, tree_sha="e" * 40, dispatch_id="test-dispatch")
    def identity(role, effort):
        return dict(provider="openai_codex", surface="codex_cli", transport="machine", run_id=f"test-{role}-run", session_id=f"test-{role}-session",
                    requested_model="test-model", requested_effort=effort, observed_model="test-model", observed_effort=effort)
    executor, reviewer = identity("executor", "medium"), identity("reviewer", "high")
    t = dict(schema_version=1, kind="technical", binding=copy.deepcopy(b), executor=executor, reviewer=reviewer, run_id=reviewer["run_id"], provenance_id="test-producer",
             completion="completed", exit_code=0, verdict="approve", findings=[], output_sha256=r.sha256(OUTPUT), report_sha256=r.sha256(REPORT))
    a = dict(schema_version=1, kind="human_audit", audit_id="test-audit", binding=copy.deepcopy(b), technical_sha256=r.sha256(r.canonical_bytes(t)), technical_run_id=t["run_id"],
             provider="human", surface="manual_audit", transport="human", actor="ducthangho", source="https://github.com/ducthangho/tra-luat/issues/1173#issuecomment-111",
             decision="approve", findings=[], limitations=["TEST ONLY: synthetic assertion, no actual person audited"], executor_independent=True)
    config = lambda x: dict(provider=x["provider"], surface=x["surface"], transport=x["transport"], model=x["requested_model"], effort=x["requested_effort"])
    policy = {k: b[k] for k in ("grant_id", "mission", "revision", "plan_hash", "packet", "spec_hash", "generation", "base_sha")}
    policy.update(schema_version=1, actor="ducthangho", source=a["source"], decision="approve", valid_from="2000-01-01T00:00:00Z", expires_at="2099-01-01T00:00:00Z", revoked=False,
                  executor_config=config(executor), reviewer_config=config(reviewer), effort_order=["low", "medium", "high"], spec_path="ops/specs/test.md")
    row = dict(binding=copy.deepcopy(b), units=dict(executor_runs=1, review_calls=1, attempts=1), executor_run_id=executor["run_id"], reviewer_run_id=reviewer["run_id"])
    ledger = dict(mission=b["mission"], revision=b["revision"], plan_hash=b["plan_hash"], allowance=dict(executor_runs=1, review_calls=2, attempts=3),
                  usage=dict(executor_runs=0, review_calls=0, attempts=0), history=[], reservations=[row])
    producer = {k: copy.deepcopy(t[k]) for k in ("binding", "executor", "reviewer", "output_sha256", "report_sha256", "completion", "exit_code", "verdict")}
    producer.update(producer_id=t["provenance_id"], technical_sha256=r.sha256(r.canonical_bytes(t)), telemetry_source=a["source"])
    registry = dict(schema_version=1, repository=r.REPOSITORY, test_only=True, policies=[policy], ledgers=[ledger], producers=[producer], audits=[copy.deepcopy(a)])
    request = dict(operation="composite", binding=b, technical=t, audit=a)
    return registry, request


def reseal(registry, request):
    """Make forged canonical assertions coherent so each target guard is isolated."""
    b, t, a = request["binding"], request["technical"], request["audit"]
    t["binding"] = copy.deepcopy(b)
    a["binding"] = copy.deepcopy(b)
    a["technical_sha256"] = r.sha256(r.canonical_bytes(t))
    a["source"] = f"https://github.com/ducthangho/tra-luat/issues/{b['packet']}#issuecomment-111"
    registry["ledgers"][0]["reservations"][0]["binding"] = copy.deepcopy(b)
    producer = registry["producers"][0]
    for key in ("binding", "executor", "reviewer", "output_sha256", "report_sha256", "completion", "exit_code", "verdict"):
        producer[key] = copy.deepcopy(t[key])
    producer["technical_sha256"] = a["technical_sha256"]
    producer["telemetry_source"] = a["source"]
    registry["audits"][0] = copy.deepcopy(a)


def check(registry, request, output=OUTPUT, report=REPORT):
    snap = r.Snapshot("f" * 40, "a" * 64, r.canonical_bytes(registry), True)
    return r.verify(snap, request, now=NOW, output=output, report=report)


class SemanticTests(unittest.TestCase):
    def setUp(self):
        self.registry, self.request = fixture()

    def blocked(self, registry=None, request=None, **kw):
        with self.assertRaises(r.Blocked):
            check(registry if registry is not None else self.registry, request if request is not None else self.request, **kw)

    def test_positive_four_operations(self):
        for operation in ("admission", "technical", "human", "composite"):
            with self.subTest(operation=operation):
                q = copy.deepcopy(self.request)
                q["operation"] = operation
                if operation == "admission":
                    del q["technical"]
                if operation in ("admission", "technical"):
                    del q["audit"]
                out = check(self.registry, q)
                self.assertEqual(out["status"], "validated")
                self.assertTrue(out["positive_evidence"])
                self.assertFalse(out["authorizes_dispatch"])
                self.assertFalse(out["lifecycle_integrated"])
                self.assertEqual(out.get("assurance"), "human_audited" if operation == "composite" else None)
                if operation != "admission":
                    self.assertEqual(out["model_reviewer_identity"]["provider"], "openai_codex")

    def test_scope_guard(self):
        self.request["binding"]["packet"] = 1170
        reseal(self.registry, self.request)
        self.blocked()

    def test_scope_fields(self):
        changes = dict(grant_id="other", mission=90, revision=2, plan_hash="0" * 64, spec_hash="0" * 64, generation=2, base_sha="0" * 40,
                       head_sha="0" * 40, tree_sha="0" * 40, dispatch_id="reroute-new-state-dir")
        for key, value in changes.items():
            with self.subTest(field=key):
                q = copy.deepcopy(self.request)
                q["binding"][key] = value
                self.blocked(request=q)

    def test_missing_authority_and_ambiguity(self):
        for key, value in (("actor", "codex-dispatcher"), ("decision", "proposed"), ("source", "https://github.com/ducthangho/tra-luat/issues/90#issuecomment-111")):
            with self.subTest(field=key):
                reg = copy.deepcopy(self.registry)
                reg["policies"][0][key] = value
                self.blocked(registry=reg)
        for section in ("policies", "ledgers", "producers", "audits"):
            for mode in ("missing", "duplicate"):
                with self.subTest(section=section, mode=mode):
                    reg = copy.deepcopy(self.registry)
                    reg[section] = [] if mode == "missing" else reg[section] * 2
                    self.blocked(registry=reg)

    def test_expiry_revocation(self):
        for key, value in (("expires_at", NOW), ("valid_from", "2099-01-01T00:00:00Z"), ("revoked", True)):
            with self.subTest(field=key):
                reg = copy.deepcopy(self.registry)
                reg["policies"][0][key] = value
                self.blocked(registry=reg)

    def test_budget_guard(self):
        self.registry["ledgers"][0]["allowance"]["executor_runs"] = 0
        self.blocked()

    def test_ledger_replay_and_usage(self):
        for axis in r.UNITS:
            reg = copy.deepcopy(self.registry)
            reg["ledgers"][0]["usage"][axis] = 1
            self.blocked(registry=reg)
        for collection in ("reservations", "history"):
            reg = copy.deepcopy(self.registry)
            row = copy.deepcopy(reg["ledgers"][0]["reservations"][0])
            reg["ledgers"][0][collection].append(row)
            self.blocked(registry=reg)
        reg = copy.deepcopy(self.registry)
        reg["ledgers"][0]["reservations"][0]["reviewer_run_id"] = "replayed-or-unreserved-run"
        self.blocked(registry=reg)

    def test_effort_guard(self):
        self.request["technical"]["reviewer"]["observed_effort"] = "medium"
        reseal(self.registry, self.request)
        self.blocked()

    def test_unknown_effort_model_and_independence(self):
        for role in ("executor", "reviewer"):
            for key, value in (("observed_effort", "unknown"), ("observed_model", "unknown"), ("observed_model", "different-model")):
                with self.subTest(role=role, field=key, value=value):
                    q = copy.deepcopy(self.request)
                    q["technical"][role][key] = value
                    self.blocked(request=q)
        for key in ("session_id", "run_id"):
            q = copy.deepcopy(self.request)
            q["technical"]["reviewer"][key] = q["technical"]["executor"][key]
            self.blocked(request=q)
        q = copy.deepcopy(self.request)
        q["technical"]["reviewer"]["surface"] = "codex_service"
        self.blocked(request=q)

    def test_producer_output_replay(self):
        self.blocked(output=OUTPUT + b"swapped")
        self.blocked(report=REPORT + b"swapped")
        self.blocked(output=b"")
        self.blocked(report=b"")
        for key, value in (("technical_sha256", "0" * 64), ("output_sha256", "0" * 64), ("telemetry_source", "caller-supplied-local-file")):
            reg = copy.deepcopy(self.registry)
            reg["producers"][0][key] = value
            self.blocked(registry=reg)
        reg = copy.deepcopy(self.registry)
        duplicate = copy.deepcopy(reg["producers"][0])
        duplicate["producer_id"] = "other-producer"
        reg["producers"].append(duplicate)
        self.blocked(registry=reg)

    def test_human_guard(self):
        self.request["audit"]["provider"] = "openai_codex"
        reseal(self.registry, self.request)
        self.blocked()

    def test_human_bindings_and_decision(self):
        changes = dict(actor="agent", surface="codex_service", transport="machine", technical_sha256="0" * 64,
                       technical_run_id="other-run", decision="changes_requested", executor_independent=False, limitations=[])
        for key, value in changes.items():
            with self.subTest(field=key):
                q = copy.deepcopy(self.request)
                q["audit"][key] = value
                self.blocked(request=q)
        q = copy.deepcopy(self.request)
        q["audit"]["binding"]["tree_sha"] = "0" * 40
        self.blocked(request=q)
        reg = copy.deepcopy(self.registry)
        reg["audits"][0]["source"] = reg["audits"][0]["source"].replace("111", "222")
        self.blocked(registry=reg)

    def test_findings_and_nonapproval_status(self):
        for severity in ("P0", "P1", "P2", "P3"):
            for receipt in ("technical", "audit"):
                q = copy.deepcopy(self.request)
                q[receipt]["findings"] = [{"severity": severity, "id": "test-finding"}]
                self.blocked(request=q)
        for key, values in (("completion", ("partial", "cancelled", "timeout", "failed", "not_run", "unassessed")),
                            ("exit_code", (1, None, True)), ("verdict", ("changes_requested", "blocked", "unassessed"))):
            for value in values:
                q = copy.deepcopy(self.request)
                q["technical"][key] = value
                self.blocked(request=q)

    def test_schema_boundaries(self):
        for obj in (self.registry, self.registry["policies"][0], self.registry["ledgers"][0], self.registry["producers"][0], self.request,
                    self.request["binding"], self.request["technical"], self.request["technical"]["reviewer"], self.request["audit"]):
            obj["surprise"] = "candidate-activation"
            self.blocked()
            del obj["surprise"]
        for field in ("mission", "revision", "packet", "generation"):
            q = copy.deepcopy(self.request)
            q["binding"][field] = True
            self.blocked(request=q)
        for raw in (b'{"a":1,"a":2}', b'{"a": NaN}', b'{"a": 1e999}', b'\xff', b'[]trailing'):
            with self.assertRaises(r.Blocked):
                r.parse_json(raw)
        self.registry["schema_version"] = True
        self.blocked()

    def test_admission_checks_configured_model_and_higher_effort(self):
        for key, value in (("effort", "medium"), ("effort", "low"), ("model", "different-model"), ("surface", "codex_service")):
            reg = copy.deepcopy(self.registry)
            reg["policies"][0]["reviewer_config"][key] = value
            q = {"operation": "admission", "binding": self.request["binding"]}
            self.blocked(registry=reg, request=q)
        for order in (["medium", "low", "high"], ["high", "medium"], ["medium", "high", "unknown"]):
            reg = copy.deepcopy(self.registry)
            reg["policies"][0]["effort_order"] = order
            self.blocked(registry=reg)

    def test_cross_ledger_dispatch_and_cross_role_run_replay(self):
        for field in ("dispatch_id", "executor_run_id", "reviewer_run_id"):
            reg = copy.deepcopy(self.registry)
            second = copy.deepcopy(reg["ledgers"][0])
            second["mission"] = 999
            row = second["reservations"][0]
            row["binding"].update(mission=999, dispatch_id="other-dispatch")
            row.update(executor_run_id="other-executor", reviewer_run_id="other-reviewer")
            if field == "dispatch_id":
                row["binding"][field] = self.request["binding"][field]
            else:
                # Reuse the opposite role's run to test global identity namespace.
                row[field] = self.request["technical"]["reviewer" if field == "executor_run_id" else "executor"]["run_id"]
            reg["ledgers"].append(second)
            self.blocked(registry=reg)

    def test_nested_malformed_values_block_cleanly(self):
        for field in ("actor", "effort_order", "executor_config", "reviewer_config", "spec_path"):
            for malformed in (None, True, [], {"unexpected": 1}):
                reg = copy.deepcopy(self.registry)
                reg["policies"][0][field] = malformed
                self.blocked(registry=reg)
        for receipt in ("technical", "audit"):
            for field in ("revision", "generation"):
                q = copy.deepcopy(self.request)
                q[receipt]["binding"][field] = True
                self.blocked(request=q)
        for section in ("policies", "ledgers", "producers", "audits"):
            reg = copy.deepcopy(self.registry)
            reg[section].append(None)
            self.blocked(registry=reg)

    def test_canonical_producer_agreement_still_requires_native_cli(self):
        for key, value in (("surface", "codex_service"), ("observed_model", "unknown"), ("observed_effort", "unknown")):
            reg, q = copy.deepcopy(self.registry), copy.deepcopy(self.request)
            q["technical"]["reviewer"][key] = value
            if key == "surface":
                reg["policies"][0]["reviewer_config"]["surface"] = value
            reseal(reg, q)
            self.blocked(registry=reg, request=q)
        reg, q = copy.deepcopy(self.registry), copy.deepcopy(self.request)
        q["technical"]["reviewer"]["session_id"] = q["technical"]["executor"]["session_id"]
        reseal(reg, q)
        self.blocked(registry=reg, request=q)

    def test_unsupported_lifecycles(self):
        for operation in r.UNSUPPORTED:
            q = copy.deepcopy(self.request)
            q["operation"] = operation
            self.blocked(request=q)


class GitCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="routing-test-only-")
        cls.home = Path(cls.tmp.name)
        cls.remote, cls.root, cls.files = cls.home / "canonical.git", cls.home / "checkout", cls.home / "inputs"
        cls.files.mkdir()
        cls.env = os.environ.copy()
        for key in list(cls.env):
            if key == "GIT_CONFIG_COUNT" or key.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_")):
                del cls.env[key]
        cls.env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull, GIT_AUTHOR_NAME="test-only", GIT_AUTHOR_EMAIL="test@invalid",
                       GIT_COMMITTER_NAME="test-only", GIT_COMMITTER_EMAIL="test@invalid", PYTHONDONTWRITEBYTECODE="1")
        cls.git("init", "--bare", str(cls.remote), cwd=cls.home)
        cls.git("init", "-b", "master", str(cls.root), cwd=cls.home)
        cls.git("remote", "add", "origin", str(cls.remote))
        cls.git("config", "core.autocrlf", "false")
        cls.git("config", "core.abbrev", "7")
        (cls.root / "ops/specs").mkdir(parents=True)
        (cls.root / "ops/specs/test.md").write_bytes(b"TEST ONLY spec\n")
        cls.git("add", ".")
        cls.git("commit", "-qm", "TEST ONLY base")
        base = cls.git("rev-parse", "HEAD").strip()
        (cls.root / "candidate.txt").write_bytes(b"TEST ONLY candidate\n")
        cls.git("add", ".")
        cls.git("commit", "-qm", "TEST ONLY candidate")
        head = cls.git("rev-parse", "HEAD").strip()
        tree = cls.git("rev-parse", "HEAD^{tree}").strip()
        cls.registry, cls.request = fixture()
        b = cls.request["binding"]
        b.update(base_sha=base, head_sha=head, tree_sha=tree, spec_hash=r.sha256(b"TEST ONLY spec\n"))
        cls.request["technical"]["binding"] = copy.deepcopy(b)
        cls.request["audit"]["binding"] = copy.deepcopy(b)
        cls.request["audit"]["technical_sha256"] = r.sha256(r.canonical_bytes(cls.request["technical"]))
        cls.registry["policies"][0].update(base_sha=base, spec_hash=b["spec_hash"])
        cls.registry["ledgers"][0]["reservations"][0]["binding"] = copy.deepcopy(b)
        cls.registry["producers"][0].update(binding=copy.deepcopy(b), technical_sha256=cls.request["audit"]["technical_sha256"])
        cls.registry["audits"][0] = copy.deepcopy(cls.request["audit"])
        (cls.root / r.VERIFIER_PATH).write_bytes(MODULE.read_bytes())
        (cls.root / "ops/codex-routing").mkdir()
        cls.registry_path = cls.root / r.REGISTRY_PATH
        cls.registry_path.write_bytes(r.canonical_bytes(cls.registry))
        cls.git("add", ".")
        cls.git("commit", "-qm", "TEST ONLY canonical verifier and assertions")
        cls.git("push", "-q", "origin", "master")
        cls.clean_oid = cls.git("rev-parse", "HEAD").strip()
        (cls.files / "stdout.txt").write_bytes(OUTPUT)
        (cls.files / "report.txt").write_bytes(REPORT)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    @classmethod
    def git(cls, *args, cwd=None):
        p = subprocess.run(["git", *args], cwd=cwd or cls.root, env=cls.env, capture_output=True, text=True, timeout=30)
        if p.returncode:
            raise AssertionError(f"Git fixture setup failed {args}: {p.stderr}")
        return p.stdout

    def setUp(self):
        self.git("reset", "--hard", self.clean_oid)
        self.git("push", "-q", "--force", "origin", "master")

    def run_cli(self, request=None, state_name="one", extra=None, fixture_mode=True):
        # Different input directories cannot change the canonical allowance.
        folder = self.files / state_name
        folder.mkdir(exist_ok=True)
        path = folder / "request.json"
        path.write_bytes(r.canonical_bytes(request if request is not None else self.request))
        cmd = [sys.executable, "-B", str(MODULE), "--root", str(self.root), "--request", str(path),
               "--raw-output", str(self.files / "stdout.txt"), "--report", str(self.files / "report.txt")]
        if fixture_mode:
            cmd.append("--fixture")
        cmd += extra or []
        p = subprocess.run(cmd, env=self.env, capture_output=True, text=True, timeout=60)
        self.assertTrue(p.stdout.strip(), p.stderr)
        out = json.loads(p.stdout)
        self.assertIn("status", out)
        return p.returncode, out

    def publish_registry(self, registry):
        self.registry_path.write_bytes(r.canonical_bytes(registry))
        self.git("add", r.REGISTRY_PATH)
        self.git("commit", "-qm", "TEST ONLY registry negative control")
        self.git("push", "-q", "origin", "master")

    def test_cli_positive_all_operations(self):
        for operation in ("admission", "technical", "human", "composite"):
            with self.subTest(operation=operation):
                q = copy.deepcopy(self.request)
                q["operation"] = operation
                if operation == "admission":
                    del q["technical"]
                if operation in ("admission", "technical"):
                    del q["audit"]
                rc, out = self.run_cli(q)
                self.assertEqual(rc, 0, out)
                self.assertEqual(out["status"], "validated")
                self.assertTrue(out["test_only"])
                self.assertIn("Git source base/head/tree/spec bytes", out["positive_evidence"])
                self.assertEqual(out["canonical_oid"], self.clean_oid)

    def test_cli_rejects_candidate_self_activation(self):
        candidate = copy.deepcopy(self.registry)
        candidate["policies"][0]["packet"] = 90
        self.registry_path.write_bytes(r.canonical_bytes(candidate))
        (self.root / r.VERIFIER_PATH).write_text("raise RuntimeError('candidate implementation must not run')\n", encoding="utf-8")
        rc, out = self.run_cli()
        self.assertEqual(rc, 0, out)
        q = copy.deepcopy(self.request)
        q["binding"]["packet"] = 90
        rc, out = self.run_cli(q)
        self.assertEqual(rc, 12, out)
        self.assertEqual(out["status"], "blocked")

    def test_cli_missing_canonical_verifier_and_policy(self):
        self.git("rm", r.VERIFIER_PATH)
        self.git("commit", "-qm", "TEST ONLY missing canonical verifier")
        self.git("push", "-q", "origin", "master")
        self.assertEqual(self.run_cli()[0], 12)
        self.git("reset", "--hard", self.clean_oid)
        self.git("rm", r.REGISTRY_PATH)
        self.git("commit", "-qm", "TEST ONLY missing canonical registry")
        self.git("push", "-q", "--force", "origin", "master")
        self.assertEqual(self.run_cli()[0], 12)

    def test_cli_changed_state_directory_no_new_allowance(self):
        self.assertEqual(self.run_cli(state_name="first-state")[0], 0)
        q = copy.deepcopy(self.request)
        q["binding"]["dispatch_id"] = "new-state-new-dispatch"
        self.assertEqual(self.run_cli(q, state_name="second-state")[0], 12)

    def test_cli_exhausted_canonical_ledger(self):
        reg = copy.deepcopy(self.registry)
        reg["ledgers"][0]["allowance"]["executor_runs"] = 0
        self.publish_registry(reg)
        rc, out = self.run_cli()
        self.assertEqual(rc, 12, out)
        self.assertIn("budget exhausted", out["reason"])

    def test_cli_rejects_local_origin_in_production(self):
        rc, out = self.run_cli(fixture_mode=False)
        self.assertEqual(rc, 12, out)
        self.assertFalse(out["test_only"])

    def test_cli_duplicate_json_and_unknown_input(self):
        self.registry_path.write_bytes(b'{"schema_version":1,"schema_version":1}')
        self.git("add", r.REGISTRY_PATH)
        self.git("commit", "-qm", "TEST ONLY duplicate JSON")
        self.git("push", "-q", "origin", "master")
        self.assertEqual(self.run_cli()[0], 12)

    def test_cli_source_tree_spec_actual_git_binding(self):
        reg, q = copy.deepcopy(self.registry), copy.deepcopy(self.request)
        # All canonical assertions agree on the forged tree; actual Git must reject.
        q["binding"]["tree_sha"] = "0" * 40
        q["technical"]["binding"] = copy.deepcopy(q["binding"])
        q["audit"]["binding"] = copy.deepcopy(q["binding"])
        q["audit"]["technical_sha256"] = r.sha256(r.canonical_bytes(q["technical"]))
        reg["ledgers"][0]["reservations"][0]["binding"] = copy.deepcopy(q["binding"])
        reg["producers"][0].update(binding=copy.deepcopy(q["binding"]), technical_sha256=q["audit"]["technical_sha256"])
        reg["audits"][0] = copy.deepcopy(q["audit"])
        self.publish_registry(reg)
        rc, out = self.run_cli(q)
        self.assertEqual(rc, 12, out)
        self.assertIn("source H/tree mismatch", out["reason"])

    def test_cli_source_spec_hash_is_measured_from_git(self):
        reg, q = copy.deepcopy(self.registry), copy.deepcopy(self.request)
        q["binding"]["spec_hash"] = "0" * 64
        reg["policies"][0]["spec_hash"] = "0" * 64
        reseal(reg, q)
        self.publish_registry(reg)
        rc, out = self.run_cli(q)
        self.assertEqual(rc, 12, out)
        self.assertIn("source spec hash mismatch", out["reason"])

    def test_cli_admission_config_and_cross_ledger_regressions(self):
        reg = copy.deepcopy(self.registry)
        reg["policies"][0]["reviewer_config"]["effort"] = "medium"
        self.publish_registry(reg)
        q = {"operation": "admission", "binding": self.request["binding"]}
        self.assertEqual(self.run_cli(q)[0], 12)
        reg = copy.deepcopy(self.registry)
        second = copy.deepcopy(reg["ledgers"][0])
        second["mission"] = 999
        second["reservations"][0]["binding"]["mission"] = 999
        reg["ledgers"].append(second)
        self.publish_registry(reg)
        self.assertEqual(self.run_cli()[0], 12)

    def test_cli_grafts_cannot_create_ancestry(self):
        reg, q = copy.deepcopy(self.registry), copy.deepcopy(self.request)
        unrelated = self.git("commit-tree", q["binding"]["tree_sha"], "-m", "TEST ONLY unrelated root").strip()
        q["binding"]["head_sha"] = unrelated
        reseal(reg, q)
        self.publish_registry(reg)
        baseline = subprocess.run(["git", "merge-base", "--is-ancestor", q["binding"]["base_sha"], unrelated], cwd=self.root, env=self.env, capture_output=True)
        self.assertEqual(baseline.returncode, 1)
        common = Path(self.git("rev-parse", "--path-format=absolute", "--git-common-dir").strip())
        graft = common / "info/grafts"
        graft.parent.mkdir(exist_ok=True)
        graft.write_text(f"{unrelated} {q['binding']['base_sha']}\n", encoding="ascii")
        try:
            bypassed = subprocess.run(["git", "merge-base", "--is-ancestor", q["binding"]["base_sha"], unrelated], cwd=self.root, env=self.env, capture_output=True)
            self.assertEqual(bypassed.returncode, 0)
            rc, out = self.run_cli(q)
            self.assertEqual(rc, 12, out)
            self.assertIn("not a raw-object ancestor", out["reason"])
            linked = self.home / "linked-graft-checkout"
            self.git("worktree", "add", "--detach", str(linked), "HEAD")
            try:
                rc, out = self.run_cli(q, extra=["--root", str(linked)])
                self.assertEqual(rc, 12, out)
                self.assertIn("not a raw-object ancestor", out["reason"])
                self.env["GIT_GRAFT_FILE"] = str(graft)
                rc, out = self.run_cli(q)
                self.assertEqual(rc, 12, out)
            finally:
                self.env.pop("GIT_GRAFT_FILE", None)
                self.git("worktree", "remove", "--force", str(linked))
        finally:
            graft.unlink()

    def test_cli_rejects_canonical_traversal_spec_path(self):
        reg = copy.deepcopy(self.registry)
        reg["policies"][0]["spec_path"] = "ops/specs/../../outside.md"
        self.publish_registry(reg)
        self.assertEqual(self.run_cli()[0], 12)

    def test_cli_git_replace_cannot_supply_canonical_registry(self):
        reg = copy.deepcopy(self.registry)
        reg["policies"][0]["revoked"] = True
        self.publish_registry(reg)
        revoked_oid = self.git("rev-parse", "HEAD").strip()
        self.git("replace", revoked_oid, self.clean_oid)
        try:
            rc, out = self.run_cli()
            self.assertEqual(rc, 12, out)
            self.assertIn("policy expired/revoked", out["reason"])
        finally:
            self.git("replace", "-d", revoked_oid)

    def test_cli_canonical_symlink_rejected_without_os_symlink(self):
        # Git index mode works on Windows without Developer Mode/symlink privilege.
        target = self.files / "symlink-target.txt"
        target.write_bytes(b"../untrusted.json")
        oid = self.git("hash-object", "-w", str(target)).strip()
        self.git("update-index", "--cacheinfo", f"120000,{oid},{r.REGISTRY_PATH}")
        self.git("commit", "-qm", "TEST ONLY canonical symlink")
        self.git("push", "-q", "origin", "master")
        self.assertEqual(self.run_cli()[0], 12)


class MutationTests(unittest.TestCase):
    def test_core_guard_removal_makes_inventory_red(self):
        global MUTANTS_KILLED
        replacements = [
            ('all(p[key] == b[key] for key in ("mission", "revision", "plan_hash", "packet", "spec_hash", "generation", "base_sha"))', 'True', "test_scope_guard"),
            ('all(ledger["usage"][k] + reserved[k] <= ledger["allowance"][k] for k in UNITS)', 'True', "test_budget_guard"),
            ('EFFORT[reviewer["observed_effort"]] > EFFORT[executor["observed_effort"]]', 'True', "test_effort_guard"),
            ('(a["provider"], a["surface"], a["transport"]) == ("human", "manual_audit", "human")', 'True', "test_human_guard"),
        ]
        source = MODULE.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory(prefix="routing-mutants-test-only-") as td:
            for index, (old, new, method) in enumerate(replacements):
                with self.subTest(guard=method):
                    self.assertEqual(source.count(old), 1)
                    path = Path(td) / f"mutant{index}.py"
                    path.write_text(source.replace(old, new), encoding="utf-8")
                    env = os.environ.copy()
                    env.update(TL_ROUTING_TEST_MODULE=str(path), PYTHONDONTWRITEBYTECODE="1")
                    p = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), f"SemanticTests.{method}"], env=env, capture_output=True, text=True, timeout=30)
                    self.assertNotEqual(p.returncode, 0, "guard removal failed to turn its behavior test red")
                    self.assertIn("AssertionError", p.stderr)
                    MUTANTS_KILLED += 1


if __name__ == "__main__":
    program = unittest.main(verbosity=2, exit=False)
    result = program.result
    if result.wasSuccessful() and not result.skipped and result.testsRun:
        print(f"{result.testsRun}/{result.testsRun} passed; mutations {MUTANTS_KILLED}/4")
        sys.exit(0)
    sys.exit(1)
