#!/usr/bin/env python3
"""tl_core.llm_route — gọi Claude cho trích xuất có cấu trúc, tự chọn đường SUBSCRIPTION ↔ API key.

Module THUẦN (không bind vào namespace tl, không đọc global tl). Lệnh: `tl llm-order`, `tl llm-khai-niem`
(handler ở `ops_misc.py`). Hai đường; thứ tự hiệu lực theo `thu_tu_hieu_luc`:
cờ `--thu-tu` > tệp đã lưu bằng `tl llm-order` > biến `TL_LLM_ORDER` > mặc định `sub,api`.

  sub  `claude -p` (Claude Code không tương tác) — tính vào SUBSCRIPTION. Đường hợp lệ DUY NHẤT để
       script dùng gói; KHÔNG lấy token OAuth của Claude Code đi gọi API thẳng.
  api  Claude API bằng SDK `anthropic`, key đọc từ `TL_ANTHROPIC_API_KEY` rồi mới tới
       `ANTHROPIC_API_KEY`. Tên riêng `TL_` vì phiên Claude Code trên web BỎ QUA `ANTHROPIC_API_KEY`
       khi xác thực (đo 24-11-2026), còn Network secrets KHÔNG lưu được cho host của Anthropic.

CHUYỂN ĐƯỜNG chỉ khi lỗi thuộc về ĐƯỜNG (thiếu key/SDK/CLI, 401, 403, 402 hết credit, 429, mất kết
nối, `claude -p` báo lỗi — thường là chạm hạn mức gói). Lỗi thuộc về YÊU CẦU (400 khác, model từ
chối, cắt `max_tokens`, sai model, đầu ra sai schema) thì DỪNG: chạy lại ở đường kia chỉ tiêu tiền
lần hai cho cùng một lỗi.

Đo 24-11-2026 trong phiên remote: `claude -p` trần nạp nguyên system prompt + bộ tool của Claude
Code (~92k token vào hạn mức gói cho một câu hỏi một dòng); thêm `--tools "" --strict-mcp-config
--setting-sources "" --disable-slash-commands --system-prompt …` còn ~1,9k. KHÔNG dùng `--bare`:
chế độ ấy chỉ nhận API key, tức lặng lẽ biến đường `sub` thành đường `api`.

Mã thoát: 0 đạt · 2 sai đối số/đầu vào · 3 HẾT ĐƯỜNG · 4 DỪNG (lỗi phía yêu cầu) · 5 đầu ra KHÔNG
khớp nguyên văn nguồn. KHÔNG BAO GIỜ in giá trị key.
"""
from __future__ import annotations

import contextlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse

MODEL_MAC_DINH = "claude-haiku-5-5"
DUONG_HOP_LE = ("api", "sub")
BIEN_KEY = ("TL_ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY")
# Biến khiến `claude` CLI xác thực bằng API thay vì gói — gỡ khỏi env của con ở đường `sub`,
# kẻo trên máy cá nhân "sub" lặng lẽ tính tiền vào API key.
BIEN_GO_KHOI_SUB = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "TL_ANTHROPIC_API_KEY")
TIMEOUT_SUB_GIAY = 300
# Subtype kết quả của `claude -p` nghĩa là MODEL ĐÃ CHẠY mà yêu cầu không đạt — lỗi phía YÊU CẦU,
# chạy lại ở đường `api` chỉ tốn credit lần hai (cross-review PR #1503 F2). Tên đo trong CLI đã cài
# 24-11-2026; subtype lạ ⇒ không phải `success` ⇒ chuyển đường (fail-closed cho việc NHẬN kết quả).
SUBTYPE_LOI_YEU_CAU = frozenset({"error_max_structured_output_retries", "error_max_turns",
                                 "error_max_budget_usd"})
HOST_API_ANTHROPIC = "api.anthropic.com"
MA_CHUYEN_DUONG = frozenset({401, 402, 403, 429, 503, 529})
KIEU_CHUYEN_DUONG = frozenset({"authentication_error", "billing_error", "permission_error", "rate_limit_error",
                               "overloaded_error"})
# `claude auth status --json` (đo trong binary 2.1.331): authMethod ∈ {none, third_party, claude.ai,
# api_key_helper, oauth_token, api_key}. CHỈ hai giá trị dưới là xác thực bằng tài khoản Anthropic (gói);
# `api_key`/`api_key_helper` là API key, `third_party` là Bedrock/Vertex/Foundry (cross-review lượt 2 N4).
AUTH_SUBSCRIPTION = frozenset({"claude.ai", "oauth_token"})
STOP_REASON_LOI_YEU_CAU = frozenset({"refusal", "max_tokens"})
# DANH SÁCH CHO PHÉP các cờ `CLAUDE_CODE_USE_*` KHÔNG đổi nhà cung cấp. Mọi tên `CLAUDE_CODE_USE_*` khác
# đang bật ⇒ từ chối đường `sub` (fail-closed, kể cả tên CLI tương lai thêm vào). Đo trên Claude Code
# 2.1.331 (24-11-2026, quét chuỗi trong binary): 11 tên; 7 là nhà cung cấp/gateway (GATEWAY, BEDROCK,
# VERTEX, ANTHROPIC_AWS, MANTLE, FOUNDRY, ANTHROPIC_GOOGLE_CLOUD), 4 là cờ tính năng dưới đây. Bản vá F3
# đầu tiên chặn theo TIỀN TỐ và chặn oan `CLAUDE_CODE_USE_CCR_V2` — cờ của chính phiên Claude Code trên
# web — lộ ra ở lần chạy thật, không phải ở ca test.
CO_CLAUDE_CODE_VO_HAI = frozenset({"CLAUDE_CODE_USE_CCR_V2", "CLAUDE_CODE_USE_POWERSHELL_TOOL",
                                   "CLAUDE_CODE_USE_COWORK_PLUGINS", "CLAUDE_CODE_USE_NATIVE_FILE_SEARCH"})
