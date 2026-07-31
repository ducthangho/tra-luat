Xử HÀNG ĐỢI NLM kho vbqppl — CHỈ chạy từ CONTAINER US-EGRESS (NLM web geo-block IP VN; mọi thao tác
NLM từ máy VN đều fail rc=1 như đã đo lượt 24). Đo bằng chứng cứ trước; mục nào đã có dấu vết xử lý
thì BỎ QUA, đừng làm lại mù. Bản sao prompt này nằm trong repo: `rasoat/PROMPT_US_NLM_QUEUE_2026-07-31.md`.

## Đọc trước khi làm gì

- `rasoat/KETQUA_GHI_BANGDUYET_CORPUS_AUDIT_2026-07-31.md` (master `69b1819`) — nguồn Việc 1-2 +
  trạng thái 176/2025. `rasoat/KETQUA_THUCHIEN_BANGDUYET_CORPUS_AUDIT_2026-07-31.md` — bằng chứng nền.
- Memory topic `rasoat-hoso-orchestration-plan` (đầu file = lượt 24 mới nhất) ·
  `nlm-cookie-chet-do-xoay-phien-khong-phai-ttl` (auth NLM: `nlm login` trần = NO-OP phải `--force`;
  «browser profile is not logged in» → `nlm login --clear`; traceback os.kill → dọn
  `chrome-port-map.json`) · `nlm-add-pdf-drive-fail` (PDF không add được bằng --drive-id — phải
  download + MCP `source_add source_type=file` + `register --nlm-source-id` tay).
- Bẫy đã trả giá: `register` GHI NGAY từ lần gọi đầu · `source-update-corpus … --apply` thiếu
  `--confirm yes` = silent-DRY ok:true (bằng chứng duy nhất là readback keyed) · `reg_get`/`--live`
  kiểm `count` trước khi tin `rows[0]` · **CẤM hành động trên drive_id/src_id đã truncate** (Việc 4
  toàn id cắt — resolve full từ registry/nlm-list trước).

## Chuẩn bị & đo (mốc 31-07, sau lượt 24)

```
git clone https://github.com/ducthangho/tra-luat.git  (hoặc pull; master ≥ 69b1819, client v1.36.16)
tl up / tl boot --refresh   # + gws-auth-load / nlm-auth-load theo nếp container US (lượt 18)
tl nlm-auth-status          # chết → xử theo memory nlm-cookie… rồi mới đi tiếp
tl --profile vbqppl reg-query --refresh --limit 3000 --json > reg.json
```
Kiểm trạng thái tiền-đề: `1hQedQKZ…` (176 mới) corpus=∅ chưa NLM · `1auEnrsy…` (176 khuyết)
corpus=false còn nguồn NLM · 9 dòng Việc 2 tên registry MỚI nhưng nguồn NLM tên CŨ. Lệch = đã có
phiên khác xử → bỏ qua mục tương ứng.

## Việc 1 — CHUỖI 176/2025 (ưu tiên số một: khép corpus cho văn bản BHXH lõi)

GDoc mới `1hQedQKZvtumfVs4ELJP0EN4SsSAkCToxzyk7Gy3AS_M` (cat 02_Bao_hiem, sohieu 176-2025-ND-CP,
doc-text đã verify đủ Điều 1→8; src docx trung gian `1hpRdcS0g7BL_z_mZC9YY8jmC99hurfAv`).
Thứ tự BẮT BUỘC (corpus=true chỉ SAU khi NLM link — thiết kế pipeline):

1. Add nguồn NLM cho GDoc mới vào notebook gợi ý `743ed200-2e55-4673-b7a0-9bfd13b41ce6`:
   MCP `source_add source_type=drive document_id=1hQedQKZvtumfVs4ELJP0EN4SsSAkCToxzyk7Gy3AS_M`
   (GDoc đi đường drive được; nếu fail kiểu PDF → nếp memory nlm-add-pdf-drive-fail).
   Notebook do reconcile/routing quyết nếu gợi ý không hợp — đừng ép.
