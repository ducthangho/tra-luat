#!/usr/bin/env python3
"""Test `llm_route.py` — chỉ thư viện chuẩn, không gọi mạng, không cần SDK `anthropic`.

Mỗi chốt có MỘT đột biến riêng chạy trên BẢN SAO TẠM (không bao giờ sửa tệp thật —
CLAUDE.md §"Đột biến ghi vào tệp THẬT"). Đột biến chỉ được tính GIẾT khi CHÍNH ca đích
đỏ bằng `TinHieuChotCa` (assertion của ca), không phải vì lỗi vô can — CLAUDE.md
§"ĐỘT BIẾN BỊ GIẾT KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO".

Dòng tổng (sổ đăng ký CI): `llm_route tests: N/N ca QUA · M/M dot bien GIET`.
"""
from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import types
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

HERE = Path(__file__).resolve().parent
NGUON = HERE / "llm_route.py"
KEY_GIA = "sk-ant-GIA-KHONG-DUOC-IN-RA-0123456789"
VAN_BAN = ("Điều 3. Giải thích từ ngữ\nTrong Luật này, các từ ngữ dưới đây được hiểu như sau:\n"
           "Trí tuệ nhân tạo là việc thực hiện bằng điện tử các năng lực trí tuệ.\n"
           "Người sử dụng là tổ chức, cá nhân trực tiếp tương tác với hệ thống.")
DUNG = {"khai_niem": [
    {"stt": 1, "thuat_ngu": "Trí tuệ nhân tạo",
     "dinh_nghia": "việc thực hiện bằng điện tử các năng lực trí tuệ."},
    {"stt": 2, "thuat_ngu": "Người sử dụng",
     "dinh_nghia": "tổ chức, cá nhân trực tiếp tương tác với hệ thống."}]}


class TinHieuChotCa(AssertionError):
    """Chỉ assertion của ca mới ném lớp này; mã triển khai không giả được nó."""


def bang(dk, thong_bao):
    if not dk:
        raise TinHieuChotCa(thong_bao)


def nap(tep=NGUON, ten="llm_route_thu"):
    spec = importlib.util.spec_from_file_location(ten, tep)
    m = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(m)
    return m


# ------------------------------------------------------------- đồ giả

class LoiGia(Exception):
    def __init__(self, status_code=None, type_=None, message="", ten=None):
        super().__init__(message)
        self.status_code, self.type, self.message = status_code, type_, message
        if ten:
            self.__class__ = type(ten, (LoiGia,), {})


def client_gia(data=None, loi=None, stop="end_turn", model="claude-haiku-5-5", nhat_ky=None):
    def create(**k):
        if nhat_ky is not None:
            nhat_ky.append(k)
        if loi:
            raise loi
        return types.SimpleNamespace(
            stop_reason=stop, stop_details=None, model=model,
            content=[types.SimpleNamespace(type="text", text=json.dumps(data or DUNG, ensure_ascii=False))],
            usage=types.SimpleNamespace(input_tokens=100, output_tokens=50,
                                        cache_read_input_tokens=0, cache_creation_input_tokens=0))
    return lambda key: types.SimpleNamespace(messages=types.SimpleNamespace(create=create))


def run_sub_gia(data=None, rc=0, is_error=False, model="claude-haiku-5-5", nhat_ky=None, result="ok"):
    def chay(cmd, **k):
        if nhat_ky is not None:
            nhat_ky.append((cmd, k))
        kq = {"is_error": is_error, "result": result, "structured_output": data or DUNG,
              "total_cost_usd": 0.0004,
              "modelUsage": {model: {"inputTokens": 2, "outputTokens": 55, "cacheReadInputTokens": 0,
                                     "cacheCreationInputTokens": 1911, "canonicalModel": model}}}
        return subprocess.CompletedProcess(cmd, rc, json.dumps(kq, ensure_ascii=False), "")
    return chay


