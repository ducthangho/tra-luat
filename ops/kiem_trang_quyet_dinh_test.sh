#!/usr/bin/env bash
# Phản chứng CHẠY ĐƯỢC cho ops/kiem_trang_quyet_dinh.sh — R5-02 (cross-review lượt 5).
#
# Bảy ca đo BA TRẠNG THÁI (0 sạch · 1 còn lời khai đã rút · 2 KHÔNG ĐO ĐƯỢC), rồi HAI
# đột biến quay cổng về ĐÚNG HÌNH DẠNG CŨ để chứng minh các ca ấy CÓ RĂNG. Một ca chỉ
# "có mặt" mà không đỏ dưới đột biến thì nó không đo gì — bài học `t24` của kho này.
#
# Đột biến chạy trên BẢN SAO TẠM, không đụng tệp thật (bài học "bom hẹn giờ" của
# `finally`: lượt chạy bị cắt giữa chừng thì tệp thật ở lại trạng thái đã méo).
#
# KHÔNG dùng `set -e`: bộ test PHẢI đọc được mã thoát khác 0, đó là dữ liệu của nó.
set -uo pipefail

GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONG="$GOC/ops/kiem_trang_quyet_dinh.sh"
TAI_LIEU="$GOC/ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

DAT=0; HONG=0
ket() {  # ket <ten ca> <mong doi> <thuc te> [ghi chu]
  if [ "$2" = "$3" ]; then DAT=$((DAT + 1)); printf '  ĐẠT   %-46s rc=%s\n' "$1" "$3"
  else HONG=$((HONG + 1)); printf '  HỎNG  %-46s đòi rc=%s, được rc=%s  %s\n' "$1" "$2" "$3" "${4:-}"; fi
}
chay() { bash "$1" "$2" >/dev/null 2>&1; echo $?; }   # chay <cong> <tai lieu> -> in rc

[ -f "$CONG" ]     || { echo "KHÔNG ĐO ĐƯỢC: thiếu $CONG" >&2; exit 2; }
[ -f "$TAI_LIEU" ] || { echo "KHÔNG ĐO ĐƯỢC: thiếu $TAI_LIEU" >&2; exit 2; }

# ------------------------------------------------------------------ dựng tài liệu biến thể
D_GOC="$TMP/goc.md";        cp "$TAI_LIEU" "$D_GOC"
D_MAT_MO="$TMP/mat-mo.md";  sed 's|^# §1.*|# MỘT MỤC KHÁC|' "$TAI_LIEU" > "$D_MAT_MO"
D_DOI_MOC="$TMP/doi-moc.md"; sed 's|^# PHỤ LỤC.*|# PHU LUC (đã đổi tên)|' "$TAI_LIEU" > "$D_DOI_MOC"
# Cắt ngay TRƯỚC dòng PHỤ LỤC: §1 và §2 nguyên vẹn, chỉ MẤT MỐC KẾT THÚC.
L_PL=$(grep -nE '^# PHỤ LỤC' "$TAI_LIEU" | head -1 | cut -d: -f1)
D_CAT="$TMP/cat.md";        head -n "$((L_PL - 1))" "$TAI_LIEU" > "$D_CAT"
# Đối chứng DƯƠNG: chèn một chuỗi cấm THẬT vào giữa §1 (lấy từ chính bảng MAU).
L_S1=$(grep -nE '^# §1' "$TAI_LIEU" | head -1 | cut -d: -f1)
D_BAN="$TMP/ban.md"
awk -v n="$((L_S1 + 2))" 'NR==n{print "Mốc neo 61% vẫn đang tuân thủ."} {print}' "$TAI_LIEU" > "$D_BAN"

# ------------------------------------------------------------------ dựng cổng đột biến
# M-REGEX: bơm lỗi vào MÃ ĐO (regex không hợp lệ) — đo NHÁNH XỬ LÝ LỖI của grep,
# không nói regex hiện hành sai.
C_REGEX="$TMP/cong-regex-hong.sh"
sed "s@^MAU=.*@MAU='61%|48,8%('@" "$CONG" > "$C_REGEX"

# M1: trạng thái thứ ba của grep rơi xuống nhánh SẠCH — đúng hình dạng bản đầu.
C_M1="$TMP/cong-m1.sh"
sed 's|^  \*) khong_do "grep hỏng (mã ${rc}) khi quét mẫu cấm.*|  *) : ;;|' "$CONG" > "$C_M1"
grep -q '^\s*\*) : ;;' "$C_M1" || { echo "KHÔNG ĐO ĐƯỢC: M1 không vá được vào cổng" >&2; exit 2; }
C_M1_REGEX="$TMP/cong-m1-regex-hong.sh"
sed "s@^MAU=.*@MAU='61%|48,8%('@" "$C_M1" > "$C_M1_REGEX"

# M2: bỏ chốt đếm/thứ tự mốc và quay về phép trích THEO MẪU của bản đầu.
C_M2="$TMP/cong-m2.sh"
python3 - "$CONG" "$C_M2" <<'PY'
import io, sys, re
src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8").read()
n = 0
for pat in (r'^\[ "\$N_MO"[^\n]*\n', r'^\[ "\$N_DONG"[^\n]*\n', r'^\[ "\$L_MO" -lt[^\n]*\n'):
    s, k = re.subn(pat, "", s, flags=re.M); n += k
