# Cross-review ĐẶC TẢ — `THU-HOI-LEASE-VA-CAP-LAI` **revision 5** · REVIEWER codex · lượt 5 (lời gọi **6/6**, trần theo comment PR #475 `5575587924`)

Đây là lời gọi CUỐI trong trần 6. Chủ kho đã đọc khuyến nghị "dừng/ADR" của lượt 4b và chốt dùng lời gọi này trên r5
(ghi ở §0 SPEC.md). Sau lượt này: hết P1 ⇒ Packet Issue; còn P1 ⇒ checkpoint kế + ADR nguồn tin cậy, không tự nới.

**Phân công như lượt 4b — CẤM tuyệt đối tự soạn** remote helper giả, `remote.<x>.vcs`, `url.*.insteadOf` trỏ kho lạ,
`refs/replace`/graft, biến môi trường Git nhằm đổi nguồn, bytes cache lệch OID, đường thoát cây, đồng tự Unicode, chuỗi
thoát — các hướng ấy chỉ **MÔ TẢ BẰNG LỜI**; bạn chạy **CONTROL hợp lệ** và ĐỌC hợp đồng. Kho giả Git thông thường
(bare/working copy, lease/sổ fixture, symlink nội bộ, merge, mode) vẫn được. **Read-only với kho**; **CẤM đọc ra ngoài
cwd**; không mạng; tối đa 60 phút; **ghi VERDICT.md sớm rồi bổ sung dần**.

## Thư mục
- `SPEC.md` — **revision 5**, sha256 `23a7deaf60af17aea2fa3b027d08fb8c187b6f03499f34540822ab7b9c3b1672`; cùng nội dung tại `cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (untracked).
- `SPEC.r4.md` (`415ce35d…`); `VERDICT.luot4b.md` (`7d3017ec…`) + `HINT.luot4b.patch` (`4a0321fd…`) — của CHÍNH BẠN lượt 4b; `VERDICT.luot3.md` (`6b8dde21…`), `VERDICT.luot2.md`, `VERDICT.luot1.md`.
  §0.2 của SPEC.md có bảng "S1–S6 → r5 làm gì". Q13/Q14 đã chốt (comment `5575587924`, offline coi là lời khai điều phối đã readback).
- `cay-kho/` — mirror đầy đủ (302 ref, detached tại `b416830ef2a509d60203d55552ce17950afcf67c`, `core.abbrev 7`); `origin` là bare cục bộ.
- `EVIDENCE.md` — lời khai lượt 1–4b + bổ sung lượt 5. `scratch/luot4b/` — script hợp lệ của bạn lượt 4b (measure/allowed_probes/allowed_coverage/extra/loop/controls); `scratch/*.py` — lượt 3. Tái dùng, không dựng lại.

## Việc phải làm
1. **S1–S6 và mọi finding cũ còn mở** (R1 một phần; các "ĐÓNG-MỘT-PHẦN" lượt 1–3): ĐÓNG · ĐÓNG-MỘT-PHẦN · CHƯA · ĐÓNG SAI, kèm bằng chứng. Chạy lại phản chứng hợp lệ dưới luật r5: A5 ba nhánh nguồn closure (policy fixture / ngoại lệ có neo / không neo / policy hỏng / tự khai []); A6 catalog mutant (control sạch; ca "bytes lệch OID" chỉ mô tả); hồ sơ adapter (control: env dựng từ rỗng + endpoint fixture ⇒ 0; ca âm chỉ mô tả); M9 publisher/consumer (đọc hợp đồng + control receipt); descriptor Q13 (mismatch ⇒ 12, retired theo sự kiện); bootstrap audit ghi bền.
2. **Tấn công r5 ở chỗ MỚI — bằng lời hoặc ca hợp lệ**: (a) hồ sơ tiến trình Q4.1 còn kẽ nào (allowlist `GIT_CONFIG_KEY_*` = `credential.*`/`http.*` — `http.*` có khoá nào nguy hiểm? `core.*`? `GIT_ALLOW_PROTOCOL=https` đủ chưa? `PATH` tối thiểu vs executable ghim); (b) băm lại nội dung Q4.5: đủ cho commit (ancestry S→H) — commit object băm gồm parents, tree — có bỏ sót object nào trên đường quyết định không; chi phí ước bao nhiêu object/lần; (c) A6 catalog: còn mutant nào được viện ra mà bị lớp khác che; (d) Q12 descriptor có tag: dispatcher-less repo hôm nay ai "duyệt" descriptor — có thành tự khai không; (e) §12 sau lời gọi 6: r5 đã nói đúng chưa.
3. **A1–A12 r5**: đơn vị? phép đỏ thật? đột biến đúng ca? ca không thể đỏ / không thể xanh?
4. **Nhất quán luật** (§3.2 §4 §5 §8 §12; ADR-0025/0028/0044; CLAUDE.md), kích thước slice.
5. **Q7–Q14**: thiếu câu nào; câu nào đã có đáp án bắt buộc.
6. **Đo lại con số r5** đo được offline.

## Xếp hạng
P1 = spec sẽ sinh mã sai/fail-open, mâu thuẫn luật, tiêu chí không thể đỏ, hoặc con số chống đỡ lời khai THẨM QUYỀN mà sai. P2 = thiếu/mơ hồ khiến executor tự quyết. P3 = chữ nghĩa. Finding cũ chưa đóng giữ hạng. Nếu KHÔNG còn P1: nói thẳng `approve` hoặc `changes_requested` chỉ P2/P3 — không nâng hạng để kéo dài, không hạ hạng để kết thúc. Nếu còn P1: nêu rõ P1 nào thuộc hình dạng "nguồn tin cậy" (⇒ ADR) và P1 nào không.

## Đầu ra — BẮT BUỘC, ghi vào cwd (ghi sớm, bổ sung dần)
1. `VERDICT.md`: `verdict` · `reviewed_spec_sha256` · `model_tu_khai` · `## Bảng finding lượt 1–4b → trạng thái` · `## Findings mới` · `## Phản chứng đã chạy lại + mới` (ghi rõ hướng nào chỉ MÔ TẢ) · `## Tiêu chí A1–A12` · `## Bảng đo lại` · `## chua_do_duoc`.
2. `HINT.patch` — unified diff `patch -p0` lên `SPEC.md` cho MỌI P1/P2 còn lại; không còn ⇒ patch 0 hunk + ghi chú.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
Bắt đầu lúc: 2026-09-07T22:07:34Z
