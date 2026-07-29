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
#   [ĐIỆN THOẠI] trình duyệt có extension → đăng nhập notebooklm.google.com → export cookie
#                → tải file lên Google Drive (ĐỪNG dán vào chat: đó là session Google đầy đủ)
#   [Ở ĐÂY]      ./nlm-cookie-import.sh --drive-id <fileId>
#
#   ./nlm-cookie-import.sh --file /path/cookies.json     # file đã có sẵn trong container
#   ./nlm-cookie-import.sh --drive-id <fileId>           # tải từ Drive bằng gws rồi nạp
#   ./nlm-cookie-import.sh --drive-id <id> --no-stage    # nạp nhưng KHÔNG đẩy lên bundle
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

SRC=""; DRIVE_ID=""; DO_STAGE=1
while [ $# -gt 0 ]; do
  case "$1" in
    --file)     SRC="${2:-}"; shift ;;
    --drive-id) DRIVE_ID="${2:-}"; shift ;;
    --no-stage) DO_STAGE=0 ;;
    -h|--help)  sed -n '2,26p' "$0"; exit 0 ;;
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
if [ -n "$DRIVE_ID" ]; then
  command -v gws >/dev/null 2>&1 || { bad "cần gws để tải từ Drive — ./scripts/env-reimport.sh --no-nlm"; exit 1; }
  SRC="$TMP/cookies.in"
  gws drive files get --params "{\"fileId\":\"$DRIVE_ID\",\"alt\":\"media\"}" --output "$SRC" >/dev/null 2>&1
  [ -s "$SRC" ] || { bad "không tải được fileId=$DRIVE_ID (sai id, hoặc gws không có quyền đọc)"; exit 1; }
  ok "tải từ Drive: $(stat -c%s "$SRC") byte"
elif [ -n "$SRC" ]; then
  [ -s "$SRC" ] || { bad "file rỗng/không tồn tại: $SRC"; exit 1; }
  ok "dùng file cục bộ: $SRC ($(stat -c%s "$SRC") byte)"
else
  bad "phải nêu --file hoặc --drive-id (xem --help)"; exit 1
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
BAT_BUOC = ["SID", "__Secure-1PSID", "__Secure-3PSID", "HSID", "SSID", "APISID", "SAPISID"]
thieu = [n for n in BAT_BUOC if not ck.get(n)]
print(f"  parse được {len(ck)} cookie")
if thieu:
    print(f"  THIẾU cookie bắt buộc: {thieu}", file=sys.stderr)
    print("  Nguyên nhân thường gặp: export chỉ lấy cookie của tab hiện tại (notebooklm.google.com)", file=sys.stderr)
    print("  mà các cookie phiên nằm ở domain .google.com / accounts.google.com.", file=sys.stderr)
    print("  → export TOÀN BỘ cookie domain google.com, hoặc mở accounts.google.com rồi export.", file=sys.stderr)
    sys.exit(2)
rts = [n for n in ("__Secure-1PSIDRTS", "__Secure-3PSIDRTS") if ck.get(n)]
print(f"  đủ {len(BAT_BUOC)} cookie phiên bắt buộc" + (f" · có rotation token {rts}" if rts else
      "  ⚠ KHÔNG có rotation token — phiên sẽ không tự gia hạn, dùng được nhưng ngắn"))
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
