# wp55 r3g4 · DANH SÁCH ĐÓNG các lớp lách — AC 18 + AC 21

**Xuất TRƯỚC khi sửa dòng mã đầu tiên.** Mọi `rc` dưới đây đo trên entrypoint
CHƯA VÁ tại head `546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f`.

Lệnh đo:

```bash
python3 probe_doctrine.py .claude/dev/packet_loop.py   # chiều LỌT
python3 probe_oan.py      .claude/dev/packet_loop.py   # chiều BẮT OAN
python3 probe_lease.py    .claude/dev/packet_loop.py   # lược đồ lease
```

---

## A · doctrine-scan — chiều LỌT (40 ca, đạt 22/40, **18 LỌT**)

| id | lớp | phép thử (bơm vào `.claude/skills/**/SKILL.md`) | rc đo được | đòi | bị bắt nhờ đâu | tầng chữa |
|---|---|---|---|---|---|---|
| A0 | nền | `merged: PR đã vào nhánh đích` | 6 | 6 | nền có đáy | — |
| Z0 | nền | adapter sạch | 0 | 0 | nền không bắt oan | — |
| A1 | NFKC | hai chấm TOÀN RỘNG `U+FF1A` | **0 LỌT** | 6 | P1-A spec | NFKC |
| A2 | NFKC | chữ TOÀN RỘNG `ｍｅｒｇｅｄ` | **0 LỌT** | 6 | P1-A spec | NFKC |
| A3 | NFKC | chữ số TRÒN `③ attempt/packet` | **0 LỌT** | 6 | danh sách này | NFKC |
| A4 | NFKC | chữ số MŨ `³ attempt/packet` | **0 LỌT** | 6 | danh sách này | NFKC |
| A5 | NFKC | ligature `ﬀ` `U+FB00` trong `eﬀective` | 6 | 6 | — (NFC đã gộp) | NFKC |
| A6 | NFKC | solidus TOÀN RỘNG `U+FF0F` | **0 LỌT** | 6 | danh sách này | NFKC |
| A7 | NFKC | gạch dưới TOÀN RỘNG `U+FF3F` | **0 LỌT** | 6 | danh sách này | NFKC |
| A8 | NFKC | vạch đứng TOÀN RỘNG `U+FF5C` | **0 LỌT** | 6 | danh sách này | NFKC |
| A9 | NFKC | khoảng trắng KHÔNG NGẮT `U+00A0` | 6 | 6 | — | gộp phân cách |
| B1–B6 | `Cf` | ZWSP · ZWNJ · ZWJ · WORD JOINER · soft hyphen · BOM | 6 ×6 | 6 | vá r2 | lọc `Cf` (giữ) |
| C1 | entity | thập phân `&#58;` | 6 | 6 | vá r2 | unescape ×1 (giữ) |
| C2 | entity | thập lục `&#x3A;` | 6 | 6 | — | unescape ×1 |
| C3 | entity | có tên `&colon;` | 6 | 6 | — | unescape ×1 |
| C4 | entity | thiếu `;` — `&#58` | 6 | 6 | — | unescape ×1 |
| C5 | entity | **LỒNG** `&amp;#58;` → render `&#58;`, **PHẢI THA** | 0 | 0 | vá r2 | KHÔNG giải lặp |
| D1 | đồng tự | Cyrillic `е` `U+0435` trong `merged` | **0 LỌT** | 6 | danh sách này | gấp đồng tự |
| D2 | đồng tự | Cyrillic `о` `U+043E` trong `local controller` | **0 LỌT** | 6 | danh sách này | gấp đồng tự |
| D3 | đồng tự | Hy Lạp `ο` `U+03BF` | **0 LỌT** | 6 | danh sách này | gấp đồng tự |
| D4 | đồng tự | Cyrillic `а` `U+0430` trong `paused` | **0 LỌT** | 6 | danh sách này | gấp đồng tự |
| E1 | nháy | nháy cong BAO QUANH cụm | 6 | 6 | — | — |
| E2 | nháy | nháy đơn cong XEN GIỮA `mer’ged` | **0 LỌT** | 6 | danh sách này | bỏ nháy |
| F1 | dash | mũi tên DÀI `U+27F6` thay `→` | **0 LỌT** | 6 | danh sách này | gấp mũi tên |
| F2 | dash | en-dash thay `_` trong `same_failure_limit` | **0 LỌT** | 6 | danh sách này | gộp phân cách |
| G1 | markdown | nhấn mạnh GIỮA TỪ `mer*g*ed` | 6 | 6 | vá r1 | bỏ trang trí (giữ) |
| G2 | markdown | tag HTML xen giữa `mer<b>ged</b>` | **0 LỌT** | 6 | danh sách này | bỏ tag HTML |
| G3 | markdown | comment HTML xen giữa `mer<!-- x -->ged` | **0 LỌT** | 6 | danh sách này | bỏ comment HTML |
| G4 | markdown | link/anchor `[merged](#a)` | **0 LỌT** | 6 | danh sách này | rút text của link |
| G5 | markdown | ô BẢNG chứa nguyên cụm | 6 | 6 | — | — |
| G6 | markdown | trong code fence | 6 | 6 | — | — |
| G7 | markdown | backslash escape `merged\:` | **0 LỌT** | 6 | danh sách này | gỡ escape |
| G8 | markdown | ngắt dòng GIỮA cụm | 6 | 6 | vá r2 | phẳng cả tệp (giữ) |
| H1 | tổ hợp dấu | `đích` bằng dấu TỔ HỢP `U+0301` | 6 | 6 | — | NFKC |
| H2 | tổ hợp dấu | dạng phân rã NFD | 6 | 6 | — | NFKC |

