# Cross-review ĐẶC TẢ — `THU-HOI-LEASE-A1a` revision 2 **bản nháp 4** · REVIEWER codex · lượt 4 (lời gọi **4/4 — CUỐI**)

Bạn là reviewer ĐỘC LẬP (provider khác bên soạn `claude`). Lịch sử: lượt 1 2 P1 + 5 P2 · lượt 2 1 P1 + 3 P2 · lượt 3 (của bạn)
1 P1 (F12 `q6-thieu-kiem-id-ten`, tồn dư F11), đã đóng F8–F10. Bản nháp 4 áp `HINT.luot3.patch` và rà mọi trường Q6 đọc (E15).
**Đây là lời gọi CUỐI trong trần 4.** Sau lượt này: sạch ⇒ chủ kho human audit; còn P1/P2/P3 ⇒ phiên soạn dừng, đưa chủ kho quyết.

**Luật chạy:** read-only với `cay-kho/`; ghi vào cwd và `scratch/`; **CẤM đọc ra ngoài cwd**; không mạng; tối đa 60 phút;
**ghi VERDICT.md SỚM rồi bổ sung dần**. Kho giả Git thường dưới `scratch/` thì được. Hướng cần tự soạn nội dung nhạy cảm
(đường thoát cây, đồng tự Unicode, chuỗi thoát, helper/object Git giả) ⇒ **MÔ TẢ BẰNG LỜI**. Đừng sửa `cay-kho/`.
Cô lập cấu hình Git như lượt 3 (`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL` rỗng dưới `scratch/`).

## Thư mục (cwd)
- `SPEC.md` — **bản nháp 4**, sha256 `b8856466da6638054f1f379c6118176177efd0b3dbbdaad2c37b2210345f0190`, 379 dòng; cùng nội dung tại
  `cay-kho/ops/specs/THU-HOI-LEASE-A1a-r2.md` (commit `33e19c41`).
- `SPEC.nhap3.md` (`fb67bebd…`) · `DIFF.nhap3-nhap4.patch` (spec + `do_q6.py` + `mut_q6.py`) · `VERDICT.luot{1,2,3}.md` · `HINT.luot3.patch`.
- `EVIDENCE.md` (E15, E16). `do_q6.py` (`040bfd0d…`) · `mut_q6.py` (`d74c282f…`) · `q6-do-2026-09-26.json` · `tu-kiem-q6-2026-09-26.log` · `mut-q6-2026-09-26.log`.
  Chạy: `python3 -B do_q6.py --tu-kiem cay-kho` · `python3 -B mut_q6.py scratch/m cay-kho do_q6.py` (tạo `scratch/m` trước) ·
  `python3 -B do_q6.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z`.
- `cay-kho/` — mirror 437 head, detached tại `33e19c41`, `core.abbrev 7`. **`origin` là bare cục bộ.** `master` = `68b552d0`; nền đo SPEC `24c48e28`.

## Việc phải làm
1. **`## ĐỐI CHIẾU LƯỢT TRƯỚC` (bắt buộc):** F12 (và F11/F2 đang ĐÓNG-MỘT-PHẦN): `ĐÓNG` · `ĐÓNG-MỘT-PHẦN` · `CHƯA` · `ĐÓNG SAI`,
   kèm bằng chứng CHẠY ĐƯỢC. Xác nhận bản nháp 4 không tái mở finding đã ĐÓNG.
2. **Lời khai E15 "mọi trường thuật toán đọc đã có chốt":** kiểm bằng cách đọc code `dan_xuat` và tìm trường/nhánh còn nhận sai;
   tái lập `mut_q6.py` (14/14) và thử **đột biến của riêng bạn** — tập ca đích khai trong script có đúng là tập đo được không,
   còn chốt nào không có mutant hay ca nào không phân biệt được chốt.
3. **Delta bản nháp 4 trên SPEC** (§8.2, header): lời văn khớp script/bản in; con số (24/24, 14/14, 89/89, băm) đo lại được.
4. Phạm vi chính là delta nháp 3 → nháp 4 và hệ quả. Không mở lại quyết định chủ kho (F1/F2, E8 lượt 2).

## Xếp hạng
P1 = sinh mã sai/fail-open, mâu thuẫn luật hoặc quyết định chủ kho, tiêu chí không thể đỏ, con số chống đỡ lời khai THẨM QUYỀN mà sai.
P2 = mơ hồ khiến executor tự quyết, hoặc con số sai không chống đỡ thẩm quyền. P3 = chữ nghĩa. Mỗi finding: **lớp** (kebab-case;
dùng lại tên lớp cũ nếu cùng lớp), vị trí, bằng chứng chạy được, đề xuất sửa. Không nâng/hạ hạng để kéo dài hay kết thúc.
Không còn P1/P2/P3 ⇒ `approve`.

## Đầu ra — BẮT BUỘC, ghi vào cwd
1. `VERDICT.md`, mở đầu:
   ```
   verdict: approve | changes_requested | blocked
   reviewed_spec_sha256: <sha256 SPEC.md bạn đã đọc>
   reviewed_sha: 33e19c4121d32aeb4497c28214d7d3ffa20c9c08
   P1: n   P2: n   P3: n
   reviewer_provider: openai_codex
   model_tu_khai: <model/effort bạn tự biết>
   ```
   rồi: `## ĐỐI CHIẾU LƯỢT TRƯỚC` · `## Findings` · `## Bảng đo lại` · `## Nghiệm thu` · `## Phản chứng đã chạy` · `## KHÔNG ĐO ĐƯỢC`.
2. `HINT.patch` — unified diff `patch -p0` cho mọi P1/P2 (SPEC và/hoặc script); không có ⇒ tệp rỗng.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
