# Cross-review wp835 r3/g3 — lượt 1 (Codex, read-only, lớp `sensitive`)

Bạn là REVIEWER độc lập (họ model openai) cho packet **wp835**, Issue #835 của `ducthangho/tra-luat`.
Executor là Claude Code (họ claude). Bạn KHÔNG sửa mã trong kho, KHÔNG commit, KHÔNG push, KHÔNG gọi mạng
GitHub. Thư mục làm việc là một clone rời; chỉ ghi kết quả vào thư mục output được nêu cuối prompt.

## Neo
- Exact head đưa ra review: `3785f9535398db04fb36a5eaa095166a8e048f1e` (nhánh `agent/wp835-g3-claude`, đã checkout detached).
- Base: `d2e3052d479d140b7e7b91df41ec4914fab7d544` (= `origin/master` lúc cấp lease; master sau đó tiến tới `cdc4e80` chỉ ở `ops/land/**`).
- Lease: `git show origin/ops/wp835-r3-g3-lease:ops/leases/wp835-r3-g3-claude.yaml`.
- Đặc tả r3 (DELTA): `git show origin/ops/wp835-r3-g3-lease:ops/specs/wp835-lease-6h-governance-r3.md`, sha256 `71403df80d133e4568cb891ae5ab41de937a9d1d1086a92f7255323568596ddc`.
- Đặc tả r2: `git show origin/ops/wp835-r2-g2-lease:ops/specs/wp835-lease-6h-governance-r2.md`, sha256 `da98e225c1e0bb419b83c368d2b3112309bd95316a4787c18f91f79bdbc57833`.
- Bản vá nguồn r2 (chưa từng được approve): `git diff 062292b origin/agent/wp835-g2-claude`.
- Tự băm lại hai đặc tả; lệch thì ghi P1 và dừng.

## Diff cần review
`git diff d2e3052 3785f95` — 2 tệp: `docs/PROTOCOL_DA_PHIEN.md` (+11 −3) và `docs/adr/0056-lease-no-progress-six-hours.md` (mới, 50 dòng).

## LỆCH ĐẶC TẢ executor tự khai — hãy kiểm bằng phép đo, đừng nhận lời
Đặc tả r3 D3 cho write set 4 tệp, trong đó `scripts/tl_selftest.py` ("CHỈ ratchet `r291_docs_ngoai_goi`: số
Markdown dưới `docs/` +1 và cây thật +1, kèm khối KÊ KHAI SLOT") và `RELEASE_MANIFEST.json` (tái sinh vì băm
`tl_selftest.py` đổi). Executor KHÔNG sửa hai tệp đó, với lý do: trên base, `_c291_docs_ngoai_goi`
(`scripts/tl_selftest.py` quanh dòng 21771–21985) đã **đóng nợ R291-DAM-SO-CUNG ở packet #794** — số `docs/*.md`
nay TÍNH từ cây (`ok4`), chỉ số tệp GÓI còn ratchet (`ok3 ... == 192`), và chú thích ghi rõ *"Thêm docs KHÔNG kê
khai slot ở đây nữa."* Tức không còn ratchet docs nào để +1; thêm một khối KÊ KHAI SLOT sẽ trái chính chú thích
ấy, và đổi băm `tl_selftest.py` chỉ để buộc tái sinh manifest.
Bằng chứng executor đo (tái lập được tại chỗ nếu bạn có thời gian; selftest ~3,5 phút):
- `python scripts/tl.py --selftest` trên cây = `3785f95` ⇒ `== tl selftest 1731/1731 ==`, rc 0, `[OK] r291_docs_ngoai_goi`.
- `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok: true`, expected 192 == checked 192 (manifest không đổi vì `docs/` nằm ngoài gói).
- Phản chứng đang chạy (kết quả sẽ có trong handoff): (A) thêm một `docs/*.md` bất kỳ ⇒ r291 vẫn OK; (B) đổi ratchet gói 192→193 ⇒ r291 ĐỎ.
Câu hỏi cho bạn: lệch này là (a) đúng — write set là trần, không phải sàn — hay (b) phải xin chủ kho trước khi thu hẹp?
Nếu (b), xếp hạng mức độ và nói rõ vì sao.

