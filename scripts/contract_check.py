#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contract_check.py — chống TRÔI HỢP ĐỒNG (tra-luat).

Gọi `ping`, so version webapp đang deploy với version đóng dấu trong
references/API_CONTRACT.md. Lệch ⇒ exit 3 + cảnh báo: hợp đồng có thể lỗi thời,
phải đối chiếu trước khi tin tham số/khóa response.

Dùng:
  python scripts/contract_check.py            # đọc version từ API_CONTRACT.md, ping, so
  python scripts/contract_check.py --expect 2.20.0
  python scripts/contract_check.py --json
  python scripts/contract_check.py --selftest # offline (parse version từ chuỗi mẫu)

Creds: env (TL_WEBAPP/TL_TOKEN) → --config → ~/.tra_luat_config.json → /tmp/tra_luat_config.json.
"""
from __future__ import annotations
import argparse, json, os, re, sys
from pathlib import Path

# UTF-8 hardening (Windows codepage / tiếng Việt)
import sys as _sys
for _s in (getattr(_sys, "stdout", None), getattr(_sys, "stderr", None)):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


HERE = Path(__file__).resolve().parent
CONTRACT = HERE.parent / "references" / "API_CONTRACT.md"
VERSION_RE = re.compile(r"[Pp]hiên bản deploy[^`]*`([0-9][0-9A-Za-z._-]*)`")


def contract_version(path: Path = CONTRACT) -> str | None:
    """Bóc version đóng dấu từ dòng 'Phiên bản deploy ... `X.Y.Z`' trong API_CONTRACT.md."""
    try:
        m = VERSION_RE.search(path.read_text(encoding="utf-8"))
        return m.group(1) if m else None
    except OSError:
        return None


TL_EXPECT_RE = re.compile(r'EXPECT_VERSION\s*=\s*["\']([0-9][0-9A-Za-z._-]*)["\']')


def tl_expect_version(path: Path = HERE / "tl.py") -> str | None:
    """Bóc EXPECT_VERSION từ scripts/tl.py (để đối chiếu offline với API_CONTRACT)."""
    try:
        m = TL_EXPECT_RE.search(path.read_text(encoding="utf-8"))
        return m.group(1) if m else None
    except OSError:
        return None


TL_PY = HERE / "tl.py"


def bump_after_deploy(new: str) -> int:
    """POST-DEPLOY: nâng version đóng dấu API_CONTRACT.md + tl.py EXPECT_VERSION (kèm literal selftest)
    từ version cũ → `new`, và neutralize các cảnh báo ⚠ 'HỎNG ở deploy'. CHỈ chạy SAU khi webapp `new`
    đã Deploy và runtime checklist XANH (không chạy pre-deploy)."""
    old = contract_version() or ""
    if not old:
        print("✗ Không đọc được version đóng dấu trong API_CONTRACT.md"); return 1
    if old == new:
        print(f"= Đã đóng dấu {new}, không cần bump."); return 0
    c = CONTRACT.read_text(encoding="utf-8", newline="")
    c = c.replace(f"Phiên bản deploy đã đóng dấu: `{old}`", f"Phiên bản deploy đã đóng dấu: `{new}`")
    c = c.replace(f"Nếu KHÁC `{old}`", f"Nếu KHÁC `{new}`")
    c = c.replace(f"version:'{old}'", f"version:'{new}'")
    c = c.replace(f"schema_version:'{old}'", f"schema_version:'{new}'")
    # Sau deploy thật, API_CONTRACT không nên còn dấu version cũ trong các dòng ghi chú meta_find/fetch_url_to_drive.
    # Chỉ áp cho API_CONTRACT (không đụng changelog lịch sử).
    c = c.replace(old, new)
    c = re.sub(r"⚠ `?find`?[^\n]*?HỎNG ở deploy[^\n]*",
               f"✓ `find` tầng-3 + `meta_find` đã vá ở {new} (driveSearch_).", c)
    c = re.sub(r"⚠ HỎNG ở deploy [0-9][0-9A-Za-z._-]*[^|\n]*?cần vá [A-Za-z0-9/.]+\)?",
               f"✓ đã vá ở {new}", c)
    # v1.34.52 (bẫy bắt khi chạy THẬT — r67 kernel-size đỏ oan): .gitattributes khóa `* -text` (byte thật,
    # không eol-normalize) NHƯNG write_text mặc định trên Windows dịch \n→\r\n → MỌI dòng phình +1 byte
    # (SKILL.md 49121→49440B, vượt trần 48KB). newline="\n" ép LF tường minh cho MỌI write_text ở hàm này.
    #
    # r208 (bẫy NGƯỢC, bắt khi bump 2.21.2o→2.21.2p): ép LF lại XÓA SẠCH CRLF của file vốn CRLF —
    # read_text mặc định nuốt \r, write_text newline="\n" ghi ra LF ⇒ tl.py 1643 CRLF → 0, tl_selftest
    # 19365 → 0, SKILL.md 307 → 0; diff phình 21.320 dòng cho một thay đổi 5 dòng (không soát nổi).
    # CÁCH ĐÚNG cho CẢ HAI: newline="" ở CẢ read lẫn write = KHÔNG dịch gì, giữ nguyên kết thúc dòng
    # vốn có của từng file (LF giữ LF, CRLF giữ CRLF) ⇒ không phình byte, không nuốt \r.
    CONTRACT.write_text(c, encoding="utf-8", newline="")
    t = TL_PY.read_text(encoding="utf-8", newline="")
    t = re.sub(r'(EXPECT_VERSION\s*=\s*")[^"]+(")', r"\g<1>" + new + r"\g<2>", t, count=1)
    t = t.replace(f'EXPECT_VERSION == "{old}"', f'EXPECT_VERSION == "{new}"')
    # v1.34.20: literal expect_version SỐNG Ở tl_selftest.py (tách từ tl.py hồi I-series) — sửa cả đó
    _st = HERE / "tl_selftest.py"
    if _st.exists():
        _t2 = _st.read_text(encoding="utf-8", newline="")
        _t2n = _t2.replace(f'EXPECT_VERSION == "{old}"', f'EXPECT_VERSION == "{new}"')
        if _t2n != _t2:
            _st.write_text(_t2n, encoding="utf-8", newline="")
    TL_PY.write_text(t, encoding="utf-8", newline="")

    # v1.16.10: đồng bộ thêm SKILL.md + RUNBOOK.md để RUNBOOK/Claude không chặn nhầm ở version cũ
    #           (tái lập được — không còn sửa tay một lần như v1.16.9).
    doc_hits = 0
    for rel in ("SKILL.md", "references/RUNBOOK.md"):
        pdoc = HERE.parent / rel
        try:
            d = pdoc.read_text(encoding="utf-8", newline="")
            if old and old in d:
                doc_hits += d.count(old); d = d.replace(old, new)
                pdoc.write_text(d, encoding="utf-8", newline="")
        except OSError:
            pass
    cv, tv = contract_version(), tl_expect_version()
    residual = [ln.strip() for ln in CONTRACT.read_text(encoding="utf-8").splitlines() if old in ln]
    print(f"✓ Bumped {old} → {new}  (stamp={cv}, EXPECT_VERSION={tv}, SKILL/RUNBOOK={doc_hits} chỗ)")
    if residual:
        print(f"  ⚠ Còn {len(residual)} dòng nhắc {old} trong API_CONTRACT — rà tay nếu muốn sạch tuyệt đối:")
        for ln in residual[:12]:
            print("   ", ln[:96])
    else:
        print("  (không còn dấu vết version cũ trong API_CONTRACT)")
    return 0 if (cv == new and tv == new) else 1


def audit() -> int:
    """OFFLINE: đối chiếu version API_CONTRACT.md ↔ scripts/tl.py EXPECT_VERSION (góp ý #4)."""
    cv = contract_version()
    tv = tl_expect_version()
    ok = bool(cv) and cv == tv
    print(f"  API_CONTRACT.md   : {cv}")
    print(f"  tl.py EXPECT_VERSION: {tv}")
    if ok:
        print(f"✓ KHỚP ({cv}).")
    else:
        print("✗ LỆCH — đồng bộ hai chỗ trước khi dùng (cả hai phải bằng version webapp đang deploy).")
    return 0 if ok else 3


def _load_creds(config_path=None):
    if os.environ.get("TL_WEBAPP") and os.environ.get("TL_TOKEN"):
        return
    for p in ([config_path] if config_path else []) + \
            [str(Path.home() / ".tra_luat_config.json"), "/tmp/tra_luat_config.json"]:
        if p and Path(p).exists():
            try:
                c = json.loads(Path(p).read_text(encoding="utf-8"))
            except Exception:
                continue
            url = c.get("webappUrl") or c.get("TL_WEBAPP")
            tok = c.get("token") or c.get("TL_TOKEN")
            if url and tok:
                os.environ["TL_WEBAPP"], os.environ["TL_TOKEN"] = url, tok
                return
    sys.exit("[contract_check] thiếu TL_WEBAPP/TL_TOKEN (env/--config/mirror).")


def _imp(name):
    """Import ƯU TIÊN scripts/ gốc → _fallback/ (giống tl._imp): hết phụ thuộc cứng 'gas'."""
    import importlib
    sys.path.insert(0, str(HERE))
    fb = HERE / "_fallback"
    if fb.exists() and str(fb) not in sys.path:
        sys.path.append(str(fb))
    return importlib.import_module(name)


def live_verdict(resp, expect: str) -> dict:
    """PURE (v1.34.21 — thẩm định Codex): phân loại kết quả ping TRƯỚC khi so version.
    LIVE_PING_FAILED (không lấy được version: lỗi mạng/auth/runtime/response lạ) KHÁC VERSION_DRIFT
    (lấy được version nhưng lệch hợp đồng) — trước đây ping hỏng in 'deploy = None ≠ hợp đồng' như drift thật.
    rc: 0 khớp · 3 drift · 4 ping-failed."""
    if not isinstance(resp, dict) or not resp.get("version"):
        detail = resp.get("error") if isinstance(resp, dict) else repr(resp)
        return {"ok": False, "rc": 4, "error": "LIVE_PING_FAILED", "detail": detail,
                "live": None, "expect": expect}
    live = resp.get("version")
    if live == expect:
        return {"ok": True, "rc": 0, "live": live, "expect": expect}
    return {"ok": False, "rc": 3, "error": "VERSION_DRIFT", "live": live, "expect": expect}


def selftest() -> int:
    import tempfile
    txt = "> **Phiên bản deploy đã đóng dấu: `2.20.0`** · đối chiếu..."
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(txt); p = Path(f.name)
    checks = [
        ("parse_version", contract_version(p) == "2.20.0"),
        ("missing_file", contract_version(Path("/nonexistent.md")) is None),
        ("verdict_match", live_verdict({"version": "2.20.0"}, "2.20.0") == {"ok": True, "rc": 0, "live": "2.20.0", "expect": "2.20.0"}),
        ("verdict_drift", (lambda v: v["rc"] == 3 and v["error"] == "VERSION_DRIFT" and v["live"] == "2.19")(live_verdict({"version": "2.19"}, "2.20.0"))),
        ("verdict_ping_failed_error", (lambda v: v["rc"] == 4 and v["error"] == "LIVE_PING_FAILED" and v["detail"] == "HTTP 401")(live_verdict({"ok": False, "error": "HTTP 401"}, "2.20.0"))),
        ("verdict_ping_failed_nondict", live_verdict(None, "2.20.0")["rc"] == 4),
    ]
    for name, ok in checks:
        print(f"  [{'OK' if ok else 'FAIL'}] {name}")
    n_ok = sum(1 for _, ok in checks if ok)
    print(f"== contract_check selftest {n_ok}/{len(checks)} ==")
    return 0 if n_ok == len(checks) else 1


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--expect", help="ép version kỳ vọng (mặc định: đọc API_CONTRACT.md)")
    ap.add_argument("--config")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--audit", action="store_true",
                    help="offline: đối chiếu version API_CONTRACT.md ↔ tl.py")
    ap.add_argument("--bump", metavar="VERSION",
                    help="POST-DEPLOY: nâng stamp API_CONTRACT + tl.py EXPECT_VERSION lên VERSION (chỉ sau khi runtime xanh)")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.bump:
        return bump_after_deploy(a.bump)
    if a.audit:
        return audit()
    expect = a.expect or contract_version()
    if not expect:
        sys.exit("[contract_check] không đọc được version từ API_CONTRACT.md — truyền --expect.")
    _load_creds(a.config)
    try:
        gas = _imp("gas")
    except ModuleNotFoundError:
        sys.exit("[contract_check] không tìm thấy gas.py (scripts/ gốc lẫn _fallback/). "
                 "Cài overlay lên bộ skill đầy đủ, hoặc dùng --audit/--selftest/--bump (offline).")
    try:
        r = gas.get("ping")
    except Exception as e:  # noqa: BLE001 — ping raise (auth/mạng/runtime) KHÔNG phải drift
        r = {"ok": False, "error": f"{type(e).__name__}: {e}"}
    v = live_verdict(r, expect)
    if a.json:
        print(json.dumps(v, ensure_ascii=False))
    else:
        if v["ok"]:
            print(f"✓ webapp version {v['live']} KHỚP hợp đồng.")
        elif v.get("error") == "LIVE_PING_FAILED":
            print(f"✗ LIVE_PING_FAILED: không lấy được version từ webapp ({v.get('detail')}).\n"
                  f"  → Đây là lỗi ping/auth/mạng/runtime — KHÔNG kết luận drift. "
                  f"Kiểm `tl ping --json`/creds rồi chạy lại.")
        else:
            print(f"✗ TRÔI: webapp deploy = {v['live']} ≠ hợp đồng {expect}.\n"
                  f"  → Đối chiếu lại references/API_CONTRACT.md trước khi gọi action; "
                  f"cập nhật bảng + dòng 'Phiên bản deploy' nếu webapp đã đổi đúng ý.")
    return v["rc"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
