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
import zipfile
import unicodedata
from pathlib import Path
from xml.etree import ElementTree as ET
from urllib.parse import urlparse

MODEL_MAC_DINH = "claude-haiku-5-5"
DUONG_HOP_LE = ("api", "sub")
BIEN_KEY = ("TL_ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY")
# Biến khiến `claude` CLI xác thực bằng API thay vì gói — gỡ khỏi env của con ở đường `sub`,
# kẻo trên máy cá nhân "sub" lặng lẽ tính tiền vào API key.
BIEN_GO_KHOI_SUB = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "TL_ANTHROPIC_API_KEY")
TIMEOUT_SUB_GIAY = 300
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
# Tiêu đề Điều: số Điều phải đi ngay với dấu "." hoặc ":" (lượt 6 S2: dòng "Điều 3 của quy chế là …" của tệp KHÔNG
# tiêu đề từng bị nhận là tiêu đề, khoản đầu bị bỏ). Dùng CHUNG cho metadata và cho phân đoạn khoản.
_RE_TIEU_DE_DIEU = re.compile(r"^\s*Điều\s+(\d+[a-zđ]?)\s*[.:]")
# r3 (lượt 3 C1): dòng tiêu đề chỉ được BỎ khi CẢ dòng đúng là tiêu đề — `Điều N.` (hoặc `:`), kèm hoặc không kèm tên
# "Giải thích từ ngữ". Tiêu đề có phần dư khác ⇒ có thể dính khoản đầu (kể cả khoản dùng từ nối khác "là") ⇒ mơ hồ.
_RE_TIEU_DE_TRON = re.compile(r"^Điều\s+\d+[a-zđ]?\s*[.:]\s*(?:Giải thích từ ngữ\s*\.?)?$", re.IGNORECASE)


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


_LA_WINDOWS = os.name == "nt"


class KhongKhoiChay(OSError):
    """Tiến trình con KHÔNG khởi chạy được (Popen hỏng) — mốc phân biệt lỗi TRƯỚC với lỗi SAU khởi chạy (lượt 6 S1)."""


def _chay_co_moc(cmd, *, timeout=None, capture_output=True, **kw):
    """Như `subprocess.run(..., capture_output=True)` nhưng lỗi KHỞI CHẠY ném `KhongKhoiChay`, còn mọi lỗi SAU khi
    `Popen` đã trả tiến trình (đọc pipe, chờ, quá hạn) giữ nguyên kiểu và tiến trình con được giết + thu hồi."""
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kw)
    except OSError as e:
        raise KhongKhoiChay(e.errno, f"khong khoi chay duoc {cmd[0]}: {e.strerror or e}") from e
    try:
        out, err = proc.communicate(timeout=timeout)
    except BaseException:
        # Lượt 7 T2: thu hồi KHÔNG phụ thuộc vào việc đọc lại (lỗi đọc có thể lặp lại): giết, đóng pipe, rồi `wait` CÓ
        # giới hạn — tiến trình khác còn giữ pipe cũng không làm lệnh treo.
        proc.kill()
        with contextlib.suppress(Exception):
            proc.wait(timeout=5)
        # Lượt 8 U2: trên Windows `communicate` đọc pipe bằng LUỒNG nền — đóng đồng bộ có thể chờ luồng ấy (khi một
        # tiến trình khác còn giữ đầu ghi) ⇒ không đóng ở đó; thu hồi đã xong ở `wait` phía trên.
        if not _LA_WINDOWS:
            for ong in (proc.stdout, proc.stderr):
                with contextlib.suppress(Exception):
                    ong.close()
        raise
    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)


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


def kiem_xac_thuc_sub(claude_bin, env, chay=_chay_co_moc) -> None:
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


def duong_sub(he_thong, noi_dung, schema, model, env, chay=_chay_co_moc, tim=shutil.which):
    claude_bin = tim("claude")
    if not claude_bin:
        raise ChuyenDuong("khong co claude CLI tren PATH")
    kiem_dinh_tuyen_sub(env)
    kiem_xac_thuc_sub(claude_bin, env, chay)
    # Ranh giới chuyển đường (Review Rescue Checkpoint sau lượt 5, quyết định chủ kho): CHỈ lỗi TRƯỚC khi tiến trình
    # `claude -p` khởi chạy (thiếu CLI, định tuyến, `auth status`, không spawn được) mới được chuyển sang `api`. Đã
    # khởi chạy rồi thì KHÔNG đoán "model đã chạy chưa" từ envelope nữa — năm lượt review liên tiếp tìm ra một cửa
    # mới trong phép đoán ấy (F2→N2→M2→Q2→R2). Mọi lỗi sau khởi chạy ⇒ DỪNG; người dùng tự chạy lại với `--thu-tu api`.
    goi_y = "loi sau khi claude -p da khoi chay — khong tu chuyen duong; het han muc goi thi chay lai voi --thu-tu api"
    # cwd tạm: tránh nạp ngữ cảnh kho. Tạo TRƯỚC mốc khởi chạy (lỗi ở đây là chuẩn bị ⇒ chuyển được) và dọn bằng
    # `ignore_errors` SAU đó: lỗi dọn dẹp không được quyết định đường (lượt 6 S1).
    try:
        cwd = tempfile.mkdtemp(prefix="llm-route-")
    except OSError as e:
        raise ChuyenDuong(f"khong tao duoc thu muc tam cho claude -p: {type(e).__name__}") from e
    try:
        # stdin=DEVNULL: không có thì `claude -p` chèn dòng "no stdin data received" TRƯỚC
        # JSON (đo 06-09-2026, CLAUDE.md §Gọi agent đa nền).
        p = chay(lenh_sub(claude_bin, he_thong, noi_dung, schema, model),
                 stdin=subprocess.DEVNULL, capture_output=True, text=True,
                 encoding="utf-8", errors="replace", timeout=TIMEOUT_SUB_GIAY,
                 env=env_cho_sub(env), cwd=cwd)
    except KhongKhoiChay as e:
        raise ChuyenDuong(f"khong khoi chay duoc claude -p: {e}") from e
    except subprocess.TimeoutExpired as e:
        raise Dung(f"claude -p qua han {TIMEOUT_SUB_GIAY}s ({goi_y})") from e
    except OSError as e:
        # Mọi OSError KHÁC `KhongKhoiChay` xảy ra SAU mốc khởi chạy (đọc pipe, chờ) ⇒ DỪNG (lượt 6 S1).
        raise Dung(f"claude -p loi I/O sau khi khoi chay: {type(e).__name__} ({goi_y})") from e
    finally:
        shutil.rmtree(cwd, ignore_errors=True)
    tho = p.stdout or ""
    i = tho.find("{")
    try:
        kq = json.loads(tho[i:]) if i >= 0 else None
    except json.JSONDecodeError:
        kq = None
    # Giải mã envelope MỘT lần, KIỂM KIỂU trước mọi phép tra (lượt 2 N2).
    if not isinstance(kq, dict):
        raise Dung(f"claude -p rc={p.returncode}: khong co envelope JSON ({goi_y}): {(p.stderr or tho).strip()[:160]}")
    subtype = kq.get("subtype") if isinstance(kq.get("subtype"), str) else None
    stop = kq.get("stop_reason") if isinstance(kq.get("stop_reason"), str) else None
    # NHẬN chỉ khi đủ dấu dương: rc 0, `subtype == "success"`, `is_error` đúng là False (lượt 1 F2), và lý do kết thúc
    # không phải từ chối/cắt đầu ra (lượt 2 N2: kể cả khi envelope tự xưng `success`).
    if not (p.returncode == 0 and subtype == "success" and kq.get("is_error") is False
            and stop not in STOP_REASON_LOI_YEU_CAU):
        mo_ta = str(kq.get("result") or "").strip()[:160]
        raise Dung(f"claude -p rc={p.returncode} subtype={subtype} stop_reason={stop} ({goi_y}): {mo_ta}")
    mu = kq.get("modelUsage")
    da_chay = {(v.get("canonicalModel") if isinstance(v.get("canonicalModel"), str) else k)
               for k, v in mu.items()} if isinstance(mu, dict) and all(isinstance(v, dict) for v in mu.values()) else None
    if da_chay != {model}:
        raise Dung(f"model da chay {sorted(da_chay) if da_chay else da_chay} khac model yeu cau {model!r}")
    u = _usage_sub(mu)
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
    Path(tep).parent.mkdir(parents=True, exist_ok=True)   # lượt 5 R5: cùng hợp đồng với `--out`
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
# r20 (lượt 19 V4) → r21 (W4) → r22 (X3) → r23 (lượt 22 Y3): NGỮ PHÁP nhãn điểm của nguồn thô, cùng miền với nhãn `_nhan` dựng từ
# `lvlText` (dấu `.` `)` `(` `-` `–` + khoảng đệm): chữ cái đơn/lặp, thường/hoa, khoảng đệm ngang (dấu cách, tab, NBSP) giữa chữ và dấu;
# nhãn thập phân nhiều cấp (`1.1.`, `1.2`); dấu đầu dòng. Từ ghép `e-mail` và viết tắt nhiều chữ cái khác nhau (`Tp.`) không khớp.
_KC = r"[ \t\u00a0]*"


def _chu_nhan(i):
    return f"(?:(?P<t{i}>[a-zđ])(?P=t{i})*|(?P<h{i}>[A-ZĐ])(?P=h{i})*)"


def _tok(i):
    """r26 (lượt 25 B1): một placeholder của `lvlText` đã dựng — số thập phân, hoặc một chữ cái lặp (thường/hoa)."""
    return f"(?:\\d+|{_chu_nhan(i)})"


# r26 (lượt 25 B1): miền nhãn = mọi nhãn `_nhan` dựng được — các placeholder nối bằng `.` / `-` / `–` (có đệm), mở bằng `(` tuỳ chọn,
# kết bằng `.` `)` (dính thân được), gạch (sau là khoảng trắng hay dấu mở trích dẫn/ngoặc), hoặc — chỉ khi đã có dấu nối giữa các
# placeholder — kết ngay sau chữ số. Nhãn chỉ có khoảng trắng (`a tổ chức`) không phân biệt được với chữ ⇒ ngoài miền (§2.28 B1).
_NOI = rf"{_KC}[.)(\-–]{_KC}"   # r27 (lượt 26 C1): mọi dấu `lvlText` cho phép giữa hai placeholder (`1(1)`, `a)b)`)


def _chu_rieng(i):
    """r28 (lượt 27 D1): placeholder chữ cái — một chữ lặp, KHÔNG dính thêm chữ cái khác (`Hồ` không phải placeholder)."""
    return f"(?:(?P<r{i}>[a-zđ])(?P=r{i})*|(?P<R{i}>[A-ZĐ])(?P=R{i})*)(?![^\\W\\d_])"


# r29 (lượt 28 E1): TIỀN TỐ nhãn = mọi dấu `lvlText` (`.` `)` `(` `-` `–`, có đệm) đứng TRƯỚC placeholder đầu (`.1.1.`, `(.a)`, `-1.1`) —
# cùng vị trí dấu mà `_nhan` cho phép (đầu · giữa · cuối). `_TIEN_TO_DAU` bắt buộc có ít nhất một dấu.
_TIEN_TO = rf"(?:{_KC}[.)(\-–])*{_KC}"
_TIEN_TO_DAU = rf"(?:{_KC}[.)(\-–])+{_KC}"
_MO_THAN = "(?=\\s|[“\"‘'(])"
_RE_DIEM = re.compile("^(?:" + "|".join([
    rf"{_TIEN_TO}{_tok(3)}(?:{_NOI}{_tok(4)})*{_KC}[.)]",
    rf"{_TIEN_TO}{_tok(5)}(?:{_NOI}{_tok(6)})*{_KC}[-–]{_MO_THAN}",
    # r29 (lượt 28 E1): nhãn có dấu ở ĐẦU rồi placeholder, kết ngay sau placeholder (`.1 …`, `(a …`).
    rf"{_TIEN_TO_DAU}(?:\d+|{_chu_rieng(7)})(?:{_NOI}(?:\d+|{_chu_rieng(8)}))*(?=\s|[“\"‘'(]|[^\W\d_])",
    r"[-–•+]",
]) + r")\s*")
_RE_LA = re.compile(r"(?:^|\s)là(?:\s|$)")
_RE_MO_BANG_LA = re.compile(r"^là(?:\s|$)")
# Câu dẫn của Điều "Giải thích từ ngữ" — r6 (lượt 6 F2, Review Rescue sau sáu lượt cùng lớp): DANH SÁCH CHO PHÉP NGUYÊN DÒNG.
# Năm bản trước dò HẬU TỐ `… như sau:` rồi loại dần hình dạng xấu (từ nối X3/A1, vị trí D3, dấu `:` và chữ "là" E2) — lượt nào
# cũng còn một dạng lọt. Nay dòng chỉ được bỏ khi CẢ dòng (gộp khoảng trắng, phân biệt hoa thường) đúng câu dẫn chuẩn.
_RE_CAU_DAN_TRON = re.compile(
    r"(?:Trong|Tại) (?:Luật|Bộ luật|Pháp lệnh|Nghị định|Nghị quyết|Thông tư|Thông tư liên tịch|Quyết định) này, "
    r"(?:các|những) (?:từ ngữ|thuật ngữ) (?:dưới đây|sau đây) được (?:hiểu|giải thích) như sau:")
# r2 (lượt 2 A2): `;` KHÔNG kết khoản — ngắt dòng sau `;` giữa một định nghĩa dài từng tạo hai khoản đều qua kiểm.
_DAU_CAU_KET = frozenset(".!?")
# r2 (lượt 2 A2): đánh số NỘI DÒNG trong thân khoản (`… 1) …`, `… 2. …`) — tiểu mục, ranh giới khoản không tin được.
# r3 (lượt 3 C2): khoảng trắng hai bên CHỈ trong phạm vi một dòng (`[ \t]`, không `\s`) — số điều ở cuối một dòng điểm, theo sau
# là xuống dòng, không phải số thứ tự nội dòng.
# r4 (lượt 4 D1): mọi khoảng trắng TRỪ xuống dòng (`[^\S\n]`) — gồm U+00A0 khoảng trắng không ngắt mà `[ \t]` bỏ sót.
# r5 (lượt 5 E1): dấu số DÍNH thân (`… 2.Abc`) cũng là đánh số nội dòng.
# r6 (lượt 6 F1): chốt nội dòng PHỦ trọn cú pháp `_RE_SO_KHOAN` thay cho liệt kê dạng theo sau dấu số — `(N)` hoặc `N` + khoảng trắng
# tuỳ ý + `.`/`)`, rồi BẤT KỲ ký tự nào trừ chữ số (số thập phân `1.5`), xuống dòng hay hết chuỗi (số điều cuối dòng điểm, C2);
# đứng trước không phải chữ/số, `.` hay `,` (`A1.`, `1.2.3`).
_RE_SO_NOI_DONG = re.compile(r"(?<![\w.,])(?:\(\d+\)|\d+[^\S\n]*[.)])(?![\d\n]|$)")

