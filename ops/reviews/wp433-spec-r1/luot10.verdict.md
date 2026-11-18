## Issue #433 · Review đặc tả lượt 10

Review trên base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`, checkout detached tại OID của `origin/master` cục bộ. Hai đặc tả là tệp chưa được Git theo dõi, nên verdict neo vào SHA-256 của chính từng tệp.

| Packet | SHA-256 của bản r1 |
|---|---|
| 1 · `NLM-GWS-DICH-NGOAI-KHO` | `2b6b72601b6e205ef33e6e9bdbb438a9e26e4c97a89c5808c5b34ed0e7bda3fb` |
| 2 · `GWS-CRED-DICH-NGOAI-KHO` | `26fb25bf750255c002b5e14d16718a4c66b116349c5a68e529d89bff3d5f9b72` |

### Finding lượt 9

| Mức · Packet | Finding | Trạng thái lượt 10 |
|---|---|---|
| P2 · 1 | Tập ngoại lệ khai theo ca | **Đóng.** §4b tra tập theo lượt và chấm đúng bộ ba `(ca, lượt, nhãn)`. Mô phỏng trong RAM xác nhận đổi lượt đích hoặc chuyển khai báo sang sai lượt đều mất tín dụng. Kiểm tương tự cho `W6.token` và `W6.encode` của packet 2. |
| P2 · 1 | Đột biến gộp chốt W1/W3 | **Chưa đóng hết.** Dòng 4–5 đo riêng việc bỏ kiểm đích bằng jar hợp lệ. Dòng 1–2 vẫn quay về vòng ghi base và bỏ cả hai chốt. Chưa có đột biến riêng bỏ lời gọi kiểm jar ở từng caller, giữ kiểm đích và writer nguyên tử. Dùng một khoá một thành phần ngoài allowlist để tách phép đo mà vẫn giữ tiền điều kiện của M1. [§4b, dòng 1–5](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#4b-bảng-đột-biến--nguồn-duy-nhất-thắng-mọi-mô-tả-đột-biến-rải-trong-4) |
| P2 · 2 | `reparse_w1` đi qua tiền tố gắn bit | **Đóng.** N3c dùng `profiles/default/cookies.json`. Duyệt tiền tố trong RAM đi qua `profiles/default` với khoá này. Đối chứng chỉ có `auth.json` không đi qua. |
| P3 · 1 | Fixture list rỗng | **Đóng.** `[1]` qua cổng truthy và `[1].items()` phát đúng `AttributeError` đã khai. |
| P3 · 2 | `ntpath.isabs` khác phiên bản | **Đóng với ba dạng của N2w.** Mô phỏng cả hai kết quả `isabs` cho thấy `\fake` và `D:fake` đều bị chặn trước, còn `D:\fake` đi qua. Gốc UNC có finding riêng bên dưới. |

### Finding mới

- **P2 · Packet 2 · M1 từ chối gốc UNC hợp lệ.** M1 khai hỗ trợ UNC nhưng bước (ii) từ chối mọi đường có ổ mà phần sau ổ không bắt đầu bằng dấu phân cách. Đo bằng `ntpath` trên Python 3.13.18 với `\\server\share`: `splitdrive` trả `(ổ UNC, "")`, `isabs` trả `True`, còn áp thứ tự của M1 trả từ chối. N2w chưa đo gốc UNC. Cần phân biệt gốc share với đường tương đối theo ổ và thêm vế dương cho gốc share. [M1](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:86)
- **P2 · Packet 2 · Đột biến W6 dòng 25 phụ thuộc bộ mã hoá môi trường.** N9w6 chỉ yêu cầu token chứa surrogate, còn dòng 25 khai cơ chế E cố định tại phép gán env. Trên POSIX đã đo `os.fsencode('\udc80') == b'\x80'`, nên fixture này hợp lệ theo N9w6 và qua được bộ mã hoá env. Lỗi xuất hiện ở tuần tự hoá và bị M7(c) bắt. Nhánh Windows của `os._createenviron` cũng dùng giá trị `str` trực tiếp qua bộ mã hoá Python, chưa đo native. Chốt fixture và dùng bộ gán giả có lỗi xác định, hoặc khai và đo hậu điều H cho nhánh phép gán thành công. [N9w6 và §4b dòng 25](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:156)
- **P3 · Packet 1 · M4 còn viện dẫn phần W6 đã chuyển.** M4 hứa “Không ngoại lệ thoát ra” cho nhóm có W6 và viện dẫn `M3(0b)`. §2 và M3 hiện hành cho phép ngoại lệ dữ liệu W6 như base. Giới hạn câu trong M4 vào phạm vi lỗi packet 1 xử lý và bỏ tham chiếu `M3(0b)` đã mất. [M4](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:248)
- **P3 · Packet 2 · M3 còn khai tập theo ca, và năm dòng W6 nằm ngoài bảng Markdown.** M3 ghi “Tập khai của mỗi ca”, trong khi §4b áp tập theo lượt. Dòng trống giữa mục 24 và 25 kết thúc bảng, khiến 25–29 mất hàng tiêu đề khi render. Đồng bộ M3 với §4b và nối năm dòng vào bảng. [M3](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:88) · [Cuối bảng](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:154)
- **P3 · Packet 2 · Ước lượng ghi thiếu một lượt W6.** N9w6 liệt kê sáu lượt `token`, `encode`, `dict_a`, `dict_b`, `dict_c`, `nul`. §8 tính “năm lượt”. Rà lại số hạng fragment vì biên dự kiến chỉ còn bốn dòng. [§8](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:204)

### W6, L1–L7 và luật dừng

- **W6, L2–L3.** Packet 1 giữ kiểm đích trước đọc merge, lọc jar bị từ chối và ghi config nguyên tử. Packet 2 đặt M7 trên cùng đường ghi và nhận đủ năm đột biến dữ liệu. Tham chiếu dư ở M4 và cơ chế dòng 25 là hai điểm cần sửa trong phần chuyển. Đã rà toàn §4b của cả hai packet, gồm 29 đột biến mỗi packet và ba đích của mục 13 packet 2. Các dòng dựa trên lập luận vẫn chờ đo trên mã candidate.
- **L1, L5–L6.** Đếm lại bảng và chạy `python3 -IB` trong RAM trên Linux, rc 0 cho các phép đo nêu trên. Kiểm mô hình numstat với đúng ba đường dẫn mỗi packet: 450 xanh, 451 đỏ, đầu vào rỗng đỏ. Khoảng 365–416 và 374–446 vẫn là ước lượng. Cơ chế bắt ngoại lệ theo lượt và kiểm dòng lỗi cố định có đối chứng trong đặc tả. Gate candidate và Windows native chưa chạy.
- **L4, L7 và trần.** Hai packet dùng chung lịch sử hình dạng lỗi. Số đếm tiền nhiệm và biên nhận của các lượt cũ chưa xác minh độc lập. Hai OID khai ADR-0053/0055 qua phép kiểm Git với `origin/master` cục bộ. Lượt 10 là lượt cuối theo giao việc. Dừng tại **Review Rescue Checkpoint**. Mọi đề nghị tăng trần thuộc E2. Các điều kiện duyệt băm, ngoại lệ bundled và packet 1 land trước khi cấp lease packet 2 vẫn áp dụng.

KET_LUAN: request_changes
tokens used
92,773
## Issue #433 · Review đặc tả lượt 10

Review trên base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`, checkout detached tại OID của `origin/master` cục bộ. Hai đặc tả là tệp chưa được Git theo dõi, nên verdict neo vào SHA-256 của chính từng tệp.

