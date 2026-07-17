#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""charact_capture.py — HARNESS CHARACTERIZATION (dev-only, .claude/ KHÔNG vào bundle/zip).

Đợt 0 kế hoạch `ke-hoach-guard-va-boc-tl-core-2026-07-18.md` §6.1/§10: capture hành vi CLI của các cmd
thuộc cụm ingest_ops + nlm_ops TRƯỚC khi MOVE (Đợt A/B), để sau move so-khớp-byte (golden 0-diff của move).

Nguyên tắc:
- OFFLINE THUẦN + FAKE-HOME TRỐNG: HOME/USERPROFILE trỏ thư mục giả; TL_CONFIG_PATH trỏ config giả
  webappUrl RỖNG (truthy → chặn rơi về config thật cạnh repo; GAS guard nội bộ 'Thiếu TL_WEBAPP/TL_TOKEN'
  là thông điệp TẤT ĐỊNH — không đụng mạng, không phụ thuộc WinSock). Không ~/.config/gws, không
  .notebooklm-mcp-cli → mọi đường live chết sạch, journal/cache ghi vào fake-home.
- KHÔNG BAO GIỜ --apply/--confirm (assert cứng). DRY/err-envelope cũng là hành vi — mục tiêu duy nhất là
  TRƯỚC == SAU move, không phải output 'đẹp'.
- Scrub: JSON-object qua chính tl._scrub_volatile (R7) + thay path REPO/FAKEHOME bằng token; CRLF→LF.
- Chạy `--stability 2` để chứng minh baseline ổn định (2 lượt byte-hệt) trước khi tin dùng.

Dùng:  python .claude/dev/charact_capture.py --clusters            # toàn bộ cmd ingest_ops + nlm_ops
       python .claude/dev/charact_capture.py nlm-add source-delete # từng cmd
       python .claude/dev/charact_capture.py --clusters --stability 2
Out:   scripts/.tl_state/charact/<cli-name>.json (schema charact.v1)
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

DEV_DIR = Path(__file__).resolve().parent          # .claude/dev
REPO = DEV_DIR.parent.parent                        # repo root
SCRIPTS = REPO / "scripts"
OUT_DIR = SCRIPTS / ".tl_state" / "charact"
FAKE_HOME = SCRIPTS / ".tl_state" / "charact_home"  # path CỐ ĐỊNH theo repo → ổn định giữa các lượt
PY = sys.executable

# Cụm theo kế hoạch §10: TOÀN BỘ cmd_ của 2 key _STUB_MAP nguồn (không chỉ danh sách move §4/§5 —
# cả cụm để bắt cả hàng xóm không-move có bị move làm lệch không).
CLUSTER_KEYS = ("ingest_ops", "nlm_ops")

# argv AN TOÀN per-cmd (KHÔNG --apply): fake target để đi sâu hơn usage-error khi có thể.
# Thiếu trong bảng → chạy trần (argparse usage/guard đầu-handler — vẫn là characterization hợp lệ).
FAKE_ID = "FAKECHARACTDRIVEID000001"   # ≥20 alnum → dạng drive-id, không tồn tại
SAFE_ARGV = {
    "register":             ["--drive-id", FAKE_ID],
    "recat":                [FAKE_ID, "--cat", "01"],
    "source-rename":        [FAKE_ID, "--to", "Ten_Moi_Charact"],
    "source-delete":        [FAKE_ID],
    "source-update-corpus": [FAKE_ID, "false"],
    "shared-source-fix":    [],
    "ingest":               [],
    "ingest-analyze":       [],
    "ingest-inbox":         [],
    "ingest-local":         [],
    "ingest-missing":       [],
    "ingest-route":         [],
    "profile-ingest":       [],
    "profile-ingest-resume": [],
    "nlm-add":              ["--drive-id", FAKE_ID],
    "nlm-migrate":          ["--to", "FAKE_NB_CHARACT"],
    "nlm-reconcile":        ["FAKE_NB_CHARACT"],
    "nlm-source-remove":    ["FAKE_SID_CHARACT"],
    "push-overflow":        [],
    "overflow-resolve":     [],
    "nlm-audit-physical":   [],
    "nlm-list":             [],
    "nlm-get":              ["FAKE_NB_CHARACT"],
    "nlm-content":          ["FAKE_SID_CHARACT"],
    "nlm-query":            ["cau hoi charact"],
    "nlm-cross":            ["cau hoi charact"],
    "nlm-query-plan":       ["cau hoi charact"],
    "nlm-links":            [],
    "nlm-orphans":          [],
    "preflight":            [],
    "nlm-auth-status":      [],
    "slot-audit":           [],
}


