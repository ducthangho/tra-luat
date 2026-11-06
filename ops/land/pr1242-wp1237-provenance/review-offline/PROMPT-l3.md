# Cross-review wp1237 r1 — LƯỢT 3 (xác minh bản vá P3 của lượt 2), reviewer openai_codex, read-only với kho

Bạn là reviewer độc lập. Không sửa `cay-kho`. Được ghi trong thư mục sandbox hiện tại.

## Hiện vật
- `SPEC.md`, `LEASE.yaml`; `VERDICT_luot1.md`, `VERDICT_luot2.md` (lượt 2: approve, P3
  `retry-window-request-count-flakiness` ở vế D8).
- `cay-kho/` HEAD detached ở reviewed_sha `69dbf3af3c82bc6e1d6769666ca670bd706e80a5`, base `fe84620f…`.
- `diff.patch` (base→head), `diff_tu_luot2.patch` (4458d06a → head; CHỈ đổi vế D8 của t237), `numstat.txt`.
- `bang_dot_bien_executor.txt` + `mutation_runner_executor.py`: đo của executor ngoài sandbox, có HTTP loopback.
  Sandbox của bạn chặn socket; t237 HTTP là KHÔNG ĐO ĐƯỢC ở đây, không tính là lỗi sản phẩm.

## Việc
1. ĐỐI CHIẾU LƯỢT TRƯỚC: bản vá D8a/D8b có đóng P3 không? Lặp lại phản chứng SIGSTOP của bạn (`review_probes.py stall`
   ở lượt 2, dựng lại nếu cần) trên tham số mới: D8a đòi ≥ 8.5s với AL_RETRY=3, AL_RETRY_DELAY=3; D8b đòi ≤ 6 lần thử
   với AL_RETRY_DELAY=1, AL_RETRY_MAX_TIME=3. Máy chậm có còn làm bản ĐÚNG đỏ không? Máy NHANH bất thường có làm đột
   biến bỏ `--retry-delay` sống ở D8a không (curl lùi 1+2+4)?
2. Ba đột biến `bo_retry_delay`, `bo_retry_max_time`, `mac_dinh_retry_3` còn chết đúng vế không (đo bằng file:// được).
3. Bản vá có đẻ ra lỗi mới, hay đụng ngoài phạm vi (chỉ `ops/lease_publish_test.py`, chỉ trong t237) không.

## Đầu ra
`VERDICT.md`, GHI SỚM và cập nhật dần: `verdict:`, `reviewed_sha: 69dbf3af3c82bc6e1d6769666ca670bd706e80a5`, `## ĐỐI CHIẾU LƯỢT TRƯỚC`, `## BẢNG SĂN`
(LỆNH + OUTPUT thật), `## FINDINGS`. `changes_requested` chỉ khi có P0–P2 có bằng chứng chạy được.
