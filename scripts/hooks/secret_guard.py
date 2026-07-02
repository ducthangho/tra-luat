#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""secret_guard.py — PreToolUse hook (Claude Code) chặn rò rỉ bí mật của tra-luat.

Ý tưởng mượn từ affaan-m/ecc (beforeSubmitPrompt secret-scan) nhưng THU HẸP cho skill này:
  - Gói tra-luat chứa TOKEN webapp THẬT trong tra_luat_config*.json → tuyệt đối không
    echo/commit/upload/dán ra ngoài.

Đăng ký trong settings.json (PreToolUse, matcher "Bash|Write|Edit"):
  {"type":"command","command":"python \"<đường-dẫn-skill>/scripts/hooks/secret_guard.py\""}

Hành vi: đọc JSON hook trên stdin; nếu phát hiện token/bí mật trong nội dung tool →
  exit 2 + thông báo stderr (Claude Code coi exit 2 là CHẶN tool call). Lỗi parse → exit 0
  (fail-open, không cản trở vận hành). KHÔNG in lại giá trị bí mật.
"""
import sys, json, re

# Mẫu bí mật (không log giá trị, chỉ báo TÊN loại)
# Tên loại để ASCII-only (tránh mojibake khi terminal không UTF-8)
_PATTERNS = [
    ("tra-luat webapp token (tl_)",   re.compile(r"\btl_(?!PLACEHOLDER)[A-Za-z0-9]{20,}")),
    ("Apps Script /exec?token= URL",  re.compile(r"script\.google\.com/macros/s/[\w-]+/exec\?[^\s\"']*token=")),
    ("OpenAI/Anthropic key (sk-)",    re.compile(r"\bsk-[A-Za-z0-9]{20,}")),
    ("GitHub token (gh*_)",           re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("AWS access key (AKIA)",         re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key (AIza)",         re.compile(r"\bAIza[0-9A-Za-z_\-]{30,}")),
    # GD0 (gws): credential nguoi dung XUAT tu `gws auth export --unmasked` + key service-account.
    # Chan GIA TRI bi mat; KHONG chan ten env GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE (duong dan, bridge dung hop le).
    ("Google OAuth client secret",    re.compile(r"\bGOCSPX-[A-Za-z0-9_\-]{20,}")),
    ("Google OAuth refresh token",    re.compile(r"\b1//[0-9A-Za-z_\-]{30,}")),
    ("Private key block (PEM)",       re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----")),
    ("service-account key JSON",      re.compile(r"\"type\"\s*:\s*\"service_account\"")),
    ("gws CLIENT_SECRET co gia tri",  re.compile(r"GOOGLE_WORKSPACE_CLI_CLIENT_SECRET\s*[=:]\s*\S")),
    # nlm (notebooklm-mcp-cli) auth.json/cookies.json: cookie phien Google (vd __Secure-1PSID/3PSID, SAPISID).
    ("NotebookLM/Google session cookie", re.compile(r"__Secure-[0-9]?PSID|\bSAPISID\b")),
]
# Lenh day bi mat ra ngoai (git add/commit/push, gh release/gist/pr, scp, rsync, curl upload)
# cham file nhay cam: config/token, script .gs, goi cai dat, hoac credential gws xuat ra.
_RISKY_FILE = re.compile(
    r"(git\s+(add|commit|push)|gh\s+(release|gist|pr)|scp\b|rsync\b|curl\b[^\n]*(-T|--upload-file))"
    r"[^\n]*?(tra_luat_config|INSTALL\.zip|Code\.[0-9].*\.gs|credentials\.json|creds\.json|notebooklm-mcp-cli)",
    re.IGNORECASE,
)
# GD0 (gws): `gws auth export` redirect/pipe ra ngoai (lo refresh_token/client_secret) — chan ngay khau lenh.
_GWS_EXPORT_LEAK = re.compile(
    r"gws\s+auth\s+export\b[^\n]*?(>|>>|\|\s*(tee|curl|nc|ncat|scp|rsync|gh|git|base64|xxd|clip|pbcopy))",
    re.IGNORECASE,
)


def _text_from(tool, ti):
    if tool == "Bash":
        return str(ti.get("command", "") or "")
    if tool == "Write":
        return str(ti.get("content", "") or "") + " " + str(ti.get("file_path", "") or "")
    if tool == "Edit":
        return str(ti.get("new_string", "") or "") + " " + str(ti.get("file_path", "") or "")
    return ""


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0  # fail-open
    tool = data.get("tool_name", "")
    text = _text_from(tool, data.get("tool_input", {}) or {})
    if not text:
        return 0
    hits = [name for name, rx in _PATTERNS if rx.search(text)]
    if _RISKY_FILE.search(text):
        hits.append("commit/upload file chua bi mat (config/token/.gs/INSTALL.zip/credentials.json)")
    if _GWS_EXPORT_LEAK.search(text):
        hits.append("gws auth export redirect/pipe (lo credential nguoi dung)")
    if hits:
        # ASCII-only để hiển thị sạch trên mọi terminal (tránh mojibake)
        sys.stderr.write(
            "[secret-guard] BLOCKED (chan thao tac): phat hien bi mat/dinh danh nhay cam: "
            + "; ".join(hits) + ".\n"
            "Khong echo/commit/upload token webapp hay tra_luat_config. "
            "Dung password manager / bien moi truong; neu chac chan an toan, chay thu cong ngoai hook.\n"
        )
        return 2  # CHAN
    return 0


if __name__ == "__main__":
    sys.exit(main())
