# tra-luat — HỢP ĐỒNG API SỐNG (webapp Apps Script)

> **Phiên bản deploy đã đóng dấu (LIVE): `2.21.2p`** · đã xác minh `ping.version=2.21.2p`, `registry_schema=reg_cols_row_kind_v1` (27 cột) · = 2.21.2n (profile_catalog + drive_info_bulk r185/WP5) ⊕ `ingest_commit` (r198/ADR-0014 — gộp organize+register+readback 1 RTT, sub-step marker) ⊕ **2.21.2p ATOMIC registry RMW** (KI-25 `withRegLock_` ôm TRỌN đọc-sửa-ghi · KI-26 `ensureRegTabs_` không tạo tab rỗng khi đang swap · KI-27 chốt chặn `REGISTRY_SHRINK_REFUSED` + sao lưu xoay vòng `files_bak_<ts>` + `reg_bak_list`/`reg_bak_restore`); `tl.py EXPECT_VERSION=2.21.2p`. *(Dấu này PHẢI khớp EXPECT_VERSION — drift-lock r119 khoá.)*
> **CÁCH XÁC MINH PHIÊN BẢN (làm đầu phiên):** `gas.get('ping')` → `version/schema_version/registry_schema/capabilities`. Nếu KHÁC
> `2.21.2p`: server đã trôi version → đối chiếu deploy. (Nếu `< 2.21.2l` thì thiếu regen2 own-scope/guard → deploy lại
> `Code.2.21.2p.gs` qua clasp -i giữ URL; version-gate vẫn CHẶN regen2 profile cho tới khi đủ.) (Header `.gs` ghi `v2.8.0` là
> nhãn cũ, KHÔNG phải phiên bản deploy; nguồn sự thật = `ping.version`.)
> Riêng CAS state rà soát là feature-gated trong cùng nhãn `2.21.2p`: chỉ được ghi khi
> `ping.capabilities` có `rasoat_state_cas`. LIVE p cũ thiếu capability sẽ bị client từ chối
> trước mutation; deploy source p hiện hành và verify ping trước khi dùng.
>
> **Slot theo notebook (LIVE từ 2.21.2g):** `nlm_slots`/`nlm_preflight`/`nlm_dedup` đếm theo
> `nlm_notebook_id == notebookId`; dòng RỖNG quy về `baseNotebookId`=VBQPPL nền (VBQPPL vẫn đếm đúng không
> cần backfill; notebook dự án hết `NOTEBOOK_FULL` giả). **(Cần 2.21.2l)** `row_kind=ref` bị loại khỏi registry
> slot mặc định; truyền `countRefs=true`/`count_refs=true` để ước lượng gồm tham chiếu. Trước khi `source_add`,
> số vật lý của notebook phải lấy từ `notebook_get.source_count`; registry slot chỉ là estimate/dedup.
>
> **Cách B — registry/manifest RIÊNG theo profile (LIVE từ 2.21.2g):** webapp 1 deployment (giữ URL+token)
> nhận `registryDocId`/`manifestId` ở MỌI request; thiếu ⇒ hằng VBQPPL nền (`BASE_REGISTRY_DOC_ID_`/
> `BASE_MANIFEST_ID_`). `tl.py --profile P` tự forward 2 tham số này (env `TL_REGISTRY_DOC_ID`/`TL_MANIFEST_ID`)
> ở MỌI call — kể cả `boot`/`manifest` (qua `_fallback/boot.py`, `_fallback/manifest_build.py`). `vbqppl`
> bỏ trống ⇒ nền. Chi tiết: `references/DELTA_v1.19.md`.
>
> **MỤC ĐÍCH:** chống "đoán tham số". Mọi action gọi webapp PHẢI tra bảng này — tên tham số,
> khóa response, GET/POST, cờ phá hủy đều đã đối chiếu với mã. KHÔNG suy diễn tên tham số.
> Khi webapp đổi → cập nhật file này + đổi dòng "Phiên bản deploy" ở trên.
>
> Gọi qua `scripts/gas.py`: `gas.get(action, **params)` / `gas.post(action, **payload)`
> (token + action tự thêm). POST = pattern 2 bước urllib (KI-01). Mọi response có thêm
> `_client_ms` (gas.py) và `elapsed_ms` (server).

---

## 0. BẪY THAM SỐ — ĐỌC TRƯỚC (nguồn gây sai nhiều nhất)

