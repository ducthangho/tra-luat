# Cross-review ĐẶC TẢ — `THU-HOI-LEASE-A1a` revision 2 **bản nháp 2** · REVIEWER codex · lượt 2 (lời gọi **2/4**)

Bạn là reviewer ĐỘC LẬP (provider khác bên soạn `claude`). Lượt 1 (của bạn) trả `changes_requested` 2 P1 + 5 P2 trên bản nháp 1.
Sau lượt 1 đã chạy checkpoint §12 và chủ kho quyết hai câu (EVIDENCE E8): **F1 ⇒ M14 chỉ còn dự báo**; **F2 ⇒ giữ nguồn Q6
(cây mốc A0) + lọc (b)**. Bản nháp 2 thực thi hai quyết định ấy và vá F3–F7.

**Luật chạy:** read-only với `cay-kho/`; ghi vào cwd và `scratch/` dưới cwd; **CẤM đọc ra ngoài cwd**; không mạng; tối đa 60 phút;
**ghi VERDICT.md SỚM rồi bổ sung dần**. Kho giả Git thường thì được dựng dưới `scratch/`. Hướng nào cần tự soạn nội dung nhạy cảm
(đường thoát cây, đồng tự Unicode, chuỗi thoát, helper Git giả, object giả) thì **MÔ TẢ BẰNG LỜI**. Đừng sửa `cay-kho/`.

## Thư mục (cwd)
- `SPEC.md` — **bản nháp 2**, sha256 `1bfdc7bbe15bf28543fcdbdc3269f78beb0f00ffd5e5e510b11de1a66bd58cc6`, 316 dòng; cùng nội dung tại
  `cay-kho/ops/specs/THU-HOI-LEASE-A1a-r2.md` (commit `981b9ea1`).
- `SPEC.nhap1.md` (sha256 `a5aacafa…`, bản bạn review lượt 1) · `DIFF.nhap1-nhap2.patch` · `SPEC.r1.md` (`64f92d40…`, đã land).
- `VERDICT.luot1.md` (sha256 `bec95f09…`) + `HINT.luot1.patch` + `EVIDENCE.luot1.md` — lượt 1 của **chính bạn**.
- `EVIDENCE.md` — lời khai mới (E8 quyết định chủ kho nguyên văn, E9 Q6, E10 #589, E11 mirror).
- `do_q6.py` + `q6-do-2026-09-26.json` — script và bản in dẫn xuất Q6+(b). Chạy: `python3 -B do_q6.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z`.
  `do_bia_mo.py` — script quét mọi ref của bản nháp 1 (nay chỉ còn chẩn đoán).
- `cay-kho/` — mirror 435 head (tập tên = máy chủ lúc 22:54:33Z), detached tại `981b9ea1`, `core.abbrev 7`. **`origin` là bare cục bộ.**
  `master` của mirror = `24c48e28`. PR #589 head `23e16979` có trong mirror (nhánh `claude/va-dang-lease-20260920`).

## Việc phải làm
1. **`## ĐỐI CHIẾU LƯỢT TRƯỚC` (bắt buộc):** với TỪNG finding F1–F7 của lượt 1, ghi `ĐÓNG` · `ĐÓNG-MỘT-PHẦN` · `CHƯA` · `ĐÓNG SAI`,
   kèm bằng chứng CHẠY ĐƯỢC. Riêng F1/F2 xét **đúng quyết định chủ kho** (E8), không xét lại quyết định; hỏi: bản nháp 2 có thực thi
   đúng quyết định ấy, và có còn chỗ nào **trao thẩm quyền** cho một nguồn chưa xác minh không.
2. **M14 dự báo:** bất biến "dự báo không đổi `rc`/`NGƯỜI_GIỮ`/dòng không-`DU_BAO`" có đủ và đo được không (A19); định nghĩa
   `CHE/KHONG/KHONG_XAC_DINH` §5.1 có kẽ nào (cặp chia nhánh, YAML hỏng, trùng `lease_id`, ref vắng); A19–A22 mỗi đột biến có
   đúng một ca đích không. Dựng kho giả dưới `scratch/`, dùng `lenh_ai_dang_giu` hiện tại của mirror làm đối chứng.
3. **M4 Q6 + (b):** chạy lại `do_q6.py` trên mirror; so với `q6-do-2026-09-26.json`; kiểm thuật toán có đúng r9 Q6
   (`cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md`, mục Q6) + (b) không; clock ghim có hợp lý; A6/A7/A7b có răng; lời khai "không
   phụ thuộc clock với mọi C ≥ 2026-09-08T10:17:12Z" có đúng. Có thể dựng một cây giả nhỏ để đột biến script.
4. **A4, A16, A18** sau vá: đủ đột biến, đúng seam, baseline bất biến.
5. **Đo lại mọi con số mới** của bản nháp 2 đo được offline (L5): 11/3/92/digest `8f372ccd…`, hạn muộn nhất, giờ mốc, +161/−2, 2206 và
   các vị trí symbol tại `23e16979`, ước dòng 422–663 (tổng số hạng). Lệch ⇒ finding.
6. Nhất quán luật (protocol §3.2 §4 §8 §12, ADR-0044, ADR-0047, CLAUDE.md) và `write_set` còn đủ/đúng.

## Xếp hạng
P1 = sinh mã sai/fail-open, mâu thuẫn luật hoặc quyết định chủ kho, tiêu chí không thể đỏ, con số chống đỡ lời khai THẨM QUYỀN mà sai.
P2 = mơ hồ khiến executor tự quyết, hoặc con số sai không chống đỡ thẩm quyền. P3 = chữ nghĩa. Mỗi finding: **lớp** (kebab-case;
dùng lại tên lớp lượt 1 nếu cùng lớp), vị trí, bằng chứng chạy được, đề xuất sửa. Không nâng/hạ hạng để kéo dài hay kết thúc.
Không còn P1/P2/P3 ⇒ `approve`.

## Đầu ra — BẮT BUỘC, ghi vào cwd
1. `VERDICT.md`, mở đầu:
   ```
   verdict: approve | changes_requested | blocked
   reviewed_spec_sha256: <sha256 SPEC.md bạn đã đọc>
   reviewed_sha: 981b9ea1d4bfaa0511cfbc8d9bdee9d8c151c86f
   P1: n   P2: n   P3: n
   reviewer_provider: openai_codex
   model_tu_khai: <model/effort bạn tự biết>
   ```
   rồi: `## ĐỐI CHIẾU LƯỢT TRƯỚC` · `## Findings` · `## Bảng đo lại` (số SPEC | số bạn đo | lệnh | giờ) · `## Nghiệm thu` ·
   `## Phản chứng đã chạy` (ghi rõ hướng nào chỉ MÔ TẢ) · `## KHÔNG ĐO ĐƯỢC`.
2. `HINT.patch` — unified diff `patch -p0` lên `SPEC.md` cho mọi P1/P2; không có ⇒ tệp rỗng + một dòng ghi chú trong VERDICT.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
