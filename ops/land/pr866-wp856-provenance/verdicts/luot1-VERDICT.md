Reviewed commit: 7302ea3623ebb7a0250a6c5090985807753cc031
Verdict: changes_requested — P0=0 P1=0 P2=4 P3=0

ĐANG REVIEW — dòng verdict tạm, chưa đủ bằng chứng để approve.

Reviewer: Codex / OpenAI; execution surface: Codex agent với công cụ shell cục bộ; transport: machine/local. Kho `/home/user/rv856` chỉ đọc; phép đo trên bản sao `/tmp`.

Đã kiểm HEAD đúng SHA yêu cầu; working tree sạch; diff base → head: 841 thêm, 7 xoá, đúng `.claude/dev/packet_loop_test.py`.

Đặc tả và phụ lục đã đọc trọn, hash khớp hai giá trị trong prompt; lease r1/g1 đúng write set một tệp. Tree head `ada5bc4bca23d7a1ccab7f8fc1d3b35081343f7f`.

Bằng chứng đang tích luỹ:

- `evidence/t6-coverage.json`: 1062 fixture từ chối trong năm bộ sinh T1–T5 mới; T6 không duyệt 570 fixture (T2, T3, một phần T4), và chúng không có bản sửa. Đây là biểu hiện lớp `fixture-vi-pham-nhieu-chot` / độ phủ tự kiểm T6; đang đo phản chứng gỡ một họ.
- Ma trận runtime có T1=148, T2=252, T3=32, T4=115, T5=23, tổng 570 ô. T2 có 8 vị trí và 10 phép biến đổi × 3 phía + 4 hướng tiền/hậu tố; tối thiểu 272 ô, thiếu 20 ô `dedup` × 10 phép × trái/phải. Ca `kg_t_ma_tran` vẫn xanh vì công thức đếm tự trừ chính 20 ô ấy (dòng 6993–6994).
- `evidence/auxiliary-gates.json`: doctrine-scan base/head rc0 (10 tệp, 0 lỗi); adr-song rc0 (53/53); Ruff 0.15.15 `--no-cache --select F`: base/head đều rc1 do 2 F541, delta F=0.

Gate đầy đủ và phát lại 75 đột biến còn đang chạy; chưa khai đạt A2/A5/A6.

Bốn lớp đã có phép đo độc lập (bảng tạm, sẽ bổ sung đầy đủ trước khi chốt):

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| `so-khop-tuyet-doi-chua-du` | P2 | `.claude/dev/packet_loop_test.py:6555`, `:6562`, `:6994` | 20 ô T2 dedup trái/phải vắng; tự kiểm ma trận vẫn SONG. Các biến thể độc lập đã bắt đầu chạy toàn 411 ca. | Sinh đủ ba phía cho cả dedup, dùng cùng phép so ở hàm tính fixture và mã đột biến; bỏ phép trừ 20 ô trong kiểm đếm. |
| `so-khop-so-nguyen-chua-chinh-xac` | P2 | `.claude/dev/packet_loop_test.py:6590`, `:6593`, `:6630` | Tiền tố đầy đủ `str(run_suite).startswith(str(suite))` ở bộ lọc suite và hai hướng tại cảnh báo: 411/411 SONG. CLI native suite=1, JSON suite=12: rc12→0. | Thêm cặp số có quan hệ tiền tố thực sự, cả âm và dương, hai thứ tự; sinh phép startswith đầy đủ, không chỉ `str(x)[:1]`. |
| `chuan-hoa-doi-so-chi-trong-phep-kiem` | P2 | `.claude/dev/packet_loop_test.py:6700` | Lời khai T5 `bat_buoc/chuan_hoa_nfkc` tương đương sai khi hiện thực toán tử bằng chuẩn hoá đối số trước kiểm. Native run/tên cùng `Ｇate`: rc0→12 VẮNG. | Ghi đột biến thật cho chuẩn hoá đối số, kiểm cả đầu ra/tên và dữ liệu truyền xuống; giữ bổ đề nhưng không suy từ bool sang cả CLI. |
| `fixture-vi-pham-nhieu-chot` | P2 | `.claude/dev/packet_loop_test.py:6910`, `:6937` | Bỏ 570 fixture khỏi T6; gỡ riêng họ `kg_t1_id_null` khỏi `_KG_T6_HO` thì cả `kg_t6_ban_sua` và `kg_t6_co_rang` vẫn SONG. | Lấy tập fixture từ tất cả bộ sinh, cung cấp bản sửa từng chốt, so độ phủ với tập độc lập; thêm đột biến xoá cả họ để khoá lỗ tự kiểm. |

`evidence/contract-measurements.json`, `evidence/priority-*.jsonl`, `evidence/parity.json` là bằng chứng. Bộ chạy ma trận chạy nguyên source entrypoint với argv/stdout/stderr riêng, không gọi hàm sản phẩm; 260/260 lượt đối chiếu native/fork/exec-main khớp (chuẩn hoá địa chỉ bộ nhớ). Full gate và các nhân chứng giết/phản chứng CLI dùng subprocess Python thường.
