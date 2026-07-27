# tra-luat — PATCH Apps Script → v2.21.1 (DÁN TAY + Deploy New version)

> Bản HỢP NHẤT mọi lỗi/điều-chỉnh rà soát được trên webapp 2.20.0 (F1–F7). Áp dụng xong:
> Deploy → New version (GIỮ URL+token) → `ping` trả `2.21.1` → `regen2 confirm=yes` → `manifest_export`.
> Sau deploy: đổi `references/API_CONTRACT.md` (dòng "Phiên bản deploy" → 2.21.1; gỡ cảnh báo
> meta_find/find-fulltext "HỎNG") + `EXPECT_VERSION` trong `scripts/tl.py` → `2.21.1`.

| Mã | Mức | Nội dung |
|---|---|---|
| F1 | P0 | khôi phục Drive-query cho `meta_find` + `find` tầng-3 fulltext (đang chết) |
| F2 | P0 | alias `configView` (boot.py gọi action không có) |
| F3 | P1 | một hằng `APP_VERSION` (đang rải rác 2.20/2.14/2.11/2.15) |
| F4 | P1 | chuẩn hóa appProperties về CHỮ THƯỜNG (`sohieu/hieuluc`) khớp regen2/meta_set |
| F5 | P1 | treeHash `manifest_export` cùng cơ sở corpus với `regen2` |
| F6 | P2 | khai tử `regen`/`regenRegistry` legacy (Doc-registry, schema cũ) |
| F7 | P2 | gỡ chia-sẻ-công-khai cho mirror chứa token (giảm lộ token) |

---

## F3 — Một hằng phiên bản

**(a) THÊM** ngay trên `var CONFIG = {` :
```js
var APP_VERSION = '2.21.1';   // NGUỒN SỰ THẬT phiên bản — mọi response đọc biến này
```
**(b) THAY** các chuỗi version rải rác:
```js
case 'ping':  return {ok:true, pong:true, ts:new Date().toISOString(), version:APP_VERSION};
// doBootstrap_:        version:'2.14.0' → version:APP_VERSION
// doConfigView_:       version:'2.11.0' → version:APP_VERSION
// doFetchUrlToDrive_:  version:'2.15.0' → version:APP_VERSION
// doRegen2_ _meta:     ['version','2.14.0'] → ['version', APP_VERSION]
// doManifestExport_:   out.version '2.20.0' → APP_VERSION ; return schema_version:'2.20.0' → APP_VERSION
```

---

## F2 — Alias `configView`

Trong `dispatchAction_`, gộp:
```js
    case 'config':
    case 'configView':   return doConfigView_(p);   // boot.py dùng 'configView'
```

---

## F1 — Khôi phục Drive-query (meta_find + find-fulltext)

