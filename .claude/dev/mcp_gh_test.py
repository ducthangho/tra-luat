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
    # Bịt MỌI đường ra mạng — kể cả `goi`, vì `main` gọi thẳng nó chứ không qua `cong_cu`.
    # Lần đầu ca này mất răng vì chỉ bịt `cong_cu`; bản vá cho `main` làm nó mất răng LẦN HAI.
    # Bài học: chốt cô lập phải neo vào ĐƯỜNG `main` THẬT ĐI, không neo vào tên hàm ta nhớ.
    goc_mo, goc_cc, goc_goi = m.Phien.mo_phien, m.Phien.cong_cu, m.Phien.goi
    m.Phien.mo_phien = lambda self: {}
    m.Phien.cong_cu = lambda self: ["gia"]
    m.Phien.goi = lambda self, *a, **k: {"result": {"tools": [{"name": "gia"}]}}
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
        m.Phien.mo_phien, m.Phien.cong_cu, m.Phien.goi = goc_mo, goc_cc, goc_goi
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



# ── t11 · NƠI NHẬN credential bị khoá — cross-review bắt được lỗ này ────────────────────────
@ca("t11_dich_den_bi_khoa")
def _t11():
    # đường hợp lệ phải đi qua
    m.Phien("/mcp/", "tok", mo=mo_gia(["{}"]))
    m.Phien("/mcp/x/actions", "tok", mo=mo_gia(["{}"]))
    # và DIEM_CUOI mặc định phải trỏ đúng host cho phép — đột biến đổi endpoint chết ở đây
    assert m.DIEM_CUOI.startswith("https://" + m.HOST_CHO_PHEP), \
        f"DIEM_CUOI trỏ sai host: {m.DIEM_CUOI}"
    for xau, vi_sao in [("http://api.githubcopilot.com/mcp/", "http trần"),
                        ("https://example.invalid/mcp/", "host lạ"),
                        ("https://api.githubcopilot.com/lung-tung", "đường dẫn lạ")]:
        try:
            m.kiem_dich_den(xau)
        except ValueError:
            continue
        raise AssertionError(f"KHÔNG chặn {vi_sao}: {xau}")
    # và `Phien.__init__` phải THẬT SỰ gọi chốt — gỡ lời gọi ấy thì ca này phải đỏ
    try:
        m.Phien("/lung-tung-khong-cho-phep", "tok", mo=mo_gia(["{}"]))
    except ValueError:
        pass
    else:
        raise AssertionError("Phien.__init__ KHÔNG gọi kiem_dich_den")


# ── t12 · initialize trả JSON-RPC error ⇒ KHÔNG được báo thành công ─────────────────────────
@ca("t12_initialize_loi_khong_bao_xanh")
def _t12():
    than = '{"jsonrpc":"2.0","id":1,"error":{"code":-32000,"message":"khong duoc phep"}}'
    d = m.Phien("/mcp/", "tok", mo=mo_gia([than])).mo_phien()
    assert d.get("_loi"), f"initialize hỏng mà không báo lỗi: {d}"
    # phải nhận ra ĐÚNG là JSON-RPC error, không phải rơi xuống nhánh "thiếu result" —
    # nhánh ấy cũng in cả khối JSON nên chuỗi "-32000" lọt vào và che mất đột biến.
    assert d["_loi"].startswith("JSON-RPC error -32000"), d["_loi"]
    # và phải ra tới rc=3 ở lớp lệnh
    os.environ.setdefault("GITHUB_PAT", "tok-gia")
    goc = m.Phien.mo_phien
    m.Phien.mo_phien = lambda self: {"_loi": "gia lap"}
    e, o = sys.stderr, sys.stdout
    sys.stderr, sys.stdout = io.StringIO(), io.StringIO()
    try:
        rc = m.main(["--liet-ke"])
    finally:
        sys.stderr, sys.stdout = e, o
        m.Phien.mo_phien = goc
    assert rc == 3, f"mong rc=3, được {rc}"


# ── t13 · lỗi TẦNG VẬN CHUYỂN ⇒ khối `_mang`, không traceback ───────────────────────────────
@ca("t13_urlerror_khong_nem_traceback")
def _t13():
    def _mo(req, timeout):
        raise urllib.error.URLError("Operation not permitted")
    d = m.Phien("/mcp/", "tok", mo=_mo).goi("tools/list", {})
    assert "_mang" in d, f"URLError không được gói lại: {d}"
    assert m.loi_cua(d), "loi_cua phải nhận ra lỗi mạng"

# ── ĐỘT BIẾN — mỗi cái phải giết ĐÚNG ca của nó ─────────────────────────────────────────────
DOT_BIEN = [
    ("m1_sse_bo_qua_data", 'if dong.startswith("data:"):', 'if False:', "t2_sse_lay_dong_data_cuoi"),
    ("m2_cat_chuoi_6000", "return dong[5:].strip()", "return dong[5:].strip()[:6000]", "t4_khong_cat_chuoi_dai"),
    ("m3_bo_session_id", "if sid:\n                    self.sid = sid", "if False:\n                    self.sid = sid", "t5_giu_session_id"),
    ("m4_bao_tin_van_co_id", "if not bao_tin:", "if True:", "t6_bao_tin_khong_co_id"),
    ("m5_thieu_token_khong_chan", 'if not tok:', 'if False:', "t1_thieu_token_fail_close"),
    ("m6_rut_van_ban_cat", 'return nd[0]["text"]', 'return nd[0]["text"][:6000]', "t4_khong_cat_chuoi_dai"),
    # ĐÚNG đột biến mà cross-review dựng ra và bộ test cũ KHÔNG giết được:
    ("m7_doi_diem_cuoi", 'DIEM_CUOI = "https://api.githubcopilot.com"',
     'DIEM_CUOI = "https://example.invalid"', "t11_dich_den_bi_khoa"),
    ("m8_bo_kiem_dich_den", "        kiem_dich_den(self.url)", "        pass", "t11_dich_den_bi_khoa"),
    ("m9_bo_kiem_error_jsonrpc", 'if isinstance(d.get("error"), dict):', "if False:",
     "t12_initialize_loi_khong_bao_xanh"),
    ("m10_bo_bat_urlerror", "except (urllib.error.URLError, TimeoutError, OSError) as e:",
     "except (_KhongBaoGio,) as e:", "t13_urlerror_khong_nem_traceback"),
]


class _KhongBaoGio(Exception):
    """Chỉ dùng cho đột biến m10 — không nhánh nào ném nó."""


CA_THEO_TEN = {
    "t11_dich_den_bi_khoa": _t11,
    "t12_initialize_loi_khong_bao_xanh": _t12,
    "t13_urlerror_khong_nem_traceback": _t13,
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
