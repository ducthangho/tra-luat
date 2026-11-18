# Review lượt 2 — Issue #387

Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout ở detached HEAD, cùng OID với `master` và `origin/master` cục bộ. Bản đặc tả đang review là tệp ngoài Git, SHA-256 `eccb0d343b7c7c5b20739c0579602b224ab9cfe53e35645df44ecf9b94b6c0fa`. Reviewer thuộc họ OpenAI, làm việc qua phiên Codex với shell chỉ đọc. Không có truy cập mạng hoặc thay đổi worktree.

## Finding lượt 1

| Finding | Trạng thái | Đối chiếu |
|---|---|---|
| P1 — Hạn chờ, Darwin `ps`, Windows | Chưa đóng hết | M2 dùng deadline chung, chuyển phần thời gian còn lại tới `ps` và dò trực tiếp `_pid_trong_job`, tránh vòng 20 lần ở `_cay_da_chet`. M2 vẫn cho phép nhận `[]` từ một lần dò đã vượt hạn. |
| P1 — Cạnh tranh với `stop` | Đóng | M2 đặt cả lời gọi đợi trước `_doc_so` ở dòng 2957. Ca (f) và đột biến dời cả lời gọi kiểm đúng trường hợp `stop` ghi xong trong khoảng đợi mới. |
| P1 — Fixture Windows | Chưa đóng hết | Dấu `job-da-gan` và kiểm PID cháu trong đúng job xử lý khe gán sau `Popen` ở dòng 882–886. Các ca dùng con `pass` vẫn có thể thoát trước khi gán job dù M4 bắt buộc `job_windows is True`. |
| P2 — Phạm vi `true` | Đóng | M1 và §8 giới hạn lời khai vào nhóm POSIX hoặc job Windows đã dò. Chúng nêu rõ `setsid`, breakaway và cháu sinh trước khi gán job. |
| P2 — Hợp đồng thời lượng | Đóng | `ket_thuc` được lấy trước vòng đợi và vẫn dùng để tính `thoi_luong_giay`. Thời gian đợi có trường monotonic riêng. |
| P2 — Đối chứng ghi sớm | Đóng | Ca (a′) buộc cháu ghi xong trước khi wrapper thoát, rồi đòi đúng `TinHieuChotCa` ở vế băm. N1 còn yêu cầu bỏ vế băm để kiểm đối chứng chuyển đỏ. |
| P2 — Bảo toàn prompt Windows | Đóng | M1 giữ điều kiện Windows độc lập với job rỗng. Ca (g) và đột biến Windows kiểm trực tiếp hành vi này. `t71` và `t77` đo được trên Windows. |
| P3 — Công bố bằng chứng | Chưa đóng hết | N1–N6 đã yêu cầu lệnh, phiên bản, rc và đầu ra cụ thể. Một số phép đo §0 vẫn dùng giờ dạng `05:2xZ`, và phần tóm tắt runner gộp phép đo tay của đột biến Ctrl-C với kết quả runner. |

## Finding lượt 2

