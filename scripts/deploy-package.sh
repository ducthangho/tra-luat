#!/usr/bin/env bash
# deploy-package.sh — đóng gói + deploy skill tra-luat TỪ LINUX/Cowork.
#
# Bản Linux của `upload-skill-to-Package.ps1` (máy dev Windows, D:\Quốc hội\) — cùng quy trình
# §10 DEV_TOOLING_GUIDE + §6 bước 7-8 kế hoạch guard-va-boc-tl-core, chạy được trong container
# remote nơi KHÔNG có PowerShell và KHÔNG double-click được .cmd.
#
# MẶC ĐỊNH LÀ AN TOÀN: build + verify, KHÔNG đẩy Drive. Muốn đẩy thật phải nêu --push.
#
#   ./scripts/deploy-package.sh                  # gate + build + verify (KHÔNG đẩy)
#   ./scripts/deploy-package.sh --push           # ... rồi đẩy lên Drive/Package + verify sau đẩy
#   ./scripts/deploy-package.sh --no-test        # bỏ gate (chỉ khi VỪA chạy gate riêng)
#   ./scripts/deploy-package.sh --out /tmp/x.zip # chỉ định đường dẫn zip
#   ./scripts/deploy-package.sh --push --force-older   # ghi đè dù Drive đang bản mới hơn/cùng số
#
# rc: 0 = xong · 1 = gate đỏ · 2 = build/verify hỏng · 3 = đẩy hỏng (gồm CHẶN THỤT LÙI)
set -uo pipefail

# Xác định GỐC REPO và FAIL RÕ nếu không tìm được. Mặc định script ở <repo>/scripts nên gốc = lên
# HAI cấp; nhưng copy script ra chỗ khác thì "lên hai cấp" trỏ đi đâu đó và bước 0 chết với thông
# báo vô nghĩa kiểu "không thấy /VERSION" — người đọc không suy ra được nguyên nhân là SAI CHỖ ĐẶT.
# (Đường ps1 đã sập thật một lượt: script ở D:\Quốc hội\ ⇒ đòi D:\VERSION.) Kiểm dấu hiệu repo.
_is_repo() { [ -n "${1:-}" ] && [ -f "$1/VERSION" ] && [ -f "$1/scripts/tl.py" ]; }
_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT=""
for _c in "${TL_REPO:-}" "$(dirname "$_HERE")" "$_HERE" "$PWD"; do
  if _is_repo "$_c"; then ROOT="$(cd "$_c" && pwd)"; break; fi
done
if [ -z "$ROOT" ]; then
  printf '  \033[31m[FAIL]\033[0m Không tìm được gốc repo tra-luat (cần có VERSION + scripts/tl.py).\n' >&2
  printf '         đã thử: TL_REPO=%s · lên-2-cấp=%s · thư-mục-script=%s · cwd=%s\n' \
         "${TL_REPO:-<chưa đặt>}" "$(dirname "$_HERE")" "$_HERE" "$PWD" >&2
  printf '         Chữa: chạy bản TRONG repo (scripts/deploy-package.sh), hoặc đặt TL_REPO=/duong/dan/repo.\n' >&2
  printf '         Đừng để HAI bản script song song — chúng sẽ trôi lệch nhau.\n' >&2
  exit 2
fi
cd "$ROOT" || exit 2
PY="${TL_PYTHON:-python3}"
TL="$PY scripts/tl.py"
STATE="scripts/.tl_state/deploy"
mkdir -p "$STATE"

DO_PUSH=0; DO_TEST=1; OUT=""; FORCE_OLDER=0
while [ $# -gt 0 ]; do
  case "$1" in
    --push)         DO_PUSH=1 ;;
    --no-test)      DO_TEST=0 ;;
    --force-older)  FORCE_OLDER=1 ;;
    --out)     OUT="${2:-}"; shift ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "✗ cờ lạ: $1 (xem --help)" >&2; exit 2 ;;
  esac
  shift
done

say()  { printf '\n\033[1m== %s ==\033[0m\n' "$*"; }
ok()   { printf '  \033[32m[OK]\033[0m   %s\n' "$*"; }
bad()  { printf '  \033[31m[FAIL]\033[0m %s\n' "$*"; }
warn() { printf '  \033[33m[WARN]\033[0m %s\n' "$*"; }

