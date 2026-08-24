#!/usr/bin/env python3
"""Đường CỨU HỘ tới MCP github bằng JSON-RPC thẳng — khi công cụ `mcp__github__*` vắng mặt.

VÌ SAO CÓ TỆP NÀY (đo 24-08-2026): sau một lần máy chủ MCP ngắt rồi nối lại, bộ công cụ tụt từ
55 xuống 44 và CẢ NHÓM `actions_*` biến mất — tức phiên mất khả năng gọi `workflow_dispatch` và
đọc log job, đúng lúc cần đo Windows trước khi land. `CLAUDE.md` đã ghi rằng phiên tự dựng lại
được đường ấy bằng `GITHUB_PAT`; nhưng KIẾN THỨC không phải CÔNG CỤ, và lần ấy phải viết lại từ
đầu giữa lúc đang cần. Tệp này là bản chạy được của đúng lời dặn đó.

Hai điểm cuối, đo được:
    /mcp/           bộ công cụ chung (repo, PR, issue, …)
    /mcp/x/actions  actions_get · actions_list · actions_run_trigger · get_job_logs

Dùng:
    python3 mcp_gh.py --liet-ke [--path /mcp/x/actions]
    python3 mcp_gh.py <ten-cong-cu> '<json-doi-so>' [--path /mcp/x/actions]

Mã thoát: 0 ok · 2 sai đối số · 3 KHÔNG ĐO ĐƯỢC (thiếu credential / initialize hỏng).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

DIEM_CUOI = "https://api.githubcopilot.com"
PHIEN_BAN_GIAO_THUC = "2025-06-18"


def _mo_mac_dinh(req, timeout):
    return urllib.request.urlopen(req, timeout=timeout)


def tach_than(raw: str) -> str:
    """Nhặt tải trọng JSON ra khỏi phản hồi — thân có thể là JSON thuần HOẶC SSE.

    SSE trả nhiều dòng `data:`; cái CUỐI mới là kết quả. Trả nguyên chuỗi, KHÔNG cắt:
    bản đầu của công cụ này cắt 6000 ký tự "cho gọn" và làm JSON hỏng ở giữa — phép đo
    tự làm hỏng thứ nó đang đo. Muốn ngắn thì cắt Ở PHÍA NGƯỜI GỌI.
    """
    for dong in reversed(raw.splitlines()):
        if dong.startswith("data:"):
            return dong[5:].strip()
    return raw


class Phien:
    def __init__(self, path: str = "/mcp/", token: str | None = None, mo=None, timeout: int = 90):
        self.url = DIEM_CUOI + path
        self.token = token
        self.sid: str | None = None
        self.n = 0
        self._mo = mo or _mo_mac_dinh
        self.timeout = timeout

    def goi(self, method: str, params=None, bao_tin: bool = False):
        """Một lời gọi JSON-RPC. `bao_tin=True` ⇒ notification: KHÔNG có `id` (đúng đặc tả)."""
        msg = {"jsonrpc": "2.0", "method": method}
        if not bao_tin:
            self.n += 1
            msg["id"] = self.n
        if params is not None:
            msg["params"] = params
        h = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": PHIEN_BAN_GIAO_THUC,
        }
        if self.sid:
            h["Mcp-Session-Id"] = self.sid
        req = urllib.request.Request(self.url, data=json.dumps(msg).encode(), headers=h)
        try:
            with self._mo(req, self.timeout) as r:
                sid = r.headers.get("Mcp-Session-Id")
                if sid:
                    self.sid = sid
                raw = r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return {"_http": e.code, "_than": e.read().decode("utf-8", "replace")}
        if bao_tin or not raw.strip():
            return {}
        than = tach_than(raw)
        try:
            return json.loads(than)
        except ValueError:
            return {"_tho": than}

    def mo_phien(self):
        d = self.goi("initialize", {"protocolVersion": PHIEN_BAN_GIAO_THUC, "capabilities": {},
                                    "clientInfo": {"name": "tra-luat-cuu-ho", "version": "1"}})
        self.goi("notifications/initialized", {}, bao_tin=True)
        return d

    def cong_cu(self) -> list:
        d = self.goi("tools/list", {})
        return [t["name"] for t in d.get("result", {}).get("tools", [])]

    def chay(self, ten: str, doi_so: dict):
        return self.goi("tools/call", {"name": ten, "arguments": doi_so})


def rut_van_ban(kq: dict):
    """Trả tải trọng thô của công cụ nếu có, để người gọi `json.loads` được ngay."""
    nd = kq.get("result", {}).get("content")
    if isinstance(nd, list) and nd and isinstance(nd[0], dict) and "text" in nd[0]:
        return nd[0]["text"]
    return json.dumps(kq, ensure_ascii=False, indent=2)


def main(argv: list) -> int:
    path = "/mcp/"
    if "--path" in argv:
        i = argv.index("--path")
        if i + 1 >= len(argv):
            print("SAI ĐỐI SỐ: --path cần một giá trị", file=sys.stderr)
            return 2
        path = argv[i + 1]
        del argv[i:i + 2]

    tok = os.environ.get("GITHUB_PAT") or ""
    if not tok:
        print("KHÔNG ĐO ĐƯỢC: thiếu GITHUB_PAT", file=sys.stderr)
        return 3

    p = Phien(path, tok)
    mo = p.mo_phien()
    if "_http" in mo:
        print(f"KHÔNG ĐO ĐƯỢC: initialize HTTP {mo['_http']} — {mo['_than'][:200]}", file=sys.stderr)
        return 3

    if not argv or argv[0] == "--liet-ke":
        ds = p.cong_cu()
        print(f"{path}  ·  {len(ds)} công cụ")
        for t in ds:
            print("  " + t)
        return 0

    try:
        doi_so = json.loads(argv[1]) if len(argv) > 1 else {}
    except ValueError as e:
        print(f"SAI ĐỐI SỐ: đối số phải là JSON — {e}", file=sys.stderr)
        return 2
    print(rut_van_ban(p.chay(argv[0], doi_so)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
