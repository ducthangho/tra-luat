## Review độc lập lượt 4 · Issue #433

Review hai bản đặc tả trên HEAD `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Worktree ở detached HEAD, trùng OID của `master` cục bộ. Hai đặc tả hiện là tệp untracked, được neo bằng SHA-256 dưới đây.

| Đặc tả | SHA-256 |
|---|---|
| Packet 1 · `NLM-GWS-DICH-NGOAI-KHO-r1.md` | `d8c961e946eb2fefd29d4addb6f038b6c59821b491b40adc508ccf464397e23c` |
| Packet 2 · `GWS-CRED-DICH-NGOAI-KHO-r1.md` | `dcd5fa740e8ff98a1a3ec0c05a4e213ba27ab02c5d91891be3b3e5fc0dc1b0a4` |

Bằng chứng từ phiên OpenAI Codex, shell cục bộ, transport `machine`, sandbox read-only. Các probe `python3 -B -` chạy trong RAM trên Linux/Python 3.13.18 với dữ liệu giả. Probe đầu dừng khi đọc sai kiểu nút AST của regex. Probe đã sửa trả rc 0 và đo đủ. Test triển khai, CI, junction Windows, trạng thái land và quyền cấp lease từ xa chưa được xác minh trong lượt offline này.

## Finding lượt 3

| Finding | Trạng thái | Bằng chứng |
|---|---|---|
| P2 · Packet 1 · Surrogate W6 và config cũ sai kiểu | **Đóng** | M3 kiểm UTF-8 trước khi gán env và xử lý config cũ theo kiểu `dict`. N3 tách lỗi gán env, lỗi tuần tự hóa và config cũ. Probe xác nhận `os.environ` ném `UnicodeEncodeError` với surrogate đơn. `.update()` ném `AttributeError` với cả `[]`, `null` và `"s"`. |
| P2 · Packet 1 · N1 chưa giết được đột biến riêng W2 | **Đóng** | Ca mới đưa jar hợp lệ qua chốt dữ liệu chung để tới đúng W2. N1 yêu cầu `db_w2_bo_chot` làm hỏng nhãn `khong_ra_ngoai` của ca đó. |
| P2 · Packet 1 · Nhánh reparse thiếu ca | **Đóng** | N6(5) giả lập đúng bit reparse và có ca giết biến thể bỏ kiểm bit. Probe bitmask xác nhận hai biến thể cho kết quả khác nhau khi thuộc tính là `1024`. Biến thể kiểm sai mặt nạ còn sống, ghi riêng bên dưới. |
| P2 · Packet 2 · Tên fragment `wp433b_` sai regex | **Đóng** | `re.fullmatch` trên mẫu lấy trực tiếp từ AST trả `False` với tên cũ, `True` với `wp433_gws_cred_dich_ngoai_kho` và ID hiện tại của packet 1. |
| P3 · Packet 1 · N6(2) thiếu phép đo thứ tự đọc config | **Đóng** | M3 đặt chốt trước lần `open` phục vụ merge. N6(2) cô lập `load_creds`, đếm lần mở và nhắm `db_w6_doc_truoc_chot` vào `khong_doc_merge`. |
| P3 · Packet 1 · N13 chưa cô lập phản chứng trần | **Đóng** | Hai bản dùng đúng ba dòng và đúng tập đường dẫn cho cặp 450/451. Probe xác nhận cả hai qua kiểm hình dạng, tổng 450 xanh và 451 đỏ. |

## Finding mới

| Mức | Packet | Finding |
|---|---|---|
| **P2** | **1** | **M3(0b) vẫn cho lọt giá trị env mà `os.environ` từ chối.** Chuỗi JSON chứa NUL qua được kiểm `str` và `.encode("utf-8")`, sau đó phép gán ném `ValueError: embedded null byte`. Probe đã xác nhận bằng giá trị giả. Với `webappUrl` hỏng, thứ tự gán của base còn có thể để lại `TL_TOKEN` đã đổi. Bổ sung điều kiện không có NUL cho cả hai trường trước bất kỳ phép gán nào. N3 cần đo rc, một dòng lỗi, cả hai biến env và byte config. |
| **P2** | **1** | **N6(5) liệt kê một đột biến chắc chắn sống, mâu thuẫn với N10(a).** Cả lọc đúng mặt nạ và lọc “mọi thuộc tính khác 0” đều từ chối `1024` và cho qua `0`. Probe xác nhận `stat.FILE_ATTRIBUTE_DIRECTORY` (`16`) phân biệt được hai cách. Dùng thuộc tính thư mục khác 0 nhưng không mang bit reparse cho đối chứng dương, rồi yêu cầu `db_reparse_moi_thu` giết đúng nhãn. |
| **P2** | **1** | **M2 và M4 chưa thống nhất với nhánh kiểm định dạng W1/W3.** W1 hiện trả cảnh báo riêng khi jar falsy. W3 hiện trả `nlm_cred rỗng/sai định dạng.` cho jar rỗng hoặc sai kiểu. M2 giao các trường hợp đó cho `_kiem_jar_nlm` với cụm `dữ liệu không hợp lệ`, còn M4 đặt chốt sau kiểm định dạng sẵn có ở W3. Ghi rõ nhánh nào được thay bằng chốt chung và thêm hậu điều cho jar rỗng/sai kiểu ở W3 và jar rỗng ở W1. |
| **P2** | **1, 2** | **Chuyển ca rc 4 làm mất phép đo tương tác với lỗi W2.** Packet 1 M4 vẫn hứa rc 4 và giữ dòng từ chối khi W2 suy giảm. Packet 2 N7(1) chỉ gây suy giảm qua W4. `r973_bootstrap_require_agent_creds` chạy `env="chat"` và cũng không đi qua W2. Có thể giữ ngân sách bằng cách tái chạy fixture W2 hiện có với cờ `--require-agent-creds`, chung trong một ca dạng bảng. Nếu chuyển phép đo, packet 2 cần giữ cả hàng W2 và ghi rõ rằng bằng chứng ấy chỉ xuất hiện sau khi packet 1 land. |
| **P2** | **2** | **M1 chưa xác định cách xử lý đường tương đối theo ổ đĩa trên Windows.** Probe `ntpath` cho `isabs("D:fake") == False`, nhưng `join("C:\\fake_cwd", "D:fake")` vẫn trả `D:fake`. Bước tách thành phần rồi dựng lại phải có quy tắc rõ để bảo đảm kết quả tuyệt đối và giữ đúng nghĩa của đích. Chốt dạng được hỗ trợ hoặc từ chối với `đường không hợp lệ`. Thêm ca phân biệt đường theo ổ đĩa, đường bắt đầu ở gốc ổ hiện tại và đường tuyệt đối có ổ đĩa. |
| **P3** | **1** | **Lời khai độ phủ ở §7 rộng hơn N5 và N8.** Việc dời hai ca chuỗi giữ nguyên lời gọi `_trong_kho_git` trong M1, và PD7/PD8 vẫn canh thân helper. Packet 1 chỉ đo bỏ toàn bộ luật (a) ở caller. Hai biến thể caller dùng riêng một chuỗi phải đợi packet 2 N3b. Thu hẹp câu “một đột biến riêng … mỗi lớp” và ghi rõ mốc có bằng chứng cho từng lớp. |
| **P3** | **1, 2** | **Hợp đồng stderr của ca rc 4 cần ghi đủ hai dòng.** Base in thêm một dòng `✗ --require-agent-creds` khi trả 4. Tiêu chí nên khớp đúng một dòng từ chối ghi và đúng một dòng báo rc 4, cùng một dòng `agent_creds:` trên stdout. |

Không có finding P0 hoặc P1 trong lượt này.

## Hợp đồng giữa hai packet và trần kích thước

- **`_kiem_dich_ghi`.** Với `cfgdir` đã chuẩn hóa thành đường tuyệt đối, lời gọi W4/W5 `(cfgdir/credentials.json, cfgdir, ("credentials.json",))` khớp M1 packet 1. Helper kiểm kho trên thư mục cha, rồi `lstat` chính `goc` và đích. Caller dùng đúng đích đã kiểm và chuyển lỗi I/O thành `ghi lỗi`. N3b của packet 2 đặt liên kết phía trên `goc`, nên mỗi ca cô lập đúng một chuỗi dò kho. Điểm còn thiếu là miền đầu vào Windows của bước chuẩn hóa.
- **Trần packet 1.** `105–130 + 280–310 + 1 = 386–441` dòng thêm trên ba tệp. Biên cận trên là **9 dòng**. Tiền lệ `wp1099_nlm_nap_lai` thêm 346 dòng theo `git show --numstat 32ba025`, nên khoảng dự toán fragment 280–310 vẫn cần xác nhận bằng diff thật. §6 và N13 đặt đúng điểm dừng trước review: **451 dòng thêm thì dừng để revision/tách**. Biên 9 dòng chưa phải kết quả đạt trần.

## Rà L1–L7

| Luật | Kết quả |
|---|---|
| **L1** | Cả hai phân biệt số ca, số đột biến, số tệp và số dòng thêm. |
| **L2** | Mục tiêu chiếu được vào ba đường dẫn mỗi packet. Ngoại lệ bundled chờ comment riêng neo băm. Packet 2 phải dừng nếu cần sửa thân helper của packet 1. |
| **L3** | Còn các lỗ hổng nghiệm thu nêu ở bảng finding, đặc biệt đột biến reparse sống và mất tương tác W2/rc 4. |
| **L4** | Cả hai khai rõ số đếm tiền nhiệm chưa đo được và phân biệt suy luận từ tiêu đề với biên nhận. |
| **L5** | Có neo base và mốc đo lại. Packet 2 phải đo lại trên OID sau land. Packet 1 N12 nên ghi `185` là số nền có mốc đo, với điều kiện nghiệm thu dựa trên số lượng expected/checked của manifest tạm tại exact head. |
| **L6** | Hai phép kiểm trần có vế dương và âm cùng hình dạng đầu vào. Regex ID đã đo trực tiếp. Hợp đồng đếm dòng stderr cho rc 4 còn thiếu như finding P3. |
| **L7** | Cả hai dẫn trần ADR, khai E4/E5 và gắn E2 cho ngoại lệ bundled, duyệt băm và yêu cầu nâng trần. |

KET_LUAN: request_changes
tokens used
71,072
## Review độc lập lượt 4 · Issue #433

Review hai bản đặc tả trên HEAD `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Worktree ở detached HEAD, trùng OID của `master` cục bộ. Hai đặc tả hiện là tệp untracked, được neo bằng SHA-256 dưới đây.

