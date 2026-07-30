# KẾT QUẢ LƯỢT DỌN KHO NỀN — 2026-07-31 (lượt 19)

**Phạm vi:** 6 việc kho NỀN bàn giao từ lượt 18 (`KETQUA_VIEC_TREO_BHXH_2026-07-30.md` §7/§9;
định nghĩa B2/B2b/B3/B5 tại `RASOAT_PROFILE_LUAT_BHXH_2026-07-29.md` §B).
**Kỷ luật lượt:** 0 ghi Drive · 0 ghi registry · 0 NLM · 0 `--apply` · 0 đổi mã.
Mọi lệnh đã chạy đều CHỈ ĐỌC: `reg-query --refresh [--base-also]` · `registry-doctor --json` ·
`doctor --json` · `vbhn-year-fix` (DRY) · `doc-text` · `doc-compare`.

**Nền đo đầu lượt:** master `cc20b71` = **r268 / v1.36.6** (repo đã tiến r266→r268 sau lượt 18 —
lại đúng bài học «repo không đứng yên»), cây sạch, `0 0` với origin;
`deploy-guard.ps1 -Version 1.36.6` → **exit 3 = Drive ĐANG ở v1.36.6 ⇒ NỢ DEPLOY = 0**.
Kho nền đo tươi: `reg-query --refresh --base-also` = **1347 dòng**.

## Bảng chốt 6 việc

| # | Việc | Kết cục |
|---|------|---------|
| 1 | Topology notebook `80742228` | **ĐÓNG BẰNG ĐO — không cần ghi gì** (§1) |
| 2 | 2 dòng `Luat_74-2025-QH15` trùng | Đo xong, IDENTICAL — **đề xuất note, chờ duyệt** (§2) |
| 3 | B2 — cặp `18-2026-VBHN-VPQH` | **Nay là 3 dòng, không phải 2** — đo xong, đề xuất chờ duyệt (§3) |
| 4 | B3 — cụm trùng/thiếu năm | Đo đủ năm 6/6 dòng — **đề xuất 6 reg_upsert sohieu, chờ duyệt** (§4) |
| 5 | B5 — 5 dòng sohieu nền trần | **4/5 tự đóng bằng đo** (đã biến mất); dòng 5 thành cặp trùng 60-2026 (§5) |
| 6 | B2b — cơ sở đếm registry-doctor | **ĐÓNG BẰNG ĐO — r251 đã làm xong việc này, đang LIVE** (§6) |

---

## 1. Topology notebook `80742228` — ĐÓNG, không có việc ghi

- Config `tra_luat_config.v2.json` **ĐÃ khai** notebook này: `profiles."Khảo sát Luật Xuất bản".notebookId
  = 80742228-ba7a-481c-bd8e-d4115876ed6e`. 54 dòng nền mang `nlm_notebook_id` này đều
  `cat=Van_ban_thuong/Khảo sát Luật Xuất bản`, `row_kind=own`, `corpus=false`, `nlm_status=pushed` — là
  hồ sơ khảo sát Luật Xuất bản, KHÔNG phải rác.
- Cơ chế: `_resolve_shard_topology` (nlm_ops.py:691) gom notebookId của **mọi profile khác** vào
  `foreign_notebooks`; `_topology_row_kind_findings` (nlm_ops.py:847-850) **bỏ qua** dòng thuộc foreign
  ⇒ không còn đường nào sinh `UNKNOWN_NOTEBOOK_NOT_IN_TOPOLOGY` cho notebook này.
- Đo tươi 31-07: `registry-doctor --profile vbqppl --json` → 0 lần chuỗi `80742228`, 0 UNKNOWN;
  `doctor --profile vbqppl --json` → `topology.ok=true`, 3 shards, `config_findings=[]`, 0 UNKNOWN.
- ⇒ Ghi chú C1b (29-07, «3 dòng UNKNOWN_NOTEBOOK») đã **LỖI THỜI** — config đã khai profile từ sau đó.

## 2. `Luat_74-2025-QH15` — 2 dòng, phân xử xong, chờ duyệt note