# ─────────────────────────── 0. VERSION phải khớp 3 chỗ ───────────────────────────
say "0. VERSION khớp 3 chỗ"
VER="$(tr -d ' \r\n' < VERSION)"
V_TL="$(grep -m1 '^VERSION = ' scripts/tl.py | sed 's/.*"\(.*\)".*/\1/')"
V_SK="$(grep -m1 'LÕI VẬN HÀNH' SKILL.md | sed 's/.*(v\([0-9.]*\) —.*/\1/')"
printf '  VERSION=%s · tl.py=%s · SKILL.md=%s\n' "$VER" "$V_TL" "$V_SK"
if [ "$VER" != "$V_TL" ] || [ "$VER" != "$V_SK" ]; then
  bad "3 chỗ VERSION LỆCH — sửa cho khớp rồi chạy lại (selftest có guard skill_md_version_matches_VERSION)."
  exit 1
fi
ok "khớp v$VER"

# ── core.abbrev=7 — điều kiện TẤT ĐỊNH của gate, không phải tuỳ chọn ──
# `doc-claims-check` suy tập độ-dài-SHA-ứng-viên từ `git rev-parse --short HEAD`. Git trả độ dài
# TỐI THIỂU-DUY-NHẤT, trôi theo cả số commit lẫn commit đang ở HEAD (clone shallow 79 commit ⇒ 7;
# sau `fetch --unshallow` 304 commit ⇒ 8). Đã ĐO trên cây này:
#   abbrev=7 → golden ✓ · docclaims ✓ · determinism ✓ · selftest 1391/1391
#   abbrev=8 → golden ✗ (case doc_claims_check_fixture) · determinism ✗ · selftest 1390/1391
#            · docclaims 18 cờ SHA_NOT_A_COMMIT toàn FALSE POSITIVE (tiền tố UUID: notebook id
#              `59e8d0de`, source id…) vì ngưỡng 8 coi mọi chuỗi 8 hex là SHA.
# CI ghim bằng `git config --global core.abbrev 7`. Ở đây ghim REPO-LOCAL: hẹp hơn (không đụng
# global của người dùng) mà vẫn đúng cơ chế.
# ⚠ KHÔNG dùng env `GIT_CONFIG_*` để ghim: env thắng cả config của repo CON, nên nó đè luôn repo
# tạm mà `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` tự dựng để đo chênh 7-vs-8 ⇒ test đó ĐỎ
# (đã sập một lượt: 1390/1391). Config repo-local không có tật này — repo tạm có config riêng.
# .git/config KHÔNG được commit ⇒ mỗi clone mới phải đặt lại, vì vậy script tự đặt.
AB="$(git config --local core.abbrev 2>/dev/null || true)"
if [ "$AB" != "7" ]; then
  git config --local core.abbrev 7
  warn "đã đặt core.abbrev=7 cho repo này (trước đó: '${AB:-<chưa đặt, git tự suy>}') — gate cần ngưỡng cố định, xem chú thích trong script"
else
  ok "core.abbrev=7 (khớp CI)"
fi
if [ -f .git/shallow ]; then
  warn "repo đang SHALLOW — doc-claims-check sẽ đỏ vì SHA cũ không resolve được; chữa: git fetch --unshallow"
fi

# ─────────────────────────── 1. Gate offline ───────────────────────────
# doc-claims-check có HAI nguồn cờ giả, đã xử lý cả hai:
#  (1) abbrev trôi — chặn tận gốc bằng core.abbrev=7 ở bước 0.
#  (2) clone SHALLOW — SHA cũ trong changelog_archive không resolve được ⇒ SHA_NOT_A_COMMIT là
#      KHUYẾT MÔI TRƯỜNG, không phải trích dẫn sai. Chữa dứt điểm: `git fetch --unshallow`
#      (đã nghiệm: 79→304 commit thì 2 cờ đó về 0). Escape hatch dưới đây chỉ hạ WARN khi TOÀN BỘ
#      cờ đều là SHA_NOT_A_COMMIT *và* repo thật sự shallow; cờ loại khác ⇒ ĐỎ như thường.
if [ "$DO_TEST" = 1 ]; then
  say "1. Gate offline 8 bước"
  declare -A RC
  g() { local n="$1"; shift; "$@" > "$STATE/${n}.out" 2>&1; RC[$n]=$?; }
  g selftest    $PY scripts/tl.py --selftest
  g gen_inst    $PY scripts/gen_instructions.py --selftest
  g workflow    $PY scripts/tl.py workflow-audit --strict --json
  g golden      $PY scripts/tl.py golden-test --json            # KHÔNG BAO GIỜ --write ở đây (R6)
  g docclaims   $PY scripts/tl.py doc-claims-check --strict --json
  g determinism $PY scripts/tl.py determinism-audit --strict --json
  g relcheck    $PY scripts/tl.py release-check --full --json
  g relverify   $PY scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json

  FAIL=0
  for n in selftest gen_inst workflow golden docclaims determinism relcheck relverify; do
    case "$n" in
      selftest|gen_inst) extra="$(tail -1 "$STATE/${n}.out")" ;;
      *) extra="$(grep -o '"ok": *\(true\|false\)' "$STATE/${n}.out" | head -1)" ;;
    esac
    pass=0
    if [ "${RC[$n]}" -eq 0 ]; then
      case "$n" in
        selftest|gen_inst) echo "$extra" | grep -qE '([0-9]+)/\1' && pass=1 ;;
        *) echo "$extra" | grep -q '"ok": *true' && pass=1 ;;
      esac
    fi
    if [ "$pass" = 1 ]; then ok "$(printf '%-12s rc=%s %s' "$n" "${RC[$n]}" "$extra")"; continue; fi

    if [ "$n" = docclaims ] && [ -f .git/shallow ] && \
       $PY -c "
