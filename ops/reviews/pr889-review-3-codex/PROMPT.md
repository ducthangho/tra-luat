# Cross-review lượt 3 PR ducthangho/tra-luat#889 — reviewer: codex — chấm HEAD ĐÃ MERGE

## Đối tượng
- `reviewed_sha`: `094e8d17ae4dfcf21dca63702c9262267bdc072c` (head đã merge của PR #889), base `e63961f`.
- PR #889 thêm vào điểm (c) của `CLAUDE.md` (+12/-0): (1) "Đo lại 23-10-2026": `runner_set=windows-only` (#878) ⇒ `["windows-latest"]`; (2) "gate trên Windows" từ #879 là MỘT PHẦN gate (`gate-cong-cu` Windows chỉ mảnh 0; bán kính đột biến chỉ Ubuntu; `gate-cong-cu-gop` loại Windows và `skipped` với `windows-only`; 6 bước `ci.yml` có `if:` theo `runner.os`).
- Lượt cross-review trước (ops/reviews/pr889-review-1-codex-verdict.md, chấm `8d5cccb`) ra 1 P2 `windows-green-does-not-prove-all-baselines`; executor vá ở `094e8d1` bằng HINT.patch + sửa thêm một câu. Lượt NÀY chấm lại trên head ĐÃ MERGE `094e8d1` — kiểm cả phần sửa thêm ngoài HINT.patch.

- Đã có một lượt 2 approve trên CÙNG head (`ops/reviews/pr889-review-2-codex-verdict.md`, KHÔNG có trong `cay-kho/` tại head này). Lượt NÀY là lượt độc lập, chạy lại vì launcher mới ghi được model máy chủ trả; đừng tìm đọc verdict lượt 2 — tự đo từ đầu.

## Nhiệm vụ chính: ĐO LẠI TỪNG KHẲNG ĐỊNH của diff tại `094e8d17ae4dfcf21dca63702c9262267bdc072c`
Mỗi khẳng định có số/SHA/tên job/điều kiện/tên ca phải kiểm bằng lệnh chạy được trong `cay-kho/`. Danh sách dưới KHÔNG đủ — mỗi khẳng định bạn tìm ra mà nó bỏ sót được tính là finding:
1. `outputs.os` của `chuan-bi` tại `094e8d17ae4dfcf21dca63702c9262267bdc072c`: ba nhánh dispatch (`windows-only`, mặc định, giá trị khác) + push + PR; giá trị mặc định của input `runner_set`. Dùng `_danh_gia_bieu_thuc_chuan_bi` trích bằng AST.
2. `gate-cong-cu`: Windows có đúng chỉ mảnh 0 không (`exclude:`); `ops/cong_cu_test.py` trên Windows có duyệt ca nền rồi DỪNG không (`nen_bo_qua_dot_bien`/`dat_windows`/`dong_windows`); dòng `so_ca = len(CA) - len(bo_qua)` có thật tại `094e8d17ae4dfcf21dca63702c9262267bdc072c`.
3. `gate-cong-cu-gop`: `exclude: windows-latest` và `if:` đòi `ubuntu-latest` ⇒ với `os=["windows-latest"]` job `skipped` thật không; nói rõ cái nào ĐO được, cái nào KHÔNG ĐO ĐƯỢC không mạng.
4. Đếm lại số bước trong `ci.yml` có `if:` theo `runner.os` (kể cả dạng `matrix.os`); con số 6 đúng không.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: 094e8d17ae4dfcf21dca63702c9262267bdc072c`, và một dòng `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

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
P1 = khẳng định sai về sự thật đo được TẠI `094e8d17ae4dfcf21dca63702c9262267bdc072c`. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`.

Chạy thêm hai cổng tại `cay-kho/` và ghi rc + dòng kết luận:
`python3 .claude/dev/packet_loop.py doctrine-scan --root .` và `python3 scripts/tl.py doc-claims-check --json` (đòi `"ok": true`).

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/`, KHÔNG push, KHÔNG gọi mạng (sandbox không có mạng).
Mọi khẳng định phải đo TẠI `094e8d17ae4dfcf21dca63702c9262267bdc072c` — ma trận/tệp ở commit SAU có thể khác, đừng lấy master hiện tại làm chuẩn. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `094e8d17ae4dfcf21dca63702c9262267bdc072c`; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Diff: `diff.patch`, `numstat.txt`.
