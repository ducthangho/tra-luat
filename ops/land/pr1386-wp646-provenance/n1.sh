#!/usr/bin/env bash
# N1: `bash n1.sh <đường-kho> <B> <H> <script-N5>`. rc 0: H = base + khối đã chốt, cùng mode, không gì khác.
# rc 1: nội dung sai. rc 2: LỖI MÔI TRƯỜNG (kho, git, python, đối số) — không kết luận gì về nội dung.
# Phạm vi độc lập môi trường ĐÃ ĐO: bỏ qua replace refs, config hệ thống/toàn cục, thuộc tính hệ thống, biến GIT_DIR/
# GIT_WORK_TREE/GIT_OBJECT_DIRECTORY/GIT_ALTERNATE_OBJECT_DIRECTORIES/GIT_INDEX_FILE/GIT_COMMON_DIR, diff.* và .gitattributes
# của kho. GIẢ ĐỊNH tin cậy, không đóng: kho đích (config cục bộ, alternates trong .git/objects/info) do chính phiên kiểm
# dựng, và SHA-1 không va chạm (cùng OID ⇒ cùng nội dung, nên alternates không đổi được nội dung theo OID).
set -u
[ $# -eq 4 ] || { echo "N1 MOI_TRUONG: can 4 doi so"; exit 2; }
R=$1; B=$2; H=$3; N5=$4; P=docs/PROTOCOL_DA_PHIEN.md
unset GIT_DIR GIT_WORK_TREE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_INDEX_FILE GIT_COMMON_DIR \
      GIT_NAMESPACE GIT_REPLACE_REF_BASE GIT_GRAFT_FILE GIT_SHALLOW_FILE GIT_CONFIG GIT_CONFIG_PARAMETERS GIT_CONFIG_COUNT
export GIT_NO_REPLACE_OBJECTS=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_ATTR_NOSYSTEM=1
T=$(mktemp -d) || { echo "N1 MOI_TRUONG: mktemp"; exit 2; }
do_(){ echo "N1 DO: $1"; rm -rf "$T"; exit 1; }
mt(){ echo "N1 MOI_TRUONG: $1"; rm -rf "$T"; exit 2; }
g(){ git -C "$R" -c diff.ignoreSubmodules=none -c core.quotePath=true "$@"; }
command -v python3 >/dev/null || mt "khong co python3"
gd=$(g rev-parse --git-dir 2>&1) || mt "khong mo duoc kho $R: $gd"
for x in "$B" "$H"; do
  [[ $x =~ ^[0-9a-f]{40}$ ]] || mt "B/H phai la OID 40 hex: $x"
  ty=$(g cat-file -t "$x" 2>&1) || mt "khong doc duoc object $x: $ty"
  [ "$ty" = commit ] || do_ "$x la $ty, khong phai commit"
done
# Cây của H đọc thẳng từ object commit thô, đối chiếu với rev-parse (chốt dự phòng cho replace).
tr=$(g cat-file commit "$H" | sed -n '1s/^tree //p') || mt "khong doc duoc commit H"
[ "$tr" = "$(g rev-parse "$H^{tree}")" ] || do_ "cay H lech giua object tho va rev-parse"
oB=$(g rev-parse --verify -q "$B:$P") || do_ "base khong co $P"
oH=$(g rev-parse --verify -q "$H:$P") || do_ "H khong co $P"
raw=$(g diff-tree -r --no-renames --ignore-submodules=none --raw --no-abbrev "$B" "$H") || mt "diff-tree loi"
[ "$raw" = "$(printf ':100644 100644 %s %s M\t%s' "$oB" "$oH" "$P")" ] \
  || do_ "diff-tree khac dung mot dong M 100644->100644 cho $P: $(printf '%s' "$raw" | head -2 | tr '\t\n' ' |')"
g cat-file blob "$oB" > "$T/base.md" && g cat-file blob "$oH" > "$T/h.md" || mt "khong doc duoc blob"
dem=$(python3 -I -c '
import sys,difflib
a=open(sys.argv[1],"rb").read().split(b"\n"); b=open(sys.argv[2],"rb").read().split(b"\n")
t=x=0
for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
    if op!="equal": x+=i2-i1; t+=j2-j1
print(t,x)' "$T/base.md" "$T/h.md") || mt "khong dem duoc dong"
[ "$dem" = "14 0" ] || do_ "dong them/xoa = $dem, can 14 0"
python3 -I "$N5" --ky-vong "$T/base.md" "$T/kv.md" >/dev/null || do_ "khong dung duoc blob ky vong tu base"
kv=$(g hash-object --no-filters "$T/kv.md") || mt "hash-object loi"
[ "$oH" = "$kv" ] || do_ "blob H $oH khac blob ky vong $kv"
# N5 chạy trên đúng blob H vừa trích (cùng đường trích không replace).
python3 -I "$N5" "$T/h.md" >/dev/null || do_ "N5 do tren blob H"
echo "N1 DAT: blob $oH, mode 100644, them/xoa $dem"; rm -rf "$T"
