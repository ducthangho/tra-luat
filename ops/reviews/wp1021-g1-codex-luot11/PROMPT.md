# Cross-review LỜI GỌI 11 — packet #1021 `BIEN-NHAN-V2-GLOB-HOA-THUONG` r2 — chấm ĐÚNG head đã merge của PR #1040

## Vì sao có lượt này
PR #1040 đã merge vào master (merge commit `c8ff9ed`). Head nhánh lúc merge là
`a16932aa09ce860a614f0bab4b2015699e7221bc`. Hai lượt approve trước (lời gọi 9 và 10) chấm `356a27e`. Sau đó executor merge master
`3dfb973` vào nhánh để qua cổng `thu-hoi`, tạo ra `a16932a`. Theo PROTOCOL §5.1 và AGENTS.md §6, head nhánh đã đổi sau review, nên
các approve neo `356a27e` không phủ `a16932a` (finding P1 của connector trên PR #1070). Lượt này đóng điều kiện review cho đúng `a16932a`.

## Đối tượng
- `reviewed_sha`: `a16932aa09ce860a614f0bab4b2015699e7221bc` (đã merge; đây là kiểm toán sau merge, KHÔNG phải xin quyền merge).
  Cha 1 = `356a27e` (head đã được approve), cha 2 = `3dfb973` (master lúc đó).
- Diff của packet so cha 2 (master): `diff.patch` (2 tệp `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py`, +340/−7).
- Đặc tả đóng băng: `SPEC.md` (sha256 `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`).
- Verdict của hai lượt approve trên `356a27e`: `verdict-cu/luot9-VERDICT.md`, `verdict-cu/luot10-VERDICT.md` (thông tin nền, ĐỪNG tin;
  đo lại những gì cần).

## Nhiệm vụ — ĐO TẠI `a16932aa09ce860a614f0bab4b2015699e7221bc`
Danh sách dưới KHÔNG đủ — mỗi khẳng định sai bạn tìm ra ngoài danh sách được tính là finding.
(a) Phép merge `a16932a` có đưa thay đổi nào vào hai tệp write set ngoài nội dung của `356a27e` không: so blob hai tệp ở `a16932a`
    với `356a27e`, và diff `3dfb973..a16932a` có đúng chỉ hai tệp ấy không. Có tệp nào khác trong cây `a16932a` khác cả hai cha
    (merge tạo nội dung mới) không.
(b) Mã của master `3dfb973` mang vào có làm đổi hành vi của hai tệp packet không: chạy toàn suite `python3 ops/bien_nhan_v2_test.py`
    tại `a16932a` (đòi N/N hai số BẰNG NHAU, `TỔNG: ĐẠT`), và cổng `python3 ops/bien_nhan_v2.py --root .` (`TỔNG: ĐẠT`, ghi tổng).
(c) Tiêu chí C1–C9 của SPEC đo được tại chỗ; C4/C5/C7 cần mạng/máy ngoài thì ghi KHÔNG ĐO ĐƯỢC.
(d) Đột biến chỉ định chạy riêng qua `_dot_bien_tep` trên bản sao: m142, m147, m153, m156, m157 — mỗi cái `giet_that` đúng ca đích.
(e) Ruff `--select F` delta so `3dfb973` = 0; `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `git diff --check 3dfb973 HEAD`.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (chứa PROMPT.md, KHÔNG trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối
thêm sau MỖI hướng thử. Cuối cùng dòng đầu `verdict: approve` hoặc `verdict: changes_requested`, dòng 2
`reviewed_sha: a16932aa09ce860a614f0bab4b2015699e7221bc`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`
Ngưỡng: `approve` CHỈ khi 0 P0, 0 P1, 0 P2, 0 P3 còn mở.

Cấu trúc: `## BẢNG TIÊU CHÍ` · `## BẢNG SĂN` (>= 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT, kết luận LỖI / KHÔNG PHẢI LỖI /
KHÔNG ĐO ĐƯỢC) · từng finding:
```
### <slug-kebab>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ NGHIỆM: <lệnh + kết quả, hoặc KHÔNG ĐO ĐƯỢC + lý do>
ĐỘ TIN: cao/vừa/thấp
```
Không có finding thì vẫn phải có BẢNG TIÊU CHÍ đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm,
hoặc qua `_dot_bien_tep`), KHÔNG push, KHÔNG gọi mạng. Mọi khẳng định phải đo TẠI `a16932aa09ce860a614f0bab4b2015699e7221bc`.
Thứ định danh tệp là SHA, không phải tên nhánh. Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `a16932a…`;
nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Mirror trần: `mirror.git`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác sandbox (`/tmp/.git`), ghi KHÔNG ĐO ĐƯỢC.
