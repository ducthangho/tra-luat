/**
 * tra-luat — Fetch-to-Drive Web App  v2.8.0
 * (v2.6.0 + IMPORT EXTERNAL: nạp folder/file từ LINK Drive NGOÀI quyền tối thiểu, server-side)
 *
 * SETUP lần đầu: Services (+) Drive API v3 → dán đè → chạy setup() → rotateToken() → Deploy New version.
 * NÂNG CẤP từ v2.6.0: dán đè file này → Deploy New version (URL + TL_TOKEN Script Property GIỮ NGUYÊN,
 *   Script Properties KHÔNG bị mất khi dán đè code). Manifest appsscript.json KHÔNG cần sửa.
 * Đồng bộ kho:   <endpoint>?token=..&action=regen2&confirm=yes → manifest.json + manifest_export + Registry + treeHash
 *
 * Actions: ping categories refreshcats | ingest fetch upload createtext copy_convert register share move |
 *          listext resolvefolder importext importlink |
 *          rename trash restore mkdir list info resolve |
 *          verifyShares dedup export exporttext exportdocx stamp findprop pinRevision |
 *          regen manifest writeconfig readconfig | batch
 *
 * CHANGELOG:
 *   v2.8.0 (2026-06-10): IMPORT EXTERNAL — nạp từ link Drive ngoài (anyone-with-link viewer là đủ).
 *     BỐI CẢNH: item link-shared KHÔNG nằm trong corpus tài khoản → MCP search_files trả rỗng (đúng,
 *       không phải lỗi); chỉ truy cập được THEO ID. Apps Script "Execute as Me" đọc/copy được mọi item
 *       link-shared theo ID (Drive.Files.get/list/copy) → import server-side, nội dung KHÔNG qua context.
 *     ACTIONS MỚI:
 *       - listext       (GET)  : liệt kê folder NGOÀI theo ID (files + folders con + shortcutTargetId,
 *                                md5Checksum để dedup; phân trang, trần 400 file/call).
 *       - resolvefolder (GET)  : tìm-hoặc-tạo subfolder theo TÊN (mặc định trong VBQPPL gốc) — alias
 *                                mỏng quanh doMkdir_, trả thêm url.
 *       - importext     (POST) : copy DANH SÁCH fileIds (≤30/đợt) vào đích; convert → Google Doc;
 *                                dedup theo appProperties srcMd5/srcId (pattern giống sha256 của
 *                                createFromBlob_ — copy server-side không có bytes để sha256);
 *                                share + register + stamp provenance như luồng chuẩn.
 *       - importlink    (POST) : ONE-SHOT — id link ngoài (folder HOẶC file) → copy cả khối.
 *                                Folder không chỉ đích → TỰ TẠO subfolder CÙNG TÊN trong VBQPPL gốc.
 *                                Tự dừng ~4.5 phút (trần execution 6') hoặc đủ max (mặc định 25, trần 30)
 *                                → trả remainingIds + nextPageToken cho đợt sau; subfolders trả riêng
 *                                (Claude HỎI người dùng trước khi đệ quy); shortcut tự resolve target;
 *                                skip ảnh/audio/video và file > UPLOAD_MAX_BYTES.
 *     QUY ƯỚC ĐÍCH (extDest_): destFolderId > destName (tạo trong destParentId|root) > cat (map động
 *       v2.6.0) > [folder nguồn → subfolder cùng tên] > VBQPPL gốc. KHÔNG dùng p.folderId làm đích
 *       trong importlink (tránh nhầm với id folder NGOÀI).
 *     PROVENANCE: mỗi bản copy stamp appProperties {srcId, srcMd5, sourceUrl:'importlink:<srcId>',
 *       ingestedAt} → dedup idempotent (gọi lại không tạo trùng), findprop tra ngược được nguồn.
 *     LƯU Ý: share KHÔNG bắt buộc cho NotebookLM (source_add(drive) chạy bằng chính tài khoản, đọc
 *       được file private) — mặc định vẫn share theo convention verifyShares; tắt bằng share=false.
 *       PDF SCAN copy "thành công" nhưng Google Doc rỗng → cổng hậu-copy phía skill bắt (exporttext
 *       rỗng → trash), server không OCR.
 *   v2.6.0 (2026-06-09): DYNAMIC CATEGORIES — xử lý TẬN GỐC lỗi cat trỏ sai folder.
 *     VẤN ĐỀ: CONFIG.CATEGORIES hardcode → khi đổi tên/xóa/tạo lại folder trên Drive, map lệch pha:
 *       (a) cat 04 trỏ id folder CŨ sau khi folder được tái tạo; (b) cat 05 trỏ folder ĐÃ XÓA (trashed);
 *       (c) thiếu cat 14 mới tạo. writeconfig KHÔNG cứu được vì chỉ mirror lại hằng số.
 *     GIẢI PHÁP (Mức 2): getCategories_() quét folder con trực tiếp của VBQPPL root, lọc trashed,
 *       parse tiền tố "NN_" từ TÊN folder → map cat→id. Quy ước đặt tên "NN_<Chủ đề>" thành NGUỒN
 *       SỰ THẬT duy nhất. Đổi tên/tạo/xóa folder → cat tự đúng. Cache 10' bằng CacheService.
 *       - resolveFolder_/resolveCatFolderId_ dùng map động (fallback CATEGORIES_FALLBACK nếu quét lỗi).
 *       - action 'categories' trả map động; thêm action 'refreshcats' (ép quét lại, xoá cache).
 *       - buildConfigObject_ mirror map động ra tra_luat_config.json.
 *       - Cảnh báo (Logger) khi >1 folder cùng số cat (vd lỡ tạo hai "04_...").
 *     CONFIG.CATEGORIES cũ ĐỔI TÊN thành CATEGORIES_FALLBACK (chỉ dùng khi Drive.Files.list lỗi).
 *   v2.5.1 (2026-06-09): exportBlob_ vá whitelist googleapis.com + fallback Advanced Drive Service.
 *   v2.4.1 (2026-06-08): (a) KHÔI PHỤC `createtext` (text thuần → Google Doc) đã bị bỏ ở v2.4.0.
 *     - Fix root-removal: dùng Drive.Files.update(addParents/removeParents) thay DriveApp.addFile/removeFile.
 *     - Giữ newline: split('\n') + appendParagraph thay vì setText() (setText gộp 1 đoạn, mất xuống dòng).
 *     `createtext` (text clean đã normalize) và `upload` (file gốc base64) là HAI đường vào khác nhau,
 *     giữ cả hai để không regression workflow "đẩy bản clean lên Drive" của reference v2.
 *     (b) FIX export*: `Drive.Files.export()` (wrapper Advanced Drive Service) ném lỗi KHÔNG NHẤT QUÁN
 *     "Export requires alt=media to download the exported content" — quirk bất định của lớp wrapper
 *     (REST files.export VỐN trả bytes; lỗi là undocumented, chỉ xuất hiện ở một số môi trường).
 *     Quirk này KẾ THỪA từ khi đổi sang Drive.Files.export() ở v2.0.0, không phải lỗi mới ở v2.4.0.
 *     Fix: dùng exportBlob_() = UrlFetchApp + REST /export (tránh hẳn wrapper bất định) cho export/exporttext/exportdocx.
 *   v2.4.0: + upload base64 + exporttext/exportdocx + listChildren_/listTree_ phân trang dùng chung.
 */

var APP_VERSION = '2.21.2q';   // v2.21.2q (#1089 CLOUD-SETUP-P3-WRITEBACK): +agent_creds_put — ghi đè NỘI DUNG đúng tệp TL_AGENT_CREDS_FILEID, CAS theo md5Checksum TRONG script lock; ADDITIVE. Trước 2.21.2q: v2.21.2p: ATOMIC registry RMW — KI-25 withRegLock_ om TRON doc-sua-ghi (Lock cua Apps Script KHONG dem tang => tu dem do sau); KI-26 ensureRegTabs_ KHONG tu tao tab rong tren duong DOC khi dang swap (day chinh la duong xoa trang registry 1313->2 ngay 25-07); KI-27 chot chan tham hoa (mat >100 dong hoac >50% => REGISTRY_SHRINK_REFUSED, tru khi khai expect_shrink) + sao luu xoay vong files_bak_<ts> giu 5 ban (0 round-trip them). ADDITIVE voi client. Truoc 2.21.2o:   // r198/ADR-0014: +ingest_commit — gộp organize(+rename)+register+readback(row+file info) MỘT round-trip, sub-step marker organize_done/rename_done/upsert_done cho journal/--resume (partial tường minh, không im lặng); tham số đủ cho CẢ ingest-local (cat NN) lẫn profile (cat=folderId flat), client r198 chỉ dùng nhánh profile. ADDITIVE — client cũ không đổi hành vi. Trước 2.21.2n: r185/WP5 (D3 review p9): +profile_catalog +drive_info_bulk — CỘNG THÊM, CHỈ ĐỌC (giảm O(profile)/O(template) round-trip discover/doctor/probe). Trước 2.21.2m: D3 v1.34.55: manifest/nlm-compact export row_kind RAW. Trước 2.21.2l: F-04 ingest_claim + F-08 reg_get_bulk

var CONFIG = {
  // ⚠️ v2.8.0: DEFAULT_TOKEN đặt PLACEHOLDER — token thật nằm ở Script Property TL_TOKEN (đã rotateToken()
  //   từ trước; Script Properties KHÔNG mất khi dán đè code). Placeholder cố ý KHÔNG dùng được,
  //   tránh token thật nằm trong file code đóng gói theo skill.
  DEFAULT_TOKEN: 'tl_PLACEHOLDER_chay_rotateToken_de_sinh_token',
  ROOT_FOLDER_ID: '11Rkwf3nhudPNNcsGlloV8acaXiXqdutJ',
  REGISTRY_DOC_ID: '1mATGFhaW0e_CYienAD80DsTS1K4zfJNlTAx-DsHaCD8',
  MANIFEST_NAME: 'tra_luat_manifest.json',
  CONFIG_NAME: 'tra_luat_config.json',               // mirror config (đặt TRONG folder VBQPPL gốc) — skill đọc lúc load
  REGISTRY_MAX_ROWS: 1500,                          // Doc chỉ render tới ngần này dòng; đủ thì trỏ sang manifest
  PDF_CONVERT_MAX: 1800000,
  EXPORT_MAX_BYTES: 9 * 1024 * 1024,
  UPLOAD_MAX_BYTES: 35 * 1024 * 1024,               // file gốc trước base64 (payload ~50MB)
  LIST_CAP: 2000,
  CAT_CACHE_TTL: 600,                               // giây — cache map cat động (10 phút)
  IMPORT_MAX_PER_CALL: 30,                          // v2.8.0: trần file copy / 1 execution
  IMPORT_TIME_BUDGET_MS: 4.5 * 60 * 1000,           // v2.8.0: chừa thời gian trả response (trần 6')
  LISTEXT_CAP: 400,                                 // v2.8.0: trần file trả về / 1 call listext
  // CATEGORIES_FALLBACK: CHỈ dùng khi quét folder động thất bại (Drive.Files.list lỗi).
  //   ⚠️ KHÔNG phải nguồn sự thật (nguồn thật = TÊN folder "NN_..." trên Drive).
  //   v2.13.3: SNAPSHOT 12/06/2026 SAU migration 45 chủ đề pháp điển — id cũ 01–14 đã thành
  //   _OLD_* (dùng nữa là xếp nhầm vào folder chết). QUY TẮC: mỗi lần tái cấu trúc folder,
  //   chụp lại snapshot từ GET action=categories&refresh=true và writeconfig cho mirror khớp.
  // 2026-06-25: đồng bộ ĐỦ folder cat đang có (trước thiếu 06,18,31,32,38,39,41,42,44) + thêm 01 An ninh quốc gia,
  //   37 Tố tụng (mã pháp điển chính thức, vừa tạo folder). Map động getCategories_ vẫn là nguồn sự thật; đây chỉ là fallback khi quét lỗi.
  CATEGORIES_FALLBACK: {
    '00':'1AK6l9ZNmr9rJxYeHkAgV9Cvi_uNHAuM7','01':'1dmTuWyBUUygiYe4kUL1Nf70DYfvSTp1y',
    '02':'1_kRzUyta67w8Q0c4lqbkwwXzI7DqE_bi','03':'15KUgPThRtN-JWLgkmYo3cq9S3tP4nxLF',
    '06':'12jIOcotstycZJgZSWm7UvkErGRj6L2Ze',
    '08':'1AmaG1OjlLzC_nMpMb3do5m1JgPbw-AES','09':'1p6Xpy1kIGqGjQdNDmGMK8HNywyCJZlLW',
    '11':'11e34iuj2X0qQeBCwbuECcKCCjqyvQJ05','13':'1StbHm-aBS0gBbvrdwep5h4UFCI3eOJXu',
    '16':'1_W-IRoM6erc8qbdjMcT2zh25mTzggAv1','17':'1gCXZpCbnOlK898Mc3ZzwfrJNYVvDMQlF',
    '18':'1dMFmY4Poz5U780s2r497NFz35U2PbY0L','19':'1amrlZ6xtuy9aRcDLITKF5B3cQDsdk_1H',
    '20':'1AoIaRJGFt1Tti7DIGAFwyUTn4G0A014-','22':'1klTTDzf186xF2YBrpaOYbUMxBxYu7NHk',
    '23':'1d50CbAM9WHRa1bAaw3HzG0b-_CKvLA_M','26':'1MC-PEMH8ahZDTVO1UH8b4een7WbevX1F',
    '29':'1MCwq57W_ZA9_cL8A1VkXtge5Vmoepmzi','31':'16tUtNbS-3ou2Gg4wScZ1FVZynl067nsx',
    '32':'14H2GCtKZReC_D0M6HMHAGBUFBo9kilNU','33':'15uR8Rfzq4dCSJE8_xVLUAg487kqgev-7',
    '34':'1AmROn7N78pGGOp9OG2oVozOWyrxUWg7x','35':'1l3rHXzZBu1n_0YxM0oweZYWOxcdyOBsi',
    '36':'1AX-QVMHOL0kbNoujLUFIerA2lAETK5dX','37':'1gdRrzncLFPrY3dR4kd7LHSJmc-oCwH7k',
    '38':'1EccVZHYZm_VTAbBFfJ2kXUjB3DmtPPzq','39':'1aijrHqL8QG3wRSTPylz8NX2JltcDnOdY',
    '41':'1bBI8-FsJwKhqcloWoB00uKHA7qCv3PD8','42':'1KcHrZeE_R9ZuwJ-LvQFWnWCz0gOv4YDj',
    '43':'11ba_XtZP40MEWuZFhEElXZwQVrAUURku',
    '44':'1SVKfgHAHu3xmInE3yOuLI7hzg1rSAHmK','45':'1L0RSsh62RJroKQpwEfVEHLE2EJRp141z',
    '46':'1Z5JUnjRzv_3-fVKu9HPnJOox_YK-B3Ux','QUARANTINE':'153C8u1SoyttNMcC2albawErEev8wgLVi'
  }
};

/* ============ DYNAMIC CATEGORIES (v2.6.0) ============
 * Nguồn sự thật = TÊN folder con của VBQPPL root: "NN_<Chủ đề>" (NN = 2 chữ số).
 * getCategories_() quét, lọc trashed, parse "NN_" → { "04": folderId, ..., "QUARANTINE": id }.
 * Cache CacheService (CONFIG.CAT_CACHE_TTL giây). force=true để bỏ cache.
 */
var CAT_CACHE_KEY = 'tl_categories_v260';
var CAT_NAME_RE   = /^(\d{2})[_\-]/;                 // "04_Tai_chinh..." → "04"
var CAT_SPECIAL   = { 'QUARANTINE': /quarantine/i }; // folder đặc biệt không theo NN_

function getCategories_(force){
  var cache=CacheService.getScriptCache();
  if(!force){
    var hit=cache.get(CAT_CACHE_KEY);
    if(hit){ try{ return JSON.parse(hit); }catch(e){ /* rơi xuống quét lại */ } }
  }
  var map={}, dupWarnings=[], scanOk=false;
  try{
    var pageToken=null;
    do{
      var resp=Drive.Files.list({
        q:"'"+rootId_()+"' in parents and "
         +"mimeType='application/vnd.google-apps.folder' and trashed=false",
        pageSize:200, fields:'nextPageToken,files(id,name)',
        pageToken:pageToken, supportsAllDrives:true, includeItemsFromAllDrives:true
      });
      (resp.files||[]).forEach(function(f){
        var name=f.name||'', m=name.match(CAT_NAME_RE);
        if(m){
          var key=m[1];
          if(map[key] && map[key]!==f.id) dupWarnings.push('cat '+key+': '+map[key]+' vs '+f.id+' ('+name+')');
          if(!map[key]) map[key]=f.id;        // giữ folder gặp đầu; cảnh báo cái sau
          return;
        }
        for(var label in CAT_SPECIAL){ if(CAT_SPECIAL[label].test(name)){ if(!map[label]) map[label]=f.id; return; } }
        // folder khác (NLM_Export, "Hướng dẫn 06"...) → bỏ qua, không phải cat
      });
      pageToken=resp.nextPageToken;
    }while(pageToken);
    scanOk=true;
  }catch(e){
    Logger.log('[getCategories_] Drive.Files.list LỖI → dùng CATEGORIES_FALLBACK: '+(e && e.message || e));
  }
  if(!scanOk || !Object.keys(map).length){
    // Quét lỗi hoặc rỗng bất thường → fallback hằng số (không để hệ thống chết).
    return JSON.parse(JSON.stringify(CONFIG.CATEGORIES_FALLBACK));
  }
  if(dupWarnings.length) Logger.log('[getCategories_] CẢNH BÁO trùng số cat:\n'+dupWarnings.join('\n'));
  cache.put(CAT_CACHE_KEY, JSON.stringify(map), CONFIG.CAT_CACHE_TTL);
  return map;
}

// Resolve mã cat → folderId; chấp nhận "4"→"04"; quét lại 1 lần nếu cache cũ chưa có folder mới tạo.
function resolveCatFolderId_(cat){
  var key=String(cat).trim();
  if(/^\d$/.test(key)) key='0'+key;
  var cats=getCategories_(false);
  if(cats[key]) return cats[key];
  cats=getCategories_(true);                          // folder vừa tạo → ép quét lại
  if(cats[key]) return cats[key];
  return null;                                        // resolveFolder_ sẽ xử lý null
}

function refreshCategories_(){ return getCategories_(true); }

/* ============ SETUP ============ */
function setup(){
  var sp=PropertiesService.getScriptProperties();
  if(!sp.getProperty('TL_TOKEN')) sp.setProperty('TL_TOKEN', CONFIG.DEFAULT_TOKEN);
  var token=sp.getProperty('TL_TOKEN'), checks={};
  // v2.8.0: cảnh báo nếu token vẫn là placeholder (chưa rotateToken)
  checks.token = (token===CONFIG.DEFAULT_TOKEN) ? 'CẢNH BÁO: token là placeholder — CHẠY rotateToken() NGAY' : 'OK (Script Property)';
  try{ checks.driveApi = 'OK ('+Drive.Files.get(rootId_(),{fields:'name',supportsAllDrives:true}).name+')'; }
  catch(e){ checks.driveApi = 'LỖI — bật Drive API v3 (Services +): '+e; }
  try{ checks.rootFolder = 'OK ('+DriveApp.getFolderById(rootId_()).getName()+')'; }catch(e){ checks.rootFolder='LỖI: '+e; }
  try{ checks.registry = 'OK ('+DocumentApp.openById(CONFIG.REGISTRY_DOC_ID).getName()+')'; }catch(e){ checks.registry='LỖI: '+e; }
  // Quét categories động ngay để xác nhận map đúng folder thật.
  try{ var cats=getCategories_(true); checks.categories='OK ('+Object.keys(cats).length+' cat: '+Object.keys(cats).sort().join(',')+')'; }
  catch(e){ checks.categories='LỖI: '+e; }
  // Bootstrap mirror config vào folder VBQPPL (skill đọc lúc load). Cần TL_WEBAPP_URL đã set,
  // hoặc truyền ?webappUrl=… vào setup. Không có URL vẫn ghi (skill sẽ hỏi URL nếu trống).
  try{ var cfg=doWriteConfig_(this && this.webappUrl ? {webappUrl:this.webappUrl} : {}); checks.config='OK ('+cfg.name+' @ '+cfg.configFileId+')'; }
  catch(e){ checks.config='LỖI: '+e; }
  Logger.log('TL_TOKEN = '+(token ? token.slice(0,8)+'…' : ''));
  Logger.log('CHECKS = '+JSON.stringify(checks,null,2));
  return {ok:true, tokenStatus:checks.token, checks:checks};
}
function rotateToken(){
  var t='tl_'+Utilities.getUuid().replace(/-/g,'');
  PropertiesService.getScriptProperties().setProperty('TL_TOKEN', t);
  // v2.12.1 KI-25: rotate + mirror NGUYÊN TỬ — quên writeconfig là nguồn lệch token duy nhất từng gặp.
  try { doWriteConfig_({}); Logger.log('NEW TL_TOKEN = '+t+' (mirror tra_luat_config.json ĐÃ cập nhật)'); }
  catch(e){ Logger.log('NEW TL_TOKEN = '+t+' | CẢNH BÁO: mirror FAIL — chạy writeconfig tay. '+e); }
  return t;
}
function getToken(){
  var t=token_(), masked=(t ? t.slice(0,8)+'…' : '');
  Logger.log('TL_TOKEN = '+masked);
  return {ok:true, tokenPresent:!!t, tokenMasked:masked};
}

/* ============ TOKEN ============ */
function token_(){ return PropertiesService.getScriptProperties().getProperty('TL_TOKEN') || CONFIG.DEFAULT_TOKEN; }
function safeEqual_(a, b){
  a=String(a||''); b=String(b||'');
  if(a.length!==b.length) return false;
  var d=0; for(var i=0;i<a.length;i++) d|=a.charCodeAt(i)^b.charCodeAt(i);
  return d===0;
}

/* ============ ENTRY ============ */
function doGet(e){ return main_(e); }
function doPost(e){ return main_(e); }
function main_(e){
  var t0 = Date.now();                              // v2.13.0: đo thời gian MỌI action
  try{
    var p = mergeParams_(e);
    if(!safeEqual_(p.token, token_())) return jsonOut_({ok:false, error:'Sai token'});
    setCorpusScope_(p);                               // v2.21.2f: registryDocId/manifestId theo profile (thiếu ⇒ VBQPPL)
    var act = p.action || 'ping';
    var out = dispatchAction_(act, p);
    if (out && typeof out === 'object' && !Array.isArray(out)){
      out.action = out.action || act;
      out.elapsed_ms = Date.now() - t0;             // server-side: thời gian xử lý trong Apps Script
    }
    return jsonOut_(out);
  }catch(err){ return jsonOut_({ok:false, error:String(err && err.message || err),
                                elapsed_ms: Date.now() - t0}); }
}

function dispatchAction_(action, p){
  switch(action){
    case 'ping':         return {ok:true, pong:true, ts:new Date().toISOString(), version:APP_VERSION,
      schema_version:APP_VERSION, registry_schema:'reg_cols_row_kind_v1',
      registry_cols:(typeof REG_COLS_ === 'undefined' ? null : REG_COLS_.length)};
    case 'bootstrap':    return doBootstrap_(p);      // v2.14.0: tạo/kiểm VBQPPL+_HOP_NAP+Van_ban_thuong + tự-kiểm ghi
    case 'fetch_url_to_drive': return doFetchUrlToDrive_(p);  // v2.15.0: tải URL ungated .doc/.docx về _HOP_NAP
    case 'organize':     return doOrganize_(p);     // v2.13.2: convert+rename+move+stamp+register 1 RTT
    case 'ingest_commit': return doIngestCommit_(p); // v2.21.2o (ADR-0014): organize+register+readback row/file 1 RTT, sub-step marker
    case 'search':       return doSearch_(p);       // v2.13.0: thay Drive MCP search_files
    case 'download':     return doDownload_(p);     // v2.13.0: b64 file BẤT KỲ (thay MCP download)
    case 'reg_addcols':  return doRegAddCols_(p);   // v2.13.0: migrate header registry lên 22 cột
    case 'reg_bak_list':    return doRegBakList_(p);    // v2.21.2p KI-27: liệt kê bản sao xoay vòng (CHỈ ĐỌC)
    case 'reg_bak_restore': return doRegBakRestore_(p); // v2.21.2p KI-27: khôi phục registry từ bản sao (confirm=yes)
    case 'categories':   return {ok:true, categories:getCategories_(false), source:'dynamic'};
    case 'refreshcats':  return {ok:true, categories:refreshCategories_(), source:'dynamic', refreshed:true};
    case 'ingest':       return doIngest_(p);
    case 'fetch':        return doFetch_(p);
    case 'upload':       return doUpload_(p);
    case 'createtext':   return doCreateText_(p);
    case 'copy_convert': return doCopyConvert_(p);
    case 'listext':      return doListExt_(p);        // v2.8.0
    case 'resolvefolder':return doResolveFolder_(p);  // v2.8.0
    case 'importext':    return doImportExt_(p);      // v2.8.0
    case 'importlink':   return doImportLink_(p);     // v2.8.0
    case 'register':     return doRegister_(p);
    case 'share':        return doShare_(p);
    case 'move':         return doMove_(p);
    case 'rename':       return doRename_(p);
    case 'trash':        return doTrash_(p);
    case 'restore':      return doRestore_(p);
    case 'mkdir':        return doMkdir_(p);
    case 'list':         return doList_(p);
    case 'info':         return doInfo_(p);
    case 'resolve':      return doResolve_(p);
    case 'verifyShares': return doVerifyShares_(p);
    case 'dedup':        return doDedup_(p);
    case 'export':       return doExport_(p);
    case 'exporttext':   return doExportText_(p);
    case 'exportdocx':   return doExportDocx_(p);
    case 'stamp':        return doStamp_(p);
    case 'findprop':     return doFindProp_(p);
    case 'pinRevision':  return doPinRevision_(p);
    case 'regen':
    case 'regenRegistry': return {ok:false, deprecated:true, error:'regen (Doc-registry, schema cu) da ngung — dung regen2 (confirm=yes) + manifest_export.', use:['regen2','manifest_export']};
    case 'manifest':     return doManifestRead_(p);
    case 'writeconfig':  return doWriteConfig_(p);
    case 'readconfig':   return doReadConfig_(p);
    case 'batch':        return doBatch_(p);
    /* --- v2.11 --- */
    case 'read':         return doRead_(p);
    case 'perm_list':    return doPermList_(p);
    case 'changes_init': return doChangesInit_(p);
    case 'changes_pull': return doChangesPull_(p);
    case 'meta_set':     return doMetaSet_(p);
    case 'meta_find':    return doMetaFind_(p);
    case 'shortcut':     return doShortcut_(p);
    case 'inbox_process':return doInboxProcess_(p);
    case 'inbox_status': return doInboxStatus_(p);
    case 'perf':         return doPerf_(p);
    case 'config':
    case 'configView':   return doConfigView_(p);
    /* --- v2.12 --- */
    case 'find':         return doFind_(p);
    case 'nlm_preflight': return doNlmPreflight_(p);  // v2.16.0
    case 'nlm_slots':     return doNlmSlots_(p);      // v2.16.0
    case 'nlm_dedup':     return doNlmDedup_(p);      // v2.16.0
    case 'vb_status':     return doVbStatus_(p);      // v2.16.0
    case 'reg_get':      return doRegGet_(p);
    case 'reg_upsert':   return doRegUpsert_(p);
    case 'reg_bulk':     return doRegBulk_(p);    // v2.13.7: vá NHIỀU dòng 1 đọc + 1 ghi
    case 'reg_get_bulk': return doRegGetBulk_(p);  // v2.21.2l (F-08): đọc N key 1 lần + commit claim gộp
    case 'profile_catalog': return doProfileCatalog_(p);  // v2.21.2n (r185/WP5): snapshot Van_ban_thuong 1 call
    case 'drive_info_bulk': return doDriveInfoBulk_(p);   // v2.21.2n (r185/WP5): metadata N fileId 1 call
    case 'ingest_claim': return doIngestClaim_(p); // v2.21.2l (F-04): reservation identity xuyên host
    case 'reg_clear':    return doRegClear_(p);    // v2.21.2c: xóa giá trị cột có kiểm soát (vd nlm_source_id)
    case 'reg_delete':   return doRegDelete_(p);   // gỡ dòng registry theo drive_id
    case 'map_set':      return doMapSet_(p);
    case 'map_unpushed': return doMapUnpushed_(p);
    case 'map_mark_stale': return doMapMarkStale_(p);
    case 'regen2':       return doRegen2_(p);
    case 'manifest_export': return doManifestExport_(p);
    case 'agent_creds_put': return doAgentCredsPut_(p); // v2.21.2q (#1089): CAS md5 + script lock, chỉ TL_AGENT_CREDS_FILEID
    default: throw new Error('Action không hỗ trợ: '+action);
  }
}

/* ============ AGENT CREDS (v2.21.2q, #1089) ============ */
// agent_creds_put: ghi đè NỘI DUNG đúng MỘT tệp — Script Property TL_AGENT_CREDS_FILEID — với CAS theo md5Checksum.
// POST JSON: { token, action:'agent_creds_put', fileId, expect_md5, b64 }. Mọi lỗi ⇒ {ok:false, error:<MÃ>} và KHÔNG ghi gì.
// Thứ tự kiểm (spec cloud-setup-p3-writeback-r2 mục Hợp đồng): cấu hình → fileId → expect_md5 → cỡ blob → lock → CAS.
// Đọc md5 + ghi + đọc lại nằm TRỌN trong script lock (chung lock với withRegLock_); nhả lock trong finally.
// Không có hằng fileId dự phòng, không có chế độ ghi mù, không đổi tên/thư mục/chia sẻ. Không log nội dung.
var AGENT_CREDS_MAX_BYTES_ = 65536;
function doAgentCredsPut_(p){
  var fid = PropertiesService.getScriptProperties().getProperty('TL_AGENT_CREDS_FILEID') || '';
  if (!fid) return {ok:false, error:'AGENT_CREDS_NOT_CONFIGURED'};
  if (String(p.fileId == null ? '' : p.fileId) !== fid) return {ok:false, error:'AGENT_CREDS_FILEID_MISMATCH'};
  var expect = (typeof p.expect_md5 === 'string') ? p.expect_md5 : '';
  if (!/^[0-9a-f]{32}$/.test(expect)) return {ok:false, error:'EXPECT_MD5_REQUIRED'};
  var bytes = null;
  try { bytes = Utilities.base64Decode(String(p.b64 == null ? '' : p.b64)); } catch (e) { bytes = null; }
  if (!bytes || bytes.length === 0 || bytes.length > AGENT_CREDS_MAX_BYTES_) return {ok:false, error:'BLOB_SIZE'};
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return {ok:false, error:'LOCK_BUSY'};
  try {
    var cur = Drive.Files.get(fid, {fields:'md5Checksum', supportsAllDrives:true}).md5Checksum || '';
    if (cur !== expect) return {ok:false, error:'CAS_CONFLICT', md5:cur};
    Drive.Files.update({}, fid, Utilities.newBlob(bytes, 'application/octet-stream'),
                       {supportsAllDrives:true, fields:'id'});
    var md5 = Drive.Files.get(fid, {fields:'md5Checksum', supportsAllDrives:true}).md5Checksum || '';
    return {ok:true, md5:md5, size:bytes.length};
  } finally {
    lock.releaseLock();
  }
}
/* ============ /AGENT CREDS ============ */

