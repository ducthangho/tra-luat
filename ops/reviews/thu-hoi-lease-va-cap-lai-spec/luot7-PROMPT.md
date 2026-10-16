# Cross-review ĐẶC TẢ — `THU-HOI-LEASE-VA-CAP-LAI` **revision 8** · REVIEWER codex · lượt 7 (lời gọi **8**, trần theo comment PR #475 `5578460203`: "review tới hết P1", bộ đếm KHÔNG reset)

Lượt 6 (lời gọi 7, VERDICT `9090aadd…`) kết luận `changes_requested`: S2/S4 ĐÓNG; còn 3 P1 (S1 một phần, S3 một phần, S7
mới) + 3 P2 (S5, S6 một phần, S8 mới) + P3 S9. r8 vá theo HINT lượt 6 (5 hunk áp trực tiếp, 2 hunk vá tay vì đụng chỗ r7 đã
sửa) cộng phần HINT không phủ; chi tiết ở §0.4 SPEC.md. **ADR-0047** `docs/adr/0047-nguon-tin-cay-cho-cong-doc-lease.md` đã
tồn tại trên nhánh PR (Proposed; bản trong `cay-kho` là bản mới nhất, untracked) — lớp 2 viết lại theo S1 lượt 6. Quyết định
"nền thực thi cụ thể nào được tin, ai duyệt mỏ neo" **vẫn của chủ kho, chưa có** — r8 ghi thẳng ở `ngoai_pham_vi`/`chua_do_duoc`
11; đừng lấy việc thiếu giá trị ấy làm P1 nếu hợp đồng (producer/approver/manifest/serialization/một phép so) đã đủ để
executor không tự quyết; nếu hợp đồng CHƯA đủ, nói rõ câu nào thiếu.

**Phân công như lượt 4b — CẤM tuyệt đối tự soạn** remote helper giả, `remote.<x>.vcs`, `url.*.insteadOf` trỏ kho lạ,
`refs/replace`/graft, biến môi trường Git nhằm đổi nguồn, bytes cache lệch OID, đường thoát cây, đồng tự Unicode, chuỗi
thoát — các hướng ấy chỉ **MÔ TẢ BẰNG LỜI**; bạn chạy **CONTROL hợp lệ** và ĐỌC hợp đồng. Kho giả Git thông thường
(bare/working copy/linked worktree, lease/sổ/metadata fixture, symlink nội bộ, merge, mode, pack/alternates/partial/shallow)
vẫn được. **Read-only với kho**; **CẤM đọc ra ngoài cwd**; không mạng; tối đa 60 phút; **ghi VERDICT.md sớm rồi bổ sung dần**.

