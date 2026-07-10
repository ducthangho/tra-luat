# -*- coding: utf-8 -*-
"""tl_core.profile_mgmt — I4 (v1.34.7): tách NGUYÊN VĂN cụm quản trị profile từ scripts/tl.py
(profile-info/list/use/rename/delete/files/manifest/adopt/doctor/index/create/rebuild-registry + helper
riêng-cụm). Hạ tầng profile DÙNG CHUNG (_apply_profile_env/_profile_lookup/_read_config_record/
_profiles_from_config/_persist_profile_config/_profile_policy_error/_active_profile…) GIỮ Ở TL.
Hành vi khoá bởi 4 wiring r74a trên FIXTURE CONFIG + golden hygiene_ops_plan_fixture_config."""
from __future__ import annotations

import argparse   # noqa: F401
import datetime   # noqa: F401
import hashlib    # noqa: F401
import json       # noqa: F401
import os         # noqa: F401
import re         # noqa: F401
import shutil     # noqa: F401
import subprocess # noqa: F401
import sys        # noqa: F401
import tempfile   # noqa: F401
import time       # noqa: F401
import zipfile    # noqa: F401
from pathlib import Path  # noqa: F401

_TL = None


def bind(tl_module) -> None:
    """REBASE __globals__ từng hàm đã chuyển về namespace SỐNG của tl (khuôn I1-I3)."""
    global _TL
    _TL = tl_module
    import types
    g = globals()
    tg = tl_module.__dict__
    for _n, _fn in list(g.items()):
        if isinstance(_fn, types.FunctionType) and _fn.__module__ == __name__ and _n != "bind":
            _re = types.FunctionType(_fn.__code__, tg, _n, _fn.__defaults__, _fn.__closure__)
            _re.__kwdefaults__ = _fn.__kwdefaults__
            _re.__doc__ = _fn.__doc__
            _re.__module__ = __name__
            g[_n] = _re



def _profile_rebuild_partition(entries: list[dict], root_file_ids: set[str],
                               keep_notebook: str) -> tuple[list[dict], list[dict], dict]:
    """PURE: chia keep/drop cho recovery. Giữ file trong own-root, notebook đích, và mọi ref."""
    keep, drop = [], []
    reasons = {"root_tree": 0, "notebook": 0, "ref": 0}
    for entry in entries:
        drive_id = str(entry.get("drive_id") or entry.get("id") or entry.get("gdoc_id") or "").strip()
        notebook_id = str(entry.get("nlm_notebook_id") or "").strip()
        row_kind = str(entry.get("row_kind") or "own").strip().lower()
        why = []
        if drive_id in root_file_ids:
            why.append("root_tree"); reasons["root_tree"] += 1
        if notebook_id == keep_notebook:
            why.append("notebook"); reasons["notebook"] += 1
        if row_kind == "ref":
            why.append("ref"); reasons["ref"] += 1
        item = {"drive_id": drive_id, "name": entry.get("name") or "",
                "nlm_notebook_id": notebook_id, "row_kind": row_kind}
        if why:
            item["keep_reason"] = why
            keep.append(item)
        elif drive_id:
            drop.append(item)
    return keep, drop, reasons


