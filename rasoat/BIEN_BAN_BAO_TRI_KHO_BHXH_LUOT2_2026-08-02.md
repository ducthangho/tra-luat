# BIÊN BẢN LƯỢT BẢO TRÌ KHO — LƯỢT 2 (máy Windows có config), 02-08-2026

Tiếp `rasoat/BIEN_BAN_BAO_TRI_KHO_BHXH_2026-08-02.md` (lượt 1, container web).
Cây chạy: worktree SẠCH `D:\Quốc hội\baotri_wt` tại `origin/master` = `705104e` = **v1.36.51** (r314→r319).
Cache thật: `C:\Users\admin\.tra_luat_cache\docs\` · cache TẠM: scratchpad phiên (ephemeral).

> **Thao tác GHI duy nhất của lượt này: 1 ô `note` trên 1 dòng registry NỀN** (§1b, sau khi người dùng
> duyệt tường minh). Không đè cache, không đụng Drive/NLM, không đổi bất kỳ cột nào khác.
> Mọi số đo khác từ lệnh ĐỌC + nạp vào cache TẠM ngoài kho.

---

## 0. Kết quả gọn

| Mục | Trạng thái | Cốt lõi |
|---|---|---|
| 1. Ghi note chống tái phát | ✅ **ĐÃ THI HÀNH — người dùng duyệt, readback chứng minh** | Ghi vào registry **NỀN `vbqppl`** (không phải sheet profile như cả hai prompt chỉ dẫn) — §1 + §1b |
| 2. Chép đè 3 record cache | ✅ **ĐÓNG bằng kết luận KHÔNG ĐÈ — người dùng duyệt** | Đo từng Điều: bản thay thế **không chữa** khiếm khuyết đã nêu, và làm MẤT thứ khác (§2) |
| — | ✅ Nghiệm thu r318 trên dữ liệu thật | Cờ chuyển từ dòng dương-tính-giả sang dòng nhãn THẬT; lời khuyên nguy hiểm đã hết (§3) |
| — | ⚠ 2 tiền đề của lượt 1 KHÔNG tái lập | «container .docx hỏng» và một phần bảng khiếm khuyết (§4) |
| — | 🔶 1 khiếm khuyết THẬT mới lộ, chưa xử | Chú thích hợp nhất bị nhét vào **thân Điều CUỐI** (§5) |

---

## 1. Mục 1 — dòng 41-2024 KHÔNG nằm ở sổ profile

`reg_get` theo `drive_id` trên hai phạm vi (dữ liệu TƯƠI, `refresh=true`):

```
profile='Luật BHXH' → ok=True, n_rows=0        ← KHÔNG có dòng này
profile='vbqppl'    → ok=True, n_rows=1        ← dòng thật ở ĐÂY
   name  Luat_41-2024-QH15_Bao_hiem_xa_hoi
   cat   _ZZZ_QUARANTINE_taluat   corpus false   nlm_status removed_superseded_by_VBHN
   note  "Đã xóa khỏi NLM; thay bằng VBHN 19/VBHN-VPQH (2026)"   (ĐÚNG 51 ký tự — khớp tiền tố payload)
```

`reg-query --profile "Luật BHXH"` VẪN thấy dòng đó, nhưng envelope tự khai rõ nó đi mượn sổ nền:

```json
{"drive_id": "1Ds95…", "cat": "_ZZZ_QUARANTINE_taluat",
 "flags": ["RAW_NAME_NOT_NLM", "BASE_SCOPE_HIT"], "scope": "vbqppl"}
