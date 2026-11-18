Review độc lập lượt 3, đặc tả Issue #433. Packet 1 cần sửa hợp đồng lỗi W6 và các phép thử W2/Windows trước khi đóng băng. Phương án B và phạm vi diff ba tệp được ghi đúng.

**Bản đã rà**  
HEAD `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout detached, trùng ref `origin/master` cục bộ. SHA-256 của đặc tả packet 1 là `d863a253124e6cc4214fe5b3b44c53b011a6a1920740e215465f2d895b188f9a`. Phạm vi khai `sensitive` phù hợp với đường ghi credential. Review do Codex họ OpenAI thực hiện trong phiên API, verdict qua stdout. Model phục vụ và effort chưa có receipt để xác minh.

### Finding lượt 2

| Finding | Trạng thái | Kết quả lượt 3 |
|---|---|---|
| P1 — `goc` dạng `alias/`, `alias/.`, tương đối, `..`, junction trên Python 3.11 | **Chuyển một phần, còn mở** | Packet 2 giữ chuẩn hoá `cfgdir`, ca biểu diễn đường và ca junction native. Gốc cố định của packet 1 tránh được hậu tố trên chính `goc`, nhưng `HOME` vẫn có thể mang thành phần đường đặc biệt. Nhánh reparse nằm trong packet 1 và chưa có phép thử tại đây. |
| P2 — khe protocol–CI | **Đóng ở mức đặc tả** | §1/M7/N11–N12 giới hạn ngoại lệ vào bundled do `generate_bundled_module_bytes` sinh. Comment của chủ kho trên #433 phải nêu packet ID, đúng tệp và băm spec trước lease, rồi lease trỏ URL comment. Manifest thuộc commit land. Trạng thái comment chưa xác minh trong phiên offline. |
| P2 — N5 cấp sai tín dụng `degraded` | **Đóng** | N7 có ca chỉ-W6, bỏ `nlm_auth`, giữ W4 thành công và có đối chứng rc 0. Hai đột biến phải làm đỏ nhãn `ma` của chính ca này. |
| P2 — hợp đồng lỗi, surrogate, list, tiêm lỗi theo đích | **Chưa đóng** | Jar có hợp đồng kiểu và UTF-8. W4/W5 cùng phép tiêm lỗi được chuyển sang packet 2. Ca surrogate W6 vẫn vướng lỗi ở bước đặt env trước bước mã hoá config. |
| P2 — W6 và lần đọc của `load_creds` | **Đóng về phạm vi** | §2/M3 giới hạn cam kết vào lần đọc phục vụ merge W6. `load_creds` vẫn chạy trước `_secrets_fetch`. N6(2) còn thiếu phép quan sát để cưỡng chế thứ tự mới. |
| P3 — rig, N8, N12 | **Đóng phần cũ** | M5/N10 chuyển tổng kết sang stderr và giới hạn lớp chặn subprocess vào cửa sổ gọi hàm. Kiểm numstat hiện là **N13** và yêu cầu đúng ba đường trong §1. |
| P3 — số liệu §0 | **Đóng các mục lượt 2** | Spec đã cập nhật dòng fallback, ba lời gọi canary và mẫu 12 fragment. Đối chiếu cục bộ xác nhận 12 fragment và ba OID từ `git log -S`. |

### Finding lượt 3

| Mức | Finding | Sửa trong đặc tả |
|---|---|---|
| **P2** | **M3/M4/N3(4) mâu thuẫn về surrogate W6.** Base đặt `TL_TOKEN` trước khi đọc hoặc dựng JSON config. Trên Linux/Python 3.13.18, phép thử RAM với surrogate đơn giả cho `UnicodeEncodeError` ngay tại phép gán `os.environ`. N3(4) lại đòi `TL_TOKEN` được đặt, config giữ byte và bootstrap đi hết nhánh lỗi. Ngoài ra, JSON config cũ parse được thành list hoặc `null` làm `existing.update(...)` ném `AttributeError` ngoài nhóm lỗi M4. | Chốt riêng hành vi với `token`/`webappUrl` không thể đặt vào env và với config cũ parse được nhưng sai kiểu. Dùng dữ liệu chỉ hỏng ở bước tuần tự hoá config để kiểm nhánh đó, đồng thời thêm ca riêng cho lỗi đặt env. [Spec M3–M4](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:238) |
| **P2** | **N1 không giết được đột biến riêng của W2 theo mô tả.** Với khoá lạ, M3(1) đã đánh dấu jar bị từ chối và W2 không chạy. Đổi riêng vòng ghi W2 về vòng cũ vẫn để nguyên chốt sớm, nên `khong_thoat` vẫn xanh. | Giữ ca khoá lạ cho chốt dữ liệu chung và việc W6 không lưu jar sai. Dùng jar hợp lệ với đích bị chặn để giết đột biến bỏ chốt ghi riêng của W2. [Spec N1](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:255) |
| **P2** | **Packet 1 đưa nhánh reparse vào helper nhưng hoãn toàn bộ phép thử của nhánh đó.** Packet 2 phụ thuộc packet 1 đã land và có thể chưa đo được Windows native khi đến lượt. | Giữ nhánh trong packet 1 để packet 2 dùng lại nguyên thân hàm. Thêm một ca giả lập kết quả `lstat` có bit reparse với mode thư mục thường, một đối chứng không có bit và đột biến bỏ bit-check. Giữ junction thật ở packet 2 để xác minh hành vi hệ điều hành. [Spec N6](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:260) |
| **P2** | **Tên fragment trong packet 2 làm phần nghiệm thu được chuyển sang đó không chạy được theo hợp đồng hiện tại.** Regex thật yêu cầu ngay sau số Issue là `_`. Phép `fullmatch` trong RAM trả `False` cho cả tên tệp và `TEST_ID` dạng `wp433b_…`. | Đổi đồng bộ sang `wp433_gws_cred_dich_ngoai_kho` hoặc dùng số Issue riêng nếu packet 2 được cấp Issue riêng. Generator hiện có hỗ trợ hai slug khác nhau dưới cùng số Issue. [Write set packet 2](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:55) |
| **P3** | **N6(2) chưa đo việc từ chối trước lần đọc phục vụ merge.** Đích giữ byte và stderr đúng vẫn có thể xanh nếu chốt bị dời xuống sau lần đọc. | Với `load_creds` giả, quan sát riêng lần đọc config phục vụ merge. Đột biến dời chốt sau lần đọc phải làm đỏ ca. |
| **P3** | **N13 mô tả phản chứng trần bằng cách nối dòng thứ tư.** Đầu vào đó đã đỏ vì số dòng hoặc đường trùng, nên chưa cô lập được điều kiện tổng. | Giữ đúng ba dòng và đúng tập đường, thay cột thêm để tổng lần lượt là 450 và 451. |

Không thấy finding P0 hoặc P1 mới.

### Ranh giới đường dẫn và hợp đồng dùng chung

Mã thật gọi `expanduser` với tên lá cố định ở W1–W3/W6. Phép đo trong RAM cho thấy `HOME=/fixture/x/` vẫn cho đường kết thúc bằng tên lá cố định. `HOME=/fixture/x/.`, HOME chứa `..` và HOME tương đối lần lượt giữ thành phần `.` ở phía cha, giữ `..` ở phía cha và cho `goc` tương đối. HOME cũng có thể là symlink. Do đó, allowlist đủ để xác định **các thành phần dưới `goc`**. Phần trên `goc` dựa vào ngoại lệ HOME và hai phép dò từ vựng/`realpath` của `_trong_kho_git`. Nên ghi rõ lựa chọn giữ nguyên cách phân giải phần HOME và thêm ca dương cho HOME là symlink trỏ ra ngoài mọi kho. N5 hiện chỉ đo hai trường hợp bị từ chối.

Packet 2 có thể dùng lại nguyên thân `_kiem_dich_ghi` cho phạm vi đã mô tả. Nên chốt tiền điều kiện ngay tại M1: `goc` đã ở dạng thích hợp để `lstat` trực tiếp, `dich == os.path.join(goc, *thanh_phan)`, mỗi phần tử tuple là một tên thành phần, và caller ghi đúng `dich` đã kiểm. Phép dò liên kết bắt đầu tại `goc`. Chuẩn hoá `cfgdir` thuộc caller packet 2. Nên ghi rõ helper chỉ bỏ qua lỗi xác nhận tiền tố chưa tồn tại, còn lỗi quan sát khác đi vào hợp đồng lỗi của caller.

### L1–L7 và ngân sách

| Luật | Kết quả |
|---|---|
| L1 | Đơn vị đếm rõ cho chỗ ghi, ca, đột biến, tệp và dòng thêm. |
| L2 | Packet 1 có đúng ba tệp worker. Phần manifest của N12 do phiên land thực hiện. |
| L3 | Còn hở ở oracle W2, nhánh reparse và thứ tự đọc W6 như trên. |
| L4 | §7 phân biệt suy luận từ tiêu đề PR với số đếm có receipt. Số kế thừa vẫn `KHÔNG ĐO ĐƯỢC`. Nên ghi nguồn hoặc quy tắc cho mốc đếm mới `1`. |
| L5 | Các số lịch sử chính có mốc và base. Hai OID ADR đạt ba phép đối chiếu trên ref cục bộ, với rc `0/128/0` cho mỗi ADR. Trạng thái ref mới fetch, lease và comment vẫn cần đối chiếu ở bước công bố hoặc cấp lease. |
| L6 | N13 kiểm tập đường và từng dòng, có đầu vào rỗng, ref sai và dòng nhị phân. Các mẫu stderr cần `fullmatch` từng dòng như §4, với đường và khoá được biểu diễn trên một dòng. |
| L7 | Không thấy ngân sách mềm hay điểm hỏi tự đặt. §6 đã gắn E2 cho duyệt băm và thẩm quyền. Nên gắn E2 ngay tại dòng điều kiện comment bundled để điều kiện chờ chủ kho có mã tại chỗ. |

`95–125 + 280–310 + 1 = 376–436` dòng thêm, còn **14 dòng** ở cận trên so với trần 450. Đây là dự toán sát trần. Đối chiếu `git show --numstat 32ba025` cho tiền lệ `wp1099` là **346 dòng fragment + 1 dòng bundled** lúc thêm. Generator trên base sinh byte khớp bundled committed, rc 0. Sau khi sửa tiêu chí, cần cập nhật dự toán fragment theo số ca thực tế và dùng N13 trên exact head để quyết định đạt trần.

Đã chạy phép thử RAM với `python3 -IB` cho đường dẫn và surrogate, cùng các phép kiểm chỉ đọc cho regex, generator, Git và ADR. Không ghi worktree, không gọi mạng, không đọc secrets thật. Gate triển khai, CI và Windows native đều `not_run` trong lượt review đặc tả này.

KET_LUAN: request_changes
tokens used
70,536
Review độc lập lượt 3, đặc tả Issue #433. Packet 1 cần sửa hợp đồng lỗi W6 và các phép thử W2/Windows trước khi đóng băng. Phương án B và phạm vi diff ba tệp được ghi đúng.

**Bản đã rà**  
HEAD `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout detached, trùng ref `origin/master` cục bộ. SHA-256 của đặc tả packet 1 là `d863a253124e6cc4214fe5b3b44c53b011a6a1920740e215465f2d895b188f9a`. Phạm vi khai `sensitive` phù hợp với đường ghi credential. Review do Codex họ OpenAI thực hiện trong phiên API, verdict qua stdout. Model phục vụ và effort chưa có receipt để xác minh.