/* ============ INGEST / FETCH / UPLOAD ============ */
function doIngest_(p){
  if(!p.url) throw new Error('ingest: thiếu url');
  var blob=fetchBlob_(p.url, p.title), bytes=blob.getBytes(), mime=blob.getContentType()||'';
  return createFromBlob_(p, bytes, mime, blob, p.url);
}
function doFetch_(p){
  if(!p.url) throw new Error('fetch: thiếu url');
  var blob = fetchBlob_(p.url, p.title);
  var f = DriveApp.getFolderById(resolveFolder_(p)).createFile(blob);
  if(p.title) f.setName(p.title);
  if(String(p.share)!=='false') shareView_(f.getId());
  return {ok:true, fileId:f.getId(), name:f.getName(), mime:f.getMimeType()};
}
// upload: nhận file base64 từ client → Drive (đối xứng exportdocx)
// POST JSON: { token, action:'upload', b64, name, mime?, cat?/folderId?, convert?, props?, force? }
function doUpload_(p){
  if(!p.b64)  throw new Error('upload: thiếu b64 (nội dung file base64)');
  if(!p.name) throw new Error('upload: thiếu name');
  var bytes=Utilities.base64Decode(p.b64);
  if(bytes.length>CONFIG.UPLOAD_MAX_BYTES) throw new Error('upload: file > UPLOAD_MAX_BYTES (~35MB); file lớn dùng ingest từ URL');
  var mime=p.mime || inferMime_(p.name);
  var blob=Utilities.newBlob(bytes, mime, p.name);
  return createFromBlob_(p, bytes, mime, blob, p.sourceUrl || 'upload');
}
// createtext: nhận TEXT THUẦN (đã normalize/clean) → tạo Google Doc trực tiếp.
//   Đối xứng exporttext; là đường "đẩy bản clean lên Drive" (KHÁC upload nhận file gốc base64).
// POST JSON: { token, action:'createtext', text, name|title, cat?/folderId?, share?, register? }
//   FIX v2.4.1: Drive.Files.update (KHÔNG DriveApp.addFile/removeFile) + giữ newline.
function doCreateText_(p){
  if(!p.text) throw new Error('createtext: thiếu text');
  var folderId=resolveFolder_(p);
  var name=p.name || p.title || ('taluat_'+Date.now());
  // 1. Tạo Google Doc (ở My Drive root) + ghi nội dung GIỮ NEWLINE
  var doc=DocumentApp.create(name);
  var body=doc.getBody(); body.clear();
  var lines=String(p.text).split('\n');
  body.appendParagraph(lines[0]);
  for(var i=1;i<lines.length;i++) body.appendParagraph(lines[i]);
  doc.saveAndClose();
  var fileId=doc.getId();
  // 2. Move root → folderId bằng Drive.Files.update (giống doMove_; tránh root-removal error)
  var cur=Drive.Files.get(fileId, {fields:'parents', supportsAllDrives:true});
  var remove=(cur.parents||[]).filter(function(id){ return id!==folderId; }).join(',');
  Drive.Files.update({}, fileId, null, {addParents:folderId, removeParents:remove, supportsAllDrives:true, fields:'id,parents'});
  // 3. Stamp provenance (nếu có), share, register
  stampProps_(fileId, provenance_(p, '', p.sourceUrl || 'createtext'));
  if(String(p.share)!=='false')    shareView_(fileId);
  if(String(p.register)!=='false') registerRow_({id:fileId, name:name, mime:'application/vnd.google-apps.document', sha256:''});
  return {ok:true, fileId:fileId, name:name, created:true,
          viewUrl:'https://docs.google.com/document/d/'+fileId+'/view',
          downloadUrl:'https://docs.google.com/document/d/'+fileId+'/export?format=docx'};
}
// copy_convert: copy file Drive (docx/doc/pdf) đang có sẵn → Google Doc, hoàn toàn server-side.
// LUỒNG ĐÚNG cho file .docx/.doc đã ở Drive: KHÔNG cần download về container, KHÔNG cần base64.
//   1. Drive.Files.copy(srcId, {name, mimeType:'application/vnd.google-apps.document', parents:[folderId]})
//   2. Kết quả: Google Doc mới → source_add(drive, doc, newDocId) vào NotebookLM.
// POST/GET: { token, action:'copy_convert', fileId, name?, cat?/folderId?, share?, register? }
//   (v2.8.0: fileId CÓ THỂ là file link-shared NGOÀI corpus — Drive.Files.copy không phân biệt nguồn.)
function doCopyConvert_(p){
  if(!p.fileId) throw new Error('copy_convert: thiếu fileId (ID file .docx/.doc/.pdf nguồn)');
  var folderId = resolveFolder_(p);
  var srcMeta = Drive.Files.get(p.fileId, {fields:'name,mimeType', supportsAllDrives:true});
  var name = p.name || p.title || srcMeta.name.replace(/\.(docx?|pdf|xlsx?|csv)$/i,'');
  // v2.13.5: toType chọn đích convert. Không truyền ⇒ 'doc' (giữ hành vi cũ).
  //   .xlsx/.xls/.csv → 'sheets'; .docx/.pdf → 'doc'. NLM chỉ nhận Google Doc/Sheet.
  var TYPE_MAP = {
    doc:    'application/vnd.google-apps.document',
    sheets: 'application/vnd.google-apps.spreadsheet',
    slides: 'application/vnd.google-apps.presentation'
  };
  var toMime = TYPE_MAP[String(p.toType||'doc').toLowerCase()] || TYPE_MAP.doc;
  // Drive.Files.copy với mimeType đích → server-side convert (giữ bảng, không scan)
  var copied = Drive.Files.copy(
    {name: name, mimeType: toMime, parents: [folderId]},
    p.fileId,
    {supportsAllDrives: true, fields: 'id,name,mimeType,webViewLink'}
  );
  stampProps_(copied.id, provenance_(p, '', 'copy_convert:'+p.fileId));
  if(String(p.share)!=='false')    shareView_(copied.id);
  if(String(p.register)!=='false') registerRow_({id:copied.id, name:copied.name, mime:copied.mimeType, sha256:''});
  return {ok:true, fileId:copied.id, name:copied.name, mime:copied.mimeType,
          srcFileId:p.fileId, srcName:srcMeta.name, folderId:folderId,
          viewUrl: copied.webViewLink || ('https://drive.google.com/file/d/'+copied.id+'/view')};
}

/* ============ IMPORT EXTERNAL (v2.8.0) ============
 * Nạp folder/file từ LINK Drive NGOÀI (anyone-with-link viewer là đủ).
 * - listext: liệt kê folder ngoài theo ID (item link-shared KHÔNG hiện trong search corpus → phải theo ID).
 * - importext/importlink: Drive.Files.copy server-side, convert → Google Doc, COPY chứ không shortcut
 *   (chủ link thu hồi quyền được — corpus phải bền).
 * - Dedup: copy server-side KHÔNG có bytes để sha256 → dùng appProperties {srcId, srcMd5}
 *   (md5Checksum của file nguồn; Google-native không có md5 → dedup theo srcId).
 * - Đích (extDest_): destFolderId > destName > cat > [tên folder nguồn] > ROOT. KHÔNG dùng p.folderId
 *   (trong importlink, folderId là id NGOÀI).
 */
var EXT_FOLDER_MIME_   = 'application/vnd.google-apps.folder';
var EXT_SHORTCUT_MIME_ = 'application/vnd.google-apps.shortcut';
var EXT_GDOC_MIME_     = 'application/vnd.google-apps.document';

// Liệt kê con trực tiếp của folder NGOÀI theo ID (kèm shortcutDetails; KHÔNG đụng listChildren_ của regen).
function listExtChildren_(folderId, pageToken, cap){
  var files=[], folders=[], token=pageToken||null, capN=cap||CONFIG.LISTEXT_CAP;
  do{
    var r=Drive.Files.list({q:"'"+folderId+"' in parents and trashed=false",
      fields:'nextPageToken,files(id,name,mimeType,size,md5Checksum,shortcutDetails)',
      pageSize:100, supportsAllDrives:true, includeItemsFromAllDrives:true, pageToken:token});
    (r.files||[]).forEach(function(f){
      var rec={id:f.id, name:f.name, mimeType:f.mimeType, size:Number(f.size)||0,
               md5Checksum:f.md5Checksum||'',
               shortcutTargetId:(f.shortcutDetails && f.shortcutDetails.targetId)||''};
      (f.mimeType===EXT_FOLDER_MIME_ ? folders : files).push(rec);
    });
    token=r.nextPageToken;
  }while(token && files.length<capN);
  return {files:files, folders:folders, nextPageToken:token||''};
}

// GET: { token, action:'listext', folderId|id, pageToken? }
function doListExt_(p){
  var fid=p.folderId||p.id;
  if(!fid) throw new Error('listext: thiếu folderId');
  try{
    var r=listExtChildren_(fid, p.pageToken, CONFIG.LISTEXT_CAP);
    return {ok:true, folderId:fid, count:r.files.length, files:r.files, folders:r.folders,
            nextPageToken:r.nextPageToken,
            capped: !!r.nextPageToken && r.files.length>=CONFIG.LISTEXT_CAP};
  }catch(e){
    return {ok:false, error:'listext: '+String(e && e.message || e)
            +' (link bị thu hồi quyền, ID sai, hoặc không phải folder?)'};
  }
}

// GET: { token, action:'resolvefolder', name, parentId?, create? } — tìm-hoặc-tạo subfolder theo TÊN.
// Alias mỏng quanh doMkdir_ (cùng semantics find-or-create), mặc định parent = VBQPPL gốc, trả thêm url.
function doResolveFolder_(p){
  if(!p.name) throw new Error('resolvefolder: thiếu name');
  if(String(p.create)==='false'){
    var parent=DriveApp.getFolderById(p.parentId||rootId_());
    var it=parent.getFoldersByName(p.name);
    if(it.hasNext()){ var ex=it.next();
      return {ok:true, folderId:ex.getId(), name:p.name, created:false,
              url:'https://drive.google.com/drive/folders/'+ex.getId()}; }
    return {ok:false, error:'resolvefolder: không thấy "'+p.name+'" (create=false)'};
  }
  var r=doMkdir_({name:p.name, parentId:p.parentId||rootId_()});
  r.url='https://drive.google.com/drive/folders/'+r.folderId;
  return r;
}

// Đích cho import external. KHÔNG dùng p.folderId (id NGOÀI trong importlink).
function extDest_(p, defaultName){
  if (p.destFolderId) return p.destFolderId;
  if (p.destName) return doMkdir_({name:p.destName, parentId:p.destParentId||rootId_()}).folderId;
  if (p.cat !== undefined && String(p.cat).trim() !== ''){
    var fid = resolveCatFolderId_(p.cat);
    if (!fid) throw new Error('extDest_: khong resolve duoc cat "'+p.cat+'"');
    return fid;
  }
  if (defaultName) return doMkdir_({name:defaultName, parentId:rootId_()}).folderId;
  return rootId_();
}

// Dedup theo provenance: đã từng import file nguồn này chưa? (srcMd5 ưu tiên; Google-native → srcId)
function findImported_(srcId, srcMd5){
  var q = srcMd5
    ? "appProperties has { key='srcMd5' and value='"+srcMd5+"' } and trashed=false"
    : "appProperties has { key='srcId' and value='"+srcId+"' } and trashed=false";
  var r=Drive.Files.list({q:q, fields:'files(id,name,parents)', pageSize:2,
                          supportsAllDrives:true, includeItemsFromAllDrives:true});
  return (r.files && r.files.length) ? r.files[0] : null;
}

// Copy 1 file ngoài → Google Doc trong destId. opts={share,register,force}. Trả record per-file, KHÔNG ném.
function copyOneExt_(srcId, destId, name, opts){
  opts=opts||{};
  var meta;
  try{
    meta=Drive.Files.get(srcId, {fields:'id,name,mimeType,size,md5Checksum,shortcutDetails',
                                 supportsAllDrives:true});
  }catch(e){
    return {ok:false, srcId:srcId, error:'GET: '+String(e && e.message || e)+' (quyền bị thu hồi / ID sai?)'};
  }
  if(meta.mimeType===EXT_SHORTCUT_MIME_ && meta.shortcutDetails && meta.shortcutDetails.targetId){
    return copyOneExt_(meta.shortcutDetails.targetId, destId, name||meta.name, opts);  // resolve shortcut
  }
  if(meta.mimeType===EXT_FOLDER_MIME_)
    return {ok:false, srcId:srcId, srcName:meta.name, skipped:true, error:'là folder — dùng importlink riêng (hỏi người dùng trước khi đệ quy)'};
  if(/^(image|audio|video)\//.test(meta.mimeType||''))
    return {ok:false, srcId:srcId, srcName:meta.name, skipped:true, error:'mime '+meta.mimeType+' — không phải văn bản'};
  if(Number(meta.size||0)>CONFIG.UPLOAD_MAX_BYTES)
    return {ok:false, srcId:srcId, srcName:meta.name, skipped:true, error:'>'+Math.round(CONFIG.UPLOAD_MAX_BYTES/1048576)+'MB — copy tay'};
  if(String(opts.force)!=='true'){
    var dup=findImported_(srcId, meta.md5Checksum||'');
    if(dup) return {ok:true, srcId:srcId, srcName:meta.name, dedup:'skip',
                    existing:dup, note:'đã import trước đó (provenance srcMd5/srcId trùng)'};
  }
  var isGDoc=(meta.mimeType===EXT_GDOC_MIME_);
  var body={name:name||meta.name, parents:[destId]};
  if(!isGDoc) body.mimeType=EXT_GDOC_MIME_;            // convert khi copy (docx/doc/pdf-text/html)
  var copied;
  try{
    copied=Drive.Files.copy(body, srcId, {supportsAllDrives:true, fields:'id,name,mimeType'});
  }catch(e){
    return {ok:false, srcId:srcId, srcName:meta.name, error:'copy: '+String(e && e.message || e)};
  }
  // Provenance: nối vào hệ stamp/findprop hiện hành; srcMd5/srcId là khóa dedup idempotent.
  var props=provenance_(opts.p||{}, '', 'importlink:'+srcId);
  props.srcId=srcId; if(meta.md5Checksum) props.srcMd5=meta.md5Checksum;
  stampProps_(copied.id, props);
  if(String(opts.share)!=='false')   shareView_(copied.id);
  if(String(opts.register)==='true') registerRow_({id:copied.id, name:copied.name, mime:copied.mimeType, sha256:''});
  return {ok:true, srcId:srcId, srcName:meta.name, fileId:copied.id, name:copied.name,
          converted:!isGDoc, mime:copied.mimeType,
          viewUrl:'https://docs.google.com/document/d/'+copied.id+'/view'};
}

// POST: { token, action:'importext', files:[{id,name?},...] (≤30),
//         destFolderId?|destName?(+destParentId?)|cat?, share?:'true', register?:'false', force? }
function doImportExt_(p){
  var list=p.files; if(typeof list==='string'){ try{ list=JSON.parse(list); }catch(e){ throw new Error('importext: files không phải JSON'); } }
  if(!list || !list.length) throw new Error('importext: thiếu files[]');
  list = list.map(function(x){ return (typeof x === 'string') ? {id:x} : x; });
  if(list.length>CONFIG.IMPORT_MAX_PER_CALL) throw new Error('importext: batch >'+CONFIG.IMPORT_MAX_PER_CALL+' — chia đợt');
  var destId=extDest_(p, null);
  var opts={share:p.share, register:p.register, force:p.force, p:p};
  var out=[], started=Date.now(), i=0;
  for(; i<list.length; i++){
    if(Date.now()-started>CONFIG.IMPORT_TIME_BUDGET_MS) break;   // chừa thời gian trả response
    out.push(copyOneExt_(list[i].id, destId, list[i].name, opts));
  }
  var remaining=list.slice(i).map(function(f){ return f.id; });
  return {ok:true, destFolderId:destId,
          destFolderUrl:'https://drive.google.com/drive/folders/'+destId,
          count:out.length,
          okCount:out.filter(function(r){return r.ok && !r.dedup;}).length,
          dedupSkipped:out.filter(function(r){return r.dedup==='skip';}).length,
          results:out, remainingIds:remaining,
          note:'results[].fileId là Google Doc → source_add(source_type=drive, doc_type=doc). '
              +'remainingIds không rỗng → gọi lại importext với danh sách đó.'};
}

// POST: { token, action:'importlink', id (folder HOẶC file ngoài),
//         destFolderId?|destName?|cat?,        // folder nguồn + không chỉ đích → subfolder CÙNG TÊN trong ROOT
//         share?:'true', register?:'false', max?:'25', pageToken?, skipIds?:'id1,id2', force? }
function doImportLink_(p){
  var id=p.id||p.fileId||p.linkId;
  if(!id) throw new Error('importlink: thiếu id (bóc từ link bằng import_drive_link.py parse)');
  var meta;
  try{ meta=Drive.Files.get(id, {fields:'id,name,mimeType', supportsAllDrives:true}); }
  catch(e){ return {ok:false, error:'importlink: không truy cập được id — '+String(e && e.message || e)
                    +' (link bị thu hồi quyền / chưa share anyone-with-link?)'}; }
  var opts={share:p.share, register:p.register, force:p.force, p:p};

  // FILE đơn (kể cả shortcut — copyOneExt_ tự resolve)
  if(meta.mimeType!==EXT_FOLDER_MIME_){
    var destId1=extDest_(p, null);
    var r1=copyOneExt_(id, destId1, p.name, opts);
    return {ok:r1.ok!==false, kind:'file', destFolderId:destId1, results:[r1]};
  }

  // FOLDER: không chỉ đích → subfolder CÙNG TÊN folder nguồn trong VBQPPL gốc
  var destId=extDest_(p, meta.name);
  var lst;
  try{ lst=listExtChildren_(id, p.pageToken, CONFIG.LISTEXT_CAP); }
  catch(e){ return {ok:false, error:'importlink/list: '+String(e && e.message || e)}; }
  var skip={};
  String(p.skipIds||'').split(',').forEach(function(s){ s=s.trim(); if(s) skip[s]=true; });
  var max=Math.min(parseInt(p.max||'25',10)||25, CONFIG.IMPORT_MAX_PER_CALL);
  var out=[], started=Date.now(), i=0;
  for(; i<lst.files.length && out.length<max; i++){
    if(Date.now()-started>CONFIG.IMPORT_TIME_BUDGET_MS) break;
    if(skip[lst.files[i].id]) continue;
    out.push(copyOneExt_(lst.files[i].id, destId, null, opts));
  }
  var remaining=lst.files.slice(i).filter(function(f){ return !skip[f.id]; })
                         .map(function(f){ return f.id; });
  return {ok:true, kind:'folder', srcFolderId:id, srcFolder:meta.name,
          destFolderId:destId, destFolderUrl:'https://drive.google.com/drive/folders/'+destId,
          copied:out.filter(function(r){return r.ok && !r.dedup;}).length,
          dedupSkipped:out.filter(function(r){return r.dedup==='skip';}).length,
          failed:out.filter(function(r){return r.ok===false && !r.skipped;}).length,
          skipped:out.filter(function(r){return r.skipped;}).length,
          results:out, remainingIds:remaining, nextPageToken:lst.nextPageToken||'',
          subfolders:lst.folders,
          note:'remainingIds → importext({files:[...], destFolderId:"'+destId+'"}) đợt sau. '
              +'subfolders → HỎI người dùng trước khi importlink đệ quy từng folder con. '
              +'results[].fileId (Google Doc) → cổng hậu-copy skill (scan-check/dedup_gate/standardize_name) '
              +'rồi source_add(drive, doc). regen confirm=yes 1 LẦN cuối phiên.'};
}

function createFromBlob_(p, bytes, mime, blob, sourceUrl){
  var sha=sha256Hex_(bytes), folderId=resolveFolder_(p);
  if(String(p.force)!=='true'){
    var dup=Drive.Files.list({q:"appProperties has { key='sha256' and value='"+sha+"' } and trashed=false",
      fields:'files(id,name,parents)', supportsAllDrives:true, includeItemsFromAllDrives:true});
    if(dup.files && dup.files.length) return {ok:true, skipped:true, reason:'Đã tồn tại (trùng sha256)', sha256:sha, existing:dup.files[0]};
  }
  var convert=smartConvert_(mime, bytes.length, p);
  var name=p.title || blob.getName() || ('VB_'+sha.slice(0,8));
  var created = convert
    ? Drive.Files.create({name:name, mimeType:'application/vnd.google-apps.document', parents:[folderId]}, blob, {supportsAllDrives:true, fields:'id,name,mimeType'})
    : Drive.Files.create({name:name, parents:[folderId]}, blob, {supportsAllDrives:true, fields:'id,name,mimeType,md5Checksum'});
  var note=(!convert && /pdf/i.test(mime) && bytes.length>CONFIG.PDF_CONVERT_MAX)
         ? 'PDF lớn: lưu nguyên bản (tránh cắt cụt); nạp NotebookLM dạng Drive-PDF.' : '';
  stampProps_(created.id, provenance_(p, sha, sourceUrl));
  if(String(p.share)!=='false')    shareView_(created.id);
  if(String(p.register)!=='false') registerRow_({id:created.id, name:created.name, mime:created.mimeType, sha256:sha});
  return {ok:true, fileId:created.id, name:created.name, mime:created.mimeType,
          converted:!!convert, sha256:sha, bytes:bytes.length, viewUrl:viewUrl_(created.id, created.mimeType), note:note};
}

/* ============ FILE OPS ============ */
function doRename_(p){ var f=anyById_(p.fileId), old=f.getName(); f.setName(p.name);
  return {ok:true, fileId:p.fileId, oldName:old, newName:p.name}; }
function doTrash_(p){ requireConfirm_(p); var f=anyById_(p.fileId), name=f.getName(); f.setTrashed(true);
  return {ok:true, fileId:p.fileId, name:name, trashed:true}; }
function doRestore_(p){ anyById_(p.fileId).setTrashed(false); return {ok:true, fileId:p.fileId, trashed:false}; }
function doMkdir_(p){
  var parent=DriveApp.getFolderById(p.parentId||rootId_());
  var it=parent.getFoldersByName(p.name);
  if(it.hasNext()){ var ex=it.next(); return {ok:true, folderId:ex.getId(), name:p.name, created:false}; }
  var nf=parent.createFolder(p.name);
  // Folder mới có thể là cat mới (NN_...) → xoá cache để lần resolve sau thấy ngay.
  try{ CacheService.getScriptCache().remove(CAT_CACHE_KEY); }catch(e){}
  return {ok:true, folderId:nf.getId(), name:p.name, created:true};
}
function doMove_(p){
  var to=resolveFolder_(p);
  var cur=Drive.Files.get(p.fileId, {fields:'parents', supportsAllDrives:true});
  var remove=(cur.parents||[]).filter(function(id){ return id!==to; }).join(',');
  var updated=Drive.Files.update({}, p.fileId, null,
    {addParents:to, removeParents:remove, supportsAllDrives:true, fields:'id,parents'});
  return {ok:true, fileId:p.fileId, toFolderId:to, parents:updated.parents, removedFrom:remove};
}
function doList_(p){
  var fid=resolveFolder_(p), cap=CONFIG.LIST_CAP, items;
  if(String(p.recursive)==='true'){
    items=[]; var all=listTree_(fid);
    for(var i=0;i<all.length && items.length<cap;i++){ var x=all[i];
      items.push({id:x.id,name:x.name,mime:x.mimeType,size:Number(x.size)||0,type:x.mimeType==='application/vnd.google-apps.folder'?'folder':'file'}); }
  }else{
    items=listChildren_(fid).slice(0,cap).map(function(x){
      return {id:x.id,name:x.name,mime:x.mimeType,size:Number(x.size)||0,type:x.mimeType==='application/vnd.google-apps.folder'?'folder':'file'}; });
  }
  return {ok:true, folderId:fid, count:items.length, capped:items.length>=cap, items:items};
}
function doInfo_(p){
  var f=Drive.Files.get(p.fileId,{fields:'id,name,mimeType,size,md5Checksum,parents,trashed,modifiedTime,appProperties',supportsAllDrives:true});
  var isNative=String(f.mimeType||'').indexOf('application/vnd.google-apps')===0;
  return {ok:true, file:f, note:isNative?'Google-native: size/md5Checksum luôn rỗng — dùng appProperties.sha256 để so trùng.':null};
}
function doResolve_(p){
  // v2.13.0: bỏ DriveApp.searchFiles (quét TOÀN My Drive, hay trả thiếu) → Drive.Files.list.
  return doSearch_({ q: p.name, scope: p.scope || 'all', max: p.max });
}
// v2.13.0 doSearch_: thay Drive MCP search_files. scope='corpus' (mặc định) chỉ tìm trong
// cây VBQPPL (lọc theo parents thuộc categories + root); scope='all' tìm toàn Drive của tài khoản.
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
function doSearch_(p){
  var q = stripVN_(String(p.q||p.name||'').trim()).toLowerCase();
  if(!q) return {ok:false, error:'search: thiếu q'};
  var MAX = Math.min(Number(p.max)||25, 100);
  var byNum = canonSoHieu_(findSoHieuInQuery_(p.q||p.name||'') || '');
  var objs = regReadAll_(String(p.refresh)==='true');
  var out=[];
  for(var i=0;i<objs.length && out.length<MAX;i++){
    var o=objs[i];
    var nm = stripVN_(String(o.name||'')).toLowerCase();
    var hitNum = byNum && canonSoHieu_(o.sohieu||sohieuFromName_(o.name))===byNum;
    var hitName = nm.indexOf(q)>=0;
    var hitKw = stripVN_(String(o.tukhoa||'')).toLowerCase().indexOf(q)>=0; // v2.19.0
    if(hitNum || hitName || hitKw){
      out.push({ id:o.drive_id||'', drive_id:o.drive_id||'', name:o.name||'', mime:o.mime||'',
        sohieu:o.sohieu||'', cat:o.cat||'', hieuluc:o.hieuluc||'', tukhoa:o.tukhoa||'', // v2.19.0
        nlm_source_id:o.nlm_source_id||'', nlm_status:o.nlm_status||'',
        on_nlm: !!o.nlm_source_id && !nlmIsRemoved_(o) });
    }
  }
  out.sort(registryRankCompare_);
  return {ok:true, scope:'registry', q:p.q||p.name, count:out.length, matches:out,
    note:'v2.17.0: search dựa REGISTRY (bỏ Drive.Files.list, hết Invalid Value). fullText nội dung không hỗ trợ ở action này.'};
}
// v2.13.0 doDownload_: trả b64 nội dung file BẤT KỲ (docx/pdf/json/binary). Google-native
// thì export theo exportMime (mặc định docx cho GDoc, text/plain nếu p.as='text').
var DOWNLOAD_MAX_BYTES_ = 9*1024*1024; // dưới trần payload Apps Script ~10MB sau b64
function doDownload_(p){
  if (!p.fileId) return { ok:false, error:'download: thiếu fileId' };
  var meta = Drive.Files.get(p.fileId, {fields:'id,name,mimeType,size', supportsAllDrives:true});
  var blob;
  if (String(meta.mimeType||'').indexOf('application/vnd.google-apps') === 0){
    var em = p.exportMime || (p.as==='text' ? 'text/plain'
      : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document');
    blob = exportBlob_(p.fileId, em);
  } else {
    blob = DriveApp.getFileById(p.fileId).getBlob();
  }
  var bytes = blob.getBytes();
  if (bytes.length > DOWNLOAD_MAX_BYTES_)
    return { ok:false, error:'download: file '+bytes.length+'B > trần '+DOWNLOAD_MAX_BYTES_+'B — tải theo trang/exporttext' };
  return { ok:true, fileId:p.fileId, name:meta.name, mime:blob.getContentType(),
           bytes:bytes.length, b64:Utilities.base64Encode(bytes) };
}
// v2.13.2 doOrganize_: sắp xếp 1 file trong MỘT call — các bước ĐỀU tùy chọn, làm theo
// đúng thứ tự: convert? -> rename? -> move? -> stamp? -> register?. Trả về kết quả từng bước.
// Params: fileId (bắt buộc); convert=true|false; name=<tên mới> (bỏ qua = giữ tên);
//   cat=<NN|folderId> (bỏ qua = không move); moveSrc=true (move/rename CẢ file gốc cùng base name);
//   stamp: sohieu/loai/linhvuc/goc/hieuluc; register=true kèm mọi cột REG (title_vn, linhvuc_list, sua_doi...).
// KHÔNG bước nào là bắt buộc — chỉ làm bước có tham số. share=true để cấp anyoneView.
function doOrganize_(p){
  if (!p.fileId) return { ok:false, error:'organize: thiếu fileId' };
  var steps = {}, id = p.fileId, srcId = p.srcId || '';
  // 1. convert (binary -> Google Doc; giữ binary làm src)
  if (String(p.convert) === 'true'){
    var cv = doCopyConvert_({ fileId: id, name: p.name || '' });
    if (!cv.ok) return { ok:false, step:'convert', error: cv.error };
    srcId = id; id = cv.newId || cv.fileId || cv.id;
    steps.convert = { ok:true, gdocId: id, srcId: srcId };
  }
  // 2. rename (name='' => giữ nguyên)
  if (p.name){
    var f = anyById_(id), oldName = f.getName(); f.setName(p.name);
    steps.rename = { ok:true, from: oldName, to: p.name };
    if (String(p.moveSrc) === 'true' && srcId){
      try {
        var sf = anyById_(srcId), ext = (sf.getName().match(/\.[A-Za-z0-9]+$/) || [''])[0];
        sf.setName(p.name + ext);
        steps.renameSrc = { ok:true, to: p.name + ext };
      } catch(e){ steps.renameSrc = { ok:false, error: String(e) }; }
    }
  }
  // 3. move (cat = mã NN hoặc folderId trực tiếp)
  if (p.cat){
    var catStr = String(p.cat).trim(), folderId;
    if (/^\d{1,2}$|^QUARANTINE$/.test(catStr)){
      folderId = resolveCatFolderId_(catStr);
      if (!folderId) return { ok:false, step:'move', steps:steps, error:'organize: khong resolve duoc cat "'+catStr+'"' };
    } else folderId = catStr;
    var mv = doMove_({ fileId: id, folderId: folderId, removeFromParent: 'true' });
    if (!mv.ok) return { ok:false, step:'move', steps: steps, error: mv.error };
    steps.move = { ok:true, folderId: folderId };
    if (String(p.moveSrc) === 'true' && srcId){
      try { doMove_({ fileId: srcId, folderId: folderId, removeFromParent: 'true' });
            steps.moveSrc = { ok:true }; }
      catch(e){ steps.moveSrc = { ok:false, error: String(e) }; }
    }
  }
  // 4. stamp appProperties (chỉ key có giá trị, tôn trọng trần 124B)
  var stampKeys = ['sohieu','loai','linhvuc','goc','hieuluc'], st = {};
  stampKeys.forEach(function(k){ if (p[k]) st[k] = String(p[k]).slice(0, 100); });
  if (Object.keys(st).length){
    try { Drive.Files.update({ appProperties: st }, id, null, { supportsAllDrives: true });
          steps.stamp = { ok:true, keys: Object.keys(st) }; }
    catch(e){ steps.stamp = { ok:false, error: String(e) }; }
  }
  // 5. share (tùy chọn) — trả webViewLink THẬT từ Drive API (không tự ghép URL)
  if (String(p.share) === 'true'){
    try {
      shareView_(id);
      var meta2 = Drive.Files.get(id, { fields:'webViewLink', supportsAllDrives:true });
      steps.share = { ok:true, url: meta2.webViewLink };
    }
    catch(e){ steps.share = { ok:false, error: String(e) }; }
  }
  // 6. register (1 chu kỳ lock duy nhất)
  if (String(p.register) === 'true'){
    var row = { drive_id: id };
    ['src_id','sohieu','loai','name','cat','linhvuc','goc','verified','note',
     'title_vn','linhvuc_list','hieuluc','sua_doi'].forEach(function(k){
      if (p['reg_' + k] !== undefined) row[k] = String(p['reg_' + k]);
      else if (k === 'src_id' && srcId) row[k] = srcId;
      else if (k === 'name' && p.name) row[k] = p.name;
      else if ((k === 'linhvuc' || k === 'goc' || k === 'loai' || k === 'sohieu' || k === 'hieuluc') && p[k]) row[k] = String(p[k]);
    });
    var up = doRegUpsert_(row);
    steps.register = up.ok ? { ok:true } : { ok:false, error: up.error };
  }
  return { ok:true, fileId: id, srcId: srcId || undefined, steps: steps };
}

/** v2.21.2o (ADR-0014, r198): ingest_commit = organize(+rename)+register+READBACK (row snapshot + file info)
 *  trong MỘT round-trip — thay chuỗi client organize → info×N → reg_get×N (~2s/call đường truyền).
 *  SUB-STEP MARKER: organize_done/rename_done/upsert_done — lỗi giữa chừng trả PARTIAL (đã-xong-gì) chứ
 *  KHÔNG im lặng, để journal/--resume (ADR-0011/D5) map đúng điểm đứt. Tham số = đúng bộ doOrganize_
 *  (fileId, convert, name, moveSrc, cat = mã NN vbqppl HOẶC folderId flat profile, reg_*, sohieu/loai/
 *  hieuluc, share, register) — đủ cho CẢ ingest-local lẫn profile-ingest; client r198 chỉ dùng nhánh
 *  profile (ADR-0014 #6). Ý thức trần 6'/request: organize là phần nặng nhất (~21s đo 24-07), còn xa trần;
 *  partial marker là van xả khi convert file lớn chết giữa chừng. */
function doIngestCommit_(p){
  var t0 = Date.now();
  var out = { ok:false, organize_done:false, rename_done:false, upsert_done:false,
              row:null, file:null, src_file:null };
  var org = doOrganize_(p);
  if (!org.ok){
    out.error = 'ingest_commit@organize: ' + (org.error || '');
    out.step = 'organize' + (org.step ? (':' + org.step) : '');
    out.organize = org; out.elapsed_ms = Date.now() - t0; return out;
  }
  out.organize_done = true;
  out.fileId = org.fileId; out.srcId = org.srcId || '';
  var st = org.steps || {};
  out.rename_done = p.name ? !!(st.rename && st.rename.ok) : true;
  if (String(p.register) === 'true'){
    out.upsert_done = !!(st.register && st.register.ok);
    if (!out.upsert_done){
      out.error = 'ingest_commit@register: ' + ((st.register || {}).error || 'register fail');
      out.step = 'register'; out.elapsed_ms = Date.now() - t0; return out;
    }
  } else out.upsert_done = true;   // call không yêu cầu ghi registry
  // Readback registry row AUTHORITATIVE (refresh=true — né cache đọc 600s)
  try {
    var rb = doRegGet_({ drive_id: out.fileId, refresh: 'true' });
    out.row = (rb && rb.ok && rb.rows && rb.rows.length) ? rb.rows[0] : null;
  } catch(e){ out.row = null; out.row_error = String(e); }
  // Readback file info (gdoc + src) — thay info×N phía client
  function finfo_(id){
    var m = Drive.Files.get(id, { fields:'id,name,mimeType,md5Checksum,size,parents', supportsAllDrives:true });
    return { id:m.id, name:m.name, mimeType:m.mimeType, md5:m.md5Checksum || '',
             size:m.size || '', parents:m.parents || [] };
  }
  try { out.file = finfo_(out.fileId); } catch(e){ out.file = null; out.file_error = String(e); }
  if (out.srcId){
    try { out.src_file = finfo_(out.srcId); } catch(e){ out.src_file = null; out.src_file_error = String(e); }
  }
  out.ok = !!(out.organize_done && out.rename_done && out.upsert_done && out.file
              && (String(p.register) !== 'true' || out.row));
  if (!out.ok && !out.error){
    out.error = !out.file ? ('ingest_commit@file_readback: ' + (out.file_error || ''))
                          : 'ingest_commit@row_readback: row not found sau register';
    out.step = !out.file ? 'file_readback' : 'row_readback';
  }
  out.elapsed_ms = Date.now() - t0;
  return out;
}

/* ============ INTEGRITY (dùng chung quét phân trang listTree_) ============ */
function doVerifyShares_(p){
  var fid=resolveFolder_(p), total=0, ok=0, err=0, fails=[];
  listTree_(fid).forEach(function(x){
    if(x.mimeType==='application/vnd.google-apps.folder') return;
    total++;
    try{ DriveApp.getFileById(x.id).setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW); ok++; }
    catch(e){ err++; if(fails.length<50) fails.push({id:x.id, name:x.name, error:String(e)}); }
  });
  return {ok:true, scanned:total, reshared:ok, failed:err, failsSample:fails};
}
function doDedup_(p){
  var fid=resolveFolder_(p), map={}, scanned=0;
  listTree_(fid).forEach(function(x){
    if(x.mimeType==='application/vnd.google-apps.folder') return;
    scanned++;
    var ap=x.appProperties||{}, key, method;
    if(ap.sha256){ key='sha256:'+ap.sha256; method='sha256'; }
    else if(ap.srcMd5){ key='srcMd5:'+ap.srcMd5; method='srcMd5(import)'; }       // v2.8.0
    else if(x.md5Checksum){ key='md5:'+x.md5Checksum; method='md5'; }
    else { key='name:'+x.name; method='name(yếu)'; }
    (map[key]=map[key]||{method:method, files:[]}).files.push({id:x.id, name:x.name, mime:x.mimeType});
  });
  var dups=Object.keys(map).filter(function(k){return map[k].files.length>1;})
    .map(function(k){return {key:k, method:map[k].method, files:map[k].files};});
  return {ok:true, scanned:scanned, duplicateGroups:dups, note:'Xem method từng nhóm rồi trash thủ công (trash cần confirm=yes).'};
}

/* ============ EXPORT (lưu vào Drive / trả nội dung trong response) ============ */
// FIX v2.4.1: dùng UrlFetchApp + REST /export (tránh wrapper Advanced Service bất định).
//   `Drive.Files.export()` (Advanced Drive Service) ném lỗi KHÔNG NHẤT QUÁN "Export requires alt=media":
//   REST files.export VỐN trả bytes, nhưng lớp wrapper đôi khi ném lỗi này (undocumented, tùy môi trường).
//   Gọi thẳng REST endpoint với Authorization: Bearer ScriptApp.getOAuthToken() → trả media ổn định.
//   (Quirk kế thừa từ v2.0.0 khi đổi từ exportBlob_ sang Drive.Files.export.)
// FIX v2.5.1: gốc lỗi "URL has not been whitelisted in the script manifest" là do
//   appsscript.json THIẾU "https://www.googleapis.com/" trong urlFetchWhitelist.
//   => Vá CHÍNH: thêm "https://www.googleapis.com/" vào urlFetchWhitelist (xem appsscript.json).
//   Thêm fallback Advanced Drive Service để bền: nếu UrlFetchApp bị chặn whitelist thì
//   rơi sang Drive.Files.export() (đã bật trong dependencies).
function exportBlob_(fileId, mime){
  // === FIX (export-scope): ưu tiên Advanced Drive Service — KHÔNG cần script.external_request ===
  // Tránh lỗi "permission to call UrlFetchApp.fetch" khi manifest thiếu scope.
  try{
    var b = Drive.Files.export(fileId, mime);   // Apps Script trả về Blob
    if(b && b.getBytes) return b;
  }catch(eAdv){
    // Quirk hiếm của wrapper v3 ("Export requires alt=media") → rơi xuống UrlFetchApp bên dưới.
    // Các lỗi khác (không phải Google-native, >~10MB, thiếu quyền) cũng thử nốt UrlFetchApp rồi mới ném.
  }
  // Fallback: REST /export qua UrlFetchApp (CẦN scope script.external_request + whitelist googleapis.com — Vá 1).
  var url='https://www.googleapis.com/drive/v3/files/'+encodeURIComponent(fileId)+
          '/export?mimeType='+encodeURIComponent(mime)+'&supportsAllDrives=true';
  var resp=UrlFetchApp.fetch(url, {headers:{Authorization:'Bearer '+ScriptApp.getOAuthToken()},
                                   muteHttpExceptions:true});
  if(resp.getResponseCode()===200) return resp.getBlob();
  throw new Error('export HTTP '+resp.getResponseCode()+
    ' (file phải là Google-native; export ~10MB; nếu lỗi quyền UrlFetchApp → thêm scope '+
    'script.external_request vào appsscript.json rồi Deploy New version)');
}

function doExport_(p){
  try{
    var mime=p.mimeType||'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
    var blob=exportBlob_(p.fileId, mime);
    if(blob.getBytes().length>CONFIG.EXPORT_MAX_BYTES)
      return {ok:false, error:'export > EXPORT_MAX_BYTES (~10MB hard-limit). VB nặng phụ lục: giữ .docx gốc.'};
    var dst=DriveApp.getFolderById(p.toFolderId||rootId_()).createFile(blob);
    if(p.name) dst.setName(p.name);
    return {ok:true, fileId:dst.getId(), name:dst.getName()};
  }catch(e){ return {ok:false, error:'export: '+String(e && e.message || e)+' (file phải là Google-native; trần ~10MB)'}; }
}
// Trả TEXT thuần trong response (cho bash: curl ... | jq -r .text > doc.txt)
function doExportText_(p){
  if(!p.fileId) throw new Error('exporttext: thiếu fileId');
  try{
    var text=exportBlob_(p.fileId, 'text/plain').getDataAsString('UTF-8');
    return {ok:true, fileId:p.fileId, chars:text.length, text:text};
  }catch(e){ return {ok:false, error:'exporttext: '+String(e && e.message || e)+' (chỉ Google-native; ~10MB)'}; }
}
// Trả .docx base64 (curl ... | jq -r .b64 | base64 -d > doc.docx)
function doExportDocx_(p){
  if(!p.fileId) throw new Error('exportdocx: thiếu fileId');
  try{
    var bytes=exportBlob_(p.fileId, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document').getBytes();
    if(bytes.length>CONFIG.EXPORT_MAX_BYTES) return {ok:false, error:'docx > EXPORT_MAX_BYTES (~10MB)'};
    return {ok:true, fileId:p.fileId, bytes:bytes.length, b64:Utilities.base64Encode(bytes)};
  }catch(e){ return {ok:false, error:'exportdocx: '+String(e && e.message || e)+' (chỉ Google-native; ~10MB)'}; }
}

/* ============ METADATA ============ */
function doStamp_(p){
  var props=(typeof p.props==='string') ? JSON.parse(p.props) : (p.props||provenance_(p, p.sha256, p.sourceUrl));
  var clean={}; Object.keys(props).forEach(function(k){ if(props[k]!=null && props[k]!=='') clean[k]=String(props[k]); });
  Drive.Files.update({appProperties:clean}, p.fileId, null, {supportsAllDrives:true, fields:'id,appProperties'});
  return {ok:true, fileId:p.fileId, props:clean};
}
function doFindProp_(p){
  var q="appProperties has { key='"+String(p.key).replace(/'/g,"\\'")+"' and value='"+String(p.value).replace(/'/g,"\\'")+"' } and trashed=false";
  var r=Drive.Files.list({q:q, fields:'files(id,name,appProperties,parents)', supportsAllDrives:true, includeItemsFromAllDrives:true});
  return {ok:true, matches:r.files||[]};
}
function doPinRevision_(p){
  var revs=Drive.Revisions.list(p.fileId, {fields:'revisions(id)'});
  var arr=revs.revisions||[]; if(!arr.length) throw new Error('Không có revision để ghim');
  var head=arr[arr.length-1].id;
  Drive.Revisions.update({keepForever:true}, p.fileId, head);
  return {ok:true, fileId:p.fileId, pinned:head};
}

/* ============ REGEN: manifest.json + Registry (1 vòng quét) ============ */
function doManifestRead_(p){
  var sp = PropertiesService.getScriptProperties();
  var mid=sp.getProperty('TL_MANIFEST_ID');
  if(!mid){
    var loc = locateManifest_();
    if (loc && loc.id){ mid = loc.id; sp.setProperty('TL_MANIFEST_ID', mid); }
  }
  if(!mid) return {ok:false, error:'Chưa có manifest — chạy action=regen2&confirm=yes rồi manifest_export trước'};
  var f=DriveApp.getFileById(mid);
  return {ok:true, manifestFileId:mid, name:f.getName(), updated:f.getLastUpdated().toISOString(),
          driveFileId:mid};
}

/* ============ CONFIG MIRROR ============
 * Nguồn CHÍNH = Script Property (TL_TOKEN, TL_WEBAPP_URL, TL_MANIFEST_ID, …) + CONFIG hardcode.
 * writeconfig: gom các giá trị đó -> ghi file JSON 'tra_luat_config.json' TRONG folder VBQPPL gốc (mirror).
 *              skill đọc file này lúc load để có WebApp URL + token + hằng số, KHỎI hỏi tay.
 * readconfig:  trả lại nội dung mirror (config private, KHÔNG downloadUrl public) để skill/bash đọc.
 * Token lưu THẲNG trong mirror theo yêu cầu vận hành; file nằm trong folder VBQPPL (cùng quyền corpus).
 * v2.6.0: categories trong mirror lấy từ getCategories_(true) (map ĐỘNG khớp folder thật),
 *         KHÔNG còn từ hằng số → file mirror luôn đúng hiện trạng.
 */
// v2.21.2g: đọc mirror config HIỆN CÓ để GIỮ/merge block đa-corpus v2 (schema/defaultProfile/profiles)
// khi rewrite/rotate token. Không có thì trả {}.
function readExistingConfigObject_(){
  var sp=PropertiesService.getScriptProperties(), cid=sp.getProperty('TL_CONFIG_ID');
  if(!cid) return {};
  try{
    var txt=DriveApp.getFileById(cid).getBlob().getDataAsString('UTF-8');
    return JSON.parse(stripBom_(txt) || '{}') || {};
  }catch(e){ return {}; }
}
function parseObjectParam_(v){
  if(!v) return {};
  if(typeof v === 'object') return v;
  try{ return JSON.parse(String(v)); }catch(e){ return {}; }
}
function mergeObjects_(a,b){
  var out={}, k;
  a=a||{}; b=b||{};
  for(k in a){ if(a.hasOwnProperty(k)) out[k]=a[k]; }
  for(k in b){ if(b.hasOwnProperty(k)) out[k]=b[k]; }
  return out;
}
function buildConfigObject_(p){
  var sp=PropertiesService.getScriptProperties();
  var webapp = (p && p.webappUrl) || sp.getProperty('TL_WEBAPP_URL') || '';
  if(p && p.webappUrl) sp.setProperty('TL_WEBAPP_URL', p.webappUrl);  // cho phép set 1 lần qua writeconfig
  // v2.21.2g (Cách B): GIỮ/merge profiles — KHÔNG xoá block đa-corpus v2 khi rotate token / writeconfig.
  var existing = readExistingConfigObject_();
  var incomingProfiles = parseObjectParam_(p && p.profiles);
  var profiles = mergeObjects_(existing.profiles || {}, incomingProfiles);
  // luôn đồng bộ profile nền vbqppl theo hằng số hiện hành (không phá profile dự án khác)
  var vbqpplProfile = mergeObjects_(profiles.vbqppl || {}, {
    rootFolderId: rootId_(),
    notebookId: sp.getProperty('TL_NOTEBOOK_VBQPPL') || '743ed200-2e55-4673-b7a0-9bfd13b41ce6',
    // v1.29.0 FIX (pending redeploy Apps Script): KHÔNG phát CONFIG.REGISTRY_DOC_ID (= Doc legacy 1mATG) — sẽ
    // clobber registryDocId đúng của config về Doc. Phát SHEET id THẬT đã resolve (regSS_ lưu TL_REGSHEET_ID_AUTO);
    // rỗng → auto-discover theo tên (client auto-heal). (Doc-constant chỉ còn dùng cho health-check line ~194.)
    registryDocId: sp.getProperty('TL_REGSHEET_ID_AUTO') || cfg_('TL_REGSHEET_ID','') || '',
    manifestId: sp.getProperty('TL_MANIFEST_ID') || '',
    categories: getCategories_(true)
  });
  profiles.vbqppl = vbqpplProfile;
  var hasProfiles = Object.keys(profiles).length > 0;
  var obj = {
    schema: hasProfiles ? 2 : 1,
    generatedAt: new Date().toISOString(),
    webappUrl: webapp,                          // URL /exec của chính web app này
    token: token_(),                            // mirror token (nguồn chính vẫn là Script Property)
    rootFolderId: rootId_(),
    registryDocId: sp.getProperty('TL_REGSHEET_ID_AUTO') || cfg_('TL_REGSHEET_ID','') || '',  // v1.29.0 FIX (xem chú thích trên): sheet id THẬT, KHÔNG Doc legacy
    manifestId: sp.getProperty('TL_MANIFEST_ID') || '',
    manifestName: CONFIG.MANIFEST_NAME,
    notebookVbqpplId: sp.getProperty('TL_NOTEBOOK_VBQPPL') || '743ed200-2e55-4673-b7a0-9bfd13b41ce6',
    categories: getCategories_(true)            // v2.6.0: map ĐỘNG khớp folder thật (không hardcode)
  };
  if(hasProfiles){
    obj.defaultProfile = (p && p.defaultProfile) || existing.defaultProfile || 'vbqppl';
    obj.profiles = profiles;
    obj.profilePolicy = 'writeconfig preserves/merges profiles; token rotation must not delete profile blocks';
  }
  return obj;
}
function privateConfigFile_(fileId){
  try { DriveApp.getFileById(fileId).setSharing(DriveApp.Access.PRIVATE, DriveApp.Permission.NONE); }
  catch(e){ Logger.log('[privateConfigFile_] khong revoke duoc sharing: ' + e); }
}
function doWriteConfig_(p){
  var obj=buildConfigObject_(p);
  var json=JSON.stringify(obj, null, 2);
  var sp=PropertiesService.getScriptProperties(), cid=sp.getProperty('TL_CONFIG_ID'), cfile=null;
  if(cid){ try{ cfile=DriveApp.getFileById(cid); }catch(e){ cfile=null; } }
  if(!cfile){
    var folder=DriveApp.getFolderById(rootId_());
    cfile=folder.createFile(CONFIG.CONFIG_NAME, json, 'application/json');
    sp.setProperty('TL_CONFIG_ID', cfile.getId());
  } else { cfile.setContent(json); }
  privateConfigFile_(cfile.getId());
  return {ok:true, configFileId:cfile.getId(), name:CONFIG.CONFIG_NAME,
          rootFolderId:rootId_(),
          driveFileId:cfile.getId(), configAccess:'private',
          note:'Config private (chua token) — doc qua Drive MCP/owner hoac dat TL_TOKEN bang env; KHONG tai headless.',
          config:obj};
}
function doReadConfig_(p){
  var sp=PropertiesService.getScriptProperties(), cid=sp.getProperty('TL_CONFIG_ID'), cfile=null;
  if(cid){ try{ cfile=DriveApp.getFileById(cid); }catch(e){ cfile=null; } }
  if(!cfile){
    // chưa mirror lần nào → tự dựng từ Script Property + CONFIG
    return {ok:true, mirrored:false, config:buildConfigObject_(p)};
  }
  var json=cfile.getBlob().getDataAsString('UTF-8');
  return {ok:true, mirrored:true, configFileId:cfile.getId(),
          updated:cfile.getLastUpdated().toISOString(),
          driveFileId:cfile.getId(), configAccess:'private',
          note:'Config private — doc qua Drive MCP/owner; KHONG tai headless.',
          config:JSON.parse(json)};
}

/* ============ BATCH ============ */
function doBatch_(p){
  var ops=(typeof p.ops==='string') ? JSON.parse(p.ops) : p.ops;
  if(!Array.isArray(ops)) throw new Error('ops phải là mảng');
  if(ops.length>30) throw new Error('batch: tối đa 30 ops/lần');
  var results=[], done=0, failed=0;
  ops.forEach(function(op,i){
    op=op||{};
    if(op.action==='batch'){
      results.push({i:i, action:'batch', ok:false, error:'không cho batch lồng batch'}); failed++; return;
    }
    try{ var r=dispatchAction_(op.action, op); var okFlag=(r && r.ok!==false);
      results.push({i:i, action:op.action, ok:okFlag, result:r}); okFlag?done++:failed++;
    }catch(e){ results.push({i:i, action:op.action, ok:false, error:String(e && e.message || e)}); failed++; }
  });
  return {ok:true, summary:{total:ops.length, done:done, failed:failed}, results:results};
}

/* ============ REGISTER / SHARE ============ */
function doRegister_(p){ registerRow_({id:p.fileId, name:p.name||'', mime:p.mime||'', sha256:p.sha256||''});
  return {ok:true, fileId:p.fileId, registered:true}; }
/* registerRow_ của base ĐÃ GỠ (KI-23) — bản v2.12 bên dưới định nghĩa lại,
   giữ nguyên chữ ký {id,name,mime,sha256} nhưng ghi vào SHEET registry. */
function doShare_(p){ shareView_(p.fileId); return {ok:true, fileId:p.fileId, shared:'ANYONE_WITH_LINK/VIEW'}; }

/* ============ HELPERS ============ */
function mergeParams_(e){
  var p={}; if(e && e.parameter) for(var k in e.parameter) p[k]=e.parameter[k];
  if(e && e.postData && e.postData.contents){ try{ var j=JSON.parse(e.postData.contents); for(var k2 in j) p[k2]=j[k2]; }catch(_){} }
  return p;
}
function jsonOut_(o){ return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function anyById_(id){ try{return DriveApp.getFileById(id);}catch(e){return DriveApp.getFolderById(id);} }
function registryRank_(o){
  var s = 0, cat = String(o.cat||''), st = String(o.nlm_status||'');
  if (o.nlm_source_id && st.indexOf('removed') !== 0) s += 1000;
  if (String(o.corpus)==='true' || /^\d{2}[_-]/.test(cat)) s += 300;
  if (o.sohieu || sohieuFromName_(o.name||'')) s += 200;
  if (stripVN_(String(o.hieuluc||'')).toLowerCase().indexOf('con hieu luc') >= 0) s += 100;
  if (cat && cat !== '(root)') s += 50;
  // VBHN-first (v2.21.2b): ban hop nhat thang ban goc/sua doi cung trang thai, ke ca CHUA push NLM
  var loai = String(o.loai||'').toUpperCase();
  if (loai === 'VBHN' || /VBHN/i.test(String(o.sohieu||'')) || /(^|[_-])VBHN([_-]|$)/i.test(String(o.name||''))) s += 150;
  // supersession: ban het hieu luc / bi thay the sink xuong (uu tien ban moi nhat)
  var hl = stripVN_(String(o.hieuluc||'')).toLowerCase();
  if (hl.indexOf('het hieu luc') >= 0 || hl.indexOf('thay the') >= 0) s -= 250;
  if (/^\d+_\d{4}_[A-Z]+_\d{5,}/.test(String(o.name||''))) s -= 200;
  if (cat === '(root)') s -= 100;
  if (!o.sohieu) s -= 40;
  return s;
}
function registryRankCompare_(a,b){ return registryRank_(b) - registryRank_(a); }
// v2.6.0: ưu tiên folderId tường minh; nếu có cat → resolve ĐỘNG (getCategories_); cuối cùng root.
function rootId_(){
  return PropertiesService.getScriptProperties().getProperty('TL_ROOT_ID') || CONFIG.ROOT_FOLDER_ID;
}
function resolveFolder_(p){
  if (p.folderId) return p.folderId;
  if (p.cat !== undefined && String(p.cat).trim() !== ''){
    var fid = resolveCatFolderId_(p.cat);
    if (!fid) throw new Error('resolveFolder_: khong resolve duoc cat "'+p.cat+'"');
    return fid;
  }
  if (p.toFolderId) return p.toFolderId;
  return rootId_();
}
function requireConfirm_(p){ if(String(p.confirm)!=='yes') throw new Error('Hành động phá hủy/nặng: cần confirm=yes'); }
function shareView_(id){ DriveApp.getFileById(id).setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW); }
function viewUrl_(id, mime){ return /document/.test(mime)?('https://docs.google.com/document/d/'+id+'/view'):('https://drive.google.com/file/d/'+id+'/view'); }

// Liệt kê con TRỰC TIẾP của 1 folder (phân trang đầy đủ)
function listChildren_(folderId){
  var out=[], token=null;
  do{
    var r=Drive.Files.list({q:"'"+folderId+"' in parents and trashed=false",
      fields:'nextPageToken,files(id,name,mimeType,size,md5Checksum,modifiedTime,appProperties)',
      pageSize:1000, supportsAllDrives:true, includeItemsFromAllDrives:true, pageToken:token});
    (r.files||[]).forEach(function(x){ out.push(x); });
    token=r.nextPageToken;
  }while(token);
  return out;
}
// Liệt kê toàn cây (đệ quy, dùng listChildren_) — cho verifyShares/dedup/list recursive
function listTree_(folderId){
  var out=[];
  (function rec(id){ listChildren_(id).forEach(function(x){
    out.push(x); if(x.mimeType==='application/vnd.google-apps.folder') rec(x.id); }); })(folderId);
  return out;
}

function sha256Hex_(bytes){ return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, bytes)
  .map(function(b){return ('0'+(b&0xff).toString(16)).slice(-2);}).join(''); }
function sha256HexStr_(s){ return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, s, Utilities.Charset.UTF_8)
  .map(function(b){return ('0'+(b&0xff).toString(16)).slice(-2);}).join(''); }