2. `tl nlm-reconcile` per-notebook `--apply` — nguồn add tay thành link_candidates bắc cầu
   exact-title → link registry.
3. Readback keyed: `tl --profile vbqppl reg-query --drive-id 1hQedQKZvtumfVs4ELJP0EN4SsSAkCToxzyk7Gy3AS_M --live --json`
   → `count=1`, `nlm_source_id` có, `nlm_status` ok.
4. `tl register --drive-id 1hQedQKZvtumfVs4ELJP0EN4SsSAkCToxzyk7Gy3AS_M --corpus true --no-autofill --apply --confirm yes`
   (★register GHI NGAY — đúng 1 lần, sau khi bước 3 đạt).
5. Gỡ nguồn NLM của bản khuyết `1auEnrsyEz2FsCW2y39B244uYoSDlva2TgTi2DE9bw50` (nlm_delete từ VN đã
   fail rc=1): re-run idempotent `tl --profile vbqppl source-update-corpus 1auEnrsyEz2FsCW2y39B244uYoSDlva2TgTi2DE9bw50 false --apply --confirm yes`
   (corpus đã false — chỉ để retry nhánh gỡ NLM; hoặc `nlm-source-remove` theo `nlm_source_id` đọc
   từ row live). Readback: row live hết nlm_source_id.
6. `tl nlm-reconcile --clear-stale`.

Đích nghiệm thu: 176/2025 vào corpus-effective bằng bản MỚI; bản khuyết sạch NLM, corpus=false.

## Việc 2 — 9 nguồn NLM còn mang TÊN CŨ sau rename lượt 24

Cách A (ưu tiên — idempotent, có journal; registry/Drive no-op, chỉ nhánh NLM chạy lại):
```
tl --profile vbqppl source-rename <drive_id> --name <TÊN_MỚI> --rename-drive --apply
```
| drive_id | TÊN MỚI |
|---|---|
| `1MZlRu4DcICseY1jpXGL2080vbilN_h79mksFt2xY_c4` | `QD_127-2021-QD-TTG_Chien_luoc_quoc_gia_AI_2030` |
| `18-39wTx-jZ9bLTzo51ihyrj2w4G0rcVd87IrRm2Jg-4` | `QD_33-2026-QD-TTG_Danh_muc_he_thong_AI_rui_ro_cao` |
| `1ZOTW36-6T58A5VumrbLx9EElXSUdEN90MTS8GYcHfW8` | `ND_353-2025-ND-CP_Co_che_thu_nghiem_cong_nghiep_cong_nghe_so` |
| `1T65C_hLSjIhDuhGmNn_L2EYJ_F5TYQsgpp3P-t0Tlx4` | `ND_356-2025-ND-CP_Chi_tiet_Luat_Bao_ve_du_lieu_ca_nhan` |
| `1e1KpRRSHzTA1VOzWPTIt2pHj5r9G-RE_hC_Es0gVF_g` | `QD_804-2026-QD-TTG_Danh_muc_bo_du_lieu_AI` |
| `18_Ybzz8XHRnmilzgDdqgPj5TZGhBwrdKUwsXH7rhtPk` | `NQ_112-2026-NQ-CP_Bo_sung_CTLP_2026_sua_Luat_69-2020` |
| `1PWj5iUJb1pcd5Q1TItAeDhuZvqrdgdK2` | `TL_ILO_2026_AI_tao_sinh_va_viec_lam_VN` |
| `1nHnfEQDEJao4E_kt8MbE0F9T3NVgNLshEgkLFvRMdA8` | `TT_10-2020-TT-BLDTBXH_Chi_tiet_BLLD_ve_HDLD` |
| `1iEiWmiBvd-WTFI2xeWpYy8LlJlDY9xUWk7OB7B0OBbI` | `ND_118-2016-ND-CP_Sua_doi_ND_56-2008_ngan_hang_mo_ghep_tang` |

