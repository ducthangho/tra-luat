Review độc lập lượt 9/10 cho Issue #646, đặc tả r1. Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. SHA-256 đặc tả `fc18ac389650951e14ecdddeb91798f6b0869380f50ac8eba46cacb57d15e42f`. Reviewer họ OpenAI, giao diện Codex API, kết quả trả trực tiếp. Rig chạy trên Linux, Git 2.43.0, dưới `/dev/shm`, với cấu hình Git cô lập và tắt ký commit. Worktree giữ nguyên, không gọi mạng.

| Finding lượt 8 | Trạng thái | Bằng chứng trên cùng rig |
|---|---|---|
| P2 · Replace làm N1 đọc sai cây của OID | Đóng | Replace commit có thêm tệp ngoài write set cho `rc=0` ở bản 8 và `rc=1` ở bản hiện tại, kể cả khi biến `GIT_NO_REPLACE_OBJECTS` của caller rỗng. Replace blob sai bằng blob đúng cũng cho `rc=1`. |
| P3 · `GIT_DIR` sai và `core.abbrev=bogus` bị báo thành lỗi nội dung | Đóng | Với H đúng, `GIT_DIR` trỏ sai cho `rc=0` và `N1 DAT`. `core.abbrev=bogus` cho `rc=2` và `N1 MOI_TRUONG`. Bản 8 cho `rc=1` ở cả hai ca. |

### Finding mới

| Mức | Phản chứng chạy được | Kết quả |
|---|---|---|
| P3 | `bash n1.sh "$R" "$B" "$H" "$R/khong-co-n5.py"` với B và H hợp lệ | Python báo thiếu script, nhưng N1 trả `rc=1` và `N1 DO`. §4 quy định lỗi đối số hoặc môi trường trả `rc=2`. |
| P3 | Từ trong clone rig, chạy `bash /dev/shm/…/n1.sh '' "$B" "$H" /dev/shm/…/n5.py` với B và H hợp lệ | `git -C ""` dùng thư mục hiện hành. N1 trả `rc=0` và `N1 DAT` dù đối số đường kho rỗng. Cùng đối số từ ngoài kho cho `rc=2`. |

Không có finding P0–P2.

### Bằng chứng và đối chiếu

- **N1 và N5.** Diff dương trên rig chỉ chèn đúng khối 14 dòng của §3, giữ mode `100644`. Các ca cũ đổi mode, thêm tệp, gitlink, sửa ngoài vùng, chèn sai vị trí và CRLF đều trả `rc=1`. N5 đúng kỳ vọng 31/31. Đổi phép so từ bằng sang chứa làm đúng năm ca âm chuyển xanh, còn 26/31.
- **Đột biến N1.** Bỏ `GIT_NO_REPLACE_OBJECTS=1` làm replace commit chuyển `1→0`. Bỏ `unset` làm `GIT_DIR` sai chuyển `0→2`. Bỏ so raw diff làm ca đổi mode và thêm tệp chuyển `1→0`. Bỏ đồng thời (d), (e) làm ca chèn sai vị trí chuyển `1→0`. Bỏ cả (c), (d), (e) làm ca thêm dòng và ca chèn sai vị trí chuyển `1→0`. Các phép bỏ riêng chốt chồng lớp giữ nguyên mã thoát ở ca đối chứng.
- **Config và alternates.** Clone mới và clone `--shared` dùng alternate hợp lệ đều đo H đúng với `rc=0`. Giả định tin cậy phù hợp khi chính phiên kiểm tạo clone, giữ quyền kiểm soát cấu hình và đo exact OID. Không tái hiện được đường đổi kết quả ngoài giả định đó.
- **L1–L7.** Các số chính có đơn vị và mốc đo. M1–M3 cùng chiếu vào một tệp. N1–N5 đều nêu phép làm đỏ. L4 không áp dụng cho packet này. §6 yêu cầu đo lại trên exact base trước khi viết. N4 khớp số hit trên base, gồm `0` hit `heartbeat_at` tại cả sáu vị trí cổng. N2 và N3 chạy trên base đều `rc=0`, riêng protocol giữ đúng hai advisory miễn trừ. Các gate trên head triển khai thật chưa chạy.
- **E2.** §6 ghi đúng mốc lịch sử tám lượt `request_changes`, quyền duyệt băm còn thiếu và mục đích cấp lease g1. OID khai `ADR-0055` khớp lịch sử first-parent của `master` cục bộ. Tính cả lượt này là 9/10 theo assignment. Biên nhận từ xa và trạng thái Mission chưa được xác minh trong lượt offline.

