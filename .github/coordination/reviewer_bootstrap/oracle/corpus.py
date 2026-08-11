"""Blind three-layer corpus for the five protocol schemas."""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import random
from typing import Iterable


@dataclasses.dataclass(frozen=True)
class Case:
    schema_name: str
    case_id: str
    layer: str
    expected: bool
    document: object
    raw: str
    held_out: bool

    @property
    def locator(self) -> str:
        return "objects/%s.json" % self.case_id


SHA40 = "a" * 40
SHA64 = "b" * 64
BASES = {
    "handoff.schema.json": {
        "schema_version": 1, "packet_id": "wp86", "generation": 4, "spec_hash": SHA64,
        "provider": "codex", "role": "executor", "session_id": "session-1", "head_sha": SHA40,
        "status": "done", "next_role": "reviewer", "manual_next_action": "review",
        "copyable_prompt": "review exact head", "tests": [{"name": "gate", "status": "passed", "evidence": "rc=0"}],
    },
    "review.schema.json": {
        "schema_version": 1, "packet_id": "wp86", "generation": 4, "provider": "human",
        "role": "reviewer", "session_id": "review-1", "reviewed_sha": SHA40,
        "independent_from_executor_session": True, "review_axes": ["spec", "standards_security"],
        "tests": [{"name": "gate", "status": "not_run", "evidence": "none", "reason": "offline"}],
        "findings": [], "verdict": "approve", "assurance": "cross_approved",
    },
    "land.schema.json": {
        "schema_version": 1, "authorization_id": "auth-1", "decision": "approved",
        "mission_id": "gh-76", "authorized_head_sha": SHA40, "actor": "owner",
        "role": "approver_land_operator", "session_id": "land-1",
    },
    "state.schema.json": {
        "schema_version": 1, "mission_issue": 76, "mission_revision": 3,
        "mission_state": "running", "packet_id": "wp86", "packet_revision": 4,
        "spec_hash": SHA64, "packet_state": "ready", "lease": None,
        "budget": {"used": 1, "reserved": 1, "limit": 71}, "last_consumed_event_id": 10,
    },
    "command.schema.json": {
        "schema_version": 1, "command": "/mission pause", "mission_id": "gh-76",
        "actor": "owner", "expected_state_revision": 3,
    },
}


def _mutations(name: str, base: dict[str, object]) -> list[dict[str, object]]:
    def changed(**updates):
        value = copy.deepcopy(base); value.update(updates); return value
    missing = copy.deepcopy(base); missing.pop(next(iter({
        "handoff.schema.json": ("next_role",), "review.schema.json": ("verdict",),
        "land.schema.json": ("mission_id",), "state.schema.json": ("mission_issue",),
        "command.schema.json": ("actor",),
    }[name])))
    cases = [missing]
    if name == "handoff.schema.json":
        cases += [changed(generation="4"), changed(provider="unknown"), changed(spec_hash="bad"), changed(role="reviewer")]
        nested=copy.deepcopy(base); nested["tests"]=[{"name":"gate","status":"not_run","evidence":"none"}]; cases.append(nested)
    elif name == "review.schema.json":
        cases += [changed(generation=0), changed(role="executor"), changed(reviewed_sha="bad"), changed(review_axes=["spec"]), changed(independent_from_executor_session=False)]
    elif name == "land.schema.json":
        cases += [changed(schema_version=2), changed(mission_id="76"), changed(authorized_head_sha="bad"), changed(role="reviewer")]
        empty={"schema_version":1}; cases.append(empty)
    elif name == "state.schema.json":
        cases += [changed(mission_state="unknown"), changed(packet_id="86"), changed(last_consumed_event_id=-1), changed(spec_hash="bad")]
        lease=copy.deepcopy(base); lease["lease"]={"packet_id":"wp86"}; cases.append(lease)
    elif name == "command.schema.json":
        cases += [changed(command="/shell exec"), changed(actor=""), changed(expected_state_revision=-1), changed(mission_id="76")]
        conditional=changed(command="/land apply"); conditional.pop("mission_id",None); cases.append(conditional)
    return cases


def build(seed: int = 8604) -> list[Case]:
    cases: list[Case] = []
    for schema_name, base in BASES.items():
        documents: list[tuple[str, bool, object, bool]] = [
            ("valid", True, copy.deepcopy(base), False),
            ("semantic", True, {**dict(reversed(list(base.items()))), "x_unrelated": "allowed"}, False),
            ("semantic", True, copy.deepcopy(base), True),
        ]
        documents += [("invalid", False, value, index == len(_mutations(schema_name, base)) - 1) for index, value in enumerate(_mutations(schema_name, base))]
        for index, (layer, expected, document, held_out) in enumerate(documents):
            token = hashlib.sha256(("%d:%s:%d" % (seed, schema_name, index)).encode()).hexdigest()[:16]
            if layer == "semantic":
                raw = json.dumps(document, ensure_ascii=False, indent=2, sort_keys=index % 2 == 0) + "\n"
            else:
                raw = json.dumps(document, ensure_ascii=False, separators=(",", ":"), sort_keys=False)
            cases.append(Case(schema_name, token, layer, expected, document, raw, held_out))
    random.Random(seed).shuffle(cases)
    return cases
