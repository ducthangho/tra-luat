#!/usr/bin/env python3
"""Gọi Claude cho tác vụ trích xuất có cấu trúc, tự chọn đường API key ↔ subscription.

DEV-SIDE (không vào gói phát hành). Hai đường, thứ tự lấy từ `--thu-tu` hoặc
biến `TL_LLM_ORDER` (mặc định `api,sub`):

  api  Claude API bằng SDK `anthropic`, key đọc từ `TL_ANTHROPIC_API_KEY` rồi mới
       tới `ANTHROPIC_API_KEY`. Tên riêng `TL_` vì phiên Claude Code trên web BỎ
       QUA `ANTHROPIC_API_KEY` khi xác thực (cảnh báo của trang sửa môi trường, đo
       24-11-2026), còn Network secrets KHÔNG lưu được cho host của Anthropic.
  sub  `claude -p` (Claude Code không tương tác) — tính vào SUBSCRIPTION. Đây là
       đường hợp lệ duy nhất để script dùng gói; KHÔNG lấy token OAuth của Claude
       Code đi gọi API thẳng.

CHUYỂN ĐƯỜNG chỉ khi lỗi thuộc về ĐƯỜNG (thiếu key/SDK/CLI, 401, 403, 402 hết
credit, 429, mất kết nối, `claude -p` báo lỗi — thường là chạm hạn mức gói). Lỗi
thuộc về YÊU CẦU (400 khác, model từ chối, cắt `max_tokens`, sai model, đầu ra
không đúng schema) thì DỪNG: chạy lại ở đường kia chỉ tiêu tiền lần hai cho cùng
một lỗi.

Đo 24-11-2026 trong phiên remote: `claude -p` trần nạp nguyên system prompt + bộ
tool của Claude Code (~92k token vào hạn mức gói cho một câu hỏi một dòng); thêm
`--tools "" --strict-mcp-config --setting-sources "" --disable-slash-commands
--system-prompt …` còn ~1,9k. KHÔNG dùng `--bare`: chế độ ấy chỉ nhận API key,
tức là lặng lẽ biến đường `sub` thành đường `api`.

Lệnh:
  python .claude/dev/llm_route.py trang-thai
  python .claude/dev/llm_route.py tach-khai-niem <tệp_điều.txt> --so-hieu 134/2025/QH15
         [--thu-tu api,sub] [--model claude-haiku-5-5] [--out kq.json] [--nhat-ky usage.jsonl]

Mã thoát: 0 đạt · 2 sai đối số/đầu vào · 3 HẾT ĐƯỜNG (mọi đường đều hỏng phía
đường) · 4 DỪNG (lỗi phía yêu cầu) · 5 đầu ra KHÔNG khớp nguyên văn nguồn.
KHÔNG BAO GIỜ in giá trị key.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

MODEL_MAC_DINH = "claude-haiku-5-5"
DUONG_HOP_LE = ("api", "sub")
BIEN_KEY = ("TL_ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY")
# Biến khiến `claude` CLI xác thực bằng API thay vì gói — gỡ khỏi env của con ở đường `sub`,
# kẻo trên máy cá nhân "sub" lặng lẽ tính tiền vào API key.
BIEN_GO_KHOI_SUB = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "TL_ANTHROPIC_API_KEY")
TIMEOUT_SUB_GIAY = 300

MA_OK, MA_DOI_SO, MA_HET_DUONG, MA_DUNG, MA_LECH_NGUYEN_VAN = 0, 2, 3, 4, 5


class ChuyenDuong(Exception):
    """Lỗi thuộc về ĐƯỜNG — thử đường kế tiếp."""


class Dung(Exception):
    """Lỗi thuộc về YÊU CẦU — không thử đường khác."""


class HetDuong(Exception):
    def __init__(self, lan_thu):
        self.lan_thu = lan_thu
        super().__init__("; ".join(f"{d}: {l}" for d, l in lan_thu))


def doc_thu_tu(gia_tri: str | None) -> tuple[str, ...]:
    tho = (gia_tri or "api,sub").replace(" ", "")
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
    if ma in (401, 402, 403, 429) or kieu in ("authentication_error", "billing_error",
                                               "permission_error", "rate_limit_error"):
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


def duong_sub(he_thong, noi_dung, schema, model, env, chay=subprocess.run, tim=shutil.which):
    claude_bin = tim("claude")
    if not claude_bin:
        raise ChuyenDuong("khong co claude CLI tren PATH")
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
    if p.returncode != 0 or not isinstance(kq, dict) or kq.get("is_error"):
        mo_ta = (kq or {}).get("result") if isinstance(kq, dict) else (p.stderr or tho)
        raise ChuyenDuong(f"claude -p rc={p.returncode}: {str(mo_ta or '').strip()[:160]}")
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

def goi(he_thong, noi_dung, schema, model=MODEL_MAC_DINH, thu_tu=("api", "sub"), env=None,
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


def lech_nguyen_van(khai_niem, van_ban):
    """Khoản nào mà cụm "<thuật ngữ> là <định nghĩa>" KHÔNG có nguyên văn trong nguồn.
    Kiểm CẢ CỤM chứ không từng mảnh: từng mảnh là chuỗi con vẫn lọt ca tách sai chỗ."""
    return [k["stt"] for k in khai_niem
            if f'{k["thuat_ngu"]} là {k["dinh_nghia"]}' not in van_ban]


def lenh_tach_khai_niem(a, env=None, cac_duong=None) -> int:
    try:
        van_ban = Path(a.tep).read_text(encoding="utf-8").strip()
    except OSError as e:
        print(f"khong doc duoc {a.tep}: {e}", file=sys.stderr)
        return MA_DOI_SO
    if not van_ban:
        print(f"{a.tep} rong", file=sys.stderr)
        return MA_DOI_SO
    try:
        thu_tu = doc_thu_tu(a.thu_tu or (env or os.environ).get("TL_LLM_ORDER"))
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return MA_DOI_SO
    noi_dung = (f"Văn bản số hiệu {a.so_hieu}.\n\n<dieu_khoan>\n{van_ban}\n</dieu_khoan>"
                if a.so_hieu else f"<dieu_khoan>\n{van_ban}\n</dieu_khoan>")
    try:
        kq = goi(HE_THONG_KHAI_NIEM, noi_dung, SCHEMA_KHAI_NIEM, a.model, thu_tu, env, cac_duong)
        kiem_schema(kq["data"], SCHEMA_KHAI_NIEM)
    except HetDuong as e:
        print("HET DUONG — moi duong deu hong phia duong:", file=sys.stderr)
        for d, l in e.lan_thu:
            print(f"  {d}: {l}", file=sys.stderr)
        return MA_HET_DUONG
    except Dung as e:
        print(f"DUNG (loi phia yeu cau, khong thu duong khac): {e}", file=sys.stderr)
        return MA_DUNG

    kn = chuan_hoa_khai_niem(kq["data"]["khai_niem"])
    ket = {"so_hieu": a.so_hieu, "nguon": str(a.tep), "khai_niem": kn}
    van_ban_json = json.dumps(ket, ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).write_text(van_ban_json + "\n", encoding="utf-8")
    print(van_ban_json)
    if a.nhat_ky:
        ghi_nhat_ky(a.nhat_ky, kq, "tach-khai-niem")

    u = kq["usage"]
    for d, l in kq["lan_thu"]:
        print(f"[chuyen duong] {d}: {l}", file=sys.stderr)
    print(f"DUONG: {kq['duong']}" + (f" (key tu {kq['nguon_key']})" if kq["nguon_key"] else
                                     " (subscription — tinh vao han muc goi)"), file=sys.stderr)
    print(f"MODEL: {kq['model']}", file=sys.stderr)
    print(f"TOKEN: input={u['input']} output={u['output']} cache_doc={u['cache_doc']} "
          f"cache_ghi={u['cache_ghi']} tong={u['input'] + u['output'] + u['cache_doc'] + u['cache_ghi']}",
          file=sys.stderr)
    if kq["usd_uoc_tinh"] is not None:
        print(f"USD (CLI uoc tinh): {kq['usd_uoc_tinh']:.6f}", file=sys.stderr)
    lech = lech_nguyen_van(kn, van_ban)
    if lech:
        print(f"LECH NGUYEN VAN o khoan {lech} — KHONG dung ket qua nay", file=sys.stderr)
        return MA_LECH_NGUYEN_VAN
    print(f"NGUYEN VAN: DAT ({len(kn)} khai niem, moi cum '<thuat ngu> la <dinh nghia>' co nguyen van trong nguon)",
          file=sys.stderr)
    return MA_OK


def lenh_trang_thai(a, env=None, tim=shutil.which) -> int:
    """Chỉ báo ĐƯỜNG NÀO CÓ MẶT — không gọi gì, không chứng minh dùng được."""
    env = os.environ if env is None else env
    ten, _ = lay_key(env)
    try:
        import importlib.util
        co_sdk = importlib.util.find_spec("anthropic") is not None
    except (ImportError, ValueError):
        co_sdk = False
    print(f"api: key={'co (' + ten + ')' if ten else 'KHONG'} · sdk={'co' if co_sdk else 'KHONG'}")
    print(f"sub: claude CLI={'co' if tim('claude') else 'KHONG'}")
    try:
        print(f"thu tu: {','.join(doc_thu_tu(env.get('TL_LLM_ORDER')))} (TL_LLM_ORDER)")
    except ValueError as e:
        print(f"thu tu: LOI — {e}")
        return MA_DOI_SO
    print("CO MAT != DUNG DUOC — so du credit chi xem duoc o Claude Console > Billing; "
          "song/chet cua key: launcher.py doctor --kiem-song")
    return MA_OK


def phan_tich(argv):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="lenh", required=True)
    t = sub.add_parser("tach-khai-niem", help="tach khai niem tu dieu 'Giai thich tu ngu'")
    t.add_argument("tep")
    t.add_argument("--so-hieu", default="")
    t.add_argument("--thu-tu", default=None, help="api,sub | sub,api | api | sub (mac dinh TL_LLM_ORDER hoac api,sub)")
    t.add_argument("--model", default=MODEL_MAC_DINH)
    t.add_argument("--out")
    t.add_argument("--nhat-ky", help="tep JSONL ghi don usage moi lan goi")
    sub.add_parser("trang-thai", help="duong nao co mat (khong goi API)")
    return p.parse_args(argv)


def main(argv=None) -> int:
    a = phan_tich(sys.argv[1:] if argv is None else argv)
    if a.lenh == "tach-khai-niem":
        return lenh_tach_khai_niem(a)
    return lenh_trang_thai(a)


if __name__ == "__main__":
    sys.exit(main())