function smartConvert_(mime, size, p){
  if(typeof p.convert!=='undefined') return String(p.convert)==='true';
  if(/wordprocessingml|msword/i.test(mime)) return true;
  // v2.12.1 KI-26: PDF KHÔNG convert mặc định — Drive OCR nuốt trang scan không kêu
  // (vụ Điều 79 VBHN 89/VBHN-VPQH). Luồng đúng: giữ PDF gốc + pdftotext local + verify_deep,
  // đạt mới createtext. Convert PDF chỉ khi truyền convert=true TƯỜNG MINH.
  if(/pdf/i.test(mime)) return false;
  return false;
}
function inferMime_(name){
  var n=String(name).toLowerCase();
  if(/\.docx$/.test(n)) return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
  if(/\.doc$/.test(n))  return 'application/msword';
  if(/\.pdf$/.test(n))  return 'application/pdf';
  if(/\.txt$/.test(n))  return 'text/plain';
  if(/\.html?$/.test(n))return 'text/html';
  if(/\.csv$/.test(n))  return 'text/csv';
  if(/\.json$/.test(n)) return 'application/json';
  return 'application/octet-stream';
}
function provenance_(p, sha, url){
  return {sohieu:p.soHieu||p.sohieu||'', nam:p.nam||'', loai:p.loai||'', coquan:p.coquan||'',
          hieuluc:p.hieuLuc||p.hieuluc||'', sha256:sha||'', sourceUrl:url||'', ingestedAt:new Date().toISOString()};
}
function stampProps_(fileId, props){
  var clean={}; Object.keys(props).forEach(function(k){ if(props[k]!=null && props[k]!=='') clean[k]=String(props[k]); });
  Drive.Files.update({appProperties:clean}, fileId, null, {supportsAllDrives:true, fields:'id'});
}
function fetchBlob_(url, title){
  var r=UrlFetchApp.fetch(url, {muteHttpExceptions:true, followRedirects:true,
    headers:{'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept':'*/*'}});
  if(r.getResponseCode()>=400) throw new Error('Fetch '+r.getResponseCode()+': '+url+' (chặn UA/khu vực hoặc cần login → dùng Chrome)');
  var b=r.getBlob(); if(title) b.setName(title); return b;
}


/**
 * ====== PATCH v2.12.0 — SHEET REGISTRY / FIND / NLM-MAP / REGEN2 / MANIFEST-EXPORT ======
 * (HỢP NHẤT: chứa trọn v2.11 SEARCH/READ/DELTA/INBOX/META + tầng Sheet registry mới)
 * Mục tiêu: Apps Script THAY HẲN Google Drive MCP; Google Sheet làm SỔ CÁI SỐNG
 * (registry + mapping NLM source id ↔ Drive id); JSON manifest hạ vai thành
 * BẢN EXPORT SNAPSHOT giữ nguyên hợp đồng với skill tra-luat (registry.json:
 * entries[].nlm_source_id/name/gdoc_id — khớp _rows_from_registry của nlm_push.py).
 *
 * CÀI ĐẶT (bản FULL này): file đã TỰ ĐỦ — base v2.8.0 (registerRow_ cũ đã gỡ,
 * main_ đã nối đủ 20 case mới) + trọn khối v2.12. Chỉ việc:
 *   1. DÁN ĐÈ TOÀN BỘ nội dung file .gs trong project (xóa hết code cũ).
 *      KHÔNG dán file test_*.js vào project (chúng chạy bằng Node trên máy).
 *   2. (ĐÃ LÀM SẴN trong main_ của file này — liệt kê để đối chiếu):
 *        // --- v2.11 ---
 *        case 'search':       return doSearch_(p);
 *        case 'read':         return doRead_(p);
 *        case 'perm_list':    return doPermList_(p);
 *        case 'changes_init': return doChangesInit_(p);
 *        case 'changes_pull': return doChangesPull_(p);
 *        case 'meta_set':     return doMetaSet_(p);
 *        case 'meta_find':    return doMetaFind_(p);
 *        case 'shortcut':     return doShortcut_(p);
 *        case 'inbox_process':return doInboxProcess_(p);
 *        case 'inbox_status': return doInboxStatus_(p);
 *        case 'perf':         return doPerf_(p);
 *        case 'config':       return doConfigView_(p);
 *        // --- v2.12 ---
 *        case 'find':         return doFind_(p);
 *        case 'reg_get':      return doRegGet_(p);
 *        case 'reg_upsert':   return doRegUpsert_(p);
 *        case 'map_set':      return doMapSet_(p);
 *        case 'map_unpushed': return doMapUnpushed_(p);
 *        case 'map_mark_stale': return doMapMarkStale_(p);
 *        case 'regen2':       return doRegen2_(p);
 *        case 'manifest_export': return doManifestExport_(p);
 *   4. Chạy _selftest_v212() trong editor 1 lần (tạo Sheet registry + kiểm môi trường).
 *   5. Deploy lại web app (Manage > Edit > New version).
 *   6. Chạy 1 lần: action=regen2&confirm=yes rồi action=manifest_export
 *      (di trú từ registry cũ sang Sheet; treeHash đổi thuật toán — xem KI-22).
 *
 * PHỤ THUỘC từ base v2.9 (không định nghĩa lại ở đây):
 *   rootId_(), main_(), resolveCatFolderId_(), shareView_(),
 *   stampProps_(), provenance_(). registerRow_ bị THAY (xóa bản cũ — KI-23).
 *   Advanced Service "Drive API" (v3) phải đang bật.
 *
 * CONFIG — tất cả qua Script Properties, bỏ trống = dùng default:
 *   (v2.11 — giữ nguyên)
 *   TL_INBOX_NAME='_INBOX'  TL_INBOX_TIME_MS=270000  TL_INBOX_MIN_TEXT=200
 *   TL_INBOX_HEAD_CHARS=3000  TL_INBOX_DEDUP='true'  TL_INBOX_ALLOW_NONUM='false'
 *   TL_DOCTYPES_EXTRA='[]'  TL_QUARANTINE_CAT='QUARANTINE'
 *   TL_READ_LIMIT_DEFAULT=60000  TL_READ_LIMIT_MAX=200000
 *   TL_SEARCH_FIELDS  TL_SEARCH_PAGESIZE=100  TL_CHANGES_PAGESIZE=500
 *   TL_MANIFEST_ID=''  TL_MANIFEST_NAME='tra_luat_manifest.json'
 *   TL_USE_BATCH='false'  TL_SELFTEST_DOC_ID=''
 *   (v2.12 — mới)
 *   TL_REGSHEET_ID=''                — ID spreadsheet registry; trống → tìm/tạo theo tên
 *   TL_REGSHEET_NAME='tra_luat_registry'
 *   TL_REG_CACHE_TTL=600             — giây cache index registry trong CacheService
 *   TL_FIND_MAX=10                   — số kết quả tối đa của action find
 *
 * ============================ KNOWN ISSUES & FIX ============================
 * (đúc kết vận hành v2.0→v2.12 — ĐỌC TRƯỚC KHI DEBUG)
 *
 * KI-01 Client POST: /exec luôn 302 về script.googleusercontent.com.
 *       `curl -X POST -L` re-POST vào URL echo → "Page Not Found".
 *       FIX: urllib (Python) / tl_post_json (POST không follow → GET vào Location);
 *       GET nhẹ dùng `curl -sL` bình thường.
 * KI-02 Response > ~50KB qua browser tab: get_page_text fail im lặng.
 *       FIX: action `read` có offset/limit; hoặc JSON.parse(document.body.innerText).
 * KI-03 Drive export trần 10MB/file; bảng trong GDoc bị ép phẳng khi export text.
 * KI-04 `'folderId' in parents` KHÔNG đệ quy. FIX: scope='corpus' OR 2 cấp đã cache.
 * KI-05 Drive bỏ multi-parent (2020). FIX: folder primary + action `shortcut`
 *       + appProperties.linhvuc2.
 * KI-06 appProperties ~30 cặp/app, key+value ≤124 byte. FIX: metaSet_ tự cắt + báo.
 * KI-07 changes pageToken hết hạn (404/410). FIX: tự re-init + tokenReset:true
 *       + khuyến nghị regen2 đối soát.
 * KI-08 Hard-kill 6': GDoc convert mồ côi → xử lý trùng. FIX: dedup md5 manifest
 *       + collision-check tên ở cat đích.
 * KI-09 dryRun PDF detect từ tên file → fail giả. FIX: peek='true' convert tạm.
 * KI-10 GDoc KHÔNG có md5 — dedup md5 chỉ bắt file nhị phân; GDoc trùng do
 *       collision-check tên lo.
 * KI-11 DocumentApp.openById chậm (~1–2s + lock). FIX: UrlFetch export (đo: action perf).
 * KI-12 Cache corpusFolders_/registry TTL 10' → tạo cat/sửa tay Sheet xong gọi
 *       kèm refresh='true'.
 * KI-13 UrlFetch quota ~20k/ngày (consumer): export + batch ăn quota này.
 * KI-14 treeHash: delta KHÔNG tính lại được toàn vẹn → manifest gắn treeHashStale;
 *       regen2 định kỳ để đối soát.
 * KI-15 Số hiệu Đ→D trong tên file (ND-CP, BCD) — nhất quán convention.
 * KI-16 SHEETS ÉP KIỂU DỮ LIỆU — bẫy nặng nhất của registry Sheet: '05/2026'
 *       thành NGÀY, '06' thành số 6 mất số 0. FIX: setNumberFormat('@') (plain
 *       text) TOÀN VÙNG ngay khi tạo tab + sau mỗi lần swap (regWriteAll_ lo).
 * KI-17 regen ghi Sheet = clear + setValues hai bước, kill giữa chừng → sheet
 *       rỗng. FIX: ghi vào tab tạm 'files_tmp' → xóa tab cũ → đổi tên (swap).
 * KI-18 Webapp chạy đồng thời 2 request ghi → đè dữ liệu. FIX: LockService
 *       tryLock(30s) quanh MỌI thao tác ghi Sheet; bận → trả {error:'busy'}.
 * KI-19 CacheService trần 100KB/key. FIX: index registry nén cột tối thiểu,
 *       vượt → chunk 2 key (reg_0/reg_1).
 * KI-20 appendRow từng dòng RẤT chậm (~200ms/dòng). FIX: mọi ghi nhiều dòng
 *       dùng batch setValues một call.
 * KI-21 NGUY HIỂM NHẤT: regen2 quét Drive KHÔNG ĐƯỢC phá cột nlm_* (Drive không
 *       biết NLM). FIX: regenMerge_ giữ nlm_source_id/nlm_status/nlm_pushed_at/
 *       verified/note theo drive_id; file biến mất → đánh dấu nlm_status=
 *       'removed_from_drive' GIỮ DÒNG (source NLM vẫn tồn tại, người quyết xóa).
 * KI-22 treeHash v2 (FNV-1a trên id:md5:modifiedTime) KHÁC thuật toán regen cũ
 *       → lần đầu chạy regen2, skill thấy treeHash đổi và coi cache stale MỘT
 *       lần — vô hại, tự làm tươi.
 * KI-23 registerRow_ bị định nghĩa lại: Apps Script lấy bản parse SAU CÙNG khi
 *       trùng tên hàm — hành vi không nên dựa vào. PHẢI XÓA bản registerRow_
 *       của base khi dán v2.12.
 * KI-24 Ghi Sheet xong đọc lại NGAY trong cùng execution có thể thấy dữ liệu cũ.
 *       FIX: SpreadsheetApp.flush() sau ghi, trước đọc.
 * ===========================================================================
 */

