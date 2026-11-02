# Cross-review lượt 2 PR ducthangho/tra-luat#870 — reviewer: codex — chấm HEAD ĐÃ MERGE

## Đối tượng
- `reviewed_sha`: `06a50c5feea77c2654f31edd26efeed7eeee62f5` (head đã merge của PR #870), base `9e9a74b`.
- PR #870 sửa bài học "HỎI CHỖ TIỆN TAY…" điểm (c) của `CLAUDE.md` (+21/-9): câu cũ "master chạy cả ubuntu lẫn windows" đã chết từ packet #548; viết lại theo output `os` của job `chuan-bi` trong `.github/workflows/ci.yml`, dẫn run 39354156843, readback `ops/land/pr848-wp744-provenance/readback-jobs-39354156843.json`, P1 PR #859 comment r4323607674, sửa ở PR #865.
- Lượt cross-review trước (ops/reviews/pr870-review-1-codex-verdict.md, chấm `b38fce8`) ra 1 P2 `master-windows-bo-sot-dispatch`; executor vá ở `06a50c5` bằng đúng HINT.patch. Lượt NÀY chấm lại trên head ĐÃ MERGE `06a50c5` — kiểm cả việc P2 cũ đã đóng thật chưa.

## Nhiệm vụ chính: ĐO LẠI TỪNG KHẲNG ĐỊNH của diff tại `06a50c5feea77c2654f31edd26efeed7eeee62f5`
Mỗi khẳng định có số/SHA/tên job/điều kiện/tên ca phải kiểm bằng lệnh chạy được trong `cay-kho/`. Danh sách dưới KHÔNG đủ — mỗi khẳng định bạn tìm ra mà nó bỏ sót được tính là finding:
1. `outputs.os` của job `chuan-bi` tại `06a50c5feea77c2654f31edd26efeed7eeee62f5`: mọi nhánh (push master, PR thường, PR nhãn `windows`, `workflow_dispatch`). Trích nguyên `_danh_gia_bieu_thuc_chuan_bi` từ `ops/lease_publish_test.py` bằng AST rồi chạy trên biểu thức thật tại `06a50c5feea77c2654f31edd26efeed7eeee62f5` (đừng import cả module).
2. Run 39354156843 = 23 job, cả 23 nhãn `ubuntu-latest`: đếm lại trong tệp readback; commit `3a3a3ca`, `3f6c694` có tồn tại và nói đúng những gì câu trích không (`git show`).
3. Đoạn về `launcher-windows.yml` (`paths:`, ma trận, `types: [..., labeled]`) và "các workflow còn lại đều `ubuntu-latest`": liệt kê mọi workflow tại `06a50c5feea77c2654f31edd26efeed7eeee62f5`.
4. Câu mới có mâu thuẫn với chỗ KHÁC của `CLAUDE.md` tại `06a50c5feea77c2654f31edd26efeed7eeee62f5` hay với `docs/PROTOCOL_DA_PHIEN.md` không.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: 06a50c5feea77c2654f31edd26efeed7eeee62f5`, và một dòng `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

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
P1 = khẳng định sai về sự thật đo được TẠI `06a50c5feea77c2654f31edd26efeed7eeee62f5`. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`.

Chạy thêm hai cổng tại `cay-kho/` và ghi rc + dòng kết luận:
`python3 .claude/dev/packet_loop.py doctrine-scan --root .` và `python3 scripts/tl.py doc-claims-check --json` (đòi `"ok": true`).

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/`, KHÔNG push, KHÔNG gọi mạng (sandbox không có mạng).
Mọi khẳng định phải đo TẠI `06a50c5feea77c2654f31edd26efeed7eeee62f5` — ma trận/tệp ở commit SAU có thể khác, đừng lấy master hiện tại làm chuẩn. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `06a50c5feea77c2654f31edd26efeed7eeee62f5`; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Diff: `diff.patch`, `numstat.txt`.