**(a) THÊM** hàm mới ngay TRÊN `function doSearch_`:
```js
/* driveSearch_ — TRA bằng Drive.Files.list (q nguyên bản: name/fullText contains,
 * appProperties has {...}). KHÁC doSearch_ (dựa registry). Cho meta_find + find tầng-3.
 * scope='corpus' → OR folder corpus 2 cấp (KI-04: 'in parents' KHÔNG đệ quy). */
function driveSearch_(p){
  var fields = sanitizeFields_(p.fields || cfgSearchFields_());
  var pageSize = Math.min(Number(p.pageSize)||cfgNum_('TL_SEARCH_PAGESIZE',100), 1000);
  var clauses = [];
  if (p.q) clauses.push('('+p.q+')');
  var parents = [];
  if (p.cat){ var cid=resolveCatFolderId_(p.cat); if(cid) parents.push(cid); }
  else if (String(p.scope)==='corpus'){ parents = corpusFolders_(String(p.refresh)==='true').ids; }
  if (parents.length)
    clauses.push('('+parents.map(function(id){return "'"+id+"' in parents";}).join(' or ')+')');
  clauses.push('trashed=false');
  if (String(p.includeFolders)!=='true' && (p.cat||String(p.scope)==='corpus'))
    clauses.push("mimeType!='application/vnd.google-apps.folder'");
  var req = { q:clauses.join(' and '), pageSize:pageSize,
              fields:'nextPageToken,files('+fields+')',
              supportsAllDrives:true, includeItemsFromAllDrives:true };
  if (p.orderBy) req.orderBy = p.orderBy;
  if (p.pageToken) req.pageToken = p.pageToken;
  var r = Drive.Files.list(req);
  return { ok:true, scope: p.cat?('cat:'+p.cat):(p.scope||'q'),
           count:(r.files||[]).length, files:r.files||[], nextPageToken:r.nextPageToken||'' };
}
```
**(b) `doMetaFind_`** — đổi dòng cuối:
```js
  return driveSearch_({ q:q, scope:p.scope||'corpus', fields:p.fields, pageSize:p.pageSize, pageToken:p.pageToken });  // B: mặc định corpus
```
**(c) `doFind_` tầng-3** — thay khối fulltext:
```js
  var ft = driveSearch_({ q: "fullText contains '" + qEsc_(q) + "'", scope:'corpus', pageSize:MAX });
  var byId2 = {}; objs.forEach(function(o){ byId2[o.drive_id] = o; });
  var rows = (ft.files||[]).map(function(f){
    return byId2[f.id] || { drive_id:f.id, name:f.name, mime:f.mimeType, cat:'', sohieu:'', nlm_source_id:'' };
  });
  return { ok:true, tier:'fulltext', count:rows.length, rows:rows };
```
> (Tùy chọn) `doPerf_`: đổi `doSearch_({q:"appProperties has..."})` → `driveSearch_(...)` để đo đúng.
> `action=search` GIỮ NGUYÊN bản registry. Có thể thêm `case 'drive_search': return driveSearch_(p);` nếu muốn gọi trực tiếp.

---

## F4 — Chuẩn hóa appProperties về CHỮ THƯỜNG

`provenance_` đang ghi `soHieu/hieuLuc` (camel) trong khi `regen2` đọc `ap.sohieu`, `meta_set` ghi `sohieu`
⇒ số hiệu stamp lúc ingest KHÔNG được regen2 nhặt. THAY `provenance_`:
```js
function provenance_(p, sha, url){
  // v2.21.1 (F4): ghi khóa THƯỜNG (sohieu/hieuluc) khớp regen2 + meta_set; nhận cả input camel/thường.
  return {sohieu:p.soHieu||p.sohieu||'', nam:p.nam||'', loai:p.loai||'',
          coquan:p.coquan||'', hieuluc:p.hieuLuc||p.hieuluc||'',
          sha256:sha||'', sourceUrl:url||'', ingestedAt:new Date().toISOString()};
}
```
> File đã stamp `soHieu` (camel) trước đây: regen2 vốn đã bỏ qua (dùng `sohieuFromName_`), nên KHÔNG regress;
> file mới sẽ được regen2 nhặt đúng. (F4 phụ thuộc F6 — sau khi gỡ legacy `regen`, không còn ai đọc `ap.soHieu`.)

---

## F5 — treeHash cùng cơ sở corpus

Trong `doManifestExport_`, thay khối dựng `out`:
```js
  var corpusObjs = objs.filter(function(o){ return String(o.corpus)==='true' && o.loai!=='thuong'; });
  var out = {
    version: APP_VERSION, schema: 'uniform-v1', generatedAt: new Date().toISOString(),
    treeHash: treeHashV2_(corpusObjs),                 // F5: cùng cơ sở regen2 _meta
    count: objs.length, corpus_count: corpusObjs.length,
    so_hieu_parsed: nParsed, so_hieu_missing: nMissing,
    entries: entries
  };
```
(Bỏ `treeHash: treeHashV2_(objs)` cũ; có thể thêm `corpus_count` vào `return`.)

---

## F6 — Khai tử `regen` legacy (giữ `regen2`/`manifest_export`/`manifest`)

Trong `dispatchAction_`, THAY:
```js
    case 'regen':
    case 'regenRegistry': return {ok:false, deprecated:true,
      error:'regen (Doc-registry, schema cũ) đã ngừng — dùng regen2 (confirm=yes) + manifest_export.',
      use:['regen2','manifest_export']};
```
Và XÓA hẳn `function doRegen_(p){ ... }` (không còn ai gọi).
> GIỮ `case 'manifest': doManifestRead_` (đọc metadata manifest — vẫn hữu ích, KHÔNG trùng manifest_export).