| Đặc tả | SHA-256 |
|---|---|
| Packet 1 · `NLM-GWS-DICH-NGOAI-KHO-r1.md` | `d8c961e946eb2fefd29d4addb6f038b6c59821b491b40adc508ccf464397e23c` |
| Packet 2 · `GWS-CRED-DICH-NGOAI-KHO-r1.md` | `dcd5fa740e8ff98a1a3ec0c05a4e213ba27ab02c5d91891be3b3e5fc0dc1b0a4` |

Bằng chứng từ phiên OpenAI Codex, shell cục bộ, transport `machine`, sandbox read-only. Các probe `python3 -B -` chạy trong RAM trên Linux/Python 3.13.18 với dữ liệu giả. Probe đầu dừng khi đọc sai kiểu nút AST của regex. Probe đã sửa trả rc 0 và đo đủ. Test triển khai, CI, junction Windows, trạng thái land và quyền cấp lease từ xa chưa được xác minh trong lượt offline này.

## Finding lượt 3

| Finding | Trạng thái | Bằng chứng |
|---|---|---|
| P2 · Packet 1 · Surrogate W6 và config cũ sai kiểu | **Đóng** | M3 kiểm UTF-8 trước khi gán env và xử lý config cũ theo kiểu `dict`. N3 tách lỗi gán env, lỗi tuần tự hóa và config cũ. Probe xác nhận `os.environ` ném `UnicodeEncodeError` với surrogate đơn. `.update()` ném `AttributeError` với cả `[]`, `null` và `"s"`. |
| P2 · Packet 1 · N1 chưa giết được đột biến riêng W2 | **Đóng** | Ca mới đưa jar hợp lệ qua chốt dữ liệu chung để tới đúng W2. N1 yêu cầu `db_w2_bo_chot` làm hỏng nhãn `khong_ra_ngoai` của ca đó. |
| P2 · Packet 1 · Nhánh reparse thiếu ca | **Đóng** | N6(5) giả lập đúng bit reparse và có ca giết biến thể bỏ kiểm bit. Probe bitmask xác nhận hai biến thể cho kết quả khác nhau khi thuộc tính là `1024`. Biến thể kiểm sai mặt nạ còn sống, ghi riêng bên dưới. |
| P2 · Packet 2 · Tên fragment `wp433b_` sai regex | **Đóng** | `re.fullmatch` trên mẫu lấy trực tiếp từ AST trả `False` với tên cũ, `True` với `wp433_gws_cred_dich_ngoai_kho` và ID hiện tại của packet 1. |
| P3 · Packet 1 · N6(2) thiếu phép đo thứ tự đọc config | **Đóng** | M3 đặt chốt trước lần `open` phục vụ merge. N6(2) cô lập `load_creds`, đếm lần mở và nhắm `db_w6_doc_truoc_chot` vào `khong_doc_merge`. |
| P3 · Packet 1 · N13 chưa cô lập phản chứng trần | **Đóng** | Hai bản dùng đúng ba dòng và đúng tập đường dẫn cho cặp 450/451. Probe xác nhận cả hai qua kiểm hình dạng, tổng 450 xanh và 451 đỏ. |

