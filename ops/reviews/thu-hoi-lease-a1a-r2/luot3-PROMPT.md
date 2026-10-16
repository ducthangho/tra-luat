# Cross-review ĐẶC TẢ — `THU-HOI-LEASE-A1a` revision 2 **bản nháp 3** · REVIEWER codex · lượt 3 (lời gọi **3/4**)

Bạn là reviewer ĐỘC LẬP (provider khác bên soạn `claude`). Lượt 1: 2 P1 + 5 P2. Lượt 2 (của bạn): 1 P1 + 3 P2 (F8–F11), đã
đóng F1, F3–F7 và F2 một phần. Bản nháp 3 áp `HINT.luot2.patch` của bạn và sửa `do_q6.py` (F11). Còn **một** lời gọi sau lượt này.

**Luật chạy:** read-only với `cay-kho/`; ghi vào cwd và `scratch/`; **CẤM đọc ra ngoài cwd**; không mạng; tối đa 60 phút;
**ghi VERDICT.md SỚM rồi bổ sung dần**. Kho giả Git thường dưới `scratch/` thì được. Hướng cần tự soạn nội dung nhạy cảm
(đường thoát cây, đồng tự Unicode, chuỗi thoát, helper/object Git giả) ⇒ **MÔ TẢ BẰNG LỜI**. Đừng sửa `cay-kho/`.

## Thư mục (cwd)
- `SPEC.md` — **bản nháp 3**, sha256 `fb67bebd45c744ac7d93a85855b6fddb9451a54f3a541e01fa4359108d6217c5`, 350 dòng; cùng nội dung tại
  `cay-kho/ops/specs/THU-HOI-LEASE-A1a-r2.md` (commit `79b8ec7b`).
- `SPEC.nhap2.md` (sha256 `1bfdc7bb…`) · `DIFF.nhap2-nhap3.patch` (spec + script) · `VERDICT.luot1.md` · `VERDICT.luot2.md` · `HINT.luot2.patch`.
- `EVIDENCE.md` — lời khai mới (E12 xử lý lượt 2, E13 master đã tiến, E14 mirror).
- `do_q6.py` (sha256 `f20c0a1a…`) + `q6-do-2026-09-26.json`. Chạy: `python3 -B do_q6.py --tu-kiem cay-kho` và
  `python3 -B do_q6.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z`.
- `cay-kho/` — mirror 435 head, detached tại `79b8ec7b`, `core.abbrev 7`. **`origin` là bare cục bộ.** `master` của mirror = `68b552d0`;
  nền đo của SPEC là `24c48e28` (có trong mirror).

## Việc phải làm
1. **`## ĐỐI CHIẾU LƯỢT TRƯỚC` (bắt buộc):** với TỪNG finding F8–F11 của lượt 2 (và F2 đang ĐÓNG-MỘT-PHẦN), ghi `ĐÓNG` ·
   `ĐÓNG-MỘT-PHẦN` · `CHƯA` · `ĐÓNG SAI`, kèm bằng chứng CHẠY ĐƯỢC. Với các finding lượt 1 đã ĐÓNG: chỉ cần xác nhận bản nháp 3
   không tái mở chúng.
2. **F11 / `do_q6.py`:** chạy `--tu-kiem`; tự đột biến bản sao để kiểm lời khai "7/7 mỗi cái đúng một ca đích"; tìm ca Q6 mà script
   vẫn nhận sai (ID/tên/kiểu/miền/trùng/một chiều/clock). Script phải khớp đúng thuật toán §8.2 — lệch lời văn ⇒ finding.
3. **F8/F9/F10:** seam unit vs CLI của A22; thứ tự ưu tiên `KHONG_XAC_DINH > CHE > KHONG` và mâu thuẫn hai đầu; A19 so DÃY dòng
   với baseline bất biến; ma trận mutant × ca đã khai có nhất quán và đo được không (dựng mô hình dưới `scratch/` như lượt 2).
4. **Đo lại con số mới** (89/89/3/11/3/0, `8f372ccd…`, sha256 script/json, 350 dòng) và kiểm E13 (master tiến không chạm write set).
5. **Chỉ các thay đổi của bản nháp 3 và hệ quả của chúng** là phạm vi chính; phần đã ĐÓNG chỉ xét nếu bị tái mở.
   Không mở lại quyết định chủ kho (F1/F2 — E8 của lượt 2).

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
   reviewed_sha: 79b8ec7b71b04f7b9bdaffebe930fbb9965cd118
   P1: n   P2: n   P3: n
   reviewer_provider: openai_codex
   model_tu_khai: <model/effort bạn tự biết>
   ```
   rồi: `## ĐỐI CHIẾU LƯỢT TRƯỚC` · `## Findings` · `## Bảng đo lại` · `## Nghiệm thu` · `## Phản chứng đã chạy` · `## KHÔNG ĐO ĐƯỢC`.
2. `HINT.patch` — unified diff `patch -p0` lên `SPEC.md` (và nếu cần, một hunk riêng cho `do_q6.py`) cho mọi P1/P2; không có ⇒ tệp rỗng.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