---

## F7 — Gỡ chia-sẻ-công-khai cho mirror chứa token

`tra_luat_config.json` đang `setSharing(ANYONE_WITH_LINK)` mà chứa **token sống** ⇒ ai có link gọi được webapp.
Trong `doWriteConfig_`, XÓA dòng share công khai:
```js
    cfile=folder.createFile(CONFIG.CONFIG_NAME, json, 'application/json');
    // (F7) BỎ: cfile.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    sp.setProperty('TL_CONFIG_ID', cfile.getId());
```
> Phiên Claude đọc mirror qua **Drive MCP (owner)** nên vẫn lấy được token khi file ở chế độ riêng tư.
> ĐÁNH ĐỔI: `gas.py._refresh_token` (tải `uc?export=download` công khai, kênh headless) sẽ KHÔNG đọc được mirror
> riêng tư — nếu cần kênh đó, đặt `TL_TOKEN` trực tiếp env thay vì auto-refresh từ link. (Token vẫn ở Script Property.)

---

## KIỂM SAU DEPLOY
```
ping                          → version 2.21.1                                  [F2/F3]
meta_find&goc=64-2025-QH15    → trả cụm văn bản (hết rỗng)                       [F1]
find&q=<cụm hiếm>             → tầng fulltext có kết quả khi tên không khớp      [F1]
regen2 confirm=yes; manifest_export → treeHash hai bên KHỚP                      [F5]
readconfig → config.token còn; file config KHÔNG còn anyone-with-link           [F7]
```
Sau khi xanh: cập nhật `API_CONTRACT.md` (2.21.1, gỡ cảnh báo meta_find) + `tl.py EXPECT_VERSION=2.21.1`.

---
# BỔ SUNG (rà soát thứ 2) — F8–F16b

| Mã | Góp ý | Mức | Nội dung |
|---|---|---|---|
| F8 | #1 | P0 | `fetch_url_to_drive` bỏ `jsonOut_()` nội bộ → trả OBJECT |
| F9 | #2 | P0 | `resolveFolder_`/`extDest_` FAIL-CLOSED khi cat sai |
| F10 | #5 | P0 | `map_set` ghi cột `nlm_notebook_id` |
| F11b | #6 | P0 | `vb_status` thêm `VBHN_IN_REGISTRY_NOT_ON_NLM` |
| F12 | #13 | P1 | `importext` chấp `files` dạng `[id,...]` (khớp `remainingIds`) |
| F13b | #14 | P1 | `copy_convert` trả `viewUrl` đúng loại (webViewLink) |
| F14b | #9 | P1 | `batch` cap 30 + cấm batch lồng |
| F15b | #15 | P2 | `bootstrap` persist root vào Script Property |
| F16b | #16 | P2 | manifest whitelist + cảnh báo fetch URL ngoài |

## F8 — `fetch_url_to_drive` trả OBJECT (KHÔNG `jsonOut_`)
Trong `doFetchUrlToDrive_`, THAY MỌI `return jsonOut_({...});` → `return {...};`
(các nhánh lỗi `{ok:false,...}` và nhánh cuối `{ok:true, version:APP_VERSION, fileId:origId, gdocId:gdocId, docxId:docxId, name:name, isDoc:isDoc, converted:true, note:'...'}`).
> Lý do: `main_` đã tự `jsonOut_(out)` + gắn `elapsed_ms`. Trả `jsonOut_` từ handler ⇒ `main_` bọc `TextOutput` ⇒ mất payload.

## F9 — `resolveFolder_`/`extDest_` FAIL-CLOSED
```js
function resolveFolder_(p){
  if (p.folderId) return p.folderId;
  if (p.cat !== undefined && String(p.cat).trim() !== ''){
    var fid = resolveCatFolderId_(p.cat);
    if (!fid) throw new Error('resolveFolder_: không resolve được cat "'+p.cat+'" (refreshcats?)');
    return fid;
  }
  if (p.toFolderId) return p.toFolderId;
  return CONFIG.ROOT_FOLDER_ID;
}
```
```js
function extDest_(p, defaultName){
  if (p.destFolderId) return p.destFolderId;
  if (p.destName) return doMkdir_({name:p.destName, parentId:p.destParentId||CONFIG.ROOT_FOLDER_ID}).folderId;
  if (p.cat !== undefined && String(p.cat).trim() !== ''){
    var fid = resolveCatFolderId_(p.cat);
    if (!fid) throw new Error('extDest_: không resolve được cat "'+p.cat+'"');
    return fid;
  }
  if (defaultName) return doMkdir_({name:defaultName, parentId:CONFIG.ROOT_FOLDER_ID}).folderId;
  return CONFIG.ROOT_FOLDER_ID;
}
```
> Thà BÁO LỖI còn hơn ném file vào ROOT âm thầm. cat='' vẫn bỏ qua (về ROOT) như cũ.

