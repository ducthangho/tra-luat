# Cross-review lượt 2 của revision 2 — packet `NO-CAU-LICH-SU-BIEN-NHAN` (Issue ducthangho/tra-luat#960) — reviewer: codex

## Đối tượng
- `reviewed_sha`: `ae0d06c23fb777545fd7547a07d9f368e4122f49` (nhánh `agent/wp960-g1-claude`, PR #995 draft, CHƯA merge).
  Lịch sử: `f7659a2` (bản lượt 1 đã review) → `0a37008` (merge `origin/master` `2618eb4`, KHÔNG đụng hai tệp packet) →
  `ae0d06c` (vá finding lượt 1).
- Diff hai tệp packet so base lease `44884446f71c89e25f9a72ac58e4f597db63c1ba`: `diff.patch`. Diff RIÊNG phần vá lượt 1
  (`f7659a2..ae0d06c`, chỉ hai tệp): `diff-tu-luot-1.patch`. `numstat.txt` so base có thêm tệp `ops/land/pr945-*` — đó là của
  master qua merge, KHÔNG thuộc packet.
- Đặc tả ĐÓNG BĂNG: `cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`, sha256 phải là
  `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca` (tự kiểm). Lease r2: `lease-r2.yaml`.
- Review class `sensitive`. Executor: Claude (khác họ với bạn).
- Verdict lượt 1 của r2: `verdict-cu/r2-luot-1-VERDICT.md` (changes_requested, 6 P1/1 P2/1 P3). Hai lượt r1: `verdict-cu/wp960-*`.
  Lượt 1 tái xuất hai hình dạng kế thừa; chủ kho quyết định vá tiếp trong r2 (Issue #960, 16:16Z). Lượt này là 2/8.

## Lời khai của executor về bản vá (tự kiểm, ĐỪNG tin)
1. `_commit_cua`: ba trạng thái phân tại chỗ. Git không trả lời (rc ngoài 0/1, kể cả 127 khi git vắng) ⇒ `KhongDoDuoc` (cả lượt rc=2).
   Token hex tra bằng `git rev-parse --disambiguate=<tok>` rồi peel từng ứng viên `^{commit}` và ĐẾM commit; >1 ⇒ `_MoHo` ⇒
   chua cho khoá ấy (rc=2). Lý do: `rev-parse --verify --quiet` trả rc=1 cho cả "không có" lẫn tiền tố mơ hồ (executor đo 27-10).
2. `_nhanh_mac_dinh`: `show-ref --verify --quiet` rc=1 ⇒ ref vắng ⇒ thử ref kế; rc=0 mà không peel ra commit ⇒ `KhongDoDuoc`.
3. run.json: chỉ VẮNG thật (`lstat` ném FileNotFoundError/NotADirectoryError) mới "không áp"; mọi thứ khác ⇒ thử đọc ⇒ chua.
4. `--sinh-no` đi trong `try` của `main`; `_sinh_no` đổi OSError/UnicodeDecodeError/YAMLError thành `KhongDoDuoc`.
5. Ca mới `c91` (7 nguồn hỏng × có/không nợ qua `bnv2.main`, đòi rc=2, không ngoại lệ, không `NỢ CHẾT`, stderr nêu đúng nguồn),
   `c92` (hai cờ sinh nợ × 3 kiểu hỏng + đối chứng lành). `c87`/`c88` thêm đối chứng ranh giới. `c72` docstring (P3).
   Fixture tiền tố mơ hồ: hai commit `commit-tree` thông điệp `mh122110`/`mh211952` rẽ từ B0 của `_kho_cau` ⇒ chung tiền tố `5298700`.
6. Đột biến mới m103–m113 (mỗi đường vào một cái); m76/m84 neo lại theo thụt lề mới.
7. `python3 ops/bien_nhan_v2_test.py` ⇒ `89/89 ca · 110/110 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM`. Gate `--root .` rc=0, nợ 1/60/0.

## Nhiệm vụ: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `ae0d06c23fb777545fd7547a07d9f368e4122f49`
Danh sách dưới KHÔNG đủ — mỗi lỗi thật bạn tìm ra ngoài danh sách được tính là finding.

(a) **Đóng finding lượt 1.** Với TỪNG finding của `verdict-cu/r2-luot-1-VERDICT.md`, chạy lại chính phản chứng của bạn trên head mới:
    đóng thật / còn mở / đóng một phần. Ca và đột biến mới có đo đúng điều finding nói không (đột biến giết vì đúng lý do)?
(b) **Đường thứ ba.** Executor khai đã liệt kê đủ đường vào. Tìm đường lỗi đo còn lại (git, ref, I/O, mã hoá, YAML, JSON, symlink,
    quyền, tiền tố mơ hồ giữa commit/tag/blob, `--disambiguate` trên kho nông/partial clone) thành rc=0/rc=1/traceback.
(c) **Hồi quy do bản vá.** `--disambiguate` + peel có đổi kết quả trên corpus thật không (OID trước đây resolve nay thành mơ hồ/None,
    hay ngược lại)? Chi phí thời gian trên kho thật? `KhongDoDuoc` từ `_commit_cua` thoát biên per-receipt và dừng CẢ lượt — có
    che kết quả các tệp khác theo cách sai đặc tả M2 không?
(d) **Không phá gì.** Suite N/N hai số BẰNG NHAU; ruff F delta 0 so base (nếu có ruff); doctrine-scan; `git diff --check 4488444 HEAD`;
    nợ 61 mục vẫn khớp vi phạm thật; mô phỏng CI `pull_request` (merge commit, không `origin/HEAD`).
(e) **Đột biến của bạn.** Trên BẢN SAO: gỡ ≥ 5 chốt của phần vá (khác m103–m113) và ghi ca nào ĐỎ; chốt không ca nào đỏ = finding.
(f) **Hình dạng kế thừa.** Spec r2 `hinh_dang_ke_thua`: gắn nhãn MỖI finding `loi-do | bo-chon-ung-vien | nguon-goc-cau | khac` — bắt buộc.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (chứa PROMPT.md, KHÔNG trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm
sau MỖI hướng thử. Cuối cùng dòng đầu `verdict: approve` hoặc `verdict: changes_requested`, dòng 2
`reviewed_sha: ae0d06c23fb777545fd7547a07d9f368e4122f49`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc như lượt 1 (`verdict-cu/r2-luot-1-VERDICT.md`): `## BẢNG ĐO` · `## BẢNG ĐÓNG FINDING LƯỢT 1` (mỗi finding một dòng:
slug | trạng thái | lệnh | output) · `## BẢNG SĂN` (>= 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT) · từng finding:
```
### <slug-kebab>  [P0|P1|P2|P3]  <tiêu đề>
HÌNH DẠNG: <loi-do | bo-chon-ung-vien | nguon-goc-cau | khac>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ NGHIỆM: <lệnh + kết quả, hoặc KHÔNG ĐO ĐƯỢC + lý do>
ĐỘ TIN: cao/vừa/thấp
```
P1 = hành vi sai đo được (kết quả sai, trạng thái sai, chốt không răng, lệch đặc tả). P2 = khai rộng hơn phép đo / thiếu điều kiện /
ca test không đo đúng điều nó khai. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface.
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`, và PHẢI kiểm `patch --dry-run --fuzz=0`
sạch trên bản sao tại `ae0d06c`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor. KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push,
KHÔNG gọi mạng. Chỉ CHẠY ca test có sẵn và ĐỘT BIẾN mã/fixture trên bản sao.
Mọi khẳng định phải đo TẠI `ae0d06c23fb777545fd7547a07d9f368e4122f49`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `ae0d06c…`; nhánh của kho ở `refs/remotes/origin/*`, `origin/master` =
`2618eb4`; `refs/remotes/origin/HEAD` là symref trỏ nhánh ứng viên — mô phỏng CI thì xoá nó trên bản sao; `core.abbrev=7`).
Mirror trần: `mirror.git`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO
ĐƯỢC chứ đừng ghi thành finding.
