#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apply_gs_patches.py — áp patch Apps Script v2.21.1 cho tra-luat, theo chế độ an toàn.

Bản v1.16.5 sửa các vấn đề của 1.16.4:
  • F2 configView alias được scope vào dispatchAction_ nên không đếm nhầm comment.
  • F14b tự động đủ 2 phần: cap batch + cấm batch lồng.
  • Audit mở rộng: không xanh giả; kiểm cả các mục P0/P1 đang phải dán tay.
  • Report có DEPLOYABILITY rõ ràng; nếu audit cuối chưa xanh thì KHÔNG coi là file deploy được.
  • --force có thể ghi partial để debug, nhưng exit code vẫn khác 0 nếu còn lỗi/audit fail.

Lưu ý: script này là SEMI-AUTO có audit nghiêm ngặt. Nó tự động các phần dễ sót
(version/root/global replacement + các rewrite nhỏ). Các rewrite hàm lớn vẫn có thể cần dán tay
theo references/PATCH_v2.21.1.gs.md; audit cuối sẽ bắt buộc kiểm chúng.

Dùng:
  python scripts/apply_gs_patches.py --in Code.gs                 # dry-run + PATCH_REPORT.md
  python scripts/apply_gs_patches.py --in Code.gs --write         # ghi Code.gs.2.21.1.gs nếu auto không lỗi
  python scripts/apply_gs_patches.py --in Code.gs --write --out Code.2.21.1.gs
  python scripts/apply_gs_patches.py --selftest
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

# UTF-8 hardening (Windows codepage / tiếng Việt)
import sys as _sys
for _s in (getattr(_sys, "stdout", None), getattr(_sys, "stderr", None)):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


APP_VERSION = "2.21.1"

ROOT_KEEP_PATTERNS = [
    r"ROOT_FOLDER_ID:\s*'",        # định nghĩa trong CONFIG
    r"CATEGORIES_FALLBACK",         # snapshot category không phải root runtime
    r"getProperty\('TL_ROOT_ID'\)", # thân rootId_()
]

