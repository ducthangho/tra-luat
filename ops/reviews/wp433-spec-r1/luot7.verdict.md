Review độc lập lượt 7 cho Issue #433, họ OpenAI, qua API với shell cục bộ chỉ đọc. `HEAD` trùng `master` tại `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Hai đặc tả được neo riêng bằng SHA-256.

| Packet | SHA-256 |
|---|---|
| 1 — `NLM-GWS-DICH-NGOAI-KHO` | `cc70d9e605f373370aad8675963aac02706ff8c64c07693ec3b1ac1bd5c098b0` |
| 2 — `GWS-CRED-DICH-NGOAI-KHO` | `59a00d7fa4e132f1fccfd40c44f44a3bff5e17727ca97cb14e47352d4b850eaa` |

### Finding lượt 6

| Finding | Trạng thái | Bằng chứng |
|---|---|---|
| P2 — Hai packet đặt `\n` sai chỗ | **Đóng** | N8(2b) và N3e đặt `\n` vào tên kho. Trên Linux/Python 3.13.18, `python3 -I -B` chạy rc 0 lúc 06:35:13Z. Tôi tạo `k\nho/.git` thật trong RAM (`/dev/shm`) và chạy nguyên hàm `_trong_kho_git` trích từ Git base trên đường cha của W1 và W5. Cả hai trả đúng đường kho chứa `\n`. Nội suy thô tách thành **2 dòng**, `repr` giữ **1 dòng** và qua `fullmatch`. |
| P2 — Packet 1 M4 đếm cụm trên cả dòng | **Đóng** | M4 giới hạn phép đếm vào trường giữa `✗ ` và `: `. N8 có ca chi tiết chứa nguyên văn một cụm thuộc loại lỗi khác. |
| P2 — Packet 2 N4 neo đột biến reparse trên base | **Đóng** | N3c và N4 neo `db_bo_reparse` vào vế M6 trên nguồn candidate. §6 yêu cầu dừng nếu vế ấy đã có trên base sau khi packet 1 land. |
| P3 — Mốc §8 | **Đóng** | Cả hai ghi `2026-11-18T06:33:42Z` theo `date -u` và gọi rõ các số là ước lượng tĩnh. |

### Finding mới

- **P2 — Cả hai packet, ca xuống dòng không dựng được trên Windows.** Packet 1 N8(2b) và packet 2 N3e yêu cầu tạo thư mục thật `k\nho`, trong khi quy tắc phân nhóm ở N10 và N8 tương ứng chưa có điều kiện nền cho ca này. Cùng phép đo trên trả `ntpath.isreserved('k\nho') == True`. Vì vậy fixture tên kho này hỏng ngay khi dựng trên Windows, trước khi đo `repr`. Dùng kho thật trên POSIX và giả lập giá trị `_trong_kho_git` trả về cho cùng hậu điều trên Windows sẽ giữ được phép đo `db_khong_repr` ở cả hai nền. Windows native chưa chạy. [Packet 1 N8](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:267) · [Packet 2 N3e](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:107)
- **P2 — Packet 1, quy tắc phân hạng mâu thuẫn với hai đột biến W6.** N3 yêu cầu `db_w6_bo_kiem_token` và `db_w6_bo_kiem_nul` được giết vì ngoại lệ thoát. M5 và N10 chỉ cấp tín dụng khi runner nhận `TinHieuChotCa` đúng ca và đúng nhãn. N3 chưa quy định cách ca chuyển ngoại lệ dự kiến tại biên gọi `cmd_bootstrap` thành nhãn `token_hong` hoặc `env_nul`. Theo hợp đồng hiện tại, chính kết quả N3 dự kiến lại không đủ điều kiện để N10 tính `GIẾT`. [M5](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:245) · [N3](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:262) · [N10](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:269)

### Phạm vi, kích thước và L1–L7

- **Chuyển reparse.** Packet 1 nhất quán giữa §2, §3, §7 và §8 về giới hạn `S_ISLNK` và việc junction còn lọt. Packet 2 M6 và §6 giới hạn sửa `_kiem_dich_ghi` đúng biểu thức nhận diện. N3c có `reparse_w1` gọi qua `cmd_nlm_auth_pull` của packet 1, cùng đối chứng cờ thư mục thường. N4 đo junction thật. Packet 1 giữ nguyên nhánh jar rỗng, còn packet 2 N3d nhận ca hồi quy.
- **Kích thước.** Hai tổng đúng theo các hạng mục §8. Packet 1 **384–439** dòng thêm, còn **11** dòng ở đầu trên. Packet 2 **340–406**, còn **44** dòng. Mỗi packet dự kiến **3 tệp**. Phép đo RAM với ba dòng `numstat` giả cho tổng **450 đạt**, **451 đỏ**. N13/N11 và §6 yêu cầu đo trên exact head và dừng trước review nếu vượt trần. Chưa có mã để đo kích thước thực.
- **L1–L7.** L1 có đơn vị đếm. L2 ánh xạ mục tiêu vào ba đường dẫn, với ngoại lệ bundled có điều kiện trước lease. L3 còn hai finding trên. L4 khai giới hạn hồ sơ tiền nhiệm và dùng chung bộ đếm có chứng cứ. L5 phân biệt thời điểm đo, ước lượng và mốc đo lại. L6 có phép đo dương và đột biến, với giới hạn nền của fixture xuống dòng nêu trên. L7 dùng trần ADR và mã E2, không đặt ngân sách mềm. OID land của `ADR-0055` qua đối chiếu trên ref cục bộ. Trạng thái GitHub, test candidate và junction native chưa được xác minh trong lượt này.

