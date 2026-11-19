# WP1319 r4 — Thiết kế các ca native trên Proxima thật (NHÁP, chờ chủ kho duyệt)

Trạng thái: **nháp, chưa có lease, chưa thi công**. Đây là "thi công mới" vì cần **mã operator mới**: một harness nhỏ do Executor (Codex) viết và reviewer độc lập review, đúng theo protocol.
Mọi ca chạy trên **profile thử**, egress bị chặn (proxy Deny như P4), không inference, không đăng nhập, không đụng gateway VM.
Căn cứ đọc mã (chỉ đọc) trong P4 đã đóng băng: `run_activation.py` `6004fcea…` trên ASUS.
- Dòng 23: khoá host là `assert lock.tell()==0,'HOST_BUSY'`, tức **dừng**, không hoãn.
- Dòng 41–46: feed nội bộ chỉ phục vụ `version: 5.5.0`.
- Dòng 72–90: trước khi tạo tiến trình, kiểm manifest từng tệp của biến thể (`assert s256…==row['sha256']`) rồi lấy `VerifiedReadLease`.

## Ca đề xuất

| Ca | Hàng | Cách đo | PASS | Loại bằng chứng |
|---|---|---|---|---|
| **R4-A** artifact hỏng | §11 #6 vế âm | Chép biến thể `baseline` ra thư mục tạm, sửa 1 byte trong 1 tệp có trong manifest. Gọi đúng đường kiểm của `run()` | Từ chối **trước** `process_creation_attempted`. Không có `Proxima.exe` nào chạy từ bản hỏng. Thư mục gốc không đổi | real_os (OS thật, tệp thật). Chưa dùng tới Proxima |
| **R4-B** artifact sai nguồn | §11 #6 vế âm | Như R4-A nhưng thay 1 tệp bằng tệp khác kích thước, hoặc thêm tệp lạ | Từ chối trước khi kích hoạt | real_os |
| **R4-C** updater có bản mới | U4 | Chạy biến thể `baseline` 45 s trên profile thử, feed khai `version: 5.5.1` kèm installer có `sha512` sai | Ghi đủ: có request tới feed, có request tải installer, và bị từ chối do sai integrity. **Không** có cài đặt khi thoát. Binary và ASAR sau chạy trùng byte | real_os (Proxima + electron-updater thật), offline |
| **R4-D** updater chạy trùng | §11 #7 vế electron-updater | Trong R4-C, mở song song lần kích hoạt thứ hai cùng profile thử | Lần thứ hai bị từ chối (khoá host hoặc khoá single-instance), không hỏng dữ liệu | real_os |

## Không đưa vào r4 (cần quyết định khác)
- **"Máy bận thì hoãn"** (§11 #7): mã hiện chỉ **dừng**. Muốn "hoãn" phải đổi thiết kế operator. Hoặc chủ kho chấp nhận "dừng, chờ người chạy lại" là đủ cho tiêu chí này.
- **Promotion fence** (§11 #8): cần hai máy và một bộ điều phối kiểm kết quả máy đầu trước khi chạy máy sau. Đây là thiết kế riêng, không làm trong r4.
- U8 đăng nhập, NSIS thật, migration, LIVE: xem `DESIGN.md`.

## Ràng buộc thi công
- Máy: ASUS, khoá `D:\tl-win\KHOA.txt`. **D: chỉ còn ~1,6 GB.** Bản sao biến thể (~3226 tệp) phải nằm trên C:, ước chừng vài trăm MB. Kiểm dung lượng trước khi chạy.
- Mã: harness mới **không** sửa các tệp P4 đã đóng băng; chỉ import hoặc gọi chúng. Băm mọi tệp trước và sau.
- Vai: Executor là Codex (viết harness). Reviewer độc lập, chỉ đọc, effort cao hơn. Operator là phiên điều phối.
- Ngân sách đề xuất: Codex ≤ 3 lời gọi (1 viết + 2 sửa), review ≤ 2, native 1 lượt + 1 lần chạy lại mỗi ca khi lỗi dựng.