KET_LUAN: approve
tokens used
73,651
Review độc lập lượt 9/10 cho Issue #646, đặc tả r1. Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. SHA-256 đặc tả `fc18ac389650951e14ecdddeb91798f6b0869380f50ac8eba46cacb57d15e42f`. Reviewer họ OpenAI, giao diện Codex API, kết quả trả trực tiếp. Rig chạy trên Linux, Git 2.43.0, dưới `/dev/shm`, với cấu hình Git cô lập và tắt ký commit. Worktree giữ nguyên, không gọi mạng.

| Finding lượt 8 | Trạng thái | Bằng chứng trên cùng rig |
|---|---|---|
| P2 · Replace làm N1 đọc sai cây của OID | Đóng | Replace commit có thêm tệp ngoài write set cho `rc=0` ở bản 8 và `rc=1` ở bản hiện tại, kể cả khi biến `GIT_NO_REPLACE_OBJECTS` của caller rỗng. Replace blob sai bằng blob đúng cũng cho `rc=1`. |
| P3 · `GIT_DIR` sai và `core.abbrev=bogus` bị báo thành lỗi nội dung | Đóng | Với H đúng, `GIT_DIR` trỏ sai cho `rc=0` và `N1 DAT`. `core.abbrev=bogus` cho `rc=2` và `N1 MOI_TRUONG`. Bản 8 cho `rc=1` ở cả hai ca. |

### Finding mới

| Mức | Phản chứng chạy được | Kết quả |
|---|---|---|
| P3 | `bash n1.sh "$R" "$B" "$H" "$R/khong-co-n5.py"` với B và H hợp lệ | Python báo thiếu script, nhưng N1 trả `rc=1` và `N1 DO`. §4 quy định lỗi đối số hoặc môi trường trả `rc=2`. |
| P3 | Từ trong clone rig, chạy `bash /dev/shm/…/n1.sh '' "$B" "$H" /dev/shm/…/n5.py` với B và H hợp lệ | `git -C ""` dùng thư mục hiện hành. N1 trả `rc=0` và `N1 DAT` dù đối số đường kho rỗng. Cùng đối số từ ngoài kho cho `rc=2`. |

Không có finding P0–P2.

### Bằng chứng và đối chiếu

- **N1 và N5.** Diff dương trên rig chỉ chèn đúng khối 14 dòng của §3, giữ mode `100644`. Các ca cũ đổi mode, thêm tệp, gitlink, sửa ngoài vùng, chèn sai vị trí và CRLF đều trả `rc=1`. N5 đúng kỳ vọng 31/31. Đổi phép so từ bằng sang chứa làm đúng năm ca âm chuyển xanh, còn 26/31.
- **Đột biến N1.** Bỏ `GIT_NO_REPLACE_OBJECTS=1` làm replace commit chuyển `1→0`. Bỏ `unset` làm `GIT_DIR` sai chuyển `0→2`. Bỏ so raw diff làm ca đổi mode và thêm tệp chuyển `1→0`. Bỏ đồng thời (d), (e) làm ca chèn sai vị trí chuyển `1→0`. Bỏ cả (c), (d), (e) làm ca thêm dòng và ca chèn sai vị trí chuyển `1→0`. Các phép bỏ riêng chốt chồng lớp giữ nguyên mã thoát ở ca đối chứng.
- **Config và alternates.** Clone mới và clone `--shared` dùng alternate hợp lệ đều đo H đúng với `rc=0`. Giả định tin cậy phù hợp khi chính phiên kiểm tạo clone, giữ quyền kiểm soát cấu hình và đo exact OID. Không tái hiện được đường đổi kết quả ngoài giả định đó.
- **L1–L7.** Các số chính có đơn vị và mốc đo. M1–M3 cùng chiếu vào một tệp. N1–N5 đều nêu phép làm đỏ. L4 không áp dụng cho packet này. §6 yêu cầu đo lại trên exact base trước khi viết. N4 khớp số hit trên base, gồm `0` hit `heartbeat_at` tại cả sáu vị trí cổng. N2 và N3 chạy trên base đều `rc=0`, riêng protocol giữ đúng hai advisory miễn trừ. Các gate trên head triển khai thật chưa chạy.
- **E2.** §6 ghi đúng mốc lịch sử tám lượt `request_changes`, quyền duyệt băm còn thiếu và mục đích cấp lease g1. OID khai `ADR-0055` khớp lịch sử first-parent của `master` cục bộ. Tính cả lượt này là 9/10 theo assignment. Biên nhận từ xa và trạng thái Mission chưa được xác minh trong lượt offline.

KET_LUAN: approve
rc=0 xong 2026-11-18T09:05:57Z
