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
# rc: 0 = nạp + probe LIVE xanh · 1 = sai tham số/thiếu điều kiện · 2 = file cookie không hợp lệ
#     3 = nlm từ chối cookie · 4 = nạp được nhưng probe LIVE vẫn đỏ
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
say "2. Kiểm nội dung (chưa ghi đè gì)"
$PY - "$SRC" <<'PY'
import json, sys, pathlib
raw = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore").strip()
ck = {}
try:
    d = json.loads(raw)
    if isinstance(d, list):
        for c in d:
            if isinstance(c, dict) and c.get("name"): ck[str(c["name"])] = str(c.get("value", ""))
    elif isinstance(d, dict):
        ck = {str(k): str(v) for k, v in d.items()}
except json.JSONDecodeError:
    for it in raw.split(";"):
        if "=" in it:
            n, v = it.strip().split("=", 1)
            if n.strip(): ck[n.strip()] = v
# Netscape .txt KHÔNG được nlm hỗ trợ. Kiểm TRƯỚC `not ck`: tệp Netscape không có dấu ';'
# nên parse ra rỗng và rơi vào thông báo chung vô ích — đúng ca hay gặp nhất, vì extension
# phổ biến nhất ("Get cookies.txt LOCALLY") xuất chính định dạng này. ĐÃ ĐO: bản đầu của
# script này in nhầm thông báo chung cho tệp Netscape.
if raw.lstrip().startswith("# Netscape") or "\t" in raw.split("\n")[0]:
    print("  Đây là định dạng Netscape (tab-separated) — nlm KHÔNG đọc được.", file=sys.stderr)
    print("  Dùng extension export JSON, hoặc chuyển sang chuỗi header:", file=sys.stderr)
    print("    awk -F'\\t' '!/^#/&&NF>=7{printf \"%s%s=%s\", s, $6, $7; s=\"; \"}' vao.txt > ra.header",
          file=sys.stderr)
    sys.exit(2)
if not ck:
    print("  KHÔNG parse được: không phải JSON list/dict cũng không phải chuỗi header", file=sys.stderr)
    sys.exit(2)
print(f"  parse được {len(ck)} cookie")
# r238: BA TẦNG. Đo 29-07 (export 19 cookie ĐỎ ở probe): 7 cookie định-danh KHÔNG đủ — API
# NotebookLM còn đòi cookie DẤU-THỜI-GIAN phiên (*PSIDTS) và cookie ĐĂNG NHẬP (LSID/__Host-GAPS,
# chỉ sống ở accounts.google.com). Chặn TRƯỚC khi nạp, thay vì để probe LIVE mới lộ (đắt hơn).
DINH_DANH = ["SID", "__Secure-1PSID", "__Secure-3PSID", "HSID", "SSID", "APISID", "SAPISID"]
thieu = [n for n in DINH_DANH if not ck.get(n)]
has_ts  = any(ck.get(n) for n in ("__Secure-1PSIDTS", "__Secure-3PSIDTS"))
has_lsid = bool(ck.get("LSID"))
has_rts = any(ck.get(n) for n in ("__Secure-1PSIDRTS", "__Secure-3PSIDRTS"))
def _guide():
    print("  → SỬA: mở tab accounts.google.com (đã đăng nhập) rồi Cookie-Editor Export JSON.", file=sys.stderr)
    print("    accounts.google.com là NƠI DUY NHẤT mang LSID/__Host-GAPS *và* thấy cả cookie .google.com", file=sys.stderr)
    print("    (SID/*PSIDTS/*PSIDRTS). Export từ Gmail/myaccount HỤT nhóm đăng nhập — đó là ca vừa lỗi.", file=sys.stderr)
    print("    Đảm bảo Cookie-Editor export TOÀN BỘ cookie của trang, không lọc.", file=sys.stderr)
if thieu:
    print(f"  THIẾU cookie định-danh: {thieu}", file=sys.stderr); _guide(); sys.exit(2)
