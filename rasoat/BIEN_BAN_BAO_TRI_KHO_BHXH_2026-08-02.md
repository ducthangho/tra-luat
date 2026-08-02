# BIÊN BẢN LƯỢT BẢO TRÌ KHO — sau khi đóng hồ sơ BHXH (02-08-2026)

Phiên: container Claude Code on the web · nhánh `claude/bhxh-41-2024-maintenance-jncsle`
· HEAD lúc bắt đầu `5c32389` (VERSION 1.36.46 — **cao hơn** mốc v1.36.37/`1a06ff1` mà prompt nêu).
Phạm vi: 2 mục của lượt bảo trì kho. **KHÔNG** gỡ quarantine 41/2024 (tiền đề đã bị bác ở lượt 8).

---

## 0. Kết quả gọn

| Mục | Trạng thái | Ghi chú |
|---|---|---|
| 1. Ghi note chống tái phát vào dòng 41-2024-QH15 | ⏸ **CHƯA GHI — chuyển máy có config** | Payload đã soạn + đã đối chiếu note cũ; container này KHÔNG ghi được (xem §2) |
| 2a. `19-2026-VBHN-VPQH` — bản còn markup sửa đổi | ✅ **Có nguồn thay thế đo đạt** | Công báo 133 (.docx) · 141/141 Điều · 0 số rác · markup={strike:2} = 2 DẤU CÁCH (ngoại lệ có bằng chứng, người dùng đã chốt) |
| 2b. `54-2025-VBHN-VPQH` — khối đầu là chrome trang web | ✅ **Có nguồn thay thế đo đạt** | Công báo 1083+1084 (.pdf text) · 72 Điều · khối đầu sạch sau khi cắt 1 dòng nhãn mục |
| 2c. `89-2026-VBHN-VPQH` — khối đầu thiếu VPQH + «Số:» | ✅ **Có nguồn thay thế đo đạt** | Công báo 222 (.docx) · 79 Điều · `verify_flags` RỖNG · VPQH+«Số:» nằm ở KHỐI KÝ CUỐI (đúng bố cục VBHN) |
| — | ⚠ 6 phát hiện CÔNG CỤ | §4 — **CẢ SÁU ĐÃ VÁ trong chính nhánh này**: §4.1/§4.3 → r314+r315 (v1.36.48) · §4.2/§4.6-phần-RÒ → r316+r317 (v1.36.49) · §4.4/§4.5 → r318 (v1.36.50). Còn duy nhất §4.6 phần KHẾ ƯỚC (`requirements.txt`) |

**Không có thao tác GHI DỮ LIỆU nào trong lượt này** — không ghi registry, không ghi Drive, không
đụng NLM. (Có sửa MÃ: r314+r315 ở §4.1/§4.3, gate xanh — xem cuối §5.) Toàn bộ số đo dưới đây từ lệnh ĐỌC + ingest vào cache TẠM
(`$SCRATCH/cache{B..F}`, ngoài repo, ephemeral theo container).

---

## 1. Xác nhận lại tiền đề đã bác (đo LIVE, không tin mô tả cũ)

`reg-query --refresh` và `reg_get refresh=true` đều trả **đúng 1 dòng**:

```
drive_id   1Ds95NoIdZyRutHGsMS85N4hB61Nglz5eeg0vRZ-XqYM
name       Luat_41-2024-QH15_Bao_hiem_xa_hoi
cat        _ZZZ_QUARANTINE_taluat        corpus  false
nlm_status removed_superseded_by_VBHN    row_kind own
note       "Đã xóa khỏi NLM; thay bằng VBHN 19/VBHN-VPQH (2026)"   (51 ký tự)
```

⇒ Khớp trọn vẹn 4 dữ kiện của prompt. Lý do quarantine là **superseded_by VBHN**, không phải
«là dự thảo». **KHÔNG gỡ quarantine, KHÔNG đặt `corpus=true`.**

### ⚠ `note` KHÔNG chiếu qua `reg-query` — kể cả `--live`

Đã kiểm bằng hành vi (không suy từ code): `reg-query --sohieu … --live --json` trả 17 khoá,
**không có `note`**. Đường đọc `note` DUY NHẤT hiện có là gọi thẳng action `reg_get`:

```python
import sys; sys.path.insert(0, "scripts"); import gas
gas.get("reg_get", profile="Luật BHXH",
        drive_id="1Ds95NoIdZyRutHGsMS85N4hB61Nglz5eeg0vRZ-XqYM", refresh="true")
```

Đây chính là cái bẫy prompt cảnh báo: ghi `--bulk` mà không đọc `reg_get` trước = **đè mất note cũ**.

---

## 2. Mục 1 — VÌ SAO container này KHÔNG được phép ghi

`precheck --profile "Luật BHXH" --cols note --json` → `ok:false`, blocker **critical**:

```
PROFILE_REGISTRY_ID_NOT_EMPTY : profile dự án registryDocId RỖNG
                                → ghi rơi nhánh BASE → CLOBBER registry nền
MANIFEST_FRESH (warn)         : snapshot 1508s > 900s
```

