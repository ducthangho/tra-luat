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

Round 5 found the same disease one level up.  ``SourcePin`` existed, and the retained semantic
verification still omitted the repository, the lease stop and the integration observation, because
those fields were compared *somewhere else* — in ``controller.py``'s own constant table, in the
preflight's caller-supplied expectation dict — and a field nobody put in the table is a field nobody
checks.  So the structure now carries the whole identity, including the parts that are only known at
run time (current head, tree, sole parent, surface, runner, selection, outcomes, run and artifact
identity), and :func:`SourcePin.retained_identity` is the *only* place that shape is written down.

It also carries its own authentication.  :func:`SourcePin.validate_sealed_document` compares a sealed
Dispatcher pin document field-for-field against these constants, so "the expectations" stop being
whatever the caller passed in: round 5's commit boundary rederived authority from mutually consistent
caller expectations, which is a comparison of an input against itself.
"""

from __future__ import annotations

import dataclasses


class PinMismatch(Exception):
    """The sealed document and the typed pin disagree.  Raised, never returned as a flag."""


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
    integration_ref: str
    write_prefix: str
    packet_id: str
    phase_key: str

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

    def integration_document(self) -> dict[str, object]:
        """The integration observation, named by ref *and* by both object ids.

        Round 5's retained evidence named no integration identity at all, so a run that had adopted
        the integration commit as its own start and a run that had merely observed it produced the
        same artifact.  §2 makes integration read-only; that is a claim about a specific commit, and
        a claim about a specific commit has to name the commit.
        """
        return {
            "ref": self.integration_ref,
            "head": self.integration_observation.head,
            "tree": self.integration_observation.tree,
            "observation_only": True,
        }

    def retained_identity(
        self,
        *,
        current_head: str,
        current_tree: str,
        sole_parent: str,
        write_prefix: str,
        surface: str,
        runner: object,
        test_selection: object,
        raw_outcomes: object,
        run_id: str,
        artifact_identity: object,
    ) -> dict[str, object]:
        """Everything the retained authority class must name, from one place.

        The static half comes from this pin; the run half is measured and passed in.  Both halves
        live in one document because ``verify`` has to compare them *together*: a correct pin beside
        an unrelated run is the shape round 5 accepted, where the wrapper named this head and the
        payload named nothing at all.
        """
        return {
            "repository": self.repository,
            "authority": self.authority_document(),
            "expected_authority": self.expected_authority(),
            "lease": self.lease_document(),
            "candidate_ref": self.candidate_ref,
            "candidate_start_head": self.repair_base.head,
            "candidate_start_tree": self.repair_base.tree,
            "repair_base": {"head": self.repair_base.head, "tree": self.repair_base.tree},
            "integration": self.integration_document(),
            "integration_observation_head": self.integration_observation.head,
            "integration_observation_tree": self.integration_observation.tree,
            "integration_is_observation_only": True,
            "current": {
                "head": current_head,
                "tree": current_tree,
                "sole_parent": sole_parent,
            },
            "write_set": {
                "effective_write_prefix": write_prefix,
                "declared_write_prefix": self.write_prefix,
            },
            "execution": {
                "surface": surface,
                "runner": runner,
                "test_selection": list(test_selection),
                "raw_outcomes": raw_outcomes,
            },
            "run": {"run_id": run_id, "artifact_identity": artifact_identity},
        }

    def sealed_document(self) -> dict[str, object]:
        """The Dispatcher-shaped sealed pin these constants correspond to.

        Written here so a fixture cannot invent its own shape and so
        :meth:`validate_sealed_document` has one thing to compare against.
        """
        return {
            "schema_version": 1,
            "kind": "dispatcher_source_pin",
            "repository": self.repository,
            "mission_issue": self.mission_issue,
            "mission_revision": self.mission_revision,
            "mission_plan_hash": self.mission_plan_hash,
            "packet_issue": self.packet_issue,
            "packet_id": self.packet_id,
            "phase_key": self.phase_key,
            "packet_revision": self.packet_revision,
            "generation": self.packet_generation,
            "attempt": self.packet_attempt,
            "packet_spec_hash": self.packet_spec_hash,
            "repair_base_commit": self.repair_base.head,
            "repair_base_tree": self.repair_base.tree,
            "candidate_ref": self.candidate_ref,
            "integration_ref": self.integration_ref,
            "integration_head_observed_only": self.integration_observation.head,
            "integration_tree_observed_only": self.integration_observation.tree,
            "effective_write_prefix": self.write_prefix,
            "lease_id": self.lease_id,
            "lease_effective_stop_utc": self.lease_effective_stop_utc,
        }

    # The exact keys a sealed document must carry, and where each one is answered from.  A key that
    # is absent is as red as a key that disagrees: round 5's sealed pin was only ever *hashed*, so a
    # document whose bytes matched a recorded digest was accepted without anyone reading a field of
    # it, and a digest says nothing about what the fields say.
    SEALED_FIELDS = (
        "repository",
        "mission_issue",
        "mission_revision",
        "mission_plan_hash",
        "packet_issue",
        "packet_revision",
        "generation",
        "attempt",
        "packet_spec_hash",
        "repair_base_commit",
        "repair_base_tree",
        "candidate_ref",
        "integration_ref",
        "integration_head_observed_only",
        "integration_tree_observed_only",
        "effective_write_prefix",
        "lease_id",
        "lease_effective_stop_utc",
    )

    def validate_sealed_document(self, document: object) -> dict[str, object]:
        """Compare a sealed pin document field-for-field against these constants.

        Raises :class:`PinMismatch` on the first disagreement.  The caller turns that into whatever
        typed rejection its layer speaks; this module deliberately does not import the error
        vocabulary, so the pin stays the leaf of the dependency graph and cannot acquire a cycle.
        """
        if not isinstance(document, dict):
            raise PinMismatch("the sealed source pin is not a JSON object")
        expected = self.sealed_document()
        missing = [key for key in self.SEALED_FIELDS if key not in document]
        if missing:
            raise PinMismatch("the sealed source pin omits %d pinned fields" % len(missing))
        drifted = [key for key in self.SEALED_FIELDS if document[key] != expected[key]]
        if drifted:
            raise PinMismatch("the sealed source pin disagrees on %d pinned fields" % len(drifted))
        if document.get("kind") != "dispatcher_source_pin":
            raise PinMismatch("the sealed document is not a dispatcher source pin")
        if document["integration_head_observed_only"] == self.repair_base.head:
            raise PinMismatch("the sealed pin names integration as the repair base")
        return {
            "sealed_fields_compared": len(self.SEALED_FIELDS),
            "sealed_pin_agrees_with_typed_pin": True,
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
    integration_ref="refs/heads/mission/76/integration",
    write_prefix=".github/coordination/reviewer_bootstrap/launcher/",
    packet_id="wp125",
    phase_key="RA-04",
)