## Thư mục
- `SPEC.md` — **revision 8**, sha256 `48ea894a81b776742ae7152a8ce039d1b46eee3acd0e63a67a77cce5b21effe0`; cùng nội dung tại `cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (untracked). §0.4 có bảng "S1/S3/S5/S6/S7/S8/S9 → r8 làm gì". Chỗ vá: Q3 (descriptor + path reserved + transition), Q4.1 (deployment profile), Q4.5 (object-store layout/availability/ngân sách ĐỀ XUẤT), `write_set`/bootstrap (consumer trước cửa sổ A0), M1/M4/M9 (schema dispatcher, join API, artifact, bỏ dispatch), A5–A8/A11/A12, Q7/Q10/Q12/Q13, §1 dòng "Đo lại L5", `hinh_dang_ke_thua` 6 lần, `chua_do_duoc` 11–13.
- `cay-kho/docs/adr/0047-nguon-tin-cay-cho-cong-doc-lease.md` (untracked, bản r8) — đọc cùng SPEC; ADR giữ BẤT BIẾN, spec giữ chi tiết; lệch giữa hai tệp là finding.
- `SPEC.r6.md` (`f78135cf…`); `VERDICT.luot6.md` (`9090aadd34f34ea6607bae2e55cd87daffd2f1f43a2df10b2190b4db4e8d7db8`) + `HINT.luot6.patch` (`47fbf8cb…`) — của CHÍNH BẠN lượt 6; `VERDICT.luot5.md` (`1596d562…`), `VERDICT.luot4b.md`, `VERDICT.luot3.md`, `VERDICT.luot2.md`, `VERDICT.luot1.md`.
- `scratch/luot6/` — **harness hợp lệ của bạn lượt 6** (measure/controls/more_controls/admission_controls/partial_and_symlink/native, JSON kết quả, `SPEC.r3.recovered.md`, `patch-check/`). Tái dùng qua loader như lượt 5 đã làm với 4b; scratch mới ở `scratch/luot7/`; không sửa script cũ. Không chạy script nào chứa hướng bị cấm.
- `cay-kho/` — clone từ mirror bare cục bộ (`refs/remotes/origin/*` = 309 nhánh máy chủ, đo 03:1xZ 08-09 — KHÔNG fetch lại từ 08-09 nên thiếu 1 nhánh mới `ops/cap-lease-mu-ref-va-verdict` #482/#483, không chạm write set này; detached tại `b416830ef2a509d60203d55552ce17950afcf67c` = `base_sha`; `core.abbrev 7`). `origin/master` trong mirror = `585c7d5`.
- `EVIDENCE.md` — lời khai điều phối lượt 1–6 + "Bổ sung lượt 7".

## Việc phải làm
1. **S1, S3, S5, S6, S7, S8 theo §0.4 r8**: ĐÓNG · ĐÓNG-MỘT-PHẦN · CHƯA · ĐÓNG SAI, kèm bằng chứng. Control cần chạy lại/mới: (a) **S7**: fixture Git thường có `ops/thu-hoi/<x>.yaml` (revocation hợp lệ) + `_ngoai-le-closure.retired.yaml` (metadata 6 khoá, 100644) + policy fixture ⇒ dispatcher schema model: revocation qua M1 0, metadata qua Q13 0; metadata thiếu/hỏng/mode sai 12; sửa/xoá marker đã có ở S ⇒ 8; tệp gần tên reserved (`_ngoai-le-closure.retired.yml`, `ngoai-le-closure.retired.yaml`) vẫn M1 ⇒ 12; (b) **S3**: catalog A6 — ca positive routing 0 vs mutant bỏ routing 12 (ĐỎ), ca thiếu routing 12/12 (SỐNG, khai sống), ca trong-miền-khác-neo 12 vs mutant bỏ so profile 0 (ĐỎ), ca ngoài miền 12/12 (SỐNG); (c) **S8**: bare/linked worktree/pack/alternates control 0; partial thiếu blob 12 rồi materialize 0; shallow 12; memo `(expected_type, OID)` cùng OID hai type 12; (d) **S5**: model join check-run → `check_suite.id` → runs → attempt jobs (`check_run_url`) → artifacts theo ID; đọc hợp đồng, ghi rõ đường API là ĐỀ XUẤT chưa canary; (e) **S6**: descriptor + activation binding fixture 0 / lệch 12; B(P1,R1)→B2(P2,R1) 0 sau binding mới; B→D 12; (f) **S1**: đọc Q4.1 r8 + ADR-0047 lớp 2 — hợp đồng đã đủ để executor không tự quyết chưa; producer/approver/manifest/serialization/một phép so có mâu thuẫn nội tại không; F.profile control khớp hằng ⇒ 0 chạy lại.
2. **Tấn công r8 ở chỗ MỚI — bằng lời hoặc ca hợp lệ**: (a) schema metadata reserved: `base_sha_before_add == S` — S nào (S lúc PR policy được kiểm, hay S lúc marker được canonical nhận sau merge khác chen vào)? drift giữa hai lần kiểm có làm marker hợp lệ thành 8/12 oan? (b) `descriptor_sha256` ghim vào hằng mã A1 nhưng marker chỉ xuất hiện khi policy tới (có thể sau A1 nhiều ngày) — mã A1 đã canonical có kiểm được marker chưa tồn tại lúc viết mã không; (c) M9 bỏ `workflow_dispatch`: đường chẩn đoán còn lại là gì, có làm A1 canary S≠H không thể tạo được không; (d) ngân sách Q4.5: 8 trần có trần nào không đo được từ reader (vd `max_reader_wall_seconds` với subprocess)? bound−1/bound/bound+1 dựng được không với `max_alternate_depth`; (e) Q4.1: "Chọn đúng một cấu hình proxy hiệu lực" — Git đọc `http.proxy` vs env `https_proxy` theo thứ tự nào, spec có bắt đúng chiều không; (f) §1 dòng "Đo lại L5": số nào chép sai từ VERDICT lượt 6 của bạn; (g) ADR-0047 vs spec: câu nào của ADR mạnh hơn/yếu hơn spec.
3. **A1–A12 r8**: đơn vị? phép đỏ thật? đột biến đúng ca? ca không thể đỏ / không thể xanh?
4. **Nhất quán luật** (§3.2 §4 §5 §8 §12; ADR-0025/0028/0044/0047; CLAUDE.md), kích thước slice (A0 nay thêm schema metadata + profile + join: ước còn đúng không).
5. **Q7–Q14**: thiếu câu nào; câu nào đã có đáp án bắt buộc.
6. **Đo lại con số r8** đo được offline; số nào không dựng lại được thì `chua_do_duoc`.

## Xếp hạng
P1 = spec sẽ sinh mã sai/fail-open, mâu thuẫn luật, tiêu chí không thể đỏ, hoặc con số chống đỡ lời khai THẨM QUYỀN mà sai. P2 = thiếu/mơ hồ khiến executor tự quyết. P3 = chữ nghĩa. Finding cũ chưa đóng giữ hạng. Nếu KHÔNG còn P1: nói thẳng `approve` hoặc `changes_requested` chỉ P2/P3 — không nâng hạng để kéo dài, không hạ hạng để kết thúc. Nếu còn P1: nêu rõ P1 nào thuộc hình dạng "nguồn tin cậy" (⇒ ADR) và P1 nào không; với S1 nói rõ phần nào là **hợp đồng thiếu** (P1/P2) và phần nào là **quyết định/facts chủ kho chưa cấp** (không phải finding).

## Đầu ra — BẮT BUỘC, ghi vào cwd (ghi sớm, bổ sung dần)
1. `VERDICT.md`: `verdict` · `reviewed_spec_sha256` · `model_tu_khai` · `## Bảng finding lượt 1–6 → trạng thái` · `## Findings mới` · `## Phản chứng đã chạy lại + mới` (ghi rõ hướng nào chỉ MÔ TẢ, harness nào tái dùng/dựng mới) · `## Tiêu chí A1–A12` · `## Bảng đo lại` · `## chua_do_duoc`.
2. `HINT.patch` — unified diff `patch -p0` lên `SPEC.md` cho MỌI P1/P2 còn lại; không còn ⇒ patch 0 hunk + ghi chú.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
Bắt đầu lúc: 2026-09-09T09:30:11Z (phóng lại sau lượt 7a chết preflight; lời gọi vẫn là 8)