Nguyên nhân gốc: container clone sạch, **không có `tra_luat_config.json` / `.v2.json`**
(chỉ có `tra_luat_config.example.json`). `_load_config_file()` trả `{}` ⇒ `_apply_profile_env()`
return sớm ⇒ `TL_PROFILE` không bao giờ được set ⇒ `_scope_params()` trả `{}`.

### Hệ quả NGHIÊM TRỌNG HƠN blocker (đo được, không suy đoán)

```
config đọc được: False
TL_PROFILE sau _apply_profile_env: ''
TL_REGISTRY_DOC_ID: ''
_scope_params({}) = {}          # ← KHÔNG có registryDocId, KHÔNG có profileName
```

Theo `references/API_CONTRACT.md:16` — *«thiếu ⇒ hằng VBQPPL nền (`BASE_REGISTRY_DOC_ID_`)»*.

⇒ **Cờ `--profile "Luật BHXH"` là NO-OP ở phiên này.** Mọi lệnh ĐỌC của lượt này
(`reg-query`, `reg_get`) đã rơi về **registry VBQPPL NỀN**, không phải registry profile —
im lặng, không cảnh báo. Số đo phụ trợ ủng hộ: manifest cache 1319 dòng, khớp dãy «nền»
1315 dòng đo ngày 31-07 (`KETQUA_GHI_KHO_NEN_2026-07-31.md` §0) chứ không phải một registry profile riêng.

> **Bài học mới, cùng họ với r281:** r281 cưỡng chế cho đường **GHI** (blocker chặn thật).
> Đường **ĐỌC** thì KHÔNG có chốt tương ứng: thiếu config ⇒ `--profile` bị nuốt lặng lẽ và
> kết quả đọc vẫn `ok:true`. Người vận hành không có cách nào biết mình đang đọc sổ nào.
> Đề xuất vá: `reg-query`/`reg_get` echo `registry_scope` (`base` | `profile:<id>`) vào envelope,
> và WARN LOUD khi `--profile` ≠ nền mà `registryDocId` rỗng.

### Chốt của người dùng (đã hỏi trong phiên)

> **«Bạn chạy trên máy Windows»** — mục 1 chuyển sang máy có config. Container này KHÔNG ghi.

Payload đã soạn sẵn: **`rasoat/pending_note_41-2024_bulk_2026-08-02.json`**
(1 item, `drive_id` đầy đủ 44 ký tự copy TỪ DỮ LIỆU NGUỒN, không gõ tay — bài học lượt 20 §2.3).

Đã kiểm bằng máy, không bằng mắt:

```
giữ nguyên note cũ làm tiền tố: True
độ dài: 51 → 746
```

Lệnh để chạy trên máy có config (Windows, PowerShell) — **theo đúng thứ tự**:

```powershell
cd "D:\Quốc hội\tra-luat"
git fetch origin claude/bhxh-41-2024-maintenance-jncsle
git checkout claude/bhxh-41-2024-maintenance-jncsle

# (1) ĐỌC note TƯƠI trên ĐÚNG sheet profile — đối chiếu tiền tố trước khi ghi
python -c "import sys; sys.path.insert(0,'scripts'); import gas, json; print(json.dumps(gas.get('reg_get', profile='Luật BHXH', drive_id='1Ds95NoIdZyRutHGsMS85N4hB61Nglz5eeg0vRZ-XqYM', refresh='true'), ensure_ascii=False, indent=1))"
#   → nếu `note` KHÁC "Đã xóa khỏi NLM; thay bằng VBHN 19/VBHN-VPQH (2026)" thì DỪNG:
#     phiên khác vừa ghi. Soạn lại phần NỐI trên nền note mới rồi mới chạy tiếp.

# (2) cổng ghi phải XANH trước
python scripts\tl.py manifest --profile "Luật BHXH"
python scripts\tl.py boot --refresh --profile "Luật BHXH"
python scripts\tl.py precheck --profile "Luật BHXH" --cols note --json    # phải ok:true, blockers rỗng

# (3) GHI — ⚠ `register --bulk` GHI NGAY, KHÔNG có chế độ DRY (bẫy đã trả giá lượt 20 §2.1)
python scripts\tl.py register --bulk rasoat\pending_note_41-2024_bulk_2026-08-02.json --cols note --profile "Luật BHXH"

# (4) READBACK keyed — rc/ok KHÔNG BAO GIỜ là bằng chứng ghi (lượt 20 §2.2)
python -c "import sys; sys.path.insert(0,'scripts'); import gas; r=gas.get('reg_get', profile='Luật BHXH', drive_id='1Ds95NoIdZyRutHGsMS85N4hB61Nglz5eeg0vRZ-XqYM', refresh='true'); n=r['rows'][0]['note']; print(len(n)); print(n)"
#   → PHẢI ra 746 ký tự và bắt đầu bằng note cũ.
```

