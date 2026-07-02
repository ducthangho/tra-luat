# VBHN QT-5 verification gate (v1.17.14)

## Vấn đề thực tế

Log rà soát ATVSLĐ cho thấy cùng số `14/VBHN-VPQH` có thể được dùng ở nhiều năm/chủ đề khác nhau. Nếu corpus đặt tên trơ như `VBHN_14-VBHN-VPQH`, `vb_status` theo số hiệu có thể trả đúng số nhưng sai nội dung.

## Quy tắc

- Tìm VBHN theo **trích yếu + “hợp nhất”**, không chỉ theo số hiệu bản gốc.
- Sau khi có ứng viên, verify nội dung: tiêu đề, dòng “được sửa đổi, bổ sung bởi…”, văn bản gốc/sửa đổi và năm.
- Không kết luận “không có VBHN” chỉ vì manifest/corpus không có hit.
- Official-first: nếu chưa có bản chính thức, hỏi người dùng nạp vào `_HOP_NAP` hoặc lấy từ nguồn chính thức/đáng tin. Không tự ghép VBHN làm bản dùng/canonical/NLM.
- Bản tự ghép chỉ là bản tạm để so sánh; phải gắn `PROVISIONAL`/`ASSEMBLED`, không add NLM làm nguồn rà soát chính, và chuyển QUARANTINE khi có bản chính thức.

## Lệnh

```bash
tl vbhn-check --subject "an toàn vệ sinh lao động" --goc "84/2015/QH13" --year 2024
tl vbhn-check --scan --json
tl vbhn-verify --text-file vbhn.txt --expect-title "an toàn vệ sinh lao động" --expect-goc "84/2015/QH13" --expect-year 2024 --official-required
tl vbhn-compare --official-text official.txt --candidate-text assembled.txt --focus "Điều 53" --json
```

`--official-required` fail nếu chỉ thấy nội dung VBHN nhưng không có dấu hiệu nguồn chính thức/footnote. Số hiệu `VBHN-VPQH` trong text không đủ để xác nhận official.

`vbhn-compare` dùng khi đã có bản chính thức và cần loại bản tự ghép: cờ `CANDIDATE_MISSING_FOOTNOTES`, `FOCUS_DIFF:*`, `FOCUS_REF_DIFF:*` là lý do lấy official làm canonical và quarantine bản tạm.

## Hành động dữ liệu

Các VBHN thiếu năm/chủ đề cần đổi tên theo dạng:

`VBHN_<số>-<cơ quan>_<năm>_<tên_rút_gọn>_HopNhat`

Không quarantine hoặc đổi tên nếu chưa verify nội dung.