MAU_CAP_EXTRACT = "độ dài chạm CAP export"   # dấu riêng của cảnh báo trần trong `tl_core/extract_cache.py`
_RE_TIEU_DE_DIEU = re.compile(r"^\s*Điều\s+(\d+[a-zđ]?)\b")


def so_dieu_tu_tieu_de(van_ban):
    """Số Điều đọc từ dòng đầu (`Điều 15. …`), hoặc None nếu dòng đầu không phải tiêu đề Điều."""
    dong = next((ln for ln in str(van_ban).lstrip("\ufeff").splitlines() if ln.strip()), "")
    m = _RE_TIEU_DE_DIEU.match(dong)
    return m.group(1) if m else None

MA_OK, MA_DOI_SO, MA_HET_DUONG, MA_DUNG, MA_LECH_NGUYEN_VAN = 0, 2, 3, 4, 5


class ChuyenDuong(Exception):
    """Lỗi thuộc về ĐƯỜNG — thử đường kế tiếp."""


class Dung(Exception):
    """Lỗi thuộc về YÊU CẦU — không thử đường khác."""


class HetDuong(Exception):
    def __init__(self, lan_thu):
        self.lan_thu = lan_thu
        super().__init__("; ".join(f"{d}: {l}" for d, l in lan_thu))


THU_TU_MAC_DINH = ("sub", "api")
BIEN_THU_TU = "TL_LLM_ORDER"
BIEN_TEP_THU_TU = "TL_LLM_ORDER_FILE"


def doc_thu_tu(gia_tri: str | None) -> tuple[str, ...]:
    tho = (",".join(THU_TU_MAC_DINH) if gia_tri is None else gia_tri).replace(" ", "")
    ds = tuple(x for x in tho.split(",") if x)
    if not ds or any(x not in DUONG_HOP_LE for x in ds) or len(set(ds)) != len(ds):
        raise ValueError(f"thu tu duong khong hop le: {gia_tri!r} (chi nhan api,sub — khong trung)")
    return ds


def lay_key(env) -> tuple[str | None, str | None]:
    for ten in BIEN_KEY:
        v = (env.get(ten) or "").strip()
        if v:
            return ten, v
    return None, None


# ----------------------------------------------------------------- đường api

def phan_loai_loi_api(e: BaseException) -> type[Exception]:
    """Trả `ChuyenDuong` hoặc `Dung`. Đọc thuộc tính, KHÔNG `isinstance` lớp SDK — để
    phân loại chạy được (và test được) khi chưa cài `anthropic`."""
    ten = type(e).__name__
    if ten in ("APIConnectionError", "APITimeoutError"):
        return ChuyenDuong
    ma = getattr(e, "status_code", None)
    kieu = getattr(e, "type", None)
    if not isinstance(kieu, str):
        kieu = None
    thong_bao = str(getattr(e, "message", "") or e).lower()
    # MÃ HTTP QUYẾT TRƯỚC, `type` trong body chỉ dùng khi KHÔNG có mã (cross-review lượt 2 N7: 504 kèm
    # `overloaded_error` từng lọt sang `sub` vì nhánh `type` thắng mã). 503/529 = dịch vụ quá tải/không
    # khả dụng — lỗi phía ĐƯỜNG (lượt 1 F7, đo bằng SDK 2.13.0 + transport giả). 500/504 có thể là yêu cầu
    # ĐÃ được xử lý (tính tiền) ⇒ DỪNG, bất kể body nói gì.
    if isinstance(ma, int) and not isinstance(ma, bool):
        if ma in MA_CHUYEN_DUONG:
            return ChuyenDuong
        # Hết credit từng được trả bằng 400 kèm câu "credit balance is too low" — chỉ chuỗi ẤY mới
        # chuyển đường; mọi 400 khác là lỗi của yêu cầu.
        if ma == 400 and "credit balance" in thong_bao:
            return ChuyenDuong
        return Dung
    if kieu in KIEU_CHUYEN_DUONG:
        return ChuyenDuong
    return Dung


def _tao_client_mac_dinh(api_key):
    try:
        import anthropic  # noqa: PLC0415 — nạp muộn: đường sub không cần SDK
    except ImportError as e:
        raise ChuyenDuong("thieu SDK anthropic (pip install anthropic)") from e
    return anthropic.Anthropic(api_key=api_key)


