# Cross-review wp1237 r1 — LƯỢT 2 (xác minh bản vá), reviewer openai_codex, read-only với kho

Bạn là reviewer độc lập. Không sửa `cay-kho`. Được ghi trong thư mục sandbox hiện tại.

## Hiện vật
- `SPEC.md` (sha256 b0e12304…), `LEASE.yaml`.
- `cay-kho/` HEAD detached ở reviewed_sha `4458d06a8180d5d74f5c786a57b1c5a3176540d9`, base `fe84620f…`.
- `diff.patch` (base→head), `diff_tu_luot1.patch` (43258fbe lượt 1 → head), `numstat.txt`.
- `VERDICT_luot1.md` — verdict lượt 1 của bạn (changes_requested, finding P2 `retry-max-time-decimal-equivalence`,
  kèm dự đoán ba đột biến SỐNG: bỏ `--retry-delay`, bỏ `--retry-max-time`, hạ mặc định 8→3).
- `bang_dot_bien_executor.txt`, `mutation_runner_executor.py`, `t237_executor_3lan.txt` — đo của executor NGOÀI sandbox
  (có HTTP loopback). Lượt 1 sandbox của bạn chặn socket nên HTTP t237 là KHÔNG ĐO ĐƯỢC; đó là giới hạn môi trường,
  đừng tính là lỗi sản phẩm. Bạn có thể đo bằng `file://` như lượt 1 (repro_max_time).

## Việc
1. ĐỐI CHIẾU LƯỢT TRƯỚC: finding P2 đã sửa đúng chưa? Chạy lại repro của bạn (1/00001/08/0099/000300/0001800
   ⇒ rc0; 0/00000/1801/0001801/18446744073709551617/abc/rỗng ⇒ rc13) trên head mới.
2. Bản vá có đẻ ra lỗi mới không: phép bỏ số 0 đứng đầu bằng `${x#"${x%%[!0]*}"}` dưới `set -u`, chuỗi toàn 0,
   tràn số sau chuẩn hoá, `10#` với chuỗi rỗng.
3. Các vế mới D7/D8 và việc bắt `TimeoutExpired` trong `chay`: có làm ca xanh rỗng, chập chờn (D8 đòi 5..8 yêu
   cầu với cách 1s, trần 6s), hay che lỗi không? Đánh giá biên an toàn trên runner chậm (Windows Git Bash).
4. Phạm vi: 2 tệp, ≤250 dòng thêm (numstat), test chỉ THÊM, không đụng workflow.
5. Săn thêm ≥4 hướng độc lập, mỗi hướng LỆNH + OUTPUT thật.

## Đầu ra
`VERDICT.md` trong thư mục hiện tại, GHI SỚM và cập nhật dần. Dạng như lượt 1:
`verdict:` (approve | changes_requested | blocked), `reviewed_sha: 4458d06a8180d5d74f5c786a57b1c5a3176540d9`,
`## ĐỐI CHIẾU LƯỢT TRƯỚC`, `## BẢNG SĂN`, `## FINDINGS` (slug kebab, hạng P0–P3, TỆP/DÒNG, ĐÃ THỬ NGHIỆM, ĐỘ TIN).
`changes_requested` chỉ khi có P0–P2 có bằng chứng chạy được. P3 không chặn.
