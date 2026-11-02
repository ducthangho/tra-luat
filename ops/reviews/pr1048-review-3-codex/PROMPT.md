# Cross-review lượt 3 — PR #1048 (sửa một bài học PowerShell trong CLAUDE.md), chấm ĐÚNG head đã merge

Bạn là REVIEWER độc lập (provider `openai_codex`), phiên mới. Executor là Claude. KHÔNG sửa `cay-kho/`.
Chỉ ghi vào thư mục sandbox này (`VERDICT.md`, tệp nháp nếu cần).

## Bối cảnh
PR #1048 ĐÃ merge (merge commit `b653574b117fa1496fbf58f09a22a8cbed5cc5dc`, cha thứ hai = head PR
`6f23a4e68805b4af3e2efe77be6e10b513843e93`). Lượt 2 (`VERDICT-luot-2.md`) approve trên `48b54d89b152871063c7296df33a60308667599e`;
sau đó executor merge master `5a174b958a05e13f5c9a968a2596ca37267d0466` vào nhánh, tạo `6f23a4e`. Lượt này tồn tại để có một verdict
trên ĐÚNG SHA đã merge (protocol §8.1 đòi review exact SHA). Đây KHÔNG phải phê duyệt merge/land.

## Neo
- `cay-kho/` là clone đầy đủ, HEAD phải = `6f23a4e68805b4af3e2efe77be6e10b513843e93`
  (kiểm `git -C cay-kho rev-parse HEAD`; lệch thì `verdict: blocked`).
- Base của diff: `5a174b958a05e13f5c9a968a2596ca37267d0466` (= merge-base của head với master lúc merge, và là cha thứ nhất của
  `6f23a4e`). `diff.patch` = `git diff 5a174b9 6f23a4e` (1 tệp `CLAUDE.md`, +10/−1). Tự kiểm lại diff khớp byte.
- Không có đặc tả đóng băng: thay đổi do chủ kho yêu cầu trực tiếp trong phiên.
- `VERDICT-luot-1.md` (16e992a, 1 P2) và `VERDICT-luot-2.md` (48b54d8, approve) là verdict cũ; `ca_if_windows.txt` là lời khai
  đo của executor trên Windows (bạn không tái lập được trên Linux).

## Việc
1. Xác nhận phần đổi giữa `48b54d8` và `6f23a4e`: `git diff 48b54d8 6f23a4e -- CLAUDE.md` phải rỗng; các tệp khác đổi giữa hai
   SHA phải đến từ master (`5a174b9`), không phải từ executor. Nếu có bất cứ thay đổi nào của executor ngoài `CLAUDE.md`, nêu.
2. Review LẠI TOÀN BỘ `diff.patch` trên hai trục **Spec** và **Standards/Security**, như lượt 2, trên cây `6f23a4e`:
   - từng mệnh đề trong đoạn mới có kiểm được trong kho không (lời khai về `scripts/deploy-package.ps1`; quét LỚP mọi `.ps1`
     có mẫu `[string](Get-Content … -Raw …)` thiếu chốt `$null`; tham chiếu `ADR-0057`, `KHOA.txt`);
   - master mới đưa vào có làm câu nào trong đoạn sửa thành SAI hoặc mâu thuẫn với chỗ khác của `CLAUDE.md`/`docs/` không
     (ví dụ một tệp `.ps1` mới, một ADR mới, một sửa đổi khác trong mục "PowerShell — 3 bẫy đã trả giá");
   - định dạng danh sách (thụt lề, `·`) của mục ấy còn nguyên không.
   Phần hành vi PowerShell: nếu không chạy được PowerShell trong sandbox, ghi `KHÔNG ĐO ĐƯỢC`, đừng suy.
3. Chạy trong `cay-kho/` (dùng `python3`, `PYTHONDONTWRITEBYTECODE=1`):
   - `python3 .claude/dev/packet_loop.py doctrine-scan --root .` (rc phải 0)
   - `python3 .claude/dev/packet_loop.py adr-song --root .` (rc phải 0)
   - `python3 scripts/tl.py doc-claims-check --json` (`ok` phải true)
   Ghi lệnh, rc, dòng kết quả thật.

Mức: P0 · P1 (sai sự thật/sai luật) · P2 (lời khai thiếu/sai có hậu quả) · P3 (nhỏ, sửa được). Chỉ báo finding có bằng chứng.

## Đầu ra: `VERDICT.md` trong thư mục sandbox này
Dòng 1: `verdict: approved` | `verdict: changes_requested` | `verdict: blocked`.
Dòng 2: `reviewed_sha: 6f23a4e68805b4af3e2efe77be6e10b513843e93`.
Dòng 3: `Kết quả: N P0, N P1, N P2, N P3.`
Mỗi finding: `### <slug> [P*]` — vị trí, bằng chứng, đề xuất sửa cụ thể. Có mục `## ĐỐI CHIẾU LƯỢT TRƯỚC` (finding lượt 1 còn
đóng không trên `6f23a4e`). Cuối: `## Đã chạy` (lệnh + rc). `approved` chỉ khi 0 P0–P3.
