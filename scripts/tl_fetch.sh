#!/bin/sh
# tl_fetch.sh — chạy tl.py từ bản TẢI VỀ (mạng giao byte trung thực) thay vì mount Cowork hay cắt cụt (#51435/#53940).
# Zip skill PUBLIC → curl `drive.usercontent.google.com` (proxy allowlist cho domain này; NHANH NHẤT, off-context,
# KHÔNG cần token). GHI VÀO THƯ MỤC MÌNH SỞ HỮU ($HOME/.tl_fetch) — KHÔNG /tmp (sticky bit: file rác owner `nobody`
# chặn `curl -o` → exit 23, và file rỗng làm script tưởng "đã có").  Shell (sống sót cắt cụt) + nhỏ (dán-lại được).
#   sh scripts/tl_fetch.sh <args>        # tải zip 1 lần → chạy `tl.py <args>` từ bản sạch
#   sh scripts/tl_fetch.sh --setup [--nlm]   # BOOTSTRAP đủ: CONFIG(curl public)+GWS TRƯỚC → init-config → ping → gws(direct-media) → boot [→ nlm uv]
#   sh scripts/tl_fetch.sh --setup-step core|gws|boot|nlm   # v1.32.2 (Cowork 45s/lệnh): TÁCH BƯỚC — mỗi lệnh 1 bước
#       core = config + init-config + ping + uv · gws = gws-bootstrap · boot = boot · nlm = nlm-install --resume
#       (bước nlm chạy LẶP CÙNG LỆNH tới khi hết PARTIAL — rc=3 là còn bước, KHÔNG phải lỗi)
# Subsequent (nhanh hơn, khỏi qua script):  cd "$(cat ~/.tl_fetch/ROOT)" && python3 scripts/tl.py <args>
FID="${TL_SKILL_FILEID:-1H5kAt3SRVP7_xmLMIzcqyFtFc4VSDH0P}"
CONFIG_FILEID="${TL_CONFIG_FILEID:-1dEOBJ8PRmKoLgziEF5xuKjRhHLNhUUYq}"   # config v2 (apps script + token) nay PUBLIC ở Package → curl được
DIR="${TL_DIR:-$HOME/.tl_fetch}"; ZIP="$DIR/skill.zip"; OUT="$DIR/live"
CFG="${TL_CONFIG:-$HOME/.tra_luat_config.json}"
PY=python3; command -v python3 >/dev/null 2>&1 || PY=python
# v1.33.30 (MERGE bundle-29): --refresh / TL_FETCH_REFRESH=1 = ép xoá CẢ zip + live rồi tải/giải nén lại
# (escape hatch khi Drive re-up CÙNG VERSION khác nội dung — version-compare bên dưới không bắt được ca đó).
MODE=run; REFRESH="${TL_FETCH_REFRESH:-0}"
[ "$1" = "--refresh" ] && { REFRESH=1; shift; }
[ "$1" = "--setup" ] && { MODE=setup; shift; }
[ "$1" = "--refresh" ] && { REFRESH=1; shift; }
STEP=""; [ "$1" = "--setup-step" ] && { MODE=step; STEP="$2"; shift 2; }
[ "$1" = "--refresh" ] && { REFRESH=1; shift; }
DO_NLM=0; [ "$1" = "--nlm" ] && { DO_NLM=1; shift; }
if [ "$REFRESH" = 1 ]; then
  rm -f "$ZIP"; rm -rf "$OUT"
  echo "[tl_fetch] --refresh: xoa cache zip/live cu -> tai + giai nen lai ban sach" >&2
fi
mkdir -p "$DIR" 2>/dev/null || { echo "[tl_fetch] không tạo được $DIR" >&2; exit 2; }

