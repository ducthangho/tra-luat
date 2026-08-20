#!/usr/bin/env bash
# Cai `actionlint` DUNG BAN GHIM — MOT cho duy nhat, cho ca hai workflow.
#
# VI SAO CO TEP NAY. Truoc do phan "cai + doi chieu phien ban" duoc CHEP vao hai
# workflow, va cai duy nhat kiem no la mot phep so khop CHUOI trong `t35`. Cross-review
# codex tren `#200` do duoc: phep so khop ay chi kiem SU DONG HIEN cua vai token tren
# cung mot dong, nen mot dong hoan toan KHONG doi chieu gi van lam `t35` xanh. Do la lan
# thu ba cung mot hinh dang loi — kiem su CO MAT cua chuoi roi tuyen la da do HANH VI.
#
# Nen chua o TANG, khong siet them mau chuoi: hanh vi cai + doi chieu nam trong MOT
# script CHAY DUOC, va `t35` CHAY THAT script nay voi `actionlint` gia roi doi no TU CHOI.
# Kiem mot thu chay duoc thi khong the xanh rong bang cach viet lai chu.
#
# KHONG co nhanh thoat som "da co actionlint tren PATH thi thoi": co mat != dung ban.
#
# Bien moi truong:
#   AL_VER      (bat buoc) ban ghim exact, dang X.Y.Z
#   AL_DICH     thu muc cai (mac dinh: ${RUNNER_TEMP:-/tmp}/actionlint)
#   AL_BASE_URL goc tai ve (mac dinh: releases cua rhysd/actionlint) — cho phep guong
#   AL_GOI      duong dan mot GOI CO SAN; co thi DUNG NO, khong tai ve. Dung cho cai
#               offline/air-gapped, va cho `t35` dua vao mot goi GIA de do HANH VI that
#               ma khong can mang (nen `t35` chay duoc ca tren runner Windows)
#   AL_NEN      ten nen (mac dinh: $RUNNER_OS, roi den `uname`)
#
# Ma thoat — RIENG BIET de nguoi goi (va `t35`) khang dinh duoc LY DO tu choi:
#   2 thieu/sai `AL_VER`      5 giai nen hong hoac khong thay binary
#   3 nen khong duoc ho tro   6 binary khong chay duoc (`--version` rc != 0)
#   4 tai ve that bai         7 CAI XONG NHUNG SAI BAN (hoac khong phai actionlint)
set -euo pipefail

loi() { ma="$1"; shift; printf '%s\n' "cai_actionlint: $*" >&2; exit "$ma"; }

AL_VER="${AL_VER-}"
case "$AL_VER" in
  [0-9]*.[0-9]*.[0-9]*) : ;;
  *) loi 2 "thieu \`AL_VER\` dang X.Y.Z (duoc '${AL_VER}')" ;;
esac

AL_DICH="${AL_DICH:-${RUNNER_TEMP:-/tmp}/actionlint}"
AL_BASE_URL="${AL_BASE_URL:-https://github.com/rhysd/actionlint/releases/download}"
NEN="${AL_NEN:-${RUNNER_OS:-$(uname -s 2>/dev/null || echo unknown)}}"

case "$NEN" in
  Linux|linux|Linux*)      GOI="actionlint_${AL_VER}_linux_amd64.tar.gz" ;;
  macOS|Darwin|darwin)     GOI="actionlint_${AL_VER}_darwin_arm64.tar.gz" ;;
  Windows|Windows_NT|MINGW*|MSYS*|CYGWIN*) GOI="actionlint_${AL_VER}_windows_amd64.zip" ;;
  *) loi 3 "nen la '${NEN}', chua co goi cho nen nay" ;;
esac

mkdir -p "$AL_DICH"
if [ -n "${AL_GOI:-}" ]; then
  [ -f "$AL_GOI" ] || loi 4 "khong thay goi co san '$AL_GOI'"
  TEN_GOI="$AL_GOI"
else
  curl -fsSL --retry 2 -o "$AL_DICH/goi.${GOI##*.}" "${AL_BASE_URL}/v${AL_VER}/${GOI}" \
    || loi 4 "tai ve that bai: ${AL_BASE_URL}/v${AL_VER}/${GOI}"
  TEN_GOI="$AL_DICH/goi.${GOI##*.}"
fi

# Chon bo giai nen theo DUOI CUA GOI THAT, khong theo nen — goi co san co the la .tar.gz
# ngay tren Windows. `unzip` khong co san trong Git Bash, nen co duong lui sang `tar`.
case "$TEN_GOI" in
  *.zip)
    if command -v unzip >/dev/null 2>&1; then
      unzip -q -o "$TEN_GOI" -d "$AL_DICH" || loi 5 "giai nen zip that bai"
    else
      tar -xf "$TEN_GOI" -C "$AL_DICH" || loi 5 "giai nen zip bang tar that bai"
    fi ;;
  *) tar -xzf "$TEN_GOI" -C "$AL_DICH" || loi 5 "giai nen tar that bai" ;;
esac

BIN=""
for ung in "$AL_DICH/actionlint" "$AL_DICH/actionlint.exe"; do
  [ -f "$ung" ] && { BIN="$ung"; break; }
done
[ -n "$BIN" ] || loi 5 "giai nen xong ma khong thay \`actionlint\` trong '$AL_DICH'"
chmod +x "$BIN" 2>/dev/null || true

# DOI CHIEU BAN GHIM. Day la BANG CHUNG DUONG, khong phai `command -v`:
# bat binary VUA CAI tu khai phien ban, roi doi dong dau khop DUNG `AL_VER`.
# Mot binary gia tra rc=0 nhung in thu khac se roi vao ma 7, khong phai xanh rong.
RA="$("$BIN" --version 2>/dev/null)" || loi 6 "'$BIN' khong chay duoc (\`--version\` that bai)"
DONG1="$(printf '%s\n' "$RA" | head -1 | tr -d '\r')"
[ "$DONG1" = "$AL_VER" ] \
  || loi 7 "cai xong nhung KHONG khop ban ghim: doi '$AL_VER', binary khai '$DONG1'"

[ -n "${GITHUB_PATH:-}" ] && printf '%s\n' "$AL_DICH" >> "$GITHUB_PATH"
printf '%s\n' "$AL_DICH"