**Không dùng `--expect` được cho lô này:** chốt CAS r279 chỉ cài trên đường ĐƠN
(`register --drive-id`, `source_ops.py:432`), mà đường đơn KHÔNG ghi được `note`
(`_REG_FIELDS` tại `source_ops.py:465` không có `note`). Đường `--bulk` — đường DUY NHẤT ghi
được `note` — thì nhánh `--expect` nằm SAU `return` của nhánh bulk nên không bao giờ chạy.
⇒ Chống va chạm phải làm THỦ CÔNG bằng bước (1) ngay sát bước (3).
*(`note` ĐÃ có trong `_REGISTER_EXPECT_COLS` — chỉ thiếu đường dẫn tới nó ở nhánh bulk.)*

---

## 3. Mục 2 — ba khiếm khuyết nguồn: nguồn thay thế + SỐ ĐO

### 3.1 Nguồn đã tìm được (Công báo, official-first)

| Số hiệu | Trang Công báo | Tệp tải | sha256 (tệp tải NGUYÊN TRẠNG) |
|---|---|---|---|
| 19-2026-VBHN-VPQH | [468972](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-19-vbhn-vpqh-468972.htm) · CB **133** ngày 28-02-2026 · ký 12-02-2026 | `.docx` 150.626 B | `3137d671…2c2283f5` |
| 54-2025-VBHN-VPQH | [45821](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-54-vbhn-vpqh-45821.htm) · CB **1083+1084** ngày 23-8-2025 · ký 11-8-2025 | `.pdf` 979.862 B | `00d77770…6089a4c6` |
| 89-2026-VBHN-VPQH | [469264](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-89-vbhn-vpqh-469264/64065.htm) · CB **222** ngày 16-04-2026 · ký 27-3-2026 | `.docx` 115.494 B | `deff1349…1266c9be` |

Đã chống nhầm số hiệu **có năm** (bất biến VBHN):
`54/VBHN-VPQH` có HAI văn bản (Ban hành VBQPPL 2025 · Hải quan 469184) — đã neo bằng
«Ngày ban hành 11/08/2025 · hợp nhất Luật Ban hành VBQPPL · người ký Lê Quang Tùng».
`89/VBHN-VPQH` cũng có HAI (MTTQ 2025 id 45980 · NSNN 2026 id 469264) — đã neo bằng
«27/03/2026 · hợp nhất Luật NSNN · Lê Quang Mạnh», khớp `89-2026-VBHN-VPQH` trong registry.

### 3.2 Số đo NĂM CỔNG (bản tốt nhất của mỗi văn bản)

| Cổng | 19-2026 (.docx) | 54-2025 (.pdf, đã cắt tay) | 89-2026 (.docx) |
|---|---|---|---|
| đủ Điều | **141** | **72** | **79** |
| khối đầu ≥ 250 ký tự | 839 ✅ | 860 ✅ | 560 ✅ |
| markup rỗng | ⚠ `{strike: 2}` | `None` ✅ | `None` ✅ |
| doc_key trùng bản cũ | `19-2026-vbhn-vpqh--consolidated` | `54-2025-vbhn-vpqh--consolidated` | `89-2026-vbhn-vpqh--consolidated` |
| khối đầu có quốc hiệu | ✅ | ✅ | ✅ |
| số hiệu neo được (T1) | ✅ khối ký cuối | ✅ | ✅ khối ký cuối |
| `verify_flags` còn lại | 1 (MARKUP_SUA_DOI) | 2 (LOC_CONG_BAO + 1 dương-tính-giả §4.4) | **0 — sạch** |
| số rác ≥9 chữ số | **0** | **0** | **0** |

> `doc_key` mới **phải đối chiếu với bản cũ trên máy bạn** trước khi chép đè — container này
> không có `~/.tra_luat_cache/docs/` (cache tài liệu là per-máy, `cache-snapshot` chỉ gói
> `manifest_index`, KHÔNG gói `docs/`). Cả ba đều theo khuôn `<sohieu-gạch-nối>--consolidated`
> nên khớp nếu bản cũ cũng `variant=consolidated`.

### 3.3 «Khối đầu thiếu VPQH + dòng Số:» — KHÔNG phải khiếm khuyết nguồn

Đã bóc `word/document.xml` của cả 19-2026 lẫn 89-2026: **«VĂN PHÒNG QUỐC HỘI» và «Số: NN/VBHN-VPQH»
CÓ trong văn bản** — nằm trong bảng **XÁC THỰC VĂN BẢN HỢP NHẤT ở CUỐI** (19-2026: vị trí
183.972/184.114). Đó là bố cục CHUẨN của VBHN: khối ký/xác thực đặt cuối, không phải letterhead đầu.

⇒ Đi tìm «nguồn tốt hơn» sẽ KHÔNG bao giờ chữa được mục 2c. Cổng đúng phải là
«số hiệu neo được ở khối đầu **HOẶC** khối ký cuối» — đúng như `sohieu_corroborated()` đã thiết kế
(`verify_deep.py:64`). Với bản Công báo, cổng đó **ĐẠT** (xem §4.1 vì sao ban đầu nó báo trượt).

### 3.4 `19-2026` — ngoại lệ markup CÓ BẰNG CHỨNG

