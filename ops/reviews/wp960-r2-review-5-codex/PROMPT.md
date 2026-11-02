# Cross-review lượt 5 của revision 2 — packet `NO-CAU-LICH-SU-BIEN-NHAN` (Issue ducthangho/tra-luat#960) — reviewer: codex

## Đối tượng
- `reviewed_sha`: `6dca85f463c6ce551eb8c27ff2d94b7a102e2fdf` (nhánh `agent/wp960-g1-claude`, PR #995, CHƯA merge).
  Lịch sử: `f7659a2` (lượt 1) → `ae0d06c` (lượt 2) → `934a5b0` (lượt 3) → `3a52e6d` (lượt 4) → `6dca85f` (vá lượt 4).
- Diff hai tệp packet so base lease `44884446f71c89e25f9a72ac58e4f597db63c1ba`: `diff.patch`. Diff RIÊNG phần vá lượt 4:
  `diff-tu-luot-4.patch` (`3a52e6d..6dca85f`).
- Đặc tả ĐÓNG BĂNG: `cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`, sha256 phải là
  `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca` (tự kiểm). Lease hiện hành: `lease-r2-g2.yaml`.
- Review class `sensitive`. Executor: Claude (khác họ với bạn). Lượt này là 5/8 (lời gọi codex thứ 6).
- Verdict trước: `verdict-cu/r2-luot-4-VERDICT.md` (4 P1), các lượt trước trong `verdict-cu/`.

## PHẠM VI ĐÃ CHỐT BỞI CHỦ KHO (Issue #960) — đọc trước khi săn
- **Tiền đề, KHÔNG vá (đừng lập lại finding):** (B1) object sai băm / commit-graph sai parent mà git IM LẶNG — cần `git fsck`.
  (B2, mới từ lượt 4) cấu hình git IN CẢNH BÁO ở mọi lệnh (vd. khoá deprecated) ⇒ cổng trả KHÔNG ĐO ĐƯỢC (rc=2), đó là ĐÚNG
  thiết kế: cổng chạy trên clone CI sạch; nó KHÔNG được biến cảnh báo thành sạch/vi phạm.
- Nếu tìm ra một trạng thái mà kết quả đo SAI (rc=0/rc=1 khi lẽ ra rc=2, hoặc ngược lại trên kho lành CI-chuẩn) thì đó là finding;
  một môi trường lệch chuẩn bị báo rc=2 thì KHÔNG phải finding, trừ khi đó là cấu hình chuẩn của CI/clone thường.

## Lời khai của executor về bản vá lượt 4 (tự kiểm, ĐỪNG tin)
1. Bỏ trừ stderr nền (`_NEN_STDERR`) và lệnh dò riêng; `_git_do`: mọi dòng stderr khác rỗng ⇒ `KhongDoDuoc`; mọi lệnh (kể cả
   kiểm sức khoẻ) đi qua `_git_do`.
2. `_env_git`: bỏ biến `GIT_*` kế thừa NGOÀI danh sách cho phép `_GIT_GIU` = {`GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_EXEC_PATH`}.
3. `remote.<x>.promisor` đọc bằng `config --type=bool --get-regexp`; chỉ `true` là partial; dòng lạ ⇒ `KhongDoDuoc`.
4. Ca: c95 thêm `promisor_tat`, `alternates_env` (object dời hết ra kho phụ qua biến); c91 thêm `cau_hinh_canh_bao` (rc=2);
   c96 thêm lệnh `--is-shallow-repository` rc=3 không stderr. Đột biến m132/m133; m126/m129 neo lại; bỏ m128.
5. `python3 ops/bien_nhan_v2_test.py` ⇒ `93/93 ca · 129/129 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM`. Gate `--root .` rc=0, nợ 1/60/0.

## Nhiệm vụ: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `6dca85f463c6ce551eb8c27ff2d94b7a102e2fdf`
Danh sách dưới KHÔNG đủ — mỗi lỗi thật bạn tìm ra ngoài danh sách được tính là finding.

(a) **Đóng finding lượt 4**: chạy lại CHÍNH phản chứng của bạn; đóng thật / còn mở / đóng một phần.
(b) **Danh sách cho phép.** Hai biến được giữ có thể làm phép đo SAI không (alternates trỏ kho khác làm OID ngoài kho "tra được";
    `GIT_EXEC_PATH` trỏ lệnh giả)? Có biến `GIT_*` nào CẦN giữ cho clone CI/worktree chuẩn mà bị bỏ?
(c) **Không phá gì.** Suite N/N hai số BẰNG NHAU; ruff F delta 0 so base; doctrine-scan; `git diff --check 4488444 HEAD`;
    corpus thật nợ 1/60/0; mô phỏng CI `pull_request` (merge commit, `fetch-depth: 0`, không `origin/HEAD`) ⇒ rc=0.
(d) **Đột biến của bạn.** Trên BẢN SAO: gỡ ≥ 5 chốt của phần vá lượt 4 (khác m132/m133) và ghi ca nào ĐỎ.
(e) **Hình dạng kế thừa.** Gắn nhãn MỖI finding `loi-do | bo-chon-ung-vien | nguon-goc-cau | khac` — bắt buộc.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (chứa PROMPT.md, KHÔNG trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm
sau MỖI hướng thử. Cuối cùng dòng đầu `verdict: approve` hoặc `verdict: changes_requested`, dòng 2
`reviewed_sha: 6dca85f463c6ce551eb8c27ff2d94b7a102e2fdf`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc như lượt 4 (`verdict-cu/r2-luot-4-VERDICT.md`): `## BẢNG ĐO` · `## BẢNG ĐÓNG FINDING LƯỢT 4` (mỗi finding một dòng:
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
sạch trên bản sao tại `6dca85f`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor. KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push,
KHÔNG gọi mạng. Chỉ CHẠY ca test có sẵn và ĐỘT BIẾN mã/fixture trên bản sao.
Mọi khẳng định phải đo TẠI `6dca85f463c6ce551eb8c27ff2d94b7a102e2fdf`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `6dca85f…`; nhánh của kho ở `refs/remotes/origin/*`, `origin/master` =
`2618eb4`; `refs/remotes/origin/HEAD` là symref trỏ nhánh ứng viên — mô phỏng CI thì xoá nó trên bản sao; `core.abbrev=7`).
Mirror trần: `mirror.git`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO
ĐƯỢC chứ đừng ghi thành finding.
