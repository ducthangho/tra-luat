#!/usr/bin/env bash
# Dung GOI HIEN VAT cho reviewer khac nen — DU REF, DU CONG CU, DU TU KHAI.
#
# VI SAO CO TEP NAY. Ba lan lien tiep cung mot hinh dang loi, deu vi viec dung goi
# nam RAI RAC trong scratchpad cua tung phien chu khong phai mot thu chay duoc trong kho:
#
#   PR #468 luot 12, P1 `mirror-thieu-ref-khong-du-do-a9`
#       goi chi mang 3 ten nhanh. Reviewer khong tai do duoc khang dinh toan kho.
#       Nguyen nhan: `git clone` mac dinh + `ai-dang-giu` CHI QUET `refs/heads/*`, nen
#       remote-tracking ref KHONG duoc dem. Checkout du noi dung tai HEAD != du ref.
#
#   PR #468 luot 13, P3 `evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu`
#       EVIDENCE.md khong khai CACH TRICH tung so va PHAN BO SOT, nen nguoi doc khong
#       phan biet duoc so nao da bam/dem lai va so nao chi la loi khai.
#
#   full-gate 2026-09-07, `t33_workflow_dang_lease_phai_qua_actionlint`
#       chay trong container THIEU `actionlint` -> `KHONG DO DUOC` -> bo lease rc=1.
#       Khong do va khong xanh: no KHONG CHAY. Cong cu phai duoc cai TRUOC khi do.
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

GIO=$(date -u +%FT%TZ)
printf '%s\n' "$GIO" > "$R/gio-chup-ref.txt"

# ---- 1. Chup ten+OID tu MAY CHU tai gio chup (nguon su that) ----
git ls-remote --heads "$REMOTE" \
  | awk -v OFS='\t' '{sub(/^refs\/heads\//,"",$2); print $2,$1}' \
  | sort -u > "$R/nguon-refs.tsv"
N_NGUON=$(wc -l < "$R/nguon-refs.tsv")
[ "$N_NGUON" -gt 0 ] || loi 6 "ls-remote khong tra ve ref nao"

# ---- 2. Mirror DU MOI REF: khong --single-branch, khong --depth ----
rm -rf "$R/kho.git"
git clone --mirror -q "$REMOTE" "$R/kho.git" || loi 3 "clone mirror that bai"

# ---- 3. Cay lam viec, roi VAT CHAT HOA moi nhanh thanh refs/heads/* ----
#    `ai-dang-giu` chi quet refs/heads/*; khong buoc nay thi goi lai thieu ref.
rm -rf "$R/cay-kho"
git clone -q --no-single-branch "$R/kho.git" "$R/cay-kho" || loi 5 "clone cay lam viec that bai"
git -C "$R/cay-kho" checkout -q --detach "$HEAD_SHA" || loi 5 "khong checkout duoc $HEAD_SHA"
git -C "$R/cay-kho" config core.abbrev 7
git -C "$R/cay-kho" for-each-ref --format='%(refname)%09%(objectname)%09%(symref)' refs/remotes/origin \
  | awk -F'\t' '$3==""{sub(/^refs\/remotes\/origin\//,"",$1); print $1"\t"$2}' \
  | while IFS=$'\t' read -r ten oid; do git -C "$R/cay-kho" update-ref "refs/heads/$ten" "$oid"; done
# Remote `origin` phai la URL that: launcher kiem `--expected-repo`. Nguon object van la mirror.
git -C "$R/cay-kho" remote rename origin mirror-cuc-bo 2>/dev/null || true
git -C "$R/cay-kho" remote add origin "$REMOTE" 2>/dev/null || true

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

# ---- 5. Cong cu bat buoc: CAI TRUOC khi do, dung ban ghim cua kho ----
: > "$R/cong-cu.txt"
if ! command -v actionlint >/dev/null 2>&1; then
  if AL_VER="${AL_VER:-1.7.7}" AL_DICH="$R/cong-cu/actionlint" bash "$KHO/ops/cai_actionlint.sh" >>"$R/cong-cu.txt" 2>&1; then
    export PATH="$R/cong-cu/actionlint:$PATH"
  else
    loi 4 "thieu \`actionlint\` va cai khong duoc — xem $R/cong-cu.txt"
  fi
fi
{ printf 'actionlint\t%s\t%s\n' "$(command -v actionlint)" "$(actionlint --version 2>/dev/null | head -1)"
  for c in shellcheck rg git python3; do
    printf '%s\t%s\t%s\n' "$c" "$(command -v "$c" || echo THIEU)" "$("$c" --version 2>/dev/null | head -1)"
  done; } >> "$R/cong-cu.txt"

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
( cd "$R" && find . -type f -print0 | sort -z | xargs -0 sha256sum \
    | grep -v '  \./ARTIFACTS\.sha256$' > ARTIFACTS.sha256 )

printf 'ref: nguon=%s mirror=%s cay-kho=%s; lech=%s/%s\n' "$N_NGUON" "$N_MIRROR" "$N_CAY" "$N_L1" "$N_L2"
if [ "$N_L1" -ne 0 ] || [ "$N_L2" -ne 0 ]; then
  loi 6 "THIEU/LECH REF — goi KHONG du de tai do"
fi
printf 'GOI DU DE TAI DO: %s/%s/%s ref, 0 lech\n' "$N_NGUON" "$N_MIRROR" "$N_CAY"
