# Cross-review ĐẶC TẢ — `THU-HOI-LEASE-A1a` revision 2 · REVIEWER codex · lượt 6 (trần **10**, chủ kho nâng: lặp tới hết P1/P2/P3)

Bạn là reviewer ĐỘC LẬP (provider khác bên soạn `claude`). Các lượt trước: 1 → 2P1+5P2 · 2 → 1P1+3P2 · 3 → 1P1 · 4 → 1P1+1P3
(verdict từng lượt ở `luotK-VERDICT.md`, gợi ý vá ở `luotK-HINT.patch`). Chủ kho đã nâng trần lên 10 và yêu cầu lặp tới khi
**0 P1/P2/P3** (#564 `5851241285`); sạch thì chủ kho human audit.

**Luật chạy:** read-only với `cay-kho/`; ghi vào cwd và `scratch/`; **CẤM đọc ra ngoài cwd**; không mạng; tối đa 60 phút;
**ghi VERDICT.md SỚM rồi bổ sung dần**. Kho giả Git thường dưới `scratch/` thì được. Cô lập cấu hình Git
(`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL` rỗng dưới `scratch/`, `TMPDIR` dưới cwd). Hướng cần tự soạn nội dung nhạy cảm
(đường thoát cây, đồng tự Unicode, chuỗi thoát, helper/object Git giả) ⇒ **MÔ TẢ BẰNG LỜI**. Đừng sửa `cay-kho/`.

## Thư mục (cwd)
- `SPEC.md` — sha256 `c314ce69fdc86ae1f31ac9de25523ac00b9d36f2305811c8a9345cdcec138c47`, 398 dòng; cùng nội dung tại `cay-kho/ops/specs/THU-HOI-LEASE-A1a-r2.md` (commit `635e9a23a3bc7106adbc7af862cb505277b6312c`).
- `SPEC.truoc.md` (bản bạn review lượt 5) · `DIFF.truoc-nay.patch` (spec + `do_q6.py` + `mut_q6.py`).
- `luot1..5-VERDICT.md`, `luotK-HINT.patch`; `EVIDENCE.md` (lời khai phiên soạn cho lượt này).
- `do_q6.py` · `mut_q6.py` · `q6-do-2026-09-26.json` · `tu-kiem-q6-2026-09-26.log` · `mut-q6-2026-09-26.log`.
  Chạy: `python3 -B do_q6.py --tu-kiem cay-kho` · `mkdir -p scratch/m && python3 -B mut_q6.py scratch/m cay-kho do_q6.py` ·
  `python3 -B do_q6.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z`.
- `cay-kho/` — mirror (tập tên head = máy chủ lúc dựng, xem `.mirror-info`), detached tại `635e9a23a3bc7106adbc7af862cb505277b6312c`, `core.abbrev 7`.
  **`origin` là bare CỤC BỘ.** Nền đo của SPEC là `24c48e28`.

## Việc phải làm
1. **`## ĐỐI CHIẾU LƯỢT TRƯỚC` (bắt buộc):** mọi finding của lượt 5 và mọi finding còn `ĐÓNG-MỘT-PHẦN`: `ĐÓNG` ·
   `ĐÓNG-MỘT-PHẦN` · `CHƯA` · `ĐÓNG SAI`, kèm bằng chứng CHẠY ĐƯỢC. Xác nhận delta không tái mở finding đã ĐÓNG.
2. **Delta** (`DIFF.truoc-nay.patch`) và hệ quả: lời văn khớp script/bản in; con số đo lại được; các ca/mutant mới có đúng
   tập đích khai; tự đột biến bản sao để tìm chốt/ca chưa phân biệt được.
3. Không mở lại quyết định chủ kho (F1 prediction-only, F2 Q6 cây mốc + (b), ngoại lệ ADR-0044 ≤3 tệp ≤663 dòng, trần 10).
   Phần đã ĐÓNG chỉ xét lại nếu delta tái mở.

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
   reviewed_sha: 635e9a23a3bc7106adbc7af862cb505277b6312c
   P1: n   P2: n   P3: n
   reviewer_provider: openai_codex
   model_tu_khai: <model/effort bạn tự biết>
   ```
   rồi: `## ĐỐI CHIẾU LƯỢT TRƯỚC` · `## Findings` · `## Bảng đo lại` · `## Nghiệm thu` · `## Phản chứng đã chạy` · `## KHÔNG ĐO ĐƯỢC`.
2. `HINT.patch` — unified diff `patch -p0` cho mọi P1/P2/P3 (SPEC và/hoặc script); không có ⇒ tệp rỗng.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
