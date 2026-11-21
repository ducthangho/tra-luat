Review offline MÃ wp1236 đợt A, r10, lượt 8: **changes_requested** — 2 P2 và 1 P3 còn mở, thuộc 2 lớp.

HEAD `5a1bf33831bb4e3a227cfb25843cef8a922c634b`  
Tree `19fe7bd12a8a2e038a11ec230efb706be5756caa`  
Spec SHA-256 `3ee831738c70c5eabb27720e295b4953c9a9bdd1ac29a03cc7b964d28658fcdc`

| Finding | Mức | Lớp giữ nguyên | Kết quả đo |
|---|---|---|---|
| N01 | P2 | `test-thieu-chot` | 11/14 đột biến độc lập không tương đương sống 42/42 ca; thiếu miền/consumer và hai thuộc tính portable bị bỏ qua Windows. |
| N02 | P3 | `test-thieu-chot` | M03 chưa vá: ledger dòng 32/88 vẫn kết thúc sai luật 5. |
| N03 | P2 | `hop-dong-dau-vao-dau-ra-chua-chot` | Nhánh Windows in rc0/TONG DAT nhưng consumer đăng ký trả rc1 vì định dạng không khớp. |

M01 có đổi phương pháp thật: bảng dùng chung chạy hàm lá và consumer, 14 mutant lượt 7 nay đều chết. Nhưng bảng chưa liệt kê đủ ngữ cảnh so sánh: `conclusion == skipped`, `checkout.trang_thai == skipped`, tên check bắt buộc và OS token. Họ NFC/NFKC cũng chưa được khóa. Đối chứng của 11 mutant sống đã được chạy trên HEAD và bản đột biến; HEAD xử lý đúng, bản đột biến cho kết quả khác. Đây là thiếu bảo vệ hồi quy, không phải nói HEAD đang có lỗi giả lập ấy. `a120` vẫn 34 lần gọi hàm lá/0 consumer; `a121` và `a122` mỗi ca chỉ một consumer. Chi tiết trong [inventory](comparison_coverage.json), [kết quả quét](independent_results.jsonl), [đối chứng](independent_contrasts.json) và [tuyến gọi](matrix_routes.json).

Các phép prefix/suffix/substring trên schema bị bảng hiện tại bắt; tên check bắt buộc và OS membership còn biến thể sống. Cần viết bảng theo từng điểm so và nhánh, dùng cùng hàng qua helper/consumer, giữ đối chứng hợp lệ và kiểm đột biến đúng tín hiệu. Lớp `test-thieu-chot` đã lặp từ các lượt 1–8: đưa bằng chứng về checkpoint xét lại phương pháp, không tiếp tục vá riêng từng ví dụ.

`a117` đổi `con` thành `conx` phù hợp quy tắc tên Windows, vẫn bắt PermissionError ở phép đo Linux. `a204` tách nhánh giúp m22 bị giết cả khi chọn nhánh nt. `CHI_POSIX` không làm yếu POSIX trong phép đo: 146 mutant chạy, tên lạ làm đỏ. Nhánh nt khai 11 bỏ qua, mẫu số 135; mutant sống ngoài tập bỏ qua cũng làm đỏ. Tuy nhiên m65 (stat OSError) và m79 (đường tuyệt đối) đo được bằng seam độc lập OS, nên không nên mất bảo vệ này trên Windows. Đã chạy đối chứng cho cả hai trong [portable probes](portable_property_probes.json). [Kiểm nhánh bỏ qua](skip_controls.json) cho thấy mẫu số 0 làm đỏ, nhưng m65/m79 hiện không được chạy và `TONG DAT` vẫn có thể xuất hiện trong mô phỏng dù gán kết quả sống cho chúng. Vì vậy tổng xanh ấy không chứng minh hai thuộc tính này trên Windows.

N03 được đo bằng chính `main` với nhánh nt và kết quả ca được điều khiển, rồi đưa stdout vào `chay_moi` thật: producer rc0, consumer rc1. Nhánh POSIX là đối chứng rc0. Các dòng `BO QUA` chen giữa `CA` và `DOT BIEN`, cộng hậu tố `(bo qua 11 chi POSIX)`, phá regex đã đăng ký. Giữ khai báo bỏ qua ngoài khối tổng kết liên tiếp và kiểm producer–consumer. Đây là phép đo hợp đồng trên Linux; **chưa chạy Windows thật**. Xem [kết quả](windows_output_contract.json).

