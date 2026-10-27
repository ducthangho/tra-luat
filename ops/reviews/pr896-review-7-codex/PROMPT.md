# Cross-review lượt 7 PR ducthangho/tra-luat#896 — reviewer: codex — chấm bản vá của lượt 6

## Đối tượng
- `reviewed_sha`: `05bc12e2b9008071ca28edbd4574e58644d48220`, head của PR #947 (nhánh `claude/pr896-review-2-codex`, CHƯA merge). Base master: `3e973a0`.
- Lượt 6 (`verdict-cu/pr896-review-6-codex-VERDICT.md`) chấm `22382d8` ra `changes_requested` 0/2/0/0:
  - P1 `phu-nhan-ancestry-chi-tren-nhanh-da-cu`: 7 trường ở 5 receipt (doctor-github-mcp-review-6, don-nhanh-base-review-4/5 là v1 đóng băng, wp461-review-1, wp523-r15-review-1).
  - P1 `surface-service-cli-trong-ho-so-land`: 3 verdict trong provenance land (pr832 wp831 lượt 7, pr848 wp744 g3 lượt 1, pr862 wp748 r21 lượt 1) tự khai `codex_service`.
  Gợi ý vá của lượt 6: `verdict-cu/pr896-review-6-codex-HINT.patch`.
- **Thay đổi kể từ lượt 6** = `22382d8..05bc12e` (`diff.patch`, `numstat.txt`), gồm hai commit: `825dab1` (CHỈ hiện vật lượt 6) và `05bc12e` (biên nhận lượt 6, hàng README, khối land lượt 6, VÀ áp NGUYÊN hint lượt 6 bằng `patch --fuzz=0` trong cùng commit). Lời khai của bên vá — tự kiểm, đừng tin.
- Toàn bộ PR #947 so với master `3e973a0`: `diff-pr947.patch`, `numstat-pr947.txt`.

## Nhiệm vụ chính: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `05bc12e2b9008071ca28edbd4574e58644d48220`
Danh sách dưới KHÔNG đủ — mỗi khẳng định bạn tìm ra mà nó bỏ sót được tính là finding.

(a) **Hai finding lượt 6 đã đóng chưa.** So `05bc12e` với hint lượt 6 (byte-for-byte trên các tệp hint đụng); mỗi câu được neo mốc có đúng OID/commit ghi receipt/phép đo không; đính chính v1 trong `ops/reviews/pr896-review-6-legacy-caveats.yaml` có đúng và có hàng README không; ba đính chính surface trong hồ sơ land có trích đúng dòng verdict và nguồn run cùng lượt không.

(b) **Lớp lỗi đã hết chưa** — chỉ hai lớp: (1) verdict (trong `ops/reviews/` HOẶC trong provenance của `ops/land/`) TỰ KHAI một execution surface khác run.json/receipt/hồ sơ của nó mà chưa có caveat/đính chính; (2) câu trạng thái trong `ops/reviews/*.receipt.yaml`, `ops/reviews/README.md`, `ops/reviews/*-legacy-caveats.yaml`, `ops/land/*-land-evidence.yaml` (kể cả verdict nằm trong thư mục provenance của land) phát biểu như hiện hành (chưa review / chưa áp / chưa là tổ tiên master / chưa merge) mà ĐO tại `05bc12e` thấy đã sai và không có mốc lịch sử. Bao gồm chính các câu do bản vá `05bc12e` viết. Phân biệt tự khai với chỉ nhắc chuỗi khi mô tả finding; phân biệt "chưa land" (cần quyết định chủ kho) với "chưa merge/chưa tổ tiên" (đo được bằng git).

(c) **Không phá gì.** Byte của mọi `*-verdict.md` bị nhắc tới giữ nguyên (sha256 so `verdict_sha256`); YAML mọi tệp đã sửa parse được, không trùng `id` caveat trong cùng receipt; receipt v1 nằm trong danh sách miễn trừ băm của `ops/bien_nhan_v2.py` không bị đổi byte. Chạy riêng `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` (đòi `N/N` hai số BẰNG NHAU). Trên BẢN SAO kho (clone từ `mirror.git` vào thư mục tạm ngoài `cay-kho/`, checkout `05bc12e`): xoá một hàng README mới / một caveat mới ⇒ ca nào ĐỎ; ca không đỏ thì ghi rõ chốt ấy không có răng.

(d) Chạy và ghi rc + dòng kết luận tại `cay-kho/`: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, `python3 scripts/tl.py doc-claims-check --json` (đòi `"ok": true`).

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (thư mục chứa PROMPT.md, KHÔNG phải trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: 05bc12e2b9008071ca28edbd4574e58644d48220`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc:
```
verdict: ...
reviewed_sha: ...
Kết quả: ...

## KẾT LUẬN VỀ FINDING CŨ
- P1 phu-nhan-ancestry-chi-tren-nhanh-da-cu: ĐÃ ĐÓNG | CHƯA ĐÓNG | ĐÓNG MỘT PHẦN — bằng chứng
- P1 surface-service-cli-trong-ho-so-land: ...

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
P1 = khẳng định sai về sự thật đo được TẠI `05bc12e2b9008071ca28edbd4574e58644d48220`. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface (đó chính là lớp lỗi đang review).
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`, và PHẢI kiểm `patch --dry-run --fuzz=0` sạch trên bản sao tại `05bc12e`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push, KHÔNG gọi mạng (sandbox không có mạng). Bạn chỉ CHẠY các ca test có sẵn và ĐỘT BIẾN tệp tài liệu/biên nhận trên bản sao; không cần tự soạn mã khai thác nào.
Mọi khẳng định phải đo TẠI `05bc12e2b9008071ca28edbd4574e58644d48220`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `05bc12e2b9008071ca28edbd4574e58644d48220`; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Mirror trần: `mirror.git`. Verdict + hint lượt 6: `verdict-cu/`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO ĐƯỢC chứ đừng ghi thành finding.
