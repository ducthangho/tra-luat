Bạn là reviewer ĐỘC LẬP (read-only với mã nguồn) cho packet #1195 `T191-PY314-INTERPOLATION` r1 của kho ducthangho/tra-luat.
Thư mục làm việc là một clone ở head `ab39416fe919452c9dadda38dd99c5589f7967e8`; base là `1813bfd4513704cf792a272a86b22e5e08893b9a`
(merge-base với master). Đặc tả đóng băng: `SPEC_R1.md` trong thư mục này (sha256 e6ea2cf7c20279e6f1521b71b6562e811add01256d6c373d677acf9e3acf4ebe).

Diff: `git diff 1813bfd4 ab39416 -- ops/lease_publish_test.py` (một tệp, ~19 dòng thêm). Ca liên quan: `t191_MOI_chot_cua_kiem_deu_duoc_t190_phu_o_nhanh_DA_DANG`
và các hàm `_*_t191` quanh dòng 10925–11330.

Hai trình thông dịch có sẵn:
- Python 3.13: `python3`
- Python 3.14: `/tmp/claude-0/v314/bin/python` (có PyYAML)
Chạy một ca: `<py> -B ops/lease_publish_test.py --chi-ca=t191_MOI_chot_cua_kiem_deu_duoc_t190_phu_o_nhanh_DA_DANG` (~20–50 s).

Việc:
1. Chạy t191 trên cả hai phiên bản ở head; ghi kết quả bằng số.
2. Đột biến TRÊN BẢN SAO (đừng sửa tệp trong clone; chép `ops/lease_publish.py` + `ops/lease_publish_test.py` sang một thư mục con mới
   trong thư mục làm việc, mỗi đột biến một thư mục, chạy với `-B`): gỡ từng phần R1..R5 của đặc tả; mỗi đột biến phải làm t191 ĐỎ trên 3.14
   (R5 có thể bị chốt khác che — nói rõ nếu vậy). Thử thêm ít nhất một đột biến bạn tự nghĩ ra nhằm chỗ bản vá có thể NỚI chốt
   (vd mục miễn khớp rộng hơn cần, `_bo_str_t191` đổi hành vi lớp khác, điều kiện phiên bản sai).
3. Soát: bản vá có nới chốt chung nào không; mục miễn mới có đúng luật của ca (lý do đo được, mọi lần xuất hiện hỏng đúng lý do);
   hành vi 3.13 có đổi không; có nút/trường 3.14 nào khác bị bỏ sót không.
Ghi kết luận vào `VERDICT.md` trong thư mục làm việc: dòng đầu `VERDICT: approve` hoặc `VERDICT: request_changes`, rồi danh sách finding
P0–P3 (mỗi finding: tệp:dòng, kịch bản hỏng cụ thể, bằng chứng chạy được), rồi bảng đột biến (tên, rc, ĐỎ/XANH). Không sửa tệp nào khác
ngoài VERDICT.md và thư mục đột biến của bạn.
