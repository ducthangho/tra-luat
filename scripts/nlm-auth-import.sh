#!/usr/bin/env bash
# nlm-cookie-import.sh — nạp cookie NotebookLM lấy từ TRÌNH DUYỆT KHÁC (kể cả điện thoại)
# vào sandbox headless, rồi làm tươi bundle trên Drive cho mọi phiên sau.
#
# VÌ SAO CẦN: 9/13 cookie phiên Google là httpOnly ⇒ JavaScript/bookmarklet KHÔNG đọc được.
# Chỉ EXTENSION trình duyệt (API chrome.cookies) mới đọc được. Chrome Android không có
# extension ⇒ phải dùng trình duyệt Android CÓ extension (Quetta / Edge Canary / Firefox +
# add-on). `nlm login` tương tác thì KHÔNG chạy được ở đây (không màn hình, không CDP tới máy bạn).
#
# LUỒNG:
#   [ĐIỆN THOẠI] trình duyệt có extension → đăng nhập MỘT trang Google BẤT KỲ (Gmail /
#                myaccount.google.com — KHÔNG cần notebooklm.google.com, có thể bị chặn theo vùng)
#                → Cookie-Editor Export JSON → tải lên Google Drive (ĐỪNG dán chat: session đầy đủ)
#   VÌ SAO: 7 cookie nlm cần (SID/__Secure-1PSID/3PSID/HSID/SSID/APISID/SAPISID) là cookie ĐĂNG NHẬP
#   GOOGLE CHUNG trên .google.com — KHÔNG phải của notebooklm. Truy cập API NotebookLM xảy ra Ở
#   SANDBOX (vùng của nó, không bị chặn) — đã kiểm: jar cũ lấy từ .google.com.hk vẫn chạy 139 notebook.
#   [Ở ĐÂY]      ./scripts/nlm-auth-import.sh          ← không cần fileId, tự tìm
#
#   ./nlm-auth-import.sh                       # TỰ TÌM trên Drive file tên chứa 'nlm-auth' (mới nhất)
#   ./nlm-auth-import.sh --watch 15            # ĐỢI tới 15′ cho file MỚI xuất hiện rồi tự nạp
#   ./nlm-auth-import.sh --drive-find <chuỗi>  # tự tìm theo chuỗi khác
#   ./nlm-auth-import.sh --drive-id <fileId>   # nêu thẳng fileId
#   ./nlm-auth-import.sh --file /path/x.json   # file đã có sẵn trong container
#   ./nlm-auth-import.sh --no-stage            # nạp nhưng KHÔNG làm tươi bundle Drive
#
# Luồng "chỉ chạy 1 lệnh": ở đây bật --watch → trên điện thoại export JSON + lưu Drive →
# sandbox tự phát hiện, tự nạp, tự probe LIVE, tự làm tươi bundle. (Cái export vẫn cần người
# bấm — browser đã đăng nhập là hành động người-thật, không script hoá được.)
#
# Định dạng chấp nhận (theo extract_cookies_from_chrome_export của nlm):
#   · JSON list  [{"name":"SID","value":"..."}, ...]   ← export của hầu hết extension
#   · JSON dict  {"SID":"...","__Secure-1PSID":"..."}
#   · header     SID=...; __Secure-1PSID=...; ...
#
# rc: 0 = nạp + canary LIVE dương (+ stage xong nếu có stage) · 1 = sai tham số/thiếu điều kiện
#     2 = file cookie không hợp lệ · 3 = nlm từ chối cookie · 4 = nạp được nhưng canary LIVE ÂM (jar cũ khôi phục)
#     5 = stage lỗi (rc 4 của stage = canary của lệnh stage từ chối, 0 upload; khác = có thể đã ghi một phần)
#     6 = canary KHÔNG KẾT LUẬN (mạng/lỗi probe) — giữ jar vừa nạp, không stage (WP726)
set -uo pipefail

ROOT="${TL_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
[ -f "$ROOT/scripts/tl.py" ] || { echo "✗ không thấy scripts/tl.py — đặt TL_ROOT=<gốc skill>" >&2; exit 1; }
cd "$ROOT" || exit 1
PY="${TL_PYTHON:-python3}"
export PATH="$HOME/.local/bin:$PATH"

