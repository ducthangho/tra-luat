verdict: approve
reviewed_sha: 45a06e4872d165aabc1a7078edaf3281490d6b0d

## Findings

Không có finding P1/P2/P3.

Điều kiện so khớp toàn bộ `nhat_ky` đã đóng lớp thiếu/thừa/sai thứ tự/sai argv/sai kwargs. Khối `(3c2)` gọi trực tiếp vẫn được `gia_run` kiểm hình dạng từng lời gọi; các đường `_do_github_api` đều qua `goi_api` và được so cả trace.

`gh` vẫn chỉ ảnh hưởng mô tả, không thể nâng hoặc hạ nhãn `github-api`; tầng tiêu thụ vẫn fail-close khi yêu cầu khả dụng.

Phép đo injection đã được dựng độc lập:

- `claude mcp add`: rc=0.
- `claude mcp get probe`: rc=0.
- Có đúng 2 dòng `Status:`.
- Bản thật `Status: × Failed to connect` ở dòng 3.
- Bản chèn `Status: √ Connected` ở dòng 8.

Vì vậy `.search` lấy bản thật đứng trước.

Không tìm thấy đột biến sống sót vì điều kiện trace đã đóng được lớp đang xét, không phải vì hết hướng: tôi thử thêm hai biến đổi mới ở hai nhánh khác nhau và cả hai đều bị giết.

Bản vá đã tới ngưỡng land; không còn danh sách điều kiện bắt buộc nào cần đóng trong phạm vi lease này.

## Phép đo đã chạy

- SHA-256 prompt: `96359883a79007596be7d6b3310f9878403dd00ba3d1ef80d977f4c6b5254e22` — khớp lease.
- `TMPDIR=/dev/shm python3 .claude/dev/launcher_test.py`
  - `105/105` ca; qua 104, bỏ qua 1, hỏng 0.
- `TMPDIR=/dev/shm python3 .claude/dev/launcher_test.py --dot-bien`
  - `85/85` đột biến đo được đều bị giết; 1 không đo được trên nền POSIX.
- Master `e38b0be` trên bản sao đầy đủ:
  - Suite: `104/104`; qua 103, bỏ qua 1, hỏng 0.
  - Đột biến: `61/61`; 1 không đo được.
- Delta ca đỏ: `0`.

Hai đột biến tự nghĩ trên bản sao tạm:

- `gh timeout=20` → `timeout=30`: `t105` đỏ vì lời gọi không khớp đặc tả.
- `if shutil.which("gh")` → `if shutil.which("gh") and co_khai`: `t105` đỏ ở nhánh chưa khai; mong `[gh]`, đo được `[]`.

Cả hai: `0/1` qua, `1` hỏng.