**Kết luận A:** spec chỉ nêu lớp NFKC (A1/A2). Danh sách đóng lộ thêm **12 lớp lọt
nữa** ở 5 nhóm mà spec KHÔNG nêu: đồng tự (D), nháy cong xen giữa (E2), biến thể
mũi tên/dash (F), cấu trúc HTML/Markdown (G2/G3/G4/G7). Vá riêng NFKC sẽ đóng 6/18
và để lại 12 — đúng cái bẫy AC 18 mô tả.

## B · doctrine-scan — chiều BẮT OAN (15 ca, đạt 12/15, **3 BẮT OAN**)

| id | lớp | phép thử | rc | đòi | ghi chú |
|---|---|---|---|---|---|
| O1 | **THẬT** | `CLAUDE.md` master dòng 80–84 nguyên văn | **6 OAN** | 0 | cụm `người có thẩm quyền` ngắt qua dòng 82/83 trong câu KỂ kết quả đo |
| O2 | term | `người có thẩm quyền` giữa câu văn xuôi | **6 OAN** | 0 | cùng gốc với O1 |
| O3 | term | cụm ấy ngắt dòng trong câu khác | **6 OAN** | 0 | cùng gốc |
| O4 | entity lồng | `&amp;#58;` | 0 | 0 | ✓ |
| O5 | đồng tự | văn bản Nga THẬT | 0 | 0 | ✓ ràng buộc cho lớp D |
| O6 | đồng tự | văn bản Hy Lạp THẬT | 0 | 0 | ✓ ràng buộc cho lớp D |
| O7 | dash | `cross-review`, `end-to-end`, `read-only` | 0 | 0 | ✓ ràng buộc cho lớp F |
| O8 | html tag | `a < b > c` trong mẫu shell | 0 | 0 | ✓ ràng buộc cho lớp G2 |
| O9 | html tag | `<b>tài liệu</b>` vô hại | 0 | 0 | ✓ ràng buộc cho lớp G2 |
| O10 | link | link Markdown bình thường | 0 | 0 | ✓ ràng buộc cho lớp G4 |
| O11 | backslash | `\*` `\_` escape bình thường | 0 | 0 | ✓ ràng buộc cho lớp G7 |
| O12 | `Cf` | văn bản tiếng Việt đủ dấu | 0 | 0 | ✓ lọc `Cf` không nuốt dấu |
| O13 | NFKC | dấu câu toàn rộng vô hại | 0 | 0 | ✓ ràng buộc cho lớp A |
| O14 | trỏ đúng | adapter TRỎ về protocol | 0 | 0 | ✓ |
| O15 | bảng khác | bảng Markdown không phải bảng vai trò | 0 | 0 | ✓ |