| Bẫy | Đúng | Sai (hay gặp) |
|---|---|---|
| Khóa số hiệu trong **registry / `reg_upsert` / `reg_get` / cột sheet** | **`sohieu`** (KHÔNG gạch dưới) | `so_hieu` → bị bỏ IM LẶNG |
| Khóa số hiệu trong **manifest JSON (entry)** | **`so_hieu`** (CÓ gạch dưới) | `sohieu` |
| `copy_convert` / `organize`(convert) / `fetch` / `ingest` / `upload` trả id GDoc ở khóa | **`fileId`** | `id` |
| `move` đích | `folderId` **hoặc** `cat` | `destFolderId` → silent fail; `removeFromParent` bị BỎ QUA (tự tính) |
| `exporttext` / `exportdocx` / `export` / `read`(text) | CHỈ Google-native (GDoc/GSheet) | gọi trên `.docx/.pdf` → 403/lỗi. Phải `copy_convert` trước |
| `find` trả danh sách ở khóa | **`rows`** | `results` / `hits` |
| `search` trả danh sách ở khóa | **`matches`** | `rows` / `files` |
| `vb_status` / `find` / `nlm_*` nhận số hiệu ở | `q` (và alias `soHieu`/`sohieu`) | `so_hieu` |
| `resolveFolder_` ưu tiên | `folderId` > `cat` > `toFolderId` > ROOT | (truyền cả folderId+cat → folderId thắng) |
| `importext`/`importlink` đích | `destFolderId` > `destName` > `cat` | **KHÔNG** dùng `folderId` (trong importlink, `id` là folder NGOÀI) |
| `reg_get name_contains` | Khớp chuỗi nguyên văn, chỉ để soi nhanh | Dùng để kết luận văn bản vắng mặt. Phải dùng `tl source-map` + `tl locate/status` |

**Action PHÁ HỦY / NẶNG — bắt buộc `confirm='yes'`:**
`trash` · `regen` · `regen2` · `reg_addcols` · `reg_delete` (+ `require_removed`).
(`source_delete` của NLM MCP: bất khả nghịch — hỏi người dùng trước.)

**Bắt buộc POST (body lớn, không nhét query string được):**
`upload` (b64) · `rasoat_state_cas` (b64) · `importext` (files[]) · `batch` (ops[]) · `reg_bulk` (items[]) · `createtext` (text dài) ·
`reg_delete` (drive_ids[]). Còn lại GET được (kể cả `reg_upsert`).

**Hằng số chốt (config mirror là nguồn sự thật):**
- `ROOT_FOLDER_ID` (VBQPPL gốc) = `11Rkwf3nhudPNNcsGlloV8acaXiXqdutJ`
- `_HOP_NAP` (staging upload DUY NHẤT) = `1bNSAKGACtk0x0cqX5QRVEGT12udi2g67`
- Notebook VBQPPL = `743ed200-2e55-4673-b7a0-9bfd13b41ce6`
- `REGISTRY_DOC_ID` = `1mATGFhaW0e_CYienAD80DsTS1K4zfJNlTAx-DsHaCD8`
- NLM Pro cap = **300 source/notebook**.

---

## 1. HỆ THỐNG / CONFIG

| action | GET/POST | params bắt buộc | params tùy chọn | response (khóa chính) |
|---|---|---|---|---|
| `ping` | GET | — | — | `ok, pong, ts, version:'2.21.2p', schema_version:'2.21.2p', registry_schema:'reg_cols_row_kind_v1', registry_cols, capabilities[]` |
| `config` | GET | — | — | `ok, version:'2.11.0', config, rootFolderId` (không lộ token) |
| `readconfig` | GET | — | — | `ok, mirrored, configFileId?, updated?, downloadUrl?, config` |
| `writeconfig` | GET | — | `webappUrl` | `ok, configFileId, name, rootFolderId, downloadUrl, config` |
| `categories` | GET | — | — | `ok, categories{NN:folderId}, source:'dynamic'` |
| `refreshcats` | GET | — | — | `ok, categories, source:'dynamic', refreshed:true` (ép quét lại folder) |
| `bootstrap` | GET | — | — | `ok, rootId, writable, inboxFolderId, inboxFolderUrl, vanBanThuongId, created` |
| `perf` | GET | — | `TL_SELFTEST_DOC_ID` (env) | `ok, ms{...}` (đo trên deployment thật) |

`config.categories` = map ĐỘNG quét từ TÊN folder `NN_<Chủ đề>` (nguồn sự thật). Đổi tên/tạo/xóa
folder → `refreshcats` để map đúng. Token đặt ở Script Property; mirror ra `tra_luat_config.json`.

---

## 2. FILE OPS (cây corpus)

