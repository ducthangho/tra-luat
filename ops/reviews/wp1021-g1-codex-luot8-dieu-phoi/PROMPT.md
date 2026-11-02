# Cross-review LƯỢT 8 PR ducthangho/tra-luat#1040 — reviewer: codex — packet #1021 `BIEN-NHAN-V2-GLOB-HOA-THUONG` r2

## Đối tượng
- `reviewed_sha`: `356a27e1378b2162bbc0be2ec06ff08fdacbdead` (nhánh `agent/wp1021-g1-claude`, PR #1040, CHƯA merge).
  Base so sánh: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93` (merge-base với master; merge của PR #1041 đã được merge vào nhánh ở `3883b60`).
- Đặc tả đóng băng: `SPEC.md` (sha256 `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`, cũng ở
  `ops/specs/BIEN-NHAN-V2-GLOB-HOA-THUONG-r2.md` trong cây). Write set: đúng `ops/bien_nhan_v2.py` và `ops/bien_nhan_v2_test.py`.
- Diff tổng so base: `diff.patch`. Diff riêng từ head lượt 7 (`c8a493c`) tới head này: `diff-tu-luot7.patch`.
- Verdict cũ (byte-exact): `verdict-cu/luot7-VERDICT.md` (sha256 `181946a7…a00d1a10`, `request_changes` 0/0/0/1, P3
  `chu-thich-tro-sai-ca-ngoai-le-lap-trinh`: docstring `_hoi_trang_thai` trỏ `c99` thay `c100`), `verdict-cu/luot6-VERDICT.md`.
  Hồ sơ executor: `handoff.md` (có Phụ lục A chứa nguyên văn bảy verdict trước).
- Lời khai bên vá (tự kiểm, ĐỪNG tin): `6964930` vá P3 lượt 7 + hai tham chiếu cũ executor tự rà; `356a27e` tự rà mọi docstring
  #1021 trước lượt 8. Cả hai commit khai **chỉ đổi docstring/chú thích**, không đổi hành vi.
- Lời khai CI (bạn KHÔNG có mạng nên ghi KHÔNG ĐO ĐƯỢC; điều phối sẽ đo riêng): Ubuntu PR run 41113943723 success, Windows
  dispatch 41113949578 success trên `356a27e`.

## Nhiệm vụ 0 — finding lượt 7 đã ĐÓNG thật chưa (ĐÓNG / CHƯA / MỘT PHẦN, kèm lệnh + output)
Và: `diff-tu-luot7.patch` có thật chỉ đổi chuỗi docstring/chú thích không — đo bằng so AST (bỏ docstring) giữa `c8a493c` và
`356a27e` cho cả hai tệp, đừng đọc bằng mắt. Mỗi tham chiếu ca/đột biến (`cNN`, `mNNN`, "chốt N", "lượt N") trong các docstring
đã đổi có trỏ đúng ca/đột biến canh thuộc tính được nói tới không — đo bằng đột biến (vd đột biến được nêu phải chết đúng ở
ca được nêu), không đo bằng grep.

## Nhiệm vụ — ĐO LẠI tại `356a27e1378b2162bbc0be2ec06ff08fdacbdead`
Danh sách dưới KHÔNG đủ — mỗi khẳng định sai bạn tìm ra ngoài danh sách được tính là finding.
(a) Toàn suite `python3 ops/bien_nhan_v2_test.py` (đòi N/N hai số BẰNG NHAU, `TỔNG: ĐẠT`).
(b) Cổng `python3 ops/bien_nhan_v2.py --root .` và `--sinh-no` (rc, dòng tổng). Tiêu chí C1–C9 của SPEC, từng dòng.
(c) Ruff `python3 -m ruff check --select F` delta so base = 0; `python3 .claude/dev/packet_loop.py doctrine-scan --root .`;
    `git diff --check b29da0b HEAD`; `rg 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` = 0 dòng.
(d) Đột biến chỉ định (chạy riêng, qua cơ chế `_dot_bien_tep` của suite, trên bản sao): m142, m147, m153, m156, m157 và một đột
    biến bạn tự chọn ở mỗi tệp — mỗi cái phải chết đúng ca đích (`giet_that`), không phải tín dụng giả.
(e) Mọi ca/đột biến mà merge master `3883b60` chạm vào (`c88`, `c101`, `m156`, `m157`) vẫn đúng như lượt 5–7 đã kết luận.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (chứa PROMPT.md, KHÔNG trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối
thêm sau MỖI hướng thử. Cuối cùng dòng đầu `verdict: approve` hoặc `verdict: changes_requested`, dòng 2
`reviewed_sha: 356a27e1378b2162bbc0be2ec06ff08fdacbdead`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`
Ngưỡng: `approve` CHỈ khi 0 P0, 0 P1, 0 P2, 0 P3 còn mở.

Cấu trúc: `## ĐỐI CHIẾU LƯỢT TRƯỚC` · `## BẢNG TIÊU CHÍ` (C1–C9 + suite + đột biến) · `## BẢNG SĂN` (>= 6 hướng ĐỘC LẬP, mỗi
hướng có LỆNH + OUTPUT THẬT, kết luận LỖI / KHÔNG PHẢI LỖI / KHÔNG ĐO ĐƯỢC) · từng finding:
```
### <slug-kebab>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ NGHIỆM: <lệnh + kết quả, hoặc KHÔNG ĐO ĐƯỢC + lý do>
HÌNH DẠNG: bo-chon-ung-vien | loi-do | khac
ĐỘ TIN: cao/vừa/thấp
```
P1 = hành vi sai đo được / chốt không có răng. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt, tham chiếu sai.
Không có finding thì vẫn phải có BẢNG TIÊU CHÍ đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface.
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`, và PHẢI kiểm
`patch --dry-run --fuzz=0` sạch trên bản sao tại `356a27e`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục
tạm, hoặc qua `_dot_bien_tep` vốn chạy trên bản sao tạm), KHÔNG push, KHÔNG gọi mạng. Chỉ CHẠY lệnh/cổng/ca có sẵn và ĐỘT BIẾN
mã trên bản sao; hướng thử nào cần tự soạn nội dung khai thác thì mô tả bằng lời thay vì soạn.
Mọi khẳng định phải đo TẠI `356a27e1378b2162bbc0be2ec06ff08fdacbdead`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `356a27e…`; nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`).
Mirror trần: `mirror.git`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác sandbox (`/tmp/.git`), ghi KHÔNG ĐO ĐƯỢC.