cu = ("THAN=$(awk '/^# §1/{f=1} /^# PHỤ LỤC/{f=0} f' \"$TEP\" "
      "| awk '/^```/{c=!c; next} !c')\n")
s, k = re.subn(r'^THAN=\$\(awk -v a=.*?\n.*?\n', cu, s, flags=re.M | re.S); n += k
assert n == 4, f"M2 chỉ vá được {n}/4 chỗ — cổng đã đổi, phép đo này KHÔNG ĐO ĐƯỢC"
io.open(dst, "w", encoding="utf-8").write(s)
PY
[ $? -eq 0 ] || { echo "KHÔNG ĐO ĐƯỢC: M2 không dựng được" >&2; exit 2; }

# CHỐT: mỗi cổng đột biến phải KHÁC cổng thật và KHÔNG RỖNG. Một tệp rỗng chạy rc=0,
# và rc=0 ở đây đọc y hệt "đột biến có răng" — đã sập thật ở lượt dựng đầu (sed hỏng vì
# dấu `|` trùng dấu phân cách, ba cổng ra tệp rỗng, bảng vẫn in CÓ RĂNG).
for c in "$C_REGEX" "$C_M1" "$C_M1_REGEX" "$C_M2"; do
  [ -s "$c" ] || { echo "KHÔNG ĐO ĐƯỢC: cổng đột biến RỖNG: $c" >&2; exit 2; }
  cmp -s "$c" "$CONG" && { echo "KHÔNG ĐO ĐƯỢC: cổng đột biến GIỐNG HỆT cổng thật: $c" >&2; exit 2; }
done

# ------------------------------------------------------------------ 7 ca trên cổng THẬT
echo "== cổng THẬT (đòi 0 · 2 · 2 · 2 · 2 · 2 · 1) =="
ket "c1 tài liệu nguyên trạng"                 0 "$(chay "$CONG" "$D_GOC")"
ket "c2 regex trong cổng không hợp lệ"         2 "$(chay "$C_REGEX" "$D_GOC")"
ket "c3 mất mốc mở"                            2 "$(chay "$CONG" "$D_MAT_MO")"
ket "c4 tệp không tồn tại"                     2 "$(chay "$CONG" "$TMP/khong-he-co.md")"
ket "c5 cắt ngay trước PHỤ LỤC (mất mốc đóng)" 2 "$(chay "$CONG" "$D_CAT")"
ket "c6 đổi tên mốc PHỤ LỤC"                   2 "$(chay "$CONG" "$D_DOI_MOC")"
ket "c7 chuỗi cấm THẬT trong §1"               1 "$(chay "$CONG" "$D_BAN")"

# ------------------------------------------------------------------ răng: đột biến phải làm ca ĐỎ
echo "== ĐỘT BIẾN (mỗi dòng dưới đây phải LỆCH so cổng thật, nếu không thì ca trên rỗng) =="
R=0
m_regex=$(chay "$C_M1_REGEX" "$D_GOC")
if [ "$m_regex" = 2 ]; then echo "  KHÔNG RĂNG  M1 (grep mã 3 rơi xuống nhánh sạch): c2 vẫn rc=2"; R=$((R+1))
else echo "  CÓ RĂNG     M1 → c2 rc=$m_regex (cổng thật 2): phép đo hỏng bị báo SẠCH, đúng bệnh bản đầu"; fi
m_cat=$(chay "$C_M2" "$D_CAT")
if [ "$m_cat" = 2 ]; then echo "  KHÔNG RĂNG  M2 (bỏ chốt mốc, trích theo mẫu): c5 vẫn rc=2"; R=$((R+1))
else echo "  CÓ RĂNG     M2 → c5 rc=$m_cat (cổng thật 2): mất mốc đóng mà vẫn kết luận"; fi
m_doi=$(chay "$C_M2" "$D_DOI_MOC")
if [ "$m_doi" = 2 ]; then echo "  KHÔNG RĂNG  M2: c6 vẫn rc=2"; R=$((R+1))
else echo "  CÓ RĂNG     M2 → c6 rc=$m_doi (cổng thật 2): quét tràn sang lịch sử"; fi
# Đối chứng NGƯỢC: đột biến KHÔNG được làm hỏng ca dương — nếu nó hỏng cả c7 thì
# ba dòng trên chỉ đang đo "cổng đột biến vỡ", không đo chốt nào.
m_ban=$(chay "$C_M2" "$D_BAN")
if [ "$m_ban" = 1 ]; then echo "  ĐỐI CHỨNG   M2 giữ nguyên c7 rc=1 — đột biến nhắm chốt mốc, không phá cả cổng"
else echo "  KHÔNG RĂNG  M2 làm c7 thành rc=$m_ban (đòi 1): đột biến phá cổng, ba dòng trên vô nghĩa"; R=$((R+1)); fi

echo
echo "kiem_trang_quyet_dinh: ${DAT} đạt / ${HONG} hỏng / ${R} chốt KHÔNG RĂNG"
[ "$HONG" -eq 0 ] && [ "$R" -eq 0 ] && [ "$DAT" -eq 7 ] || exit 1
echo "TỔNG: ĐẠT (7/7 ca, 4/4 phép đo răng)"
