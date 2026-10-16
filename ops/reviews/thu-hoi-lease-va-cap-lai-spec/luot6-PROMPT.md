# Cross-review ĐẶC TẢ — `THU-HOI-LEASE-VA-CAP-LAI` **revision 6** · REVIEWER codex · lượt 6 (lời gọi **7**, trần mới theo comment PR #475 `5578460203`: "review tới hết P1", bộ đếm KHÔNG reset)

Lượt 5 (lời gọi 6/6 của trần cũ `5575587924`) kết luận `changes_requested` + `blocked` chờ ADR. Chủ kho tại Review Rescue
Checkpoint (§12) đã **reroute**: tiếp tục vòng *Claude vá → codex review có HINT* trên PR #475 **cho tới khi hết P1**; lời gọi
này là **7**; mọi ID finding (S1–S6, R, N, L1) giữ nguyên. ADR "nguồn tin cậy cho cổng đọc lease" đang được hỏi chủ kho, **chưa
có** — bạn đánh giá hợp đồng Q4.1/Q4.5 của r6 như HẠT của ADR ấy; đừng lấy "ADR chưa tồn tại" làm P1 tự thân, nhưng nói rõ
điều gì trong r6 vẫn mở nếu không có ADR. §0/Q14 của r6 còn câu kế toán trần cũ ("lời gọi cuối 6/6", "trần 6 lượt") — điều
phối đã biết, sẽ sửa ở r7 cùng finding của bạn; xếp P3, đừng tốn thời gian.

**Phân công như lượt 4b — CẤM tuyệt đối tự soạn** remote helper giả, `remote.<x>.vcs`, `url.*.insteadOf` trỏ kho lạ,
`refs/replace`/graft, biến môi trường Git nhằm đổi nguồn, bytes cache lệch OID, đường thoát cây, đồng tự Unicode, chuỗi
thoát — các hướng ấy chỉ **MÔ TẢ BẰNG LỜI**; bạn chạy **CONTROL hợp lệ** và ĐỌC hợp đồng. Kho giả Git thông thường
(bare/working copy, lease/sổ fixture, symlink nội bộ, merge, mode) vẫn được. **Read-only với kho**; **CẤM đọc ra ngoài
cwd**; không mạng; tối đa 60 phút; **ghi VERDICT.md sớm rồi bổ sung dần**.