## Tiêu chí (N1–N7 của đặc tả r3) — đo, đừng đọc
- **N1** §4 và fallback `review_sla`: 360 phút cho lease MỚI; `lease_until`, generation, bia mộ, exact head, heartbeat 15 phút sau `changes_requested` giữ nguyên. So từng câu base/head.
- **N2** `python .claude/dev/packet_loop.py adr-song --root .` rc 0.
- **N3** `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; `git diff --check d2e3052 3785f95` rc 0.
- **N4/N5** như trên; thêm `python scripts/tl.py doc-claims-check --strict --json` delta so base = 0 (executor đo: cả hai rc 2 với đúng MỘT flag chung `docs/AUDIT_LAUNCHER_VONG_3.md:462 f08e45b SHA_NOT_A_COMMIT` — kho là clone nông, nên flag này có thể là tạo tác độ sâu; đỏ sẵn, delta 0).
- **N7** ADR giữ `CHƯA KÍCH HOẠT VẬN HÀNH`; không câu nào khai 360 phút đã có hiệu lực vận hành.

## Hướng soi theo lớp (tìm theo LỚP, không dừng ở ca đầu tiên)
1. Đổi số: mọi `ADR-0056` trong diff có đúng nghĩa "ngưỡng lease 6 giờ" không; có chỗ nào còn trỏ `ADR-0055` với nghĩa lease 6 giờ, hoặc chỗ nào lỡ đổi `ADR-0055` của #919 (trần Codex 10) không. Dòng §20 `ADR-0052`/`ADR-0055` phải nguyên byte so base.
2. Thứ tự bảng §20 và khớp 1:1 tệp ADR.
3. So bản vá với bản r2 (`a62ba1f`): ngoài đổi số và ba chỗ provenance r3 trong tệp ADR (dòng Trạng thái, câu "đo lại 25-10-2026 tại base d2e3052", câu write set), có khác biệt nào khác không? Những câu provenance mới có lời khai nào rộng hơn phép đo không (ví dụ "không có controller nào trong kho mang hằng 30 phút" — executor đo bằng `rg --hidden` các mẫu `heartbeat_required_minutes|30 phút|minutes=30` trên *.py/*.sh/*.yml/*.ps1 ngoài `ops/leases/`; chỉ thấy các tham chiếu vô can: vòng rasoat, trần 30 phút gate mutant, comment ci.yml).
4. Còn câu nào khác trong protocol nói ngưỡng 30 phút thu hồi lease mà bản vá bỏ sót không (gợi ý: dòng ~1307 là bảng phương án thiết kế lịch sử — đánh giá có cần sửa không).
5. Câu trong ADR mâu thuẫn với protocol §4 hoặc với ADR-0017.

Đừng tự soạn nội dung dựng đường dẫn thoát khỏi cây thư mục; hướng nào cần thế thì mô tả bằng lời.

## Output (bắt buộc)
Ghi DUY NHẤT tệp `VERDICT.md` vào thư mục output được chỉ định trong lời gọi. Dòng đầu tiên đúng một trong hai:
`VERDICT: approve` hoặc `VERDICT: changes_requested`. Sau đó: `Reviewed commit: 3785f9535398db04fb36a5eaa095166a8e048f1e`,
danh sách finding mỗi cái gắn P0/P1/P2/P3 kèm tệp:dòng, phép đo/lệnh đã chạy và output rút gọn, và câu trả lời
cho câu hỏi lệch đặc tả. Approve chỉ khi không còn P0/P1/P2. Nói rõ phép nào bạn KHÔNG chạy được.
