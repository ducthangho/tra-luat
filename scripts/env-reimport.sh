#!/usr/bin/env bash
# env-reimport.sh — dựng lại TOÀN BỘ môi trường tra-luat trong sandbox Linux headless
# (Claude Code on the web / Cowork). Idempotent: chạy lại nhiều lần vô hại.
#
# Cần DUY NHẤT `TL_TOKEN` (webapp token) trong env — đó là khoá giải mã đường public `.enc`.
# KHÔNG cần TL_MASTER_KEY. Mọi fileId đã baked sẵn trong scripts/tl.py.
#
#   ./env-reimport.sh              # gws + nlm + kiểm LIVE
#   ./env-reimport.sh --no-nlm     # chỉ gws (đủ cho Drive/deploy)
#   ./env-reimport.sh --check      # chỉ kiểm, KHÔNG cài/không ghi cred
#   ./env-reimport.sh --force-nlm  # cho phép nlm-auth-load --force (BỎ chốt chống hạ cấp)
#
# rc: 0 = mọi thứ sống · 1 = thiếu điều kiện đầu vào · 2 = gws hỏng
#     3 = gws OK nhưng NLM chết (canary LIVE không dương; làm tươi ở máy giữ hồ sơ trình duyệt gốc)
#     4 = gws OK nhưng canary NLM KHÔNG KẾT LUẬN được (mạng/lỗi probe) — không phải sống, không phải chết
set -uo pipefail

ROOT="${TL_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
[ -f "$ROOT/scripts/tl.py" ] || ROOT="$(cd "$ROOT/.." && pwd)"
[ -f "$ROOT/scripts/tl.py" ] || { echo "✗ không tìm thấy scripts/tl.py — đặt TL_ROOT=<gốc skill>" >&2; exit 1; }
cd "$ROOT" || exit 1

PY="${TL_PYTHON:-python3}"
TL="$PY scripts/tl.py"
export PATH="$HOME/.local/bin:$PATH"

DO_NLM=1; CHECK_ONLY=0; FORCE_NLM=0
while [ $# -gt 0 ]; do
  case "$1" in
    --no-nlm)    DO_NLM=0 ;;
    --check)     CHECK_ONLY=1 ;;
    --force-nlm) FORCE_NLM=1 ;;
    -h|--help)   sed -n '2,16p' "$0"; exit 0 ;;
    *) echo "✗ cờ lạ: $1 (xem --help)" >&2; exit 1 ;;
  esac
  shift
done

say()  { printf '\n\033[1m== %s ==\033[0m\n' "$*"; }
ok()   { printf '  \033[32m[OK]\033[0m   %s\n' "$*"; }
bad()  { printf '  \033[31m[FAIL]\033[0m %s\n' "$*"; }
warn() { printf '  \033[33m[WARN]\033[0m %s\n' "$*"; }
info() { printf '  \033[36m[..]\033[0m   %s\n' "$*"; }

# ─────────────────────── 0. Điều kiện đầu vào ───────────────────────
say "0. Điều kiện đầu vào"
if [ -z "${TL_TOKEN:-}" ]; then
  bad "thiếu TL_TOKEN — không có khoá giải mã cred."
  echo "        export TL_TOKEN='<webapp token GAS>'   (và TL_WEBAPP nếu chưa có)" >&2
  exit 1
fi
ok "TL_TOKEN có (${#TL_TOKEN} ký tự)"
[ -n "${TL_WEBAPP:-}" ] && ok "TL_WEBAPP có (${#TL_WEBAPP} ký tự)" || warn "TL_WEBAPP trống — dựa vào config/baked"

info "ping webapp…"
if $TL ping 2>/dev/null | grep -q '"ok": *true'; then
  ok "webapp sống — $($TL ping 2>/dev/null | $PY -c 'import json,sys;d=json.load(sys.stdin);print("version="+str(d.get("version")))' 2>/dev/null)"