## C · lược đồ `lease` — AC 21 (25 ca, đạt 9/25, **11 LỌT + 5 TRACEBACK**)

| id | hình dạng | rc | traceback | đòi |
|---|---|---|---|---|
| L0 | lease ĐỦ và hợp lệ | 0 | – | cho qua ✓ |
| L1 | `null` | 8 | – | chặn ✓ |
| L2 | dict RỖNG | 8 | – | chặn ✓ |
| L3 | **CHỈ** `expires_utc` (P1-B) | **0 LỌT** | – | chặn |
| L4 | thiếu `lease_id` | **0 LỌT** | – | chặn |
| L5 | thiếu `granted_by` | **0 LỌT** | – | chặn |
| L6 | thiếu `evidence` | **0 LỌT** | – | chặn |
| L7 | thiếu `expires_utc` | 8 | – | chặn ✓ |
| L8 | lease là CHUỖI | 1 | **Y** | chặn có kiểm soát |
| L9 | lease là SỐ | 1 | **Y** | chặn có kiểm soát |
| L10 | lease là MẢNG | 1 | **Y** | chặn có kiểm soát |
| L11 | lease là bool | 1 | **Y** | chặn có kiểm soát |
| L12 | `expires_utc` RỖNG | 8 | – | chặn ✓ |
| L13 | `expires_utc` SAI DẠNG | 2 | – | chặn ✓ |
| L14 | `expires_utc` THIẾU MÚI GIỜ | 2 | – | chặn ✓ |
| L15 | `expires_utc` là SỐ | 1 | **Y** | chặn có kiểm soát |
| L16 | `expires_utc` năm 9999 | **0 LỌT** | – | chặn |
| L17 | `expires_utc` TRƯỚC 1970 | 8 | – | chặn ✓ |
| L18 | `expires_utc` là `null` | 8 | – | chặn ✓ |
| L19 | `granted_by` là PROVIDER (tự cấp) | **0 LỌT** | – | chặn |
| L20 | `granted_by` NGOÀI allowlist | **0 LỌT** | – | chặn |
| L21 | `granted_by` là SỐ | **0 LỌT** | – | chặn |
| L22 | `lease_id` RỖNG | **0 LỌT** | – | chặn |
| L23 | `evidence` RỖNG | **0 LỌT** | – | chặn |
| L24 | `lease_id` là MẢNG | **0 LỌT** | – | chặn |

**Kết luận C:** spec nêu 5 hình dạng; danh sách đóng lộ **16 hình dạng hỏng**.
Đáng chú ý L19/L20 — `begin-attempt` nhận một lease TỰ CẤP (`granted_by: "claude"`)
hoặc cấp bởi tên ngoài allowlist, dù `record-lease` chặn cả hai. Đây chính là
"hai chốt tự kiểm rời nhau" ở mức THẨM QUYỀN, không chỉ mức lược đồ.

---

## Tầng chữa — MỘT LƯỢT cho cả ba bảng

### 1 · `_chuan_hoa` — một hàm, áp cho **CẢ HAI VẾ** so khớp

Thứ tự có lý do, không tuỳ tiện:

1. bỏ **comment HTML** `<!--…-->` → G3
2. bỏ **tag HTML** (đòi tên tag ngay sau `<`, nên `a < b > c` KHÔNG bị coi là tag) → G2, ràng buộc O8/O9
3. rút **text của link/ảnh Markdown** `[t](u)` → `t` → G4, ràng buộc O10
4. gỡ **backslash escape** `\X` → `X` → G7, ràng buộc O11
5. `html.unescape` **ĐÚNG MỘT LẦN** → C1–C4, giữ C5 tha
   *(đặt SAU bước 2 để `&lt;b&gt;` — thứ hiển thị nguyên văn `<b>` — không bị hiểu thành tag)*