| action | GET/POST | bắt buộc | tùy chọn | response |
|---|---|---|---|---|
| `list` | GET | — | `folderId`\|`cat`, `recursive` | `ok, folderId, count, capped, items[{id,name,mime,size,type}]` |
| `info` | GET | `fileId` | — | `ok, file{...,appProperties}, note` (Google-native: size/md5 rỗng → dùng appProperties.sha256) |
| `rename` | GET | `fileId`, `name` | — | `ok, fileId, oldName, newName` |
| `move` | GET | `fileId` | `folderId`\|`cat` | `ok, fileId, toFolderId, parents, removedFrom` |
| `mkdir` | GET | `name` | `parentId` (mặc định ROOT) | `ok, folderId, name, created` |
| `trash` | GET | `fileId`, **`confirm='yes'`** | — | `ok, fileId, name, trashed` |
| `restore` | GET | `fileId` | — | `ok, fileId, trashed:false` |
| `share` | GET | `fileId` | — | `ok, fileId, shared:'ANYONE_WITH_LINK/VIEW'` |
| `shortcut` | GET | `id`, `cat` | — | `ok, shortcutId, target, cat` (đa-lĩnh vực — KI-05) |
| `verifyShares` | GET | — | `folderId`\|`cat` | `ok, scanned, reshared, failed, failsSample` |
| `dedup` | GET | — | `folderId`\|`cat` | `ok, scanned, duplicateGroups, note` (trash thủ công) |
| `findprop` | GET | `key`, `value` | — | `ok, matches[{id,name,appProperties,parents}]` |
| `perm_list` | GET | `id` | — | `ok, id, permissions[]` |
| `pinRevision` | GET | `fileId` | — | `ok, fileId, pinned` |
| `meta_set` | POST | `id` | `loai,sohieu,linhvuc,linhvuc2,goc,hieuluc,vbhn,extra(JSON)` | `ok, id, appProperties, truncated[]` (tự cắt 124B/cặp — KI-06) |
| `meta_find` | GET | `goc` HOẶC (`key`+`value`) | `fields,pageSize,pageToken` | (như `search`) — ✓ đã vá ở 2.21.2b |
| `stamp` | GET | `fileId` | `props(JSON)` hoặc `sha256,sourceUrl,soHieu,nam,loai,coquan,hieuLuc` | `ok, fileId, props` |

> `verifyShares`/`dedup`/`list recursive` quét cả cây qua `listTree_`.

---

## 3. NẠP FILE — 4 ĐƯỜNG VÀO (không lẫn lộn)

| action | GET/POST | bắt buộc | tùy chọn | response | dùng khi |
|---|---|---|---|---|---|
| `ingest` | GET | `url` | `title, cat`\|`folderId, convert, share, register, force, soHieu/nam/loai/coquan/hieuLuc` | `ok, fileId, name, mime, converted, sha256, bytes, viewUrl, note` / `ok,skipped,reason,existing` | URL công khai → Drive (server-side, dedup sha256) |
| `fetch` | GET | `url` | `title, cat`\|`folderId, share` | `ok, fileId, name, mime` | tải raw không convert/không dedup |
| `upload` | **POST** | `b64`, `name` | `mime, cat`\|`folderId, convert, props, force, sourceUrl` | (như `ingest`) | bytes base64 từ container (≤35MB) |
| `rasoat_state_cas` | **POST** | `b64`, `name='rasoat_state.json'`, `folderId` | `expect_claim` (bắt buộc khi state đã tồn tại) | `ok, fileId, old_count, cleanup[], don_sach, action_atomic:true` / `ok:false,error:THIEU_EXPECT_CLAIM\|CLAIM_LECH\|…` | LockService ôm list/read/compare/create/cleanup; không share/register, client không fallback upload rời |
| `createtext` | **POST** | `text` | `name`\|`title, cat`\|`folderId, share, register, sourceUrl` | `ok, fileId, name, created, viewUrl, downloadUrl` | text đã normalize → GDoc (giữ newline) |
| `copy_convert` | GET | `fileId` | `name`\|`title, cat`\|`folderId, toType, share, register` | `ok, fileId, name, mime, srcFileId, srcName, folderId, viewUrl` | file `.docx/.doc/.pdf` ĐÃ ở Drive → GDoc/GSheet (luồng đúng nhất) |
| `fetch_url_to_drive` | GET | `url` | — | `ok, fileId, gdocId, docxId, name, isDoc` / `ok:false, reason:'gated'` | DISCOVERY .doc/.docx ungated → `_HOP_NAP`. ✓ đã vá ở 2.21.2b |

> `copy_convert.toType`: `doc` (mặc định) / `sheets` (.xlsx/.csv) / `slides`. NLM chỉ nạp GDoc/GSheet.
> `smartConvert_`: `.docx/.doc` → convert mặc định; **PDF KHÔNG convert mặc định** (OCR nuốt trang scan
> — KI-26); ép convert PDF bằng `convert='true'` tường minh sau khi đã verify.
> KHÔNG truyền `cat`/`folderId` → đổ vào ROOT.

---

## 4. EXPORT / ĐỌC NỘI DUNG (chỉ Google-native)

| action | GET/POST | bắt buộc | tùy chọn | response |
|---|---|---|---|---|
| `read` | GET | `id` | `offset, limit, mime` | `ok, id, name, mime, total, offset, returned, more, text` (lát cắt — KI-02) |
| `exporttext` | GET | `fileId` | — | `ok, fileId, chars, text` (UTF-8) |
| `exportdocx` | GET | `fileId` | — | `ok, fileId, bytes, b64` (.docx base64) |
| `export` | GET | `fileId` | `mimeType, toFolderId, name` | `ok, fileId, name` (lưu file mới vào Drive) |
| `download` | GET | `fileId` | `exportMime, as('text')` | `ok, fileId, name, mime, bytes, b64` (file BẤT KỲ; native thì export) |

> Trần export ~10MB. `.docx/.pdf` chưa convert → lỗi, kèm hướng dẫn `copy_convert`.
> **Quy tắc token-tiết-kiệm:** export ra ĐĨA → regex trích đúng Điều → in đoạn ngắn.
> TUYỆT ĐỐI không cat toàn văn vào context.

