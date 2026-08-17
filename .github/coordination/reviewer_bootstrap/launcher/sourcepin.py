"""The one authoritative source-pin structure (Issue 125 §2, WP125-RV-006-R4).

Every exact value this Packet is bound to lives here once, in a frozen typed structure, and both
production validation and retained evidence read it.  Round 4 had the same values written out in
three places — the preflight expectations, the controller's semantic predicate and the selftest
fixture — and they drifted exactly as separately-maintained copies do: the retained evidence carried
the *integration* commit ``60446be6…``/``5d19b56a…`` where it should have carried the durable
generation-2 repair base ``3556468f…``/``e46a231e…``, and the candidate start head and tree were
accepted as merely OID-shaped with no comparison at all.  Shape is not identity: ``"0"*40`` is
OID-shaped.

Two commits matter and they are not the same commit:

* ``REPAIR_BASE`` is what generation 2 was cut from and what the lease names — the identity a claim
  is bound to.
* ``INTEGRATION`` is an observation only.  §2 says master and integration are read-only observations
  and no synchronization is authorized, so this value exists to be *compared against*, never to be
  adopted as the candidate's own.
"""

from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class Commit:
    """A commit named by both of its exact object ids."""

    head: str
    tree: str

    def matches(self, head: object, tree: object) -> bool:
        return head == self.head and tree == self.tree


@dataclasses.dataclass(frozen=True)
class SourcePin:
    """The complete durable identity of this Packet's source."""

    repository: str
    mission_issue: int
    mission_revision: int
    mission_plan_hash: str
    packet_issue: int
    packet_revision: int
    packet_generation: int
    packet_attempt: int
    packet_spec_hash: str
    candidate_ref: str
    repair_base: Commit
    integration_observation: Commit
    lease_id: str
    lease_effective_stop_utc: str

    def expected_authority(self) -> dict[str, object]:
        """The expectation table preflight compares observations against."""
        return {
            "repository": self.repository,
            "mission_issue": self.mission_issue,
            "mission_revision": self.mission_revision,
            "mission_plan_hash": self.mission_plan_hash,
            "packet_issue": self.packet_issue,
            "packet_revision": self.packet_revision,
            "packet_generation": self.packet_generation,
            "packet_attempt": self.packet_attempt,
            "packet_spec_hash": self.packet_spec_hash,
        }

    def authority_document(self) -> dict[str, object]:
        """The nested authority shape carried by the retained evidence."""
        return {
            "repository": self.repository,
            "mission": {
                "issue": self.mission_issue,
                "revision": self.mission_revision,
                "plan_hash": self.mission_plan_hash,
            },
            "packet": {
                "issue": self.packet_issue,
                "revision": self.packet_revision,
                "generation": self.packet_generation,
                "attempt": self.packet_attempt,
                "spec_hash": self.packet_spec_hash,
            },
        }

    def lease_document(self) -> dict[str, object]:
        return {
            "lease_id": self.lease_id,
            "effective_stop_utc": self.lease_effective_stop_utc,
            "generation": self.packet_generation,
            "candidate_ref": self.candidate_ref,
            "candidate_start_head": self.repair_base.head,
        }

    def retained_identity(self) -> dict[str, object]:
        """Everything the retained authority class must name, from one place."""
        return {
            "authority": self.authority_document(),
            "expected_authority": self.expected_authority(),
            "lease": self.lease_document(),
            "candidate_ref": self.candidate_ref,
            "candidate_start_head": self.repair_base.head,
            "candidate_start_tree": self.repair_base.tree,
            "integration_observation_head": self.integration_observation.head,
            "integration_observation_tree": self.integration_observation.tree,
            "integration_is_observation_only": True,
        }


PIN = SourcePin(
    repository="ducthangho/tra-luat",
    mission_issue=76,
    mission_revision=6,
    mission_plan_hash="ac5d5180be3de124dce002041683c3d6926aa60b36d39c7cad02136fd0776b9a",
    packet_issue=125,
    packet_revision=1,
    packet_generation=2,
    packet_attempt=1,
    packet_spec_hash="b8e3387d13cf60974a3e7a35350557605df52b282666a401b7b5b4100e42f3f3",
    candidate_ref="refs/heads/agent/wp125-g2-claude",
    repair_base=Commit(
        head="3556468f25c31ff8a0fad651559cd20b67f4becf",
        tree="e46a231ea0686bde717f9f681143cd38d2ddb67e",
    ),
    integration_observation=Commit(
        head="60446be6467347e7242d5e03c001c19794e6e96d",
        tree="5d19b56a32d5fd127141ad0cd0824b8c976ba877",
    ),
    lease_id="wp125-r1-g2-a1-lease-3556468f-b8e3387d",
    lease_effective_stop_utc="2026-08-17T19:36:38.140Z",
)
