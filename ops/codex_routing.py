#!/usr/bin/env python3
"""Read-only Codex routing foundation; no gate, dispatch or approval is performed.

CLI trust starts at the fixed canonical HTTPS URL in a fresh bare Git store:
fetch, read back, pin the OID, execute
that snapshot's verifier in an isolated Python subprocess, then independently
recheck the live OID before reading fixed canonical records. Candidate records
and candidate verifier changes cannot enable production admission. Platform PATH
and non-Git proxy/CA environment are runtime trust roots.

The pure API accepts an explicitly trusted Snapshot. Constructing that object
is the caller's trust responsibility; a dict or a successful schema check is
not authentication. Canonical records are trusted assertions of producer and
human decisions, not proof of actual model serving or that a person read code.
A successor must provide authenticated record publication and atomic dispatch /
ledger writes. Revalidating one reservation is read-only and idempotent; it does
not authorize a second call or consume/reserve any budget.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

SCHEMA = 1
_GIT_BINARY = None  # Pinned by CLI before creating its isolated transport store.
VERIFIER_PATH = "ops/codex_routing.py"
REGISTRY_PATH = "ops/codex-routing/registry.json"
REPOSITORY = "ducthangho/tra-luat"
AUTHORITY_ACTORS = frozenset({"ducthangho"})
# Scoped foundation supports this model and its low/medium/high effort contract.
EFFORT = {"low": 0, "medium": 1, "high": 2}
SUPPORTED_MODELS = frozenset({"gpt-6.1-sol"})
UNSUPPORTED = frozenset({"adr0054", "k3", "k4", "accept", "record-review"})
LIMITATIONS = [
    "Foundation only: packet-loop, ADR-0054, K3/K4 and acceptance are not integrated.",
    "Canonical records attest assertions; metadata does not prove human reading or actual model serving.",
    "Read-only validation creates no grant, reservation, budget consumption or replay-safe dispatch transaction.",
    "CLI output is not producer authentication or merge/land authorization.",
]
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}\Z")
BINDING = {"grant_id", "mission", "revision", "plan_hash", "packet", "spec_hash", "generation", "base_sha", "head_sha", "tree_sha", "dispatch_id"}
IDENTITY = {"provider", "surface", "transport", "run_id", "session_id", "requested_model", "requested_effort", "observed_model", "observed_effort"}
UNITS = {"executor_runs", "review_calls", "attempts"}


class Blocked(ValueError):
    """An input or an eligibility condition was not established."""


def require(ok, message):
    if not ok:
        raise Blocked(message)


def shape(value, keys, label):
    require(type(value) is dict and set(value) == set(keys), f"{label}: exact fields required {sorted(keys)}")
    return value


def number(value, label, minimum=1):
    require(type(value) is int and value >= minimum, f"{label}: integer >= {minimum} required")


def token(value, label):
    require(type(value) is str and bool(TOKEN.fullmatch(value)), f"{label}: invalid identifier")


def digest(value, label, sha=False):
    require(type(value) is str and bool((HEX40 if sha else HEX64).fullmatch(value)), f"{label}: invalid hash")


def timestamp(value):
    require(type(value) is str and bool(re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", value)), "timestamp: UTC seconds required")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise Blocked("timestamp: invalid calendar value") from exc


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def _pairs(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, f"JSON duplicate key: {key}")
        out[key] = value
    return out


def parse_json(raw):
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                          parse_float=lambda value: (_ for _ in ()).throw(Blocked(f"floating JSON number unsupported: {value}")),
                          parse_constant=lambda value: (_ for _ in ()).throw(Blocked(f"invalid JSON number: {value}")))
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise Blocked(f"invalid JSON: {exc}") from exc


def source(value, packet):
    require(type(value) is str and bool(re.fullmatch(
        rf"https://github\.com/{re.escape(REPOSITORY)}/issues/{packet}#issuecomment-[1-9][0-9]*", value)),
        "decision/source: exact repository and Packet comment required")


def binding(value):
    shape(value, BINDING, "binding")
    for key in ("mission", "revision", "packet", "generation"):
        number(value[key], key)
    for key in ("grant_id", "dispatch_id"):
        token(value[key], key)
    for key in ("plan_hash", "spec_hash"):
        digest(value[key], key)
    for key in ("base_sha", "head_sha", "tree_sha"):
        digest(value[key], key, True)
    require(value["base_sha"] != value["head_sha"], "base/head must differ")


def units(value):
    shape(value, UNITS, "budget units")
    for key in UNITS:
        number(value[key], key, 0)


def identity(value):
    shape(value, IDENTITY, "machine identity")
    require(value["provider"] == "openai_codex" and value["transport"] == "machine", "Codex machine identity required")
    require(value["surface"] in ("codex_cli", "codex_service", "codex_desktop"), "invalid Codex surface")
    for key in ("run_id", "session_id", "requested_model", "observed_model"):
        token(value[key], key)
    require(value["observed_model"] not in ("unknown", "KHONG_do_duoc"), "observed model unknown")
    require(value["requested_effort"] in EFFORT and value["observed_effort"] in EFFORT, "observed/requested effort unknown")


@dataclasses.dataclass(frozen=True)
class Snapshot:
    """Trusted canonical bytes, loaded by a trusted caller; not a signature."""
    oid: str
    verifier_sha256: str
    registry_raw: bytes
    test_only: bool = False


def _registry(snapshot):
    require(type(snapshot) is Snapshot, "trusted Snapshot required")
    require(type(snapshot.registry_raw) is bytes, "canonical registry bytes required")
    digest(snapshot.oid, "canonical OID", True)
    digest(snapshot.verifier_sha256, "verifier hash")
    require(type(snapshot.test_only) is bool, "test_only must be bool")
    registry = parse_json(snapshot.registry_raw)
    shape(registry, {"schema_version", "repository", "test_only", "policies", "ledgers", "producers", "audits"}, "registry")
    require(type(registry["schema_version"]) is int and registry["schema_version"] == SCHEMA, "unsupported registry schema")
    require(registry["repository"] == REPOSITORY and registry["test_only"] is snapshot.test_only, "repository/test fixture mismatch")
    for key in ("policies", "ledgers", "producers", "audits"):
        require(type(registry[key]) is list, f"registry {key}: list required")
    return registry


def one(rows, predicate, label):
    selected = [row for row in rows if predicate(row)]
    require(len(selected) == 1, f"{label}: missing or ambiguous canonical record")
    return selected[0]


def _admission(registry, b, now):
    pkeys = {"schema_version", "grant_id", "mission", "revision", "plan_hash", "packet", "spec_hash", "generation", "base_sha", "actor", "source", "decision", "valid_from", "expires_at", "revoked", "executor_config", "reviewer_config", "effort_order", "spec_path"}
    for p in registry["policies"]:
        shape(p, pkeys, "policy")
        require(type(p["schema_version"]) is int and p["schema_version"] == SCHEMA, "policy schema")
        for key in ("mission", "revision", "packet", "generation"):
            number(p[key], f"policy {key}")
        token(p["grant_id"], "policy grant_id")
        require(type(p["spec_path"]) is str and bool(re.fullmatch(r"ops/specs/[A-Za-z0-9_.-]+\.md", p["spec_path"])), "policy spec path")
        digest(p["plan_hash"], "policy plan_hash")
        digest(p["spec_hash"], "policy spec_hash")
        digest(p["base_sha"], "policy base_sha", True)
        require(p["actor"] in AUTHORITY_ACTORS and p["decision"] == "approve", "policy owner decision missing")
        source(p["source"], p["packet"])
        require(type(p["revoked"]) is bool, "policy revoked must be bool")
        require(timestamp(p["valid_from"]) < timestamp(p["expires_at"]), "policy validity interval")
        for config in (p["executor_config"], p["reviewer_config"]):
            shape(config, {"provider", "surface", "transport", "model", "effort"}, "role configuration")
            require(config["provider"] == "openai_codex" and config["transport"] == "machine", "Codex configuration required")
            require(config["surface"] in ("codex_cli", "codex_service", "codex_desktop"), "configuration surface")
            token(config["model"], "configured model")
            require(config["effort"] in EFFORT, "configured effort")
        executor, reviewer = p["executor_config"], p["reviewer_config"]
        supported = SUPPORTED_MODELS | ({"test-model"} if registry["test_only"] else set())
        require(executor["model"] == reviewer["model"] and executor["model"] in supported, "same supported configured model required")
        require(EFFORT[reviewer["effort"]] > EFFORT[executor["effort"]], "reviewer configured effort must be higher")
        require(reviewer["surface"] == "codex_cli", "admission requires native CLI reviewer; service remains advisory")
        require(type(p["effort_order"]) is list and len(p["effort_order"]) >= 2
                and len(p["effort_order"]) == len(set(p["effort_order"]))
                and all(type(e) is str and e in EFFORT for e in p["effort_order"])
                and p["effort_order"] == sorted(p["effort_order"], key=EFFORT.__getitem__), "fixed supported model effort order required")
    p = one(registry["policies"], lambda x: x["grant_id"] == b["grant_id"], "policy")
    require(all(p[key] == b[key] for key in ("mission", "revision", "plan_hash", "packet", "spec_hash", "generation", "base_sha")), "policy scope/revision mismatch")
    require(not p["revoked"] and timestamp(p["valid_from"]) <= now < timestamp(p["expires_at"]), "policy expired/revoked/not yet valid")
    seen = set()  # Dispatch/run identities are global across every ledger and role.
    for ledger in registry["ledgers"]:
        shape(ledger, {"mission", "revision", "plan_hash", "allowance", "usage", "history", "reservations"}, "ledger")
        number(ledger["mission"], "ledger mission")
        number(ledger["revision"], "ledger revision")
        digest(ledger["plan_hash"], "ledger plan_hash")
        units(ledger["allowance"])
        units(ledger["usage"])
        require(type(ledger["history"]) is list and type(ledger["reservations"]) is list, "ledger history/reservations required")
        totals, reserved = dict.fromkeys(UNITS, 0), dict.fromkeys(UNITS, 0)
        for collection, sum_into in ((ledger["history"], totals), (ledger["reservations"], reserved)):
            for row in collection:
                shape(row, {"binding", "units", "executor_run_id", "reviewer_run_id"}, "dispatch row")
                binding(row["binding"])
                require(all(row["binding"][k] == ledger[k] for k in ("mission", "revision", "plan_hash")), "ledger row scope")
                units(row["units"])
                require(all(row["units"][k] > 0 for k in UNITS), "dispatch must reserve every required axis")
                for key in ("executor_run_id", "reviewer_run_id"):
                    token(row[key], key)
                    require(row[key] not in seen, "duplicate/replayed dispatch run")
                    seen.add(row[key])
                dispatch = row["binding"]["dispatch_id"]
                require(dispatch not in seen, "duplicate/replayed dispatch id")
                seen.add(dispatch)
                for key in UNITS:
                    sum_into[key] += row["units"][key]
        require(all(totals[k] == ledger["usage"][k] for k in UNITS), "ledger usage/history mismatch")
        require(all(ledger["usage"][k] + reserved[k] <= ledger["allowance"][k] for k in UNITS), "budget exhausted")
    ledger = one(registry["ledgers"], lambda x: all(x[k] == b[k] for k in ("mission", "revision", "plan_hash")), "ledger")
    reservation = one(ledger["reservations"], lambda x: x["binding"] == b, "reservation (state-dir cannot create allowance)")
    return p, reservation


def _technical(registry, b, policy, reservation, t, output, report):
    shape(t, {"schema_version", "kind", "binding", "executor", "reviewer", "run_id", "provenance_id", "completion", "exit_code", "verdict", "findings", "output_sha256", "report_sha256"}, "technical receipt")
    require(type(t["schema_version"]) is int and t["schema_version"] == SCHEMA and t["kind"] == "technical", "technical schema/kind")
    binding(t["binding"])
    require(t["binding"] == b, "technical binding mismatch")
    require(type(t["exit_code"]) is int and t["exit_code"] == 0 and t["completion"] == "completed" and t["verdict"] == "approve", "technical not successfully approved")
    require(type(t["findings"]) is list and not t["findings"], "technical findings remain (P0-P3)")
    for role in ("executor", "reviewer"):
        machine, config = t[role], policy[f"{role}_config"]
        identity(machine)
        require(all(machine[k] == config[c] for k, c in (("provider", "provider"), ("surface", "surface"), ("transport", "transport"), ("requested_model", "model"), ("requested_effort", "effort"))), "identity/config mismatch")
        require(machine["run_id"] == reservation[f"{role}_run_id"], "reservation run mismatch")
    executor, reviewer = t["executor"], t["reviewer"]
    require(reviewer["surface"] == "codex_cli", "native CLI review required; service remains advisory")
    require(executor["run_id"] != reviewer["run_id"] and executor["session_id"] != reviewer["session_id"], "independent run/session required")
    require(reviewer["observed_model"] == executor["observed_model"] == reviewer["requested_model"] == executor["requested_model"], "same observed/configured model required")
    order = policy["effort_order"]
    require(executor["observed_effort"] in order and reviewer["observed_effort"] in order
            and EFFORT[reviewer["observed_effort"]] > EFFORT[executor["observed_effort"]], "reviewer observed effort must be higher")
    require(t["run_id"] == reviewer["run_id"], "technical run mismatch")
    for key in ("output_sha256", "report_sha256"):
        digest(t[key], key)
    require(type(output) is bytes and type(report) is bytes and bool(output) and bool(report), "immutable output/report required")
    require(sha256(output) == t["output_sha256"] and sha256(report) == t["report_sha256"], "output/report swapped or changed")
    try:
        lines = [line.strip() for line in output.decode("utf-8").splitlines() if line.strip()]
    except UnicodeError as exc:
        raise Blocked("output must be UTF-8") from exc
    require(lines and lines[-1] == "KET_LUAN: approve", "final CLI verdict missing")
    token(t["provenance_id"], "provenance id")
    keys = {"producer_id", "binding", "technical_sha256", "executor", "reviewer", "output_sha256", "report_sha256", "completion", "exit_code", "verdict", "telemetry_source"}
    seen_runs = set()
    for producer in registry["producers"]:
        shape(producer, keys, "producer")
        binding(producer["binding"])
        token(producer["producer_id"], "producer id")
        for key in ("technical_sha256", "output_sha256", "report_sha256"):
            digest(producer[key], key)
        source(producer["telemetry_source"], producer["binding"]["packet"])
        for role in ("executor", "reviewer"):
            identity(producer[role])
            require(producer[role]["run_id"] not in seen_runs, "producer run replay")
            seen_runs.add(producer[role]["run_id"])
        require(type(producer["exit_code"]) is int, "producer exit code must be integer")
    producer = one(registry["producers"], lambda x: x["producer_id"] == t["provenance_id"], "producer")
    require(producer["technical_sha256"] == sha256(canonical_bytes(t)), "producer technical hash mismatch")
    require(all(producer[k] == t[k] for k in ("binding", "executor", "reviewer", "output_sha256", "report_sha256", "completion", "exit_code", "verdict")), "producer evidence mismatch")
    return sha256(canonical_bytes(t))


def _audit(registry, b, technical_hash, t, a):
    keys = {"schema_version", "kind", "audit_id", "binding", "technical_sha256", "technical_run_id", "provider", "surface", "transport", "actor", "source", "decision", "findings", "limitations", "executor_independent"}
    shape(a, keys, "human audit")
    require(type(a["schema_version"]) is int and a["schema_version"] == SCHEMA and a["kind"] == "human_audit", "audit schema/kind")
    require((a["provider"], a["surface"], a["transport"]) == ("human", "manual_audit", "human"), "machine cannot be human auditor")
    require(a["actor"] in AUTHORITY_ACTORS and a["decision"] == "approve", "human authority/decision missing")
    source(a["source"], b["packet"])
    token(a["audit_id"], "audit id")
    binding(a["binding"])
    require(a["binding"] == b and a["technical_sha256"] == technical_hash and a["technical_run_id"] == t["run_id"], "audit binds different technical receipt/candidate")
    require(type(a["executor_independent"]) is bool and a["executor_independent"], "human audit must assert independence")
    require(type(a["findings"]) is list and not a["findings"], "human findings remain (P0-P3)")
    require(type(a["limitations"]) is list and a["limitations"] and all(type(x) is str and x.strip() for x in a["limitations"]), "audit must disclose evidence limitations")
    for record in registry["audits"]:
        shape(record, keys, "canonical audit")
    record = one(registry["audits"], lambda x: x["audit_id"] == a["audit_id"], "canonical human decision")
    require(record == a, "human decision differs from trusted canonical record")
    return sha256(canonical_bytes(a))


def _verify(snapshot, request, *, now, output=b"", report=b""):
    """Deterministic read-only API. Raises Blocked; never mints a receipt or grant."""
    registry = _registry(snapshot)
    require(type(request) is dict, "request object required")
    operation = request.get("operation")
    require(type(operation) is str, "operation required")
    require(operation not in UNSUPPORTED, "unsupported lifecycle: successor integration required")
    require(operation in ("admission", "technical", "human", "composite"), "unknown operation")
    keys = {"operation", "binding"} | ({"technical"} if operation != "admission" else set()) | ({"audit"} if operation in ("human", "composite") else set())
    shape(request, keys, "request")
    b = request["binding"]
    binding(b)
    policy, reservation = _admission(registry, b, timestamp(now))
    result = {"status": "validated", "operation": operation, "test_only": snapshot.test_only, "canonical_oid": snapshot.oid,
              "verifier_sha256": snapshot.verifier_sha256, "registry_sha256": sha256(snapshot.registry_raw),
              "policy_sha256": sha256(canonical_bytes(policy)), "binding": b, "reservation_id": b["dispatch_id"],
              "positive_evidence": ["canonical policy scope and decision", "canonical allowance/history/reservation"],
              "limitations": LIMITATIONS, "lifecycle_integrated": False, "authorizes_dispatch": False}
    if operation != "admission":
        t = request["technical"]
        technical_hash = _technical(registry, b, policy, reservation, t, output, report)
        result.update(technical_sha256=technical_hash, model_reviewer_identity=t["reviewer"], technical_status="approved")
        result["positive_evidence"].append("canonical native CLI producer, hashes, observed model/effort and independent session")
        if operation in ("human", "composite"):
            result["audit_sha256"] = _audit(registry, b, technical_hash, t, request["audit"])
            result["positive_evidence"].append("canonical human decision binds exact technical receipt")
            if operation == "composite":
                result["assurance"] = "human_audited"
    return result


def verify(snapshot, request, *, now, output=b"", report=b""):
    """Validate an explicitly trusted snapshot; malformed nested values block."""
    try:
        return _verify(snapshot, request, now=now, output=output, report=report)
    except (TypeError, KeyError, IndexError, UnicodeError, RecursionError, OverflowError) as exc:
        raise Blocked(f"malformed trust-boundary value: {type(exc).__name__}") from exc


def _git_executable(root):
    """Resolve an absolute native executable without Windows cwd lookup."""
    cwd, source = Path.cwd().resolve(), Path(root).resolve()
    excluded = [source]
    if cwd != Path(cwd.anchor):
        excluded.append(cwd)
    module = Path(__file__).resolve()
    if module.parent.name == "ops":
        excluded.append(module.parent.parent)
    name = "git.exe" if os.name == "nt" else "git"
    for entry in os.get_exec_path():
        directory = Path(entry)
        if not directory.is_absolute():
            continue
        candidate = (directory / name).resolve()
        if any(candidate.is_relative_to(path) for path in excluded):
            continue
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    raise Blocked("trusted absolute Git executable unavailable outside checkout/cwd")


def _git(root, *args):
    try:
        # Git configuration environments are caller claims. Retain platform
        # HTTP(S)_PROXY and non-Git CA trust variables, never Git TLS/config overrides.
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith("GIT_")}
        env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
                   GIT_CONFIG_NOSYSTEM="1", GIT_NO_REPLACE_OBJECTS="1", GIT_TERMINAL_PROMPT="0", GIT_NO_LAZY_FETCH="1")
        p = subprocess.run([_GIT_BINARY or _git_executable(root), "-C", str(root), *args], env=env, capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as exc:
        raise Blocked(f"Git unavailable: {type(exc).__name__}") from exc
    require(p.returncode == 0, f"Git {args[0]} failed (rc={p.returncode})")
    return p.stdout


def _raw_commit(root, oid):
    """Read stored parent edges, ignoring grafts, shallow boundaries and graphs."""
    digest(oid, "raw commit OID", True)
    header = _git(root, "cat-file", "commit", oid).split(b"\n\n", 1)[0].splitlines()
    require(header and header[0].startswith(b"tree "), "raw commit missing tree")
    tree = header[0][5:].decode("ascii")
    digest(tree, "raw commit tree", True)
    parents, parent_section = [], True
    for line in header[1:]:
        if line.startswith(b"parent "):
            require(parent_section, "raw parent outside contiguous parent header")
            parent = line[7:].decode("ascii")
            digest(parent, "raw commit parent", True)
            parents.append(parent)
        else:
            parent_section = False
    return tree, parents


def _raw_ancestor(root, base, head):
    # No merge-base/rev-list: their history can be rewritten by info/grafts,
    # including a common-dir graft in a linked worktree. cat-file reads bytes.
    _raw_commit(root, base)
    pending, visited = [head], set()
    while pending:
        oid = pending.pop()
        if oid == base:
            return True
        if oid in visited:
            continue
        visited.add(oid)
        require(len(visited) <= 100000, "raw ancestry proof exceeds bounded inventory")
        pending.extend(_raw_commit(root, oid)[1])
    return False


def _live_oid(root, fixture):
    """Transport only in a fresh trusted store, never the source checkout."""
    origin = f"https://github.com/{REPOSITORY}.git"
    if fixture:
        origin = _git(root, "config", "--local", "--get", "remote.origin.url").decode("utf-8").strip()
        require(origin.startswith("/") or bool(re.match(r"[A-Za-z]:[/\\]", origin)), "fixture requires local absolute Git remote")
    transport = ("-c", "http.sslVerify=true", "-c", "http.followRedirects=false",
                 "-c", "credential.helper=", "-c", "protocol.allow=never",
                 "-c", "protocol.https.allow=always", "-c", f"protocol.file.allow={'always' if fixture else 'never'}")
    _git(root, *transport, "fetch", "--quiet", "--no-tags", origin, "+refs/heads/master:refs/remotes/origin/master")
    oid = _git(root, "rev-parse", "refs/remotes/origin/master^{commit}").decode("ascii").strip()
    digest(oid, "live OID", True)
    require(_git(root, *transport, "ls-remote", "--exit-code", origin, "refs/heads/master").split() == [oid.encode(), b"refs/heads/master"], "live master differs from fetched canonical OID")
    return oid


def _blob(root, oid, path):
    require(type(path) is str and not PurePosixPath(path).is_absolute() and ".." not in PurePosixPath(path).parts and "\\" not in path, "unsafe canonical path")
    # Check every ancestor as well as the leaf. A symlink is never policy data.
    parts = PurePosixPath(path).parts
    for i in range(1, len(parts) + 1):
        name = "/".join(parts[:i])
        entry = _git(root, "ls-tree", "-z", oid, "--", name).split(b"\0")
        require(len(entry) == 2 and entry[-1] == b"", "canonical path missing/ambiguous")
        meta, got = entry[0].split(b"\t", 1)
        require(got.decode("utf-8") == name and meta.split()[:2] in ([b"040000", b"tree"], [b"100644", b"blob"], [b"100755", b"blob"]), "canonical symlink/non-file rejected")
        require(meta.split()[1] == (b"blob" if i == len(parts) else b"tree"), "canonical path type mismatch")
    return _git(root, "show", f"{oid}:{path}")


def verify_live(root, expected_oid, request, now, fixture, output, report, source_root):
    """Run only from a trusted canonical copy; caller-supplied API data is not trust."""
    require(type(fixture) is bool, "fixture flag must be bool")
    oid = _live_oid(root, fixture)
    require(oid == expected_oid, "canonical moved during verifier bootstrap; retry from fresh snapshot")
    verifier = _blob(root, oid, VERIFIER_PATH)
    snap = Snapshot(oid, sha256(verifier), _blob(root, oid, REGISTRY_PATH), fixture)
    result = verify(snap, request, now=now, output=output, report=report)
    b = request["binding"]
    require(_raw_commit(source_root, b["head_sha"])[0] == b["tree_sha"], "source H/tree mismatch")
    require(_raw_ancestor(source_root, b["base_sha"], b["head_sha"]), "source base is not a raw-object ancestor of head")
    p = one(parse_json(snap.registry_raw)["policies"], lambda x: x["grant_id"] == b["grant_id"], "policy")
    require(sha256(_blob(source_root, b["head_sha"], p["spec_path"])) == b["spec_hash"], "source spec hash mismatch")
    result["positive_evidence"].append("Git source base/head/tree/spec bytes")
    return result


def _local_file(path):
    p = Path(path).absolute()
    require(all(not ancestor.is_symlink() for ancestor in (p, *p.parents)), "local symlink input rejected")
    require(p.is_file(), "input must be a regular file")
    return p.read_bytes()


def main(argv=None):
    global _GIT_BINARY
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="source Git checkout; canonical transport is isolated")
    parser.add_argument("--request", required=True, help="JSON claims; never a policy path")
    parser.add_argument("--raw-output")
    parser.add_argument("--report")
    parser.add_argument("--fixture", action="store_true", help="local Git test only; result cannot authorize production")
    args = parser.parse_args(argv)
    try:
        root = Path(args.root).resolve(strict=True)
        _GIT_BINARY = _git_executable(root)
        request = parse_json(_local_file(args.request))
        output = _local_file(args.raw_output) if args.raw_output else b""
        report = _local_file(args.report) if args.report else b""
        # No candidate imports or PYTHONPATH: execute the live pinned implementation.
        # Canonical verifier independently fetches/readbacks OID and fixed records.
        with tempfile.TemporaryDirectory(prefix="codex-routing-canon-") as td:
            store = Path(td) / "canonical.git"
            _git(td, "init", "--quiet", "--bare", "--template=", str(store))
            if args.fixture:
                fixture_origin = _git(root, "config", "--local", "--get", "remote.origin.url").decode("utf-8").strip()
                _git(store, "remote", "add", "origin", fixture_origin)
            oid = _live_oid(store, args.fixture)
            verifier = _blob(store, oid, VERIFIER_PATH)
            module = Path(td) / "codex_routing.py"
            module.write_bytes(verifier)
            payload = {"root": str(store), "source_root": str(root), "oid": oid, "request": request, "now": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "fixture": args.fixture,
                       "output": output.hex(), "report": report.hex()}
            script = ("import importlib.util,json,sys; s=importlib.util.spec_from_file_location('canonical_routing',sys.argv[1]); "
                      "m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m); "
                      "p=json.load(sys.stdin); "
                      "r=m.verify_live(p['root'],p['oid'],p['request'],p['now'],p['fixture'],bytes.fromhex(p['output']),bytes.fromhex(p['report']),p['source_root']); "
                      "print(json.dumps(r,sort_keys=True))")
            run = subprocess.run([sys.executable, "-I", "-B", "-c", script, str(module)], input=canonical_bytes(payload), capture_output=True, timeout=180,
                                 env={**os.environ, "PATH": str(Path(_GIT_BINARY).parent)})
            require(run.returncode == 0, f"canonical verifier blocked/unavailable (rc={run.returncode}): {run.stderr.decode('utf-8', 'replace')[-1600:]}")
            result = parse_json(run.stdout)
            require(type(result) is dict and result.get("status") == "validated" and result.get("canonical_oid") == oid
                    and result.get("test_only") is args.fixture and result.get("positive_evidence"), "canonical verifier returned no positive evidence")
            print(json.dumps(result, sort_keys=True))
            return 0
    except (Blocked, OSError, UnicodeError, subprocess.SubprocessError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "blocked", "positive_evidence": [], "reason": str(exc), "test_only": args.fixture, "limitations": LIMITATIONS}, sort_keys=True))
        return 12


if __name__ == "__main__":
    sys.exit(main())