# r239 (đo 29-07): LSID là CỔNG THẬT. Kiểm chứng LIVE: bản chỉ có định-danh (thiếu LSID/__Host/*RTS)
# bị Google ĐẨY VỀ signin dù đã mint *PSIDTS qua RotateCookies ⇒ *PSIDTS KHÔNG phải nút thắt (nlm tự
# mint). Nút thắt = cookie ĐĂNG NHẬP (LSID/__Host-GAPS) + ROTATION (*PSIDRTS), chỉ có ở accounts.google.com.
if not has_lsid:
    print("  THIẾU LSID — cookie ĐĂNG NHẬP (sống ở accounts.google.com). ĐÂY là nút thắt:", file=sys.stderr)
    print("  đo LIVE 29-07: bộ cookie THIẾU LSID bị Google ĐẨY VỀ signin dù đã mint *PSIDTS.", file=sys.stderr)
    _guide(); sys.exit(2)
print(f"  đủ {len(DINH_DANH)} định-danh + LSID"
      + ("" if has_ts else " (thiếu *PSIDTS — nlm sẽ tự mint qua RotateCookies, KHÔNG chặn)")
      + (" · có *PSIDRTS (tự gia hạn)" if has_rts else
         "\n  ⚠ thiếu *PSIDRTS — phiên KHÔNG tự gia hạn; nếu Google vẫn đẩy signin thì cần export lại đủ hơn"))
PY
RC=$?; [ $RC -eq 0 ] || { bad "file cookie không dùng được (xem lý do trên)"; exit 2; }
ok "định dạng + độ đủ: đạt"

# ── 3. Sao lưu jar hiện có rồi nạp ──
say "3. Nạp vào nlm"
JAR="$HOME/.notebooklm-mcp-cli"
if [ -d "$JAR" ]; then
  cp -a "$JAR" "$TMP/jar.bak" && ok "đã sao lưu jar hiện có (khôi phục được nếu nạp hỏng)"
fi
if nlm login --manual -f "$SRC" 2>&1 | sed 's/^/     /'; then
  ok "nlm nhận cookie"
else
  bad "nlm TỪ CHỐI cookie"
  [ -d "$TMP/jar.bak" ] && { rm -rf "$JAR"; cp -a "$TMP/jar.bak" "$JAR"; warn "đã khôi phục jar cũ"; }
  exit 3
fi

# ── 4. PHÁN QUYẾT = probe LIVE (không tin bước 3 báo thành công) ──
say "4. Probe LIVE"
if CHK="$(nlm login --check 2>&1)" && printf '%s' "$CHK" | grep -qi "valid"; then
  ok "NLM SỐNG — $(printf '%s' "$CHK" | grep -iE 'notebooks found|account' | tr '\n' ' ' | sed 's/  */ /g')"
else
  bad "nạp xong nhưng probe LIVE vẫn ĐỎ:"; printf '%s\n' "$CHK" | sed 's/^/       /'
  [ -d "$TMP/jar.bak" ] && { rm -rf "$JAR"; cp -a "$TMP/jar.bak" "$JAR"; warn "đã khôi phục jar cũ"; }
  exit 4
fi

# ── 5. Làm tươi bundle trên Drive để phiên SAU khỏi làm lại ──
if [ "$DO_STAGE" = 1 ]; then
  say "5. Đẩy cookie tươi vào bundle Drive"
  if [ -z "${TL_TOKEN:-}" ]; then
    warn "thiếu TL_TOKEN — bỏ qua stage. Phiên sau sẽ phải nhập cookie lại."
  elif $PY scripts/tl.py nlm-auth-stage 2>&1 | tail -2 | sed 's/^/     /'; then
    ok "bundle Drive đã tươi — phiên sau chỉ cần `tl nlm-auth-load`"
  else
    warn "nlm-auth-stage lỗi — cookie ở ĐÂY vẫn dùng được, chỉ là chưa chia sẻ cho phiên khác"
  fi
else
  say "5. BỎ QUA stage (--no-stage)"
fi

say "XONG — NLM sẵn sàng"
echo "  File cookie tạm đã được xoá. Nhớ XOÁ luôn bản trên Drive/điện thoại:"
echo "  nó là session Google đầy đủ, không phải token giới hạn phạm vi."
