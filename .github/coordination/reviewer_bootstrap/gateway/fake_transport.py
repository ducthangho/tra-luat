"""Offline additive transport built solely on the integrated RA-01 fake GitHub store."""

from __future__ import annotations

import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOTSTRAP_ROOT = os.path.dirname(HERE)
if BOOTSTRAP_ROOT not in sys.path:
    sys.path.insert(0, BOOTSTRAP_ROOT)

from core.fake_github import FakeGitHub, FakeGitHubError  # noqa: E402


class FakeGatewayGitHub(FakeGitHub):
    """RA-01 fake store with closed-operation materialization for durable readback.

    The inherited `post_heartbeat` and `post_verdict` operations are the only write surface.
    `read_comment` remains the inherited closed operation name, but its bound handler materializes
    a comment-shaped object from the actual RA-01 ledger row.  No direct comments mutation exists.
    """

    @staticmethod
    def _materialize_gateway_object(reconcile_key: str, record: object):
        if not isinstance(record, dict) or not isinstance(record.get("payload"), dict):
            return None
        payload = record["payload"]
        required = {
            "object_id",
            "author",
            "repository",
            "lane",
            "reviewed_sha",
            "body",
        }
        if not required.issubset(payload):
            return None
        return {
            "id": payload["object_id"],
            "issue_number": record.get("issue_number"),
            "body": payload["body"],
            "author": payload["author"],
            "repository": payload["repository"],
            "lane": payload["lane"],
            "reviewed_sha": payload["reviewed_sha"],
            "operation": record.get("op"),
            "reconcile_key": reconcile_key,
            "gateway_created": True,
        }

    def _gateway_objects(self) -> dict[int, dict[str, object]]:
        objects = {}
        for reconcile_key in self.ledger.keys():
            materialized = self._materialize_gateway_object(
                reconcile_key, self.ledger.get(reconcile_key)
            )
            if materialized is not None and isinstance(materialized["id"], int):
                objects[materialized["id"]] = materialized
        return objects

    def _op_read_comment(self, params):
        object_id = params["comment_id"]
        if object_id in self.comments:
            return copy.deepcopy(self.comments[object_id])
        materialized = self._gateway_objects().get(object_id)
        if materialized is None:
            raise FakeGitHubError(404, "No comment %d" % object_id, operation="read_comment")
        return copy.deepcopy(materialized)

    def gateway_write_count(self) -> int:
        return len(self._gateway_objects())

    def total_durable_write_count(self) -> int:
        return len(self.ledger)

    def snapshot_objects(self) -> dict[int, dict[str, object]]:
        objects = copy.deepcopy(self.comments)
        objects.update(copy.deepcopy(self._gateway_objects()))
        return objects
