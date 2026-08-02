# PROMPT BÀN GIAO — sau lượt bảo trì kho LƯỢT 2 (02-08-2026)

Dán nguyên khối này vào phiên mới. Chạy trên **máy Windows có config** (`D:\Quốc hội\tra-luat`).

---

## ⚠ ĐỌC TRƯỚC — bốn thứ ĐỪNG làm lại

1. **KHÔNG gỡ Luật 41/2024 khỏi `_ZZZ_QUARANTINE_taluat`.** Quarantine ĐÚNG (superseded_by VBHN
   19-2026-VBHN-VPQH, doctrine VBHN-first). Tiền đề gốc bị bác từ lượt 8. Bất kỳ đề xuất nào dẫn tới
   `corpus=true` cho dòng `1Ds95…` là đã đi lại vào tiền đề đã bác.
2. **KHÔNG chép đè 3 record cache** `19-2026` / `54-2025` / `89-2026`. Lượt 2 đã tải lại đúng nguồn
   Công báo (sha256 khớp tuyệt đối), nạp cache tạm, **đối chiếu từng Điều** và kết luận: bản thay thế
   **không chữa** khiếm khuyết đã nêu, còn làm MẤT thứ khác. Số đo: biên bản lượt 2 §2.
3. **KHÔNG đi tìm «nguồn tốt hơn» cho 89-2026.** Tiền đề «khối đầu thiếu VPQH + dòng Số:» là **SAI**:
   record đang dùng CÓ cả hai ở ĐẦU; bản Công báo mới mới là bản thiếu.
4. **KHÔNG coi cờ đỏ trong `verify_flags` của cache là bệnh thật khi chưa đo lại.** Cờ được ĐÓNG BĂNG
   lúc nạp. Cờ `T1-nhẹ` trên `19-2026`/`54-2025` chỉ là dư âm lỗi §4.1 **đã vá ở r314**.

**Sổ lượt 2:** `rasoat/BIEN_BAN_BAO_TRI_KHO_BHXH_LUOT2_2026-08-02.md` (nhánh
`claude/baotri-kho-bhxh-luot2`, commit `bf216ab`, đã push).
**Sổ lượt 1:** `rasoat/BIEN_BAN_BAO_TRI_KHO_BHXH_2026-08-02.md` — ★§4.2 của nó (container .docx hỏng)
**cần đính chính**, xem lượt 2 §4.

---

## VIỆC 1 — Ghi note chống tái phát: CHỜ ĐÚNG MỘT QUYẾT ĐỊNH CỦA NGƯỜI DÙNG

Mọi thứ đã sẵn sàng; chỉ vướng chỗ **cả hai prompt cũ chỉ SAI SỔ**.

Đo được (lượt 2 §1): dòng nằm **vật lý ở registry NỀN `vbqppl`**, không ở sheet profile «Luật BHXH».

```
reg_get(drive_id=1Ds95…, profile='Luật BHXH') → ok=True, n_rows=0
reg_get(drive_id=1Ds95…, profile='vbqppl')    → ok=True, n_rows=1   ← dòng thật
reg-query --profile "Luật BHXH"  → vẫn thấy, nhưng envelope khai "scope":"vbqppl" + cờ BASE_SCOPE_HIT
```

`reg_bulk` là **UPDATE-only, KHÔNG insert** ⇒ ghi bằng `--profile "Luật BHXH"` **không tạo dòng rác**
nhưng là **NO-OP báo `missed`**. Rủi ro thật: tưởng đã ghi xong.

**→ Hỏi người dùng: ghi vào sổ NỀN `vbqppl` (đúng nơi dòng tồn tại) hay dừng?** Được duyệt thì chạy:

