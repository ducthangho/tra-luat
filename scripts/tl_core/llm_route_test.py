#!/usr/bin/env python3
"""Test `scripts/tl_core/llm_route.py` — chỉ thư viện chuẩn, không gọi mạng, không cần SDK `anthropic`.
Không vào gói phát hành: tên tệp nằm trong `_RELEASE_EXCLUDE_NAMES_ANYWHERE` (`tl_core/release.py`).

Mỗi chốt có MỘT đột biến riêng chạy trên BẢN SAO TẠM (không bao giờ sửa tệp thật —
CLAUDE.md §"Đột biến ghi vào tệp THẬT"). Đột biến chỉ được tính GIẾT khi CHÍNH ca đích
đỏ bằng `TinHieuChotCa` (assertion của ca), không phải vì lỗi vô can — CLAUDE.md
§"ĐỘT BIẾN BỊ GIẾT KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO".

Dòng tổng (sổ đăng ký CI): `llm_route tests: N/N ca QUA · M/M dot bien GIET`.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import types
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


def chay_lenh(m, env, cac_duong, thu_tu=None):
    """Bộ lái tối thiểu giống handler `cmd_llm_khai_niem`: trả (rc, kq|None, nhật ký chữ).
    Test lõi THUẦN mà không nạp cả CLI tl."""
    tt = m.doc_thu_tu(thu_tu) if thu_tu else m.THU_TU_MAC_DINH
    try:
        kq = m.tach_khai_niem(VAN_BAN, "134/2025/QH15", "claude-haiku-5-5", tt, env, cac_duong)
    except m.HetDuong as e:
        return m.MA_HET_DUONG, None, "HET DUONG " + str(e)
    except m.Dung as e:
        return m.MA_DUNG, None, "DUNG " + str(e)
    nhat = " ".join(f"[chuyen duong] {d}: {ly}" for d, ly in kq["lan_thu"])
    nhat += (f" DUONG: {kq['duong']} key={kq['nguon_key']}"
             f" TOKEN: input={kq['usage']['input']} output={kq['usage']['output']}")
    return (m.MA_LECH_NGUYEN_VAN if kq["lech"] else m.MA_OK), kq, nhat


def api(m, tao_client):
    return lambda *a: m.duong_api(*a, tao_client=tao_client)


def sub(m, chay, tim=lambda t: "/usr/bin/claude"):
    return lambda *a: m.duong_sub(*a, chay=chay, tim=tim)


def cam(ten):
    def _f(*a):
        raise TinHieuChotCa(f"duong {ten} KHONG duoc goi")
    return _f


KEY = {"TL_ANTHROPIC_API_KEY": KEY_GIA}


# ------------------------------------------------------------- ca: chọn đường

def ca_api_dat(m):
    nk = []
    rc, kq, nhat = chay_lenh(m, KEY, {"api": api(m, client_gia(nhat_ky=nk)), "sub": cam("sub")}, "api,sub")
    bang(rc == 0, f"rc={rc} {nhat}")
    bang("DUONG: api key=TL_ANTHROPIC_API_KEY" in nhat and "TOKEN: input=100 output=50" in nhat, nhat)
    bang(nk and nk[0]["output_config"]["format"]["type"] == "json_schema", f"khong dung structured output: {nk}")


def ca_mac_dinh_sub_truoc(m):
    bang(m.THU_TU_MAC_DINH == ("sub", "api"), f"mac dinh phai sub,api: {m.THU_TU_MAC_DINH}")
    rc, kq, nhat = chay_lenh(m, KEY, {"sub": sub(m, run_sub_gia()), "api": cam("api")})
    bang(rc == 0 and kq["duong"] == "sub" and not kq["lan_thu"], f"rc={rc} {nhat}")


def ca_uu_tien_bien_tl(m):
    ten, _ = m.lay_key({"ANTHROPIC_API_KEY": "a", "TL_ANTHROPIC_API_KEY": "b"})
    bang(ten == "TL_ANTHROPIC_API_KEY", f"phai uu tien TL_: {ten}")
    ten, _ = m.lay_key({"TL_ANTHROPIC_API_KEY": "   ", "ANTHROPIC_API_KEY": "a"})
    bang(ten == "ANTHROPIC_API_KEY", f"bien rong khong duoc tinh la key: {ten}")


def ca_thieu_key_chuyen_sub(m):
    rc, kq, nhat = chay_lenh(m, {}, {"api": api(m, client_gia()), "sub": sub(m, run_sub_gia())}, "api,sub")
    bang(rc == 0 and kq["duong"] == "sub" and "[chuyen duong] api: khong co" in nhat, nhat)


def ca_het_credit_402_chuyen_sub(m):
    # 402 KHÔNG kèm `type` để đo riêng nhánh mã trạng thái (có `billing_error` thì nhánh `kieu`
    # che mất, và đột biến gỡ 402 sống sót — đo 24-11-2026).
    for loi in (LoiGia(402, None, "payment required"), LoiGia(None, "billing_error", "billing"),
                LoiGia(400, "invalid_request_error", "Your credit balance is too low")):
        rc, kq, nhat = chay_lenh(m, KEY, {"api": api(m, client_gia(loi=loi)), "sub": sub(m, run_sub_gia())}, "api,sub")
        bang(rc == 0 and kq["duong"] == "sub", f"het credit ({loi.status_code}) phai chuyen sub: rc={rc} {nhat}")


def ca_400_khac_thi_dung(m):
    rc, _, nhat = chay_lenh(m, KEY, {"api": api(m, client_gia(loi=LoiGia(400, "invalid_request_error", "bad"))),
                                     "sub": cam("sub")}, "api,sub")
    bang(rc == m.MA_DUNG, f"400 thuong phai DUNG (rc 4), khong tieu tien lan hai: rc={rc} {nhat}")


def ca_ket_noi_chuyen_duong(m):
    bang(m.phan_loai_loi_api(LoiGia(ten="APIConnectionError")) is m.ChuyenDuong, "mat ket noi phai chuyen duong")
    bang(m.phan_loai_loi_api(LoiGia(429, "rate_limit_error")) is m.ChuyenDuong, "429 phai chuyen duong")
    bang(m.phan_loai_loi_api(LoiGia(500, "api_error")) is m.Dung, "500 khong nam trong tap chuyen duong")


def ca_sub_loi_chuyen_api(m):
    rc, kq, nhat = chay_lenh(m, KEY, {"api": api(m, client_gia()),
                                      "sub": sub(m, run_sub_gia(rc=1, is_error=True, result="usage limit"))})
    bang(rc == 0 and kq["duong"] == "api" and "[chuyen duong] sub:" in nhat, f"rc={rc} {nhat}")


def ca_sub_go_key_va_cat_ngu_canh(m):
    nk = []
    env = {"ANTHROPIC_API_KEY": KEY_GIA, "TL_ANTHROPIC_API_KEY": KEY_GIA, "ANTHROPIC_AUTH_TOKEN": "x", "PATH": "/usr/bin"}
    m.duong_sub("he", "nd", {"type": "object"}, "claude-haiku-5-5", env,
                chay=run_sub_gia(nhat_ky=nk), tim=lambda t: "/usr/bin/claude")
    cmd, k = nk[0]
    bang(not any(b in k["env"] for b in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "TL_ANTHROPIC_API_KEY")),
         f"duong sub phai go key khoi env con: {sorted(k['env'])}")
    bang(k.get("stdin") is subprocess.DEVNULL, "duong sub phai stdin=DEVNULL")
    bang(cmd[cmd.index("--tools") + 1] == "", f"phai --tools rong: {cmd}")
    bang("--bare" not in cmd, "--bare bien sub thanh api")
    bang("--strict-mcp-config" in cmd and "--setting-sources" in cmd, f"thieu co cat ngu canh: {cmd}")


def ca_sub_sai_model_thi_dung(m):
    rc, _, nhat = chay_lenh(m, {}, {"sub": sub(m, run_sub_gia(model="claude-opus-5-5")), "api": cam("api")})
    bang(rc == m.MA_DUNG, f"model khac yeu cau phai DUNG: rc={rc} {nhat}")


def ca_het_duong(m):
    rc, _, nhat = chay_lenh(m, {}, {"api": api(m, client_gia()), "sub": sub(m, run_sub_gia(), tim=lambda t: None)})
    bang(rc == m.MA_HET_DUONG and "HET DUONG" in nhat, f"rc={rc} {nhat}")


def ca_tu_choi_thi_dung(m):
    rc, _, nhat = chay_lenh(m, KEY, {"api": api(m, client_gia(stop="refusal")), "sub": cam("sub")}, "api,sub")
    bang(rc == m.MA_DUNG, f"refusal phai DUNG, khong chuyen sub: rc={rc} {nhat}")


def ca_schema_sai_thi_dung(m):
    sai = {"khai_niem": [{"stt": "1", "thuat_ngu": "a", "dinh_nghia": "b"}]}
    rc, _, nhat = chay_lenh(m, KEY, {"api": api(m, client_gia(data=sai))}, "api")
    bang(rc == m.MA_DUNG, f"stt khong phai integer phai DUNG: rc={rc} {nhat}")


# ------------------------------------------------------------- ca: nguyên văn

def ca_lech_nguyen_van(m):
    sai = json.loads(json.dumps(DUNG))
    sai["khai_niem"][0]["dinh_nghia"] = "việc mô phỏng trí tuệ con người bằng máy."
    rc, _, nhat = chay_lenh(m, KEY, {"api": api(m, client_gia(data=sai))}, "api")
    bang(rc == m.MA_LECH_NGUYEN_VAN, f"dinh nghia bi dien giai phai rc 5: rc={rc} {nhat}")


def ca_chuan_hoa_chu_la(m):
    co_la = json.loads(json.dumps(DUNG))
    for k in co_la["khai_niem"]:
        k["dinh_nghia"] = "là " + k["dinh_nghia"]
    rc, kq, nhat = chay_lenh(m, {}, {"sub": sub(m, run_sub_gia(data=co_la))}, "sub")
    bang(rc == 0, f"rc={rc} {nhat}")
    bang(kq["khai_niem"] == DUNG["khai_niem"], f"hai duong phai ra CUNG ket qua sau chuan hoa: {kq['khai_niem']}")


def ca_tach_sai_cho(m):
    sai = json.loads(json.dumps(DUNG))
    sai["khai_niem"][0]["thuat_ngu"] = "Trí tuệ"   # mảnh vẫn là chuỗi con, cụm thì không
    rc, _, nhat = chay_lenh(m, KEY, {"api": api(m, client_gia(data=sai))}, "api")
    bang(rc == m.MA_LECH_NGUYEN_VAN, f"tach sai ranh gioi phai rc 5: rc={rc} {nhat}")


def ca_khong_in_key(m):
    rc, kq, nhat = chay_lenh(m, KEY, {"api": api(m, client_gia())}, "api")
    with tempfile.TemporaryDirectory() as d:
        nk = Path(d) / "u.jsonl"
        m.ghi_nhat_ky(str(nk), kq, "thu")
        dong = nk.read_text(encoding="utf-8")
    bang(rc == 0, nhat)
    bang(KEY_GIA not in nhat + dong + json.dumps(kq, ensure_ascii=False, default=str),
         "gia tri key lot ra ket qua/nhat ky")
    bang(json.loads(dong)["duong"] == "api", f"nhat ky sai: {dong}")


# ------------------------------------------------------------- ca: thứ tự đường

def ca_thu_tu(m):
    bang(m.doc_thu_tu(None) == ("sub", "api"), "mac dinh sub,api")
    bang(m.doc_thu_tu("api, sub") == ("api", "sub"), "nhan khoang trang")
    for x in ("api,api", "openai", ",", ""):
        try:
            m.doc_thu_tu(x)
        except ValueError:
            continue
        raise TinHieuChotCa(f"thu tu {x!r} phai bi tu choi")


def ca_thu_tu_hieu_luc_va_luu(m):
    with tempfile.TemporaryDirectory() as d:
        tep = Path(d) / "con" / "llm.json"
        env = {"TL_LLM_ORDER_FILE": str(tep)}
        bang(m.thu_tu_hieu_luc(env=env) == (("sub", "api"), "mac dinh"), "khong gi ca phai la mac dinh")
        env["TL_LLM_ORDER"] = "api"
        bang(m.thu_tu_hieu_luc(env=env) == (("api",), "bien TL_LLM_ORDER"), "bien thang mac dinh")
        m.luu_thu_tu("api,sub", env=env)
        tt, nguon = m.thu_tu_hieu_luc(env=env)
        bang(tt == ("api", "sub") and nguon.startswith("tep "), f"tep da luu phai thang bien: {tt} {nguon}")
        bang(m.thu_tu_hieu_luc("sub", env=env) == (("sub",), "co --thu-tu"), "co phai thang tep")
        try:
            m.luu_thu_tu("openai", env=env)
            raise TinHieuChotCa("gia tri sai phai bi tu choi TRUOC khi ghi")
        except ValueError:
            pass
        bang(json.loads(tep.read_text(encoding="utf-8")) == {"thu_tu": "api,sub"}, "gia tri sai khong duoc ghi de tep")
        bang(not [x for x in tep.parent.iterdir() if x.name != tep.name], "con sot tep tam sau khi ghi")
        bang(m.xoa_thu_tu(env=env) and not tep.exists(), "reset phai xoa tep")
        bang(m.thu_tu_hieu_luc(env=env)[1] == "bien TL_LLM_ORDER", "sau reset phai ve bien")


def ca_tep_hong_fail_closed(m):
    with tempfile.TemporaryDirectory() as d:
        for noi_dung in ("{hong", '{"thu_tu": 5}', '{"thu_tu": "openai"}', "[]"):
            tep = Path(d) / "llm.json"
            tep.write_text(noi_dung, encoding="utf-8")
            try:
                kq = m.thu_tu_hieu_luc(env={"TL_LLM_ORDER_FILE": str(tep), "TL_LLM_ORDER": "api"})
            except ValueError:
                continue
            raise TinHieuChotCa(f"tep hong {noi_dung!r} phai fail-closed, KHONG lui ve {kq}")


# ------------------------------------------------------------- ca: lấy nguyên văn qua tl extract

def ca_lay_dieu_qua_extract(m):
    goi = []

    def chay(cmd, **k):
        goi.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, "dau\n===== Điều 3 =====\n" + VAN_BAN + "\n", "[tl] canonical: X\n")

    vb, loi = m.lay_dieu_qua_extract("134/2025/QH15", "3", "/x/tl.py", chay=chay, them=["--profile", "P"])
    bang(vb == VAN_BAN.strip() and "canonical" in loi, f"cat sai: {vb!r}")
    bang(goi[0][1:6] == ["/x/tl.py", "extract", "134/2025/QH15", "--dieu", "3"] and goi[0][-2:] == ["--profile", "P"],
         f"phai goi dung tl extract: {goi[0]}")

    def chay_hong(cmd, **k):
        return subprocess.CompletedProcess(cmd, 1, "", "khong tim thay")
    try:
        m.lay_dieu_qua_extract("999/2099/QH99", "3", "/x/tl.py", chay=chay_hong)
    except ValueError:
        return
    raise TinHieuChotCa("extract loi phai nem ValueError, khong tra van ban rong")


CA = [ca_api_dat, ca_mac_dinh_sub_truoc, ca_uu_tien_bien_tl, ca_thieu_key_chuyen_sub, ca_het_credit_402_chuyen_sub,
      ca_400_khac_thi_dung, ca_ket_noi_chuyen_duong, ca_sub_loi_chuyen_api, ca_sub_go_key_va_cat_ngu_canh,
      ca_sub_sai_model_thi_dung, ca_het_duong, ca_tu_choi_thi_dung, ca_schema_sai_thi_dung,
      ca_lech_nguyen_van, ca_chuan_hoa_chu_la, ca_tach_sai_cho, ca_khong_in_key,
      ca_thu_tu, ca_thu_tu_hieu_luc_va_luu, ca_tep_hong_fail_closed, ca_lay_dieu_qua_extract]

# (tên, (chuỗi gốc, chuỗi thay), ca đích PHẢI đỏ bằng TinHieuChotCa)
DOT_BIEN = [
    ("402_khong_chuyen", ("if ma in (401, 402, 403, 429)", "if ma in (401, 403, 429)"), "ca_het_credit_402_chuyen_sub"),
    ("moi_400_deu_chuyen", ('if ma == 400 and "credit balance" in thong_bao:', "if ma == 400:"), "ca_400_khac_thi_dung"),
    ("sub_giu_key", ("if k not in BIEN_GO_KHOI_SUB}", "}"), "ca_sub_go_key_va_cat_ngu_canh"),
    ("them_bare", ('"--no-session-persistence", "--tools", "",', '"--no-session-persistence", "--bare", "--tools", "",'),
     "ca_sub_go_key_va_cat_ngu_canh"),
    ("bo_kiem_model_sub", ("    if da_chay != {model}:\n", "    if False:\n"), "ca_sub_sai_model_thi_dung"),
    ("refusal_chuyen_duong", ('raise Dung(f"model tu choi', 'raise ChuyenDuong(f"model tu choi'), "ca_tu_choi_thi_dung"),
    ("bo_kiem_schema", ('    kiem_schema(kq["data"], SCHEMA_KHAI_NIEM)\n', ""), "ca_schema_sai_thi_dung"),
    ("bo_kiem_nguyen_van", ('kq["lech"] = lech_nguyen_van(kq["khai_niem"], van_ban)', 'kq["lech"] = []'),
     "ca_lech_nguyen_van"),
    ("bo_chuan_hoa_la", ('        if k["dinh_nghia"].startswith("là "):', "        if False:"), "ca_chuan_hoa_chu_la"),
    ("kiem_tung_manh", ("""            if f'{k["thuat_ngu"]} là {k["dinh_nghia"]}' not in van_ban]""",
                        """            if k["dinh_nghia"] not in van_ban or k["thuat_ngu"] not in van_ban]"""),
     "ca_tach_sai_cho"),
    ("uu_tien_bien_chuan", ('BIEN_KEY = ("TL_ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY")',
                            'BIEN_KEY = ("ANTHROPIC_API_KEY", "TL_ANTHROPIC_API_KEY")'), "ca_uu_tien_bien_tl"),
    ("mac_dinh_api_truoc", ('THU_TU_MAC_DINH = ("sub", "api")', 'THU_TU_MAC_DINH = ("api", "sub")'),
     "ca_mac_dinh_sub_truoc"),
    ("bien_thang_tep", ("    if tep.exists():\n        try:", "    if tep.exists() and not env.get(BIEN_THU_TU):\n        try:"),
     "ca_thu_tu_hieu_luc_va_luu"),
    ("tep_hong_lui_mac_dinh", ('            raise ValueError(f"tep thu tu {tep} hong', '            return THU_TU_MAC_DINH, "mac dinh"\n            raise ValueError(f"tep thu tu {tep} hong'),
     "ca_tep_hong_fail_closed"),
    ("luu_truoc_kiem", ("    thu_tu = doc_thu_tu(gia_tri)\n    tep = tep_thu_tu(env)",
                        "    thu_tu = tuple(str(gia_tri).split(','))\n    tep = tep_thu_tu(env)"), "ca_thu_tu_hieu_luc_va_luu"),
    ("extract_loi_tra_rong", ('    if p.returncode != 0 or dau not in out:\n        raise ValueError(',
                              '    if dau not in out:\n        return "", ""\n    if False:\n        raise ValueError('),
     "ca_lay_dieu_qua_extract"),
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
