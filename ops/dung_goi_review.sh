#!/usr/bin/env bash
# Dung GOI HIEN VAT cho reviewer khac nen — DU REF, DU CONG CU, DU TU KHAI.
#
# VI SAO CO TEP NAY. Viec dung goi hien vat truoc nay nam RAI RAC trong scratchpad tung phien
# chu khong phai mot thu chay duoc trong kho. Chuan hoa no vao mot script co the KIEM va CHAY LAI
# la mot cai thien co ly — nhung do la LUA CHON THIET KE, khong phai ket luan nguyen nhan.
#
# GIOI HAN PHAI DOC: ba su co duoi day KHONG duoc chung minh la chung mot nguyen nhan. Hien vat
# lich su cua chung khong con, nen khong ai kiem duoc tung ca xay ra the nao. Doc day nhu DANH
# SACH DONG CO viet tep nay, khong phai nhu chan doan da xac thuc:
#
#   PR #468 luot 12, P1 `mirror-thieu-ref-khong-du-do-a9`
#       goi chi mang 3 ten nhanh. Reviewer khong tai do duoc khang dinh toan kho.
#       DINH CHINH (cross-review PR #477, P3): ban dau tep nay ghi nguyen nhan la
#       "`ai-dang-giu` CHI QUET refs/heads/*". DIEU DO SAI. `_cac_ref_cuc_bo`
#       (`ops/lease_publish.py:307-321` ban b416830) chay `for-each-ref refs/heads refs/remotes` va
#       tinh ten tu CA `refs/remotes/origin/*`; `_quet_lease_toan_kho` doc het danh sach ay.
#       Banner CLI (`:937` ban b416830) in "quet refs/heads/*" nen de tin nham — do la loi doc banner
#       thay vi doc ma. Nguyen nhan LICH SU cua goi 3 ref: CHUA XAC THUC DUOC (hien vat luot
#       12 khong con). Cross-review #477 luot 2 do: `--bare --no-local` TU NO khong quyet dinh
#       — bare tu nguon co 306 local head thi giu du 306; bare tu clone thuong (1 local head)
#       moi con 1. Tuc phu thuoc CAU TRUC REF CUA NGUON. Chac chan KHONG phai pham vi quet;
#       phan con lai la GIA THUYET. Buoc materialize duoi day van giu, nhung vi ly do KHAC:
#       de goi khong phu thuoc ten remote va de doi chieu tap ten truc tiep.
#
#   PR #468 luot 13, P3 `evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu`
#       EVIDENCE.md khong khai CACH TRICH tung so va PHAN BO SOT, nen nguoi doc khong
#       phan biet duoc so nao da bam/dem lai va so nao chi la loi khai.
#
#   full-gate 2026-09-07, `t33_workflow_dang_lease_phai_qua_actionlint`
#       chay trong container THIEU `actionlint` -> bo lease rc=1. Noi cho chinh xac: ca t33
#       DA CHAY va DO o tien dieu kien (assertion o lease_publish_test.py:1359-1363 ban b416830,
#       ngay truoc subprocess.run dong 1364). Thu CHUA CHAY la thao tac LINT WORKFLOW ben trong ham.
#       Cong cu phai duoc cai TRUOC khi do.
#
# Nen chua o TANG: hanh vi dung goi nam trong MOT script chay duoc, tu do va tu khai
# gioi han, thay vi mot doan lenh chep tay moi luot.
#
# Ma thoat — RIENG BIET de nguoi goi khang dinh duoc LY DO:
#   2 thieu tham so        5 tao cay lam viec that bai
#   3 clone mirror hong    6 THIEU/LECH REF (goi KHONG du de tai do)
#   4 thieu cong cu bat buoc ma khong cai duoc
set -euo pipefail

loi() { ma="$1"; shift; printf '%s\n' "dung_goi_review: $*" >&2; exit "$ma"; }