# r35 (lượt 34, lớp `can-tai-nguyen-doc-nguon`): NGÂN SÁCH đọc nguồn thô — vượt ⇒ nguồn không xác minh được (fail-closed), không
# traceback, không đình trệ. Một Điều thật dưới 200k ký tự (trần export `tl extract`); số khoản tối đa vài chục.
_TRAN_VAN_BAN = 400_000
_TRAN_CHU_SO = 4
_RE_SO_QUA_DAI = re.compile(r"\(?[0-9]{%d}" % (_TRAN_CHU_SO + 1))
# r36: trần BYTE khi đọc tệp `--tep` (UTF-8 tối đa 4 byte/ký tự) — đọc có giới hạn, không nạp trọn tệp lớn.
TRAN_BYTE_TEP = 4 * _TRAN_VAN_BAN


def vuot_ngan_sach(van_ban):
    """r35: chuỗi mô tả nếu nguồn thô vượt ngân sách đọc (người gọi dừng TRƯỚC model), None nếu trong hạn."""
    s = str(van_ban)
    if len(s) > _TRAN_VAN_BAN:
        return f"van ban {len(s)} ky tu vuot tran {_TRAN_VAN_BAN}"
    # r36 (lượt 35): số đầu dòng quá `_TRAN_CHU_SO` chữ số cũng là vượt ngân sách — chặn TRƯỚC model ở mọi đường thô, cùng một chốt.
    # r36 (lượt 36): CÙNG quy tắc với `tach_khoan` — gỡ đúng một BOM, tách dòng bằng `splitlines` (LF/CRLF/CR).
    if any(_RE_SO_QUA_DAI.match(ln.lstrip(" \t\u00a0")) for ln in _bo_mot_bom(s).splitlines()):
        return f"so dau dong qua {_TRAN_CHU_SO} chu so"
    return None


# r36 (Review Rescue Checkpoint §12 sau lượt 34 — lớp `ranh-gioi-khoan` lặp từ lượt 1; chủ kho duyệt): DANH SÁCH CHO PHÉP đầu dòng
# thay cho mọi ngữ pháp nhãn bị CẤM. Mười lăm lượt (V4 … J1, rồi bộ quét r35) đoán trước hình dạng nhãn để chặn — lượt nào cũng còn một
# hình dạng lọt, vì danh sách cấm phải đoán mọi cách viết của `lvlText`. Nay một dòng thô chỉ được nhận khi đầu dòng thuộc TẬP NHỎ đã
# biết; mọi đầu dòng khác (nhãn điểm, nhãn nhiều thành phần, ký hiệu, chữ số, dấu lạ…) ⇒ từ chối CẢ nguồn, chuyển `--tep <tệp .docx>`:
#   [số khoản `N.` / `N)` / `(N)`, N ≤ 4 chữ số, rồi đệm ngang tuỳ ý]  [một dấu mở `“` `"` `‘` `(` tuỳ ý]  TỪ ĐẦU
# TỪ ĐẦU = dải chữ cái liền đầu thân, và phải (a) chứa ít nhất một chữ NGOÀI bảng placeholder ASCII (`Hồ`, `Dữ`, `Cơ` — `_nhan` chỉ
# sinh chữ số, chữ ASCII và dấu `lvlText`, nên chữ có dấu thanh/mũ không thể là nhãn), hoặc (b) là chữ ASCII dài ≥ 2, KHÔNG phải một
# chữ lặp (`aa`, `BB` là nhãn Word sau `z`), và — ở CẢ HAI nhánh (r38) — theo sau là ĐỆM ngang rồi một CHỮ CÁI (`Quy trình`, `Hồ sơ`). Mọi thứ khác bị chặn oan có chủ đích:
# `Tp. …`, `e-mail …`, `A1 …`, `ASEAN (…)`, thân mở bằng chữ số hay dấu lạ — chặn oan rẻ hơn nhận nhầm.
# r36 (lượt 36): bảng placeholder = ĐÚNG miền thật của `_chu_cai` (a–z, A–Z) — `đ/Đ` không bao giờ là nhãn nên thuộc nhánh (a).
_CHU_PH = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
_DEM_NGANG = frozenset(" \t\u00a0")
_RE_SO_DAU = re.compile("(?:([0-9]{1,%d})[.)]|\\(([0-9]{1,%d})\\))[ \t\u00a0]*" % (_TRAN_CHU_SO, _TRAN_CHU_SO))
_MO_CHO_PHEP = frozenset("“\"‘(")


def _mo_dau_nhieu_ve(t):
    """r39 → r40 (lượt 38–39 — quyết định chủ kho: "Khi phần mở đầu khoản cũng có hình dạng nhãn điểm nhiều vế, đường thô từ chối cả
    Điều. Dùng DOCX có cấp danh sách để xác minh."). True khi thân `t` mở bằng [một dấu mở `(` `“` `"` `‘`] ≥ 2 VẾ (dải chữ/số) chỉ
    ngăn bằng đệm ngang, rồi DẤU KẾT nhãn (`.` `)` `-` `–` `—`) và còn chữ phía sau. Mốc thoát DUY NHẤT là từ nối cấp khoản: vế `là`
    đứng NGOÀI dấu mở và có khoảng trắng theo sau (cùng điều kiện `_RE_LA`) — `là` trong ngoặc/nháy mở hay dính dấu kết không thoát.
    r40 (lượt 39): bỏ ngoại lệ "gạch ≤ 3 vế ngắn" — mọi số vế, mọi độ dài vế; `kinh tế - xã hội …` ở đầu dòng nay bị chặn (thu hẹp
    miền theo quyết định chủ kho). Tuyến tính."""
    mo = t[:1] in _MO_NHIEU_VE
    i = 1 if mo else 0
    so_ve, j = 0, i
    while True:
        k = j
        while k < len(t) and t[k].isalnum():
            k += 1
        if k == j:
            return False
        so_ve += 1
        m = k
        while m < len(t) and t[m] in _DEM_NGANG:
            m += 1
        if not mo and t[j:k] == "là" and m > k:
            return False   # từ nối cấp khoản ⇒ phần trước là thuật ngữ, không phải nhãn
        if m > k and m < len(t) and t[m].isalnum():
            j = m
            continue
        break
    return so_ve >= 2 and m < len(t) and t[m] in _DAU_KET_NHIEU_VE and bool(t[m + 1:].strip(" \t\u00a0"))


_MO_NHIEU_VE = frozenset("(“\"‘")
_DAU_KET_NHIEU_VE = frozenset(".)-–—")


def dau_dong_cho_phep(ln):
    """r36: phân loại đầu dòng (đã strip) theo DANH SÁCH CHO PHÉP → `("so", số, vị trí thân)` · `("than",)` · None (ngoài danh sách)."""
    m = _RE_SO_DAU.match(ln)
    i = m.end() if m else 0
    if i < len(ln) and ln[i] in _MO_CHO_PHEP:
        i += 1
    j = i
    while j < len(ln) and ln[j].isalpha():
        j += 1
    tu = ln[i:j]
    if not tu:
        return None
    k = j
    while k < len(ln) and ln[k] in _DEM_NGANG:
        k += 1
    if k == j or k >= len(ln) or not ln[k].isalnum():
        # r38 (lượt 37): CẢ HAI nhánh — từ đầu phải là một TỪ TRỌN đứng trước đệm rồi một chữ cái/chữ số (`Điều 3 của …`). Nhãn điểm GÕ TAY bằng chữ tiếng
        # Việt (`đ)`, `(đ)`, `đ.`, `ơ-`) có chữ ngoài bảng placeholder Word nhưng theo sau là DẤU nhãn ⇒ không phải thân.
        return None
    if _mo_dau_nhieu_ve(ln[m.end() if m else 0:]):
        return None   # r39 (lượt 38, quyết định chủ kho "thu hẹp miền")
    co_dau = any(c not in _CHU_PH for c in tu)
    if not co_dau and (len(tu) < 2 or tu == tu[0] * len(tu)):
        return None   # (b): chữ ASCII dài ≥ 2 và không phải một chữ lặp (`aa`, `BB` là nhãn Word sau `z`)
    if m:
        return ("so", int(m.group(1) or m.group(2)), m.end())
    return ("than",)


# ------------------------------------------------------------------ #1525: ranh giới khoản từ CẤU TRÚC .docx
# Vì sao: `tach_khoan` đoán ranh giới từ văn bản THÔ, và mười lượt cross-review packet #1514 cho thấy trên văn bản thô
# "khoản có điểm" và "lời dẫn nhóm + điểm là định nghĩa" có CÙNG hình dạng (nợ #1525). Google Doc đánh số TỰ ĐỘNG nên
# export text/plain mất số; export .docx còn `w:numPr` (`w:numId` + `w:ilvl`) trên từng đoạn ⇒ ranh giới là DỮ LIỆU.
# Chỉ thư viện chuẩn. Fail-closed: `ValueError` khi cấu trúc mơ hồ/không hỗ trợ hoặc Điều không có đánh số tự động — DỪNG,
# không lùi về đoán (r5, lượt 4 D1).
_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_TRAN_XML = 64 * 1024 * 1024   # dự phòng khi không nạp được `read_member_bounded`
# r35 (lượt 34, `can-tai-nguyen-doc-nguon`): trần ĐỘ SÂU cây XML — các phép duyệt sau (`_danh_dau_giu_trang`, `_doan_trong`, `duyet`)
# đệ quy theo wrapper; cây sâu hơn ⇒ `RecursionError` (không thuộc lỗi nguồn CLI bắt). Word/Google Docs xuất sâu dưới 20 tầng.
_TRAN_SAU_XML = 128
_TRAN_NUT_XML = 2_000_000   # r36 (lượt 35): trần SỐ NÚT mỗi part
_TRAN_GOI = 64 * 1024 * 1024   # r36 (lượt 36): trần byte cả gói .docx, đo TRƯỚC khi mở ZIP
_TRAN_MEMBER = 2000   # r36: trần số member trong gói
# r35: trần độ dài NHÃN mở rộng từ `lvlText` và tổng chữ Điều dựng từ .docx.
_TRAN_NHAN = 64


def _xml_cay(du_lieu):
    """r35 → r36 (lượt 35, `can-tai-nguyen-doc-nguon`): parse TĂNG DẦN (`XMLPullParser`, từng khối 64 KiB) và đếm ĐỘ SÂU + SỐ NÚT ngay
    ở sự kiện `start` — vượt trần thì dừng TRƯỚC khi dựng hết cây và trước mọi phép duyệt đệ quy ⇒ ValueError."""
    b = du_lieu if isinstance(du_lieu, (bytes, bytearray)) else str(du_lieu).encode("utf-8")
    p = ET.XMLPullParser(events=("start", "end"))
    tt = {"sau": 0, "nut": 0, "goc": None}

    def dem():
        for su_kien, el in p.read_events():
            if su_kien == "start":
                tt["sau"] += 1
                tt["nut"] += 1
                tt["goc"] = el if tt["goc"] is None else tt["goc"]
                if tt["sau"] > _TRAN_SAU_XML:
                    raise ValueError(f"cay XML sau hon {_TRAN_SAU_XML} tang — khong ho tro")
                if tt["nut"] > _TRAN_NUT_XML:
                    raise ValueError(f"cay XML nhieu hon {_TRAN_NUT_XML} nut — khong ho tro")
            else:
                tt["sau"] -= 1
    for i in range(0, len(b), 65536):
        p.feed(b[i:i + 65536])
        dem()
    p.close()
    dem()
    return tt["goc"]

# Tiêu đề Điều / ranh giới cấu trúc lớn: chỉ xét ở ĐẦU đoạn (sau khi gộp khoảng trắng).
# r11 (lượt 10 K2): số thứ tự của tiêu đề cấu trúc còn có dạng viết bằng chữ (`Phần thứ nhất`) và chữ cái đơn.
# r12 (lượt 11 L3): số thứ tự viết bằng chữ chỉ là TỪ SỐ (`thứ nhất`…`thứ mười…`); La Mã và chữ cái đơn phải VIẾT HOA (không
# nuốt `Mục vi phạm`, `Phần thứ cấp`).
_RE_RANH_GIOI_LON = re.compile(
    r"^(?i:chương|mục|phần)\s+(?:[IVXLCDM]+|\d+|(?i:thứ\s+(?:nhất|hai|ba|tư|bốn|năm|sáu|bảy|tám|chín|mười)(?!\w))|[A-ZĐ])(?!\w)")
# r12 (lượt 11 L2): tiêu đề Điều THIẾU dấu sau số (`Điều 4 Phạm vi`) — nhận khi CẢ đoạn không kết bằng dấu câu (tiêu đề không có
# dấu câu cuối; dẫn chiếu trong thân điểm/khoản kết bằng `;` `.` …).
# r13 (lượt 12 M1): TIỀN TỐ và HẬU TỐ xét RIÊNG — tên Điều được có dấu câu GIỮA tên (`Điều 5 Phạm vi, đối tượng`); chỉ dấu câu
# CUỐI đoạn (bỏ qua ngoặc/nháy đóng) phân biệt dẫn chiếu với tiêu đề. Số theo sau không phải chữ/số (`Điều 5—Phạm vi` cũng khớp).
# r14 (lượt 13 N1, Review Rescue Checkpoint §12): lớp `ranh-gioi-khoan` lặp qua L2 → M1 → N1 — mỗi lần vá MỘT hình dạng tiêu đề
# thì lộ hình dạng khác (dấu cuối, dấu giữa tên, gạch dưới…). Đổi từ "nhận diện tiêu đề" sang "cấm tiền tố": trong thân Điều,
# MỌI đoạn mà (sau khi bỏ ký tự không phải chữ/số ở đầu, chuẩn hoá NFC) mở bằng `Điều` + số ⇒ chặn, bất kể ký tự sau số hay dấu câu
# cuối đoạn. Cái giá đã khai: điểm/khoản MỞ BẰNG dẫn chiếu `Điều 5 …` cũng bị chặn (rc 2, không ghép sai).
# r15 (lượt 14 Q1) → r16 (lượt 15 R1): bản chiếu dò tiền tố — mọi ký tự không phải chữ/số (gạch dưới, dấu câu) thành khoảng
# trắng, gộp khoảng trắng. Ký tự vô hình / dấu tổ hợp lạ / chữ không NFC đã bị TỪ CHỐI trước đó (`_ky_tu_la`), nên bản chiếu không
# phải chuẩn hoá Unicode nữa. CHỈ dùng để DÒ; nguyên văn đưa model và phép so vẫn là chữ gốc.
_RE_DIEU_TRONG_THAN = re.compile(r"^[ĐÐ]iều\s*\d", re.IGNORECASE)


