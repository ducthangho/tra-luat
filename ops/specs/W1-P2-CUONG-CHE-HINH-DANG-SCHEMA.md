# ĐẶC TẢ ĐÓNG BĂNG — `W1-P2-CUONG-CHE-HINH-DANG-SCHEMA` — **BẢN 1**

Packet **nối tiếp** của `W1-P1-VAN-CHUYEN-PROMPT` (#368). Nhận bốn nợ mà cross-review vòng 4
tìm ra trên head `6edbd0463cbd7e09a281ac618053e819294e4720`, và W1-P1 **không được phép** vá vì
điều kiện dừng `S0`/`S2_DA_KICH_HOAT` của lease `w1-p1-van-chuyen-prompt-exec-4-codex-20260828`
đã đóng băng write set.

**GIỚI HẠN LỜI KHAI (kế thừa, không đổi):** chứng minh BYTE tới consumer adapter. KHÔNG tuyên bố
model "đã hiểu" nội dung prompt.

**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**. Trạng thái thứ ba làm cổng ĐỎ, không làm tròn lên.

---

## VÌ SAO CÓ PACKET NÀY

W1-P1 đóng ba tầng của cùng một bệnh — *"validator đọc thành ĐẠT một thứ nó không đo"*:

| vòng | tầng đã đóng |
|---|---|
| 2 | schema không khai `x-tra-luat-runtime-bindings` ⇒ trước đây bỏ qua sạch cưỡng chế semantic identity |
| 3 | schema khai đủ binding nhưng không khai HÌNH DẠNG (`type`/`required`/`additionalProperties`) |

Vòng 4 tìm ra **tầng thứ tư**, và nó nằm ngoài tầm với của W1-P1.

---

## Bốn nợ — nguyên văn, kèm phép đo đã chạy

### N1 (P1) — `schema-rut-ruot-properties-tang-4`

`_doi_schema_do_duoc_hinh_dang` (`review_verdict_binding.py`) chỉ đọc **BA khoá mục đỉnh**:
`type`, `additionalProperties`, `required`. Nó **không hỏi `properties` có ràng buộc gì không**.

Một schema giữ nguyên **cả ba chốt** mà rút từng sub-schema thành `{}` vẫn đi lọt. Phiên điều phối
tái lập ĐỘC LẬP, verdict để BỐN trường bị ràng buộc runtime đều ĐÚNG và mọi trường khác là rác:

```
giữ type/required/additionalProperties, 16 sub-schema -> {}
  -> NHẬN     verdict có independent_from_executor_session=False,
              verdict="xyz", assurance="bịa", schema_version là CHUỖI
ĐỐI CHỨNG schema GỐC, cùng verdict
  -> TỪ CHỐI  "verdict không qua jsonschema tại assurance: 'bịa' is not one of..."
```

### N2 (P2) — `ngoai-le-jsonschema-lot-thanh-cu-sap`

Khối `try` quanh `check_schema` + `iter_errors` chỉ bắt `jsonschema_exceptions.SchemaError`.
Một schema qua được `check_schema` nhưng hỏng lúc DUYỆT vẫn ném ngoại lệ khác — `$ref` treo cho
`jsonschema.exceptions._WrappedReferencingError`. Nó không phải `ReviewVerdictError` nên **sổng ra
ngoài** thành crash, không phải từ chối sạch.

### N3 (P3) — `oracle-r22-chuoi-schema-review-qua-rong`

Phép kiểm "chết đúng lý do" của `r22` là `if "schema review" not in str(e)`. Chuỗi ấy xuất hiện ở
**tám điểm ném KHÁC NHAU** trong `review_verdict_binding.py`. Oracle nay chấp nhận quá nhiều lý do
chết ⇒ vẫn còn cửa cho tín dụng giả, đúng họ bệnh mà `r22` sinh ra để chặn.

### N4 (P3) — `chot-nang-luc-tu-choi-schema-tuong-duong`

Bốn chốt mới **ĐÓNG NHẦM** hai schema hợp lệ:

- `type: ["object"]` — dạng mảng là JSON Schema hợp lệ và NGHĨA Y HỆT, nhưng `schema.get("type") != "object"` từ chối.
- `additionalProperties: {"not": {}}` — tương đương tuyệt đối với `false`, vẫn bị từ chối.

Đây là câu trả lời cho câu hỏi *"bốn chốt mới có đóng nhầm gì không"*: **có**.

---

## Write set — BA đường dẫn

```
.claude/dev/review_verdict_binding.py
.claude/dev/launcher_test.py
.claude/dev/packet_loop_test.py
```

**KHÔNG mở** `.github/coordination/schemas/review_verdict.v1.schema.json`, **KHÔNG** `launcher.py`,
**KHÔNG** `packet_loop.py`, **KHÔNG** `ops/lease_publish.py`, **KHÔNG** `duyet_danh_tinh.py`.

**Vì sao ba mà không bốn.** Packet này chạm authority (`review_verdict_binding.py` quyết định một
verdict có được nhận không), nên đọc theo vế NGHIÊM của ADR-0044: **≤ 3 tệp và ≤ 300 dòng THÊM**.
W1-P1 vừa trả giá cho việc không đọc vế ấy — nó dừng ở 4 tệp / +605 và kích hoạt `S2`. Không lặp lại.

Bốn nợ N1–N4 **không cái nào cần sửa schema**: cả bốn đều là lỗi của phía ĐỌC schema, không phải của
schema. Nợ cần đổi schema (`packet-id-khong-rang-buoc`) vì thế **KHÔNG** vào packet này.

---

## Mục nghiệm thu — mỗi mục kèm phép đo làm nó ĐỎ

**A1 (N1).** Schema giữ `type`/`required`/`additionalProperties` mà `properties` rỗng ràng buộc
⇒ `validate_review_verdict` **TỪ CHỐI**. Phép đo làm nó ĐỎ: chính bảng trên — verdict rác toàn tập
với bốn trường bị ràng buộc đúng, phải bị từ chối; và ĐỐI CHỨNG schema gốc + verdict hợp lệ phải NHẬN.

**A2 (N1) — end-to-end.** Cùng schema ấy đi qua `record-review` phải cho `rc=5` **và** state
byte-exact. Không có vế end-to-end thì A1 chỉ là chốt trong phòng thí nghiệm.

**A3 (N2).** Schema có `$ref` treo ⇒ `ReviewVerdictError`, **không** ngoại lệ nào khác sổng ra.
Phép đo làm nó ĐỎ: gỡ nhánh bắt mới ⇒ ca phải ĐỎ bằng ngoại lệ NGUYÊN THUỶ, không phải bằng
`ReviewVerdictError`.

**A4 (N3).** Oracle `r22` phải phân biệt được TÁM điểm ném. Phép đo làm nó ĐỎ: đột biến khiến
validator từ chối vì một lý do KHÁC (ví dụ "phải là JSON object") mà `r22` vẫn đếm là "chết đúng
lý do" ⇒ ca phải ĐỎ.

**A5 (N4).** `type: ["object"]` và `additionalProperties: {"not": {}}` phải được **NHẬN**, trong khi
`type: "array"`, `type: ["object","array"]` và `additionalProperties: true` vẫn phải bị **TỪ CHỐI**.
Phép đo làm nó ĐỎ: nới chốt thành "chấp nhận mọi thứ" ⇒ ba ca sau phải ĐỎ.

**A6 — không tầng rỗng.** Mọi chốt mới phải có ĐỘT BIẾN RIÊNG giết đúng ca đích của nó, và đối chứng
khác họ phải còn sống. Thêm chốt mà không ai gọi, hoặc thêm ca mà đột biến không giết được, là lặp
lại đúng P1-1 của W1-P1.

**A7 — ĐỐI CHỨNG KHÔNG ĐƯỢC ĐỘNG.** Toàn bộ hành vi đã đóng ở W1-P1 phải giữ nguyên: schema gốc +
verdict hợp lệ ⇒ NHẬN; schema gốc + sha sai ⇒ TỪ CHỐI; xoá bindings + sha sai ⇒ TỪ CHỐI; bỏ
`type`/`required`/`additionalProperties` ⇒ TỪ CHỐI.

---

## Nền phải ĐO LẠI trước khi bắt đầu

Tại `6edbd0463cbd7e09a281ac618053e819294e4720`, clone sạch (**KHÔNG worktree**), `git config core.abbrev 7`,
`PYTHONDONTWRITEBYTECODE=1` + `PYTHONPYCACHEPREFIX` ra ngoài cây:

```
launcher_test.py     165/165 ca (tổng 166, bỏ qua 1, hỏng 0)
packet_loop_test.py  TỔNG ĐẠT — nền 282/282, BỎ QUA 0; ca 282, ĐB 83, lách 78, oan 35, AC18 0
actionlint           rc=1, ĐÚNG 1 finding ops-don-ref.yml:117:9 SC1003 — ĐỎ SẴN, delta 0
```

**`actionlint` CẦN `shellcheck` TRÊN PATH.** Không có thì nó tự tắt tích hợp trong im lặng và trả
`rc=0 / 0 finding` — trông TỐT HƠN nền, thật ra không đo gì. W1-P1 đã vấp đúng chỗ này.

Đây là ĐO của phiên điều phối, **không phải chân lý** — executor phải tự đo lại.

---

## Nợ KHÔNG thuộc packet này — chép nguyên, đừng để rơi

- **`packet-id-khong-rang-buoc` (P2).** `cmd_record_review` đối chiếu `payload['provider']` và
  `payload['verdict']` với cờ CLI nhưng KHÔNG đối chiếu `payload['packet_id']` với `--packet`.
  Đo được: verdict khai `packet_id` của packet khác ⇒ `rc=0`, state đổi, packet → `accepted`.
  **Cần đổi CẢ schema** (thêm khoá binding) ⇒ packet riêng, cùng lượt với các binding P3 khác.
- **`allow-list-khoa-cung-nang-cap-schema` (P3).** Chốt "khoá lạ" từ chối mọi binding không nằm
  trong `BINDING_BAT_BUOC`. Nghĩa là thêm BẤT KỲ binding nào vào schema sẽ làm `record-review` từ
  chối MỌI verdict cho tới khi module được cập nhật. **Không nên "chữa" bằng cách nới lỏng** —
  fail-close + allow-list là đúng doctrine. Ràng buộc thật: schema và `review_verdict_binding.py`
  phải nằm CÙNG một write set và đổi trong CÙNG một commit. Đây là điều kiện thiết kế của packet
  `packet-id` ở trên.
- **`adapter-lech-cli-sau-khi-them-co-bat-buoc` (P2).** Lệnh nguyên văn trong `.claude/skills/cross-review/SKILL.md:297`
  nay `rc=2` — `--verdict-file` thành `required=True`. Fail-closed nên không nguy hiểm, nhưng đường
  ghi lại một lượt review DUY NHẤT được tài liệu hoá hiện không chạy được. Cần đường dẫn thứ TƯ
  (`SKILL.md`) ⇒ ngoài write set ba đường.

---

## Điều kiện DỪNG

- **S1** cần đường dẫn thứ TƯ ⇒ DỪNG, khai.
- **S2** vượt **300 dòng THÊM** hoặc **3 tệp** ⇒ DỪNG, khai. (Vế NGHIÊM của ADR-0044; W1-P1 đã trả giá.)
- **S3** `origin/master` đi tiếp mà CÓ chạm một trong ba đường write set ⇒ DỪNG.
- **S4** muốn sửa schema, `launcher.py` hoặc `packet_loop.py` ⇒ DỪNG, chúng thuộc packet khác.
- **S5** muốn khai một mục ĐẠT mà không có ca làm nó ĐỎ được ⇒ DỪNG.
- **S6** chạm trần **HAI vòng review** (ADR-0043) ⇒ DỪNG, không tự nâng. Nâng trần phải có khối
  `nang_tran` do người có thẩm quyền ký. W1-P1 đã vượt trần này mà không ai biết, vì bộ đếm
  `review_rounds_used` và cưỡng chế `nang_tran` **đều chưa tồn tại** (đo 28-08: 0 tệp cho cả hai).

---

## KHÔNG ĐO ĐƯỢC — kế thừa, chưa giải

- **Parity Windows** cho `6edbd04`. Bộ MCP GitHub đang dùng không có tool nào cho Actions/check-run,
  và `api.github.com` trả 403 theo-repo. Chưa đo, không suy đoán.
