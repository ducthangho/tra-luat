Review đặc tả packet 1, Issue #433, lượt 12/12. HEAD `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. SHA-256 đặc tả `eb7c60409ad6cad0fd962c154d6fc0e4bb0472a286bd840ac3b474aa8b485633`. Tôi dùng Codex họ OpenAI trong phiên API chỉ đọc. Các phép kiểm chạy trong RAM bằng dữ liệu giả, không gọi mạng. Gate trên mã triển khai ở trạng thái `not_run`.

### Finding lượt 11 · Packet 1

| Mức | Finding | Trạng thái | Bằng chứng |
|---|---|---|---|
| P2 | §4b dòng 4 gộp kiểm đích và writer W2 | Đóng | `db_w2_bo_kiem_dich` chỉ bỏ `_kiem_dich_ghi`. Mô phỏng A/B giữ nguyên writer. Có chốt thì writer không được gọi, bỏ chốt thì writer nhận đích của fixture. |
| P2 | N1 đòi stderr ở biên trả tuple W3 | Đóng | Cả ba lượt W3 của N1 đo lý do trả về bằng `fullmatch`. Mẫu `<cụm>: .*` nhận chi tiết đã `repr` và loại chuỗi có tiền tố thừa hoặc xuống dòng thô. |
| P3 | Con trỏ phần dữ liệu W6 | Đóng | §2 và §7 trỏ đúng M7/N9w6 của packet 2. |

### Finding mới

| Mức | Packet | Finding |
|---|---|---|
| **P2** | **1** | **§4b dòng 14 đổi cả luật kho lẫn luật symlink.** M1 tìm kho từ `dirname(dich)`. Khi `HOME` chính là gốc kho `/K`, lời gọi chuẩn tìm từ `/K`, còn đột biến truyền `/K` làm `dich` nên cuộc tìm bắt đầu ở `/`. Tôi chạy nguyên thân `_trong_kho_git` của base với `lstat` giả trong RAM. Lời gọi chuẩn trả `nằm trong kho git`, đột biến cho qua. Với fixture N6(2), HOME thường ngoài kho và lá config là symlink, mô hình trả `là liên kết tượng trưng` ở bản chuẩn và cho qua ở bản đột biến. Vì vậy fixture dự kiến đỏ đúng nhãn `stderr` nhưng không chứng minh đột biến cô lập một cơ chế. Cần giữ nguyên đường đầu vào luật (a) và chỉ đổi việc kiểm lá config ở luật (b). |
| P3 | 1 | **§2 và M3 mô tả quá rộng việc giữ hành vi base khi tuần tự hoá W6 lỗi.** Với surrogate giả, `json.dump` của base ghi một phần JSON rồi ném `UnicodeEncodeError`. Biểu thức `json.dumps(...).encode(...)` của M3 ném cùng loại ngoại lệ trước khi gọi writer. Đo trong RAM xác nhận hai hành vi. Nên ghi rõ ngoại lệ vẫn lan ra, còn config cũ giữ nguyên byte nhờ thứ tự mới. |

Rà đủ 30 dòng §4b cho kết quả 26 H và 4 E. Bốn dòng E là 10, 11, 22 và 24. Tập khai gắn với từng lượt và hai dòng dùng chung dấu trên nhiều lượt đã liệt kê các lượt tương ứng. Ngoài dòng 14, tôi không thấy đột biến gộp chốt khác. Rà L1–L7, điểm chặn nằm ở phép phản chứng cô lập cơ chế của dòng 14. Các điều kiện quyền E2 vẫn chờ duyệt băm và ngoại lệ bundled trước cấp lease.

Packet 2 vẫn hoãn. Các finding UNC, surrogate ở biên env, khai ngoại lệ theo lượt, bảng Markdown và số lượt W6 đã ghi trong packet 2, không chặn verdict này. Phần W4/W5, reparse và kiểm dữ liệu W6 vẫn có ranh giới rõ giữa hai đặc tả.

Ước lượng 369–420 dòng để lại biên 30 dòng. Phép tính trong RAM cho 450 qua và 451 trượt. N13 vẫn cần đo `numstat` trên exact head triển khai. Lượt 12 đã chạm trần riêng của packet 1, nên dừng tại Review Rescue Checkpoint.

