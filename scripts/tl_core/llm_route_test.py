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


_VANG = object()


AUTH_SUB = {"loggedIn": True, "authMethod": "claude.ai", "apiProvider": "firstParty"}
_VANG_USAGE = object()


def run_sub_gia(data=None, rc=0, is_error=False, model="claude-haiku-5-5", nhat_ky=None, result="ok",
                subtype="success", auth=AUTH_SUB, auth_rc=0, usage=_VANG_USAGE, stop_reason=None):
    def chay(cmd, **k):
        if nhat_ky is not None:
            nhat_ky.append((cmd, k))
        if list(cmd[1:3]) == ["auth", "status"]:
            return subprocess.CompletedProcess(cmd, auth_rc, json.dumps(auth), "")
        mu = ({model: {"inputTokens": 2, "outputTokens": 55, "cacheReadInputTokens": 0,
                       "cacheCreationInputTokens": 1911, "canonicalModel": model}}
              if usage is _VANG_USAGE else usage)
        kq = {"subtype": subtype, "is_error": is_error, "result": result, "structured_output": data or DUNG,
              "total_cost_usd": 0.0004, "modelUsage": mu}
        if stop_reason is not None:
            kq["stop_reason"] = stop_reason
        kq = {k2: v for k2, v in kq.items() if v is not _VANG}
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
                                      "sub": sub(m, run_sub_gia(rc=1, is_error=True, result="usage limit", usage={}))})
    bang(rc == 0 and kq["duong"] == "api" and "[chuyen duong] sub:" in nhat, f"rc={rc} {nhat}")


def ca_sub_go_key_va_cat_ngu_canh(m):
    nk = []
    env = {"ANTHROPIC_API_KEY": KEY_GIA, "TL_ANTHROPIC_API_KEY": KEY_GIA, "ANTHROPIC_AUTH_TOKEN": "x", "PATH": "/usr/bin"}
    m.duong_sub("he", "nd", {"type": "object"}, "claude-haiku-5-5", env,
                chay=run_sub_gia(nhat_ky=nk), tim=lambda t: "/usr/bin/claude")
    cmd, k = next(c for c in nk if "-p" in c[0])
    auth_cmd, auth_k = next(c for c in nk if list(c[0][1:3]) == ["auth", "status"])
    bang(not any(b in auth_k["env"] for b in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "TL_ANTHROPIC_API_KEY")),
         "phep do auth status phai dung CUNG env da go key nhu loi goi model")
    bang(not any(b in k["env"] for b in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "TL_ANTHROPIC_API_KEY")),
         f"duong sub phai go key khoi env con: {sorted(k['env'])}")
    bang(k.get("stdin") is subprocess.DEVNULL, "duong sub phai stdin=DEVNULL")
    bang(cmd[cmd.index("--tools") + 1] == "", f"phai --tools rong: {cmd}")
    bang("--bare" not in cmd, "--bare bien sub thanh api")
    bang("--strict-mcp-config" in cmd and cmd[cmd.index("--setting-sources") + 1] == "",
         f"phai --setting-sources RONG (khong nap settings nguoi dung): {cmd}")


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


# ------------------------------------------------------------- ca: cross-review lượt 1 (F1–F3)

VAN_BAN_SO = ("Điều 2. Giải thích từ ngữ\nTrong Luật này, các từ ngữ dưới đây được hiểu như sau:\n"
              "1. Hồ sơ là tài liệu do cơ quan có thẩm quyền lập.\n"
              "2. Chủ thể là một trong các đối tượng sau:\na) tổ chức;\nb) cá nhân.")
KN_SO = [{"stt": 1, "thuat_ngu": "Hồ sơ", "dinh_nghia": "tài liệu do cơ quan có thẩm quyền lập."},
         {"stt": 2, "thuat_ngu": "Chủ thể", "dinh_nghia": "một trong các đối tượng sau:\na) tổ chức;\nb) cá nhân."}]


