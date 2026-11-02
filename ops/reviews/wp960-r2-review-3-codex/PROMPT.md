# Cross-review lượt 3 của revision 2 — packet `NO-CAU-LICH-SU-BIEN-NHAN` (Issue ducthangho/tra-luat#960) — reviewer: codex

## Đối tượng
- `reviewed_sha`: `934a5b063670acfbed410487d8244cd17d586d6e` (nhánh `agent/wp960-g1-claude`, PR #995, CHƯA merge).
  Lịch sử: `f7659a2` (lượt 1) → `0a37008` (merge master, không đụng hai tệp) → `ae0d06c` (lượt 2) → `934a5b0` (vá lượt 2).
- Diff hai tệp packet so base lease `44884446f71c89e25f9a72ac58e4f597db63c1ba`: `diff.patch`. Diff RIÊNG phần vá lượt 2:
  `diff-tu-luot-2.patch` (`ae0d06c..934a5b0`).
- Đặc tả ĐÓNG BĂNG: `cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`, sha256 phải là
  `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca` (tự kiểm). Lease r2: `lease-r2.yaml`.
- Review class `sensitive`. Executor: Claude (khác họ với bạn). Lượt này là 3/8.
- Verdict trước: `verdict-cu/r2-luot-2-VERDICT.md` (5 P1), `verdict-cu/r2-luot-1-VERDICT.md`, hai lượt r1.
  Sau lượt 2, chủ kho chọn ĐỔI KIẾN TRÚC tra git (Issue #960) thay vì vá từng nghĩa của rc=1.

## Lời khai của executor về bản vá (tự kiểm, ĐỪNG tin)
1. Kiến trúc: `_git_do` — kết quả git chỉ được TIN khi rc thuộc tập sạch của lệnh ấy VÀ stderr RỖNG (env `LC_ALL=C`,
   `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1`); còn lại `KhongDoDuoc`. Cơ sở (executor đo 27-10): git báo tiền tố mơ hồ,
   object rỗng/hỏng, loose ref hỏng trên STDERR trong khi stdout nói `missing` và rc 0/1. "Không có" chỉ đọc từ stdout.
2. `_commit_cua`: `rev-parse --disambiguate` (ứng viên) → `cat-file --batch-check` từng ứng viên 40 hex (loại); chỉ `commit`
   được tính; >1 commit ⇒ `_MoHo` (chua khoá ấy); dòng sai dạng / ứng viên `missing` ⇒ `KhongDoDuoc`. Tag KHÔNG được peel.
3. `_nhanh_mac_dinh`: `for-each-ref` ba ref + `symbolic-ref -q` từng ref (for-each-ref bỏ IM LẶNG symref gãy — đo 27-10).
4. `_kho_lanh` (một lần, trước phép tra đầu tiên): `--is-shallow-repository` ≠ `false` hoặc `extensions.partialclone` có ⇒
   `KhongDoDuoc` cả lượt.
5. `merge-base --is-ancestor` qua `_git_do(sach=(0,1))`; lỗi ⇒ chua khoá ấy. `_sinh_no` bắt `Exception` khi phân tích như `kiem`.
6. Ca: c91 14 nguồn hỏng × có/không nợ qua CLI (stderr phải nêu đúng nguồn); c92 thêm timestamp/lồng sâu; c93 commit+blob chung
   tiền tố `e4a3f5d`; c94 đồ giả `_git_do` trả dòng sai giao thức. Đột biến m114–m124; m84/m92/m103–m105/m109 neo lại.
7. `python3 ops/bien_nhan_v2_test.py` ⇒ `91/91 ca · 121/121 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM`. Gate `--root .` rc=0, nợ 1/60/0.

## Nhiệm vụ: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `934a5b063670acfbed410487d8244cd17d586d6e`
Danh sách dưới KHÔNG đủ — mỗi lỗi thật bạn tìm ra ngoài danh sách được tính là finding.

(a) **Đóng finding lượt 2** (và lượt 1): chạy lại CHÍNH phản chứng của bạn trên head mới; đóng thật / còn mở / đóng một phần.
(b) **Tiền đề kiến trúc.** "Git báo mọi tình trạng hỏng trên stderr" — tìm phản ví dụ: tình trạng hỏng mà stderr RỖNG và stdout
    vẫn đúng dạng (ref/object/pack/alternates/commit-graph/replace refs/grafts/`GIT_DIR` lạ…). Ngược lại: stderr có nội dung
    VÔ HẠI (cảnh báo cấu hình, `safe.directory`, gc tự động, hook…) làm kho LÀNH thành rc=2 — bắt nhầm cũng là lỗi.
(c) **Hồi quy.** Trên corpus thật: OID trước resolve nay khác? tag giờ không peel có đổi kết quả? thời gian chạy?
    Mô phỏng CI `pull_request` (merge commit, `fetch-depth: 0`, không `origin/HEAD`) — `_kho_lanh` có bắt nhầm không?
(d) **Không phá gì.** Suite N/N hai số BẰNG NHAU; ruff F delta 0 so base; doctrine-scan; `git diff --check 4488444 HEAD`.
(e) **Đột biến của bạn.** Trên BẢN SAO: gỡ ≥ 5 chốt của phần vá lượt 2 (khác m114–m124) và ghi ca nào ĐỎ.
(f) **Hình dạng kế thừa.** Gắn nhãn MỖI finding `loi-do | bo-chon-ung-vien | nguon-goc-cau | khac` — bắt buộc.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (chứa PROMPT.md, KHÔNG trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm
sau MỖI hướng thử. Cuối cùng dòng đầu `verdict: approve` hoặc `verdict: changes_requested`, dòng 2
`reviewed_sha: 934a5b063670acfbed410487d8244cd17d586d6e`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc như lượt 2 (`verdict-cu/r2-luot-2-VERDICT.md`): `## BẢNG ĐO` · `## BẢNG ĐÓNG FINDING LƯỢT 2` (mỗi finding một dòng:
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
sạch trên bản sao tại `934a5b0`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor. KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push,
KHÔNG gọi mạng. Chỉ CHẠY ca test có sẵn và ĐỘT BIẾN mã/fixture trên bản sao.
Mọi khẳng định phải đo TẠI `934a5b063670acfbed410487d8244cd17d586d6e`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `934a5b0…`; nhánh của kho ở `refs/remotes/origin/*`, `origin/master` =
`2618eb4`; `refs/remotes/origin/HEAD` là symref trỏ nhánh ứng viên — mô phỏng CI thì xoá nó trên bản sao; `core.abbrev=7`).
Mirror trần: `mirror.git`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO
ĐƯỢC chứ đừng ghi thành finding.