## Finding mới

| Mức | Packet | Finding |
|---|---|---|
| **P2** | **1** | **M3(0b) vẫn cho lọt giá trị env mà `os.environ` từ chối.** Chuỗi JSON chứa NUL qua được kiểm `str` và `.encode("utf-8")`, sau đó phép gán ném `ValueError: embedded null byte`. Probe đã xác nhận bằng giá trị giả. Với `webappUrl` hỏng, thứ tự gán của base còn có thể để lại `TL_TOKEN` đã đổi. Bổ sung điều kiện không có NUL cho cả hai trường trước bất kỳ phép gán nào. N3 cần đo rc, một dòng lỗi, cả hai biến env và byte config. |
| **P2** | **1** | **N6(5) liệt kê một đột biến chắc chắn sống, mâu thuẫn với N10(a).** Cả lọc đúng mặt nạ và lọc “mọi thuộc tính khác 0” đều từ chối `1024` và cho qua `0`. Probe xác nhận `stat.FILE_ATTRIBUTE_DIRECTORY` (`16`) phân biệt được hai cách. Dùng thuộc tính thư mục khác 0 nhưng không mang bit reparse cho đối chứng dương, rồi yêu cầu `db_reparse_moi_thu` giết đúng nhãn. |
| **P2** | **1** | **M2 và M4 chưa thống nhất với nhánh kiểm định dạng W1/W3.** W1 hiện trả cảnh báo riêng khi jar falsy. W3 hiện trả `nlm_cred rỗng/sai định dạng.` cho jar rỗng hoặc sai kiểu. M2 giao các trường hợp đó cho `_kiem_jar_nlm` với cụm `dữ liệu không hợp lệ`, còn M4 đặt chốt sau kiểm định dạng sẵn có ở W3. Ghi rõ nhánh nào được thay bằng chốt chung và thêm hậu điều cho jar rỗng/sai kiểu ở W3 và jar rỗng ở W1. |
| **P2** | **1, 2** | **Chuyển ca rc 4 làm mất phép đo tương tác với lỗi W2.** Packet 1 M4 vẫn hứa rc 4 và giữ dòng từ chối khi W2 suy giảm. Packet 2 N7(1) chỉ gây suy giảm qua W4. `r973_bootstrap_require_agent_creds` chạy `env="chat"` và cũng không đi qua W2. Có thể giữ ngân sách bằng cách tái chạy fixture W2 hiện có với cờ `--require-agent-creds`, chung trong một ca dạng bảng. Nếu chuyển phép đo, packet 2 cần giữ cả hàng W2 và ghi rõ rằng bằng chứng ấy chỉ xuất hiện sau khi packet 1 land. |
| **P2** | **2** | **M1 chưa xác định cách xử lý đường tương đối theo ổ đĩa trên Windows.** Probe `ntpath` cho `isabs("D:fake") == False`, nhưng `join("C:\\fake_cwd", "D:fake")` vẫn trả `D:fake`. Bước tách thành phần rồi dựng lại phải có quy tắc rõ để bảo đảm kết quả tuyệt đối và giữ đúng nghĩa của đích. Chốt dạng được hỗ trợ hoặc từ chối với `đường không hợp lệ`. Thêm ca phân biệt đường theo ổ đĩa, đường bắt đầu ở gốc ổ hiện tại và đường tuyệt đối có ổ đĩa. |
| **P3** | **1** | **Lời khai độ phủ ở §7 rộng hơn N5 và N8.** Việc dời hai ca chuỗi giữ nguyên lời gọi `_trong_kho_git` trong M1, và PD7/PD8 vẫn canh thân helper. Packet 1 chỉ đo bỏ toàn bộ luật (a) ở caller. Hai biến thể caller dùng riêng một chuỗi phải đợi packet 2 N3b. Thu hẹp câu “một đột biến riêng … mỗi lớp” và ghi rõ mốc có bằng chứng cho từng lớp. |
| **P3** | **1, 2** | **Hợp đồng stderr của ca rc 4 cần ghi đủ hai dòng.** Base in thêm một dòng `✗ --require-agent-creds` khi trả 4. Tiêu chí nên khớp đúng một dòng từ chối ghi và đúng một dòng báo rc 4, cùng một dòng `agent_creds:` trên stdout. |

