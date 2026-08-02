# PROMPT BÀN GIAO — sau lượt bảo trì kho 02-08-2026

Dán nguyên khối này vào phiên mới. **Chạy trên MÁY CÓ CONFIG** (Windows `D:\Quốc hội\tra-luat`
hoặc Cowork đã bootstrap) — hai mục đầu KHÔNG chạy được trên container web sạch.

---

## ⚠ ĐỌC TRƯỚC — hai điều đừng làm lại

1. **KHÔNG gỡ Luật 41/2024 khỏi `_ZZZ_QUARANTINE_taluat`.** Quarantine ĐÚNG: lý do là
   `superseded_by` VBHN 19-2026-VBHN-VPQH (doctrine VBHN-first), không phải «là dự thảo».
   Tiền đề gốc của Q-APPROVALS đã bị bác ở lượt 8 (28-07), phần việc chính đáng đã thi hành
   lượt 12–13. Bất kỳ đề xuất nào dẫn tới `corpus=true` cho dòng này = đã đi lại vào tiền đề đã bác.
2. **KHÔNG đi tìm «nguồn tốt hơn» cho lỗi «khối đầu thiếu VĂN PHÒNG QUỐC HỘI + dòng Số:».**
   Đã bóc `word/document.xml`: hai chuỗi đó CÓ trong văn bản, nằm ở bảng **XÁC THỰC VĂN BẢN
   HỢP NHẤT cuối bản** — đúng thể thức VBHN. Không nguồn nào chữa được vì không có gì để chữa.

**Sổ của lượt trước:** `rasoat/BIEN_BAN_BAO_TRI_KHO_BHXH_2026-08-02.md` (§4 = 6 phát hiện công cụ).
Nhánh: `claude/bhxh-41-2024-maintenance-jncsle`.

---

## VIỆC 1 — Ghi note chống tái phát (đã soạn sẵn, chỉ còn chạy)

Payload: **`rasoat/pending_note_41-2024_bulk_2026-08-02.json`** — 1 item, `drive_id`
`1Ds95NoIdZyRutHGsMS85N4hB61Nglz5eeg0vRZ-XqYM`, note cũ (51 ký tự) GIỮ NGUYÊN làm tiền tố,
chỉ NỐI thêm → 746 ký tự.

Chạy đúng thứ tự (chi tiết + lý do từng bước: biên bản §2):

```powershell
# (1) ĐỌC note TƯƠI trên ĐÚNG sheet — reg-query KHÔNG chiếu cột note, kể cả --live
python -c "import sys; sys.path.insert(0,'scripts'); import gas, json; print(json.dumps(gas.get('reg_get', profile='Luật BHXH', drive_id='1Ds95NoIdZyRutHGsMS85N4hB61Nglz5eeg0vRZ-XqYM', refresh='true'), ensure_ascii=False, indent=1))"
#     note PHẢI = "Đã xóa khỏi NLM; thay bằng VBHN 19/VBHN-VPQH (2026)"
#     KHÁC ⇒ DỪNG, phiên khác vừa ghi. Soạn lại phần NỐI trên nền note MỚI.

# (2) cổng ghi
python scripts\tl.py manifest --profile "Luật BHXH"
python scripts\tl.py boot --refresh --profile "Luật BHXH"
python scripts\tl.py precheck --profile "Luật BHXH" --cols note --json   # ok:true, blockers rỗng

# (3) GHI — `register --bulk` GHI NGAY, KHÔNG có DRY
python scripts\tl.py register --bulk rasoat\pending_note_41-2024_bulk_2026-08-02.json --cols note --profile "Luật BHXH"

# (4) READBACK keyed — rc/ok KHÔNG phải bằng chứng ghi
python -c "import sys; sys.path.insert(0,'scripts'); import gas; n=gas.get('reg_get', profile='Luật BHXH', drive_id='1Ds95NoIdZyRutHGsMS85N4hB61Nglz5eeg0vRZ-XqYM', refresh='true')['rows'][0]['note']; print(len(n)); print(n)"
#     PHẢI ra 746 và bắt đầu bằng note cũ.
```

**`--expect` (CAS r279) KHÔNG dùng được cho lô này** — chỉ nhánh `--bulk` ghi được `note`, mà
nhánh đó không có `--expect` (biên bản §2). Chống va chạm = bước (1) sát bước (3).