# r16 (lượt 15 R1/R3) → r17 (lượt 16 S1/S2, Review Rescue Checkpoint §12): lớp "biên ký tự" lặp N1 → Q1 → R1 → S1 — r16 TỪ CHỐI
# theo DANH SÁCH CẤM nhóm Unicode (Cf/Mn/…) và thua ngay ký tự trống thuộc nhóm CHỮ (Hangul Filler U+3164, `Lo`). Doctrine kho:
# danh sách cấm không bao giờ đủ ⇒ ĐẢO thành DANH SÁCH CHO PHÉP. Chữ của Điều chỉ được gồm: ASCII in được (U+0020–U+007E), chữ
# tiếng Việt dựng sẵn (nguyên âm × 5 thanh, đ/Đ), chữ Latin-1 (U+00C0–U+00FF trừ × ÷), một bộ dấu in ấn cố định, NBSP, tab; xuống
# dòng `\n`/`\r` chỉ ở văn bản thô. Ký tự khác (kể cả dấu tổ hợp tách rời ⇒ không cần kiểm NFC riêng) ⇒ dừng (rc 2), không đoán.
# Kiểm trên chữ GỐC, TRƯỚC mọi bước tách dòng / gộp khoảng trắng / strip (S2).
def _dung_bang_cho_phep():
    ds = set(chr(i) for i in range(0x20, 0x7F))
    ds |= set(chr(i) for i in range(0xC0, 0x100)) - {"×", "÷"}
    for nguyen_am in "aăâeêioôơuưy":
        for thanh in ("", "\u0300", "\u0301", "\u0303", "\u0309", "\u0323"):
            for c in (nguyen_am, nguyen_am.upper()):
                ds.add(unicodedata.normalize("NFC", c + thanh))
    # r19 (lượt 18 U1): KHÔNG nhận số mũ `¹²³` — mọi chữ số tới được chốt cú pháp đều là ASCII (r18 đổi số mũ về chữ số thường
    # và làm lệch nhánh số gõ tay / số thập phân; đường thô thì chưa đổi). Cái giá đã khai: `m²`… bị chặn.
    ds |= set("đĐ\u00a0\t“”‘’–—…«»§°±×÷≤≥€₫‰•·№")
    return frozenset(c for c in ds if len(c) == 1)


_KY_TU_CHO_PHEP = _dung_bang_cho_phep()


def _bo_mot_bom(van_ban):
    """r17 (lượt 16 S2) → r18 (lượt 17 T2): bỏ ĐÚNG MỘT BOM đầu văn bản — tầng DUY NHẤT gỡ BOM của đường thô."""
    s = str(van_ban)
    return s[1:] if s.startswith("\ufeff") else s


def ky_tu_ngoai_danh_sach(van_ban):
    """r18 (lượt 17 T2): chốt dùng chung cho CLI — lý do (chuỗi) nếu văn bản thô có ký tự ngoài danh sách cho phép; None nếu sạch."""
    return _ky_tu_la(_bo_mot_bom(van_ban), xuong_dong=True)


def _ky_tu_la(chu, xuong_dong=False):
    """r17 (lượt 16 S1/S2): ký tự đầu tiên NGOÀI danh sách cho phép (`_KY_TU_CHO_PHEP`; `\n`/`\r` chỉ khi `xuong_dong`); None nếu sạch."""
    for c in str(chu):
        if c not in _KY_TU_CHO_PHEP and not (xuong_dong and c in "\n\r"):
            return f"ky tu U+{ord(c):04X} ({unicodedata.category(c)}) ngoai danh sach cho phep"
    return None


def _dau_doan(chu):
    """r14 (lượt 13 N1) → r15 (lượt 14 Q1): bản chiếu để dò tiền tố cấu trúc — chỉ chữ/số, mọi ký tự khác thành một dấu cách.
    r19 (lượt 18 U1): chữ số duy nhất trong danh sách cho phép là ASCII ⇒ không cần chiếu số."""
    return " ".join("".join(c if c.isalnum() else " " for c in chu).split())


def _mo_bang_dieu(chu):
    """r14 (lượt 13 N1): đoạn mở bằng `Điều <số>` ở bất kỳ hình dạng nào."""
    return bool(_RE_DIEU_TRONG_THAN.match(_dau_doan(chu)))
# Số khoản/điểm GÕ TAY ở đầu đoạn (không phải đánh số tự động).
# r3 (lượt 2 B5): `(?!\d)` — thân mở bằng số thập phân (`1.5 lần`) không phải số gõ tay.
# r16 (lượt 15 R2): dạng ngoặc KÍN `(1)` là số gõ tay kể cả khi thân dính chữ số (`(1)5 lần`) — `(?!\d)` chỉ bảo vệ số thập phân
# của dạng `1.` / `1)`.
_RE_SO_GO_TAY_DOCX = re.compile(r"^(?:\(\s*\d+\s*\)|\(?\d+[^\S\n]*[.)](?!\d))")
# Phần tử khối được phép làm con của body / sdtContent mà không mang nội dung (bỏ qua). Phần tử khối KHÁC ⇒ mốc lạ.
_KHOI_BO_QUA = {"sectPr", "bookmarkStart", "bookmarkEnd", "proofErr", "permStart", "permEnd", "commentRangeStart",
                "commentRangeEnd", "customXmlPr", "sdtPr", "sdtEndPr",   # r3 (lượt 2 B6): thuộc tính wrapper
                "moveFromRangeStart", "moveFromRangeEnd", "moveToRangeStart", "moveToRangeEnd"}
# r3 (lượt 2 B1/B4, DANH SÁCH CHO PHÉP): con của `w:p` / `w:r` mà bộ đọc HIỂU. Phần tử khác ⇒ đoạn mang `la` ⇒ chặn trong vùng.
_MOC_MOVE = {"moveFromRangeStart", "moveFromRangeEnd", "moveToRangeStart", "moveToRangeEnd"}   # r7 F6: kiểm cân ở doc_dieu_docx
_CON_DOAN_BO_QUA = {"pPr", "bookmarkStart", "bookmarkEnd", "proofErr", "permStart", "permEnd", "commentRangeStart",
                    "commentRangeEnd"} | _MOC_MOVE
_CON_DOAN_DI_VAO = {"ins", "moveTo", "hyperlink", "smartTag", "customXml"}   # bọc run: đi vào nội dung
_CON_RUN_CHU = {"t": None, "tab": " ", "ptab": " ", "noBreakHyphen": "-", "softHyphen": ""}   # r7 F6: ptab   # phần tử → chữ hiển thị (None = .text)
_CON_RUN_BO_QUA = {"rPr", "lastRenderedPageBreak", "commentReference", "annotationRef"}
_TAT_OOXML = ("0", "false", "off")
_MC = "{http://schemas.openxmlformats.org/markup-compatibility/2006}"


# r22 (lượt 21 X2): TRƯỜNG ĐƠN TRỊ — mọi phần tử con mà bộ đọc lấy bằng `.find()` (phần tử ĐẦU) phải xuất hiện ≤ 1 lần; khai nhiều
# lần ⇒ mâu thuẫn, không đoán Word chọn cái nào. Part chính và styles ⇒ ValueError cả tệp; numbering ⇒ `loi` của định nghĩa (A5).
_DON_TRI_DOCUMENT = {"p": ("pPr",), "r": ("rPr",), "pPr": ("pStyle", "numPr", "rPr"), "numPr": ("numId", "ilvl"),
                     "rPr": ("rStyle", "strike", "dstrike"),
                     # r23 (lượt 22 Y2): nút CHỌN VÙNG cũng đơn trị — hai `body`, hai `sdtContent` ⇒ bộ đọc chỉ thấy phần đầu.
                     "document": ("body",), "sdt": ("sdtPr", "sdtEndPr", "sdtContent")}
_DON_TRI_STYLES = {"style": ("basedOn", "pPr", "rPr"), "pPr": ("numPr",), "numPr": ("numId", "ilvl"),
                   "rPr": ("strike", "dstrike"), "docDefaults": ("rPrDefault", "pPrDefault"), "rPrDefault": ("rPr",),
                   "pPrDefault": ("pPr",)}
_DON_TRI_LVL = ("start", "numFmt", "lvlText", "lvlRestart", "isLgl", "pStyle")


def _kiem_don_tri(goc, bang, ten_part):
    """r22 (lượt 21 X2): ValueError khi một phần tử con đơn trị (theo `bang`) xuất hiện nhiều lần."""
    for el in goc.iter():
        ten = str(el.tag)[len(_W):] if str(el.tag).startswith(_W) else None
        for con in bang.get(ten, ()):
            if len(el.findall(_W + con)) > 1:
                raise ValueError(f"{ten_part}: {ten} khai {con} nhieu lan — khong ho tro")


def _chan_mc(goc, ten_part):
    """r11 (lượt 10 K1): BẤT KỲ phần tử markup-compatibility (`mc:AlternateContent`…) ở đâu trong part ⇒ không giải được nhánh
    tương thích nào có hiệu lực (style, cấp, chữ) ⇒ dừng. Danh sách cho phép: không hỗ trợ `mc` ở mọi tầng."""
    if any(str(e.tag).startswith(_MC) for e in goc.iter()):
        raise ValueError(f"{ten_part} co phan tu markup-compatibility (mc:) — khong ho tro")


def _nap_doc_gioi_han():
    """`read_member_bounded` (chống zip-bomb) khi nạp được; None ⇒ dùng trần `_TRAN_XML` tại chỗ."""
    goc = str(Path(__file__).resolve().parents[1])
    if goc not in sys.path:
        sys.path.insert(0, goc)
    try:
        from tl_core.ingest_engine import read_member_bounded
    except Exception:  # noqa: BLE001
        read_member_bounded = None
    return read_member_bounded


def _doc_thanh_phan(z, ten, doc_gioi_han):
    if doc_gioi_han is not None:
        return doc_gioi_han(z, ten)
    with z.open(ten) as f:
        b = f.read(_TRAN_XML + 1)
    if len(b) > _TRAN_XML:
        raise ValueError(f"{ten} vuot tran {_TRAN_XML} byte")
    return b


def _gon_doan(s):
    return " ".join(str(s).split())


def _bat_ooxml(el):
    """Thuộc tính bật/tắt kiểu OOXML (`<w:strike/>` = bật; `w:val="0|false|off"` = tắt)."""
    return el is not None and el.get(_W + "val", "1") not in _TAT_OOXML


def _so_id(v):
    """r7 (lượt 6 F3): ID đánh số OOXML là SỐ NGUYÊN — `01` và `1` là một. Chuẩn hoá về chữ số thập phân.
    r8 (lượt 7 G1): CHỈ nhận chữ số thập phân ASCII (`int()` còn nhận `+1`, `1_0`, chữ số Unicode…); khác ⇒ None (không hợp lệ)."""
    v = str(v).strip() if v is not None else ""
    # r14 (lượt 13 N2): chuẩn hoá bằng CHUỖI (bỏ số 0 đầu) — `int()` ném ValueError với chuỗi quá trần độ dài của Python, làm hỏng
    # cả lần đọc dù định nghĩa ấy không được dùng (A5).
    return (v.lstrip("0") or "0") if re.fullmatch(r"[0-9]+", v) else None


def _so_nguyen(v):
    """r12 (lượt 11 L4): giá trị số nguyên OOXML; vắng hay sai dạng ⇒ ValueError (không để `TypeError` thoát ra)."""
    if v is None or not re.fullmatch(r"-?[0-9]+", str(v).strip()):
        raise ValueError(f"gia tri so nguyen OOXML khong hop le: {v!r}")
    return int(v)


_TRAN_SO = 999   # r7 (lượt 6 F4): trần SỐ THỨ TỰ (bộ đếm ≥ giá trị bắt đầu nên phủ cả `start`) — chặn nhãn chữ dài vô hạn


def _giai_quan_he(z, doc_gioi_han, tep_rels, thu_muc, loai, mac_dinh):
    """Part đích của quan hệ `loai` trong `tep_rels` (đường dẫn tương đối `thu_muc`). Không có tệp quan hệ ⇒ `mac_dinh`; không có
    quan hệ loại ấy ⇒ None; nhiều quan hệ, trỏ ra ngoài gói, hay part vắng ⇒ ValueError."""
    try:
        rels = _xml_cay(_doc_thanh_phan(z, tep_rels, doc_gioi_han))
    except KeyError:
        return mac_dinh
    ns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    # r12 (lượt 11 L1): so URI kiểu quan hệ ĐẦY ĐỦ (Transitional), không so hậu tố — quan hệ mở rộng trùng hậu tố bị bỏ qua.
    uri = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/" + loai
    dich = [r_ for r_ in rels.findall(ns + "Relationship") if str(r_.get("Type", "")).strip() == uri]
    if not dich:
        return None
    if len(dich) > 1 or dich[0].get("TargetMode") == "External":
        raise ValueError(f"quan he {loai} khong ho tro (nhieu hoac tro ra ngoai)")
    import posixpath
    t = dich[0].get("Target", "")
    ten = posixpath.normpath(t.lstrip("/") if t.startswith("/") else posixpath.join(thu_muc, t))
    if ten.startswith("..") or ten not in z.namelist():
        raise ValueError(f"part {loai} {t!r} khong co trong goi")
    return ten


def _phan_chinh(z, doc_gioi_han):
    """r9 (lượt 8 H2): part CHÍNH theo quan hệ gốc `_rels/.rels` (`officeDocument`) — không mở cứng `word/document.xml` (gói có thể
    đổi tên part chính và còn để bản XML cũ ở tên mặc định). Gói tối giản không có `_rels/.rels` ⇒ tên mặc định."""
    ten = _giai_quan_he(z, doc_gioi_han, "_rels/.rels", "", "officeDocument", "word/document.xml")
    if ten is None:
        raise ValueError("goi khong khai quan he officeDocument")
    return ten


def _phan_qua_quan_he(z, doc_gioi_han, loai, mac_dinh, chinh="word/document.xml"):
    """r8 (lượt 7 G2): tên part (numbering/styles) lấy từ tệp quan hệ của PART CHÍNH (r9: theo `_phan_chinh`) — tài liệu có thể đặt
    tên khác mặc định. Không có tệp quan hệ ⇒ tên mặc định. Quan hệ trỏ ra ngoài gói hay part vắng ⇒ ValueError. Không có quan hệ
    loại ấy ⇒ None."""
    import posixpath
    thu_muc, ten_chinh = posixpath.split(chinh)
    return _giai_quan_he(z, doc_gioi_han, posixpath.join(thu_muc, "_rels", ten_chinh + ".rels"), thu_muc, loai, mac_dinh)


