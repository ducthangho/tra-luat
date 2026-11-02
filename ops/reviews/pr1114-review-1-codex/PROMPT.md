# Cross-review PR #1114 — cloud_agent_creds_test đưa payload node qua stdin (WinError 206), lượt 1

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox (làm việc trên BẢN SAO tạm khi cần đột biến).

## Đầu vào trong sandbox
- `cay-kho/` — clone, detached ở head ứng viên `e101b11e9586de3125f811ec4f42a89af69de8f2`, đủ `refs/remotes/origin/*`. Base = `165b27a4bfe02e81af7bc94bda1e71c10d8c38e4` (merge-base với master).
  `git diff --name-only 165b27a4bfe02e81af7bc94bda1e71c10d8c38e4 HEAD` chỉ được chạm `ops/cloud_agent_creds_test.py`.
- `DIFF.patch` = `git diff 165b27a..HEAD`.

## Bối cảnh (lời khai của executor — KIỂM, đừng nhận)
Lượt Windows `41283928240` đỏ ở `p3b4_co_blob`: `FileNotFoundError: [WinError 206] The filename or extension is too long`. Lời khai: `chay_b` truyền
payload JSON qua argv cho `node`; ca 65536 byte base64 ~87K ký tự vượt trần dòng lệnh 32767 ký tự của Windows (CreateProcess). Bản vá đọc
payload bằng `require('fs').readFileSync(0, 'utf8')` trong `JS_GIA` và truyền bằng `input=` trong `chay_b`. Không có Windows trong sandbox.

## Việc của bạn — ĐO, đừng đọc
1. `PYTHONDONTWRITEBYTECODE=1 python3 ops/cloud_agent_creds_test.py` trên head và trên base (bản sao riêng): số CA, số ĐỘT BIẾN, TONG. So delta.
   Mọi ca/đột biến đạt trên base phải đạt trên head.
2. Tái hiện trần Windows trên Linux: dựng một wrapper `node` giả (đặt trước trên PATH của bản sao) từ chối mọi lời gọi có tổng độ dài dòng lệnh
   > 32767 ký tự rồi gọi node thật. Base phải ĐỎ ở `p3b4_co_blob`, head phải xanh. Ghi lệnh + output.
3. Còn đường nào khác trong `ops/cloud_agent_creds_test.py` (hoặc mã nó gọi) truyền dữ liệu lớn qua argv mà bản vá bỏ sót? Liệt kê từng `subprocess`
   và ước lượng độ dài argv lớn nhất có thể (đo, không đoán).
4. Ngữ nghĩa: stdin có bị dùng cho mục đích khác bởi mã `.gs` được trích (`_trich_gs`) hoặc `JS_CHAY` không; mã hoá UTF-8 hai đầu; trường hợp payload rỗng.
   Đột biến: (a) bỏ `input=` ⇒ ca phải ĐỎ; (b) đổi `readFileSync(0` thành đọc argv ⇒ ĐỎ. Ghi kết quả.
5. `python3 -m ruff check --select F ops/cloud_agent_creds_test.py` và `git diff --check 165b27a HEAD`.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: e101b11e9586de3125f811ec4f42a89af69de8f2`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