---

## VIỆC 2 — Chép đè 3 record cache (nguồn đã tìm + đo xong)

Ba bản Công báo đã đo đạt, sha256 + URL + lệnh nguyên văn ở biên bản §3.1 và §3.6.
**Cần môi trường:** `poppler-utils` (pdftotext) · `pip install pypdf cffi`.
`pypdf` là BẮT BUỘC: thiếu nó thì **mọi PDF bị chặn** — sau r314 thông điệp đã đúng thủ phạm
(`reason: pdf_probe_unavailable`, exit 6, kèm lệnh cài) chứ không còn vu cho tài liệu là «bản SCAN».
`python-docx` nay chỉ còn là TUỲ CHỌN: sau r316 nhánh không-`python-docx` không nhét số neo hình
vẽ vào thân Điều nữa (nghiệm thu: 3 số rác → 0 trên cả hai bản .docx).

| Số hiệu | Nguồn | Đo được |
|---|---|---|
| 19-2026-VBHN-VPQH | CB 133 (28-02-2026) `.docx` | 141 Điều · khối đầu 839 · 0 số rác · `markup={strike:2}` |
| 54-2025-VBHN-VPQH | CB 1083+1084 (23-8-2025) `.pdf` | 72 Điều · khối đầu 860 · cắt tay 1 dòng nhãn mục · 0/72 Điều bị đụng |
| 89-2026-VBHN-VPQH | CB 222 (16-04-2026) `.docx` | 79 Điều · khối đầu 560 · `verify_flags` RỖNG |

`19-2026` `markup={strike:2}` là **ngoại lệ ĐÃ DUYỆT** (người dùng chốt 02-08): cả hai run bị gạch
chỉ chứa MỘT DẤU CÁCH, không có quy phạm nào. Phản chứng đã chạy: bản PDF cho `markup=None` nhưng
trộn ~900 ký tự căn cứ ban hành của 4 luật khác vào **thân Điều 1** ⇒ PDF XẤU HƠN (§3.4).

**Hai việc phải quyết TRƯỚC khi chép đè** (chưa làm được ở container không có cache):

1. `doc-compare` bản tạm vs bản cũ: `doc_key` phải TRÙNG, số Điều không được GIẢM.
2. **`method_rank`**: bản mới nạp bằng `--method file` ⇒ rank **50**. Nếu bản cũ đang
   `method_rank=95` + `evidence_status=verified` thì chép đè là **HẠ hạng**. Chọn một:
   (a) đẩy tệp lên Drive rồi nạp lại bằng `--method exportdocx` (rank 95, giữ hạng); hoặc
   (b) chấp nhận hạ hạng có chủ đích và ghi rõ vào record + biên bản.
   **Đừng chép đè trước khi quyết** — mất `verified` là mất thứ khó lấy lại.

---

## VIỆC 3 — Lượt VÁ CODE: còn 2,5/6 phát hiện (biên bản §4)

Không phát hiện nào lộ ra bằng đọc code; đều do chạy thật. **Bốn cái đã vá trong nhánh này**
(r313→r316, v1.36.47+v1.36.48, gate xanh: selftest 1598/1598 · ruff delta 0 · golden 0-diff ·
release-verify 177/177). Còn lại:

| # | Lỗi | Vì sao ưu tiên |
|---|---|---|
| ~~§4.1~~ | ~~`_VBHN_WITHYEAR_RE` chỉ nhận gạch nối ⇒ `T1-nhẹ` dương tính giả~~ | ✅ **ĐÃ VÁ — r313 (v1.36.47)**, cùng nhánh này |
| ~~§4.3~~ | ~~Thiếu `pypdf`/`pdfplumber` ⇒ MỌI PDF bị kết luận «bản SCAN»~~ | ✅ **ĐÃ VÁ — r314 (v1.36.47)**, cùng nhánh này |
| ~~§4.2~~ | ~~`scan_file` FAIL-OPEN: docx không đọc được → báo «sạch markup»~~ | ✅ **ĐÃ VÁ — r315 (v1.36.48)**, cùng nhánh này |
| §4.6 (còn PHẦN KHẾ ƯỚC) | Phần RÒ ✅ **ĐÃ VÁ — r316 (v1.36.48)**: `wp:`/`wp14:` hết lọt vào thân Điều, nghiệm thu 3 số rác → 0 trên cả hai bản. **Chưa vá:** `requirements.txt` vẫn khai stdlib-only | r316 cứu được nhánh không-`python-docx`, nhưng `pypdf` KHÔNG có đường thay thế — thiếu nó là mọi PDF bị chặn (r314) |
| §4.4 | `CB_DAU_MUC` sai CẢ HAI CHIỀU; lời khuyên kèm theo nếu làm theo đúng chữ sẽ XOÁ Chương I–V | Cảnh báo nguy hiểm hơn thứ nó cảnh báo |
| §4.5 | `CB_CHU_KY_SO` chỉ khớp mẫu 4 dòng, bỏ sót biến thể 3 dòng ⇒ chrome lọt vào khối đầu | Bẩn khối đầu, không sai nội dung |