def _load_tl():
    """Nạp tl.py 1 lần trong process harness (để lấy _STUB_MAP + build_parser + _scrub_volatile)."""
    sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("tl", str(SCRIPTS / "tl.py"))
    tl = importlib.util.module_from_spec(spec)
    sys.modules["tl"] = tl
    spec.loader.exec_module(tl)
    return tl


def cluster_cli_names(tl) -> dict:
    """Map cli-name → (stub_key, handler) cho MỌI cmd_ thuộc CLUSTER_KEYS (qua parser thật)."""
    handlers = {}
    for key in CLUSTER_KEYS:
        for n in tl._STUB_MAP.get(key, []):
            if n.startswith("cmd_"):
                handlers[n] = key
    ap = tl.build_parser()
    sub = next(a for a in ap._actions if isinstance(a, tl.argparse._SubParsersAction))
    out = {}
    for name, p in sub.choices.items():
        fn = p.get_default("fn")
        hname = getattr(fn, "__name__", "")
        if hname in handlers:
            out[name] = (handlers[hname], hname)
    return dict(sorted(out.items()))


def make_fake_home() -> dict:
    FAKE_HOME.mkdir(parents=True, exist_ok=True)
    cfg = FAKE_HOME / "tl_config_charact.json"
    cfg.write_text(json.dumps({"note": "charact fake config — webapp RỖNG có chủ đích (đường GAS chết "
                                       "bằng thông điệp nội bộ tất định, không đụng mạng)",
                               "webappUrl": "", "token": ""}, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    env = os.environ.copy()
    env.update({
        "USERPROFILE": str(FAKE_HOME), "HOME": str(FAKE_HOME),
        "TL_CONFIG_PATH": str(cfg),
        "TL_CACHE_DIR": str(FAKE_HOME / ".tra_luat_cache"),
        "TL_DETERMINISTIC": "1", "TZ": "UTC", "PYTHONHASHSEED": "0",
        "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8",
        "NO_COLOR": "1",
    })
    # chặn rò cred qua env phiên dev (nếu có)
    for k in ("TL_WEBAPP", "TL_TOKEN", "TL_MASTER_KEY", "TL_SECRETS_FILEID", "TL_NLM_CRED_FILEID"):
        env.pop(k, None)
    return env


def _scrub_text(s: str) -> str:
    s = (s or "").replace("\r\n", "\n").replace("\r", "\n")
    for p, tok in ((str(FAKE_HOME), "<FAKEHOME>"), (str(REPO), "<REPO>")):
        s = s.replace(p, tok).replace(p.replace("\\", "/"), tok).replace(p.replace("\\", "\\\\"), tok)
    s = re.sub(r"[A-Za-z]:[\\/][^\s'\"]*charact_home", "<FAKEHOME>", s)
    # tuổi-cache tick theo đồng hồ (R7 — ca thật: 'cache cũ 93699s' nlm-list stale C-#8 đọc .tl_state
    # REPO-relative nên fake-home KHÔNG cô lập; nội dung cache bất biến, chỉ AGE đổi) → chuẩn hoá.
    s = re.sub(r"\b\d+(?:\.\d+)?s\b", "<AGE>s", s)
    s = re.sub(r"\b\d+(?:\.\d+)?\s*phút\b", "<AGE> phút", s)
    return s


_AGE_KEY_RE = re.compile(r"(?:[a-z0-9_]*_)?age(?:_s|_sec|_secs|_min|_ms)?$")


def _scrub_ages(obj):
    """Chuẩn hoá field tuổi trong JSON (age_s/cache_age_min/…) — fullmatch theo khuôn *_age_* để KHÔNG
    đụng key thường chứa 'age' (message/usage/coverage)."""
    if isinstance(obj, dict):
        return {k: (0 if (isinstance(v, (int, float)) and _AGE_KEY_RE.fullmatch(str(k))) else _scrub_ages(v))
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [_scrub_ages(x) for x in obj]
    return obj


def scrub_payload(tl, rc: int, stdout: str, stderr: str, cmd: str, argv: list) -> dict:
    body = {"schema": "charact.v1", "cmd": cmd, "argv": argv, "rc": rc}
    so = _scrub_text(stdout)
    js = None
    t = so.strip()
    if t.startswith("{") or t.startswith("["):
        try:
            js = _scrub_ages(tl._scrub_volatile(json.loads(t)))
        except Exception:  # noqa: BLE001 — stdout không phải JSON thuần → giữ text
            js = None
    body["stdout_json_scrubbed"] = js
    body["stdout_scrubbed"] = None if js is not None else so
    body["stderr_scrubbed"] = _scrub_text(stderr)
    return body


def run_one(tl, env: dict, name: str) -> dict:
    argv = list(SAFE_ARGV.get(name, [])) + ["--json", "--deterministic"]
    assert not any(a in ("--apply", "--confirm") or str(a).startswith("--confirm") for a in argv), \
        f"CẤM --apply/--confirm trong charact: {name} {argv}"
    cmd = [PY, str(SCRIPTS / "tl.py"), name] + argv
    try:
        cp = subprocess.run(cmd, cwd=str(FAKE_HOME), env=env, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", timeout=120)
        rc, so, se = cp.returncode, cp.stdout, cp.stderr
    except subprocess.TimeoutExpired as e:
        rc, so, se = 124, str(e.stdout or ""), "CHARACT_TIMEOUT_120S"
    return scrub_payload(tl, rc, so, se, name, argv)


def main() -> int:
    ap = argparse.ArgumentParser(description="charact capture (dev-only)")
    ap.add_argument("cmds", nargs="*", help="cli-name cần capture (trống + --clusters = cả 2 cụm)")
    ap.add_argument("--clusters", action="store_true", help="toàn bộ cmd của ingest_ops + nlm_ops")
    ap.add_argument("--stability", type=int, default=1, help="chạy N lượt, so byte giữa các lượt")
    ap.add_argument("--outdir", default=str(OUT_DIR))
    a = ap.parse_args()
    tl = _load_tl()
    cmap = cluster_cli_names(tl)
    names = list(cmap) if (a.clusters or not a.cmds) else [c for c in a.cmds]
    unknown = [c for c in names if c not in cmap]
    if unknown:
        print(f"[charact] ⚠ ngoài 2 cụm (vẫn chạy nếu là lệnh tl hợp lệ): {unknown}")
    outdir = Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    env = make_fake_home()
    prev_bytes: dict = {}
    unstable: list = []
    for r in range(1, max(1, a.stability) + 1):
        print(f"== lượt {r}/{a.stability} — {len(names)} cmd ==")
        for name in names:
            body = run_one(tl, env, name)
            key, hname = cmap.get(name, ("?", "?"))
            body["stub_key"] = key
            body["handler"] = hname
            raw = json.dumps(body, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
            bts = raw.encode("utf-8")
            if r == 1:
                (outdir / f"{name}.json").write_bytes(bts.replace(b"\r\n", b"\n"))
            else:
                if prev_bytes.get(name) != bts:
                    unstable.append(name)
            prev_bytes[name] = bts
            print(f"  [{key:10s}] {name:22s} rc={body['rc']} bytes={len(bts)}")
    if a.stability > 1:
        print(f"== stability ×{a.stability}: {'ỔN ĐỊNH byte-hệt' if not unstable else 'LỆCH: ' + ', '.join(unstable)} ==")
        return 1 if unstable else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
