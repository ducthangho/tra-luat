#!/usr/bin/env python3
"""Phản chứng cho `mcp_gh.py` — chạy OFFLINE, không chạm mạng.

Mỗi tính chất có một ĐỘT BIẾN riêng phải giết đúng ca của nó. Đột biến chạy trên BẢN SAO TẠM
với tên module riêng và không để lại `.pyc` — kho đã trả giá cho ca "đột biến chưa từng được
chạy" vì CPython coi `.pyc` còn hợp lệ theo (mtime giây, kích thước).

Mã thoát: 0 tất cả đạt · 1 có ca đỏ.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import pathlib
import sys
import tempfile
import urllib.error

sys.dont_write_bytecode = True

GOC = pathlib.Path(__file__).resolve().parent
NGUON = GOC / "mcp_gh.py"


def nap(duong_dan: pathlib.Path, ten: str):
    importlib.invalidate_caches()
    spec = importlib.util.spec_from_file_location(ten, duong_dan)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class PhanHoiGia:
    def __init__(self, than: str, headers=None):
        self._b = than.encode()
        self.headers = headers or {}

    def read(self):
        return self._b

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def mo_gia(cac_than, ghi_lai=None, headers_lan_dau=None):
    """Trả một hàm mở giả; `ghi_lai` nhận từng (msg, headers) đã gửi."""
    hop = list(cac_than)

    def _mo(req, timeout):
        if ghi_lai is not None:
            ghi_lai.append((json.loads(req.data.decode()), dict(req.headers)))
        h = headers_lan_dau if len(hop) == len(cac_than) and headers_lan_dau else {}
        return PhanHoiGia(hop.pop(0) if hop else "{}", h)

    return _mo


DAT, DO = [], []


def ca(ten):
    def deco(fn):
        try:
            fn()
            DAT.append(ten)
        except AssertionError as e:
            DO.append((ten, str(e)))
        except Exception as e:  # noqa: BLE001
            DO.append((ten, f"{type(e).__name__}: {e}"))
        return fn
    return deco


m = nap(NGUON, "mcp_gh_that")

# ── t1 · thiếu credential ⇒ FAIL-CLOSE rc=3, không phải rc=0 ────────────────────────────────
@ca("t1_thieu_token_fail_close")
def _t1():
    cu = os.environ.pop("GITHUB_PAT", None)
    # CÔ LẬP: bịt mọi đường ra mạng để rc=3 CHỈ có thể đến từ chốt token. Bản đầu không bịt,
    # nên `main` đi tiếp, lời gọi mạng hỏng, và rc=3 xuất hiện vì LÝ DO KHÁC — đột biến
    # "gỡ chốt token" sống sót. Ca xanh mà không đo cái nó tưởng đang đo.
    goc_mo, goc_cc = m.Phien.mo_phien, m.Phien.cong_cu
    m.Phien.mo_phien = lambda self: {}
    m.Phien.cong_cu = lambda self: ["gia"]
    try:
        loi, ra = io.StringIO(), io.StringIO()
        that_e, sys.stderr = sys.stderr, loi
        that_o, sys.stdout = sys.stdout, ra          # nuốt cả stdout: ca này không in gì ra ngoài
        try:
            rc = m.main(["--liet-ke"])
        finally:
            sys.stderr, sys.stdout = that_e, that_o
        assert rc == 3, f"mong rc=3, được {rc} (chốt token bị gỡ?)"
        assert "KHÔNG ĐO ĐƯỢC" in loi.getvalue(), "phải nói KHÔNG ĐO ĐƯỢC"
    finally:
        m.Phien.mo_phien, m.Phien.cong_cu = goc_mo, goc_cc
        if cu is not None:
            os.environ["GITHUB_PAT"] = cu


# ── t2 · thân SSE: dòng `data:` CUỐI mới là kết quả ─────────────────────────────────────────
@ca("t2_sse_lay_dong_data_cuoi")
def _t2():
    sse = 'event: message\ndata: {"id":1,"result":{"sai":true}}\n\ndata: {"id":2,"result":{"dung":true}}\n'
    assert json.loads(m.tach_than(sse))["result"] == {"dung": True}, "phải lấy data: CUỐI"


# ── t3 · thân JSON thuần vẫn đọc được ───────────────────────────────────────────────────────
@ca("t3_json_thuan")
def _t3():
    assert json.loads(m.tach_than('{"result":{"ok":1}}'))["result"] == {"ok": 1}


# ── t4 · KHÔNG CẮT CHUỖI — đây là lỗi đã xảy ra thật ────────────────────────────────────────
@ca("t4_khong_cat_chuoi_dai")
def _t4():
    to = {"result": {"content": [{"text": json.dumps({"x": ["y" * 40] * 500})}]}}
    than = "data: " + json.dumps(to)
    ra = m.tach_than(than)
    assert len(ra) > 20000, f"thân bị cắt còn {len(ra)}"
    json.loads(ra)                               # phải còn parse được
    vb = m.rut_van_ban(json.loads(ra))
    json.loads(vb)                               # tải trọng công cụ cũng nguyên vẹn
    assert len(vb) > 20000, f"rut_van_ban cắt còn {len(vb)}"


# ── t5 · Mcp-Session-Id nhận từ phản hồi đầu, gửi lại ở lời gọi sau ─────────────────────────
@ca("t5_giu_session_id")
def _t5():
    ds = []
    p = m.Phien("/mcp/", "tok", mo=mo_gia(['{"result":{}}', '{"result":{}}'], ds,
                                          headers_lan_dau={"Mcp-Session-Id": "S-42"}))
    p.goi("initialize", {})
    p.goi("tools/list", {})
    assert p.sid == "S-42", f"không giữ được sid: {p.sid}"
    h2 = {k.lower(): v for k, v in ds[1][1].items()}
    assert h2.get("mcp-session-id") == "S-42", f"lời gọi sau thiếu sid: {h2}"


# ── t6 · notification KHÔNG có `id`; request thì CÓ ─────────────────────────────────────────
@ca("t6_bao_tin_khong_co_id")
def _t6():
    ds = []
    p = m.Phien("/mcp/", "tok", mo=mo_gia(['{"result":{}}', ""], ds))
    p.goi("tools/list", {})
    p.goi("notifications/initialized", {}, bao_tin=True)
    assert "id" in ds[0][0], "request phải có id"
    assert "id" not in ds[1][0], "notification KHÔNG được có id"


# ── t7 · lỗi HTTP trả cấu trúc, không ném ───────────────────────────────────────────────────
@ca("t7_http_loi_tra_cau_truc")
def _t7():
    def _mo(req, timeout):
        raise urllib.error.HTTPError(req.full_url, 403, "Forbidden", {}, io.BytesIO(b"cam"))
    d = m.Phien("/mcp/", "tok", mo=_mo).goi("tools/list", {})
    assert d.get("_http") == 403 and d.get("_than") == "cam", d


# ── t8/t9 · sai đối số ⇒ rc=2, phân biệt với rc=3 ───────────────────────────────────────────
@ca("t8_path_thieu_gia_tri_rc2")
def _t8():
    that, sys.stderr = sys.stderr, io.StringIO()
    try:
        rc = m.main(["--path"])
    finally:
        sys.stderr = that
    assert rc == 2, f"mong rc=2, được {rc}"


@ca("t9_doi_so_khong_phai_json_rc2")
def _t9():
    os.environ.setdefault("GITHUB_PAT", "tok-gia")
    goc = m.Phien.mo_phien
    m.Phien.mo_phien = lambda self: {}
    that, sys.stderr = sys.stderr, io.StringIO()
    try:
        rc = m.main(["actions_list", "{khong-phai-json"])
    finally:
        sys.stderr = that
        m.Phien.mo_phien = goc
    assert rc == 2, f"mong rc=2, được {rc}"


# ── t10 · rut_van_ban lùi về cả đối tượng khi không có content.text ─────────────────────────
@ca("t10_rut_van_ban_lui_ve_ca_doi_tuong")
def _t10():
    assert json.loads(m.rut_van_ban({"result": {"khac": 1}}))["result"] == {"khac": 1}


# ── ĐỘT BIẾN — mỗi cái phải giết ĐÚNG ca của nó ─────────────────────────────────────────────
DOT_BIEN = [
    ("m1_sse_bo_qua_data", 'if dong.startswith("data:"):', 'if False:', "t2_sse_lay_dong_data_cuoi"),
    ("m2_cat_chuoi_6000", "return dong[5:].strip()", "return dong[5:].strip()[:6000]", "t4_khong_cat_chuoi_dai"),
    ("m3_bo_session_id", "if sid:\n                    self.sid = sid", "if False:\n                    self.sid = sid", "t5_giu_session_id"),
    ("m4_bao_tin_van_co_id", "if not bao_tin:", "if True:", "t6_bao_tin_khong_co_id"),
    ("m5_thieu_token_khong_chan", 'if not tok:', 'if False:', "t1_thieu_token_fail_close"),
    ("m6_rut_van_ban_cat", 'return nd[0]["text"]', 'return nd[0]["text"][:6000]', "t4_khong_cat_chuoi_dai"),
]


CA_THEO_TEN = {
    "t1_thieu_token_fail_close": _t1,
    "t2_sse_lay_dong_data_cuoi": _t2,
    "t4_khong_cat_chuoi_dai": _t4,
    "t5_giu_session_id": _t5,
    "t6_bao_tin_khong_co_id": _t6,
}


def chay_dot_bien():
    """Chạy từng đột biến trên bản sao tạm. KHÔNG đụng sổ `DAT`/`DO` của lượt nền —
    bản đầu xoá chúng và tổng kết in "0 đạt · 0 đỏ": một cổng báo xanh mà không đếm gì."""
    goc = NGUON.read_text(encoding="utf-8")
    chet, song = [], []
    for i, (ten, cu, moi, ca_dich) in enumerate(DOT_BIEN):
        if cu not in goc:
            song.append(f"{ten} (KHÔNG KHỚP — mẫu đột biến đã trôi)")
            continue
        with tempfile.TemporaryDirectory() as d:
            # tên tệp RIÊNG từng đột biến: hai bản cùng kích thước ghi trong cùng một giây
            # sẽ dùng lại `.pyc` của nhau — ca đã trả giá.
            p = pathlib.Path(d) / f"mcp_gh_db{i}.py"
            p.write_text(goc.replace(cu, moi, 1), encoding="utf-8")
            mm = nap(p, f"mcp_gh_db{i}")
            assert not list(pathlib.Path(d).glob("__pycache__/*")), "đột biến để lại .pyc"
            that_m = globals()["m"]
            globals()["m"] = mm
            try:
                CA_THEO_TEN[ca_dich]()
            except Exception:  # noqa: BLE001
                chet.append(ten)
            else:
                song.append(f"{ten} → {ca_dich} VẪN XANH")
            finally:
                globals()["m"] = that_m
    return chet, song


if __name__ == "__main__":
    chet, song = chay_dot_bien()
    print(f"CA        : {len(DAT)} đạt · {len(DO)} đỏ")
    for t, e in DO:
        print(f"  ĐỎ {t}: {e}")
    print(f"ĐỘT BIẾN  : {len(chet)}/{len(DOT_BIEN)} bị giết")
    for s in song:
        print(f"  SỐNG SÓT {s}")
    ok = not DO and len(chet) == len(DOT_BIEN)
    print("TỔNG: " + ("ĐẠT" if ok else "ĐỎ"))
    sys.exit(0 if ok else 1)