### Finding lượt 2

| Finding | Trạng thái | Kết quả lượt 3 |
|---|---|---|
| P1 — `goc` dạng `alias/`, `alias/.`, tương đối, `..`, junction trên Python 3.11 | **Chuyển một phần, còn mở** | Packet 2 giữ chuẩn hoá `cfgdir`, ca biểu diễn đường và ca junction native. Gốc cố định của packet 1 tránh được hậu tố trên chính `goc`, nhưng `HOME` vẫn có thể mang thành phần đường đặc biệt. Nhánh reparse nằm trong packet 1 và chưa có phép thử tại đây. |
| P2 — khe protocol–CI | **Đóng ở mức đặc tả** | §1/M7/N11–N12 giới hạn ngoại lệ vào bundled do `generate_bundled_module_bytes` sinh. Comment của chủ kho trên #433 phải nêu packet ID, đúng tệp và băm spec trước lease, rồi lease trỏ URL comment. Manifest thuộc commit land. Trạng thái comment chưa xác minh trong phiên offline. |
| P2 — N5 cấp sai tín dụng `degraded` | **Đóng** | N7 có ca chỉ-W6, bỏ `nlm_auth`, giữ W4 thành công và có đối chứng rc 0. Hai đột biến phải làm đỏ nhãn `ma` của chính ca này. |
| P2 — hợp đồng lỗi, surrogate, list, tiêm lỗi theo đích | **Chưa đóng** | Jar có hợp đồng kiểu và UTF-8. W4/W5 cùng phép tiêm lỗi được chuyển sang packet 2. Ca surrogate W6 vẫn vướng lỗi ở bước đặt env trước bước mã hoá config. |
| P2 — W6 và lần đọc của `load_creds` | **Đóng về phạm vi** | §2/M3 giới hạn cam kết vào lần đọc phục vụ merge W6. `load_creds` vẫn chạy trước `_secrets_fetch`. N6(2) còn thiếu phép quan sát để cưỡng chế thứ tự mới. |
| P3 — rig, N8, N12 | **Đóng phần cũ** | M5/N10 chuyển tổng kết sang stderr và giới hạn lớp chặn subprocess vào cửa sổ gọi hàm. Kiểm numstat hiện là **N13** và yêu cầu đúng ba đường trong §1. |
| P3 — số liệu §0 | **Đóng các mục lượt 2** | Spec đã cập nhật dòng fallback, ba lời gọi canary và mẫu 12 fragment. Đối chiếu cục bộ xác nhận 12 fragment và ba OID từ `git log -S`. |