def ns(**k):
    mac_dinh = dict(tep=None, so_hieu="134/2025/QH15", thu_tu=None, model="claude-haiku-5-5",
                    out=None, nhat_ky=None)
    mac_dinh.update(k)
    return types.SimpleNamespace(**mac_dinh)


def chay_lenh(m, env, cac_duong, **k):
    with tempfile.TemporaryDirectory() as d:
        tep = Path(d) / "dieu.txt"
        tep.write_text(VAN_BAN, encoding="utf-8")
        o, e = io.StringIO(), io.StringIO()
        with redirect_stdout(o), redirect_stderr(e):
            rc = m.lenh_tach_khai_niem(ns(tep=str(tep), **k), env=env, cac_duong=cac_duong)
    return rc, o.getvalue(), e.getvalue()


def duong_api_voi(m, tao_client):
    return lambda *a: m.duong_api(*a, tao_client=tao_client)


def duong_sub_voi(m, chay, tim=lambda t: "/usr/bin/claude"):
    return lambda *a: m.duong_sub(*a, chay=chay, tim=tim)


# ------------------------------------------------------------- ca

def ca_api_dat(m):
    nk = []
    rc, out, err = chay_lenh(m, {"TL_ANTHROPIC_API_KEY": KEY_GIA},
                             {"api": duong_api_voi(m, client_gia(nhat_ky=nk)),
                              "sub": lambda *a: (_ for _ in ()).throw(TinHieuChotCa("sub bi goi"))})
    bang(rc == 0, f"rc={rc} err={err}")
    bang("DUONG: api (key tu TL_ANTHROPIC_API_KEY)" in err, err)
    bang("TOKEN: input=100 output=50" in err, err)
    bang(nk and nk[0]["output_config"]["format"]["type"] == "json_schema", f"khong dung structured output: {nk}")


def ca_uu_tien_bien_tl(m):
    ten, _ = m.lay_key({"ANTHROPIC_API_KEY": "a", "TL_ANTHROPIC_API_KEY": "b"})
    bang(ten == "TL_ANTHROPIC_API_KEY", f"phai uu tien TL_: {ten}")
    ten, _ = m.lay_key({"TL_ANTHROPIC_API_KEY": "   ", "ANTHROPIC_API_KEY": "a"})
    bang(ten == "ANTHROPIC_API_KEY", f"bien rong khong duoc tinh la key: {ten}")


def ca_thieu_key_chuyen_sub(m):
    rc, out, err = chay_lenh(m, {}, {"api": duong_api_voi(m, client_gia()),
                                     "sub": duong_sub_voi(m, run_sub_gia())})
    bang(rc == 0, f"rc={rc} err={err}")
    bang("DUONG: sub" in err and "[chuyen duong] api: khong co" in err, err)


def ca_het_credit_402_chuyen_sub(m):
    # 402 KHÔNG kèm `type` để đo riêng nhánh mã trạng thái (có `billing_error` thì nhánh
    # `kieu` che mất, và đột biến gỡ 402 sống sót — đo 24-11-2026).
    for loi in (LoiGia(402, None, "payment required"), LoiGia(None, "billing_error", "billing"),
                LoiGia(400, "invalid_request_error", "Your credit balance is too low")):
        rc, _, err = chay_lenh(m, {"TL_ANTHROPIC_API_KEY": KEY_GIA},
                               {"api": duong_api_voi(m, client_gia(loi=loi)),
                                "sub": duong_sub_voi(m, run_sub_gia())})
        bang(rc == 0 and "DUONG: sub" in err, f"het credit ({loi.status_code}) phai chuyen sub: rc={rc} {err}")


def ca_400_khac_thi_dung(m):
    def sub_cam(*a):
        raise TinHieuChotCa("400 thuong KHONG duoc tieu tien lan hai o duong sub")
    rc, _, err = chay_lenh(m, {"TL_ANTHROPIC_API_KEY": KEY_GIA},
                           {"api": duong_api_voi(m, client_gia(loi=LoiGia(400, "invalid_request_error", "bad schema"))),
                            "sub": sub_cam})
    bang(rc == m.MA_DUNG, f"400 thuong phai DUNG (rc 4), duoc rc={rc} {err}")


