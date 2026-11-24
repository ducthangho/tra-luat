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
    dong = next((ln for ln in str(van_ban).splitlines() if ln.strip()), "")
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
    # 503/529 = dịch vụ API quá tải/không khả dụng — lỗi phía ĐƯỜNG (cross-review PR #1503 F7, đo bằng
    # SDK 2.13.0 + transport giả). KHÔNG mở rộng mù sang mọi 5xx: 500/504 có thể là yêu cầu đã được xử lý
    # (tính tiền) hoặc tính năng chưa hỗ trợ — giữ DỪNG, chờ người giữ hợp đồng quyết.
    if ma in (401, 402, 403, 429, 503, 529) or kieu in ("authentication_error", "billing_error",
                                                         "permission_error", "rate_limit_error",
                                                         "overloaded_error"):
        return ChuyenDuong
    # Hết credit từng được trả bằng 400 kèm câu "credit balance is too low" — chỉ chuỗi
    # ẤY mới chuyển đường; mọi 400 khác là lỗi của yêu cầu.
    if ma == 400 and "credit balance" in thong_bao:
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


def duong_sub(he_thong, noi_dung, schema, model, env, chay=subprocess.run, tim=shutil.which):
    claude_bin = tim("claude")
    if not claude_bin:
        raise ChuyenDuong("khong co claude CLI tren PATH")
    kiem_dinh_tuyen_sub(env)
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
    subtype = kq.get("subtype") if isinstance(kq, dict) else None
    if subtype in SUBTYPE_LOI_YEU_CAU:
        raise Dung(f"claude -p {subtype} (loi phia yeu cau — khong chuyen duong)")
    # NHẬN chỉ khi đủ BA dấu dương: rc 0, `subtype == "success"`, `is_error` đúng là False.
    # Thiếu một dấu (envelope lỗi mà rc 0, thiếu `is_error`) ⇒ không nhận (F2, PR #1503).
    if not (p.returncode == 0 and isinstance(kq, dict) and subtype == "success" and kq.get("is_error") is False):
        mo_ta = (kq or {}).get("result") if isinstance(kq, dict) else (p.stderr or tho)
        raise ChuyenDuong(f"claude -p rc={p.returncode} subtype={subtype}: {str(mo_ta or '').strip()[:160]}")
    mu = kq.get("modelUsage") or {}
    da_chay = {(v or {}).get("canonicalModel") or k for k, v in mu.items()}
    if da_chay != {model}:
        raise Dung(f"model da chay {sorted(da_chay)} khac model yeu cau {model!r}")
    data = kq.get("structured_output")
    if data is None:
        raise Dung("claude -p khong tra structured_output")
    u = next(iter(mu.values()))
    return {
        "duong": "sub", "nguon_key": None, "model": model, "data": data,
        "usage": {"input": u.get("inputTokens", 0), "output": u.get("outputTokens", 0),
                  "cache_doc": u.get("cacheReadInputTokens", 0),
                  "cache_ghi": u.get("cacheCreationInputTokens", 0)},
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
    "Với mỗi khoản: 'thuat_ngu' là phần đứng trước chữ 'là' đầu tiên; "
    "'dinh_nghia' là phần sau chữ 'là' đó, chép NGUYÊN VĂN từng ký tự (giữ dấu câu, kể cả dấu chấm cuối), "
    "không diễn giải, không sửa chính tả. 'stt' là thứ tự khoản, bắt đầu từ 1. "
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


_RE_SO_KHOAN = re.compile(r"^(\d+)\s*[.)]\s+")
_RE_DIEU = re.compile(r"^Điều\s+\d+")
_RE_DIEM = re.compile(r"^([a-zđ]\)|[-–•+])\s*")


def tach_khoan(van_ban) -> list[str]:
    """Các khoản (đã gỡ số thứ tự) của một Điều "Giải thích từ ngữ", theo thứ tự nguồn.

    Bỏ dòng tiêu đề `Điều N.` và câu dẫn trước khoản đầu. Nguồn CÓ số thứ tự (`1.`, `2)`) ⇒ chỉ dòng
    mang số mới mở khoản mới. Nguồn MẤT số (Google Doc export rơi số tự động — đo trên Điều 3 Luật
    134/2025/QH15) ⇒ dòng có " là " và không mở đầu bằng ký hiệu điểm (`a)`, `-`) mở khoản mới.
    Dòng còn lại nối vào khoản trước (điểm a, b…)."""
    dong = [ln.strip() for ln in str(van_ban).splitlines() if ln.strip()]
    if dong and _RE_DIEU.match(dong[0]):
        dong = dong[1:]
    co_so = any(_RE_SO_KHOAN.match(ln) for ln in dong)
    khoan: list[str] = []
    for ln in dong:
        m = _RE_SO_KHOAN.match(ln)
        if co_so:
            if m:
                khoan.append(ln[m.end():])
            elif khoan:
                khoan[-1] += "\n" + ln
            continue
        mo = " là " in ln and not _RE_DIEM.match(ln) and not ln.endswith(":")
        if mo:
            khoan.append(ln)
        elif khoan:
            khoan[-1] += "\n" + ln
    return khoan


def _gon(s) -> str:
    return " ".join(str(s).split())


def lech_nguyen_van(khai_niem, van_ban):
    """Các `stt` sai so với nguồn. So TRỌN KHOẢN (khoảng trắng gộp), không so chuỗi con: cross-review
    PR #1503 F1 đo được định nghĩa bị CẮT (`tài liệu` thay cho cả câu), mảng rỗng, thiếu khoản và
    tráo số đều qua phép kiểm chuỗi con. Nay đòi: mục thứ i có `stt == i+1` và cụm
    `<thuật ngữ> là <định nghĩa>` bằng đúng khoản thứ i của nguồn; khoản nguồn không có mục tương
    ứng cũng là lệch (số của khoản ấy). Nguồn không tách được khoản nào ⇒ `[0]` (không xác minh được)."""
    khoan = tach_khoan(van_ban)
    if not khoan:
        return [0]
    lech = []
    for i, k in enumerate(khai_niem):
        cum = f'{k["thuat_ngu"]} là {k["dinh_nghia"]}'
        if not (i < len(khoan) and k["stt"] == i + 1 and _gon(cum) == _gon(khoan[i])):
            lech.append(k["stt"])
    lech.extend(range(len(khai_niem) + 1, len(khoan) + 1))
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