def ca_dinh_nghia_bi_cat(m):
    cat = json.loads(json.dumps(KN_SO))
    cat[0]["dinh_nghia"] = "tài liệu"          # F1: chuỗi con của nguồn nhưng CẮT cụt
    bang(m.lech_nguyen_van(cat, VAN_BAN_SO) == [1], f"dinh nghia bi cat phai lech: {m.lech_nguyen_van(cat, VAN_BAN_SO)}")


def ca_bo_khoan_va_mang_rong(m):
    bang(m.lech_nguyen_van(KN_SO[:1], VAN_BAN_SO) == [2], "thieu khoan 2 phai lech [2]")
    bang(m.lech_nguyen_van([], VAN_BAN_SO) == [1, 2], "mang rong phai lech moi khoan")
    bang(m.lech_nguyen_van(KN_SO, "Không có khoản nào ở đây") == [0], "nguon khong tach duoc khoan phai [0]")


def ca_trao_so(m):
    trao = [dict(KN_SO[1], stt=1), dict(KN_SO[0], stt=2)]
    bang(m.lech_nguyen_van(trao, VAN_BAN_SO) == [1, 2], "trao thu tu khoan phai lech")
    sai_so = [dict(KN_SO[0], stt=2), dict(KN_SO[1], stt=1)]
    bang(m.lech_nguyen_van(sai_so, VAN_BAN_SO) == [2, 1], "dung thu tu ma sai stt phai lech")


def ca_khoan_co_so_va_diem_dat(m):
    bang(m.tach_khoan(VAN_BAN_SO) == [(1, "Hồ sơ là tài liệu do cơ quan có thẩm quyền lập."),
                                       (2, "Chủ thể là một trong các đối tượng sau:\na) tổ chức;\nb) cá nhân.")],
         f"tach sai: {m.tach_khoan(VAN_BAN_SO)}")
    bang(m.lech_nguyen_van(KN_SO, VAN_BAN_SO) == [], "ket qua dung (co diem a, b) bi chan oan")
    bang(m.lech_nguyen_van(m.chuan_hoa_khai_niem(json.loads(json.dumps(DUNG["khai_niem"]))), VAN_BAN) == [],
         "nguon mat so thu tu (Google Doc) bi chan oan")


def ca_sub_het_luot_schema_thi_dung(m):
    # usage={}: KHÔNG token ⇒ chỉ chốt subtype mới dừng được ca này (chốt "đã chạy model" không che nó).
    rc, _, nhat = chay_lenh(m, KEY, {"sub": sub(m, run_sub_gia(rc=1, is_error=True, usage={},
                                                               subtype="error_max_structured_output_retries")),
                                     "api": cam("api")})
    bang(rc == m.MA_DUNG, f"can luot sua schema la loi phia yeu cau, khong duoc tieu credit API: rc={rc} {nhat}")


def ca_sub_thieu_dau_duong_khong_nhan(m):
    # Mỗi tín hiệu lỗi TÁCH RIÊNG (F10): rc khác 0 một mình, is_error một mình, subtype lạ, thiếu trường.
    # Lượt 2 N2: model ĐÃ CHẠY (có token) ⇒ DỪNG, không gọi API lần hai; CHƯA chạy (không token) ⇒ chuyển.
    hong = (dict(subtype="error_during_execution"), dict(is_error=_VANG), dict(subtype=_VANG), dict(rc=1),
            dict(is_error=True))
    for loi in hong:
        rc, kq, nhat = chay_lenh(m, KEY, {"sub": sub(m, run_sub_gia(**loi)), "api": cam("api")})
        bang(rc == m.MA_DUNG, f"envelope loi {loi} SAU khi model chay: phai DUNG (khong nhan, khong goi api): rc={rc} {nhat}")
        rc, kq, nhat = chay_lenh(m, KEY, {"sub": sub(m, run_sub_gia(usage={}, **loi)), "api": api(m, client_gia())})
        bang(rc == 0 and kq["duong"] == "api", f"envelope loi {loi} TRUOC khi model chay phai chuyen api: rc={rc} {nhat}")


