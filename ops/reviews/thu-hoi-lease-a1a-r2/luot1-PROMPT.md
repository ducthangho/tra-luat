# Cross-review ĐẶC TẢ — `THU-HOI-LEASE-A1a` **revision 2** · REVIEWER codex · lượt 1 (lời gọi **1/4**)

Bạn là reviewer ĐỘC LẬP (provider khác executor `claude`). Việc: review một **đặc tả** (chưa có mã). Trần 4 lời gọi do
chủ kho nâng (#564 comment `5847670544`). Sau vòng này, phiên điều phối vá theo LỚP rồi gọi lượt kế.

**Luật chạy:** read-only với `cay-kho/` (chỉ ghi vào cwd và thư mục tạm bạn tự tạo dưới cwd, vd `scratch/`); **CẤM đọc ra
ngoài cwd**; không mạng; tối đa 60 phút; **ghi VERDICT.md SỚM rồi bổ sung dần** (lượt bị ngắt vẫn giữ được phần đã ghi).
Kho giả Git thông thường (git init, bare, nhánh, lease fixture) thì được dựng dưới `scratch/`. Hướng tấn công nào cần tự
soạn nội dung nhạy cảm (đường thoát cây, đồng tự Unicode, chuỗi thoát, helper Git giả) thì **MÔ TẢ BẰNG LỜI**, đừng soạn.

## Thư mục (cwd)
- `SPEC.md` — **revision 2**, sha256 `a5aacafac1e69c78ad3dd56e5c977527600fe6dad320656dd7ed29688f7bc313`, 288 dòng. Cùng nội dung
  tại `cay-kho/ops/specs/THU-HOI-LEASE-A1a-r2.md` (tracked, commit `f8a37c04`).
- `SPEC.r1.md` — revision 1, sha256 `64f92d4026fda7bdeb4326be660614eea2d25f6e30db9a20ff0c1c6aa4f5f37c` (đã land trên master).
- `EVIDENCE.md` — **lời khai** của phiên soạn: nguyên văn hai quyết định chủ kho (#499 `5825988768`, #564 `5847471844`), bản
  in Q1/Q3/(b)/M14/suite. Đo lại những gì đo được offline; cái không đo được (Q1, Q3 cần mạng) ghi KHÔNG ĐO ĐƯỢC.
- `do_bia_mo.py` — script đo tập (b) mà SPEC §8 mục 2 mô tả. Chạy: `python3 -B do_bia_mo.py cay-kho`.
- `cay-kho/` — mirror đầy đủ (430 head), detached tại `f8a37c046f37f1b094d125b3a0c9f833bd0e83a7`, `core.abbrev 7`.
  **`origin` là bare CỤC BỘ `kho.git`**, không phải GitHub. `master` của mirror = `24c48e28` (nền đo của SPEC).
  Protocol: `cay-kho/docs/PROTOCOL_DA_PHIEN.md` (§3.2 §4 §8 §12). Luật L1–L5 của đặc tả: `cay-kho/.claude/skills/soan-spec/SKILL.md`.
  ADR: `cay-kho/docs/adr/0044-*.md` (trần kích thước), `0047-*.md` (nguồn tin cậy). Mã: `cay-kho/ops/lease_publish.py`.

## Việc phải làm
1. **Đo lại mọi con số của SPEC đo được offline** (L5): số dòng/vị trí symbol, 168 ca (đếm `def tNNN`; chạy suite nếu kịp —
   `python3 -B ops/lease_publish_test.py` trên một BẢN SAO `git archive` dưới `scratch/`, ~2–3 phút), tập (b) 4 cặp, bảng
   blob M14, 234/10 cặp, 495/465. Lệch ⇒ finding kèm số của bạn. Nhớ: tập (b) phụ thuộc giờ đo (hạn lease) — so theo
   giờ SPEC khai, và nói rõ bạn đo lúc nào.
2. **Q1/Q3 → M12/M13 có đúng quyết định chủ kho không** (so nguyên văn trong EVIDENCE E1). Đặc biệt: định nghĩa Q3
   (body thô, không `\n` cuối) đã được biến thành chốt ĐỎ được chưa (A18); việc ghim descriptor có mở rộng cửa của
   đường marker MỚI trong `lenh_kiem_thu_hoi_github` ở chế độ chưa kích hoạt không — đọc mã quanh `DESCRIPTOR_Q13_SHA256`.
3. **M4 theo (b)**: miền có đúng "(b) chỉ cặp còn hiệu lực" không; định nghĩa "còn hiệu lực" (CÒN_HẠN + chưa bị thay
   tiếp) có khớp `_phan_loai_lease`/`_bia_mo_doi_xung`; lý lẽ "cặp hết hạn sau mốc vô hại" có đúng với `_du_bao_check`;
   hạn chế "cặp sinh sau mốc bị dự báo 8, A1b phải ghim lại" có đủ không hay là lỗ.
4. **M14 (#564 dạng 2)**: thiết kế "bia mộ đối xứng trên nhánh mặc định che mọi bản sao cùng `lease_id`" — có fail-open
   không (ai ghi được vào `refs/remotes/origin/master` cục bộ? bia mộ đối xứng mà lease thay thế nằm ở đâu?); có ca nào
   một lease ĐANG SỐNG bị tắt nhầm; bẫy khử trùng `muc['ref']` có thật không (tự dựng kho giả dưới `scratch/` và chạy
   `lenh_ai_dang_giu` hiện tại để tái hiện); A19–A22 có phân biệt được bằng đầu vào không (mỗi chốt một đột biến riêng).
5. **Nghiệm thu A1–A22**: ca nào không thể đỏ, không thể xanh, đột biến sai ca, hoặc thiếu ca cho một nhánh của mục tiêu.
6. **Nhất quán luật**: protocol §3.2/§4/§8/§12, ADR-0044 (§8 mục 1: đặc tả khai ước 392–611 dòng và KHÔNG tự chọn ngoại
   lệ/tách — có hợp lệ không), ADR-0047, CLAUDE.md của kho. `write_set` có đúng ba đường và đủ cho M12–M14 không.

## Xếp hạng
P1 = đặc tả sẽ sinh mã sai/fail-open, mâu thuẫn luật, tiêu chí không thể đỏ, hoặc con số chống đỡ một lời khai THẨM
QUYỀN mà sai. P2 = thiếu/mơ hồ khiến executor phải tự quyết, hoặc con số sai không chống đỡ thẩm quyền. P3 = chữ nghĩa.
Mỗi finding: **lớp** (một cụm từ kebab-case, vd `loi-khai-rong-hon-phep-do`), vị trí trong SPEC, bằng chứng CHẠY ĐƯỢC
(lệnh + output), và đề xuất sửa. Không nâng hạng để kéo dài, không hạ hạng để kết thúc. Không còn P1/P2/P3 ⇒ nói thẳng
`approve`.

## Đầu ra — BẮT BUỘC, ghi vào cwd
1. `VERDICT.md`, mở đầu bằng khối:
   ```
   verdict: approve | changes_requested | blocked
   reviewed_spec_sha256: <sha256 SPEC.md bạn đã đọc>
   reviewed_sha: f8a37c046f37f1b094d125b3a0c9f833bd0e83a7
   P1: n   P2: n   P3: n
   reviewer_provider: openai_codex
   model_tu_khai: <model/effort bạn tự biết>
   ```
   rồi các mục: `## Findings` · `## Bảng đo lại` (số SPEC | số bạn đo | lệnh | giờ) · `## Nghiệm thu A1–A22` ·
   `## Phản chứng đã chạy` (ghi rõ hướng nào chỉ MÔ TẢ) · `## KHÔNG ĐO ĐƯỢC`.
2. `HINT.patch` — unified diff `patch -p0` lên `SPEC.md` cho mọi P1/P2; không có ⇒ tệp rỗng kèm một dòng ghi chú trong VERDICT.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