# 1) TẢI ZIP — (a) curl Drive public TRƯỚC (nhanh, không token); (b) webapp GAS (token); (c) MCP-placed.
# v1.33.29 — FOOTGUN re-bootstrap (log verify v1.33.28 suýt kết luận sai 'ops-plan thiếu'): $ZIP cũ còn đó
# → bước tải BỎ QUA → --setup chạy mãi bản CŨ dù Drive đã có bản mới. --setup / --setup-step core = ý định
# "lấy bản MỚI NHẤT" → xoá zip cũ ép tải lại (zip ~1MB, curl nhanh; các step gws/boot/nlm giữ zip để khỏi tốn).
if [ "$MODE" = setup ]; then rm -f "$ZIP"; fi
if [ "$MODE" = step ] && [ "$STEP" = core ]; then rm -f "$ZIP"; fi
if [ ! -s "$ZIP" ]; then
  U="https://drive.usercontent.google.com/download?id=$FID&export=download&confirm=t"
  curl -fsSL "$U" -o "$ZIP" 2>/dev/null || wget -qO "$ZIP" "$U" 2>/dev/null || true
  [ -s "$ZIP" ] && echo "[tl_fetch] zip skill: curl Drive (public)" >&2
fi
if [ ! -s "$ZIP" ]; then
  "$PY" - "$FID" "$ZIP" "$CFG" <<'PYEOF' 2>/dev/null || true
import sys, os, json, base64, urllib.request, urllib.parse
fid, out, cfg = sys.argv[1:4]
w = os.environ.get("TL_WEBAPP"); t = os.environ.get("TL_TOKEN")
if not (w and t):
    for p in [cfg, os.path.expanduser("~/.tra_luat_config.json"), "/tmp/tra_luat_config.json"]:
        if p and os.path.exists(p):
            c = json.load(open(p, encoding="utf-8"))
            w = w or c.get("webappUrl") or c.get("TL_WEBAPP"); t = t or c.get("token") or c.get("TL_TOKEN")
            if w and t:
                break
if not (w and t):
    sys.exit(2)
u = w + ("&" if "?" in w else "?") + urllib.parse.urlencode({"action": "download", "token": t, "fileId": fid})
r = json.load(urllib.request.urlopen(u, timeout=180))
if not r.get("b64"):
    sys.exit(3)
open(out, "wb").write(base64.b64decode(r["b64"]))
PYEOF
  [ -s "$ZIP" ] && echo "[tl_fetch] zip skill: webapp GAS" >&2
fi
[ -s "$ZIP" ] || { echo "[tl_fetch] CHƯA tải được zip. Agent: Drive MCP download_file_content fileId=$FID → ghi $ZIP (path MÌNH sở hữu, KHÔNG /tmp). Cần allowlist drive.usercontent.google.com HOẶC script.google.com." >&2; exit 2; }

