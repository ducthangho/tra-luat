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
import unicodedata
from pathlib import Path
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
_RE_DIEM = re.compile(r"^([a-zđ]\)|[-–•+])\s*")
_RE_LA = re.compile(r"(?:^|\s)là(?:\s|$)")
_RE_MO_BANG_LA = re.compile(r"^là(?:\s|$)")
# Câu dẫn chuẩn của Điều "Giải thích từ ngữ" (wp1514 X3): CHỈ dòng khớp mẫu này mới được bỏ như câu dẫn.
_RE_CAU_DAN = re.compile(r"(?:được hiểu|được giải thích)\s+như\s+sau\s*:$", re.IGNORECASE)
# r2 (lượt 2 A2): `;` KHÔNG kết khoản — ngắt dòng sau `;` giữa một định nghĩa dài từng tạo hai khoản đều qua kiểm.
_DAU_CAU_KET = frozenset(".!?")
# r2 (lượt 2 A2): đánh số NỘI DÒNG trong thân khoản (`… 1) …`, `… 2. …`) — tiểu mục, ranh giới khoản không tin được.
# r3 (lượt 3 C2): khoảng trắng hai bên CHỈ trong phạm vi một dòng (`[ \t]`, không `\s`) — số điều ở cuối một dòng điểm, theo sau
# là xuống dòng, không phải số thứ tự nội dòng.
# r4 (lượt 4 D1): mọi khoảng trắng TRỪ xuống dòng (`[^\S\n]`) — gồm U+00A0 khoảng trắng không ngắt mà `[ \t]` bỏ sót.
_RE_SO_NOI_DONG = re.compile(r"(?:^|[^\S\n])\(?\d+[.)](?=[^\S\n])")


PHAM_VI_KIEM = ("thuat ngu va dinh nghia khop nguyen van tung khoan theo phan doan cua bo quet; "
                "KHONG chung minh ranh gioi khoan (tach tu van ban tho) — can nguoi duyet")


def tach_khoan(van_ban):
    """Các khoản của một Điều "Giải thích từ ngữ": danh sách `(số_nguồn | None, văn bản đã gỡ số)`, theo thứ
    tự nguồn; `None` khi KHÔNG xác định được ranh giới (fail-closed).

    Ranh giới do CẤU TRÚC dòng quyết, KHÔNG do chữ "là" (Review Rescue Checkpoint sau lượt 5: năm lượt liên tiếp
    tìm ra một cửa mới trong phép đoán theo từ nối — F1→N1→M1→Q1→R1):
    - Bỏ BOM, dòng tiêu đề `Điều N.` và câu dẫn CHUẨN (`… được hiểu/giải thích như sau:`) đứng TRƯỚC khoản đầu.
    - Mỗi khoản phải kết thúc bằng dấu câu kết (`_ket_thuc_cau`, wp1514).
    - Dòng điểm (`a)`, `-`) nối vào khoản đang mở. Ở nguồn CÓ số, dòng là TIẾP DÒNG chỉ khi khoản đang mở CHƯA có
      từ nối và dòng mở bằng "là" (lượt 4 Q3); ngoặc/trích dẫn trải nhiều dòng ⇒ chặn (lượt 7 T1).
    - Nguồn CÓ số: dòng mang số mở khoản; số phải LIÊN TỤC từ 1 (lượt 5 R1: khoản mất số ở giữa); mọi dòng
      không số khác ⇒ None (có thể là khoản mất số — không đoán).
    - Nguồn MẤT số (Google Doc rơi số tự động — Điều 3 Luật 134/2025/QH15): MỖI DÒNG là một khoản, không có tiếp
      dòng (lượt 6 S2) — dòng gãy giữa câu thành khoản không xác minh được ⇒ chặn."""
    dong = [ln.strip() for ln in str(van_ban).lstrip("\ufeff").splitlines() if ln.strip()]
    if any(_dong_mo_ho(_bo_dau_dong(ln)) for ln in dong):
        return None   # lượt 8 U1/U3 (quyết định chủ kho): nguồn có dấu phân cách mơ hồ ⇒ từ chối CẢ nguồn
    if dong and _RE_TIEU_DE_DIEU.match(dong[0]):
        if not _RE_TIEU_DE_TRON.match(" ".join(dong[0].split())):
            # lượt 11 X3 → r2 A2c → r3 C1: tiêu đề có phần dư ⇒ có thể DÍNH khoản đầu ⇒ bỏ dòng là bỏ luôn khoản ⇒ mơ hồ.
            # Danh sách CHO PHÉP hình dạng tiêu đề, thay cho dò chữ "là" (bỏ sót khoản dùng từ nối khác và "là" sát dấu câu).
            return None
        dong = dong[1:]
    co_so = any(_RE_SO_KHOAN.match(ln) for ln in dong)
    khoan: list[list] = []
    for i_dong, ln in enumerate(dong):
        m = _RE_SO_KHOAN.match(ln) if co_so else None
        if m:
            khoan.append([int(m.group(1) or m.group(2)), ln[m.end():]])
        elif _RE_DIEM.match(ln):
            if not khoan:
                return None
            khoan[-1][1] += "\n" + ln
        elif co_so and khoan and _RE_MO_BANG_LA.match(ln) and _tu_noi(khoan[-1][1]) is None:
            # Lượt 7 T1 (quyết định chủ kho): tiếp dòng KHÔNG còn dựa vào trạng thái ngoặc/trích dẫn — ba lượt liền tìm
            # ra một cách làm bộ quét báo "còn mở" sai. Khoản có ngoặc trải nhiều dòng ⇒ bị chặn (giới hạn đã khai).
            # Tiếp dòng CHỈ ở nguồn có số (lượt 6 S2): nguồn mất số không có ranh giới nào khác ngoài dòng.
            khoan[-1][1] += "\n" + ln
        elif i_dong == 0 and _RE_CAU_DAN.search(" ".join(ln.split())) and _tu_noi(ln) is None:
            # r4 (lượt 4 D3): CHỈ đúng MỘT câu dẫn, ở dòng ĐẦU (ngay sau tiêu đề) — câu dẫn lặp hay câu dẫn muộn có thể che dòng mở khoản.
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
    duoi = re.sub(r'[\s)"\u201d]+$', "", str(txt))   # cả DẢI đuôi khoảng trắng + dấu đóng (lượt 2 A3: xen khoảng trắng)
    return bool(duoi) and duoi[-1] in _DAU_CAU_KET


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


def lech_nguyen_van(khai_niem, van_ban):
    """Các `stt` sai so với nguồn. So TRỌN KHOẢN (khoảng trắng gộp), không so chuỗi con (lượt 1 F1: định nghĩa
    bị cắt, thiếu khoản, tráo số đều từng lọt). Mục thứ i phải: `stt` = số của khoản thứ i trong nguồn (hoặc
    i+1 khi nguồn mất số); thuật ngữ KHÔNG chứa chữ "là" (tách tại chữ "là" ĐẦU TIÊN — lượt 2 N1); và cụm
    `<thuật ngữ> là <định nghĩa>` bằng đúng khoản ấy. Khoản nguồn không có mục tương ứng cũng là lệch.
    Nguồn không xác định được ranh giới khoản ⇒ `[0]` (không xác minh được ⇒ không dùng)."""
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
            m = _tu_noi(khoan[i][1])
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
