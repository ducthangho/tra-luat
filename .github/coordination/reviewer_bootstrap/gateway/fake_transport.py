"""Offline additive transport built solely on the integrated RA-01 fake GitHub store."""

from __future__ import annotations

import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOTSTRAP_ROOT = os.path.dirname(HERE)
if BOOTSTRAP_ROOT not in sys.path:
    sys.path.insert(0, BOOTSTRAP_ROOT)

from core.fake_github import FakeGitHub  # noqa: E402


class FakeGatewayGitHub(FakeGitHub):
    """RA-01 fake store plus additive comment metadata needed for readback tests.

    The inherited `read_comment`, `post_heartbeat` and `post_verdict` operations remain the only
    executed operation surface.  Extra metadata lives on the same fake comment object and is
    returned by the inherited explicit read dispatcher.
    """

    def add_gateway_comment(self, record: dict[str, object]) -> None:
        object_id = int(record["id"])
        if object_id in self.comments:
            raise ValueError("gateway object id collision")
        self.comments[object_id] = copy.deepcopy(record)

    def gateway_write_count(self) -> int:
        return sum(1 for record in self.comments.values() if record.get("gateway_created") is True)

    def total_durable_write_count(self) -> int:
        return len(self.ledger)

    def snapshot_objects(self) -> dict[int, dict[str, object]]:
        return copy.deepcopy(self.comments)