def ca_ket_noi_chuyen_duong(m):
    lop = m.phan_loai_loi_api(LoiGia(ten="APIConnectionError"))
    bang(lop is m.ChuyenDuong, f"mat ket noi phai chuyen duong: {lop}")
    bang(m.phan_loai_loi_api(LoiGia(429, "rate_limit_error")) is m.ChuyenDuong, "429 phai chuyen duong")
    bang(m.phan_loai_loi_api(LoiGia(500, "api_error")) is m.Dung, "500 khong nam trong tap chuyen duong")


def ca_sub_loi_chuyen_api(m):
    rc, _, err = chay_lenh(m, {"TL_ANTHROPIC_API_KEY": KEY_GIA},
                           {"api": duong_api_voi(m, client_gia()),
                            "sub": duong_sub_voi(m, run_sub_gia(rc=1, is_error=True, result="usage limit reached"))},
                           thu_tu="sub,api")
    bang(rc == 0 and "DUONG: api" in err and "[chuyen duong] sub:" in err, f"rc={rc} {err}")


def ca_sub_go_key_va_cat_ngu_canh(m):
    nk = []
    env = {"ANTHROPIC_API_KEY": KEY_GIA, "TL_ANTHROPIC_API_KEY": KEY_GIA,
           "ANTHROPIC_AUTH_TOKEN": "x", "PATH": "/usr/bin"}
    m.duong_sub("he", "nd", {"type": "object"}, "claude-haiku-5-5", env,
                chay=run_sub_gia(nhat_ky=nk), tim=lambda t: "/usr/bin/claude")
    cmd, k = nk[0]
    bang(not any(b in k["env"] for b in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "TL_ANTHROPIC_API_KEY")),
         f"duong sub phai go key khoi env con: {sorted(k['env'])}")
    bang(k.get("stdin") is subprocess.DEVNULL, "duong sub phai stdin=DEVNULL")
    i = cmd.index("--tools")
    bang(cmd[i + 1] == "", f"phai --tools rong: {cmd}")
    bang("--bare" not in cmd, "--bare bien sub thanh api")
    bang("--strict-mcp-config" in cmd and "--setting-sources" in cmd, f"thieu co cat ngu canh: {cmd}")


def ca_sub_sai_model_thi_dung(m):
    rc, _, err = chay_lenh(m, {}, {"api": duong_api_voi(m, client_gia()),
                                   "sub": duong_sub_voi(m, run_sub_gia(model="claude-opus-5-5"))},
                           thu_tu="sub")
    bang(rc == m.MA_DUNG, f"model khac yeu cau phai DUNG: rc={rc} {err}")


def ca_het_duong(m):
    rc, _, err = chay_lenh(m, {}, {"api": duong_api_voi(m, client_gia()),
                                   "sub": duong_sub_voi(m, run_sub_gia(), tim=lambda t: None)})
    bang(rc == m.MA_HET_DUONG and "HET DUONG" in err, f"rc={rc} {err}")


def ca_lech_nguyen_van(m):
    sai = json.loads(json.dumps(DUNG))
    sai["khai_niem"][0]["dinh_nghia"] = "việc mô phỏng trí tuệ con người bằng máy."
    rc, _, err = chay_lenh(m, {"TL_ANTHROPIC_API_KEY": KEY_GIA},
                           {"api": duong_api_voi(m, client_gia(data=sai))})
    bang(rc == m.MA_LECH_NGUYEN_VAN, f"dinh nghia bi dien giai phai rc 5: rc={rc} {err}")