def ca_sub_dinh_tuyen_nha_cung_cap(m):
    for env in ({"CLAUDE_CODE_USE_BEDROCK": "1"}, {"CLAUDE_CODE_USE_GATEWAY": "true"},
                {"claude_code_use_foundry": "yes"}, {"ANTHROPIC_BASE_URL": "https://gw.example.com/v1"},
                {"CLAUDE_CODE_USE_TUONG_LAI_CHUA_BIET": "1"}):     # tên lạ ⇒ fail-closed
        goi = []
        try:
            m.duong_sub("he", "nd", {"type": "object"}, "claude-haiku-5-5", env,
                        chay=run_sub_gia(nhat_ky=goi), tim=lambda t: "/usr/bin/claude")
        except m.ChuyenDuong:
            bang(not goi, f"da goi claude -p du moi truong dinh tuyen {env}")
            continue
        raise TinHieuChotCa(f"moi truong {env} phai bi tu choi o duong sub")
    # Phiên Claude Code trên web đặt CLAUDE_CODE_USE_CCR_V2 — chặn nó là chặn oan đường sub ở chính
    # môi trường dùng nhiều nhất (lộ ở lần chạy thật 24-11-2026).
    for env in ({"CLAUDE_CODE_USE_VERTEX": "0"}, {"ANTHROPIC_BASE_URL": "https://api.anthropic.com"},
                {"CLAUDE_CODE_USE_CCR_V2": "1", "CLAUDE_CODE_USE_POWERSHELL_TOOL": "1"}):
        try:
            m.duong_sub("he", "nd", {"type": "object"}, "claude-haiku-5-5", env,
                        chay=run_sub_gia(), tim=lambda t: "/usr/bin/claude")
        except m.ChuyenDuong as e:
            raise TinHieuChotCa(f"moi truong hop le {env} bi CHAN OAN o duong sub: {e}") from e


def ca_qua_tai_chuyen_duong(m):
    for loi in (LoiGia(529, None, "overloaded"), LoiGia(503, None, "unavailable"),
                LoiGia(None, "overloaded_error", "overloaded")):
        bang(m.phan_loai_loi_api(loi) is m.ChuyenDuong, f"qua tai ({loi.status_code}/{loi.type}) phai chuyen duong")
    bang(m.phan_loai_loi_api(LoiGia(504, None, "x")) is m.Dung, "504 giu DUNG (yeu cau co the da duoc xu ly)")


def ca_co_rong_va_symlink_dut(m):
    with tempfile.TemporaryDirectory() as d:
        env = {"TL_LLM_ORDER_FILE": str(Path(d) / "khong_co.json"), "TL_LLM_ORDER": "api"}
        try:
            m.thu_tu_hieu_luc("", env=env)
            raise TinHieuChotCa("--thu-tu rong phai bi tu choi, khong roi sang bien")
        except ValueError:
            pass
        lk = Path(d) / "lk.json"
        try:
            lk.symlink_to(Path(d) / "da_chuyen_di.json")
        except (OSError, NotImplementedError):
            return   # nền không tạo được symlink (Windows thiếu quyền) — vế này KHÔNG ĐO ĐƯỢC ở đó
        env["TL_LLM_ORDER_FILE"] = str(lk)
        try:
            kq = m.thu_tu_hieu_luc(env=env)
            raise TinHieuChotCa(f"symlink dut phai fail-closed, khong roi ve {kq}")
        except ValueError:
            pass
        bang(m.xoa_thu_tu(env=env) is True and not lk.is_symlink(), "--reset phai xoa ca symlink dut")


def ca_extract_cham_tran(m):
    def chay(cmd, **k):
        return subprocess.CompletedProcess(cmd, 0, "===== Điều 3 =====\n" + VAN_BAN,
                                           "[tl] ⚠ độ dài chạm CAP export (~200k ký tự) — văn bản DÀI có thể bị CẮT\n")
    try:
        m.lay_dieu_qua_extract("1/2025/QH15", "3", "/x/tl.py", chay=chay)
    except ValueError as e:
        bang("cache-build" in str(e), f"thong bao phai chi duong no-cap: {e}")
        return
    raise TinHieuChotCa("nguon cham tran phai dung TRUOC khi goi model")