# type:
# - insert_before: anchor string phải khớp đúng 1 lần
# - replace_once: find string phải khớp đúng 1 lần
# - scoped_replace: scope phải khớp đúng 1 lần, find trong scope phải >=1 lần
# - global_root: thay CONFIG.ROOT_FOLDER_ID bằng rootId_() ngoài 3 nơi cho phép
PATCHES: List[Dict[str, str]] = [
    dict(id="APP_VERSION", f="F3", type="insert_before",
         anchor="var CONFIG = {",
         text=f"var APP_VERSION = '{APP_VERSION}';   // nguồn sự thật phiên bản\n\n"),
    dict(id="rootId_helper", f="F15c", type="insert_before",
         anchor="function resolveFolder_(p){",
         text=("function rootId_(){\n"
               "  return PropertiesService.getScriptProperties().getProperty('TL_ROOT_ID') || CONFIG.ROOT_FOLDER_ID;\n"
               "}\n")),
    dict(id="privateConfigFile_helper", f="F7b", type="insert_before",
         anchor="function doWriteConfig_(p){",
         text=("function privateConfigFile_(fileId){\n"
               "  try { DriveApp.getFileById(fileId).setSharing(DriveApp.Access.PRIVATE, DriveApp.Permission.NONE); }\n"
               "  catch(e){ Logger.log('[privateConfigFile_] khong revoke duoc sharing: ' + e); }\n"
               "}\n")),

    # Version unification
    dict(id="ver_ping", f="F3", type="scoped_replace",
         scope_start="function dispatchAction_(action, p){",
         scope_end="/* --- v2.12 --- */",
         find="version:'2.20.0'", replace="version:APP_VERSION"),
    dict(id="ver_boot", f="F3", type="replace_once",
         find="version:'2.14.0', rootId:rootId", replace="version:APP_VERSION, rootId:rootId"),
    dict(id="ver_regen2", f="F3", type="replace_once",
         find="['version', '2.14.0']", replace="['version', APP_VERSION]"),
    dict(id="ver_configview", f="F3", type="replace_once",
         find="version:'2.11.0', config:eff", replace="version:APP_VERSION, config:eff"),
    dict(id="ver_manifest_out", f="F3", type="replace_once",
         find="version: '2.20.0', schema: 'uniform-v1'", replace="version: APP_VERSION, schema: 'uniform-v1'"),
    dict(id="ver_manifest_schema", f="F3", type="replace_once",
         find="schema_version:'2.20.0'", replace="schema_version:APP_VERSION"),

    # F2 — scope vào dispatchAction_, tránh đếm nhầm comment chứa case 'config'
    dict(id="configview_alias", f="F2", type="scoped_replace",
         scope_start="function dispatchAction_(action, p){",
         scope_end="/* --- v2.12 --- */",
         find="    case 'config':       return doConfigView_(p);",
         replace="    case 'config':\n    case 'configView':   return doConfigView_(p);"),

    # F8 — fetch_url_to_drive trả object, không trả jsonOut_ nội bộ
    dict(id="fetch_jsonout", f="F8", type="scoped_replace",
         scope_start="function doFetchUrlToDrive_(p){",
         scope_end="source_add (GDoc).'});",
         find="return jsonOut_(", replace="return ("),
    dict(id="fetch_version", f="F3", type="scoped_replace",
         scope_start="function doFetchUrlToDrive_(p){",
         scope_end="source_add (GDoc).'});",
         find="version:'2.15.0'", replace="version:APP_VERSION"),

    # F12 — importext nhận files=[id,...]
    dict(id="importext_norm", f="F12", type="replace_once",
         find="if(!list || !list.length) throw new Error('importext: thiếu files[]');",
         replace=("if(!list || !list.length) throw new Error('importext: thiếu files[]');\n"
                  "  list = list.map(function(x){ return (typeof x === 'string') ? {id:x} : x; });")),

    # F4b — regen2 đọc cả soHieu camel cũ
    dict(id="regen2_sohieu", f="F4b", type="replace_once",
         find="sohieu: normSoHieu_(ap.sohieu||'') || sohieuFromName_(f.name),",
         replace="sohieu: normSoHieu_(ap.sohieu || ap.soHieu || '') || sohieuFromName_(f.name),"),

    # D — manifest message hết nhắc regen legacy
    dict(id="manifest_msg", f="D", type="replace_once",
         find="error:'Chưa có manifest — chạy action=regen&confirm=yes trước'",
         replace="error:'Chưa có manifest — chạy action=regen2&confirm=yes rồi manifest_export trước'"),

    # F14b — batch cap + cấm batch lồng
    dict(id="batch_cap", f="F14b", type="replace_once",
         find="if(!Array.isArray(ops)) throw new Error('ops phải là mảng');",
         replace=("if(!Array.isArray(ops)) throw new Error('ops phải là mảng');\n"
                  "  if(ops.length>30) throw new Error('batch: tối đa 30 ops/lần');")),
    dict(id="batch_no_nested", f="F14b", type="replace_once",
         find="    op=op||{};\n    try{ var r=dispatchAction_(op.action, op);",
         replace=("    op=op||{};\n"
                  "    if(op.action==='batch'){\n"
                  "      results.push({i:i, action:'batch', ok:false, error:'không cho batch lồng batch'}); failed++; return;\n"
                  "    }\n"
                  "    try{ var r=dispatchAction_(op.action, op);")),

    # F4 — provenance_ chữ thường
    dict(id="provenance", f="F4", type="replace_once",
         find=("function provenance_(p, sha, url){\n"
               "  return {soHieu:p.soHieu||'', nam:p.nam||'', loai:p.loai||'', coquan:p.coquan||'',\n"
               "          hieuLuc:p.hieuLuc||'', sha256:sha||'', sourceUrl:url||'', ingestedAt:new Date().toISOString()};\n"
               "}"),
         replace=("function provenance_(p, sha, url){\n"
                  "  return {sohieu:p.soHieu||p.sohieu||'', nam:p.nam||'', loai:p.loai||'', coquan:p.coquan||'',\n"
                  "          hieuluc:p.hieuLuc||p.hieuluc||'', sha256:sha||'', sourceUrl:url||'', ingestedAt:new Date().toISOString()};\n"
                  "}")),

    # F9 — resolveFolder_ fail-closed
    dict(id="resolveFolder", f="F9", type="replace_once",
         find=("function resolveFolder_(p){\n"
               "  if(p.folderId) return p.folderId;\n"
               "  if(p.cat){ var fid=resolveCatFolderId_(p.cat); if(fid) return fid; }\n"
               "  return p.toFolderId || CONFIG.ROOT_FOLDER_ID;\n"
               "}"),
         replace=("function resolveFolder_(p){\n"
                  "  if (p.folderId) return p.folderId;\n"
                  "  if (p.cat !== undefined && String(p.cat).trim() !== ''){\n"
                  "    var fid = resolveCatFolderId_(p.cat);\n"
                  "    if (!fid) throw new Error('resolveFolder_: khong resolve duoc cat \"'+p.cat+'\"');\n"
                  "    return fid;\n"
                  "  }\n"
                  "  if (p.toFolderId) return p.toFolderId;\n"
                  "  return rootId_();\n"
                  "}")),

    # F9 — extDest_ fail-closed; function nhỏ nên auto được
    dict(id="extDest", f="F9", type="replace_once",
         find=("function extDest_(p, defaultName){\n"
               "  if(p.destFolderId) return p.destFolderId;\n"
               "  if(p.destName) return doMkdir_({name:p.destName, parentId:p.destParentId||CONFIG.ROOT_FOLDER_ID}).folderId;\n"
               "  if(p.cat){ var fid=resolveCatFolderId_(p.cat); if(fid) return fid; }\n"
               "  if(defaultName) return doMkdir_({name:defaultName, parentId:CONFIG.ROOT_FOLDER_ID}).folderId;\n"
               "  return CONFIG.ROOT_FOLDER_ID;\n"
               "}"),
         replace=("function extDest_(p, defaultName){\n"
                  "  if (p.destFolderId) return p.destFolderId;\n"
                  "  if (p.destName) return doMkdir_({name:p.destName, parentId:p.destParentId||rootId_()}).folderId;\n"
                  "  if (p.cat !== undefined && String(p.cat).trim() !== ''){\n"
                  "    var fid = resolveCatFolderId_(p.cat);\n"
                  "    if (!fid) throw new Error('extDest_: khong resolve duoc cat \"'+p.cat+'\"');\n"
                  "    return fid;\n"
                  "  }\n"
                  "  if (defaultName) return doMkdir_({name:defaultName, parentId:rootId_()}).folderId;\n"
                  "  return rootId_();\n"
                  "}")),

    # global root cuối cùng
    # ---- BỔ SUNG coverage (best-of-both v1.16.6): rewrite hàm lớn + 2 vá staleness ----
    dict(id="driveSearch_add", f="F1", type="insert_before",
         anchor="function doSearch_(p){",
         text=("function driveSearch_(p){\n"
               "  var fields = sanitizeFields_(p.fields || cfgSearchFields_());\n"
               "  var pageSize = Math.min(Number(p.pageSize)||cfgNum_('TL_SEARCH_PAGESIZE',100), 1000);\n"
               "  var clauses = [];\n"
               "  if (p.q) clauses.push('('+p.q+')');\n"
               "  var parents = [];\n"
               "  if (p.cat){ var cid=resolveCatFolderId_(p.cat); if(cid) parents.push(cid); }\n"
               "  else if (String(p.scope)==='corpus'){ parents = corpusFolders_(String(p.refresh)==='true').ids; }\n"
               "  if (parents.length)\n"
               "    clauses.push('('+parents.map(function(id){return \"'\"+id+\"' in parents\";}).join(' or ')+')');\n"
               "  clauses.push('trashed=false');\n"
               "  if (String(p.includeFolders)!=='true' && (p.cat||String(p.scope)==='corpus'))\n"
               "    clauses.push(\"mimeType!='application/vnd.google-apps.folder'\");\n"
               "  var req = { q:clauses.join(' and '), pageSize:pageSize,\n"
               "              fields:'nextPageToken,files('+fields+')',\n"
               "              supportsAllDrives:true, includeItemsFromAllDrives:true };\n"
               "  if (p.orderBy) req.orderBy = p.orderBy;\n"
               "  if (p.pageToken) req.pageToken = p.pageToken;\n"
               "  var r = Drive.Files.list(req);\n"
               "  return { ok:true, scope: p.cat?('cat:'+p.cat):(p.scope||'q'),\n"
               "           count:(r.files||[]).length, files:r.files||[], nextPageToken:r.nextPageToken||'' };\n"
               "}\n")),
    dict(id="metafind_drive", f="F1", type="replace_once",
         find="  return doSearch_({ q:q, fields:p.fields, pageSize:p.pageSize, pageToken:p.pageToken });",
         replace="  return driveSearch_({ q:q, scope:p.scope||'corpus', fields:p.fields, pageSize:p.pageSize, pageToken:p.pageToken });"),
    dict(id="find_tier3_drive", f="F1", type="replace_once",
         find="  var ft = doSearch_({ q: \"fullText contains '\" + qEsc_(q) + \"'\", scope:'corpus', pageSize:MAX });",
         replace="  var ft = driveSearch_({ q: \"fullText contains '\" + qEsc_(q) + \"'\", scope:'corpus', pageSize:MAX });"),
    dict(id="regen_stub", f="F6", type="replace_once",
         find="    case 'regen':\n    case 'regenRegistry':return doRegen_(p);",
         replace=("    case 'regen':\n"
                  "    case 'regenRegistry': return {ok:false, deprecated:true, error:'regen (Doc-registry, schema cu) da ngung — dung regen2 (confirm=yes) + manifest_export.', use:['regen2','manifest_export']};")),
    dict(id="mapset_notebook", f="F10", type="replace_once",
         find="    note: p.notebook ? ('nb:' + p.notebook) : '' });",
         replace=("    nlm_notebook_id: p.notebookId || p.nlm_notebook_id || p.notebook || '',\n"
                  "    note: p.note || (p.notebook ? ('nb:' + p.notebook) : '') });")),
    dict(id="vbstatus_branch", f="F11b", type="replace_once",
         find=("  } else if(isVbhn){\n"
               "    status = (isSup(row) || !onNlm) ? 'VBHN_SUPERSEDED' : 'VBHN_IN_FORCE';\n"
               "  } else {"),
         replace=("  } else if(isVbhn){\n"
                  "    if(isSup(row)) status='VBHN_SUPERSEDED';\n"
                  "    else if(onNlm) status='VBHN_IN_FORCE';\n"
                  "    else status='VBHN_IN_REGISTRY_NOT_ON_NLM';\n"
                  "  } else {")),
    dict(id="copyconvert_fields", f="F13b", type="replace_once",
         find="    {supportsAllDrives: true, fields: 'id,name,mimeType'}",
         replace="    {supportsAllDrives: true, fields: 'id,name,mimeType,webViewLink'}"),
    dict(id="copyconvert_viewurl", f="F13b", type="replace_once",
         find=("          srcFileId:p.fileId, srcName:srcMeta.name, folderId:folderId,\n"
               "          viewUrl:'https://docs.google.com/document/d/'+copied.id+'/view'};"),
         replace=("          srcFileId:p.fileId, srcName:srcMeta.name, folderId:folderId,\n"
                  "          viewUrl: copied.webViewLink || ('https://drive.google.com/file/d/'+copied.id+'/view')};")),
    dict(id="organize_failclosed", f="F9b", type="replace_once",
         find=("  if (p.cat){\n"
               "    var folderId = /^[0-9]{2}$|^QUARANTINE$/.test(String(p.cat))\n"
               "      ? resolveCatFolderId_(String(p.cat)) : String(p.cat);\n"
               "    var mv = doMove_({ fileId: id, folderId: folderId, removeFromParent: 'true' });\n"
               "    if (!mv.ok) return { ok:false, step:'move', steps: steps, error: mv.error };\n"
               "    steps.move = { ok:true, folderId: folderId };"),
         replace=("  if (p.cat){\n"
                  "    var catStr = String(p.cat).trim(), folderId;\n"
                  "    if (/^\\d{1,2}$|^QUARANTINE$/.test(catStr)){\n"
                  "      folderId = resolveCatFolderId_(catStr);\n"
                  "      if (!folderId) return { ok:false, step:'move', steps:steps, error:'organize: khong resolve duoc cat \"'+catStr+'\"' };\n"
                  "    } else folderId = catStr;\n"
                  "    var mv = doMove_({ fileId: id, folderId: folderId, removeFromParent: 'true' });\n"
                  "    if (!mv.ok) return { ok:false, step:'move', steps: steps, error: mv.error };\n"
                  "    steps.move = { ok:true, folderId: folderId };")),
    dict(id="writeconfig", f="F7", type="replace_once",
         find=("function doWriteConfig_(p){\n"
               "  var obj=buildConfigObject_(p);\n"
               "  var json=JSON.stringify(obj, null, 2);\n"
               "  var sp=PropertiesService.getScriptProperties(), cid=sp.getProperty('TL_CONFIG_ID'), cfile=null;\n"
               "  if(cid){ try{ cfile=DriveApp.getFileById(cid); }catch(e){ cfile=null; } }\n"
               "  if(!cfile){\n"
               "    var folder=DriveApp.getFolderById(CONFIG.ROOT_FOLDER_ID);\n"
               "    cfile=folder.createFile(CONFIG.CONFIG_NAME, json, 'application/json');\n"
               "    cfile.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);\n"
               "    sp.setProperty('TL_CONFIG_ID', cfile.getId());\n"
               "  } else { cfile.setContent(json); }\n"
               "  return {ok:true, configFileId:cfile.getId(), name:CONFIG.CONFIG_NAME,\n"
               "          rootFolderId:CONFIG.ROOT_FOLDER_ID,\n"
               "          downloadUrl:'https://drive.google.com/uc?export=download&id='+cfile.getId(),\n"
               "          config:obj};\n"
               "}"),
         replace=("function doWriteConfig_(p){\n"
                  "  var obj=buildConfigObject_(p);\n"
                  "  var json=JSON.stringify(obj, null, 2);\n"
                  "  var sp=PropertiesService.getScriptProperties(), cid=sp.getProperty('TL_CONFIG_ID'), cfile=null;\n"
                  "  if(cid){ try{ cfile=DriveApp.getFileById(cid); }catch(e){ cfile=null; } }\n"
                  "  if(!cfile){\n"
                  "    var folder=DriveApp.getFolderById(rootId_());\n"
                  "    cfile=folder.createFile(CONFIG.CONFIG_NAME, json, 'application/json');\n"
                  "    sp.setProperty('TL_CONFIG_ID', cfile.getId());\n"
                  "  } else { cfile.setContent(json); }\n"
                  "  privateConfigFile_(cfile.getId());\n"
                  "  return {ok:true, configFileId:cfile.getId(), name:CONFIG.CONFIG_NAME,\n"
                  "          rootFolderId:rootId_(),\n"
                  "          driveFileId:cfile.getId(), configAccess:'private',\n"
                  "          note:'Config private (chua token) — doc qua Drive MCP/owner hoac dat TL_TOKEN bang env; KHONG tai headless.',\n"
                  "          config:obj};\n"
                  "}")),
    dict(id="readconfig_e", f="E", type="replace_once",
         find=("  return {ok:true, mirrored:true, configFileId:cfile.getId(),\n"
               "          updated:cfile.getLastUpdated().toISOString(),\n"
               "          downloadUrl:'https://drive.google.com/uc?export=download&id='+cfile.getId(),\n"
               "          config:JSON.parse(json)};"),
         replace=("  return {ok:true, mirrored:true, configFileId:cfile.getId(),\n"
                  "          updated:cfile.getLastUpdated().toISOString(),\n"
                  "          driveFileId:cfile.getId(), configAccess:'private',\n"
                  "          note:'Config private — doc qua Drive MCP/owner; KHONG tai headless.',\n"
                  "          config:JSON.parse(json)};")),
    dict(id="manifest_downloadurl", f="E", type="replace_once",
         find="          downloadUrl:'https://drive.google.com/uc?export=download&id='+mid};",
         replace="          driveFileId:mid};"),
    dict(id="header_regen_comment", f="D", type="replace_once",
         find="&action=regen&confirm=yes  \u2192 manifest.json",
         replace="&action=regen2&confirm=yes \u2192 manifest.json + manifest_export"),
    # ---- v1.16.7: F5 (treeHash cùng cơ sở corpus) + xóa doRegen_ + sửa comment stale ----
    dict(id="f5_corpusObjs", f="F5", type="replace_once",
         find="  var entries = objs.map(entryOf_);",
         replace=("  var entries = objs.map(entryOf_);\n"
                  "  var corpusObjs = objs.filter(function(o){ return String(o.corpus)==='true' && o.loai!=='thuong'; });")),
    dict(id="f5_treehash", f="F5", type="replace_once",
         find="    treeHash: treeHashV2_(objs), count: objs.length,",
         replace="    treeHash: treeHashV2_(corpusObjs), corpus_count: corpusObjs.length, count: objs.length,"),
    dict(id="f5_return", f="F5", type="replace_once",
         find="  return { ok:true, manifestId:id, treeHash:out.treeHash, count:out.count,",
         replace="  return { ok:true, manifestId:id, treeHash:out.treeHash, count:out.count, corpus_count:out.corpus_count,"),
    dict(id="del_doRegen", f="F6", type="delete_span",
         start="function doRegen_(p){", end="function doManifestRead_(p){"),
    dict(id="cmt_ping_ver", f="A", type="replace_once",
         find="ping phải trả version: 2.20.0'.", replace="ping phải trả version: 2.21.1."),
    dict(id="cmt_readconfig", f="E", type="replace_once",
         find="readconfig:  trả lại nội dung mirror (và downloadUrl) để skill/bash đọc.",
         replace="readconfig:  trả lại nội dung mirror (config private, KHÔNG downloadUrl public) để skill/bash đọc."),
    dict(id="cmt_vbstatus_enum", f="F11b", type="replace_once",
         find="VBHN_IN_FORCE|VBHN_SUPERSEDED|NOT_IN_REGISTRY.",
         replace="VBHN_IN_FORCE|VBHN_SUPERSEDED|VBHN_IN_REGISTRY_NOT_ON_NLM|NOT_IN_REGISTRY."),
    dict(id="global_root", f="F15c", type="global_root"),
]