def ca_chuan_hoa_chu_la(m):
    co_la = json.loads(json.dumps(DUNG))
    for k in co_la["khai_niem"]:
        k["dinh_nghia"] = "là " + k["dinh_nghia"]
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "kq.json"
        rc, _, err = chay_lenh(m, {}, {"sub": duong_sub_voi(m, run_sub_gia(data=co_la))},
                               thu_tu="sub", out=str(out))
        kn = json.loads(out.read_text(encoding="utf-8"))["khai_niem"] if out.exists() else []
    bang(rc == 0, f"rc={rc} {err}")
    bang(kn == DUNG["khai_niem"], f"hai duong phai ra CUNG ket qua sau chuan hoa: {kn}")


def ca_tach_sai_cho(m):
    sai = json.loads(json.dumps(DUNG))
    sai["khai_niem"][0]["thuat_ngu"] = "Trí tuệ"   # mảnh vẫn là chuỗi con, cụm thì không
    rc, _, err = chay_lenh(m, {"TL_ANTHROPIC_API_KEY": KEY_GIA}, {"api": duong_api_voi(m, client_gia(data=sai))})
    bang(rc == m.MA_LECH_NGUYEN_VAN, f"tach sai ranh gioi phai rc 5: rc={rc} {err}")


def ca_tu_choi_thi_dung(m):
    rc, _, err = chay_lenh(m, {"TL_ANTHROPIC_API_KEY": KEY_GIA},
                           {"api": duong_api_voi(m, client_gia(stop="refusal")),
                            "sub": duong_sub_voi(m, run_sub_gia())})
    bang(rc == m.MA_DUNG, f"refusal phai DUNG, khong chuyen sub: rc={rc} {err}")


def ca_schema_sai_thi_dung(m):
    sai = {"khai_niem": [{"stt": "1", "thuat_ngu": "a", "dinh_nghia": "b"}]}
    rc, _, err = chay_lenh(m, {"TL_ANTHROPIC_API_KEY": KEY_GIA}, {"api": duong_api_voi(m, client_gia(data=sai))})
    bang(rc == m.MA_DUNG, f"stt khong phai integer phai DUNG: rc={rc} {err}")


def ca_khong_in_key(m):
    with tempfile.TemporaryDirectory() as d:
        nk = Path(d) / "u.jsonl"
        rc, out, err = chay_lenh(m, {"TL_ANTHROPIC_API_KEY": KEY_GIA},
                                 {"api": duong_api_voi(m, client_gia())}, nhat_ky=str(nk))
        dong = nk.read_text(encoding="utf-8")
    bang(rc == 0, err)
    bang(KEY_GIA not in out + err + dong, "gia tri key lot ra stdout/stderr/nhat ky")
    bang(json.loads(dong)["duong"] == "api", f"nhat ky sai: {dong}")


def ca_thu_tu(m):
    bang(m.doc_thu_tu(None) == ("api", "sub"), "mac dinh api,sub")
    bang(m.doc_thu_tu("sub, api") == ("sub", "api"), "nhan khoang trang")
    for x in ("api,api", "openai", ","):
        try:
            m.doc_thu_tu(x)
        except ValueError:
            continue
        raise TinHieuChotCa(f"thu tu {x!r} phai bi tu choi")


CA = [ca_api_dat, ca_uu_tien_bien_tl, ca_thieu_key_chuyen_sub, ca_het_credit_402_chuyen_sub,
      ca_400_khac_thi_dung, ca_ket_noi_chuyen_duong, ca_sub_loi_chuyen_api, ca_sub_go_key_va_cat_ngu_canh,
      ca_sub_sai_model_thi_dung, ca_het_duong, ca_lech_nguyen_van, ca_chuan_hoa_chu_la, ca_tach_sai_cho,
      ca_tu_choi_thi_dung,
      ca_schema_sai_thi_dung, ca_khong_in_key, ca_thu_tu]

