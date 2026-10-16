# Cross-review ĐẶC TẢ — `THU-HOI-LEASE-VA-CAP-LAI` **revision 9** (bản đóng băng, Issue #488) · REVIEWER codex · lượt 8 (lời gọi **9**; lệnh chủ kho 09-09: bản chưa có cross-review "không P1" thì vá tiếp + review; bộ đếm KHÔNG reset)

Lượt 7 (lời gọi 8, VERDICT `f28b7d0c…`) đọc r8 và kết luận **0 P1**, `changes_requested` chỉ vì 2 P2 (S8 một phần, S10 mới).
r9 = r8 + HINT lượt 7 (5 hunk áp sạch) + §0 dòng 7a/7 + §0.5 + Q14 kết luận dừng; **ADR-0047 sửa cùng commit theo S10**
(§Quyết định hai biên mã lỗi, lớp 3 "vượt trần/hết deadline", luật 3 khoanh claim phái sinh, approver uỷ quyền bền).
r9 đã được đóng băng và Packet Issue **#488** (slice A0) neo `spec_hash` = sha256 r9. **Lượt này đọc đúng bản đóng băng ấy** —
nếu bạn tìm ra P1 thì Issue phải đi revision; nếu chỉ P2/P3 thì ghi để executor A0 xử trong packet (§3.2), spec không đổi.
Đừng nâng hạng để kéo dài; đừng hạ hạng để kết thúc. Quyết định nền thực thi/người duyệt/profile production **vẫn của
chủ kho, chưa có** — không phải finding.

**Phân công như lượt 4b — CẤM tuyệt đối tự soạn** remote helper giả, `remote.<x>.vcs`, `url.*.insteadOf` trỏ kho lạ,
`refs/replace`/graft, biến môi trường Git nhằm đổi nguồn, bytes cache lệch OID, đường thoát cây, đồng tự Unicode, chuỗi
thoát — các hướng ấy chỉ **MÔ TẢ BẰNG LỜI**; bạn chạy **CONTROL hợp lệ** và ĐỌC hợp đồng. Kho giả Git thông thường
(bare/working copy/linked worktree, lease/sổ/metadata fixture, symlink nội bộ, merge, mode, pack/alternates/partial/shallow)
vẫn được. **Read-only với kho**; **CẤM đọc ra ngoài cwd**; không mạng; tối đa 60 phút; **ghi VERDICT.md sớm rồi bổ sung dần**.