# ------------------------------------------------------------- ca: cross-review lượt 2 (N1–N7)

def ca_nguon_mo_ho_thi_khong_dat(m):
    # N1: khoản "X là" xuống dòng ở nguồn MẤT số ⇒ ranh giới không xác định ⇒ [0], không được báo đạt.
    mo_ho = "Điều 3a. Giải thích từ ngữ\nTrong Luật này:\nHồ sơ là\ntài liệu lập.\nChủ thể là cá nhân."
    bang(m.tach_khoan(mo_ho) is None, f"nguon mo ho phai None: {m.tach_khoan(mo_ho)}")
    bang(m.lech_nguyen_van([{"stt": 1, "thuat_ngu": "Chủ thể", "dinh_nghia": "cá nhân."}], mo_ho) == [0],
         "chi tra khoan sau ma van bao dat")
    truoc = "Điều 3. Giải thích từ ngữ\nĐoạn văn lạ không phải câu dẫn\nHồ sơ là tài liệu."
    bang(m.tach_khoan(truoc) is None, "dong la truoc khoan dau phai lam nguon mo ho")


def ca_so_khoan_nguon_va_dang_so(m):
    dinh = "Điều 2.\nTrong Luật này:\n1.Hồ sơ là tài liệu.\n(4) Chủ thể là cá nhân."
    bang(m.tach_khoan(dinh) == [(1, "Hồ sơ là tài liệu."), (4, "Chủ thể là cá nhân.")], f"{m.tach_khoan(dinh)}")
    dung = [{"stt": 1, "thuat_ngu": "Hồ sơ", "dinh_nghia": "tài liệu."},
            {"stt": 4, "thuat_ngu": "Chủ thể", "dinh_nghia": "cá nhân."}]
    bang(m.lech_nguyen_van(dung, dinh) == [], "so khoan theo nguon (1, 4) phai dat")
    bang(m.lech_nguyen_van([dung[0], dict(dung[1], stt=2)], dinh) == [2], "danh so theo vi tri thay so nguon phai lech")


def ca_tach_tai_la_dau_tien(m):
    vb = "Điều 3.\nTrong Luật này:\nTổ chức là đơn vị là pháp nhân."
    sai = [{"stt": 1, "thuat_ngu": "Tổ chức là đơn vị", "dinh_nghia": "pháp nhân."}]
    bang(m.lech_nguyen_van(sai, vb) == [1], "tach tai chu 'la' thu hai phai lech")
    dung = [{"stt": 1, "thuat_ngu": "Tổ chức", "dinh_nghia": "đơn vị là pháp nhân."}]
    bang(m.lech_nguyen_van(dung, vb) == [], "tach tai chu 'la' dau tien phai dat")


def ca_khoan_mat_so_co_diem_dat(m):
    vb = "Điều 3.\nTrong Luật này:\nChủ thể là một trong các đối tượng sau:\na) tổ chức;\nb) cá nhân.\nHồ sơ là tài liệu."
    kn = [{"stt": 1, "thuat_ngu": "Chủ thể", "dinh_nghia": "một trong các đối tượng sau:\na) tổ chức;\nb) cá nhân."},
          {"stt": 2, "thuat_ngu": "Hồ sơ", "dinh_nghia": "tài liệu."}]
    bang(m.lech_nguyen_van(kn, vb) == [], f"khoan mat so co diem a, b bi chan oan: {m.tach_khoan(vb)}")


def ca_bom_tieu_de(m):
    bang(m.so_dieu_tu_tieu_de("\ufeffĐiều 15. Giải thích từ ngữ") == "15", "BOM che tieu de Dieu (N3)")
    bang(m.tach_khoan("\ufeffĐiều 3.\nHồ sơ là tài liệu.") == [(None, "Hồ sơ là tài liệu.")], "BOM lam lech tach khoan")