KET_LUAN: request_changes
tokens used
79,393
Review đặc tả packet 1, Issue #433, lượt 12/12. HEAD `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. SHA-256 đặc tả `eb7c60409ad6cad0fd962c154d6fc0e4bb0472a286bd840ac3b474aa8b485633`. Tôi dùng Codex họ OpenAI trong phiên API chỉ đọc. Các phép kiểm chạy trong RAM bằng dữ liệu giả, không gọi mạng. Gate trên mã triển khai ở trạng thái `not_run`.

### Finding lượt 11 · Packet 1

| Mức | Finding | Trạng thái | Bằng chứng |
|---|---|---|---|
| P2 | §4b dòng 4 gộp kiểm đích và writer W2 | Đóng | `db_w2_bo_kiem_dich` chỉ bỏ `_kiem_dich_ghi`. Mô phỏng A/B giữ nguyên writer. Có chốt thì writer không được gọi, bỏ chốt thì writer nhận đích của fixture. |
| P2 | N1 đòi stderr ở biên trả tuple W3 | Đóng | Cả ba lượt W3 của N1 đo lý do trả về bằng `fullmatch`. Mẫu `<cụm>: .*` nhận chi tiết đã `repr` và loại chuỗi có tiền tố thừa hoặc xuống dòng thô. |
| P3 | Con trỏ phần dữ liệu W6 | Đóng | §2 và §7 trỏ đúng M7/N9w6 của packet 2. |

### Finding mới

| Mức | Packet | Finding |
|---|---|---|
| **P2** | **1** | **§4b dòng 14 đổi cả luật kho lẫn luật symlink.** M1 tìm kho từ `dirname(dich)`. Khi `HOME` chính là gốc kho `/K`, lời gọi chuẩn tìm từ `/K`, còn đột biến truyền `/K` làm `dich` nên cuộc tìm bắt đầu ở `/`. Tôi chạy nguyên thân `_trong_kho_git` của base với `lstat` giả trong RAM. Lời gọi chuẩn trả `nằm trong kho git`, đột biến cho qua. Với fixture N6(2), HOME thường ngoài kho và lá config là symlink, mô hình trả `là liên kết tượng trưng` ở bản chuẩn và cho qua ở bản đột biến. Vì vậy fixture dự kiến đỏ đúng nhãn `stderr` nhưng không chứng minh đột biến cô lập một cơ chế. Cần giữ nguyên đường đầu vào luật (a) và chỉ đổi việc kiểm lá config ở luật (b). |
| P3 | 1 | **§2 và M3 mô tả quá rộng việc giữ hành vi base khi tuần tự hoá W6 lỗi.** Với surrogate giả, `json.dump` của base ghi một phần JSON rồi ném `UnicodeEncodeError`. Biểu thức `json.dumps(...).encode(...)` của M3 ném cùng loại ngoại lệ trước khi gọi writer. Đo trong RAM xác nhận hai hành vi. Nên ghi rõ ngoại lệ vẫn lan ra, còn config cũ giữ nguyên byte nhờ thứ tự mới. |

Rà đủ 30 dòng §4b cho kết quả 26 H và 4 E. Bốn dòng E là 10, 11, 22 và 24. Tập khai gắn với từng lượt và hai dòng dùng chung dấu trên nhiều lượt đã liệt kê các lượt tương ứng. Ngoài dòng 14, tôi không thấy đột biến gộp chốt khác. Rà L1–L7, điểm chặn nằm ở phép phản chứng cô lập cơ chế của dòng 14. Các điều kiện quyền E2 vẫn chờ duyệt băm và ngoại lệ bundled trước cấp lease.

Packet 2 vẫn hoãn. Các finding UNC, surrogate ở biên env, khai ngoại lệ theo lượt, bảng Markdown và số lượt W6 đã ghi trong packet 2, không chặn verdict này. Phần W4/W5, reparse và kiểm dữ liệu W6 vẫn có ranh giới rõ giữa hai đặc tả.

Ước lượng 369–420 dòng để lại biên 30 dòng. Phép tính trong RAM cho 450 qua và 451 trượt. N13 vẫn cần đo `numstat` trên exact head triển khai. Lượt 12 đã chạm trần riêng của packet 1, nên dừng tại Review Rescue Checkpoint.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T08:21:13Z
