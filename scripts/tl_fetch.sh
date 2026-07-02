#!/bin/sh
# tl_fetch.sh — chạy tl.py từ bản TẢI VỀ (mạng giao byte trung thực) thay vì mount Cowork hay cắt cụt (#51435/#53940).
# Zip skill PUBLIC → curl `drive.usercontent.google.com` (proxy allowlist cho domain này; NHANH NHẤT, off-context,
# KHÔNG cần token). GHI VÀO THƯ MỤC MÌNH SỞ HỮU ($HOME/.tl_fetch) — KHÔNG /tmp (sticky bit: file rác owner `nobody`
# chặn `curl -o` → exit 23, và file rỗng làm script tưởng "đã có").  Shell (sống sót cắt cụt) + nhỏ (dán-lại được).
#   sh scripts/tl_fetch.sh <args>        # tải zip 1 lần → chạy `tl.py <args>` từ bản sạch
#   sh scripts/tl_fetch.sh --setup [--nlm]   # BOOTSTRAP đủ: CONFIG(curl public)+GWS TRƯỚC → init-config → ping → gws(direct-media) → boot [→ nlm uv]
# Subsequent (nhanh hơn, khỏi qua script):  cd "$(cat ~/.tl_fetch/ROOT)" && python3 scripts/tl.py <args>
FID="${TL_SKILL_FILEID:-1H5kAt3SRVP7_xmLMIzcqyFtFc4VSDH0P}"
CONFIG_FILEID="${TL_CONFIG_FILEID:-1dEOBJ8PRmKoLgziEF5xuKjRhHLNhUUYq}"   # config v2 (apps script + token) nay PUBLIC ở Package → curl được
DIR="${TL_DIR:-$HOME/.tl_fetch}"; ZIP="$DIR/skill.zip"; OUT="$DIR/live"
CFG="${TL_CONFIG:-$HOME/.tra_luat_config.json}"
PY=python3; command -v python3 >/dev/null 2>&1 || PY=python
MODE=run; [ "$1" = "--setup" ] && { MODE=setup; shift; }
DO_NLM=0; [ "$1" = "--nlm" ] && { DO_NLM=1; shift; }
mkdir -p "$DIR" 2>/dev/null || { echo "[tl_fetch] không tạo được $DIR" >&2; exit 2; }

# 1) TẢI ZIP — (a) curl Drive public TRƯỚC (nhanh, không token); (b) webapp GAS (token); (c) MCP-placed.
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
TL=$(find "$OUT" -path '*/scripts/tl.py' 2>/dev/null | head -1)
if [ -z "$TL" ] || [ ! -s "$TL" ]; then
  rm -rf "$OUT"; mkdir -p "$OUT"
  unzip -oq "$ZIP" -d "$OUT" 2>/dev/null || { echo "[tl_fetch] unzip LỖI (zip hỏng) → xoá $ZIP tải lại." >&2; rm -f "$ZIP"; exit 3; }
  TL=$(find "$OUT" -path '*/scripts/tl.py' 2>/dev/null | head -1)
  [ -n "$TL" ] || { echo "[tl_fetch] không thấy scripts/tl.py trong zip." >&2; exit 3; }
fi
ROOT=$(dirname "$(dirname "$TL")"); echo "$ROOT" > "$DIR/ROOT"

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