| drive_id | cat | corpus | nlm |
|---|---|---|---|
| `1PfTsnRYtcpTbMNqnr_4lO8n7GyWGmBmTSHC79IR66a0` | 20_Lao_dong | true | pushed (canonical) |
| `1mGRs4vsTZDO9XBqXy6Jp_ZU6JcObttnvrGzQLauP54A` | _ZZZ_QUARANTINE_taluat | false | — (cờ RAW_NAME_NOT_NLM) |

`doc-compare` hai bản: **IDENTICAL, jaccard 1.0, 56.875 = 56.875 ký tự** ⇒ bản quarantine là bản
trùng tuyệt đối, đúng chỗ (quarantine), chỉ thiếu chú dẫn. **Đề xuất:** gắn `note` trỏ canonical
(nhóm GHI-2 dưới). KHÔNG xoá dòng/file.

## 3. B2 — `18-2026-VBHN-VPQH` nay là BA dòng (sổ cũ ghi 2)

| drive_id | name | cat | corpus | nlm | đo nội dung vs canonical |
|---|---|---|---|---|---|
| `1gJn-6pjj2IM…` | VBHN_18-2026…_2026_Bo_luat_Lao_dong | 20_Lao_dong | **true** | pushed | (canonical; goc+title_vn đủ) |
| `1n1ezVBAsrKz…` | VBHN_18-2026…_2026_Bo_luat_Lao_dong | _ZZZ_QUARANTINE | false | — | NEAR, jaccard **1.0**, chênh 1 ký tự |
| `1FqSESXbEdh4…` | VBHN_18-2026…_Bo_luat_Lao_dong (thiếu «2026» trong tên) | **20_Lao_dong** | false | removed_by_user | NEAR, jaccard **0.9968**, chênh 33 ký tự |

Dòng thứ ba là bản CŨ (tên thiếu năm, đã gỡ khỏi NLM) **còn nằm chung thư mục chủ đề 20 với canonical**
— đúng kiểu «người tra vớ nhầm». **Đề xuất:** (a) note cho cả 2 bản twin (nhóm GHI-2);
(b) `recat 1FqSESXbEdh4… --quarantine` để dời bản cũ khỏi cat 20 (nhóm GHI-3, quyết riêng — có chạm Drive).
Ghi nhận thêm: canonical mang `hieuluc="Con hieu luc"` (biến thể vocab B1) — thuộc việc E#6 chuẩn hoá
vocab, KHÔNG gộp vào lượt này.

## 4. B3 — cụm trùng/thiếu năm: đo đủ căn cứ năm cho CẢ 6 dòng

`vbhn-year-fix` DRY trả 0 fixable — **by-design**: hygiene.py:67-70 cố ý bỏ qua dòng `corpus≠true`
(tránh conflict giả với canonical) ⇒ cụm này phải đi `reg_upsert` TAY từng dòng (đúng memory
«đổi sohieu qua reg_upsert KHÔNG reg_bulk»). Căn cứ năm đo bằng `doc-text` đọc header từng bản:

| drive_id | name | Đo được | sohieu đề xuất |
|---|---|---|---|
| `1Q0XmTbuwaNu…` | VBHN_40-VPQH_Luat_BHYT_HopNhat | «Số: 40/VBHN-VPQH … ngày 16/3/2026», Luật BHYT | `40-2026-VBHN-VPQH` |
| `12i-lNclnS72…` | 40_VBHN-VPQH_699508 | cùng văn bản BHYT 16/3/2026 | `40-2026-VBHN-VPQH` |
| `1pbLZB2xYGj9…` | 89_VBHN-VPQH_670749 | «Số: 89/VBHN-VPQH … ngày 22/8/2025», Luật MTTQ VN | `89-2025-VBHN-VPQH` |
| `1jyM8uEKJRKm…` | VBHN_89-VBHN-VPQH_Luat_NSNN… | header KHÔNG in «Số:»; nội dung = NSNN 89/2025+145/2025, trùng canonical `89-2026-VBHN-VPQH` (sổ B3 đã đối chiếu trùng nội dung) | `89-2026-VBHN-VPQH` |
| `1Qja1LwpJHCA…` | VBHN_25-VPQH_Ke_toan.docx | «Số: 25/VBHN-VPQH … ngày 26/02/2025», Luật Kế toán | `25-2025-VBHN-VPQH` |
| `1ZK0wZiBwWBG…` | 25_VBHN-VPQH_559965.docx | «Số: 25/VBHN-VPQH … ngày **29/12/2022**», Luật **NHNN VN** | `25-2022-VBHN-VPQH` |