# 2) GIẢI NÉN (bỏ qua nếu đã có tl.py từ lần trước → re-run nhanh)
# v1.33.29 — FOOTGUN tầng 2 (cùng log): $OUT/live còn tl.py bản CŨ → bước giải nén bị BỎ QUA và ROOT bị ghi
# đè về bản CŨ dù $ZIP vừa tải là bản MỚI. So VERSION trong zip vs bản đã giải nén; LỆCH → re-extract.
ZV=$(unzip -p "$ZIP" '*/VERSION' 2>/dev/null | head -1 | tr -d '\r\n ')
OV=$(cat "$OUT"/*/VERSION 2>/dev/null | head -1 | tr -d '\r\n ')
if [ -n "$ZV" ] && [ -n "$OV" ] && [ "$ZV" != "$OV" ]; then
  echo "[tl_fetch] VERSION zip=$ZV != ban-da-giai-nen=$OV -> re-extract ban moi." >&2
  rm -rf "$OUT"
fi
TL=$(find "$OUT" -path '*/scripts/tl.py' 2>/dev/null | head -1)
if [ -z "$TL" ] || [ ! -s "$TL" ]; then
  rm -rf "$OUT"; mkdir -p "$OUT"
  unzip -oq "$ZIP" -d "$OUT" 2>/dev/null || { echo "[tl_fetch] unzip LỖI (zip hỏng) → xoá $ZIP tải lại." >&2; rm -f "$ZIP"; exit 3; }
  # v1.33.56 (review tl_core/F4): zip dùng mtime 1980 → giải nén ĐÈ bản cũ làm source mtime <= pyc cũ →
  # Python dùng __pycache__ STALE im lặng (chạy code phiên trước). Dọn pycache sau mỗi lần unzip.
  find "$OUT" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
  TL=$(find "$OUT" -path '*/scripts/tl.py' 2>/dev/null | head -1)
  [ -n "$TL" ] || { echo "[tl_fetch] không thấy scripts/tl.py trong zip." >&2; exit 3; }
fi
ROOT=$(dirname "$(dirname "$TL")"); echo "$ROOT" > "$DIR/ROOT"
echo "[tl_fetch] ROOT=$ROOT (VERSION $(cat "$ROOT/VERSION" 2>/dev/null | tr -d '\r\n '))" >&2

# 3b) v1.32.2 — TÁCH BƯỚC setup (Cowork 45s/lệnh: --setup trọn gói từng bị kill giữa chừng).
if [ "$MODE" = step ]; then
  export PATH="$HOME/.local/bin:$PATH"
  case "$STEP" in
    core)
      if [ ! -s "$CFG" ]; then
        CU="https://drive.usercontent.google.com/download?id=$CONFIG_FILEID&export=download&confirm=t"
        curl -fsSL "$CU" -o "$CFG.tmp" 2>/dev/null || wget -qO "$CFG.tmp" "$CU" 2>/dev/null || true
        if [ -s "$CFG.tmp" ] && ! head -c 256 "$CFG.tmp" | grep -qi '<!doctype html\|<html\|accounts.google.com'; then
          mv "$CFG.tmp" "$CFG"; echo "[tl_fetch] config: curl public ✓" >&2
        else rm -f "$CFG.tmp"; echo "[tl_fetch] THIẾU config (curl fail) — xem hướng dẫn --setup." >&2; exit 10; fi
      fi
      "$PY" "$TL" init-config --file "$CFG" 2>/dev/null || true
      "$PY" "$TL" ping || exit 1     # ping đã tự retry cold-start ×3 (v1.32.2)
      command -v uv >/dev/null 2>&1 || [ -x "$HOME/.local/bin/uv" ] || \
        "$PY" -m pip install --user --upgrade uv >/dev/null 2>&1 || true
      echo "[tl_fetch] ✓ STEP core xong → tiếp: --setup-step gws" >&2 ;;
    gws)
      GWSTGZ=$(find "$OUT" -path '*assets*' -name 'gws.tgz' 2>/dev/null | head -1)
      if [ -n "$GWSTGZ" ]; then "$PY" "$TL" gws-bootstrap-cowork --local-tgz "$GWSTGZ"
      else "$PY" "$TL" gws-bootstrap-cowork; fi
      echo "[tl_fetch] ✓ STEP gws xong → tiếp: --setup-step boot" >&2 ;;
    boot)
      "$PY" "$TL" boot || exit 1
      echo "[tl_fetch] ✓ STEP boot xong → (tùy chọn) --setup-step nlm" >&2 ;;
    nlm)
      "$PY" "$TL" nlm-install --resume; RC=$?
      if [ "$RC" = 3 ]; then echo "[tl_fetch] PARTIAL — chạy LẠI: --setup-step nlm (rc=3 = còn bước, KHÔNG lỗi)." >&2; exit 3; fi
      [ "$RC" = 0 ] || exit "$RC"
      "$PY" "$TL" nlm-auth-load 2>/dev/null && echo "[tl_fetch] ✓ nlm auth headless." >&2 || \
        echo "[tl_fetch] nlm CHƯA auth headless → 'nlm login' thủ công / nlm-MCP." >&2
      echo "[tl_fetch] ✓ STEP nlm xong — SETUP đủ." >&2 ;;
    *) echo "[tl_fetch] --setup-step cần core|gws|boot|nlm" >&2; exit 2 ;;
  esac
  exit 0
fi