MANUAL = [
    ("F1",  "driveSearch_ + doMetaFind_(scope:'corpus') + doFind_ tầng fulltext"),
    ("F6",  "stub regen/regenRegistry + xóa/không dùng doRegen_ legacy"),
    ("F7/F7b", "doWriteConfig_: bỏ public share + gọi privateConfigFile_(cfile.getId())"),
    ("F9b", "doOrganize_: cat fail-closed"),
    ("F10", "doMapSet_: ghi nlm_notebook_id"),
    ("F11b", "doVbStatus_: VBHN_IN_REGISTRY_NOT_ON_NLM"),
    ("F13b", "doCopyConvert_: fields webViewLink + viewUrl đúng loại"),
    ("E", "doReadConfig_/doWriteConfig_: bỏ/ghi chú downloadUrl khi config private"),
]

# Static audits cuối cùng. Một số audit sẽ FAIL sau auto-only: đó là đúng, nghĩa là chưa deploy được
# cho tới khi dán các mục manual tương ứng.
AUDITS = [
    dict(id="no_jsonout_in_fetch", desc="không còn return jsonOut_ trong doFetchUrlToDrive_",
         kind="scoped_absent", scope_start="function doFetchUrlToDrive_(p){",
         scope_end="source_add (GDoc).'});", pattern="return jsonOut_("),
    dict(id="no_old_versions", desc="không còn version runtime cũ 2.14/2.15/2.11 hoặc schema_version 2.20",
         kind="absent", pattern=r"(version:'2\.1[145]\.0'|schema_version:'2\.20\.0')"),
    dict(id="has_app_version", desc="có APP_VERSION", kind="present", pattern=r"var APP_VERSION = "),
    dict(id="configView_alias", desc="dispatchAction_ có alias configView", kind="scoped_present",
         scope_start="function dispatchAction_(action, p){", scope_end="/* --- v2.12 --- */",
         pattern=r"case 'configView':\s*return doConfigView_\(p\);"),
    dict(id="has_rootId", desc="có rootId_()", kind="present", pattern=r"function rootId_\(\)"),
    dict(id="root_only_allowed", desc="CONFIG.ROOT_FOLDER_ID chỉ còn ở nơi cho phép", kind="root_residual"),
    dict(id="manifest_treehash_corpus", desc="manifest_export treeHash trên corpusObjs (F5)",
         kind="scoped_present", scope_start="function doManifestExport_(p){", scope_end="return { ok:true, manifestId:id",
         pattern=r"treeHashV2_\(corpusObjs\)"),
    dict(id="manifest_no_alltree", desc="manifest_export KHÔNG còn treeHashV2_(objs) (F5)",
         kind="scoped_absent", scope_start="function doManifestExport_(p){", scope_end="return { ok:true, manifestId:id",
         pattern="treeHashV2_(objs)"),
    dict(id="manifest_corpus_count", desc="manifest_export trả corpus_count (F5)",
         kind="scoped_present", scope_start="function doManifestExport_(p){", scope_end="return { ok:true, manifestId:id",
         pattern=r"corpus_count"),
    dict(id="no_doRegen_legacy", desc="đã xóa doRegen_ legacy (F6)", kind="absent",
         pattern=r"function doRegen_\("),
    dict(id="has_privateConfigFile", desc="có helper privateConfigFile_", kind="present", pattern=r"function privateConfigFile_\("),
    dict(id="calls_privateConfigFile", desc="doWriteConfig_ gọi privateConfigFile_(cfile.getId())", kind="scoped_present",
         scope_start="function doWriteConfig_(p){", scope_end="function doReadConfig_(p){",
         pattern=r"privateConfigFile_\(cfile\.getId\(\)\)"),
    dict(id="no_config_anyone_share", desc="doWriteConfig_ không setSharing ANYONE_WITH_LINK", kind="scoped_absent",
         scope_start="function doWriteConfig_(p){", scope_end="function doReadConfig_(p){",
         pattern="setSharing(DriveApp.Access.ANYONE_WITH_LINK"),
    dict(id="meta_find_corpus", desc="doMetaFind_ gọi driveSearch_ với scope corpus", kind="scoped_present",
         scope_start="function doMetaFind_(p){", scope_end="function doShortcut_(p){",
         pattern=r"driveSearch_\(\{\s*q\s*:\s*q,\s*scope\s*:\s*p\.scope\s*\|\|\s*'corpus'"),
    dict(id="find_fulltext_drive", desc="doFind_ tầng fulltext dùng driveSearch_", kind="scoped_present",
         scope_start="function doFind_(p){", scope_end="function doVbStatus_(p){",
         pattern=r"driveSearch_\(\{\s*q\s*:\s*\"fullText contains"),
    dict(id="batch_cap", desc="batch có cap 30", kind="scoped_present",
         scope_start="function doBatch_(p){", scope_end="function fetchBlob_(url, title){",
         pattern=r"ops\.length\s*>\s*30"),
    dict(id="batch_no_nested", desc="batch cấm lồng batch", kind="scoped_present",
         scope_start="function doBatch_(p){", scope_end="function fetchBlob_(url, title){",
         pattern=r"op\.action\s*===\s*'batch'"),
    dict(id="organize_fail_closed", desc="doOrganize_ cat sai trả ok:false, không rơi root", kind="scoped_present",
         scope_start="function doOrganize_(p){", scope_end="/* ============ INTEGRITY",
         pattern=r"organize: .*resolve duoc cat|organize: .*resolve được cat"),
    dict(id="extDest_fail_closed", desc="extDest_ cat sai throw", kind="scoped_present",
         scope_start="function extDest_(p, defaultName){", scope_end="function findImported_(srcId, srcMd5){",
         pattern=r"extDest_: .*resolve duoc cat|extDest_: .*resolve được cat"),
    dict(id="map_set_notebook", desc="doMapSet_ ghi nlm_notebook_id", kind="scoped_present",
         scope_start="function doMapSet_(p){", scope_end="return { ok:true, drive_id: target",
         pattern=r"nlm_notebook_id\s*:\s*\S"),
    dict(id="vb_status_registry_not_on_nlm", desc="vb_status có VBHN_IN_REGISTRY_NOT_ON_NLM", kind="present",
         pattern=r"VBHN_IN_REGISTRY_NOT_ON_NLM"),
    dict(id="copy_convert_webViewLink", desc="copy_convert trả webViewLink", kind="scoped_present",
         scope_start="function doCopyConvert_(p){", scope_end="/* ============ IMPORT EXTERNAL",
         pattern=r"webViewLink"),
    dict(id="no_private_config_downloadUrl", desc="không còn downloadUrl public cho config private", kind="absent",
         pattern=r"downloadUrl\s*:\s*'https://drive\.google\.com/uc\?export=download&id='"),
    dict(id="manifest_no_regen_legacy_msg", desc="manifest message không nhắc action=regen", kind="absent",
         pattern=r"action=regen&confirm=yes"),
]