## F10 — `map_set` ghi `nlm_notebook_id`
Trong `doMapSet_`, THAY khối `regUpsertOne_`:
```js
  var nb = p.notebookId || p.nlm_notebook_id || p.notebook || '';
  var r = regUpsertOne_({ drive_id: target,
    nlm_source_id: p.nlm_source_id || '',
    nlm_status: p.status || (p.nlm_source_id ? 'synced' : ''),
    nlm_pushed_at: p.nlm_source_id ? new Date().toISOString() : '',
    nlm_title: p.nlm_title || '',
    nlm_notebook_id: nb,                                   // F10: ghi đúng cột (đa-notebook/quota/dedup)
    note: p.note || (p.notebook ? ('nb:'+p.notebook) : '') });
```

## F11b — `vb_status` tách VBHN chưa-lên-NLM
Trong `doVbStatus_`, THAY nhánh `else if(isVbhn)`:
```js
  } else if (isVbhn){
    if (isSup(row)) status = 'VBHN_SUPERSEDED';
    else if (onNlm) status = 'VBHN_IN_FORCE';
    else status = 'VBHN_IN_REGISTRY_NOT_ON_NLM';          // F11b: không còn nhầm là superseded
  } else {
```
> Cập nhật enum trong API_CONTRACT §7: thêm `VBHN_IN_REGISTRY_NOT_ON_NLM`.

## F12 — `importext` chấp `files` dạng `[id,...]`
Trong `doImportExt_`, NGAY SAU dòng kiểm `if(!list || !list.length)...`:
```js
  list = list.map(function(x){ return (typeof x === 'string') ? {id:x} : x; });   // F12: khớp remainingIds
```

## F13b — `copy_convert` `viewUrl` đúng loại
Trong `doCopyConvert_`: thêm `webViewLink` vào fields + trả nó:
```js
  var copied = Drive.Files.copy(
    {name: name, mimeType: toMime, parents: [folderId]},
    p.fileId,
    {supportsAllDrives: true, fields: 'id,name,mimeType,webViewLink'}
  );
  ...
  return {ok:true, fileId:copied.id, name:copied.name, mime:copied.mimeType,
          srcFileId:p.fileId, srcName:srcMeta.name, folderId:folderId,
          viewUrl: copied.webViewLink || ('https://drive.google.com/file/d/'+copied.id+'/view')};
```

## F14b — `batch` cap + cấm lồng
Trong `doBatch_`:
```js
  if(!Array.isArray(ops)) throw new Error('ops phải là mảng');
  if(ops.length>30) throw new Error('batch: tối đa 30 ops/lần');           // F14b
  var results=[], done=0, failed=0;
  ops.forEach(function(op,i){
    op=op||{};
    if(op.action==='batch'){                                              // F14b: chặn đệ quy
      results.push({i:i, action:'batch', ok:false, error:'không cho batch lồng batch'}); failed++; return; }
    try{ var r=dispatchAction_(op.action, op); var okFlag=(r && r.ok!==false);
      results.push({i:i, action:op.action, ok:okFlag, result:r}); okFlag?done++:failed++;
    }catch(e){ results.push({i:i, action:op.action, ok:false, error:String(e && e.message || e)}); failed++; }
  });
```