else
  bad "webapp KHÔNG trả lời (token sai/hết hạn, hoặc egress chặn script.google.com)"; exit 1
fi

# ─────────────────────── 1. gws (Drive) ───────────────────────
say "1. gws — transport Drive"
if command -v gws >/dev/null 2>&1; then
  ok "gws đã có: $(command -v gws) ($(gws --version 2>/dev/null | head -1))"
elif [ "$CHECK_ONLY" = 1 ]; then
  warn "gws CHƯA cài (--check nên không cài)"
else
  info "cài gws + giải mã cred (gws-bootstrap-cowork)…"
  $TL gws-bootstrap-cowork >/dev/null 2>&1 || { bad "gws-bootstrap-cowork lỗi — chạy tay để xem log"; exit 2; }
  ok "đã cài gws + nạp cred"
fi

if [ ! -s "$HOME/.config/gws/credentials.json" ] && [ "$CHECK_ONLY" = 0 ]; then
  info "nạp lại cred (gws-auth-load)…"
  $TL gws-auth-load >/dev/null 2>&1 || warn "gws-auth-load lỗi"
fi

if $TL gws-ping --env cowork >/dev/null 2>&1; then
  ok "gws-ping rc=0"
else
  bad "gws-ping ĐỎ"; exit 2
fi

# smoke THẬT: chứng minh refresh_token đổi được access token, không chỉ đọc config
if gws drive files list --params '{"pageSize":1}' >/dev/null 2>&1; then
  ok "smoke LIVE: Drive trả dữ liệu (refresh_token còn hiệu lực)"
else
  bad "gws auth cấu hình OK nhưng gọi Drive THẤT BẠI — refresh_token có thể đã bị thu hồi."
  echo "        Sửa ở máy có browser: gws auth login → python scripts/tl.py gws-auth-stage" >&2
  exit 2
fi

# ─────────────────────── 2. nlm (NotebookLM) ───────────────────────
_canary_song() {  # WP726: 0 sống · 3 chết · 2 không kết luận. Cùng cổng `nlm-auth-stage` của WP710: thân trả về
  # phải ĐÚNG notebook (`require_notebook_body=True`); rc 0 hay số notebook KHÔNG đủ. KHÔNG in gì của probe
  # (thông điệp có thể mang stderr thô của nlm) — chỉ dùng mã thoát.
  "$PY" - >/dev/null 2>&1 <<'PY'
import sys
sys.path.insert(0, "scripts")
try:
    import tl
    tg = tl._imp("tl_gws")
    tg.bind(tl)
    alive, _ = tg._nlm_auth_alive(tg._nlm_canary_notebook(None), require_notebook_body=True)
except Exception:
    alive = None
sys.exit(0 if alive is True else 3 if alive is False else 2)
PY
}

NLM_RC=0
if [ "$DO_NLM" = 0 ]; then
  say "2. nlm — BỎ QUA (--no-nlm)"