/* ------------------------- 0) CONFIG LOADER ------------------------- */

var V211_ = { props: null, corpus: null, doctypes: null, manSetMd5: null };

function props_(){
  if (V211_.props === null)
    V211_.props = PropertiesService.getScriptProperties().getProperties() || {};
  return V211_.props;
}
function cfg_(k, d){ var v = props_()[k]; return (v === undefined || v === null || v === '') ? d : v; }
function cfgNum_(k, d){ var v = cfg_(k, null); return v === null ? d : Number(v); }
function cfgBool_(k, d){ var v = cfg_(k, null); return v === null ? d : String(v) === 'true'; }
function cfgJson_(k, d){ var v = cfg_(k, null); if (v === null) return d;
  try { return JSON.parse(v); } catch(e){ return d; } }
function _resetCfgCache_(){ V211_ = { props:null, corpus:null, doctypes:null, manSetMd5:null }; }

function cfgSearchFields_(){
  return cfg_('TL_SEARCH_FIELDS',
    'id,name,mimeType,size,md5Checksum,modifiedTime,parents,appProperties');
}

/** action=config — xem config hiệu lực (không lộ token). */
function doConfigView_(p){
  var keys = ['TL_INBOX_NAME','TL_INBOX_TIME_MS','TL_INBOX_MIN_TEXT','TL_INBOX_HEAD_CHARS',
    'TL_INBOX_DEDUP','TL_INBOX_ALLOW_NONUM','TL_DOCTYPES_EXTRA','TL_QUARANTINE_CAT',
    'TL_READ_LIMIT_DEFAULT','TL_READ_LIMIT_MAX','TL_SEARCH_FIELDS','TL_SEARCH_PAGESIZE',
    'TL_CHANGES_PAGESIZE','TL_MANIFEST_ID','TL_MANIFEST_NAME','TL_USE_BATCH','TL_SELFTEST_DOC_ID'];
  var eff = {}, raw = props_();
  keys.forEach(function(k){ eff[k] = { set: raw[k] !== undefined, value: raw[k] !== undefined ? raw[k] : '(default)' }; });
  return { ok:true, version:APP_VERSION, config:eff, rootFolderId: rootId_() };
}

/* ------------------------- 1) PURE UTILS (test offline được) ------------------------- */

function stripVN_(s){
  return String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'')
    .replace(/đ/g,'d').replace(/Đ/g,'D');
}