---

## 5. IMPORT NGOÀI (link Drive ngoài corpus)

| action | GET/POST | bắt buộc | tùy chọn | response |
|---|---|---|---|---|
| `listext` | GET | `folderId`\|`id` | `pageToken` | `ok, folderId, count, files[], folders[], nextPageToken, capped` |
| `resolvefolder` | GET | `name` | `parentId, create` | `ok, folderId, name, created, url` (find-or-create) |
| `importext` | **POST** | `files[]` (≤30, `[{id,name?}]`) | `destFolderId`\|`destName`(+`destParentId`)\|`cat, share, register, force` | `ok, destFolderId, count, okCount, dedupSkipped, results[], remainingIds[]` |
| `importlink` | **POST** | `id` (folder/file ngoài) | `destFolderId`\|`destName`\|`cat, share, register, max(≤30), pageToken, skipIds, force` | folder: `ok,kind,srcFolder,destFolderId,copied,results[],remainingIds[],subfolders[]` · file: `ok,kind:'file',results[]` |

> Folder ngoài không chỉ đích → tự tạo subfolder CÙNG TÊN trong ROOT. Tự dừng ~4.5' / đủ `max`
> → trả `remainingIds` + `nextPageToken` cho đợt sau. `subfolders` → HỎI người dùng trước khi đệ quy.
> Dedup idempotent theo appProperties `srcMd5`/`srcId`. `results[].fileId` (GDoc) → `source_add(drive,doc)`.
> **Định tuyến tìm file:** TRONG corpus → `search scope=corpus`/registry; NGOÀI corpus/shared/My Drive root
> → **Drive MCP `search_files`** (webapp `scope=all` quét THIẾU — v1.14.0).

---

## 6. REGISTRY (Sheet = sổ cái sống) + NLM MAP

> **v1.19 (GS ≥ 2.21.2h):** MỌI action registry (`reg_get/reg_upsert/reg_bulk/reg_clear/map_set/organize/
> regen2/find/locate/source_map/nlm_*`) nhận tham số tùy chọn `registryDocId` (Sheet registry của profile);
> thiếu ⇒ Sheet VBQPPL nền. `tl.py --profile P` tự thêm. Truyền `registryDocId` sai/không mở được ⇒ lỗi rõ
> (KHÔNG fallback VBQPPL, tránh ghi nhầm corpus).
> Cột sheet `REG_COLS_` (thứ tự cố định): `drive_id, src_id, sohieu, loai, name, cat, mime, md5, size,
> modified_time, linhvuc, goc, nlm_source_id, nlm_status, nlm_pushed_at, verified, registered_at, note,
> title_vn, linhvuc_list, hieuluc, sua_doi, nlm_title, corpus, nlm_notebook_id, tukhoa`.
> `nlm_status ∈ {'', pending_push, pushed, synced, stale, failed, removed_from_drive}`.