def _doc_danh_so(z, doc_gioi_han, chinh="word/document.xml"):
    """numId → {"muc": {ilvl: (numFmt, lvlText, start)}, "loi": lý do không hỗ trợ | None}.

    r2 (lượt 1 A5): định nghĩa danh sách KHÔNG hỗ trợ không làm hỏng cả tài liệu — chỉ ghi `loi`, người gọi chặn khi Điều
    đích dùng danh sách ấy. Không hỗ trợ: `lvlOverride` ngoài `startOverride`, `w:lvlRestart`, `w:isLgl` (lượt 1 A2)."""
    ten = _phan_qua_quan_he(z, doc_gioi_han, "numbering", "word/numbering.xml", chinh)
    try:
        xml = _doc_thanh_phan(z, ten, doc_gioi_han) if ten else None
    except KeyError:
        return {}
    if xml is None:
        return {}
    goc = _xml_cay(xml)
    _chan_mc(goc, "numbering")
    truu_tuong = {}
    for an in goc.findall(_W + "abstractNum"):
        muc, loi = {}, None
        if an.find(_W + "numStyleLink") is not None:
            loi = "abstractNum numStyleLink khong ho tro"
        if an.find(_W + "styleLink") is not None:
            loi = "abstractNum styleLink khong ho tro"
        if any(k.endswith("}restartNumberingAfterBreak") and v not in _TAT_OOXML for k, v in an.attrib.items()):
            loi = "abstractNum restartNumberingAfterBreak (danh so lai sau ngat section) khong ho tro"   # r5 (lượt 4 D2)
        for lvl in an.findall(_W + "lvl"):
            try:   # r13 (lượt 12 M2): `w:ilvl` bắt buộc ở `lvl`; vắng/sai dạng ⇒ định nghĩa lỗi (chặn KHI DÙNG — A5)
                il = _so_nguyen(lvl.get(_W + "ilvl"))
            except ValueError as e:
                loi = loi or f"lvl: {e}"
                continue
            if il in muc:   # r20→r21 (lượt 20 W5): hai `w:lvl` cùng cấp ⇒ định nghĩa mâu thuẫn (chặn KHI DÙNG — A5)
                loi = loi or f"lvl cap {il} trung"
                continue
            if not 0 <= il <= 8:   # r6 (lượt 5 E6): miền cấp OOXML 0–8
                loi = loi or f"ilvl {il} ngoai mien 0-8"
                continue
            if any(len(lvl.findall(_W + t)) > 1 for t in _DON_TRI_LVL):   # r22 (lượt 21 X2): trường đơn trị khai nhiều lần
                loi = loi or f"cap {il}: truong don tri khai nhieu lan"
                continue
            fmt = lvl.find(_W + "numFmt")
            txt = lvl.find(_W + "lvlText")
            st = lvl.find(_W + "start")
            if lvl.find(_W + "lvlRestart") is not None or _bat_ooxml(lvl.find(_W + "isLgl")):
                loi = loi or f"cap {il}: lvlRestart/isLgl khong ho tro"
            if lvl.find(_W + "pStyle") is not None:   # r3 (lượt 2 B2): cấp gắn style chọn cấp hiển thị — chưa hỗ trợ
                loi = loi or f"cap {il}: lvl gan pStyle khong ho tro"
            try:   # r13 (lượt 12 M2): `start` lỗi ⇒ định nghĩa lỗi, chặn khi dùng (A5) — không ném lúc nạp
                bd = _so_nguyen(st.get(_W + "val")) if st is not None else 0
            except ValueError as e:
                loi = loi or f"cap {il}: start {e}"
                continue
            muc[il] = (fmt.get(_W + "val") if fmt is not None else "decimal",
                       (txt.get(_W + "val") or "") if txt is not None else "", bd)
        aid_an = _so_id(an.get(_W + "abstractNumId"))
        if aid_an is None:
            continue   # r8 (lượt 7 G1): abstractNumId không hợp lệ ⇒ không ghép được ⇒ danh sách trỏ tới nó bị chặn
        if aid_an in truu_tuong:
            loi = loi or f"abstractNumId {aid_an} trung sau chuan hoa"
        truu_tuong[aid_an] = (muc, loi)
    kq = {}
    for num in goc.findall(_W + "num"):
        nid = _so_id(num.get(_W + "numId"))
        aid = num.find(_W + "abstractNumId")
        if nid is None:
            continue
        if nid in kq:
            kq[nid] = {"muc": {}, "loi": f"numId {nid} trung sau chuan hoa"}
            continue
        if len(num.findall(_W + "abstractNumId")) > 1:   # r22 (lượt 21 X2)
            kq[nid] = {"muc": {}, "loi": f"numId {nid} khai abstractNumId nhieu lan"}
            continue
        if aid is None or _so_id(aid.get(_W + "val")) not in truu_tuong:
            kq[nid] = {"muc": {}, "loi": "numId khong tro abstractNum hop le"}
            continue
        muc, loi = truu_tuong[_so_id(aid.get(_W + "val"))]
        muc = dict(muc)
        da_ov = set()
        for ov in num.findall(_W + "lvlOverride"):
            try:   # r13 (lượt 12 M2): `w:ilvl` bắt buộc ở `lvlOverride`
                il = _so_nguyen(ov.get(_W + "ilvl"))
            except ValueError as e:
                loi = loi or f"lvlOverride: {e}"
                continue
            if not 0 <= il <= 8:
                loi = loi or f"lvlOverride ilvl {il} ngoai mien 0-8"
                continue
            if il in da_ov:   # r21 (lượt 20 W5): hai `lvlOverride` cùng cấp ⇒ mâu thuẫn
                loi = loi or f"lvlOverride cap {il} trung"
                continue
            da_ov.add(il)
            if [c.tag for c in ov] != [_W + "startOverride"]:
                loi = loi or f"lvlOverride cap {il} ngoai startOverride"
                continue
            fmt, txt, _ = muc.get(il, ("decimal", "", 0))
            try:
                muc[il] = (fmt, txt, _so_nguyen(ov.find(_W + "startOverride").get(_W + "val")))
            except ValueError as e:
                loi = loi or f"lvlOverride cap {il}: startOverride {e}"
        kq[nid] = {"muc": muc, "loi": loi}
    return kq


def _doc_kieu(z, doc_gioi_han, chinh="word/document.xml"):
    """styleId → (basedOn, numId|None, ilvl|None, strike|None, dstrike|None); khoá đặc biệt `""` = (docDefaults strike,
    dstrike, style đoạn mặc định). r3 (lượt 2 B3): gạch ĐƠN và gạch KÉP tính RIÊNG qua từng tầng, không gộp một cờ."""
    ten = _phan_qua_quan_he(z, doc_gioi_han, "styles", "word/styles.xml", chinh)
    try:
        goc = _xml_cay(_doc_thanh_phan(z, ten, doc_gioi_han)) if ten else None
    except KeyError:
        goc = None
    if goc is None:
        return {"": (None, None, None)}
    _chan_mc(goc, "styles")
    _kiem_don_tri(goc, _DON_TRI_STYLES, "styles")   # r22 (lượt 21 X2)

    def gach(rpr, ten):
        e = rpr.find(_W + ten) if rpr is not None else None
        return None if e is None else _bat_ooxml(e)
    kq = {}
    mac_dinh_doan = None
    for st in goc.findall(_W + "style"):
        b = st.find(_W + "basedOn")
        np_ = st.find(f"{_W}pPr/{_W}numPr")
        nid = il = None
        if np_ is not None:
            e = np_.find(_W + "numId")
            nid = (_so_id(e.get(_W + "val")) or "!") if e is not None else None   # r9 (lượt 8 H4): "!" = ID lỗi, khác vắng
            e = np_.find(_W + "ilvl")
            try:   # r13 (lượt 12 M2): ilvl lỗi ở style ⇒ "!" — chỉ chặn khi đoạn dùng style ấy CÓ đánh số
                il = _so_nguyen(e.get(_W + "val")) if e is not None else None
            except ValueError:
                il = "!"
        rpr = st.find(_W + "rPr")
        if not st.get(_W + "styleId") or st.get(_W + "styleId").startswith("#"):
            # r32 (lượt 31 H3): ID rỗng/vắng hay mở bằng `#` trùng miền KHOÁ NỘI BỘ của bảng (`""`, `#numPr_mac_dinh`, `#loai`) ⇒ từ chối.
            raise ValueError(f"styles: styleId {st.get(_W + 'styleId')!r} khong hop le (trung khoa noi bo) — khong ho tro")
        if st.get(_W + "styleId") in kq:   # r23 (lượt 22 Y2): hai style cùng `styleId` ⇒ định nghĩa sau ghi đè ngầm
            raise ValueError(f"styles: styleId {st.get(_W + 'styleId')!r} khai nhieu lan — khong ho tro")
        kq[st.get(_W + "styleId")] = (b.get(_W + "val") if b is not None else None, nid, il,
                                      gach(rpr, "strike"), gach(rpr, "dstrike"))
        # r32 (lượt 31 H1): loại HIỆU LỰC (vắng `w:type` ⇒ paragraph) — cùng quy tắc với bảng loại dưới.
        if (st.get(_W + "type") or "paragraph") == "paragraph" and st.get(_W + "default") in ("1", "true", "on"):
            mac_dinh_doan = st.get(_W + "styleId")
    dd = goc.find(f"{_W}docDefaults/{_W}rPrDefault/{_W}rPr")
    kq[""] = (gach(dd, "strike"), gach(dd, "dstrike"), mac_dinh_doan)
    # r20 (lượt 19 V2): đánh số khai ở MẶC ĐỊNH ĐOẠN (`docDefaults/pPrDefault/pPr/numPr`) — bộ đọc chỉ giải style → trực tiếp, nên số
    # kế thừa từ mặc định không vào bộ đếm ⇒ đánh dấu để `doc_dieu_docx` dừng (không đoán thứ tự hiệu lực của Word).
    kq["#numPr_mac_dinh"] = goc.find(f"{_W}docDefaults/{_W}pPrDefault/{_W}pPr/{_W}numPr") is not None
    # r31 (lượt 30 G1): LOẠI style (`w:type`, mặc định `paragraph`). Chuỗi `basedOn` đổi loại ⇒ ValueError (không đoán Word bỏ qua hay
    # không); điểm vào đoạn/run kiểm loại tại `_phan_tich_doan`.
    loai = {st.get(_W + "styleId"): (st.get(_W + "type") or "paragraph") for st in goc.findall(_W + "style")}
    for sid, ten_loai in loai.items():
        goc_sid = kq[sid][0]
        if goc_sid in loai and loai[goc_sid] != ten_loai:
            raise ValueError(f"styles: {sid!r} ({ten_loai}) basedOn {goc_sid!r} ({loai[goc_sid]}) khac loai — khong ho tro")
    kq["#loai"] = loai
    return kq


def _giai_chuoi(kieu, sid, chi_so, gop):
    """r36 (lượt 36, `can-tai-nguyen-doc-nguon`): MỘT bộ phân giải chuỗi `basedOn` có NHỚ cho MỌI hậu tố đã đi qua (kể cả kết quả
    vắng) — mỗi cạnh style đi tối đa một lần cho cả tệp. `gop`: "dau" = giá trị khác None đầu tiên; "dem" = số tầng bật. Vòng lặp ⇒
    ValueError (bảo thủ hơn bản cũ: vòng ở bất kỳ đâu trong chuỗi đều chặn)."""
    nho = kieu.setdefault("#nho", {})
    loai = kieu.get("#loai", {})   # r33 (lượt 32 I1): chỉ ID đã XÁC THỰC là định nghĩa (không trúng khoá nội bộ)
    duong, da = [], set()
    while sid and sid in loai and (sid, chi_so, gop) not in nho:
        if sid in da:
            raise ValueError(f"style {sid}: vong lap basedOn")
        da.add(sid)
        duong.append(sid)
        sid = kieu[sid][0]
    kq = nho[(sid, chi_so, gop)] if (sid, chi_so, gop) in nho else (None if gop == "dau" else 0)
    for x in reversed(duong):
        v = kieu[x][chi_so]
        kq = (v if v is not None else kq) if gop == "dau" else kq + (1 if v else 0)
        nho[(x, chi_so, gop)] = kq
    return kq


def _theo_kieu(kieu, sid, chi_so):
    """Giá trị hiệu lực theo chuỗi `basedOn` (chi_so: 1 numId, 2 ilvl, 3 strike, 4 dstrike). Vòng lặp ⇒ ValueError."""
    return _giai_chuoi(kieu, sid, chi_so, "dau")


def _dem_bat_trong_chuoi(kieu, sid, chi_so):
    """r6 (lượt 5 E2): SỐ tầng trong chuỗi `basedOn` bật thuộc tính toggle (gạch ngang)."""
    return _giai_chuoi(kieu, sid, chi_so, "dem")