import json,sys
d=json.load(open('$STATE/docclaims.out'))
f=d.get('flags') or []
sys.exit(0 if f and all(x.get('reason')=='SHA_NOT_A_COMMIT' for x in f) else 1)" 2>/dev/null; then
      warn "$(printf '%-12s rc=%s — %s cờ, TẤT CẢ là SHA_NOT_A_COMMIT trên clone SHALLOW ⇒ khuyết môi trường, KHÔNG chặn' \
              "$n" "${RC[$n]}" "$($PY -c "import json;print(len(json.load(open('$STATE/docclaims.out'))['flags']))")")"
      warn "       muốn chắc: git fetch --unshallow rồi chạy lại — cờ phải về 0"
      continue
    fi
    bad "$(printf '%-12s rc=%s %s  → soi %s' "$n" "${RC[$n]}" "$extra" "$STATE/${n}.out")"
    # nguyên nhân số 1 của relverify đỏ: vừa thêm/sửa/xoá tệp ⇒ cây lệch RELEASE_MANIFEST.
    # Nói thẳng cách chữa, đừng bắt người đọc đi dò 194 dòng hash.
    if [ "$n" = relverify ] && grep -q '"failed"' "$STATE/relverify.out" 2>/dev/null; then
      warn "       cây đã đổi so với manifest — chữa: $PY scripts/tl.py release-manifest --out RELEASE_MANIFEST.json"
      $PY - "$STATE/relverify.out" <<'PY' 2>/dev/null
import json,sys
d=json.load(open(sys.argv[1]))
for f in (d.get('failed') or [])[:8]:
    print(f"         · {f.get('path')}: {f.get('expected_size')}→{f.get('actual_size')} byte")
PY
    fi
    FAIL=1
  done
  [ "$FAIL" = 0 ] || { bad "GATE ĐỎ — DỪNG, không build/không đẩy (golden diff = BUG của thay đổi, R6)"; exit 1; }
  ok "gate xanh"
else
  warn "BỎ QUA gate (--no-test) — chỉ hợp lệ khi vừa chạy gate riêng ở commit NÀY"
fi

# ─────────────────────────── 2. Build zip ×2, đòi same-SHA ───────────────────────────
# release-bundle TỪ CHỐI ghi vào trong skill root (OUT_INSIDE_SKILL_ROOT → tự chuyển ra ngoài,
# nếu không zip sẽ tự nuốt chính nó). Vì vậy mặc định xuất ra THƯ MỤC CHA, và luôn đọc đường
# dẫn THẬT từ khoá "out" của JSON thay vì tin vào tham số mình truyền vào.
say "2. Build bundle ×2 (đòi tất định same-SHA)"
BUILD_DIR="$(dirname "$ROOT")"
ZIP="${OUT:-$BUILD_DIR/tra-luat-skill-v${VER}-gws3env.zip}"
ZIP2="$BUILD_DIR/.tl-reproducibility-probe.zip"
rm -f "$ZIP" "$ZIP2"

jget() { $PY -c "import json,sys;print(json.load(open(sys.argv[1])).get(sys.argv[2]) or '')" "$1" "$2" 2>/dev/null; }

$TL release-bundle --out "$ZIP"  --json > "$STATE/bundle1.out" 2>&1 || { bad "release-bundle lỗi — soi $STATE/bundle1.out"; exit 2; }
$TL release-bundle --out "$ZIP2" --json > "$STATE/bundle2.out" 2>&1 || { bad "release-bundle (lần 2) lỗi"; exit 2; }
ZIP="$(jget  "$STATE/bundle1.out" out)"   # đường dẫn THẬT (có thể đã bị chuyển)
ZIP2="$(jget "$STATE/bundle2.out" out)"
for z in "$ZIP" "$ZIP2"; do
  [ -n "$z" ] && [ -s "$z" ] || { bad "release-bundle báo ok nhưng KHÔNG có zip thật: '${z:-<rỗng>}' — soi $STATE/bundle1.out"; exit 2; }