Không có finding P0 hoặc P1 trong lượt này.

## Hợp đồng giữa hai packet và trần kích thước

- **`_kiem_dich_ghi`.** Với `cfgdir` đã chuẩn hóa thành đường tuyệt đối, lời gọi W4/W5 `(cfgdir/credentials.json, cfgdir, ("credentials.json",))` khớp M1 packet 1. Helper kiểm kho trên thư mục cha, rồi `lstat` chính `goc` và đích. Caller dùng đúng đích đã kiểm và chuyển lỗi I/O thành `ghi lỗi`. N3b của packet 2 đặt liên kết phía trên `goc`, nên mỗi ca cô lập đúng một chuỗi dò kho. Điểm còn thiếu là miền đầu vào Windows của bước chuẩn hóa.
- **Trần packet 1.** `105–130 + 280–310 + 1 = 386–441` dòng thêm trên ba tệp. Biên cận trên là **9 dòng**. Tiền lệ `wp1099_nlm_nap_lai` thêm 346 dòng theo `git show --numstat 32ba025`, nên khoảng dự toán fragment 280–310 vẫn cần xác nhận bằng diff thật. §6 và N13 đặt đúng điểm dừng trước review: **451 dòng thêm thì dừng để revision/tách**. Biên 9 dòng chưa phải kết quả đạt trần.