## F15b — `bootstrap` persist root (Script Property)
Trong `doBootstrap_`, khi tạo root mới:
```js
    var nf = DriveApp.createFolder('VBQPPL'); rootId = nf.getId(); created.root = rootId;
    PropertiesService.getScriptProperties().setProperty('TL_ROOT_ID', rootId);   // F15b: bền qua execution
    try { CONFIG.ROOT_FOLDER_ID = rootId; } catch(e){}
    try { doWriteConfig_({}); } catch(e){}
```
> Để THỰC SỰ dùng root mới ở lần sau: thêm helper `rootId_()` ưu tiên `TL_ROOT_ID` rồi thay
> `CONFIG.ROOT_FOLDER_ID` ở các điểm resolve (getCategories_/resolveFolder_/corpusFolders_). Nếu hệ
> thống vẫn dựa root hardcode ổn định → có thể BỎ hẳn nhánh tự tạo root (an toàn hơn).

## F16b — manifest whitelist + cảnh báo fetch ngoài
`appsscript.json` `urlFetchWhitelist` cần ĐỦ. **→ F16c (lớp 2.21.1) đã thay bằng 2 file riêng:** `APPSSCRIPT_MANIFEST.open-egress.json` / `.restricted-egress.json`. Mẫu whitelist:
```json
"urlFetchWhitelist": [
  "https://www.googleapis.com/",
  "https://drive.google.com/",
  "https://docs.google.com/",
  "https://drive.usercontent.google.com/"
]
```
> ⚠️ MÂU THUẪN cần quyết: `fetch_url_to_drive` (UrlFetchApp) tải URL NGOÀI (congbao/vbpl…). Nếu đặt
> `urlFetchWhitelist` HẸP (chỉ 4 domain trên) → fetch nguồn ngoài BỊ CHẶN. Hai lựa chọn:
> (a) KHÔNG đặt urlFetchWhitelist (cho fetch mọi domain) — đơn giản, đúng tinh thần fetch_url_to_drive; hoặc
> (b) Giữ whitelist hẹp + BỎ `fetch_url_to_drive`, chỉ nạp ngoài qua HƯỚNG B (web_fetch của Claude → upload).
> Chọn (a) nếu muốn auto-fetch .doc/.docx ungated; chọn (b) nếu ưu tiên siết egress.

## GIA CỐ ĐỢT SAU (không trong bản này — góp ý #8, #12)
- **#8** chuyển action GHI (rename/move/share/restore/reg_upsert/map_set/map_mark_stale) sang **POST-only**
  + token qua header `Authorization: Bearer` thay query string. Kéo theo sửa `gas.py` + API_CONTRACT → làm gọn một đợt riêng.
- **#12** `regCacheBust_` nới vòng (vd 64) hoặc dùng `tl212_reg_meta{chunks}`. LƯU Ý: read dừng ở null đầu
  tiên nên KHÔNG "ghép sai" — chỉ phí cache; ưu tiên thấp.

---
# BỔ SUNG (rà soát thứ 3) — lớp 2.21.1

| Mã | Góp ý | Mức | Nội dung |
|---|---|---|---|
| F7b | #1 | P0 | revoke sharing công khai của file config ĐÃ tồn tại (không chỉ khi tạo mới) |
| F9b | #2 | P0 | `doOrganize_` fail-closed khi cat sai (chặn đường rơi ROOT còn lại) |
| F15c | #3 | P1 | hoàn thiện root persistence: helper `rootId_()` + thay mọi `CONFIG.ROOT_FOLDER_ID` vận hành |
| F16c | #4 | P1 | chốt policy egress: 2 manifest riêng (open / restricted), bỏ file có khóa ghi-chú |
| F4b | #5 | P1 | `regen2` đọc CẢ `ap.soHieu` cũ lẫn `ap.sohieu` mới (tương thích ngược) |

## F7b — revoke sharing file config CŨ
THÊM helper:
```js
function privateConfigFile_(fileId){
  try { DriveApp.getFileById(fileId).setSharing(DriveApp.Access.PRIVATE, DriveApp.Permission.NONE); }
  catch(e){ Logger.log('[privateConfigFile_] không revoke được sharing: ' + e); }
}
```
Trong `doWriteConfig_`, SAU khi có `cfile` (cả nhánh tạo mới lẫn nhánh dùng lại), TRƯỚC khi return:
```js
  privateConfigFile_(cfile.getId());   // F7b: thu hồi public-share cũ + bảo đảm private
```
> (Thay cho F7 chỉ-bỏ-setSharing-khi-tạo-mới.) Sau deploy: kiểm bằng `perm_list&id=<configId>` hoặc Drive UI,
> KHÔNG chỉ tin `readconfig`. Token vẫn nằm trong file → file PHẢI private; phiên Claude đọc qua Drive MCP (owner).