- **P1 — Fixture Windows cần giữ con sống tới khi gán job ở mọi ca có yêu cầu `job_windows is True`.** M4 chỉ mô tả rõ bắt tay cho con sinh cháu, trong khi (d), (f), (g) chỉ định `pass`. `_job_windows` gọi `OpenProcess` và `AssignProcessToJobObject` sau `Popen`, nên các ca này có thể đỏ theo lịch chạy của máy. Áp bắt tay cho cả con không sinh cháu. Sau dấu, con mới thực hiện thân ca và thoát. Giữ N5 chạy native trên máy chủ kho.
- **P2 — Kết quả dò trả sau deadline vẫn có thể thành `true`.** M2 kiểm thời gian trước khi dò rồi chấp nhận `[]` ngay. Quét `/proc` và query job là lời gọi đồng bộ, còn timeout truyền cho Darwin `ps` không tự đo trọn thời gian của helper. Chốt rõ giới hạn thời gian của lời gọi đồng bộ, kiểm lại deadline sau khi dò và thêm ca stub trả `[]` sau hạn. Ca (e) hiện luôn trả `[7]` nên bỏ lọt trường hợp này. Ca đó cũng vá `_thanh_vien_nhom` ở đầu vào, vì vậy đột biến giữ `timeout=15` bên trong lời gọi `subprocess.run` vẫn có thể sống.
- **P2 — Ctrl-C cần giữ mã thật của con và xác định thứ tự ưu tiên với kết quả chụp.** `ngat_khi_chup` ở dòng 2967–2971 chuyển trạng thái thành `bi_ngat` và trả 130 qua `ma`, còn `run.json["ma_thoat"]` lấy `ma_that`. M2 nói “mã 130” và ca (h) chỉ kiểm `rc`, nên có thể ghi nhầm 130 vào sổ mà vẫn xanh. Ngoài ra, vòng đợi mới chạy sau khi đã tính `kq_chup`. Nếu cờ ngắt được xử lý trước khối áp dụng `kq_chup`, Ctrl-C có thể che kết quả `ghi_workspace` hoặc `khong_do_duoc_workspace` vốn đã xác định. Áp kết quả chụp trước khi xét cờ ngắt mới, và kiểm cả mã trong sổ, lý do ngắt, cùng trường hợp giữ trạng thái đã xác định.
- **P2 — Hai cách chạy N5 đang đòi bằng chứng khác nhau.** Cách chạy toàn bộ yêu cầu đọc cả hai neo M5. Cách chạy tay chỉ áp M6. Neo `xoa_prompt_khi_wrapper_vua_thoat` nhắm `t76`, vốn tự bỏ qua trên Windows ở dòng 1760. N5 cần ghi rõ `KHONG DO DUOC` là kết quả dự kiến của neo này trên Windows, giữ bằng chứng giết `t76` ở N4 và thống nhất danh sách phải đo cho cả hai cách chạy native.
- **P3 — §6 tự đặt mốc dừng trên 400 dòng trước khi xong M4.** ADR-0053 đặt trần 450 dòng thêm. Dùng 400 làm mốc rà dự toán hoặc dẫn thẩm quyền cho điểm dừng bổ sung. §8 cũng ghi “hai đột biến” cho phương án tách B nhưng liệt kê ba tên.

## Neo, kích thước và L1–L7

- **Neo.** Phép đếm theo logic `t117` trên `git archive HEAD` trong bộ nhớ kiểm 550 mục, không có sai lệch so với số lần khớp kỳ vọng, gồm ngoại lệ đã biết khớp hai lần. Thử trong bộ nhớ đổi chữ ký, timeout và dòng quyết định xóa prompt làm đúng hai neo M5 mất chỗ khớp. Chữ ký có mặc định giữ các lời gọi một đối số và stub hiện hữu tương thích, với điều kiện nhánh truyền `han_giay` chỉ chạy trên Darwin và stub của ca mới nhận đối số đó. Mười một neo mới cần kiểm trên mã thi hành.
- **Kích thước.** Phép cộng `45–75 + 230–320 = 275–395` đúng, còn 55 dòng ở đầu trên so với trần 450. Số thử `44 + 232 = 276` do §0 báo nằm trong khoảng dự toán. Hai tệp phù hợp write set. Gate quyết định vẫn là tổng cột thêm từ `git diff --numstat` trên head thi hành.
- **L1–L7.** L1 cần sửa số đếm ở phương án tách B. L2 đạt. L3 còn thiếu phép đỏ cho lần dò hoàn thành quá hạn, dây truyền timeout thật và ưu tiên khi Ctrl-C. L4 dùng `khong_ap_dung` phù hợp cho tính năng bổ sung. L5 cần hoàn chỉnh mốc đo và tách kết quả runner khỏi phép đo tay. L6 đạt trên base theo phép đếm neo, cần chạy lại trên head thi hành. L7 cần xử lý điểm dừng 400 dòng.

**Bằng chứng độc lập:** Linux, Python 3.13.18, ngày 2026-11-18 UTC. `git diff --no-index --numstat` từ bản 1 sang bản sửa cho `114` dòng thêm, `90` dòng bớt, rc `1` vì có khác biệt. Phép đếm `python -B` trên `git archive HEAD` trả rc `0`. `mktemp -d /tmp/r387-review.XXXXXX` trả rc `1` do filesystem chỉ đọc. `--lap-ca`, suite đầy đủ và phép đo native đều `not_run` trong phiên này. Số chạy thử ở §0 là bằng chứng do đặc tả báo cáo.

