## Packet A · Issue #387 · Review lượt 8

Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Đặc tả A có SHA-256 `b65b89713dc04392e6e72aaa97f81d4dbfae2452c046ed67a5f4b13bf646dc8d`.

| Finding lượt 7 | Trạng thái | Bằng chứng |
|---|---|---|
| A · P2 · Ca (i) đỏ ở teardown trên Windows | **Đóng** | Ca (i) kiểm nền Linux trước khi dựng fixture. Cả 9 ca qua `_r387_chay` đều có chốt này. Chỉ (t) và (e) dùng phép dò giả trực tiếp và chạy trên mọi nền. Ca (i) xanh trên Linux, với `_nen_do_cay_truoc_bam()` được vá để mô phỏng nền khác. |
| A · P3 · Ca (i) bỏ lọt mốc lấy trước `unlink` | **Đóng** | Áp hai thay thế theo thứ tự M6, mỗi neo khớp đúng một lần tại lúc thay. Ca (i) đỏ đúng vế `moc ket_thuc phai lay SAU unlink ban chup: [True]`. Đột biến bỏ lấy lại mốc đỏ ở vế thời lượng, với `0.015` giây. |

## Finding mới

**A · P2 · N4 đòi `OK` cho một đột biến mà runner báo không đo được trên Linux.** N4 yêu cầu mọi mục `DOT_BIEN` còn lại sau bộ lọc nền đều `OK`, và chỉ nêu 5 mục `windows` của base. Nhưng `124_khi_chau_con_song` mang điều kiện `posix`, nên qua bộ lọc trên Linux, rồi ca đích `t62` tự bỏ qua vì cần fixture Windows. Lúc `09:10:37Z`, phép chạy hẹp với đúng mục này trong runner in `KHONG DO DUOC tren nen nay (ca dich bo qua: t62_qua_han_ma_khong_giet_het_cay_phai_tra_125)` và trả `(0, 1)`. Lệnh `--lap-ca t62_qua_han_ma_khong_giet_het_cay_phai_tra_125 --lan 1` xác nhận `0/1 qua, 1 bo qua, 0 hong`. N4 cần ghi ngoại lệ kế thừa này bên cạnh 5 mục bị bộ lọc nền loại, đồng thời giữ yêu cầu `OK` cho mọi mục đo được và đủ 18 đột biến mới của A. [Đặc tả A, N4](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP2/ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md:126) · [Mục đột biến ở base](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP2/.claude/dev/launcher_test.py:15689)

B chỉ được đối chiếu ranh giới. Đo native Darwin và Windows thuộc B. Không có finding B mới trong lượt này.

## Trần, luật dừng và L1–L7

- `git diff --no-index --numstat` lúc `09:10:50Z` xác nhận bản vá thử thêm `46 + 364 = 410` dòng trên hai tệp, còn 40 dòng dưới trần 450. §6 yêu cầu đo lại trên head thi hành, dừng nếu vượt trần hoặc cần sửa ngoài write set, và vào Review Rescue Checkpoint khi chạm trần lời gọi theo `ADR-0055`.
- L1, L2, L4, L5 và L7 không có finding mới. Với L3 và L6, điểm cần sửa là tập đột biến N4 dùng để kết luận đạt. N1 đỏ đúng `r387(a) cay chua chet ma khai None` khi ghép test vá thử với launcher base. Hai đột biến dò thừa và ngủ thừa đều đỏ đúng ở (e5).
- Phép đo hẹp trên Linux, Python 3.13.18, dùng bản sao trong RAM. Cả 11 ca A và `t117` đều xanh với `--lap-ca … --lan 1`. Bốn đột biến nền khác và đối chứng N1 đều đỏ với rc 1 đúng vế. Suite đầy đủ và phép đo native Windows/Darwin chưa chạy trong lượt này.

KET_LUAN: request_changes
tokens used
71,458
## Packet A · Issue #387 · Review lượt 8

Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Đặc tả A có SHA-256 `b65b89713dc04392e6e72aaa97f81d4dbfae2452c046ed67a5f4b13bf646dc8d`.

| Finding lượt 7 | Trạng thái | Bằng chứng |
|---|---|---|
| A · P2 · Ca (i) đỏ ở teardown trên Windows | **Đóng** | Ca (i) kiểm nền Linux trước khi dựng fixture. Cả 9 ca qua `_r387_chay` đều có chốt này. Chỉ (t) và (e) dùng phép dò giả trực tiếp và chạy trên mọi nền. Ca (i) xanh trên Linux, với `_nen_do_cay_truoc_bam()` được vá để mô phỏng nền khác. |
| A · P3 · Ca (i) bỏ lọt mốc lấy trước `unlink` | **Đóng** | Áp hai thay thế theo thứ tự M6, mỗi neo khớp đúng một lần tại lúc thay. Ca (i) đỏ đúng vế `moc ket_thuc phai lay SAU unlink ban chup: [True]`. Đột biến bỏ lấy lại mốc đỏ ở vế thời lượng, với `0.015` giây. |

## Finding mới

**A · P2 · N4 đòi `OK` cho một đột biến mà runner báo không đo được trên Linux.** N4 yêu cầu mọi mục `DOT_BIEN` còn lại sau bộ lọc nền đều `OK`, và chỉ nêu 5 mục `windows` của base. Nhưng `124_khi_chau_con_song` mang điều kiện `posix`, nên qua bộ lọc trên Linux, rồi ca đích `t62` tự bỏ qua vì cần fixture Windows. Lúc `09:10:37Z`, phép chạy hẹp với đúng mục này trong runner in `KHONG DO DUOC tren nen nay (ca dich bo qua: t62_qua_han_ma_khong_giet_het_cay_phai_tra_125)` và trả `(0, 1)`. Lệnh `--lap-ca t62_qua_han_ma_khong_giet_het_cay_phai_tra_125 --lan 1` xác nhận `0/1 qua, 1 bo qua, 0 hong`. N4 cần ghi ngoại lệ kế thừa này bên cạnh 5 mục bị bộ lọc nền loại, đồng thời giữ yêu cầu `OK` cho mọi mục đo được và đủ 18 đột biến mới của A. [Đặc tả A, N4](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP2/ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md:126) · [Mục đột biến ở base](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP2/.claude/dev/launcher_test.py:15689)

B chỉ được đối chiếu ranh giới. Đo native Darwin và Windows thuộc B. Không có finding B mới trong lượt này.

## Trần, luật dừng và L1–L7

- `git diff --no-index --numstat` lúc `09:10:50Z` xác nhận bản vá thử thêm `46 + 364 = 410` dòng trên hai tệp, còn 40 dòng dưới trần 450. §6 yêu cầu đo lại trên head thi hành, dừng nếu vượt trần hoặc cần sửa ngoài write set, và vào Review Rescue Checkpoint khi chạm trần lời gọi theo `ADR-0055`.
- L1, L2, L4, L5 và L7 không có finding mới. Với L3 và L6, điểm cần sửa là tập đột biến N4 dùng để kết luận đạt. N1 đỏ đúng `r387(a) cay chua chet ma khai None` khi ghép test vá thử với launcher base. Hai đột biến dò thừa và ngủ thừa đều đỏ đúng ở (e5).
- Phép đo hẹp trên Linux, Python 3.13.18, dùng bản sao trong RAM. Cả 11 ca A và `t117` đều xanh với `--lap-ca … --lan 1`. Bốn đột biến nền khác và đối chứng N1 đều đỏ với rc 1 đúng vế. Suite đầy đủ và phép đo native Windows/Darwin chưa chạy trong lượt này.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T09:11:31Z