`markup={strike: 2}`. Đã bóc nguyên văn HAI run bị gạch: **cả hai chỉ chứa MỘT DẤU CÁCH**,
không có chữ nào. Văn bản sau `strip` đọc liền mạch, không dính chữ:

> «…Quyết định của Tòa án hủy bỏ quyết định tuyên bố mất tích **hoặc hủy bỏ** quyết định tuyên bố
> là đã chết đối với trường hợp quy định điểm b khoản 3 Điều 75 của Luật này.»

**Phản chứng đã chạy — bản PDF Công báo XẤU HƠN, không tốt hơn.** Nạp thử `19-2026.pdf`
(3.7 MB, 80 trang) cho `markup=None` nhưng đổi lấy khiếm khuyết NẶNG hơn: `pdftotext` **trộn
CHÚ THÍCH vào thân Điều**. Đối chiếu 141 Điều PDF vs DOCX: **13 Điều lệch**, trong đó

* **Điều 1**: PDF 1.360 ký tự vs DOCX 452 — PDF nhét ~900 ký tự «căn cứ ban hành» của BỐN luật
  khác (73/2025, 84/2025, 113/2025, 142/2025) vào THÂN Điều 1. Ai hỏi «nguyên văn Điều 1
  Luật BHXH» sẽ nhận cả lời văn của Luật Nhà giáo/Thanh tra/Dân số/Phục hồi phá sản.
* **Điều 16, 37**: lạc số chú thích («2», «4») vào thân Điều.
* Khối đầu PDF còn 3 dòng chữ ký số mà `--loc-congbao` **không bỏ** (`chu_ky_so=0` — mẫu 4 dòng
  không khớp biến thể 3 dòng này, xem §4.5).

⇒ Chọn `.docx`. Người dùng đã chốt trong phiên: **«Nhận .docx, ghi nhận strike=2»**.

### 3.5 `54-2025` — cắt tay MỘT dòng, có phản chứng

`--loc-congbao` bỏ 62 dòng (dòng chạy 58 · chữ ký số 4), 127.302 → 122.791 ký tự
(bằng chứng từng dòng: `rasoat/loc_congbao_audit_54-2025_2026-08-02.json`).
Còn sót **đúng 1 dòng** nhãn mục Công báo ở đầu — `VĂN BẢN PHÁP LUẬT KHÁC` (dòng 10 của bản bóc).
Cắt tay đúng dòng đó rồi nạp lại:

```
doc_key giống:  True        n_dieu: 72 → 72        chars: 122791 → 122747
khối đầu: 894 → 860 ký tự   Điều khác nhau giữa 2 bản: KHÔNG (0)
```

⇒ **0/72 Điều bị đụng** — thao tác cắt chỉ chạm khối đầu. Khối đầu mới bắt đầu đúng ở
`VĂN BẢN HỢP NHẤT - VĂN PHÒNG QUỐC HỘI`.

### 3.6 Tái lập y hệt (mọi bước, kể cả bước sửa tệp)

**Điều kiện môi trường** (container sạch KHÔNG có, phải cài — xem §4.2/§4.3):

```bash
apt-get update && apt-get install -y --no-install-recommends poppler-utils   # pdftotext
pip install pypdf cffi python-docx
```

**Hoàn chỉnh chuỗi cert cho `g7.cdnchinhphu.vn`** (máy chủ gửi THIẾU intermediate;
KHÔNG tắt xác minh TLS — nạp đúng intermediate từ AIA rồi verify vẫn BẬT đầy đủ):

```bash
curl -sS http://secure.globalsign.com/cacert/gsrsaovsslca2018.crt -o inter.der
openssl x509 -inform DER -in inter.der -out inter.pem     # GlobalSign RSA OV SSL CA 2018
cat "$SSL_CERT_FILE" inter.pem > bundle-completed.pem      # → dùng cho curl --cacert
```