# 3) BOOTSTRAP đủ (--setup) hoặc chạy 1 lệnh
if [ "$MODE" = setup ]; then
  # CONFIG (apps script + token) nay PUBLIC ở Package → curl drive.usercontent TRƯỚC (LOAD CONFIG ĐẦU TIÊN,
  # KHÔNG cần Drive MCP). Nhận diện trang login → file CHƯA public → mới fallback Drive MCP.
  if [ ! -s "$CFG" ]; then
    CU="https://drive.usercontent.google.com/download?id=$CONFIG_FILEID&export=download&confirm=t"
    curl -fsSL "$CU" -o "$CFG.tmp" 2>/dev/null || wget -qO "$CFG.tmp" "$CU" 2>/dev/null || true
    if [ -s "$CFG.tmp" ] && ! head -c 256 "$CFG.tmp" | grep -qi '<!doctype html\|<html\|accounts.google.com'; then
      mv "$CFG.tmp" "$CFG"; echo "[tl_fetch] config: curl Drive/Package (public) ✓" >&2
    else
      rm -f "$CFG.tmp"
    fi
  fi
  if [ ! -s "$CFG" ]; then
    echo "[tl_fetch] THIẾU $CFG — curl config public THẤT BẠI (file chưa 'anyone-with-link'? curl trả trang login)." >&2
    echo "  → CHẠY 1 LẦN script set-public (set-package-public.cmd) để bật public; HOẶC" >&2
    echo "    Agent: Drive MCP download_file_content fileId=$CONFIG_FILEID → base64 decode → ghi $CFG → chạy lại 'sh scripts/tl_fetch.sh --setup'." >&2
    exit 10
  fi
  echo "[tl_fetch] === SETUP: init-config → ping → uv → gws → boot$([ $DO_NLM = 1 ] && echo ' → nlm') ===" >&2
  "$PY" "$TL" init-config --file "$CFG" 2>/dev/null || true
  "$PY" "$TL" ping || { echo "[tl_fetch] ping FAIL — kiểm webapp/token." >&2; exit 1; }
  # uv: Cowork CHƯA có sẵn → cài TRƯỚC (astral CDN bị chặn → pip từ PyPI MỞ). Dùng cho nlm (Python 3.11) + tăng tốc.
  if ! command -v uv >/dev/null 2>&1 && [ ! -x "$HOME/.local/bin/uv" ]; then
    echo "[tl_fetch] cài uv (pip --user, PyPI)…" >&2
    "$PY" -m pip install --user --upgrade uv >/dev/null 2>&1 || pip install --user --upgrade uv >/dev/null 2>&1 || \
      echo "[tl_fetch] ⚠ cài uv lỗi (sẽ fallback Drive-python cho nlm)." >&2
  fi
  export PATH="$HOME/.local/bin:$PATH"
  command -v uv >/dev/null 2>&1 && echo "[tl_fetch] uv: $(uv --version 2>/dev/null)" >&2
  # gws: nếu BUNDLE có sẵn assets/gws.tgz → cài từ đó (khỏi tải Drive); không thì gws-bootstrap tự tải (public-curl trước).
  GWSTGZ=$(find "$OUT" -path '*assets*' -name 'gws.tgz' 2>/dev/null | head -1)
  if [ -n "$GWSTGZ" ]; then
    "$PY" "$TL" gws-bootstrap-cowork --local-tgz "$GWSTGZ" || echo "[tl_fetch] gws-bootstrap (local-tgz) lỗi (fallback GAS)." >&2
  else
    "$PY" "$TL" gws-bootstrap-cowork || echo "[tl_fetch] gws-bootstrap lỗi (fallback GAS, chậm hơn)." >&2
  fi
  "$PY" "$TL" boot || exit 1
  # nlm SAU gws. `--uv`: egress mở → uv tự lo Python 3.11 (KHÔNG tải 31MB Drive); fallback Drive bên trong nếu uv lỗi.
  if [ "$DO_NLM" = 1 ]; then
    "$PY" "$TL" nlm-install --uv || echo "[tl_fetch] nlm-install lỗi (xem log)." >&2
    # auth HEADLESS: nạp nlm cookie mã-hoá-token từ Drive (nlm-auth-load) — KHÔNG cần `nlm login`/master key
    if "$PY" "$TL" nlm-auth-load 2>/dev/null; then
      echo "[tl_fetch] ✓ nlm auth headless (nlm_cred Drive)." >&2
    else
      echo "[tl_fetch] nlm CHƯA auth headless (chưa stage NLM_CRED_FILEID) → 'nlm login' thủ công, hoặc nlm-MCP fallback." >&2
    fi
  fi
  echo "[tl_fetch] ✓ SETUP xong. Subsequent: cd $ROOT && $PY scripts/tl.py <args>" >&2
  exit 0
fi
echo "[tl_fetch] chạy $TL (bỏ qua mount). Subsequent: cd $ROOT && $PY scripts/tl.py <args>" >&2
exec "$PY" "$TL" "$@"