| Đối chiếu lượt 7/lịch sử | Nhãn trên HEAD |
|---|---|
| M01 `test-thieu-chot` | `VA_MOT_PHAN`: 14 r7 đã GIET, còn N01. |
| M03 `test-thieu-chot` | `CHUA_VA`: còn N02. |
| M02 lỗi argparse | `DA_VA_THAT`: 5 nhánh lỗi rc2/prefix đúng, help rc0, m146 GIET. Lớp đầu ra vẫn `VA_MOT_PHAN` vì N03 mới sinh. |
| `yaml-ngoai-schema-bi-chan` (F01) | `DA_VA_THAT`: 5 kiểu YAML ngoài schema nhận đúng, chốt có phản chứng. |
| `k2-mat-loi-doc` (F02/G01) | `DA_VA_THAT`: YAML/UTF8/symlink/duyệt lỗi giữ lý do. |
| `cli-vong-yaml-traceback` (F03/H02) | `DA_VA_THAT`: vòng bị chặn, alias dùng chung hợp lệ; stat lỗi rc2. |
| `mo-ta-duong-dan-lech-hop-dong` (L03) | `DA_VA_THAT`: docstring và hành vi `./tệp` khớp. |

Hội tụ lớp 7→8 = **0/2**; M02 riêng đóng nhưng lớp có N03 nên không vào tử số. Waiver tại `79b3c24` không áp dụng HEAD này.

Ledger 141 ID: tự đo lại 129/129 GIET đúng ca, trong đó 14/14 r7; kiểm miền kiểu và đối chứng cho 7 TUONG_DUONG; 3/5 KHONG_AP_DUNG có thay thế cùng nghĩa GIET. Hai mục còn lại nên phân loại TUONG_DUONG với chứng minh hiện hành; việc bỏ lookbehind khỏi implementation không có nghĩa bỏ chốt khỏi đặc tả. Xem [ledger đo lại](ledger_remeasure.jsonl), [12 mục cần xét nghĩa](ledger_tail.json).

Quét riêng hoàn tất: baseline 42/42, 14×42 ca, 11 sống không tương đương, 3 GIET, 0 lỗi chạy/vô can; không dùng bộ quét executor, không cache hay đổi YAML loader. [Kho mới](kho_dot_bien_reviewer_luot8.jsonl) có 11 cặp `ast.unparse` neo duy nhất, băm `7a2f7c411e361f136904703c2ed246285872bb0c9abba9fbb4ff1e05019200b6`; [kho cộng dồn](kho_dot_bien_reviewer_luot6_7_8.jsonl) có 152 ID.

| Kiểm bắt buộc | Kết quả |
|---|---|
| `python3 -B ops/gate_output_doi_chieu_test.py` | rc0: CA42/42, DOT BIEN146/146, TU KIEM DAT(2), TONG DAT |
| Ruff `--no-cache --select F`, ba tệp | rc0, Ruff0.15.15 |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | rc0: đăng ký31/31, hợp đồng Ruff3/3, phản chứng1226/1226 |
| `git diff --numstat 010046f… HEAD` | rc0:3 tệp,+1592/-0≤1700 |
| `git diff --check 010046f… HEAD` | rc0 |
| Windows local/CI, remote CI, LIVE | `not_run`; không tính là đạt |

Reviewer `openai_codex / codex_cli / machine`, session `01a1fc41-952e-7250-a25f-144dbc753b16`; model/effort phục vụ `KHONG_DO_DUOC`. Môi trường Linux, Python 3.13.18, PyYAML 6.0.3. Bằng chứng lệnh, mã thoát thật và băm stdout nằm trong `*.receipt.json` và `VERDICT.json`. Snapshot 17339 tệp tracked/untracked/ignored đầu–cuối không đổi; HEAD/tree giữ nguyên. Repo được giữ chỉ đọc bằng thao tác trong sandbox workspace-write; snapshot không chứng minh toàn bộ lịch sử ghi giữa hai mốc. Không mạng/GitHub/commit/push; mọi hiện vật ở `work/`.

Validator `kiem_verdict_lop.py --vong 8`: rc0, `HOP_LE (§8.3): 3 finding, 6 lop`; lưu tại [kiem_verdict.txt](kiem_verdict.txt).

KET_LUAN: changes_requested