def _count(text: str, sub: str) -> int:
    return text.count(sub)


def _scope_span(text: str, start: str, end: str) -> Optional[Tuple[int, int]]:
    i = text.find(start)
    if i < 0:
        return None
    j = text.find(end, i)
    if j < 0:
        return None
    return i, j + len(end)


def apply_patch(text: str, p: Dict[str, str]) -> Tuple[str, Dict[str, object]]:
    t = p["type"]
    if t == "insert_before":
        n = _count(text, p["anchor"])
        if n != 1:
            return text, dict(ok=False, matches=n, note="anchor != 1")
        return text.replace(p["anchor"], p["text"] + p["anchor"], 1), dict(ok=True, matches=1)
    if t == "replace_once":
        n = _count(text, p["find"])
        if n != 1:
            return text, dict(ok=False, matches=n, note="find != 1")
        return text.replace(p["find"], p["replace"], 1), dict(ok=True, matches=1)
    if t == "scoped_replace":
        span = _scope_span(text, p["scope_start"], p["scope_end"])
        if not span:
            return text, dict(ok=False, matches=0, note="scope không tìm thấy")
        a, b = span
        seg = text[a:b]
        n = seg.count(p["find"])
        if n < 1:
            return text, dict(ok=False, matches=0, note="find không có trong scope")
        seg2 = seg.replace(p["find"], p["replace"])
        return text[:a] + seg2 + text[b:], dict(ok=True, matches=n, note=f"scoped {n} thay")
    if t == "global_root":
        lines, cnt = text.split("\n"), 0
        out = []
        for ln in lines:
            if "CONFIG.ROOT_FOLDER_ID" in ln and not any(re.search(k, ln) for k in ROOT_KEEP_PATTERNS):
                ln = ln.replace("CONFIG.ROOT_FOLDER_ID", "rootId_()")
                cnt += 1
            out.append(ln)
        return "\n".join(out), dict(ok=(cnt > 0), matches=cnt, note=f"global-root {cnt} dòng")
    if t == "delete_span":
        if text.count(p["start"]) != 1:
            return text, dict(ok=False, matches=text.count(p["start"]), note="start != 1")
        a = text.find(p["start"]); b = text.find(p["end"], a)
        if b < 0:
            return text, dict(ok=False, matches=0, note="end khong thay sau start")
        return text[:a] + text[b:], dict(ok=True, matches=1, note="xoa %d ky tu" % (b - a))
    return text, dict(ok=False, matches=0, note="type lạ")


