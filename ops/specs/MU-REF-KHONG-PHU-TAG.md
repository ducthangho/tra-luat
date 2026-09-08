# Đặc tả packet — MU-REF-KHONG-PHU-TAG (revision 1)

Đặc tả ĐÓNG BĂNG. Lease neo vào `spec_hash` = sha256 của chính tệp này.

## `nguon_cap_viec`

Chỉ thị chủ kho trong phiên `session_01C52eS8AgeiwTrDifXGDGYP` (2026-09-08): xử lý hai nội dung
phát hiện khi đo, mở PR ở phiên riêng, cấp lease và thực thi. Nội dung (a) là packet này.

## Bối cảnh đo được (mọi số kèm thời điểm và lệnh)

### Phép canh mù của kho CHỈ phủ `refs/heads`

`CLAUDE.md` (mục "`git for-each-ref` ĐỌC BỘ ĐỆM CỤC BỘ") quy định phép canh mù bằng cách so
HAI NGUỒN, và chép sẵn lệnh:

```
git ls-remote --heads origin | sed 's#.*refs/heads/##' | sort            > /tmp/mc
git for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin \
    | grep -v '^HEAD$' | sort                                           > /tmp/cb
comm -23 /tmp/mc /tmp/cb
```

Cả hai vế đều **chỉ đọc `refs/heads`**. `refs/tags` không xuất hiện ở vế nào.

### Hậu quả đo được — 2026-09-08, container remote của phiên trên

Chạy đúng lệnh doctrine trên kho vừa fetch: **307 máy chủ / 307 cục bộ, `MU = 0`** ⇒ doctrine
tuyên SẠCH.

Đo thêm namespace tag trên CÙNG kho, CÙNG thời điểm:

```
git ls-remote --tags origin | sed 's#.*refs/tags/##' | sed 's#\^{}$##' | sort -u   > /tmp/mct
git for-each-ref --format='%(refname:lstrip=2)' refs/tags | sort -u                > /tmp/cbt
comm -23 /tmp/mct /tmp/cbt
```

⇒ **62 tag máy chủ / 39 tag cục bộ / 23 tag MÙ.**

Trong 23 tag mù: **20** thuộc `luu-tru/*`, cộng `archive/dlbrut-ke-hoach-dau` ·
`bak/pre-renumber` · `rescue/d0-2026-08-04`.

Điều làm nó nghiêm trọng, và chính `CLAUDE.md` nói: *"`luu-tru/*` là ref BỀN duy nhất giữ các
commit công bố verdict sau khi nhánh `ops/**` bị xoá"*. Tức phép canh mù bỏ sót **đúng loại ref
giữ verdict đã công bố** — 20/23 tag mù thuộc chính loại ấy.

### Nó làm một cổng cho kết quả KHÁC NHAU, và `rc` KHÔNG phân biệt

Đối chiếu cổng nền↔sandbox của cross-review #478 lượt 4:

| vế | `rc` | kích thước stdout |
|---|---:|---:|
| kho nền (thiếu 23 tag) | **0** | **70861 B** |
| sandbox (đủ tag) | **0** | **70854 B** |

`rc` BẰNG NHAU ở cả hai vế; chỉ nội dung lệch, đúng **7 byte**, tại một dòng:

```
-      "reason": "SHA_NOT_A_COMMIT_IN_HISTORICAL_DOC"
+      "reason": "SHA_NOT_REACHABLE_FROM_HEAD"
```

Nguyên nhân đã truy tới object: SHA `1835b46` (trích trong
`docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md:39`) chỉ tra được qua tag
`archive/dlbrut-ke-hoach-dau`. Trên kho thiếu tag: `git cat-file -t 1835b46` ⇒
`fatal: Not a valid object name`. Trên kho đủ tag ⇒ `commit`.
Sau khi fetch đủ tag, đối chiếu lượt 5 cho `70854 = 70854`, **khớp từng byte**.

Vậy: một kho "sạch" theo phép canh của kho vẫn có thể phân loại SAI khả-tra của một SHA, và
`rc` không hề đổi. Đây đúng lớp lỗi `CLAUDE.md` đã ghi — *cổng VẮNG MẶT trông giống cổng XANH* —
đổi đối tượng sang **một namespace ref không được canh trông giống một kho đầy đủ**.

## `review_class`

`sensitive` — packet chạm `CLAUDE.md`, tệp doctrine gốc.

## `write_set`

```
CLAUDE.md
ops/kiem_mu_ref.py
ops/kiem_mu_ref_test.py
```

Đo `ai-dang-giu` trên cả ba đường, 2026-09-08: **`NGƯỜI_GIỮ 0`** (các dòng `HẾT_HẠN` thuộc nợ
`AG-T0-01B`, không chặn).

## `ngoai_pham_vi`

- **KHÔNG sửa `.claude/skills/cross-review/SKILL.md`.** Tệp ấy chép cùng đoạn `comm` chỉ phủ
  `--heads` và vì thế mang cùng khuyết tật, nhưng nó thuộc write set của packet
  `VERDICT-KHONG-BOC-HOI` chạy song song. Nợ có tên: `SKILL-MD-COMM-CHI-PHU-HEADS`, do packet
  ấy đồng bộ. Đụng vào đây là chồng lấn write set.
- KHÔNG sửa `ops/lease_publish.py` (`_cac_ref_cuc_bo`, banner `ai-dang-giu`). Banner in
  "quét refs/heads/*" trong khi mã đọc cả `refs/remotes` — đã ghi ở `ops/dung_goi_review.sh`.
  Đó là nợ nhãn riêng, không thuộc packet này.
