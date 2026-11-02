# Cross-review lượt 7 của revision 2 — packet `NO-CAU-LICH-SU-BIEN-NHAN` (Issue ducthangho/tra-luat#960) — reviewer: codex

## Đối tượng
- `reviewed_sha`: `057abc816169688e894f64bbe637ea63d6bd9791` (nhánh `agent/wp960-g1-claude`, PR #1005 draft (CI xanh trên `78c138f`), CHƯA merge).
  Lịch sử: `6dca85f` (lượt 5) đã được chủ kho MERGE vào master qua PR #995 (`79dbaf4`) trong lúc executor vá lượt 5;
  `78c138f` (lượt 6) = commit trên `79dbaf4` vá test lượt 5; `057abc8` = áp HINT.patch lượt 6 (CHỈ `ops/bien_nhan_v2_test.py`).
- Diff hai tệp packet so base lease `44884446f71c89e25f9a72ac58e4f597db63c1ba`: `diff.patch` (toàn bộ r2). Diff RIÊNG phần vá
  lượt 6: `diff-tu-luot-6.patch` (`78c138f..057abc8`).
- Đặc tả ĐÓNG BĂNG: `cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`, sha256 phải là
  `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca` (tự kiểm). Lease hiện hành: `lease-r2-g2.yaml`.
- Review class `sensitive`. Executor: Claude (khác họ với bạn). Lượt này là 7 — lời gọi codex thứ 8 = TRẦN CUỐI; sẽ không có lượt sau.
- Verdict trước: `verdict-cu/r2-luot-6-VERDICT.md` (2 P1, cả hai là ca test thiếu răng), các lượt trước trong `verdict-cu/`.
- Đây có thể là lượt kết luận: verdict `approve` ở lượt này là điều kiện M-1 cho toàn bộ r2 (code cổng đã vào master ở
  `6dca85f`, giống hệt cổng tại `057abc8`). Đánh giá CẢ r2 trên head này, không chỉ phần vá lượt 6.

## PHẠM VI ĐÃ CHỐT BỞI CHỦ KHO (Issue #960) — đọc trước khi săn
- **Tiền đề, KHÔNG vá (đừng lập lại finding):** (B1) object sai băm / commit-graph sai parent mà git IM LẶNG — cần `git fsck`.
  (B2, mới từ lượt 4) cấu hình git IN CẢNH BÁO ở mọi lệnh (vd. khoá deprecated) ⇒ cổng trả KHÔNG ĐO ĐƯỢC (rc=2), đó là ĐÚNG
  thiết kế: cổng chạy trên clone CI sạch; nó KHÔNG được biến cảnh báo thành sạch/vi phạm.
- Nếu tìm ra một trạng thái mà kết quả đo SAI (rc=0/rc=1 khi lẽ ra rc=2, hoặc ngược lại trên kho lành CI-chuẩn) thì đó là finding;
  một môi trường lệch chuẩn bị báo rc=2 thì KHÔNG phải finding, trừ khi đó là cấu hình chuẩn của CI/clone thường.

## Lời khai của executor về bản vá lượt 6 (tự kiểm, ĐỪNG tin)
1. Chỉ `ops/bien_nhan_v2_test.py` đổi; `ops/bien_nhan_v2.py` tại `057abc8` giống hệt `6dca85f` (byte). Áp ĐÚNG HINT.patch của bạn ở lượt 6.
2. c94 thêm batch-check sai OID / sai loại; c87 thêm `Ban 12ab34c chua vao master.`. Đột biến m137/m138/m139.
3. `python3 ops/bien_nhan_v2_test.py` ⇒ `93/93 ca · 135/135 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM`. Gate `--root .` rc=0, nợ 1/60/0.

## Nhiệm vụ: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `057abc816169688e894f64bbe637ea63d6bd9791`
Danh sách dưới KHÔNG đủ — mỗi lỗi thật bạn tìm ra ngoài danh sách được tính là finding.

(a) **Đóng finding lượt 6**: chạy lại CHÍNH phản chứng (v1/v2/v3 và witness); đột biến m137–m139 giết đúng ca đích vì đúng lý do?
(b) **Toàn bộ r2 so đặc tả.** M1–M6, B1–B8 trên head này; mọi finding của các lượt 1–4 còn đóng (chạy lại phản chứng then chốt).
(c) **Không phá gì.** Suite N/N hai số BẰNG NHAU; ruff F delta 0 so base; doctrine-scan; `git diff --check 4488444 HEAD`;
    corpus thật nợ 1/60/0; mô phỏng CI `pull_request` (merge commit, `fetch-depth: 0`, không `origin/HEAD`) ⇒ rc=0.
(d) **Đột biến của bạn.** Trên BẢN SAO: gỡ ≥ 5 chốt bất kỳ của r2 (khác các m đã có) và ghi ca nào ĐỎ.
(e) **Hình dạng kế thừa.** Gắn nhãn MỖI finding `loi-do | bo-chon-ung-vien | nguon-goc-cau | khac` — bắt buộc.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (chứa PROMPT.md, KHÔNG trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm
sau MỖI hướng thử. Cuối cùng dòng đầu `verdict: approve` hoặc `verdict: changes_requested`, dòng 2
`reviewed_sha: 057abc816169688e894f64bbe637ea63d6bd9791`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc như lượt 6 (`verdict-cu/r2-luot-6-VERDICT.md`): `## BẢNG ĐO` · `## BẢNG ĐÓNG FINDING LƯỢT 6` (mỗi finding một dòng:
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
sạch trên bản sao tại `057abc8`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor. KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push,
KHÔNG gọi mạng. Chỉ CHẠY ca test có sẵn và ĐỘT BIẾN mã/fixture trên bản sao.
Mọi khẳng định phải đo TẠI `057abc816169688e894f64bbe637ea63d6bd9791`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `057abc8…`; nhánh của kho ở `refs/remotes/origin/*`, `origin/master` =
`79dbaf4`; `refs/remotes/origin/HEAD` là symref trỏ nhánh ứng viên — mô phỏng CI thì xoá nó trên bản sao; `core.abbrev=7`).
Mirror trần: `mirror.git`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO
ĐƯỢC chứ đừng ghi thành finding.