def _segment_for_audit(text: str, audit: Dict[str, str]) -> Optional[str]:
    if "scope_start" not in audit:
        return text
    span = _scope_span(text, audit["scope_start"], audit["scope_end"])
    if not span:
        return None
    return text[span[0]:span[1]]


def run_audits(text: str) -> List[Tuple[str, str, bool, int, str]]:
    res = []
    for a in AUDITS:
        k = a["kind"]
        seg = _segment_for_audit(text, a)
        if seg is None:
            res.append((a["id"], a["desc"], False, 0, "scope missing"))
            continue
        if k == "absent":
            hits = len(re.findall(a["pattern"], seg))
            res.append((a["id"], a["desc"], hits == 0, hits, ""))
        elif k == "present":
            hits = len(re.findall(a["pattern"], seg))
            res.append((a["id"], a["desc"], hits >= 1, hits, ""))
        elif k == "scoped_absent":
            hits = seg.count(a["pattern"])
            res.append((a["id"], a["desc"], hits == 0, hits, ""))
        elif k == "scoped_present":
            hits = len(re.findall(a["pattern"], seg, flags=re.S))
            res.append((a["id"], a["desc"], hits >= 1, hits, ""))
        elif k == "root_residual":
            bad = [ln for ln in text.split("\n")
                   if "CONFIG.ROOT_FOLDER_ID" in ln and not any(re.search(p, ln) for p in ROOT_KEEP_PATTERNS)]
            res.append((a["id"], a["desc"], len(bad) == 0, len(bad), ""))
        else:
            res.append((a["id"], a["desc"], False, 0, "unknown audit"))
    return res


