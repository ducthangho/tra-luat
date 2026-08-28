# Đặc tả ĐÓNG BĂNG — `L7-TRICH-DAN-THU-MUC-AN` (Issue #378), **bản sửa đổi 2**

```yaml
schema_version: 1
packet_id: wp378
revision: 2
objective: >-
  Lớp L7 của `doc-claims-check` nhận đường dẫn bắt đầu bằng dấu chấm, và chỉ nhận
  ứng viên nằm TRONG kho sau resolve().
write_set:
  - type: exact
    path: scripts/tl_core/workflow.py
  - type: exact
    path: scripts/tl_selftest.py
  - type: exact
    path: RELEASE_MANIFEST.json
depends_on: []
executor: codex
environment: cloud
risk: normal
review_class: sensitive
effective_review_class: sensitive
```

## Triệu chứng — đo bằng công cụ thật

`scripts/tl_core/workflow.py:1123` trên `master` `d4b3045a6e5ec7daf4a9ebfacb405153de04fc99`:

```
_DOC_CLAIMS_PYLOC_RE = re.compile(r"\b([A-Za-z0-9_][A-Za-z0-9_./\-]*\.py):(\d+)\b")
```

Ký tự đầu buộc là chữ/số ⇒ dấu chấm bị cắt. `python3 scripts/tl.py doc-claims-check --strict --json --path TỆP`:

```
A: `.claude/dev/launcher.py:1`      → PYLOC_FILE_MISSING   claim="claude/dev/launcher.py:1"
D: `.github/checks/ci_phamvi.py:1`  → PYLOC_FILE_MISSING   claim="github/checks/ci_phamvi.py:1"
B: `./scripts/tl.py:99999999`       → PYLOC_LINE_OUT_OF_RANGE     (ĐÚNG, phải giữ)
C: `../scripts/tl.py:99999999`      → PYLOC_LINE_OUT_OF_RANGE     (ĐÚNG, phải giữ)
E: `khong_co_that.py:3`             → PYLOC_FILE_MISSING          (ĐÚNG, phải giữ)
```

`A` và `D` là tệp CÓ THẬT. Chuỗi `claim` in ra khác chuỗi trong tài liệu.

## Nền đo được — phải so DELTA, không so tuyệt đối

```
python3 scripts/tl.py doc-claims-check --strict --json
  ok: true · files_scanned: 106 · L7: 0 · flags: 0 · advisories: 359
```

Lỗi này TIỀM ẨN. Không tệp `.md` nào trích dẫn `.claude/**.py` kèm số dòng — và đó không phải
may mắn: `CLAUDE.md` (trong danh sách quét) nhắc `.claude/dev/launcher.py` ở dòng 268, 325,
430, 532 và **luôn không kèm số dòng**. Cổng đang dạy tài liệu viết kém chính xác hơn.

## VÌ SAO CÓ BẢN SỬA ĐỔI 2 — đặc tả bản 1 KHÔNG THỂ XANH

Bản 1 khoá write set ở đúng hai tệp và viết thẳng *"KHÔNG sửa bất kỳ tệp `.md` nào"* cùng
`S1` cấm đường dẫn thứ ba. Đo được sau khi lượt 1 chạy xong:

```
gate (ubuntu-latest) run 33160410378  FAILURE
  bước ĐỎ: "release-verify strict (manifest khớp cây)"

package_hash_expected  298108fed28af6a6f2fa4ed69b3028b9950f058c535bc7258f8833fe5fe59cd8
package_hash_current   3416357457db806c6e32efbb17310831d990ff6dec94a817ebb27d8173fd8386
package_hash_match     false
```

**Cả hai tệp write set đều nằm trong gói phát hành 180 tệp**, nên đụng vào chúng BẮT BUỘC
phải sinh lại `RELEASE_MANIFEST.json`. Đặc tả bản 1 vừa đòi sửa chúng vừa cấm sinh lại
manifest — một hợp đồng **tự mâu thuẫn**, không phải người thi công làm sai. `§3.2`: finding
cho thấy chính spec thiếu thì đi qua revision mới. Đây là revision ấy.

Việc còn lại của lượt 2 **chỉ có một**, và nó cơ học:

```console
$ python3 scripts/tl.py release-manifest --out RELEASE_MANIFEST.json --json
```

Điều phối đã đo thử trên bản sao ngoài cây: đúng **7 dòng** đổi — `total_bytes`,
`package_hash`, `content_hash`, và cặp `size`/`sha256` của đúng hai tệp write set.
**Đo lại, đừng nhận con số này.**

## BA CON SỐ "ĐỎ" CỦA LƯỢT 1 LÀ ẢO — đọc trước khi hoảng

Workspace thi công được điều phối tạo bằng **fetch từng phần**, nên thiếu object git cũ.
Hệ quả, A/B ba cây cùng một lệnh:

```
                        golden-test   selftest      doc-claims flags
cây SẠCH tại base         rc=2        1696/1698     5 (L2 SHA_NOT_A_COMMIT)
cây ĐÃ VÁ                 rc=2        1703/1705     5
clone ĐỦ OBJECT           rc=0        1705/1705     0
```

Cây **sạch** cũng đỏ ⇒ **không phải bản vá**. Con số thật trên clone đủ object là
`selftest 1705/1705 rc=0`, `golden-test rc=0`, `doc-claims flags 0`.

Nếu lượt 2 gặp lại ba con số ấy: **đó là môi trường, không phải hồi quy**. Vẫn khai ra,
nhưng đừng vá gì để chữa chúng.

## acceptance_criteria

1. `.claude/dev/launcher.py:1` ⇒ KHÔNG cờ.
2. `.github/checks/ci_phamvi.py:1` ⇒ KHÔNG cờ.
3. `.claude/dev/launcher.py:99999999` ⇒ `PYLOC_LINE_OUT_OF_RANGE`.
4. `.claude/khong_co_that.py:3` ⇒ `PYLOC_FILE_MISSING`.
5. `claim` trong JSON khớp TỪNG BYTE chuỗi trong tài liệu, kể cả dấu chấm đầu.
6. Ứng viên sau `resolve()` phải nằm TRONG kho; ra ngoài ⇒ không phải ứng viên.
7. HỒI QUY: `./scripts/tl.py:99999999` và `../scripts/tl.py:99999999` VẪN ra
   `PYLOC_LINE_OUT_OF_RANGE`. Có đột biến riêng cho ca này.
8. Mỗi chốt 1–7 có ca test riêng VÀ đột biến riêng làm đúng ca ấy ĐỎ.
9. Bảng BA HẠNG đột biến: giết thật / tín dụng giả / sống sót. Mutant chết vì ngoại lệ vô can
   KHÔNG được tính là giết. Tín hiệu "assertion của ca đích" phải là thứ mã triển khai
   không giả được.
10. Đo nền trước, so DELTA sau trên toàn kho. Cờ L7 MỚI xuất hiện ⇒ đó là phát hiện THẬT,
    phải KHAI. Không nới ca test, không sửa tài liệu cho cổng xanh.
11. **(bản 2)** `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`
    ⇒ `rc=0` và `package_hash_match: true`.
12. **(bản 2)** `RELEASE_MANIFEST.json` chỉ đổi những dòng do bản vá gây ra. Khai `git diff
    --numstat` cho tệp ấy. Đổi `skill_version`, `expected_file_count`, hay bất kỳ trường nào
    KHÔNG phải hệ quả của hai tệp write set ⇒ DỪNG và khai.
13. **(bản 2)** `python3 scripts/tl.py release-bundle` hai lần cho **cùng** SHA-256.

## Điều kiện dừng

- `S1` cần đường dẫn thứ ba ngoài write set ⇒ DỪNG.
- `S2` vượt `≤6 tệp / ≤1000 dòng thêm+xoá` ⇒ DỪNG, khai.
- `S3` bản vá làm `./` hoặc `../` mất khỏi tầm quét ⇒ DỪNG. Đổi một lỗi lấy một lỗ hổng.
  Tiền lệ: bản vá vòng một của PR #123 dùng lookbehind phủ định trên lớp `[\w.\-/]` và
  làm đúng việc ấy; chính tác giả đo được và ghi lại.
- `S4` sau bản vá xuất hiện cờ L7 mới trên tài liệu thật ⇒ DỪNG, khai từng cái, xin quyết định.
- `S5` `origin/master` đã đi tiếp so `base_sha` mà chưa đo lại.
- `S6` **(bản 2)** sinh lại manifest làm đổi thêm trường ngoài hệ quả của hai tệp write set
  ⇒ DỪNG, khai. Manifest là artefact phái sinh; nó phải phản chiếu cây, không được mang
  quyết định nào của riêng lượt này.
- `S7` **(bản 2)** phải sửa `CHANGELOG.md` hay bất kỳ tệp thứ tư nào để cổng xanh ⇒ DỪNG.
  Bản 2 mở write set đúng MỘT tệp, không mở thêm.

## Ghi chú trần kích thước — khai rõ, không lặng lẽ

Dùng trần `normal` (`≤6 tệp / ≤1000 dòng`) chứ không phải `≤3 tệp / ≤300 dòng` của ADR-0044.
Trần ADR-0044 gắn với packet chạm **authority** — ai được ghi, ai được duyệt, cái gì được land.
`doc-claims-check` gác trích dẫn trong tài liệu; nó không cấp lease, không quyết định land.
`scripts/tl_selftest.py` là tệp gộp 29.892 dòng nên ép 300 dòng là ép cắt bớt phép đo.
Người thi công thấy lập luận này SAI thì nói — đừng im lặng dùng trần rộng hơn.
