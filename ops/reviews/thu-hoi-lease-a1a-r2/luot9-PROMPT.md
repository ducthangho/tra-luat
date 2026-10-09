# Cross-review — `THU-HOI-LEASE-A1a` **revision 3** + hậu kiểm connector (PR #658) · REVIEWER codex · lượt **9** (trần **10**)

Bạn là reviewer ĐỘC LẬP (provider khác bên soạn `claude`). Lượt 8 (verdict `luot8-VERDICT.md`) cho `changes_requested`
2 P1: **F17** (lời khai lịch sử đối chiếu ref ở bảng S) và **F18** (đặc tả r2 đóng băng vẫn bắt executor chạy bộ đo mang
lỗi C5/C6). Chủ kho quyết (vòng 5, #564 `5852159297`): làm **revision 3 tối thiểu** chỉ đổi chỉ dẫn bộ đo thi công.
Lượt này là lượt **9/10**; lượt 10 là lượt cuối cùng có thể có.

**Luật chạy:** read-only với `cay-kho/`; ghi vào cwd và `scratch/`; **CẤM đọc ra ngoài cwd**; không mạng; tối đa 60 phút;
**ghi VERDICT.md SỚM rồi bổ sung dần**. Kho giả Git thường dưới `scratch/` thì được. Cô lập cấu hình Git
(`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL` rỗng dưới `scratch/`, `TMPDIR` dưới cwd). Hướng cần tự soạn nội dung nhạy cảm
(đường thoát cây, đồng tự Unicode, chuỗi thoát, helper/object Git giả) ⇒ **MÔ TẢ BẰNG LỜI**. Đừng sửa `cay-kho/`.

**Quy tắc mới từ lượt này (chủ kho, vòng 5):** mọi sửa nhắm **đặc tả** (`SPEC.md`) chỉ được **mô tả bằng lời** trong
VERDICT — **không** đưa hunk nào vào `SPEC.md` trong `HINT.patch`. Sửa nhắm script/hiện vật review thì vẫn được dùng
`HINT.patch` (có nhãn).

## Thư mục (cwd)
- `SPEC.md` — **revision 3**, sha256 `ac7e0129b281b517c69e9a2512a05b47d55ad99f0ac964462c061ea511f70bc1`, 436 dòng; cùng nội dung tại `cay-kho/ops/specs/THU-HOI-LEASE-A1a-r3.md`.
- `SPEC.r2.md` — revision 2 đã đóng băng (sha256 `9bc0fe28…`); `DIFF.r2-r3.patch` — toàn bộ khác biệt r2→r3.
- `DIFF.luot8-luot9.patch` — thay đổi kho kể từ head lượt 8 (`d766717`); `DIFF.pr658.patch` — toàn bộ PR #658 so `master`.
- `luot1..8-VERDICT.md`, `luot1..8-HINT.patch`, `luot1..8-PROMPT.md`, `luot1..8-EVIDENCE.md`; `EVIDENCE.md` — lời khai phiên soạn lượt này.
- `HAU-KIEM-CONNECTOR-652.md` (bảng S đã viết lại theo từng lượt — F17), `CONNECTOR-652.md` (finding connector, dữ liệu).
- `do_q6.py` · `mut_q6.py` — bản gốc r2 trích băm, **phải giữ nguyên byte**. `do_q6_hk.py` · `mut_q6_hk.py` — bộ đo thi công r3.
  Log: `tu-kiem-q6-2026-09-27.log`, `mut-q6-2026-09-27.log`; `q6-do-2026-09-26.json`.
- `cay-kho/` — clone, detached tại `3f1bf2e2e5a77ec2bb1a40bb65b8c26410a3ff12`, `core.abbrev 7`, `origin` = `https://github.com/ducthangho/tra-luat.git`; tập
  (tên nhánh, OID) dưới `refs/remotes/origin/*` đã đối chiếu với `git ls-remote --heads` của máy chủ, lệch **0**
  (`.mirror-info`, `.tap-ten-oid-may-chu.txt`). Sandbox không mạng.

## Việc phải làm
1. **`## ĐỐI CHIẾU LƯỢT TRƯỚC` (bắt buộc):** F17, F18 của lượt 8 và mọi mục lượt 8 xếp `ĐÓNG-MỘT-PHẦN` (C3, C4, C5, C6):
   `ĐÓNG` · `ĐÓNG-MỘT-PHẦN` · `CHƯA` · `ĐÓNG SAI`, kèm bằng chứng CHẠY ĐƯỢC.
2. **Revision 3:** `DIFF.r2-r3.patch` có đúng là chỉ đổi chỉ dẫn bộ đo thi công + header + §0 vòng 5 không; mọi phần khác
   có nguyên văn r2 không. Khối "Bộ đo THI CÔNG": băm khớp tệp; ba lệnh chạy được đúng như viết; **tiêu chí dương có
   thể ĐỎ** không (dựng bản in giả hoặc đột biến bản sao script để thử từng tiêu chí đỏ được); có tiêu chí nào để lọt
   một bộ đo sai (ví dụ ma trận khai thêm `mong="LECH"`, script đổi mà băm không được kiểm, tự kiểm đổi số ca).
3. **Bản vá lượt 8:** hai ca/mutant mới (`ten-DEL-sau-duoi`, `ten-byte-sau-duoi`, `bo-rieng-DEL`, `bo-chot-utf8`) có răng
   không; tập đích mở rộng của `doc-ls-tree-khong-z`/`bo-chot-ky-tu-dieu-khien` có đúng thực đo không.
4. Không mở lại quyết định chủ kho (F1 prediction-only, F2 Q6 cây mốc + (b), ngoại lệ ADR-0044 ≤3 tệp ≤663 dòng, trần 10,
   revision 3 tối thiểu, quy tắc mô tả-bằng-lời cho đặc tả). Phần r2 không đổi chỉ xét lại nếu delta tái mở.

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
   reviewed_sha: 3f1bf2e2e5a77ec2bb1a40bb65b8c26410a3ff12
   P1: n   P2: n   P3: n
   reviewer_provider: openai_codex
   model_tu_khai: <model/effort bạn tự biết>
   execution_surface_tu_khai: <điều bạn đo được về bề mặt chạy, hoặc KHONG_DO_DUOC>
   transport_tu_khai: <điều bạn đo được về đường nhận prompt, hoặc KHONG_DO_DUOC>
   ```
   Đừng suy hai trường cuối từ cấu hình được yêu cầu. Rồi: `## ĐỐI CHIẾU LƯỢT TRƯỚC` · `## Findings` · `## Bảng đo lại` ·
   `## Nghiệm thu` · `## Phản chứng đã chạy` · `## KHÔNG ĐO ĐƯỢC`.
2. `HINT.patch` — unified diff `patch -p0` **chỉ** cho script/hiện vật review (không hunk nào vào `SPEC.md`); không có ⇒ tệp
   rỗng. Nếu không rỗng, **dòng đầu tiên** phải là nguyên văn:
   `NHÃN: chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit`.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
