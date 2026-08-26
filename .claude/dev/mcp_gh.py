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

# Credential `GITHUB_PAT` đi kèm MỌI lời gọi, nên NƠI NHẬN là thứ phải khoá, không phải thứ
# để mặc định. Cross-review bắt được lỗ này: đột biến đổi `DIEM_CUOI` thành `https://example.invalid`
# vẫn cho `10 đạt · 6/6 · TỔNG ĐẠT` — bộ test không hề canh credential đi đâu.
HOST_CHO_PHEP = "api.githubcopilot.com"
DUONG_CHO_PHEP = ("/mcp/", "/mcp/x/actions")


def kiem_dich_den(url: str) -> None:
    """Chặn TRƯỚC khi gắn `Authorization` vào một đích không thuộc danh sách cho phép."""
    from urllib.parse import urlparse
    u = urlparse(url)
    if u.scheme != "https":
        raise ValueError(f"từ chối gửi credential qua {u.scheme!r}: chỉ https")
    if u.hostname != HOST_CHO_PHEP:
        raise ValueError(f"từ chối gửi credential tới host {u.hostname!r}: chỉ {HOST_CHO_PHEP}")
    if u.path not in DUONG_CHO_PHEP:
        raise ValueError(f"từ chối đường dẫn {u.path!r}: chỉ {DUONG_CHO_PHEP}")


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
        kiem_dich_den(self.url)
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
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            # KHÔNG bắt `Exception` trần — sẽ che lỗi lập trình. Chỉ bắt lỗi TẦNG VẬN CHUYỂN.
            return {"_mang": f"{type(e).__name__}: {e}"}
        if bao_tin or not raw.strip():
            return {}
        than = tach_than(raw)
        try:
            return json.loads(than)
        except ValueError:
            return {"_tho": than}

    def mo_phien(self):
        """Trả `{}` khi mở được; ngược lại trả chính khối lỗi. `notifications/initialized` CHỈ
        gửi sau khi mở THẬT — bản đầu gửi vô điều kiện và báo rc=0 cho một phiên chưa mở được."""
        d = self.goi("initialize", {"protocolVersion": PHIEN_BAN_GIAO_THUC, "capabilities": {},
                                    "clientInfo": {"name": "tra-luat-cuu-ho", "version": "1"}})
        loi = loi_cua(d)
        if loi:
            return {"_loi": loi}
        self.goi("notifications/initialized", {}, bao_tin=True)
        return {}

    def cong_cu(self) -> list:
        d = self.goi("tools/list", {})
        return [t["name"] for t in d.get("result", {}).get("tools", [])]

    def chay(self, ten: str, doi_so: dict):
        return self.goi("tools/call", {"name": ten, "arguments": doi_so})


def loi_cua(d: dict):
    """Ba đường hỏng, PHẢI phân biệt — `rc=0` cho bất kỳ đường nào là báo xanh cho phiên chưa mở.

    Bản đầu chỉ kiểm `_http`, nên `{"error": …}` của JSON-RPC lọt qua và in `0 công cụ`;
    còn `URLError` thì thoát bằng traceback `rc=1`, sai hợp đồng `rc=3`.
    """
    if "_http" in d:
        return f"HTTP {d['_http']} — {str(d.get('_than'))[:200]}"
    if "_mang" in d:
        return f"lỗi mạng — {d['_mang']}"
    if "_tho" in d:
        return f"phản hồi không phải JSON — {str(d['_tho'])[:200]}"
    if isinstance(d.get("error"), dict):
        e = d["error"]
        return f"JSON-RPC error {e.get('code')} — {str(e.get('message'))[:200]}"
    if "result" not in d:
        return f"phản hồi thiếu `result` — {json.dumps(d, ensure_ascii=False)[:200]}"
    return None


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

    try:
        p = Phien(path, tok)
    except ValueError as e:
        print(f"KHÔNG ĐO ĐƯỢC: đích không hợp lệ — {e}", file=sys.stderr)
        return 3
    mo = p.mo_phien()
    if mo.get("_loi"):
        print(f"KHÔNG ĐO ĐƯỢC: initialize — {mo['_loi']}", file=sys.stderr)
        return 3

    if not argv or argv[0] == "--liet-ke":
        d = p.goi("tools/list", {})
        loi = loi_cua(d)
        if loi:
            print(f"KHÔNG ĐO ĐƯỢC: tools/list — {loi}", file=sys.stderr)
            return 3
        ds = [t["name"] for t in d.get("result", {}).get("tools", [])]
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