## Rà L1–L7

| Luật | Kết quả |
|---|---|
| **L1** | Cả hai phân biệt số ca, số đột biến, số tệp và số dòng thêm. |
| **L2** | Mục tiêu chiếu được vào ba đường dẫn mỗi packet. Ngoại lệ bundled chờ comment riêng neo băm. Packet 2 phải dừng nếu cần sửa thân helper của packet 1. |
| **L3** | Còn các lỗ hổng nghiệm thu nêu ở bảng finding, đặc biệt đột biến reparse sống và mất tương tác W2/rc 4. |
| **L4** | Cả hai khai rõ số đếm tiền nhiệm chưa đo được và phân biệt suy luận từ tiêu đề với biên nhận. |
| **L5** | Có neo base và mốc đo lại. Packet 2 phải đo lại trên OID sau land. Packet 1 N12 nên ghi `185` là số nền có mốc đo, với điều kiện nghiệm thu dựa trên số lượng expected/checked của manifest tạm tại exact head. |
| **L6** | Hai phép kiểm trần có vế dương và âm cùng hình dạng đầu vào. Regex ID đã đo trực tiếp. Hợp đồng đếm dòng stderr cho rc 4 còn thiếu như finding P3. |
| **L7** | Cả hai dẫn trần ADR, khai E4/E5 và gắn E2 cho ngoại lệ bundled, duyệt băm và yêu cầu nâng trần. |

KET_LUAN: request_changes
rc=0 xong 2026-11-18T06:19:32Z
