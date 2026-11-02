# Cross-review PR ducthangho/tra-luat#889 — reviewer: codex

Bạn là reviewer CHỈ ĐỌC + ĐO. KHÔNG sửa `cay-kho/`, KHÔNG push, KHÔNG gọi mạng (sandbox không có mạng).
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`.

## Đối tượng
- `reviewed_sha`: `8d5cccbb13b0b2c5ba1c9bbc4f8af410a19f87b8` (head PR #889), base `e63961f` (= origin/master lúc mở PR).
- Diff: `diff.patch`, `numstat.txt` (chỉ `CLAUDE.md`, +9/-0). Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng reviewed_sha; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Thứ định danh tệp là SHA, không phải tên nhánh.
- PR thêm 9 dòng vào bài học "HỎI CHỖ TIỆN TAY…" điểm (c) của `CLAUDE.md`: (1) "Đo lại 23-10-2026": `runner_set=windows-only` (#878) ⇒ `["windows-latest"]`; (2) "gate trên Windows" từ #879 là MỘT PHẦN gate (`gate-cong-cu` Windows chỉ mảnh 0, ca nền rồi dừng; bán kính đột biến chỉ Ubuntu; `gate-cong-cu-gop` loại Windows và `skipped` với `windows-only`; 6 bước `ci.yml` có `if:` theo `runner.os`).

## Nhiệm vụ chính: ĐO LẠI TỪNG KHẲNG ĐỊNH của 9 dòng mới
Mỗi khẳng định có số/SHA/tên job/điều kiện phải kiểm bằng lệnh chạy được trong `cay-kho/`. Danh sách dưới KHÔNG đủ — mỗi khẳng định bạn tìm ra mà nó bỏ sót được tính là finding:
1. `outputs.os` của job `chuan-bi` tại reviewed_sha: ba nhánh (push, dispatch `windows-only`, dispatch mặc định). Kho có evaluator `_danh_gia_bieu_thuc_chuan_bi` trong `ops/lease_publish_test.py` — trích nguyên hàm bằng AST rồi chạy trên biểu thức thật (đừng import cả module). Giá trị mặc định của input `runner_set` là gì?
2. `gate-cong-cu`: Windows có đúng chỉ mảnh 0 không (đọc `exclude:`); trên Windows `ops/cong_cu_test.py` có thật "chạy đủ ca nền rồi dừng", không đo bán kính đột biến không — đọc `nen_bo_qua_dot_bien` / `dat_windows` / `dong_windows` trong `ops/cong_cu_test.py`, và nếu chạy được thì gọi chúng trên đầu vào giả lập nền `nt`.
3. `gate-cong-cu-gop`: `exclude: windows-latest` và `if:` đòi `ubuntu-latest` trong `os` ⇒ với `os=["windows-latest"]` job có `skipped` thật không (lưu ý: `exclude` làm ma trận RỖNG có thể là lỗi chứ không phải skip — `if:` mức job có chạy TRƯỚC khi mở ma trận không? nói rõ cái nào ĐO được, cái nào KHÔNG ĐO ĐƯỢC không mạng).
4. "Các job `gate*` còn lại vẫn có mặt trên Windows ở MỨC JOB": liệt kê mọi job, matrix, `exclude`, `if:` mức job.
5. "6 bước trong `ci.yml` mang `if:` theo `runner.os`": đếm lại (kể cả biểu thức trong `${{ }}`, `matrix.os`, `runner.os` ở dạng khác) — con số 6 đúng không, và có bước nào tắt trên Windows bằng cách KHÁC (`matrix.os`, shell, `continue-on-error`) mà câu bỏ sót không?
6. Commit `be00ef7` (#879) và chú thích của nó có nói đúng những gì câu mới trích không.
7. Câu mới có mâu thuẫn với chỗ KHÁC của `CLAUDE.md` (cả đoạn (c) cũ, mục "API CHỈ CÓ TRÊN MỘT NỀN", mục "Không phải packet nào cũng route sang phiên cloud được") hay với `docs/PROTOCOL_DA_PHIEN.md`/`docs/adr/0049*` không? Có câu nào khác trong `CLAUDE.md` vẫn khai "gọi tay ⇒ hai nền" vô điều kiện không?

Chạy thêm hai cổng tại `cay-kho/` và ghi rc + dòng kết luận:
`python3 .claude/dev/packet_loop.py doctrine-scan --root .` và `python3 scripts/tl.py doc-claims-check --json` (đòi `"ok": true`).

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` NGAY khi bắt đầu (dòng `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, kèm `reviewed_sha: 8d5cccbb13b0b2c5ba1c9bbc4f8af410a19f87b8`, và một dòng `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc:
```
verdict: ...
reviewed_sha: ...

## BẢNG ĐO
| khẳng định | PR khai | đo được (lệnh) | khớp? |

## BẢNG SĂN   (>= 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT)
HƯỚNG n: <tên>
  giả thuyết : ...
  lệnh       : ...
  output     : ...
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC

### <slug-kebab>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ NGHIỆM: <lệnh + kết quả, hoặc KHÔNG ĐO ĐƯỢC + lý do>
ĐỘ TIN: cao/vừa/thấp
```
P1 = khẳng định sai về sự thật đo được. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
