#!/usr/bin/env bash
# Chốt: TRANG QUYẾT ĐỊNH (§1) của bản phản biện KHÔNG được mang lại lời khai ĐÃ RÚT.
#
# BA TRẠNG THÁI, không phải hai. Bản đầu của tệp này ĐỒNG NHẤT "phép đo thất bại"
# với "không tìm thấy" — R5-02 (cross-review lượt 5, `4951f55`) đo được:
# `grep` trả 1 khi KHÔNG KHỚP và **>1 khi KHÔNG THỰC HIỆN ĐƯỢC phép đo**, mà bản đầu
# cho cả hai rơi xuống nhánh in SẠCH. `set -euo pipefail` KHÔNG chữa được, vì lệnh
# nằm trong ĐIỀU KIỆN của `if` — bash cố ý miễn trừ chỗ đó.
# Ba phản chứng đã đo trên bản đầu: regex hỏng ⇒ **rc=0 "sạch"** (stderr có
# `grep: Invalid regular expression`, stdout vẫn báo sạch) · cắt tài liệu ngay trước
# PHỤ LỤC, tức MẤT MỐC KẾT THÚC ⇒ **rc=0 "đã soi 77 dòng"** · đổi tên mốc PHỤ LỤC ⇒
# **rc=1 bắt oan** vì phép quét tràn sang phần lịch sử. Cùng họ với bài học
# "cổng không nói dối — nó VẮNG MẶT": ở đây cổng CÓ MẶT và nói SẠCH khi nó mù.
#
#   0 = SẠCH  ·  1 = còn lời khai ĐÃ RÚT  ·  2 = KHÔNG ĐO ĐƯỢC
#
# Phản chứng chạy được (gồm cả đột biến quay về hình dạng cũ): ops/kiem_trang_quyet_dinh_test.sh
#
# KHAI THẲNG PHẠM VI: **KHÔNG workflow nào chạy cổng này, và cũng không chạy bộ test của nó.**
# `ci_dang_ky_test.py` chỉ quét `*_test.py` nên một `*_test.sh` KHÔNG nằm trong sổ, tức không có
# gì báo động nếu nó thối rữa. Đây là chốt CHẠY TAY của §1.4, và nói ra điều đó rẻ hơn nhiều so
# với để người đọc tưởng có máy canh — bài học 'phạm vi TUYÊN BỐ phải bằng phạm vi ĐO ĐƯỢC'.
set -euo pipefail

RC_BAN=1
RC_KHONG_DO=2

khong_do() { echo "KHÔNG ĐO ĐƯỢC: $*" >&2; exit "$RC_KHONG_DO"; }

TEP="${1:-ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md}"
[ -f "$TEP" ] || khong_do "không phải tệp thường: ${TEP}"
[ -r "$TEP" ] || khong_do "không đọc được: ${TEP}"

MOC_MO='^# §1'
MOC_DONG='^# PHỤ LỤC'
# Các lời khai ĐÃ BỊ RÚT ở bản 5/bản 6 — chúng KHÔNG được quay lại trang quyết định.
MAU='61%|40/82|48,8%|50/82|81/82|co giãn|đòn bẩy mạnh nhất'

# grep có BA mã thoát: 0 khớp · 1 không khớp · >1 KHÔNG ĐO ĐƯỢC.
# Hàm này trả 9 cho trạng thái thứ ba để người gọi KHÔNG thể nhầm nó thành "0 khớp".
dem() {  # dem <regex>  ->  in "<số dòng khớp> <số hiệu dòng khớp đầu tiên>"
  local re="$1" out="" rc=0
  out=$(grep -nE -- "$re" "$TEP") || rc=$?
  case "$rc" in
    0) printf '%s %s\n' "$(printf '%s\n' "$out" | wc -l)" "${out%%:*}" ;;
    1) printf '0 0\n' ;;
    *) return 9 ;;
  esac
}

KQ=$(dem "$MOC_MO")   || khong_do "grep hỏng (mã $?) khi đếm mốc mở ${MOC_MO}"
read -r N_MO L_MO <<<"$KQ"
KQ=$(dem "$MOC_DONG") || khong_do "grep hỏng (mã $?) khi đếm mốc đóng ${MOC_DONG}"
read -r N_DONG L_DONG <<<"$KQ"

# Đòi ĐÚNG MỘT mốc mỗi loại và đúng THỨ TỰ. Thiếu mốc đóng thì phạm vi quét không
# xác định được — đó là KHÔNG ĐO ĐƯỢC, KHÔNG phải "quét tới hết tệp rồi kết luận".
[ "$N_MO"   -eq 1 ] || khong_do "mốc mở ${MOC_MO} xuất hiện ${N_MO} lần, đòi ĐÚNG 1 — mốc neo đã đổi?"
[ "$N_DONG" -eq 1 ] || khong_do "mốc đóng ${MOC_DONG} xuất hiện ${N_DONG} lần, đòi ĐÚNG 1 — mốc neo đã đổi?"
[ "$L_MO" -lt "$L_DONG" ] || khong_do "mốc mở ở dòng ${L_MO} KHÔNG đứng trước mốc đóng ở dòng ${L_DONG}"

THAN=$(awk -v a="$L_MO" -v b="$L_DONG" 'NR>=a && NR<b' "$TEP" \
       | awk '/^```/{c=!c; next} !c') || khong_do "awk hỏng khi trích §1 (dòng ${L_MO}–${L_DONG})"

DONG=$(printf '%s\n' "$THAN" | wc -l)
[ "$DONG" -ge 20 ] || khong_do "chỉ trích được ${DONG} dòng cho §1 (đòi ≥20) — cấu trúc tài liệu đã đổi?"

rc=0
KHOP=$(printf '%s\n' "$THAN" | grep -nE -- "$MAU") || rc=$?
case "$rc" in
  0) printf '%s\n' "$KHOP" >&2
     echo "ĐỎ: trang quyết định còn mang lời khai ĐÃ BỊ RÚT (xem trên) — bệnh R4-02 tái phát." >&2
     exit "$RC_BAN" ;;
  1) : ;;
  *) khong_do "grep hỏng (mã ${rc}) khi quét mẫu cấm — KHÔNG được kết luận SẠCH từ một phép đo hỏng" ;;
esac

echo "ok: trang quyết định sạch — đã soi ${DONG} dòng (§1 ở dòng ${L_MO}–$((L_DONG - 1)), đã bỏ khối mã), 0 lời khai bị rút"