6. **NFKC** (không phải NFC) → A1–A8
7. lọc hạng `Cf` → B1–B6, ràng buộc O12
8. `casefold`
9. **gấp đồng tự** Cyrillic/Hy Lạp → Latin (chỉ chữ thường, sau casefold) → D1–D4, ràng buộc O5/O6
10. **gấp nháy cong** rồi bỏ nháy → E1/E2
11. **gấp mũi tên** biến thể → `→` → F1
12. bỏ trang trí `` ` `` `*` `~`; **gộp phân cách** (`_`, hyphen/dash, NBSP, khoảng trắng) về MỘT khoảng trắng → A9, F2, G1, ràng buộc O7

Gộp phân cách về khoảng trắng (thay vì XOÁ như bản cũ) còn sửa một lời khai SAI
trong chú thích bản cũ: bản cũ xoá `_`, nên `same_failure_limit` → `samefailurelimit`
còn `same failure limit` → `same failure limit` — **hai chuỗi KHÔNG khớp nhau**,
trái với điều chú thích tuyên bố.

### 2 · chiều BẮT OAN — hạng `thuật ngữ NGÔN NGỮ THƯỜNG`

Tiêu chí khai TƯỜNG MINH, áp cho **toàn bộ** danh sách cấm chứ không riêng cụm
đang đỏ: *một mục là `ngôn ngữ thường` khi nó là cụm danh từ tiếng Việt/Anh dùng
được trong câu bình thường mà KHÔNG mượn nghĩa protocol.*

Soát toàn danh sách theo tiêu chí ấy:

| mục | phán định | vì sao |
|---|---|---|
| ngưỡng số (`3 attempt/packet`, `45 phút/run`, …) | coined | ghép số + danh từ protocol |
| định danh (`max_*`, `same_failure_limit`) | coined | tên biến |
| dòng state machine | coined | chuỗi trạng thái |
| `dispatcher/reconciler`, `local controller`, `land operator`, `apply job`, `phiên land` | coined | nhãn vai do protocol đặt ra |
| 4 ô nội dung bảng vai trò | coined | câu mô tả của protocol |
| định nghĩa `merged:` / `integrated:` / `landed:` / `complete:` | coined | định nghĩa |
| **`người có thẩm quyền`** | **ngôn ngữ thường** | cụm danh từ tiếng Việt phổ thông |

Soát ra **đúng một** mục — đó là kết quả của việc áp tiêu chí, không phải bỏ
riêng cụm đang đỏ. Mục hạng này KHÔNG bị xoá khỏi danh sách; nó chỉ tính là chép
doctrine khi có **ngữ cảnh tái tạo doctrine**, định nghĩa CƠ HỌC:

> tồn tại một ĐƠN VỊ (một dòng thô, hoặc một đoạn = các dòng liền không trống)
> mà bản chuẩn hoá của nó chứa cụm ấy **và** (dòng thô có `|` — tức ô bảng —
> **hoặc** bản chuẩn hoá của đơn vị còn chứa một mục KHÁC cùng nhóm).

- O1/O2/O3: đoạn văn xuôi, không `|`, không mục §2 nào khác ⇒ **THA** ✓
- dòng thật `| Người có thẩm quyền | start/pause/… |` ⇒ có `|` ⇒ **BẮT** ✓
- `Land Operator` trơ trọi vẫn **BẮT** (coined, không thuộc hạng này) ✓

### 3 · lease — MỘT hàm kiểm chung

`_kiem_luoc_do_lease(lease)` kiểm TRỌN lược đồ + kiểu + thẩm quyền + cửa sổ hạn,
dùng bởi **cả** `record-lease` **lẫn** `begin-attempt`. Mọi hình dạng sai trả mã
thoát có kiểm soát (`RC_ARG`/`RC_STATE`/`RC_GUARD`), KHÔNG traceback.
Cửa sổ hạn: `1970 < expires_utc ≤ now + 366 ngày` — chặn L16 (năm 9999) mà không
chặn lease thật (hạn 2026-08-15).