KET_LUAN: request_changes
tokens used
71,597
# Review lượt 2 — Issue #387

Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout ở detached HEAD, cùng OID với `master` và `origin/master` cục bộ. Bản đặc tả đang review là tệp ngoài Git, SHA-256 `eccb0d343b7c7c5b20739c0579602b224ab9cfe53e35645df44ecf9b94b6c0fa`. Reviewer thuộc họ OpenAI, làm việc qua phiên Codex với shell chỉ đọc. Không có truy cập mạng hoặc thay đổi worktree.

## Finding lượt 1

| Finding | Trạng thái | Đối chiếu |
|---|---|---|
| P1 — Hạn chờ, Darwin `ps`, Windows | Chưa đóng hết | M2 dùng deadline chung, chuyển phần thời gian còn lại tới `ps` và dò trực tiếp `_pid_trong_job`, tránh vòng 20 lần ở `_cay_da_chet`. M2 vẫn cho phép nhận `[]` từ một lần dò đã vượt hạn. |
| P1 — Cạnh tranh với `stop` | Đóng | M2 đặt cả lời gọi đợi trước `_doc_so` ở dòng 2957. Ca (f) và đột biến dời cả lời gọi kiểm đúng trường hợp `stop` ghi xong trong khoảng đợi mới. |
| P1 — Fixture Windows | Chưa đóng hết | Dấu `job-da-gan` và kiểm PID cháu trong đúng job xử lý khe gán sau `Popen` ở dòng 882–886. Các ca dùng con `pass` vẫn có thể thoát trước khi gán job dù M4 bắt buộc `job_windows is True`. |
| P2 — Phạm vi `true` | Đóng | M1 và §8 giới hạn lời khai vào nhóm POSIX hoặc job Windows đã dò. Chúng nêu rõ `setsid`, breakaway và cháu sinh trước khi gán job. |
| P2 — Hợp đồng thời lượng | Đóng | `ket_thuc` được lấy trước vòng đợi và vẫn dùng để tính `thoi_luong_giay`. Thời gian đợi có trường monotonic riêng. |
| P2 — Đối chứng ghi sớm | Đóng | Ca (a′) buộc cháu ghi xong trước khi wrapper thoát, rồi đòi đúng `TinHieuChotCa` ở vế băm. N1 còn yêu cầu bỏ vế băm để kiểm đối chứng chuyển đỏ. |
| P2 — Bảo toàn prompt Windows | Đóng | M1 giữ điều kiện Windows độc lập với job rỗng. Ca (g) và đột biến Windows kiểm trực tiếp hành vi này. `t71` và `t77` đo được trên Windows. |
| P3 — Công bố bằng chứng | Chưa đóng hết | N1–N6 đã yêu cầu lệnh, phiên bản, rc và đầu ra cụ thể. Một số phép đo §0 vẫn dùng giờ dạng `05:2xZ`, và phần tóm tắt runner gộp phép đo tay của đột biến Ctrl-C với kết quả runner. |

## Finding lượt 2

