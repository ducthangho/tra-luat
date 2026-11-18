# WP1319 r4 — Kết quả chạy native (DỞ DANG: chưa đọc được kết quả)

Trạng thái lúc 2026-11-18 khoảng 10:50Z: **chưa có kết quả nào được đọc về. Không hàng nào trong ma trận được đổi theo r4.**

## Đã làm
- **Executor:** Codex, 3/3 lời gọi (hết ngân sách Codex).
  - Lượt 1: run `702483193dcc4d1a9c84e1614e20f971` viết harness.
  - Lượt 2: run `bf2e3d3b13424128b1c5c6462bdff5ab` sửa 18 mục theo `VERDICT-code.md`.
  - Lượt 3: run `03452cd18f894432a7753243c8fa55a9` sửa 2 lỗi do phiên điều phối phát hiện khi đối chiếu bản sửa:
    - D3 bị chặn bởi kiểm cổng 19222 trong khi chính Proxima của ca C đang giữ cổng đó;
    - ảnh chụp tiến trình lúc thoát có timeout 5 s.
- **Review mã:** lượt 1/2, `request_changes` (xem `VERDICT-code.md`).
  - Phiên điều phối tự đối chiếu diff bản sửa với từng mục P0/P1.
  - **Chưa** có review độc lập trên bản sửa. Việc này dồn sang lượt review 2/2 (review gói sau khi chạy).
- **Harness chạy trên ASUS:** sha256 `3e55da30197af857d476bed31b442e377f816d7d2cb7c3b559fb49279cec6556`, `test_r4_pure.py` `b73b6cc3…`, `r4_freeze.py` `ed7c1fa3…`.
  - Đã chép bằng zip base64 `0f373a77…`; băm từng tệp trên ASUS khớp.
  - Unittest trên Windows (Python 3.13.1): 16/16 đạt.
- **Đầu vào trích từ zip P4** (chỉ đọc, chép vào `inputs\`):
  - `export-manifest.json` sha256 `99cfbaf4…`;
  - tệp suy ra `p4-code-expected.json` `4298cf46…` (15 tệp: 13 `code` + 2 `parent`).
- **Lượt chạy:** bắt đầu 2026-11-18T10:23:32Z, pid 25068.
  - Khoá `D:\tl-win\KHOA.txt` được ghi đúng định dạng ADR, hạn 11:23:32Z.
  - Các mốc quan sát được qua Desktop Commander:
    - 10:26Z: bản sao 3226 tệp đã chép xong lên `C:\Users\admin\tl-work\wp1319-r4\copy`. Tức là bước kiểm `baseline` gốc **không** STOP.
    - 10:28Z: `results\C.stdout` và `C.stderr` đã tạo; 4 tiến trình `Proxima.exe` và 2 `python.exe` chạy từ bản sao. Tức là P0/A/B1/B2 đã chạy xong. Kết quả của chúng chưa đọc được.
  - Từ khoảng 10:31Z, Desktop Commander trên ASUS ngừng nhận lệnh; khoảng 10:46Z máy chuyển **Offline**.

## Chưa biết (`KHONG_do_duoc`)
- Kết quả của P0, A, B1, B2, C, D và `result.json`.
- Khoá đã được nhả hay chưa. Phiên điều phối **không** đụng vào khoá. Theo ADR, khoá tự hết hạn lúc 11:23:32Z.
- Máy offline vì ngủ, mất mạng hay quá tải.

## Finding của phiên điều phối (cho lượt chạy lại)
- **F-r4-1:** harness **không** gọi `SetThreadExecutionState(ES_CONTINUOUS|ES_SYSTEM_REQUIRED)` như `run_activation.py` của P4 (dòng 14–16). Laptop có thể ngủ giữa ca C, làm treo lượt đo và sai các phép đo theo thời gian.
  - Đã hết ngân sách Codex nên chưa sửa.
  - Lượt chạy lại cần chủ kho cấp thêm ngân sách Executor, hoặc ghi nhận điều kiện "máy được giữ thức" trong lúc chạy.

## Việc còn lại
1. ASUS online trở lại: đọc `results\result.json` (hoặc `result-stop-*.json`), `run-transcript.*`, và trạng thái khoá. Không tự xoá khoá.
2. Nếu lượt chạy trọn: chạy `r4_freeze.py`, review 2/2, rồi cập nhật MATRIX.
3. Nếu lượt chạy dở vì máy ngủ: giữ nguyên hiện vật dở, ghi FAIL hoặc `not_measured`. Chạy lại 1 lần trong ngân sách native, sau khi xử lý F-r4-1.