- KHÔNG đổi `ops/dung_goi_review.sh`. `EVIDENCE.md` của nó đã TỰ KHAI "Chi phu `refs/heads`.
  KHONG co anh chup tag hay namespace khac" — lời khai ấy ĐÚNG, không phải lỗi.
- KHÔNG tự fetch/ghi ref trong bộ kiểm. Nó chỉ ĐO và báo; việc chữa do người gọi quyết.

## `muc_tieu`

1. Một bộ kiểm CHẠY ĐƯỢC trong kho (`ops/kiem_mu_ref.py`) so hai nguồn trên **cả hai** namespace
   `refs/heads` và `refs/tags`, theo TẬP TÊN (không theo `wc -l`).
2. **BA trạng thái, không phải hai**: `đủ` · `mù` · `KHÔNG ĐO ĐƯỢC`. Trạng thái thứ ba làm cổng
   ĐỎ — `ls-remote` hỏng/không mạng thì fail-close, đúng doctrine `None ≠ False`.
3. `CLAUDE.md` sửa đoạn doctrine để phủ tag, và nói thẳng vì sao (`luu-tru/*` giữ verdict).
4. Phản chứng chạy được cho từng chốt.

## `nghiem_thu` — mọi tiêu chí NÊU ĐƠN VỊ

| # | tiêu chí | đơn vị / ngưỡng |
|---|---|---|
| A1 | `python3 -B ops/kiem_mu_ref_test.py` | `N/N đạt` với **hai số BẰNG NHAU**, `bỏ qua = 0`, `rc = 0` |
| A2 | số ca test tối thiểu | **≥ 8** ca |
| A3 | ca "thiếu tag ⇒ ĐỎ" | mã thoát **≠ 0**, stdout nêu **đúng số tag mù** (số nguyên) |
| A4 | ca "thiếu head ⇒ ĐỎ" | mã thoát **≠ 0** |
| A5 | ca "đủ cả hai ⇒ XANH" | mã thoát **= 0** |
| A6 | ca "`ls-remote` lỗi ⇒ KHÔNG ĐO ĐƯỢC" | mã thoát **≠ 0** và **≠** mã của ca mù; stdout chứa `KHÔNG ĐO ĐƯỢC` |
| A7 | ca "thừa cục bộ (ref đã xoá trên máy chủ)" | mã thoát **= 0** — thừa là vô hại, không được báo mù |
| A8 | ca "lực lượng BẰNG NHAU mà TẬP LỆCH" | mã thoát **≠ 0** — chốt chống đếm bằng `wc -l` |
| A9 | đột biến: đổi phép so tập thành so số đếm | ca A8 phải **ĐỎ**; không đỏ thì ca A8 chưa đo cái nó khai |
| A10 | đột biến: bỏ nhánh `refs/tags` | ca A3 phải **ĐỎ** |
| A11 | đột biến: biến `KHÔNG ĐO ĐƯỢC` thành `đủ` | ca A6 phải **ĐỎ** |
| A12 | chạy trên kho thật, đủ ref | `rc = 0`, báo `head: 309/309` và `tag: 62/62` (số đúng tại lúc đo, ghi kèm mốc) |
| A13 | `python3 -B ops/lease_publish_test.py` | `121/121 đạt; đã chạy=121, bỏ qua=0`, `rc = 0` |
| A14 | `python3 -B ops/bien_nhan_v2.py` | `0 vi phạm`, `TỔNG: ĐẠT`, `rc = 0` |
| A15 | `python3 scripts/tl.py doc-claims-check --strict` | `rc = 0`, `ok: true` |
| A16 | `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | `rc = 0` |
| A17 | cột THÊM của `git diff --numstat` | **≤ 400** dòng (ADR-0044 đo additions) |
| A18 | `shellcheck` / `actionlint` | không áp — packet không chạm `.sh` hay workflow |

**A9–A11 là chốt răng**: mỗi đột biến phải làm ca ĐÍCH đỏ. Đột biến bị giết vì lỗi VÔ CAN
(`TypeError`, `AttributeError`) là **TÍN DỤNG GIẢ**, không tính — theo bài học `#355`/`#359`.

## `dieu_kien_dung`

- Bộ kiểm TỰ FETCH để "chữa" cái mù — nó phải ĐO và BÁO, không tự sửa trạng thái đang đo.
- So bằng `wc -l` ở bất kỳ đâu — doctrine cấm, và A8 sinh ra để bắt đúng việc ấy.
- Gộp `KHÔNG ĐO ĐƯỢC` vào `mù` hoặc vào `đủ` — ba trạng thái phải phân biệt được bằng mã thoát.
- Sửa `.claude/skills/cross-review/SKILL.md` — chồng lấn write set (xem `ngoai_pham_vi`).
- Chép doctrine từ `CLAUDE.md` sang adapter — `doctrine-scan` sẽ đỏ.
- Đổi ngưỡng/nội dung `doc-claims-check` để làm số 7 byte biến mất. Con số ấy là BẰNG CHỨNG,
  không phải lỗi cần dọn.

## `chua_do_duoc`

- **Vì sao 23 tag ấy chưa từng được fetch** trong container này: không có log fetch gốc.
  Chỉ đo được TRẠNG THÁI (thiếu), không đo được LỊCH SỬ. Đừng ghi một nguyên nhân vào doctrine.
- Có bao nhiêu phiên khác đang chạy trên kho thiếu tag: KHÔNG ĐO ĐƯỢC từ một container.
- Liệu còn namespace thứ ba (`refs/pull`, `refs/notes`) cũng cần canh: mirror của kho có
  **324** `refs/pull`, nhưng chưa có phép đo nào cho thấy thiếu chúng gây kết luận sai. Ghi làm
  câu hỏi mở, KHÔNG mở rộng phạm vi packet theo phỏng đoán.
