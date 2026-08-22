# VERDICT — cross-review lượt 2 của `PLAT-X8` (#225 / PR #248), reviewer `claude`

`reviewed_sha` **`86a556632f8464de06262efcc2aa7c0e88415f0e`** · executor `codex` · verdict **`approved`** *(về kỹ thuật — xem giới hạn ngay dưới)*

## ĐỌC TRƯỚC: verdict này KHÔNG mang assurance

**`la_canonical: false`.** Ba lý do độc lập, mỗi lý do đủ một mình:

1. **Không có lease `role: reviewer`** — lượt này lại chạy dưới lease executor, y như lượt 1. Không cấp lease lùi ngày.
2. **Biên nhận không qua validation.** `PROTOCOL:460-464`: *"`schema_version: 1` do tác giả tệp MỚI tự khai KHÔNG tạo miễn trừ"*; miễn trừ chỉ neo allowlist đóng băng 11 tệp. Nâng lên v2 đòi receipt ID + **hai danh tính chứng thực độc lập** — phiên này không có, và bịa ra là **giả mạo hồi tố**. ⇒ `PROTOCOL:758-760`: lượt này **KHÔNG tăng `review_rounds_used`**.
3. **Người review là người soạn đặc tả** — verdict KHÔNG bảo chứng tính đúng của đặc tả.

**Hệ quả phải nói thẳng: `PLAT-X8` vẫn còn NGUYÊN hai vòng canon.** Cả hai lượt review claude tới nay đều là **dữ liệu tìm lỗi**, không phải vòng canon. Con số *"canon 1/2"* ở các bản ghi trước là SAI, đã đính chính.

## Hai P1 của lượt 1 — ĐÃ ĐÓNG, đo trên exact head

| ca đo | trước vá | **sau vá** |
|---|---|---|
| `docs/adr/../../ops/lease_publish.py` | `systemic` ⚠ | **`sensitive`** ✓ |
| `planned:docs/adr/../../ops/lease_publish.py` | `systemic` ⚠ | **`sensitive`** ✓ |
| `planned:ops/lease_publish.py` *(đối chứng — không được từ chối oan)* | `sensitive` | **`sensitive`** ✓ |
| `docs/adr/0045-x.md` *(đối chứng — không được nâng oan)* | `systemic` | **`systemic`** ✓ |

`schema_version`, `write_set` `sensitive` khai `routine`:

```
2 · '2'                              -> CHẶN   ✓
1 · '1' · vắng mặt                   -> QUA    ✓  (legacy CÓ CHỦ Ý)
'v2' 2.0 '2.0' 'abc' None [] {} True -> CHẶN   ✓  (tám giá trị, kể cả bool)
```

**`True` bị loại là chỗ đáng khen**: `bool` là lớp con của `int` trong Python, nên một bản vá chỉ kiểm `isinstance(x, int)` sẽ để `True` lọt thành `schema_version: 1`. Executor bắt được mà finding không nêu.

## P1-3 mới · `thu-muc-tran-doi-lop` — hệ quả CHƯA AI KHAI, không phải lỗ

Đo cả hai phía:

| | trước vá | sau vá |
|---|---|---|
| `docs/adr/` *(có `/` cuối)* | `systemic` | **`sensitive`** |
| `docs/adr` *(không `/`)* | `sensitive` | `sensitive` |

**Trước vá, cùng một thư mục cho hai lớp khác nhau chỉ vì dấu `/`** — đúng hình dạng *"phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN"* (`v1.36.68`). Chuẩn hoá xoá chỗ lệch và gộp về **fail-closed**. Không phải lỗ; nhưng là **đổi hành vi chưa ai khai**, và một cổng phân lớp thì mọi đổi hành vi phải có vết.

### Gợi ý theo `PROTOCOL §441-451` — bốn phần

| phần | nội dung |
|---|---|
| **vá ở đâu** | **KHÔNG vá.** Khai thành nợ là gợi ý hợp lệ theo §441, và đây là ca ấy |
| **vá thế nào** | Nếu muốn `docs/adr/` khớp mục prefix `docs/adr/`, phải nối lại `/` sau chuẩn hoá cho mục thư mục. **Đắt hơn giá trị**: nó dựng lại đúng chỗ phân biệt cách viết mà bản vá vừa xoá, và mở lại câu hỏi *"đường nào là thư mục"* — thứ `write_set` không khai |
| **ca test khoá nó** | Nếu ai đó chọn vá: ca đòi `docs/adr/` ⇒ `systemic` **và** `docs/adr` ⇒ `systemic` (hai cách viết PHẢI cùng lớp — đó mới là bất biến đáng khoá, không phải giá trị cụ thể). Đột biến: bỏ bước nối `/` ⇒ ca ĐỎ |
| **có thể đẻ ra gì** | Nâng oan một `write_set` khai cả thư mục lên `sensitive` ⇒ đòi assurance cao hơn cần. Đo được rủi ro hôm nay: **0 lease nào** trong 136 blob khai một mục thư mục trần trong `write_set` |

## Nghiệm thu — đo, `rc` đọc trực tiếp

| chốt | kết quả |
|---|---|
| write set | **đúng hai tệp** `ops/lease_publish.py` · `ops/lease_publish_test.py` |
| trần `ADR-0044` | **313 dòng thêm** — khớp CHÍNH XÁC `ngoai_le_ADR_0044` của lease `…-2r4` phủ. Chủ kho duyệt 13 dòng vượt |
| `A9` | `rc=0`, **85/85**, hai số BẰNG NHAU, ≥ sàn **73** |
| **`A12`** | `workflow_dispatch` run `32587850266` trên exact head — `gate (ubuntu-latest)` **success 31 bước 0 hỏng** · `gate (windows-latest)` **success 31 bước 0 hỏng**. Đo **theo job** |
| tự quy chiếu, vế DƯƠNG | cổng MỚI lên chính lease `…-2r4` ⇒ **`rc=0`** |
| tự quy chiếu, vế ÂM | hạ `effective_review_class` `sensitive→systemic` ⇒ **`rc=10`** |
| quét lease lịch sử | 136 blob · 129 dùng `schema 1` · 7 dùng `2` · **KHÔNG giá trị hỏng** ⇒ bản vá fail-closed không giết lease cũ nào |
| P2 `commit-message-mot-dong` | **ĐÃ VÁ** — thông điệp mới có phép đo, đột biến, và ngoại lệ trần kèm người duyệt |

> ⚠ **Con số 136 và 313 hết hạn khi có lease mới hoặc commit mới.** Thứ giữ chúng là `t23` (mọi lease thật phải qua cổng) và một phép đo lại, không phải hai con số này.

## Còn mở

- `ADR-0045` **(e) human readback trước land** — chưa xong, thuộc lượt LAND.
- **`ngoai_le_ADR_0044` KHÔNG cổng nào canh** (`lease_publish.py` không đọc số dòng). Preflight thủ công. Người land phải TỰ ĐO `git diff --shortstat` và đối chiếu **313**; lệch lên trên ⇒ ngoại lệ không phủ.
- Nợ `PLAT-X8-CHUA-CO-BO-KIEM-RECEIPT`: hai bộ kiểm mà cross-review đề nghị (đỏ mọi receipt mới tự khai v1; đỏ finding thiếu phần §441) là **máy móc mới, ngoài write set** — khai nợ thay vì lặng lẽ dựng.