★ **Cụm 25 là COLLISION THẬT giữa HAI VĂN BẢN KHÁC NHAU** (Kế toán 2025 vs NHNN 2022 cùng số 25) —
đúng ca bất biến «sohieu phải có năm» sinh ra để chặn. Cụm 40 và 89 sau khi thêm năm sẽ thành
twin-có-chủ của canonical tương ứng (40-2026 BHYT · 89-2025 MTTQ · 89-2026 NSNN).
Mọi dòng đều `corpus=false` quarantine/thuong ⇒ đổi sohieu KHÔNG đụng corpus/NLM.

## 5. B5 — 4/5 tự đóng; dòng còn lại là cặp trùng `60-2026-VBHN-VPQH`

- Đo tươi cả kho nền (1347 dòng) lẫn scope hồ sơ BHXH: các sohieu trần `67-2025`, `89-2026`,
  `24-2026`, `100-2026` **= 0 dòng** — 5 dòng «trống name/loai/hieuluc» của sổ 29-07 đã không còn
  (được dọn/enrich ở các lượt container). **Không còn gì để gắn note.**
- Riêng `60-2026-VBHN-VPQH` nay là **2 dòng đủ metadata nhưng TRÙNG file**:
  `1hUVmJ10lV…` (corpus=true, pushed — canonical) và `1K2i2rFACxlQdX…` (corpus **rỗng**, không NLM).
  `doc-compare`: **IDENTICAL — content_hash trùng, jaccard 1.0, 72.031 ký tự cả hai.**
  Cặp này cũng chính là nhóm `duplicate_sohieu`/`duplicate_name` mà registry-doctor đang báo.
  **Đề xuất:** `1K2i2rF…` set `corpus=false` + note trỏ canonical (nhóm GHI-2); tuỳ chọn nâng lên
  `recat --quarantine` (nhóm GHI-3). Lưu ý: corpus đang RỖNG, đây là upsert giá trị mới —
  không cần `reg_clear` (luật reg_clear chỉ áp khi muốn LÀM RỖNG field).

## 6. B2b — cơ sở đếm registry-doctor: XÁC NHẬN BY-DESIGN, việc ghi-vào-output ĐÃ XONG TỪ r251

- Đọc code + đo output tươi: `registry-doctor --profile vbqppl --json` nay in
  `count=1315 · scanned=706 · skipped_ref=29 · skipped_own_thuong=245 · skipped_own_corpus_false=335`
  kèm trường **`basis`** kể rõ: «MỌI bucket chỉ tính trên `scanned`; BA lớp bị loại: (1) row_kind=ref;
  (2) loai=thuong; (3) own corpus=false bất kể loai (r251)».
- ⇒ Chênh lệch B2b ghi ngày 29-07 (`missing_sohieu=19` vs đếm thẳng 56; `duplicate_*=0` vs 2 nhóm)
  đúng là **by-design 3 lớp loại**, và yêu cầu «ghi rõ cơ sở đếm vào output như sweep» **đã được
  chính bản vá r251 của lượt 18 thực hiện** — nay đang trên master + Drive (v1.36.6). KHÔNG mở r mới.
- Cùng họ by-design: `vbhn-year-fix` bỏ qua corpus≠true (§4). Hai công cụ nhất quán một triết lý:
  bucket sức khoẻ chỉ đo trên corpus canonical.

---

## GHI CHỜ DUYỆT (không lệnh nào đã chạy)

Chạy tại `C:\qh\tra-luat`, profile `vbqppl`, **env sạch trước gate** (không TL_* thừa); xong toàn bộ
thì `tl boot --refresh`.