SRC=""; DRIVE_ID=""; DO_STAGE=1; FIND=""; WATCH=""
while [ $# -gt 0 ]; do
  case "$1" in
    --file)       SRC="${2:-}"; shift ;;
    --drive-id)   DRIVE_ID="${2:-}"; shift ;;
    --drive-find) FIND="${2:-nlm-auth}"; shift ;;
    --watch)      WATCH="${2:-15}"; shift ;;   # đợi tối đa N phút cho file MỚI xuất hiện trên Drive
    --no-stage)   DO_STAGE=0 ;;
    -h|--help)  sed -n '2,30p' "$0"; exit 0 ;;
    *) echo "✗ cờ lạ: $1" >&2; exit 1 ;;
  esac
  shift
done

ok()   { printf '  \033[32m[OK]\033[0m   %s\n' "$*"; }
bad()  { printf '  \033[31m[FAIL]\033[0m %s\n' "$*"; }
warn() { printf '  \033[33m[WARN]\033[0m %s\n' "$*"; }
say()  { printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

command -v nlm >/dev/null 2>&1 || { bad "chưa có nlm — chạy ./scripts/env-reimport.sh trước"; exit 1; }

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


# TMP có quyền 700; luôn xoá kể cả khi lỗi — file này là SESSION GOOGLE ĐẦY ĐỦ.
TMP="$(mktemp -d)"; chmod 700 "$TMP"; trap 'rm -rf "$TMP"' EXIT

say "1. Lấy file cookie"

# Trả về "id<TAB>epoch<TAB>name" của bản MỚI NHẤT khớp $1, rỗng nếu không có. epoch từ modifiedTime.
_pick_newest() {
  gws drive files list --params "{\"q\":\"name contains '$1' and trashed = false\",\"orderBy\":\"modifiedTime desc\",\"pageSize\":1,\"fields\":\"files(id,name,modifiedTime)\"}" 2>/dev/null \
  | $PY -c '
import json,sys
from datetime import datetime
try:
    fs=json.load(sys.stdin).get("files") or []
except Exception:
    fs=[]
if fs:
    f=fs[0]; mt=f.get("modifiedTime","")
    try:
        ep=int(datetime.fromisoformat(mt.replace("Z","+00:00")).timestamp())
    except Exception:
        ep=0
    # KHÔNG dùng f-string: Python 3.11 cấm backslash trong biểu thức f-string (\t) — dùng %.
    sys.stdout.write("%s\t%s\t%s" % (f["id"], ep, f.get("name","")))
'
}

# --watch: đợi file MỚI (modifiedTime > mốc lúc bắt đầu) — để bạn export trên điện thoại lúc nào
# cũng được, sandbox tự phát hiện rồi nạp. Không tự động hoá được cái export (browser+người), NHƯNG
# tự động hoá được toàn bộ khâu sau đó.
if [ -n "$WATCH" ] && [ -z "$DRIVE_ID" ] && [ -z "$SRC" ]; then
  command -v gws >/dev/null 2>&1 || { bad "cần gws để watch Drive"; exit 1; }
  W_FIND="${FIND:-nlm-auth}"
  BASE="$(_pick_newest "$W_FIND" | cut -f2)"; BASE="${BASE:-0}"
  DEADLINE=$(( $(date -u +%s) + WATCH * 60 ))
  ok "watch: đợi file mới tên chứa '$W_FIND' trên Drive (tối đa ${WATCH}′)"
  [ "$BASE" != "0" ] && printf '  \033[36m[..]\033[0m   mốc hiện tại: bản mới nhất @ epoch %s — chỉ nhận bản MỚI HƠN\n' "$BASE"
  echo "        → Trên điện thoại: export cookie JSON (Cookie-Editor) rồi lưu vào Drive tên có '$W_FIND'."
  while :; do
    ROW="$(_pick_newest "$W_FIND")"
    CID="$(printf '%s' "$ROW" | cut -f1)"; CEP="$(printf '%s' "$ROW" | cut -f2)"; CNAME="$(printf '%s' "$ROW" | cut -f3)"
    if [ -n "$CID" ] && [ "${CEP:-0}" -gt "${BASE:-0}" ]; then
      DRIVE_ID="$CID"; ok "phát hiện bản MỚI: $CNAME"; break
    fi
    if [ "$(date -u +%s)" -ge "$DEADLINE" ]; then
      bad "hết ${WATCH}′ mà không có file mới. Chạy lại khi đã export xong, hoặc tăng --watch."; exit 1
    fi
    sleep 20
  done
fi

# Không tham số nào ⇒ TỰ TÌM trên Drive. Mục tiêu: trên điện thoại bạn chỉ cần export rồi
# lưu vào Drive; ở đây gõ đúng một lệnh, KHÔNG phải đi tra fileId.
if [ -z "$DRIVE_ID" ] && [ -z "$SRC" ] && [ -z "$FIND" ]; then FIND="nlm-auth"; fi
if [ -n "$FIND" ] && [ -z "$DRIVE_ID" ]; then
  command -v gws >/dev/null 2>&1 || { bad "cần gws để tìm trên Drive"; exit 1; }
  Q="name contains '$FIND' and trashed = false"
  HITS="$(gws drive files list --params "{\"q\":\"$Q\",\"orderBy\":\"modifiedTime desc\",\"pageSize\":5,\"fields\":\"files(id,name,modifiedTime)\"}" 2>/dev/null)"
  N="$(printf '%s' "$HITS" | $PY -c 'import json,sys;print(len(json.load(sys.stdin).get("files") or []))' 2>/dev/null || echo 0)"
  if [ "${N:-0}" = "0" ]; then
    bad "không thấy file nào tên chứa '$FIND' trên Drive."
    echo "        Trên điện thoại: export cookie (JSON) rồi lưu vào Drive với tên có '$FIND'," >&2
    echo "        ví dụ 'nlm-auth-2026-07-29.json'. Hoặc nêu thẳng: --drive-id <fileId>" >&2
    exit 1
  fi
  printf '%s' "$HITS" | $PY -c '
import json,sys
fs=json.load(sys.stdin)["files"]
for i,f in enumerate(fs):
    print(("  → " if i==0 else "    ")+f"{f['"'"'name'"'"']}  ({f['"'"'modifiedTime'"'"']})")
' 2>/dev/null
  DRIVE_ID="$(printf '%s' "$HITS" | $PY -c 'import json,sys;print(json.load(sys.stdin)["files"][0]["id"])' 2>/dev/null)"
  [ -n "$DRIVE_ID" ] || { bad "không đọc được fileId từ kết quả tìm"; exit 1; }
  ok "chọn bản MỚI NHẤT (mũi tên) — id=${DRIVE_ID:0:12}…"
fi
if [ -n "$DRIVE_ID" ]; then
  command -v gws >/dev/null 2>&1 || { bad "cần gws để tải từ Drive — ./scripts/env-reimport.sh --no-nlm"; exit 1; }
  # gws CHẶN --output ra ngoài thư mục hiện tại ⇒ tải vào TRONG repo rồi xoá (thêm vào trap).
  mkdir -p scripts/.tl_state
  SRC="scripts/.tl_state/.authdl.$$"
  trap 'rm -f "'"$SRC"'"; rm -rf "$TMP"' EXIT
  # Google có thể ĐÃ chuyển .json thành Google Docs khi upload (mimeType vnd.google-apps.*) — khi đó
  # alt=media KHÔNG tải được, phải export text/plain. Đo 29-07: upload .json qua điện thoại ⇒ Docs.
  MIME="$(gws drive files get --params "{\"fileId\":\"$DRIVE_ID\",\"fields\":\"mimeType\"}" 2>/dev/null | $PY -c 'import json,sys;print((json.load(sys.stdin) or {}).get("mimeType",""))' 2>/dev/null)"
  if printf '%s' "$MIME" | grep -q 'application/vnd.google-apps'; then
    warn "Drive đã chuyển file thành Google Docs ($MIME) — export text/plain để lấy lại JSON thô"
    gws drive files export --params "{\"fileId\":\"$DRIVE_ID\",\"mimeType\":\"text/plain\"}" --output "$SRC" >/dev/null 2>&1
  else
    gws drive files get --params "{\"fileId\":\"$DRIVE_ID\",\"alt\":\"media\"}" --output "$SRC" >/dev/null 2>&1
  fi
  [ -s "$SRC" ] || { bad "không tải được fileId=$DRIVE_ID (sai id, gws không có quyền, hoặc export lỗi)"; exit 1; }
  # Docs export chèn BOM (﻿) đầu file ⇒ json.loads nổ "Unexpected UTF-8 BOM". Cắt sớm.
  $PY -c 'import sys,pathlib;p=pathlib.Path(sys.argv[1]);b=p.read_bytes();p.write_bytes(b[3:] if b[:3]==b"\xef\xbb\xbf" else b)' "$SRC"
  ok "tải từ Drive: $(stat -c%s "$SRC") byte"
elif [ -n "$SRC" ]; then
  [ -s "$SRC" ] || { bad "file rỗng/không tồn tại: $SRC"; exit 1; }
  ok "dùng file cục bộ: $SRC ($(stat -c%s "$SRC") byte)"
else
  bad "không có nguồn cookie (xem --help)"; exit 1
fi

# ── 2. Kiểm định dạng + ĐỦ cookie, TRƯỚC khi đụng vào jar đang có ──
say "2. Kiểm định dạng (chưa đụng jar sống)"
# Netscape .txt KHÔNG được hỗ trợ — bắt sớm, nói rõ (extension phổ biến "Get cookies.txt LOCALLY"
# xuất đúng định dạng này). Không có ';' nên helper cũng parse rỗng → thông điệp chung vô ích.
if head -c 200 "$SRC" | grep -qE '^# Netscape|^\.[a-z].*\t.*\t' 2>/dev/null; then
  bad "file là định dạng Netscape (tab-separated) — nlm KHÔNG đọc được."
  echo "        Dùng extension export JSON (Cookie Quick Manager), KHÔNG phải Netscape .txt." >&2
  exit 2
fi
ok "không phải Netscape"

# ── 3. Chuyển → jar LIST giữ domain (r240: thay `nlm login --manual` vốn làm phẳng mất domain) ──
say "3. Nạp vào nlm (jar LIST giữ domain)"
JAR="$HOME/.notebooklm-mcp-cli"
PDIR="$JAR/profiles/default"
if [ -d "$JAR" ]; then
  cp -a "$JAR" "$TMP/jar.bak" && ok "đã sao lưu jar hiện có (khôi phục được nếu hỏng)"
fi
# nlm_auth_convert VALIDATE trước (identity 7 + LSID) rồi mới ghi — thiếu ⇒ rc≠0, KHÔNG ghi jar.
$PY scripts/nlm_auth_convert.py "$SRC" "$PDIR" "${TL_NLM_EMAIL:-ducthangho@gmail.com}"; CONV_RC=$?
if [ "$CONV_RC" != 0 ]; then
  bad "cookie KHÔNG dùng được (xem lý do trên) — jar cũ giữ nguyên"
  [ -d "$TMP/jar.bak" ] && { rm -rf "$JAR"; cp -a "$TMP/jar.bak" "$JAR"; }
  exit "$CONV_RC"
fi
ok "đã ghi jar (nlm sẽ tự mint *PSIDTS qua RotateCookies khi probe)"

# ── 4. PHÁN QUYẾT = canary LIVE trên đúng notebook (WP726: KHÔNG dùng `nlm login --check` — false-green) ──
say "4. Canary LIVE"
_canary_song; CANARY_RC=$?
if [ "$CANARY_RC" = 0 ]; then
  ok "NLM SỐNG — canary dương trên đúng notebook"
elif [ "$CANARY_RC" = 2 ]; then
  bad "canary KHÔNG KẾT LUẬN được (mạng/lỗi probe) — giữ jar vừa nạp, KHÔNG stage; chạy lại sau."
  exit 6
else
  bad "nạp xong nhưng canary LIVE vẫn ÂM (cookie không đọc được đúng notebook)."
  [ -d "$TMP/jar.bak" ] && { rm -rf "$JAR"; cp -a "$TMP/jar.bak" "$JAR"; warn "đã khôi phục jar cũ"; }
  exit 4
fi

# ── 5. Làm tươi bundle trên Drive để phiên SAU khỏi làm lại ──
if [ "$DO_STAGE" = 1 ]; then
  say "5. Đẩy cookie tươi vào bundle Drive"
  if [ -z "${TL_TOKEN:-}" ]; then
    warn "thiếu TL_TOKEN — bỏ qua stage. Phiên sau sẽ phải nhập cookie lại."
  else
    # Chỉ dùng MÃ THOÁT (WP726): rc 4 = canary của chính lệnh stage không dương ⇒ 0 upload; rc khác 0 còn lại
    # = lỗi stage, có thể đã ghi một phần. Không in đầu ra của lệnh.
    $PY scripts/tl.py nlm-auth-stage >/dev/null 2>&1; STAGE_RC=$?
    if [ "$STAGE_RC" = 0 ]; then
      ok "bundle Drive đã tươi — phiên sau chỉ cần: tl nlm-auth-load"
    elif [ "$STAGE_RC" = 4 ]; then
      bad "nlm-auth-stage rc=4: canary của lệnh stage KHÔNG dương — KHÔNG upload gì."
      exit 5
    else
      bad "nlm-auth-stage rc=$STAGE_RC: lỗi stage — có thể đã ghi một phần, kiểm Drive trước khi thử lại."
      exit 5
    fi
  fi
else
  say "5. BỎ QUA stage (--no-stage)"
fi

say "XONG — NLM sẵn sàng"
echo "  File cookie tạm đã được xoá. Nhớ XOÁ luôn bản trên Drive/điện thoại:"
echo "  nó là session Google đầy đủ, không phải token giới hạn phạm vi."