done
if [ "$(jget "$STATE/bundle1.out" out)" != "${OUT:-$BUILD_DIR/tra-luat-skill-v${VER}-gws3env.zip}" ]; then
  warn "release-bundle CHUYỂN chỗ xuất → $ZIP (không ghi được trong skill root)"
fi
S1="$(sha256sum "$ZIP"  | cut -d' ' -f1)"
S2="$(sha256sum "$ZIP2" | cut -d' ' -f1)"
[ -n "$S1" ] && [ -n "$S2" ] || { bad "không tính được sha256 của bundle"; exit 2; }
if [ "$S1" != "$S2" ]; then
  bad "BUILD KHÔNG TẤT ĐỊNH: $S1 ≠ $S2 — có thứ phi-tất-định lọt vào gói, DỪNG."
  exit 2
fi
rm -f "$ZIP2"
ok "same-SHA ✓ sha256=${S1:0:16}… · $(stat -c%s "$ZIP") byte · $ZIP"

# ─────────────────────────── 3. Verify nội dung zip ───────────────────────────
say "3. Verify nội dung gói"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
unzip -q "$ZIP" -d "$TMP" || { bad "unzip hỏng"; exit 2; }
TOP="$(cd "$TMP" && ls -1 | head -1)"
PKG="$TMP/$TOP"

Z_VER="$(tr -d ' \r\n' < "$PKG/VERSION" 2>/dev/null)"
[ "$Z_VER" = "$VER" ] && ok "VERSION trong gói = $Z_VER" || { bad "VERSION trong gói ($Z_VER) ≠ repo ($VER)"; exit 2; }

# 3b. thứ TUYỆT ĐỐI không được vào gói (dev-side + secrets)
LEAK=0
for p in ".git" ".claude" ".githooks" ".github" "CLAUDE.md" \
         "tra_luat_config.json" "tra_luat_config.v2.json" "claude-code-best-practice" \
         "references/changelog_archive"; do
  if [ -e "$PKG/$p" ]; then bad "RÒ: gói chứa '$p'"; LEAK=1; fi
done
if find "$PKG" -name '*.enc' -o -name '*cookie*' -o -name '*token*' -o -name 'credentials*' | grep -q .; then
  bad "RÒ: gói chứa tệp secrets (*.enc/cookie/token/credentials):"
  find "$PKG" -name '*.enc' -o -name '*cookie*' -o -name '*token*' -o -name 'credentials*' | sed 's/^/        /'
  LEAK=1
fi
[ "$LEAK" = 0 ] && ok "không có tệp dev-side/secrets trong gói"

# 3c. quét token/khoá lọt vào NỘI DUNG tệp văn bản
# Bảng mẫu bí mật nằm ở scripts/pkg_secret_scan.py — DÙNG CHUNG với deploy-package.ps1. Không inline
# lại ở đây: hai bảng mẫu SẼ trôi lệch, thêm mẫu bên này quên bên kia là đẩy lọt secret.
SCAN="$($PY scripts/pkg_secret_scan.py "$PKG")"; SCAN_RC=$?
if [ "$SCAN_RC" -ne 0 ]; then
  bad "QUÉT TOKEN BẮT ĐƯỢC BÍ MẬT trong gói — DỪNG, KHÔNG đẩy:"; echo "$SCAN" | sed 's/^/        /'
  LEAK=1
else
  ok "quét token: sạch"
fi
[ "$LEAK" = 0 ] || { bad "gói KHÔNG đạt — dừng trước khi đẩy"; exit 2; }

# 3d. release-verify CHẠY TRONG GÓI (manifest tự mô tả)
if [ -f "$PKG/RELEASE_MANIFEST.json" ]; then
  ( cd "$PKG" && $PY scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json ) \
      > "$STATE/relverify_inzip.out" 2>&1
  if grep -q '"ok": *true' "$STATE/relverify_inzip.out"; then ok "release-verify TRONG gói: ok"
  else bad "release-verify TRONG gói ĐỎ — soi $STATE/relverify_inzip.out"; exit 2; fi
else
  warn "gói không có RELEASE_MANIFEST.json — bỏ qua verify trong gói"
fi

# đếm SAU khi release-verify đã chạy ⇒ phải loại __pycache__ do chính lần chạy đó sinh ra,
# nếu không số đếm phồng lên (224 vs 195 thật) và đọc như gói có rác.
FILES="$(find "$PKG" -type f -not -path '*/__pycache__/*' | wc -l)"
ok "gói: $FILES tệp · top-level '$TOP'"

