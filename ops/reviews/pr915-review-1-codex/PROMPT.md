# Cross-review lượt 1 PR ducthangho/tra-luat#915 — reviewer: codex — chấm HEAD ĐÃ MERGE

## Đối tượng
- `reviewed_sha`: `2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f` (head đã merge của PR #915, merge `9371628`), base `50a59a9`.
- PR #915 có ba commit: (1) `3bc4244` sửa điểm (c) của `CLAUDE.md` (+3/-2) bằng NGUYÊN `HINT.patch` của lượt cross-review #896: `t162` CHỈ khoá output `os` của `chuan-bi`; `exclude:`/`if:` mức job phải đọc trong `ci.yml`; phần mảnh/gom của `gate-cong-cu*` có chốt `loi_g5_workflow` trong `.claude/dev/ci_dang_ky_test.py`; (2) `7cfe062` CHỈ hiện vật của ba lượt review (`ops/reviews/pr870-review-2-codex/`, `pr889-review-2-codex/`, `pr896-review-1-codex/` + ba bản phẳng `*-verdict.md`); (3) `2789cbb` ba biên nhận v2 `*-verdict.receipt.yaml` + 17 hàng `ops/reviews/README.md`.
- Chưa có cross-review CLI nào cho #915; Codex connector chấm `2789cbb` sạch.

## Nhiệm vụ chính: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f`
Danh sách dưới KHÔNG đủ — mỗi khẳng định bạn tìm ra mà nó bỏ sót được tính là finding:
1. Câu mới trong `CLAUDE.md` (điểm (c)): `t162` có đúng chỉ đọc `jobs.chuan-bi.outputs.os` không; `loi_g5_workflow`/`_loi_g5_manh_gop` có thật sự kiểm `exclude` và `needs`/`if` của job mảnh/gom không (đọc mã tại `2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f`, đột biến bản sao `ci.yml` ở thư mục tạm, KHÔNG sửa `cay-kho/`); câu có khai rộng hơn phép đo không (vd: "phần mảnh/gom" có đúng là MỌI job `gate-cong-cu*` không).
2. Ba biên nhận: mọi trường `verdict_sha256`/`verdict_bytes`/`reviewed_sha`/`reviewed_tree`/`base_sha`/`so_p*`/dòng `Kết quả`/`run_json_ghi_chu` (thời lượng, mã thoát, prompt_sha256 = sha256 PROMPT.md) có khớp đúng hiện vật trong thư mục không; bản phẳng có đúng nguyên byte bản trong thư mục không; `SHA256SUMS` mỗi thư mục `sha256sum -c` sạch không; `evidence_url` trỏ commit nào và commit ấy có đúng CHỈ mang hiện vật không.
3. Lời khai trong biên nhận/README: `cross_reviewed` mà KHÔNG `cross_approved` có đúng lý do không (run.json có khoá model nào không); caveat `SNAPSHOT-CAY-KHONG-VAO-KHO` khai hai ảnh cùng sha256 `5b88623b…` — có đối chiếu được trong hiện vật không, hay chỉ là lời khai (nói rõ ĐO được/KHÔNG ĐO ĐƯỢC); caveat `P2-DA-VA-CHUA-REVIEW-LAI` có đúng commit `3bc4244` không.
4. Chạy `python3 ops/bien_nhan_v2.py --root .`, các ca `t26`/`t27`/`t138` của `ops/lease_publish_test.py` (gọi riêng từng hàm), và `python3 scripts/pkg_secret_scan.py` trên ba thư mục; ghi rc + dòng kết luận.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: 2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f`, và một dòng `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

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
P1 = khẳng định sai về sự thật đo được TẠI `2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f`. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`.

Chạy thêm hai cổng tại `cay-kho/` và ghi rc + dòng kết luận:
`python3 .claude/dev/packet_loop.py doctrine-scan --root .` và `python3 scripts/tl.py doc-claims-check --json` (đòi `"ok": true`).

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/`, KHÔNG push, KHÔNG gọi mạng (sandbox không có mạng).
Mọi khẳng định phải đo TẠI `2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f` — ma trận/tệp ở commit SAU có thể khác, đừng lấy master hiện tại làm chuẩn. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f`; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Diff: `diff.patch`, `numstat.txt`.
