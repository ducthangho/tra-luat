# Cross-review lượt 3 PR ducthangho/tra-luat#896 — reviewer: codex — chấm bản vá P1 của lượt 2

## Đối tượng
- `reviewed_sha`: `82359c4deec90edebbaebf9ab9d094902120b567`, head của PR #947 (nhánh `claude/pr896-review-2-codex`, CHƯA merge).
- PR #947 ghi sổ lượt 2 (`verdict-cu/pr896-review-2-codex-VERDICT.md`). Lượt 2 chấm `8d56009` ra `changes_requested`, 1 P1 `verdict-surface-bo-sot-pr889-luot1`: `ops/reviews/pr889-review-1-codex-verdict.md` dòng 7 tự khai `codex_service`, trong khi run.json `9f946d71` ghi `codex_cli`, và biên nhận `pr889-review-1` lẫn README chưa có caveat `VERDICT-KHAI-SAI-EXECUTION-SURFACE`.
- **Bản vá P1** = commit `82359c4` (cha `578fb4b`): áp NGUYÊN `HINT.patch` của lượt 2 bằng `patch -p0 --fuzz=0`. Diff: `diff.patch`, `numstat.txt` (`578fb4b..82359c4`).
- Toàn bộ nội dung PR #947 so với master `356eb26`: `diff-pr947.patch`, `numstat-pr947.txt`. Gồm: hiện vật lượt 2 (`ops/reviews/pr896-review-2-codex/` + bản phẳng, commit `25e7d11`), biên nhận/README/khối land (commit `765ae89`), merge master `578fb4b`, và bản vá `82359c4`.

## Nhiệm vụ chính: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `82359c4deec90edebbaebf9ab9d094902120b567`
Danh sách dưới KHÔNG đủ — mỗi khẳng định bạn tìm ra mà nó bỏ sót được tính là finding.

(a) **P1 của lượt 2 đã đóng chưa.** Caveat mới trong `ops/reviews/pr889-review-1-codex-verdict.receipt.yaml` và hàng mới trong `ops/reviews/README.md` có trích đúng không: số dòng 7, nguyên văn verdict, run id, `run.json` dòng 47, `run/stderr-header.txt` ghi `OpenAI Codex v0.163.0`. Byte verdict `pr889-review-1` có còn nguyên không (sha256 so với `verdict_sha256` của biên nhận và với SHA256SUMS). Đếm lại bằng grep trên MỌI `ops/reviews/*-verdict.md` (không chỉ #870/#889): có verdict nào khác tự khai một execution surface mà run.json/biên nhận của nó ghi khác, và chưa có caveat không? Phân biệt verdict TỰ KHAI surface với verdict chỉ NHẮC chuỗi ấy khi mô tả finding.

(b) **Lời khai của PR #947 về chính lượt 2** có khớp hiện vật không: `ops/reviews/pr896-review-2-codex-verdict.receipt.yaml` (`verdict_sha256`/`verdict_bytes`, `reviewed_sha`/`reviewed_tree`/`base_sha`, `so_p*` với dòng `Kết quả`, `run_json_ghi_chu`, số sự kiện và số `response_id` khác nhau trong `model_phuc_vu`, `evidence_url` trỏ commit nào và commit ấy có CHỈ mang hiện vật không), `sha256sum -c SHA256SUMS` trong `ops/reviews/pr896-review-2-codex/`, `OMITTED.txt`, năm hàng README của lượt 2, và khối `cap_nhat_20261026_luot2` cuối `ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml` (khối có sửa dòng cũ nào không; `landed: false`; đề xuất đơn vị land có ghi rõ là cần chủ kho chấp nhận không). Sau bản vá `82359c4`, câu nào trong hồ sơ lượt 2 đã trở thành SAI hoặc CŨ (ví dụ caveat `HINT-P1-CHUA-AP`, chữ "HINT.patch CHUA ap")? Nêu rõ, và nói câu đó đúng tại thời điểm nào.

(c) **Cổng có răng không.** Chạy riêng từng ca: `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` — ghi rc + dòng tổng kết (đòi `N/N` hai số BẰNG NHAU, đừng tin rc). Trên BẢN SAO kho (clone từ `mirror.git` vào thư mục tạm ngoài `cay-kho/`, checkout `82359c4`): xoá hàng README mới ⇒ ca nào ĐỎ; xoá caveat mới khỏi biên nhận ⇒ ca nào ĐỎ. Ca không đỏ thì ghi rõ chốt ấy không có răng (lượt 2 đã đo t27 chỉ đỏ khi xoá hàng README; đo lại cho bản vá này).

(d) Chạy và ghi rc + dòng kết luận tại `cay-kho/`: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, `python3 scripts/tl.py doc-claims-check --json` (đòi `"ok": true`), và `python3 scripts/pkg_secret_scan.py ops/reviews/pr896-review-2-codex`.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (thư mục chứa PROMPT.md, KHÔNG phải trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: 82359c4deec90edebbaebf9ab9d094902120b567`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc:
```
verdict: ...
reviewed_sha: ...
Kết quả: ...

## KẾT LUẬN VỀ FINDING CŨ
- P1 verdict-surface-bo-sot-pr889-luot1 (lượt 2): ĐÃ ĐÓNG | CHƯA ĐÓNG | ĐÓNG MỘT PHẦN — bằng chứng

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
P1 = khẳng định sai về sự thật đo được TẠI `82359c4deec90edebbaebf9ab9d094902120b567`. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface (đó chính là lớp lỗi đang review).
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push, KHÔNG gọi mạng (sandbox không có mạng). Bạn chỉ CHẠY các ca test có sẵn và ĐỘT BIẾN tệp tài liệu/biên nhận trên bản sao; không cần tự soạn mã khai thác nào.
Mọi khẳng định phải đo TẠI `82359c4deec90edebbaebf9ab9d094902120b567`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `82359c4deec90edebbaebf9ab9d094902120b567`; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Mirror trần: `mirror.git`. Verdict lượt 2: `verdict-cu/`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO ĐƯỢC chứ đừng ghi thành finding.
