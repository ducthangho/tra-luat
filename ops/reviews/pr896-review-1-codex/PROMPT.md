# Cross-review lượt 1 PR ducthangho/tra-luat#896 — reviewer: codex — chấm HEAD ĐÃ MERGE

## Đối tượng
- `reviewed_sha`: `816f43988eb3012726120ad00166a989cc2b9af6` (head đã merge của PR #896), base `1ccc314`.
- PR #896 có hai phần: (1) viết lại điểm (c) của `CLAUDE.md` (+31/-34) để KHÔNG chép ma trận `os` nữa mà trỏ nguồn sự thật: output `os` của `chuan-bi` + `exclude:`/`if:` mức job trong `ci.yml`; ca `t162_M4_evaluator_toi_gian_chuan_bi` khoá hành vi ma trận; `t161_M3_chot_nguon_duy_nhat_ma_tran_ci` chỉ khoá cấu trúc; trường `labels`/`runner_id` của job; (2) THÊM khối `bo_sung_sau_landed` vào `ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml` + 3 readback, ghi lượt Codex connector chấm lại sạch trên merge commit `6ac385f`.
- Không có cross-review CLI trước cho #896; Codex connector bắt 1 P2 trên `0bb792b` (`t161` không đánh giá biểu thức — phải trỏ `t162`), executor vá ở `816f439`. Lượt NÀY là cross-review CLI đầu tiên, trên head ĐÃ MERGE `816f439`.

## Nhiệm vụ chính: ĐO LẠI TỪNG KHẲNG ĐỊNH của diff tại `816f43988eb3012726120ad00166a989cc2b9af6`
Mỗi khẳng định có số/SHA/tên job/điều kiện/tên ca phải kiểm bằng lệnh chạy được trong `cay-kho/`. Danh sách dưới KHÔNG đủ — mỗi khẳng định bạn tìm ra mà nó bỏ sót được tính là finding:
1. `t162` có thật sự gọi `_danh_gia_bieu_thuc_chuan_bi` cho push / PR thường / PR nhãn `windows` / từng `runner_set` và assert giá trị kỳ vọng không; `t161` có đúng CHỈ khoá cấu trúc không (đọc thân hàm tại `816f43988eb3012726120ad00166a989cc2b9af6`). Đột biến biểu thức `os` trong bản sao `ci.yml` ở thư mục tạm (KHÔNG sửa `cay-kho/`) rồi chạy riêng `t162`/`t161` để đo răng nếu chạy được.
2. "Ảnh chụp" 23-10-2026 trên `e63961f` (push master/PR thường ⇒ chỉ Ubuntu; dispatch ⇒ hai nền hoặc chỉ Windows với `windows-only`; `launcher-windows.yml` có `paths:`) có khớp `ci.yml` tại `e63961f` và tại `816f43988eb3012726120ad00166a989cc2b9af6` không.
3. Đoạn "có job Windows chưa phải gate đã đo trên Windows" (mảnh 0, `so_ca = len(CA) - len(bo_qua)`, `gate-cong-cu-gop` loại Windows) còn đúng tại `816f43988eb3012726120ad00166a989cc2b9af6` không.
4. Khối `bo_sung_sau_landed`: mọi lời khai `measured` có khớp đúng tệp readback được trích không (comment 6366307732, 6366338141, codex-review-state, reaction +1, blob CLAUDE.md `975cd94…` ở `094e8d1` và `6ac385f`, `git diff --stat 094e8d1 6ac385f`); `sha256sum -c SHA256SUMS.txt` trong thư mục provenance; khối có chỉ THÊM, không sửa dòng cũ (`git diff 1ccc31498b7d37c12305e8f1b5bf2d1fc217b92e 816f43988eb3012726120ad00166a989cc2b9af6 -- ops/land/`). Chạy `python3 ops/land_evidence_nguon.py --root . --tep ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml`.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: 816f43988eb3012726120ad00166a989cc2b9af6`, và một dòng `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

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
P1 = khẳng định sai về sự thật đo được TẠI `816f43988eb3012726120ad00166a989cc2b9af6`. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`.

Chạy thêm hai cổng tại `cay-kho/` và ghi rc + dòng kết luận:
`python3 .claude/dev/packet_loop.py doctrine-scan --root .` và `python3 scripts/tl.py doc-claims-check --json` (đòi `"ok": true`).

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/`, KHÔNG push, KHÔNG gọi mạng (sandbox không có mạng).
Mọi khẳng định phải đo TẠI `816f43988eb3012726120ad00166a989cc2b9af6` — ma trận/tệp ở commit SAU có thể khác, đừng lấy master hiện tại làm chuẩn. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `816f43988eb3012726120ad00166a989cc2b9af6`; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Diff: `diff.patch`, `numstat.txt`.
