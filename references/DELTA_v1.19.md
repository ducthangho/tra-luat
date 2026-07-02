# DELTA v1.19 — Cách B: registry/manifest RIÊNG theo profile

Ngày: 2026-06-23 · 1 webapp deployment (giữ URL+token), nhận `registryDocId`/`manifestId` mỗi request.
Trạng thái: **`2.21.2h` là bản cần deploy (LIVE target)** = Cách B + writeconfig giữ/merge profiles (§A8) + `row_kind=own|ref|overflow` + profile-scope đầy đủ cho CLI. `2.21.2g` là tiền thân (Cách B + writeconfig nhưng chưa có schema/row_kind hotfix). EXPECT/contract = `2.21.2h`. **KHÔNG tự deploy từ skill.**

## A. Apps Script (`.gs`) — `references/Code.2.21.2h.gs` (LIVE target; tiền thân `Code.2.21.2g.gs`)

Mục tiêu: mọi action thao tác registry/manifest nhận `registryDocId`/`manifestId`; thiếu ⇒ hằng VBQPPL nền
(tương thích ngược, `vbqppl` chạy y như cũ).

1. **Hằng:**
   - `BASE_REGISTRY_DOC_ID_ = '1mATGFhaW0e_CYienAD80DsTS1K4zfJNlTAx-DsHaCD8'` (VBQPPL)
   - `BASE_MANIFEST_ID_     = '1d8Pau1x-Qeq0i8ClQnxuTMohGNf6GEeI'` (VBQPPL)
   - giữ `NLM_DEFAULT_NOTEBOOK_` (có từ 2.21.2e).
2. **Helper:** `resolveRegistry_(e)` / `resolveManifest_(e)` → tham số nếu có, không thì base. Thêm
   `setCorpusScope_(p)` set biến request-scoped `_REQ_REGISTRY_ID_`/`_REQ_MANIFEST_ID_` (gọi ở `main_()`
   ngay sau check token) — realize "nhận docId mỗi request" cho TẤT CẢ action mà không phải đổi chữ ký từng hàm.
3. **Điểm chốt registry:** `regSS_()` ưu tiên `_REQ_REGISTRY_ID_` (mở đúng Sheet profile; fail thì THROW,
   KHÔNG fallback VBQPPL để tránh ghi nhầm corpus). Thiếu ⇒ giữ resolution cũ (VBQPPL). Vì vậy
   `doRegGet_/doRegUpsert_/doRegBulk_/doRegClear_/doOrganize_/doMapSet_/doRegen2_/doFind_/doLocate_/
   doSourceMap_/doNlmSlots_/doNlmDedup_/doNlmPreflight_` (đều đi qua `regReadAll_/regUpsertOne_/regWriteAll_`)
   tự dùng đúng registry profile. Nhóm `nlm_*` vẫn giữ base-fallback theo `nlm_notebook_id`/`baseNotebookId`.
4. **Cache registry KEY theo registry** (`_regCacheKey_`) — tránh lẫn rows vbqppl/vbthuong giữa các request.
5. **`manifest_export`:** nếu có `manifestId` ⇒ ghi ĐÚNG file đó (KHÔNG đụng `TL_MANIFEST_ID` nền); `treeHash`
   tính theo registry tham số (vì `regReadAll_` đã đọc registry profile). Hotfix: khi có `registryDocId`,
   `treeHash/corpus_count` tính trên dòng thực của registry profile để profile drift làm đổi hash; thiếu
   `registryDocId` thì VBQPPL nền giữ corpus-only như cũ. Trả thêm `registry_scope`/`manifest_scope`.
6. **Version:** `2.21.2h` — `EXPECT_VERSION=2.21.2h`, `API_CONTRACT` đóng dấu `2.21.2h`.
   `ping` trả thêm `schema_version`, `registry_schema='reg_cols_row_kind_v1'`, `registry_cols` để tránh silent mismatch khi REG_COLS_ đổi.
