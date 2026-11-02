# Cross-review — packet `WINDOWS-LOCAL-MAY-CHU-KHO` r3 g1 (mission `gh-1035`)

Bạn là REVIEWER độc lập (provider `openai_codex`), phiên mới. Executor là Claude; bạn KHÔNG sửa `cay-kho/`.
Ghi duy nhất vào thư mục sandbox này (`VERDICT.md`, tệp nháp nếu cần). Phiên điều phối chụp snapshot `cay-kho/`
trước và sau lượt của bạn, ngoài thư mục sandbox. Không có verdict cũ nào để đọc.

## Neo
- Kho: `cay-kho/` (clone đầy đủ từ GitHub, không shallow), HEAD phải = `144c96ad15071d0d9c2061b34d17f2c13b647e70`.
  Kiểm bằng `git -C cay-kho rev-parse HEAD`; lệch thì dừng và ghi `verdict: blocked`.
- Base: `adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc`. Diff: `diff.patch` (= `git diff base HEAD`).
- Đặc tả đóng băng: `spec-r3.md` (bản chép từ nhánh `ops/windows-local-may-chu-kho-r3-lease`, cũng fetch sẵn trong
  `cay-kho` dưới `origin/ops/windows-local-may-chu-kho-r3-lease`), sha256 phải =
  `f1a666a32161f0607ac27bc8c3be6963bb6367e64f02825635a75cc8185fa973`. Tệp này CHƯA có trên master (PR #1062 chưa merge).
- Lease: `lease.yaml` (effective_review_class `sensitive`, write set 2 tệp, trần ≤ 2 tệp / ≤ 140 dòng thêm).
- Protocol: `cay-kho/docs/PROTOCOL_DA_PHIEN.md` (§8 review, §10.2, §20). ADR được bổ sung: `docs/adr/0057-*.md`,
  `docs/adr/0058-*.md`. Khuôn "ADR mới sửa ADR khác": `docs/adr/0058-*.md` (với ADR-0057).

## Việc
Review hai trục **Spec** và **Standards/Security**:
1. Diff có làm ĐÚNG và ĐỦ §2 đặc tả không: nhịp tim (trường thứ năm, ≥ 30 phút một lần, hạn ≤ 2 giờ kể từ lần ghi);
   không tiếp nhận khoá còn tiến trình sống (kiểm tải, `python.exe` khởi động sau UTC bắt đầu của khoá cũ, không phải
   MCP, không áp cho 3(c)); lượt bị ngắt (`ngat=co`, thời lượng không dùng cho rà soát, không tự đổi chế độ nguồn);
   đọc lại trước mọi lần ghi lại dòng khoá; nhả khoá là ghi tệp rỗng 0 byte; số đo D10–D12 chép đúng §1; mục
   "không cổng nào cưỡng chế". §20: đúng một dòng ADR-0059 với cột cổng `không cổng — kỷ luật executor`; ô mô tả
   ADR-0058 thêm "khoá bổ sung bởi `ADR-0059`" (chỉ sửa ô ấy); câu con trỏ §10.2 nhắc 0057, 0058, 0059 và vẫn
   TRUNG TÍNH (không tạo nghĩa vụ). Không chép doctrine vào protocol. Có luật nào ADR-0059 nói mạnh hơn/rộng hơn
   đặc tả, hoặc mâu thuẫn ADR-0057/0058 ở các điểm được giữ nguyên?
2. **Đi qua văn bản ADR-0059 theo TỪNG BƯỚC** (chỉ dùng chữ của ADR-0057/0058/0059, không dùng hiểu biết ngoài) cho
   ba ca, ghi rõ từng bước dựa vào câu nào và kết quả:
   (i) A bị ngắt tới khi khoá quá hạn, tiến trình của A đã dừng; B tiếp nhận theo 3(a); A kết nối lại.
       Kết quả đúng: dòng của B giữ nguyên.
   (ii) Khoá của A quá hạn nhưng chưa ai tiếp nhận; A kết nối lại. Kết quả đúng: A gia hạn được.
   (iii) Ca D10 (số đo ở §1 đặc tả). Kết quả đúng: "không tiếp nhận".
   Nếu văn bản cho ra kết quả khác, hoặc cho ra hai cách đọc, đó là finding. Thử thêm biến thể gần (ví dụ tiến trình
   của chính A còn chạy khi A gia hạn; dòng bốn trường của ADR-0058; nhả khoá khi dòng đã của phiên khác).
3. Tiêu chí §3/§4: chạy trong `cay-kho/` (dùng `python3`):
   - `python3 .claude/dev/packet_loop.py adr-song --root .` (rc phải 0)
   - `python3 .claude/dev/packet_loop.py doctrine-scan --root .` (rc phải 0)
   - `python3 scripts/tl.py doc-claims-check --json` (`ok` phải true; trước đó `git -C cay-kho config core.abbrev 7`)
   - đếm tệp/dòng thêm của diff (≤ 2 tệp, ≤ 140 dòng thêm), tệp nằm trong write set, không chạm `docs/adr/0057-*`,
     `docs/adr/0058-*`. Ghi lệnh, rc và dòng kết quả thật.
4. Tính đúng của các lời khai trong ADR: tham chiếu chéo (§ số của ADR-0057/0058, protocol §3.1, PR/issue, session,
   số đo, phép suy giờ khởi động trong ca D10) có tồn tại/khớp không; câu nào tự mâu thuẫn hoặc mơ hồ đến mức
   executor đọc ra hai nghĩa. Khái quát mỗi lỗi thành LỚP và quét mọi biểu hiện cùng lớp.

Mức độ: P0 (chặn tuyệt đối) · P1 (sai luật/sai spec) · P2 (thiếu/sai lời khai có hậu quả) · P3 (nhỏ, có
thể sửa). Chỉ báo finding có bằng chứng (dòng tệp + lệnh/đối chiếu).

## Đầu ra: `VERDICT.md` trong thư mục sandbox này
Ghi tăng dần. Dòng 1: `verdict: approved` hoặc `verdict: changes_requested` (hoặc `blocked`).
Dòng 2: `reviewed_sha: 144c96ad15071d0d9c2061b34d17f2c13b647e70`.
Dòng 3: `Kết quả: N P0, N P1, N P2, N P3.`
Sau đó: mỗi finding một mục `### <slug> [P*]` gồm vị trí, bằng chứng, đề xuất sửa cụ thể. Rồi mục `## Ba ca` với
bước đi của (i)(ii)(iii). Cuối: mục `## Đã chạy` liệt kê lệnh + rc. `approved` chỉ khi 0 P0–P3.
