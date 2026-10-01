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
#   8 KHONG CO BAM de doi chieu goi   9 BAM GOI KHONG KHOP
#  12 khong tao duoc thu muc cai
set -euo pipefail

loi() { ma="$1"; shift; printf '%s\n' "cai_actionlint: $*" >&2; exit "$ma"; }

AL_VER="${AL_VER-}"
# DUNG REGEX DAY DU, khong dung glob cua `case`. Ban truoc viet
#   [0-9]*.[0-9]*.[0-9]*
# va no LOT: trong glob, `*` khop MOI ky tu (ke ca chu cai) chu khong phai "nhieu chu so",
# con `.` la ky tu THUONG chu khong phai metachar. Do duoc o cross-review #203:
#   AL_VER=1x.2y.3z  ->  rc=0, script CAI BINH THUONG
# tuc mot ban ghim khong phai so van qua cong. `[[ =~ ]]` la cua bash, va tep nay khai
# `#!/usr/bin/env bash` ngay dong dau nen dung duoc.
if [[ ! "$AL_VER" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  loi 2 "thieu \`AL_VER\` dang X.Y.Z (duoc '${AL_VER}')"
fi

AL_DICH="${AL_DICH:-${RUNNER_TEMP:-/tmp}/actionlint}"
AL_BASE_URL="${AL_BASE_URL:-https://github.com/rhysd/actionlint/releases/download}"
NEN="${AL_NEN:-${RUNNER_OS:-$(uname -s 2>/dev/null || echo unknown)}}"

case "$NEN" in
  Linux|linux|Linux*)      GOI="actionlint_${AL_VER}_linux_amd64.tar.gz" ;;
  macOS|Darwin|darwin)     GOI="actionlint_${AL_VER}_darwin_arm64.tar.gz" ;;
  Windows|Windows_NT|MINGW*|MSYS*|CYGWIN*) GOI="actionlint_${AL_VER}_windows_amd64.zip" ;;
  *) loi 3 "nen la '${NEN}', chua co goi cho nen nay" ;;
esac

# ─────────────────────── DOI CHIEU BAM GOI (cross-review #203, P2-3) ───────────────────────
# VI SAO. Truoc do goi tai tu mang duoc chay NGAY sau khi giai nen, va thu duy nhat "xac
# minh" no la `actionlint --version` — tuc BINARY TU KHAI. Mot binary bi thay the tu in
# `1.7.7` cung qua. Ma binary nay chay trong job co `contents: write` + `issues: write`.
#
# NOI THANG GIOI HAN, dung de ai doc rong hon thuc te: bam duoi day duoc TINH TU CHINH ban
# tai ve luc ghim, khong phai tu mot trust root doc lap (actionlint khong cong bo tep
# checksum ky). Nen no chan DRIFT va chan THAY THE VE SAU — dung muc bao dam cua
# `pip install X==1.2.3` co hash, KHONG hon. No khong chung minh ban goc sach tai thoi
# diem ghim.
bam_ghim() {
  case "$1" in
    actionlint_1.7.7_linux_amd64.tar.gz)  echo "023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757" ;;
    actionlint_1.7.7_darwin_arm64.tar.gz) echo "2693315b9093aeacb4ebd91a993fea54fc215057bf0da2659056b4bc033873db" ;;
    actionlint_1.7.7_windows_amd64.zip)   echo "7f12f1801bca3d480d67aaf7774f4c2a6359a3ca8eebe382c95c10c9704aa731" ;;
    *) echo "" ;;
  esac
}

# `sha256sum` (GNU/Git Bash) hoac `shasum -a 256` (macOS). Thieu CA HAI thi FAIL-CLOSE:
# mot cong tu tat khi thieu cong cu la cong khong ton tai dung luc no can nhat.
# DOC TU STDIN, dung truyen TEN TEP. Ly do da tra gia tren Windows (luot 32371632630):
# GNU coreutils THOAT dong ket qua khi TEN TEP chua dau cheo nguoc hoac xuong dong — no
# them mot `\` vao DAU DONG roi escape ten. Duong dan runner Windows la `D:\a\_temp/...`
# nen dau ra thanh:
#     \7f12f180...  D:\\a\\_temp/actionlint/goi.zip
# va `cut -d" " -f1` lay ve `\7f12f180...` — lech dung MOT KY TU so voi ban ghim. Cong bam
# bao KHONG KHOP tren mot goi HOAN TOAN DUNG.
# Tai lap duoc tren Linux: dau cheo nguoc la ky tu HOP LE trong ten tep POSIX (xem t38).
# Doc tu stdin thi khong co ten tep trong dau ra, nen khong con gi de thoat.
bam_cua() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum < "$1" | cut -d" " -f1
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 < "$1" | cut -d" " -f1
  else
    echo ""
  fi
}

MONG="${AL_SHA256:-$(bam_ghim "$GOI")}"
# FAIL SOM: khong co bam thi DUNG NGAY, dung tai ve roi moi phat hien. Tai mot thu ta
# khong doi chieu duoc rat de thanh "thoi cai dai" o lan sua sau.
[ -n "$MONG" ] || loi 8 "khong co bam de doi chieu goi '$GOI'. Ghim bam trong \`bam_ghim\` cho ban nay, hoac truyen \`AL_SHA256\`. KHONG co duong bo qua — day la ma se duoc CHAY."

mkdir -p "$AL_DICH" || loi 12 "khong tao duoc thu muc cai '$AL_DICH'"
if [ -n "${AL_GOI:-}" ]; then
  [ -f "$AL_GOI" ] || loi 4 "khong thay goi co san '$AL_GOI'"
  TEN_GOI="$AL_GOI"