## F9b — `doOrganize_` fail-closed
THAY khối `// 3. move` trong `doOrganize_`:
```js
  if (p.cat){
    var catStr = String(p.cat).trim(), folderId;
    if (/^\d{1,2}$|^QUARANTINE$/.test(catStr)){            // chấp cả '4' lẫn '04'
      folderId = resolveCatFolderId_(catStr);
      if (!folderId) return { ok:false, step:'move', steps:steps,
                              error:'organize: không resolve được cat "'+catStr+'"' };
    } else folderId = catStr;                              // folderId trực tiếp
    var mv = doMove_({ fileId: id, folderId: folderId });
    if (!mv.ok) return { ok:false, step:'move', steps: steps, error: mv.error };
    steps.move = { ok:true, folderId: folderId };
    if (String(p.moveSrc) === 'true' && srcId){
      try { doMove_({ fileId: srcId, folderId: folderId }); steps.moveSrc = { ok:true }; }
      catch(e){ steps.moveSrc = { ok:false, error: String(e) }; }
    }
  }
```
> Trước đây cat sai → `folderId=null` → `doMove_` rơi ROOT (qua mặt F9). Giờ chặn tại nguồn.

## F15c — hoàn thiện root persistence
THÊM helper (cạnh `resolveFolder_`):
```js
function rootId_(){
  return PropertiesService.getScriptProperties().getProperty('TL_ROOT_ID') || CONFIG.ROOT_FOLDER_ID;
}
```
THAY **mọi** chỗ dùng `CONFIG.ROOT_FOLDER_ID` trong các hàm VẬN HÀNH bằng `rootId_()`:
`getCategories_`, `resolveFolder_`, `extDest_`, `doResolveFolder_`, `doMkdir_` (parent mặc định),
`corpusFolders_`, `doBootstrap_`, `buildConfigObject_`/`doWriteConfig_`, `locateManifest_`, `regSS_`, `doRegen2_` (HOUSEKEEPING/scan gốc), `inboxFolderId_` (fallback tạo `_HOP_NAP`).
GIỮ NGUYÊN `CONFIG.ROOT_FOLDER_ID` trong: định nghĩa `CONFIG`, `CATEGORIES_FALLBACK`, và chính hàm `rootId_()`.
> `rootId_()` fallback về `CONFIG.ROOT_FOLDER_ID` nên thay-toàn-bộ là idempotent (an toàn). Cách greppable:
> thay tất cả `CONFIG.ROOT_FOLDER_ID` → `rootId_()` TRỪ 3 nơi nêu trên.
> Trong `doBootstrap_` GIỮ `sp.setProperty('TL_ROOT_ID', rootId)` (F15b). Giờ lần sau hệ thống DÙNG được root mới.
> *(Hướng an toàn thay thế: nếu KHÔNG muốn tự phục hồi, BỎ hẳn nhánh tạo root mới trong `doBootstrap_` —
> root hardcode hỏng thì báo lỗi để người vận hành sửa config. Chọn 1 trong 2, đừng để nửa vời.)*

## F16c — chốt policy egress (2 manifest)
Bỏ file ví dụ có khóa `_GHI_CHU_`. Dùng MỘT trong hai (theo lựa chọn):
- **`references/APPSSCRIPT_MANIFEST.open-egress.json`** — KHÔNG `urlFetchWhitelist` ⇒ `fetch_url_to_drive` tải được nguồn ngoài (congbao/vbpl…). Chọn nếu ƯU TIÊN auto-fetch.
- **`references/APPSSCRIPT_MANIFEST.restricted-egress.json`** *(r219: hiện vật ĐÃ CÓ trong kho — trước đó tài liệu khuyến nghị bản này làm MẶC ĐỊNH nhưng chỉ ghi cách tự dựng, người vận hành theo khuyến nghị thì không có gì để copy)* — có `urlFetchWhitelist` (4 domain Google) ⇒ siết egress; **KHÔNG dùng `fetch_url_to_drive`**, nạp ngoài qua HƯỚNG B (Claude `web_fetch` → `upload`). Chọn nếu ƯU TIÊN an toàn.
> Hai tệp chỉ khác nhau ĐÚNG khóa `urlFetchWhitelist`; mọi sửa đổi khác (scope, advanced service, webapp access) phải áp cho CẢ HAI, nếu không thì đổi policy egress sẽ âm thầm kéo theo đổi quyền.
> Khuyến nghị mặc định: **restricted-egress** (giá trị auto-fetch hạn chế vì phần lớn nguồn official là PDF — xem A2),
> trừ khi anh thực sự cần auto-fetch .doc/.docx ungated.

