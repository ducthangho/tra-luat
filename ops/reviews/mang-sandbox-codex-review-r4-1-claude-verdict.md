verdict: approve
reviewed_sha: 9f553fc8296c1d0c267cc13c9ce87cf89e30452d
P1: 0
P2: 0
finding_moi: 0

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `_c291_docs_ngoai_goi__reviewer-khong-chay-duoc-selftest` [P2, lượt trước, head `33581a93`]:
  **ĐÃ VÁ THẬT** — nhưng không phải theo nghĩa "sửa mã". Finding đó nói về ĐIỀU KIỆN REVIEW (không
  chạy được lệnh nào), không phải về bản vá. Lượt này có quyền Bash và đã CHẠY THẬT toàn bộ phản
  chứng bắt buộc (A)(B)(C)(D) — xem BẢNG ĐO bên dưới. Không finding nào về `_c291_docs_ngoai_goi`
  còn treo: ratchet đúng, có răng (đột biến 71→70 làm nó ĐỎ đúng ca), selftest 1698/1698 sạch trên
  head `9f553fc8`. Đóng.

## BẢNG ĐO

| khẳng định (lease r4 / spec) | đo được | khớp? |
|---|---|---|
| Write set r4 = đúng 5 đường đã khai | `git diff --name-only ac82ddc5 9f553fc8` = 5 đường, đúng khớp danh sách lease | ✓ |
| r4 (so r3) chỉ tái sinh manifest | `git diff --numstat 33581a93 9f553fc8` = `RELEASE_MANIFEST.json` duy nhất, `5 thêm/5 xoá` | ✓ |
| Manifest = sinh bằng bộ sinh, không gõ tay | `release-manifest --root . --out /tmp/x2.json --deterministic` rồi `diff` với `RELEASE_MANIFEST.json` trong cây (đã dọn 2 tệp scratch review ra khỏi cây trước khi sinh, vì generator quét filesystem thô, không theo `.git/info/exclude`) | `diff` **RỖNG** — giống hệt byte |
| `file_count` vẫn 180 | `grep '"file_count"' RELEASE_MANIFEST.json` → `180`; `grep -c '"path":'` → `180` | ✓ |
| `ok3`: `len(paths) + 71 == 251` | `find docs -name '*.md' \| wc -l` → **71** (đo lại số hạng, không đọc quan hệ) | ✓ 180+71=251 và cả hai số hạng riêng đều đúng |
| Không còn vị trí THI HÀNH nào dùng `70`/`250` cũ | `grep -n "len(paths) + 70\|len(tren_dia) == 70"` scripts/tl_selftest.py → rỗng; chỉ một vị trí thi hành duy nhất (dòng 21267/21270), đã là 71/251 | ✓ |
| `ci.yml` không có `continue-on-error`, selftest chạy TRƯỚC `release-verify` | `grep continue-on-error` chỉ khớp 1 dòng CHÚ THÍCH (dòng 278); liệt kê thứ tự step: "tl selftest" ở vị trí ~20-21, "release-verify strict" ở vị trí ~30 | ✓ |
| §10.2 nói "Worker CI không so feature branch với manifest committed" | `sed -n '699-715p' docs/PROTOCOL_DA_PHIEN.md` — đúng câu đó, dòng 710 | ✓ — mâu thuẫn với `ci.yml` là CÓ THẬT |
| `ci.yml` bước `release-verify strict` thực tế so cây với `RELEASE_MANIFEST.json` COMMITTED | `sed -n '480-481p' .github/workflows/ci.yml` → `run: python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` — đúng là tệp trong repo, không phải manifest tạm | ✓ — xác nhận đúng cái lease khai |

## PHẢN CHỨNG BẮT BUỘC — kết quả chạy thật

**(A) Selftest trên head `9f553fc8`**
```
python3 scripts/tl.py --selftest
```
→ `== tl selftest 1698/1698 ==`, không dòng `[FAIL]`. Chạy **một lần**, không gặp panic
`pyo3_runtime.PanicException` như cảnh báo trong prompt — sạch ngay từ lượt đầu, không cần chạy lại.