7. **Backward-compat:** thiếu `registryDocId`/`manifestId` ⇒ VBQPPL nền.
8. **writeconfig (giữ trong `2.21.2h`):** `references/Code.2.21.2h.gs` — `buildConfigObject_` GIỮ/merge block
   `schema/defaultProfile/profiles` v2 đã có trong mirror khi rewrite/rotate token (issue v1.19.1#4); cho phép
   khởi tạo `profiles` qua `writeconfig` (luôn đồng bộ `profiles.vbqppl` theo hằng nền). Vì đã LIVE, rotate
   token/`writeconfig` KHÔNG còn xoá block `profiles`.

## B. `tl.py` forward tham số theo profile

Khi `--profile P` (KHÁC mặc định), `tl.py` chèn `registryDocId=<P.registryDocId>` + `manifestId=<P.manifestId>`
(env `TL_REGISTRY_DOC_ID`/`TL_MANIFEST_ID`) vào MỌI call webapp qua wrapper `_ScopedGas` (không đè nếu call
truyền tường minh). Profile mặc định `vbqppl` bỏ trống ⇒ webapp dùng nền. CLI `slot-audit`/`profile-info` giữ nguyên.

## C. Thiết lập 1 lần cho profile `vbthuong` (SAU khi deploy .gs)

```bash
ROOT=1Ik9TXfkkXThbBecMWm4CMXo-mZCRAw84   # folder Van_ban_thuong
NB=fec6c125-e01c-433d-aed5-666c16540dd8   # notebook dự án
# 1) Tạo registry Sheet RIÊNG (copy cấu trúc cột VBQPPL rồi xóa rows; giữ REG_COLS_ + nlm_notebook_id)
#    → registryDocId_vbthuong
# 2) Tạo manifest RIÊNG cho registry/notebook profile:
python scripts/tl.py --config tra_luat_config.v2.json --profile vbthuong manifest   # manifest_export(registryDocId=…, manifestId=file mới)
#    → manifestId_vbthuong
# 3) Ghi 2 ID thật vào profiles.vbthuong (thay "dùng chung")
# 4) PHÂN LOẠI nguồn của notebook dự án TRƯỚC khi backfill (xem doctrine §C.1 — KHÔNG xoá VBQPPL):
#    - VĂN BẢN THƯỜNG riêng của dự án  → reg_upsert vào registry vbthuong, đặt nlm_notebook_id=$NB.
#    - VBQPPL CANONICAL được dùng chung → GIỮ NGUYÊN dòng ở registry VBQPPL (KHÔNG move/xoá);
#      nếu cần slot/dedup của notebook dự án phản ánh đúng thì THÊM dòng tham chiếu trong registry vbthuong
#      (cùng drive_id/nlm_source_id, nlm_notebook_id=$NB), không sửa gốc VBQPPL.
# 5) Kiểm tra
python scripts/tl.py --config tra_luat_config.v2.json --profile vbthuong boot
python scripts/tl.py --config tra_luat_config.v2.json --profile vbthuong slot-audit --notebook-id $NB
```

### C.1 Doctrine backfill (SỬA giả định "19 văn bản" — thực tế ví dụ: 37 nguồn = 4 VB thường + 33 VBQPPL canonical)

**KHÔNG được "chuyển dòng khỏi VBQPPL + xoá" hàng loạt** cho mọi nguồn trong notebook dự án. Notebook dự án
thường gồm hai loại nguồn, xử lý KHÁC nhau:

| Loại nguồn | Đăng ký ở đâu | Thao tác |
|---|---|---|
| **Văn bản thường riêng của profile** (vd 4 văn bản) | registry profile (`vbthuong`) | `row_kind=own`, `corpus=false`, `loai=thuong`, `nlm_notebook_id=$NB`. Không cần ở VBQPPL. |
| **VBQPPL canonical tham chiếu trong notebook dự án** (vd 33 luật) | GIỮ ở registry VBQPPL | KHÔNG move/xoá khỏi VBQPPL (xoá = hỏng corpus pháp điển). Muốn slot/dedup của notebook dự án đúng thì THÊM **dòng tham chiếu** ở registry profile: `row_kind=ref`, cùng `drive_id`/`nlm_source_id`, `nlm_notebook_id=$NB`, gốc VBQPPL nguyên vẹn. |
| **VBQPPL overflow host trong profile** (notebook VBQPPL sát/đầy, vd ≥295/300) | registry profile được chỉ định | Đây vẫn là văn bản quy phạm, không phải văn bản thường: đặt `row_kind=overflow`, `corpus=VBQPPL` (hoặc `corpus=true` theo schema cũ), `loai` quy phạm, `nlm_notebook_id=$NB_OVERFLOW`. QA/cross_notebook_query/hygiene phải xử lý như VBQPPL host ở profile, không tính là dòng `own` văn bản thường. |

Lý do: mô hình registry "một-dòng-một-notebook" KHÔNG biểu diễn được nguồn dùng chung hai notebook; phải
dùng dòng tham chiếu thay vì di dời. Slot theo notebook (2.21.2e+) vẫn đếm đúng vì base-fallback + dòng tham
chiếu mang `nlm_notebook_id=$NB`. Khi nghi ngờ một nguồn là canonical pháp điển, MẶC ĐỊNH coi là VBQPPL
(giữ gốc), chỉ thêm tham chiếu — không bao giờ xoá gốc để "chuyển" sang profile.

Guard sức chứa: trước khi `nlm_push`/`nlm_preflight` cho VBQPPL canonical, nếu notebook đích có `nlm_slots >= 295/300`
thì không fail cứng `NOTEBOOK_FULL`; phải trả REVIEW với route overflow (`row_kind=overflow`, `corpus=VBQPPL`,
profile/notebook host được chỉ định) để người vận hành duyệt.

Slot registry là ước lượng để dedup/routing, không thay thế số vật lý của NotebookLM. Trước khi `source_add`, phải lấy
`notebook_get.source_count`; ví dụ registry profile có thể đếm 13 dòng own/overflow trong khi notebook vật lý có 37 nguồn
vì 24 dòng `ref` đang trỏ sang canonical VBQPPL. Khi cần đối chiếu slot registry gồm tham chiếu, gọi `nlm_slots countRefs=true`.

## D. QUY ƯỚC RA PROMPT/LỆNH VỀ SAU (Cách B)

Nguyên tắc: **nêu rõ profile ở đầu yêu cầu** để định tuyến đúng registry/notebook/manifest. Nếu muốn khỏi nhắc
mỗi lần: đặt `defaultProfile="vbthuong"` cho không gian dự án, hoặc thêm khối `corpus_profile=vbthuong` vào
Instruction của Project/NotebookLM.

| Ý định | Prompt mẫu (nói với trợ lý) | Lệnh tl chạy ngầm |
|---|---|---|
| Nạp vb mới không trùng | "vbthuong: nạp các văn bản mới không trùng trong _HOP_NAP vào notebook dự án" | `--profile vbthuong` ingest/preingest → dedup theo registry vbthuong → `map_set notebookId=$NB` |
| Tra nguyên văn | "vbthuong: tra nguyên văn Điều X của <văn bản>" | query notebook fec6c125 + verify; miss → fallback vbqppl |
| Rà soát đối chiếu VBQPPL | "vbthuong: rà soát Điều X, đối chiếu thêm VBQPPL" | `cross_notebook_query(fec6c125, 743ed200)` |
| Kiểm slot trước khi nạp | "vbthuong: kiểm slot notebook dự án" | `--profile vbthuong slot-audit --notebook-id $NB` |
| Link tải cho người dùng | "cho link tải <văn bản>" | `link-priority`: TVPL → LVN → Công báo → official khác |
| Chuyển corpus | "chuyển sang vbqppl" / "làm trên VBQPPL" | đổi `--profile vbqppl` |
| Tạo profile dự án mới | "tạo profile <tên> cho dự án …, folder <id>, notebook <id>" | dựng profile mới như mục C |

Mặc định khi KHÔNG nêu profile = `defaultProfile` (hiện `vbqppl`).

## E. Đơn giản hóa tạo Instruction (v1.19.1)

- **Mặc định tạo Instruction = VBQPPL.** Không nêu corpus ⇒ `tl instructions` sinh Instruction VBQPPL như cũ
  (không có khối `profile_setup`).
- **Văn bản thường với tên + notebook cụ thể ⇒ tạo profile mới + folder + Instruction gắn profile (fallback VBQPPL):**
  ```bash
  tl profile-create --name <X> --notebook <notebookId> [--folder-name <X>] [--apply]
  ```
  - DRY (mặc định): in `config_profiles_patch` (ghi vào `profiles.<X>`), các bước tiếp theo, và Instruction Project.
  - `--apply`: tạo folder `<X>` trong Drive folder `Van_ban_thuong` (`bootstrap`→`vanBanThuongId` + `resolvefolder create=true`),
    điền `rootFolderId` thật vào patch + Instruction.
  - Instruction sinh ra: `corpus_profile` nêu Project mặc định dùng `<X>` (notebook riêng, folder `Van_ban_thuong/<X>`),
    mọi thao tác theo `<X>`, MISS mới fallback VBQPPL; kèm khối `profile_setup` (config snippet + 4 bước dựng 1 lần).
- `tl instructions` cũng nhận `--profile <X> --notebook <id> --folder-name <X>` để sinh trực tiếp (không tạo folder).

## Kiểm thử

```text
python -m py_compile scripts/*.py              OK
python scripts/tl.py --selftest                65/65 OK
python scripts/gen_instructions.py --selftest  14/14 OK
python scripts/contract_check.py --audit       KHỚP 2.21.2h
python scripts/apply_gs_patches.py --selftest  12/12 OK
node --check Code.2.21.2h.gs OK
tl profile-create (DRY) / tl instructions --profile  OK
```