```powershell
cd "D:\Quốc hội\tra-luat"     # hoặc worktree SẠCH tại origin/master
$env:PYTHONIOENCODING="utf-8" # console cp1258 nuốt Unicode

# (1) ĐỌC note TƯƠI — đường đọc `note` DUY NHẤT là action reg_get; reg-query KHÔNG chiếu cột này
python -c "import sys; sys.path.insert(0,'scripts'); import gas, json; print(json.dumps(gas.get('reg_get', profile='vbqppl', drive_id='1Ds95NoIdZyRutHGsMS85N4hB61Nglz5eeg0vRZ-XqYM', refresh='true'), ensure_ascii=False, indent=1))"
#   note PHẢI = "Đã xóa khỏi NLM; thay bằng VBHN 19/VBHN-VPQH (2026)"  (ĐÚNG 51 ký tự)
#   KHÁC ⇒ DỪNG: phiên khác vừa ghi. Soạn lại phần NỐI trên nền note MỚI.

# (2) cổng ghi
python scripts\tl.py manifest --profile vbqppl
python scripts\tl.py boot --refresh --profile vbqppl
python scripts\tl.py precheck --profile vbqppl --cols note --json     # ok:true, blockers rỗng

# (3) GHI — ⚠ `register --bulk` GHI NGAY, KHÔNG có --apply/--confirm, KHÔNG chạm --expect
python scripts\tl.py register --bulk rasoat\pending_note_41-2024_bulk_2026-08-02.json --cols note --profile vbqppl

# (4) READBACK keyed — rc/ok KHÔNG BAO GIỜ là bằng chứng ghi
python -c "import sys; sys.path.insert(0,'scripts'); import gas; n=gas.get('reg_get', profile='vbqppl', drive_id='1Ds95NoIdZyRutHGsMS85N4hB61Nglz5eeg0vRZ-XqYM', refresh='true')['rows'][0]['note']; print(len(n)); print(n)"
#   PHẢI ra 746 và BẮT ĐẦU bằng note cũ.
```

Chống va chạm **chỉ có thể làm thủ công**: đặt bước (1) ngay sát bước (3). `--expect` (CAS r279) nằm
trên đường ĐƠN, mà đường đơn không ghi được `note`; nhánh `--bulk` không có `--expect`.

---

## VIỆC 2 — Mục «3 khiếm khuyết nguồn»: ĐỀ NGHỊ ĐÓNG bằng kết luận «không đè»

Bảng đo (lượt 2 §2) — CŨ = record đang dùng, MỚI = bản Công báo:

| | 19-2026 | 54-2025 | 89-2026 |
|---|---|---|---|
| hạng | **95/verified → 50/staged** | **95/verified → 50/staged** | 50/staged → 50/staged |
| lệch NỘI DUNG | 9 Điều | **32 Điều** | 3 Điều |
| «VPQH + Số:» ở khối đầu | **CÓ → MẤT** | không → không | **CÓ → MẤT** |
| markup | `{strike:2}` → `{strike:2}` (Y HỆT) | None → None | None → None |
| neo chú thích `[n]` | 19 → **0** | 0 → 0 | 5 → **0** |

Nếu người dùng vẫn muốn bỏ **1 dòng nhãn mục** ở khối đầu `54-2025` thì đi nguồn **`.doc`/`.docx`
Công báo** (link `.doc` có sẵn trên trang 45821), **KHÔNG dùng PDF** — PDF trộn chú thích vào 32/72 Điều.
Và vẫn phải quyết `method_rank 95→50` trước (giữ hạng = đẩy Drive rồi nạp `--method exportdocx`).

---

## VIỆC 3 — Khiếm khuyết THẬT chưa xử (lượt vá mã riêng)

Bản **đang dùng** nhét **chú thích hợp nhất vào THÂN ĐIỀU CUỐI**:

| | Điều cuối | thân Điều | chú thích dính vào |
|---|---|---|---|
| 19-2026 | Điều 141 | 8.552 ký tự | **4.009** |
| 89-2026 | Điều 79 | 1.112 ký tự | **970** |