/** Escape giá trị chuỗi đưa vào q của files.list (KI: ' và \ phá query). */
function qEsc_(s){ return String(s||'').replace(/\\/g,'\\\\').replace(/'/g,"\\'"); }

/** Cắt lát text cho action read. Pure để test. */
function readSlice_(text, offset, limit, dflt, hardMax){
  var t = String(text||''), off = Math.max(0, Number(offset)||0);
  var lim = Number(limit)||dflt; lim = Math.max(1, Math.min(lim, hardMax));
  var chunk = t.slice(off, off+lim);
  return { total:t.length, offset:off, returned:chunk.length,
           more: off + chunk.length < t.length, text:chunk };
}

function stripBom_(s){ return String(s||'').replace(/^\uFEFF/, ''); }

/* ------------------------- 2) SEARCH / READ / PERMISSIONS ------------------------- */

/**
 * GET/POST { action:'search', q?, cat?, scope?:'corpus', fields?, orderBy?,
 *            pageSize?, pageToken?, includeFolders?, refresh? }
 * - q: chuỗi query files.list nguyên bản (name contains, fullText contains,
 *   appProperties has {...}, modifiedTime > ...). Xem KI-04 về parents.
 * - cat: giới hạn con TRỰC TIẾP của 1 cat (resolveCatFolderId_).
 * - scope='corpus': OR toàn bộ folder corpus 2 cấp (thay tìm đệ quy).
 * - Mặc định chỉ trả FILE khi dùng cat/scope; includeFolders='true' để thấy folder.
 * Đây là action thay thế phần search của Drive MCP.
 */
/* (đã gỡ định nghĩa doSearch_ cũ trùng — dùng bản registry ở trên, v2.17.0) */

/** Chỉ cho ký tự hợp lệ trong fields — chặn injection vào URL API. */
function sanitizeFields_(f){ return String(f).replace(/[^a-zA-Z0-9_,()\/ ]/g,''); }

/**
 * GET/POST { action:'read', id, offset?, limit?, mime? }
 * Đọc nội dung text 1 file theo lát cắt (KI-02). Google Docs/Slides → export
 * text/plain; Sheets → text/csv; file text thường → đọc thẳng blob.
 * PDF/DOCX chưa convert → trả lỗi kèm hướng dẫn (convert qua inbox/copy_convert).
 */
function doRead_(p){
  if (!p.id) return { ok:false, error:'Thiếu id' };
  var meta = Drive.Files.get(p.id, { fields:'id,name,mimeType,size', supportsAllDrives:true });
  var text, mt = meta.mimeType || '';
  var exportMap = {
    'application/vnd.google-apps.document':     'text/plain',
    'application/vnd.google-apps.presentation': 'text/plain',
    'application/vnd.google-apps.spreadsheet':  'text/csv'
  };
  if (exportMap[mt]) text = exportText_(p.id, p.mime || exportMap[mt]);
  else if (/^text\/|json|xml|csv/.test(mt))
    text = DriveApp.getFileById(p.id).getBlob().getDataAsString('UTF-8');
  else return { ok:false, error:'MIME ' + mt + ' không đọc text trực tiếp được — convert sang Google Doc trước (inbox_process / copy_convert).', mime:mt };
  var s = readSlice_(stripBom_(text), p.offset, p.limit,
                     cfgNum_('TL_READ_LIMIT_DEFAULT',60000), cfgNum_('TL_READ_LIMIT_MAX',200000));
  return { ok:true, id:meta.id, name:meta.name, mime:mt,
           total:s.total, offset:s.offset, returned:s.returned, more:s.more, text:s.text };
}

/** Export nhanh qua REST (KI-11: nhanh hơn DocumentApp; KI-03: trần 10MB). */
function exportText_(id, mime){
  return exportBlob_(id, mime || 'text/plain').getDataAsString('UTF-8');
}

/** GET/POST { action:'perm_list', id } — thay permissions của Drive MCP. */
function doPermList_(p){
  if (!p.id) return { ok:false, error:'Thiếu id' };
  var res = Drive.Permissions.list(p.id, {
    fields: 'permissions(id,type,role,emailAddress,domain,allowFileDiscovery)',
    supportsAllDrives: true });
  return { ok:true, id:p.id, permissions: res.permissions || [] };
}

/* ------------------------- 3) META (appProperties) + SHORTCUT ------------------------- */

/** Schema khóa metadata chuẩn của corpus — chiều phân loại KHÔNG nằm ở thư mục. */
var META_KEYS_ = ['loai','sohieu','linhvuc','linhvuc2','goc','hieuluc','vbhn'];

/**
 * POST { action:'meta_set', id, loai?, sohieu?, linhvuc?, linhvuc2?, goc?,
 *        hieuluc?, vbhn?, extra? (JSON) }
 * Ghi appProperties. KI-06: tự cắt 124 byte/cặp, báo truncated.
 */
function doMetaSet_(p){
  if (!p.id) return { ok:false, error:'Thiếu id' };
  var ap = {}, truncated = [];
  var extra = (typeof p.extra === 'string') ? cfgJsonStr_(p.extra) : (p.extra || {});
  META_KEYS_.forEach(function(k){ if (p[k] !== undefined && p[k] !== '') ap[k] = String(p[k]); });
  Object.keys(extra||{}).forEach(function(k){ ap[k] = String(extra[k]); });
  Object.keys(ap).forEach(function(k){
    // 124 byte cho key+value (UTF-8). Cắt thô theo byte-length ước lượng.
    var budget = 124 - byteLen_(k);
    while (byteLen_(ap[k]) > budget) ap[k] = ap[k].slice(0, ap[k].length - 1);
    if (String(p[k]||extra[k]||'') !== ap[k]) truncated.push(k);
  });
  Drive.Files.update({ appProperties: ap }, p.id, null, { supportsAllDrives:true });
  return { ok:true, id:p.id, appProperties:ap, truncated:truncated };
}
function byteLen_(s){ return unescape(encodeURIComponent(String(s||''))).length; }
function cfgJsonStr_(s){ try { return JSON.parse(s); } catch(e){ return {}; } }

/**
 * GET/POST { action:'meta_find', key?, value?, goc? }
 * - key+value: appProperties has { key='k' and value='v' }
 * - goc='134-2025-QH15': trả CỤM văn bản — luật gốc (sohieu=goc) + mọi văn bản
 *   hướng dẫn (goc=goc). Phục vụ rà soát theo cụm (HD06).
 */
function doMetaFind_(p){
  var q;
  if (p.goc){
    var g = qEsc_(p.goc);
    q = "(appProperties has { key='sohieu' and value='" + g + "' } or " +
        "appProperties has { key='goc' and value='" + g + "' })";
  } else if (p.key && p.value !== undefined){
    q = "appProperties has { key='" + qEsc_(p.key) + "' and value='" + qEsc_(p.value) + "' }";
  } else return { ok:false, error:'Cần (key,value) hoặc goc' };
  return driveSearch_({ q:q, scope:p.scope||'corpus', fields:p.fields, pageSize:p.pageSize, pageToken:p.pageToken });
}

/**
 * POST { action:'shortcut', id, cat } — tạo shortcut của file sang cat phụ
 * (KI-05: thay multi-parent cho văn bản đa lĩnh vực).
 */
function doShortcut_(p){
  if (!p.id || !p.cat) return { ok:false, error:'Thiếu id hoặc cat' };
  var cid = resolveCatFolderId_(p.cat);
  if (!cid) return { ok:false, error:'Không thấy cat: ' + p.cat };
  var src = Drive.Files.get(p.id, { fields:'id,name', supportsAllDrives:true });
  var sc = Drive.Files.create({
    name: src.name, mimeType: 'application/vnd.google-apps.shortcut',
    parents: [cid], shortcutDetails: { targetId: p.id }
  }, null, { supportsAllDrives:true, fields:'id,name,parents' });
  return { ok:true, shortcutId: sc.id, target: p.id, cat: p.cat };
}

/* ------------------------- 4) CORPUS FOLDER MAP + DELTA MANIFEST ------------------------- */

/**
 * Map folder corpus 2 cấp: { ids:[...], nameById:{id:'05_Lao_dong' | '05_Lao_dong/BHXH'} }
 * Cache 10' (KI-12) — gọi với force=true sau khi tạo cat mới.
 */
function corpusFolders_(force){
  if (!force && V211_.corpus) return V211_.corpus;
  var cache = CacheService.getScriptCache(), CK = 'tl211_corpus';
  if (!force){
    var hit = cache.get(CK);
    if (hit){ V211_.corpus = JSON.parse(hit); return V211_.corpus; }
  }
  var root = rootId_();
  var out = { ids:[root], nameById:{} }; out.nameById[root] = '(root)';
  var FQ = "mimeType='application/vnd.google-apps.folder' and trashed=false";
  var l1 = Drive.Files.list({ q:"'"+root+"' in parents and "+FQ, pageSize:1000,
    fields:'files(id,name)', supportsAllDrives:true, includeItemsFromAllDrives:true }).files || [];
  l1.forEach(function(f){ out.ids.push(f.id); out.nameById[f.id] = f.name; });
  // Cấp 2: KI-27 — per-parent (OR-multi-parent trả snapshot cũ với item vừa move)
  for (var i = 0; i < l1.length; i++){
    var qq = "'" + l1[i].id + "' in parents and " + FQ;
    var l2 = Drive.Files.list({ q:qq, pageSize:1000, fields:'files(id,name,parents)',
      supportsAllDrives:true, includeItemsFromAllDrives:true }).files || [];
    l2.forEach(function(f){
      var pn = out.nameById[(f.parents||[])[0]] || '?';
      out.ids.push(f.id); out.nameById[f.id] = pn + '/' + f.name;
    });
  }
  V211_.corpus = out;
  try { cache.put(CK, JSON.stringify(out), 600); } catch(e){} // >100KB thì bỏ cache, không sao
  return out;
}

/** POST { action:'changes_init' } — lấy startPageToken, bắt đầu theo dõi delta. */
function doChangesInit_(p){
  var tok = Drive.Changes.getStartPageToken({ supportsAllDrives:true }).startPageToken;
  PropertiesService.getScriptProperties().setProperty('TL_CHANGES_TOKEN', tok);
  V211_.props = null;
  return { ok:true, startPageToken: tok,
           note:'Từ giờ dùng changes_pull thay regen full (regen chỉ để đối soát định kỳ — KI-14).' };
}

/**
 * POST { action:'changes_pull', apply?:'true', refresh? }
 * Hỏi Drive "có gì đổi từ token trước" → lọc trong phạm vi corpus → phân loại
 * added/updated/removed/moved_out → (tùy chọn) vá thẳng vào manifest.
 * Thay regen full-tree-walk 30–60s bằng call <~1–3s. KI-07, KI-14.
 */
function doChangesPull_(p){
  var sp = PropertiesService.getScriptProperties();
  var tok = sp.getProperty('TL_CHANGES_TOKEN');
  if (!tok) return { ok:false, error:'Chưa có token — chạy changes_init trước.' };
  var corpus = corpusFolders_(String(p.refresh)==='true');
  var inCorpus = {}; corpus.ids.forEach(function(id){ inCorpus[id] = true; });

  var man = null, manId = null, manIds = {};
  var wantApply = String(p.apply) === 'true';
  var located = locateManifest_();
  if (located){ manId = located.id; man = located.obj; manifestIndexIds_(man, manIds); }
  // v2.12: "đã biết" = manifest JSON ∪ SHEET registry (Sheet là nguồn chân lý mới —
  // không gộp thì delta `removed` của file chỉ có trong Sheet bị vứt oan).
  try { regReadAll_(false).forEach(function(o){ manIds[o.drive_id] = true; }); } catch(e){}

  var deltas = [], pages = 0, tokenReset = false, t0 = Date.now();
  var pageSize = cfgNum_('TL_CHANGES_PAGESIZE', 500);
  try {
    while (tok){
      var res = Drive.Changes.list(tok, {
        pageSize: pageSize, includeRemoved: true,
        fields: 'nextPageToken,newStartPageToken,changes(fileId,removed,file(id,name,mimeType,md5Checksum,modifiedTime,trashed,parents,appProperties))',
        supportsAllDrives: true, includeItemsFromAllDrives: true });
      (res.changes || []).forEach(function(c){
        var id = c.fileId, f = c.file || null;
        var known = !!manIds[id];
        if (c.removed || (f && f.trashed)){
          if (known) deltas.push({ kind:'removed', id:id });
          return;
        }
        if (!f) return;
        var par = (f.parents || [])[0];
        var inside = par && inCorpus[par];
        if (inside && f.mimeType === 'application/vnd.google-apps.folder'){
          deltas.push({ kind:'folder_changed', id:id, file:pickF_(f) }); return; // cấu trúc đổi → nên refresh cache
        }
        if (inside) deltas.push({ kind: known ? 'updated' : 'added', id:id, file:pickF_(f) });
        else if (known) deltas.push({ kind:'moved_out', id:id, file:pickF_(f) });
      });
      pages++;
      if (res.newStartPageToken){ tok = null; sp.setProperty('TL_CHANGES_TOKEN', res.newStartPageToken); }
      else { tok = res.nextPageToken;
             // Lưu token trung gian: nếu bị kill giữa chừng, lần sau pull tiếp từ đây
             if (tok) sp.setProperty('TL_CHANGES_TOKEN', tok); }
      if (Date.now() - t0 > 4 * 60 * 1000) break; // an toàn trần 6'
    }
  } catch(e){
    var msg = String(e && e.message || e);
    if (/40[34]|410|invalid|expired/i.test(msg)){ // KI-07
      var nt = Drive.Changes.getStartPageToken({ supportsAllDrives:true }).startPageToken;
      sp.setProperty('TL_CHANGES_TOKEN', nt); tokenReset = true;
    } else throw e;
  }
  V211_.props = null;

  var applied = null;
  if (wantApply && man && deltas.length){
    applied = manifestMerge_(man, deltas, corpus.nameById);
    if (applied.applied > 0 && !applied.unknownSchema) saveManifest_(manId, man, located.name);
  }
  // v2.12: vá thẳng SHEET registry (mặc định BẬT — applySheet='false' để tắt).
  // md5/modifiedTime đổi trên file đã push NLM → nlm_status='stale' (KI-21 hook).
  var sheetApplied = null;
  if (String(p.applySheet) !== 'false' && deltas.length){
    try { sheetApplied = regApplyDeltas_(deltas, corpus.nameById); }
    catch(e){ sheetApplied = { error: String(e && e.message || e) }; }
  }
  return { ok:true, pages:pages, deltas:deltas, count:deltas.length,
           applied:applied, sheetApplied:sheetApplied, tokenReset:tokenReset,
           note: tokenReset ? 'Token hết hạn → đã re-init. CHẠY regen2 để đối soát toàn cây.' : null,
           elapsedMs: Date.now() - t0 };
}

function pickF_(f){ return { name:f.name, mimeType:f.mimeType, md5Checksum:f.md5Checksum||null,
  modifiedTime:f.modifiedTime, parent:(f.parents||[])[0]||null }; }

/** Tìm manifest theo TL_MANIFEST_ID, fallback tìm tên trong ROOT. */
function locateManifest_(){
  var id = cfg_('TL_MANIFEST_ID','');
  if (!id){
    var nm = cfg_('TL_MANIFEST_NAME','tra_luat_manifest.json');
    var r = Drive.Files.list({ q:"name='"+qEsc_(nm)+"' and '"+rootId_()+
      "' in parents and trashed=false", pageSize:1, fields:'files(id,name)',
      supportsAllDrives:true, includeItemsFromAllDrives:true }).files || [];
    if (!r.length) return null;
    id = r[0].id;
  }
  try {
    var txt = DriveApp.getFileById(id).getBlob().getDataAsString('UTF-8');
    return { id:id, obj: JSON.parse(stripBom_(txt)), name: DriveApp.getFileById(id).getName() };
  } catch(e){ return null; }
}

/** Index id manifest — hỗ trợ schema mới entries[] và schema cũ files. */
function manifestIndexIds_(man, out){
  if (!man) return;
  var rows = man.entries || man.files;
  if (!rows) return;
  if (Array.isArray(rows)) rows.forEach(function(e){
    var id = e && (e.id || e.drive_id || e.gdoc_id);
    if (id) out[id] = true;
  });
  else if (typeof rows === 'object') Object.keys(rows).forEach(function(k){ out[k] = true; });
}

/**
 * PURE — vá deltas vào manifest. Trả {applied,added,updated,removed,unknownSchema}.
 * Không biết treeHash tính thế nào → chỉ đánh dấu treeHashStale (KI-14).
 */
function manifestMerge_(man, deltas, nameById){
  var r = { applied:0, added:0, updated:0, removed:0, unknownSchema:false };
  var key = man.entries ? 'entries' : 'files';
  var rows = man[key];
  var isArr = Array.isArray(rows);
  var isMap = !isArr && rows && typeof rows === 'object';
  if (!isArr && !isMap){ r.unknownSchema = true; return r; }

  function entryOf_(d){
    var f = d.file || {};
    return { id:d.id, gdoc_id:d.id, name:f.name, mime:f.mimeType, md5:f.md5Checksum||'',
             modified_time:f.modifiedTime || '', cat: nameById[f.parent] || '' };
  }
  function upsertArr_(d){
    for (var i=0;i<rows.length;i++) if (rows[i] && (rows[i].id === d.id || rows[i].drive_id === d.id || rows[i].gdoc_id === d.id)){
      var e = rows[i], n = entryOf_(d);
      Object.keys(n).forEach(function(k){ if (n[k] !== null && n[k] !== undefined) e[k] = n[k]; });
      r.updated++; return;
    }
    rows.push(entryOf_(d)); r.added++;
  }
  function removeArr_(id){
    for (var i=rows.length-1;i>=0;i--) if (rows[i] && (rows[i].id === id || rows[i].drive_id === id || rows[i].gdoc_id === id)){
      rows.splice(i,1); r.removed++; }
  }
  deltas.forEach(function(d){
    if (d.kind === 'folder_changed') return;
    if (d.kind === 'removed' || d.kind === 'moved_out'){
      if (isArr) removeArr_(d.id);
      else if (rows[d.id] !== undefined){ delete rows[d.id]; r.removed++; }
    } else { // added | updated
      if (isArr) upsertArr_(d);
      else {
        var existed = rows[d.id] !== undefined;
        var cur = existed ? rows[d.id] : {};
        var n = entryOf_(d);
        Object.keys(n).forEach(function(k){ if (n[k] !== null && n[k] !== undefined) cur[k] = n[k]; });
        rows[d.id] = cur;
        existed ? r.updated++ : r.added++;
      }
    }
  });
  r.applied = r.added + r.updated + r.removed;
  if (r.applied > 0){
    man.treeHashStale = true;                       // KI-14
    man.deltaSeq = (Number(man.deltaSeq)||0) + 1;
    man.lastDelta = new Date().toISOString();
  }
  return r;
}

function saveManifest_(id, obj, name){
  var blob = Utilities.newBlob(JSON.stringify(obj, null, 1), 'application/json',
                               name || cfg_('TL_MANIFEST_NAME','tra_luat_manifest.json'));
  Drive.Files.update({}, id, blob, { supportsAllDrives:true });
}

/* ------------------------- 5) INBOX PIPELINE v2 (thay trọn khối v2.10) ------------------------- */

function doctypes_(){
  if (V211_.doctypes) return V211_.doctypes;
  var base = [
    ['VĂN BẢN HỢP NHẤT','VBHN'], ['BỘ LUẬT','BLuat'],  ['PHÁP LỆNH','PL'],
    ['NGHỊ ĐỊNH','ND'],          ['NGHỊ QUYẾT','NQ'],  ['THÔNG TƯ','TT'],
    ['QUYẾT ĐỊNH','QD'],         ['KẾT LUẬN','KL'],    ['CHỈ THỊ','CT'],
    ['HƯỚNG DẪN','HD'],          ['CÔNG ĐIỆN','CD'],   ['CÔNG ƯỚC','DUQT'],
    ['HIỆP ĐỊNH','DUQT'],        ['LUẬT','Luat']
  ];
  V211_.doctypes = base.concat(cfgJson_('TL_DOCTYPES_EXTRA', []));
  return V211_.doctypes;
}

function inboxFolderId_(){
  // v2.18.0: ưu tiên _HOP_NAP staging chuẩn (đồng bộ doBootstrap_)
  var sp = PropertiesService.getScriptProperties();
  var pinned = sp.getProperty('TL_INBOX_ID');                       // tôn trọng pin tay nếu còn sống
  if (pinned){ try { if (!DriveApp.getFolderById(pinned).isTrashed()) return pinned; } catch(e){} }
  var HOPNAP = '1bNSAKGACtk0x0cqX5QRVEGT12udi2g67';                 // id _HOP_NAP cứng (cùng doBootstrap_ tạo)
  try { if (!DriveApp.getFolderById(HOPNAP).isTrashed()) return HOPNAP; } catch(e){}
  // fallback: tìm/tạo _HOP_NAP trong ROOT (codebase này KHÔNG có findChildFolderByName_/rootFolderId_)
  var root = DriveApp.getFolderById(rootId_());
  var it = root.getFoldersByName('_HOP_NAP');
  var f = it.hasNext() ? it.next() : root.createFolder('_HOP_NAP');
  sp.setProperty('TL_INBOX_ID', f.getId());
  return f.getId();
}

/** List inbox bằng API riêng (không dùng listChildren_) để lấy md5Checksum (KI-08/KI-10). */
function inboxList_(fid){
  var out = [], tok = null;
  do {
    var r = Drive.Files.list({ q:"'"+fid+"' in parents and trashed=false", pageSize:1000,
      fields:'nextPageToken,files(id,name,mimeType,size,md5Checksum)',
      pageToken: tok || undefined, supportsAllDrives:true, includeItemsFromAllDrives:true });
    out = out.concat(r.files || []); tok = r.nextPageToken;
  } while (tok);
  return out;
}

/**
 * PURE — vị trí xuất hiện đầu tiên của tên loại văn bản, BỎ QUA occurrence
 * thuộc dòng số hiệu ("Luật số: 45/2019/QH14" đứng TRƯỚC dòng "BỘ LUẬT" →
 * v2.10 nhận nhầm type=Luat cho Bộ luật. Test: detect Bộ luật).
 */
function findTypePos_(headUp, wordUp){
  var p = -1;
  while (true){
    p = headUp.indexOf(wordUp, p + 1);
    if (p < 0) return -1;
    // KHÔNG dùng \b: JS \b chỉ hiểu ASCII, sau 'Ố' (non-word) \b fail im lặng.
    if (!/^\s*SỐ(?![A-ZĐÀ-Ỹ0-9])/.test(headUp.slice(p + wordUp.length))) return p;
  }
}

/**
 * PURE — Detect {type, number, shortName} từ đoạn đầu văn bản.
 * v2.11: (a) số hiệu chứa VBHN → ép type='VBHN' (header VBHN thường mở bằng
 * "BỘ LUẬT..." gây nhận nhầm); (b) bỏ qua occurrence "LOẠI + SỐ:" khi dò loại
 * và khi dò dòng tiêu đề (sửa 2 bug v2.10: type nhầm Luat cho Bộ luật,
 * shortName ra 'LUAT'); (c) ghép tối đa 2 dòng tiêu đề ngắn
 * ("LUẬT"\n"DÂN SỐ" → DAN_SO).
 */
function inboxDetect_(headText){
  var t = String(headText||''), up = t.toUpperCase();
  var r = { type:null, number:null, shortName:null };
  var DT = doctypes_();
  var head = up.slice(0,1500), bestPos = 1e9, typeVN = null;
  DT.forEach(function(d){
    var p = findTypePos_(head, d[0]);
    if (p >= 0 && p < bestPos){ bestPos = p; r.type = d[1]; typeVN = d[0]; }
  });
  var m = t.match(/(?:[Ss]ố\s*[:.]?\s*)(\d{1,4}\/\d{4}\/[A-ZĐ][\w\u00C0-\u1EF9-]*)/) ||
          t.match(/(\d{1,4}\/\d{4}\/(?:QH\d+|N[ĐD]-CP|TT-[A-ZĐ]+|NQ-[A-ZĐ\d]+|Q[ĐD]-[A-ZĐ]+|UBTVQH\d+))/) ||
          t.match(/(?:[Ss]ố\s*[:.]?\s*)(\d{1,4}\/[A-ZĐ]{2,6}-[A-ZĐ\d]{2,10})/) ||
          t.match(/(\d{1,4}\/VBHN-[A-ZĐ]+)/);
  if (m) r.number = m[1].replace(/\//g,'-').replace(/Đ/g,'D');         // KI-15
  if (r.number && /VBHN/.test(r.number)) r.type = 'VBHN';
  if (typeVN){
    var typeWordsUp = DT.map(function(d){ return d[0]; });
    var lines = t.split(/\r?\n/).map(function(x){ return x.trim(); }).filter(String);
    for (var i=0;i<lines.length;i++){
      var LU = lines[i].toUpperCase();
      if (LU.indexOf(typeVN) !== 0) continue;
      if (/SỐ\s*[:.]/.test(LU)) continue;            // "Luật số: ..." không phải dòng tiêu đề
      var got = [];
      for (var j=i+1; j<Math.min(i+5,lines.length) && got.length<2; j++){
        var cand = lines[j], CU = cand.toUpperCase();
        if (/^Căn cứ/i.test(cand)) break;
        if (typeWordsUp.indexOf(CU) >= 0) continue;  // dòng là tên loại khác → bỏ
        if (!/^[A-ZĐÀ-Ỹ0-9\s,.'()–-]{3,80}$/.test(cand)) break;
        got.push(cand);
        if (cand.length >= 16) break;                // tiêu đề dài 1 dòng là đủ
      }
      if (got.length){
        r.shortName = stripVN_(got.join(' ')).replace(/[^\w\s-]/g,'').trim()
          .replace(/\s+/g,'_').slice(0,48);
        break;
      }
    }
  }
  return r;
}

/** PURE — tên chuẩn; cho phép thiếu số hiệu khi allowNoNum (Công ước/ĐUQT). */
function inboxStdName_(d, allowNoNum){
  if (d.number) return d.type + '_' + d.number + (d.shortName ? '_' + d.shortName : '');
  if (allowNoNum && d.type && d.shortName) return d.type + '_KhongSo_' + d.shortName;
  return null;
}

/** GET/POST { action:'inbox_status' } */
function doInboxStatus_(p){
  var fid = inboxFolderId_(), items = inboxList_(fid).map(function(x){
    return { id:x.id, name:x.name, mime:x.mimeType, size:Number(x.size)||0, md5:x.md5Checksum||null };
  });
  return { ok:true, inboxFolderId:fid, count:items.length, items:items,
           uploadUrl:'https://drive.google.com/drive/folders/' + fid };
}

/** Nạp set md5 từ manifest (KI-10: chỉ file nhị phân có md5). Lazy 1 lần/execution. */
function manifestMd5Set_(){
  if (V211_.manSetMd5) return V211_.manSetMd5;
  var set = {};
  var loc = locateManifest_();
  if (loc && loc.obj && loc.obj.files){
    var each = function(e){ var h = e && (e.md5 || e.md5Checksum); if (h) set[h] = e.id || true; };
    if (Array.isArray(loc.obj.files)) loc.obj.files.forEach(each);
    else Object.keys(loc.obj.files).forEach(function(k){ each(loc.obj.files[k]); });
  }
  V211_.manSetMd5 = set;
  return set;
}

/**
 * POST { token, action:'inbox_process',
 *        cat?:'NN'           — cat đích cho cả batch
 *        map?:{fileId:'NN'}  — cat từng file (ưu tiên hơn cat)
 *        dryRun?:'true', peek?:'true' (KI-09), maxFiles?:N,
 *        share?:'false', register?:'false' }
 *
 * Pipeline mỗi file: dedup md5 → convert → đọc head (export, KI-11) → detect
 * → collision-check tên ở cat đích (KI-08) → rename → share → stamp meta
 * (loai/sohieu/linhvuc qua appProperties) → move → register.
 * 4 nhóm kết quả: done / pending / quarantined / errored (errored = transient,
 * file VẪN Ở INBOX và sẽ retry lần sau — khác quarantined là đã cách ly).
 */
function doInboxProcess_(p){
  var t0 = Date.now(), dry = String(p.dryRun) === 'true', peek = String(p.peek) === 'true';
  var TIME_MS = cfgNum_('TL_INBOX_TIME_MS', 270000);
  var MIN_TEXT = cfgNum_('TL_INBOX_MIN_TEXT', 200);
  var HEAD = cfgNum_('TL_INBOX_HEAD_CHARS', 3000);
  var allowNoNum = cfgBool_('TL_INBOX_ALLOW_NONUM', false);
  var dedup = cfgBool_('TL_INBOX_DEDUP', true);

  var fid = inboxFolderId_(), kids = inboxList_(fid);
  var maxN = Math.min(Number(p.maxFiles)||kids.length, kids.length);
  var map = (typeof p.map === 'object' && p.map) || {};
  var qid = resolveCatFolderId_(cfg_('TL_QUARANTINE_CAT','QUARANTINE'));
  var md5set = dedup ? manifestMd5Set_() : {};
  var done = [], quarantined = [], pending = [], errored = [], i = 0;

  for (; i < maxN; i++){
    if (Date.now() - t0 >= TIME_MS) break;  // >= để TL_INBOX_TIME_MS=0 dừng ngay (test/khẩn cấp)
    var f = kids[i], rec = { srcId:f.id, srcName:f.name };
    try {
      if (f.mimeType === 'application/vnd.google-apps.folder'){
        rec.status='skipped_folder'; pending.push(rec); continue; }
      var isGDoc = f.mimeType === 'application/vnd.google-apps.document';
      var isOffice = /pdf|msword|officedocument\.wordprocessingml/.test(f.mimeType||'');
      if (!isGDoc && !isOffice){ rec.status='skipped_unsupported_mime'; pending.push(rec); continue; }

      // 0) Dedup md5 với manifest (KI-08/KI-10)
      if (dedup && f.md5Checksum && md5set[f.md5Checksum]){
        rec.status='duplicate_md5'; rec.existingId = md5set[f.md5Checksum];
        if (!dry && qid) moveTo_(f.id, qid, fid);
        quarantined.push(rec); continue;
      }

      // 1) Bảo đảm có Google Doc để đọc + làm bản ingest
      var gdocId = null, converted = false;
      if (isGDoc) gdocId = f.id;
      else if (!dry || peek){                        // KI-09: peek convert cả khi dry
        var c = Drive.Files.copy(
          { name: f.name.replace(/\.(docx?|pdf)$/i,''),
            mimeType: 'application/vnd.google-apps.document', parents:[fid] },
          f.id, { supportsAllDrives:true, fields:'id' });
        gdocId = c.id; converted = true;
      }

      // 2) Đọc đầu nội dung — export nhanh thay DocumentApp (KI-11)
      var head = gdocId ? exportText_(gdocId,'text/plain').slice(0, HEAD) : f.name;
      if (converted && head.replace(/\s/g,'').length < MIN_TEXT){
        Drive.Files.update({ trashed:true }, gdocId, null, { supportsAllDrives:true });
        if (!dry && qid) moveTo_(f.id, qid, fid);
        rec.status='quarantined_scan_or_empty'; quarantined.push(rec); continue;
      }
      var d = inboxDetect_(head); rec.detect = d;
      if (dry && peek && converted){                 // dọn bản nháp peek
        Drive.Files.update({ trashed:true }, gdocId, null, { supportsAllDrives:true });
        gdocId = null; converted = false;
      }

      // 3) Tên chuẩn (cho phép thiếu số nếu config) — thiếu vẫn → quarantine
      var std = inboxStdName_(d, allowNoNum);
      if (!std){
        if (!dry){
          if (converted && gdocId) Drive.Files.update({ trashed:true }, gdocId, null, { supportsAllDrives:true });
          if (qid) moveTo_(f.id, qid, fid);
        }
        rec.status='quarantined_detect_fail'; quarantined.push(rec); continue;
      }
      var cat = map[f.id] || p.cat || null;
      var catId = cat ? resolveCatFolderId_(cat) : null;
      rec.stdName = std; rec.cat = cat || '(chưa chỉ định)';

      // 4) Collision-check tên ở cat đích TRƯỚC khi ghi (KI-08)
      if (catId){
        var dup = Drive.Files.list({ q:"name='"+qEsc_(std)+"' and '"+catId+
          "' in parents and trashed=false", pageSize:1, fields:'files(id)',
          supportsAllDrives:true, includeItemsFromAllDrives:true }).files || [];
        if (dup.length){
          rec.status='collision_existing_in_cat'; rec.existingId = dup[0].id;
          if (!dry && converted && gdocId)
            Drive.Files.update({ trashed:true }, gdocId, null, { supportsAllDrives:true });
          quarantined.push(rec); continue;           // file gốc GIỮ ở inbox, người quyết
        }
      }
      if (dry){ rec.status = catId ? 'dry_ok' : 'dry_renamed_pending_cat'; done.push(rec); continue; }

      // 5) Rename (giữ ext bản gốc) + share + stamp meta chuẩn
      var ext = (f.name.match(/\.(docx?|pdf)$/i)||[''])[0].toLowerCase();
      if (gdocId && gdocId !== f.id){
        Drive.Files.update({ name: std }, gdocId, null, { supportsAllDrives:true });
        Drive.Files.update({ name: std + ext }, f.id, null, { supportsAllDrives:true });
      } else Drive.Files.update({ name: std }, f.id, null, { supportsAllDrives:true });
      if (String(p.share) !== 'false' && gdocId) shareView_(gdocId);
      stampProps_(gdocId || f.id, provenance_(p,'','inbox:' + f.id));
      doMetaSet_({ id: gdocId || f.id, loai: d.type, sohieu: d.number || '',
                   linhvuc: cat || '' });            // chiều phân loại → metadata

      // 6) Move (cả hai artifact) — hoặc giữ tại inbox chờ cat
      if (catId){
        if (gdocId && gdocId !== f.id) moveTo_(gdocId, catId, fid);
        moveTo_(f.id, catId, fid);
        if (String(p.register) !== 'false')
          registerRow_({ id: gdocId || f.id, name: std,
            mime:'application/vnd.google-apps.document', sha256: f.md5Checksum || '' });
        rec.gdocId = gdocId; rec.status='done'; done.push(rec);
      } else { rec.gdocId = gdocId; rec.status='renamed_pending_cat'; pending.push(rec); }
    } catch(e){
      // Lỗi transient (rate limit, timeout API): file VẪN Ở INBOX → retry lần sau
      rec.status='error'; rec.error = String(e && e.message || e); errored.push(rec);
    }
  }
  return { ok:true, dryRun:dry, peek:peek, inboxFolderId:fid,
           done:done, quarantined:quarantined, pending:pending, errored:errored,
           processed:i, remaining: kids.length - i, elapsedMs: Date.now() - t0,
           note: kids.length - i > 0 ? 'Còn file — gọi lại inbox_process để tiếp.' : null };
}

function moveTo_(fileId, toId, fromId){
  Drive.Files.update({}, fileId, null,
    { addParents:toId, removeParents:fromId, supportsAllDrives:true, fields:'id,parents' });
}

/* ------------------------- 6) BATCH ENDPOINT (THỬ NGHIỆM — TL_USE_BATCH) ------------------------- */
/* Gom ≤100 call metadata-only (rename/move/permission) vào 1 HTTP round-trip.
 * Mặc định TẮT: lợi ích nhỏ so với export/changes, độ phức tạp parse cao.
 * Mọi chỗ dùng đều phải bọc try → fallback tuần tự. */

/** PURE — dựng body multipart/mixed. reqs: [{method,path,body?}] (path bắt đầu /drive/v3/...) */
function batchBuild_(reqs, boundary){
  var out = [];
  reqs.forEach(function(r, i){
    out.push('--' + boundary);
    out.push('Content-Type: application/http');
    out.push('Content-ID: <item' + (i+1) + '>');
    out.push('');
    out.push(r.method + ' ' + r.path + ' HTTP/1.1');
    if (r.body !== undefined){
      out.push('Content-Type: application/json; charset=UTF-8');
      out.push('');
      out.push(JSON.stringify(r.body));
    } else out.push('');
    out.push('');
  });
  out.push('--' + boundary + '--');
  return out.join('\r\n');
}

/** PURE — parse response multipart: trả [{status, body(JSON|null)}] theo thứ tự. */
function batchParse_(text, boundary){
  var parts = String(text).split('--' + boundary).slice(1, -1), out = [];
  parts.forEach(function(pt){
    var m = pt.match(/HTTP\/[\d.]+\s+(\d{3})/);
    var status = m ? Number(m[1]) : 0, body = null;
    var bi = pt.indexOf('{');
    if (bi >= 0){ try { body = JSON.parse(pt.slice(bi, pt.lastIndexOf('}')+1)); } catch(e){} }
    out.push({ status:status, body:body });
  });
  return out;
}

function driveBatch_(reqs){
  var boundary = 'tl_batch_' + Date.now();
  var r = UrlFetchApp.fetch('https://www.googleapis.com/batch/drive/v3', {
    method:'post', contentType:'multipart/mixed; boundary=' + boundary,
    payload: batchBuild_(reqs, boundary),
    headers:{ Authorization:'Bearer ' + ScriptApp.getOAuthToken() },
    muteHttpExceptions:true });
  if (r.getResponseCode() !== 200)
    throw new Error('batch ' + r.getResponseCode() + ': ' + r.getContentText().slice(0,200));
  var ct = r.getHeaders()['Content-Type'] || '';
  var bm = ct.match(/boundary=([^;]+)/);
  if (!bm) throw new Error('batch: thiếu boundary trong response');
  return batchParse_(r.getContentText(), bm[1].trim());
}

/* ------------------------- 7) PERF + SELFTEST ------------------------- */

/**
 * GET/POST { action:'perf' } — ĐO TRÊN DEPLOYMENT THẬT (số liệu thật phải đo
 * tại đây, không suy diễn). Trả ms cho: list 1 trang corpus, search appProperties,
 * changes pull khô (không apply), export vs DocumentApp (cần TL_SELFTEST_DOC_ID).
 */
function doPerf_(p){
  var out = { ok:true, ms:{} }, t;

  t = Date.now();
  var l = Drive.Files.list({ q:"'"+rootId_()+"' in parents and trashed=false",
    pageSize:1000, fields:'files(id,name,mimeType)', supportsAllDrives:true,
    includeItemsFromAllDrives:true });
  out.ms.list_root_1page = Date.now() - t; out.rootChildren = (l.files||[]).length;

  t = Date.now(); corpusFolders_(true);
  out.ms.corpus_folders_build_nocache = Date.now() - t;

  t = Date.now();
  doSearch_({ q:"appProperties has { key='loai' and value='Luat' }", pageSize:10 });
  out.ms.search_appProperties = Date.now() - t;

  var docId = cfg_('TL_SELFTEST_DOC_ID','');
  if (docId){
    t = Date.now(); var a = exportText_(docId,'text/plain');
    out.ms.export_text = Date.now() - t; out.exportChars = a.length;
    t = Date.now(); var b = DocumentApp.openById(docId).getBody().getText();
    out.ms.documentapp_getText = Date.now() - t; out.docAppChars = b.length;
    out.speedup_export_vs_documentapp =
      Math.round((out.ms.documentapp_getText / Math.max(1,out.ms.export_text)) * 10) / 10;
  } else out.note = 'Đặt TL_SELFTEST_DOC_ID để đo export vs DocumentApp.';

  if (PropertiesService.getScriptProperties().getProperty('TL_CHANGES_TOKEN')){
    t = Date.now(); var cp = doChangesPull_({ apply:'false' });
    out.ms.changes_pull = Date.now() - t; out.changesCount = cp.count;
  }
  return out;
}

/** Chạy tay trong editor 1 lần sau khi dán patch — kiểm môi trường, quyền, logic thuần. */
function _selftest_v211(){
  var rep = { pure:{}, env:{} };
  // pure
  rep.pure.stripVN = stripVN_('Nghị Định Đặc Biệt') === 'Nghi Dinh Dac Biet';
  rep.pure.qEsc = qEsc_("a'b") === "a\\'b";
  var d = inboxDetect_('CHÍNH PHỦ\nSố: 95/2026/NĐ-CP\nNGHỊ ĐỊNH\nQUY ĐỊNH CHI TIẾT THI HÀNH MỘT SỐ ĐIỀU CỦA LUẬT X\nCăn cứ ...');
  rep.pure.detect_nd = d.type === 'ND' && d.number === '95-2026-ND-CP';
  rep.pure.slice = readSlice_('abcdef',2,2,60000,200000).text === 'cd';
  // env
  try { rep.env.driveAdvanced = !!Drive.Files; } catch(e){ rep.env.driveAdvanced = false; }
  try { rep.env.rootOk = !!DriveApp.getFolderById(rootId_()).getName(); }
  catch(e){ rep.env.rootOk = false; }
  try { rep.env.corpusFolders = corpusFolders_(true).ids.length; } catch(e){ rep.env.corpusFolders = 'ERR ' + e; }
  try { rep.env.manifest = !!locateManifest_(); } catch(e){ rep.env.manifest = 'ERR ' + e; }
  try { // batch read-only 2 op — kiểm parser trên response thật
    var b = driveBatch_([
      { method:'GET', path:'/drive/v3/files/' + rootId_() + '?fields=id,name&supportsAllDrives=true' },
      { method:'GET', path:'/drive/v3/files/' + rootId_() + '?fields=id&supportsAllDrives=true' }]);
    rep.env.batch = b.length === 2 && b[0].status === 200;
  } catch(e){ rep.env.batch = 'ERR ' + String(e).slice(0,120); }
  Logger.log(JSON.stringify(rep, null, 2));
  return rep;
}

/* ===================================================================== */
/* ============ 8) SHEET REGISTRY — SỔ CÁI SỐNG (v2.12) ================ */
/* ===================================================================== */

/**
 * Cột registry — THỨ TỰ CỐ ĐỊNH, đổi là phá dữ liệu cũ (thêm cột mới = nối CUỐI).
 * drive_id  : Google Doc canonical (cái NLM nạp) — KHÓA CHÍNH
 * src_id    : file gốc nhị phân (.docx/.pdf) nằm cạnh, nếu có
 * sohieu    : số hiệu CHUẨN HÓA (113-2025-QH15, HOA, Đ→D) — KHÓA TRA CỦA SKILL
 * nlm_*     : mapping NotebookLM — Drive KHÔNG BAO GIỜ tự ghi đè nhóm này (KI-21)
 * nlm_status: '' | pending_push | synced | stale | failed | removed_from_drive
 */
var REG_COLS_ = ['drive_id','src_id','sohieu','loai','name','cat','mime','md5',
  'size','modified_time','linhvuc','goc','nlm_source_id','nlm_status',
  'nlm_pushed_at','verified','registered_at','note',
  // v2.13.0: 4 cột mới — title_vn (tên tiếng Việt gốc), linhvuc_list (mọi chủ đề, ';'),
  // hieuluc (trạng thái hiệu lực), sua_doi (luật sửa đổi: 'sohieu_dich:ten;...' — NGƯỢC chiều goc)
  'title_vn','linhvuc_list','hieuluc','sua_doi',
  // v2.13.6: nlm_title = TÊN THẬT của source trên NLM (có thể đã curate khác tên Drive).
  // Cho phép manifest_export tự đủ làm nguồn chống trùng (bỏ file nlm_sources_*.json riêng).
  'nlm_title',
  // v2.14.0: corpus ('true'|'false') — đa-loại; nlm_notebook_id — đa-notebook (văn bản thường)
  'corpus','nlm_notebook_id',
  // v2.19.0: tukhoa = móc chủ đề (tiêu đề Chương/Điều) cho Claude lọc-thô chọn nguồn.
  // Curated (skill bóc lúc ingest, KHÔNG AI) → phải nằm trong REG_NLM_KEEP_ để regen2 giữ.
  'tukhoa',
  // v2.21.2h: row_kind = own | ref | overflow.
  'row_kind'];
// v2.13.0 doRegAddCols_: ghi lại header 22 cột (idempotent) — chạy MỘT LẦN sau khi dán v2.13.
function doRegAddCols_(p){
  if (String(p.confirm)!=='yes') return { ok:false, error:'Cần confirm=yes (ghi header registry)' };
  var sh = ensureRegTabs_(regSS_());
  sh.getRange(1,1,1,REG_COLS_.length).setNumberFormat('@').setValues([REG_COLS_.slice()]);
  SpreadsheetApp.flush(); regCacheBust_();
  return { ok:true, cols:REG_COLS_.length, header:REG_COLS_ };
}
var REG_TAB_ = 'files', REG_META_TAB_ = '_meta';
// v2.13.0: regen2 quét Drive chỉ biết cấu trúc (cat/name/md5/mtime) — mọi cột "curated"
// (nhập tay/qua pipeline) phải được GIỮ khi merge, nếu không regen sẽ xóa sạch goc/linhvuc/title_vn.
var REG_NLM_KEEP_ = ['nlm_source_id','nlm_status','nlm_pushed_at','verified','note',
  'loai','linhvuc','goc','src_id','title_vn','linhvuc_list','hieuluc','sua_doi',
  'nlm_title','nlm_notebook_id','tukhoa','row_kind']; // KI-21 + v2.13.6 + v2.14.0 + v2.21.2h

/* ---------------- 8.1 PURE (test offline được) ---------------- */

/** Chuẩn hóa số hiệu về dạng khóa: 113/2025/QH15 | 113-2025-qh15 → 113-2025-QH15. */
function normSoHieu_(s){
  if (!s) return '';
  return String(s).trim().toUpperCase().replace(/Đ/g,'D')
    .replace(/[\/\s]+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'');
}

/** Rút số hiệu từ TÊN CHUẨN Loai_so-nam-coquan_Chude (phần giữa 2 dấu '_'). */
function sohieuFromName_(name){
  var m = String(name||'').match(/^[A-Za-z]+_([0-9][\w-]*?)(?:_|\.|$)/);
  return m ? normSoHieu_(m[1]) : '';
}

/** Bắt số hiệu trong CÂU HỎI tự nhiên (cả 113/2025/QH15 lẫn 113-2025-QH15 lẫn 18/VBHN-VPQH). */
function findSoHieuInQuery_(q){
  var m = String(q||'').match(/\d{1,4}[\/-]\d{4}[\/-][A-ZĐ][\w\u00C0-\u1EF9-]*/) ||
          String(q||'').match(/\d{1,4}[\/-][A-ZĐ]{2,6}-[A-ZĐ\d]{2,10}/);
  return m ? normSoHieu_(m[0]) : '';
}

/** values 2D (kèm header) → mảng object theo REG_COLS_; bỏ dòng không có drive_id. */
function rowsToObjs_(values){
  var out = [];
  for (var i = 1; i < values.length; i++){
    var o = {}, any = false;
    for (var c = 0; c < REG_COLS_.length; c++){
      var v = values[i][c]; o[REG_COLS_[c]] = (v === undefined || v === null) ? '' : String(v);
    }
    if (o.drive_id) out.push(o);
  }
  return out;
}
function objsToRows_(objs){
  var rows = [REG_COLS_.slice()];
  objs.forEach(function(o){ rows.push(REG_COLS_.map(function(c){ return o[c] !== undefined ? o[c] : ''; })); });
  return rows;
}

/**
 * PURE — treeHash v2: FNV-1a 32-bit trên các dòng 'id:md5:modifiedTime' ĐÃ SORT
 * → bất biến với thứ tự, đổi 1 byte là đổi hash. KHÁC thuật toán regen cũ (KI-22).
 */
function treeHashV2_(objs){
  var lines = objs.map(function(o){ return o.drive_id + ':' + (o.md5||'') + ':' + (o.modified_time||''); }).sort();
  var h = 0x811c9dc5;
  var s = lines.join('\n');
  for (var i = 0; i < s.length; i++){
    h ^= s.charCodeAt(i);
    h = (h + ((h<<1)+(h<<4)+(h<<7)+(h<<8)+(h<<24))) >>> 0;  // h *= 16777619 (mod 2^32)
  }
  return ('00000000' + h.toString(16)).slice(-8) + '-' + objs.length;
}

function regIsCorpusCounted_(o){
  var rk = String(o.row_kind || 'own').toLowerCase();
  if (rk === 'ref') return false;
  var corpus = String(o.corpus || '').toLowerCase();
  return corpus === 'true' || corpus === 'vbqppl' || rk === 'overflow';
}
function manifestHashObjs_(objs){
  // Profile registryDocId means "this registry is the corpus of record"; hash real rows
  // so drift in vbthuong/other profiles changes treeHash even when corpus=false/loai=thuong.
  if (_REQ_REGISTRY_ID_) return objs.filter(function(o){ return !!o.drive_id; });
  return objs.filter(function(o){ return regIsCorpusCounted_(o) && o.loai!=='thuong'; });
}

/**
 * PURE — trộn kết quả quét Drive vào registry hiện có (KI-21: GIỮ nhóm nlm_*).
 * scanned: objs từ Drive (không có nlm_*); existing: objs từ Sheet.
 * File trong Sheet mà Drive không còn thấy:
 *   - có nlm_source_id → GIỮ DÒNG, nlm_status='removed_from_drive' (người quyết xóa NLM)
 *   - không có        → bỏ dòng.
 */
function regenMerge_(scanned, existing){
  var exById = {}; existing.forEach(function(e){ exById[e.drive_id] = e; });
  var seen = {}, out = [], stats = { added:0, updated:0, kept_removed:0, dropped:0, staled:0 };
  scanned.forEach(function(s){
    seen[s.drive_id] = true;
    var ex = exById[s.drive_id];
    if (ex){
      REG_NLM_KEEP_.forEach(function(k){ s[k] = ex[k] || s[k] || ''; }); // v2.13: registry ưu tiên, trống thì giữ giá trị quét
      // === v2.18.0 SELF-HEAL: file xuất hiện lại trong scan ⇒ bỏ trạng thái removed_from_drive dính cứng ===
      // Trong scanned.forEach mỗi 's' đều đang có trên Drive ở lần scan này ⇒ không cần cờ 'seen' (vốn là object).
      if (s.nlm_status === 'removed_from_drive'){
        // v2.21.2c: KHÔNG tự suy ra 'pushed' chỉ vì còn nlm_source_id cũ.
        // Trạng thái này cũng được dùng khi nguồn NLM đã xóa nhưng registry chưa clear mapping.
        // Chỉ bỏ cờ removed khi không còn nlm_source_id; còn có source_id thì giữ để operator reconcile.
        if (s.nlm_source_id) {
          stats.kept_nlm_removed = (stats.kept_nlm_removed || 0) + 1;
        } else {
          s.nlm_status = '';
          stats.unremoved = (stats.unremoved || 0) + 1;
        }
      }
      if (!s.registered_at) s.registered_at = ex.registered_at || '';
      // nội dung đổi sau khi đã push NLM → stale
      if (s.nlm_source_id && s.nlm_status !== 'removed_from_drive' &&
          (ex.md5 !== s.md5 || ex.modified_time !== s.modified_time) &&
          (ex.md5 || ex.modified_time)){
        if (s.nlm_status === 'synced' || s.nlm_status === ''){ s.nlm_status = 'stale'; stats.staled++; }
      }
      stats.updated++;
    } else { s.registered_at = s.registered_at || new Date().toISOString(); stats.added++; }
    out.push(s);
  });
  existing.forEach(function(e){
    if (seen[e.drive_id]) return;
    if (e.nlm_source_id){ e.nlm_status = 'removed_from_drive'; out.push(e); stats.kept_removed++; }
    else stats.dropped++;
  });
  return { objs: out, stats: stats };
}

/** PURE — upsert 1 entry vào mảng objs theo drive_id; chỉ ghi đè field có giá trị. */
function regUpsertArr_(objs, entry){
  for (var i = 0; i < objs.length; i++){
    if (objs[i].drive_id === entry.drive_id){
      Object.keys(entry).forEach(function(k){
        if (entry[k] !== undefined && entry[k] !== '') objs[i][k] = entry[k];
      });
      return { objs: objs, updated: true };
    }
  }
  var o = {}; REG_COLS_.forEach(function(c){ o[c] = entry[c] !== undefined ? entry[c] : ''; });
  if (!o.registered_at) o.registered_at = new Date().toISOString();
  objs.push(o);
  return { objs: objs, updated: false };
}

/* ---------------- 8.2 Sheet I/O ---------------- */

/** Tìm/tạo spreadsheet registry. Lưu ID vào Script Property để khỏi tìm lại. */
function regSS_(){
  var sp = PropertiesService.getScriptProperties();
  // v2.21.2f: profile truyền registryDocId → mở ĐÚNG Sheet đó (KHÔNG fallback VBQPPL nếu fail, tránh ghi nhầm corpus).
  if (_REQ_REGISTRY_ID_){
    try { return SpreadsheetApp.openById(_REQ_REGISTRY_ID_); }
    catch(e){ throw new Error('registryDocId không mở được (profile): ' + _REQ_REGISTRY_ID_ + ' — ' + (e && e.message || e)); }
  }
  var id = cfg_('TL_REGSHEET_ID','') || sp.getProperty('TL_REGSHEET_ID_AUTO');
  if (id){ try { return SpreadsheetApp.openById(id); } catch(e){} }
  var nm = cfg_('TL_REGSHEET_NAME','tra_luat_registry');
  var found = Drive.Files.list({ q:"name='"+qEsc_(nm)+"' and '"+rootId_()+
    "' in parents and trashed=false", pageSize:1, fields:'files(id)',
    supportsAllDrives:true, includeItemsFromAllDrives:true }).files || [];
  var ss;
  if (found.length) ss = SpreadsheetApp.openById(found[0].id);
  else {
    ss = SpreadsheetApp.create(nm);
    // SpreadsheetApp.create đặt ở root My Drive → move vào ROOT corpus
    Drive.Files.update({}, ss.getId(), null,
      { addParents: rootId_(), removeParents: 'root', supportsAllDrives:true });
  }
  sp.setProperty('TL_REGSHEET_ID_AUTO', ss.getId());
  V211_.props = null;
  ensureRegTabs_(ss);
  return ss;
}

/* ===== v2.21.2p — KI-25/KI-26/KI-27: ATOMIC read-modify-write registry =====
 * SỰ CỐ 2026-07-25 (registry 1.313 → 2 dòng), nguyên nhân GỐC có đường code:
 *   regReadAll_ chạy NGOÀI lock, regWriteAll_ chỉ khóa phần GHI. Giữa deleteSheet(old) và
 *   tmp.setName(REG_TAB_) KHÔNG tồn tại tab `files`; request song song đọc đúng lúc đó thì
 *   ensureRegTabs_ LẶNG LẼ TẠO TAB RỖNG → trả 0 dòng → request ấy ghi đè cả registry bằng
 *   đúng số dòng nó vừa thêm. Cùng cơ chế đã gây race 2026-07-12 (patched=1 mà row bị nuốt).
 * KI-25 Lock phải ôm TRỌN chu trình đọc-sửa-ghi, không chỉ phần ghi → withRegLock_.
 *       ★Apps Script Lock KHÔNG đếm tầng: releaseLock() lồng nhau nhả SỚM giữa chu trình
 *        → phải tự đếm độ sâu, chỉ tầng ngoài cùng mới nhả thật.
 * KI-26 ensureRegTabs_ KHÔNG được tự tạo tab rỗng trên đường ĐỌC khi đang có swap (bằng chứng:
 *       tab `files_tmp` tồn tại) → chờ ngắn rồi thử lại, vẫn thiếu thì ném 'busy' cho client retry.
 * KI-27 regWriteAll_ TỪ CHỐI ghi làm mất >100 dòng HOẶC >50% (trừ khi khai expectShrink đúng số),
 *       và ĐỔI TÊN tab cũ thành files_bak_<ts> (giữ REG_BAK_KEEP_ bản) thay vì xóa → sao lưu
 *       xoay vòng 0 round-trip.
 */
var _REG_LOCK_DEPTH_ = 0;
var REG_BAK_PREFIX_ = 'files_bak_';
var REG_BAK_KEEP_ = 5;
var REG_SHRINK_ABS_ = 100;     // mất > 100 dòng = thảm họa
var REG_SHRINK_FRAC_ = 0.5;    // hoặc mất > 50%

/** KI-25: chạy fn khi ĐANG GIỮ script lock; re-entrant an toàn (Lock của Apps Script không đếm tầng). */
function withRegLock_(fn){
  if (_REG_LOCK_DEPTH_ > 0){            // đã ở trong lock của chính execution này → KHÔNG lấy/nhả lại
    _REG_LOCK_DEPTH_++;
    try { return fn(); } finally { _REG_LOCK_DEPTH_--; }
  }
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) throw new Error('busy: registry đang bị khóa bởi request khác');
  _REG_LOCK_DEPTH_ = 1;
  try { return fn(); }
  finally { _REG_LOCK_DEPTH_ = 0; lock.releaseLock(); }
}

function ensureRegTabs_(ss){
  var sh = ss.getSheetByName(REG_TAB_);
  if (!sh && _REG_LOCK_DEPTH_ === 0 && ss.getSheetByName(REG_TAB_ + '_tmp')){
    // KI-26: tab chính thiếu + tab _tmp còn đó = request khác ĐANG swap. TUYỆT ĐỐI không tạo tab
    // rỗng (đó chính là đường đã xóa trắng registry 25-07) — chờ ngắn rồi thử lại.
    for (var k = 0; k < 6 && !sh; k++){ Utilities.sleep(500); sh = ss.getSheetByName(REG_TAB_); }
    if (!sh) throw new Error('busy: registry đang swap — thử lại (KI-26; KHÔNG tạo tab rỗng)');
  }
  if (!sh){
    sh = ss.insertSheet(REG_TAB_);
    sh.getRange(1,1,1,REG_COLS_.length).setValues([REG_COLS_]);
    sh.getRange(1,1,Math.max(sh.getMaxRows(),1000),REG_COLS_.length).setNumberFormat('@'); // KI-16
  }
  if (!ss.getSheetByName(REG_META_TAB_)) ss.insertSheet(REG_META_TAB_);
  return sh;
}

/** POST { action:'reg_bak_list' } — liệt kê bản sao registry xoay vòng (KI-27). CHỈ ĐỌC. */
function doRegBakList_(p){
  var ss = regSS_();
  var cur = ss.getSheetByName(REG_TAB_);
  var baks = ss.getSheets().map(function(s){ return s.getName(); })
    .filter(function(n){ return n.indexOf(REG_BAK_PREFIX_) === 0; }).sort().reverse();
  return { ok:true, current_rows: cur ? Math.max(0, cur.getLastRow()-1) : 0,
           keep: REG_BAK_KEEP_, count: baks.length,
           baks: baks.map(function(n){
             var s = ss.getSheetByName(n);
             return { tab:n, stamp:n.slice(REG_BAK_PREFIX_.length),
                      rows: s ? Math.max(0, s.getLastRow()-1) : 0 };
           }) };
}

/** POST { action:'reg_bak_restore', tab|stamp, confirm:'yes' } — khôi phục registry từ bản sao (KI-27).
 *  Bản ĐANG DÙNG được giữ lại thành files_bak_<ts> trước khi thay ⇒ khôi phục cũng đảo ngược được. */
function doRegBakRestore_(p){
  if (String(p.confirm) !== 'yes') return { ok:false, error:'Cần confirm=yes (thay toàn bộ registry)' };
  var want = String(p.tab || '').trim();
  if (!want && p.stamp) want = REG_BAK_PREFIX_ + String(p.stamp).trim();
  if (want.indexOf(REG_BAK_PREFIX_) !== 0) return { ok:false, error:'tab phải bắt đầu bằng ' + REG_BAK_PREFIX_ };
  return withRegLock_(function(){
    var ss = regSS_();
    var src = ss.getSheetByName(want);
    if (!src) return { ok:false, error:'Không thấy bản sao: ' + want };
    var cur = ss.getSheetByName(REG_TAB_);
    var beforeRows = cur ? Math.max(0, cur.getLastRow()-1) : 0;
    var afterRows = Math.max(0, src.getLastRow()-1);
    if (cur){
      // giữ bản đang dùng thành 1 bak mới ⇒ thao tác khôi phục KHÔNG phải cửa một chiều
      cur.setName(REG_BAK_PREFIX_ + new Date().toISOString().replace(/[^0-9]/g,'').slice(0,14));
    }
    var copy = src.copyTo(ss);
    copy.setName(REG_TAB_);
    SpreadsheetApp.flush();
    regCacheBust_();
    pruneRegBaks_(ss);
    return { ok:true, restored_from:want, rows_before:beforeRows, rows_after:afterRows,
             note:'Bản trước khi khôi phục đã được giữ thành files_bak_<ts> mới. Chạy manifest_export để đồng bộ snapshot.' };
  });
}

/** KI-27: dọn bản sao cũ, giữ REG_BAK_KEEP_ bản mới nhất (tên có timestamp ⇒ sort chuỗi là đủ). */
function pruneRegBaks_(ss){
  try {
    var baks = ss.getSheets()
      .map(function(s){ return s.getName(); })
      .filter(function(n){ return n.indexOf(REG_BAK_PREFIX_) === 0; })
      .sort();
    while (baks.length > REG_BAK_KEEP_){
      var victim = baks.shift();
      var s = ss.getSheetByName(victim);
      if (s) ss.deleteSheet(s);
    }
  } catch(e){}   // dọn rác là best-effort, KHÔNG được làm hỏng giao dịch ghi
}

/** v2.21.2f: cache registry KEY theo registry đang dùng (tránh lẫn vbqppl/vbthuong giữa các request). */
function _regCacheTag_(){
  var id = _REQ_REGISTRY_ID_ || 'base';
  // rút gọn an toàn cho cache key (id Drive chỉ gồm [A-Za-z0-9_-]).
  return id.length > 16 ? id.slice(-16) : id;
}
function _regCacheKey_(i){ return 'tl212_reg_' + _regCacheTag_() + '_' + i; }

/** Đọc toàn bộ registry → objs, cache CacheService (KI-19: chunk khi >90KB). */
function regReadAll_(force){
  var cache = CacheService.getScriptCache(), TTL = cfgNum_('TL_REG_CACHE_TTL',600);
  if (!force){
    var c0 = cache.get(_regCacheKey_(0));
    if (c0 !== null){
      var buf = c0, i = 1, ci;
      while ((ci = cache.get(_regCacheKey_(i))) !== null){ buf += ci; i++; }
      try { return JSON.parse(buf); } catch(e){}
    }
  }
  var sh = ensureRegTabs_(regSS_());
  var values = sh.getDataRange().getValues();
  var objs = rowsToObjs_(values);
  try {
    var js = JSON.stringify(objs);
    for (var k = 0; k * 90000 < js.length || k === 0; k++)
      cache.put(_regCacheKey_(k), js.slice(k*90000, (k+1)*90000), TTL);
  } catch(e){}
  return objs;
}
function regCacheBust_(){
  var cache = CacheService.getScriptCache();
  for (var i = 0; i < 64; i++) cache.remove(_regCacheKey_(i));
}

/** Ghi TOÀN BỘ registry — tab tạm rồi swap (KI-17), format text (KI-16), lock (KI-18/KI-25),
 *  chốt chặn thảm họa + sao lưu xoay vòng (KI-27).
 *  opts.expectShrink = số dòng CHỦ Ý xóa (doRegDelete_/doRegClear_ truyền vào) — chỉ cần khai khi
 *  phép co chạm ngưỡng thảm họa; ghi bình thường KHÔNG phải đụng gì. */
function regWriteAll_(objs, opts){
  return withRegLock_(function(){
    var ss = regSS_(), rows = objsToRows_(objs);
    var expectShrink = Number((opts || {}).expectShrink || 0);
    var old = ss.getSheetByName(REG_TAB_);
    var oldN = old ? Math.max(0, old.getLastRow() - 1) : 0;   // trừ hàng tiêu đề
    var newN = Math.max(0, rows.length - 1);
    if (oldN > 0 && newN < oldN){
      var lost = oldN - newN;
      var catastrophic = (lost > REG_SHRINK_ABS_) || (lost > oldN * REG_SHRINK_FRAC_);
      if (catastrophic && lost > expectShrink){
        throw new Error('REGISTRY_SHRINK_REFUSED: ghi này làm registry mất ' + lost + ' dòng ('
          + oldN + ' → ' + newN + '), vượt ngưỡng thảm họa (>' + REG_SHRINK_ABS_ + ' dòng hoặc >'
          + Math.round(REG_SHRINK_FRAC_*100) + '%). KHÔNG ghi gì. Nếu ĐÚNG Ý, gọi lại kèm '
          + 'expect_shrink=' + lost + '. (KI-27; sự cố 25-07 registry 1313→2)');
      }
    }
    var tmp = ss.getSheetByName(REG_TAB_ + '_tmp');
    if (tmp) ss.deleteSheet(tmp);
    tmp = ss.insertSheet(REG_TAB_ + '_tmp');
    tmp.getRange(1,1,Math.max(rows.length,1000),REG_COLS_.length).setNumberFormat('@'); // KI-16 TRƯỚC khi ghi
    tmp.getRange(1,1,rows.length,REG_COLS_.length).setValues(rows);                      // KI-20 một call
    if (old){
      // KI-27: ĐỔI TÊN thay vì xóa ⇒ bản sao ngay tại khoảnh khắc nguy hiểm, 0 round-trip thêm.
      old.setName(REG_BAK_PREFIX_ + new Date().toISOString().replace(/[^0-9]/g, '').slice(0, 14));
    }
    tmp.setName(REG_TAB_);
    SpreadsheetApp.flush();                                                              // KI-24
    regCacheBust_();
    pruneRegBaks_(ss);
  });
}

/** Upsert 1 dòng — đọc, vá trong RAM, ghi lại dòng đó (không rewrite cả sheet). */
function regUpsertOne_(entry){
  return withRegLock_(function(){
    var sh = ensureRegTabs_(regSS_());
    var values = sh.getDataRange().getValues();
    var idCol = 0, rowIdx = -1;
    for (var i = 1; i < values.length; i++)
      if (String(values[i][idCol]) === entry.drive_id){ rowIdx = i; break; }
    if (rowIdx >= 0){
      var cur = {}; REG_COLS_.forEach(function(c, j){ cur[c] = String(values[rowIdx][j] || ''); });
      Object.keys(entry).forEach(function(k){
        if (entry[k] !== undefined && entry[k] !== '') cur[k] = String(entry[k]); });
      sh.getRange(rowIdx+1, 1, 1, REG_COLS_.length).setNumberFormat('@')
        .setValues([REG_COLS_.map(function(c){ return cur[c] || ''; })]);
    } else {
      var o = {}; REG_COLS_.forEach(function(c){ o[c] = entry[c] !== undefined ? String(entry[c]) : ''; });
      if (!o.registered_at) o.registered_at = new Date().toISOString();
      var r = sh.getLastRow() + 1;
      sh.getRange(r, 1, 1, REG_COLS_.length).setNumberFormat('@')
        .setValues([REG_COLS_.map(function(c){ return o[c]; })]);
    }
    SpreadsheetApp.flush();   // KI-24
    regCacheBust_();
    return { updated: rowIdx >= 0 };
  });
}

/* ---------------- 8.3 registerRow_ THAY THẾ (KI-23) ---------------- */
/**
 * Giữ NGUYÊN chữ ký cũ {id,name,mime,sha256} để inbox/ingest/copy_convert của
 * base gọi không phải sửa — nhưng đích ghi giờ là SHEET, kèm sohieu chuẩn hóa.
 * XÓA bản registerRow_ cũ trong base trước khi dán v2.12.
 */
function registerRow_(r){
  regUpsertOne_({ drive_id: r.id, name: r.name || '', mime: r.mime || '',
    md5: r.sha256 || r.md5 || '', sohieu: sohieuFromName_(r.name || ''),
    registered_at: new Date().toISOString() });
}

/* ---------------- 8.4 Actions registry/NLM-map ---------------- */

/** GET/POST { action:'reg_get', sohieu? | drive_id? | nlm_source_id? | name_contains?, refresh? } */
function doRegGet_(p){
  var objs = regReadAll_(String(p.refresh)==='true');
  var out;
  if (p.sohieu){ var k = normSoHieu_(p.sohieu);
    out = objs.filter(function(o){ return o.sohieu === k; }); }
  else if (p.drive_id) out = objs.filter(function(o){ return o.drive_id === p.drive_id || o.src_id === p.drive_id; });
  else if (p.nlm_source_id) out = objs.filter(function(o){ return o.nlm_source_id === p.nlm_source_id; });
  else if (p.name_contains){ var kw = stripVN_(p.name_contains).toLowerCase();
    out = objs.filter(function(o){ return stripVN_(o.name).toLowerCase().indexOf(kw) >= 0; }); }
  else return { ok:false, error:'Cần sohieu | drive_id | nlm_source_id | name_contains' };
  return { ok:true, count:out.length, rows:out };
}

/** POST { action:'reg_upsert', drive_id, ...mọi cột REG_COLS_ } */
function doRegUpsert_(p){
  if (!p.drive_id) return { ok:false, error:'Thiếu drive_id' };
  var entry = {};
  REG_COLS_.forEach(function(c){ if (p[c] !== undefined) entry[c] = String(p[c]); });
  if (entry.sohieu) entry.sohieu = normSoHieu_(entry.sohieu);
  else if (entry.name) entry.sohieu = sohieuFromName_(entry.name);
  var r = regUpsertOne_(entry);
  return { ok:true, drive_id:p.drive_id, updated:r.updated };
}

/**
 * v2.13.7 — POST { action:'reg_bulk', items:[{drive_id|nlm_source_id, <cột>...}], cols? }
 * Vá NHIỀU dòng trong MỘT thao tác: đọc registry 1 LẦN → vá trong RAM (khớp theo
 * drive_id, hoặc nlm_source_id) → ghi CẢ sheet 1 LẦN (regWriteAll_). Thay cho việc
 * gọi N lần reg_upsert (mỗi lần đọc+ghi lại sheet → chậm tuyến tính, dễ timeout).
 * AN TOÀN: mặc định CHỈ cho vá cột 'nlm_title'. Mở rộng có kiểm soát qua cols=
 * 'nlm_title,nlm_status' (chỉ nhận cột thuộc REG_COLS_). Empty string KHÔNG ghi đè.
 * Item không khớp dòng nào → trả về trong 'miss' (đây là tín hiệu nguồn "mồ côi").
 */

/**
 * v2.21.2c — POST { action:'reg_clear', drive_id? | nlm_source_id?, cols:'nlm_source_id,nlm_status,...', confirm:'yes' }
 * Xóa giá trị cột có kiểm soát. Dùng cho ca source NLM đã xóa nhưng registry còn nlm_source_id cũ.
 * Chỉ clear các cột an toàn; không đụng drive_id/name/cat/mime/md5.
 */
function doRegClear_(p){
  if (String(p.confirm) !== 'yes') return { ok:false, error:'Cần confirm=yes' };
  var keyDrive = String(p.drive_id || p.fileId || '').trim();
  var keyNlm = String(p.nlm_source_id || '').trim();
  if (!keyDrive && !keyNlm) return { ok:false, error:'Cần drive_id hoặc nlm_source_id' };
  // v2.21.2j (#5 log hồ sơ BHXH): 2 TẦNG — nlm_*/note như cũ (confirm=yes); CỘT THƯỜNG (mọi cột REG_COLS_
  // trừ PROTECTED drive_id/name) đòi THÊM force='yes' (đính chính sohieu/loai/goc... gán nhầm — trước đây
  // giá trị rỗng bị bỏ im lặng, không có đường xoá chính danh). Tương thích ngược 100%: call cũ không force
  // vẫn chỉ nlm_*/note.
  var allowed = { nlm_source_id:true, nlm_status:true, nlm_pushed_at:true, nlm_title:true, nlm_notebook_id:true, note:true };
  var PROTECTED_ = { drive_id:true, name:true };
  var force = String(p.force || '') === 'yes';
  var cols = String(p.cols || '').split(',').map(function(x){ return x.trim(); }).filter(Boolean);
  if (!cols.length) return { ok:false, error:'Cần cols' };
  for (var i=0;i<cols.length;i++){
    var c = cols[i];
    if (allowed[c]) continue;
    if (PROTECTED_[c]) return { ok:false, error:'Cột BẢO VỆ không bao giờ clear: '+c };
    if (REG_COLS_.indexOf(c) < 0) return { ok:false, error:'Cột không thuộc REG_COLS_: '+c };
    if (!force) return { ok:false, error:'Cột thường cần force=yes (2.21.2j): '+c };
  }
  // KI-25 (v2.21.2p): đọc + sửa + ghi phải nằm TRỌN trong MỘT lock, không chỉ phần ghi.
  return withRegLock_(function(){
    var objs = regReadAll_(true), hits = [];
    objs.forEach(function(o){
      var ok = (keyDrive && o.drive_id === keyDrive) || (keyNlm && o.nlm_source_id === keyNlm);
      if (!ok) return;
      cols.forEach(function(c){ o[c] = ''; });
      hits.push(o.drive_id || '');
    });
    if (hits.length) regWriteAll_(objs);   // clear KHÔNG xóa dòng ⇒ không co, khỏi expectShrink
    return { ok:true, cleared: hits.length, drive_ids:hits, cols:cols };
  });
}

function doRegBulk_(p){
  var items = (typeof p.items === 'string') ? JSON.parse(p.items) : p.items;
  if (!Array.isArray(items)) return { ok:false, error:'items phải là mảng' };
  var ALLOW = (p.cols ? String(p.cols).split(',') : ['nlm_title'])
                .map(function(s){ return s.trim(); })
                .filter(function(c){ return REG_COLS_.indexOf(c) >= 0; });
  if (!ALLOW.length) return { ok:false, error:'cols không hợp lệ (phải thuộc REG_COLS_)' };
  // KI-25 (v2.21.2p): CHÍNH đường này gây race 2026-07-12 (patched=1 mà row bị nuốt) — đọc và ghi
  // phải cùng một lock, nếu không hai process đều đọc bản cũ rồi bản sau đè mất bản trước.
  return withRegLock_(function(){
    var objs = regReadAll_(true);
    var byDrive = {}, bySrc = {};
    objs.forEach(function(o){
      if (o.drive_id) byDrive[o.drive_id] = o;
      if (o.nlm_source_id) bySrc[o.nlm_source_id] = o;
    });
    var patched = 0, dirty = false, miss = [];
    items.forEach(function(it){
      it = it || {};
      var row = (it.drive_id && byDrive[it.drive_id]) ||
                (it.nlm_source_id && bySrc[it.nlm_source_id]) || null;
      if (!row){ miss.push(it.nlm_source_id || it.drive_id || '?'); return; }
      var changed = false;
      ALLOW.forEach(function(c){
        if (it[c] !== undefined && String(it[c]) !== '' && row[c] !== String(it[c])){
          row[c] = String(it[c]); changed = true;
        }
      });
      if (changed){ dirty = true; patched++; }
    });
    if (dirty) regWriteAll_(objs);   // 1 LẦN GHI duy nhất
    return { ok:true, total:items.length, patched:patched,
             missed:miss.length, miss:miss.slice(0,30), cols:ALLOW };
  });
}

/* ================= v2.21.2l — F-04 ingest_claim + F-08 reg_get_bulk =================
 * Grill-with-docs 12 quyết định (D1-D12, 2026-07-15; kế hoạch
 * D:\Quốc hội\ke-hoach-gas-2.21.2l-ingest-claim-2026-07-15.md). Tab `claims` RIÊNG, CÙNG
 * Spreadsheet với `files` (co-located theo registryDocId đang dùng — _REQ_REGISTRY_ID_).
 * Cột: identity_hash|state|run_id|acquired_at|expires_at|source_id|drive_id.
 * state ∈ {pending, committed, released} — "expired" là SUY RA (now > expires_at khi
 * state=pending), KHÔNG phải giá trị ghi cứng.
 *
 * 3 hàm PURE (KHÔNG gọi GAS service nào — test qua Node: references/gas_claim_test.js,
 * KHÔNG merge/inline logic quyết định vào hàm I/O để giữ test-được offline):
 *   _claimGcFilter_(rows, nowMs, retentionMs)      — lazy GC (D10): loại committed/released
 *     quá cũ (retention, dùng acquired_at làm mốc — pending KHÔNG bao giờ bị xoá, tự chữa
 *     qua reclaim khi hết TTL).
 *   _claimAcquireDecide_(existingRow, nowMs, ttlMs, runId) — D9: existingRow=null (chưa ai
 *     giữ)/released → grant; pending cùng run_id (idempotent retry) → grant; pending khác
 *     run_id NHƯNG đã hết TTL (bỏ rơi) → grant reclaim; pending khác run_id CÒN hạn → deny
 *     (D5: caller skip+báo cáo, KHÔNG retry trong run); committed → deny kèm source_id (để
 *     caller LINK thay vì add trùng).
 *   _claimCommitDecide_(existingRow, runId, nowMs) — D3: chỉ OK khi row đang pending VÀ
 *     ĐÚNG run_id (đây là chốt chặn double-commit: nếu claim đã bị host khác reclaim sau khi
 *     TTL hết, run_id đổi chủ → mismatch → từ chối, KHÔNG cần re-check TTL riêng ở bước này).
 */

var CLAIMS_TAB_ = 'claims';
var CLAIMS_COLS_ = ['identity_hash', 'state', 'run_id', 'acquired_at', 'expires_at', 'source_id', 'drive_id'];
var CLAIM_TTL_MS_ = 5 * 60 * 1000;              // D4: 5 phút
var CLAIM_GC_RETENTION_MS_ = 24 * 60 * 60 * 1000; // D10: 24h cho committed/released

function _claimGcFilter_(rows, nowMs, retentionMs) {
  return (rows || []).filter(function (r) {
    if (r.state === 'committed' || r.state === 'released') {
      var age = nowMs - Date.parse(r.acquired_at || 0);
      return !(age >= retentionMs);
    }
    return true;   // pending giữ nguyên — tự chữa qua reclaim (D10)
  });
}

function _claimAcquireDecide_(existingRow, nowMs, ttlMs, runId) {
  if (!existingRow) return { action: 'grant', reason: 'NEW' };
  if (existingRow.state === 'released') return { action: 'grant', reason: 'RELEASED_RECLAIM' };
  if (existingRow.state === 'committed') {
    return { action: 'deny', reason: 'ALREADY_COMMITTED', source_id: existingRow.source_id || '' };
  }
  // state === 'pending' (hoặc 'expired' phòng hờ nếu có giá trị lạ — coi như pending)
  if (existingRow.run_id === runId) return { action: 'grant', reason: 'IDEMPOTENT_SAME_OWNER' };
  if (nowMs > Date.parse(existingRow.expires_at || 0)) return { action: 'grant', reason: 'EXPIRED_RECLAIM' };
  return { action: 'deny', reason: 'HELD_BY_OTHER' };
}

function _claimCommitDecide_(existingRow, runId, nowMs) {
  if (!existingRow) return { ok: false, reason: 'NOT_FOUND' };
  if (existingRow.state !== 'pending') return { ok: false, reason: 'NOT_PENDING' };
  if (existingRow.run_id !== runId) return { ok: false, reason: 'RUN_ID_MISMATCH' };
  return { ok: true, reason: 'COMMITTED' };
}

/** D3 (release tường minh khi item fail vĩnh viễn): CHỈ chủ sở hữu (đúng run_id) mới release được
 * claim đang pending — chặn caller lạ giải phóng nhầm claim ai đó khác đang giữ. Không phải lỗi khi
 * release claim không tồn tại/đã committed/released (idempotent, không throw). */
function _claimReleaseDecide_(existingRow, runId) {
  if (!existingRow) return { ok: true, reason: 'NOOP_NOT_FOUND' };
  if (existingRow.state !== 'pending') return { ok: true, reason: 'NOOP_NOT_PENDING' };
  if (existingRow.run_id !== runId) return { ok: false, reason: 'RUN_ID_MISMATCH' };
  return { ok: true, reason: 'RELEASED' };
}

/* ---------------- I/O claims (mirror regReadAll_/regWriteAll_ — Sheet riêng, cùng Spreadsheet) ---------------- */

function _claimsRowsToObjs_(values) {
  var out = [];
  for (var i = 1; i < values.length; i++) {
    var o = {};
    for (var c = 0; c < CLAIMS_COLS_.length; c++) {
      var v = values[i][c]; o[CLAIMS_COLS_[c]] = (v === undefined || v === null) ? '' : String(v);
    }
    if (o.identity_hash) out.push(o);
  }
  return out;
}
function _claimsObjsToRows_(objs) {
  var rows = [CLAIMS_COLS_.slice()];
  objs.forEach(function (o) { rows.push(CLAIMS_COLS_.map(function (c) { return o[c] !== undefined ? o[c] : ''; })); });
  return rows;
}
function ensureClaimsTab_(ss) {
  var sh = ss.getSheetByName(CLAIMS_TAB_);
  if (!sh) {
    sh = ss.insertSheet(CLAIMS_TAB_);
    sh.getRange(1, 1, 1, CLAIMS_COLS_.length).setNumberFormat('@').setValues([CLAIMS_COLS_]);
  }
  return sh;
}
function claimsReadAll_() {
  var sh = ensureClaimsTab_(regSS_());
  return _claimsRowsToObjs_(sh.getDataRange().getValues());
}
/** Ghi TOÀN BỘ claims tab — tab tạm rồi swap (khớp pattern regWriteAll_ KI-17/KI-18/KI-24). */
function claimsWriteAll_(objs) {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) throw new Error('busy: claims đang bị khóa bởi request khác');
  try {
    var ss = regSS_(), rows = _claimsObjsToRows_(objs);
    var tmp = ss.getSheetByName(CLAIMS_TAB_ + '_tmp');
    if (tmp) ss.deleteSheet(tmp);
    tmp = ss.insertSheet(CLAIMS_TAB_ + '_tmp');
    tmp.getRange(1, 1, Math.max(rows.length, 100), CLAIMS_COLS_.length).setNumberFormat('@');
    tmp.getRange(1, 1, rows.length, CLAIMS_COLS_.length).setValues(rows);
    var old = ss.getSheetByName(CLAIMS_TAB_);
    if (old) ss.deleteSheet(old);
    tmp.setName(CLAIMS_TAB_);
    SpreadsheetApp.flush();
  } finally { lock.releaseLock(); }
}

/**
 * v2.21.2l (F-04) — POST { action:'ingest_claim', keys:[identity_hash,...]?, run_id, drive_ids?:[...],
 *   release_keys:[identity_hash,...]? }
 * Acquire hàng loạt (D9: một action nhận mảng — không tách single/bulk). Lazy GC (D10) trước khi quyết.
 * drive_ids (song song keys, cùng thứ tự, optional) chỉ để LƯU kèm claim cho dễ soi tay trên Sheet —
 * KHÔNG dùng để quyết định (identity_hash là khóa duy nhất, D2). `release_keys` (D3): giải phóng tường
 * minh khi item fail vĩnh viễn (không chờ TTL) — có thể gửi CÙNG lúc với `keys` (acquire batch khác +
 * release batch khác trong 1 round-trip) hoặc riêng.
 */
function doIngestClaim_(p) {
  var keys = (typeof p.keys === 'string') ? JSON.parse(p.keys) : (p.keys || []);
  var releaseKeys = (typeof p.release_keys === 'string') ? JSON.parse(p.release_keys) : (p.release_keys || []);
  if ((!Array.isArray(keys) || !keys.length) && (!Array.isArray(releaseKeys) || !releaseKeys.length)) {
    return { ok: false, error: 'Cần keys và/hoặc release_keys (mảng identity_hash)' };
  }
  var runId = String(p.run_id || '').trim();
  if (!runId) return { ok: false, error: 'Cần run_id' };
  var driveIds = (typeof p.drive_ids === 'string') ? JSON.parse(p.drive_ids) : (p.drive_ids || []);
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) return { ok: false, error: 'busy: claims đang bị khóa bởi request khác' };
  var results = [], released = [], release_failed = [];
  try {
    var now = Date.now();
    var rows = claimsReadAll_();
    rows = _claimGcFilter_(rows, now, CLAIM_GC_RETENTION_MS_);
    var byKey = {}; rows.forEach(function (r) { byKey[r.identity_hash] = r; });
    var dirty = false;
    (keys || []).forEach(function (k, i) {
      var existing = byKey[k] || null;
      var decision = _claimAcquireDecide_(existing, now, CLAIM_TTL_MS_, runId);
      results.push({ identity_hash: k, granted: decision.action === 'grant', reason: decision.reason,
        source_id: decision.source_id || '' });
      if (decision.action === 'grant') {
        var row = { identity_hash: k, state: 'pending', run_id: runId,
          acquired_at: new Date(now).toISOString(), expires_at: new Date(now + CLAIM_TTL_MS_).toISOString(),
          source_id: '', drive_id: driveIds[i] || (existing && existing.drive_id) || '' };
        byKey[k] = row; dirty = true;
      }
    });
    (releaseKeys || []).forEach(function (k) {
      var existing = byKey[k] || null;
      var rd = _claimReleaseDecide_(existing, runId);
      if (rd.ok) {
        if (existing && existing.state === 'pending') { existing.state = 'released'; byKey[k] = existing; dirty = true; }
        released.push(k);
      } else {
        release_failed.push({ identity_hash: k, reason: rd.reason });
      }
    });
    if (dirty || rows.length !== Object.keys(byKey).length) {
      claimsWriteAll_(Object.keys(byKey).map(function (k) { return byKey[k]; }));
    }
  } finally { lock.releaseLock(); }
  return { ok: true, run_id: runId, results: results,
    granted: results.filter(function (r) { return r.granted; }).length,
    denied: results.filter(function (r) { return !r.granted; }).length,
    released: released, release_failed: release_failed };
}

/**
 * v2.21.2l (F-08) — GET/POST { action:'reg_get_bulk', keys:[...], key_field:'drive_id'|'nlm_source_id',
 *   commit_claims?:[{identity_hash, source_id, run_id}...] }
 * Đọc N dòng registry `files` 1 LẦN, trả TOÀN BỘ 27 REG_COLS_ (D6) theo THỨ TỰ request (key không khớp
 * → null). commit_claims (D3): commit GỘP vào cùng round-trip — verify run_id khớp chủ sở hữu claim
 * (_claimCommitDecide_) trước khi mark committed; KHÔNG re-check TTL riêng (đã acquire được nghĩa là còn
 * hạn lúc đó; run_id mismatch tự bắt ca bị host khác reclaim).
 */
/* ================= v2.21.2n — r185/WP5: profile_catalog + drive_info_bulk =================
 * D3 (kế hoạch review p9 2026-07-23): endpoint CỘNG THÊM, CHỈ ĐỌC — mục tiêu giảm TỔNG ROUND-TRIP
 * (không chỉ che độ trễ): discover/doctor trước đây ~3×N call (list folder + list _meta + download
 * marker cho TỪNG profile) → 1 call trả snapshot TẤT ĐỊNH; template probe O(template) list/download
 * → 1 call metadata theo lô. KHÔNG đổi endpoint mutation. */
function doProfileCatalog_(p){
  // Snapshot cây Van_ban_thuong cho profile-list --discover / doctor shallow: con trực tiếp +
  // items từng subfolder + items _meta + NỘI DUNG mọi file marker tra_luat_profile.json (kể cả
  // bản TRÙNG — client tự phát hiện DUPLICATE, server không chọn hộ). Thứ tự folder/items ổn định
  // (sort theo name rồi id). folderId = vanBanThuongId (client lấy từ bootstrap/config).
  if (!p.folderId) return { ok:false, error:'profile_catalog: thiếu folderId (vanBanThuongId)' };
  var cap = Math.min(Number(p.folderCap)||60, 200);
  var MARKER = 'tra_luat_profile.json', MARKER_MAX = 16384;
  function lite_(x){ return {id:x.id, name:x.name, mime:x.mimeType, size:Number(x.size)||0,
    type:x.mimeType==='application/vnd.google-apps.folder'?'folder':'file'}; }
  function byName_(a,b){ return a.name===b.name ? (a.id<b.id?-1:1) : (a.name<b.name?-1:1); }
  var top = listChildren_(String(p.folderId)).map(lite_).sort(byName_);
  var rootFiles = top.filter(function(x){ return x.type!=='folder'; });
  var subs = top.filter(function(x){ return x.type==='folder'; });
  var folders = [];
  for (var i=0; i<subs.length && i<cap; i++){
    var fo = subs[i], items = [], metaId = '', markers = [];
    try { items = listChildren_(fo.id).map(lite_).sort(byName_); } catch(e){ items = []; }
    for (var j=0; j<items.length; j++)
      if (items[j].type==='folder' && items[j].name==='_meta'){ metaId = items[j].id; break; }
    if (metaId){
      var mi = [];
      try { mi = listChildren_(metaId).map(lite_).sort(byName_); } catch(e){ mi = []; }
      items = items.concat(mi);
    }
    for (var k=0; k<items.length; k++){
      var it = items[k];
      if (it.type!=='folder' && it.name===MARKER){
        var rec = { id: it.id, json_text: null, error: null };
        try {
          var txt = DriveApp.getFileById(it.id).getBlob().getDataAsString('UTF-8');
          if (txt.length > MARKER_MAX) rec.error = 'MARKER_TOO_LARGE:'+txt.length;
          else rec.json_text = txt;
        } catch(e){ rec.error = 'MARKER_READ_FAILED:'+e; }
        markers.push(rec);
      }
    }
    folders.push({ id: fo.id, name: fo.name, meta_folder_id: metaId, items: items, markers: markers });
  }
  return { ok:true, schema:'profile_catalog.v1', folderId:String(p.folderId),
           folder_total: subs.length, capped: subs.length > cap,
           folders: folders, root_files: rootFiles };
}
function doDriveInfoBulk_(p){
  // Metadata N fileId trong 1 call — GIỮ THỨ TỰ INPUT (tất định); lỗi per-item không phá lô.
  var ids = [];
  try { ids = JSON.parse(p.ids || '[]'); } catch(e){ return { ok:false, error:'drive_info_bulk: ids không phải JSON array' }; }
  if (!ids || !ids.length) return { ok:false, error:'drive_info_bulk: ids rỗng' };
  if (ids.length > 200) return { ok:false, error:'drive_info_bulk: quá 200 id/lô — chia lô ở client' };
  var out = [];
  for (var i=0; i<ids.length; i++){
    var id = String(ids[i]||'');
    if (!id){ out.push({ id:id, ok:false, error:'EMPTY_ID' }); continue; }
    try {
      var f = Drive.Files.get(id, {fields:'id,name,mimeType,size,parents,trashed,modifiedTime',
                                   supportsAllDrives:true});
      out.push({ id:id, ok:true, name:f.name, mime:f.mimeType, size:Number(f.size)||0,
                 parents:f.parents||[], trashed:!!f.trashed, modifiedTime:f.modifiedTime });
    } catch(e){ out.push({ id:id, ok:false, error:String(e).slice(0,200) }); }
  }
  return { ok:true, schema:'drive_info_bulk.v1', count:out.length, results:out };
}

function doRegGetBulk_(p) {
  var keys = (typeof p.keys === 'string') ? JSON.parse(p.keys) : p.keys;
  if (!Array.isArray(keys) || !keys.length) return { ok: false, error: 'Cần keys (mảng)' };
  var keyField = (p.key_field === 'nlm_source_id') ? 'nlm_source_id' : 'drive_id';
  var objs = regReadAll_(true);
  var byKey = {};
  objs.forEach(function (o) { if (o[keyField]) byKey[o[keyField]] = o; });
  var rows = keys.map(function (k) { return byKey[k] || null; });
  var out = { ok: true, key_field: keyField, count: rows.filter(Boolean).length, rows: rows };
  var commitClaims = (typeof p.commit_claims === 'string') ? JSON.parse(p.commit_claims) : p.commit_claims;
  if (Array.isArray(commitClaims) && commitClaims.length) {
    var lock = LockService.getScriptLock();
    if (!lock.tryLock(30000)) {
      out.committed = []; out.commit_failed = commitClaims.map(function (c) {
        return { identity_hash: c.identity_hash, reason: 'BUSY' }; });
      return out;
    }
    try {
      var now = Date.now();
      var claimRows = claimsReadAll_();
      claimRows = _claimGcFilter_(claimRows, now, CLAIM_GC_RETENTION_MS_);
      var byHash = {}; claimRows.forEach(function (r) { byHash[r.identity_hash] = r; });
      var committed = [], failed = [], dirty = false;
      commitClaims.forEach(function (c) {
        var existing = byHash[c.identity_hash] || null;
        var d = _claimCommitDecide_(existing, String(c.run_id || ''), now);
        if (d.ok) {
          existing.state = 'committed'; existing.source_id = String(c.source_id || '');
          byHash[c.identity_hash] = existing; dirty = true;
          committed.push(c.identity_hash);
        } else {
          failed.push({ identity_hash: c.identity_hash, reason: d.reason });
        }
      });
      if (dirty) claimsWriteAll_(Object.keys(byHash).map(function (k) { return byHash[k]; }));
      out.committed = committed; out.commit_failed = failed;
    } finally { lock.releaseLock(); }
  }
  return out;
}
/* ================= hết v2.21.2l F-04/F-08 ================= */

/**
 * POST { action:'reg_delete', confirm:'yes', drive_ids:[...]|JSON, require_removed?:'yes'|'no' }
 * Gỡ HẲN dòng khỏi registry theo drive_id. KHÔNG đụng nguồn NLM (không source_delete).
 * AN TOÀN: require_removed!=='no' ⇒ CHỈ xóa dòng có nlm_status bắt đầu 'removed'
 * (chặn lỡ tay xóa dòng live dùng chung nlm_source_id với bản ghost).
 */
function doRegDelete_(p){
  if (String(p.confirm) !== 'yes') return { ok:false, error:"Cần confirm=yes (gỡ dòng registry)" };
  var ids = (typeof p.drive_ids === 'string') ? JSON.parse(p.drive_ids) : p.drive_ids;
  if (!Array.isArray(ids) || !ids.length) return { ok:false, error:'drive_ids phải là mảng không rỗng' };
  var want = {}; ids.forEach(function(x){ want[String(x)] = true; });
  var requireRemoved = String(p.require_removed || 'yes') !== 'no';
  // KI-25 (v2.21.2p): lock ôm trọn đọc-sửa-ghi.
  return withRegLock_(function(){
    var objs = regReadAll_(true);
    var keep = [], removed = [], skippedLive = [], found = {};
    objs.forEach(function(o){
      if (want[o.drive_id]){
        found[o.drive_id] = true;
        if (requireRemoved && String(o.nlm_status || '').indexOf('removed') !== 0){
          skippedLive.push(o.drive_id); keep.push(o); return;   // BẢO VỆ dòng live
        }
        removed.push(o.drive_id); return;                        // bỏ khỏi keep = xóa
      }
      keep.push(o);
    });
    var notFound = ids.filter(function(x){ return !found[String(x)]; });
    // KI-27: đây là phép CO HỢP LỆ — khai đúng số dòng chủ ý xóa để chốt chặn không chặn nhầm.
    if (removed.length) regWriteAll_(keep, { expectShrink: removed.length });
    return { ok:true, requested:ids.length, removed:removed.length,
             skipped_live:skippedLive.length, not_found:notFound.length,
             removed_ids:removed.slice(0,60), skipped_live_ids:skippedLive.slice(0,20),
             not_found_ids:notFound.slice(0,20) };
  });
}

/**
 * POST { action:'map_set', drive_id|sohieu, nlm_source_id, status?, notebook? }
 * Gọi SAU MỖI source_add thành công / reconcile (quy tắc v1.9.12 của skill).
 */
function doMapSet_(p){
  var objs, target = null;
  if (p.drive_id){ target = p.drive_id; }
  else if (p.sohieu){
    objs = regReadAll_(false);
    var k = normSoHieu_(p.sohieu);
    var hit = objs.filter(function(o){ return o.sohieu === k; });
    if (hit.length !== 1) return { ok:false, error:'sohieu khớp ' + hit.length + ' dòng — dùng drive_id', candidates:hit.map(function(o){return o.drive_id;}) };
    target = hit[0].drive_id;
  } else return { ok:false, error:'Cần drive_id hoặc sohieu' };
  var r = regUpsertOne_({ drive_id: target,
    nlm_source_id: p.nlm_source_id || '',
    nlm_status: p.status || (p.nlm_source_id ? 'synced' : ''),
    nlm_pushed_at: p.nlm_source_id ? new Date().toISOString() : '',
    nlm_title: p.nlm_title || '',   // v2.13.6: tên THẬT trên NLM (để manifest tự đủ chống trùng)
    nlm_notebook_id: p.notebookId || p.nlm_notebook_id || p.notebook || '',
    note: p.note || (p.notebook ? ('nb:' + p.notebook) : '') });
  return { ok:true, drive_id: target, updated: r.updated };
}

/** GET/POST { action:'map_unpushed', includeStale? } — input cho nlm_push.py. */
function doMapUnpushed_(p){
  var objs = regReadAll_(String(p.refresh)==='true');
  var withStale = String(p.includeStale) !== 'false';
  // v2.13.4: cổng server-side — supersede index (VBHN goc/sdbs) + check tên chuẩn + quota NLM
  var supGoc = {}, supSdbs = {};
  objs.forEach(function(v){
    var nm = String(v.name||'');
    if (nm.toUpperCase().indexOf('VBHN') < 0) return;
    var col = String(v.goc||'').split(/[;,]/).map(function(x){return normSoHieu_(x.trim());}).filter(String);
    var nameGoc = [], mm, reG=/goc_([0-9A-Za-z-]+)/g, reS=/sdbs_([0-9A-Za-z-]+)/g;
    while ((mm=reG.exec(nm))) nameGoc.push(normSoHieu_(mm[1]));
    var nameSdbs = [];
    while ((mm=reS.exec(nm))) { if (/\d{4}/.test(mm[1])) nameSdbs.push(normSoHieu_(mm[1])); }
    var gocSet = nameGoc.length ? nameGoc : (col.length ? [col[0]] : []);
    var sdbsSet = nameGoc.length ? nameSdbs.concat(col.filter(function(x){return gocSet.indexOf(x)<0;}))
                                 : col.slice(1);
    gocSet.forEach(function(k){ (supGoc[k]=supGoc[k]||[]).push({name:v.name, on_nlm:!!v.nlm_source_id}); });
    sdbsSet.forEach(function(k){ (supSdbs[k]=supSdbs[k]||[]).push({name:v.name, on_nlm:!!v.nlm_source_id}); });
  });
  function nameFlags_(n){
    var f=[];
    if (stripVN_(n) !== n) f.push('co_dau_tieng_viet');
    if (n.indexOf(' ') >= 0) f.push('co_khoang_trang');
    if (!/^(Luat|BL[A-Z]*|PL|NQ|ND|TT|QD|VBHN|KL|CT|HP|TTLT|CU|CPTPP|EVFTA|HD)_/.test(stripVN_(n)))
      f.push('thieu_prefix_loai');
    if (/_\d{5,7}$/.test(n)) f.push('duoi_so_tvpl');
    if (/_\d{13}$/.test(n)) f.push('duoi_timestamp');
    return f;
  }
  var pushedCount = objs.filter(function(o){return !!o.nlm_source_id;}).length;
  var tier = (cfg_('TL_NLM_TIER','pro')||'pro').toLowerCase();
  var caps = {free:50, plus:100, pro:300, ultra:600};
  var cap = caps[tier] || 300;
  var out = objs.filter(function(o){
    if (o.mime && o.mime !== 'application/vnd.google-apps.document') return false; // NLM chỉ nạp GDoc
    if (!o.nlm_source_id) return true;
    return withStale && (o.nlm_status === 'stale' || o.nlm_status === 'failed' || o.nlm_status === 'pending_push');
  }).map(function(o){
    var nf = nameFlags_(String(o.name||''));
    var k = o.sohieu ? normSoHieu_(o.sohieu) : '';
    var sup = null;
    if (k && supGoc[k]) sup = {rel:'goc', vbhn:supGoc[k]};
    else if (k && supSdbs[k]) sup = {rel:'sdbs', vbhn:supSdbs[k]};
    return { drive_id:o.drive_id, sohieu:o.sohieu, name:o.name,
      cat:o.cat, nlm_status:o.nlm_status || 'never_pushed',
      name_ok: nf.length === 0, name_flags: nf.length ? nf : undefined,
      superseded_by: sup || undefined };
  });
  return { ok:true, count:out.length, rows:out,
    nlm_quota: { tier:tier, cap:cap, pushed:pushedCount, slots_free:cap - pushedCount } };
}

/** POST { action:'map_mark_stale', drive_id } */
function doMapMarkStale_(p){
  if (!p.drive_id) return { ok:false, error:'Thiếu drive_id' };
  var r = regUpsertOne_({ drive_id:p.drive_id, nlm_status:'stale' });
  return { ok:true, drive_id:p.drive_id, updated:r.updated };
}

/** Hook từ doChangesPull_: vá deltas vào Sheet + stale hóa (KI-21). */
function regApplyDeltas_(deltas, nameById){
  // KI-25 (v2.21.2p): lock ôm trọn đọc-sửa-ghi (đường này có splice XÓA dòng ⇒ co được thật).
  return withRegLock_(function(){
  var objs = regReadAll_(true);
  var byId = {}; objs.forEach(function(o){ byId[o.drive_id] = o; });
  var stats = { upserted:0, staled:0, removed_marked:0 };
  var dirty = false;
  var _splice = 0;
  deltas.forEach(function(d){
    if (d.kind === 'folder_changed') return;
    var ex = byId[d.id];
    if (d.kind === 'removed' || d.kind === 'moved_out'){
      if (ex && ex.nlm_source_id && ex.nlm_status !== 'removed_from_drive'){
        ex.nlm_status = 'removed_from_drive'; stats.removed_marked++; dirty = true;
      } else if (ex && !ex.nlm_source_id){
        var idx = objs.indexOf(ex); if (idx >= 0){ objs.splice(idx,1); dirty = true; _splice++; }
      }
      return;
    }
    var f = d.file || {};
    var entry = { drive_id:d.id, name:f.name||'', mime:f.mimeType||'',
      md5:f.md5Checksum||'', modified_time:f.modifiedTime||'',
      cat: nameById[f.parent] || '', sohieu: sohieuFromName_(f.name||'') };
    if (ex){
      var changed = (entry.md5 && entry.md5 !== ex.md5) ||
                    (entry.modified_time && entry.modified_time !== ex.modified_time);
      Object.keys(entry).forEach(function(k){ if (entry[k]) ex[k] = entry[k]; });
      if (changed && ex.nlm_source_id && ex.nlm_status === 'synced'){
        ex.nlm_status = 'stale'; stats.staled++;
      }
    } else {
      var o = {}; REG_COLS_.forEach(function(c){ o[c] = entry[c] || ''; });
      o.registered_at = new Date().toISOString();
      objs.push(o);
    }
    stats.upserted++; dirty = true;
  });
  // KI-27: số dòng bị splice là phép CO CHỦ Ý của delta-pull ⇒ khai để không bị chặn nhầm;
  // nếu Drive scan lỗi khiến splice vọt lên bất thường thì chốt chặn vẫn bắt (lost > expectShrink).
  if (dirty) regWriteAll_(objs, { expectShrink: _splice });
  return stats;
  });
}

/* ---------------- 8.5 FIND hợp nhất (3 tầng tốc độ) ---------------- */
/**
 * GET/POST { action:'find', q, max?, refresh? }
 * Tầng 1 — số hiệu trong q → tra index registry (~ms, sau cold-load).
 * Tầng 2 — keyword khớp tên chuẩn (AND các token, stripVN) → top N.
 * Tầng 3 — fallback fullText contains toàn corpus (~0.5–1.5s, KI-04 đã lo scope).
 * Mỗi kết quả kèm nlm_source_id để bước verify/scoped-query nối liền mạch.
 */
function doFind_(p){
  var q = String(p.q||'').trim();
  if (!q) return { ok:false, error:'Thiếu q' };
  var MAX = Math.min(Number(p.max)||cfgNum_('TL_FIND_MAX',10), 50);
  var objs = regReadAll_(String(p.refresh)==='true');

  var so = findSoHieuInQuery_(q);
  if (so){
    // v2.12.1: index số hiệu = sohieu ∪ tách(goc). VBHN khai goc='goc;sdbs1;sdbs2' sẽ
    // TRÚNG khi người dùng hỏi theo luật gốc hoặc luật sửa đổi (vụ VBHN 89 NSNN bị miss).
    var hit = objs.filter(function(o){
      if (o.sohieu === so) return true;
      if (o.goc){
        var gs = String(o.goc).split(';');
        for (var gi = 0; gi < gs.length; gi++){
          if (normSoHieu_(gs[gi]) === so) return true;
        }
      }
      return false;
    });
    if (hit.length) return { ok:true, tier:'sohieu', sohieu:so, count:hit.length, rows:hit.sort(registryRankCompare_).slice(0,MAX) };
  }
  var toks = stripVN_(q).toLowerCase().split(/[^a-z0-9]+/).filter(function(t){ return t.length >= 2; });
  if (toks.length){
    var scored = [];
    objs.forEach(function(o){
      var nm = stripVN_(o.name).toLowerCase();
      var all = toks.every(function(t){ return nm.indexOf(t) >= 0; });
      if (all) scored.push(o);
    });
    if (scored.length) return { ok:true, tier:'name', count:scored.length, rows:scored.sort(registryRankCompare_).slice(0,MAX) };
  }
  // Tầng 3 — fullText (chỉ khi 2 tầng trên miss)
  var ft = driveSearch_({ q: "fullText contains '" + qEsc_(q) + "'", scope:'corpus', pageSize:MAX });
  var byId2 = {}; objs.forEach(function(o){ byId2[o.drive_id] = o; });
  // v2.18.2 KI-29: doSearch_ trả 'matches' (không 'files') ⇒ tầng 3 fulltext xưa luôn rỗng. Đọc cả hai.
  var rows = (ft.files||ft.matches||[]).map(function(f){
    return byId2[f.id] || { drive_id:f.id, name:f.name, mime:f.mimeType, cat:'', sohieu:'', nlm_source_id:'' };
  });
  return { ok:true, tier:'fulltext', count:rows.length, rows:rows };
}

/* ---------------- 8.6 REGEN2 + MANIFEST EXPORT ---------------- */
/**
 * POST { action:'regen2', confirm:'yes', refresh?, manifestScope:'own|inherited',
 *        rootFolderId?, profileName?, categoriesMode?, confirmInherited?, confirmBlowup? }
 * Quét corpus bằng files.list OR-parents theo lô (3–6 call cho ~750 file, thay
 * iterator DriveApp 30–60s của regen cũ) → merge GIỮ nlm_* (KI-21) → ghi Sheet
 * qua tab tạm + swap (KI-17) → _meta {treeHash v2, count, generatedAt}.
 */
function profileOwnFolders_(root){
  var out = { ids:[root], nameById:{} };
  out.nameById[root] = '(root)';
  var queue = [root], seen = {}, qi = 0, MAX_FOLDERS = 2000;
  seen[root] = true;
  while (qi < queue.length){
    if (queue.length > MAX_FOLDERS) throw new Error('PROFILE_OWN_TREE_TOO_LARGE: >'+MAX_FOLDERS+' folders');
    var parent = queue[qi++], tok = null;
    do {
      var req = {
        q:"'"+parent+"' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        pageSize:1000, fields:'nextPageToken,files(id,name)',
        supportsAllDrives:true, includeItemsFromAllDrives:true
      };
      if (tok) req.pageToken = tok;
      var res = Drive.Files.list(req);
      (res.files||[]).forEach(function(f){
        if (seen[f.id]) return;
        seen[f.id] = true;
        var parentPath = out.nameById[parent] || '(root)';
        out.ids.push(f.id);
        out.nameById[f.id] = parentPath === '(root)' ? f.name : parentPath + '/' + f.name;
        queue.push(f.id);
      });
      tok = res.nextPageToken;
    } while (tok);
  }
  return out;
}
function profileOwnCount_(objs){
  return (objs||[]).filter(function(o){
    var rk = String(o.row_kind || 'own').toLowerCase();
    return rk === 'own' || rk === 'overflow';
  }).length;
}
function profileScopeBlowup_(oldOwnCount, newOwnCount){
  var threshold = Math.max(2 * oldOwnCount, oldOwnCount + 50);
  return { blowup:newOwnCount > threshold, threshold:threshold };
}
function doRegen2_(p){
  if (String(p.confirm) !== 'yes') return { ok:false, error:"Cần confirm=yes (thao tác ghi đè registry)" };
  var t0 = Date.now();
  var profileName = String(p.profileName || _REQ_PROFILE_NAME_ || '').trim() || 'vbqppl';
  var isProfile = !!_REQ_REGISTRY_ID_ || profileName !== 'vbqppl';
  var categoriesMode = String(p.categoriesMode || _REQ_CATEGORIES_MODE_ || '').trim().toLowerCase();
  var manifestScope = String(p.manifestScope || _REQ_MANIFEST_SCOPE_ ||
    (isProfile ? 'own' : 'inherited')).trim().toLowerCase();
  if (manifestScope !== 'own' && manifestScope !== 'inherited')
    return {ok:false, error:'manifestScope phải là own|inherited'};
  if (isProfile && categoriesMode === 'inherit' && String(p.confirmInherited) !== 'yes')
    return {ok:false, error:'PROFILE_INHERIT_TOUCHED_DRIVE_CONFIRM_REQUIRED',
      required:'confirmInherited=yes', profile:profileName, manifest_scope:manifestScope};
  if (isProfile && manifestScope === 'inherited' && String(p.confirmInherited) !== 'yes')
    return {ok:false, error:'PROFILE_INHERITED_SCOPE_CONFIRM_REQUIRED',
      required:'confirmInherited=yes', profile:profileName};
  var ownRoot = String(p.rootFolderId || _REQ_ROOT_FOLDER_ID_ || '').trim();
  if (isProfile && manifestScope === 'own' && !ownRoot)
    return {ok:false, error:'PROFILE_OWN_ROOT_REQUIRED', profile:profileName,
      required:'rootFolderId'};
  var HOUSEKEEPING = [ cfg_('TL_MANIFEST_NAME','tra_luat_manifest.json'),
    cfg_('TL_REGSHEET_NAME','tra_luat_registry'), 'tra_luat_config.json' ];
  // categories=inherit chỉ phục vụ organize/lookup fallback. regen2 own tuyệt đối không lấy category tree VBQPPL.
  var ownScope = isProfile && manifestScope === 'own';
  var corpus = ownScope ? profileOwnFolders_(ownRoot) : corpusFolders_(String(p.refresh)==='true');
  var scanned = [];
  var FIELDS = 'nextPageToken,files(id,name,mimeType,size,md5Checksum,modifiedTime,parents,appProperties)';
  // KI-27 (đo 12/06/2026): q OR-nhiều-parent trả SNAPSHOT INDEX CŨ với file vừa move
  // (~30-60 phút mới thấy), trong khi q 1-parent luôn tươi → quét TỪNG folder một.
  // Chậm hơn (~N query) nhưng ĐÚNG; pageToken chỉ set khi có (KHÔNG undefined — Invalid Value).
  for (var ci = 0; ci < corpus.ids.length; ci++){
    var qq = "'" + corpus.ids[ci] + "' in parents" +
             " and mimeType!='application/vnd.google-apps.folder' and trashed=false";
    var tok = null;
    do {
      var reqp = { q:qq, pageSize:1000, fields:FIELDS,
                   supportsAllDrives:true, includeItemsFromAllDrives:true };
      if (tok) reqp.pageToken = tok;
      var res = Drive.Files.list(reqp);
      (res.files||[]).forEach(function(f){
        // BUG THẬT bắt được nhờ test: ROOT chứa cả file "nội trợ" (manifest JSON,
        // registry sheet, config mirror) — không loại thì regen tự ăn sổ sách của
        // chính mình vào registry như văn bản pháp luật. Shortcut cũng loại
        // (con trỏ — văn bản thật đã đăng ký ở vị trí primary, KI-05).
        if (f.mimeType === 'application/vnd.google-apps.shortcut') return;
        if (HOUSEKEEPING.indexOf(f.name) >= 0) return;
        var ap = f.appProperties || {};
        var _pathName = corpus.nameById[(f.parents||[])[0]] || '';
        var _cl;
        if (ownScope){
          var _lowPath = String(_pathName||'').toLowerCase().split('/');
          var _blocked = _lowPath.indexOf('_hop_nap') >= 0 || _lowPath.indexOf('_goc') >= 0;
          _cl = {register:!_blocked, corpus:false, loai:'thuong'};
        } else {
          _cl = classifyScanFolder_(_pathName);              // v2.14.0
        }
        if (!_cl.register) return;                            // _HOP_NAP / _goc / container / ngoài corpus → bỏ qua
        scanned.push({ drive_id:f.id, src_id:'', sohieu: normSoHieu_(ap.sohieu || ap.soHieu || '') || sohieuFromName_(f.name),
          loai: ap.loai || _cl.loai || '', name:f.name, cat: _pathName,
          mime:f.mimeType, md5:f.md5Checksum||'', size:String(f.size||''),
          modified_time:f.modifiedTime||'', linhvuc: ap.linhvuc||'', goc: ap.goc||'',
          nlm_source_id:'', nlm_status:'', nlm_pushed_at:'', verified:'', registered_at:'', note:'',
          corpus: (_cl.corpus && !_isNonVbMime_(f.mimeType)) ? 'true' : 'false', nlm_notebook_id:'', row_kind:'own' }); // v2.14.0 + v2.21.2h + 2026-06-26 mime-guard
      });
      tok = res.nextPageToken;
    } while (tok);
  }
  // Ghép cặp GDoc ↔ bản gốc nhị phân cùng base-name trong cùng cat → src_id
  var byKey = {};
  scanned.forEach(function(o){
    if (o.mime === 'application/vnd.google-apps.document') byKey[o.cat + '|' + o.name] = o;
  });
  scanned = scanned.filter(function(o){
    if (o.mime === 'application/vnd.google-apps.document') return true;
    var base = o.name.replace(/\.(docx?|pdf)$/i,'');
    var g = byKey[o.cat + '|' + base];
    if (g){ g.src_id = o.drive_id; if (!g.md5) g.md5 = o.md5; return false; } // gốc gắn vào dòng GDoc
    return true; // file nhị phân không có GDoc cặp → vẫn giữ dòng riêng
  });

  // KI-25 (v2.21.2p): ôm lock từ ĐỌC tới GHI. CHỦ Ý không ôm cả phần quét Drive phía trên —
  // quét chậm (hàng phút), ôm lock suốt sẽ làm mọi request ghi khác hết hạn tryLock 30s.
  var _rg2 = withRegLock_(function(){
  var existing = regReadAll_(true);
  var refs = [], mergeBase = existing;
  if (ownScope){
    // Ref trỏ VBQPPL dùng chung không nằm trong cây own; phải giữ nguyên, không đánh removed_from_drive.
    refs = existing.filter(function(o){ return String(o.row_kind||'own').toLowerCase() === 'ref'; });
    mergeBase = existing.filter(function(o){ return String(o.row_kind||'own').toLowerCase() !== 'ref'; });
  }
  var merged = regenMerge_(scanned, mergeBase);
  if (ownScope && refs.length) merged.objs = merged.objs.concat(refs);
  var oldOwnCount = profileOwnCount_(existing);
  var newOwnCount = profileOwnCount_(merged.objs);
  var guard = profileScopeBlowup_(oldOwnCount, newOwnCount);
  if (isProfile && guard.blowup && String(p.confirmBlowup) !== 'yes'){
    return {
      ok:false, error:'PROFILE_MANIFEST_SCOPE_BLOWUP', code:'PROFILE_MANIFEST_SCOPE_BLOWUP',
      profile:profileName, manifest_scope:manifestScope, categories_mode:categoriesMode,
      old_own_count:oldOwnCount, new_own_count:newOwnCount, threshold:guard.threshold,
      required:'confirmBlowup=yes', wrote_registry:false,
      note:'Dừng trước regWriteAll_. Kiểm rootFolderId/manifestScope; không dùng cây categories kế thừa để populate profile.'
    };
  }
  // KI-27: regen2 CHÍNH là đường đã xóa 766 dòng registry nền 30-06 (profile registryDocId rỗng).
  // Chốt chặn thảm họa nay áp cả ở đây: mất >100 dòng hoặc >50% ⇒ TỪ CHỐI, buộc khai expect_shrink.
  regWriteAll_(merged.objs, { expectShrink: Number(p.expect_shrink || 0) });

  // v2.14.0: treeHash CHỈ trên corpus (loại dòng loai=thuong / corpus!=true) — VBHN/45-chủ-đề/treeHash là corpus-only
  var corpusObjs = manifestHashObjs_(merged.objs);
  var th = treeHashV2_(corpusObjs);
  var meta = regSS_().getSheetByName(REG_META_TAB_);
  meta.getRange(1,1,5,2).setValues([
    ['treeHash', th], ['count', String(merged.objs.length)],
    ['corpus_count', String(corpusObjs.length)],
    ['generatedAt', new Date().toISOString()], ['version', APP_VERSION] ]);
  SpreadsheetApp.flush();
  return { ok:true, treeHash:th, count:merged.objs.length, corpus_count:corpusObjs.length,
           profile:profileName, manifest_scope:manifestScope, categories_mode:categoriesMode,
           old_own_count:oldOwnCount, new_own_count:newOwnCount,
           blowup_confirmed:!!(guard.blowup && String(p.confirmBlowup)==='yes'),
           stats:merged.stats,
           note:'Chạy tiếp manifest_export để cập nhật JSON snapshot cho skill.' };
  });
  if (_rg2 && _rg2.ok === false) return _rg2;          // guard blowup trả sớm — giữ nguyên hình dạng
  _rg2.elapsedMs = Date.now() - t0;
  return _rg2;
}
/** Suy số hiệu từ TÊN file BẢO THỦ — chỉ khi tên bắt đầu bằng <Loại>_<sốhiệu>_…
 *  hoặc dạng raw VBHN "<num>_VBHN-<CQ>_<digits>". Trả '' khi không chắc
 *  (KHÔNG đoán: bỏ qua token viện dẫn giữa tên, file tạm, *.signed.pdf, chỉ-mục).
 *  Đã kiểm trên 706 tên thật: 380/405 khớp, 0 dương-tính-giả. */
function parseSoHieuFromName_(name){
  if (!name) return '';
  var n = String(name).replace(/\.(docx?|pdf|txt|html?)$/i, '');
  var LOAI   = '(?:Luat|BL|HP|VBHN|N[ĐD]|TT|TTLT|NQ|KL|CT|QĐ|QD|PL|LCT|SL)';
  var SOHIEU = '(\\d+(?:-\\d{4})?-[A-ZĐ0-9]+(?:-[A-ZĐ0-9]+)*)';   // số hiệu KHÔNG chứa '_'
  var m = n.match(new RegExp('^' + LOAI + '_' + SOHIEU + '(?:_|\\.|$)'));
  if (m){
    var sh = m[1];
    if (/^VBHN_/.test(n) && sh.indexOf('VBHN') === -1){   // "04-BGDDT" -> "04-VBHN-BGDDT"
      var pp = sh.split('-'); sh = pp[0] + '-VBHN-' + pp.slice(1).join('-');
    }
    return sh;
  }
  m = n.match(/^(\d+)_VBHN-([A-ZĐ]+)(?:_m)?_\d{6,}/);       // raw: "88_VBHN-VPQH_670747"
  if (m) return m[1] + '-VBHN-' + m[2];
  return '';
}


// v2.21.2c: canonical hóa VBHN bị lưu ngắn NN-VPQH và suy năm từ tên/metadata manifest.
function isVbhnEntry_(o){
  var txt = [o.loai||'', o.sohieu||'', o.name||'', o.nlm_title||'', o.title_vn||''].join(' ').toUpperCase();
  return txt.indexOf('VBHN') >= 0 || txt.indexOf('VAN BAN HOP NHAT') >= 0;
}
function canonManifestSoHieu_(sh, o){
  sh = normSoHieu_(sh || '');
  if (isVbhnEntry_(o) && /^\d{1,4}-VPQH$/.test(sh)) sh = sh.replace('-VPQH','-VBHN-VPQH');
  return sh;
}
function issueYearFromTextSafe_(txt){
  txt = String(txt || '');
  var ascii = txt.normalize ? txt.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').replace(/Đ/g,'D').toLowerCase() : txt.toLowerCase();
  var pats = [
    /(?:ngày|ngay)\s+\d{1,2}\s*(?:\/|-|\s+tháng\s+|\s+thang\s+)\s*\d{1,2}\s*(?:\/|-|\s+năm\s+|\s+nam\s+)(19\d{2}|20\d{2})/i,
    /(?:năm|nam|issue[_\s-]*year|issued[_\s-]*year|nam[_\s-]*ban[_\s-]*hanh)\D{0,8}(19\d{2}|20\d{2})/i,
    /(?:^|[_\s.-])(19\d{2}|20\d{2})(?=$|[_\s.-])/i
  ];
  for (var i=0;i<pats.length;i++){ var m = ascii.match(pats[i]); if (m) return m[1]; }
  return '';
}
function issueYearFromEntry_(o){
  // v2.21.2d: KHÔNG lấy năm bất kỳ trong tukhoa/trich yếu vì dễ nhầm năm của luật gốc (84/2015, 22/2019...).
  var explicit = o.issue_year || o.nam_ban_hanh || o.issued_year || o.year || o.nam || '';
  if (explicit){
    var y0 = issueYearFromTextSafe_(explicit);
    if (y0) return y0;
    var m0 = String(explicit).match(/^\s*(19\d{2}|20\d{2})\s*$/);
    if (m0) return m0[1];
  }
  var yDate = issueYearFromTextSafe_(o.ngay_ban_hanh || o.ngayBanHanh || o.ngaybanhanh || o.issued_date || o.issue_date || o.date || '');
  if (yDate) return yDate;
  var yName = issueYearFromTextSafe_([o.name||'', o.nlm_title||'', o.title_vn||''].join(' '));
  return yName || '';
}

function doManifestExport_(p){
  var objs = regReadAll_(true);

  function entryOf_(o){
    // so_hieu: ưu tiên registry; trống -> parse từ tên (đánh dấu nguồn suy luận)
    var sh = (o.sohieu || '').toString().trim();
    var shSrc = '';
    if (sh){ sh = canonManifestSoHieu_(sh, o); shSrc = 'registry'; }
    else {
      var parsed = parseSoHieuFromName_(o.name);
      if (parsed){ sh = canonManifestSoHieu_(parsed, o); shSrc = 'parsed'; }
    }
    // SCHEMA CHUẨN: MỌI entry có ĐỦ khóa (rỗng '' nếu thiếu) — không dùng undefined để khỏi bị omit
    return {
      id: o.drive_id || '', gdoc_id: o.drive_id || '', src_id: o.src_id || '',
      name: o.name || '', mime: o.mime || '', cat: o.cat || '', md5: o.md5 || '',
      so_hieu: sh, so_hieu_src: shSrc, issue_year: issueYearFromEntry_(o),
      loai: o.loai || '', linhvuc: o.linhvuc || '', linhvuc_list: o.linhvuc_list || '',
      goc: o.goc || '', sua_doi: o.sua_doi || '', hieuluc: o.hieuluc || '',
      nlm_source_id: o.nlm_source_id || '', nlm_status: o.nlm_status || '',
      nlm_title: o.nlm_title || '', nlm_notebook_id: o.nlm_notebook_id || '',
      verified: o.verified || '', title_vn: o.title_vn || '', tukhoa: o.tukhoa || '',
      corpus: (o.corpus === undefined || o.corpus === '') ? '' : o.corpus,
      row_kind: o.row_kind || '',   // 2.21.2m D3: RAW — export không che blank thành 'own'
      modified_time: o.modified_time || ''
    };
  }

  var entries = objs.map(entryOf_);
  var corpusObjs = manifestHashObjs_(objs);
  var nParsed  = 0, nMissing = 0;
  for (var i = 0; i < entries.length; i++){
    if (entries[i].so_hieu_src === 'parsed') nParsed++;
    if (!entries[i].so_hieu) nMissing++;
  }

  var out = {
    version: APP_VERSION, schema: 'uniform-v1', generatedAt: new Date().toISOString(),
    treeHash: treeHashV2_(corpusObjs), corpus_count: corpusObjs.length, count: objs.length,
    so_hieu_parsed: nParsed, so_hieu_missing: nMissing,
    entries: entries
  };

  var nm   = cfg_('TL_MANIFEST_NAME', 'tra_luat_manifest.json');
  var blob = Utilities.newBlob(JSON.stringify(out, null, 1), 'application/json', nm);
  var id;
  if (_REQ_MANIFEST_ID_){
    // v2.21.2f: profile truyền manifestId → ghi ĐÚNG file đó; KHÔNG đụng TL_MANIFEST_ID nền (VBQPPL).
    Drive.Files.update({}, _REQ_MANIFEST_ID_, blob, { supportsAllDrives:true });
    id = _REQ_MANIFEST_ID_;
  } else {
    var loc  = locateManifest_();
    if (loc){ Drive.Files.update({}, loc.id, blob, { supportsAllDrives:true }); id = loc.id; }
    else {
      var created = Drive.Files.create({ name:nm, parents:[rootId_()] }, blob,
        { supportsAllDrives:true, fields:'id' });
      id = created.id;
    }
    PropertiesService.getScriptProperties().setProperty('TL_MANIFEST_ID', id);
  }
  return { ok:true, manifestId:id, treeHash:out.treeHash, count:out.count, corpus_count:out.corpus_count,
           so_hieu_parsed:nParsed, so_hieu_missing:nMissing, schema_version:APP_VERSION,
           registry_scope:(_REQ_REGISTRY_ID_ || 'base'), manifest_scope:(_REQ_MANIFEST_ID_ || 'base') };
}

/* ---------------- 8.7 SELFTEST v2.12 ---------------- */
function _selftest_v212(){
  var rep = _selftest_v211();          // chạy lại nền v2.11
  rep.v212 = {};
  rep.v212.normSoHieu = normSoHieu_('113/2025/qh15') === '113-2025-QH15' &&
                        normSoHieu_('95/2026/NĐ-CP') === '95-2026-ND-CP';
  rep.v212.sohieuFromName = sohieuFromName_('Luat_113-2025-QH15_DAN_SO') === '113-2025-QH15';
  rep.v213_6 = { nlm_title_col: REG_COLS_.indexOf('nlm_title') >= 0,
                 nlm_title_kept: REG_NLM_KEEP_.indexOf('nlm_title') >= 0 };
  var th1 = treeHashV2_([{drive_id:'a',md5:'1',modified_time:'t'},{drive_id:'b',md5:'2',modified_time:'t'}]);
  var th2 = treeHashV2_([{drive_id:'b',md5:'2',modified_time:'t'},{drive_id:'a',md5:'1',modified_time:'t'}]);
  rep.v212.treeHashOrderFree = th1 === th2;
  try { var ss = regSS_(); rep.v212.sheet = ss.getId();
    rep.v212.rows = regReadAll_(true).length; }
  catch(e){ rep.v212.sheet = 'ERR ' + String(e).slice(0,120); }
  Logger.log(JSON.stringify(rep, null, 2));
  return rep;
}


/* ============================================================
 * v2.14.0 — PHÂN LOẠI FOLDER QUÉT (regen2) + BOOTSTRAP
 * Phân loại theo SEGMENT ĐẦU của pathName (corpus.nameById):
 *   '(root)' | 'NN_...[/con]' | '_HOP_NAP' | 'Van_ban_thuong[/<dự án>]' | '.../_goc' | 'QUARANTINE...'
 * ============================================================ */
var SCAN_CAT_RE_ = /^(\d{2})[_\-]/;
// 2026-06-26: mime KHÔNG phải văn bản pháp luật (json/bảng tính/csv/slide) → KHÔNG tính corpus
//   (VBQPPL chỉ là Google Doc/PDF/Word). Tránh file cấu hình/chỉ mục/backup ở root bị đếm nhầm.
function _isNonVbMime_(m){
  return /json|spreadsheet|\.sheet|ms-excel|csv|presentation|\.script/i.test(String(m || ''));
}

function classifyScanFolder_(pathName){
  var segs = String(pathName||'').split('/').filter(function(s){ return s; });
  var low  = segs.map(function(s){ return s.toLowerCase(); });
  if (low.indexOf('_hop_nap') >= 0) return { register:false, corpus:false, loai:'' };
  if (low.indexOf('_goc')     >= 0) return { register:false, corpus:false, loai:'' };
  if (!segs.length || segs[0] === '(root)') return { register:true, corpus:true, loai:'' };
  var first = segs[0];
  // 2026-06-25 FIX: QUARANTINE = CÁCH LY khỏi corpus → giữ dòng (register) nhưng corpus:FALSE.
  //   Trước đây gộp chung với cat hợp lệ nên file quarantine VẪN bị đếm vào corpus (dup/junk không rời corpus).
  if (/quarantine/i.test(first)) return { register:true, corpus:false, loai:'' };
  if (SCAN_CAT_RE_.test(first)) return { register:true, corpus:true, loai:'' };
  if (first === 'Van_ban_thuong'){
    if (segs.length === 1) return { register:false, corpus:false, loai:'' };       // container
    return { register:true, corpus:false, loai:'thuong' };                          // dự án
  }
  return { register:false, corpus:false, loai:'' };                                 // folder ngoài corpus
}

/**
 * POST { action:'bootstrap' } — idempotent:
 *   • tạo/kiểm VBQPPL gốc (nếu rootFolderId trống/bị xóa → tạo mới + ghi config mirror)
 *   • find-or-create _HOP_NAP, Van_ban_thuong
 *   • tự-kiểm ghi (tạo file probe → trash)
 *  KHÔNG probe private (share LUÔN bật ở luồng push — đặc tả 1.12.2 §3).
 */
function doBootstrap_(p){
  var rootId = rootId_(), rootOk = false, created = {};
  try { var rf = DriveApp.getFolderById(rootId); if (rf && !rf.isTrashed()) rootOk = true; } catch(e){}
  if (!rootOk){
    var nf = DriveApp.createFolder('VBQPPL'); rootId = nf.getId(); created.root = rootId;
    PropertiesService.getScriptProperties().setProperty('TL_ROOT_ID', rootId);
    try { CacheService.getScriptCache().remove(CAT_CACHE_KEY); } catch(e){}
    try { V211_.corpus = null; } catch(e){}
    try { doWriteConfig_({}); } catch(e){}   // đồng bộ mirror nếu có
  }
  var root = DriveApp.getFolderById(rootId);
  var hopnap = findOrCreateChild_(root, '_HOP_NAP');
  var vbt    = findOrCreateChild_(root, 'Van_ban_thuong');
  var writable = false, probeId = null;
  try {
    var probe = root.createFile('._tl_bootstrap_probe.txt', 'ok', 'text/plain');
    probeId = probe.getId(); probe.setTrashed(true); writable = true;   // trash = đảo ngược được
  } catch(e){ writable = false; }
  return { ok:true, version:APP_VERSION, rootId:rootId, writable:writable, probeTrashedId:probeId,
           inboxFolderId:hopnap.getId(),
           inboxFolderUrl:'https://drive.google.com/drive/folders/'+hopnap.getId(),
           vanBanThuongId:vbt.getId(), created:created,
           note:'bootstrap idempotent; share LUÔN bật ở luồng push (KHÔNG probe private).' };
}

function findOrCreateChild_(parent, name){
  var it = parent.getFoldersByName(name);
  if (it.hasNext()) return it.next();
  return parent.createFolder(name);
}


/* ============================================================
 * v2.15.0 — fetch_url_to_drive (DISCOVERY auto-fetch lane)
 * Chỉ tải URL UNGATED trỏ .doc/.docx về _HOP_NAP, rồi convert .docx + GDoc.
 * KHÔNG xử lý credential; gặp HTML/login/redirect-gate → trả {ok:false, reason:'gated'}.
 * Router đã gác token trước khi vào đây.
 * ============================================================ */
var FETCH_MAX_MB_ = 25;
var FETCH_GATED_BLOCKLIST_ = ['thuvienphapluat.vn', 'luatvietnam.vn'];

function doFetchUrlToDrive_(p){
  var url = String(p.url || '').trim();
  if (!/^https?:\/\//i.test(url)) return ({ok:false, error:'url không hợp lệ'});
  var host = (url.match(/^https?:\/\/([^\/]+)/i) || [,''])[1].toLowerCase();
  for (var i=0;i<FETCH_GATED_BLOCKLIST_.length;i++){
    if (host.indexOf(FETCH_GATED_BLOCKLIST_[i]) >= 0)
      return ({ok:false, reason:'gated', error:'Nguồn login-gate — tải tay rồi thả _HOP_NAP'});
  }
  // chỉ chấp nhận .doc/.docx theo đuôi (A2); ct kiểm thêm sau khi fetch
  var extOk = /\.docx?(?:$|\?)/i.test(url);

  var resp;
  try {
    resp = UrlFetchApp.fetch(url, {followRedirects:true, muteHttpExceptions:true,
                                   validateHttpsCertificates:true});
  } catch(e){ return ({ok:false, error:'fetch lỗi: '+e}); }
  var code = resp.getResponseCode();
  if (code !== 200) return ({ok:false, error:'HTTP '+code});

  var headers = resp.getAllHeaders() || {};
  var ct = String(headers['Content-Type'] || headers['content-type'] || '').toLowerCase();
  if (ct.indexOf('text/html') >= 0)
    return ({ok:false, reason:'gated', error:'Trả HTML (nghi trang login) — không phải file doc/docx'});
  var ctDoc = (ct.indexOf('msword') >= 0) || (ct.indexOf('wordprocessingml') >= 0) ||
              (ct.indexOf('application/octet-stream') >= 0 && extOk);
  if (!ctDoc && !extOk)
    return ({ok:false, error:'Content-Type không phải doc/docx ('+ct+') — chỉ auto-fetch doc/docx'});

  var blob = resp.getBlob();
  var bytes = blob.getBytes();
  if (bytes.length > FETCH_MAX_MB_ * 1024 * 1024)
    return ({ok:false, error:'File > '+FETCH_MAX_MB_+'MB — tải tay'});

  var isDoc = (ct.indexOf('msword') >= 0) || /\.doc(?:$|\?)/i.test(url) && !/\.docx(?:$|\?)/i.test(url);
  var name = decodeURIComponent((url.split('?')[0].split('/').pop()) || 'taive');
  if (!/\.docx?$/i.test(name)) name += (isDoc ? '.doc' : '.docx');

  var folderId = inboxFolderId_();
  var folder = DriveApp.getFolderById(folderId);

  // 1) lưu bản gốc tải về
  var origFile = folder.createFile(blob.setName(name));
  var origId = origFile.getId();

  // 2) convert → GDoc (server-side); .doc cũng ra GDoc
  var gdocId = null, docxId = null;
  try {
    var gdoc = Drive.Files.create(
      {name: name.replace(/\.docx?$/i,''), mimeType:'application/vnd.google-apps.document',
       parents:[folderId]}, blob, {supportsAllDrives:true, fields:'id,name'});
    gdocId = gdoc.id;
  } catch(e){ return ({ok:false, error:'convert GDoc lỗi: '+e, fileId:origId}); }

  // 3) nếu là .doc → còn phải xuất .docx (A2: ".doc → .docx + GDoc")
  if (isDoc && gdocId){
    try {
      var exp = UrlFetchApp.fetch(
        'https://www.googleapis.com/drive/v3/files/'+gdocId+
        '/export?mimeType=' + encodeURIComponent('application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
        {headers:{Authorization:'Bearer '+ScriptApp.getOAuthToken()}, muteHttpExceptions:true});
      if (exp.getResponseCode()===200){
        var dblob = exp.getBlob().setName(name.replace(/\.docx?$/i,'')+'.docx');
        docxId = folder.createFile(dblob).getId();
      }
    } catch(e){ /* docx phụ — không chặn luồng */ }
  }

  return ({ok:true, version:APP_VERSION, fileId:origId, gdocId:gdocId, docxId:docxId,
    name:name, isDoc:isDoc, converted:true,
    note:'Đã về _HOP_NAP — tiếp tục dedup/VBHN-first rồi source_add (GDoc).'});
}


/* ============================================================
 * v2.16.0 — KHỐI NLM PREFLIGHT (server-side dedup/slot)
 * Đã gắn 3 case ở dispatchAction_; whitelist xem ghi chú cuối file.
 * ============================================================ */

var NLM_PRO_CAP_ = 300;                 // (b) Pro tier = 300 nguồn/notebook
var NLM_VERIFY_LIVE_THRESHOLD_ = 10;    // remaining ≤ ngưỡng ⇒ khuyên đối chiếu notebook_get
// v2.21.2e (đa-corpus): notebook NỀN (VBQPPL). Dòng registry có nlm_status nhưng RỖNG nlm_notebook_id
// (legacy đẩy lên VBQPPL trước khi có cột) được quy về notebook nền này khi đếm slot — KHÔNG đếm vào
// notebook dự án khác (sửa NOTEBOOK_FULL giả), nhưng VẪN đếm đúng cho VBQPPL mà không cần backfill hàng loạt.
// Truyền p.baseNotebookId để override.
var NLM_DEFAULT_NOTEBOOK_ = '743ed200-2e55-4673-b7a0-9bfd13b41ce6';

// ===== v2.21.2f (Cách B — registry/manifest RIÊNG theo profile) =====
// 1 deployment (giữ URL+token); mỗi request có thể truyền registryDocId/manifestId. Thiếu ⇒ VBQPPL nền.
var BASE_REGISTRY_DOC_ID_ = '1mATGFhaW0e_CYienAD80DsTS1K4zfJNlTAx-DsHaCD8'; // registry Sheet VBQPPL (nền)
var BASE_MANIFEST_ID_     = '1d8Pau1x-Qeq0i8ClQnxuTMohGNf6GEeI';            // manifest VBQPPL (nền)
// Biến request-scoped: main_() set 1 lần từ p; mọi truy cập registry/manifest đọc lại qua resolveRegistry_/resolveManifest_.
var _REQ_REGISTRY_ID_ = '';
var _REQ_MANIFEST_ID_ = '';
var _REQ_PROFILE_NAME_ = '';
var _REQ_ROOT_FOLDER_ID_ = '';
var _REQ_CATEGORIES_MODE_ = '';
var _REQ_MANIFEST_SCOPE_ = '';
function setCorpusScope_(p){
  _REQ_REGISTRY_ID_ = String((p && (p.registryDocId || p.registry_doc_id)) || '').trim();
  _REQ_MANIFEST_ID_ = String((p && (p.manifestId    || p.manifest_id))     || '').trim();
  _REQ_PROFILE_NAME_ = String((p && (p.profileName || p.profile_name)) || '').trim();
  _REQ_ROOT_FOLDER_ID_ = String((p && (p.rootFolderId || p.root_folder_id)) || '').trim();
  _REQ_CATEGORIES_MODE_ = String((p && (p.categoriesMode || p.categories_mode)) || '').trim();
  _REQ_MANIFEST_SCOPE_ = String((p && (p.manifestScope || p.manifest_scope)) || '').trim();
}
// resolveRegistry_(e): tham số registryDocId → nếu thiếu, VBQPPL nền (tương thích ngược).
function resolveRegistry_(e){
  if (e && e.parameter && e.parameter.registryDocId) return String(e.parameter.registryDocId).trim();
  return _REQ_REGISTRY_ID_ || BASE_REGISTRY_DOC_ID_;
}
function resolveManifest_(e){
  if (e && e.parameter && e.parameter.manifestId) return String(e.parameter.manifestId).trim();
  return _REQ_MANIFEST_ID_ || BASE_MANIFEST_ID_;
}

/* Chuẩn hóa tên cho so khớp BẰNG-TUYỆT-ĐỐI (KHÔNG dùng cho substring). */
function nlmNorm_(s){
  return stripVN_(String(s || ''))
    .toLowerCase()
    .replace(/[^\w\s./:-]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/* Trả khóa số hiệu của 1 dòng registry:
 *   fine   = số–năm–cơquan đã chuẩn hóa (vd 143-2025-QH15, 03-VBHN-VPQH)
 *   coarse = số–năm (bỏ cơ quan) nếu có dạng SO-NAM-... (vd 143-2025); '' nếu VBHN không năm. */
function nlmSohieuKeys_(o){
  var fine = normSoHieu_(o.sohieu) || sohieuFromName_(o.name) || '';
  var coarse = '';
  var m = fine.match(/^(\d{1,4})-((?:19|20)\d{2})(?:-|$)/);
  if (m) coarse = m[1] + '-' + m[2];
  return { fine: fine, coarse: coarse };
}

function nlmIsRemoved_(o){
  var st = String(o.nlm_status || '').toLowerCase();
  return st === 'removed' || st === 'removed_from_drive' || st === 'deleted' ||
         st === 'trash'   || st === 'trashed';
}

function nlmIsSuperseded_(o){
  var hl = stripVN_(String(o.hieuluc || '')).toLowerCase();
  return hl.indexOf('het hieu luc') >= 0 || hl.indexOf('thay the') >= 0 ||
         hl.indexOf('superseded') >= 0  || hl.indexOf('expired') >= 0;
}

function nlmCompactRow_(o){
  return {
    drive_id: o.drive_id || '',
    src_id: o.src_id || '',
    name: o.name || '',
    nlm_title: o.nlm_title || '',
    sohieu: o.sohieu || '',
    loai: o.loai || '',
    cat: o.cat || '',
    mime: o.mime || '',
    md5: o.md5 || '',
    hieuluc: o.hieuluc || '',
    corpus: o.corpus || '',
    row_kind: o.row_kind || '',   // 2.21.2m D3: RAW
    nlm_source_id: o.nlm_source_id || '',
    nlm_status: o.nlm_status || '',
    nlm_notebook_id: o.nlm_notebook_id || ''
  };
}

/* ---------- ĐẾM SLOT (ước lượng từ registry; cap=300) ---------- */
function doNlmSlots_(p){
  var notebookId = String(p.notebookId || p.nlm_notebook_id || '').trim();
  var cap = Number(p.limit || p.maxSlots || p.cap || NLM_PRO_CAP_);
  var refresh = String(p.refresh) === 'true';
  var baseNb = String(p.baseNotebookId || NLM_DEFAULT_NOTEBOOK_ || '').trim(); // v2.21.2e: dòng rỗng quy về VBQPPL nền
  var countRefsRaw = String(p.countRefs || p.count_refs || 'false').toLowerCase();
  var countRefs = countRefsRaw === 'true' || countRefsRaw === '1' || countRefsRaw === 'yes';

  var objs = regReadAll_(refresh);
  var usedRows = objs.filter(function(o){
    if (!o.nlm_source_id) return false;
    if (nlmIsRemoved_(o)) return false;
    if (String(o.row_kind || 'own').toLowerCase() === 'ref' && !countRefs) return false;
    // v2.21.2e (sửa NOTEBOOK_FULL giả): chỉ đếm dòng THUỘC notebook đang hỏi.
    // Dòng rỗng nlm_notebook_id quy về notebook nền (VBQPPL) ⇒ KHÔNG cộng vào notebook dự án khác,
    // nhưng VẪN đếm đúng cho VBQPPL mà không cần backfill toàn bộ registry cũ.
    if (notebookId){
      var _nb  = String(o.nlm_notebook_id || '').trim();
      var _eff = _nb || baseNb;
      if (_eff !== notebookId) return false;
    }
    return true;
  });

  var byStatus = {};
  usedRows.forEach(function(o){
    var st = String(o.nlm_status || 'unknown');
    byStatus[st] = (byStatus[st] || 0) + 1;
  });

  var remaining = Math.max(0, cap - usedRows.length);
  var warnThreshold = Number(p.warnThreshold || p.overflowThreshold || 295);
  return {
    ok: true,
    notebookId: notebookId || null,
    cap: cap,
    used: usedRows.length,
    remaining: remaining,
    full: usedRows.length >= cap,
    near_full: usedRows.length >= warnThreshold,
    warn_threshold: warnThreshold,
    count_refs: countRefs,
    byStatus: byStatus,
    freshness: 'registry-estimate',
    verify_live_recommended: remaining <= NLM_VERIFY_LIVE_THRESHOLD_,
    base_notebook: baseNb || null,
    note: 'used/remaining tính từ registry; cột nlm_* có thể lệch NLM live. ' +
          'v2.21.2e: đếm theo nlm_notebook_id; dòng rỗng quy về base_notebook (VBQPPL). ' +
          'Nếu near_full=true với VBQPPL canonical, định tuyến overflow sang profile/notebook được chỉ định.'
  };
}

/* ---------- DEDUP CHẶT (a) ----------
 * HARD (duplicate): drive_id | src_id | md5 | số hiệu FINE trùng.
 * SOFT (review)   : cùng số+năm khác cơ quan (coarse) | tên BẰNG-TUYỆT-ĐỐI khi cả hai KHÔNG có số hiệu.
 * KHÔNG dùng substring tên ở bất kỳ đâu. */
function doNlmDedup_(p){
  var refresh = String(p.refresh) === 'true';
  var max = Math.min(Number(p.max || 20), 50);

  var driveId = String(p.driveId || p.drive_id || p.fileId || p.gdocId || p.gdoc_id || '').trim();
  var srcId   = String(p.srcId || p.src_id || '').trim();
  var md5      = String(p.md5 || p.md5Checksum || '').trim();
  var notebookId = String(p.notebookId || p.nlm_notebook_id || '').trim();
  var baseNb = String(p.baseNotebookId || NLM_DEFAULT_NOTEBOOK_ || '').trim(); // v2.21.2e: dòng rỗng quy về VBQPPL nền

  var candSohieu = String(p.soHieu || p.sohieu || '').trim();
  var candName   = String(p.name || p.title || p.nlm_title || '').trim();
  var cand = nlmSohieuKeys_({
    sohieu: candSohieu,
    name: candName || findSoHieuInQuery_(candSohieu)
  });
  var candNameNorm = nlmNorm_(candName);

  var objs = regReadAll_(refresh);
  var hard = [], soft = [], pending = [];   // v2.18.1 KI-28: pending = trùng cứng CHƯA trên NLM (không chặn)

  objs.forEach(function(o){
    // v2.21.2e (đa-corpus): chỉ xét dòng THUỘC notebook đang hỏi; dòng rỗng quy về notebook nền (VBQPPL).
    if (notebookId){
      var _nb  = String(o.nlm_notebook_id || '').trim();
      var _eff = _nb || baseNb;
      if (_eff !== notebookId) return;
    }
    if (nlmIsRemoved_(o)) return;

    var keys = nlmSohieuKeys_(o);
    var hardReasons = [], softReasons = [];

    if (driveId && String(o.drive_id || '') === driveId) hardReasons.push('drive_id');
    if (srcId   && String(o.src_id   || '') === srcId)   hardReasons.push('src_id');
    if (md5     && String(o.md5      || '') === md5)     hardReasons.push('md5');
    if (cand.fine && keys.fine && cand.fine === keys.fine) hardReasons.push('sohieu_fine');

    if (!hardReasons.length) {
      if (cand.coarse && keys.coarse && cand.coarse === keys.coarse)
        softReasons.push('sohieu_coarse');
      if (!cand.fine && !keys.fine && candNameNorm &&
          candNameNorm === nlmNorm_(o.name || o.nlm_title))
        softReasons.push('name_exact');
    }

    var rowOnNlm = !!o.nlm_source_id;                 // nlmIsRemoved_ đã loại removed ở trên
    var isSelf = driveId && String(o.drive_id || '') === driveId;

    if (hardReasons.length) {
      var rh = nlmCompactRow_(o); rh.reasons = hardReasons; rh.on_nlm = rowOnNlm;
      if (nlmIsSuperseded_(o)) rh.flag = 'EXISTING_SUPERSEDED';
      // v2.18.1 KI-28: CHỈ dòng ĐANG TRÊN NLM mới là "trùng cứng CHẶN nạp".
      if (rowOnNlm) hard.push(rh);
      else if (!isSelf) { rh.note = 'trùng số hiệu nhưng CHƯA trên NLM — không chặn'; pending.push(rh); }
      // else: self chưa-trên-NLM → bỏ qua hẳn
    } else if (softReasons.length) {
      var rs = nlmCompactRow_(o); rs.reasons = softReasons; rs.on_nlm = rowOnNlm;
      if (nlmIsSuperseded_(o)) rs.flag = 'EXISTING_SUPERSEDED';
      soft.push(rs);
    }
  });

  return {
    ok: true,
    duplicate: hard.length > 0,            // v2.18.1: chỉ trùng-cứng-ĐANG-TRÊN-NLM mới chặn
    count: hard.length,
    hits: hard.slice(0, max),
    pending: pending.slice(0, max),        // v2.18.1: trùng số hiệu chưa lên NLM → REVIEW, không auto-skip
    pending_count: pending.length,
    review: soft.slice(0, max),
    review_count: soft.length,
    cand_key: cand
  };
}

/* ---------- PREFLIGHT: gộp slot + dedup + find, ra quyết định ---------- */
function doNlmPreflight_(p){
  var q = String(p.q || p.soHieu || p.sohieu || p.name || p.title || '').trim();
  var notebookId = String(p.notebookId || p.nlm_notebook_id || '').trim();
  var cap = Number(p.limit || p.maxSlots || p.cap || NLM_PRO_CAP_);
  var refresh = String(p.refresh) === 'true';
  var isNormative = String(p.normative || p.isNormative || p.vbqppl || '').toLowerCase();
  isNormative = isNormative === 'true' || isNormative === '1' || isNormative === 'yes';
  var overflowProfile = String(p.overflowProfile || p.overflow_profile || p.hostProfile || '').trim();
  var overflowNotebookId = String(p.overflowNotebookId || p.overflow_notebook_id || p.hostNotebookId || '').trim();

  var slots = doNlmSlots_({ notebookId: notebookId, cap: cap, refresh: refresh ? 'true' : 'false' });
  var dedup = doNlmDedup_({
    driveId: p.driveId || p.drive_id || p.fileId || p.gdocId || p.gdoc_id || '',
    srcId: p.srcId || p.src_id || '',
    md5: p.md5 || p.md5Checksum || '',
    soHieu: p.soHieu || p.sohieu || '',
    name: p.name || p.title || p.nlm_title || '',
    notebookId: notebookId, refresh: refresh ? 'true' : 'false', max: p.max || 20
  });

  var found = null;
  if (q) {
    try { found = doFind_({ q: q, max: Math.min(Number(p.findMax || 10), 20),
                            refresh: refresh ? 'true' : 'false' }); }
    catch (e) { found = { ok: false, error: String(e && e.message || e) }; }
  }

  var decision = 'ADD', reasons = [];
  if (slots.full && isNormative && (overflowProfile || overflowNotebookId)) {
    decision = 'REVIEW';
    reasons.push('NOTEBOOK_NEAR_FULL_ROUTE_OVERFLOW');
  } else if (slots.full) { decision = 'SKIP'; reasons.push('NOTEBOOK_FULL'); }
  if (dedup.duplicate)   { decision = 'SKIP';   reasons.push('DUPLICATE_IN_REGISTRY'); }
  if (decision === 'ADD' && slots.near_full && isNormative && (overflowProfile || overflowNotebookId)) {
    decision = 'REVIEW';
    reasons.push('NOTEBOOK_NEAR_FULL_ROUTE_OVERFLOW');
  }
  // v2.18.1 KI-28: pending (trùng số hiệu CHƯA trên NLM) → REVIEW, KHÔNG chặn
  if (decision === 'ADD' && dedup.pending_count) { decision = 'REVIEW'; reasons.push('SAMENUM_PENDING_NOT_ON_NLM'); }
  if (decision === 'ADD' && dedup.review_count) { decision = 'REVIEW'; reasons.push('NEAR_MATCH_REVIEW'); }
  if (decision === 'ADD' && slots.verify_live_recommended) reasons.push('VERIFY_SLOTS_LIVE');

  var superseded = (dedup.hits || []).concat(dedup.pending || [], dedup.review || [])
                     .filter(function(r){ return r.flag === 'EXISTING_SUPERSEDED'; });
  if (superseded.length) reasons.push('EXISTING_SUPERSEDED_PRESENT');

  // v2.21.2k: khi ĐỊNH TUYẾN overflow (base đầy/gần-đầy + overflow cấu hình), ĐẾM SLOT CHÍNH SHARD OVERFLOW để
  // KHÔNG khuyên add vào shard ĐÃ ĐẦY (trước đây chỉ đếm base rồi route overflow MÙ — Code.gs bug audit v1.34.46).
  // Chỉ đếm khi THỰC route overflow (reason NEAR_FULL_ROUTE_OVERFLOW) → tiết kiệm 1 lượt regReadAll khi base còn chỗ.
  var overflowSlots = null;
  if (overflowNotebookId && reasons.indexOf('NOTEBOOK_NEAR_FULL_ROUTE_OVERFLOW') !== -1) {
    overflowSlots = doNlmSlots_({ notebookId: overflowNotebookId, cap: cap, refresh: refresh ? 'true' : 'false' });
    if (overflowSlots.full && decision === 'REVIEW') {
      // MỌI shard (base + overflow) đầy → GIỮ REVIEW (agent HỎI người dùng duyệt shard mới), KHÔNG khuyên add
      // vào shard đầy. Khớp client `_overflow_route` (blocked → ask user) + fail-closed `_ingest_target` v1.34.47.
      reasons.push('ALL_SHARDS_FULL_ASK_USER');
    }
  }

  return {
    ok: true,
    decision: decision,           // ADD | SKIP | REVIEW
    reasons: reasons,
    notebookId: notebookId || null,
    query: q || null,
    slots: slots,
    dedup: dedup,
    overflow_route: (overflowProfile || overflowNotebookId) ? {
      row_kind: 'overflow',
      corpus: 'VBQPPL',
      profile: overflowProfile || null,
      notebookId: overflowNotebookId || null,
      slots: overflowSlots,                                             // v2.21.2k: slot LIVE của shard overflow (null nếu chưa route)
      has_room: overflowSlots ? (overflowSlots.remaining > 0) : null,   // v2.21.2k
      full: overflowSlots ? overflowSlots.full : null                   // v2.21.2k
    } : null,
    overflow_slots: overflowSlots,   // v2.21.2k: tiện client đọc trực tiếp (used/remaining/full/near_full shard overflow)
    find: found,
    superseded_matches: superseded,
    note: 'decision=ADD ⇒ source_add. SKIP ⇒ không add (đã trùng/đầy). ' +
          'REVIEW ⇒ HỎI người dùng (gần trùng / trùng số chưa lên NLM / cần đối chiếu). ' +
          'EXISTING_SUPERSEDED_PRESENT ⇒ cân nhắc VBHN-first (thay bản cũ).'
  };
}

/* ============================================================
 * v2.16.0 — vb_status: tra cứu nhanh hiệu lực + supersededBy
 * Nhập số hiệu → {in_registry, on_nlm, hieuluc, status, superseded_by[]}
 * Dùng goc-index của doFind_; trả JSON nhỏ, KHÔNG kéo manifest.
 * ============================================================ */
function canonSoHieu_(s){
  var k = normSoHieu_(s);
  var m = k.match(/^(\d+)-(VPQH|UBTVQH\d*)$/);   if (m) return m[1]+'-VBHN-'+m[2];
  m = k.match(/^(\d+)VBHN-(.+)$/);               if (m) return m[1]+'-VBHN-'+m[2];
  return k;
}


function effectiveDateIso_(s){
  s = String(s || '');
  var m = s.match(/(\d{1,2})\s*[\/\-.]\s*(\d{1,2})\s*[\/\-.]\s*(\d{4})/);
  if(!m) m = s.match(/ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})/i);
  if(!m) return '';
  var d = ('0'+Number(m[1])).slice(-2), mo = ('0'+Number(m[2])).slice(-2), y = String(m[3]);
  return y + '-' + mo + '-' + d;
}


function doVbStatus_(p){
  var q = String(p.q||p.soHieu||p.sohieu||'').trim();
  if(!q) return {ok:false, error:'vb_status: thiếu số hiệu/q'};
  var so = findSoHieuInQuery_(q) || q;
  var soN = canonSoHieu_(so);
  if(!soN) return {ok:false, error:'vb_status: không nhận ra số hiệu từ "'+q+'"'};
  var isVbhn = soN.indexOf('VBHN')>=0;
  var objs = regReadAll_(String(p.refresh)==='true');

  function keyOf(o){ return canonSoHieu_(o.sohieu || sohieuFromName_(o.name) || ''); }
  function hlLow(x){ return stripVN_(String(x||'')).toLowerCase(); }
  function isSup(o){ var h=hlLow(o&&o.hieuluc); return h.indexOf('het hieu luc')>=0||h.indexOf('thay the')>=0||h.indexOf('superseded')>=0; }
  function compact(o){ return {sohieu:o.sohieu||keyOf(o), name:o.name||'', drive_id:o.drive_id||'',
     hieuluc:o.hieuluc||'', on_nlm: !!o.nlm_source_id && !nlmIsRemoved_(o), cat:o.cat||'',
     nlm_source_id:o.nlm_source_id||''}; }

  var selfAll=[], selfActive=[];
  objs.forEach(function(o){ if(keyOf(o)===soN){ selfAll.push(o); if(!nlmIsRemoved_(o)) selfActive.push(o); } });
  selfAll.sort(registryRankCompare_);
  selfActive.sort(registryRankCompare_);

  var consBy=[];
  objs.forEach(function(o){
    if(!o.goc) return;
    var parts=String(o.goc).split(';');
    for(var i=0;i<parts.length;i++){ if(canonSoHieu_(parts[i])===soN){ consBy.push(o); break; } }
  });
  var seen={}, consByU=[];
  consBy.forEach(function(o){ var k=keyOf(o); if(!seen[k]){ seen[k]=1; consByU.push(o); } });
  var consByC = consByU.map(compact);

  var inDrive = selfAll.some(function(o){ return !!o.drive_id; });
  var nlmRows = selfActive.filter(function(o){ return !!o.nlm_source_id && !nlmIsRemoved_(o); }).sort(registryRankCompare_);
  var onNlm = nlmRows.length>0;
  var row = nlmRows[0] || selfActive[0] || selfAll[0] || null;
  var hieuluc = row ? (row.hieuluc||'') : '';
  var effIso = effectiveDateIso_(hieuluc);
  var todayIso = Utilities.formatDate(new Date(), 'GMT+7', 'yyyy-MM-dd');
  var pendingEffect = !!(effIso && effIso > todayIso);

  var supersedes=[];
  if(row && row.goc){
    var sd={};
    String(row.goc).split(';').forEach(function(g){ var gk=canonSoHieu_(g); if(gk && !sd[gk]){ sd[gk]=1; supersedes.push({sohieu:gk}); } });
  }

  var status, flags=[];
  if(!selfAll.length){
    status = consBy.length ? 'CONSOLIDATED_INTO_VBHN' : 'NOT_IN_REGISTRY';
  } else if(isVbhn){
    if(pendingEffect) status='VBHN_PENDING_EFFECT';
    else if(isSup(row)) status='VBHN_SUPERSEDED';
    else if(onNlm) status='VBHN_IN_FORCE';
    else status='VBHN_IN_REGISTRY_NOT_ON_NLM';
  } else {
    if(pendingEffect) status='PENDING_EFFECT';
    else if(isSup(row)) status='SUPERSEDED';
    else if(hlLow(hieuluc).indexOf('con hieu luc')>=0) status='IN_FORCE';
    else if(consBy.length) status='IN_FORCE_CONSOLIDATED';
    else status='IN_REGISTRY_HIEULUC_UNKNOWN';
  }
  var sbLive = consByC.filter(function(x){ return x.on_nlm || hlLow(x.hieuluc).indexOf('con hieu luc')>=0; });
  if(sbLive.length>1) flags.push('MULTIPLE_VBHN');
  if(selfActive.length>1) flags.push('DUPLICATE_ROWS');
  if(selfAll.length && !selfActive.length) flags.push('SELF_REMOVED');
  if(pendingEffect) flags.push('PENDING_EFFECT');

  return {ok:true, query:q, sohieu:soN, is_vbhn:isVbhn,
    in_drive:inDrive, on_nlm:onNlm, hieuluc:hieuluc||null, effective_date:effIso||null,
    pending_effect:pendingEffect, status:status, flags:flags,
    self: row? {drive_id:row.drive_id||'', name:row.name||'', loai:row.loai||'', cat:row.cat||'',
                hieuluc:row.hieuluc||'', nlm_source_id:row.nlm_source_id||'', nlm_status:row.nlm_status||''} : null,
    self_count: selfAll.length,
    superseded_by: consByC,
    supersedes: supersedes,
    note:'status: PENDING_EFFECT|VBHN_PENDING_EFFECT|IN_FORCE|IN_FORCE_CONSOLIDATED|SUPERSEDED|CONSOLIDATED_INTO_VBHN|VBHN_IN_FORCE|VBHN_SUPERSEDED|VBHN_IN_REGISTRY_NOT_ON_NLM|NOT_IN_REGISTRY. superseded_by=VBHN hợp nhất số này; supersedes=số bản này hợp nhất.'
  };
}

function _grantScopes(){
  var r = UrlFetchApp.fetch(
    'https://www.googleapis.com/drive/v3/about?fields=user',
    { headers:{ Authorization:'Bearer '+ScriptApp.getOAuthToken() },
      muteHttpExceptions:true });
  Logger.log('HTTP ' + r.getResponseCode());  // kỳ vọng 200
}

/* =====================================================================
 * GHI CHÚ appsscript.json (KHÔNG thuộc .gs — sửa ở file manifest):
 *   urlFetchWhitelist thêm:
 *     "https://drive.google.com/",
 *     "https://docs.google.com/",
 *     "https://drive.usercontent.google.com/"
 *   (Vá phụ cho UrlFetchApp phía Apps Script; KHÔNG mở egress container.)
 * Sau khi dán file này: Deploy → New version (GIỮ Deployment ID/URL+token).
 * Kiểm: ping phải trả version: 2.21.2h (Cách B đa-corpus + writeconfig + row_kind/schema guard).
 * 2.21.2h thêm: row_kind own/ref/overflow, ping schema fields, countRefs và profile-scope CLI đầy đủ.
 * ===================================================================== */
