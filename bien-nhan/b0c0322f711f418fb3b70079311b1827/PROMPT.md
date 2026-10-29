# Cross-review lượt 1 — packet `WINDOWS-LOCAL-MAY-CHU-KHO` r1 g1 (mission #748), PR #1022

Bạn là REVIEWER độc lập (provider `openai_codex`), phiên mới. Executor là Claude; bạn KHÔNG sửa
`cay-kho/`. Ghi duy nhất vào thư mục sandbox này (`VERDICT.md`, tệp nháp nếu cần).

## Neo
- Kho: `cay-kho/` (clone đầy đủ, không shallow), HEAD phải = `fff91390dafb3b8a16e6d11a7243dce036618260`.
  Kiểm bằng `git -C cay-kho rev-parse HEAD`; lệch thì dừng và ghi `verdict: blocked`.
- Base: `96667715996d41bc45e70a64fbaa8996de20f6a0`. Diff: `diff.patch` (= `git diff base HEAD`).
- Đặc tả đóng băng: `cay-kho/ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r1.md`, sha256 phải =
  `377ecea689043fcab4d007d65d9592bd28819fa37983796e0c1b75b2c154e715`.
- Lease: `lease.yaml` (effective_review_class `sensitive`, write set 2 tệp).
- Protocol: `cay-kho/docs/PROTOCOL_DA_PHIEN.md` (§8 review, §10.2, §20). ADR khuôn: `docs/adr/0055-*.md`, `0056-*.md`.

## Việc
Review hai trục **Spec** và **Standards/Security**:
1. Diff có làm ĐÚNG và ĐỦ §2 đặc tả không (từng gạch đầu dòng của §2.1 có trong ADR? bảng D1–D6 chép đúng
   số liệu §1? mục "không cổng nào cưỡng chế"? đúng một dòng §20 với cột cổng = `không cổng — kỷ luật executor`?
   đúng một câu con trỏ ở §10.2?). Có thêm luật nào KHÔNG có trong đặc tả không (ADR nói mạnh hơn/rộng hơn spec)?
2. Tiêu chí §3/§4: chạy trong `cay-kho/` (dùng `python3`):
   - `python3 .claude/dev/packet_loop.py adr-song --root .` (rc phải 0)
   - `python3 .claude/dev/packet_loop.py doctrine-scan --root .` (rc phải 0)
   - `python3 scripts/tl.py doc-claims-check --json` (`ok` phải true)
   - đếm tệp/dòng thêm của diff (≤ 2 tệp, ≤ 140 dòng thêm), tệp nằm trong write set.
   Ghi lệnh, rc và dòng kết quả thật.
3. Tính đúng của các lời khai trong ADR: tham chiếu chéo (§ số, tên tệp, PR/issue, SHA) có tồn tại trong
   kho không; lời khai về cái KHÔNG đổi có mâu thuẫn protocol không; câu nào tự mâu thuẫn hoặc mơ hồ đến
   mức executor đọc ra hai nghĩa. Khái quát mỗi lỗi thành LỚP và quét mọi biểu hiện cùng lớp.
4. Câu con trỏ ở §10.2 có đặt đúng chỗ và không chép doctrine không.

Mức độ: P0 (chặn tuyệt đối) · P1 (sai luật/sai spec) · P2 (thiếu/sai lời khai có hậu quả) · P3 (nhỏ, có
thể sửa). Chỉ báo finding có bằng chứng (dòng tệp + lệnh/đối chiếu).

## Đầu ra: `VERDICT.md` trong thư mục sandbox này
Ghi tăng dần. Dòng 1: `verdict: approved` hoặc `verdict: changes_requested` (hoặc `blocked`).
Dòng 2: `reviewed_sha: fff91390dafb3b8a16e6d11a7243dce036618260`.
Dòng 3: `Kết quả: N P0, N P1, N P2, N P3.`
Sau đó: mỗi finding một mục `### <slug> [P*]` gồm vị trí, bằng chứng, đề xuất sửa cụ thể.
Cuối: mục `## Đã chạy` liệt kê lệnh + rc. `approved` chỉ khi 0 P0–P3.