KET_LUAN: request_changes
tokens used
67,732
Review độc lập lượt 7 cho Issue #433, họ OpenAI, qua API với shell cục bộ chỉ đọc. `HEAD` trùng `master` tại `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Hai đặc tả được neo riêng bằng SHA-256.

| Packet | SHA-256 |
|---|---|
| 1 — `NLM-GWS-DICH-NGOAI-KHO` | `cc70d9e605f373370aad8675963aac02706ff8c64c07693ec3b1ac1bd5c098b0` |
| 2 — `GWS-CRED-DICH-NGOAI-KHO` | `59a00d7fa4e132f1fccfd40c44f44a3bff5e17727ca97cb14e47352d4b850eaa` |

### Finding lượt 6

| Finding | Trạng thái | Bằng chứng |
|---|---|---|
| P2 — Hai packet đặt `\n` sai chỗ | **Đóng** | N8(2b) và N3e đặt `\n` vào tên kho. Trên Linux/Python 3.13.18, `python3 -I -B` chạy rc 0 lúc 06:35:13Z. Tôi tạo `k\nho/.git` thật trong RAM (`/dev/shm`) và chạy nguyên hàm `_trong_kho_git` trích từ Git base trên đường cha của W1 và W5. Cả hai trả đúng đường kho chứa `\n`. Nội suy thô tách thành **2 dòng**, `repr` giữ **1 dòng** và qua `fullmatch`. |
| P2 — Packet 1 M4 đếm cụm trên cả dòng | **Đóng** | M4 giới hạn phép đếm vào trường giữa `✗ ` và `: `. N8 có ca chi tiết chứa nguyên văn một cụm thuộc loại lỗi khác. |
| P2 — Packet 2 N4 neo đột biến reparse trên base | **Đóng** | N3c và N4 neo `db_bo_reparse` vào vế M6 trên nguồn candidate. §6 yêu cầu dừng nếu vế ấy đã có trên base sau khi packet 1 land. |
| P3 — Mốc §8 | **Đóng** | Cả hai ghi `2026-11-18T06:33:42Z` theo `date -u` và gọi rõ các số là ước lượng tĩnh. |

### Finding mới

- **P2 — Cả hai packet, ca xuống dòng không dựng được trên Windows.** Packet 1 N8(2b) và packet 2 N3e yêu cầu tạo thư mục thật `k\nho`, trong khi quy tắc phân nhóm ở N10 và N8 tương ứng chưa có điều kiện nền cho ca này. Cùng phép đo trên trả `ntpath.isreserved('k\nho') == True`. Vì vậy fixture tên kho này hỏng ngay khi dựng trên Windows, trước khi đo `repr`. Dùng kho thật trên POSIX và giả lập giá trị `_trong_kho_git` trả về cho cùng hậu điều trên Windows sẽ giữ được phép đo `db_khong_repr` ở cả hai nền. Windows native chưa chạy. [Packet 1 N8](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:267) · [Packet 2 N3e](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:107)
- **P2 — Packet 1, quy tắc phân hạng mâu thuẫn với hai đột biến W6.** N3 yêu cầu `db_w6_bo_kiem_token` và `db_w6_bo_kiem_nul` được giết vì ngoại lệ thoát. M5 và N10 chỉ cấp tín dụng khi runner nhận `TinHieuChotCa` đúng ca và đúng nhãn. N3 chưa quy định cách ca chuyển ngoại lệ dự kiến tại biên gọi `cmd_bootstrap` thành nhãn `token_hong` hoặc `env_nul`. Theo hợp đồng hiện tại, chính kết quả N3 dự kiến lại không đủ điều kiện để N10 tính `GIẾT`. [M5](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:245) · [N3](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:262) · [N10](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:269)

### Phạm vi, kích thước và L1–L7

- **Chuyển reparse.** Packet 1 nhất quán giữa §2, §3, §7 và §8 về giới hạn `S_ISLNK` và việc junction còn lọt. Packet 2 M6 và §6 giới hạn sửa `_kiem_dich_ghi` đúng biểu thức nhận diện. N3c có `reparse_w1` gọi qua `cmd_nlm_auth_pull` của packet 1, cùng đối chứng cờ thư mục thường. N4 đo junction thật. Packet 1 giữ nguyên nhánh jar rỗng, còn packet 2 N3d nhận ca hồi quy.
- **Kích thước.** Hai tổng đúng theo các hạng mục §8. Packet 1 **384–439** dòng thêm, còn **11** dòng ở đầu trên. Packet 2 **340–406**, còn **44** dòng. Mỗi packet dự kiến **3 tệp**. Phép đo RAM với ba dòng `numstat` giả cho tổng **450 đạt**, **451 đỏ**. N13/N11 và §6 yêu cầu đo trên exact head và dừng trước review nếu vượt trần. Chưa có mã để đo kích thước thực.
- **L1–L7.** L1 có đơn vị đếm. L2 ánh xạ mục tiêu vào ba đường dẫn, với ngoại lệ bundled có điều kiện trước lease. L3 còn hai finding trên. L4 khai giới hạn hồ sơ tiền nhiệm và dùng chung bộ đếm có chứng cứ. L5 phân biệt thời điểm đo, ước lượng và mốc đo lại. L6 có phép đo dương và đột biến, với giới hạn nền của fixture xuống dòng nêu trên. L7 dùng trần ADR và mã E2, không đặt ngân sách mềm. OID land của `ADR-0055` qua đối chiếu trên ref cục bộ. Trạng thái GitHub, test candidate và junction native chưa được xác minh trong lượt này.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T06:36:50Z