def node_check_text(text: str):
    if not shutil.which("node"):
        return None
    r = subprocess.run(
        ["node", "--check", "-"],
        input=text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return (r.returncode == 0, r.stderr.strip())


def write_report(rdir: Path, applied, failed, audits, node_res, manual, deployable: bool, wrote: Optional[str], forced: bool) -> Path:
    p = Path(rdir) / "PATCH_REPORT.md"
    L: List[str] = [f"# PATCH_REPORT — apply_gs_patches → v{APP_VERSION}\n"]
    L.append("## Kết luận deployability\n")
    if deployable:
        L.append("✅ **DEPLOYABLE_CANDIDATE** — auto patches không lỗi, static audit xanh, node --check xanh/được bỏ qua. Vẫn phải chạy runtime checklist sau Deploy.")
    else:
        L.append("❌ **NOT_DEPLOYABLE_YET** — còn lỗi auto patch, audit fail, hoặc node --check fail. Không deploy file này.")
    if forced:
        L.append("⚠️ File được ghi bằng `--force`; nếu còn lỗi/audit fail thì chỉ dùng để debug, không dùng production.")
    if wrote:
        L.append(f"\nOutput: `{wrote}`")

    L.append("\n## Tự động: %d áp, %d lỗi\n" % (len(applied), len(failed)))
    for pid, fid, st in applied:
        L.append("- ✅ %s (%s): %s" % (pid, fid, st.get("note", "ok")))
    for pid, fid, st in failed:
        L.append("- ❌ %s (%s): matches=%s — %s" % (pid, fid, st.get("matches"), st.get("note")))

    L.append("\n## Manual candidates / đối chiếu theo PATCH doc\n")
    L.append("Các mục dưới đây có thể đã được dán tay trước hoặc chưa. Static audit cuối mới là nguồn quyết định.")
    for fid, dsc in manual:
        L.append(f"- ⬜ {fid} — {dsc}")

    L.append("\n## Static audit cuối\n")
    for aid, desc, ok, n, note in audits:
        tail = f" — {desc}"
        if note:
            tail += f" ({note})"
        L.append("- %s %s (n=%s)%s" % ("✅" if ok else "❌", aid, n, tail))
    if node_res is not None:
        ok, err = node_res
        L.append("\n## node --check: %s%s" % ("✅ OK" if ok else "❌ FAIL", "" if ok else "\n```\n" + err + "\n```"))
    else:
        L.append("\n## node --check: (bỏ qua — không có `node`)")
    p.write_text("\n".join(L) + "\n", encoding="utf-8")
    return p


def process(in_path: str, out_path: Optional[str], write: bool, force: bool, only: Optional[Iterable[str]] = None, report_dir: Optional[str] = None) -> int:
    text = Path(in_path).read_text(encoding="utf-8")
    applied, failed, cur = [], [], text
    only_set = set(only or [])
    for p in PATCHES:
        if only_set and p["id"] not in only_set:
            continue
        new, st = apply_patch(cur, p)
        if st["ok"]:
            cur = new
            applied.append((p["id"], p["f"], st))
        else:
            failed.append((p["id"], p["f"], st))

    audits = run_audits(cur)
    node_res = node_check_text(cur)
    auto_ok = not failed
    audits_ok = all(ok for _, _, ok, _, _ in audits)
    node_ok = node_res is None or node_res[0]
    deployable = auto_ok and audits_ok and node_ok

    wrote = None
    if write:
        if auto_ok or force:
            out_path = out_path or str(Path(in_path).with_suffix(f".{APP_VERSION}.gs"))
            Path(out_path).write_text(cur, encoding="utf-8")
            wrote = out_path
        else:
            wrote = None

    rep = write_report(Path(report_dir or Path(in_path).parent), applied, failed, audits, node_res, MANUAL, deployable, wrote, force)
    print("DRY-RUN" if not write else ("WROTE " + wrote if wrote else "KHÔNG GHI (còn auto patch lỗi; dùng --force chỉ để debug)"))
    print("  auto: %d áp / %d lỗi | audit: %d/%d đạt | node: %s | report: %s" % (
        len(applied), len(failed), sum(1 for _, _, ok, _, _ in audits if ok), len(audits),
        "OK" if node_ok else "FAIL", rep))
    print("  status:", "DEPLOYABLE_CANDIDATE" if deployable else "NOT_DEPLOYABLE_YET")
    if failed:
        for pid, fid, st in failed:
            print("  ❌ %s (%s) matches=%s %s" % (pid, fid, st.get("matches"), st.get("note")))
    for aid, desc, ok, n, note in audits:
        if not ok:
            print("  audit ❌ %s n=%s %s" % (aid, n, note or ""))
    # Exit code nghiêm ngặt: 0 chỉ khi deployable candidate. --force không biến file lỗi thành OK.
    return 0 if deployable else (1 if failed or not node_ok else 2)


# ---------------- selftest ----------------
FIXTURE = """var CONFIG = {
  ROOT_FOLDER_ID: '11Rkwf3nhudPNNcsGlloV8acaXiXqdutJ'
};
function token_(){ return 't'; }
function resolveCatFolderId_(c){ return null; }
function resolveFolder_(p){
  if(p.folderId) return p.folderId;
  if(p.cat){ var fid=resolveCatFolderId_(p.cat); if(fid) return fid; }
  return p.toFolderId || CONFIG.ROOT_FOLDER_ID;
}
function provenance_(p, sha, url){
  return {soHieu:p.soHieu||'', nam:p.nam||'', loai:p.loai||'', coquan:p.coquan||'',
          hieuLuc:p.hieuLuc||'', sha256:sha||'', sourceUrl:url||'', ingestedAt:new Date().toISOString()};
}
function doImportExt_(p){
  var list=p.files;
  if(!list || !list.length) throw new Error('importext: thiếu files[]');
}
function doBatch_(p){
  var ops=p.ops; if(typeof ops==='string') ops=JSON.parse(ops);
  if(!Array.isArray(ops)) throw new Error('ops phải là mảng');
  var results=[], done=0, failed=0;
  ops.forEach(function(op,i){
    op=op||{};
    try{ var r=dispatchAction_(op.action, op); var okFlag=(r && r.ok!==false);
      results.push({i:i, action:op.action, ok:okFlag, result:r}); okFlag?done++:failed++;
    }catch(e){ results.push({i:i, action:op.action, ok:false, error:String(e && e.message || e)}); failed++; }
  });
  return {ok:failed===0, done:done, failed:failed, results:results};
}
function doFetchUrlToDrive_(p){
  if(!p.url) return jsonOut_({ok:false});
  return jsonOut_({ok:true, version:'2.15.0', note:'Đã về _HOP_NAP — tiếp tục dedup/VBHN-first rồi source_add (GDoc).'});
}
function doPerf_(){ var q="'"+CONFIG.ROOT_FOLDER_ID+"' in parents"; return q; }
function dispatchAction_(action, p){
  switch(action){
    case 'ping':         return {ok:true, pong:true, ts:new Date().toISOString(), version:'2.20.0'};
    case 'config':       return doConfigView_(p);
    // comment: case 'config':       return doConfigView_(p);
    /* --- v2.12 --- */
  }
}
function doBootstrap_(){ return {ok:true, version:'2.14.0', rootId:rootId}; }
function doConfigView_(){ return {ok:true, version:'2.11.0', config:eff}; }
function doRegen2_(){ return [['version', '2.14.0']]; }
function doManifestExport_(){ var out={ version: '2.20.0', schema: 'uniform-v1' }; return {schema_version:'2.20.0'}; }
function doWriteConfig_(p){ var cfile={getId:function(){return 'id'}}; }
function doReadConfig_(p){ return {}; }
function fetchBlob_(url, title){ return null; }
"""


def selftest() -> int:
    d = Path(tempfile.mkdtemp())
    f = d / "Code.gs"
    f.write_text(FIXTURE, encoding="utf-8")
    only = {"APP_VERSION", "rootId_helper", "privateConfigFile_helper", "ver_ping", "ver_boot", "ver_configview",
            "ver_regen2", "ver_manifest_out", "ver_manifest_schema", "configview_alias", "fetch_jsonout", "fetch_version",
            "importext_norm", "batch_cap", "batch_no_nested", "provenance", "resolveFolder", "global_root"}
    # process trả NOT_DEPLOYABLE vì audit manual fail — selftest chỉ kiểm engine và applied text.
    process(str(f), str(d / "out.gs"), write=True, force=False, only=only, report_dir=str(d))
    out = (d / "out.gs").read_text(encoding="utf-8")
    checks = [
        ("APP_VERSION chèn", f"var APP_VERSION = '{APP_VERSION}';" in out),
        ("ping dùng APP_VERSION", "version:APP_VERSION" in out),
        ("configView alias không đếm comment", "case 'configView':   return doConfigView_(p);" in out),
        ("fetch không còn jsonOut", "return jsonOut_(" not in out.split("function doFetchUrlToDrive_")[1].split("function doPerf_")[0]),
        ("provenance lowercase", "sohieu:p.soHieu||p.sohieu" in out),
        ("resolveFolder fail-closed", "throw new Error('resolveFolder_" in out and "return rootId_();" in out),
        ("batch cap", "ops.length>30" in out),
        ("batch no nested", "op.action==='batch'" in out),
        ("root def giữ nguyên", "ROOT_FOLDER_ID: '11Rkwf3" in out),
        ("doPerf root → rootId_()", "rootId_()" in out.split("doPerf_")[1].split("dispatchAction_")[0]),
        ("privateConfigFile helper", "function privateConfigFile_(fileId){" in out),
    ]
    nc = node_check_text(out)
    checks.append(("node --check out", nc is None or nc[0]))
    ok = sum(1 for _, c in checks if c)
    for n, c in checks:
        print("  [%s] %s" % ("OK" if c else "FAIL", n))
    print("== apply_gs_patches selftest %d/%d ==" % (ok, len(checks)))
    return 0 if ok == len(checks) else 1


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp")
    ap.add_argument("--out", dest="out")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--force", action="store_true", help="Ghi cả khi còn auto patch lỗi; exit code vẫn khác 0 nếu chưa deployable")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.inp:
        ap.print_help()
        return 1
    return process(a.inp, a.out, a.write, a.force)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