## Thư mục
- `SPEC.md` — **revision 9**, sha256 `465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79`; cùng nội dung tại `cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (untracked). §0.5 có bảng "S8/S10 → r9 làm gì". Delta so r8 = HINT lượt 7 của CHÍNH BẠN (`HINT.luot7.patch`, `95b63772…`) + §0/Q14 kế toán.
- `ADR-0047.md` (= `cay-kho/docs/adr/0047-nguon-tin-cay-cho-cong-doc-lease.md`, untracked) — sha256 `b9975929c52e12767417b46b47829c265230117fe65df6a9fd22540d4868fdab`, bản đã sửa theo S10. Lệch ADR ↔ spec vẫn là finding.
- `SPEC.r8.md` (`48ea894a…`); `VERDICT.luot7.md` (`f28b7d0ce868d15905d4468ea248db43bfed79b7fe1899f278fe4afe9a4c461c`) — của CHÍNH BẠN lượt 7; `VERDICT.luot6.md` (`9090aadd…`), `VERDICT.luot5.md` … `VERDICT.luot1.md`.
- `scratch/luot6/`, `scratch/luot7/` — harness hợp lệ của bạn (replay/r8_controls/join_model/budget_controls/typed_memo/native_r8 + JSON). Tái dùng qua loader; scratch mới ở `scratch/luot8/`; không sửa script cũ; không chạy script nào chứa hướng bị cấm.
- `cay-kho/` — clone từ mirror bare cục bộ (309 nhánh máy chủ đo 03:1xZ 08-09, KHÔNG fetch lại; detached tại `b416830ef2a509d60203d55552ce17950afcf67c` = `base_sha`; `core.abbrev 7`); `origin/master` = `585c7d5`.
- `EVIDENCE.md` — lời khai điều phối lượt 1–7 + "Bổ sung lượt 8".

## Việc phải làm
1. **S8 và S10 theo §0.5 r9**: ĐÓNG · ĐÓNG-MỘT-PHẦN · CHƯA · ĐÓNG SAI, kèm bằng chứng. Control: (a) S8 — cây 129 thư mục anh em (tổng 258 cạnh, đường dài 2) dưới trần 128 theo định nghĩa "một lần resolve tại một occurrence" ⇒ 0; mutant cộng toàn snapshot ⇒ 12; bound−1/bound/bound+1 ⇒ 0/0/12 (biên inclusive) cho ít nhất hai counter; alternate depth 3/4/5 ⇒ 0/0/12; deadline với subprocess im lặng; (b) S10 — đối chiếu **từng câu** ADR-0047 r9 với spec r9 (hai biên mã lỗi reader 12 / `RC_STATE=8`; "vượt trần hoặc hết deadline"; luật 3 claim phái sinh vs input khai báo; approver uỷ quyền bền): còn câu nào mạnh/yếu hơn nhau; A10 oracle `reader_rc=12 → RC_STATE=8` và mutant trả thẳng 12 ⇒ ĐỎ có dựng được không.
2. **Xác nhận lại các ĐÓNG của lượt 7 KHÔNG bị r9 làm hỏng** (S1/S3/S5/S6/S7, S2/S4): HINT của bạn áp lên r8 có tạo mâu thuẫn mới với đoạn nào của Q3/Q4/M9/A6/A10 không (đọc, không cần chạy lại toàn bộ; chạy lại control nào rẻ).
3. **Tấn công r9 ở chỗ MỚI — bằng lời hoặc ca hợp lệ**: (a) mục "Đồng bộ hợp đồng với ADR-0047" trong spec có tự mâu thuẫn với A10 cũ không; (b) §0.5/Q14: kế toán lượt 7a/7 đúng chưa (7a chết preflight KHÔNG tính — §12 "lỗi preflight … trước khi model sinh output không tăng bộ đếm"); (c) Issue #488 (mô tả trong EVIDENCE, không có raw trong bundle): packet_id `THU-HOI-LEASE-VA-CAP-LAI-A0`, `mission_issue: null`, `depends_on: []` với dependency CÓ TÊN `LAND-DOC-RECEIPT-THU-HOI` ghi ở comment — có trái §3.2 không; write set 3 path A0 có khớp spec `write_set` không; (d) §1 dòng "Đo lại L5" và §0.5 có số nào chép sai từ VERDICT lượt 7 của bạn.
4. **A1–A12 r9**: đơn vị? phép đỏ thật? đột biến đúng ca? ca không thể đỏ / không thể xanh? (tập trung A6/A10 — chỗ r9 đổi).
5. **Nhất quán luật** (§3.2 §4 §5 §8 §12; ADR-0025/0028/0044/0047; CLAUDE.md), kích thước slice.
6. **Đo lại con số r9** đo được offline; số nào không dựng lại được thì ghi `chua_do_duoc`.

## Xếp hạng
P1 = spec sẽ sinh mã sai/fail-open, mâu thuẫn luật, tiêu chí không thể đỏ, hoặc con số chống đỡ lời khai THẨM QUYỀN mà sai. P2 = thiếu/mơ hồ khiến executor tự quyết. P3 = chữ nghĩa. Finding cũ chưa đóng giữ hạng. Nếu KHÔNG còn P1: nói thẳng `approve` hoặc `changes_requested` chỉ P2/P3 — và nói rõ P2 nào executor A0 xử được trong packet mà không cần revision spec. Nếu còn P1: nêu rõ P1 nào thuộc hình dạng "nguồn tin cậy" (⇒ ADR) và P1 nào không.

## Đầu ra — BẮT BUỘC, ghi vào cwd (ghi sớm, bổ sung dần)
1. `VERDICT.md`: `verdict` · `reviewed_spec_sha256` · `reviewed_adr0047_sha256` · `model_tu_khai` · `## Bảng finding lượt 1–7 → trạng thái` · `## Findings mới` · `## Phản chứng đã chạy lại + mới` (ghi rõ hướng nào chỉ MÔ TẢ, harness nào tái dùng/dựng mới) · `## Tiêu chí A1–A12` · `## Bảng đo lại` · `## chua_do_duoc`.
2. `HINT.patch` — unified diff `patch -p0` lên `SPEC.md` cho MỌI P1/P2 còn lại; không còn ⇒ patch 0 hunk + ghi chú. Nếu cần sửa ADR, ghi nguyên câu cần thay trong VERDICT (patch chỉ lên SPEC.md).
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
Bắt đầu lúc: 2026-09-09T10:56:22Z