### Finding lượt 3

| Mức | Finding | Sửa trong đặc tả |
|---|---|---|
| **P2** | **M3/M4/N3(4) mâu thuẫn về surrogate W6.** Base đặt `TL_TOKEN` trước khi đọc hoặc dựng JSON config. Trên Linux/Python 3.13.18, phép thử RAM với surrogate đơn giả cho `UnicodeEncodeError` ngay tại phép gán `os.environ`. N3(4) lại đòi `TL_TOKEN` được đặt, config giữ byte và bootstrap đi hết nhánh lỗi. Ngoài ra, JSON config cũ parse được thành list hoặc `null` làm `existing.update(...)` ném `AttributeError` ngoài nhóm lỗi M4. | Chốt riêng hành vi với `token`/`webappUrl` không thể đặt vào env và với config cũ parse được nhưng sai kiểu. Dùng dữ liệu chỉ hỏng ở bước tuần tự hoá config để kiểm nhánh đó, đồng thời thêm ca riêng cho lỗi đặt env. [Spec M3–M4](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:238) |
| **P2** | **N1 không giết được đột biến riêng của W2 theo mô tả.** Với khoá lạ, M3(1) đã đánh dấu jar bị từ chối và W2 không chạy. Đổi riêng vòng ghi W2 về vòng cũ vẫn để nguyên chốt sớm, nên `khong_thoat` vẫn xanh. | Giữ ca khoá lạ cho chốt dữ liệu chung và việc W6 không lưu jar sai. Dùng jar hợp lệ với đích bị chặn để giết đột biến bỏ chốt ghi riêng của W2. [Spec N1](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:255) |
| **P2** | **Packet 1 đưa nhánh reparse vào helper nhưng hoãn toàn bộ phép thử của nhánh đó.** Packet 2 phụ thuộc packet 1 đã land và có thể chưa đo được Windows native khi đến lượt. | Giữ nhánh trong packet 1 để packet 2 dùng lại nguyên thân hàm. Thêm một ca giả lập kết quả `lstat` có bit reparse với mode thư mục thường, một đối chứng không có bit và đột biến bỏ bit-check. Giữ junction thật ở packet 2 để xác minh hành vi hệ điều hành. [Spec N6](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:260) |
| **P2** | **Tên fragment trong packet 2 làm phần nghiệm thu được chuyển sang đó không chạy được theo hợp đồng hiện tại.** Regex thật yêu cầu ngay sau số Issue là `_`. Phép `fullmatch` trong RAM trả `False` cho cả tên tệp và `TEST_ID` dạng `wp433b_…`. | Đổi đồng bộ sang `wp433_gws_cred_dich_ngoai_kho` hoặc dùng số Issue riêng nếu packet 2 được cấp Issue riêng. Generator hiện có hỗ trợ hai slug khác nhau dưới cùng số Issue. [Write set packet 2](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:55) |
| **P3** | **N6(2) chưa đo việc từ chối trước lần đọc phục vụ merge.** Đích giữ byte và stderr đúng vẫn có thể xanh nếu chốt bị dời xuống sau lần đọc. | Với `load_creds` giả, quan sát riêng lần đọc config phục vụ merge. Đột biến dời chốt sau lần đọc phải làm đỏ ca. |
| **P3** | **N13 mô tả phản chứng trần bằng cách nối dòng thứ tư.** Đầu vào đó đã đỏ vì số dòng hoặc đường trùng, nên chưa cô lập được điều kiện tổng. | Giữ đúng ba dòng và đúng tập đường, thay cột thêm để tổng lần lượt là 450 và 451. |

