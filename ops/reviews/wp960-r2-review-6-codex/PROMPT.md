# Cross-review lượt 6 của revision 2 — packet `NO-CAU-LICH-SU-BIEN-NHAN` (Issue ducthangho/tra-luat#960) — reviewer: codex

## Đối tượng
- `reviewed_sha`: `78c138f863696def68f88080b2b32057fe98f207` (nhánh `agent/wp960-g1-claude`, PR #1005 draft, CHƯA merge).
  Lịch sử: `6dca85f` (lượt 5) đã được chủ kho MERGE vào master qua PR #995 (`79dbaf4`) trong lúc executor vá lượt 5;
  `78c138f` = một commit trên `79dbaf4`, CHỈ sửa `ops/bien_nhan_v2_test.py` (vá hai finding lượt 5).
- Diff hai tệp packet so base lease `44884446f71c89e25f9a72ac58e4f597db63c1ba`: `diff.patch` (toàn bộ r2). Diff RIÊNG phần vá
  lượt 5: `diff-tu-luot-5.patch` (`6dca85f..78c138f`).
- Đặc tả ĐÓNG BĂNG: `cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`, sha256 phải là
  `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca` (tự kiểm). Lease hiện hành: `lease-r2-g2.yaml`.
- Review class `sensitive`. Executor: Claude (khác họ với bạn). Lượt này là 6/8 (lời gọi codex thứ 7 / trần 8).
- Verdict trước: `verdict-cu/r2-luot-5-VERDICT.md` (1 P1 + 1 P2, cả hai là ca test thiếu răng), các lượt trước trong `verdict-cu/`.
- Đây có thể là lượt kết luận: verdict `approve` ở lượt này là điều kiện M-1 cho toàn bộ r2 (code cổng đã vào master ở
  `6dca85f`, giống hệt cổng tại `78c138f`). Đánh giá CẢ r2 trên head này, không chỉ phần vá lượt 5.

## PHẠM VI ĐÃ CHỐT BỞI CHỦ KHO (Issue #960) — đọc trước khi săn
- **Tiền đề, KHÔNG vá (đừng lập lại finding):** (B1) object sai băm / commit-graph sai parent mà git IM LẶNG — cần `git fsck`.
  (B2, mới từ lượt 4) cấu hình git IN CẢNH BÁO ở mọi lệnh (vd. khoá deprecated) ⇒ cổng trả KHÔNG ĐO ĐƯỢC (rc=2), đó là ĐÚNG
  thiết kế: cổng chạy trên clone CI sạch; nó KHÔNG được biến cảnh báo thành sạch/vi phạm.
- Nếu tìm ra một trạng thái mà kết quả đo SAI (rc=0/rc=1 khi lẽ ra rc=2, hoặc ngược lại trên kho lành CI-chuẩn) thì đó là finding;
  một môi trường lệch chuẩn bị báo rc=2 thì KHÔNG phải finding, trừ khi đó là cấu hình chuẩn của CI/clone thường.

## Lời khai của executor về bản vá lượt 5 (tự kiểm, ĐỪNG tin)
1. Chỉ `ops/bien_nhan_v2_test.py` đổi; `ops/bien_nhan_v2.py` tại `78c138f` giống hệt `6dca85f` (byte).
2. c95 `promisor_tat` thêm `off`/`no`; c95 `git_dir_khac` dời master kho ngoài sang X; c94 thêm đồ giả `config --type=bool`
   trả `maybe`. Đột biến m134 (bỏ `--type=bool`), m135 (bỏ chốt giá trị lạ), m136 (giữ `GIT_DIR`).
3. `python3 ops/bien_nhan_v2_test.py` ⇒ `93/93 ca · 132/132 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM`. Gate `--root .` rc=0, nợ 1/60/0.

## Nhiệm vụ: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `78c138f863696def68f88080b2b32057fe98f207`
Danh sách dưới KHÔNG đủ — mỗi lỗi thật bạn tìm ra ngoài danh sách được tính là finding.

(a) **Đóng finding lượt 5**: chạy lại CHÍNH phản chứng (u3/u4/u7 và witness); đột biến m134–m136 giết đúng ca đích vì đúng lý do?
(b) **Toàn bộ r2 so đặc tả.** M1–M6, B1–B8 trên head này; mọi finding của các lượt 1–4 còn đóng (chạy lại phản chứng then chốt).
(c) **Không phá gì.** Suite N/N hai số BẰNG NHAU; ruff F delta 0 so base; doctrine-scan; `git diff --check 4488444 HEAD`;
    corpus thật nợ 1/60/0; mô phỏng CI `pull_request` (merge commit, `fetch-depth: 0`, không `origin/HEAD`) ⇒ rc=0.
(d) **Đột biến của bạn.** Trên BẢN SAO: gỡ ≥ 5 chốt bất kỳ của r2 (khác các m đã có) và ghi ca nào ĐỎ.
(e) **Hình dạng kế thừa.** Gắn nhãn MỖI finding `loi-do | bo-chon-ung-vien | nguon-goc-cau | khac` — bắt buộc.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (chứa PROMPT.md, KHÔNG trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm
sau MỖI hướng thử. Cuối cùng dòng đầu `verdict: approve` hoặc `verdict: changes_requested`, dòng 2
`reviewed_sha: 78c138f863696def68f88080b2b32057fe98f207`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc như lượt 5 (`verdict-cu/r2-luot-5-VERDICT.md`): `## BẢNG ĐO` · `## BẢNG ĐÓNG FINDING LƯỢT 5` (mỗi finding một dòng:
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
sạch trên bản sao tại `78c138f`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor. KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push,
KHÔNG gọi mạng. Chỉ CHẠY ca test có sẵn và ĐỘT BIẾN mã/fixture trên bản sao.
Mọi khẳng định phải đo TẠI `78c138f863696def68f88080b2b32057fe98f207`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `78c138f…`; nhánh của kho ở `refs/remotes/origin/*`, `origin/master` =
`79dbaf4`; `refs/remotes/origin/HEAD` là symref trỏ nhánh ứng viên — mô phỏng CI thì xoá nó trên bản sao; `core.abbrev=7`).
Mirror trần: `mirror.git`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO
ĐƯỢC chứ đừng ghi thành finding.
