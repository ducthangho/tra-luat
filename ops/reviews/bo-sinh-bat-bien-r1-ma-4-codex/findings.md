## R4-01 — P3 — hai nguồn cùng lệch làm mất bộ đối số bắt buộc

Lớp `nghiem-thu-khong-co-lap-chot-dich`; SPEC §2.3.1. Vị trí `ops/gate_output_doi_chieu_test.py:1137`, `:1177`, `:1193`.

Trên clone, đổi đúng hai neo:

```python
_mau_loai_unicode("\r\n", {"Cs"})
# thành
_mau_loai_unicode("\r", {"Cs"})

("\r\n", ("Cs",), 30, ("Cs",))
# thành
("\r", ("Cs",), 30, ("Cs",))
```

`a135` và `a136` đều rc 0, giống controls nguyên vẹn; không có `DO:`. Bộ thứ năm nguyên văn của SPEC đã biến mất. AST đối chiếu với bảng kỳ vọng, nhưng cả hai đều lấy danh tính từ mã có thể cùng đổi; `goi` cũng được sinh từ bảng ấy. Bộ phản chứng `rieng` lại lấy miền từ cùng AST, nên chuyển sang chứng minh bộ mới thay cho bộ bắt buộc.

Đã quét đồng thời hai nguồn cho cả năm bộ: a136 bắt bộ 1/2 (rc 3), còn bộ 3/4/5 vẫn rc 0. Với bộ sinh giả chỉ sai tại bộ thứ năm nguyên văn, bản gốc trả rc 3 `DO:a135:…so_phan_tu/cuoi_ngoai_bmp`; bản cùng lệch trả rc 0 và trace không còn lời gọi `("\r\n", ("Cs",))`. Controls khỏe đều rc 0. Xem `ast-review.json`, `co-drift-witness.json`.

Đây là đột biến ngoài tập toán tử cố định nhưng **trong miền đặc tả**, đúng yêu cầu kiểm đổi dữ liệu ở hai nơi. Không suy thành lỗi module sản phẩm ở HEAD nguyên vẹn.

Phép đóng: ghim danh tính năm bộ từ SPEC bằng nguồn kỳ vọng độc lập với các caller và bảng đang bị đột biến; tạo phản chứng riêng theo miền cố định này và đối chiếu cả AST lẫn các bộ đã kiểm với nó. Thêm phản chứng đổi đồng thời caller + kỳ vọng: bộ sinh chỉ sai tại bộ nguyên văn phải vẫn bị bắt. Ước **15–25 dòng thêm**, hoặc ít hơn nếu thay cơ chế AST bằng miền cố định. Rủi ro sửa: tăng trùng lặp hằng / chi phí meta-test; giữ kiểm mỗi bộ, các controls và đo lại thời gian. Nếu miễn: hồi quy đồng thời caller/kỳ vọng có thể bỏ hẳn một bộ đối số, còn bộ test vẫn tuyên bố đã kiểm đủ năm.

## R4-02 — P3 — tổng 158 không bảo vệ đủ 128 giá trị ASCII

Lớp `nghiem-thu-khong-co-lap-chot-dich`; SPEC §2.1.1. Vị trí `ops/land_evidence_nguon_test.py:914`, `:924–928`, `c39`.

```python
vu_tru = [*map(chr, range(128)), ...]
# thành (neo/thay đầy đủ trong domain-review4.json)
vu_tru = [chr(0x81), *map(chr, range(1, 128)), ...]
```

Mất U+0000, thêm U+0081, vẫn 158 giá trị khác nhau và 648 ô. `c37`, `c39`, `c40` đều rc 0. Biến thể mất DEL U+007F (`range(127)` rồi U+0081) cũng làm `c37/c39` rc 0. Controls nguyên vẹn cùng đường xanh. Chốt chỉ kiểm category ở `vu_tru[128:]`, không kiểm danh tính 128 phần tử đầu. Các phép range±1/cắt trong bảng hiện tại đổi cả cardinality nên chưa cô lập nghĩa vụ này.

Đây là **mất giá trị miền bắt buộc**, khác thay một ô cấu trúc bằng ô mới được §8 loại khỏi phạm vi. Nếu miễn: bốn ô tương ứng NUL hoặc DEL tại các vị trí văn bản tự do biến mất mà chốt vẫn nhận đủ miền và đủ 648 ô.

Phép đóng: kiểm tập ASCII là chính xác U+0000…U+007F trước vòng ô; thêm phản chứng thay NUL/DEL bằng ký tự ngoài ASCII mà giữ cardinality/uniqueness, đòi rc 3 `DO:c37:` và 0 ô, bản nguyên vẹn rc 0/648 ô. Ước **8–14 dòng thêm**. Rủi ro sửa: không vô tình đòi thứ tự ASCII nếu SPEC chỉ đòi tập; đảm bảo guard mới cũng có phản chứng gỡ riêng.

Lệnh tái lập chung (clone tạm mới mỗi lần, chỉ dưới work/):

```bash
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/../work/tmp" python3 -B ../work/repro_R4.py
```

Đã chạy rc 0 của script; tám kết quả con (bốn controls, bốn mutant) đều rc 0. `domain_review4.py` đo thêm DEL và các mutant ±2/nhánh/aggregation; raw rc/stdout/stderr ở `domain-review4.json` và `repro-R4.json`.