**(B) Răng ratchet r3** — trên bản sao NGOÀI cây (`/tmp/.../scratchpad/reviewB/cay`), sửa dòng 21267
`len(paths) + 71 == 251` → `len(paths) + 70 == 251` (chỉ một trong hai dòng, đúng như yêu cầu):
```
== tl selftest 1697/1698 ==
  [FAIL] r291_docs_ngoai_goi
```
Đúng như dự đoán: ĐỎ đúng một ca, tổng 1697/1698. **Có răng.**

**(C) Răng manifest r4** — trên bản sao NGOÀI cây (`/tmp/.../scratchpad/reviewC/cay`):
- Khôi phục manifest cũ (`git show 33581a93:RELEASE_MANIFEST.json > RELEASE_MANIFEST.json`) rồi
  `release-verify RELEASE_MANIFEST.json --strict --json`:
  → `rc=2`, `"package_hash_expected": "fea0b9ae…"`, `"package_hash_current": "298108fe…"`,
  `"package_hash_match": false`. Khớp CHÍNH XÁC cặp băm mà lease khai đã thấy trên CI thật.
- `git checkout -- RELEASE_MANIFEST.json` (khôi phục về `9f553fc8`) rồi chạy lại cùng lệnh:
  → `rc=0`, `"package_hash_match": true`, `"extra_files": []`. **Có răng, và cây thật xanh.**

Lưu ý phương pháp (không phải finding): lần đầu tôi chạy test (C) quên khôi phục
`RELEASE_MANIFEST.json` về head trước khi đo "cây thật", khiến kết quả đọc nhầm là vẫn đỏ — đã phát
hiện qua `git status --porcelain` và chạy lại đúng cách. Ghi ra đây để minh bạch quy trình đo,
không phải một khiếm khuyết của bản vá.

**(D) Năm cổng có thể vỡ theo manifest — chạy trên cây thật, `/home/user/rv334`:**

| cổng | lệnh | rc |
|---|---|---|
| golden-test | `python3 scripts/tl.py golden-test` | 0 |
| determinism-audit --strict | `python3 scripts/tl.py determinism-audit --strict` | 0 |
| doc-claims-check --strict | `python3 scripts/tl.py doc-claims-check --strict` | 0 |
| ci_phamvi --kiem-bam | `python3 .github/checks/ci_phamvi.py --kiem-bam` | 0 (`OK ci_phamvi (ve BAM)`) |
| release-check --full | `python3 scripts/tl.py release-check --full` | 0 |

Không cổng nào khác vỡ theo manifest.

**Chi tiết kỹ thuật đáng ghi (không phải finding, là minh bạch phép đo):** `release-check --full`
tự sinh manifest TẠM (không strict, không so `extra_files`) rồi tự-verify nó — khác cơ chế với
`release-verify <manifest> --strict` gọi trực tiếp. Đúng với thiết kế §10.2 (manifest tạm cho
worker gate). Trong lúc chạy gate (D) trên cây thật, hai tệp scratch của review (`BRIEF_REVIEW2.md`,
`LEASE_r4.yaml`, đã bị `.git/info/exclude` che khỏi `git status`) vẫn hiện diện trong cây — chúng
không ảnh hưởng tới rc của cả 5 cổng trên (đã kiểm: gọi trực tiếp `release-verify RELEASE_MANIFEST.json
--strict` với hai tệp đó còn nằm trong cây thì rc=2 vì `extra_files`, nhưng lệnh đó KHÔNG nằm trong
danh sách 5 cổng bắt buộc — nó đã được đo riêng, sạch, ở mục (C) sau khi loại hai tệp scratch).

## Trục 2 — quan sát bổ sung

1. Không phát hiện dấu hiệu manifest bị gõ tay: cấu trúc khoá (`ok, schema, skill, skill_version,
   webapp_target, root_name, file_count, total_bytes, package_hash, content_hash, required_missing,
   files, determinism_note`) đầy đủ, `determinism_note` còn nguyên câu gốc, và toàn bộ nội dung
   khớp byte-for-byte với bản do generator sinh lại — bằng chứng mạnh hơn soát cấu trúc bằng mắt.
