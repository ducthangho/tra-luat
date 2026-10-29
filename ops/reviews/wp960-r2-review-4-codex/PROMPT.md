# Cross-review lượt 4 của revision 2 — packet `NO-CAU-LICH-SU-BIEN-NHAN` (Issue ducthangho/tra-luat#960) — reviewer: codex

## Đối tượng
- `reviewed_sha`: `3a52e6d194d08a755793cf449f393fb15b56757b` (nhánh `agent/wp960-g1-claude`, PR #995, CHƯA merge).
  Lịch sử: `f7659a2` (lượt 1) → `ae0d06c` (lượt 2) → `934a5b0` (lượt 3) → `43b96f0` (merge master, không đụng hai tệp) →
  `3a52e6d` (vá lượt 3).
- Diff hai tệp packet so base lease `44884446f71c89e25f9a72ac58e4f597db63c1ba`: `diff.patch`. Diff RIÊNG phần vá lượt 3:
  `diff-tu-luot-3.patch` (`934a5b0..3a52e6d`, chỉ hai tệp).
- Đặc tả ĐÓNG BĂNG: `cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`, sha256 phải là
  `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca` (tự kiểm). Lease hiện hành: `lease-r2-g2.yaml`
  (g2 = gia hạn 24h của g1, cùng write set/base/ngân sách).
- Review class `sensitive`. Executor: Claude (khác họ với bạn). Lượt này là 4/8 (lời gọi codex thứ 5: lượt 3 chạy hai lần vì
  lần đầu chết giữa chừng).
- Verdict trước: `verdict-cu/r2-luot-3-VERDICT.md` (6 P1 + 1 P2), các lượt trước trong `verdict-cu/`.

## QUYẾT ĐỊNH CỦA CHỦ KHO SAU LƯỢT 3 (Issue #960, 29-10) — phạm vi lượt này
- **Nhóm A — đã vá, phải đo:** `GIT_DIR` kế thừa · replace ref/graft · ref con khớp tiền tố (`master/topic`) · `GIT_TRACE` và
  cảnh báo cấu hình làm kho lành thành rc=2 · chốt rc chưa có răng · partial clone thật (promisor).
- **Nhóm B — KHAI là tiền đề, KHÔNG vá:** object sai băm / commit-graph sai parent mà git IM LẶNG (rc sạch, stderr rỗng,
  stdout đúng dạng) — chỉ `git fsck` phát hiện được. Đừng lập lại finding cho đúng lớp này; nếu tìm ra một trạng thái hỏng
  KHÁC mà git im lặng, hãy nói rõ vì sao nó không thuộc nhóm B.

## Lời khai của executor về bản vá lượt 3 (tự kiểm, ĐỪNG tin)
1. `_env_git`: bỏ MỌI biến `GIT_*` kế thừa rồi đặt `LC_ALL=C`, `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1`,
   `GIT_NO_REPLACE_OBJECTS=1`. `_chay_git` là MỘT chỗ gọi git cho phép đo lẫn kiểm sức khoẻ kho.
2. stderr NỀN: `_kho_lanh` chạy `rev-parse --git-dir`, lưu các dòng stderr của nó theo kho; `_git_do` trừ các dòng ấy trước
   khi đòi stderr rỗng (cảnh báo cấu hình in ở mọi lệnh — đo 29-10 với `core.fsyncObjectFiles`).
3. `_kho_lanh` từ chối: kho nông · `extensions.partialclone` · `remote.<x>.promisor` · tệp grafts (`--git-path info/grafts`).
4. `_nhanh_mac_dinh` bỏ qua ref con mà `for-each-ref` khớp theo tiền tố; dòng lạ khác vẫn `KhongDoDuoc`.
5. Bỏ cờ `core.commitGraph=false` vì nó chỉ giảm nhẹ nhóm B mà không có ca đo được.
6. Ca: c91 thêm partial promisor thật (`clone --filter=blob:none`) + grafts (lời nhắc deprecated đã tắt); c95 năm kiểu môi
   trường trên kho lành ⇒ đúng một L-ANCESTRY; c96 git giả rc=3 không stderr ⇒ rc=2. Đột biến m125–m131; m103/m114 neo lại.
7. `python3 ops/bien_nhan_v2_test.py` ⇒ `93/93 ca · 128/128 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM`. Gate `--root .` rc=0, nợ 1/60/0.

## Nhiệm vụ: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `3a52e6d194d08a755793cf449f393fb15b56757b`
Danh sách dưới KHÔNG đủ — mỗi lỗi thật bạn tìm ra ngoài danh sách được tính là finding.

(a) **Đóng finding lượt 3** (nhóm A): chạy lại CHÍNH phản chứng của bạn; đóng thật / còn mở / đóng một phần.
(b) **Stderr nền.** Phép trừ dòng nền có thể nuốt một lỗi THẬT không (dòng lỗi trùng chữ với dòng nền; lỗi chỉ in ở lệnh
    đầu)? Có cảnh báo vô hại nào KHÔNG in ở `rev-parse --git-dir` mà in ở lệnh đo (vẫn bắt nhầm)?
(c) **Môi trường.** Còn đường nào môi trường/cấu hình đổi kết quả đo mà stderr rỗng (ngoài nhóm B): `includeIf`, alternates,
    `core.*`, `safe.directory`, hooks, `HOME`/XDG config…? Bỏ mọi `GIT_*` có làm hỏng trường hợp hợp lệ nào (CI, worktree)?
(d) **Không phá gì.** Suite N/N hai số BẰNG NHAU; ruff F delta 0 so base; doctrine-scan; `git diff --check 4488444 HEAD`;
    corpus thật nợ 1/60/0; mô phỏng CI `pull_request` (merge commit, `fetch-depth: 0`, không `origin/HEAD`).
(e) **Đột biến của bạn.** Trên BẢN SAO: gỡ ≥ 5 chốt của phần vá lượt 3 (khác m125–m131) và ghi ca nào ĐỎ.
(f) **Hình dạng kế thừa.** Gắn nhãn MỖI finding `loi-do | bo-chon-ung-vien | nguon-goc-cau | khac` — bắt buộc.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (chứa PROMPT.md, KHÔNG trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm
sau MỖI hướng thử. Cuối cùng dòng đầu `verdict: approve` hoặc `verdict: changes_requested`, dòng 2
`reviewed_sha: 3a52e6d194d08a755793cf449f393fb15b56757b`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc như lượt 3 (`verdict-cu/r2-luot-3-VERDICT.md`): `## BẢNG ĐO` · `## BẢNG ĐÓNG FINDING LƯỢT 3` (mỗi finding một dòng:
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
sạch trên bản sao tại `3a52e6d`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor. KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push,
KHÔNG gọi mạng. Chỉ CHẠY ca test có sẵn và ĐỘT BIẾN mã/fixture trên bản sao.
Mọi khẳng định phải đo TẠI `3a52e6d194d08a755793cf449f393fb15b56757b`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `3a52e6d…`; nhánh của kho ở `refs/remotes/origin/*`, `origin/master` =
`2618eb4`; `refs/remotes/origin/HEAD` là symref trỏ nhánh ứng viên — mô phỏng CI thì xoá nó trên bản sao; `core.abbrev=7`).
Mirror trần: `mirror.git`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO
ĐƯỢC chứ đừng ghi thành finding.