R="${1-}"; HEAD_SHA="${2-}"
if [ -z "$R" ] || [ -z "$HEAD_SHA" ]; then
  loi 2 "dung: $0 <thu-muc-goi> <head-sha> [kho-nguon]"
fi
KHO="${3-$(pwd)}"
REMOTE=$(git -C "$KHO" remote get-url origin)
mkdir -p "$R"

# ---- 0. TU CHOI TAI DUNG vao mot goi DA DUNG — kiem TRUOC MOI thao tac ghi/xoa ----
# Khong xoa bo cai cu => dung lai cung `$R` se TICH LUY: cross-review #477 luot 4 do ba lan
# dung cung R, manifest tang 2142 -> 2154 -> 2166 (+12 tep, +7.385.648 byte moi lan).
# Chot nay phai o DAY chu khong o buoc cong cu: dat muon thi script da `rm -rf` va clone lai
# `kho.git`/`cay-kho` roi moi tu choi, lam HONG manifest cua lan dung truoc (do duoc: 1520/2136).
# Khong xoa toan bo $R — $R khong thuoc so huu cua script; nguoi goi phai dung mot $R MOI.
# (Luu y: script van rm -rf kho.git va cay-kho ben trong).
for cu in "$R"/cong-cu/actionlint.?????? "$R"/ARTIFACTS.sha256; do
  [ -e "$cu" ] || continue
  loi 4 "goi da duoc dung truoc (thay '$cu') — dung mot \$R MOI. Script khong xoa thu muc no khong tao ra."
done

GIO=$(date -u +%FT%TZ)
printf '%s\n' "$GIO" > "$R/gio-chup-ref.txt"

# ---- 1. Chup ten+OID tu MAY CHU tai gio chup (nguon su that) ----
git ls-remote --heads "$REMOTE" \
  | awk -v OFS='\t' '{sub(/^refs\/heads\//,"",$2); print $2,$1}' \
  | sort -u > "$R/nguon-refs.tsv"
N_NGUON=$(wc -l < "$R/nguon-refs.tsv")
[ "$N_NGUON" -gt 0 ] || loi 6 "ls-remote khong tra ve ref nao"

# ---- 2. Mirror DU MOI REF: khong --single-branch, khong --depth ----
# Cung lop rui ro voi `cong-cu` (xem #477 luot 3): symlink lam `rm -rf` xoa ra ngoai goi.
[ -L "$R/kho.git" ] && loi 3 "\$R/kho.git la symlink — tu choi de khong xoa ra ngoai goi"
rm -rf "$R/kho.git"
git clone --mirror -q "$REMOTE" "$R/kho.git" || loi 3 "clone mirror that bai"

# ---- 3. Cay lam viec, roi VAT CHAT HOA moi nhanh thanh refs/heads/* ----
#    LY DO DUNG (khong phai "ai-dang-giu chi quet refs/heads" — xem DINH CHINH o dau tep):
#    de goi KHONG PHU THUOC ten remote, va de doi chieu tap ten truc tiep giua ba nguon.
#    Scanner doc ca refs/remotes, nen buoc nay khong phai de "duoc dem".
# Cung lop rui ro voi `cong-cu` (xem #477 luot 3): symlink lam `rm -rf` xoa ra ngoai goi.
[ -L "$R/cay-kho" ] && loi 3 "\$R/cay-kho la symlink — tu choi de khong xoa ra ngoai goi"
rm -rf "$R/cay-kho"
git clone -q --no-single-branch "$R/kho.git" "$R/cay-kho" || loi 5 "clone cay lam viec that bai"
git -C "$R/cay-kho" checkout -q --detach "$HEAD_SHA" || loi 5 "khong checkout duoc $HEAD_SHA"
git -C "$R/cay-kho" config core.abbrev 7
git -C "$R/cay-kho" for-each-ref --format='%(refname)%09%(objectname)%09%(symref)' refs/remotes/origin \
  | awk -F'\t' '$3==""{sub(/^refs\/remotes\/origin\//,"",$1); print $1"\t"$2}' \
  | while IFS=$'\t' read -r ten oid; do git -C "$R/cay-kho" update-ref "refs/heads/$ten" "$oid"; done
