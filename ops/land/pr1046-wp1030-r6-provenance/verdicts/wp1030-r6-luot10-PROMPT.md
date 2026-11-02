# Cross-review L10 — packet wp1030 (Issue #1030), PR #1046 đã merge

Bạn là REVIEWER độc lập, CHỈ ĐỌC, chạy dưới lease `wp1030-r6-review-l10-codex`
(nhánh `ops/wp1030-r4-g1-lease`, tệp `ops/leases/wp1030-r6-review-l10-codex.yaml`).
Executor là họ Claude; bạn là họ OpenAI — đây là lượt `cross_approved` §8.1.

## Bố trí
- `./cay/` = clone sạch của `ducthangho/tra-luat` ở **đúng** `79017438cccaf77cd41e8126633943075b7b9200`
  (tree `721e379cec1a561b64765043bd6959ff436cbfa1`), detached, có đủ lịch sử. **KHÔNG sửa bất kỳ tệp nào trong `./cay/`.**
- `./goi/` = chỗ duy nhất bạn được ghi. Ghi VERDICT vào `./goi/VERDICT.md`, ghi TĂNG DẦN (mỗi hướng xong thì ghi ngay).
  Dòng đầu `trang_thai: dang_review`, xong thì đổi thành `trang_thai: xong`.
- Bản sao thử nghiệm: tạo bằng `mktemp -d -p ./goi` rồi `git clone --shared ./cay <thu-muc>`; không đụng `./cay/`.
- Không mạng ra ngoài ngoài GitHub đọc; không push, không PR, không comment GitHub, không LIVE, không credential thật.
- Không viết nguyên văn chuỗi bỏ-qua-CI (`skip` + `ci` trong ngoặc vuông) ở bất kỳ đâu.

## Phạm vi
- Spec có hiệu lực: `cay/ops/specs/wp1030-pkg-secret-scan-duoi-la-r6.md`, sha256 phải là
  `17d76055b288836057a18c234c4893bc0fced836d07bd8d3f43495a97f7fa6be` — đo lại, lệch thì DỪNG và ghi vào VERDICT.
- Diff packet = `git -C cay diff 059a4a5a080a98270973ef9ce23a38dad5aa2f38..79017438cccaf77cd41e8126633943075b7b9200`
  (059a4a5 = merge-base của head với cha thứ nhất của merge 8cdb15a7). Kỳ vọng 6 tệp:
  `scripts/pkg_secret_scan.py`, `scripts/test_fragments/wp1030_pkg_secret_scan_duoi_la.py`, `scripts/tl_test_fragments_bundled.py`,
  `changelog.d/wp-1030.md`, `RELEASE_MANIFEST.json`, `scripts/tl_selftest.py`.

## Phải trả lời (lease.verdict_must_answer)
1. `79017438` có đúng là `7da1bd25ff1f731967547de48e3a889daa22bf52` + merge `059a4a5` mà KHÔNG đổi 6 tệp packet không — đo bằng git
   (cha, merge-base, diff 6 tệp giữa 7da1bd2 và 79017438), không nhận lời khai.
2. Có lỗi hành vi P0–P3 nào trong diff packet tại ĐÚNG `79017438` so với spec r6 (M1–M6, A1–A9) không. Gợi ý hướng, không giới hạn:
   - M1 `_is_scannable`: tệp đuôi lạ đi cùng nhánh với tệp không đuôi (trần `MAX_BYTES`, NUL trong 8192 byte đầu, `OSError` ⇒ không quét);
     tệp `TEXT_SUFFIXES` giữ nguyên hành vi.
   - M2 fragment: A1/A2 khẳng định bằng TẬP hit; khoá giả dựng lúc chạy (fragment không tự thành hit); ba điều kiện tha trong gói
     (i) bộ quét vắng (ii) chính sách loại theo thiết kế đo trên sentinel có thật (iii) không `.git` — mọi lỗi ⇒ False (fail-closed).
     Kiểm xem có đường nào để fragment được tha trong checkout dev, hoặc được tha khi chính sách giữ bộ quét mà gói thiếu tệp.
   - M6/A9: hunk của `scripts/tl_selftest.py` chỉ nằm trong `_c291_docs_ngoai_goi` và `_c357_agents_ngoai_goi` (dòng xoá theo AST base,
     dòng thêm theo AST head).
   - M3/M5: bundle và manifest khớp sinh lại (`python scripts/tl.py test-fragments-check --json`, `release-verify RELEASE_MANIFEST.json --strict --json`).
3. Verdict `approve` hoặc `request_changes`, neo `reviewed_sha: 79017438cccaf77cd41e8126633943075b7b9200`.

Chạy kiểm được thì chạy (trong `./cay` chỉ các lệnh chỉ đọc; selftest đầy đủ `python scripts/tl.py --selftest` được phép nếu nó không
ghi vào cây — nếu nghi ngờ thì chạy trên bản sao `--shared`). Ghi rõ lệnh, rc, dòng tổng. Không đột biến ngoài mã packet.

## Dạng VERDICT.md
```
trang_thai: xong
Cross-review L10 — wp1030, Issue #1030
Lease: wp1030-r6-review-l10-codex
Provider: openai_codex
reviewed_sha: 79017438cccaf77cd41e8126633943075b7b9200
reviewed_tree: <đo>
verdict: approve | request_changes
P0: <n>  P1: <n>  P2: <n>  P3: <n>

HƯỚNG k: <tên>
  giả thuyết : ...
  lệnh       : ...
  output     : ...
  kết luận   : LỖI Pn | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC
...
FINDING (nếu có): mã, mức, tệp:dòng, đường tái hiện chạy được, đề xuất sửa (mô tả bằng lời).
```