else
  say "2. nlm — NotebookLM CLI"
  if command -v nlm >/dev/null 2>&1; then
    ok "nlm đã có: $(command -v nlm)"
  elif [ "$CHECK_ONLY" = 1 ]; then
    warn "nlm CHƯA cài (--check)"
  else
    info "cài nlm (nlm-install — tải Python 3.11 từ Drive nếu cần)…"
    $TL nlm-install >/dev/null 2>&1 || warn "nlm-install lỗi — sẽ fallback NotebookLM MCP"
  fi

  if command -v nlm >/dev/null 2>&1 && [ "$CHECK_ONLY" = 0 ]; then
    info "kéo cookie mới nhất từ Drive (nlm-auth-load)…"
    LOAD_OUT="$($TL nlm-auth-load 2>&1)"; LOAD_RC=$?
    if [ $LOAD_RC -eq 0 ]; then
      ok "nạp cookie xong"
    elif printf '%s' "$LOAD_OUT" | grep -q "TỪ CHỐI HẠ CẤP"; then
      # Chốt r229: bundle trên Drive CŨ HƠN jar cục bộ ⇒ ghi đè sẽ giết cookie tươi hơn.
      # KHÔNG tự --force: nếu jar cục bộ cũng chết thì bundle càng chết, force vô ích.
      warn "chốt chống hạ cấp CHẶN: bundle trên Drive cũ hơn jar cục bộ — KHÔNG ghi đè (đúng)"
      printf '        %s\n' "$(printf '%s' "$LOAD_OUT" | head -1)"
      if [ "$FORCE_NLM" = 1 ]; then
        warn "--force-nlm: ép ghi đè theo yêu cầu"
        $TL nlm-auth-load --force >/dev/null 2>&1 && ok "đã ép nạp" || warn "ép nạp vẫn lỗi"
      fi
    else
      warn "nlm-auth-load lỗi: $(printf '%s' "$LOAD_OUT" | head -1)"
    fi
  fi

  # PHÁN QUYẾT DUY NHẤT = probe LIVE. Tuổi cookie/cờ rotation KHÔNG kết luận thay được.
  if command -v nlm >/dev/null 2>&1; then
    info "canary LIVE (đúng notebook, không dùng nlm login --check)…"
    _canary_song; CANARY_RC=$?
    if [ "$CANARY_RC" = 0 ]; then
      ok "NLM SỐNG — canary dương trên đúng notebook"
    elif [ "$CANARY_RC" = 2 ]; then
      NLM_RC=4
      warn "canary NLM KHÔNG KẾT LUẬN được (mạng/lỗi probe) — chưa biết sống hay chết; chạy lại sau."
    else
      NLM_RC=3
      bad "NLM CHẾT — phiên hết hạn, KHÔNG cứu được từ sandbox headless."
      echo "        Cookie phiên Google xoay từ browser profile; container này không có." >&2
      echo "        CÁCH A — máy có trình duyệt (Windows/desktop):" >&2
      echo "            máy giữ hồ sơ trình duyệt gốc: đăng nhập lại nếu cần, rồi pwsh -NoProfile -File scripts/nlm-credential-refresh.ps1 -ConfigPath <config>" >&2
      echo "            rồi quay lại đây chạy: ./scripts/env-reimport.sh" >&2
      echo "        CÁCH B — chỉ có điện thoại: trình duyệt CÓ EXTENSION (Quetta/Edge Canary/" >&2
      echo "            Firefox+add-on) → đăng nhập notebooklm.google.com → export cookie JSON" >&2
      echo "            → tải lên Drive → ./scripts/nlm-auth-import.sh --drive-id <fileId>" >&2
      echo "            (Chrome Android KHÔNG được: không extension, mà 9/13 cookie là httpOnly)" >&2
      echo "        LƯU Ý: KHÔNG có đường 'fallback NotebookLM MCP' ở phiên này — đã đo:" >&2
      echo "            phiên chỉ có server github; MCP của gói nlm cũng dùng CHUNG cookie này." >&2
    fi
  fi
fi

# ─────────────────────── 3. Tổng kết ───────────────────────
say "3. Tổng kết"
$TL doctor 2>&1 | grep -E "^(✓|⚠|⛔).*(credential|nlm|gws|webapp ping|API_CONTRACT)" | sed 's/^/  /'

if [ "$NLM_RC" = 0 ]; then
  say "SẴN SÀNG — gws + nlm đều sống"
  exit 0
fi
if [ "$NLM_RC" = 4 ]; then
  say "gws SỐNG · NLM KHÔNG KẾT LUẬN (rc=4)"
  echo "  Deploy/Drive/registry chạy bình thường. Canary NLM chưa trả lời được — chạy lại để biết sống/chết."
  exit 4
fi
say "gws SỐNG · NLM CHẾT (rc=3)"
echo "  Deploy/Drive/registry chạy bình thường. Chỉ đường NLM CLI bị chặn."
exit 3