# ─────────────────────────── 4. Đẩy Drive ───────────────────────────
if [ "$DO_PUSH" = 0 ]; then
  say "XONG (build-only)"
  echo "  Gói sẵn sàng: $ZIP"
  echo "  Đẩy thật:     ./scripts/deploy-package.sh --push"
  exit 0
fi

say "4. Đẩy lên Drive/Package"
BEFORE="$(gws drive files get --params '{"fileId":"1H5kAt3SRVP7_xmLMIzcqyFtFc4VSDH0P","fields":"name,size,modifiedTime"}' 2>/dev/null)"
D_NAME="$(echo "$BEFORE" | tr -d '\n ' | sed 's/.*"name":"\([^"]*\)".*/\1/')"
echo "  Package HIỆN TẠI: ${D_NAME:-<không đọc được>}"

# ── CHỐT CHỐNG THỤT LÙI (CLAUDE.md §Quy ước deploy mục 3) ──
# Package là MỘT fileId, `drive-push` GHI ĐÈ và giữ fileId, KHÔNG có LockService như registry ⇒
# last-writer-wins IM LẶNG. Sự cố 30-07-2026: hai phiên đẩy cùng fileId trong ~20 phút. Lần đó vô
# hại vì phiên sau build từ master mới nhất, nhưng ngược chiều thì Package THỤT LÙI âm thầm và mọi
# phiên Cowork mới bootstrap bản cũ. Không có chốt này thì mục 1-2 của quy ước chỉ là lời hứa.
# Bằng NHAU cũng chặn: cùng số mà khác cây là đúng cái sai "một số version = một cây" cấm.
D_VER="$(printf '%s' "$D_NAME" | sed -n 's/.*-v\([0-9][0-9.]*\)-.*/\1/p')"
if [ -z "$D_VER" ]; then
  warn "không rút được version từ tên Package ('${D_NAME:-rỗng}') — KHÔNG kiểm được thụt lùi, tự chịu trách nhiệm"
elif [ "$(printf '%s\n%s\n' "$VER" "$D_VER" | sort -V | tail -1)" = "$D_VER" ]; then
  if [ "$FORCE_OLDER" = 1 ]; then
    warn "Drive đang v$D_VER $([ "$D_VER" = "$VER" ] && echo '=' || echo '>') v$VER sắp đẩy — GHI ĐÈ vì có --force-older"
  else
    bad "CHẶN THỤT LÙI: Drive đang v$D_VER, bản sắp đẩy v$VER — phiên khác vừa đẩy (hoặc cây này tụt sau)."
    echo "        Chữa: git fetch origin master && (merge/rebase) → chạy lại gate → deploy lại." >&2
    echo "        Cố ý ghi đè bản mới hơn/cùng số: thêm --force-older (đọc CLAUDE.md §Quy ước deploy trước)." >&2
    exit 3
  fi
else
  ok "Drive đang v$D_VER < v$VER sắp đẩy — không thụt lùi"
fi

$TL drive-push "$ZIP" --rename-to-file || { bad "drive-push lỗi (cần `gws auth login` có quyền GHI Drive)"; exit 3; }
ok "đã đẩy"

# ─────────────────────────── 5. Verify SAU đẩy (byte-match) ───────────────────────────
say "5. Verify sau đẩy — tải về đối chiếu byte"
DL="$STATE/verify-download.zip"; rm -f "$DL"
gws drive files get --params '{"fileId":"1H5kAt3SRVP7_xmLMIzcqyFtFc4VSDH0P","alt":"media"}' --output "$DL" >/dev/null 2>&1
if [ ! -s "$DL" ]; then bad "không tải lại được Package để verify"; exit 3; fi
S3="$(sha256sum "$DL" | cut -d' ' -f1)"
if [ "$S3" = "$S1" ]; then
  ok "BYTE-MATCH ✓ sha256 Drive = local (${S1:0:16}…)"
else
  bad "LỆCH BYTE: local=${S1:0:16}… drive=${S3:0:16}… — đẩy KHÔNG toàn vẹn"; exit 3
fi
D_VER="$(unzip -p "$DL" '*/VERSION' 2>/dev/null | tr -d ' \r\n')"
[ "$D_VER" = "$VER" ] && ok "VERSION trên Drive = $D_VER" || { bad "VERSION trên Drive ($D_VER) ≠ $VER"; exit 3; }
rm -f "$DL"

say "DEPLOY XONG — Package = v$VER"
echo "  Phiên Cowork mới bootstrap từ zip này sẽ nhận v$VER."
