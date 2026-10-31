# Cross-review lượt 2 (độc lập, bổ sung assurance §8.1/§8.2 sau merge) — packet `WINDOWS-LOCAL-MAY-CHU-KHO` r2 g1 (mission #748)

Ghi chú bối cảnh: head này đã merge (PR #1029, merge `eaf83fd`). Lượt 1 (run `83f0f266`) approve nhưng biên nhận thiếu
snapshot đầu/cuối §8.2, nên chủ kho cho một lượt review độc lập mới. Bạn KHÔNG được xem verdict lượt 1; tự review lại
từ đầu. Phiên điều phối chụp snapshot `cay-kho/` trước và sau lượt của bạn, ngoài thư mục sandbox.

Bạn là REVIEWER độc lập (provider `openai_codex`), phiên mới. Executor là Claude; bạn KHÔNG sửa
`cay-kho/`. Ghi duy nhất vào thư mục sandbox này (`VERDICT.md`, tệp nháp nếu cần).

## Neo
- Kho: `cay-kho/` (clone đầy đủ, không shallow), HEAD phải = `9aa725c72b6b38263de366ce34a80fb384a522a0`.
  Kiểm bằng `git -C cay-kho rev-parse HEAD`; lệch thì dừng và ghi `verdict: blocked`.
- Base: `5f3855eaf47e024b6c63f8923f64d8f80c5de707`. Diff: `diff.patch` (= `git diff base HEAD`).
- Đặc tả đóng băng: `cay-kho/ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r2.md`, sha256 phải =
  `4c92ecbf38fb7f5f97ddea64ed4a43f1cbc9e7a826e87fd8c234dc7e25677c2b`.
- Lease: `lease.yaml` (effective_review_class `sensitive`, write set 2 tệp).
- Protocol: `cay-kho/docs/PROTOCOL_DA_PHIEN.md` (§8 review, §10.2, §20). ADR bị sửa: `docs/adr/0057-*.md`.
  Khuôn "ADR sửa đúng một điểm của ADR khác": `docs/adr/0056-*.md` (với ADR-0017).

## Việc
Review hai trục **Spec** và **Standards/Security**:
1. Diff có làm ĐÚNG và ĐỦ §2 đặc tả không: ADR-0058 có đủ phạm vi theo `list_devices`, khoá/sổ đo theo máy
   (`D:\tl-win\` hoặc `C:\tl-win\`, `ghi_chu` `may=…`), hạn khoá ≤ 2 giờ, gia hạn, ba trường hợp hết hiệu lực
   (a)/(b)/(c) kèm yêu cầu bằng chứng cho (c), thứ tự tiếp nhận, cấm dừng tiến trình phiên khác? Bảng D7–D9 chép
   đúng số liệu §1? Mục "không cổng nào cưỡng chế"? §20: đúng một dòng ADR-0058 với cột cổng
   `không cổng — kỷ luật executor`, và ô mô tả ADR-0057 nêu "phạm vi và khoá sửa bởi ADR-0058" (chỉ sửa ô ấy)?
   Câu con trỏ §10.2 nhắc cả 0057 lẫn 0058 và vẫn TRUNG TÍNH (không tạo nghĩa vụ — đây là finding P1 lượt 1 của
   r1)? Có luật nào ADR-0058 nói mạnh hơn/rộng hơn đặc tả, hoặc mâu thuẫn ADR-0057 ở các điểm được giữ nguyên?
2. Tiêu chí §3/§4: chạy trong `cay-kho/` (dùng `python3`):
   - `python3 .claude/dev/packet_loop.py adr-song --root .` (rc phải 0)
   - `python3 .claude/dev/packet_loop.py doctrine-scan --root .` (rc phải 0)
   - `python3 scripts/tl.py doc-claims-check --json` (`ok` phải true)
   - đếm tệp/dòng thêm của diff (≤ 2 tệp, ≤ 120 dòng thêm), tệp nằm trong write set, không chạm `docs/adr/0057-*`.
   Ghi lệnh, rc và dòng kết quả thật.
3. Tính đúng của các lời khai trong ADR: tham chiếu chéo (§ số của ADR-0057, tên tệp, PR/issue, SHA, session) có
   tồn tại/khớp không; lời khai "những gì KHÔNG đổi" có mâu thuẫn ADR-0057/protocol không; câu nào tự mâu thuẫn
   hoặc mơ hồ đến mức executor đọc ra hai nghĩa. Khái quát mỗi lỗi thành LỚP và quét mọi biểu hiện cùng lớp.

Mức độ: P0 (chặn tuyệt đối) · P1 (sai luật/sai spec) · P2 (thiếu/sai lời khai có hậu quả) · P3 (nhỏ, có
thể sửa). Chỉ báo finding có bằng chứng (dòng tệp + lệnh/đối chiếu).

## Đầu ra: `VERDICT.md` trong thư mục sandbox này
Ghi tăng dần. Dòng 1: `verdict: approved` hoặc `verdict: changes_requested` (hoặc `blocked`).
Dòng 2: `reviewed_sha: 9aa725c72b6b38263de366ce34a80fb384a522a0`.
Dòng 3: `Kết quả: N P0, N P1, N P2, N P3.`
Sau đó: mỗi finding một mục `### <slug> [P*]` gồm vị trí, bằng chứng, đề xuất sửa cụ thể.
Cuối: mục `## Đã chạy` liệt kê lệnh + rc. `approved` chỉ khi 0 P0–P3.