**Sửa container .docx của Công báo** (§4.2 — tên entry dùng `\` thay `/`):

```python
import sys, zipfile
src, dst = sys.argv[1], sys.argv[2]
zin = zipfile.ZipFile(src)
with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zo:
    for it in zin.infolist():
        zo.writestr(it.filename.replace("\\", "/"), zin.read(it.filename))
```

**Nạp cache** — ⚠ `--so-hieu` phải dùng dạng **GẠCH NỐI** `NN-YYYY-VBHN-XXX`, KHÔNG dùng dạng
gạch chéo (§4.1):

```bash
python scripts/ingest_to_cache.py --so-hieu "19-2026-VBHN-VPQH" --method file \
  --input 19-2026-VBHN-VPQH.fixed.docx --cache-dir <TẠM> --variant consolidated \
  --title "Luật Bảo hiểm xã hội" --issuing-agency "Văn phòng Quốc hội" \
  --effective-status in_force --officialness official \
  --goc "41-2024-QH15;73-2025-QH15;84-2025-QH15"

python scripts/ingest_to_cache.py --so-hieu "89-2026-VBHN-VPQH" --method file \
  --input 89-2026-VBHN-VPQH.fixed.docx --cache-dir <TẠM> --variant consolidated \
  --title "Luật Ngân sách nhà nước" --issuing-agency "Văn phòng Quốc hội" \
  --effective-status in_force --officialness official --goc "89-2025-QH15;145-2025-QH15"

# 54: bóc PDF → bỏ ĐÚNG dòng "VĂN BẢN PHÁP LUẬT KHÁC" → nạp .txt (--loc-congbao vẫn chạy trên TEXT)
python scripts/ingest_to_cache.py --so-hieu "54-2025-VBHN-VPQH" --method file \
  --input 54-2025-cut.txt --cache-dir <TẠM> --variant consolidated \
  --title "Luật Ban hành văn bản quy phạm pháp luật" --issuing-agency "Văn phòng Quốc hội" \
  --effective-status in_force --officialness official --goc "64-2025-QH15;87-2025-QH15" --loc-congbao
```

**CHƯA chép đè bản cũ.** Trình tự còn lại (làm trên máy có cache thật): nạp vào cache TẠM →
`doc-compare` bản tạm vs bản cũ → xác nhận `doc_key` trùng và số Điều không GIẢM → mới chép đè.
`method_rank=50` (`file`) THẤP hơn `exportdocx` (95); nếu bản cũ đang `method_rank=95` +
`evidence_status=verified` thì chép đè sẽ **HẠ hạng** — cân nhắc nâng bằng đường
`exportdocx` sau khi đẩy tệp lên Drive, hoặc chấp nhận hạ hạng có chủ đích và ghi rõ.

---

## 4. Năm phát hiện CÔNG CỤ (không phát hiện nào lộ ra bằng đọc code — đều do chạy thật)

### 4.1 `sohieu_corroborated` mù với dạng số hiệu GẠCH CHÉO ⇒ `T1-nhẹ` dương tính giả

`verify_deep.py:84` dùng `_VBHN_WITHYEAR_RE = ^(\d+)-(\d{4})-VBHN-(.+)$` — **chỉ nhận dạng gạch nối**.
Nhưng `ingest_to_cache --help` ghi *«Số hiệu canonical, vd 18/VBHN-VPQH»*, tức hướng dẫn người dùng
gõ dạng **gạch chéo**. Đo:

```
_VBHN_WITHYEAR_RE.fullmatch('54/2025/VBHN-VPQH') → False    corroborated(...) = False   ← trượt oan
_VBHN_WITHYEAR_RE.fullmatch('54-2025-VBHN-VPQH') → True     corroborated(...) = True
```

Cả 3 văn bản đều báo `T1-nhẹ: số '…' không thấy ở khối đầu lẫn khối ký cuối` khi nạp bằng dạng
gạch chéo, và **hết sạch** khi nạp bằng dạng gạch nối — dù tệp y hệt. Cùng họ lỗi với
★ v1.35.57/r221 (`re.escape(so_hieu.split("/")[0])`).

> ✅ **ĐÃ VÁ — r314 (v1.36.48), cùng nhánh này.** Nắn ngăn cách của BẢN SAO cục bộ ngay trước
> `fullmatch`; **KHÔNG** nới `_VBHN_WITHYEAR_RE` dùng chung (ở `classify`/`hygiene`/`resolve`/
> `lookup_ops` nó canh đúng bất biến khoá registry). Khoá bằng 2 ca:
> `r314_sohieu_corroborated_nhan_dang_gach_cheo` (chiều thuận + PARITY hai dạng) và
> `r314_khong_noi_regex_dung_chung` (chiều ngược — ĐỎ nếu ai vá bằng cách nới regex chung).

### 4.2 `.docx` tải từ `g7.cdnchinhphu.vn` là container HỎNG — và `scan_file` FAIL-OPEN che mất

Tên entry trong zip dùng `\` thay `/` (19-2026: 33/40 entry · 89-2026: 30/37) ⇒ **không có**
`word/document.xml` theo tên chuẩn. Đường nạp fail-CLOSED đúng
(`SOURCE_CONTAINER_READ_FAILED`), nhưng `docx_markup.scan_file()` (`docx_markup.py:133`)
nuốt mọi exception và trả **mọi thể = 0**:

```
scan_file(bản HỎNG)     → {} → tôi đã kết luận SAI "SẠCH markup"
scan_file(bản đã sửa)   → {'strike': 2}          ← sự thật
```

Docstring nói đây là chủ ý («docx hỏng → coi như sạch markup»), nhưng markup là **TÍN HIỆU PHÁP LÝ**
(chính `docx_markup.py` mở đầu bằng «lỗi ĐÚNG-SAI về nội dung pháp luật»). Một cổng an toàn pháp lý
mà mặc định «sạch» khi không đọc được là fail-open. Hôm nay vô hại vì đường nạp chặn trước;
sẽ CÓ HẠI ngay khi có reader chịu được tên entry `\` (LibreOffice/Word đều mở được tệp này).
**Vá đề xuất:** `scan_file` trả `{"_unreadable": True}` thay vì `{}` và để caller khai báo LOUD.

> ✅ **ĐÃ VÁ — r316 (v1.36.49), cùng nhánh này.** `scan_file` trả `{UNREADABLE: True}`; `warn_line`
> có nhánh KÊU TO riêng; `normalize_document` khai `MARKUP_KHONG_DOC_DUOC` **tách khỏi**
> `MARKUP_SUA_DOI`; `lookup_ops` khai `markup_unreadable` + `markup_found=True` (fail-CLOSED).
> ★Phát hiện thêm **ca thứ hai** của cùng lỗ, nằm sẵn trong selftest: `r188_docx_reader_bounded_wired`
> ĐANG đòi `sum(scan_file(bomb).values()) == 0` cho docx vượt trần zip-bomb — tức khế ước cũ ghi
> thành văn rằng «không đo được ⇒ báo sạch». Ca đó đã đổi sang đòi cờ `UNREADABLE`.
> Tài liệu SẠCH vẫn IM LẶNG (ca `r316_tai_lieu_sach_van_im_lang` giữ chốt).

### 4.3 `assert_pdf_not_scanned` báo «bản SCAN» khi thực ra là **THIẾU THƯ VIỆN**

`pdf_text_layer_chars()` (`ingest_to_cache.py:211`) thử `pdfplumber` rồi `pypdf`; thiếu **cả hai** →
`return 0` → `assert_pdf_not_scanned` ném `ScannedPDFError`. `requirements.txt` ghi rõ
*«uses only Python standard library»* ⇒ **cài sạch thì KHÔNG có cái nào**.

Đo trên `54-2025-g7.pdf` (PDF text thật, `pdftotext` bóc được **167.433 ký tự**, trang 1 có 2.536 ký tự):

```
chưa cài pypdf : {"ok": false, "reason": "scanned_pdf", "message": "…chỉ 0 ký tự text ở trang đầu…"}
đã cài pypdf   : {"ok": true, …, "n_articles": 72}
```

Thông điệp còn CHỈ SAI đường sửa — *«hãy chuyển sang nguồn web TEXT khác»* — đẩy người vận hành đi
săn nguồn không tồn tại, trong khi lỗi nằm ở máy mình. **Vá đề xuất:** tách «không đo được» khỏi
«đo được = 0»; thiếu thư viện ⇒ `PDF_PROBE_UNAVAILABLE` + hướng dẫn cài, KHÔNG kết luận về tài liệu.

> ✅ **ĐÃ VÁ — r315 (v1.36.48), cùng nhánh này.** `pdf_text_layer_chars` trả `None` = KHÔNG ĐO ĐƯỢC
> (khác hẳn `0`); lớp lỗi riêng `PdfProbeUnavailableError` **không** kế thừa `ScannedPDFError`;
> handler `__main__` thêm `reason: "pdf_probe_unavailable"` + `action: "install_dep"` + **exit 6**.
> Vẫn fail-CLOSED, chỉ đổi thông điệp về đúng thủ phạm. Tiện thể sửa lỗi **cộng dồn** giữa hai
> đường dò (bản cũ nuôi chung biến `total`). Khoá bằng
> `r315_thieu_thu_vien_khong_bi_goi_la_ban_scan` + `r315_do_duoc_0_van_la_ban_scan`.
> **Chưa làm:** `requirements.txt` vẫn khai stdlib-only (đụng khế ước cài đặt của gói — tách lượt).

### 4.4 `CB_DAU_MUC` sai CẢ HAI CHIỀU trên cùng một tệp

Mẫu `^\s*(?:VĂN\s+BẢN\s+QUY\s+PHẠM\s+PHÁP\s+LUẬT|PHẦN\s+…)\s*$` (`verify_deep.py`) trên `54-2025`:

* **Dương tính giả — dòng 1578**: đó là dòng thứ ba của TIÊU ĐỀ CHƯƠNG bị xuống dòng
  («Chương VI / HIỆU LỰC VÀ NGUYÊN TẮC ÁP DỤNG / **VĂN BẢN QUY PHẠM PHÁP LUẬT**»).
  Lời khuyên kèm theo — *«Cắt tay tới dòng mang số hiệu rồi nạp lại»* — nếu làm theo đúng chữ
  sẽ **XOÁ SẠCH Chương I–V**. Cảnh báo này nguy hiểm hơn thứ nó cảnh báo.
* **Âm tính giả — dòng 10**: nhãn mục THẬT `VĂN BẢN PHÁP LUẬT KHÁC` **không nằm trong mẫu**
  nên không bị bắt.

*(Chú ý khi đọc cờ: chỉ số dòng trong cảnh báo tính trên văn bản **TRƯỚC** lọc, không phải sau —
`con_dau_muc` liệt kê trên `lines` gốc.)*

> ✅ **ĐÃ VÁ — r318 (v1.36.50), cùng nhánh này.** Mẫu nhận thêm `VĂN BẢN PHÁP LUẬT KHÁC` (+ tiền tố
> `PHẦN` tuỳ chọn); loại trừ dương-tính-giả bằng phép nhìn lui ≤2 dòng không-trống (gặp
> `Chương|Phần|Mục <số>` đứng một mình ⇒ là tiêu đề bị xuống dòng, không báo); lời khuyên viết lại,
> chỉ đúng dòng cần bỏ + cảnh báo TƯỜNG MINH đừng cắt theo neo `Số:`.
> Nghiệm thu 54-2025: cảnh báo chuyển từ dòng **1578** (tiêu đề Chương) sang dòng **10** (nhãn THẬT).
> ★GIỮ quyết định gốc r217: chỉ KHAI BÁO, KHÔNG tự bỏ — bytes corpus đã nạp không đổi.

### 4.5 Khối chữ ký số Công báo có biến thể **3 dòng**, `CB_CHU_KY_SO` chỉ khớp mẫu 4 dòng

PDF `19-2026` mở đầu bằng `Ký bởi:` / `Cơ quan:` / `Ngày ký:` (3 dòng) — `--loc-congbao` báo
`chu_ky_so=0`, ba dòng chrome này **lọt vào khối đầu**. PDF `54-2025` dùng mẫu 4 dòng
(`Người ký:` / `Email:` / `Cơ quan:` / `Thời gian ký:`) và bị bỏ đúng 4/4.

> ✅ **ĐÃ VÁ — r318 (v1.36.50), cùng nhánh này.** Tập nhãn đóng + dò dãy liền 3–4 dòng, thứ tự tự do,
> thử dãy DÀI trước. ★Dãy bắt buộc chứa nhãn người-ký, nếu không thì vài dòng thân bài mở đầu bằng
> «Cơ quan:»/«Ngày ký:» đủ để nuốt mất quy phạm (ca `r318_khong_nuot_than_van_ban` khoá).
> Nghiệm thu 19-2026: `chu_ky_so` 0 → **3**, khối đầu bắt đầu đúng ở quốc hiệu, 141/141 Điều giữ nguyên.

### 4.6 (phụ) Thiếu `python-docx` ⇒ **số neo hình vẽ lọt vào thân Điều**

Nhánh bóc-tag dự phòng nhặt cả trị `wp:posOffset`. Đo trước/sau khi cài `python-docx`:

| | trước | sau |
|---|---|---|
| 19-2026 | 3 số rác (`2927786221920` ở khối đầu · 2 số ở Điều 141) | **0** |
| 89-2026 | 3 số rác — trong đó Điều 72 dính chuỗi **59 chữ số** | **0** |
| 89-2026 `verify_flags` | 1 cờ | **0 — rỗng** |

⇒ `python-docx` (và `pypdf`) thực chất là **phụ thuộc bắt buộc để nạp đúng**, không phải tuỳ chọn.

> ✅ **ĐÃ VÁ (phần RÒ) — r317 (v1.36.49), cùng nhánh này.** `drop_drawing_measures()` bỏ nội dung
> element thuộc `wp:`/`wp14:` TRƯỚC khi bóc tag, ở **cả hai** reader bóc-tag (`plain_from_document_xml`
> và `_docx_zip_text`). Nghiệm thu end-to-end (chặn `python-docx` để ép đúng nhánh rò): 19-2026 và
> 89-2026 đều **3 số rác → 0**, số Điều giữ nguyên 141/79.
> Ba bất biến khoá bằng test: không-drawing ⇒ chuỗi ra = chuỗi vào · text-box sống sót · số dài
> THẬT trong `w:t` không bị đụng.
> ⚠ **Bẫy giữa chừng:** regex đầu viết `wp14?` — parse ra `"wp1"`+`"4"` tuỳ chọn nên KHÔNG khớp
> `wp:` trần; `wp14:pctWidth` bị bỏ còn `wp:posOffset` vẫn lọt, ra chuỗi số **CỤT** trông như đã
> sửa xong. Chỉ đếm lại trên tệp thật mới thấy. Đúng là `wp(?:14)?`.
> **CHƯA vá phần khế ước:** `requirements.txt` vẫn khai stdlib-only. r317 làm nhánh không-`python-docx`
> hết rò, nhưng `pypdf` KHÔNG có đường thay thế — thiếu nó là mọi PDF bị chặn (r315). Lượt riêng.
`requirements.txt` hiện nói ngược lại. **Vá đề xuất:** hoặc thêm vào `requirements.txt`, hoặc để
`doctor`/`precheck` CẢNH BÁO LOUD khi thiếu, kèm hệ quả cụ thể.

---

## 5. Việc còn treo (KHÔNG làm trong lượt này)

1. **Ghi note mục 1** — chờ chạy trên máy có config (lệnh nguyên văn ở §2). Payload đã commit.
2. **Chép đè 3 record cache** — chờ máy có `~/.tra_luat_cache/docs/`; phải `doc-compare` với bản cũ
   và quyết về `method_rank` 95 → 50 (§3.6).
3. **Phát hiện công cụ §4** — **CẢ SÁU ĐÃ VÁ** trong chính nhánh này:
   **§4.1→r314 · §4.3→r315** (v1.36.48) · **§4.2→r316 · §4.6 phần RÒ→r317** (v1.36.49) ·
   **§4.4+§4.5→r318** (v1.36.50).
   Cổng lượt cuối: selftest **1604/1604** · ruff F **delta so master = 0** · golden 0-diff ·
   determinism ok · doc-claims 9/9 layer = 0 · `release-verify` 177/177 + `package_hash` khớp ·
   `RELEASE_MANIFEST.json` đã tái sinh.
   **§4.4/§4.5 → r318 (v1.36.50)**: khối chữ ký số 3 dòng hết lọt vào khối đầu (19-2026:
   `chu_ky_so` 0→3) · nhãn mục hết sai hai chiều (54-2025: cờ chuyển từ dòng 1578 sang dòng 10)
   · lời khuyên «cắt tới dòng Số:» — thứ sẽ xoá sạch thân VBHN — đã thay bằng chỉ dẫn an toàn.
   Còn treo DUY NHẤT: **§4.6 phần khế ước** (`requirements.txt` vẫn khai stdlib-only, mà `pypdf`
   KHÔNG có đường thay thế — thiếu nó là mọi PDF bị chặn).
   ⚠ **Hai bẫy đã dính khi vá, ghi vì không cái nào lộ ra bằng đọc code:**
   (a) bump VERSION bằng `read_text()/write_text()` nuốt 307 CRLF của `SKILL.md` + 1766 của `tl.py`
   (`.gitattributes` khoá `* -text` CHÍNH VÌ manifest hash là byte thật ⇒ phải `read_bytes()/write_bytes()`);
   bắt được nhờ `r219_gotchas_nhan_trang_thai` ĐỎ.
   (b) regex `wp14?` parse ra `"wp1"`+`"4"` tuỳ chọn nên KHÔNG khớp `wp:` trần ⇒ nửa số bị bỏ, ra
   chuỗi CỤT trông như đã sửa xong; chỉ đếm lại trên tệp thật mới thấy. Đúng là `wp(?:14)?`.
   (c) `\b` KHÔNG khớp trước dấu gạch dưới ⇒ lượt đánh số lại đổi được chú thích mà SÓT tên ca
   selftest (`r313_…`), đúng lúc master vừa mang `r313_anchor_*` vào — hai thay đổi khác nhau dùng
   chung tiền tố. Đổi số phải theo TÊN ĐẦY ĐỦ, tường minh.
   (d) phép giải xung đột merge ghi `VERSION` thêm ký tự xuống dòng cuối (7B→8B); `package_hash`
   tính trên byte THẬT nên phải so byte với master TRƯỚC khi commit, không chỉ so nội dung.

5. **⚠ ĐỤNG SỐ đã xảy ra trong lượt này:** master tiến lên `c24a8b3` (Merge PR #12) và lấy
   **r313 + v1.36.47** cho RAS-17 — trùng số nhánh này đang dùng. Đã nhường số theo tiền lệ
   r309/PR #9 trong CLAUDE.md: r313→r314 … r316→r317, v1.36.47/48 → v1.36.48/49, rồi mới hoà
   master. Bài học: nhánh mở LÂU phải `git fetch origin master` + đối chiếu `max_r` **trước mỗi
   lượt bump**, không chỉ lúc mở nhánh.

6. **Memory topic `rasoat-hoso-orchestration-plan`** — container này KHÔNG có công cụ memory
   (giống lượt 24/26 đã ghi trong `KETQUA_NLM_QA_QB_QC_2026-07-31.md:169`). Nội dung cần thêm ở §6.

---

## 6. Nội dung cần thêm vào memory topic `rasoat-hoso-orchestration-plan`

```
Lượt bảo trì kho 02-08-2026 (nhánh claude/bhxh-41-2024-maintenance-jncsle):
· 41/2024 QUARANTINE ĐÚNG — superseded_by VBHN 19-2026-VBHN-VPQH. KHÔNG gỡ. Tiền đề Q-APPROVALS
  gốc đã bác lượt 8; note chống tái phát đã SOẠN (rasoat/pending_note_41-2024_bulk_2026-08-02.json)
  nhưng CHƯA GHI — container web không có config v2.
· ⚠ Container clone sạch KHÔNG có tra_luat_config.json ⇒ `--profile` là NO-OP và mọi lệnh ĐỌC rơi
  về registry NỀN, IM LẶNG. Đường GHI có chốt (r281), đường ĐỌC thì KHÔNG. Kiểm bằng
  `tl profile-info --json` → `profile_found:false` TRƯỚC khi tin bất kỳ số đo registry nào.
· `note` không chiếu qua reg-query kể cả --live → phải gọi action reg_get. `--expect` (CAS r279)
  KHÔNG dùng được cho lô ghi note vì chỉ có nhánh --bulk ghi được note mà nhánh đó không có --expect.
· 3 khiếm khuyết nguồn đã có bản thay thế Công báo đo đạt (19-2026 CB133 .docx · 54-2025 CB1083+1084
  .pdf · 89-2026 CB222 .docx). «Khối đầu thiếu VPQH+Số:» KHÔNG phải lỗi nguồn — VBHN đặt khối
  xác thực ở CUỐI theo đúng thể thức.
· 6 phát hiện công cụ chờ vá — xem rasoat/BIEN_BAN_BAO_TRI_KHO_BHXH_2026-08-02.md §4.
```