- **P1 — Fixture Windows cần giữ con sống tới khi gán job ở mọi ca có yêu cầu `job_windows is True`.** M4 chỉ mô tả rõ bắt tay cho con sinh cháu, trong khi (d), (f), (g) chỉ định `pass`. `_job_windows` gọi `OpenProcess` và `AssignProcessToJobObject` sau `Popen`, nên các ca này có thể đỏ theo lịch chạy của máy. Áp bắt tay cho cả con không sinh cháu. Sau dấu, con mới thực hiện thân ca và thoát. Giữ N5 chạy native trên máy chủ kho.
- **P2 — Kết quả dò trả sau deadline vẫn có thể thành `true`.** M2 kiểm thời gian trước khi dò rồi chấp nhận `[]` ngay. Quét `/proc` và query job là lời gọi đồng bộ, còn timeout truyền cho Darwin `ps` không tự đo trọn thời gian của helper. Chốt rõ giới hạn thời gian của lời gọi đồng bộ, kiểm lại deadline sau khi dò và thêm ca stub trả `[]` sau hạn. Ca (e) hiện luôn trả `[7]` nên bỏ lọt trường hợp này. Ca đó cũng vá `_thanh_vien_nhom` ở đầu vào, vì vậy đột biến giữ `timeout=15` bên trong lời gọi `subprocess.run` vẫn có thể sống.
- **P2 — Ctrl-C cần giữ mã thật của con và xác định thứ tự ưu tiên với kết quả chụp.** `ngat_khi_chup` ở dòng 2967–2971 chuyển trạng thái thành `bi_ngat` và trả 130 qua `ma`, còn `run.json["ma_thoat"]` lấy `ma_that`. M2 nói “mã 130” và ca (h) chỉ kiểm `rc`, nên có thể ghi nhầm 130 vào sổ mà vẫn xanh. Ngoài ra, vòng đợi mới chạy sau khi đã tính `kq_chup`. Nếu cờ ngắt được xử lý trước khối áp dụng `kq_chup`, Ctrl-C có thể che kết quả `ghi_workspace` hoặc `khong_do_duoc_workspace` vốn đã xác định. Áp kết quả chụp trước khi xét cờ ngắt mới, và kiểm cả mã trong sổ, lý do ngắt, cùng trường hợp giữ trạng thái đã xác định.
- **P2 — Hai cách chạy N5 đang đòi bằng chứng khác nhau.** Cách chạy toàn bộ yêu cầu đọc cả hai neo M5. Cách chạy tay chỉ áp M6. Neo `xoa_prompt_khi_wrapper_vua_thoat` nhắm `t76`, vốn tự bỏ qua trên Windows ở dòng 1760. N5 cần ghi rõ `KHONG DO DUOC` là kết quả dự kiến của neo này trên Windows, giữ bằng chứng giết `t76` ở N4 và thống nhất danh sách phải đo cho cả hai cách chạy native.
- **P3 — §6 tự đặt mốc dừng trên 400 dòng trước khi xong M4.** ADR-0053 đặt trần 450 dòng thêm. Dùng 400 làm mốc rà dự toán hoặc dẫn thẩm quyền cho điểm dừng bổ sung. §8 cũng ghi “hai đột biến” cho phương án tách B nhưng liệt kê ba tên.

## Neo, kích thước và L1–L7

- **Neo.** Phép đếm theo logic `t117` trên `git archive HEAD` trong bộ nhớ kiểm 550 mục, không có sai lệch so với số lần khớp kỳ vọng, gồm ngoại lệ đã biết khớp hai lần. Thử trong bộ nhớ đổi chữ ký, timeout và dòng quyết định xóa prompt làm đúng hai neo M5 mất chỗ khớp. Chữ ký có mặc định giữ các lời gọi một đối số và stub hiện hữu tương thích, với điều kiện nhánh truyền `han_giay` chỉ chạy trên Darwin và stub của ca mới nhận đối số đó. Mười một neo mới cần kiểm trên mã thi hành.
- **Kích thước.** Phép cộng `45–75 + 230–320 = 275–395` đúng, còn 55 dòng ở đầu trên so với trần 450. Số thử `44 + 232 = 276` do §0 báo nằm trong khoảng dự toán. Hai tệp phù hợp write set. Gate quyết định vẫn là tổng cột thêm từ `git diff --numstat` trên head thi hành.
- **L1–L7.** L1 cần sửa số đếm ở phương án tách B. L2 đạt. L3 còn thiếu phép đỏ cho lần dò hoàn thành quá hạn, dây truyền timeout thật và ưu tiên khi Ctrl-C. L4 dùng `khong_ap_dung` phù hợp cho tính năng bổ sung. L5 cần hoàn chỉnh mốc đo và tách kết quả runner khỏi phép đo tay. L6 đạt trên base theo phép đếm neo, cần chạy lại trên head thi hành. L7 cần xử lý điểm dừng 400 dòng.

**Bằng chứng độc lập:** Linux, Python 3.13.18, ngày 2026-11-18 UTC. `git diff --no-index --numstat` từ bản 1 sang bản sửa cho `114` dòng thêm, `90` dòng bớt, rc `1` vì có khác biệt. Phép đếm `python -B` trên `git archive HEAD` trả rc `0`. `mktemp -d /tmp/r387-review.XXXXXX` trả rc `1` do filesystem chỉ đọc. `--lap-ca`, suite đầy đủ và phép đo native đều `not_run` trong phiên này. Số chạy thử ở §0 là bằng chứng do đặc tả báo cáo.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T05:31:37Z