Nguyên văn phần dính: «[1] Luật Nhà giáo số 73/2025/QH15 có căn cứ ban hành như sau: …» — **đúng đoạn chữ**
lượt 1 dùng để bác bản PDF (lượt 1 thấy nó ở Điều 1; thực tế bản đang dùng có nó ở Điều cuối).

Đường xử: **tách khối chú thích ra khỏi Điều cuối khi nạp** (`normalize_document`/`ingest_to_cache`), giữ
chú thích ở trường riêng — **không** chép đè, vì bản Công báo bỏ SẠCH chú thích (mất thông tin pháp lý
«khoản này do luật nào sửa, hiệu lực từ bao giờ»). Cần test khoá **cả hai chiều**: (a) chú thích ra khỏi
thân Điều; (b) tài liệu KHÔNG có chú thích thì chuỗi ra = chuỗi vào.

---

## VIỆC 4 — Hai việc sổ sách nhỏ

1. **Đính chính §4.2 biên bản lượt 1**: «.docx Công báo là container HỎNG» **không tái lập** — đo trên
   ĐÚNG tệp đó (sha256 khớp) cho **0/40** và **0/37** entry dùng `\`. Bệnh ở **đường tải của container web**.
   Bản vá r316 (`scan_file` hết fail-open) vẫn đúng vì lý do riêng, chỉ mô tả nguyên nhân cần sửa.
2. **VIỆC 4 của prompt lượt 1** (echo `registry_scope`) — **đã có một phần**: `reg-query` đã trả `scope`
   + cờ `BASE_SCOPE_HIT`. Còn thiếu: **WARN LOUD** khi `--profile` ≠ nền mà `registryDocId` rỗng.

---

## RÀNG BUỘC

* ⚠ **Kiểm mình đang đứng ở đâu TRƯỚC MỌI THỨ.** 02-08 cây canonical `D:\Quốc hội\tra-luat` đang đứng
  **nhánh `claude/ras17-merge-gate-anchor`, behind origin/master 10, 9 tệp BẨN** (việc sống của phiên khác).
  Lượt 2 đã né bằng **worktree sạch**: `git worktree add "D:\Quốc hội\baotri_wt" origin/master --detach`
  rồi **copy `tra_luat_config.v2.json` vào worktree** (tệp này `.gitignore`, worktree không tự có; thiếu nó
  thì `--profile` thành NO-OP và mọi lệnh ĐỌC rơi về sổ NỀN IM LẶNG).
* **Kiểm cờ profile có tác dụng thật:** `python scripts/tl.py profile-info --profile "<X>" --json`
  → `profile_found:false` hoặc `source:"env-only"` ⇒ **đang đọc sổ NỀN**, đừng tin số đo registry nào.
* **Mọi lệnh đo phải `PYTHONIOENCODING=utf-8`** — console cp1258 ném `UnicodeEncodeError` giữa chừng.
* ⚠ **`bash -c` NUỐT BACKSLASH** ⇒ detector tự viết sẽ báo «0 vi phạm» GIẢ. Viết ra tệp `.py`, dùng `chr(92)`.
* `rasoat/` **trong git nhưng NGOÀI gói** (`_RELEASE_EXCLUDE_DIRS`, r249) ⇒ thêm sổ **không** phải bump
  VERSION, **không** phải tái sinh `RELEASE_MANIFEST.json`.
* Kho thường có 2–3 phiên song song: `git status -sb` + `gh pr list` + quét **tên nhánh remote** trước khi
  viết mã. `git fetch origin master` và đối chiếu `max_r` **trước MỖI lượt bump**, không chỉ lúc mở nhánh.
* Môi trường máy này (đã đo): `Python 3.13.1` · `pypdf` ✅ · `python-docx` ✅ · `pdftotext` ✅ ·
  `pdfplumber` ✗ (không cần). TLS tới `g7.cdnchinhphu.vn` **không** cần vá chuỗi cert như container.