Không thấy finding P0 hoặc P1 mới.

### Ranh giới đường dẫn và hợp đồng dùng chung

Mã thật gọi `expanduser` với tên lá cố định ở W1–W3/W6. Phép đo trong RAM cho thấy `HOME=/fixture/x/` vẫn cho đường kết thúc bằng tên lá cố định. `HOME=/fixture/x/.`, HOME chứa `..` và HOME tương đối lần lượt giữ thành phần `.` ở phía cha, giữ `..` ở phía cha và cho `goc` tương đối. HOME cũng có thể là symlink. Do đó, allowlist đủ để xác định **các thành phần dưới `goc`**. Phần trên `goc` dựa vào ngoại lệ HOME và hai phép dò từ vựng/`realpath` của `_trong_kho_git`. Nên ghi rõ lựa chọn giữ nguyên cách phân giải phần HOME và thêm ca dương cho HOME là symlink trỏ ra ngoài mọi kho. N5 hiện chỉ đo hai trường hợp bị từ chối.

Packet 2 có thể dùng lại nguyên thân `_kiem_dich_ghi` cho phạm vi đã mô tả. Nên chốt tiền điều kiện ngay tại M1: `goc` đã ở dạng thích hợp để `lstat` trực tiếp, `dich == os.path.join(goc, *thanh_phan)`, mỗi phần tử tuple là một tên thành phần, và caller ghi đúng `dich` đã kiểm. Phép dò liên kết bắt đầu tại `goc`. Chuẩn hoá `cfgdir` thuộc caller packet 2. Nên ghi rõ helper chỉ bỏ qua lỗi xác nhận tiền tố chưa tồn tại, còn lỗi quan sát khác đi vào hợp đồng lỗi của caller.

