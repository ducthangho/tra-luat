#!/usr/bin/env bash
# Chốt cho `R4-02`: TRANG QUYẾT ĐỊNH (§1) không được mang lời khai ĐÃ BỊ RÚT.
#
# VÌ SAO CÓ: cross-review lượt 4 đo được rằng bản trước sửa phần bằng chứng rồi
# QUÊN phần khuyến nghị — nơi chủ kho thực sự đọc để hành động. Hai tầng cho hai
# kết luận ngược nhau; tệp không quyết định được.
#
# VÌ SAO BỎ KHỐI MÃ: lần viết đầu của chốt này in chính lệnh grep vào §1, nên nó
# TỰ KHỚP mẫu của mình và luôn ĐỎ. Một chốt phải phân biệt được nội dung với công
# cụ đo nội dung.
set -euo pipefail
TEP="${1:-ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md}"
# Các chuỗi này đều là lời khai đã bị rút ở một lượt cross-review, kèm lượt đã rút:
#   61% · 40/82 · 48,8% · 50/82  -> N1 / R4-01   |  81/82 -> N2
#   "co giãn"                    -> lượt 2 B2    |  "đòn bẩy mạnh nhất" -> lượt 2 (PR #250)
MAU='61%|40/82|48,8%|50/82|81/82|co giãn|đòn bẩy mạnh nhất'
THAN=$(awk '/^# §1/{f=1} /^# PHỤ LỤC/{f=0} f' "$TEP" | awk '/^```/{c=!c; next} !c')
if printf '%s\n' "$THAN" | grep -nE "$MAU"; then
  echo "ĐỎ: trang quyết định còn mang lời khai ĐÃ BỊ RÚT (xem trên) — bệnh R4-02 tái phát." >&2
  exit 1
fi
DONG=$(printf '%s\n' "$THAN" | grep -c '' || true)
if [ "$DONG" -lt 20 ]; then
  echo "ĐỎ: KHÔNG ĐO ĐƯỢC — chỉ trích được $DONG dòng cho §1; mốc neo '# §1'/'# PHỤ LỤC' đã đổi?" >&2
  exit 2
fi
echo "ok: trang quyết định sạch — đã soi $DONG dòng (đã bỏ khối mã), 0 lời khai bị rút"