def duong_api(he_thong, noi_dung, schema, model, env, tao_client=_tao_client_mac_dinh):
    ten_bien, key = lay_key(env)
    if not key:
        raise ChuyenDuong("khong co " + " / ".join(BIEN_KEY))
    client = tao_client(key)
    try:
        resp = client.messages.create(
            model=model, max_tokens=8192, system=he_thong,
            output_config={"effort": "low", "format": {"type": "json_schema", "schema": schema}},
            messages=[{"role": "user", "content": noi_dung}],
        )
    except ChuyenDuong:
        raise
    except Exception as e:  # noqa: BLE001 — phân loại ngay dưới, không nuốt
        lop = phan_loai_loi_api(e)
        ma = getattr(e, "status_code", None)
        raise lop(f"{type(e).__name__}" + (f" HTTP {ma}" if ma else "")) from e
    if resp.stop_reason == "refusal":
        raise Dung(f"model tu choi: {getattr(resp, 'stop_details', None)}")
    if resp.stop_reason == "max_tokens":
        raise Dung("dau ra bi cat (max_tokens)")
    if resp.model != model:
        raise Dung(f"model da chay {resp.model!r} khac model yeu cau {model!r}")
    van_ban = next((b.text for b in resp.content if getattr(b, "type", "") == "text"), None)
    if van_ban is None:
        raise Dung("phan hoi khong co khoi text")
    try:
        data = json.loads(van_ban)
    except json.JSONDecodeError as e:
        raise Dung(f"dau ra khong phai JSON: {e}") from e
    u = resp.usage
    return {
        "duong": "api", "nguon_key": ten_bien, "model": resp.model, "data": data,
        "usage": {"input": u.input_tokens, "output": u.output_tokens,
                  "cache_doc": getattr(u, "cache_read_input_tokens", 0) or 0,
                  "cache_ghi": getattr(u, "cache_creation_input_tokens", 0) or 0},
        "usd_uoc_tinh": None,
    }


# ----------------------------------------------------------------- đường sub

def lenh_sub(claude_bin, he_thong, noi_dung, schema, model):
    return [claude_bin, "-p", "--model", model, "--output-format", "json",
            "--no-session-persistence", "--tools", "", "--strict-mcp-config",
            "--setting-sources", "", "--disable-slash-commands",
            "--system-prompt", he_thong, "--json-schema", json.dumps(schema, ensure_ascii=False),
            noi_dung]


def env_cho_sub(env):
    return {k: v for k, v in env.items() if k not in BIEN_GO_KHOI_SUB}


def _bat(v) -> bool:
    return str(v or "").strip().lower() not in ("", "0", "false", "no", "off")


def kiem_dinh_tuyen_sub(env) -> None:
    """Đường `sub` chỉ được báo là SUBSCRIPTION khi Claude Code KHÔNG bị định tuyến sang nhà cung
    cấp khác (cross-review PR #1503 F3: `CLAUDE_CODE_USE_BEDROCK=1` lọt vào tiến trình con, CLI vẫn
    in "subscription"). Mọi `CLAUDE_CODE_USE_*` đang bật mà KHÔNG nằm trong danh sách CHO PHÉP
    `CO_CLAUDE_CODE_VO_HAI` đều bị từ chối — danh sách cấm theo tên luôn thiếu (CLAUDE.md: "đảo thành danh
    sách CHO PHÉP"); và `ANTHROPIC_BASE_URL`
    chỉ được trỏ đúng host của Anthropic. Cấu hình trong tệp settings bị cắt bằng
    `--setting-sources ""`; managed settings của tổ chức thì KHÔNG cắt được — khai, không giả vờ."""
    co = sorted(k for k, v in env.items()
                if k.upper().startswith("CLAUDE_CODE_USE_") and k.upper() not in CO_CLAUDE_CODE_VO_HAI and _bat(v))
    if co:
        raise ChuyenDuong("Claude Code dang bi dinh tuyen sang nha cung cap khac (" + ", ".join(co)
                          + ") — khong bao dam tinh vao subscription")
    goc = (env.get("ANTHROPIC_BASE_URL") or "").strip()
    if goc:
        try:
            host = urlparse(goc).hostname
        except ValueError:
            host = None
        if host != HOST_API_ANTHROPIC:
            raise ChuyenDuong(f"ANTHROPIC_BASE_URL tro toi host {host!r} — khong bao dam tinh vao subscription")


