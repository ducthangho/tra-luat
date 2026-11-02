# Cross-review lượt 2 — PR #1048 (sửa một bài học PowerShell trong CLAUDE.md)

Bạn là REVIEWER độc lập (provider `openai_codex`), phiên mới. Executor là Claude. KHÔNG sửa `cay-kho/`.
Chỉ ghi vào thư mục sandbox này (`VERDICT.md`, tệp nháp nếu cần).

## Neo
- `cay-kho/` là clone đầy đủ, HEAD phải = `48b54d89b152871063c7296df33a60308667599e`
  (kiểm `git -C cay-kho rev-parse HEAD`; lệch thì `verdict: blocked`).
- Base: `8cdb15a786304bab084b43c8b30c127ae87e2594`. Diff: `diff.patch` (1 tệp `CLAUDE.md`, +10/−1).
- Không có đặc tả đóng băng: thay đổi do chủ kho yêu cầu trực tiếp trong phiên. Mô tả PR (ngữ cảnh, không phải
  bằng chứng đã kiểm): bài học cũ khuyên "ép `[string]`" khi `Get-Content -Raw` đọc tệp rỗng trả `$null`. Executor khai
  đã đo trên Windows (PS 5.1.26100 và 7.6.9, tệp 0 byte và tệp chỉ có BOM `EF BB BF`):
  `[string](Get-Content -Raw …)` vẫn `$null`; `[string]$x = Get-Content -Raw …` và `'' + (Get-Content -Raw …)` ra `""`.

## Việc
Review hai trục **Spec** (đoạn sửa có nói đúng và đủ điều nó muốn nói) và **Standards/Security**:
1. Từng mệnh đề trong đoạn mới có kiểm được trong kho không. Đặc biệt:
   - lời khai về `scripts/deploy-package.ps1` (dòng ép `[string]` và dòng `if ($null -eq $txt)` ngay sau): đọc tệp, đối chiếu;
   - mọi `.ps1` khác trong kho có dùng mẫu `[string](Get-Content … -Raw …)` mà KHÔNG có chốt `$null` theo sau không — nếu có,
     bài học mới có hệ quả với mã đó; nêu tên (đây là quét LỚP, không chỉ một biểu hiện);
   - câu về `ErrorActionPreference = 'Continue'` và `if` ném lỗi: có diễn đạt đúng ngữ nghĩa PowerShell không (nếu bạn
     không chạy được PowerShell trong sandbox, nói rõ `KHÔNG ĐO ĐƯỢC` cho phần hành vi, đừng suy).
   - tham chiếu `ADR-0057`, `KHOA.txt`: có tồn tại trong kho không.
2. Đoạn mới có mâu thuẫn với chỗ khác trong `CLAUDE.md` hay `docs/` không; có làm hỏng định dạng danh sách
   (thụt lề, gạch đầu dòng `·`) của mục "PowerShell — 3 bẫy đã trả giá" không.
3. Chạy trong `cay-kho/` (dùng `python3`, `PYTHONDONTWRITEBYTECODE=1`):
   - `python3 .claude/dev/packet_loop.py doctrine-scan --root .` (rc phải 0)
   - `python3 .claude/dev/packet_loop.py adr-song --root .` (rc phải 0)
   - `python3 scripts/tl.py doc-claims-check --json` (`ok` phải true)
   Ghi lệnh, rc, dòng kết quả thật.

Mức: P0 · P1 (sai sự thật/sai luật) · P2 (lời khai thiếu/sai có hậu quả) · P3 (nhỏ, sửa được). Chỉ báo finding có bằng chứng.

## Đầu ra: `VERDICT.md` trong thư mục sandbox này
Dòng 1: `verdict: approved` | `verdict: changes_requested` | `verdict: blocked`.
Dòng 2: `reviewed_sha: 48b54d89b152871063c7296df33a60308667599e`.
Dòng 3: `Kết quả: N P0, N P1, N P2, N P3.`
Mỗi finding: `### <slug> [P*]` — vị trí, bằng chứng, đề xuất sửa cụ thể. Cuối: `## Đã chạy` (lệnh + rc).
`approved` chỉ khi 0 P0–P3.

## Lượt trước
`VERDICT-luot-1.md` (reviewed `16e992a`) có 1 P2 `continue-thieu-pham-vi-loi`. Executor đã chạy ĐÚNG ba ca bạn đề xuất,
trên cả PS 5.1 lẫn 7.6 (kết quả trong `ca_if_windows.txt` — lời khai của executor, bạn không tái lập được trên Linux),
rồi sửa câu theo kết quả: `diff-tu-luot-1.patch`. Kiểm finding đã đóng thật chưa (câu mới có khớp bảng kết quả, có còn
phát biểu rộng hơn phép đo không), rồi review LẠI TOÀN BỘ diff.