2. Bản vá KHÔNG làm yếu `ok3`/`ok4`: mục (B) đã đo trực tiếp — mutate một số hạng thì ca ĐỎ đúng,
   nghĩa là ràng buộc vẫn siết đúng cả hai số hạng lẫn quan hệ giữa chúng.

## Mâu thuẫn doctrine `AG-DOCTRINE-03-manifest-worker-vs-land`

Đồng ý với cách xử của lease. Ba lý do, dựa trên đo thật chứ không chỉ đọc lời khai:

1. **Mâu thuẫn là có thật và đã đo được** (xem BẢNG ĐO) — §10.2 mô tả một kiến trúc DỰ ĐỊNH (manifest
   tạm, không so committed manifest), còn `ci.yml` dòng 480-481 thi hành khác: so trực tiếp
   `RELEASE_MANIFEST.json` committed trên MỌI PR bằng `--strict`. Đây không phải diễn giải sai của
   lease — đọc thẳng cả hai tệp cho cùng kết luận.
2. **Tiền lệ lịch sử nhất quán và đã kiểm được hướng đi**: ba commit `9c18f9e4`/`e8060a9c`/`b0923ac1`
   cùng một khuôn (sửa tệp trong gói ⇒ tái sinh manifest ⇒ merge sạch) — không phải suy diễn, là
   lịch sử `git log`. Một quyết định phá vỡ thực tế đang chạy (sửa `ci.yml` giữa chừng một packet
   nội dung nhỏ) rủi ro cao hơn giá trị nó mang lại cho ĐÚNG packet này.
3. **Phạm vi packet r4 là MỘT việc cơ học** (5 dòng, 1 tệp) — sửa `ci.yml`/`§10.2` là quyết định kiến
   trúc riêng, đúng như lease tự nhận và tự trỏ sang `CONG-NGOAI-WRITE-SET` (#361). Bắt r4 gánh việc
   đó là phá nguyên tắc "đúng một việc" mà chính packet này đang cố giữ (§12: đổi CÁCH LÀM chứ không
   vá thêm — nhưng đổi cách làm là việc của #361, không phải của một revision tái sinh manifest).

Không hạ nhẹ tay phần còn lại vì đồng ý điểm này: toàn bộ phản chứng (A)(B)(C)(D) đã chạy độc lập với
quyết định doctrine, và không cái nào phụ thuộc vào việc đồng ý hay không — nếu bất kỳ cổng nào trong
5 cổng đỏ, hoặc răng (B)/(C) không cắn, thì đã phải báo P1 bất kể lập trường doctrine.

**Khuyến nghị duy nhất, không chặn land**: ưu tiên packet `CONG-NGOAI-WRITE-SET` (#361) sớm — đây là
lần thứ hai đúng hình dạng lỗi này xảy ra trong CÙNG một packet (r1/r2 thiếu `tl_selftest.py`, r3
thiếu manifest), và §12 đã tự đòi xem lại cách làm ở lần thứ ba. Ghi nhận đây là quan sát, không phải
finding P2/P1 — lease đã tự đặt tên đúng nợ này (`AG-POLICY-01`, `HINH_DANG_LAP_LAI`).

## Kết luận

Không finding nào (P1/P2/P3) sống sót. Mọi khẳng định định lượng trong lease đã được ĐO LẠI ĐỘC LẬP,
không chỉ đọc lời khai — kể cả những cái "chắc chắn khớp" (BẢNG ĐO trên liệt kê cả cái khớp, không
chỉ cái lệch). Cả hai commit (r3 ratchet, r4 manifest) đúng phạm vi khai, đúng cơ chế khai (sinh chứ
không gõ), có răng thật (đột biến làm đỏ đúng chỗ), và không cổng nào khác vỡ theo. `approve`.
