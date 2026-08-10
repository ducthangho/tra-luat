"""Fake GitHub store (acceptance §3, mục "Fake GitHub store" của #77).

Bất biến:
  - Cho phép chạy TOÀN BỘ test suite mà KHÔNG chạm mạng. Store là dict thuần; module này KHÔNG
    import socket/http/urllib và không có đường ra ngoài tiến trình.
  - Mô phỏng cả đường LỖI - 403, 404, 409, rate-limit - chứ không chỉ đường hạnh phúc.

Quan hệ với idempotence: hai op ghi (post_heartbeat, post_verdict) đi qua Ledger. Cùng
`reconcile_key` + cùng payload là replay idempotent; cùng `reconcile_key` + payload KHÁC là 409
CONFLICT. Phân biệt hai ca đó là điểm khác nhau giữa "khử trùng lặp" và "nuốt mất dữ liệu".

ZERO credential: module này không đọc biến môi trường nào. Không có tham số token, không có
header auth, không có chỗ để nhét credential vào kể cả khi ai đó muốn.
"""

import json

from . import operations
from .ledger import Ledger

# Các đường lỗi mô phỏng được. rate_limit dùng 429 như GitHub.
ERROR_KINDS = {
    "403": (403, "Forbidden: actor lacks permission for this lane"),
    "404": (404, "Not Found"),
    "409": (409, "Conflict"),
    "rate_limit": (429, "API rate limit exceeded"),
}


class FakeGitHubError(Exception):
    """Lỗi có status như GitHub trả. Mang status máy đọc được, không chỉ là chuỗi."""

    def __init__(self, status, message, operation=None):
        self.status = int(status)
        self.operation = operation
        super().__init__("%s %s (operation=%s)" % (self.status, message, operation))


class FakeGitHub:
    """Store GitHub giả, hoàn toàn trong tiến trình."""

    def __init__(self, ledger_path, repo="ducthangho/tra-luat"):
        self.repo = repo
        self.ledger = Ledger(ledger_path)
        self.issues = {}
        self.comments = {}
        self.pulls = {}
        self.ci_runs = {}
        self.diffs = {}
        self._injected = {}
        self.calls = []

    # ── dựng dữ liệu ────────────────────────────────────────────────────────
    def add_issue(self, number, body, labels=()):
        self.issues[int(number)] = {"number": int(number), "body": body, "labels": list(labels)}

    def add_comment(self, comment_id, issue_number, body):
        self.comments[int(comment_id)] = {
            "id": int(comment_id),
            "issue_number": int(issue_number),
            "body": body,
        }

    def add_pull(self, number, head_sha, base, draft=True):
        self.pulls[int(number)] = {
            "number": int(number),
            "head_sha": head_sha,
            "base": base,
            "draft": bool(draft),
        }

    def add_ci_run(self, run_id, conclusion):
        self.ci_runs[int(run_id)] = {"id": int(run_id), "conclusion": conclusion}

    def add_diff(self, pull_number, diff_text):
        self.diffs[int(pull_number)] = diff_text

    # ── bơm lỗi ─────────────────────────────────────────────────────────────
    def inject(self, op_name, kind, times=1):
        """Bơm `times` lần lỗi `kind` cho op `op_name`. Hết lượt thì op trở lại bình thường."""
        if kind not in ERROR_KINDS:
            raise ValueError("unknown error kind: %r; known: %s" % (kind, ", ".join(sorted(ERROR_KINDS))))
        self._injected.setdefault(op_name, []).extend([kind] * int(times))

    def _maybe_fail(self, op_name):
        queue = self._injected.get(op_name)
        if queue:
            status, message = ERROR_KINDS[queue.pop(0)]
            raise FakeGitHubError(status, message, operation=op_name)

    # ── điểm vào DUY NHẤT ───────────────────────────────────────────────────
    def call(self, op_name, params):
        """Kiểm schema TRƯỚC, rồi mới chạy. Không có đường nào vòng qua validate()."""
        checked = operations.validate(op_name, params)
        self.calls.append(op_name)
        self._maybe_fail(op_name)
        if checked["repo"] != self.repo:
            raise FakeGitHubError(404, "No such repository %r" % checked["repo"], operation=op_name)
        return getattr(self, "_op_" + op_name)(checked)

    # ── op đọc ──────────────────────────────────────────────────────────────
    def _op_read_issue(self, p):
        issue = self.issues.get(p["issue_number"])
        if issue is None:
            raise FakeGitHubError(404, "No issue #%d" % p["issue_number"], operation="read_issue")
        return dict(issue)

    def _op_read_comment(self, p):
        comment = self.comments.get(p["comment_id"])
        if comment is None:
            raise FakeGitHubError(404, "No comment %d" % p["comment_id"], operation="read_comment")
        return dict(comment)

    def _op_read_pr(self, p):
        pull = self.pulls.get(p["pull_number"])
        if pull is None:
            raise FakeGitHubError(404, "No pull #%d" % p["pull_number"], operation="read_pr")
        return dict(pull)

    def _op_read_ci_run(self, p):
        run = self.ci_runs.get(p["run_id"])
        if run is None:
            raise FakeGitHubError(404, "No CI run %d" % p["run_id"], operation="read_ci_run")
        return dict(run)

    def _op_read_diff(self, p):
        diff = self.diffs.get(p["pull_number"])
        if diff is None:
            raise FakeGitHubError(404, "No diff for pull #%d" % p["pull_number"], operation="read_diff")
        return {"pull_number": p["pull_number"], "diff": diff}

    # ── op uỷ quyền ─────────────────────────────────────────────────────────
    def _op_run_test(self, p):
        """RA-01 chỉ khai schema. Thực thi thật là việc của sandbox RA-02.

        Trả marker tường minh thay vì giả vờ đã chạy - một kết quả test bịa còn tệ hơn không có
        kết quả nào. Đây đúng lớp lỗi "in 168/168 mà chẳng chạy gì" đã đo ở #54.
        """
        return {
            "delegated": True,
            "executed_here": False,
            "reason": "sandbox execution is RA-02 scope; RA-01 defines the operation only",
            "command": p["command"],
            "timeout_seconds": p.get("timeout_seconds"),
        }

    # ── op ghi (idempotent theo reconcile_key) ──────────────────────────────
    def _write(self, op_name, p, record):
        key = p["reconcile_key"]
        existing = self.ledger.get(key)
        if existing is not None and existing != record:
            raise FakeGitHubError(
                409,
                "reconcile_key %r already recorded with different content" % key,
                operation=op_name,
            )
        created, stored = self.ledger.record(key, record)
        return {"created": created, "reconcile_key": key, "record": stored}

    def _op_post_heartbeat(self, p):
        record = {
            "op": "post_heartbeat",
            "issue_number": p["issue_number"],
            "payload": p["payload"],
        }
        return self._write("post_heartbeat", p, record)

    def _op_post_verdict(self, p):
        record = {
            "op": "post_verdict",
            "issue_number": p["issue_number"],
            "reviewed_sha": p["reviewed_sha"],
            "verdict": p["verdict"],
            "payload": p.get("payload", {}),
        }
        return self._write("post_verdict", p, record)

    # ── trạng thái ──────────────────────────────────────────────────────────
    def state_hash(self):
        return self.ledger.state_hash()

    def snapshot(self):
        return json.dumps(
            {"repo": self.repo, "ledger": self.ledger.keys()},
            ensure_ascii=False,
            sort_keys=True,
        )