```

⇒ **Cả hai prompt bàn giao đều chỉ sai sổ.** Chạy đúng như prompt (`--profile "Luật BHXH"`) thì:
`reg_bulk` là **UPDATE-only, KHÔNG insert** (`source_ops.py:398-405`) ⇒ không tạo dòng rác, nhưng
sẽ là **NO-OP báo `missed`** — rủi ro thật là *tưởng đã ghi xong*.

Kiểm lại hai khẳng định kỹ thuật của lượt 1 trên mã v1.36.51 — **cả hai vẫn đúng**:
* `note` không chiếu qua `reg-query` (kể cả `--live`); đường đọc duy nhất là action `reg_get`.
* Nhánh `--bulk` **không có cổng `--apply`/`--confirm`** (ghi ngay sau `_apply_gate`) và **không** chạm
  `--expect` ⇒ chống va chạm chỉ có thể làm thủ công: đọc `reg_get` ngay sát lệnh ghi.

---

## 1b. Mục 1 — ĐÃ THI HÀNH (người dùng duyệt tường minh «đồng ý cả 2»)

Ghi vào **sổ NỀN `vbqppl`**, đúng nơi dòng tồn tại. Trình tự đã chạy:

| Bước | Kết quả |
|---|---|
| `manifest --profile vbqppl` | `count 1319 corpus=668`, treeHash `7cde69d7-668`, 7,2s |
| `boot --refresh --profile vbqppl` | `entries_indexed 1319`, registry `1C21i65w…` |
| `precheck --profile vbqppl --cols note --json` | **`blockers: []`, `warnings: []`** — 3 check `ok:true`, snapshot 5s |
| đọc `reg_get` TƯƠI **ngay sát** lệnh ghi | note LIVE = **đúng 51 ký tự**, khớp tiền tố kỳ vọng |
| `register --bulk … --cols note --profile vbqppl` | `patched: 1 · missed: 0 · verified: true` · journal `register-bulk_1785679205_23488` |
| **readback keyed** (`reg_get refresh=true`) | **746 ký tự**, `startswith(note cũ) = True`, đúng 1 dòng |

⚠ Vì `--bulk` **không có `--expect`** (CAS r279 chỉ nằm trên đường ĐƠN, mà đường đơn không ghi được
`note`), chống va chạm được làm bằng **một script gộp đọc-kiểm-rồi-mới-ghi**: đọc `reg_get`, so bằng
máy với chuỗi 51 ký tự kỳ vọng, **lệch thì thoát rc=3 và không ghi gì**. Không so bằng mắt.

**Các cột khác giữ NGUYÊN** (đo lại sau khi ghi — chứng minh chỉ chạm đúng 1 ô):

```
cat        = '_ZZZ_QUARANTINE_taluat'      corpus     = 'false'
nlm_status = 'removed_superseded_by_VBHN'  row_kind   = 'own'
sohieu     = '41-2024-QH15'                name       = 'Luat_41-2024-QH15_Bao_hiem_xa_hoi'
```

⇒ Quarantine giữ nguyên, **không** có `corpus=true`. Payload đã đổi tên thành
`rasoat/DA_THI_HANH_note_41-2024_bulk_2026-08-02.json` để không ai chạy lại (chạy lại sau khi phiên khác
nối thêm note = **đè mất phần nối của họ**; đổi tên khiến lệnh cũ gãy TO thay vì clobber im lặng).

---

## 2. Mục 2 — ĐO XONG, và kết luận NGƯỢC với kế hoạch

Nguồn Công báo tải lại đúng bản của lượt 1 — **byte-size và sha256 khớp tuyệt đối**:

| Số hiệu | Tệp | Bytes | sha256 | khớp biên bản lượt 1 |
|---|---|---|---|---|
| 19-2026 | CB 133 `.docx` | 150.626 | `3137d671…2c2283f5` | ✅ |
| 54-2025 | CB 1083+1084 `.pdf` | 979.862 | `00d77770…6089a4c6` | ✅ |
| 89-2026 | CB 222 `.docx` | 115.494 | `deff1349…1266c9be` | ✅ |

Nạp cả ba vào cache TẠM rồi đối chiếu **từng Điều** với bản đang dùng (chuẩn hoá khoảng trắng;
phân loại lệch TRÌNH BÀY vs lệch NỘI DUNG bằng cách bỏ hết dấu câu rồi so):

| | 19-2026 | 54-2025 | 89-2026 |
|---|---|---|---|
| `doc_key` trùng | ✅ | ✅ | ✅ |
| số Điều | 141 = 141 | 72 = 72 | 79 = 79 |
| lệch TRÌNH BÀY | 14 Điều | 0 | 2 Điều |
| lệch NỘI DUNG | 9 Điều | **32 Điều** | 3 Điều |
| hạng CŨ → MỚI | **95/verified → 50/staged** | **95/verified → 50/staged** | 50/staged → 50/staged |
| khối đầu CŨ → MỚI | 936 → 839 | 663 → 865 | 653 → 560 |
| «VĂN PHÒNG QUỐC HỘI» + «Số:» ở ĐẦU | **CÓ → MẤT** | không → không | **CÓ → MẤT** |
| markup | `{strike:2}` → `{strike:2}` | None → None | None → None |
| neo chú thích `[n]` trong thân | 19 → **0** | 0 → 0 | 5 → **0** |

### 2.1 Từng khiếm khuyết của đề bài, đối chiếu số đo

| Khiếm khuyết nêu trong kế hoạch | Số đo | Phán |
|---|---|---|
| `19-2026` — «bản còn markup sửa đổi» | bản Công báo có **Y HỆT** `markup={strike:2}` | **Đè KHÔNG chữa được** |
| `54-2025` — «khối đầu là chrome trang web» | không phải chrome web: là **ĐÚNG 1 dòng** nhãn mục Công báo `VĂN BẢN PHÁP LUẬT KHÁC`; phần còn lại là khối đầu văn bản chuẩn | đúng một phần, **rất nhỏ** |
| `89-2026` — «khối đầu thiếu VPQH + dòng Số:» | record ĐANG DÙNG mở đầu bằng `VĂN PHÒNG QUỐC HỘI … Số: 89/VBHN-VPQH`; **bản Công báo mới mới là bản THIẾU** | **Tiền đề SAI — đè sẽ TẠO RA đúng lỗi đó** |

### 2.2 Vì sao 54-2025 (nguồn PDF) tệ hơn hẳn

32/72 Điều bị **trộn chú thích hợp nhất vào thân Điều**: **+7.239 ký tự** đo trên chuỗi ĐÃ CHUẨN HOÁ
khoảng trắng (chênh thô toàn bộ `articles` là +10.886, nhưng phần dôi là khoảng trắng dàn trang của PDF —
dùng số chuẩn hoá mới là chữ thật thêm vào). Nguyên văn phần chèn thêm
ở Điều 21 (mẫu lặp lại +211 ký tự trên nhiều Điều):

> «4 Điều này được sửa đổi, bổ sung theo quy định tại khoản 3 Điều 1 của Luật số 87/2025/QH15 …
> có hiệu lực kể từ ngày 01 tháng 7 năm 2025.»

Đây **cùng một lỗi** mà lượt 1 đã dùng để bác bản PDF của 19-2026 (§3.4: «`pdftotext` trộn CHÚ THÍCH
vào thân Điều»). Lượt 1 bác PDF cho 19-2026 nhưng lại **chọn PDF cho 54-2025** — cùng nguồn bệnh, khác kết luận.

### 2.3 Cờ `T1-nhẹ` trên record cũ là DƯ ÂM, không phải khiếm khuyết

Chạy `sohieu_corroborated()` của mã hiện hành trên chính nội dung record cũ:

```
19-2026 : cờ T1 LƯU trong record = True  | đo lại r319 = True  ⇒ dư âm lỗi §4.1 đã vá ở r314
54-2025 : cờ T1 LƯU trong record = True  | đo lại r319 = True  ⇒ dư âm
89-2026 : không có cờ                    | đo lại r319 = True
```

Cả dạng gạch nối lẫn gạch chéo đều `corroborated=True`. ⇒ Hai cờ đỏ trên record cũ **không** là lý do để đè.

### 2.4 Khuyến nghị

**KHÔNG chép đè cả ba.** Với 19-2026 và 54-2025 còn phải trả giá `method_rank 95→50` và
`evidence_status verified→staged` — thứ khó lấy lại — để đổi lấy một bản KHÔNG tốt hơn.
Riêng 54-2025, nếu vẫn muốn bỏ 1 dòng nhãn mục thì đường đúng là nạp lại từ **`.doc`/`.docx` Công báo**
(link `.doc` có sẵn trên cùng trang 45821), **không** từ PDF — nhưng vẫn cần cân nhắc §5.

---

## 3. Nghiệm thu r318 trên dữ liệu thật (đạt)

Nạp bản 54-2025 CHƯA cắt, `--loc-congbao`:

```
LOC_CONG_BAO: bỏ 62 dòng (dòng chạy=58 · số trang=0 · chữ ký số=4), 125774 → 123017 ký tự
DAU_MUC_CONG_BAO_CON_LAI: dòng 8 — nhãn MỤC của Công báo …, CỐ Ý không tự bỏ.
  Cách sửa: bỏ ĐÚNG (các) dòng nêu trên rồi nạp lại.
  ★ĐỪNG cắt từ đầu bản tới dòng «Số: …»: với VBHN dòng đó nằm ở KHỐI KÝ CUỐI, cắt theo neo sẽ
   xoá sạch thân văn bản.