KHÔNG kèm `--sohieu` (registry đã đúng), không đổi gì khác. Cách B nếu A vẫn fail: MCP
`source_rename` theo `nlm_source_id` đọc từ row `--live`. Verify: `source_describe`/`nlm-list` ra
tiêu đề mới; reconcile không kêu title-mismatch.

## Việc 3 — 2 dòng nlm-only CHẾT (P1#4 lượt 23; chỉ-đọc trước, GHI chờ duyệt)

| khóa | tên registry |
|---|---|
| `nlm:398d50d7-a639-4528-8820-56644b12fb3e` | `NQ_59-NQ-TW_Hoi_nhap_quoc_te_2025` (59-2025-NQ-TW, corpus=true) |
| `nlm:e583ebea-db66-4cdd-94d9-df663cfc5f54` | `VBHN_73-82-ND-CP_Phu_luc` (corpus=true) |

Đo: `source_describe` + `source_get_content` từng nguồn. Nguồn SỐNG → chỉ ghi nhận (cờ audit
header là chuyện auditor). Nguồn CHẾT thật → TRÌNH phương án (nạp lại từ Drive gốc nếu lần ra /
hạ corpus) — **không tự hạ corpus**.

## Việc 4 — tồn cũ (★id dưới đây bị CẮT trong sổ/memory — resolve FULL trước, cấm hành động trên id cắt)

- Ghost `CD_32-2026` src `5ec30323…` — kiểm source, gỡ ghost.
- Nguồn docx thô 45-2019 src `04e51f9c…` — gỡ khỏi NLM (cụm hygiene 45-2019 chờ gỡ từ lượt 22).
- 4 nguồn `raw_on_nlm` — liệt kê bằng `tl sweep` / `nlm-audit-physical`; đối chiếu sổ cũ
  (`rasoat/KETQUA_GHI_KHO_NEN_2026-07-31.md`, `rasoat/KETQUA_VIEC_TREO_BHXH_2026-07-30.md`) xem đã
  duyệt gỡ chưa — đã duyệt thì làm, chưa thì trình.
- Nguồn NLM bản thiếu `131-2021` (drive `1831Z…`, bản thiếu 118/185 Điều đã corpus=false lượt 22) — gỡ.
- Chốt toàn cục: `tl nlm-reconcile --all-notebooks` + `--clear-stale`; đối chiếu
  `nlm-audit-physical` registry↔NLM = khớp.

## Nếp bắt buộc

Mỗi thao tác GHI: DRY (nếu lệnh có) → apply → **readback keyed** (`reg-query --drive-id … --live`,
kiểm `count` trước `rows[0]`; phía NLM đo bằng `source_describe`/`nlm-list` trước-sau). Journal đủ,
undo được. Kết phiên TỰ đóng gói: sổ `rasoat/KETQUA_US_NLM_QUEUE_<ngày>.md` + commit/push qua
**worktree tạm** (`git worktree add <tmp> origin/master --detach` → commit → `push HEAD:master` —
checkout chung hay bị phiên khác chiếm) + cập nhật memory topic `rasoat-hoso-orchestration-plan`
(đầu file = mới nhất) + prompt bàn giao mới. Console in tiếng Việt: `PYTHONIOENCODING=utf-8`.

## NGOÀI phạm vi phiên này (đừng nhặt nhầm)

Note dup↔bản chuẩn (cần đường đọc cột note GAS-level — việc riêng, văn bản note nằm trong sổ GHI
lượt 24) · lô 3b 43 tên thiếu chủ đề (chạy lệnh quét năm r276 trước) · r vá auditor/doc-text (tuỳ
duyệt) · sheet-dup `1Qja1Lwp…` Kế toán (CẤM reg-delete — xoá cả hai dòng) · 43 row_kind overflow ·
quarantine hẳn bản khuyết 176 (`1auEnrsy…`) = tuỳ duyệt SAU khi Việc 1 xong · deploy (nợ 0 —
Drive = v1.36.16, đã đo 31-07).