## Thư mục
- `SPEC.md` — **revision 6**, sha256 `f78135cff428f0744476d7f27426f459d926578c4bac4a4339928330c4a0d6a5`; cùng nội dung tại `cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (untracked). §0.3 có bảng "S1/S2/S3/S5/S6 → r6 làm gì". Phần vá tập trung ở Q4.1 (hồ sơ adapter + profile digest), Q4.5 (API object-store), A6 (catalog seam), M9 (receipt = workflow artifact, join độc lập), Q3/Q13 (descriptor ghim mã + tệp retired).
- `SPEC.r5.md` (`23a7deaf…`); `VERDICT.luot5.md` (`1596d5627f62aa9958beac4655a9b7135d565bfb4f9949e3d262f64196f595e0`) + `HINT.luot5.patch` (`8ca8474b…`) — của CHÍNH BẠN lượt 5; `VERDICT.luot4b.md` (`7d3017ec…`) + `HINT.luot4b.patch`; `VERDICT.luot3.md`, `VERDICT.luot2.md`, `VERDICT.luot1.md`.
- `cay-kho/` — mirror đầy đủ (`refs/remotes/origin/*` = 309 nhánh máy chủ, đo 03:1xZ 08-09; detached tại `b416830ef2a509d60203d55552ce17950afcf67c` = `base_sha` của spec; `core.abbrev 7`); `origin` là bare cục bộ `../kho.git`. Lưu ý `origin/master` trong mirror nay là `585c7d5` (master đã đi 48 commit sau `b416830`) — spec đóng băng ở `b416830`; nếu bạn thấy mã trên `origin/master` làm một lời khai của r6 sai, nêu kèm SHA.
- `EVIDENCE.md` — lời khai điều phối lượt 1–5 + mục "Bổ sung lượt 6" (số đo container mới).
- **`scratch/` của các lượt trước KHÔNG còn** (container cũ đã huỷ). Bạn phải dựng lại harness hợp lệ trong `scratch/luot6/` — ghi rõ cái nào dựng lại, không tự nhận số cũ là số lượt này.

## Việc phải làm
1. **S1, S2, S3, S5, S6 theo §0.3 r6**: ĐÓNG · ĐÓNG-MỘT-PHẦN · CHƯA · ĐÓNG SAI, kèm bằng chứng. Control hợp lệ cần chạy lại: (a) routing object-store Q4.5 — `GIT_DIR` = repo tạm cô lập + `GIT_OBJECT_DIRECTORY` = objects kho nguồn ⇒ `cat-file --batch` đọc được commit/tree/blob (không `missing`); thiếu routing ⇒ `missing` ⇒ 12; (b) tự đi đồ thị từ bytes đã băm: ancestry S→H, tree cha ⇒ "sổ vắng" chỉ khi tree đã xác minh; (c) profile digest Q4.1: control tính digest từ env dựng từ rỗng + fixture, digest khớp mỏ neo ⇒ 0 (ca âm chỉ mô tả); (d) A6 catalog theo seam (bỏ routing ⇒ (iv) đỏ; bỏ băm ⇒ (i) đỏ; bỏ no-replace ⇒ sống; `refs/replace` ⇒ verdict không đổi); (e) M9 receipt = artifact + join độc lập (đọc hợp đồng, model); (f) Q13: descriptor ghim mã + tệp `ops/thu-hoi/_ngoai-le-closure.retired.yaml`, chuỗi A→B→D với tệp retired còn.
2. **Tấn công r6 ở chỗ MỚI — bằng lời hoặc ca hợp lệ**: (a) Q4.1 profile digest: thành phần nào của digest do CALLER kiểm soát được (đường/băm executable, `git --version`, tệp CA, tên helper) — digest có chống được "cùng digest, khác hành vi" không; mỏ neo `PROFILE_ADAPTER_DA_DUYET` ghim trong mã: ai duyệt, đổi runner/ubuntu image thì chặn oan hay lọt; allowlist khoá hữu hạn có ĐỦ để adapter chạy thật trong container remote (proxy qua `HTTPS_PROXY`, CA bundle riêng) — host proxy ∈ allowlist ghim là gì; (b) Q4.5 `GIT_OBJECT_DIRECTORY` trỏ objects kho nguồn: packfile, `objects/info/alternates`, promisor/partial clone (object thiếu HỢP LỆ), shallow — có bị đọc thành "vắng" rồi 12 oan, hay tệ hơn thành "sổ vắng" ⇒ 0; trần chi phí fail-close có đơn vị chưa; memoize `(type, OID)` có đúng không khi cùng OID hai type; (c) A6 catalog seam nhất quán với Q4.5 chưa; mutant nào còn bị lớp khác che mà r6 vẫn hứa kill; (d) M9: `actions/upload-artifact` — consumer join check-run → run → artifact có đường API thật không (check-run mang gì để tới `run_id`), retention artifact, `workflow_dispatch` "không tạo pass" đủ chưa, dependency `LAND-DOC-RECEIPT-THU-HOI` ngoài write set có làm A1 không thể nghiệm thu; (e) Q13 tệp retired: "T có policy mà thiếu tệp ⇒ 12" — PR nào phải kèm tệp, reader nhìn thấy tệp + policy vắng ⇒ 12 có chặn oan rollback hợp lệ; (f) §0/§12 sau reroute: r6 tự mô tả trạng thái đúng chưa (P3 nếu chỉ chữ).
3. **A1–A12 r6**: đơn vị? phép đỏ thật? đột biến đúng ca? ca không thể đỏ / không thể xanh?
4. **Nhất quán luật** (§3.2 §4 §5 §8 §12; ADR-0025/0028/0044; CLAUDE.md), kích thước slice.
5. **Q7–Q14**: thiếu câu nào; câu nào đã có đáp án bắt buộc.
6. **Đo lại con số r6** đo được offline — kể cả số của chính bạn lượt 5 mà r6 chép (1186 object · 4 311 029 B · ancestry 9 commit · closure 2622 commit); số nào không dựng lại được thì ghi `chua_do_duoc`.

## Xếp hạng
P1 = spec sẽ sinh mã sai/fail-open, mâu thuẫn luật, tiêu chí không thể đỏ, hoặc con số chống đỡ lời khai THẨM QUYỀN mà sai. P2 = thiếu/mơ hồ khiến executor tự quyết. P3 = chữ nghĩa. Finding cũ chưa đóng giữ hạng. Nếu KHÔNG còn P1: nói thẳng `approve` hoặc `changes_requested` chỉ P2/P3 — không nâng hạng để kéo dài, không hạ hạng để kết thúc. Nếu còn P1: nêu rõ P1 nào thuộc hình dạng "nguồn tin cậy" (⇒ ADR) và P1 nào không.

## Đầu ra — BẮT BUỘC, ghi vào cwd (ghi sớm, bổ sung dần)
1. `VERDICT.md`: `verdict` · `reviewed_spec_sha256` · `model_tu_khai` · `## Bảng finding lượt 1–5 → trạng thái` · `## Findings mới` · `## Phản chứng đã chạy lại + mới` (ghi rõ hướng nào chỉ MÔ TẢ, harness nào dựng lại) · `## Tiêu chí A1–A12` · `## Bảng đo lại` · `## chua_do_duoc`.
2. `HINT.patch` — unified diff `patch -p0` lên `SPEC.md` cho MỌI P1/P2 còn lại; không còn ⇒ patch 0 hunk + ghi chú.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
Bắt đầu lúc: 2026-09-08T03:12:57Z