| action | GET/POST | bắt buộc | tùy chọn | response |
|---|---|---|---|---|
| `reg_get` | GET | `sohieu`\|`drive_id`\|`nlm_source_id`\|`name_contains` | `refresh` | `ok, count, rows[]` |
| `reg_upsert` | GET | `drive_id` | **bất kỳ cột REG_COLS_** (dùng `sohieu`, KHÔNG `so_hieu`) | `ok, drive_id, updated` |
| `reg_bulk` | **POST** | `items[]` (`[{drive_id\|nlm_source_id, <cột>}]`) | `cols` (mặc định `'nlm_title'`) | `ok, total, patched, missed, miss[], cols[]` |
| `reg_delete` | **POST** | **`confirm='yes'`**, `drive_ids[]` | `require_removed` (mặc định `'yes'`) | `ok, requested, removed, skipped_live, not_found` — v2.21.2p tự khai `expect_shrink` = số dòng xóa (KI-27) |
| `reg_clear` | GET | `drive_id`\|`nlm_source_id` | `cols` (nlm_*/note tự do; **2.21.2l: cột thường ∈ REG_COLS_ cần thêm `force='yes'`; drive_id/name BẢO VỆ**), `confirm='yes'` | `ok, cleared, drive_ids[], cols[]` |
| `reg_addcols` | GET | **`confirm='yes'`** | — | `ok, cols, header[]` (ghi lại header sheet — chạy 1 lần sau khi thêm cột) |
| `reg_bak_list` | GET | — | — | `ok, current_rows, keep, count, baks[]` (`{tab,stamp,rows}`, mới→cũ) — **v2.21.2p KI-27** CHỈ ĐỌC: liệt kê bản sao registry xoay vòng `files_bak_<ts>` (giữ 5 bản, sinh tự động mỗi lần `regWriteAll_`) |
| `reg_bak_restore` | **POST** | **`confirm='yes'`**, `tab` (`files_bak_<ts>`) **hoặc** `stamp` | — | `ok, restored_from, rows_before, rows_after` — **v2.21.2p KI-27**: thay TOÀN BỘ registry bằng bản sao; bản đang dùng được giữ thành `files_bak_<ts>` mới ⇒ khôi phục ĐẢO NGƯỢC được. Chạy `manifest_export` sau đó |
| `map_set` | GET | `drive_id`\|`sohieu` | `nlm_source_id, status, notebookId`(=`nlm_notebook_id`\|`notebook`)`, nlm_title` | `ok, drive_id, updated` (gọi SAU mỗi `source_add` ok; **v1.18: LUÔN truyền `notebookId` để slot đếm đúng theo notebook**) |
| `map_unpushed` | GET | — | `includeStale, refresh` | `ok, count, rows[], nlm_quota{tier,cap,pushed,slots_free}` |
| `map_mark_stale` | GET | `drive_id` | — | `ok, drive_id, updated` |
| `register` | GET | `fileId` | `name, mime, sha256` | `ok, fileId, registered` (chữ ký cũ; ghi vào sheet) |
| `ingest_claim` | **POST** | `run_id`; `keys[]` (mảng `identity_hash`) và/hoặc `release_keys[]` | `drive_ids[]` (song song `keys`, chỉ để lưu tham khảo) | `ok, run_id, results:[{identity_hash,granted,reason,source_id?}], granted, denied, released[], release_failed[]` |
| `reg_get_bulk` | GET/POST | `keys[]` | `key_field` (`'drive_id'`\|`'nlm_source_id'`, mặc định `drive_id`), `commit_claims[]` (`[{identity_hash,source_id,run_id}]`) | `ok, key_field, count, rows[]` (NGUYÊN THỨ TỰ `keys`, không khớp → `null`; TOÀN BỘ 27 `REG_COLS_`/dòng) + `committed[], commit_failed[]` nếu có `commit_claims` |
| `profile_catalog` | GET | `folderId` (vanBanThuongId) | `folderCap` (mặc định 60, trần 200) | `ok, schema='profile_catalog.v1', folder_total, capped, folders[]` (`{id,name,meta_folder_id,items[],markers[{id,json_text,error}]}` — items = con folder ∪ con `_meta`, sort name→id; MỌI bản marker trùng đều liệt kê, client tự phát hiện DUPLICATE), `root_files[]` — v2.21.2n (r185/WP5): 1 call thay ~3×N call discover/doctor |
| `drive_info_bulk` | GET/POST | `ids[]` (JSON array, ≤200) | — | `ok, schema='drive_info_bulk.v1', count, results[]` (`{id,ok,name,mime,size,parents[],trashed,modifiedTime}` — GIỮ THỨ TỰ input, lỗi per-item không phá lô) — v2.21.2n (r185/WP5): probe template/asset theo lô |
| `ingest_commit` | GET | `fileId` | đúng bộ `organize` (`convert, name, moveSrc, cat` = mã NN vbqppl HOẶC folderId flat profile, `sohieu/loai/hieuluc`, `reg_*`, `share, register`) | `ok, organize_done, rename_done, upsert_done, fileId, srcId, row` (snapshot registry sau register, `reg_get refresh=true`), `file`/`src_file` (`{id,name,mimeType,md5,size,parents[]}`), `elapsed_ms`; lỗi giữa chừng → `ok=false + step + PARTIAL marker` (đã-xong-gì, không im lặng) — v2.21.2p (r198/ADR-0014): thay chuỗi organize→info×N→reg_get×N MỘT round-trip; client `profile-ingest` feature-detect ≥2.21.2p, fallback đường cũ; `ingest-local` CHƯA chuyển (soak trước) |

> **v2.21.2l (F-04/F-08 — ĐÃ DEPLOY, LIVE trong 2.21.2m; xem CHANGELOG v1.34.52/55):** `ingest_claim` là
> reservation identity XUYÊN HOST (Sheet tab `claims` riêng, TTL 5 phút) — acquire TRƯỚC `source_add`, chống 2
> host cùng nạp 1 nội dung. `granted=false` với `reason='ALREADY_COMMITTED'` kèm `source_id` → LINK thay vì add
> lại; `reason='HELD_BY_OTHER'` → thử lại sau (không phải lỗi). `reg_get_bulk.commit_claims` GỘP commit claim
> vào cùng round-trip readback (không round-trip riêng) — `commit_failed[].reason='RUN_ID_MISMATCH'` nghĩa là
> claim đã bị host khác reclaim (đã hết TTL) SAU khi bạn acquire — đừng ghi đè, chạy lại từ đầu cho item đó.

> `reg_bulk` AN TOÀN: mặc định CHỈ vá cột `nlm_title`; mở rộng có kiểm soát qua `cols='nlm_title,nlm_status'`
> (chỉ nhận cột thuộc REG_COLS_); chuỗi rỗng KHÔNG ghi đè; item không khớp → `miss` (tín hiệu mồ côi).
> `reg_delete` mặc định CHỈ xóa dòng `nlm_status` bắt đầu `removed` (bảo vệ dòng live); `require_removed='no'`
> để xóa bất kể (cẩn trọng).
> `name_contains` là raw string match: phân biệt dấu/gạch nối/gạch dưới và không chuẩn hóa tiếng Việt. Không dùng để kết luận "không có trong nguồn".
> Tiêu chí "query được trên NLM" là có `nlm_source_id` và không bị đánh dấu removed; `nlm_status='added'/'paired'/'stale'` là nợ chuẩn hóa metadata, không tự phủ nhận nguồn.

