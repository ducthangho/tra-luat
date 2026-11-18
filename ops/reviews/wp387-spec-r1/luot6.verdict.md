Review độc lập lượt 6 cho đặc tả Packet A, Issue #387. Base đối chiếu `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. SHA-256 đặc tả A `85cd970f908703f3f8aba94c2aaec16d4d0a7f1ac53d1e0ecc211de8e5adc7ad`. Phiên `openai_codex / codex_cli / machine`, Linux, Python 3.13.18, sandbox chỉ đọc.

### Finding lượt 5

| Finding | Trạng thái | Căn cứ |
|---|---|---|
| P2 — Bộ ghi kill chuyển tiếp tín hiệu thật | **Đóng** | A M4 dùng hàm giả chỉ ghi nhật ký sau `lenh_run`. B M4 giữ cơ chế này và chỉ bọc `killpg` khi có. Log lịch sử của vá thử A ghi đột biến chèn `os.kill` bị giết đúng ca (a). |
| P2 — Teardown Windows và sót thư mục | **Chuyển hợp lệ sang B** | A bỏ fixture Windows. B M4 nhận phần bắt tay gán Job Object, chờ job rỗng và đóng handle trước khi dọn thư mục. B N5 giữ gate native Windows. Còn một lỗ hổng trong nhánh dọn lỗi, ghi riêng dưới đây. |
| P3 — §9 dẫn sai L1–L7 | **Đóng** | A §9 dẫn đúng `.claude/skills/soan-spec/SKILL.md` §2. |

### Finding mới

