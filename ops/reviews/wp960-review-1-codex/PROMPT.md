# Cross-review lượt 1 — packet `NO-CAU-LICH-SU-BIEN-NHAN` (Issue ducthangho/tra-luat#960), PR #976 — reviewer: codex

## Đối tượng
- `reviewed_sha`: `7ae7fc1ec1b8345115a4918aedefff6e45d20b2a` (head PR #976, nhánh `agent/wp960-g1-claude`, CHƯA merge).
  Đó là merge `origin/master` (`e139e55`) vào commit thi công `7208fe0` (cha `e3ea139` = base của lease).
- Diff so `origin/master` (`e139e55`): `diff.patch`, `numstat.txt` — đúng hai tệp `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py`.
- Đặc tả ĐÓNG BĂNG (nguồn DUY NHẤT của phạm vi): `cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN.md`, sha256 phải là
  `69394c7658db28196b72e3a1b00f4f6931ad9aba8b9fdcf76563fab33edaa671` (tự kiểm). Mục tiêu M1–M5, nghiệm thu A1–A7, `ngoai_pham_vi`, `chua_do_duoc`.
- Review class hiệu lực: `sensitive`. Executor: Claude (khác họ với bạn).

## Lời khai của executor (tự kiểm, ĐỪNG tin)
1. `python3 ops/bien_nhan_v2.py --root .` ⇒ rc=0, `TỔNG: ĐẠT`, dòng `câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 5 · L-SURFACE chua_do_duoc 0`.
2. `python3 ops/bien_nhan_v2_test.py` ⇒ `76/76 ca đạt · 84/84 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt` (~5 phút).
3. Danh sách nợ rỗng ⇒ rc=1 với đúng 66 dòng ba luật (ca `c76`); `--sinh-no-cau-lich-su` in lại đúng khối `NO_CAU_LICH_SU`.
4. Mỗi chốt mới có một đột biến (`m73`–`m82`) giết ĐÚNG ca đích (`c69`–`c75`); `m13` cũ được trỏ sang hàm mới `_ma_thoat`.
5. Diễn giải đặc tả mà executor tự chọn (soi kỹ — đây là chỗ dễ sai nhất):
   - "câu" = đoạn tách bởi `[.;!?]` + khoảng trắng, trên scalar ĐÃ gộp khoảng trắng; chỉ scalar giá trị kiểu chuỗi, không đọc chú thích YAML.
   - OID ứng viên = 7–40 hex thường có ít nhất một chữ số VÀ một chữ cái; L-REVIEW chỉ nhận OID 40 ký tự.
   - "commit đầu tiên thêm câu" = tập commit `git blame` của các dòng TRONG phạm vi scalar có chứa OID; mốc phải là tổ tiên của MỌI commit đó; dòng chưa commit ⇒ so với HEAD.
   - Nhánh mặc định = `refs/remotes/origin/HEAD` → `refs/remotes/origin/master` → `refs/heads/master`.
   - L-SURFACE: giá trị surface = token đầu tiên SAU cụm `execution[_ ]surface` trên cùng dòng mà thuộc tập surface của hợp đồng provider; run_json/verdict không đọc được ⇒ luật không áp, đếm vào `chua_do_duoc` (không rc=2). Nguồn provider hỏng ⇒ L-SURFACE vào KHÔNG ĐO ĐƯỢC.
   - Mục nợ của tệp không có trong cây ⇒ bỏ qua (như `NO_DA_DO`); test `c75` đòi mọi mục nợ trỏ tệp có thật trong kho.
   - `luot` không phải số nguyên ⇒ L-REVIEW vào KHÔNG ĐO ĐƯỢC khi có biên nhận khác cùng `reviewed_sha`.

## Nhiệm vụ: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `7ae7fc1ec1b8345115a4918aedefff6e45d20b2a`
Danh sách dưới KHÔNG đủ — mỗi lỗi thật bạn tìm ra ngoài danh sách được tính là finding.

(a) **Đúng đặc tả.** Đối chiếu từng M1–M4 và A1–A7 với mã + ca test. Ca nào không đo đúng điều A# đòi (ví dụ đột biến giết ca vì lý do khác lý do đặc tả nêu) là finding.
(b) **Ba trạng thái.** Tìm mọi đường một lỗi ĐO (git hỏng, object thiếu, YAML lạ, tệp không đọc được, nhánh mặc định thiếu) bị báo thành VI PHẠM (rc=1) hoặc bị nuốt thành SẠCH (rc=0). Đây là lớp lỗi kho đã trả giá nhiều lần (`R4-02`).
(c) **Ứng viên & mốc.** Thử trên BẢN SAO: câu bị bỏ sót / bắt nhầm; mốc `dung_tai` có thể "tẩy trắng" một câu cũ không (sửa câu cũ thêm mốc trỏ master hiện tại); blame range của scalar có đúng không với `>-`, `|`, scalar một dòng, scalar trong list.
(d) **Nợ đóng băng.** `NO_CAU_LICH_SU` có khớp ĐÚNG vi phạm thật (không thừa, không thiếu)? Có ổn định khi chạy trong CI `pull_request` (checkout merge commit, `fetch-depth: 0`) — đặc biệt khi `origin/HEAD` không tồn tại? Nợ chết / nợ mới có bắt được không?
(e) **Không phá gì.** Toàn bộ `ops/bien_nhan_v2_test.py` N/N hai số BẰNG NHAU; mọi đột biến cũ vẫn có răng; `ruff check --select F` delta 0 so `origin/master` (nếu có ruff; không có thì KHÔNG ĐO ĐƯỢC); `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `git diff --check origin/master HEAD`.
(f) **Đột biến của bạn.** Trên BẢN SAO (clone từ `mirror.git` vào thư mục tạm ngoài `cay-kho/`, checkout `7ae7fc1`): gỡ từng chốt mới trong `ops/bien_nhan_v2.py` (≥ 5 chốt khác với `m73`–`m82`) và ghi ca nào ĐỎ; chốt không ca nào đỏ = finding.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (thư mục chứa PROMPT.md, KHÔNG phải trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: 7ae7fc1ec1b8345115a4918aedefff6e45d20b2a`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc:
```
verdict: ...
reviewed_sha: ...
Kết quả: ...

## BẢNG ĐO
| khẳng định | bên giao khai | đo được (lệnh) | khớp? |

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
P1 = hành vi sai đo được (kết quả sai, trạng thái sai, chốt không răng, lệch đặc tả). P2 = khai rộng hơn phép đo / thiếu điều kiện / ca test không đo đúng điều nó khai. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface.
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`, và PHẢI kiểm `patch --dry-run --fuzz=0` sạch trên bản sao tại `7ae7fc1`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor. KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push, KHÔNG gọi mạng. Chỉ CHẠY ca test có sẵn và ĐỘT BIẾN mã/fixture trên bản sao.
Mọi khẳng định phải đo TẠI `7ae7fc1ec1b8345115a4918aedefff6e45d20b2a`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `7ae7fc1…`; mọi nhánh ở `refs/remotes/origin/*`, KHÔNG có `refs/remotes/origin/HEAD`; `core.abbrev=7`). Mirror trần: `mirror.git`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO ĐƯỢC chứ đừng ghi thành finding.