def _so_khong_am(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


_KHOA_MU = {"input": "inputTokens", "output": "outputTokens", "cache_doc": "cacheReadInputTokens",
            "cache_ghi": "cacheCreationInputTokens"}
_KHOA_USAGE = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")


def _usage_sub(mu):
    """Tổng token từ `modelUsage` nếu ĐÚNG KIỂU, ngược lại None. Đòi `inputTokens` và `outputTokens` CÓ MẶT
    (không bù 0 cho trường thiếu — lượt 3 M2); trường cache vắng được tính 0 nhưng có mặt thì phải đúng kiểu."""
    if not isinstance(mu, dict) or not mu or not all(isinstance(v, dict) for v in mu.values()):
        return None
    tong = {"input": 0, "output": 0, "cache_doc": 0, "cache_ghi": 0}
    for v in mu.values():
        if "inputTokens" not in v or "outputTokens" not in v:
            return None
        for dich, nguon in _KHOA_MU.items():
            x = v.get(nguon, 0)
            if not _so_khong_am(x):
                return None
            tong[dich] += x
    return tong


def _dau_model_da_chay(kq):
    """Bằng chứng model ĐÃ chạy trong envelope lỗi: True (có token dương ở BẤT KỲ đâu — kể cả token cache, kể
    cả khối `usage` tổng), False (mọi số đo có mặt đều đúng kiểu và bằng 0, hoặc không có số đo nào), None (có
    số đo SAI KIỂU ⇒ không biết). Cross-review lượt 3 M2: chỉ xét input/output của `modelUsage` thì envelope
    chỉ có token cache, hay chỉ có `usage` tổng, từng bị coi là "chưa chạy" rồi gọi tiếp API."""
    thay = []
    mu = kq.get("modelUsage")
    if mu is not None:
        if not isinstance(mu, dict) or not all(isinstance(v, dict) for v in mu.values()):
            return None
        for v in mu.values():
            thay += [v[k] for k in _KHOA_MU.values() if k in v]
    us = kq.get("usage")
    if us is not None:
        if not isinstance(us, dict):
            return None
        thay += [us[k] for k in _KHOA_USAGE if k in us]
    if not all(_so_khong_am(x) for x in thay):
        return None
    return any(x > 0 for x in thay)


def kiem_xac_thuc_sub(claude_bin, env, chay=subprocess.run) -> None:
    """Đường `sub` CHỈ được báo là subscription khi CLI tự khai xác thực bằng TÀI KHOẢN Anthropic
    (`authMethod` ∈ AUTH_SUBSCRIPTION) qua nhà cung cấp `firstParty`, đo bằng `claude auth status --json`
    với ĐÚNG env mà lời gọi model sẽ dùng (cross-review lượt 2 N4: key lưu từ `/login`, `apiKeyHelper` trong
    policy… đều nằm ngoài ba biến bị gỡ). Không đo được ⇒ ChuyenDuong. Giới hạn đã khai: tín hiệu này
    KHÔNG phân biệt hạn mức gói với "extra usage" mà tài khoản tự bật."""
    try:
        with tempfile.TemporaryDirectory(prefix="llm-route-auth-") as cwd:
            # `--setting-sources ""` GIỐNG lời gọi model (`lenh_sub`): đo không cùng nguồn settings thì đo một cấu hình
            # KHÁC cấu hình sẽ chạy (cross-review lượt 3 M3: settings người dùng định tuyến Bedrock làm `auth status` trần
            # khai `third_party`, còn lượt `-p` thì không nạp nó).
            p = chay([claude_bin, "--setting-sources", "", "auth", "status", "--json"], stdin=subprocess.DEVNULL,
                     capture_output=True,
                     text=True, encoding="utf-8", errors="replace", timeout=60, env=env_cho_sub(env), cwd=cwd)
        tt = json.loads(p.stdout or "null") if p.returncode == 0 else None
    except (OSError, subprocess.SubprocessError, ValueError) as e:
        raise ChuyenDuong(f"khong do duoc nguon xac thuc cua claude CLI ({type(e).__name__})") from e
    if not isinstance(tt, dict):
        raise ChuyenDuong(f"khong do duoc nguon xac thuc cua claude CLI (rc={p.returncode})")
    phuong_thuc, nha_cc = tt.get("authMethod"), tt.get("apiProvider")
    # Kiểm KIỂU trước phép tra tập (lượt 3 M3: `authMethod=[]` từng ném TypeError).
    if not (tt.get("loggedIn") is True and isinstance(phuong_thuc, str) and phuong_thuc in AUTH_SUBSCRIPTION
            and nha_cc == "firstParty"):
        raise ChuyenDuong(f"claude CLI xac thuc bang authMethod={phuong_thuc!r} apiProvider={nha_cc!r} — "
                          "khong phai tai khoan subscription")


def duong_sub(he_thong, noi_dung, schema, model, env, chay=subprocess.run, tim=shutil.which):
    claude_bin = tim("claude")
    if not claude_bin:
        raise ChuyenDuong("khong co claude CLI tren PATH")
    kiem_dinh_tuyen_sub(env)
    kiem_xac_thuc_sub(claude_bin, env, chay)
    try:
        # stdin=DEVNULL: không có thì `claude -p` chèn dòng "no stdin data received" TRƯỚC
        # JSON (đo 06-09-2026, CLAUDE.md §Gọi agent đa nền). cwd tạm: tránh nạp ngữ cảnh kho.
        with tempfile.TemporaryDirectory(prefix="llm-route-") as cwd:
            p = chay(lenh_sub(claude_bin, he_thong, noi_dung, schema, model),
                     stdin=subprocess.DEVNULL, capture_output=True, text=True,
                     encoding="utf-8", errors="replace", timeout=TIMEOUT_SUB_GIAY,
                     env=env_cho_sub(env), cwd=cwd)
    except subprocess.TimeoutExpired as e:
        raise ChuyenDuong(f"claude -p qua han {TIMEOUT_SUB_GIAY}s") from e
    except OSError as e:
        raise ChuyenDuong(f"khong chay duoc claude: {type(e).__name__}") from e
    tho = p.stdout or ""
    i = tho.find("{")
    try:
        kq = json.loads(tho[i:]) if i >= 0 else None
    except json.JSONDecodeError:
        kq = None
    # Giải mã envelope MỘT lần, KIỂM KIỂU trước mọi phép tra (lượt 2 N2: `subtype=[]` từng ném TypeError,
    # `modelUsage` dạng mảng ném AttributeError).
    if not isinstance(kq, dict):
        raise ChuyenDuong(f"claude -p rc={p.returncode}: khong co envelope JSON ({(p.stderr or tho).strip()[:160]})")
    subtype = kq.get("subtype") if isinstance(kq.get("subtype"), str) else None
    stop = kq.get("stop_reason") if isinstance(kq.get("stop_reason"), str) else None
    u = _usage_sub(kq.get("modelUsage"))
    # Lỗi phía YÊU CẦU ⇒ DỪNG: subtype đã biết, hoặc lý do kết thúc là từ chối/cắt đầu ra — kể cả khi
    # envelope tự xưng `success` (lượt 2 N2).
    if subtype in SUBTYPE_LOI_YEU_CAU or stop in STOP_REASON_LOI_YEU_CAU:
        raise Dung(f"claude -p subtype={subtype} stop_reason={stop} (loi phia yeu cau — khong chuyen duong)")
    # NHẬN chỉ khi đủ BA dấu dương: rc 0, `subtype == "success"`, `is_error` đúng là False (lượt 1 F2).
    if not (p.returncode == 0 and subtype == "success" and kq.get("is_error") is False):
        mo_ta = str(kq.get("result") or "").strip()[:160]
        # Envelope lỗi mà model ĐÃ CHẠY (có token ở bất kỳ trường nào) hoặc KHÔNG BIẾT (số đo sai kiểu) ⇒ gọi lại ở
        # `api` có thể tiêu tiền lần hai cho cùng việc: DỪNG. Chỉ khi mọi số đo sạch và bằng 0 (hạn mức, xác thực,
        # khởi động) mới chuyển đường. `error_during_execution` dùng cho CẢ hai ca (lượt 2 N2) ⇒ phân bằng phép đo.
        dau = _dau_model_da_chay(kq)
        if dau is not False:
            ly_do = "sau khi model da chay" if dau else "so do token sai kieu — khong biet model da chay chua"
            raise Dung(f"claude -p rc={p.returncode} subtype={subtype} {ly_do}: {mo_ta}")
        raise ChuyenDuong(f"claude -p rc={p.returncode} subtype={subtype}: {mo_ta}")
    mu = kq.get("modelUsage")
    da_chay = {(v.get("canonicalModel") if isinstance(v.get("canonicalModel"), str) else k)
               for k, v in mu.items()} if isinstance(mu, dict) and all(isinstance(v, dict) for v in mu.values()) else None
    if da_chay != {model}:
        raise Dung(f"model da chay {sorted(da_chay) if da_chay else da_chay} khac model yeu cau {model!r}")
    if u is None or not (u["input"] or u["output"]):
        raise Dung("claude -p thanh cong nhung khong co so do token — khong chung minh model da chay")
    data = kq.get("structured_output")
    if data is None:
        raise Dung("claude -p khong tra structured_output")
    return {
        "duong": "sub", "nguon_key": None, "model": model, "data": data,
        "usage": u,
        # Số CLI tự ước theo giá API; với gói nó là thước đo hạn mức, không phải hoá đơn.
        "usd_uoc_tinh": kq.get("total_cost_usd"),
    }


# ----------------------------------------------------------------- điều phối

def goi(he_thong, noi_dung, schema, model=MODEL_MAC_DINH, thu_tu=THU_TU_MAC_DINH, env=None,
        cac_duong=None):
    env = dict(os.environ if env is None else env)
    cac_duong = cac_duong or {"api": duong_api, "sub": duong_sub}
    lan_thu = []
    for d in thu_tu:
        try:
            kq = cac_duong[d](he_thong, noi_dung, schema, model, env)
        except ChuyenDuong as e:
            lan_thu.append((d, str(e)))
            continue
        kq["lan_thu"] = lan_thu
        return kq
    raise HetDuong(lan_thu)


def kiem_schema(data, schema, duong="$"):
    """Kiểm tối thiểu (object/array/string/integer, required, additionalProperties=false)."""
    t = schema.get("type")
    if t == "object":
        if not isinstance(data, dict):
            raise Dung(f"{duong}: can object")
        thieu = [k for k in schema.get("required", []) if k not in data]
        if thieu:
            raise Dung(f"{duong}: thieu khoa {thieu}")
        if schema.get("additionalProperties") is False:
            la = sorted(set(data) - set(schema.get("properties", {})))
            if la:
                raise Dung(f"{duong}: khoa la {la}")
        for k, con in schema.get("properties", {}).items():
            if k in data:
                kiem_schema(data[k], con, f"{duong}.{k}")
    elif t == "array":
        if not isinstance(data, list):
            raise Dung(f"{duong}: can array")
        for i, x in enumerate(data):
            kiem_schema(x, schema.get("items", {}), f"{duong}[{i}]")
    elif t == "string" and not isinstance(data, str):
        raise Dung(f"{duong}: can string")
    elif t == "integer" and (not isinstance(data, int) or isinstance(data, bool)):
        raise Dung(f"{duong}: can integer")


def ghi_nhat_ky(tep, kq, tac_vu):
    dong = {"thoi_diem": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "tac_vu": tac_vu,
            "duong": kq["duong"], "model": kq["model"], **kq["usage"],
            "usd_uoc_tinh": kq["usd_uoc_tinh"], "lan_thu": kq["lan_thu"]}
    with open(tep, "a", encoding="utf-8") as f:
        f.write(json.dumps(dong, ensure_ascii=False) + "\n")


# ----------------------------------------------------------------- tác vụ: tách khái niệm

SCHEMA_KHAI_NIEM = {
    "type": "object",
    "properties": {
        "khai_niem": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"stt": {"type": "integer"}, "thuat_ngu": {"type": "string"},
                               "dinh_nghia": {"type": "string"}},
                "required": ["stt", "thuat_ngu", "dinh_nghia"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["khai_niem"],
    "additionalProperties": False,
}

HE_THONG_KHAI_NIEM = (
    "Bạn tách các khái niệm trong điều khoản 'Giải thích từ ngữ' của văn bản quy phạm pháp luật Việt Nam. "
    "Mỗi khoản giải thích một thuật ngữ, có dạng '<thuật ngữ> là <định nghĩa>'. "
    "Với mỗi khoản: 'thuat_ngu' là phần đứng trước chữ 'là' đầu tiên NẰM NGOÀI ngoặc tròn (chữ 'là' trong "
    "'(sau đây gọi là …)' không tính); 'dinh_nghia' là phần sau chữ 'là' đó, chép NGUYÊN VĂN từng ký tự (giữ dấu "
    "câu, kể cả dấu chấm cuối, giữ xuống dòng của các điểm a), b)), "
    "không diễn giải, không sửa chính tả. 'stt' là SỐ khoản như trong văn bản (khoản không đánh số thì đếm từ 1). "
    "Bỏ qua dòng tiêu đề Điều và câu dẫn 'Trong ..., các từ ngữ dưới đây được hiểu như sau'."
)


def chuan_hoa_khai_niem(khai_niem):
    """Bỏ chữ "là " thừa ở đầu định nghĩa. Đo 24-11-2026: cùng prompt, đường `api` cắt
    đúng sau "là" còn đường `sub` giữ "là …" — cả hai đều qua phép kiểm chuỗi con cũ,
    nên HAI ĐƯỜNG cho HAI KẾT QUẢ mà không ai báo. Ranh giới tách do MÃ quyết, không do model."""
    for k in khai_niem:
        k["thuat_ngu"] = k["thuat_ngu"].strip()
        k["dinh_nghia"] = k["dinh_nghia"].strip()
        if k["dinh_nghia"].startswith("là "):
            k["dinh_nghia"] = k["dinh_nghia"][3:].lstrip()
    return khai_niem


# Số khoản: `1.` `1)` `1.Hồ sơ` (dính thân) hoặc `(1)`; `(?!\d)` để "1.5 triệu" không bị đọc thành khoản 1.
_RE_SO_KHOAN = re.compile(r"^(?:(\d+)\s*[.)](?!\d)|\((\d+)\))\s*")
_RE_DIEU = re.compile(r"^Điều\s+\d+")
_RE_DIEM = re.compile(r"^([a-zđ]\)|[-–•+])\s*")
_RE_LA = re.compile(r"(?:^|\s)là(?:\s|$)")


def tach_khoan(van_ban):
    """Các khoản của một Điều "Giải thích từ ngữ": danh sách `(số_nguồn | None, văn bản đã gỡ số)`, theo thứ
    tự nguồn; `None` khi KHÔNG xác định được ranh giới (fail-closed — cross-review lượt 2 N1).

    - Bỏ BOM, dòng tiêu đề `Điều N.` và câu dẫn (dòng kết thúc `:` không chứa chữ "là") đứng TRƯỚC khoản
      đầu. Bất kỳ dòng nào khác trước khoản đầu ⇒ None: nó có thể là thân của khoản đầu bị bỏ (N1 đo được
      khoản "X là" xuống dòng bị nuốt mất rồi vẫn báo đạt).
    - Nguồn CÓ số thứ tự ⇒ chỉ dòng mang số mở khoản; dòng khác nối vào khoản trước; số nguồn được giữ để
      đối chiếu `stt` (nguồn đánh `1.` rồi `4.` thì `stt` phải là 4, không phải 2).
    - Nguồn MẤT số (Google Doc rơi số tự động — Điều 3 Luật 134/2025/QH15): dòng có chữ "là" mở khoản; dòng
      điểm (`a)`, `-`) nối vào khoản trước; dòng KHÔNG có "là" và không phải điểm ⇒ None (không phân biệt
      được tiếp dòng với khoản dùng từ nối khác — để người dùng đưa nguồn có số)."""
    dong = [ln.strip() for ln in str(van_ban).lstrip("\ufeff").splitlines() if ln.strip()]
    if dong and _RE_DIEU.match(dong[0]):
        dong = dong[1:]
    co_so = any(_RE_SO_KHOAN.match(ln) for ln in dong)
    khoan: list[list] = []
    for ln in dong:
        m = _RE_SO_KHOAN.match(ln)
        if co_so:
            if m:
                khoan.append([int(m.group(1) or m.group(2)), ln[m.end():]])
            elif khoan and (_RE_DIEM.match(ln) or not _la_ngoai_ngoac(ln)):
                khoan[-1][1] += "\n" + ln
            elif khoan:
                # Nguồn CÓ số mà dòng không số lại mở bằng "<X> là …": có thể là một khoản MẤT số (lượt 3 M1: khoản 4
                # mất số bị gộp vào khoản 3 rồi vẫn báo đạt) ⇒ mơ hồ, fail-closed.
                return None
            elif ln.endswith(":") and not _RE_LA.search(ln):
                continue
            else:
                return None
            continue
        if _RE_DIEM.match(ln):
            if not khoan:
                return None
            khoan[-1][1] += "\n" + ln
        elif _RE_LA.search(ln):
            khoan.append([None, ln])
        elif not khoan and ln.endswith(":"):
            continue
        else:
            return None
    return [(so, txt) for so, txt in khoan]


def _gon(s) -> str:
    return " ".join(str(s).split())


def _la_ngoai_ngoac(txt):
    """Match của chữ "là" ĐẦU TIÊN nằm NGOÀI mọi cặp ngoặc tròn, hoặc None. Lượt 3 M1: khoản có tên gọi tắt
    `X (sau đây gọi là Y) là …` — chữ "là" trong ngoặc KHÔNG phải từ nối định nghĩa."""
    for m in _RE_LA.finditer(txt):
        truoc = txt[:m.start()]
        if truoc.count("(") <= truoc.count(")"):
            return m
    return None


def lech_nguyen_van(khai_niem, van_ban):
    """Các `stt` sai so với nguồn. So TRỌN KHOẢN (khoảng trắng gộp), không so chuỗi con (lượt 1 F1: định nghĩa
    bị cắt, thiếu khoản, tráo số đều từng lọt). Mục thứ i phải: `stt` = số của khoản thứ i trong nguồn (hoặc
    i+1 khi nguồn mất số); thuật ngữ KHÔNG chứa chữ "là" (tách tại chữ "là" ĐẦU TIÊN — lượt 2 N1); và cụm
    `<thuật ngữ> là <định nghĩa>` bằng đúng khoản ấy. Khoản nguồn không có mục tương ứng cũng là lệch.
    Nguồn không xác định được ranh giới khoản ⇒ `[0]` (không xác minh được ⇒ không dùng)."""
    khoan = tach_khoan(van_ban)
    if not khoan:
        return [0]
    so_cua = [so if so is not None else i + 1 for i, (so, _) in enumerate(khoan)]
    lech = []
    for i, k in enumerate(khai_niem):
        tn, dn = _gon(k.get("thuat_ngu", "")), _gon(k.get("dinh_nghia", ""))
        dung = False
        if i < len(khoan) and k.get("stt") == so_cua[i]:
            # So THEO VỊ TRÍ ranh giới trong nguồn (lượt 3 M1), không so chuỗi ghép: thuật ngữ = phần trước chữ "là"
            # đầu tiên NGOÀI ngoặc; định nghĩa = phần sau nó. Khoản không có từ nối "là" ngoài ngoặc (vd "bao gồm")
            # ⇒ không xác minh được ⇒ lệch (chặn, không nhận sai).
            m = _la_ngoai_ngoac(khoan[i][1])
            if m:
                dung = tn == _gon(khoan[i][1][:m.start()]) and dn == _gon(khoan[i][1][m.end():])
        if not dung:
            lech.append(k.get("stt"))
    lech.extend(so_cua[len(khai_niem):])
    return lech


# ----------------------------------------------------------------- thứ tự đường (lưu bền)

def tep_thu_tu(env=None) -> Path:
    env = os.environ if env is None else env
    return Path(env.get(BIEN_TEP_THU_TU) or Path.home() / ".tra_luat_llm.json")


def thu_tu_hieu_luc(cli=None, env=None, tep=None):
    """Trả (thứ_tự, nguồn). Cờ > tệp đã lưu > biến môi trường > mặc định.

    Tệp ĐỌC KHÔNG ĐƯỢC hay sai định dạng thì NÉM ValueError, không lùi về mặc định: lùi im lặng
    là đổi đường tính tiền sau lưng người dùng (fail-closed)."""
    env = os.environ if env is None else env
    # `is not None`, không phải truthiness: `--thu-tu ""` là GIÁ TRỊ SAI (ném ValueError), không phải
    # "không truyền cờ" — đọc nó thành vắng là rơi sang biến/tệp tính tiền đường khác (F9, PR #1503).
    if cli is not None:
        return doc_thu_tu(cli), "co --thu-tu"
    tep = tep_thu_tu(env) if tep is None else Path(tep)
    # `is_symlink()` kèm `exists()`: symlink ĐỨT là "có cấu hình mà không đọc được" ⇒ fail-closed,
    # không phải "không có tệp" (F9).
    if tep.exists() or tep.is_symlink():
        try:
            gia_tri = json.loads(tep.read_text(encoding="utf-8")).get("thu_tu")
        except (OSError, ValueError, AttributeError) as e:
            raise ValueError(f"tep thu tu {tep} hong ({type(e).__name__}) — sua hoac `tl llm-order --reset`") from e
        if not isinstance(gia_tri, str):
            raise ValueError(f"tep thu tu {tep} thieu khoa chuoi 'thu_tu' — `tl llm-order --reset`")
        return doc_thu_tu(gia_tri), f"tep {tep}"
    if (env.get(BIEN_THU_TU) or "").strip():
        return doc_thu_tu(env[BIEN_THU_TU]), f"bien {BIEN_THU_TU}"
    return THU_TU_MAC_DINH, "mac dinh"


def luu_thu_tu(gia_tri, env=None, tep=None) -> tuple[tuple[str, ...], Path]:
    """Ghi NGUYÊN TỬ (tệp tạm cùng thư mục → os.replace). Kiểm hợp lệ TRƯỚC khi ghi."""
    thu_tu = doc_thu_tu(gia_tri)
    tep = tep_thu_tu(env) if tep is None else Path(tep)
    tep.parent.mkdir(parents=True, exist_ok=True)
    fd, tam = tempfile.mkstemp(prefix=".tl-llm-", dir=str(tep.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"thu_tu": ",".join(thu_tu)}, f)
        os.replace(tam, tep)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tam)
        raise
    return thu_tu, tep


def xoa_thu_tu(env=None, tep=None) -> bool:
    tep = tep_thu_tu(env) if tep is None else Path(tep)
    if tep.exists() or tep.is_symlink():
        tep.unlink()
        return True
    return False


def trang_thai_duong(env=None, tim=shutil.which) -> dict:
    """Đường nào CÓ MẶT — không gọi gì, không chứng minh dùng được."""
    env = os.environ if env is None else env
    ten, _ = lay_key(env)
    try:
        import importlib.util
        co_sdk = importlib.util.find_spec("anthropic") is not None
    except (ImportError, ValueError):
        co_sdk = False
    return {"api": {"bien_key": ten, "sdk": co_sdk}, "sub": {"claude_cli": bool(tim("claude"))}}


# ----------------------------------------------------------------- lấy nguyên văn Điều

def lay_dieu_qua_extract(so_hieu, dieu, tl_py, chay=subprocess.run, them=()):
    """Lấy nguyên văn Điều bằng CHÍNH `tl extract` (đường đọc đã verify, có cảnh báo markup/dự thảo
    riêng) — không dựng đường đọc thứ hai. Trả (văn bản, stderr của extract)."""
    p = chay([sys.executable, str(tl_py), "extract", str(so_hieu), "--dieu", str(dieu), *them],
             capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    dau = f"===== Điều {dieu} ====="
    out = p.stdout or ""
    if p.returncode != 0 or dau not in out:
        raise ValueError(f"tl extract {so_hieu} --dieu {dieu} rc={p.returncode}: "
                         f"{(p.stderr or out).strip()[-300:]}")
    # Nguồn chạm trần export ⇒ Điều có thể đã mất khoản cuối, và phép kiểm nguyên văn KHÔNG thể biết
    # (nó so với chính bản bị cắt) — dừng TRƯỚC khi gọi model (cross-review PR #1503 F6). Neo vào dấu
    # RIÊNG của cảnh báo CAP trong `extract_cache.py`, không vào một từ chung.
    # Nguồn chạm trần export ⇒ DỪNG trước khi gọi model, BẤT KỂ Điều đích (lượt 1 F6). Lượt 2 (N6) chỉ ra cách này
    # chặn oan Điều đã kết thúc trước điểm cắt; bản vá lượt 2 thử xác nhận ranh giới bằng một lần `tl extract` THỨ HAI
    # tìm Điều N+1 — lượt 3 (M4) đo được lần đọc thứ hai có thể là bản khác (nguồn được resolve/cập nhật giữa hai
    # lần), tức cấp bằng chứng cho bản bị cắt. Chặn oan (P2) rẻ hơn nhận nhầm (P1): quay về chặn mọi Điều, chỉ
    # đường `tl cache-build` (no-cap). Muốn nới phải lấy ranh giới từ CHÍNH snapshot của lần extract này.
    if MAU_CAP_EXTRACT in (p.stderr or ""):
        raise ValueError(f"nguon cua {so_hieu} cham tran export (~200k ky tu) — Dieu {dieu} co the bi CAT; "
                         f"chay `tl cache-build {so_hieu}` (no-cap) roi chay lai")
    return out.split(dau, 1)[1].strip(), p.stderr or ""


def tach_khai_niem(van_ban, so_hieu="", model=MODEL_MAC_DINH, thu_tu=THU_TU_MAC_DINH, env=None,
                   cac_duong=None) -> dict:
    """Ném HetDuong / Dung. Trả kết quả `goi` kèm `khai_niem` đã chuẩn hoá và `lech` (danh sách stt)."""
    noi_dung = (f"Văn bản số hiệu {so_hieu}.\n\n<dieu_khoan>\n{van_ban}\n</dieu_khoan>"
                if so_hieu else f"<dieu_khoan>\n{van_ban}\n</dieu_khoan>")
    kq = goi(HE_THONG_KHAI_NIEM, noi_dung, SCHEMA_KHAI_NIEM, model, thu_tu, env, cac_duong)
    kiem_schema(kq["data"], SCHEMA_KHAI_NIEM)
    kq["khai_niem"] = chuan_hoa_khai_niem(kq["data"]["khai_niem"])
    kq["lech"] = lech_nguyen_van(kq["khai_niem"], van_ban)
    return kq


def tong_token(u) -> int:
    return u["input"] + u["output"] + u["cache_doc"] + u["cache_ghi"]