---

## 7. NLM PREFLIGHT / TRẠNG THÁI VĂN BẢN (server-side, không kéo manifest)

| action | GET/POST | bắt buộc | tùy chọn | response |
|---|---|---|---|---|
| `vb_status` | GET | `q` (\|`soHieu`\|`sohieu`) | `refresh` | `ok, sohieu, is_vbhn, in_drive, on_nlm, hieuluc, effective_date, pending_effect, status, flags[], self, self_count, superseded_by[], supersedes[]` |
| `nlm_slots` | GET | — | `notebookId, baseNotebookId, cap(300), refresh, countRefs/count_refs, warnThreshold/overflowThreshold` | `ok, notebookId, cap, used, remaining, full, near_full, warn_threshold, count_refs, byStatus, base_notebook, verify_live_recommended` |
| `nlm_dedup` | GET | (≥1 khóa) `driveId`/`srcId`/`md5`/`soHieu`/`name` | `notebookId, baseNotebookId, refresh, max` | `ok, duplicate, count, hits[], pending[], pending_count, review[], review_count, cand_key` |
| `nlm_preflight` | GET | `q`\|`soHieu`\|`name` | `notebookId, baseNotebookId, cap, driveId, srcId, md5, findMax, refresh, normative/isNormative/vbqppl, overflowProfile/overflowNotebookId` | `ok, decision:ADD\|SKIP\|REVIEW, reasons[], slots, dedup, find, overflow_route{+slots,has_room,full}, overflow_slots, superseded_matches[]` |
| `find` | GET | `q` | `max, refresh` | `ok, tier:'sohieu'\|'name'\|'fulltext', count, rows[]` |
| `search` | GET | `q` (\|`name`) | `max, refresh` | `ok, scope:'registry', count, matches[]` |
| `resolve` | GET | `name` | `scope, max` | (delegate → `search`) |

> ✓ `find` tầng-3 + `meta_find` đã vá ở 2.21.2b (driveSearch_).
> `vb_status.status ∈ {PENDING_EFFECT, VBHN_PENDING_EFFECT, IN_FORCE, IN_FORCE_CONSOLIDATED, SUPERSEDED, CONSOLIDATED_INTO_VBHN,
> VBHN_IN_FORCE, VBHN_SUPERSEDED, VBHN_IN_REGISTRY_NOT_ON_NLM (sau F11b/2.21.2b), NOT_IN_REGISTRY, IN_REGISTRY_HIEULUC_UNKNOWN}`.
> **CỔNG TIỀN-NẠP (QT-2):** trước khi `organize`+`map_set`/`source_add` BẤT KỲ văn bản sửa đổi/VBHN/
> nghi bị thay thế → chạy `vb_status` (hoặc `nlm_preflight`) cho số hiệu chính + số hiệu đích bị sửa.
> `nlm_preflight.decision`: ADD → source_add · SKIP → trùng/đầy · REVIEW → HỎI người dùng.
>
> **v2.21.2l — ĐẾM SLOT SHARD OVERFLOW TRƯỚC KHI ROUTE:** khi route overflow (base đầy/gần-đầy + overflow
> cấu hình), `nlm_preflight` gọi `nlm_slots` cho chính shard overflow → trả `overflow_slots` (used/remaining/
> full/near_full) + `overflow_route.{slots,has_room,full}`. Base+overflow ĐỀU đầy → reason
> `ALL_SHARDS_FULL_ASK_USER` (GIỮ decision=REVIEW: HỎI người dùng duyệt shard mới, KHÔNG khuyên add vào shard
> đầy). Trước 2.21.2l chỉ đếm base rồi route overflow MÙ (audit v1.34.46). Client v1.34.47 đã fail-closed độc lập.
>
> **v1.18/v1.19 — ĐẾM SLOT THEO NOTEBOOK (sửa `NOTEBOOK_FULL` giả, GS ≥ 2.21.2h):** `nlm_slots`/`nlm_preflight`/
> `nlm_dedup` chỉ đếm/đối chiếu dòng có `nlm_notebook_id == notebookId`. Dòng RỖNG `nlm_notebook_id`
> (legacy đẩy lên VBQPPL) quy về `baseNotebookId` (mặc định `743ed200-…`) ⇒ KHÔNG cộng vào notebook dự án
> khác (vd `fec6c125-…` không còn báo 314/300 giả), nhưng VẪN tính đúng cho VBQPPL mà không cần backfill.
> `row_kind=ref` không tính vào slot registry mặc định; `countRefs=true`/`count_refs=true` tính cả dòng tham chiếu
> để đối chiếu notebook dự án. Khi đẩy phải `map_set notebookId=…`. Trước khi `source_add`, lấy số vật lý
> bằng `notebook_get.source_count` vì NLM có thể đang có 37 nguồn trong khi registry own/overflow chỉ 13.
> CLI đối chiếu registry estimate: `tl slot-audit --notebook-id <id> --json`.
> **PHÂN GIẢI SỐ HIỆU (chống nhầm):** khóa khớp theo (số + năm + loại + chủ đề), KHÔNG khớp mờ chỉ theo số;
> push NLM phải verify tên/nội dung (đọc dòng đầu) trước khi chốt.

