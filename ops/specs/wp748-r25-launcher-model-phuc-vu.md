# WP748 r25/g25 — `launcher.py run` ghi model do máy chủ trả cho từng response của lượt codex

## Thẩm quyền và nguồn gốc

Chủ kho cấp packet ở https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6378484722 (OWNER, 2026-10-24T01:59:43Z).
Executor: Claude Code (`anthropic_claude`, `claude_code`, remote Linux). Reviewer: phiên Codex độc lập chỉ đọc qua
`launcher.py run`, neo đúng head cuối. Review Class `sensitive`. Base `origin/master`
`1c20f3b` (đầy đủ ở lease).

Vì sao cần: các packet r21–r24 đều kết thúc `landed: false` vì `run.json` của `launcher.py run` không có khoá model nào
⇒ họ model reviewer `khong_do_duoc` (`docs/PROTOCOL_DA_PHIEN.md` §8, §8.1). Đo 24-10-2026 (codex-cli 0.163.0):
- `codex exec --json` không phát sự kiện nào mang model; rollout `~/.codex/sessions/*.jsonl` chỉ có model CẤU HÌNH
  (`turn_context`, `thread_settings`), `token_usage_record` có `response_id` nhưng không có model; `~/.codex/logs_2.sqlite` rỗng.
- Bật `RUST_LOG=trace`: mỗi khung máy chủ gửi `response.created` / `response.completed` (target
  `tungstenite::protocol`, dòng `Received message {...}`) mang `response.id` và `response.model`. Đây là nguồn đo.
- Log trace thô chứa thông tin xác thực (đo được 13 dòng nhắc `authorization`, 2 dòng `bearer`); tệp đo thử đã xoá.
- Header `x-codex-safety-buffering-faster-model` có mặt ⇒ không được giả định mọi response cùng một model.

## Write set hiệu lực

1. `.claude/dev/launcher.py`
2. `.claude/dev/launcher_test.py`

## Hợp đồng

1. **Nguồn duy nhất:** trường `model` của đối tượng `response` trong sự kiện `response.created` hoặc `response.completed`
   do máy chủ gửi. Không suy từ `-m`, `turn_context`, header CLI hay tên chương trình.
2. **Không chạm đĩa:** khi `launcher.py run` bật đo cho lượt codex, dòng trace của con KHÔNG được ghi vào bất kỳ tệp nào
   (kể cả `stderr.log`, tệp tạm, `run.json`); chỉ `{response_id, model}` được giữ trong bộ nhớ rồi ghi vào sổ. Dòng không
   phải trace vẫn vào `stderr.log` như cũ. Cách bật trace phải hẹp nhất có thể (target cụ thể), và hẹp không thay được lọc.
3. **Sổ:** `run.json` thêm `model_phuc_vu` = danh sách `{response_id, model, su_kien}` theo thứ tự đến (khử trùng theo
   `response_id` + `model`), và `model_phuc_vu_trang_thai` ∈ {`DO_DUOC`, `KHONG_DO_DUOC`}. Không thấy sự kiện nào ⇒
   `KHONG_DO_DUOC` kèm lý do; nhiều model khác nhau ⇒ ghi đủ, không gộp, không chọn "model chính". Lệnh không phải codex ⇒
   không đo, không có khoá hoặc ghi rõ `KHONG_DO_DUOC` (không đổi hành vi cũ của lượt khác).
4. **Không đo ngược:** không sửa biên nhận/hồ sơ cũ.
5. **Không yếu hơn hiện tại:** mọi chốt cũ của `lenh_run` (giết cây khi quá hạn, mã 124/125, Job Object Windows, ghi sổ
   `stdout_byte`/`stderr_byte`/sha256, neo prompt) giữ nguyên hành vi; đọc ống stderr không được làm treo lượt chạy khi con
   hoặc cháu còn giữ ống.

## Chấp nhận

- Ca test dùng con GIẢ (không gọi mạng, không credential thật) in khung trace giả có chuỗi bí mật mẫu: chứng minh
  `run.json`, `stdout.log`, `stderr.log` và thư mục lượt chạy KHÔNG chứa chuỗi ấy; `model_phuc_vu` đúng từng response;
  ca không có sự kiện ⇒ `KHONG_DO_DUOC`; ca hai model ⇒ ghi cả hai; ca quá hạn vẫn 124/125 đúng.
- Mỗi chốt mới có đột biến riêng làm ca đích ĐỎ (gỡ lọc trace ⇒ ca bí mật đỏ; suy model từ `-m` ⇒ ca không sự kiện đỏ).
- `launcher_test.py` N/N trên Linux; lane Windows (`launcher-windows.yml`, nhãn `windows`) chạy và xanh.
- Một lượt `launcher.py run` thật với codex cho `model_phuc_vu_trang_thai: DO_DUOC`, và quét bí mật thư mục lượt chạy sạch.
- Trong trần `sensitive` ADR-0053 (≤ 6 tệp, ≤ 450 dòng thêm); vượt ⇒ dừng, hỏi chủ kho.
- Codex review qua `launcher.py run` trên head cuối: 0 P0/P1/P2; chủ kho duyệt trên SHA cụ thể trước merge.

## Dừng

Dừng và báo khi: người giữ chồng lấn; cần ghi ngoài write set; không tìm được cách bật trace mà lọc được hết bí mật;
codex đổi định dạng khiến nguồn đo biến mất; hoặc thiếu bằng chứng dương.
