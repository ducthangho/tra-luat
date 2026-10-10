#!/usr/bin/env bash
# nlm-auto-refresh.sh — TỰ ĐỘNG refresh NLM cho Routine bảo trì (không tương tác).
#
# Logic (STATELESS, so mốc modifiedTime trên Drive — không cần nhớ trạng thái giữa phiên):
#   · Có file 'nlm-auth' MỚI HƠN bundle nlm_cred.enc  ⇒ export tươi user vừa thả vào Drive
#       → import (nlm-auth-import.sh) → stage vào bundle mã hoá → XOÁ plaintext khỏi Drive (bảo mật).
#   · Không có file mới                                 ⇒ keep-warm: nạp bundle, probe, stage lại nếu sống.
#   · Bước cuối = `tl nlm-auth-stage` (tự chạy canary LIVE trước khi đọc jar, WP710) quyết định rc:
#     0 sống + bundle tươi · 3 chết (canary không dương, cần re-harvest) · 2 gws/hạ tầng hỏng hoặc không kết luận.
#
# Dành cho Routine phiên-mới: chỉ cần TL_TOKEN (môi trường inject). KHÔNG commit/push/sửa code.
set -uo pipefail
ROOT="${TL_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
[ -f "$ROOT/scripts/tl.py" ] || { echo "✗ không thấy scripts/tl.py"; exit 2; }
cd "$ROOT" || exit 2
PY="${TL_PYTHON:-python3}"
export PATH="$HOME/.local/bin:$PATH"

say(){ printf '\n== %s ==\n' "$*"; }
[ -n "${TL_TOKEN:-}" ] || { echo "✗ thiếu TL_TOKEN"; exit 2; }

# ── 0. đảm bảo gws + nlm ──
say "0. hạ tầng"
command -v gws >/dev/null 2>&1 || $PY scripts/tl.py gws-bootstrap-cowork >/dev/null 2>&1 || { echo "✗ gws"; exit 2; }
$PY scripts/tl.py gws-ping --env cowork >/dev/null 2>&1 || { echo "✗ gws-ping ĐỎ (gws auth hỏng)"; exit 2; }
command -v nlm >/dev/null 2>&1 || $PY scripts/tl.py nlm-install >/dev/null 2>&1 || echo "  ⚠ nlm chưa cài được"
echo "  gws OK"

# ── 1. so mốc: có export MỚI HƠN bundle không? ──
say "1. dò export mới trên Drive"
BUNDLE_ID="$($PY -c 'import sys;sys.path.insert(0,"scripts");import tl;print(tl.NLM_CRED_FILEID)' 2>/dev/null)"
_epoch(){ # in epoch modifiedTime của fileId $1 (0 nếu lỗi)
  gws drive files get --params "{\"fileId\":\"$1\",\"fields\":\"modifiedTime\"}" 2>/dev/null \
  | $PY -c 'import json,sys
from datetime import datetime
try:
    mt=json.load(sys.stdin).get("modifiedTime","")
    print(int(datetime.fromisoformat(mt.replace("Z","+00:00")).timestamp()))
except Exception: print(0)'
}
BUNDLE_EP="$(_epoch "$BUNDLE_ID")"
# file plaintext 'nlm-auth' mới nhất
NEW_ROW="$(gws drive files list --params '{"q":"name contains \"nlm-auth\" and trashed = false","orderBy":"modifiedTime desc","pageSize":1,"fields":"files(id,name,modifiedTime)"}' 2>/dev/null \
  | $PY -c 'import json,sys
from datetime import datetime
try:
    fs=json.load(sys.stdin).get("files") or []
    if fs:
        f=fs[0]; ep=int(datetime.fromisoformat(f["modifiedTime"].replace("Z","+00:00")).timestamp())
        sys.stdout.write("%s\t%s\t%s" % (f["id"], ep, f.get("name","")))
except Exception: pass')"
NEW_ID="$(printf '%s' "$NEW_ROW" | cut -f1)"; NEW_EP="$(printf '%s' "$NEW_ROW" | cut -f2)"; NEW_NAME="$(printf '%s' "$NEW_ROW" | cut -f3)"
echo "  bundle epoch=$BUNDLE_EP · export mới nhất=${NEW_NAME:-<không có>} epoch=${NEW_EP:-0}"

REFRESHED=0
if [ -n "$NEW_ID" ] && [ "${NEW_EP:-0}" -gt "${BUNDLE_EP:-0}" ]; then
  # ── 2a. có export tươi → import + stage + xoá plaintext ──
  say "2. IMPORT export tươi ($NEW_NAME)"
  if ./scripts/nlm-auth-import.sh --drive-id "$NEW_ID" 2>&1 | sed 's/^/  /'; then
    REFRESHED=1
    # chỉ xoá plaintext SAU khi import+stage thành công (đã mã hoá an toàn vào bundle)
    gws drive files delete --params "{\"fileId\":\"$NEW_ID\"}" >/dev/null 2>&1 \
      && echo "  ✓ đã xoá plaintext '$NEW_NAME' khỏi Drive (đã mã hoá vào bundle)" \
      || echo "  ⚠ không xoá được plaintext '$NEW_NAME' — xoá tay cho an toàn"
    rm -f "$ROOT/download.html" 2>/dev/null || true
  else
    echo "  ⚠ import export tươi THẤT BẠI — giữ nguyên plaintext để soi tay"
  fi
else
  # ── 2b. không có export mới → keep-warm ──
  say "2. keep-warm (không có export mới)"
  $PY scripts/tl.py nlm-auth-load >/dev/null 2>&1 || true
fi

# ── 3. canary LIVE + stage quyết định trạng thái (WP726) ──
# KHÔNG dùng `nlm login --check` (false-green). Phán quyết = mã thoát của `nlm-auth-stage`: lệnh ấy tự chạy canary
# LIVE trên đúng notebook TRƯỚC khi đọc jar và chỉ upload khi canary dương (WP710). Không in đầu ra của lệnh
# (chỉ mã) và KHÔNG nuốt mã thoát.
say "3. canary LIVE + stage"
if [ "$REFRESHED" = 1 ]; then
  # Import vừa xong đã qua canary VÀ đã stage thành công (nlm-auth-import thoát khác 0 nếu một trong hai hỏng)
  # ⇒ không stage lần hai (WP726 lượt review 1, F2).
  echo "  ✓ NLM SỐNG (canary dương, bundle tươi) — vừa refresh từ export mới"
  exit 0
fi
$PY scripts/tl.py nlm-auth-stage >/dev/null 2>&1
STAGE_RC=$?
if [ "$STAGE_RC" = 0 ]; then
  echo "  ✓ NLM SỐNG (canary dương, bundle tươi) — keep-warm"
  exit 0
fi
if [ "$STAGE_RC" != 4 ]; then
  echo "  ✗ nlm-auth-stage rc=$STAGE_RC — hạ tầng/không kết luận; có thể đã ghi một phần, kiểm Drive trước khi thử lại"
  exit 2
fi
echo "  🔴 NLM CHẾT (canary không dương, 0 upload) — cần re-harvest cookie:"
echo "     điện thoại: Firefox + Cookie Quick Manager → export toàn bộ cookie google → Drive"
echo "     (tài khoản ducthangho@gmail.com, tên có 'nlm-auth'); Routine sau tự import."
echo "     hoặc máy giữ hồ sơ trình duyệt gốc: đăng nhập lại nếu cần, rồi pwsh -NoProfile -File scripts/nlm-credential-refresh.ps1 -ConfigPath <config>"
exit 3