# Remote `origin` phai la URL that: launcher kiem `--expected-repo`. Nguon object van la mirror.
# KHONG `|| true`: git template co san remote `mirror-cuc-bo` lam rename that bai, roi
# `add origin` cung that bai vi origin cu con do -> origin TRO SAI ma script van rc=0.
# Cross-review PR #477 tai hien duoc bang template that.
git -C "$R/cay-kho" remote rename origin mirror-cuc-bo || loi 5 "khong doi ten duoc remote origin"
git -C "$R/cay-kho" remote add origin "$REMOTE" || loi 5 "khong them duoc remote origin"
thuc_te=$(git -C "$R/cay-kho" remote get-url origin) || loi 5 "khong doc lai duoc origin"
[ "$thuc_te" = "$REMOTE" ] || loi 5 "origin SAI: mong doi '$REMOTE', thuc te '$thuc_te'"

# ---- 4. Doi chieu ba nguon nhu TAP HOP (ten+OID), khong so `wc -l` ----
for cap in "kho.git:refs/heads:mirror" "cay-kho:refs/heads:cay-kho"; do
  d=${cap%%:*}; rest=${cap#*:}; ns=${rest%%:*}; ten=${rest##*:}
  git -C "$R/$d" for-each-ref --format='%(refname)%09%(objectname)%09%(symref)' "$ns" \
    | awk -F'\t' -v OFS='\t' '$3==""{sub(/^refs\/heads\//,"",$1); print $1,$2}' \
    | sort -u > "$R/$ten-refs.tsv"
done
comm -3 "$R/nguon-refs.tsv" "$R/mirror-refs.tsv"  > "$R/refs-lech-mirror.tsv"
comm -3 "$R/nguon-refs.tsv" "$R/cay-kho-refs.tsv" > "$R/refs-lech-cay-kho.tsv"
N_MIRROR=$(wc -l < "$R/mirror-refs.tsv"); N_CAY=$(wc -l < "$R/cay-kho-refs.tsv")
N_L1=$(wc -l < "$R/refs-lech-mirror.tsv");  N_L2=$(wc -l < "$R/refs-lech-cay-kho.tsv")

# ---- 5. Cong cu bat buoc: LUON goi installer ghim cho actionlint, KHONG tin PATH cho cong cu nay ----
#    `ops/cai_actionlint.sh:14` (ban b416830) viet ro: "KHONG co nhanh thoat som `da co actionlint tren
#    PATH thi thoi`: co mat != dung ban." Ban dau tep nay CO nhanh ay -> cross-review PR #477
#    do duoc bon ca `wrong-version`/`invalid-pin`/`empty-pin`/`broken-binary` deu rc=0.
#    Nen: luon cai ban ghim, va bat rc bang ASSIGNMENT chu khong trong doi so `printf`
#    (rc trong command substitution KHONG lam `printf` that bai, `set -e` khong cuu duoc).
# `${VAR:-...}` thay ca khi RONG — the la nuot mot ban ghim rong thanh mac dinh.
# Dung `${VAR-...}` (chi khi CHUA DAT), roi chan tuong minh neu dat ma rong.
AL_VER="${AL_VER-1.7.7}"
[ -n "$AL_VER" ] || loi 4 "AL_VER duoc dat nhung RONG — khong tu thay bang mac dinh"

# Thu muc cai phai MOI — nhung TUYET DOI KHONG dat duoc bang `rm -rf`.
# Cross-review #477 luot 3 do duoc hai hau qua cua `rm -rf "$R/cong-cu/actionlint"`:
#   1. MAT DU LIEU NGOAI GOI: `$R` do caller chon. Neu `$R/cong-cu` la symlink toi mot thu
#      muc dung chung, `rm -rf` di qua thanh phan symlink O GIUA va xoa sach `actionlint` o
#      DICH. A/B tren cung nguon: 3d2ac9b giu sentinel, a6a5222 XOA sentinel, ca hai rc=0.
#   2. PHA DUONG OFFLINE: caller dat archive tai `$R/cong-cu/actionlint/cache.tar.gz` thi
#      `rm` xoa chinh dau vao TRUOC khi installer doc no.
# Nen: TU CHOI symlink, roi tao thu muc cai MOI bang `mktemp -d`. Khong xoa gi.
CONG_CU="$R/cong-cu"
[ -L "$CONG_CU" ] && loi 4 "\$R/cong-cu la symlink — tu choi de khong ghi/xoa ra ngoai goi"
mkdir -p "$CONG_CU" || loi 4 "khong tao duoc $CONG_CU"
[ -L "$CONG_CU" ] && loi 4 "\$R/cong-cu la symlink — tu choi de khong ghi/xoa ra ngoai goi"
AL_DICH=$(mktemp -d "$CONG_CU/actionlint.XXXXXX") || loi 4 "khong tao duoc thu muc cai actionlint"
AL_VER="$AL_VER" AL_DICH="$AL_DICH" bash "$KHO/ops/cai_actionlint.sh" > "$R/cai-actionlint.log" 2>&1 \
  || loi 4 "cai actionlint (ban ghim $AL_VER) that bai — xem $R/cai-actionlint.log"

# KHONG prepend AL_DICH vao PATH, va KHONG resolve lai actionlint theo TEN.
# Ly do (cung cross-review #477 luot 2):
#   - prepend ca thu muc => moi tep trong do che lenh he thong (be mat che lenh MOI do
#     chinh ban va truoc tao ra);
#   - `command -v actionlint` tra ve FUNCTION neu co `export -f actionlint`, vi bash
#     function uu tien hon PATH => van chay ban gia. Phan chung: function in "1.7.70".
# Nen: goi binary bang DUONG DAN CAI DAT CU THE (co the la tuong doi neu $R la tuong doi).
AL_BIN="$AL_DICH/actionlint"
[ -x "$AL_BIN" ] || AL_BIN="$AL_DICH/actionlint.exe"
[ -x "$AL_BIN" ] || loi 4 "khong thay binary actionlint trong $AL_DICH sau khi cai"

: > "$R/cong-cu.txt"

# actionlint: doc dong dau, bo CR, so BANG NHAU voi ban ghim.
# `case *"$AL_VER"*` la khop CHUOI CON — nhan ca `1.7.70` va `11.7.7`. Do la dung lop loi
# ma `cai_actionlint.sh` da tra gia o #200/#203.
if ! al_raw=$("$AL_BIN" --version 2>&1); then
  loi 4 "actionlint khong chay duoc: $AL_BIN"
fi
# #675: khong `| head -1` duoi pipefail (SIGPIPE -> rc=141 tren dau ra dai; do: ops/do_sigpipe.sh).
al_ban="${al_raw%%$'\n'*}"; al_ban="${al_ban//$'\r'/}"
[ "$al_ban" = "$AL_VER" ] || loi 4 "actionlint SAI BAN: can '$AL_VER', do duoc '$al_ban' ($AL_BIN)"
printf '%s\t%s\t%s\n' actionlint "$AL_BIN" "$al_ban" >> "$R/cong-cu.txt"

# Cac cong cu con lai: thao tac thuc te (git, v.v.) tin vao moi truong goi shell (bare name).
# Rieng viec ghi version o day moi dung `type -P` de trich duong dan nhung KHONG thay the lenh goi thuc te.
# THIEU hoac KHONG CHAY DUOC o buoc ghi nay deu la CHAN.
# `shellcheck` la BAT BUOC: thieu no thi `actionlint` bo luat SC* TRONG IM LANG.
for c in shellcheck git python3; do
  duong=$(type -P "$c" 2>/dev/null) || duong=""
  [ -n "$duong" ] || loi 4 "thieu cong cu bat buoc: $c"
  if ! raw=$("$duong" --version 2>&1); then
    loi 4 "cong cu bat buoc khong chay duoc: $c ($duong)"
  fi
  # Lay dong DAU TIEN co chu so — `shellcheck --version` in ten o dong 1, so o dong 2,
  # nen `head -1` ghi "ShellCheck - shell script analysis tool" vao cot "phien ban".
  ban=$(printf '%s\n' "$raw" | tr -d '\r' | grep -m1 '[0-9]' || true)
  [ -n "$ban" ] || loi 4 "cong cu bat buoc khong khai duoc phien ban: $c ($duong)"
  printf '%s\t%s\t%s\n' "$c" "$duong" "$ban" >> "$R/cong-cu.txt"
done

# ---- 6. EVIDENCE: khai CACH TRICH va PHAN BO SOT, khong chi khai ket qua ----
cat > "$R/EVIDENCE.md" <<EOF
# EVIDENCE — goi hien vat cho reviewer

Sinh boi \`ops/dung_goi_review.sh\` luc \`$GIO\`. Moi so duoi day do SCRIPT tinh, khong chep tay.

## Cach trich tung so

| so | trich bang | loai nguon |
|---|---|---|
| ref may chu | \`git ls-remote --heads origin\` -> \`nguon-refs.tsv\` | do lai duoc |
| ref mirror | \`for-each-ref refs/heads\` tren \`kho.git\`, bo symref | do lai duoc |
| ref cay lam viec | \`for-each-ref refs/heads\` tren \`cay-kho\` | do lai duoc |
| do lech | \`comm -3\` giua hai TSV — so TAP HOP (ten+OID) | do lai duoc |
| phien ban cong cu | \`<cong-cu> --version\` -> \`cong-cu.txt\` | do lai duoc |

## Bao phu ref

| nguon | so ref |
|---|---:|
| may chu | **$N_NGUON** |
| mirror trong goi | **$N_MIRROR** |
| cay lam viec | **$N_CAY** |

Lech mirror: **$N_L1** dong. Lech cay lam viec: **$N_L2** dong.

## PHAN BO SOT — doc truoc khi tin bang tren

- Object den tu \`kho.git\` CUC BO, khong tai truc tiep tu may chu luc review. Remote
  \`origin\` cua \`cay-kho\` do script DAT LAI thanh URL that de qua phep kiem
  \`--expected-repo\`; nguon object giu o remote \`mirror-cuc-bo\`.
- \`refs/heads/*\` trong \`cay-kho\` do \`update-ref\` tao. Day la CHU Y, khong phai rac.
- Anh chup ref la moc \`$GIO\`. Kho co the da doi sau do; khong co mang trong sandbox
  nen KHONG doi chieu lai duoc voi may chu tai luc reviewer doc.
- Chi phu \`refs/heads\`. KHONG co anh chup tag hay namespace khac.
- Bang nay khong phu CI tren GitHub Actions.
EOF

# ---- 7. Manifest: loai DUNG manifest goc, khong loai theo ten co so moi cap ----
# Loc theo DUONG DAN DAY DU. Khong dung `! -name` (loai theo ten co so o MOI cap) va
# khong loc hau to tren dong bam (thu muc ten `nested  .` lam dong con khop hau to).
( cd "$R" && find . -type f ! -path './ARTIFACTS.sha256' -print0 | sort -z \
    | xargs -0 sha256sum > ARTIFACTS.sha256 )

printf 'ref: nguon=%s mirror=%s cay-kho=%s; lech=%s/%s\n' "$N_NGUON" "$N_MIRROR" "$N_CAY" "$N_L1" "$N_L2"
if [ "$N_L1" -ne 0 ] || [ "$N_L2" -ne 0 ]; then
  loi 6 "THIEU/LECH REF — goi KHONG du de tai do"
fi
printf 'GOI DU DE TAI DO: %s/%s/%s ref, 0 lech\n' "$N_NGUON" "$N_MIRROR" "$N_CAY"