def cmd_profile_rebuild_registry(a) -> int:
    """Phục hồi registry profile bị phình.

    Giữ hợp của: (1) file thật trong cây rootFolderId của profile; (2) dòng thuộc notebook cần giữ;
    (3) row_kind=ref. DRY mặc định; apply cần --confirm yes. Không suy dòng own chỉ từ notebook.
    """
    profile = _active_profile()
    if profile == DEFAULT_PROFILE:
        print("[tl] profile-rebuild-registry chỉ dùng cho profile dự án, không dùng trên vbqppl.", file=sys.stderr)
        return 2
    _perr = _profile_policy_error(require_registry=True, require_manifest=False, forbid_inherit=True)
    if _perr:
        return _emit_profile_policy_error(_perr, getattr(a, "json", False))
    # ⛔ SỰ CỐ 2026-06-30: profile dự án registryDocId RỖNG → reg_delete rơi vào registry NỀN VBQPPL → XÓA SẠCH 766 dòng.
    # CHẶN: profile-rebuild CHỈ chạy khi profile có registryDocId RIÊNG (scope != base), nếu không sẽ phá base.
    _prof_reg = (os.environ.get("TL_REGISTRY_DOC_ID") or "").strip()
    if not _prof_reg:
        print("[tl] ⛔ PROFILE_REGISTRY_ID_EMPTY_WOULD_CLOBBER_BASE: profile dự án '%s' KHÔNG có registryDocId riêng → "
              "reg_delete sẽ rơi vào registry NỀN VBQPPL và XÓA NHẦM. Tạo registry riêng + ghi registryDocId vào config "
              "TRƯỚC. (KHÔNG chạy rebuild khi chưa tách registry.)" % profile, file=sys.stderr)
        return 2
    keep_notebook = (a.keep_notebook or os.environ.get("TL_NOTEBOOK_ID") or "").strip()
    root_id = (os.environ.get("TL_ROOT_FOLDER_ID") or "").strip()
    if not keep_notebook:
        print("[tl] cần --keep-notebook <notebookId> hoặc notebookId trong profile config.", file=sys.stderr)
        return 2
    if not root_id:
        print("[tl] profile thiếu rootFolderId; không thể xác định dòng own an toàn.", file=sys.stderr)
        return 2
    if a.apply and a.confirm != "yes":
        print("[tl] --apply cần --confirm yes vì reg_delete là thao tác phá hủy.", file=sys.stderr)
        return 2

    g = _gas()
    ping = g.get("ping")
    if ping.get("version") != EXPECT_VERSION:
        print(f"[tl] webapp version={ping.get('version')} ≠ {EXPECT_VERSION}; dừng phục hồi để tránh lệch contract.",
              file=sys.stderr)
        return 3

    tree = g.get("list", folderId=root_id, recursive="true")
    if tree.get("ok") is False:
        print(json.dumps({"ok": False, "error": "PROFILE_ROOT_LIST_FAILED", "detail": tree},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    if tree.get("capped"):
        print(json.dumps({"ok": False, "error": "PROFILE_ROOT_LIST_CAPPED", "count": tree.get("count"),
                          "note": "Không xóa khi danh sách cây own chưa đầy đủ."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    # D2 (log rà): LOẠI file HẠ TẦNG (registry sheet + manifest + bản registry orphan trùng) khỏi cây own —
    # chúng nằm TRONG rootFolderId nhưng KHÔNG phải văn bản corpus; trước regen2 NUỐT thành dòng "corpus" rác
    # (count 8 vs 5 thật). Loại theo: registryDocId (config), mime spreadsheet/json, tên chứa registry/manifest.
    _reg_doc_id = (os.environ.get("TL_REGISTRY_DOC_ID") or "").strip()
    def _is_infra_file(x: dict) -> bool:
        mime = str(x.get("mimeType") or x.get("mime") or "").lower()
        nm = _strip_accents(str(x.get("name") or "")).lower()
        # VĂN BẢN THẬT (GDoc/PDF/Word) KHÔNG BAO GIỜ là infra → chặn false-positive dù tên lạ.
        if any(t in mime for t in ("vnd.google-apps.document", "pdf", "wordprocessing", "msword")):
            return False
        # infra = Google Sheet (registry) / file .json (manifest) / tên rõ là registry/manifest (orphan copy).
        if "spreadsheet" in mime or mime.endswith("/json") or nm.endswith(".json"):
            return True
        return any(t in nm for t in ("registry", "manifest", "reg_query"))
    root_file_ids = {
        str(x.get("id") or "") for x in (tree.get("items") or [])
        if x.get("type") != "folder" and x.get("id")
        and str(x.get("id")) != _reg_doc_id and not _is_infra_file(x)
    }

    me = g.get("manifest_export")
    manifest_id = me.get("manifestId")
    if not manifest_id:
        print(json.dumps({"ok": False, "error": "PROFILE_MANIFEST_EXPORT_FAILED", "detail": me},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    root_file_ids.discard(manifest_id)   # D2: manifest file (nếu nằm trong rootFolder) KHÔNG phải corpus
    downloaded = g.get("download", fileId=manifest_id)
    try:
        manifest = json.loads(base64.b64decode(downloaded.get("b64") or "").decode("utf-8"))
        entries = manifest.get("entries") or manifest.get("files") or []
    except Exception as exc:
        print(json.dumps({"ok": False, "error": "PROFILE_MANIFEST_READ_FAILED", "detail": str(exc)},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2

    keep, drop, reasons = _profile_rebuild_partition(entries, root_file_ids, keep_notebook)

    plan = {
        "ok": True,
        "profile": profile,
        "rootFolderId": root_id,
        "keep_notebook": keep_notebook,
        "manifest_entries": len(entries),
        "root_files": len(root_file_ids),
        "keep": len(keep),
        "drop": len(drop),
        "keep_reason_hits": reasons,
        "drop_sample": [x["name"] for x in drop[:20]],
        "mode": "APPLY" if a.apply else "DRY",
    }
    if not a.apply:
        plan["note"] = "Kiểm tra plan; thực thi bằng --apply --confirm yes."
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    results = []
    drive_ids = [x["drive_id"] for x in drop]
    for start in range(0, len(drive_ids), 200):
        chunk = drive_ids[start:start + 200]
        res = g.post("reg_delete", drive_ids=chunk, confirm="yes", require_removed="no")
        results.append(res)
        if res.get("ok") is False:
            plan.update({"ok": False, "reg_delete_batches": results,
                         "error": "PROFILE_REBUILD_PARTIAL_FAILURE"})
            print(json.dumps(plan, ensure_ascii=False, indent=2))
            return 1
    refreshed = g.get("manifest_export")
    plan.update({"applied": True, "reg_delete_batches": results, "manifest_export": refreshed,
                 "ok": refreshed.get("ok") is not False})
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0 if plan["ok"] else 1


def _profile_info_from_config(config_path: str | None, profile: str | None = None) -> dict:
    cfg = {}
    used = ""
    for p in _config_candidates(config_path):
        if Path(p).exists():
            cfg = _read_json_file(p)
            if cfg:
                used = p
                break
    if not cfg:
        return {
            "ok": bool(os.environ.get("TL_WEBAPP") and os.environ.get("TL_TOKEN")),
            "source": "env-only",
            "profile": profile or os.environ.get("TL_PROFILE") or DEFAULT_PROFILE,
            "profile_found": False,
            "note": "Không đọc được config v2; chỉ có thể dùng env hiện tại.",
            "env": {
                "TL_PROFILE": os.environ.get("TL_PROFILE", ""),
                "TL_ROOT_FOLDER_ID": os.environ.get("TL_ROOT_FOLDER_ID", ""),
                "TL_META_FOLDER_ID": os.environ.get("TL_META_FOLDER_ID", ""),
                "TL_NOTEBOOK_ID": os.environ.get("TL_NOTEBOOK_ID", ""),
                "TL_REGISTRY_DOC_ID": os.environ.get("TL_REGISTRY_DOC_ID", ""),
                "TL_MANIFEST_ID": os.environ.get("TL_MANIFEST_ID", ""),
                "TL_MANIFEST_SCOPE": os.environ.get("TL_MANIFEST_SCOPE", ""),
            },
        }
    applied = _apply_profile_env(cfg, profile)
    return {
        "ok": True,
        "source": used,
        "schema": cfg.get("schema", 1),
        "config_of_record": "Đọc tra_luat_config.json VBQPPL trước để lấy webappUrl/token, rồi overlay profile.",
        "vbqppl_config_drive_id": VBQPPL_CONFIG_DRIVE_ID,
        "defaultProfile": cfg.get("defaultProfile", DEFAULT_PROFILE),
        "activeProfile": applied["profile"],
        "profile_found": applied["profile_found"],
        "profiles": applied["profiles"],
        "profile": applied["profile_data"],
        "env": {
            "TL_PROFILE": os.environ.get("TL_PROFILE", ""),
            "TL_ROOT_FOLDER_ID": os.environ.get("TL_ROOT_FOLDER_ID", ""),
            "TL_META_FOLDER_ID": os.environ.get("TL_META_FOLDER_ID", ""),
            "TL_NOTEBOOK_ID": os.environ.get("TL_NOTEBOOK_ID", ""),
            "TL_REGISTRY_DOC_ID": os.environ.get("TL_REGISTRY_DOC_ID", ""),
            "TL_MANIFEST_ID": os.environ.get("TL_MANIFEST_ID", ""),
            "TL_MANIFEST_SCOPE": os.environ.get("TL_MANIFEST_SCOPE", ""),
        },
    }


def cmd_profile_info(a) -> int:
    out = _profile_info_from_config(getattr(a, "config", None), getattr(a, "profile", None))
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2


def _profile_manifest_entries_for(profile: str | None, config_path: str | None = None,
                                  refresh: bool = False) -> tuple[list[dict], str | None]:
    if refresh:
        try:
            load_creds(config_path, profile)
        except SystemExit as e:
            return [], str(e)
    else:
        apply_profile_offline(config_path, profile)
    try:
        return _manifest_entries(refresh=refresh), None
    except SystemExit as e:
        return [], str(e)
    except Exception as e:  # noqa: BLE001
        if refresh:
            return [], str(e)
        try:
            load_creds(config_path, profile)
            return _manifest_entries(refresh=False), None
        except SystemExit as e2:
            return [], str(e2)
        except Exception as e2:  # noqa: BLE001
            return [], str(e2)


def cmd_profile_list(a) -> int:
    path, cfg = _read_config_record(getattr(a, "config", None))
    if getattr(a, "discover", False):   # B (v1.30.0): quét Drive LIVE đối chiếu config — xem _profile_list_discover
        with _ProfileEnvGuard():        # ép scope NỀN bên trong nhưng KHÔNG nhiễm env caller cùng-process
            return _profile_list_discover(a, path, cfg)
    active = _selected_profile_name(getattr(a, "profile", None), cfg)
    rows = _profile_config_rows(cfg, active)
    out = {"ok": bool(cfg), "config": path, "defaultProfile": cfg.get("defaultProfile") or DEFAULT_PROFILE,
           "activeProfile": active, "profiles": rows}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        if not cfg:
            print("[tl] Không thấy config; chạy `tl init-config --from-public` hoặc truyền --config.", file=sys.stderr)
            return 2
        print(f"== profiles · config={path} · default={out['defaultProfile']} · active={active} ==")
        for r in rows:
            mk = "*" if r["active"] else ("d" if r["default"] else " ")
            print(f" {mk} {r['profile']:24s} nb={r['notebookId'] or '-'} root={r['rootFolderId'] or '-'} "
                  f"registry={r['registryDocId'] or '-'} manifest={r['manifestId'] or '-'} "
                  f"cat={r['categories'] or '-'} scope={r['manifestScope'] or '-'}")
    return 0 if cfg else 2


def cmd_profile_use(a) -> int:
    name = (getattr(a, "name", None) or "").strip()
    path, cfg = _read_config_record(getattr(a, "config", None))
    profs = _profiles_from_config(cfg)
    plan = {"ok": name in profs, "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
            "config": path, "profile": name, "currentDefault": cfg.get("defaultProfile") or DEFAULT_PROFILE,
            "note": "DRY mặc định; --apply mới ghi defaultProfile vào config."}
    if name not in profs:
        plan["error"] = "PROFILE_NOT_FOUND"
        print(json.dumps(plan, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    if not getattr(a, "apply", False):
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    out = _set_default_profile_config(getattr(a, "config", None), name)
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2


def cmd_profile_rename(a) -> int:
    old, new = (a.old or "").strip(), (a.new or "").strip()
    path, cfg = _read_config_record(getattr(a, "config", None))
    prof = (_profiles_from_config(cfg).get(old) or {}) if cfg else {}
    plan = {"ok": bool(prof) and old != DEFAULT_PROFILE and bool(new),
            "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
            "config": path, "old": old, "new": new,
            "rename_assets": bool(getattr(a, "rename_assets", False)),
            "assets": _profile_asset_ids(prof),
            "note": "Đổi key config trước; --rename-assets mới đổi tên folder/registry/manifest trên Drive."}
    if not plan["ok"]:
        plan["error"] = "PROFILE_RENAME_PLAN_INVALID"
        print(json.dumps(plan, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    if not getattr(a, "apply", False):
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    asset_results = []
    if getattr(a, "rename_assets", False):
        load_creds(getattr(a, "config", None), DEFAULT_PROFILE)
        g = _gas()
        slug = _profile_file_slug(new)
        names = {"root": new, "registry": f"tra_luat_registry.{slug}", "manifest": f"tra_luat_manifest.{slug}.json"}
        for it in plan["assets"]:
            role, fid = it["role"], it["fileId"]
            if role not in names:
                continue
            try:
                r = g.get("rename", fileId=fid, name=names[role])
            except Exception as e:  # noqa: BLE001
                r = {"ok": False, "error": str(e)}
            asset_results.append({"role": role, "fileId": fid, "targetName": names[role], "result": r})
    out = _rename_profile_config(getattr(a, "config", None), old, new, getattr(a, "force", False))
    out["asset_renames"] = asset_results
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2


def cmd_profile_delete(a) -> int:
    name = (a.name or "").strip()
    path, cfg = _read_config_record(getattr(a, "config", None))
    prof = (_profiles_from_config(cfg).get(name) or {}) if cfg else {}
    entries, merr = _profile_manifest_entries_for(name, getattr(a, "config", None), getattr(a, "refresh", False)) if prof else ([], None)
    source_ids = _profile_live_source_ids(entries)
    # (MERGE Claude, an toàn) GUARD shared_source_id: KHÔNG xóa nguồn NLM dùng chung ≥2 drive_id (xóa 1 gãy link kia — đúng
    # 2 FALSE-LINK hiện có). Tách deletable/blocked; chỉ xóa deletable, báo blocked để sửa shared trước.
    nlm_deletable, nlm_blocked_shared = _profile_deletable_sources(entries, source_ids)
    plan = {"ok": bool(prof) and name != DEFAULT_PROFILE,
            "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
            "config": path, "profile": name, "assets": _profile_asset_ids(prof),
            "manifest_error": merr, "manifest_rows": len(entries),
            "nlm_source_count": len(source_ids), "nlm_source_ids": source_ids[:50],
            "nlm_deletable": nlm_deletable[:50], "nlm_blocked_shared_source_id": nlm_blocked_shared,
            "delete_nlm_sources": bool(getattr(a, "delete_nlm_sources", False)),
            "trash_assets": bool(getattr(a, "trash_assets", False)),
            "default_mode": "detach (gỡ config, GIỮ Drive+NLM) trừ khi có --delete-nlm-sources/--trash-assets",
            "note": "DRY mặc định. --apply --confirm yes gỡ profile khỏi config (backup trước); NLM/Drive cần cờ riêng. "
                    "Nguồn shared_source_id KHÔNG bị xóa (sửa map_set/reg_clear tách trước)."}
    if nlm_blocked_shared:
        plan["shared_warning"] = (f"⚠ {len(nlm_blocked_shared)} nguồn NLM DÙNG CHUNG source_id với văn bản KHÁC — "
                                  "KHÔNG xóa (gãy link). Sửa shared_source_id trước khi purge.")
    if not plan["ok"]:
        plan["error"] = "PROFILE_DELETE_PLAN_INVALID"
        print(json.dumps(plan, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    if not getattr(a, "apply", False):
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    if getattr(a, "confirm", "") != "yes":
        print(json.dumps({**plan, "ok": False, "error": "CONFIRM_YES_REQUIRED"}, ensure_ascii=False, indent=2),
              file=sys.stderr)
        return 2
    # (MERGE Claude) backup config TRƯỚC khi gỡ → hồi phục được
    bkp = None
    try:
        if path and Path(path).exists():
            bkp = str(Path(path).with_suffix(f".{_profile_file_slug(name)}.bak.json"))
            _write_json_atomic(Path(bkp), cfg)
    except Exception:
        bkp = None
    nlm_results = []
    # v1.29.3 (AUDIT B1 #6): JOURNAL vòng xóa NLM (BẤT KHẢ NGHỊCH — forensic) + vòng trash Drive (restore được) —
    # crash giữa vòng → `tl journal <run>` chỉ RÕ đã xóa/trash tới đâu (trước đây mất dấu). Op non-reg → resume/undo không đụng.
    _pd_rid = None
    if getattr(a, "delete_nlm_sources", False) or getattr(a, "trash_assets", False):
        _pd_rid = _apply_journal_start("profile-delete-assets", {"profile": name,
                                                                 "nlm": len(nlm_deletable) if getattr(a, "delete_nlm_sources", False) else 0,
                                                                 "trash": len(plan.get("assets") or []) if getattr(a, "trash_assets", False) else 0})
    if getattr(a, "delete_nlm_sources", False):
        nc = _imp("nlm_cli")
        for sid in nlm_deletable:       # CHỈ xóa nguồn KHÔNG shared
            _journal_append(_pd_rid, {"t": "intent", "op": "nlm_source_delete", "key": sid, "set": {"irreversible": True}})
            _dr = nc.source_delete(sid)
            _journal_append(_pd_rid, {"t": "commit", "op": "nlm_source_delete", "key": sid, "ok": bool(_dr.get("ok"))})
            nlm_results.append({"source_id": sid, "result": _dr})
    trash_results = []
    if getattr(a, "trash_assets", False):
        load_creds(getattr(a, "config", None), DEFAULT_PROFILE)
        g = _gas()
        for it in plan["assets"]:
            _journal_append(_pd_rid, {"t": "intent", "op": "drive_trash", "key": it["fileId"], "set": {"restore": "tl ... restore"}})
            try:
                r = g.get("trash", fileId=it["fileId"], confirm="yes")
            except Exception as e:  # noqa: BLE001
                r = {"ok": False, "error": str(e)}
            _journal_append(_pd_rid, {"t": "commit", "op": "drive_trash", "key": it["fileId"], "ok": bool(r.get("ok"))})
            trash_results.append({**it, "result": r})
    out = _remove_profile_config(getattr(a, "config", None), name)
    out["config_backup"] = bkp
    out["nlm_deletes"] = nlm_results
    out["nlm_blocked_shared_source_id"] = nlm_blocked_shared
    out["asset_trash"] = trash_results
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2


def cmd_profile_files(a) -> int:
    profile = getattr(a, "target_profile", None) or getattr(a, "profile", None)
    entries, err = _profile_manifest_entries_for(profile, getattr(a, "config", None), getattr(a, "refresh", False))
    if err:
        print(json.dumps({"ok": False, "error": err, "profile": profile or _active_profile()}, ensure_ascii=False, indent=2),
              file=sys.stderr)
        return 2
    rows = []
    for e in entries:
        if getattr(a, "row_kind", None) and _entry_row_kind(e) != str(a.row_kind).lower():
            continue
        if getattr(a, "nlm", False) and not _entry_nlm(e):
            continue
        if getattr(a, "no_nlm", False) and _entry_nlm(e):
            continue
        if getattr(a, "corpus", False) and not _entry_corpus_true(e):
            continue
        if getattr(a, "no_corpus", False) and _entry_corpus_true(e):
            continue
        q = _strip_accents(getattr(a, "name", "") or "").lower()
        if q and q not in _strip_accents(_entry_name(e)).lower():
            continue
        rows.append({"drive_id": _entry_drive_id(e), "name": _entry_name(e), "sohieu": _entry_sohieu(e),
                     "cat": _entry_cat(e), "row_kind": _entry_row_kind(e), "corpus": _entry_corpus_true(e),
                     "nlm_source_id": _entry_nlm(e), "nlm_notebook_id": _entry_nlm_notebook_id(e),
                     "hieuluc": e.get("hieuluc") or e.get("hieu_luc") or ""})
    limit = getattr(a, "limit", None)
    shown = rows[:limit] if limit else rows
    out = {"ok": True, "profile": profile or _active_profile(), "count": len(rows), "shown": len(shown), "rows": shown}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== profile-files · profile={out['profile']} · {len(rows)} rows ==")
        for r in shown:
            print(f"  {r['drive_id'][:12]:12s} {r['row_kind']:4s} nlm={'Y' if r['nlm_source_id'] else '-'} "
                  f"corpus={'Y' if r['corpus'] else '-'} {r['sohieu'] or '-':18s} {r['name'][:100]}")
    return 0


def cmd_profile_manifest(a) -> int:
    profile = getattr(a, "target_profile", None) or getattr(a, "profile", None)
    if getattr(a, "refresh", False):
        load_creds(getattr(a, "config", None), profile)
    else:
        apply_profile_offline(getattr(a, "config", None), profile)
    data = _load_manifest_full(refresh=getattr(a, "refresh", False))
    if data.get("ok") is False:
        print(json.dumps(data, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    if getattr(a, "out", None):
        Path(a.out).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    entries = data.get("entries") or data.get("files") or data.get("rows") or []
    summary = {"ok": True, "profile": profile or _active_profile(), "manifestId": data.get("manifestId"),
               "count": len(entries), "out": getattr(a, "out", None)}
    if getattr(a, "json", False):
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def _create_profile_manifest_json(g, meta_id: str, profile: str, root_id: str, notebook_id: str) -> dict:
    slug = _profile_file_slug(profile)
    body = json.dumps(_manifest_placeholder(profile, root_id, notebook_id), ensure_ascii=False, indent=2)
    up = g.post("upload", b64=_b64_text(body), name=f"tra_luat_manifest.{slug}.json",
                mime="application/json", folderId=meta_id, convert="false",
                register="false", share="false", force="true")
    mid = up.get("fileId") or up.get("id")
    return {"ok": bool(mid), "manifestId": mid, "upload": up}


def _profile_list_discover(a, path, cfg) -> int:
    """B (v1.30.0): `profile-list --discover` — quét Van_ban_thuong LIVE, đối chiếu config, cảnh báo profile-thật-
    trên-Drive chưa đăng ký (kèm lệnh profile-adopt điền sẵn), vỏ rỗng, asset lạc gốc. READ-ONLY (không ghi gì)."""
    try:
        load_creds(getattr(a, "config", None), DEFAULT_PROFILE)   # webapp NỀN (như profile-create) — KHÔNG forward scope profile
        g = _gas()
        boot = g.get("bootstrap")
        vbt_id = boot.get("vanBanThuongId") if isinstance(boot, dict) else None
        if not vbt_id:
            print(json.dumps({"ok": False, "error": "NO_VAN_BAN_THUONG_ID", "bootstrap": boot},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        scan = _discover_scan_vbthuong(g, vbt_id, folder_cap=int(getattr(a, "folder_cap", None) or 60))
    except SystemExit as e:
        print(f"[tl] profile-list --discover cần webapp LIVE (Cowork): {e}", file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": f"DISCOVER_SCAN_FAILED: {e}"}, ensure_ascii=False), file=sys.stderr)
        return 2
    rep = _discover_classify(scan.get("folders") or [], scan.get("root_files") or [],
                             _profiles_from_config(cfg), vbt_id=vbt_id)
    out = {"ok": True, "config": path, "vanBanThuongId": vbt_id,
           "folder_total": scan.get("folder_total"), "scanned": len(scan.get("folders") or []),
           "capped": bool(scan.get("capped")), **rep}
    if scan.get("capped"):
        out["warning"] = (f"CHỈ quét {out['scanned']}/{out['folder_total']} thư mục (cap) — chạy lại với "
                          f"--folder-cap {out['folder_total']} để phủ đủ; kết luận 'config_only' có thể là giả khi cap.")
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
        return 0
    print(f"== profile-list --discover · Van_ban_thuong={vbt_id} · {out['scanned']}/{out['folder_total']} thư mục ==")
    for r in rep["folders"]:
        mark = {"in_config": "✅", "unregistered_profile": "🟠", "empty_folder": "⚪", "plain_folder": "·"}.get(r["status"], "?")
        print(f" {mark} {str(r['folder_name'])[:44]:44s} {r['status']:22s} items={r['n_items']}"
              + (f" profile={r['profile']}" if r.get("profile") else ""))
        if r.get("suggest"):
            print(f"      $ {r['suggest']}")
    for m in rep["misplaced_root_assets"]:
        print(f" 🔴 LẠC GỐC: {m['name']} ({m['kind']}) id={m['id']}\n      {m['note']}")
    for c in rep["config_only"]:
        print(f" ⚠ CONFIG-ONLY: {c['profile']} root={c['rootFolderId']} — {c['note']}")
    if out.get("warning"):
        print(f" ⚠ {out['warning']}")
    return 0


def cmd_profile_adopt(a) -> int:
    with _ProfileEnvGuard():            # review v1.30.0: không nhiễm env profile của caller cùng-process
        return _cmd_profile_adopt_impl(a)


def _cmd_profile_adopt_impl(a) -> int:
    """C (v1.30.0): SEED profile ĐÃ CÓ hạ tầng trên Drive vào config (khác profile-create = dựng MỚI từ đầu).
    Dò registry Sheet + manifest JSON trong folder (+_meta); GUARD registry (mime Sheet thật / ≠ Doc legacy
    1mATG / KHÔNG dùng-chung profile khác / schema REGISTRY_SCHEMA_COLS khi --apply); notebookId: --notebook >
    manifest JSON (chỉ khi manifest đúng profile). Ghi qua _persist_profile_config (journaled). DRY mặc định."""
    name = (getattr(a, "name", None) or "").strip()
    folder = (getattr(a, "folder", None) or "").strip()
    if not name or not folder:
        print("[tl] profile-adopt cần --name và --folder", file=sys.stderr)
        return 2
    if name == DEFAULT_PROFILE:
        print("[tl] REFUSE_ADOPT_DEFAULT_PROFILE: vbqppl là profile nền (webapp/token of-record).", file=sys.stderr)
        return 2
    path, cfg = _read_config_record(getattr(a, "config", None))
    existing = _profiles_from_config(cfg).get(name)
    existing = existing if isinstance(existing, dict) else None
    if existing and str(existing.get("rootFolderId") or "").strip() not in ("", folder):
        print(json.dumps({"ok": False, "error": "PROFILE_EXISTS_DIFFERENT_FOLDER", "profile": name,
                          "config_rootFolderId": existing.get("rootFolderId"), "requested_folder": folder,
                          "note": "Đổi --name, hoặc profile-rename/profile-delete profile cũ trước."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    try:
        load_creds(getattr(a, "config", None), DEFAULT_PROFILE)   # token NỀN, không forward scope profile
    except SystemExit as e:
        print(f"[tl] profile-adopt cần webapp LIVE (Cowork): {e}", file=sys.stderr)
        return 2
    g = _gas()
    finfo = _gas_get_retry(g, "info", fileId=folder)
    fmime = _mime_from_info(finfo) if isinstance(finfo, dict) else ""
    if not fmime.endswith("apps.folder"):
        print(json.dumps({"ok": False, "error": "FOLDER_ID_INVALID", "mime": fmime, "info": finfo},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    try:
        items = _gas_get_retry(g, "list", folderId=folder).get("items") or []
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": f"FOLDER_LIST_FAILED: {e}"}, ensure_ascii=False), file=sys.stderr)
        return 2
    meta = next((x for x in items if str(x.get("type")) == "folder" and str(x.get("name")) == "_meta"), None)
    if meta:
        try:
            items = items + (_gas_get_retry(g, "list", folderId=meta.get("id")).get("items") or [])
        except Exception:
            pass
    picked = _adopt_pick_assets(items, reg_override=(getattr(a, "registry", None) or "").strip(),
                                man_override=(getattr(a, "manifest", None) or "").strip())
    plan_errors = list(picked["errors"])
    if getattr(a, "bootstrap_manifest", False):
        plan_errors = [x for x in plan_errors if not x.startswith("MANIFEST_NOT_FOUND")]
    reg_id = str((picked["registry"] or {}).get("id") or "")
    _profs_all = _profiles_from_config(cfg)
    if reg_id:
        if reg_id == _LEGACY_REGISTRY_DOC_ID:
            plan_errors.append("REGISTRY_LEGACY_DOC_FORBIDDEN: id trùng Doc legacy 1mATG… (đọc RỖNG count=0 ảo) — KHÔNG dùng.")
        else:
            # Review v1.30.0 (CONFIRMED): CHẶN adopt registry đang thuộc profile KHÁC — --apply sẽ reg_addcols
            # (mutate Sheet) + 2 profile ghi chung 1 registry = phá doctrine own-assets.
            _owners = [n for n in _profile_asset_owners(_profs_all, reg_id) if n != name]
            if _owners:
                plan_errors.append(f"REGISTRY_SHARED_WITH_OTHER_PROFILE: registry {reg_id} đang thuộc profile "
                                   f"{_owners} — tách registry riêng (profile-create) thay vì dùng chung.")
            rmime = _mime_from_info(_gas_get_retry(g, "info", fileId=reg_id))
            if rmime and rmime != REGISTRY_SHEET_MIME:
                plan_errors.append(f"REGISTRY_NOT_SHEET_MIME: mime='{rmime}' — registry PHẢI là Google Sheet.")
    man_id = str((picked["manifest"] or {}).get("id") or "")
    if man_id:
        _mowners = [n for n in _profile_asset_owners(_profs_all, man_id) if n != name]
        if _mowners:
            plan_errors.append(f"MANIFEST_SHARED_WITH_OTHER_PROFILE: manifest {man_id} đang thuộc profile "
                               f"{_mowners} — mỗi profile 1 manifest riêng.")
    nb = (getattr(a, "notebook", None) or "").strip()
    nb_src = "flag" if nb else None
    _nb_warn = None
    if not nb and man_id:
        try:    # notebookId nằm sẵn trong manifest JSON của profile (schema _manifest_placeholder)
            d = _gas_get_retry(g, "download", fileId=man_id)
            if d.get("b64"):
                mj = json.loads(base64.b64decode(d["b64"]).decode("utf-8"))
                # Review v1.30.0 (CONFIRMED): manifest lạ (trường profile ≠ tên adopt) KHÔNG được cấp notebookId.
                nb, _nb_warn = _notebook_from_manifest_json(mj, name)
                nb_src = "manifest" if nb else None
        except Exception:
            pass
    prof_block = {"rootFolderId": folder, "metaFolderId": (meta or {}).get("id"),
                  "notebookId": nb, "registryDocId": reg_id, "manifestId": man_id,
                  "manifestScope": "own", "categories": "own"}
    plan = {"ok": not plan_errors, "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
            "config": path, "profile": name, "folder": folder, "picked": picked,
            "notebook_source": nb_src, "profile_block": prof_block, "errors": plan_errors,
            "warnings": (([_nb_warn] if _nb_warn else [])
                         + ([] if nb else ["NO_NOTEBOOK_ID: chưa xác định notebook — bổ sung --notebook hoặc config sau; "
                                           "lệnh NLM sẽ chặn tới khi có (đúng thiết kế, không fallback base)."])),
            "note": "DRY mặc định; --apply verify schema registry (reg_addcols idempotent) rồi ghi config.profiles "
                    "(journaled config_write). Adopt lại cùng folder = idempotent merge."}
    if plan_errors or not getattr(a, "apply", False):
        print(json.dumps(plan, ensure_ascii=False, indent=2), file=sys.stderr if plan_errors else sys.stdout)
        return 2 if plan_errors else 0
    ver = _verify_registry_sheet(g, reg_id)     # --apply: verify schema (heal cột thiếu — idempotent, cùng đường profile-create)
    if not ver.get("ok"):
        print(json.dumps({"ok": False, "step": "verify_registry_sheet", **ver}, ensure_ascii=False, indent=2),
              file=sys.stderr)
        return 2
    if getattr(a, "bootstrap_manifest", False) and not man_id:
        man = _create_profile_manifest_json(g, (meta or {}).get("id") or folder, name, folder, nb)
        if not man.get("ok"):
            print(json.dumps({"ok": False, "step": "bootstrap_manifest", **man}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        man_id = str(man.get("manifestId") or "")
        prof_block["manifestId"] = man_id
        try:
            g.get("manifest_export", registryDocId=reg_id, manifestId=man_id)
        except Exception as e:  # noqa: BLE001
            plan["warnings"].append(f"manifest_export bootstrap bỏ qua: {e}")
    cfgp = _persist_profile_config(getattr(a, "config", None), name, prof_block)
    out = {**plan, "ok": bool(cfgp), "registry_verify": ver, "config_written": cfgp,
           "next_steps": [f"tl --profile {name} profile-info  (kiểm registry Sheet + categories='own')",
                          f"tl --profile {name} boot --refresh",
                          "tl profile-index --rebuild --apply  (cập nhật sổ cái _PROFILES_INDEX)"]}
    if not cfgp:
        out["errors"] = ["CONFIG_WRITE_FAILED: không tìm được file config ghi được — truyền --config."]
    print(json.dumps(out, ensure_ascii=False, indent=2), file=sys.stdout if out["ok"] else sys.stderr)
    return 0 if out["ok"] else 2


def cmd_profile_doctor(a) -> int:
    with _ProfileEnvGuard():            # review v1.30.0: không nhiễm env profile của caller cùng-process
        return _cmd_profile_doctor_impl(a)


def _cmd_profile_doctor_impl(a) -> int:
    """D (v1.30.0): kiểm bất biến layout/hạ tầng mọi profile dự án trong config (hoặc --profile-name <p>).
    --fix --apply: move asset lạc chỗ vào _meta của profile (tạo _meta nếu thiếu; action `move` — fileId GIỮ NGUYÊN
    nên config KHÔNG phải đổi; journal drive_move). Asset dùng-chung ≥2 profile: KHÔNG auto-move (critical).
    rc: 0 sạch / 1 có finding / 2 lỗi chạy."""
    path, cfg = _read_config_record(getattr(a, "config", None))
    profs = _profiles_from_config(cfg)
    target = (getattr(a, "target_profile", None) or "").strip()
    names = [target] if target else [n for n in sorted(profs) if n != DEFAULT_PROFILE]
    if target and target not in profs:
        print(json.dumps({"ok": False, "error": "PROFILE_NOT_FOUND", "profile": target}, ensure_ascii=False),
              file=sys.stderr)
        return 2
    try:
        load_creds(getattr(a, "config", None), DEFAULT_PROFILE)
    except SystemExit as e:
        print(f"[tl] profile-doctor cần webapp LIVE (đọc parents/mime qua action info): {e}", file=sys.stderr)
        return 2
    g = _gas()
    findings, infos_all = [], {}
    for n in names:
        prof = profs.get(n) if isinstance(profs.get(n), dict) else {}
        infos = {}
        for key in ("registryDocId", "manifestId"):
            fid = str(prof.get(key) or "").strip()
            if not fid:
                continue
            try:
                fi = _gas_get_retry(g, "info", fileId=fid)
                f = fi.get("file") if isinstance(fi.get("file"), dict) else {}
                infos[fid] = {"mimeType": f.get("mimeType"), "parents": f.get("parents") or [],
                              "trashed": bool(f.get("trashed")), "name": f.get("name")}
            except Exception as e:  # noqa: BLE001
                findings.append({"check": "INFO_FAILED", "severity": "warn", "profile": n, "fileId": fid,
                                 "note": f"không đọc được info ({e}) — bỏ qua check layout/mime cho file này."})
        infos_all.update(infos)
        findings.extend(_doctor_check_profile(n, prof, infos))
    # Review v1.30.0 (CONFIRMED): asset dùng chung ≥2 profile trong config → BỎ fix-move, nâng critical
    # (move theo profile này phá layout profile kia). Soi trên TOÀN BỘ config, kể cả khi --profile-name 1 profile.
    findings = _strip_shared_fixes(findings, profs)
    fixes = [f for f in findings if f.get("fix")]
    out = {"ok": True, "mode": "APPLY" if getattr(a, "apply", False) else "DRY", "config": path,
           "profiles_checked": names, "findings": findings,
           "criticals": sum(1 for f in findings if f.get("severity") == "critical"),
           "fixable": len(fixes),
           "invariant": "LAYOUT: registry+manifest của profile nằm TRONG thư mục profile (root hoặc _meta).",
           "note": "DRY mặc định; --fix --apply move asset lạc chỗ vào _meta (fileId giữ nguyên — config không đổi)."}
    fix_results = []
    if getattr(a, "fix", False) and getattr(a, "apply", False) and fixes:
        rid = _apply_journal_start("profile-doctor-fix", {"fixes": len(fixes)})
        for f in fixes:
            n = f.get("profile")
            prof = profs.get(n) if isinstance(profs.get(n), dict) else {}
            dest = str(prof.get("metaFolderId") or "").strip()
            if not dest:    # tạo/tìm _meta dưới root profile rồi ghi bền vào config (journaled)
                mr = g.get("resolvefolder", name="_meta", parentId=str(prof.get("rootFolderId") or ""), create="true")
                dest = str((mr or {}).get("folderId") or "")
                if dest:
                    _persist_profile_config(getattr(a, "config", None), n, {"metaFolderId": dest})
            if not dest:
                fix_results.append({**f, "result": {"ok": False, "error": "NO_DEST_META"}})
                continue
            # Review v1.30.0 (CONFIRMED ×2): (a) KHÔNG kèm 'before' — op non-reg theo hợp đồng journal v1.29.1
            # (resume/undo CHỈ xử reg_*; kèm before sẽ làm undo sinh restore-op rác đẩy vào _journaled_reg_write);
            # parents cũ lưu trong set.from_parents (forensic/undo TAY). (b) move idempotent (re-move cùng đích
            # = no-op) → bọc _gas_get_retry chống timeout transient (trước đây 1 timeout = fix treo tới lần chạy sau).
            _journal_append(rid, {"t": "intent", "op": "drive_move", "key": f["fileId"],
                                  "set": {"toFolderId": dest, "from_parents": f.get("parents") or []}})
            try:
                mv = _gas_get_retry(g, "move", fileId=f["fileId"], toFolderId=dest)
            except Exception as e:  # noqa: BLE001
                mv = {"ok": False, "error": str(e)}
            _journal_append(rid, {"t": "commit", "op": "drive_move", "key": f["fileId"], "ok": bool(mv.get("ok"))})
            fix_results.append({**f, "result": mv, "moved_to": dest})
        out["fix_results"] = fix_results
        out["journal"] = rid
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== profile-doctor · {len(names)} profile · findings={len(findings)} (critical={out['criticals']}) ==")
        for f in findings:
            sev = {"critical": "🔴", "warn": "🟠"}.get(f.get("severity"), "·")
            print(f" {sev} [{f.get('profile')}] {f.get('check')}: {f.get('note')}")
            if f.get("fix"):
                print(f"      fix: move {f['fix']['fileId']} → {f['fix']['to'] or '_meta (sẽ tạo)'}")
        for r in fix_results:
            print(f" ▸ FIX {r.get('fileId')}: {'OK → ' + str(r.get('moved_to')) if (r.get('result') or {}).get('ok') else 'FAIL ' + str(r.get('result'))}")
        if not findings:
            print(" ✅ sạch — layout + hạ tầng profile đạt bất biến.")
    return 0 if not findings else 1


def _profile_index_rows(cfg: dict, folder_names: dict | None = None) -> list[dict]:
    """E (PURE, test offline): sinh dòng sổ cái _PROFILES_INDEX từ config — BẢN CHIẾU đọc-được;
    nguồn sự thật DUY NHẤT vẫn là config."""
    default = (cfg or {}).get("defaultProfile") or DEFAULT_PROFILE
    rows = []
    for pname, prof in sorted(_profiles_from_config(cfg or {}).items()):
        prof = prof if isinstance(prof, dict) else {}
        cats = prof.get("categories")
        rows.append({
            "profile": pname,
            "default": "yes" if pname == default else "",
            "rootFolderId": str(prof.get("rootFolderId") or ""),
            "folder_name": str((folder_names or {}).get(str(prof.get("rootFolderId") or "")) or ""),
            "notebookId": str(prof.get("notebookId") or ""),
            "registryDocId": str(prof.get("registryDocId") or ""),
            "manifestId": str(prof.get("manifestId") or ""),
            "categories": ("own-tree(45)" if isinstance(cats, dict) else str(cats or "")),
            "manifestScope": str(prof.get("manifestScope") or ""),
            "baseAlso": ("" if pname == DEFAULT_PROFILE else ("off" if prof.get("baseAlso") is False else "on")),
            "note": ("nền VBQPPL — webapp/token of-record" if pname == DEFAULT_PROFILE else ""),
        })
    return rows


def _profile_index_csv(rows: list[dict]) -> str:
    import csv as _csv
    import io as _io
    buf = _io.StringIO()
    w = _csv.DictWriter(buf, fieldnames=_PROFILES_INDEX_COLS, extrasaction="ignore")
    w.writeheader()
    for r in rows or []:
        w.writerow(r)
    return buf.getvalue()


def cmd_profile_index(a) -> int:
    with _ProfileEnvGuard():            # review v1.30.0: không nhiễm env profile của caller cùng-process
        return _cmd_profile_index_impl(a)


def _cmd_profile_index_impl(a) -> int:
    """E (v1.30.0): SỔ CÁI profile trên Drive — `Van_ban_thuong/_PROFILES_INDEX` (Google Sheet, BẢN CHIẾU từ config).
    DRY: in bảng/CSV. --rebuild --apply: upload CSV → copy_convert Sheet MỚI → trash bản cũ + CSV trung gian
    (upload KHÔNG ghi-đè-tại-chỗ ⇒ fail-safe tạo-trước-dọn-sau; sheetId ĐỔI mỗi rebuild — mở qua folder, đừng bookmark id;
    journal drive_trash)."""
    path, cfg = _read_config_record(getattr(a, "config", None))
    if not cfg:
        print("[tl] Không thấy config; chạy `tl init-config --from-public` hoặc truyền --config.", file=sys.stderr)
        return 2
    rows = _profile_index_rows(cfg)
    if not getattr(a, "apply", False):
        out = {"ok": True, "mode": "DRY", "config": path, "count": len(rows), "rows": rows,
               "note": "`--rebuild --apply` để ghi Van_ban_thuong/_PROFILES_INDEX (Sheet) trên Drive (cần webapp LIVE)."}
        print(json.dumps(out, ensure_ascii=False, indent=2) if getattr(a, "json", False) else _profile_index_csv(rows))
        return 0
    if not getattr(a, "rebuild", False):
        print("[tl] profile-index --apply cần --rebuild (xác nhận: tạo Sheet mới + trash bản cũ).", file=sys.stderr)
        return 2
    try:
        load_creds(getattr(a, "config", None), DEFAULT_PROFILE)
    except SystemExit as e:
        print(f"[tl] profile-index --apply cần webapp LIVE (Cowork): {e}", file=sys.stderr)
        return 2
    g = _gas()
    boot = g.get("bootstrap")
    vbt_id = boot.get("vanBanThuongId") if isinstance(boot, dict) else None
    if not vbt_id:
        print(json.dumps({"ok": False, "error": "NO_VAN_BAN_THUONG_ID", "bootstrap": boot}, ensure_ascii=False),
              file=sys.stderr)
        return 2
    olds = []
    try:    # tên folder cho cột folder_name (best-effort) + tìm bản index cũ để dọn SAU khi tạo bản mới
        top_items = _gas_get_retry(g, "list", folderId=vbt_id).get("items") or []
        fmap = {str(x.get("id")): str(x.get("name")) for x in top_items if str(x.get("type")) == "folder"}
        rows = _profile_index_rows(cfg, folder_names=fmap)
        olds = _index_old_candidates(top_items)
    except Exception:
        pass
    csv_text = _profile_index_csv(rows)
    rid = _apply_journal_start("profile-index", {"rows": len(rows), "old": len(olds)})
    up = g.post("upload", b64=_b64_text(csv_text), name=f"{_PROFILES_INDEX_NAME}.csv", mime="text/csv",
                folderId=vbt_id, convert="false", register="false", share="false", force="true")
    csv_id = up.get("fileId") or up.get("id")
    if not csv_id:
        print(json.dumps({"ok": False, "step": "upload_csv", "detail": up}, ensure_ascii=False, indent=2),
              file=sys.stderr)
        return 2
    cv = g.get("copy_convert", fileId=csv_id, name=_PROFILES_INDEX_NAME, folderId=vbt_id, toType="sheets",
               register="false", share="false")
    sheet_id = cv.get("fileId") or cv.get("id")
    if not sheet_id:
        print(json.dumps({"ok": False, "step": "convert_sheet", "csvFileId": csv_id, "detail": cv},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    cleanup = []
    for old in olds + [{"id": csv_id, "name": f"{_PROFILES_INDEX_NAME}.csv"}]:
        oid = str(old.get("id") or "")
        if not oid or oid == sheet_id:
            continue
        _journal_append(rid, {"t": "intent", "op": "drive_trash", "key": oid, "set": {"restore": "action restore"}})
        try:
            tr = g.get("trash", fileId=oid, confirm="yes")
        except Exception as e:  # noqa: BLE001
            tr = {"ok": False, "error": str(e)}
        _journal_append(rid, {"t": "commit", "op": "drive_trash", "key": oid, "ok": bool(tr.get("ok"))})
        cleanup.append({"fileId": oid, "name": old.get("name"), "result": tr})
    out = {"ok": True, "sheetId": sheet_id, "vanBanThuongId": vbt_id, "rows": len(rows),
           "replaced_old": cleanup, "journal": rid,
           "note": "Sổ cái = BẢN CHIẾU từ config (nguồn sự thật duy nhất). Mỗi rebuild tạo Sheet MỚI (id đổi), "
                   "bản cũ + CSV trung gian vào Trash (phục hồi được)."}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0


def cmd_profile_create(a) -> int:
    """Dựng profile văn bản thường: folder riêng + _meta + registry Sheet + manifest JSON + config own-scope."""
    try:
        import gen_instructions  # type: ignore
    except Exception as e:
        print(f"[tl] Không import được gen_instructions.py: {e}", file=sys.stderr)
        return 2
    name = (a.name or "").strip()
    folder_name = (getattr(a, "folder_name", None) or name).strip()
    nb = (a.notebook or "").strip()
    if not name or not nb:
        print("[tl] profile-create cần --name và --notebook", file=sys.stderr)
        return 2
    root_id = meta_id = registry_id = manifest_id = None
    actions = []
    if getattr(a, "apply", False):
        # tạo folder dưới Van_ban_thuong qua webapp NỀN (VBQPPL token); KHÔNG forward profile registry.
        load_creds(getattr(a, "config", None), DEFAULT_PROFILE)
        gas = _gas()
        boot = gas.get("bootstrap")
        vbt_id = boot.get("vanBanThuongId") if isinstance(boot, dict) else None
        if not vbt_id:
            print(f"[tl] profile-create: không lấy được vanBanThuongId từ bootstrap: {boot}", file=sys.stderr)
            return 2
        r = gas.get("resolvefolder", name=folder_name, parentId=vbt_id, create="true")
        root_id = r.get("folderId") if isinstance(r, dict) else None
        if not root_id:
            print(f"[tl] profile-create: tạo/tìm folder thất bại: {r}", file=sys.stderr)
            return 2
        actions.append(f"folder Van_ban_thuong/{folder_name} → rootFolderId={root_id}")
        mr = gas.get("resolvefolder", name="_meta", parentId=root_id, create="true")
        meta_id = mr.get("folderId") if isinstance(mr, dict) else None
        if not meta_id:
            print(f"[tl] profile-create: tạo/tìm _meta thất bại: {mr}", file=sys.stderr)
            return 2
        actions.append(f"folder Van_ban_thuong/{folder_name}/_meta → metaFolderId={meta_id}")
        reg = _create_profile_registry_sheet(gas, meta_id, name)
        if not reg.get("ok"):
            print(json.dumps({"ok": False, "step": "create_registry_sheet", **reg}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        registry_id = reg.get("registryDocId")
        actions.append(f"registry Sheet riêng → registryDocId={registry_id} ({len(REGISTRY_SCHEMA_COLS)} cột)")
        man = _create_profile_manifest_json(gas, meta_id, name, root_id, nb)
        if not man.get("ok"):
            print(json.dumps({"ok": False, "step": "create_manifest_json", **man}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        manifest_id = man.get("manifestId")
        actions.append(f"manifest JSON riêng → manifestId={manifest_id}")
        try:
            mex = gas.get("manifest_export", registryDocId=registry_id, manifestId=manifest_id)
            if mex.get("ok"):
                actions.append("manifest_export bootstrap OK (empty registry)")
        except Exception as e:  # noqa: BLE001
            actions.append(f"⚠ manifest_export bootstrap bỏ qua: {e}")
        # GHI BỀN config.profiles.<name> ngay sau khi hạ tầng đã verify là Sheet thật.
        _cfgp = _persist_profile_config(getattr(a, "config", None), name,
                                        {"rootFolderId": root_id, "metaFolderId": meta_id, "notebookId": nb,
                                         "registryDocId": registry_id, "manifestId": manifest_id,
                                         "manifestScope": "own", "categories": "own"})
        if _cfgp:
            actions.append(f"config.profiles.{name} ĐÃ GHI vào {_cfgp} (own root+_meta+Sheet registry+manifest)")
        else:
            actions.append("⚠ KHÔNG ghi được config (thiếu file) — ghi TAY config_profiles_patch bên dưới rồi mới dùng --profile.")
    text = gen_instructions.generate(getattr(a, "target", "project") or "project", VERSION,
                                     name, nb, folder_name, root_id)
    profile_patch = {name: {
        "rootFolderId": root_id or "<TẠO: chạy lại với --apply>",
        "metaFolderId": meta_id or "<TẠO: _meta>",
        "notebookId": nb,
        "registryDocId": registry_id or "<TẠO: Google Sheet tra_luat_registry.<profile>>",
        "manifestId": manifest_id or "<TẠO: JSON tra_luat_manifest.<profile>.json>",
        "manifestScope": "own",
        "categories": "own",
    }}
    out = {
        "ok": True, "profile": name, "folder_name": folder_name, "notebookId": nb,
        "rootFolderId": root_id, "applied": bool(getattr(a, "apply", False)),
        "metaFolderId": meta_id, "registryDocId": registry_id, "manifestId": manifest_id,
        "config_profiles_patch": {"profiles": profile_patch},
        "next_steps": [
            ("A1: config.profiles." + name + " ĐÃ ghi tự động khi --apply (own root+_meta+registry Sheet+manifest)."
             if root_id else "Ghi config_profiles_patch vào profiles của tra_luat_config.json (giữ vbqppl nền)."),
            f"A2: dùng `tl --profile {name} profile-ingest <file>` để nạp flat vào root profile; không recat vào 45 chủ đề VBQPPL.",
            f'Đặt defaultProfile="{name}" cho Project này (hoặc luôn chạy --profile {name}).',
            f"Kiểm `tl --profile {name} profile-info` thấy registryDocId là Google Sheet và categories='own'.",
        ],
        "actions": actions, "instruction": text,
    }
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        if not getattr(a, "apply", False):
            print(f"[DRY] profile-create '{name}': chạy --apply để tạo folder Van_ban_thuong/{folder_name}.")
        for ac in actions:
            print("  - " + ac)
        print("\n# config profiles patch (ghi vào tra_luat_config.json):")
        print(json.dumps({"profiles": profile_patch}, ensure_ascii=False, indent=2))
        print("\n# next steps:")
        for s in out["next_steps"]:
            print("  - " + s)
        print("\n# Instruction (Claude Project):\n" + text)
    return 0

# ── I11 (v1.34.18): leftover-sweep từ tl.py (affinity-tốt-nhất) ──


def _strip_shared_fixes(findings: list[dict], profiles: dict) -> list[dict]:
    """Review v1.30.0 (PURE, CONFIRMED): finding có fix-move nhưng fileId DÙNG CHUNG ≥2 profile → BỎ fix, nâng
    thành SHARED_ASSET_MULTI_PROFILE critical (move theo profile này = phá layout profile kia — tách asset trước)."""
    out = []
    for f in findings or []:
        if f.get("fix"):
            owners = _profile_asset_owners(profiles, f.get("fileId") or "")
            if len(owners) > 1:
                f = {k: v for k, v in f.items() if k != "fix"}
                f["check"] = "SHARED_ASSET_MULTI_PROFILE"
                f["severity"] = "critical"
                f["owners"] = owners
                f["note"] = (f"asset dùng chung {len(owners)} profile ({', '.join(owners)}) — KHÔNG auto-move "
                             "(phá layout profile kia); tách registry/manifest riêng trước (doctrine own-assets).")
        out.append(f)
    return out

def _discover_scan_vbthuong(g, vbt_id: str, folder_cap: int = 60) -> dict:
    """B: quét Van_ban_thuong 2 cấp read-only qua GAS `list` — con trực tiếp + trong `_meta` của từng thư mục con
    (registry/manifest kiểu mới nằm trong _meta, kiểu cũ nằm thẳng trong folder). Cap thư mục quét, LOUD khi cắt."""
    top = _gas_get_retry(g, "list", folderId=vbt_id)
    items = top.get("items") or []
    root_files = [x for x in items if str(x.get("type")) != "folder"]
    subfolders = [x for x in items if str(x.get("type")) == "folder"]
    out_folders = []
    for fo in subfolders[:folder_cap]:
        try:
            sitems = _gas_get_retry(g, "list", folderId=fo.get("id")).get("items") or []
        except Exception:
            sitems = []
        meta = next((x for x in sitems if str(x.get("type")) == "folder" and str(x.get("name")) == "_meta"), None)
        if meta:
            try:
                sitems = sitems + (_gas_get_retry(g, "list", folderId=meta.get("id")).get("items") or [])
            except Exception:
                pass
        out_folders.append({"id": fo.get("id"), "name": fo.get("name"), "items": sitems,
                            "meta_folder_id": (meta or {}).get("id")})
    return {"ok": True, "vbt_id": vbt_id, "folders": out_folders, "root_files": root_files,
            "capped": len(subfolders) > folder_cap, "folder_total": len(subfolders)}

def _adopt_pick_assets(items: list[dict], reg_override: str = "", man_override: str = "") -> dict:
    """C (PURE, test offline): chọn registry Sheet + manifest JSON từ items (con folder + _meta). Override thắng.
    Nhiều ứng viên không override → AMBIGUOUS (bắt người chọn — KHÔNG đoán); tên-registry-nhưng-không-Sheet → chặn."""
    regs, mans, reg_nonsheet = [], [], []
    for it in items or []:
        k = _discover_item_kind(it)
        if k == "registry":
            regs.append(it)
        elif k == "manifest":
            mans.append(it)
        elif k == "registry_nonsheet":
            reg_nonsheet.append(it)
    out = {"registry_candidates": [{"id": x.get("id"), "name": x.get("name")} for x in regs],
           "manifest_candidates": [{"id": x.get("id"), "name": x.get("name")} for x in mans],
           "registry_nonsheet": [{"id": x.get("id"), "name": x.get("name")} for x in reg_nonsheet],
           "registry": None, "manifest": None, "errors": []}
    if reg_override:
        out["registry"] = {"id": reg_override, "name": "(override --registry)"}
    elif len(regs) == 1:
        out["registry"] = {"id": regs[0].get("id"), "name": regs[0].get("name")}
    elif len(regs) > 1:
        out["errors"].append("REGISTRY_AMBIGUOUS: nhiều registry Sheet trong thư mục — truyền --registry <id>.")
    elif reg_nonsheet:
        out["errors"].append("REGISTRY_NOT_SHEET: thấy file tên registry nhưng KHÔNG phải Google Sheet "
                             "(Doc/legacy?) — bài học CLOBBER: Doc-as-Sheet đọc RỖNG. Truyền --registry <Sheet thật>.")
    else:
        out["errors"].append("REGISTRY_NOT_FOUND: không thấy tra_luat_registry*/Registry_* (Sheet) trong thư mục/_meta — "
                             "truyền --registry <id> (vd asset lạc gốc từ --discover) hoặc dựng mới bằng profile-create.")
    if man_override:
        out["manifest"] = {"id": man_override, "name": "(override --manifest)"}
    elif len(mans) == 1:
        out["manifest"] = {"id": mans[0].get("id"), "name": mans[0].get("name")}
    elif len(mans) > 1:
        std = [m for m in mans if str(m.get("name") or "").lower().startswith("tra_luat_manifest")]
        if len(std) == 1:
            out["manifest"] = {"id": std[0].get("id"), "name": std[0].get("name")}
        else:
            out["errors"].append("MANIFEST_AMBIGUOUS: nhiều *manifest*.json — truyền --manifest <id>.")
    else:
        out["errors"].append("MANIFEST_NOT_FOUND: không thấy *manifest*.json — truyền --manifest <id>, "
                             "hoặc --bootstrap-manifest để sinh mới từ registry sẵn có.")
    return out

def _index_old_candidates(items: list[dict]) -> list[dict]:
    """Review v1.30.0 (PURE, CONFIRMED): bản index CŨ cần dọn = TÊN CHÍNH XÁC `_PROFILES_INDEX` (Sheet) /
    `_PROFILES_INDEX.csv` — KHÔNG startswith (file người dùng đặt `_PROFILES_INDEX_backup…` từng có nguy cơ trash nhầm)."""
    keep = {_PROFILES_INDEX_NAME, f"{_PROFILES_INDEX_NAME}.csv"}
    return [x for x in (items or []) if str(x.get("name") or "") in keep]
