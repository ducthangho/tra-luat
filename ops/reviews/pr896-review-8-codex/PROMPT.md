# Cross-review lượt 8 PR ducthangho/tra-luat#896 — reviewer: codex — chấm bản vá của lượt 7

## Đối tượng
- `reviewed_sha`: `fb87110cfab832406984f893e6a4c79fbb932aef`, head của PR #947 (nhánh `claude/pr896-review-2-codex`, CHƯA merge). Base master: `3e973a0`.
- Lượt 7 (`verdict-cu/pr896-review-7-codex-VERDICT.md`) chấm `05bc12e` ra `changes_requested` 0/2/1/0:
  - P1 `pr490-chua-merge-trai-lich-su-git`: `ops/land/pr491-r358-ghi-so-land-evidence.yaml` khai #490 chưa merge.
  - P1 `mo-ta-partial-luot6-khong-khop-hien-vat`: receipt lượt 6 + README mô tả sai `luot-hong-c0fa33fa/VERDICT.partial.md`.
  - P2 `surface-tu-khai-khac-ho-so-land-chua-co-caveat`: #823 wp802 lượt 5, #877 wp854 lượt 2.
  Gợi ý vá của lượt 7: `verdict-cu/pr896-review-7-codex-HINT.patch`.
- **Thay đổi kể từ lượt 7** = `05bc12e..fb87110` (`diff.patch`, `numstat.txt`), gồm hai commit: `54021fb` (CHỈ hiện vật lượt 7) và `fb87110` (biên nhận lượt 7, hàng README, khối land lượt 7, VÀ áp NGUYÊN hint lượt 7 bằng `patch --fuzz=0` trong cùng commit). Lời khai của bên vá — tự kiểm, đừng tin. Đặc biệt kiểm caveat `LAN-CHAY-DAU-CHET-VI-MAY-CHU-QUA-TAI` mới của biên nhận lượt 7 (mô tả `luot-hong-577bb136/VERDICT.partial.md`) với chính tệp ấy.
- Toàn bộ PR #947 so với master `3e973a0`: `diff-pr947.patch`, `numstat-pr947.txt`.

## Nhiệm vụ chính: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `fb87110cfab832406984f893e6a4c79fbb932aef`
Danh sách dưới KHÔNG đủ — mỗi khẳng định bạn tìm ra mà nó bỏ sót được tính là finding.

(a) **Ba finding lượt 7 đã đóng chưa.** So `fb87110` với hint lượt 7 (byte-for-byte trên các tệp hint đụng); mỗi câu được neo mốc/đính chính có đúng OID, dòng, nguồn, số đo không.

(b) **Lớp lỗi đã hết chưa** — chỉ hai lớp: (1) verdict (trong `ops/reviews/` HOẶC trong provenance của `ops/land/`) TỰ KHAI một execution surface khác run.json/receipt/hồ sơ của nó mà chưa có caveat/đính chính; (2) câu trạng thái trong `ops/reviews/*.receipt.yaml`, `ops/reviews/README.md`, `ops/reviews/*-legacy-caveats.yaml`, `ops/land/*-land-evidence.yaml` (kể cả verdict nằm trong thư mục provenance của land) phát biểu như hiện hành (chưa review / chưa áp / chưa là tổ tiên master / chưa merge) mà ĐO tại `fb87110` thấy đã sai và không có mốc lịch sử. Bao gồm chính các câu do bản vá `fb87110` viết. Phân biệt tự khai với chỉ nhắc chuỗi khi mô tả finding; phân biệt "chưa land" (cần quyết định chủ kho) với "chưa merge/chưa tổ tiên" (đo được bằng git).

(c) **Không phá gì.** Byte của mọi `*-verdict.md` bị nhắc tới giữ nguyên (sha256 so `verdict_sha256`); YAML mọi tệp đã sửa parse được, không trùng `id` caveat trong cùng receipt; receipt v1 nằm trong danh sách miễn trừ băm của `ops/bien_nhan_v2.py` không bị đổi byte. Chạy riêng `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` (đòi `N/N` hai số BẰNG NHAU). Trên BẢN SAO kho (clone từ `mirror.git` vào thư mục tạm ngoài `cay-kho/`, checkout `fb87110`): xoá một hàng README mới / một caveat mới ⇒ ca nào ĐỎ; ca không đỏ thì ghi rõ chốt ấy không có răng.

(d) Chạy và ghi rc + dòng kết luận tại `cay-kho/`: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, `python3 scripts/tl.py doc-claims-check --json` (đòi `"ok": true`).

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (thư mục chứa PROMPT.md, KHÔNG phải trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: fb87110cfab832406984f893e6a4c79fbb932aef`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc:
```
verdict: ...
reviewed_sha: ...
Kết quả: ...

## KẾT LUẬN VỀ FINDING CŨ
- P1 pr490-chua-merge-trai-lich-su-git: ĐÃ ĐÓNG | CHƯA ĐÓNG | ĐÓNG MỘT PHẦN — bằng chứng
- P1 mo-ta-partial-luot6-khong-khop-hien-vat: ...
- P2 surface-tu-khai-khac-ho-so-land-chua-co-caveat: ...

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
P1 = khẳng định sai về sự thật đo được TẠI `fb87110cfab832406984f893e6a4c79fbb932aef`. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface (đó chính là lớp lỗi đang review).
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`, và PHẢI kiểm `patch --dry-run --fuzz=0` sạch trên bản sao tại `fb87110`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push, KHÔNG gọi mạng (sandbox không có mạng). Bạn chỉ CHẠY các ca test có sẵn và ĐỘT BIẾN tệp tài liệu/biên nhận trên bản sao; không cần tự soạn mã khai thác nào.
Mọi khẳng định phải đo TẠI `fb87110cfab832406984f893e6a4c79fbb932aef`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `fb87110cfab832406984f893e6a4c79fbb932aef`; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Mirror trần: `mirror.git`. Verdict + hint lượt 7: `verdict-cu/`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO ĐƯỢC chứ đừng ghi thành finding.