---

## 8. REGEN / MANIFEST / BATCH / DELTA

| action | GET/POST | bắt buộc | tùy chọn | response |
|---|---|---|---|---|
| `regen2` (v2.21.2p: nhận thêm `expect_shrink=<n>` — bắt buộc khi phép co chạm ngưỡng thảm hoạ KI-27) | GET | **`confirm='yes'`** | `refresh, registryDocId, manifestScope=own|inherited, rootFolderId, profileName, categoriesMode, confirmInherited=yes, confirmBlowup=yes` | `ok, treeHash, count, corpus_count, old_own_count, new_own_count, manifest_scope, stats, elapsedMs`; hoặc `PROFILE_MANIFEST_SCOPE_BLOWUP` trước khi ghi |
| `manifest_export` | GET | — | `registryDocId, manifestId` (v1.19) | `ok, manifestId, treeHash, count, corpus_count, so_hieu_parsed, so_hieu_missing, schema_version, registry_scope, manifest_scope` |
| `manifest` | GET | — | — | `ok, manifestFileId, name, updated, downloadUrl` (đọc metadata) |
| `regen` (cũ) | GET | **`confirm='yes'`** | — | `ok, count, treeHash, manifestFileId` (ghi Doc registry + JSON — LEGACY, ưu tiên `regen2`) |
| `batch` | **POST** | `ops[]` (`[{action,...}]`) | — | `ok, summary{total,done,failed}, results[]` |
| `changes_init` | GET | — | — | `ok, startPageToken, note` |
| `changes_pull` | GET | — | `apply, applySheet, refresh` | `ok, pages, deltas[], count, applied, sheetApplied, tokenReset, elapsedMs` |
| `inbox_status` | GET | — | — | `ok, inboxFolderId, count, items[], uploadUrl` |
| `inbox_process` | **POST** | — | `cat, map(JSON), dryRun, peek, maxFiles, share, register` | `ok, done[], quarantined[], pending[], errored[], processed, remaining` |

> **`regen2` GIỮ cột curate** `REG_NLM_KEEP_` = `nlm_source_id, nlm_status, nlm_pushed_at, verified, note,
> loai, linhvuc, goc, src_id, title_vn, linhvuc_list, hieuluc, sua_doi, nlm_title, nlm_notebook_id, tukhoa`
> (KI-21). Cột MỚI muốn sống qua regen2 → thêm vào CẢ `REG_COLS_` lẫn `REG_NLM_KEEP_` rồi Deploy +
> `reg_addcols&confirm=yes`.
> **Scope profile (2.21.2l):** profile khác `vbqppl` mặc định `manifestScope=own`, chỉ quét `rootFolderId`
> và mọi subfolder của chính profile. `categoriesMode=inherit` không cấp quyền quét cây category VBQPPL.
> Dòng `row_kind=ref` được giữ nguyên khi quét own. Trước `regWriteAll_`, guard chặn nếu
> `new_own_count > max(2×old_own_count, old_own_count+50)`; override có chủ ý bằng `confirmBlowup=yes`.
> **Sinh manifest 1 lệnh:** `scripts/_fallback/manifest_build.py` = `regen2` + `manifest_export` (tự kiểm regen2 ok mới export).
> `inbox_process` mặc định đọc `_HOP_NAP` (từ v2.18.0; bản cũ trỏ nhầm `_INBOX`).

---

## 9. NLM MCP (notebooklm-jacob — KHÔNG phải webapp)

| tool | tham số chốt | ghi chú |
|---|---|---|
| `source_add` | `source_type='drive', document_id=<gdoc id>, doc_type='doc', wait=true` | CHỈ Google Doc. ≤5 file Claude tự nạp tuần tự; >5 → HỎI người dùng |
| `notebook_query` | `notebook_id, query, source_ids=[…]` (1–3, hard cap 5) | scope đúng source_id; verify trích dẫn với cache/raw (KHÔNG nhận RAG làm nguyên văn) |
| `notebook_get` | `notebook_id` | lấy id+title nhanh; dùng khi KHÔNG có CLI `nlm` |
| `source_list_drive` | `notebook_id` | **TRÁNH** — ép freshness → timeout ~4', MCP không phơi `skip_freshness` |
| `source_delete` | `confirm=True` | bất khả nghịch — HỎI người dùng trước |

