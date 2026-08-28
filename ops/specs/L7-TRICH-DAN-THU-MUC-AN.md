# Đặc tả ĐÓNG BĂNG — `L7-TRICH-DAN-THU-MUC-AN` (Issue #378)

```yaml
schema_version: 1
packet_id: wp378
revision: 1
objective: >-
  Lớp L7 của `doc-claims-check` nhận đường dẫn bắt đầu bằng dấu chấm, và chỉ nhận
  ứng viên nằm TRONG kho sau resolve().
write_set:
  - type: exact
    path: scripts/tl_core/workflow.py
  - type: exact
    path: scripts/tl_selftest.py
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

## Điều kiện dừng

- `S1` cần đường dẫn thứ ba ngoài write set ⇒ DỪNG.
- `S2` vượt `≤6 tệp / ≤1000 dòng thêm+xoá` ⇒ DỪNG, khai.
- `S3` bản vá làm `./` hoặc `../` mất khỏi tầm quét ⇒ DỪNG. Đổi một lỗi lấy một lỗ hổng.
  Tiền lệ: bản vá vòng một của PR #123 dùng lookbehind phủ định trên lớp `[\w.\-/]` và
  làm đúng việc ấy; chính tác giả đo được và ghi lại.
- `S4` sau bản vá xuất hiện cờ L7 mới trên tài liệu thật ⇒ DỪNG, khai từng cái, xin quyết định.
- `S5` `origin/master` đã đi tiếp so `base_sha` mà chưa đo lại.

## Ghi chú trần kích thước — khai rõ, không lặng lẽ

Dùng trần `normal` (`≤6 tệp / ≤1000 dòng`) chứ không phải `≤3 tệp / ≤300 dòng` của ADR-0044.
Trần ADR-0044 gắn với packet chạm **authority** — ai được ghi, ai được duyệt, cái gì được land.
`doc-claims-check` gác trích dẫn trong tài liệu; nó không cấp lease, không quyết định land.
`scripts/tl_selftest.py` là tệp gộp 29.892 dòng nên ép 300 dòng là ép cắt bớt phép đo.
Người thi công thấy lập luận này SAI thì nói — đừng im lặng dùng trần rộng hơn.