def ca_sub_stop_reason_va_kieu(m):
    for gia in (run_sub_gia(stop_reason="refusal"), run_sub_gia(stop_reason="max_tokens", rc=1, is_error=True)):
        rc, _, nhat = chay_lenh(m, KEY, {"sub": sub(m, gia), "api": cam("api")})
        bang(rc == m.MA_DUNG, f"stop_reason tu choi/cat dau ra phai DUNG, khong goi api: rc={rc} {nhat}")
    for gia in (run_sub_gia(subtype=[]), run_sub_gia(usage=[{"inputTokens": 1}]), run_sub_gia(usage={"x": None})):
        try:
            rc, _, nhat = chay_lenh(m, {}, {"sub": sub(m, gia), "api": cam("api")})
        except (TypeError, AttributeError) as e:
            raise TinHieuChotCa(f"envelope sai kieu lam no {type(e).__name__}") from e
        bang(rc != 0, f"envelope sai kieu khong duoc NHAN: rc={rc} {nhat}")
    rc, _, nhat = chay_lenh(m, {}, {"sub": sub(m, run_sub_gia(usage={"claude-haiku-5-5": {"inputTokens": 0, "outputTokens": 0,
                                                                                        "canonicalModel": "claude-haiku-5-5"}})),
                                    "api": cam("api")})
    bang(rc == m.MA_DUNG, f"thanh cong ma 0 token khong chung minh model chay: rc={rc} {nhat}")


def ca_sub_xac_thuc_tai_khoan(m):
    for auth, rc_a in (({"loggedIn": True, "authMethod": "api_key", "apiProvider": "firstParty"}, 0),
                       ({"loggedIn": True, "authMethod": "api_key_helper", "apiProvider": "firstParty"}, 0),
                       ({"loggedIn": True, "authMethod": "third_party", "apiProvider": "bedrock"}, 0),
                       ({"loggedIn": True, "authMethod": "claude.ai", "apiProvider": "vertex"}, 0),
                       ({"loggedIn": False, "authMethod": "none", "apiProvider": "firstParty"}, 0),
                       (AUTH_SUB, 1)):
        goi = []
        try:
            m.duong_sub("he", "nd", {"type": "object"}, "claude-haiku-5-5", {},
                        chay=run_sub_gia(auth=auth, auth_rc=rc_a, nhat_ky=goi), tim=lambda t: "/usr/bin/claude")
        except m.ChuyenDuong:
            bang(not [c for c in goi if "-p" in c[0]], f"da goi model du xac thuc {auth} rc={rc_a}")
            continue
        raise TinHieuChotCa(f"xac thuc {auth} rc={rc_a} khong phai subscription ma van di sub")
    for auth in (AUTH_SUB, {"loggedIn": True, "authMethod": "oauth_token", "apiProvider": "firstParty"}):
        try:
            m.duong_sub("he", "nd", {"type": "object"}, "claude-haiku-5-5", {},
                        chay=run_sub_gia(auth=auth), tim=lambda t: "/usr/bin/claude")
        except m.ChuyenDuong as e:
            raise TinHieuChotCa(f"xac thuc subscription {auth} bi chan oan: {e}") from e


def ca_cap_co_ranh_gioi(m):
    goi = []

    def chay(dieu_sau_co):
        def _c(cmd, **k):
            goi.append(cmd)
            d = cmd[cmd.index("--dieu") + 1]
            if d in ("3", "3a"):
                return subprocess.CompletedProcess(cmd, 0, f"===== Điều {d} =====\n" + VAN_BAN,
                                                   "[tl] ⚠ độ dài chạm CAP export (~200k ký tự)\n")
            if dieu_sau_co:
                return subprocess.CompletedProcess(cmd, 0, f"===== Điều {d} =====\nĐiều {d}. X", "")
            return subprocess.CompletedProcess(cmd, 1, "", "khong tim thay")
        return _c
    vb, _ = m.lay_dieu_qua_extract("1/2025/QH15", "3", "/x/tl.py", chay=chay(True))
    bang(vb == VAN_BAN.strip() and goi[-1][goi[-1].index("--dieu") + 1] == "4", "Dieu da co Dieu 4 sau phai qua")
    for dieu_sau_co, dieu in ((False, "3"), (True, "3a")):
        try:
            m.lay_dieu_qua_extract("1/2025/QH15", dieu, "/x/tl.py", chay=chay(dieu_sau_co))
        except ValueError:
            continue
        raise TinHieuChotCa(f"CAP khong xac nhan duoc ranh gioi (dieu={dieu}) phai chan")