- **P2 · A — M2 làm đổi mốc kết thúc trên Darwin.** Base gọi `_bay_gio()` sau `_thanh_vien_nhom(p.pid)` và sau bước xoá prompt. A M2 dời mốc lên trước cả hai. Phép dò Darwin gọi `ps` với `timeout=15`, nên `ket_thuc_utc` và `thoi_luong_giay` có thể giảm cả thời gian dò, trái cam kết ở §2. Windows cũng đổi thứ tự lấy mốc. Giữ vị trí lấy mốc của base trên nền ngoài Linux, rồi thêm phép đo thứ tự này vào N5. [A §2–M2](ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md#2-ngoaiphamvi)
- **P2 · A — Đối chứng base của N1 đỏ trước khi chạy hành vi cần đo.** `_r387_chay` của vá thử đọc `_HAN_CHO_CAY_TRUOC_BAM_LOG` trước `lenh_run`. Hằng đó vắng trong `launcher.py` của base. Tôi đọc base từ `git archive` trong bộ nhớ và tái hiện `AttributeError` ở chính bước này bằng fixture với stub tối thiểu. N1 chỉ đòi dòng `LAP` và rc nên có thể nhận lỗi fixture làm bằng chứng lỗi băm. Cho fixture chạy được với base và yêu cầu `TinHieuChotCa` ở vế mới đã định danh, sau khi đã xác nhận cháu ghi muộn và băm sổ lệch băm đĩa.
- **P3 · A — (e5) bắt được phép dò thừa nhưng bỏ lọt phép chờ thừa.** Đột biến `r387_a_nen_khac_van_do` bị chặn đúng tại `(e5)`. Tuy nhiên, khi chèn `sleep(0.2)` trên nền ngoài Linux trước khi trả `False`, ca (e) vẫn qua. Dùng đồng hồ giả hoặc stub `sleep` làm ca đỏ để kiểm lời hứa “trả ngay”.
- **P2 · B — N5 có thể bỏ lọt thư mục sót sau teardown.** B M4 yêu cầu đóng handle sau khi chờ và vẫn đóng khi hết hạn. Trên đường hết hạn, `CloseHandle` khởi phát kết liễu job nhưng fixture đi ngay tới `San`, nơi `rmtree(..., ignore_errors=True)` nuốt lỗi. Vá thử cũng bỏ qua giá trị trả về của `CloseHandle`. Vì N5 chỉ kiểm kết quả ca và đột biến, một thư mục sót sau bước dọn có thể không được báo. Thêm kiểm tra kết quả đóng handle và kiểm tra thư mục thật sự biến mất, kể cả ở ca ép teardown lỗi.
- **P3 · B — N4 đo sai nền cho phản chứng.** B N4 đếm `BO QUA r387` trên Linux, nhưng guard cũ `_R387_CHI_LINUX` chỉ sinh bỏ qua ngoài Linux. N5 bắt được trên Windows. Chuyển phép đo của N4 sang nền mà guard cũ có thể kích hoạt hoặc buộc ca đối chứng giả lập nền đó.

### Ranh giới, kích thước và L1–L7

A giữ hàm đợi Linux, ba khóa sổ, thứ tự đọc lại trạng thái `stop` và xử lý Ctrl-C. Đường ngoài Linux trả `False` trước khi dò. Biểu thức quyết định xoá prompt ngoài Linux vẫn là biểu thức base. B nhận thay đổi `ps` của Darwin, dò Job Object và fixture Windows, các ca theo nền, neo `nhom_luon_rong` và bốn đột biến theo nền. B bỏ `(e5)` và đột biến tương ứng khi thay guard của A. Ngoài các finding trên, không thấy hạng mục chuyển giao bị trùng hoặc rơi mất.

`git diff --no-index --numstat` xác nhận A thêm `39 + 325 = 364` dòng, dưới trần 450 đúng 86 dòng. B thêm 118 dòng so với vá thử A. L1, L2, L4 và L7 khớp phạm vi A. L5 đã đối chiếu lại số dòng trên hai bản vá thử. L3 và L6 còn lỗ hổng ở N1 và `(e5)` như trên. Điều kiện đo lại trên exact head vẫn nằm ở N6.

Sandbox từ chối `mktemp` dưới `/tmp`. Tôi dùng bản vá thử `trA` có sẵn ở chế độ chỉ đọc, đặt `tempfile.tempdir` trong tiến trình và chạy từng ca bằng `--lap-ca … --lan 1`. Ca (e), ca (t) và `t117` đều `1/1 qua, 0 bo qua, 0 hong`, rc 0 lúc 08:13 UTC. Hai phản chứng cho `(e5)` chạy trong bộ nhớ. Chưa chạy native Darwin/Windows, toàn bộ suite hay toàn bộ runner đột biến. Phiên review giữ nguyên checkout và không gọi mạng.

KET_LUAN: request_changes
tokens used
65,310
Review độc lập lượt 6 cho đặc tả Packet A, Issue #387. Base đối chiếu `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. SHA-256 đặc tả A `85cd970f908703f3f8aba94c2aaec16d4d0a7f1ac53d1e0ecc211de8e5adc7ad`. Phiên `openai_codex / codex_cli / machine`, Linux, Python 3.13.18, sandbox chỉ đọc.

### Finding lượt 5

| Finding | Trạng thái | Căn cứ |
|---|---|---|
| P2 — Bộ ghi kill chuyển tiếp tín hiệu thật | **Đóng** | A M4 dùng hàm giả chỉ ghi nhật ký sau `lenh_run`. B M4 giữ cơ chế này và chỉ bọc `killpg` khi có. Log lịch sử của vá thử A ghi đột biến chèn `os.kill` bị giết đúng ca (a). |
| P2 — Teardown Windows và sót thư mục | **Chuyển hợp lệ sang B** | A bỏ fixture Windows. B M4 nhận phần bắt tay gán Job Object, chờ job rỗng và đóng handle trước khi dọn thư mục. B N5 giữ gate native Windows. Còn một lỗ hổng trong nhánh dọn lỗi, ghi riêng dưới đây. |
| P3 — §9 dẫn sai L1–L7 | **Đóng** | A §9 dẫn đúng `.claude/skills/soan-spec/SKILL.md` §2. |

### Finding mới

- **P2 · A — M2 làm đổi mốc kết thúc trên Darwin.** Base gọi `_bay_gio()` sau `_thanh_vien_nhom(p.pid)` và sau bước xoá prompt. A M2 dời mốc lên trước cả hai. Phép dò Darwin gọi `ps` với `timeout=15`, nên `ket_thuc_utc` và `thoi_luong_giay` có thể giảm cả thời gian dò, trái cam kết ở §2. Windows cũng đổi thứ tự lấy mốc. Giữ vị trí lấy mốc của base trên nền ngoài Linux, rồi thêm phép đo thứ tự này vào N5. [A §2–M2](ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md#2-ngoaiphamvi)
- **P2 · A — Đối chứng base của N1 đỏ trước khi chạy hành vi cần đo.** `_r387_chay` của vá thử đọc `_HAN_CHO_CAY_TRUOC_BAM_LOG` trước `lenh_run`. Hằng đó vắng trong `launcher.py` của base. Tôi đọc base từ `git archive` trong bộ nhớ và tái hiện `AttributeError` ở chính bước này bằng fixture với stub tối thiểu. N1 chỉ đòi dòng `LAP` và rc nên có thể nhận lỗi fixture làm bằng chứng lỗi băm. Cho fixture chạy được với base và yêu cầu `TinHieuChotCa` ở vế mới đã định danh, sau khi đã xác nhận cháu ghi muộn và băm sổ lệch băm đĩa.
- **P3 · A — (e5) bắt được phép dò thừa nhưng bỏ lọt phép chờ thừa.** Đột biến `r387_a_nen_khac_van_do` bị chặn đúng tại `(e5)`. Tuy nhiên, khi chèn `sleep(0.2)` trên nền ngoài Linux trước khi trả `False`, ca (e) vẫn qua. Dùng đồng hồ giả hoặc stub `sleep` làm ca đỏ để kiểm lời hứa “trả ngay”.
- **P2 · B — N5 có thể bỏ lọt thư mục sót sau teardown.** B M4 yêu cầu đóng handle sau khi chờ và vẫn đóng khi hết hạn. Trên đường hết hạn, `CloseHandle` khởi phát kết liễu job nhưng fixture đi ngay tới `San`, nơi `rmtree(..., ignore_errors=True)` nuốt lỗi. Vá thử cũng bỏ qua giá trị trả về của `CloseHandle`. Vì N5 chỉ kiểm kết quả ca và đột biến, một thư mục sót sau bước dọn có thể không được báo. Thêm kiểm tra kết quả đóng handle và kiểm tra thư mục thật sự biến mất, kể cả ở ca ép teardown lỗi.
- **P3 · B — N4 đo sai nền cho phản chứng.** B N4 đếm `BO QUA r387` trên Linux, nhưng guard cũ `_R387_CHI_LINUX` chỉ sinh bỏ qua ngoài Linux. N5 bắt được trên Windows. Chuyển phép đo của N4 sang nền mà guard cũ có thể kích hoạt hoặc buộc ca đối chứng giả lập nền đó.

### Ranh giới, kích thước và L1–L7

A giữ hàm đợi Linux, ba khóa sổ, thứ tự đọc lại trạng thái `stop` và xử lý Ctrl-C. Đường ngoài Linux trả `False` trước khi dò. Biểu thức quyết định xoá prompt ngoài Linux vẫn là biểu thức base. B nhận thay đổi `ps` của Darwin, dò Job Object và fixture Windows, các ca theo nền, neo `nhom_luon_rong` và bốn đột biến theo nền. B bỏ `(e5)` và đột biến tương ứng khi thay guard của A. Ngoài các finding trên, không thấy hạng mục chuyển giao bị trùng hoặc rơi mất.

`git diff --no-index --numstat` xác nhận A thêm `39 + 325 = 364` dòng, dưới trần 450 đúng 86 dòng. B thêm 118 dòng so với vá thử A. L1, L2, L4 và L7 khớp phạm vi A. L5 đã đối chiếu lại số dòng trên hai bản vá thử. L3 và L6 còn lỗ hổng ở N1 và `(e5)` như trên. Điều kiện đo lại trên exact head vẫn nằm ở N6.

Sandbox từ chối `mktemp` dưới `/tmp`. Tôi dùng bản vá thử `trA` có sẵn ở chế độ chỉ đọc, đặt `tempfile.tempdir` trong tiến trình và chạy từng ca bằng `--lap-ca … --lan 1`. Ca (e), ca (t) và `t117` đều `1/1 qua, 0 bo qua, 0 hong`, rc 0 lúc 08:13 UTC. Hai phản chứng cho `(e5)` chạy trong bộ nhớ. Chưa chạy native Darwin/Windows, toàn bộ suite hay toàn bộ runner đột biến. Phiên review giữ nguyên checkout và không gọi mạng.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T08:14:55Z