> **FAST-LANE (Claude Code/Cowork) — MỌI ĐỌC NLM qua CLI `nlm`, KHÔNG qua MCP** (qua `scripts/nlm_cli.py`):
> - `tl nlm-list <nb>` = `nlm source list -S -d -j` — liệt kê ~4s (đo 299); thay `source_list_drive` (MCP timeout ~4'); CLI có `--skip-freshness` MCP thiếu.
> - `tl nlm-content <src>` = `nlm source content -j` — toàn văn raw; thay `source_get_content` (MCP TRÀN TOKEN doc lớn).
> - `tl nlm-query <q>` = `nlm notebook query -j` — RAG; thay `notebook_query`. get/describe: `nlm source/notebook get|describe`.
> Cùng package `notebooklm-mcp-cli` với MCP server. MCP CHỈ fallback (thiếu CLI/auth) hoặc GHI (source_add/studio). Đối soát: `tl nlm-reconcile`. Auth tự refresh; hết hạn → `nlm login`.

---

## 10. KHÓA RESPONSE PHỔ BIẾN (đỡ phải nhớ)

- Mọi action ok: `ok:true`. Lỗi: `ok:false, error:'...'` (đôi khi `reason:'gated'`).
- ID file mới tạo: **luôn `fileId`** (copy_convert/ingest/fetch/upload/createtext/fetch_url_to_drive).
- Danh sách kết quả: `find`→`rows` · `search`→`matches` · `list`→`items` · `reg_get`→`rows` ·
  `listext`→`files`/`folders` · `import*`→`results`.
- Phân trang ngoài: `nextPageToken` (listext/importlink); cờ cắt: `capped`.
- Thời gian: `elapsed_ms` (server, mọi action) + `_client_ms` (gas.py).

---

## 11. CONFIG SCHEMA v2 — ĐA-CORPUS (PROFILE) — v1.18

> File mirror `tra_luat_config.json` lưu TRONG folder VBQPPL như cũ (Drive ID
> `1_-rK3Vv1nCfF1a44JL0kLUXwSks7YOSP`). Client tự nhận `schema:2` (thiếu `schema` ⇒ coi v1, tương thích cũ).
> `webappUrl`/`token` LUÔN lấy từ file VBQPPL này; profile chỉ overlay folder/notebook/registry/manifest.
> CLI: `tl --profile <name> profile-info --json` để xem profile đang dùng (chi tiết `references/MULTI_CORPUS_PROFILE_V1_18.md`).

```json
{
  "schema": 2,
  "webappUrl": "<từ VBQPPL>",
  "token": "<từ VBQPPL>",
  "defaultProfile": "vbqppl",
  "profiles": {
    "vbqppl": {
      "rootFolderId": "11Rkwf3nhudPNNcsGlloV8acaXiXqdutJ",
      "notebookId": "743ed200-2e55-4673-b7a0-9bfd13b41ce6",
      "registryDocId": "1mATGFhaW0e_CYienAD80DsTS1K4zfJNlTAx-DsHaCD8",
      "manifestId": "1d8Pau1x-Qeq0i8ClQnxuTMohGNf6GEeI",
      "categories": { "...": "giữ nguyên" }
    },
    "vbthuong": {
      "rootFolderId": "<TẠO MỚI hoặc dùng folder Van_ban_thuong sẵn có>",
      "notebookId": "fec6c125-e01c-433d-aed5-666c16540dd8",
      "registryDocId": "<TẠO MỚI>",
      "manifestId": "<TẠO MỚI>",
      "categories": "inherit"
    }
  }
}
```

- **Profile NỀN `vbqppl`**: corpus pháp điển VBQPPL + token/webapp dùng chung. **Profile dự án `vbthuong` (…)**:
  VĂN BẢN THƯỜNG, có folder/notebook/registry/manifest RIÊNG. Chọn qua env `TL_PROFILE`/cờ `--profile`;
  không chỉ định ⇒ `defaultProfile` (`vbqppl`). `tl` map profile → env `TL_ROOT_FOLDER_ID`/`TL_NOTEBOOK_ID`/
  `TL_REGISTRY_DOC_ID`/`TL_MANIFEST_ID`; cache manifest tách theo profile (`~/.tra_luat_cache/<profile>/`).
- **TẠO manifest/registry riêng cho profile mới** (qua webapp, sau khi người dùng duyệt folder/notebook đích):
  1. Folder: chọn/tạo folder Drive (`Van_ban_thuong/...` có thể dùng làm gốc) → `rootFolderId`.
  2. Registry riêng: Google Sheet mới theo ĐÚNG `REG_COLS_` + `REG_NLM_KEEP_` (`sohieu, loai, name, cat,
     drive_id, nlm_source_id, nlm_status, nlm_notebook_id, nlm_pushed_at, verified, goc, sua_doi, hieuluc, …`)
     → `registryDocId`.
  3. Manifest riêng: `manifest_export` với đích registry/notebook của profile → `tra_luat_manifest.vbthuong.json`
     → `manifestId`.
  4. Ghi 3 ID vào `profiles.vbthuong`.
- **Precedence tra cứu**: registry/manifest của profile P trước → MISS mới fallback VBQPPL (báo "lấy từ VBQPPL");
  QA xuyên corpus `cross_notebook_query(notebook_names="<P.notebookId>,743ed200-…")`; canonical của P thắng.
