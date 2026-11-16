tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# Đặc tả packet — `REVIEW-VERDICT-SCHEMA-CHAT` (revision 2)

| trường | giá trị |
|---|---|
| `packet_id` | `REVIEW-VERDICT-SCHEMA-CHAT` |
| `packet_issue` | #1336 |
| `revision` | 2 |
| `nguon_cap_viec` | #387, các nợ D5–D7. Vòng hỏi `soan-spec` của phiên điều phối #1206 ngày 16-11-2026 chốt: Q1 (đây là P-C, chạy SAU P-B #1335) và Q6. Chủ kho trả lời "Đồng ý theo khuyến nghị". |
| `review_class` | `sensitive` (schema định danh reviewer và verdict) |
| `phu_thuoc` | P-B #1335 phải land trước, vì hai packet cùng chạm `.claude/dev/launcher_test.py`. Lease của packet này lấy base là master đã chứa merge của P-B. |

## 0. Vấn đề (đo 16-11-2026 04:5xZ, `jsonschema` 4.26.0 — đúng bản `ci.yml` ghim)

Tệp schema: `.github/coordination/schemas/review_verdict.v1.schema.json`.

1. **D5. Ký tự xuống dòng ở cuối chuỗi lọt qua `pattern`.** `jsonschema.validate('a'*40+'\n', {'pattern':'^[0-9a-f]{40}$'})`
   cho QUA. Lý do: validator Python khớp bằng `re.search`, mà `$` của `re` khớp được ngay trước một
   `\n` ở cuối chuỗi. Cùng lỗi áp cho mọi trường có `pattern` kết thúc bằng `$`: `packet_id`,
   `reviewed_sha`, `findings[].finding_id`. Thêm một lệch nữa: validator stdlib của `launcher_test.py`
   (`_schema_hop_le`, quanh dòng 7727) dùng `fullmatch`, nên **oracle của test chặt hơn validator thật**.
   Ca test vì thế xanh trong khi validator thật cho qua.
2. **D6a. `format` không được kiểm.** `"evidence_url": {"format": "uri"}` không có tác dụng, vì format checker
   tắt mặc định. Đo được: chuỗi `khong phai uri` vẫn QUA.
3. **D6b. Hai trường định danh không ràng nhau.** `provider` (`claude`, `codex`, `human`) không bị ràng với
   `model_reviewer_identity.provider` (`anthropic`, `openai`, `human`). Schema nhận cặp `codex` + `anthropic`.
4. **D7. Ca bí danh làm phồng số ca.** `r13_PROMPT_FILE_thieu_prompt_file_phai_DO` chỉ gọi lại
   `_t70_prompt_file_chan()`, helper của `t70`, và không có khẳng định riêng. Bảng đột biến cho
   `PROMPT_FILE_mo_coi_di_tiep` vẫn đòi giết cả hai, nên số ca (N/N) đếm một khẳng định hai lần.
5. **Ai đọc schema này (đo 16-11).** Trên master, ngoài các ca test, không có cổng nào validate verdict
   theo schema này lúc chạy. Mức nghiêm trọng vì vậy thấp: đây là hợp đồng chưa được cưỡng chế, không phải
   lỗ đang mở. Packet chỉ siết hợp đồng; nó **không** dựng cổng cưỡng chế mới.

## 1. `write_set`

```
.github/coordination/schemas/review_verdict.v1.schema.json
.claude/dev/launcher_test.py
```

## 2. `ngoai_pham_vi`

- Không dựng cổng mới để validate verdict lúc chạy. Nếu cần, đó là packet khác.
- Không đổi `schema_version`. Mọi verdict hợp lệ trước đây (SHA không có `\n`, URI hợp lệ, cặp provider
  đúng) phải vẫn hợp lệ; quét lại các verdict mẫu có trong kho để chứng minh (N4).
