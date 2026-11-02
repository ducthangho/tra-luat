# Cross-review lượt 2 — packet `NO-CAU-LICH-SU-BIEN-NHAN` (Issue ducthangho/tra-luat#960), PR #976 — reviewer: codex

## Đối tượng
- `reviewed_sha`: `916a60ac2d91025879aa420c42aacbf6c26d94c4` (head PR #976, nhánh `agent/wp960-g1-claude`, CHƯA merge).
  Lịch sử: `7208fe0` (thi công, cha `e3ea139` = base lease) → `7ae7fc1` (merge `origin/master` `e139e55`) → `acedecb` → `33d331b` → `916a60a`.
- Diff so `origin/master` (`e139e55`): `diff.patch`, `numstat.txt` — đúng hai tệp `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py`.
- Đặc tả ĐÓNG BĂNG (nguồn DUY NHẤT của phạm vi): `cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN.md`, sha256 phải là
  `69394c7658db28196b72e3a1b00f4f6931ad9aba8b9fdcf76563fab33edaa671` (tự kiểm). Mục tiêu M1–M5, nghiệm thu A1–A7, `ngoai_pham_vi`, `chua_do_duoc`.
- Review class hiệu lực: `sensitive`. Executor: Claude (khác họ với bạn).

## Lượt trước và bản vá
- Lượt 1 (`verdict-cu/wp960-review-1-codex-VERDICT.md`) chấm `7ae7fc1` ra `changes_requested` 0/6/2/0. Connector GitHub cũng chấm `7ae7fc1` với 4 P2: run.json hỏng thành "không áp"; OID viết tắt toàn chữ số bị bỏ; dòng TRÍCH DẪN hiện vật khác bị đọc thành tự khai surface; mốc blame cả scalar kéo câu cũ vào.
- Bản vá = `7ae7fc1..916a60a` (`diff-tu-luot1.patch`): ba commit `acedecb`, `33d331b`, `916a60a`. Toàn bộ so `origin/master`: `diff.patch`, `numstat.txt`.

## Lời khai của executor (tự kiểm, ĐỪNG tin)
1. `python3 ops/bien_nhan_v2.py --root .` ⇒ rc=0, `TỔNG: ĐẠT`, `câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 3 · L-SURFACE chua_do_duoc 0` (hai nợ L-SURFACE pr896-review-8, pr915-review-1 gỡ vì là dòng trích dẫn).
2. `python3 ops/bien_nhan_v2_test.py` ⇒ `85/85 ca · 95/95 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM` (~6 phút).
3. Mốc: "commit thêm câu" = commit ĐẦU TIÊN trong `git log --reverse -- <tệp>` có scalar chứa câu ĐÃ CHUẨN HOÁ (thay blame); phiên bản không giải mã được ⇒ KHÔNG ĐO ĐƯỢC; câu chỉ ở cây làm việc ⇒ so HEAD; không theo dõi đổi tên tệp.
4. OID: tra MỌI token 7–40 hex; token trộn số+chữ không tra được ⇒ KHÔNG ĐO ĐƯỢC; token THUẦN số/THUẦN chữ không tra được ⇒ bỏ qua (coi là số/từ thường). Lượt 1 đề nghị token thuần chữ không tra được ⇒ rc=2; executor KHÔNG làm vì từ hex thường sẽ đỏ hàng loạt — chấm lại lựa chọn này.
5. L-SURFACE: run.json/verdict CÓ mà hỏng ⇒ KHÔNG ĐO ĐƯỢC; xét MỌI khai báo trên dòng; khai báo đứng SAU trích dẫn `đường/dẫn.ext:N:` bị bỏ qua.
6. Alias YAML vòng ⇒ `KhongDoDuoc`. Fixture `_kho_cau` ghim ngày commit ⇒ SHA tất định (c74 từng chập chờn trên CI).
7. A3: khối `>-` do bộ phân tích YAML gấp trước khi cổng thấy, nên cổng không có chốt riêng cho nó; `m78` chỉ có răng với khối `|`.
8. Kích thước diff +1037/−12, vượt ngưỡng 1.000 dòng của ADR-0044 cho packet thường (khai trong PR).

## Nhiệm vụ: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `916a60ac2d91025879aa420c42aacbf6c26d94c4`
Danh sách dưới KHÔNG đủ — mỗi lỗi thật bạn tìm ra ngoài danh sách được tính là finding.

(a) **Đúng đặc tả.** Đối chiếu từng M1–M4 và A1–A7 với mã + ca test. Ca nào không đo đúng điều A# đòi (ví dụ đột biến giết ca vì lý do khác lý do đặc tả nêu) là finding.
(b) **Ba trạng thái.** Tìm mọi đường một lỗi ĐO (git hỏng, object thiếu, YAML lạ, tệp không đọc được, nhánh mặc định thiếu) bị báo thành VI PHẠM (rc=1) hoặc bị nuốt thành SẠCH (rc=0). Đây là lớp lỗi kho đã trả giá nhiều lần (`R4-02`).
(c) **Ứng viên & mốc.** Thử trên BẢN SAO: câu bị bỏ sót / bắt nhầm; mốc `dung_tai` có thể "tẩy trắng" một câu cũ không (sửa câu cũ thêm mốc trỏ master hiện tại); blame range của scalar có đúng không với `>-`, `|`, scalar một dòng, scalar trong list.
(d) **Nợ đóng băng.** `NO_CAU_LICH_SU` có khớp ĐÚNG vi phạm thật (không thừa, không thiếu)? Có ổn định khi chạy trong CI `pull_request` (checkout merge commit, `fetch-depth: 0`) — đặc biệt khi `origin/HEAD` không tồn tại? Nợ chết / nợ mới có bắt được không?
(e) **Không phá gì.** Toàn bộ `ops/bien_nhan_v2_test.py` N/N hai số BẰNG NHAU; mọi đột biến cũ vẫn có răng; `ruff check --select F` delta 0 so `origin/master` (nếu có ruff; không có thì KHÔNG ĐO ĐƯỢC); `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `git diff --check origin/master HEAD`.
(g) **Finding cũ.** Với từng finding của lượt 1 và 4 finding connector: ĐÃ ĐÓNG | CHƯA ĐÓNG | ĐÓNG MỘT PHẦN, kèm phép đo. Bản vá có tự sinh lỗi mới không (đặc biệt `_commit_them_cau` theo lịch sử, `_co_cau`, `_RE_TRICH_DAN`).
(f) **Đột biến của bạn.** Trên BẢN SAO (clone từ `mirror.git` vào thư mục tạm ngoài `cay-kho/`, checkout `916a60a`): gỡ từng chốt mới trong `ops/bien_nhan_v2.py` (≥ 5 chốt khác với `m73`–`m82`) và ghi ca nào ĐỎ; chốt không ca nào đỏ = finding.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (thư mục chứa PROMPT.md, KHÔNG phải trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: 916a60ac2d91025879aa420c42aacbf6c26d94c4`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc:
```
verdict: ...
reviewed_sha: ...
Kết quả: ...

## KẾT LUẬN VỀ FINDING CŨ
- <slug>: ĐÃ ĐÓNG | CHƯA ĐÓNG | ĐÓNG MỘT PHẦN — bằng chứng

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
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`, và PHẢI kiểm `patch --dry-run --fuzz=0` sạch trên bản sao tại `916a60a`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor. KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push, KHÔNG gọi mạng. Chỉ CHẠY ca test có sẵn và ĐỘT BIẾN mã/fixture trên bản sao.
Mọi khẳng định phải đo TẠI `916a60ac2d91025879aa420c42aacbf6c26d94c4`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `916a60a…`; mọi nhánh ở `refs/remotes/origin/*`, KHÔNG có `refs/remotes/origin/HEAD`; `core.abbrev=7`). Mirror trần: `mirror.git`. Verdict lượt 1: `verdict-cu/`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO ĐƯỢC chứ đừng ghi thành finding.