def _chu_cai(n, hoa):
    """Nhãn chữ kiểu Word: a…z, rồi aa…zz, aaa… (LẶP một chữ — r4, lượt 3 C2; không phải kiểu cột bảng tính)."""
    if n <= 0:
        raise ValueError(f"so thu tu chu {n} khong hop le")
    s = chr(ord("a") + (n - 1) % 26) * ((n - 1) // 26 + 1)
    return s.upper() if hoa else s


def _nhan(muc, ilvl, bo_dem):
    """Nhãn hiển thị của một đoạn (vd `2.`, `a)`, `-`) từ `lvlText` + bộ đếm các cấp. Định dạng ngoài danh sách ⇒ ValueError."""
    fmt, txt, _ = muc[ilvl]
    if fmt == "bullet":
        return "-"

    def thay(m):
        k = int(m.group(1)) - 1
        if k not in muc or k > ilvl:
            raise ValueError(f"lvlText {txt!r} tro cap {k}")
        f, _, _ = muc[k]
        n = bo_dem[k]
        if n < 0:
            raise ValueError(f"so thu tu am {n} — khong ho tro")   # r36 (lượt 36): số âm không có hình dạng Word đã đo
        dai[0] += len(str(n)) if f == "decimal" else (max(n, 1) - 1) // 26 + 1
        if dai[0] > _TRAN_NHAN:
            raise ValueError(f"nhan mo rong dai hon {_TRAN_NHAN} ky tu — khong ho tro")   # r36: đo TRƯỚC khi dựng chuỗi
        if f == "decimal":
            return str(n)
        if f in ("lowerLetter", "upperLetter"):
            return _chu_cai(n, f == "upperLetter")
        raise ValueError(f"numFmt {f!r} khong ho tro")
    if fmt not in ("decimal", "lowerLetter", "upperLetter"):
        raise ValueError(f"numFmt {fmt!r} khong ho tro")
    # r17 (lượt 16 S2): khoảng trắng trong nhãn chỉ là dấu cách thường (không `\s` — tab, NBSP, NEL…).
    if len(txt) > _TRAN_NHAN or not re.fullmatch(r"(?:%[1-9]|[.)(\-– ])+", txt) or "%" not in txt:
        # r36 (lượt 35): kiểm độ dài TRƯỚC khi mở rộng; ngữ pháp một vế lặp (tuyến tính, không quay lui chéo hai vế).
        # r10 (lượt 9 J3) → r11 (lượt 10 K3): DANH SÁCH CHO PHÉP toàn chuỗi — chỉ placeholder `%N` (ít nhất một), các dấu `.` `)`
        # `(` `-` `–` và khoảng trắng; chữ, chữ số trần, `%` lẻ, ký tự vô hình ⇒ không hỗ trợ.
        raise ValueError(f"lvlText {txt!r} ngoai danh sach cho phep — khong ho tro")
    dai = [len(txt) - 2 * txt.count("%")]   # r36: độ dài phần dấu, cộng dần độ dài từng placeholder trước khi dựng
    nhan = re.sub(r"%(\d)", thay, txt)
    if not nhan.strip():
        raise ValueError("lvlText rong")
    return nhan.strip()


def _doan_trong(cha, trong_bang=False):
    """Duyệt khối theo THỨ TỰ tài liệu (r2, lượt 1 A1/A2): `w:p` ⇒ ("p", el, trong_bang); `w:tbl` ⇒ ("bang", …) rồi các
    đoạn trong ô (để ĐẾM số); `w:sdt`/`w:customXml` ⇒ đi vào nội dung; khối lạ ⇒ ("la", …) — không bỏ nội dung nào."""
    for el in cha:
        # r14 (lượt 13 N3): so QName ĐẦY ĐỦ — khối ngoài namespace Word (kể cả trùng tên cục bộ `p`/`sdt`/`customXml`) ⇒ khối lạ.
        ten = el.tag[len(_W):] if isinstance(el.tag, str) and el.tag.startswith(_W) else None
        if ten is None:
            yield ("la", el, trong_bang)
        elif ten == "p":
            yield ("p", el, trong_bang)
        elif ten == "tbl":
            # r7: tệp chỉ chứa Điều cần đọc ⇒ bảng ở BẤT KỲ đâu bị chặn; không cần duyệt ô để đếm số trước Điều.
            yield ("bang", el, trong_bang)
        elif ten == "sdt":
            # r23 (lượt 22 Y2): wrapper phải có ĐÚNG MỘT `sdtContent` (đơn trị, `_DON_TRI_DOCUMENT`) và không con lạ — thiếu nội dung
            # hay con ngoài {sdtPr, sdtEndPr, sdtContent} ⇒ khối lạ (trước đây thiếu `sdtContent` thì bỏ qua lặng lẽ).
            nd = el.find(_W + "sdtContent")
            if nd is None or not _sdt_hop_le(el):
                yield ("la", el, trong_bang)
            else:
                yield from _doan_trong(nd, trong_bang)
        elif ten == "customXml":
            yield from _doan_trong(el, trong_bang)
        elif ten not in _KHOI_BO_QUA:
            yield ("la", el, trong_bang)


def _sdt_hop_le(el):
    """r23 (lượt 22 Y2): con của `w:sdt` chỉ được là `sdtPr` / `sdtEndPr` / `sdtContent` (theo QName đầy đủ)."""
    return all(c.tag in (_W + "sdtPr", _W + "sdtEndPr", _W + "sdtContent") for c in el)


_XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"


def _danh_dau_giu_trang(goc):
    """r25 (lượt 24 A1): `xml:space` HIỆU LỰC (kế thừa từ tổ tiên, `default` đặt lại) cho từng `w:t`/`w:delText` — tập id các phần tử
    giữ khoảng trắng biên (`preserve`). Không `preserve` ⇒ Word BỎ khoảng trắng đầu/cuối của phần tử ấy."""
    giu = set()

    def di(el, gia):
        gia = el.get(_XML_SPACE, gia)
        if el.tag in (_W + "t", _W + "delText") and gia == "preserve":
            giu.add(id(el))
        for c in el:
            di(c, gia)
    di(goc, "default")
    return frozenset(giu)


_GIU_TRANG = {"tap": frozenset()}   # tập id do `doc_dieu_docx` đặt cho lần đọc hiện hành


def _chu_t(e):
    """r25 (lượt 24 A1): chữ HIỆU LỰC của `w:t`/`w:delText` — bỏ khoảng trắng XML ở hai biên khi `xml:space` hiệu lực không phải
    `preserve` (quy tắc Word, cùng r222)."""
    s = e.text or ""
    return s if id(e) in _GIU_TRANG["tap"] else s.strip(" \t\r\n")


def _ruot_bi_bo(el):
    """r22 (lượt 21 X1, chính sách r222 `chunk_payload`): chữ HIỂN THỊ của nội dung bị bỏ (`w:del`/`w:moveFrom`) — `t`/`delText` theo chữ,
    `tab`/`ptab`/`br`/`cr` là khoảng trắng, `noBreakHyphen` là `-`; phần tử khác bỏ qua."""
    # r24 (lượt 23 Z1): DANH SÁCH CHO PHÉP — chỉ phần tử ĐÃ BIẾT là khoảng trắng mới được tính là khoảng trắng; mọi con khác của run
    # (ký hiệu `w:sym`, trường, hình…) và mọi con không phải run của wrapper được tính là NỘI DUNG (`\x00`) ⇒ mẩu bị bỏ TRỌN.
    phan = []
    runs = [el] if el.tag == _W + "r" else None
    if runs is None:
        runs = []
        for c in el:
            if c.tag == _W + "r":
                runs.append(c)
            else:
                phan.append("\x00")
    for r in runs:
        for e in r:
            ten = e.tag[len(_W):] if isinstance(e.tag, str) and e.tag.startswith(_W) else None
            if ten in ("t", "delText"):
                phan.append(_chu_t(e))   # r25 (lượt 24 A1)
            elif ten in ("tab", "ptab", "br", "cr"):
                phan.append(" ")
            elif ten == "noBreakHyphen":
                phan.append("-")
            elif ten == "softHyphen" or ten in _CON_RUN_BO_QUA:
                continue
            else:
                phan.append("\x00")
    return "".join(phan)


def _phan_tich_doan(p, kieu):
    """dict của một đoạn (XML GỐC — r5 lọc chữ đã bỏ ngay tại đây): chu, so (numId, ilvl)|None, so_tu_style, ngat, la.

    r3 (lượt 2): duyệt TƯỜNG MINH theo danh sách cho phép (`_CON_DOAN_*`, `_CON_RUN_*`) thay cho `iter()` — phần tử không hiểu
    (ký hiệu `w:sym`, trường `w:fldChar`, hình, chú thích, `mc:AlternateContent`…) ⇒ `la` (B4). Gạch đơn/kép tính RIÊNG qua
    docDefaults → style đoạn (mặc định nếu vắng) → style ký tự → định dạng trực tiếp (B3)."""
    ppr = p.find(_W + "pPr")
    ps = ppr.find(_W + "pStyle") if ppr is not None else None
    psid = ps.get(_W + "val") if ps is not None else kieu.get("", (None, None, None))[2]
    mac = kieu.get("", (None, None, None))
    # r6 (lượt 5 E2): gạch là TOGGLE — nhiều tầng bật có thể đảo nhau. ĐẾM số tầng bật (docDefaults + chuỗi style đoạn +
    # chuỗi style ký tự): 0 ⇒ tắt, 1 ⇒ bật (bỏ chữ), ≥2 ⇒ KHÔNG giải được ⇒ đoạn "lạ" (chặn nếu nằm trong Điều). Định dạng TRỰC
    # TIẾP trên run là tuyệt đối.
    dem_nen = {t: (1 if mac[k] else 0) + _dem_bat_trong_chuoi(kieu, psid, 3 if t == "strike" else 4)
               for k, t in ((0, "strike"), (1, "dstrike"))}
    # r30 (lượt 29 F2): `pStyle` trỏ style KHÔNG CÓ trong part styles — Word lùi về style đoạn mặc định (có thể mang gạch), bộ đọc thì
    # coi như không style ⇒ chữ gạch có thể lọt. Không đoán fallback: đoạn ấy là "lạ" (chặn nếu nằm trong Điều).
    # r31 (lượt 30 G1): ID có mà SAI LOẠI (không phải paragraph style) cũng là tham chiếu không phân giải được.
    loai_kieu = kieu.get("#loai", {})
    kq = {"phan": [], "ngat": False, "la": ps is not None and loai_kieu.get(psid) != "paragraph",   # r33 (lượt 32 I1): tra trên ID đã xác thực
          "sau_ngat_trang": False}

    def run(r):
        rpr = r.find(_W + "rPr")
        dem = dict(dem_nen)
        truc_tiep = {}
        if rpr is not None:
            rs = rpr.find(_W + "rStyle")
            if rs is not None and rs.get(_W + "val") in loai_kieu and loai_kieu[rs.get(_W + "val")] != "character":
                kq["la"] = True   # r31 (lượt 30 G1): `rStyle` trỏ style KHÁC loại character ⇒ không đoán Word áp hay bỏ
            if rs is not None:
                for t, ci in (("strike", 3), ("dstrike", 4)):
                    dem[t] += _dem_bat_trong_chuoi(kieu, rs.get(_W + "val"), ci)
            for t in ("strike", "dstrike"):
                if rpr.find(_W + t) is not None:
                    truc_tiep[t] = _bat_ooxml(rpr.find(_W + t))
        hl = {}
        for t in ("strike", "dstrike"):
            if t in truc_tiep:
                hl[t] = truc_tiep[t]
            elif dem[t] > 1:
                kq["la"] = True   # toggle nhiều tầng: không xác định được chữ có bị gạch không
                hl[t] = False
            else:
                hl[t] = dem[t] == 1
        # r26 (lượt 25 B3): trạng thái NGẮT của run chỉ ghi vào đoạn SAU khi biết run còn hiệu lực (run gạch bị bỏ trọn — kể cả
        # ngắt của nó, §2.25 Y1).
        chu_run, chu_sau_ngat, ngat_mem, sau_trang, la_run = [], False, False, kq["sau_ngat_trang"], False
        for c in r:
            ten = c.tag[len(_W):] if c.tag.startswith(_W) else None
            if ten in _CON_RUN_CHU:
                chu = _chu_t(c) if _CON_RUN_CHU[ten] is None else _CON_RUN_CHU[ten]   # r25 (lượt 24 A1): `xml:space` hiệu lực
                if sau_trang and chu.strip():
                    chu_sau_ngat = True   # r9 (lượt 8 H5); r10 (lượt 9 J5): chỉ tính khi run KHÔNG bị gạch (xét bên dưới)
                chu_run.append(chu)
            elif ten in ("br", "cr"):
                chu_run.append(" ")
                if c.get(_W + "type") not in ("page", "column"):
                    ngat_mem = True
                else:
                    sau_trang = True   # r8 (lượt 7 G4): ngắt TRANG/CỘT ở CUỐI đoạn là trình bày
            elif ten in ("delText",):
                # chữ đã xoá (track changes) — không vào nguyên văn; r22 (lượt 21 X1, lưới phụ r222): `delText` lạc chỉ có khoảng
                # trắng ⇒ giữ khoảng trắng.
                if _chu_t(c) and not _chu_t(c).strip():   # r25 (lượt 24 A1): theo `xml:space` hiệu lực
                    chu_run.append(_chu_t(c))
                continue
            elif ten in _CON_RUN_BO_QUA:
                continue
            else:
                la_run = True   # B4: phần tử hiển thị chưa hiểu ⇒ không biết chữ thật; r27 (lượt 26 C2): ghi vào đoạn SAU khi biết run còn
                # hiệu lực (run gạch bị bỏ TRỌN — phần tử lạ trong nó đã được `_ruot_bi_bo` tính là nội dung)
        if hl["strike"] or hl["dstrike"]:
            # r5 (lượt 4 D3): chữ GẠCH NGANG hiệu lực (gạch đơn/kép, mọi tầng, theo namespace) là chữ ĐÃ BỎ của dự thảo ⇒ bỏ,
            # như `tl extract --markup strip` — nhưng lọc theo CÂY, không qua regex của `docx_markup` (regex có thể nuốt ranh
            # giới đoạn khi run rỗng tự đóng đứng trước run gạch).
            # r21 (lượt 20 W2; chính sách r222 của `docx_markup`): run gạch mà ruột CHỈ có khoảng trắng là tàn dư định dạng — giữ
            # khoảng trắng, kẻo hai từ hiệu lực hai bên DÍNH thành một chữ không có trong văn bản.
            ruot = _ruot_bi_bo(r)   # r23 (lượt 22 Y1): CÙNG phép đọc ruột với `del`/`moveFrom` — tính cả `delText` có chữ
            if ruot and not ruot.strip():
                kq["phan"].append(ruot)
            return
        if la_run:
            kq["la"] = True
        if ngat_mem:
            kq["ngat"] = True
        kq["sau_ngat_trang"] = sau_trang
        if chu_sau_ngat:
            kq["ngat"] = True   # có chữ HIỆU LỰC sau ngắt trang/cột ⇒ có thể che số khoản gõ tay ⇒ như ngắt mềm
        kq["phan"].extend(chu_run)

    def duyet(cha):
        for c in cha:
            ten = c.tag[len(_W):] if c.tag.startswith(_W) else None
            if ten == "r":
                run(c)
            elif ten in _CON_DOAN_DI_VAO:
                duyet(c)
            elif ten == "sdt":   # r4 (lượt 3 C5): content control NỘI DÒNG — đi vào nội dung, bỏ thuộc tính
                nd = c.find(_W + "sdtContent")
                if nd is None or not _sdt_hop_le(c):   # r23 (lượt 22 Y2)
                    kq["la"] = True
                else:
                    duyet(nd)
            elif ten in ("del", "moveFrom"):
                # nội dung đã xoá/chuyển đi — không vào nguyên văn; r21 (lượt 20 W2, chính sách r222): ruột CHỈ có khoảng trắng
                # ⇒ giữ khoảng trắng (không để hai từ hai bên dính lại).
                ruot = _ruot_bi_bo(c)   # r22 (lượt 21 X1): tab/ngắt trong ruột cũng là phân cách
                if ruot and not ruot.strip():
                    kq["phan"].append(ruot)
                continue
            elif ten in _CON_DOAN_BO_QUA or ten in ("customXmlPr", "smartTagPr", "sdtPr", "sdtEndPr"):
                continue
            else:
                kq["la"] = True
    duyet(p)
    # numPr HIỆU LỰC: trực tiếp đè style (theo basedOn); numId "0" = tắt.
    nid, il = _theo_kieu(kieu, psid, 1), _theo_kieu(kieu, psid, 2)
    # r10 (lượt 9 J1): style mang BẤT KỲ thuộc tính đánh số nào (numId hay ilvl) ⇒ cấp/danh sách hiệu lực phụ thuộc quy tắc
    # style↔cấp của Word — đoạn đánh số dùng style ấy bị chặn trong Điều, kể cả khi numId khai trực tiếp.
    tu_style = nid is not None or il is not None
    np_ = ppr.find(_W + "numPr") if ppr is not None else None
    if np_ is not None:
        e = np_.find(_W + "numId")
        if e is not None:
            nid = _so_id(e.get(_W + "val"))
            if nid is None:
                kq["la"] = True   # r8 (lượt 7 G1): numId không hợp lệ ⇒ không biết danh sách
        e = np_.find(_W + "ilvl")
        il = _so_nguyen(e.get(_W + "val")) if e is not None else il   # r13 (lượt 12 M2): vắng/sai dạng ⇒ ValueError
    if nid == "!":
        kq["la"], nid = True, None   # r9 (lượt 8 H4): numId lỗi khai qua style ⇒ đoạn lạ
    # r10 (lượt 9 J2) → r11 (lượt 10 K1): phần tử `mc:` ở rPr/pPr nay bị `_chan_mc` chặn cho CẢ part.
    if il == "!":
        if nid not in (None, "0"):
            raise ValueError("style co ilvl khong hop le tren doan danh so")   # r13 (lượt 12 M2)
        il = None
    so = None if nid in (None, "0") else (nid, il or 0)
    # r7 (lượt 6 F5): cấp ngoài miền ở ĐOẠN không cần chốt riêng — chỉ đếm khi cấp có trong định nghĩa (đã giới hạn 0–8),
    # và bước xác thực chặn đoạn trỏ cấp không có định nghĩa.
    tho = "".join(kq["phan"])
    return {"chu": _gon_doan(tho), "ky_tu_la": _ky_tu_la(tho), "so": so, "so_tu_style": tu_style and so is not None,
            "ngat": kq["ngat"], "la": kq["la"]}


def doc_dieu_docx(nguon, dieu):
    """Đọc Điều `dieu` từ .docx (`nguon`: đường dẫn hoặc bytes). Trả dict `van_ban`, `khoan`, `cau_dan`:

    - `khoan`: `[(so, văn bản khoản, đầu khoản)]`, `so` = số Word hiển thị (liên tục từ 1); điểm nối vào khoản bằng `\\n`,
      mang nhãn từ cấu trúc (`a) …`, `- …`); `đầu khoản` = chữ của đoạn mở khoản (lượt 1 A3: dò từ nối CHỈ ở đó).
    - `van_ban`: tiêu đề + câu dẫn + các khoản có nhãn — đưa cho model.
    - `cau_dan`: các đoạn KHÔNG đánh số đứng trước khoản đầu (người gọi xác thực — hàm này không quyết câu dẫn).

    Ném `ValueError` khi cấu trúc mơ hồ/không hỗ trợ — kể cả khi Điều không có đánh số tự động (r5, lượt 4 D1: không lùi về
    đường thô, vì ranh giới cuối Điều trong .docx không đánh số chỉ có bằng chứng tiền tố)."""
    doc_gioi_han = _nap_doc_gioi_han()
    import io
    # r36 → r38 (lượt 37): đo byte và mở gói trên CÙNG một handle; đếm entry từ bản ghi EOCD TRƯỚC khi `ZipFile` nạp thư mục trung tâm.
    with (io.BytesIO(nguon) if isinstance(nguon, (bytes, bytearray)) else open(nguon, "rb")) as fh:
        co = fh.seek(0, 2)
        if co > _TRAN_GOI:
            raise ValueError(f"goi .docx {co} byte vuot tran {_TRAN_GOI} — khong ho tro")
        n_entry = _dem_entry_zip(fh, co)
        if n_entry > _TRAN_MEMBER:
            raise ValueError(f"goi .docx co {n_entry} member vuot tran {_TRAN_MEMBER} — khong ho tro")
        fh.seek(0)
        z_cm = zipfile.ZipFile(fh)
        return _doc_dieu_docx_goi(z_cm, dieu, doc_gioi_han)


def _dem_entry_zip(fh, co):
    """r38 → r39 (lượt 38): số entry THẬT của thư mục trung tâm, đếm TUẦN TỰ từng bản ghi (`PK\\x01\\x02`, 46 byte cố định + tên + extra
    + comment) trên đúng vùng mà `zipfile` sẽ đọc (`EOCD - kích thước CD`), dừng ngay khi vượt `_TRAN_MEMBER` — TRƯỚC khi `ZipFile`
    cấp phát metadata. Không thấy EOCD, có locator ZIP64, vùng CD ngoài tệp, bản ghi hỏng, hay số đếm lệch số khai ⇒ ValueError."""
    doc = min(co, 22 + 65535)
    fh.seek(co - doc)
    b = fh.read(doc)
    i = b.rfind(b"PK\x05\x06")
    if i < 0 or len(b) < i + 22:
        raise ValueError("goi .docx khong co ban ghi EOCD — khong phai ZIP hop le")
    vt_eocd = co - doc + i
    n_khai = int.from_bytes(b[i + 10:i + 12], "little")
    co_cd = int.from_bytes(b[i + 12:i + 16], "little")
    co_loc = False
    if vt_eocd >= 20:
        # r40 (lượt 39): locator ZIP64 đọc ở VỊ TRÍ TUYỆT ĐỐI ngay trước EOCD trên cùng handle (như `zipfile._EndRecData64`), không
        # trong cửa sổ đã đọc — EOCD sát đầu cửa sổ (comment dài) từng làm locator nằm ngoài phần được soi.
        fh.seek(vt_eocd - 20)
        co_loc = fh.read(4) == b"PK\x06\x07"
    if n_khai == 0xFFFF or co_cd == 0xFFFFFFFF or co_loc:
        raise ValueError("goi .docx dang ZIP64 — khong ho tro")
    dau = vt_eocd - co_cd
    if dau < 0:
        raise ValueError("thu muc trung tam ZIP nam ngoai tep")
    fh.seek(dau)
    n, vt = 0, dau
    while vt < vt_eocd:
        h = fh.read(46)
        if len(h) < 46 or h[:4] != b"PK\x01\x02":
            raise ValueError("ban ghi thu muc trung tam ZIP hong")
        n += 1
        if n > _TRAN_MEMBER:
            return n
        them = int.from_bytes(h[28:30], "little") + int.from_bytes(h[30:32], "little") + int.from_bytes(h[32:34], "little")
        vt += 46 + them
        fh.seek(vt)
    if vt != vt_eocd or n != n_khai:
        raise ValueError(f"thu muc trung tam ZIP khong nhat quan (dem {n}, khai {n_khai})")
    return n


def _doc_dieu_docx_goi(z_cm, dieu, doc_gioi_han):
    """Phần thân của `doc_dieu_docx` sau khi gói đã qua trần byte/entry (r38 tách ra để đọc trên một handle)."""
    with z_cm as z:
        # r24 (lượt 23 Z2): tên member TRÙNG trong thư mục ZIP ⇒ đọc theo tên chỉ lấy MỘT bản ngầm ⇒ dừng (cả gói).
        _ten = z.namelist()
        if len(_ten) > _TRAN_MEMBER:
            raise ValueError(f"goi .docx co {len(_ten)} member vuot tran {_TRAN_MEMBER} — khong ho tro")
        if len(_ten) != len(set(_ten)):
            raise ValueError("goi .docx co member trung ten — khong ho tro")
        chinh = _phan_chinh(z, doc_gioi_han)
        goc_xml = _doc_thanh_phan(z, chinh, doc_gioi_han)   # r12 (lượt 11 L5): BYTES — parser tự đọc khai báo mã hoá
        danh_so = _doc_danh_so(z, doc_gioi_han, chinh)
        kieu = _doc_kieu(z, doc_gioi_han, chinh)
    if kieu.get("#numPr_mac_dinh"):
        raise ValueError("styles co danh so o mac dinh doan (docDefaults/pPrDefault/numPr) — khong ho tro")   # r20 (lượt 19 V2)
    goc_cay = _xml_cay(goc_xml)
    _chan_mc(goc_cay, "document")
    _kiem_don_tri(goc_cay, _DON_TRI_DOCUMENT, "document")   # r22 (lượt 21 X2)
    _GIU_TRANG["tap"] = _danh_dau_giu_trang(goc_cay)   # r25 (lượt 24 A1)
    if goc_cay.tag != _W + "document":
        # r5 (lượt 4 D5): .docx Strict (namespace purl.oclc.org) hay tệp lạ — giới hạn đã khai.
        raise ValueError("document.xml khong phai WordprocessingML Transitional (vd .docx Strict) — luu lai dang Word Document")
    # r2 (lượt 1 A4): sửa đổi DẤU ĐOẠN (gộp/tách đoạn bằng track-changes) — bộ lọc bỏ dấu nhưng giữ hai `w:p` ⇒ ranh giới
    # đoạn KHÔNG còn là ranh giới thật. Đo trên XML GỐC, theo namespace (mọi tiền tố).
    for rpr in goc_cay.iter(_W + "rPr"):
        if any(c.tag in (_W + "del", _W + "ins", _W + "moveFrom", _W + "moveTo") for c in rpr):
            raise ValueError("tai lieu co sua doi dau doan (track changes gop/tach doan) — ranh gioi doan khong tin duoc")
    for loai in ("moveFrom", "moveTo"):
        # r7 (lượt 6 F6): mốc phạm vi move phải CÂN theo id — mốc lẻ ⇒ thay đổi cấu trúc không xác định ⇒ dừng.
        dau = [e.get(_W + "id") for e in goc_cay.iter(_W + loai + "RangeStart")]
        cuoi = [e.get(_W + "id") for e in goc_cay.iter(_W + loai + "RangeEnd")]
        if None in dau or None in cuoi:   # r13 (lượt 12 M2): mốc thiếu `w:id` ⇒ không so được (sorted None/str ném TypeError)
            raise ValueError(f"moc pham vi {loai} thieu w:id")
        dau, cuoi = sorted(dau), sorted(cuoi)
        if dau != cuoi:
            raise ValueError(f"moc pham vi {loai} khong can (start {dau} / end {cuoi})")
    body = goc_cay.find(_W + "body")
    if body is None:
        raise ValueError("document.xml khong co w:body")
    # Đi theo thứ tự tài liệu, ĐẾM số ở MỌI đoạn đánh số (kể cả trong bảng/sdt) — bộ đếm Word chạy suốt tài liệu theo numId.
    bo_dem_tl = {}
    doan = []   # dict: chu, so (numId, ilvl)|None, dem, loai ("p"|"bang"|"la"), trong_bang, ngat, la, so_tu_style
    tong_doan = [0]
    for loai, el, trong_bang in _doan_trong(body):
        if loai != "p":
            doan.append({"chu": "", "so": None, "dem": None, "loai": loai, "trong_bang": trong_bang,
                         "ngat": False, "la": loai == "la", "so_tu_style": False, "ky_tu_la": None})
            continue
        pt = _phan_tich_doan(el, kieu)
        tong_doan[0] += len(pt["chu"])
        if tong_doan[0] > _TRAN_VAN_BAN:
            # r38 (lượt 37): tệp chỉ chứa Điều cần đọc ⇒ chữ hiệu lực cộng dồn NGAY khi phân tích từng đoạn, không đợi lưu hết.
            raise ValueError(f"Dieu trong .docx vuot tran {_TRAN_VAN_BAN} ky tu — khong ho tro")
        so = pt["so"]
        dem_snap = None
        if so is not None:
            nid, il = so
            dn = danh_so.get(nid)
            if dn is not None and dn["loi"] is None and il in dn["muc"]:
                muc = dn["muc"]
                dem = bo_dem_tl.setdefault(nid, {})
                dem[il] = dem.get(il, muc[il][2] - 1) + 1
                if dem[il] > _TRAN_SO or dem[il] < 0:   # r38 (lượt 37): miền 0.._TRAN_SO chốt NGAY khi cập nhật, mọi kiểu cấp
                    raise ValueError(f"so thu tu numId {nid} cap {il} vuot {_TRAN_SO}")   # r7 (lượt 6 F4)
                for k in [k for k in dem if k > il]:
                    del dem[k]
                if any(k not in dem for k in range(il)):
                    # r8 (lượt 7 G1/G3): NHẢY cấp (cấp tổ tiên chưa có mục) — Word dựng nhãn tổ tiên từ giá trị khởi tạo, cách hiển
                    # thị chưa đo được và giá trị ấy đi vòng qua trần số ⇒ không đoán.
                    raise ValueError(f"numId {nid}: doan cap {il} nhay qua cap chua co muc")
                dem_snap = dict(dem)
        doan.append({**pt, "dem": dem_snap, "loai": "p", "trong_bang": trong_bang})
    # r7 (lượt 6 F1, quyết định chủ kho "Docx must contain only that Article"): tệp chứa ĐÚNG Điều cần đọc — đoạn có nội dung
    # ĐẦU TIÊN là tiêu đề `Điều <dieu>.`, vùng là TOÀN BỘ phần sau tới hết tài liệu. KHÔNG đoán điểm kết thúc Điều (bốn lượt
    # liền, mọi luật cắt theo tiền tố đều bị một đoạn trích giống tiêu đề đánh lừa).
    if any(d["loai"] != "p" or d["trong_bang"] for d in doan):
        raise ValueError("tep co bang hoac khoi khong ho tro")
    for d in doan:
        # r17 (lượt 16 S2) → r35 (lượt 34, lớp `ranh-gioi-ky-tu`): kiểm chữ GỐC (trước gộp khoảng trắng) trên MỌI đoạn, TRƯỚC khi bỏ
        # đoạn rỗng hay chọn tiêu đề — đoạn chỉ có khoảng trắng ngoài danh sách gộp thành rỗng và từng thoát cả hai bước.
        la = d["ky_tu_la"]
        if la:   # r16 (lượt 15 R1): từ chối thay cho chuẩn hoá
            raise ValueError(f"Dieu co {la} — chu khong doc an toan duoc: {d['chu'][:60]!r}")
    co_nd = [i for i, d in enumerate(doan) if d["chu"] or d["so"] is not None or d["la"]]
    if not co_nd:
        raise ValueError("tep khong co noi dung")
    i0 = co_nd[0]
    re_dau = re.compile(rf"^Điều\s+{re.escape(str(dieu))}\s*[.:]", re.IGNORECASE)   # r8 (lượt 7 G6): như `_RE_TIEU_DE_TRON`
    if not re_dau.match(doan[i0]["chu"]):
        raise ValueError(f"doan dau tien cua tep phai la tieu de 'Dieu {dieu}.' (tep chi chua dung Dieu can doc): "
                         f"{doan[i0]['chu'][:60]!r}")
    if doan[i0]["so"] is not None:
        raise ValueError("doan tieu de Dieu duoc danh so tu dong")
    if doan[i0]["ngat"]:
        raise ValueError("doan tieu de Dieu co ngat dong mem")   # r4 (lượt 3 C1): kể cả khi chữ khớp mẫu tiêu đề
    if not _RE_TIEU_DE_TRON.match(doan[i0]["chu"]):
        # r3 (lượt 2 B1): tiêu đề DÍNH thân khoản — cùng danh sách cho phép với đường thô (`Điều N.` / `… Giải thích từ ngữ`).
        raise ValueError(f"tieu de Dieu ngoai hinh dang cho phep: {doan[i0]['chu'][:60]!r}")
    if doan[i0]["la"]:
        raise ValueError("tieu de Dieu co phan tu khong ho tro")   # r5 (lượt 4 D4)
    vung = doan[i0 + 1:]
    if any(_mo_bang_dieu(d["chu"]) or _RE_RANH_GIOI_LON.match(_dau_doan(d["chu"])) for d in vung):
        raise ValueError("tep chua them tieu de Dieu/Chuong/Muc/Phan — chi de dung Dieu can doc trong tep")
    if any(d["la"] for d in vung):
        raise ValueError("Dieu co phan tu khong ho tro (ky hieu, truong, hinh, chu thich…) — khong biet chu that")
    if any(d["ngat"] for d in vung):
        # r3 (lượt 2 B1): ngắt dòng mềm trong đoạn có thể che ranh giới khoản.
        raise ValueError("Dieu co ngat dong mem trong doan — ranh gioi khoan khong tin duoc")
    if any(d["so"] is not None and not d["chu"] for d in vung):
        raise ValueError("doan danh so tu dong rong trong Dieu")   # r3 (lượt 2 B1): quyết TRƯỚC khi bỏ đoạn rỗng
    if any(d["so_tu_style"] for d in vung):
        # r3 (lượt 2 B2/B8): cấp hiển thị của đánh số qua style phụ thuộc liên kết style↔cấp — giới hạn đã khai.
        raise ValueError("doan trong Dieu danh so qua style (khong co numId truc tiep) — khong ho tro")
    vung = [d for d in vung if d["chu"]]   # bỏ đoạn rỗng
    if sum(len(d["chu"]) for d in vung) > _TRAN_VAN_BAN:
        # r36 (lượt 35): chốt tổng chữ SỚM, trước khi mở rộng nhãn và dựng chuỗi khoản (chốt cuối vẫn đo cả nhãn).
        raise ValueError(f"Dieu trong .docx vuot tran {_TRAN_VAN_BAN} ky tu — khong ho tro")
    tieu_de = doan[i0]["chu"]
    co_so = [d for d in vung if d["so"] is not None]
    if not co_so:
        raise ValueError(f"Dieu {dieu} khong co doan danh so tu dong — dung tep van ban (--tep .txt) cho duong tho")
    for d in co_so:   # lượt 1 A5: chỉ xác thực các danh sách Điều đích DÙNG
        nid, il = d["so"]
        dn = danh_so.get(nid)
        if dn is None or il not in dn.get("muc", {}):
            raise ValueError(f"doan tro numId {nid} ilvl {il} khong co trong numbering.xml")
        if dn["loi"]:
            raise ValueError(f"numId {nid}: {dn['loi']}")
    cap0 = min(d["so"][1] for d in co_so)
    nid0 = co_so[0]["so"][0]
    muc0 = danh_so[nid0]["muc"]
    fmt0, txt0, _ = muc0[cap0]
    if fmt0 != "decimal" or not re.fullmatch(rf"%{cap0 + 1}[.)]", txt0):
        # lượt 1 A2: nhãn khoản phải CHÍNH LÀ số của cấp khoản (`%N.`/`%N)`), không cố định/ghép cấp khác.
        raise ValueError(f"cap khoan co numFmt {fmt0!r}, lvlText {txt0!r} (can decimal, '%{cap0 + 1}.')")
    cau_dan, khoan = [], []
    con = [_TRAN_VAN_BAN - len(tieu_de)]   # r36 (lượt 36): NGÂN SÁCH trừ dần khi thêm từng dòng/nhãn/phân cách, trước khi dựng

    def tieu(n):
        con[0] -= n
        if con[0] < 0:
            raise ValueError(f"Dieu dung tu .docx vuot tran {_TRAN_VAN_BAN} ky tu — khong ho tro")
    for d in vung:
        chu = d["chu"]
        if d["so"] is None:
            if not khoan:
                tieu(1 + len(chu))
                cau_dan.append(chu)   # trước khoản đầu: không phải khoản theo cấu trúc
            else:
                # đoạn KHÔNG đánh số sau khoản đầu: khoản mất số, tiếp dòng, lời dẫn nhóm hay điểm GÕ TAY (r7, lượt 6 F2: dấu
                # điểm gõ tay không đủ phân biệt điểm thật với định nghĩa riêng) ⇒ không đoán. Điểm phải là cấp con tự động.
                raise ValueError(f"doan khong danh so sau khoan dau (diem phai danh so tu dong): {chu[:60]!r}")
            continue
        nid, il = d["so"]
        if _RE_SO_GO_TAY_DOCX.match(chu):
            raise ValueError(f"doan danh so tu dong con mang so go tay: {chu[:60]!r}")
        if il == cap0 and nid == nid0:
            tieu(1 + len(f"{d['dem'][cap0]}. ") + len(chu))
            khoan.append([d["dem"][cap0], [chu], chu])   # r35: gom dòng, nối MỘT lần (không sao chép lặp chuỗi khoản)
        elif nid == nid0 and il > cap0 and khoan:
            nhan = _nhan(muc0, il, d['dem'])
            tieu(1 + len(nhan) + 1 + len(chu))   # r38 (lượt 37): trừ ngân sách TRƯỚC khi ghép dòng điểm
            khoan[-1][1].append(f"{nhan} {chu}")
        else:
            # cấp khoản của danh sách KHÁC, cấp con của danh sách khác, hay cấp con trước khoản đầu ⇒ ranh giới không rõ.
            raise ValueError("doan danh so khong thuoc danh sach khoan (hoac cap con truoc khoan dau)")
    if [so for so, _, _ in khoan] != list(range(1, len(khoan) + 1)):
        raise ValueError(f"so khoan khong lien tuc tu 1: {[so for so, _, _ in khoan]}")
    khoan = [(so, "\n".join(cac), dau) for so, cac, dau in khoan]
    dong = [tieu_de, *cau_dan] + [f"{so}. {txt}" for so, txt, _ in khoan]
    return {"van_ban": "\n".join(dong), "khoan": [(so, txt, dau) for so, txt, dau in khoan], "cau_dan": cau_dan,
            "chu_doan": [d["chu"] for d in vung]}


PHAM_VI_KIEM_CAU_TRUC = ("thuat ngu va dinh nghia khop nguyen van tung khoan; ranh gioi khoan doc tu CAU TRUC danh sach "
                         "danh so cua .docx (w:numPr) — can nguoi duyet")


def doc_dieu_cau_truc(nguon, dieu):
    """#1525: Điều `dieu` từ .docx theo cấu trúc danh sách đánh số. Trả `(van_ban, khoan)` — `khoan` dùng cho
    `lech_nguyen_van`. Ném `ValueError` khi cấu trúc mơ hồ/không hỗ trợ hoặc Điều không có đánh số tự động. Câu dẫn (đoạn không số trước khoản đầu) phải là ĐÚNG MỘT câu dẫn chuẩn hoặc vắng."""
    kq = doc_dieu_docx(nguon, dieu)
    for chu in kq["chu_doan"]:
        # r4 (lượt 3 C3): cùng chốt dấu phân cách mơ hồ với đường thô — `_quet` không nhận cặp dấu ngoài danh sách nên "là"
        # trong `[…]`/`«…»` có thể bị lấy làm từ nối cấp khoản. Đo trên CHỮ đoạn (nhãn tự động không nằm trong chữ).
        # r7: không còn điểm gõ tay ⇒ đo nguyên chữ đoạn (nhãn tự động không nằm trong chữ).
        if _dong_mo_ho(chu):
            raise ValueError(f"doan co dau ngoac/trich dan mo ho: {chu[:60]!r}")
    cd = kq["cau_dan"]
    if len(cd) > 1 or (cd and not _RE_CAU_DAN_TRON.fullmatch(" ".join(cd[0].split()))):
        raise ValueError(f"doan khong danh so truoc khoan dau khong phai cau dan chuan: {cd}")
    return kq["van_ban"], kq["khoan"]


PHAM_VI_KIEM = ("thuat ngu va dinh nghia khop nguyen van tung khoan theo phan doan cua bo quet; "
                "KHONG chung minh ranh gioi khoan (tach tu van ban tho) — can nguoi duyet; "
                # r37 (lượt 36, quyết định chủ kho): giới hạn đã khai được KHOÁ vào tín hiệu đầu ra của đường thô.
                "diem danh so dang 'N.' 'N)' '(N)' trung hinh dang so khoan — co the bi nhan thanh khoan rieng; "
                # r39 (lượt 38, quyết định chủ kho "THU HẸP MIỀN"): hai phía miền được khoá ở đây.
                "dong co phan mo dau dang nhan diem nhieu ve (vd 'ab c.', 'Ban a)', '(Ho so)') bi TU CHOI ca Dieu — "
                "khong phai gioi han; cum tu dung truoc 'la' khong mang dau ket ('Ho so la …') van duoc nhan; "
                "can ranh gioi chac chan thi dung --tep <tep .docx>")


def tach_khoan(van_ban):
    """Các khoản của một Điều "Giải thích từ ngữ": danh sách `(số_nguồn | None, văn bản đã gỡ số)`, theo thứ
    tự nguồn; `None` khi KHÔNG xác định được ranh giới (fail-closed).

    Ranh giới do CẤU TRÚC dòng quyết, KHÔNG do chữ "là" (Review Rescue Checkpoint sau lượt 5: năm lượt liên tiếp
    tìm ra một cửa mới trong phép đoán theo từ nối — F1→N1→M1→Q1→R1):
    - Bỏ BOM, dòng tiêu đề `Điều N.` và câu dẫn CHUẨN (`_RE_CAU_DAN_TRON`, nguyên dòng) đứng TRƯỚC khoản đầu.
    - Mỗi khoản phải kết thúc bằng dấu câu kết (`_ket_thuc_cau`, wp1514).
    - #1525: dòng điểm (`a)`, `-`) và dòng mở bằng "là" ⇒ None — đường thô chỉ nhận khoản đúng một dòng (khoản có điểm
      đi đường cấu trúc .docx); ngoặc/trích dẫn trải nhiều dòng ⇒ chặn (lượt 7 T1).
    - Nguồn CÓ số: dòng mang số mở khoản; số phải LIÊN TỤC từ 1 (lượt 5 R1: khoản mất số ở giữa); mọi dòng
      không số khác ⇒ None (có thể là khoản mất số — không đoán).
    - Nguồn MẤT số (Google Doc rơi số tự động — Điều 3 Luật 134/2025/QH15): MỖI DÒNG là một khoản, không có tiếp
      dòng (lượt 6 S2) — dòng gãy giữa câu thành khoản không xác minh được ⇒ chặn."""
    s = _bo_mot_bom(van_ban)
    if vuot_ngan_sach(s):
        return None   # r35 (lượt 34, `can-tai-nguyen-doc-nguon`): vượt ngân sách đọc ⇒ không xác minh được
    if _ky_tu_la(s, xuong_dong=True):
        # r16 (lượt 15 R3) → r17 (lượt 16 S1/S2): ký tự ngoài danh sách cho phép, kiểm TRƯỚC `splitlines`/`strip` (NEL, LS/PS…
        # không được thành ranh giới dòng) ⇒ từ chối CẢ nguồn.
        return None
    dong = [ln.strip() for ln in s.splitlines() if ln.strip()]
    if dong and _RE_TIEU_DE_DIEU.match(dong[0]):
        if not _RE_TIEU_DE_TRON.match(" ".join(dong[0].split())):
            # lượt 11 X3 → r2 A2c → r3 C1: tiêu đề có phần dư ⇒ có thể DÍNH khoản đầu ⇒ bỏ dòng là bỏ luôn khoản ⇒ mơ hồ.
            # Danh sách CHO PHÉP hình dạng tiêu đề, thay cho dò chữ "là" (bỏ sót khoản dùng từ nối khác và "là" sát dấu câu).
            return None
        dong = dong[1:]
    # r27 (lượt 26 C1) → r35 (bộ quét nhãn) → r36 (Review Rescue §12): DANH SÁCH CHO PHÉP đầu dòng (`dau_dong_cho_phep`) cho cả nguồn
    # có số lẫn mất số. Dòng nào đầu dòng ngoài danh sách — nhãn điểm (`a)`, `-`), nhãn nhiều thành phần, ký hiệu… — ⇒ từ chối CẢ nguồn.
    # #1525 (đóng K1 lượt 10 #1514): trên văn bản THÔ, dòng điểm có thể thuộc khoản đang mở (khoản có điểm) hoặc là ranh giới mới
    # (lời dẫn nhóm + định nghĩa riêng) — cùng hình dạng ở MỌI loại nguồn. Đường thô chỉ nhận khoản ĐÚNG MỘT DÒNG; khoản có điểm
    # đi đường cấu trúc (`--tep <tệp .docx>`, `doc_dieu_cau_truc`). Dòng "là" ở nguồn có số rơi xuống nhánh cuối (dòng không số ⇒
    # None); ở nguồn mất số nó là một khoản và bị `_tu_noi` chặn.
    loai = [dau_dong_cho_phep(ln) for ln in dong]
    if any(q is None for q in loai):
        return None
    # lượt 8 U1/U3 (quyết định chủ kho): nguồn có dấu phân cách mơ hồ ⇒ từ chối CẢ nguồn. r38 (lượt 37): đo trên CHÍNH span thân mà
    # danh sách cho phép đã chọn (sau số khoản) — không để `_bo_dau_dong` tự cấp một span khác (nó từng bóc `đ)` như nhãn điểm).
    if any(_dong_mo_ho(ln[q[2]:] if q[0] == "so" else ln) for ln, q in zip(dong, loai)):
        return None
    co_so = any(q[0] == "so" for q in loai)
    khoan: list[list] = []
    for i_dong, (ln, q) in enumerate(zip(dong, loai)):
        if q[0] == "so":
            khoan.append([q[1], ln[q[2]:]])
        elif i_dong == 0 and _RE_CAU_DAN_TRON.fullmatch(" ".join(ln.split())):
            # r4 (lượt 4 D3): CHỈ đúng MỘT câu dẫn, ở dòng ĐẦU (ngay sau tiêu đề) — câu dẫn lặp hay câu dẫn muộn có thể che dòng mở khoản.
            # r6 (lượt 6 F2): và CẢ dòng phải đúng câu dẫn chuẩn (`_RE_CAU_DAN_TRON`) — câu dẫn khác ⇒ không bỏ ⇒ nguồn bị chặn.
            continue   # câu dẫn CHUẨN (wp1514 X3): dòng khác kết thúc ":" KHÔNG bị bỏ — có thể là phần đầu một khoản
        elif not co_so:
            khoan.append([None, ln])
        else:
            return None
    if co_so and [so for so, _ in khoan] != list(range(1, len(khoan) + 1)):
        return None
    if not all(_ket_thuc_cau(txt) for _, txt in khoan):
        return None   # wp1514 X3b/X3c: khoản không kết thúc bằng dấu câu kết ⇒ ranh giới khoản không tin được
    if any(_RE_SO_NOI_DONG.search(txt) for _, txt in khoan):
        return None   # r2 (lượt 2 A2): tiểu mục đánh số trong thân khoản ⇒ số khoản kế có thể là tiểu mục
    return [(so, txt) for so, txt in khoan]


def _ket_thuc_cau(txt) -> bool:
    """Khoản kết thúc bằng dấu câu kết `.` `!` `?` (bỏ cả dải khoảng trắng + dấu đóng `)` `"` `”` ở cuối). `:` và `;` KHÔNG kết
    câu: khoản `… sau:` phải có các dòng điểm theo sau (wp1514 X3c: tiểu mục đánh số sau `:` bị nhận là khoản mới;
    X3b: dòng gãy giữa câu ở nguồn mất số thành một khoản)."""
    # cả DẢI đuôi khoảng trắng + dấu đóng (lượt 2 A3: xen khoảng trắng). r35 (lượt 34, `can-tai-nguyen-doc-nguon`): QUÉT LÙI một lần
    # thay cho regex không neo đầu (dải trắng dài giữa dòng ⇒ số bước bậc hai).
    s = str(txt)
    i = len(s)
    while i and (s[i - 1].isspace() or s[i - 1] in ')"\u201d'):
        i -= 1
    return bool(i) and s[i - 1] in _DAU_CAU_KET


def _gon(s) -> str:
    """Gộp khoảng trắng TRONG mỗi dòng, GIỮ ranh giới dòng (wp1514 X4: gộp cả `\n` từng cho định nghĩa dồn các dòng
    điểm thành một dòng vẫn qua kiểm); bỏ dòng rỗng."""
    return "\n".join(" ".join(ln.split()) for ln in str(s).split("\n") if ln.strip())


# DANH SÁCH CHO PHÉP các dấu phân cách mà `_dong_mo_ho`/`_quet` hiểu. Mọi dấu khác thuộc nhóm ngoặc/trích dẫn
# Unicode (Ps/Pe/Pi/Pf) hay dấu kép loại Po ⇒ nguồn mơ hồ (lượt 9 V1: danh sách cấm theo từng kiểu dấu luôn thiếu).
_DAU_HIEU_DUOC = frozenset({"(", ")", '"', "\u201c", "\u201d"})
# Lượt 11 X1: nháy đơn thẳng `'` (U+0027, nhóm Po) cũng là dấu trích dẫn mà bộ quét không hiểu.
_DAU_KEP_PO = frozenset({"'", "\uff02", "\u2033", "\u2036", "\uff07"})


def _bo_dau_dong(ln) -> str:
    """Bỏ dấu số khoản (`1.`, `1)`, `(1)`) hoặc dấu điểm (`a)`, `-`) ở ĐẦU dòng — dấu ngoặc của chúng không phải ngoặc
    nội dung (`a)` không có `(` đi kèm)."""
    m = _RE_SO_KHOAN.match(ln) or _RE_DIEM.match(ln)
    return ln[m.end():] if m else ln


def _dong_mo_ho(ln) -> bool:
    """Một dòng có dấu phân cách MƠ HỒ: ngoặc tròn hay trích dẫn KHÔNG khép ngay trong dòng (trải sang dòng khác —
    lượt 8 U3: số thứ tự trong trích dẫn nhiều dòng bị nhận là số khoản), dấu `)` không có `(`, hoặc trích dẫn cong
    LỒNG cùng kiểu dấu (lượt 8 U1: dấu đóng của cụm trong khép nhầm cụm ngoài). Ký tự bên trong một cụm trích dẫn là
    nội dung, trừ dấu mở cong `“` (lồng ⇒ mơ hồ). Chốt BẢO THỦ: chặn oan được, nhận nhầm thì không."""
    if ln.count('"') >= 3:
        return True   # wp1514 X2: hai tầng trích dẫn bị làm phẳng thành `"` không phân biệt được với hai cụm độc lập
    sau, trich = 0, None
    for c in ln:
        if c not in _DAU_HIEU_DUOC and (unicodedata.category(c) in ("Ps", "Pe", "Pi", "Pf") or c in _DAU_KEP_PO):
            return True   # lượt 9 V1: dấu ngoặc/trích dẫn bộ quét KHÔNG hiểu (`«»`, `‘’`, `„`, `[]`…) ⇒ mơ hồ
        if trich is not None:
            if c == trich:
                trich = None
            elif c == "\u201c" and trich == "\u201d":
                return True
        elif c == "(":
            sau += 1
        elif c == ")":
            if not sau:
                return True
            sau -= 1
        elif c == '"':
            trich = '"'
        elif c == "\u201c":
            trich = "\u201d"
        elif c == "\u201d":
            return True
    return sau != 0 or trich is not None


def _quet(txt):
    """Duyệt `txt` từng ký tự kèm trạng thái "đang trong ngoặc tròn / cụm trích dẫn" TRƯỚC ký tự ấy. Một bộ quét
    có trạng thái thay cho đếm/regex (lượt 5 R3: xoá cặp ngoặc trong cùng bằng regex bỏ sót ngoặc lồng)."""
    sau, trich = 0, None   # `trich`: None, hoặc ký tự ĐÓNG của cụm trích dẫn đang mở (`"` hoặc `”`)
    for i, c in enumerate(txt):
        yield i, c, sau > 0 or trich is not None
        if trich is not None:
            # Trong trích dẫn MỌI ký tự là nội dung (lượt 6 S2: `“(”`; lượt 7 T1: `“"”` từng lật trạng thái ngoặc kép
            # thẳng) — chỉ đúng dấu đóng của CHÍNH cụm đang mở mới khép nó.
            if c == trich:
                trich = None
        elif c == "(":
            sau += 1
        elif c == ")" and sau:
            sau -= 1
        elif c == '"':
            trich = '"'
        elif c == "\u201c":
            trich = "\u201d"


def _tu_noi(txt):
    """Match của từ nối định nghĩa "là" CẤP KHOẢN, hoặc None: chữ "là" ĐẦU TIÊN nằm NGOÀI ngoặc tròn và cụm trích
    dẫn (lượt 3 M1, lượt 4 Q1), ở PHẦN ĐẦU khoản — trước dòng điểm đầu tiên và không sau một dấu `:` NGOÀI ngoặc
    (lượt 4 Q1; lượt 5 R3: dấu `:` trong ngoặc lồng không tính). Phần đầu được phép xuống dòng (lượt 4 Q3)."""
    dau = []
    for ln in str(txt).split("\n"):
        if dau and _RE_DIEM.match(ln.strip()):
            break
        dau.append(ln)
    dau = "\n".join(dau)
    vi_tri_la = {m.start(): m for m in _RE_LA.finditer(dau)}
    for i, c, trong in _quet(dau):
        if trong:
            continue
        if c == ":":
            return None
        if i in vi_tri_la:
            return vi_tri_la[i]
    return None


def lech_nguyen_van(khai_niem, van_ban, khoan=None):
    """Các `stt` sai so với nguồn. So TRỌN KHOẢN (khoảng trắng gộp), không so chuỗi con (lượt 1 F1: định nghĩa
    bị cắt, thiếu khoản, tráo số đều từng lọt). Mục thứ i phải: `stt` = số của khoản thứ i trong nguồn (hoặc
    i+1 khi nguồn mất số); thuật ngữ KHÔNG chứa chữ "là" (tách tại chữ "là" ĐẦU TIÊN — lượt 2 N1); và cụm
    `<thuật ngữ> là <định nghĩa>` bằng đúng khoản ấy. Khoản nguồn không có mục tương ứng cũng là lệch.
    Nguồn không xác định được ranh giới khoản ⇒ `[0]` (không xác minh được ⇒ không dùng).
    #1525: `khoan` truyền vào (ranh giới đọc từ CẤU TRÚC .docx, `doc_dieu_cau_truc`) thay cho `tach_khoan(van_ban)`."""
    if khoan is None:
        khoan = tach_khoan(van_ban)
    if not khoan:
        return [0]
    so_cua = list(range(1, len(khoan) + 1))   # số nguồn (nếu có) đã được buộc LIÊN TỤC từ 1 ở `tach_khoan`
    lech = []
    for i, k in enumerate(khai_niem):
        tn, dn = _gon(k.get("thuat_ngu", "")), _gon(k.get("dinh_nghia", ""))
        dung = False
        if i < len(khoan) and k.get("stt") == so_cua[i]:
            # So THEO VỊ TRÍ ranh giới trong nguồn (lượt 3 M1), không so chuỗi ghép: thuật ngữ = phần trước chữ "là"
            # đầu tiên NGOÀI ngoặc; định nghĩa = phần sau nó. Khoản không có từ nối "là" ngoài ngoặc (vd "bao gồm")
            # ⇒ không xác minh được ⇒ lệch (chặn, không nhận sai).
            # #1525 r2 (lượt 1 A3): khoản từ CẤU TRÚC mang `đầu khoản` (phần tử thứ ba) — dò từ nối CHỈ ở đó, không lấy "là"
            # của một điểm có nhãn ngoài mẫu `_RE_DIEM` (`A)`, `1.`…). Đầu khoản là tiền tố của khoản nên vị trí giữ nguyên.
            m = _tu_noi(khoan[i][2] if len(khoan[i]) > 2 else khoan[i][1])
            if m:
                tn_nguon, dn_nguon = _gon(khoan[i][1][:m.start()]), _gon(khoan[i][1][m.end():])
                # Lượt 4 Q1: HAI VẾ phải khác rỗng — khoản mất phần đầu (chỉ còn "là …") từng qua với thuật ngữ "".
                dung = bool(tn_nguon and dn_nguon) and tn == tn_nguon and dn == dn_nguon
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

def _chay_gioi_han(args, timeout=600, tran=None, **_kw):
    """r38 → r39 (lượt 38, `can-tai-nguyen-doc-nguon`): chạy tiến trình con, đọc stdout + stderr THEO KHỐI với trần byte mỗi ống. MỘT
    hạn chót phủ từ lúc đọc tới khi tiến trình KẾT THÚC (cả `wait`); vượt trần, quá hạn hay lỗi đọc ⇒ giết + thu hồi CÓ GIỚI HẠN, rồi
    ném (ValueError / `subprocess.TimeoutExpired`) TRƯỚC model. Mỗi lần đọc tối đa phần còn lại + 1 byte (biết vượt mà không nạp thêm).
    Trả đối tượng có `returncode`/`stdout`/`stderr` (chuỗi UTF-8, `errors=replace`) như `subprocess.run(text=True)`."""
    import threading
    import types
    tran = TRAN_BYTE_TEP if tran is None else tran
    han = time.monotonic() + timeout
    p = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    buf, vuot, loi = {"out": bytearray(), "err": bytearray()}, [], []

    def doc(ong, ten):
        try:
            while True:
                con = tran + 1 - len(buf[ten])
                if con <= 0:
                    vuot.append(ten)   # đã đọc quá trần: KHÔNG được coi lần đọc 0 byte kế tiếp là hết dữ liệu
                    return
                k = ong.read1(min(65536, con))
                if not k:
                    return
                buf[ten] += k
        except Exception as e:  # noqa: BLE001 — lỗi đọc phải về người gọi, không được trả dữ liệu đọc dở như đã đủ
            loi.append(e)

    def thu_hoi():
        with contextlib.suppress(Exception):
            p.kill()
        with contextlib.suppress(Exception):
            p.wait(timeout=5)
    luong = [threading.Thread(target=doc, args=(p.stdout, "out"), daemon=True),
             threading.Thread(target=doc, args=(p.stderr, "err"), daemon=True)]
    for t in luong:
        t.start()
    def con_lai():
        return max(0.0, han - time.monotonic())   # r40 (lượt 39): MỘT nguồn thời gian còn lại cho mọi lần chờ
    while any(t.is_alive() for t in luong) and not vuot and not loi and con_lai() > 0:
        for t in luong:
            t.join(min(0.05, con_lai()))
    if vuot or loi:
        thu_hoi()
        ten = "stdout" if (vuot or ["out"])[0] == "out" else "stderr"
        raise ValueError(f"tl extract in qua {tran} byte ra {ten} — vuot ngan sach doc" if vuot
                         else f"loi doc ong cua tl extract: {type(loi[0]).__name__}")
    if any(t.is_alive() for t in luong):
        thu_hoi()
        raise subprocess.TimeoutExpired(args, timeout)
    try:
        p.wait(timeout=con_lai())
    except subprocess.TimeoutExpired:
        thu_hoi()
        raise
    if time.monotonic() > han:
        thu_hoi()   # r40 (lượt 39): MỘT nơi quyết nhận thành công — qua hạn thì không nhận, kể cả khi tiến trình vừa kết thúc
        raise subprocess.TimeoutExpired(args, timeout)
    return types.SimpleNamespace(returncode=p.returncode, stdout=bytes(buf["out"]).decode("utf-8", "replace"),
                                 stderr=bytes(buf["err"]).decode("utf-8", "replace"))


def lay_dieu_qua_extract(so_hieu, dieu, tl_py, chay=_chay_gioi_han, them=()):
    """Lấy nguyên văn Điều bằng CHÍNH `tl extract` (đường đọc đã verify, có cảnh báo markup/dự thảo
    riêng) — không dựng đường đọc thứ hai. Trả (văn bản, stderr của extract)."""
    # r20 (lượt 19 V1): `--markup-strict` — nguồn dự thảo KHÔNG chứng minh được đã lọc chữ gạch bỏ ⇒ `tl extract` rc 3, không in chữ
    # ⇒ dừng trước model (thay vì chỉ chuyển tiếp cảnh báo). Cái giá đã khai: nguồn chỉ đọc được qua text/plain bị chặn.
    p = chay([sys.executable, str(tl_py), "extract", str(so_hieu), "--dieu", str(dieu), "--markup-strict", *them],
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
    # r21 (lượt 20 W3): đường `tl cache-build` rồi chạy lại cũng đi `--markup-strict` (r20) và có thể bị chặn ⇒ chỉ đường
    # chắc chắn là tệp `.docx` của riêng Điều.
    if MAU_CAP_EXTRACT in (p.stderr or ""):
        raise ValueError(f"nguon cua {so_hieu} cham tran export (~200k ky tu) — Dieu {dieu} co the bi CAT; "
                         f"chep Dieu {dieu} sang mot tep .docx rieng roi chay `--tep <tep.docx> --dieu {dieu}`")
    # r18 (lượt 17 T2): chỉ bỏ phần bao do `tl extract` in ra (dòng mốc + khoảng trắng ASCII) — `str.strip()` tổng quát còn nuốt
    # NEL, U+3000… ở biên trước khi `tach_khoan` kịp kiểm.
    return out.split(dau, 1)[1].strip(" \t\r\n"), p.stderr or ""


def tach_khai_niem(van_ban, so_hieu="", model=MODEL_MAC_DINH, thu_tu=THU_TU_MAC_DINH, env=None,
                   cac_duong=None, khoan=None) -> dict:
    """Ném HetDuong / Dung. Trả kết quả `goi` kèm `khai_niem` đã chuẩn hoá và `lech` (danh sách stt)."""
    noi_dung = (f"Văn bản số hiệu {so_hieu}.\n\n<dieu_khoan>\n{van_ban}\n</dieu_khoan>"
                if so_hieu else f"<dieu_khoan>\n{van_ban}\n</dieu_khoan>")
    kq = goi(HE_THONG_KHAI_NIEM, noi_dung, SCHEMA_KHAI_NIEM, model, thu_tu, env, cac_duong)
    kiem_schema(kq["data"], SCHEMA_KHAI_NIEM)
    kq["khai_niem"] = chuan_hoa_khai_niem(kq["data"]["khai_niem"])
    kq["lech"] = lech_nguyen_van(kq["khai_niem"], van_ban, khoan)
    return kq


def tong_token(u) -> int:
    return u["input"] + u["output"] + u["cache_doc"] + u["cache_ghi"]