- Không sửa `launcher.py`.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Mọi `pattern` trong schema từ chối chuỗi có `\n` ở cuối, và hành vi giống nhau ở `jsonschema` (Python, `re.search`) lẫn ECMA-262. Gợi ý: SHA thì thêm `minLength`/`maxLength` 40; tên độ dài biến đổi thì kết bằng lookahead đầu cuối dùng được ở cả hai engine. Executor chọn cách cụ thể và ghi lý do. | schema |
| M2 | `evidence_url`: ràng buộc phải có hiệu lực **mà không cần bật format checker**, ví dụ thêm `pattern` `^https://` không chứa khoảng trắng và không có `\n` cuối, theo M1. Giữ `format: uri` để làm tài liệu. | schema |
| M3 | Ràng `provider` với `model_reviewer_identity.provider` bằng `allOf` + `if/then`: `claude`↔`anthropic`, `codex`↔`openai`, `human`↔`human`. | schema |
| M4 | Validator stdlib của `launcher_test.py` khớp **đúng ngữ nghĩa** validator thật: dùng `re.search` như `jsonschema` thay vì `fullmatch`, và hỗ trợ các keyword mới mà schema dùng (`allOf`, `if`, `then`, `minLength`, `maxLength`). Oracle không được chặt hơn hay lỏng hơn validator thật. | `launcher_test.py` |
| M5 | Ca test chạy qua CẢ HAI validator (stdlib của test và `jsonschema` 4.26.0 khi có cài) trên cùng một bảng: SHA + `\n` ⇒ từ chối; `packet_id` + `\n` ⇒ từ chối; `finding_id` + `\n` ⇒ từ chối; `evidence_url` `khong phai uri` ⇒ từ chối; `codex`+`anthropic`, `claude`+`openai` ⇒ từ chối; các cặp đúng ⇒ qua. Hai validator phải cho cùng kết quả trên mọi dòng của bảng. | `launcher_test.py` |
| M6 | D7: hoặc bỏ `r13` khỏi danh sách ca và khỏi bảng đột biến, hoặc cho `r13` một khẳng định riêng đo một thứ khác `t70`. Chọn một, ghi lý do. | `launcher_test.py` |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Bảng M5 xanh ở cả hai validator trên head. Trên **base**, dòng SHA + `\n` cho QUA ở `jsonschema`, nên ca ĐỎ (vế âm, chính là phép đo mục 0.1). | Đột biến: trả `pattern` SHA về `^[0-9a-f]{40}$` và bỏ ràng độ dài ⇒ ca đỏ ở dòng SHA. |
| N2 | Ca "hai validator đồng ý" trên bảng M5: đếm và in số dòng lệch theo **từng dòng** (L6c). Cộng thêm một ca **tuân thủ oracle** RIÊNG chạy trên một schema thử nghiệm có pattern KHÔNG neo (ví dụ `{"pattern": "abc"}` với `"xabcx"`: `search` khớp, `fullmatch` không). Hai validator phải cho cùng kết quả trên ca ấy. | Đột biến: oracle stdlib quay lại dùng `fullmatch` ⇒ ca tuân thủ oracle đỏ. Bảng M5 một mình không phát hiện được đột biến này sau khi schema đã siết, vì cả hai cách khớp cho cùng kết quả (finding P2 4582005794 trên PR #1333). |
| N3 | Dòng `codex`+`anthropic` bị từ chối. | Đột biến: xoá khối `allOf` ⇒ đỏ. |
| N4 | Mọi verdict JSON mẫu trong kho mà schema cũ nhận thì schema mới vẫn nhận, trừ những mẫu thật sự vi phạm. Liệt kê số mẫu đã quét, số mẫu qua, và từng mẫu bị từ chối kèm lý do. Đo trên cây head. | Một mẫu đúng bị từ chối oan. |
| N5 | `python -u .claude/dev/launcher_test.py` ra N/N, hai số bằng nhau. N bằng số ca nền lúc cấp lease, cộng ca mới, trừ `r13` nếu chọn bỏ. Bảng đột biến: mọi đột biến mới bị giết đúng lý do; `t117` xanh. | Ca đỏ hoặc số lệch. |
| N6 | `adr-song`, `doctrine-scan` rc 0; ruff `--select F` delta 0; CI Ubuntu xanh; gate hậu merge đủ bốn mốc. | — |

Windows: **không bắt buộc**. Schema và validator là logic thuần, không gọi API riêng của nền nào. CI
Ubuntu đủ.

## 5. Kích thước và trần

Dự kiến 2 tệp, khoảng 20–40 dòng schema và 80–150 dòng test. Trần `ADR-0053`: ≤ 6 tệp, ≤ 450 dòng thêm.

## 6. `luat_dung`

- Vượt trần `ADR-0053` ⇒ dừng; chủ kho quyết nâng trần (E2).
- Chạm trần lời gọi Codex theo `ADR-0055` (E2).
- P-B #1335 chưa land thì không cấp lease cho packet này. Phiên điều phối tự xếp thứ tự; đây không phải
  điểm hỏi chủ kho.

## 7. `pham_vi_e`

Không chạm E4, không chạm E5. Packet siết một hợp đồng schema, không đổi ai được review hay assurance nào
được cấp.

## 8. `hinh_dang_ke_thua`

Từ #387 (tám nợ có tên, sinh từ verdict `blocked` của #381). Hình dạng: **"oracle của test chặt hơn
validator thật"**. Ca xanh không chứng minh validator thật từ chối, cùng họ với "ca có MẶT khác ca có
ĐO" (CLAUDE.md). Đếm: lần 1 được ghi cho schema verdict.

## 9. `chua_do_duoc`

- Các engine JSON Schema khác (ECMA-262, như `ajv`) không có trong kho, nên không đo. M1 yêu cầu pattern
  đúng ở cả hai engine dựa trên ngữ nghĩa đã biết của ECMA-262, chưa chạy thật.
- Verdict do bên ngoài kho sinh ra (connector) không đi qua schema này. Ngoài phạm vi.

## 10. Thay đổi so với r1

r1: `ops/specs/REVIEW-VERDICT-SCHEMA-CHAT-r1.md`, sha256 `dc0d0ac59072f407c9d49af6841973ad9b8d2508ca3fa79a23c8fdbee8038bf8`. Chủ kho đã duyệt r1 nhưng chưa lease nào dùng nó.
r2 đóng finding P2 4582005794 của connector trên PR #1333 (head `99c8ee8`): sau khi pattern đã siết, đột biến
`search`→`fullmatch` không làm bảng M5 đổi màu. Phiên điều phối đo `re.search('abc','xabcx')` = True và
`re.fullmatch('abc','xabcx')` = False. Thay đổi: N2 thêm một ca tuân thủ oracle trên pattern không neo.