def ca_504_uu_tien_ma(m):
    bang(m.phan_loai_loi_api(LoiGia(504, "overloaded_error", "x")) is m.Dung, "504 kem overloaded_error phai DUNG (ma thang body)")
    bang(m.phan_loai_loi_api(LoiGia(500, "rate_limit_error", "x")) is m.Dung, "500 kem rate_limit_error phai DUNG")
    bang(m.phan_loai_loi_api(LoiGia(None, "overloaded_error", "x")) is m.ChuyenDuong, "khong ma: dung type")


CA = [ca_api_dat, ca_mac_dinh_sub_truoc, ca_uu_tien_bien_tl, ca_thieu_key_chuyen_sub, ca_het_credit_402_chuyen_sub,
      ca_400_khac_thi_dung, ca_ket_noi_chuyen_duong, ca_sub_loi_chuyen_api, ca_sub_go_key_va_cat_ngu_canh,
      ca_sub_sai_model_thi_dung, ca_het_duong, ca_tu_choi_thi_dung, ca_schema_sai_thi_dung,
      ca_lech_nguyen_van, ca_chuan_hoa_chu_la, ca_tach_sai_cho, ca_khong_in_key,
      ca_thu_tu, ca_thu_tu_hieu_luc_va_luu, ca_tep_hong_fail_closed, ca_lay_dieu_qua_extract,
      ca_dinh_nghia_bi_cat, ca_bo_khoan_va_mang_rong, ca_trao_so, ca_khoan_co_so_va_diem_dat,
      ca_sub_het_luot_schema_thi_dung, ca_sub_thieu_dau_duong_khong_nhan, ca_sub_dinh_tuyen_nha_cung_cap,
      ca_qua_tai_chuyen_duong, ca_co_rong_va_symlink_dut, ca_extract_cham_tran,
      ca_nguon_mo_ho_thi_khong_dat, ca_so_khoan_nguon_va_dang_so, ca_tach_tai_la_dau_tien, ca_khoan_mat_so_co_diem_dat,
      ca_bom_tieu_de, ca_sub_stop_reason_va_kieu, ca_sub_xac_thuc_tai_khoan, ca_cap_co_ranh_gioi, ca_504_uu_tien_ma]