| Packet | SHA-256 của bản r1 |
|---|---|
| 1 · `NLM-GWS-DICH-NGOAI-KHO` | `2b6b72601b6e205ef33e6e9bdbb438a9e26e4c97a89c5808c5b34ed0e7bda3fb` |
| 2 · `GWS-CRED-DICH-NGOAI-KHO` | `26fb25bf750255c002b5e14d16718a4c66b116349c5a68e529d89bff3d5f9b72` |

### Finding lượt 9

| Mức · Packet | Finding | Trạng thái lượt 10 |
|---|---|---|
| P2 · 1 | Tập ngoại lệ khai theo ca | **Đóng.** §4b tra tập theo lượt và chấm đúng bộ ba `(ca, lượt, nhãn)`. Mô phỏng trong RAM xác nhận đổi lượt đích hoặc chuyển khai báo sang sai lượt đều mất tín dụng. Kiểm tương tự cho `W6.token` và `W6.encode` của packet 2. |
| P2 · 1 | Đột biến gộp chốt W1/W3 | **Chưa đóng hết.** Dòng 4–5 đo riêng việc bỏ kiểm đích bằng jar hợp lệ. Dòng 1–2 vẫn quay về vòng ghi base và bỏ cả hai chốt. Chưa có đột biến riêng bỏ lời gọi kiểm jar ở từng caller, giữ kiểm đích và writer nguyên tử. Dùng một khoá một thành phần ngoài allowlist để tách phép đo mà vẫn giữ tiền điều kiện của M1. [§4b, dòng 1–5](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#4b-bảng-đột-biến--nguồn-duy-nhất-thắng-mọi-mô-tả-đột-biến-rải-trong-4) |
| P2 · 2 | `reparse_w1` đi qua tiền tố gắn bit | **Đóng.** N3c dùng `profiles/default/cookies.json`. Duyệt tiền tố trong RAM đi qua `profiles/default` với khoá này. Đối chứng chỉ có `auth.json` không đi qua. |
| P3 · 1 | Fixture list rỗng | **Đóng.** `[1]` qua cổng truthy và `[1].items()` phát đúng `AttributeError` đã khai. |
| P3 · 2 | `ntpath.isabs` khác phiên bản | **Đóng với ba dạng của N2w.** Mô phỏng cả hai kết quả `isabs` cho thấy `\fake` và `D:fake` đều bị chặn trước, còn `D:\fake` đi qua. Gốc UNC có finding riêng bên dưới. |

### Finding mới

- **P2 · Packet 2 · M1 từ chối gốc UNC hợp lệ.** M1 khai hỗ trợ UNC nhưng bước (ii) từ chối mọi đường có ổ mà phần sau ổ không bắt đầu bằng dấu phân cách. Đo bằng `ntpath` trên Python 3.13.18 với `\\server\share`: `splitdrive` trả `(ổ UNC, "")`, `isabs` trả `True`, còn áp thứ tự của M1 trả từ chối. N2w chưa đo gốc UNC. Cần phân biệt gốc share với đường tương đối theo ổ và thêm vế dương cho gốc share. [M1](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:86)
- **P2 · Packet 2 · Đột biến W6 dòng 25 phụ thuộc bộ mã hoá môi trường.** N9w6 chỉ yêu cầu token chứa surrogate, còn dòng 25 khai cơ chế E cố định tại phép gán env. Trên POSIX đã đo `os.fsencode('\udc80') == b'\x80'`, nên fixture này hợp lệ theo N9w6 và qua được bộ mã hoá env. Lỗi xuất hiện ở tuần tự hoá và bị M7(c) bắt. Nhánh Windows của `os._createenviron` cũng dùng giá trị `str` trực tiếp qua bộ mã hoá Python, chưa đo native. Chốt fixture và dùng bộ gán giả có lỗi xác định, hoặc khai và đo hậu điều H cho nhánh phép gán thành công. [N9w6 và §4b dòng 25](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:156)
- **P3 · Packet 1 · M4 còn viện dẫn phần W6 đã chuyển.** M4 hứa “Không ngoại lệ thoát ra” cho nhóm có W6 và viện dẫn `M3(0b)`. §2 và M3 hiện hành cho phép ngoại lệ dữ liệu W6 như base. Giới hạn câu trong M4 vào phạm vi lỗi packet 1 xử lý và bỏ tham chiếu `M3(0b)` đã mất. [M4](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:248)
- **P3 · Packet 2 · M3 còn khai tập theo ca, và năm dòng W6 nằm ngoài bảng Markdown.** M3 ghi “Tập khai của mỗi ca”, trong khi §4b áp tập theo lượt. Dòng trống giữa mục 24 và 25 kết thúc bảng, khiến 25–29 mất hàng tiêu đề khi render. Đồng bộ M3 với §4b và nối năm dòng vào bảng. [M3](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:88) · [Cuối bảng](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:154)
- **P3 · Packet 2 · Ước lượng ghi thiếu một lượt W6.** N9w6 liệt kê sáu lượt `token`, `encode`, `dict_a`, `dict_b`, `dict_c`, `nul`. §8 tính “năm lượt”. Rà lại số hạng fragment vì biên dự kiến chỉ còn bốn dòng. [§8](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:204)

### W6, L1–L7 và luật dừng

- **W6, L2–L3.** Packet 1 giữ kiểm đích trước đọc merge, lọc jar bị từ chối và ghi config nguyên tử. Packet 2 đặt M7 trên cùng đường ghi và nhận đủ năm đột biến dữ liệu. Tham chiếu dư ở M4 và cơ chế dòng 25 là hai điểm cần sửa trong phần chuyển. Đã rà toàn §4b của cả hai packet, gồm 29 đột biến mỗi packet và ba đích của mục 13 packet 2. Các dòng dựa trên lập luận vẫn chờ đo trên mã candidate.
- **L1, L5–L6.** Đếm lại bảng và chạy `python3 -IB` trong RAM trên Linux, rc 0 cho các phép đo nêu trên. Kiểm mô hình numstat với đúng ba đường dẫn mỗi packet: 450 xanh, 451 đỏ, đầu vào rỗng đỏ. Khoảng 365–416 và 374–446 vẫn là ước lượng. Cơ chế bắt ngoại lệ theo lượt và kiểm dòng lỗi cố định có đối chứng trong đặc tả. Gate candidate và Windows native chưa chạy.
- **L4, L7 và trần.** Hai packet dùng chung lịch sử hình dạng lỗi. Số đếm tiền nhiệm và biên nhận của các lượt cũ chưa xác minh độc lập. Hai OID khai ADR-0053/0055 qua phép kiểm Git với `origin/master` cục bộ. Lượt 10 là lượt cuối theo giao việc. Dừng tại **Review Rescue Checkpoint**. Mọi đề nghị tăng trần thuộc E2. Các điều kiện duyệt băm, ngoại lệ bundled và packet 1 land trước khi cấp lease packet 2 vẫn áp dụng.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T06:59:30Z