### L1–L7 và ngân sách

| Luật | Kết quả |
|---|---|
| L1 | Đơn vị đếm rõ cho chỗ ghi, ca, đột biến, tệp và dòng thêm. |
| L2 | Packet 1 có đúng ba tệp worker. Phần manifest của N12 do phiên land thực hiện. |
| L3 | Còn hở ở oracle W2, nhánh reparse và thứ tự đọc W6 như trên. |
| L4 | §7 phân biệt suy luận từ tiêu đề PR với số đếm có receipt. Số kế thừa vẫn `KHÔNG ĐO ĐƯỢC`. Nên ghi nguồn hoặc quy tắc cho mốc đếm mới `1`. |
| L5 | Các số lịch sử chính có mốc và base. Hai OID ADR đạt ba phép đối chiếu trên ref cục bộ, với rc `0/128/0` cho mỗi ADR. Trạng thái ref mới fetch, lease và comment vẫn cần đối chiếu ở bước công bố hoặc cấp lease. |
| L6 | N13 kiểm tập đường và từng dòng, có đầu vào rỗng, ref sai và dòng nhị phân. Các mẫu stderr cần `fullmatch` từng dòng như §4, với đường và khoá được biểu diễn trên một dòng. |
| L7 | Không thấy ngân sách mềm hay điểm hỏi tự đặt. §6 đã gắn E2 cho duyệt băm và thẩm quyền. Nên gắn E2 ngay tại dòng điều kiện comment bundled để điều kiện chờ chủ kho có mã tại chỗ. |

`95–125 + 280–310 + 1 = 376–436` dòng thêm, còn **14 dòng** ở cận trên so với trần 450. Đây là dự toán sát trần. Đối chiếu `git show --numstat 32ba025` cho tiền lệ `wp1099` là **346 dòng fragment + 1 dòng bundled** lúc thêm. Generator trên base sinh byte khớp bundled committed, rc 0. Sau khi sửa tiêu chí, cần cập nhật dự toán fragment theo số ca thực tế và dùng N13 trên exact head để quyết định đạt trần.

Đã chạy phép thử RAM với `python3 -IB` cho đường dẫn và surrogate, cùng các phép kiểm chỉ đọc cho regex, generator, Git và ADR. Không ghi worktree, không gọi mạng, không đọc secrets thật. Gate triển khai, CI và Windows native đều `not_run` trong lượt review đặc tả này.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T06:12:46Z