**GHI-1 · B3 đổi sohieu — 6 lệnh reg_upsert TỪNG DÒNG (không bulk; sohieu là khoá immutable):**
```
tl register --drive-id 1Q0XmTbuwaNu6obtR1a5D-8e20UcI3IKTbeAc7T7gs3w --sohieu 40-2026-VBHN-VPQH --profile vbqppl --apply --confirm yes
tl register --drive-id 12i-lNclnS72jHWH1jwvWYJx5wZtwrGm5i3papThKod4 --sohieu 40-2026-VBHN-VPQH --profile vbqppl --apply --confirm yes
tl register --drive-id 1pbLZB2xYGj9HCAiyrrVyPOMSaFHuui0YlrjzOwQ5yjw --sohieu 89-2025-VBHN-VPQH --profile vbqppl --apply --confirm yes
tl register --drive-id 1jyM8uEKJRKmohcl4EQ8F1WpupoueR0gWor1IoT8xkOQ --sohieu 89-2026-VBHN-VPQH --profile vbqppl --apply --confirm yes
tl register --drive-id 1Qja1LwpJHCA_qYPrDF2hTpnV0QHomCms --sohieu 25-2025-VBHN-VPQH --profile vbqppl --apply --confirm yes
tl register --drive-id 1ZK0wZiBwWBGq86bgnRlbX9kqvxuSq9DM --sohieu 25-2022-VBHN-VPQH --profile vbqppl --apply --confirm yes
```

**GHI-2 · note twin + hạ corpus bản trùng 60-2026 — 1 lệnh bulk cols=note (+1 dòng kèm corpus), theo lệ B4
(`register --bulk --cols`):** file kèm `rasoat/pending_kho_nen_note_bulk_2026-07-31.json` — 10 dòng:
4 twin (1mGRs4vs · 1n1ezVBAsrKz · 1FqSESXbEdh4 · 1K2i2rFACxlQdX) note trỏ canonical + kết quả đo;
6 dòng B3 note căn cứ năm. Riêng `1K2i2rF…` thêm cột `corpus=false`.
```
tl register --bulk rasoat/pending_kho_nen_note_bulk_2026-07-31.json --cols "note" --profile vbqppl --apply --confirm yes
tl register --drive-id 1K2i2rFACxlQdXfPO_GPZfbPZN0xxnRUZFHXcBvY0Tfo --corpus false --profile vbqppl --apply --confirm yes
```
(CLI `tl register` per-row KHÔNG lộ cột `note` — cột có thật trong `REG_COLS_` GAS; đường note duy
nhất hiện nay là `--bulk --cols "note"`. Nếu muốn per-row `--note` thì đó là một r nhỏ, tuỳ duyệt.)

**GHI-3 · dọn sâu tuỳ chọn (chạm Drive — quyết riêng từng món):**
```
tl recat 1FqSESXbEdh4mpEpT3-DXkBpITeVZ2jm8xXMZoEl-ax0 --quarantine --profile vbqppl --apply --confirm yes
tl recat 1K2i2rFACxlQdXfPO_GPZfbPZN0xxnRUZFHXcBvY0Tfo --quarantine --profile vbqppl --apply --confirm yes
```

## Phát hiện phụ (ghi sổ, KHÔNG thuộc 6 việc, không tự làm)

1. **17 dòng `OVERFLOW_ROW_NOT_MARKED_OVERFLOW`** (doctor topology): dòng nằm notebook overflow
   (`2d8c2fef…`, `45739ff7…`) nhưng `row_kind=own`. Đường sửa đúng theo ghi chú r232 trong code:
   reg_upsert row_kind từng dòng — KHÔNG phải `nlm-reconcile --apply`.
2. `doctor` rc=2 vì `overflow_liveness alive=false` cả 2 notebook — đo từ IP VN nên là **geo-block
   đã biết** (lượt 18), không kết luận cookie chết từ vantage này.
3. `registry-doctor` nền: `missing_sohieu=194/706 scanned` + 8 nhóm duplicate_sohieu — phần lớn nhóm
   là kiểu «văn bản + phụ lục cùng số hiệu» (30-2020, 62-2026, 128-2026, 142-2026…) và cặp scan
   `79-NQ-TW`; món 60-2026 đã xử ở §5; 12-2022-ND-CP ×2 tên gần trùng đáng soi lượt sau.
4. Sổ RASOAT_PROFILE 29-07 §C1b (3 dòng UNKNOWN topology) đã lỗi thời — xem §1.

## Bàn giao

- Toàn bộ 6 việc: 3 đóng bằng đo (1, 5-phần-lớn, 6), 3 chờ duyệt GHI (2, 3, 4 + đuôi 5).
- File bulk đề xuất: `rasoat/pending_kho_nen_note_bulk_2026-07-31.json` (chưa chạy).
- Không đổi mã, không mở r mới, nợ deploy vẫn 0.