## F4b — `regen2` tương thích ngược metadata camelCase
Trong `doRegen2_`, dòng dựng `sohieu` của `scanned.push`:
```js
        sohieu: normSoHieu_(ap.sohieu || ap.soHieu || '') || sohieuFromName_(f.name),
```
> Đọc được CẢ file cũ stamp `soHieu` (camel) lẫn file mới `sohieu` (sau F4). (`hieuluc` trong regen2 lấy từ
> registry/curate, không đọc từ appProperties nên không cần đổi.)

## KIỂM SAU DEPLOY (bổ sung 2.21.1)
```
perm_list&id=<configId>      → KHÔNG còn 'anyone' (F7b)
organize cat=99              → ok:false 'không resolve được cat' (F9b, hết rơi ROOT)
regen2 → file cũ stamp soHieu được nhặt sohieu đúng (F4b)
```

---
# BỔ SUNG (rà soát thứ 4) — A–E

| Mã | Mức | Nội dung |
|---|---|---|
| A | nit | hết stale `2.21.0` (đã sửa trong patch + INSTALL) |
| B | P1 | `meta_find` mặc định `scope:'corpus'` (đã sửa trong F1) |
| C | P1 | F15c rà TRIỆT ĐỂ `CONFIG.ROOT_FOLDER_ID` (gồm setup/doExport_/doPerf_/diagnostics) |
| D | P2 | `doManifestRead_` message hết nhắc `regen` deprecated |
| E | P2 | `readconfig`/`writeconfig` `downloadUrl` khi config private |

## C — F15c rà TRIỆT ĐỂ `rootId_()`
Quy tắc CHÍNH XÁC: thay **TẤT CẢ** `CONFIG.ROOT_FOLDER_ID` bằng `rootId_()` trên toàn file,
gồm cả **`setup()`, `doExport_()` (fallback toFolderId), `doPerf_()`, mọi probe/diagnostic/return**,
**TRỪ ĐÚNG 3 NƠI**: (1) định nghĩa `CONFIG = {... ROOT_FOLDER_ID: ...}`; (2) `CATEGORIES_FALLBACK`
(snapshot); (3) thân hàm `rootId_()` (fallback). `apply_gs_patches.py` làm tự động (global-root) + audit
"không còn `CONFIG.ROOT_FOLDER_ID` ngoài 3 nơi".

## D — `doManifestRead_` message
THAY:
```js
  if(!mid) return {ok:false, error:'Chưa có manifest — chạy action=regen&confirm=yes trước'};
```
BẰNG:
```js
  if(!mid) return {ok:false, error:'Chưa có manifest — chạy action=regen2&confirm=yes rồi manifest_export trước'};
```

## E — `readconfig`/`writeconfig` downloadUrl khi config private
Sau F7/F7b config PRIVATE → `uc?export=download` không tải headless được. Trong `doReadConfig_` (nhánh có file)
và `doWriteConfig_`, THAY field `downloadUrl` bằng:
```js
  // E: config PRIVATE — không còn link tải công khai
  driveFileId: cfile.getId(),
  configAccess: 'private',
  note: 'Config private (chứa token) — đọc qua Drive MCP/owner hoặc đặt TL_TOKEN bằng env; KHÔNG tải headless.',
```
(Bỏ `downloadUrl:'https://drive.google.com/uc?export=download&id='+cfile.getId()`.) Nếu vẫn cần giữ tên
`downloadUrl` cho tương thích client, đặt `downloadUrl:''` + thêm `note` như trên.