else
  curl -fsSL --retry 2 -o "$AL_DICH/goi.${GOI##*.}" "${AL_BASE_URL}/v${AL_VER}/${GOI}" \
    || loi 4 "tai ve that bai: ${AL_BASE_URL}/v${AL_VER}/${GOI}"
  TEN_GOI="$AL_DICH/goi.${GOI##*.}"
fi

# Doi chieu bam TREN TEP DA CO (tai ve hoac `AL_GOI`). Luu y: khi dung `AL_GOI` ma khong
# truyen `AL_SHA256`, moc so van la BAM GHIM CUA GOI CHINH THUC — tuc ban cai offline cung
# phai la dung artefact ay. Do la CO Y, khong phai lo hong.
THUC="$(bam_cua "$TEN_GOI")"
[ -n "$THUC" ] || loi 8 "KHONG DO DUOC bam: thieu ca \`sha256sum\` lan \`shasum\`. Cap mot trong hai cho runner, dung bo qua buoc nay."
[ "$THUC" = "$MONG" ] || loi 9 "bam goi KHONG KHOP: mong '$MONG', thuc '$THUC' (goi '$TEN_GOI')"

# DUA GOI VE THU MUC DICH DUOI MOT TEN KHONG CO DAU HAI CHAM, roi giai nen tu TRONG
# thu muc ay bang TEN TRAN. Nghe thua mot buoc chep, nhung day la chot chong mot loi
# DA LAM DO WINDOWS THAT (luot 32368383473, job 96423003418):
#
#   tar (child): Cannot connect to C: resolve failed
#
# GNU tar doc doi so cua `-f` theo dang `HOST:PATH` khi co dau hai cham DUNG TRUOC dau
# gach cheo dau tien. Tren Windows duong dan mang ky tu o dia (`C:\...`) nen tar khong mo
# tep — no di PHAN GIAI TEN MAY `C`. Hau qua: tren Windows script LUON tra rc=5, tuc
# installer khong bao gio cai duoc, va `ci.yml` chan windows do.
#
# VI SAO KHONG dung `--force-local`: co cua GNU tar, KHONG co o bsdtar (tar.exe cua
# Windows 10+ va cua macOS) — vá bằng nó là đổi một lỗi nền này lấy một lỗi nền khác.
# VI SAO KHONG chi dung `basename`: ten tep cung co the chua dau hai cham
# (`AL_GOI=/duong/we:ird.tar.gz`), va luc ay basename van dinh dung luat tren.
# Ten dich duoi day do TA dat nen chac chan khong co dau hai cham — do la thu lam chot,
# khong phai phep loc chuoi tren dau vao.
# Chon ten cuc bo theo NOI DUNG ARCHIVE, KHONG theo suffix. Ban truoc mac dinh moi ten
# khong khop dung `*.zip` la tar.gz. Cross-review #203 luot 3 do duoc CUNG mot zip hop le:
# ten khong duoi -> rc=5, ten `.ZIP` -> rc=5, ten `.zip` -> rc=0. `AL_GOI` chi hua mot
# duong dan toi goi co san; no khong hua quy uoc ten hay cach viet hoa.
#
# Doc bon magic byte dau: ba chu ky ZIP chuan va chu ky gzip. `od` co tren GNU, BSD va
# Git Bash; thieu no thi fail-close rc=5, khong doan "khong zip thi chac la tar".
command -v od >/dev/null 2>&1 \
  || loi 5 "KHONG DO DUOC loai goi: thieu \`od\` de doc magic bytes"
if ! DAU_THO="$(LC_ALL=C od -An -N4 -tx1 "$TEN_GOI")"; then
  loi 5 "khong doc duoc magic bytes cua goi '$TEN_GOI'"
fi
DAU_GOI="${DAU_THO//[[:space:]]/}"
case "$DAU_GOI" in
  504b0304|504b0506|504b0708)
    LOAI_GOI="zip"
    GOI_CUC_BO="goi_giai_nen.zip"
    ;;
  1f8b*)
    LOAI_GOI="tar.gz"
    GOI_CUC_BO="goi_giai_nen.tar.gz"
    ;;
  *) loi 5 "khong nhan dien duoc loai goi tu magic bytes '$DAU_GOI'" ;;
esac
if [ "$TEN_GOI" != "$AL_DICH/$GOI_CUC_BO" ]; then
  cp "$TEN_GOI" "$AL_DICH/$GOI_CUC_BO" || loi 5 "khong chep duoc goi vao '$AL_DICH'"
fi

# Chon bo giai nen theo LOAI DA DO TU NOI DUNG, khong theo nen hay ten tep. `unzip`
# khong co san trong Git Bash, nen co duong lui sang `tar`.
case "$LOAI_GOI" in
  zip)
    if command -v unzip >/dev/null 2>&1; then
      ( cd "$AL_DICH" && unzip -q -o "$GOI_CUC_BO" ) || loi 5 "giai nen zip that bai"
    else
      ( cd "$AL_DICH" && tar -xf "$GOI_CUC_BO" ) || loi 5 "giai nen zip bang tar that bai"
    fi ;;
  tar.gz) ( cd "$AL_DICH" && tar -xzf "$GOI_CUC_BO" ) || loi 5 "giai nen tar that bai" ;;
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
# #675: khong `| head -1` duoi pipefail (SIGPIPE -> rc=141 tren dau ra dai; do: ops/do_sigpipe.sh).
DONG1="${RA%%$'\n'*}"; DONG1="${DONG1//$'\r'/}"
[ "$DONG1" = "$AL_VER" ] \
  || loi 7 "cai xong nhung KHONG khop ban ghim: doi '$AL_VER', binary khai '$DONG1'"

[ -n "${GITHUB_PATH:-}" ] && printf '%s\n' "$AL_DICH" >> "$GITHUB_PATH"
printf '%s\n' "$AL_DICH"