```

* Cờ chỉ **dòng 8** = nhãn mục THẬT (`VĂN BẢN PHÁP LUẬT KHÁC`, xuất hiện đúng 1 lần).
* **Không** báo dòng 1974 — dòng `VĂN BẢN QUY PHẠM PHÁP LUẬT` đứng một mình, là dòng thứ ba của tiêu đề
  «Chương VI …» bị xuống dòng. Phép nhìn lui của r318b loại đúng dương-tính-giả.
* Lời khuyên nguy hiểm cũ («cắt tay tới dòng mang số hiệu») đã thay bằng chỉ dẫn an toàn + cảnh báo tường minh.
* Số lọc 62 dòng (58+4) khớp **từng con số** với lượt 1.

Cắt đúng dòng 8 rồi nạp lại: 72 → 72 Điều, khối đầu bắt đầu đúng ở `VĂN BẢN HỢP NHẤT - VĂN PHÒNG QUỐC HỘI`.
⇒ Thao tác cắt chỉ chạm khối đầu, xác nhận kết luận «0/72 Điều bị đụng» của lượt 1.

---

## 4. Hai tiền đề của lượt 1 KHÔNG tái lập trên máy này

1. **«.docx Công báo là container HỎNG (tên entry dùng `\`)»** (§4.2 lượt 1: 33/40 và 30/37 entry).
   Đo lại trên **đúng tệp đó** (sha256 khớp tuyệt đối): **0/40 và 0/37** entry dùng `\`,
   `word/document.xml` có đúng tên chuẩn, `python-docx` mở thẳng được. Không cần bước sửa zip.
   ⇒ Bệnh nằm ở **đường tải của container web**, không ở tệp Công báo. Bản vá r316 (`scan_file` hết
   fail-open) vẫn đúng và đáng giữ vì lý do riêng của nó, nhưng **mô tả nguyên nhân trong §4.2 cần đính chính**.
2. **Bảng «ba khiếm khuyết nguồn»** — 2/3 không đứng vững khi đo trên record đang dùng (xem §2.1).

⚠ Bẫy đã dính khi đo: `bash -c "…'\\\\'…"` **nuốt backslash** ⇒ detector báo «0 vi phạm» GIẢ.
Phải viết ra tệp `.py` và dùng `chr(92)`. (Cùng họ bẫy đã ghi trong memory.)

---

## 5. Khiếm khuyết THẬT mới lộ — chưa xử, KHÔNG thuộc lượt này

Bản **đang dùng** của 19-2026 và 89-2026 nhét **khối chú thích hợp nhất vào THÂN ĐIỀU CUỐI**:

| | Điều cuối | thân Điều CŨ | phần chú thích dính vào |
|---|---|---|---|
| 19-2026 | Điều 141 | 8.552 ký tự | **4.009 ký tự** |
| 89-2026 | Điều 79 | 1.112 ký tự | **970 ký tự** |

Nguyên văn phần dính (19-2026, Điều 141):

> «[1] Luật Nhà giáo số 73/2025/QH15 có căn cứ ban hành như sau: “Căn cứ Hiến pháp … Quốc hội ban hành
> Luật Nhà giáo.”. Luật Thanh tra số 84/2025/QH15 …»

★ Đây **đúng đoạn chữ** mà lượt 1 đã dùng làm lý do bác bản PDF — chỉ khác chỗ rơi: lượt 1 thấy nó ở
**Điều 1**, thực tế bản đang dùng có nó ở **Điều 141**. Ai hỏi «nguyên văn Điều 141» sẽ nhận kèm căn cứ
ban hành của bốn luật khác.

**Đường xử ĐÚNG không phải là chép đè** (bản Công báo bỏ SẠCH chú thích: neo `[n]` 19 → 0 và 5 → 0,
tức mất thông tin «khoản này do luật nào sửa, hiệu lực từ bao giờ» — thông tin có giá trị pháp lý).
Đường đúng là **tách khối chú thích ra khỏi Điều cuối khi nạp** (sửa `normalize_document`/`ingest_to_cache`),
giữ nguyên chú thích ở trường riêng. Đó là một lượt VÁ MÃ độc lập, cần test khoá cả hai chiều.

---

## 6. Việc còn treo

**Cả hai mục của lượt bảo trì kho ĐÃ ĐÓNG** (người dùng duyệt 02-08: «đồng ý cả 2»).
~~Mục 1~~ → thi hành, readback chứng minh (§1b). ~~Mục 2~~ → đóng bằng kết luận **KHÔNG ĐÈ**.

Còn lại là việc SINH RA từ lượt này, **không** thuộc phạm vi đã duyệt:

1. **Tách chú thích hợp nhất khỏi Điều cuối** (§5) — lượt vá mã riêng, cần test khoá cả hai chiều.
2. **Đính chính §4.2 của biên bản lượt 1** (§4 trên đây) — «container .docx hỏng» không tái lập.
3. **VIỆC 4 của prompt lượt 1** (echo `registry_scope`) — *đã có một phần*: `reg-query` **đã** trả
   `scope` + cờ `BASE_SCOPE_HIT`. Phần còn thiếu là WARN LOUD khi `--profile` ≠ nền mà `registryDocId` rỗng.
4. Nếu sau này vẫn muốn bỏ **1 dòng nhãn mục** ở khối đầu `54-2025`: đi nguồn `.doc`/`.docx` Công báo,
   **KHÔNG dùng PDF**, và quyết `method_rank 95→50` trước.

## 7. Điều kiện môi trường (máy này, để tái lập)

`Python 3.13.1` · `pypdf` ✅ · `python-docx` ✅ · `pdftotext` ✅ (`/mingw64/bin`) · `pdfplumber` ✗ (không cần).
TLS tới `g7.cdnchinhphu.vn` **không** cần vá chuỗi cert như container — `urllib` mặc định tải được cả ba tệp.
Console cp1258 nuốt Unicode ⇒ mọi lệnh đo phải `PYTHONIOENCODING=utf-8`.