# (tên, (chuỗi gốc, chuỗi thay), ca đích PHẢI đỏ bằng TinHieuChotCa)
DOT_BIEN = [
    ("402_khong_chuyen", ("if ma in (401, 402, 403, 429)", "if ma in (401, 403, 429)"),
     "ca_het_credit_402_chuyen_sub"),
    ("moi_400_deu_chuyen", ('if ma == 400 and "credit balance" in thong_bao:', "if ma == 400:"),
     "ca_400_khac_thi_dung"),
    ("sub_giu_key", ("if k not in BIEN_GO_KHOI_SUB}", "}"), "ca_sub_go_key_va_cat_ngu_canh"),
    ("bo_kiem_model_sub", ("    if da_chay != {model}:\n", "    if False:\n"), "ca_sub_sai_model_thi_dung"),
    ("bo_kiem_nguyen_van", ("    if lech:\n        print(f\"LECH", "    if False:\n        print(f\"LECH"),
     "ca_lech_nguyen_van"),
    ("bo_chuan_hoa_la", ('        if k["dinh_nghia"].startswith("là "):', '        if False:'), "ca_chuan_hoa_chu_la"),
    ("kiem_tung_manh", ("""            if f'{k["thuat_ngu"]} là {k["dinh_nghia"]}' not in van_ban]""",
                        """            if k["dinh_nghia"] not in van_ban or k["thuat_ngu"] not in van_ban]"""),
     "ca_tach_sai_cho"),
    ("refusal_chuyen_duong", ('raise Dung(f"model tu choi', 'raise ChuyenDuong(f"model tu choi'),
     "ca_tu_choi_thi_dung"),
    ("bo_kiem_schema", ("        kiem_schema(kq[\"data\"], SCHEMA_KHAI_NIEM)\n", ""), "ca_schema_sai_thi_dung"),
    ("uu_tien_bien_chuan", ('BIEN_KEY = ("TL_ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY")',
                            'BIEN_KEY = ("ANTHROPIC_API_KEY", "TL_ANTHROPIC_API_KEY")'), "ca_uu_tien_bien_tl"),
    ("them_bare", ('"--no-session-persistence", "--tools", "",', '"--no-session-persistence", "--bare", "--tools", "",'),
     "ca_sub_go_key_va_cat_ngu_canh"),
]


def chay_ca(m, ds):
    qua, hong = 0, []
    for f in ds:
        try:
            f(m)
            qua += 1
        except TinHieuChotCa as e:
            hong.append((f.__name__, f"CHOT: {e}"))
        except Exception as e:  # noqa: BLE001
            hong.append((f.__name__, f"LOI VO CAN {type(e).__name__}: {e}"))
    return qua, hong


def chay_dot_bien():
    goc = NGUON.read_text(encoding="utf-8")
    giet, ket = 0, []
    theo_ten = {f.__name__: f for f in CA}
    for ten, (cu, moi), dich in DOT_BIEN:
        if goc.count(cu) != 1:
            ket.append(f"  {ten}: KHONG AP DUOC (neo xuat hien {goc.count(cu)} lan)")
            continue
        with tempfile.TemporaryDirectory() as d:
            tep = Path(d) / f"llm_route_db_{ten}.py"
            tep.write_text(goc.replace(cu, moi), encoding="utf-8")
            try:
                m = nap(tep, f"llm_route_db_{ten}")
            except Exception as e:  # noqa: BLE001
                ket.append(f"  {ten}: TIN DUNG GIA (nap loi {type(e).__name__})")
                continue
            try:
                theo_ten[dich](m)
                ket.append(f"  {ten}: SONG — {dich} van qua")
            except TinHieuChotCa:
                giet += 1
            except Exception as e:  # noqa: BLE001
                ket.append(f"  {ten}: TIN DUNG GIA ({dich} chet vi {type(e).__name__})")
    return giet, ket


def main() -> int:
    m = nap()
    qua, hong = chay_ca(m, CA)
    for ten, ly_do in hong:
        print(f"HONG {ten}: {ly_do}")
    giet, ket = chay_dot_bien()
    for d in ket:
        print(d)
    print(f"llm_route tests: {qua}/{len(CA)} ca QUA · {giet}/{len(DOT_BIEN)} dot bien GIET")
    return 0 if (not hong and giet == len(DOT_BIEN)) else 1


if __name__ == "__main__":
    sys.exit(main())
