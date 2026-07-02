# VBHN official-first gate (v1.17.14)

## Vấn đề từ log thực tế

Bản VBHN ATVSLĐ tự lắp từ luật gốc + Điều 139 Luật BHXH đã gần đúng nhưng vẫn sai quy phạm ở Điều 53: câu tham chiếu cũ không bị xóa, nên tồn tại cả `khoản 1 Điều 111` và `khoản 1 Điều 90`. Bản tự lắp cũng thiếu footnote hợp nhất `[1]–[8]` và mang lỗi nhỏ từ corpus gốc.

Kết luận vận hành: không tự ghép VBHN để làm bản dùng. Khi thiếu VBHN chính thức, hỏi người dùng nạp file vào `_HOP_NAP` hoặc tìm nguồn chính thức/đáng tin.

## Quy trình bắt buộc

1. Chạy `source-map` và `vbhn-check`.
2. Nếu corpus chưa có VBHN chính thức, dừng ở REVIEW và hỏi người dùng nạp file chính thức.
3. Sau khi có file chính thức, export text rồi chạy:

```bash
python scripts/tl.py vbhn-verify --text-file official.txt --expect-title "an toàn vệ sinh lao động" --expect-goc "84/2015/QH13" --expect-goc "41/2024/QH15" --expect-year 2024 --official-required --source-name "14_VBHN-VPQH_629950.docx" --json
```

4. Nếu đã có bản tạm/tự ghép, so sánh trước khi thay:

```bash
python scripts/tl.py vbhn-compare --official-text official.txt --candidate-text assembled.txt --focus "Điều 53" --json
```

5. Lấy bản chính thức làm canonical, register + metadata + NLM. Bản tạm phải gỡ NLM, đổi tên `ZZZ_ASSEMBLED...KHONG_DUNG` hoặc tương đương và chuyển `QUARANTINE`.

## Cờ cần xử lý

- `ASSEMBLED_VBHN_NOT_ALLOWED_AS_CANONICAL`: nguồn/tên có dấu hiệu tự ghép; không được chốt làm bản dùng.
- `OFFICIAL_SOURCE_NOT_CONFIRMED`: chưa có dấu hiệu nguồn chính thức rõ.
- `VBHN_FOOTNOTES_NOT_EVIDENT`: không thấy footnote hợp nhất, cần kiểm lại nguồn.
- `CANDIDATE_MISSING_FOOTNOTES`: bản tạm thiếu footnote so với official.
- `FOCUS_DIFF:*` hoặc `FOCUS_REF_DIFF:*`: khác nội dung/tham chiếu tại điều trọng tâm, phải dùng official.

