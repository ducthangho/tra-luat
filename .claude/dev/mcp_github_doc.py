#!/usr/bin/env python3
"""mcp_github_doc.py — client MCP github, ĐỌC cấu hình từ `.mcp.json` của DỰ ÁN.

VÌ SAO CÓ TỆP NÀY
`launcher.py doctor` đã ĐO được `mcp-endpoint` (một lượt `initialize`), nhưng nó CỐ Ý
dừng ở handshake: docstring `_do_mcp_endpoint` nói thẳng rằng nó KHÔNG chứng minh gọi
được `mcp__github__*`, cũng KHÔNG chứng minh đọc được kho này. Phiên remote mất uỷ quyền
connector thì không còn công cụ `mcp__github__*` nào, mà `git` lại chạy — đúng ca
"bốn đường, hỏng độc lập" trong CLAUDE.md. Tệp này nối nốt đoạn dây còn thiếu:
`initialize` -> `notifications/initialized` -> `tools/call`.

KHÔNG GHI CỨNG URL/TOKEN: đọc `.mcp.json` (khoá `mcpServers`/`servers`, tên đúng bằng
`github`) và giải `${BIEN}` trong `headers` từ môi trường — cùng một nguồn sự thật mà
phiên agent dùng, nên hai đường không trôi lệch được.

BA TRẠNG THÁI, không phải hai: `mo` (có header `X-GitHub-*`) · `chan` (403 KHÔNG header
GitHub = proxy tự sinh, CHƯA từng tới GitHub) · `khong_do_duoc` (mạng/DNS/quá hạn).
Phân loại theo HEADER, không theo mã trạng thái — cùng tiêu chí `_do_rest_github` và
`_do_mcp_endpoint` đã trả giá để có.

MÔ TẢ KHÔNG BAO GIỜ CHỞ TOKEN: không in `headers`, không nội suy `url` vào nhánh từ chối.

PHẠM VI ĐỌC — đây là đường TRUY CẬP qua MCP khi connector không dùng được, KHÔNG phải
thước đo byte-exact cho body issue/PR/comment. MCP đã được đo là có thể nuốt token dạng
thẻ và escape HTML. Muốn ĐỐI CHIẾU byte đã đến GitHub, dùng `gh_readback.py`: hai tệp đi
hai đường vận chuyển và trả lời hai câu hỏi khác nhau, không phải bản sao của nhau.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import launcher as _launcher

_GIAO_THUC = "2025-06-18"
_QUA_HAN_GIAY = 180
_RE_BIEN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
_RE_HAU_TO = re.compile(r"[a-z0-9_-]+(?:/[a-z0-9_-]+)*")


class Hong(Exception):
    pass


def _doc_cau_hinh(goc: Path) -> tuple[str, dict[str, str]]:
    """Trả (url, headers đã giải biến) cho server `github` do launcher chọn.

    Launcher sở hữu việc đọc lược đồ, chọn khoá và khớp tên. Client phải đọc lại
    đúng mục đã chọn vì hợp đồng chuẩn cố ý không trả ``headers``.
    """
    tep = goc / ".mcp.json"
    try:
        anh_truoc = tep.read_bytes()
    except OSError:
        co_khai, mo_ta, _, _ = _launcher._doc_mcp_json(str(goc))
        if not co_khai:
            raise Hong(mo_ta)
        raise Hong("khong doc duoc .mcp.json") from None
    co_khai, mo_ta, ten_chuan, url = _launcher._doc_mcp_json(str(goc))
    anh_sau = tep.read_bytes()
    # Hai lượt đọc vẫn để lại một cửa sổ đua. So ảnh chỉ biến việc ghép URL của
    # ảnh cũ với headers ảnh mới thành từ chối ồn ào; không tuyên bố xoá race.
    if hashlib.sha256(anh_truoc).digest() != hashlib.sha256(anh_sau).digest():
        raise Hong(".mcp.json da thay doi trong luc doc — TU CHOI")
    if not co_khai:
        raise Hong(mo_ta)
    if url is None:
        # Khác phạm vi có chủ ý: launcher chỉ đo CÓ KHAI (stdio hợp lệ), còn
        # client này là streamable HTTP nên không thể làm việc nếu thiếu URL.
        raise Hong("server `github` khong khai `url` cho client HTTP (kieu stdio?)")

    # `_doc_mcp_json` không trả headers hoặc tên khoá chứa server. Chỉ phần này
    # không tái sử dụng được; lặp đúng quy tắc ưu tiên khoá để lấy mục đã chọn.
    d = json.loads(anh_sau.decode("utf-8"))
    for khoa in ("mcpServers", "servers"):
        if khoa in d:
            srv = d[khoa]
            break
    muc = srv[ten_chuan]
    # `urlsplit` trì hoãn kiểm port tới lúc đọc `.port`. Phải đọc nó trong cùng
    # `try`: một bí mật ở vị trí port không được đi tiếp vào `Request`.
    try:
        p = urllib.parse.urlsplit(str(url))
        _ = p.port
    except ValueError as e:
        raise Hong(f"`url` khong phan tich duoc ({type(e).__name__})") from None
    if (p.username, p.password) != (None, None):
        raise Hong("`url` co credential trong userinfo — TU CHOI")
    if p.scheme.lower() not in ("http", "https"):
        raise Hong("`url` khong phai http(s) — TU CHOI")
    if not p.hostname:
        raise Hong("`url` khong co ten may — TU CHOI")

    def _giai(x: str) -> str:
        def _thay(m):
            v = os.environ.get(m.group(1))
            if not v:
                raise Hong(f"bien moi truong {m.group(1)} chua dat hoac rong")
            return v
        return _RE_BIEN.sub(_thay, x)

    headers = muc["headers"] if "headers" in muc else {}
    if not isinstance(headers, dict):
        raise Hong("headers cua server `github` khong phai object")
    dau = {str(k): _giai(str(v)) for k, v in headers.items()}
    # TOOLSET CON: máy chủ github-mcp-server phơi các bộ công cụ hẹp ở ĐƯỜNG DẪN CON
    # (`/mcp/x/actions` …). Chỉ cho phép nối HẬU TỐ vào URL đã khai — KHÔNG nhận URL
    # tuỳ ý từ môi trường, kẻo biến một biến môi trường thành đường đi tới máy chủ khác
    # mang theo token của `.mcp.json`.
    hau_to = os.environ.get("TL_MCP_TOOLSET") or ""
    if hau_to:
        if len(hau_to) > 64 or not _RE_HAU_TO.fullmatch(hau_to):
            raise Hong("TL_MCP_TOOLSET co ky tu ngoai danh sach cho phep")
        p = p._replace(path=p.path.rstrip("/") + "/" + hau_to)
    return p.geturl(), dau


def _goc_du_an() -> Path:
    """TL_GOC ghi đè tường minh; mặc định neo theo vị trí client như launcher."""
    ghi_de = os.environ.get("TL_GOC")
    return Path(ghi_de).resolve() if ghi_de else Path(__file__).resolve().parents[2]


class Phien:
    """Một phiên MCP streamable-HTTP: giữ `Mcp-Session-Id` qua các lời gọi."""

    def __init__(self, goc: Path):
        self.url, self._dau_goc = _doc_cau_hinh(goc)
        self.phien_id: str | None = None

    def _post(self, than: dict) -> tuple[int, str, dict]:
        dau = dict(self._dau_goc)
        dau["Content-Type"] = "application/json"
        dau["Accept"] = "application/json, text/event-stream"
        dau["MCP-Protocol-Version"] = _GIAO_THUC
        if self.phien_id:
            dau["Mcp-Session-Id"] = self.phien_id
        req = urllib.request.Request(self.url, data=json.dumps(than).encode("utf-8"),
                                     headers=dau, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=_QUA_HAN_GIAY) as r:
                return int(r.status), r.read().decode("utf-8", "replace"), dict(r.headers)
        except urllib.error.HTTPError as e:
            co_gh = any(k.lower().startswith("x-github") for k in e.headers)
            vi_sao = (" (toi GitHub, thieu quyen)" if co_gh
                      else " (KHONG header GitHub -> proxy tu sinh)")
            raise Hong(f"HTTP {e.code}{vi_sao}") from None
        except Exception as e:  # noqa: BLE001
            raise Hong(f"{type(e).__name__} khi POST") from None

    @staticmethod
    def _boc(raw: str) -> dict:
        """Đọc JSON thuần hoặc response JSON-RPC trong một stream nhiều SSE event."""
        # data fields chỉ được nối TRONG cùng event; dòng trống chốt event.
        su_kien, data = [], []
        for dong in raw.splitlines() + [""]:
            if dong == "":
                if data:
                    su_kien.append("\n".join(data))
                    data = []
            elif dong.startswith("data:"):
                gia_tri = dong[5:]
                data.append(gia_tri[1:] if gia_tri.startswith(" ") else gia_tri)
        mau = su_kien or [raw]
        da_doc = []
        for x in mau:
            try:
                d = json.loads(x)
            except json.JSONDecodeError:
                continue
            if isinstance(d, dict):
                da_doc.append(d)
        # Notification có thể đứng sau response. Không được lấy mù event CUỐI CÙNG.
        for d in da_doc:
            if "id" in d and ("result" in d or "error" in d):
                return d
        if da_doc:
            return da_doc[-1]
        raise Hong("than phan hoi khong phai JSON")

    def bat_tay(self) -> dict:
        ma, raw, dau = self._post({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": _GIAO_THUC, "capabilities": {},
                       "clientInfo": {"name": "tra-luat-mcp-doc", "version": "1"}}})
        if not any(k.lower().startswith("x-github") for k in dau):
            raise Hong(f"HTTP {ma} KHONG header GitHub -> proxy tu sinh, CHUA toi GitHub")
        for k, v in dau.items():
            if k.lower() == "mcp-session-id":
                self.phien_id = v
        d = self._boc(raw)
        if "error" in d:
            raise Hong("initialize loi: " + json.dumps(d["error"], ensure_ascii=False)[:300])
        # Bắt buộc theo spec: báo đã khởi tạo xong trước khi gọi tool.
        _, raw_bao, _ = self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})
        if raw_bao.strip():
            bao = self._boc(raw_bao)
            if "error" in bao:
                raise Hong("notifications/initialized loi")
        return d.get("result", {})

    def rpc(self, method: str, params: dict) -> dict:
        _, raw, _ = self._post({"jsonrpc": "2.0", "id": 2, "method": method,
                                "params": params})
        d = self._boc(raw)
        if "error" in d:
            raise Hong(f"{method} loi: " + json.dumps(d["error"], ensure_ascii=False)[:300])
        kq = d.get("result", {})
        # `tools/call` bao loi nghiep vu trong result hop le, khong o JSON-RPC error.
        # Chan tai day de moi duong dung rpc (ke ca liet_ke) deu fail-closed.
        if isinstance(kq, dict) and kq.get("isError") is True:
            phan = [c.get("text", "") for c in kq.get("content", [])
                    if isinstance(c, dict) and c.get("type") == "text"]
            raise Hong("may chu MCP bao loi: " + "\n".join(phan)[:300])
        return kq

    def liet_ke(self) -> list[str]:
        return sorted(t["name"] for t in self.rpc("tools/list", {}).get("tools", []))

    def goi(self, ten: str, doi_so: dict) -> str:
        kq = self.rpc("tools/call", {"name": ten, "arguments": doi_so})
        phan = [c.get("text", "") for c in kq.get("content", []) if c.get("type") == "text"]
        return "\n".join(phan)


def _main(argv: list[str]) -> int:
    goc = _goc_du_an()
    lenh = argv[1] if len(argv) > 1 else "do"
    try:
        p = Phien(goc)
        kq = p.bat_tay()
        if lenh == "do":
            ten = (kq.get("serverInfo") or {}).get("name", "?")
            print(f"mcp-endpoint: MO · server={ten} · phien={'co' if p.phien_id else 'khong'}")
            print(f"so cong cu: {len(p.liet_ke())}")
            return 0
        if lenh == "tools":
            ds = p.liet_ke()
            print(f"N_TOOLS {len(ds)}")
            print("\n".join(ds))
            return 0
        if lenh == "goi":
            print(p.goi(argv[2], json.loads(argv[3])))
            return 0
        print(f"lenh la: do | tools | goi <ten> <json>", file=sys.stderr)
        return 2
    except Hong as e:
        print(f"KHONG_DO_DUOC/CHAN: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