# (tên, (chuỗi gốc, chuỗi thay), ca đích PHẢI đỏ bằng TinHieuChotCa)
DOT_BIEN = [
    ("402_khong_chuyen", ("MA_CHUYEN_DUONG = frozenset({401, 402, 403, 429, 503, 529})",
                          "MA_CHUYEN_DUONG = frozenset({401, 403, 429, 503, 529})"), "ca_het_credit_402_chuyen_sub"),
    ("529_khong_chuyen", ("MA_CHUYEN_DUONG = frozenset({401, 402, 403, 429, 503, 529})",
                          "MA_CHUYEN_DUONG = frozenset({401, 402, 403, 429, 503})"), "ca_qua_tai_chuyen_duong"),
    ("type_thang_ma", ("    if isinstance(ma, int) and not isinstance(ma, bool):\n        if ma in MA_CHUYEN_DUONG:",
                       "    if kieu in KIEU_CHUYEN_DUONG:\n        return ChuyenDuong\n    if isinstance(ma, int) and not isinstance(ma, bool):\n        if ma in MA_CHUYEN_DUONG:"),
     "ca_504_uu_tien_ma"),
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
    ("so_chuoi_con", ("_gon(cum) == _gon(khoan[i][1])", "_gon(cum) in _gon(khoan[i][1])"), "ca_dinh_nghia_bi_cat"),
    ("so_ca_nguon", ("_gon(cum) == _gon(khoan[i][1])", "_gon(cum) in _gon(van_ban)"), "ca_dinh_nghia_bi_cat"),
    ("bo_khoan_thieu", ("    lech.extend(so_cua[len(khai_niem):])\n", ""), "ca_bo_khoan_va_mang_rong"),
    ("bo_kiem_stt", ('k.get("stt") == so_cua[i] and ', ""), "ca_trao_so"),
    ("stt_theo_vi_tri", ("    so_cua = [so if so is not None else i + 1 for i, (so, _) in enumerate(khoan)]",
                         "    so_cua = [i + 1 for i, (so, _) in enumerate(khoan)]"), "ca_so_khoan_nguon_va_dang_so"),
    ("so_khoan_can_khoang_trang", ('_RE_SO_KHOAN = re.compile(r"^(?:(\\d+)\\s*[.)](?!\\d)|\\((\\d+)\\))\\s*")',
                                   '_RE_SO_KHOAN = re.compile(r"^(?:(\\d+)\\s*[.)](?!\\d)|\\((\\d+)\\))\\s+")'),
     "ca_so_khoan_nguon_va_dang_so"),
    ("nuot_dong_truoc_khoan_dau", ("        elif not khoan and ln.endswith(\":\"):\n            continue\n        else:\n            return None",
                                   "        elif not khoan and ln.endswith(\":\"):\n            continue\n        elif not khoan:\n            continue\n        else:\n            return None"),
     "ca_nguon_mo_ho_thi_khong_dat"),
    ("bo_kiem_la_trong_thuat_ngu", ("tn.strip() and not _RE_LA.search(tn)", "tn.strip()"), "ca_tach_tai_la_dau_tien"),
    ("diem_mo_khoan_moi", ("        if _RE_DIEM.match(ln):\n            if not khoan:\n                return None\n            khoan[-1][1] += \"\\n\" + ln\n        elif",
                           "        if False:\n            pass\n        elif"), "ca_khoan_mat_so_co_diem_dat"),
    ("bom_khong_go", ('    dong = next((ln for ln in str(van_ban).lstrip("\\ufeff").splitlines() if ln.strip()), "")',
                      '    dong = next((ln for ln in str(van_ban).splitlines() if ln.strip()), "")'), "ca_bom_tieu_de"),
    ("bo_stop_reason", ("if subtype in SUBTYPE_LOI_YEU_CAU or stop in STOP_REASON_LOI_YEU_CAU:",
                        "if subtype in SUBTYPE_LOI_YEU_CAU:"), "ca_sub_stop_reason_va_kieu"),
    ("nhan_0_token", ('    if u is None or not (u["input"] or u["output"]):\n        raise Dung(',
                      '    if False:\n        raise Dung('), "ca_sub_stop_reason_va_kieu"),
    ("loi_sau_chay_van_chuyen", ('        if u is not None and (u["input"] or u["output"]):\n            raise Dung(',
                                 '        if False:\n            raise Dung('), "ca_sub_thieu_dau_duong_khong_nhan"),
    ("bo_kiem_xac_thuc", ("    kiem_xac_thuc_sub(claude_bin, env, chay)\n", ""), "ca_sub_xac_thuc_tai_khoan"),
    ("cho_api_key_la_sub", ('AUTH_SUBSCRIPTION = frozenset({"claude.ai", "oauth_token"})',
                            'AUTH_SUBSCRIPTION = frozenset({"claude.ai", "oauth_token", "api_key"})'), "ca_sub_xac_thuc_tai_khoan"),
    ("bo_kiem_nha_cung_cap", ('phuong_thuc in AUTH_SUBSCRIPTION and nha_cc == "firstParty"',
                              'phuong_thuc in AUTH_SUBSCRIPTION'), "ca_sub_xac_thuc_tai_khoan"),
    ("cap_cho_qua_het", ("        if not (str(dieu).isdigit() and _co_dieu(so_hieu, str(int(dieu) + 1), tl_py, chay, them)):",
                         "        if False:"), "ca_cap_co_ranh_gioi"),
    ("schema_retries_chuyen_duong", ('SUBTYPE_LOI_YEU_CAU = frozenset({"error_max_structured_output_retries", ',
                                     'SUBTYPE_LOI_YEU_CAU = frozenset({'), "ca_sub_het_luot_schema_thi_dung"),
    ("nhan_khi_thieu_is_error", ('kq.get("is_error") is False', 'not kq.get("is_error")'),
     "ca_sub_thieu_dau_duong_khong_nhan"),
    ("nhan_khi_thieu_subtype", ('subtype == "success" and kq.get', 'subtype in ("success", None) and kq.get'),
     "ca_sub_thieu_dau_duong_khong_nhan"),
    ("bo_kiem_dinh_tuyen", ("    kiem_dinh_tuyen_sub(env)\n", ""), "ca_sub_dinh_tuyen_nha_cung_cap"),
    ("dinh_tuyen_theo_ten", ('if k.upper().startswith("CLAUDE_CODE_USE_") and k.upper() not in CO_CLAUDE_CODE_VO_HAI and _bat(v)',
                             'if k in ("CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX") and _bat(v)'),
     "ca_sub_dinh_tuyen_nha_cung_cap"),
    ("chan_ca_co_vo_hai", ('and k.upper() not in CO_CLAUDE_CODE_VO_HAI and _bat(v)', 'and _bat(v)'),
     "ca_sub_dinh_tuyen_nha_cung_cap"),
    ("cho_phep_qua_rong", ('CO_CLAUDE_CODE_VO_HAI = frozenset({"CLAUDE_CODE_USE_CCR_V2", ',
                           'CO_CLAUDE_CODE_VO_HAI = frozenset({"CLAUDE_CODE_USE_TUONG_LAI_CHUA_BIET", "CLAUDE_CODE_USE_CCR_V2", '),
     "ca_sub_dinh_tuyen_nha_cung_cap"),
    ("base_url_khong_kiem_host", ("        if host != HOST_API_ANTHROPIC:", "        if False:"),
     "ca_sub_dinh_tuyen_nha_cung_cap"),
    ("uu_tien_bien_chuan", ('BIEN_KEY = ("TL_ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY")',
                            'BIEN_KEY = ("ANTHROPIC_API_KEY", "TL_ANTHROPIC_API_KEY")'), "ca_uu_tien_bien_tl"),
    ("mac_dinh_api_truoc", ('THU_TU_MAC_DINH = ("sub", "api")', 'THU_TU_MAC_DINH = ("api", "sub")'),
     "ca_mac_dinh_sub_truoc"),
    ("bien_thang_tep", ("    if tep.exists() or tep.is_symlink():\n        try:",
                        "    if (tep.exists() or tep.is_symlink()) and not env.get(BIEN_THU_TU):\n        try:"),
     "ca_thu_tu_hieu_luc_va_luu"),
    ("co_rong_la_vang", ("    if cli is not None:\n", "    if cli:\n"), "ca_co_rong_va_symlink_dut"),
    ("symlink_dut_la_khong_co", ("    if tep.exists() or tep.is_symlink():\n        try:", "    if tep.exists():\n        try:"),
     "ca_co_rong_va_symlink_dut"),
    ("bo_chot_cap", ("    if MAU_CAP_EXTRACT in (p.stderr or \"\"):\n", "    if False:\n"), "ca_extract_cham_tran"),
    ("bo_kiem_rc_sub", ('if not (p.returncode == 0 and subtype == "success"', 'if not (subtype == "success"'),
     "ca_sub_thieu_dau_duong_khong_nhan"),
    ("doc_settings_nguoi_dung", ('"--setting-sources", "",', '"--setting-sources", "user",'),
     "ca_sub_go_key_va_cat_ngu_canh"),
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
