# Cross-review lượt 4 PR ducthangho/tra-luat#896 — reviewer: codex — chấm bản vá của lượt 3

## Đối tượng
- `reviewed_sha`: `2e4183bc2dc40e6bc306e377fc442ff0f405bbe0`, head của PR #947 (nhánh `claude/pr896-review-2-codex`, CHƯA merge). Base master: `101263f`.
- Lượt 3 (`verdict-cu/pr896-review-3-codex-VERDICT.md`) chấm `82359c4` ra `changes_requested` 0/2/1/0:
  - P1 `verdict-surface-bo-sot-wp766`: `ops/reviews/wp766-r1-g1-exec-review-1-codex-verdict.md` dòng 12 tự khai `codex_service`, run.json ghi `codex_cli`, receipt chưa có caveat.
  - P1 `ho-so-luot2-van-khai-hint-chua-ap`: hồ sơ lượt 2 (receipt, README, khối land) vẫn nói HINT lượt 2 chưa áp sau khi `82359c4` đã áp.
  - P2 `surface-service-cli-thieu-dieu-kien-nguon`: 13 verdict tự khai service/API trong khi receipt ghi `codex_cli`, không có runtime evidence, chưa có caveat.
  Gợi ý vá của lượt 3: `verdict-cu/pr896-review-3-codex-HINT.patch`.
- **Bản vá** = commit `2e4183b` (cha `c8c1ee0`, là merge master). Diff: `diff.patch`, `numstat.txt` (`c8c1ee0..2e4183b`). Lời khai của bên vá (tự kiểm, đừng tin): 15 receipt áp NGUYÊN hint (`--fuzz=0`); hai hunk README và hunk hồ sơ land lệch ngữ cảnh nên được CHÈN TAY theo nội dung `+`/`-` của hint; ngoài hint, bên vá đổi thêm caveat `HINT-LUOT3-CHUA-AP` của chính lượt 3 thành `HINT-LUOT3-DA-AP-CAN-VERDICT-MOI` (receipt + README) và thêm `ghi_chu_luot3` cuối khối land mới.
- Cũng trong PR: `c8c1ee0` merge master; xung đột với #951 (cùng caveat `VERDICT-KHAI-SAI-EXECUTION-SURFACE` cho `pr889-review-1`) được giải bằng bản của master ở đúng hai hunk.
- Toàn bộ PR #947 so với master `101263f`: `diff-pr947.patch`, `numstat-pr947.txt`.

## Nhiệm vụ chính: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `2e4183bc2dc40e6bc306e377fc442ff0f405bbe0`
Danh sách dưới KHÔNG đủ — mỗi khẳng định bạn tìm ra mà nó bỏ sót được tính là finding.

(a) **Ba finding lượt 3 đã đóng chưa.** So `2e4183b` với hint lượt 3: phần chèn tay có đúng nội dung hint không (thừa/thiếu/sai dòng nào); caveat wp766 trích đúng dòng/run/run.json không; 13 caveat P2 có đúng 13 tệp, đúng dòng verdict, đúng run ID khai, và KHÔNG tự chọn bề mặt không; mọi câu "HINT chưa áp" của lượt 2 và lượt 3 nay có mốc lịch sử đúng không.

(b) **Lớp lỗi đã hết toàn kho chưa.** Quét MỌI `ops/reviews/*-verdict.md` (và bản trong thư mục nếu có): còn verdict nào TỰ KHAI một execution surface khác với run.json hoặc receipt của nó mà chưa có caveat không? Còn câu trạng thái nào trong `ops/reviews/*.receipt.yaml`, `ops/reviews/README.md`, `ops/land/pr896-*` đã CŨ tại `2e4183b` mà không có mốc lịch sử không (bao gồm chính các câu do bản vá `2e4183b` viết, ví dụ "commit kế tiếp sau c8c1ee0")? Phân biệt tự khai với chỉ nhắc chuỗi khi mô tả finding.

(c) **Không phá gì.** Byte của mọi `*-verdict.md` bị nhắc tới có giữ nguyên không (sha256 so `verdict_sha256` của receipt). YAML của mọi receipt/land đã sửa còn parse được không, trùng `id` caveat trong cùng receipt không. Chạy riêng `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` (đòi `N/N` hai số BẰNG NHAU). Trên BẢN SAO kho (clone từ `mirror.git` vào thư mục tạm ngoài `cay-kho/`, checkout `2e4183b`): xoá một hàng README mới / một caveat mới ⇒ ca nào ĐỎ; ca nào không đỏ thì ghi rõ chốt ấy không có răng.

(d) Chạy và ghi rc + dòng kết luận tại `cay-kho/`: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, `python3 scripts/tl.py doc-claims-check --json` (đòi `"ok": true`).

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (thư mục chứa PROMPT.md, KHÔNG phải trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: 2e4183bc2dc40e6bc306e377fc442ff0f405bbe0`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc:
```
verdict: ...
reviewed_sha: ...
Kết quả: ...

## KẾT LUẬN VỀ FINDING CŨ
- P1 verdict-surface-bo-sot-wp766: ĐÃ ĐÓNG | CHƯA ĐÓNG | ĐÓNG MỘT PHẦN — bằng chứng
- P1 ho-so-luot2-van-khai-hint-chua-ap: ...
- P2 surface-service-cli-thieu-dieu-kien-nguon: ...

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
P1 = khẳng định sai về sự thật đo được TẠI `2e4183bc2dc40e6bc306e377fc442ff0f405bbe0`. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface (đó chính là lớp lỗi đang review).
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`, và PHẢI kiểm `patch --dry-run --fuzz=0` sạch trên bản sao tại `2e4183b`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push, KHÔNG gọi mạng (sandbox không có mạng). Bạn chỉ CHẠY các ca test có sẵn và ĐỘT BIẾN tệp tài liệu/biên nhận trên bản sao; không cần tự soạn mã khai thác nào.
Mọi khẳng định phải đo TẠI `2e4183bc2dc40e6bc306e377fc442ff0f405bbe0`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `2e4183bc2dc40e6bc306e377fc442ff0f405bbe0`; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Mirror trần: `mirror.git`. Verdict + hint lượt 3: `verdict-cu/`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO ĐƯỢC chứ đừng ghi thành finding.
