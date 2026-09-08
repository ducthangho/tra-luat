# Cross-review ĐẶC TẢ — `THU-HOI-LEASE-VA-CAP-LAI` **revision 4** · REVIEWER codex · lượt 4b (lời gọi 5/6, neo comment PR #475 `5575587924`)

Lượt 4a đã CHẾT ở bước ghi verdict vì bộ lọc nội dung của nền bắn khi bạn tự soạn probe dựng remote helper/config
độc hại (`scratch/probes_r4.py`, `coverage_r4.py` — vẫn còn trong `scratch/`, tái dùng phần KHÔNG bị chặn). Lượt này
ĐỔI PHÂN CÔNG, không đổi mục tiêu:

**CẤM tuyệt đối tự soạn**: remote helper giả, `remote.<x>.vcs`, `url.*.insteadOf` trỏ kho lạ, `refs/replace`/graft,
biến môi trường Git nhằm đổi nguồn, đường thoát cây, đồng tự Unicode, chuỗi thoát — mọi hướng "kẻ tấn công đổi nguồn/
đổi cây" chỉ được **MÔ TẢ BẰNG LỜI** (điều kiện, lệnh Git hợp lệ nào, kỳ vọng rc) để phiên điều phối dựng. Với các hướng
ấy bạn chỉ chạy **CONTROL hợp lệ** (adapter đọc đúng nguồn, đúng cây) và kiểm hợp đồng bằng cách ĐỌC spec. Bạn vẫn được
dựng kho giả Git bình thường (bare/working copy, lease/sổ fixture, symlink nội bộ, merge) như các lượt trước.

Cùng vai, cùng cấm khác như lượt 1–3: **read-only với kho**; **CẤM đọc ra ngoài cwd**; không mạng; tối đa 60 phút;
phút 45 bắt đầu ghi VERDICT.md — **ghi VERDICT.md sớm rồi bổ sung dần**, để một lần bị chặn không mất trọn lượt.

## Thư mục
- `SPEC.md` — **revision 4**, sha256 `415ce35db32aa370ce43315c1ff6d4db7b59005e6288538e72705ce4caed4d0e`; cùng nội dung tại `cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (untracked).
- `SPEC.r3.md` (`ef9b3700…`); `VERDICT.luot3.md` (`6b8dde21…`) + `HINT.luot3.patch` (`0a81bd8b…`) — của CHÍNH BẠN lượt 3; `VERDICT.luot2.md`, `VERDICT.luot1.md`.
  §0.1 của SPEC.md có bảng "R1–R10 → r4 làm gì". Chủ kho đã chốt Q13/Q14 (neo comment PR #475 `5575587924` — offline, coi là lời khai điều phối đã readback).
- `cay-kho/` — mirror đầy đủ (302 ref, detached tại `b416830ef2a509d60203d55552ce17950afcf67c`, `core.abbrev 7`); `origin` là bare cục bộ.
- `EVIDENCE.md` — lời khai lượt 1–3 + 4a. `scratch/luot3/` — script của bạn lượt 3 (probes_r3, extra_r3, followup_r3, loop_r3, measure_r3) để tái dùng.

## Việc phải làm
1. **R1–R10 và finding cũ còn mở**: ĐÓNG · ĐÓNG-MỘT-PHẦN · CHƯA · ĐÓNG SAI, kèm bằng chứng. Chạy lại phản chứng **hợp lệ** dưới luật r4 (bootstrap A0 workflow chưa kích hoạt S/T rỗng; A0 dự báo giữ verdict cũ; M9 exact S/H/T + strict up-to-date; `effective_write_set` tự khai ⇒ 8; symlink hai cây/vòng nội bộ; cutover phân loại delta; C không đích + g2 hết hạn; A8 mutant kết hợp; `record-lease` target ID). R1/R2: đọc hợp đồng adapter Q4.1/Q4.5, nêu bằng lời chỗ hở nếu có, chạy control hợp lệ.
2. **Tấn công r4 ở chỗ mới — bằng lời hoặc bằng ca hợp lệ**: (b) hàm dự báo A0 có bị dùng làm quyết định ở đâu không; (c) audit bootstrap lần land A0: điều kiện đủ, ghi ở đâu; (d) C không đích + g3 riêng: g3 có thể được cấp trước khi C hiệu lực không; (e) ngoại lệ Q13: phạm vi/hết hạn/neo có đủ để không "grandfather" mãi; (f) §12 với trần 6 và lượt 4a chết đã tính là lời gọi.
3. **A1–A12 r4**: đơn vị? phép đỏ thật? đột biến đúng ca? ca không thể đỏ / không thể xanh?
4. **Nhất quán luật** (§3.2 §4 §5 §8 §12; ADR-0025/0028/0044; CLAUDE.md), kích thước slice (825–1195).
5. **Q7–Q14**: thiếu câu nào; câu nào đã có đáp án bắt buộc.
6. **Đo lại con số r4** đo được offline.

## Xếp hạng
P1 = spec sẽ sinh mã sai/fail-open, mâu thuẫn luật, tiêu chí không thể đỏ, hoặc con số chống đỡ lời khai THẨM QUYỀN mà sai. P2 = thiếu/mơ hồ khiến executor tự quyết. P3 = chữ nghĩa. Finding cũ chưa đóng giữ hạng. Nếu KHÔNG còn P1: nói thẳng `approve` hoặc `changes_requested` chỉ P2/P3 — không nâng hạng để kéo dài, không hạ hạng để kết thúc.

## Đầu ra — BẮT BUỘC, ghi vào cwd (ghi sớm, bổ sung dần)
1. `VERDICT.md`: `verdict` · `reviewed_spec_sha256` · `model_tu_khai` · `## Bảng finding lượt 1–3 → trạng thái` · `## Findings mới` · `## Phản chứng đã chạy lại + mới` (ghi rõ hướng nào chỉ MÔ TẢ BẰNG LỜI) · `## Tiêu chí A1–A12` · `## Bảng đo lại` · `## chua_do_duoc`.
2. `HINT.patch` — unified diff `patch -p0` lên `SPEC.md` cho MỌI P1/P2 còn lại; không còn ⇒ patch 0 hunk + ghi chú.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
Bắt đầu lúc: 2026-09-07T21:31:10Z
