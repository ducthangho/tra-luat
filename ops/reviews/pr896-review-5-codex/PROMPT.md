# Cross-review lượt 5 PR ducthangho/tra-luat#896 — reviewer: codex — chấm bản vá của lượt 4

## Đối tượng
- `reviewed_sha`: `1a276a15192013fdb1e472db409133b53ac57944`, head của PR #947 (nhánh `claude/pr896-review-2-codex`, CHƯA merge). Base master: `3e973a0`.
- Lượt 4 (`verdict-cu/pr896-review-4-codex-VERDICT.md`) chấm `2e4183b` ra `changes_requested` 0/3/1/0:
  - P1 `muc-luc-luot3-van-khai-hint-chua-ap`
  - P1 `trang-thai-chua-review-da-bi-verdict-sau-bac` (8 receipt)
  - P1 `phu-nhan-ancestry-chi-tren-nhanh-da-cu` (23 receipt)
  - P2 `surface-service-cli-con-sot-ngoai-13` (pr526-review-3, slice-b-c-review-2)
  Gợi ý vá của lượt 4: `verdict-cu/pr896-review-4-codex-HINT.patch`.
- **Bản vá** = commit `1a276a1` (cha `77a0a45`, là merge master `3e973a0`). Diff: `diff.patch`, `numstat.txt` (`77a0a45..1a276a1`). Lời khai của bên vá (tự kiểm, đừng tin): 31 tệp áp NGUYÊN hint (`--fuzz=0`); hunk hồ sơ land và hai hunk README lệch ngữ cảnh nên được CHÈN TAY theo nội dung `+`/`-` của hint; ngoài hint, bên vá đổi caveat `HINT-LUOT4-CHUA-AP` của chính lượt 4 thành `HINT-LUOT4-DA-AP-CAN-VERDICT-MOI` (receipt + README, kèm sửa hàng mục lục lượt 4) và thêm `ghi_chu_luot4` cuối hồ sơ land.
- Toàn bộ PR #947 so với master `3e973a0`: `diff-pr947.patch`, `numstat-pr947.txt`.

## Nhiệm vụ chính: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `1a276a15192013fdb1e472db409133b53ac57944`
Danh sách dưới KHÔNG đủ — mỗi khẳng định bạn tìm ra mà nó bỏ sót được tính là finding.

(a) **Bốn finding lượt 4 đã đóng chưa.** So `1a276a1` với hint lượt 4: phần chèn tay có đúng nội dung hint không (thừa/thiếu/sai dòng nào); mỗi câu được neo mốc có đúng OID/phép đo không; tệp đính chính v1 `ops/reviews/pr896-review-4-legacy-caveats.yaml` có đúng và có hàng README tương ứng không; receipt v1 đóng băng có bị sửa byte không.

(b) **Lớp lỗi đã hết chưa** — chỉ hai lớp: (1) verdict TỰ KHAI một execution surface khác run.json/receipt của nó mà chưa có caveat/đính chính; (2) câu trạng thái trong `ops/reviews/*.receipt.yaml`, `ops/reviews/README.md`, `ops/reviews/*-legacy-caveats.yaml`, `ops/land/pr896-*` phát biểu như hiện hành (chưa review / chưa áp / chưa là tổ tiên master / chưa merge) mà ĐO tại `1a276a1` thấy đã sai và không có mốc lịch sử. Bao gồm chính các câu do bản vá `1a276a1` viết. Phân biệt tự khai với chỉ nhắc chuỗi khi mô tả finding; phân biệt "chưa land" (cần quyết định chủ kho) với "chưa merge/chưa tổ tiên" (đo được bằng git).

(c) **Không phá gì.** Byte của mọi `*-verdict.md` bị nhắc tới giữ nguyên (sha256 so `verdict_sha256`); YAML mọi tệp đã sửa parse được, không trùng `id` caveat trong cùng receipt; receipt v1 nằm trong danh sách miễn trừ băm của `ops/bien_nhan_v2.py` không bị đổi byte. Chạy riêng `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` (đòi `N/N` hai số BẰNG NHAU). Trên BẢN SAO kho (clone từ `mirror.git` vào thư mục tạm ngoài `cay-kho/`, checkout `1a276a1`): xoá một hàng README mới / một caveat mới ⇒ ca nào ĐỎ; ca không đỏ thì ghi rõ chốt ấy không có răng.

(d) Chạy và ghi rc + dòng kết luận tại `cay-kho/`: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, `python3 scripts/tl.py doc-claims-check --json` (đòi `"ok": true`).

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (thư mục chứa PROMPT.md, KHÔNG phải trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: 1a276a15192013fdb1e472db409133b53ac57944`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc:
```
verdict: ...
reviewed_sha: ...
Kết quả: ...

## KẾT LUẬN VỀ FINDING CŨ
- P1 muc-luc-luot3-van-khai-hint-chua-ap: ĐÃ ĐÓNG | CHƯA ĐÓNG | ĐÓNG MỘT PHẦN — bằng chứng
- P1 trang-thai-chua-review-da-bi-verdict-sau-bac: ...
- P1 phu-nhan-ancestry-chi-tren-nhanh-da-cu: ...
- P2 surface-service-cli-con-sot-ngoai-13: ...

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
P1 = khẳng định sai về sự thật đo được TẠI `1a276a15192013fdb1e472db409133b53ac57944`. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface (đó chính là lớp lỗi đang review).
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`, và PHẢI kiểm `patch --dry-run --fuzz=0` sạch trên bản sao tại `1a276a1`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push, KHÔNG gọi mạng (sandbox không có mạng). Bạn chỉ CHẠY các ca test có sẵn và ĐỘT BIẾN tệp tài liệu/biên nhận trên bản sao; không cần tự soạn mã khai thác nào.
Mọi khẳng định phải đo TẠI `1a276a15192013fdb1e472db409133b53ac57944`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `1a276a15192013fdb1e472db409133b53ac57944`; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Mirror trần: `mirror.git`. Verdict + hint lượt 4: `verdict-cu/`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO ĐƯỢC chứ đừng ghi thành finding.