Quy trình bắt buộc: bump VERSION 3 chỗ · test `rXXX_` cho TỪNG cái · `--selftest` N/N ·
`git diff` → CHANGELOG (★ vX.Y.Z) → commit. Deploy CHỜ DUYỆT (xem CLAUDE.md §Quy ước deploy).

⚠ **Bẫy đã dính khi vá r313/r314 — đọc trước khi sửa bất kỳ tệp nào trong gói:** bump VERSION bằng
`pathlib.read_text()/write_text()` **nuốt 307 CRLF của `SKILL.md` và 1766 của `tl.py`** (chế độ text
dịch CRLF→LF). `.gitattributes` khoá `* -text` CHÍNH VÌ manifest hash là byte thật ⇒ phải đi
`read_bytes()/write_bytes()`. Bắt được nhờ `r219_gotchas_nhan_trang_thai` ĐỎ (nó neo
`SKILL.md.stat().st_size`) — nếu không có ca đó thì lỗi này lọt vào gói mà gate vẫn xanh.
Và: sửa tệp NẰM TRONG gói ⇒ **tái sinh `RELEASE_MANIFEST.json`** (kể cả khi chỉ sửa CHANGELOG).

---

## VIỆC 4 — Chốt còn thiếu cho đường ĐỌC (đề xuất, chưa vá)

r281 cưỡng chế `--profile` cho đường **GHI**. Đường **ĐỌC** thì không: thiếu config v2 ⇒
`_apply_profile_env` return sớm ⇒ `_scope_params` trả `{}` ⇒ webapp rơi về registry VBQPPL NỀN,
**`ok:true`, im lặng**. Lượt 02-08 đã dính: mọi số đo registry của lượt đó là của sổ NỀN.

Đề xuất: `reg-query`/`reg_get` echo `registry_scope` (`base` | `profile:<id>`) vào envelope;
WARN LOUD khi `--profile` ≠ nền mà `registryDocId` rỗng.

**Kiểm nhanh trước khi tin BẤT KỲ số đo registry nào:**
```
python scripts/tl.py profile-info --profile "Luật BHXH" --json
```
→ `"profile_found": false` hoặc `"source": "env-only"` ⇒ **đang đọc sổ NỀN**, không phải profile.

---

## Ràng buộc (giữ nguyên)

* Mọi lệnh mang `--profile "Luật BHXH"` — **và kiểm `profile-info` để chắc cờ đó có tác dụng thật**.
* Skill tối thiểu v1.36.20 cho thao tác ghi; nhánh này đang **v1.36.48** (r313→r316).
* Registry: `reg-query --refresh` dò trùng trên dữ liệu TƯƠI trước · readback `--live` hẹp sau ·
  cân nhắc `--expect COL=VAL` khi đường ghi có hỗ trợ.
* 2–3 phiên chạy song song trên cùng cây canonical ⇒ `git status -sb` trước mọi commit + phép kiểm
  chống-xoá-ngược:
  ```powershell
  cd "D:\Quốc hội\tra-luat"; git diff HEAD --numstat | ForEach-Object { $a,$d,$f = $_ -split "`t"; if ([int]$d -gt 0) { Write-Host "`n--- $f ($a+ / $d-)" -ForegroundColor Yellow; git diff HEAD -- $f | Select-String '^-[^-]' | Select-Object -First 6 } }
  ```
* Memory topic `rasoat-hoso-orchestration-plan`: nội dung cần thêm nằm ở biên bản §6
  (container web không có công cụ memory — giống lượt 24/26).
