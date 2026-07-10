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
    out["config_report"] = _config_candidates_report(getattr(a, "config", None))   # P1: of-record + duplicate
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
    _ccr = _config_candidates_report(getattr(a, "config", None))   # P1: config-of-record + cảnh báo duplicate
    out = {"ok": bool(cfg), "config": path, "defaultProfile": cfg.get("defaultProfile") or DEFAULT_PROFILE,
           "activeProfile": active, "profiles": rows, "config_report": _ccr}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        if not cfg:
            print("[tl] Không thấy config; chạy `tl init-config --from-public` hoặc truyền --config.", file=sys.stderr)
            return 2
        print(f"== profiles · config={path} · default={out['defaultProfile']} · active={active} ==")
        if _ccr.get("warning"):
            print(f" ⚠ {_ccr['warning']}", file=sys.stderr)
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
    # P2 (v1.34.24): sau khi đổi default, in luôn Instruction Block (doctrine PHIÊN) — offline từ config;
    # bản đầy-metadata (marker): `tl profile-load <p>`.
    if out.get("ok"):
        try:
            import gen_instructions  # type: ignore
            out["instruction"] = gen_instructions.generate_profile_load_block(
                _profile_block_meta(name, profs.get(name) or {}), "session", VERSION)
            out["instruction_note"] = ("Block trên sinh OFFLINE từ config — metadata mô tả đầy đủ (marker): "
                                       f"`tl profile-load {name}`.")
        except Exception:  # noqa: BLE001
            pass
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
        mark = {"configured": "✅", "adoptable": "🟢", "broken_marker": "🔴", "unregistered_profile": "🟠",
                "empty_folder": "⚪", "plain_folder": "·"}.get(r["status"], "?")
        print(f" {mark} {str(r['folder_name'])[:44]:44s} {r['status']:22s} items={r['n_items']}"
              + (f" profile={r['profile']}" if r.get("profile") else "")
              + (f" marker={r['marker_status']}" if r.get("marker_status") else ""))
        if r.get("suggest"):
            print(f"      $ {r['suggest']}")
    for m in rep["misplaced_root_assets"]:
        print(f" 🔴 LẠC GỐC: {m['name']} ({m['kind']}) id={m['id']}\n      {m['note']}")
    for c in rep["orphaned"]:
        print(f" ⚠ ORPHANED: {c['profile']} root={c['rootFolderId']} — {c['note']}")
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
    # P1 (v1.34.22, ADR-0003): adopt --apply GHI LUÔN MARKER (mutation phải ghi 2 nơi marker+config);
    # thiếu _meta → tạo. Marker fail KHÔNG rollback config — doctor/backfill vá sau (finding MARKER_MISSING).
    _meta_id = str((meta or {}).get("id") or "")
    if not _meta_id:
        try:
            _mr2 = g.get("resolvefolder", name="_meta", parentId=folder, create="true")
        except Exception as e:  # noqa: BLE001
            _mr2 = {"ok": False, "error": str(e)}
        _meta_id = str((_mr2 or {}).get("folderId") or "")
        if _meta_id:
            prof_block["metaFolderId"] = _meta_id
            _persist_profile_config(getattr(a, "config", None), name, {"metaFolderId": _meta_id})
    _marker_result = None
    if _meta_id:
        _old_mk = _marker_read(g, folder, meta_id=_meta_id)
        _marker_result = _marker_write(g, _meta_id,
                                       _marker_body(name, {**prof_block, "metaFolderId": _meta_id},
                                                    existing=_old_mk.get("marker")),
                                       old_id=_old_mk.get("fileId") or "",
                                       run_id=_apply_journal_start("profile-adopt-marker", {"profile": name}))
    out = {**plan, "ok": bool(cfgp), "registry_verify": ver, "config_written": cfgp,
           "marker": _marker_result,
           "next_steps": [f"tl --profile {name} profile-info  (kiểm registry Sheet + categories='own')",
                          f"tl --profile {name} boot --refresh",
                          "tl profile-index --rebuild --apply  (cập nhật sổ cái _PROFILES_INDEX)"]}
    if _marker_result and not _marker_result.get("verified"):
        out.setdefault("warnings", []).append("MARKER_WRITE_UNVERIFIED: marker chưa ghi được — chạy "
                                              "`tl profile-backfill-markers --apply` sau.")
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
        # P1 (v1.34.22, ADR-0003): kiểm MARKER — thiếu/hỏng/lệch-config đều là finding (drift 3 chiều
        # marker↔config; chiều index kiểm bằng profile-index DRY).
        _root = str(prof.get("rootFolderId") or "").strip()
        if _root:
            _mr = _marker_read(g, _root, meta_id=str(prof.get("metaFolderId") or "") or None)
            if _mr.get("error"):
                findings.append({"check": "MARKER_READ_FAILED", "severity": "warn", "profile": n,
                                 "note": str(_mr["error"])})
            elif not _mr.get("found"):
                findings.append({"check": "MARKER_MISSING", "severity": "warn", "profile": n,
                                 "note": "chưa có _meta/" + _PROFILE_MARKER_NAME +
                                         " — chạy `tl profile-backfill-markers --apply` (ADR-0003)."})
            else:
                _mok, _merrs = _marker_validate(_mr.get("marker") or {})
                if not _mok:
                    findings.append({"check": "MARKER_INVALID", "severity": "warn", "profile": n,
                                     "note": ";".join(_merrs) + " — tái tạo: profile-backfill-markers --force."})
                else:
                    _mdiffs = _marker_diff(_mr["marker"], prof)
                    if _mdiffs:
                        findings.append({"check": "MARKER_CONFIG_DRIFT", "severity": "warn", "profile": n,
                                         "fields": [d["field"] for d in _mdiffs],
                                         "note": "marker ≠ config — marker là nguồn sự thật: `tl profile-sync "
                                                 "--apply`; marker SAI → profile-backfill-markers --force."})
        # P4 (v1.34.26): --deep = chiều Drive↔NLM↔registry — đối chiếu nguồn LIVE trên notebook với row
        # registry (theo nlm_source_id): unregistered / nlm-only pending|blocked / sentinel sót.
        if getattr(a, "deep", False):
            _nb_deep = str(prof.get("notebookId") or "").strip()
            if not _nb_deep:
                findings.append({"check": "NLM_DEEP_NO_NOTEBOOK", "severity": "warn", "profile": n,
                                 "note": "profile thiếu notebookId — bỏ kiểm chiều NLM."})
            else:
                try:
                    _nc_deep = _imp("nlm_cli")
                    _sl_deep = _nc_deep.source_list(_nb_deep)
                except Exception as e:  # noqa: BLE001
                    _sl_deep = {"ok": False, "error": f"{type(e).__name__}: {e}"}
                if not _sl_deep.get("ok"):
                    findings.append({"check": "NLM_DEEP_UNAVAILABLE", "severity": "warn", "profile": n,
                                     "note": str(_sl_deep.get("error"))[:200]})
                else:
                    apply_profile_offline(getattr(a, "config", None), n)   # scope registry PROFILE cho reg_get
                    _pend = _blk = 0
                    for _s in (_sl_deep.get("sources") or []):
                        _sid = str(_s.get("id") or "")
                        if not _sid:
                            continue
                        try:
                            _rr = (_gas_get_retry(g, "reg_get", nlm_source_id=_sid, refresh="false")
                                   or {}).get("rows") or []
                        except Exception:  # noqa: BLE001
                            continue
                        _own_d = [r for r in _rr if str(r.get("drive_id") or "")
                                  and not str(r.get("drive_id")).startswith(_NLM_ONLY_SENTINEL_PREFIX)]
                        _sent_d = [r for r in _rr if str(r.get("drive_id") or "")
                                   .startswith(_NLM_ONLY_SENTINEL_PREFIX)]
                        if not _rr:
                            findings.append({"check": "NLM_SOURCE_UNREGISTERED", "severity": "warn",
                                             "profile": n, "source_id": _sid,
                                             "title": str(_s.get("title") or "")[:80],
                                             "note": "nguồn trên notebook KHÔNG có row registry — chạy lại "
                                                     "`tl profile-from-nlm` (idempotent) hoặc reg-upsert tay."})
                        elif _own_d and _sent_d:
                            findings.append({"check": "SENTINEL_STALE", "severity": "warn", "profile": n,
                                             "source_id": _sid,
                                             "note": "row own + sentinel nlm_only cùng tồn tại (đứt giữa "
                                                     "materialize) — `profile-materialize-sources --apply` tự dọn."})
                        elif _sent_d:
                            if "materialize=blocked" in str(_sent_d[0].get("note") or ""):
                                _blk += 1
                            else:
                                _pend += 1
                    if _pend:
                        findings.append({"check": "NLM_ONLY_PENDING", "severity": "info", "profile": n,
                                         "count": _pend,
                                         "note": f"{_pend} nguồn nlm-only chưa materialize → `tl profile-"
                                                 f"materialize-sources --profile-name {n} --apply` "
                                                 "(materialize_preferred)."})
                    if _blk:
                        findings.append({"check": "NLM_ONLY_BLOCKED", "severity": "warn", "profile": n,
                                         "count": _blk,
                                         "note": "nguồn không xuất được (URL/YouTube/rỗng) — Ở LẠI nlm-only "
                                                 "là HỢP LỆ (Q4); thử lại: --retry-blocked."})
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
        # P1 (v1.34.22, ADR-0003): create --apply GHI LUÔN MARKER vào _meta (nguồn sự thật tồn tại/định danh).
        _mkw = _marker_write(gas, meta_id,
                             _marker_body(name, {"rootFolderId": root_id, "metaFolderId": meta_id,
                                                 "notebookId": nb, "registryDocId": registry_id,
                                                 "manifestId": manifest_id, "manifestScope": "own",
                                                 "categories": "own"}),
                             run_id=_apply_journal_start("profile-create-marker", {"profile": name}))
        if _mkw.get("verified"):
            actions.append(f"marker _meta/{_PROFILE_MARKER_NAME} → {_mkw.get('fileId')} (readback OK)")
        else:
            actions.append("⚠ MARKER_WRITE_UNVERIFIED — chạy `tl profile-backfill-markers --apply` sau.")
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

# ── P1 (v1.34.22, ADR-0003): PROFILE MARKER — `_meta/tra_luat_profile.json` là nguồn sự thật về
#    TỒN TẠI + ĐỊNH DANH + metadata mô tả của profile; config = cache runtime; sync MỘT CHIỀU marker→config. ──
_PROFILE_MARKER_NAME = "tra_luat_profile.json"
_PROFILE_MARKER_SCHEMA = "tra_luat_profile.v1"
_MARKER_IDENTITY_KEYS = ("rootFolderId", "metaFolderId", "notebookId", "registryDocId",
                         "manifestId", "categories", "manifestScope")


def _marker_body(name: str, prof: dict, existing: dict | None = None, now: str | None = None) -> dict:
    """PURE (ADR-0003): dựng nội dung marker từ block config; GIỮ metadata MÔ TẢ của marker cũ
    (description/style/relations/source_policy/created_at — phần mô tả sống trên marker, config không có)."""
    prof = prof or {}
    ex = existing if isinstance(existing, dict) else {}
    ts = now or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    body = {"schema": _PROFILE_MARKER_SCHEMA, "profile": str(name or "")}
    for k in _MARKER_IDENTITY_KEYS:
        v = prof.get(k)
        body[k] = v if isinstance(v, dict) else str(v or "")
    body["description"] = str(ex.get("description") or "")
    body["style"] = str(ex.get("style") or "")
    rel = dict(ex.get("relations")) if isinstance(ex.get("relations"), dict) else {}
    rel.setdefault("base", DEFAULT_PROFILE)   # nền VBQPPL luôn bật (CONTEXT.md) — relations chỉ MÔ TẢ, không mở scope
    body["relations"] = rel
    body["source_policy"] = str(ex.get("source_policy") or "materialize_preferred")
    body["created_at"] = str(ex.get("created_at") or ts)
    body["updated_at"] = ts
    body["updated_by"] = f"tl v{VERSION}"
    return body


def _marker_validate(d) -> tuple:
    """PURE: marker hợp lệ = schema đúng + profile + rootFolderId khác rỗng. Trả (ok, errors[])."""
    if not isinstance(d, dict):
        return False, ["NOT_A_DICT"]
    errs = []
    if str(d.get("schema") or "") != _PROFILE_MARKER_SCHEMA:
        errs.append(f"SCHEMA_MISMATCH:{d.get('schema')}")
    if not str(d.get("profile") or "").strip():
        errs.append("PROFILE_EMPTY")
    if not str(d.get("rootFolderId") or "").strip():
        errs.append("ROOT_FOLDER_ID_EMPTY")
    return (not errs), errs


def _marker_diff(marker: dict, prof: dict) -> list:
    """PURE: lệch ĐỊNH DANH marker↔config (bỏ qua metadata mô tả). Chỉ so field marker CÓ giá trị —
    marker thiếu field không tính là lệch (config có thể giàu hơn khi marker đời cũ)."""
    def _c(x):
        return json.dumps(x, sort_keys=True, ensure_ascii=False) if isinstance(x, dict) else str(x or "")
    out = []
    for k in _MARKER_IDENTITY_KEYS:
        mv = (marker or {}).get(k)
        cv = (prof or {}).get(k)
        if _c(mv) and _c(mv) != _c(cv):
            out.append({"field": k, "marker": mv, "config": cv})
    return out


def _marker_find_in_items(items: list) -> dict | None:
    """PURE: tìm file marker trong danh sách items (con folder + con _meta đã gộp)."""
    for it in items or []:
        if str(it.get("type")) != "folder" and str(it.get("name")) == _PROFILE_MARKER_NAME:
            return it
    return None


def _marker_read(g, root_id: str, meta_id: str | None = None) -> dict:
    """Đọc marker của một folder profile: xác định _meta (theo meta_id hoặc list root tìm tên) → list _meta →
    download JSON. Trả {found, fileId, marker, meta_folder_id, error} — lỗi mạng/parse KHÔNG raise."""
    out = {"found": False, "fileId": "", "marker": None, "meta_folder_id": str(meta_id or ""), "error": None}
    try:
        mid = str(meta_id or "")
        if not mid:
            items = (_gas_get_retry(g, "list", folderId=str(root_id)) or {}).get("items") or []
            meta = next((x for x in items if str(x.get("type")) == "folder" and str(x.get("name")) == "_meta"), None)
            mid = str((meta or {}).get("id") or "")
            out["meta_folder_id"] = mid
        if not mid:
            return out
        mitems = (_gas_get_retry(g, "list", folderId=mid) or {}).get("items") or []
        it = _marker_find_in_items(mitems)
        if not it:
            return out
        out["fileId"] = str(it.get("id") or "")
        d = _gas_get_retry(g, "download", fileId=out["fileId"])
        out["marker"] = json.loads(base64.b64decode(d.get("b64") or "").decode("utf-8"))
        out["found"] = True
    except Exception as e:  # noqa: BLE001
        out["error"] = f"MARKER_READ_FAILED:{type(e).__name__}: {e}"
    return out


def _marker_write(g, meta_id: str, body: dict, old_id: str = "", run_id: str | None = None) -> dict:
    """Ghi marker (ADR-0003: CHỈ lệnh tl được ghi — journaled + readback): upload bản MỚI vào _meta →
    readback download so schema/profile/rootFolderId → trash bản cũ SAU khi bản mới verified (fail-safe
    tạo-trước-dọn-sau, khuôn profile-index). Trả {ok, verified, fileId, trashed_old, upload}."""
    key = str(body.get("profile") or "")
    if run_id:
        _journal_append(run_id, {"t": "intent", "op": "marker_write", "key": key,
                                 "set": {"metaFolderId": str(meta_id), "marker": body,
                                         "old_fileId": str(old_id or "")}})
    try:
        up = g.post("upload", b64=_b64_text(json.dumps(body, ensure_ascii=False, indent=2)),
                    name=_PROFILE_MARKER_NAME, mime="application/json", folderId=str(meta_id),
                    convert="false", register="false", share="false", force="true")
    except Exception as e:  # noqa: BLE001
        up = {"ok": False, "error": f"MARKER_UPLOAD_RAISED:{type(e).__name__}"}
    fid = str((up or {}).get("fileId") or (up or {}).get("id") or "")
    verified = False
    if fid:
        try:
            d = _gas_get_retry(g, "download", fileId=fid)
            rb = json.loads(base64.b64decode(d.get("b64") or "").decode("utf-8"))
            verified = all(str(rb.get(k) or "") == str(body.get(k) or "")
                           for k in ("schema", "profile", "rootFolderId"))
        except Exception:  # noqa: BLE001
            verified = False
    trashed = []
    if verified and old_id and str(old_id) != fid:
        try:
            tr = g.get("trash", fileId=str(old_id), confirm="yes")
            trashed.append({"fileId": str(old_id), "ok": bool(tr.get("ok"))})
        except Exception as e:  # noqa: BLE001
            trashed.append({"fileId": str(old_id), "ok": False, "error": str(e)})
    if run_id:
        _journal_append(run_id, {"t": "commit", "op": "marker_write", "key": key, "ok": verified,
                                 "verify": {"fileId": fid, "trashed_old": trashed,
                                            "error": (up or {}).get("error")}})
    return {"ok": bool((up or {}).get("ok")) and bool(fid), "verified": verified, "fileId": fid,
            "trashed_old": trashed, "upload": up}


def _config_candidates_report(config_path: str | None = None) -> dict:
    """Observability P1: config-of-record (file THẬT được đọc) + mọi ứng viên đang tồn tại trên đĩa.
    Cảnh báo DUPLICATE khi có file khác of-record — sửa file không-được-đọc là 'sửa mà không ăn' im lặng."""
    cands = _config_candidates(config_path)
    on_disk = [p for p in cands if Path(p).exists()]
    used = ""
    for p in cands:
        if Path(p).exists() and _read_json_file(p):
            used = p
            break
    out = {"config_of_record": used, "candidates_on_disk": on_disk}
    others = [p for p in on_disk if p != used]
    if used and others:
        out["warning"] = (f"DUPLICATE_CONFIG_CANDIDATES: {len(others)} file config khác tồn tại nhưng KHÔNG được đọc "
                          f"(of-record = {used}) — sửa các file này sẽ không có tác dụng: {others}")
    return out


def _profile_sync_rows(folders: list, profiles: dict, vbt_id: str = "") -> list:
    """PURE (ADR-0003): từ scan Van_ban_thuong (folders kèm marker) + config.profiles → dòng trạng thái
    sync MỘT CHIỀU marker→config: in_sync / drift{diffs} / new_from_marker{block} / marker_missing /
    broken_marker / refused_base (marker tự nhận vbqppl) / root_conflict / orphaned (config có, scan không thấy).
    v1.34.23 (live-smoke bắt): profile có root == chính vbt_id (vbthuong) KHÔNG bị báo orphaned oan."""
    profiles = profiles or {}
    by_root = {str((p or {}).get("rootFolderId") or "").strip(): n
               for n, p in profiles.items() if str((p or {}).get("rootFolderId") or "").strip()}
    rows, seen = [], set()
    for f in folders or []:
        fid = str(f.get("id") or "")
        marker = f.get("marker") if isinstance(f.get("marker"), dict) else None
        merr = f.get("marker_error")
        if not marker and not merr:
            n = by_root.get(fid)
            if n and n != DEFAULT_PROFILE:
                rows.append({"profile": n, "folder_id": fid, "status": "marker_missing",
                             "suggest": "tl profile-backfill-markers --apply"})
                seen.add(n)
            continue
        if merr:
            rows.append({"profile": by_root.get(fid) or "", "folder_id": fid,
                         "status": "broken_marker", "error": str(merr)})
            continue
        ok, errs = _marker_validate(marker)
        name = str(marker.get("profile") or "").strip()
        if not ok:
            rows.append({"profile": name, "folder_id": fid, "status": "broken_marker", "error": ";".join(errs)})
            continue
        if name == DEFAULT_PROFILE:
            rows.append({"profile": name, "folder_id": fid, "status": "refused_base",
                         "note": "vbqppl là profile nền (webapp/token of-record) — marker này bị BỎ QUA."})
            continue
        seen.add(name)
        block = {k: marker.get(k) for k in _MARKER_IDENTITY_KEYS
                 if (marker.get(k) if isinstance(marker.get(k), dict) else str(marker.get(k) or ""))}
        prof = profiles.get(name)
        if not isinstance(prof, dict):
            rows.append({"profile": name, "folder_id": fid, "status": "new_from_marker", "block": block})
            continue
        croot = str(prof.get("rootFolderId") or "").strip()
        mroot = str(marker.get("rootFolderId") or "").strip()
        if croot and mroot and croot != mroot:
            rows.append({"profile": name, "folder_id": fid, "status": "root_conflict",
                         "config_root": croot, "marker_root": mroot,
                         "note": "tên profile trùng nhưng root KHÁC — KHÔNG tự ghi (đổi tên marker qua "
                                 "mutation hoặc profile-rename config trước)."})
            continue
        diffs = _marker_diff(marker, prof)
        rows.append({"profile": name, "folder_id": fid,
                     "status": "drift" if diffs else "in_sync", "diffs": diffs, "block": block})
    folder_ids = {str(f.get("id") or "") for f in folders or []}
    for n in sorted(profiles):
        if n == DEFAULT_PROFILE or n in seen:
            continue
        rid = str((profiles.get(n) or {}).get("rootFolderId") or "").strip()
        if rid and rid != str(vbt_id or "") and rid not in folder_ids:
            rows.append({"profile": n, "folder_id": rid, "status": "orphaned",
                         "note": "config có profile nhưng scan Van_ban_thuong không thấy folder (root ngoài VBT/"
                                 "trash/cap?) — kiểm bằng profile-list --discover --folder-cap lớn hơn."})
    return rows


def _profile_block_meta(name: str, prof: dict, marker: dict | None = None) -> dict:
    """PURE (P2): hợp nhất định danh config + metadata MÔ TẢ từ marker (marker thắng phần mô tả —
    description/style/relations/source_policy sống trên marker, ADR-0003)."""
    prof = prof or {}
    mm = marker if isinstance(marker, dict) else {}
    return {"profile": name,
            "notebookId": str(mm.get("notebookId") or prof.get("notebookId") or ""),
            "rootFolderId": str(mm.get("rootFolderId") or prof.get("rootFolderId") or ""),
            "folder_name": name,
            "registryDocId": str(mm.get("registryDocId") or prof.get("registryDocId") or ""),
            "manifestId": str(mm.get("manifestId") or prof.get("manifestId") or ""),
            "description": str(mm.get("description") or ""),
            "style": str(mm.get("style") or ""),
            "relations": (mm.get("relations") if isinstance(mm.get("relations"), dict)
                          else {"base": DEFAULT_PROFILE}),
            "source_policy": str(mm.get("source_policy") or "materialize_preferred")}


def cmd_profile_load(a) -> int:
    with _ProfileEnvGuard():
        return _cmd_profile_load_impl(a)


def _cmd_profile_load_impl(a) -> int:
    """P2 (v1.34.24, Q7 + ADR-0003): 'dùng profile X trong PHIÊN' — xuất Instruction Block THỐNG NHẤT
    mọi môi trường (chỉ rẽ --target session|project), KHÔNG ghi config/marker (read-only; đổi mặc định
    máy = profile-use --apply). Metadata mô tả đọc từ MARKER best-effort LIVE; offline → config + note.
    Marker↔config lệch → cảnh báo gợi ý profile-sync. rc: 0 / 2 PROFILE_NOT_FOUND."""
    try:
        import gen_instructions  # type: ignore
    except Exception as e:  # noqa: BLE001
        print(f"[tl] Không import được gen_instructions.py: {e}", file=sys.stderr)
        return 2
    name0 = (getattr(a, "name", None) or "").strip()
    path, cfg = _read_config_record(getattr(a, "config", None))
    profs = _profiles_from_config(cfg) if cfg else {}
    name, prof = _profile_lookup(profs, name0) if name0 else (DEFAULT_PROFILE, profs.get(DEFAULT_PROFILE))
    if name != DEFAULT_PROFILE and not isinstance(prof, dict):
        print(json.dumps({"ok": False, "error": "PROFILE_NOT_FOUND", "profile": name0,
                          "known": sorted(profs),
                          "note": "profile có marker trên Drive nhưng chưa vào config? → "
                                  "`tl profile-sync --apply` rồi load lại."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    prof = prof if isinstance(prof, dict) else {}
    marker, source, drift, m_note = None, "config_offline", [], None
    if name != DEFAULT_PROFILE and not getattr(a, "offline", False):
        try:
            load_creds(getattr(a, "config", None), DEFAULT_PROFILE)
            g = _gas()
            mr = _marker_read(g, str(prof.get("rootFolderId") or ""),
                              meta_id=str(prof.get("metaFolderId") or "") or None)
            if mr.get("found"):
                mok, merrs = _marker_validate(mr.get("marker") or {})
                if mok:
                    marker = mr["marker"]
                    source = "marker"
                    drift = _marker_diff(marker, prof)
                else:
                    m_note = "MARKER_INVALID:" + ";".join(merrs)
            elif mr.get("error"):
                m_note = str(mr["error"])
            else:
                m_note = "MARKER_MISSING — `tl profile-backfill-markers --apply` để có metadata mô tả."
        except SystemExit as e:
            m_note = f"OFFLINE ({e})"
        except Exception as e:  # noqa: BLE001
            m_note = f"MARKER_READ_FAILED:{type(e).__name__}"
    meta = _profile_block_meta(name, prof, marker)
    target = (getattr(a, "target", None) or "session").strip() or "session"
    text = gen_instructions.generate_profile_load_block(meta, target, VERSION)
    out = {"ok": True, "profile": name, "target": target, "source": source, "config": path,
           "config_report": _config_candidates_report(getattr(a, "config", None))}
    if drift:
        out["drift"] = drift
        out["warning"] = ("MARKER_CONFIG_DRIFT (" + ",".join(d["field"] for d in drift) +
                          ") — chạy `tl profile-sync --apply` trước khi tin định danh; block dùng ĐỊNH DANH marker.")
    if m_note:
        out["marker_note"] = m_note + " — block sinh từ config (metadata mô tả có thể thiếu)."
    if getattr(a, "json", False):
        out["instruction"] = text
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        if out.get("warning"):
            print(f"[tl] ⚠ {out['warning']}", file=sys.stderr)
        if m_note:
            print(f"[tl] {out['marker_note']}", file=sys.stderr)
        print(text)
    return 0


def cmd_profile_sync(a) -> int:
    with _ProfileEnvGuard():            # không nhiễm env profile của caller cùng-process (khuôn v1.30.0)
        return _cmd_profile_sync_impl(a)


def _cmd_profile_sync_impl(a) -> int:
    """P1 (v1.34.22, ADR-0003): đồng bộ MỘT CHIỀU marker Drive → config. DRY mặc định (báo cáo drift/new/
    missing); --apply ghi config theo marker (journaled qua _persist_profile_config + READBACK từng field).
    KHÔNG BAO GIỜ ghi marker (ghi marker = việc của lệnh mutation/backfill). rc: 0 sạch hoặc apply verified
    hết / 1 có việc (DRY) hoặc ghi lỗi / 2 lỗi chạy."""
    path, cfg = _read_config_record(getattr(a, "config", None))
    if not cfg:
        print("[tl] Không thấy config; chạy `tl init-config --from-public` hoặc truyền --config.", file=sys.stderr)
        return 2
    profs = _profiles_from_config(cfg)
    target = (getattr(a, "target_profile", None) or "").strip()
    try:
        load_creds(getattr(a, "config", None), DEFAULT_PROFILE)   # webapp NỀN — không forward scope profile
        g = _gas()
        boot = g.get("bootstrap")
        vbt_id = boot.get("vanBanThuongId") if isinstance(boot, dict) else None
        if not vbt_id:
            print(json.dumps({"ok": False, "error": "NO_VAN_BAN_THUONG_ID", "bootstrap": boot},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        scan = _discover_scan_vbthuong(g, vbt_id, folder_cap=int(getattr(a, "folder_cap", None) or 60))
    except SystemExit as e:
        print(f"[tl] profile-sync cần webapp LIVE: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": f"SYNC_SCAN_FAILED: {e}"}, ensure_ascii=False), file=sys.stderr)
        return 2
    rows = _profile_sync_rows(scan.get("folders") or [], profs, vbt_id=str(vbt_id))
    if target:
        rows = [r for r in rows if str(r.get("profile") or "") == target]
    actionable = [r for r in rows if r.get("status") in ("new_from_marker", "drift")]
    findings = [r for r in rows if r.get("status") not in ("in_sync", "refused_base")]
    applied, all_ok = [], True
    if getattr(a, "apply", False):
        for r in actionable:
            name = str(r.get("profile"))
            block = (r.get("block") if r.get("status") == "new_from_marker"
                     else {d["field"]: d["marker"] for d in (r.get("diffs") or [])})
            cfgp = _persist_profile_config(getattr(a, "config", None), name, block)
            got = {}
            if cfgp:
                _, cfg2 = _read_config_record(getattr(a, "config", None))
                got = _profiles_from_config(cfg2).get(name) or {}
            def _c(x):
                return json.dumps(x, sort_keys=True, ensure_ascii=False) if isinstance(x, dict) else str(x or "")
            ver = bool(cfgp) and all(_c(got.get(k)) == _c(v) for k, v in (block or {}).items())
            applied.append({"profile": name, "status": r.get("status"), "config": cfgp,
                            "written": sorted(block or {}), "verified": ver})
            all_ok = all_ok and ver
            r["applied"] = ver
    out = {"ok": (all_ok if getattr(a, "apply", False) else not findings),
           "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
           "config": path, "vanBanThuongId": vbt_id, "scanned": len(scan.get("folders") or []),
           "capped": bool(scan.get("capped")), "rows": rows,
           "actionable": len(actionable), "applied": applied,
           "config_report": _config_candidates_report(getattr(a, "config", None)),
           "note": "MỘT CHIỀU marker→config (ADR-0003). Marker sai → sửa qua lệnh mutation hoặc "
                   "profile-backfill-markers --force; marker_missing → profile-backfill-markers --apply."}
    if scan.get("capped"):
        out["warning"] = (f"CHỈ quét {out['scanned']}/{scan.get('folder_total')} thư mục (cap) — "
                          f"chạy lại với --folder-cap {scan.get('folder_total')}.")
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)) if getattr(a, "json", False)
          else json.dumps(out, ensure_ascii=False, indent=2))
    if getattr(a, "apply", False):
        return 0 if all_ok else 1
    return 0 if not findings else 1


def cmd_profile_backfill_markers(a) -> int:
    with _ProfileEnvGuard():
        return _cmd_profile_backfill_markers_impl(a)


def _cmd_profile_backfill_markers_impl(a) -> int:
    """P1 (ADR-0003 quyết định 4): backfill MỘT LẦN config → marker cho profile hiện hữu CHƯA có marker.
    DRY mặc định; --force ghi đè marker lệch theo config (migration có chủ đích — bình thường marker là
    nguồn sự thật, dùng profile-sync). Ghi = upload bản mới + readback + trash bản cũ (journaled).
    KHÔNG đụng vbqppl. rc: 0 plan/ghi verified hết / 1 ghi lỗi / 2 lỗi chạy."""
    path, cfg = _read_config_record(getattr(a, "config", None))
    if not cfg:
        print("[tl] Không thấy config; chạy `tl init-config --from-public` hoặc truyền --config.", file=sys.stderr)
        return 2
    profs = _profiles_from_config(cfg)
    target = (getattr(a, "target_profile", None) or "").strip()
    if target and target not in profs:
        print(json.dumps({"ok": False, "error": "PROFILE_NOT_FOUND", "profile": target}, ensure_ascii=False),
              file=sys.stderr)
        return 2
    names = [target] if target else [n for n in sorted(profs) if n != DEFAULT_PROFILE]
    try:
        load_creds(getattr(a, "config", None), DEFAULT_PROFILE)
    except SystemExit as e:
        print(f"[tl] profile-backfill-markers cần webapp LIVE: {e}", file=sys.stderr)
        return 2
    g = _gas()
    try:    # v1.34.23 (live-smoke bắt): cần vbt_id để KHÔNG đặt marker vào _meta của chính Van_ban_thuong
        _vbt = str((g.get("bootstrap") or {}).get("vanBanThuongId") or "")
    except Exception:  # noqa: BLE001
        _vbt = ""
    rows, plans = [], []
    for n in names:
        if n == DEFAULT_PROFILE:
            continue
        prof = profs.get(n) if isinstance(profs.get(n), dict) else {}
        root = str(prof.get("rootFolderId") or "").strip()
        if not root:
            rows.append({"profile": n, "status": "no_root",
                         "note": "profile thiếu rootFolderId trong config — sửa config/adopt trước."})
            continue
        if _vbt and root == _vbt:
            rows.append({"profile": n, "status": "skipped_vbt_root",
                         "note": "root là CHÍNH Van_ban_thuong (vbthuong) — marker đặt ở _meta của VBT gốc "
                                 "sẽ nhiễu discover; profile đặc biệt này định danh qua config (xử lý ở P2)."})
            continue
        mr = _marker_read(g, root, meta_id=str(prof.get("metaFolderId") or "") or None)
        if mr.get("error"):
            rows.append({"profile": n, "status": "read_failed", "error": mr["error"]})
            continue
        if mr.get("found") and not getattr(a, "force", False):
            row = {"profile": n, "status": "has_marker", "fileId": mr["fileId"]}
            diffs = _marker_diff(mr.get("marker") or {}, prof)
            if diffs:
                row["diffs"] = diffs
                row["note"] = ("marker ≠ config — marker là NGUỒN SỰ THẬT: `tl profile-sync --apply`; "
                               "marker SAI thật sự → chạy lại với --force (ghi đè theo config).")
            rows.append(row)
            continue
        row = {"profile": n, "status": "planned", "meta_folder_id": mr.get("meta_folder_id") or "",
               "overwrite": bool(mr.get("found"))}
        rows.append(row)
        plans.append({"profile": n, "prof": prof, "root": root, "row": row,
                      "meta_id": mr.get("meta_folder_id") or "", "old_id": mr.get("fileId") or "",
                      "existing": mr.get("marker")})
    if not getattr(a, "apply", False):
        out = {"ok": True, "mode": "DRY", "config": path, "rows": rows,
               "note": "--apply để ghi marker (upload mới + readback + trash bản cũ, journaled — ADR-0003)."}
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)) if getattr(a, "json", False)
              else json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    rid = _apply_journal_start("profile-backfill-markers", {"profiles": len(plans)})
    all_ok = True
    for p in plans:
        meta_id = p["meta_id"]
        if not meta_id:
            try:
                mr2 = g.get("resolvefolder", name="_meta", parentId=p["root"], create="true")
            except Exception as e:  # noqa: BLE001
                mr2 = {"ok": False, "error": str(e)}
            meta_id = str((mr2 or {}).get("folderId") or "")
            if meta_id:
                _persist_profile_config(getattr(a, "config", None), p["profile"], {"metaFolderId": meta_id})
        if not meta_id:
            p["row"].update({"status": "failed", "error": "NO_META_FOLDER"})
            all_ok = False
            continue
        body = _marker_body(p["profile"], {**p["prof"], "metaFolderId": meta_id}, existing=p["existing"])
        w = _marker_write(g, meta_id, body, old_id=p["old_id"], run_id=rid)
        p["row"].update({"status": "written" if w["verified"] else "failed",
                         "verified": w["verified"], "fileId": w["fileId"],
                         "trashed_old": w["trashed_old"]})
        if not w["verified"]:
            p["row"]["error"] = str((w.get("upload") or {}).get("error") or "READBACK_MISMATCH")
        all_ok = all_ok and w["verified"]
    out = {"ok": all_ok, "mode": "APPLY", "config": path, "rows": rows, "journal": rid,
           "note": "marker đã ghi qua upload+readback+trash-bản-cũ; config.metaFolderId được điền khi phải tạo _meta."}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)) if getattr(a, "json", False)
          else json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if all_ok else 1


_PROFILE_SYSPROMPT_NAME = "nlm_system_prompt.md"


_SEED_RAW_EXT_RE = re.compile(r"\.(docx?|pdf|html?|txt|rtf|odt)$", re.IGNORECASE)


def _promote_seed_candidates(items: list) -> list:
    """PURE (P3, Q3): lọc file NGUỒN trong folder promote (items có thể ĐỆ QUY) để seed registry —
    bỏ folder, bỏ asset hạ tầng (registry/manifest/marker/sysprompt/CSV trung gian). Cặp sibling
    GDoc↔raw CÙNG TÊN (doctrine 'file gốc đặt cạnh GDoc') → chỉ seed GDoc; raw đơn lẻ giữ nguyên.
    Trả [{drive_id, name}] giữ thứ tự gốc."""
    prelim = []
    for it in items or []:
        if str(it.get("type")) == "folder":
            continue
        nm = str(it.get("name") or "")
        if nm in (_PROFILE_MARKER_NAME, _PROFILE_SYSPROMPT_NAME):
            continue
        if _discover_item_kind(it) in ("registry", "manifest", "registry_nonsheet"):
            continue
        if nm.lower().endswith(".csv") and "tra_luat_registry" in nm:
            continue
        did = str(it.get("id") or "")
        if did:
            prelim.append({"drive_id": did, "name": nm,
                           "mime": str(it.get("mime") or it.get("mimeType") or "")})

    def _basekey(nm: str) -> str:
        return re.sub(r"[\s_\-]+", " ",
                      _strip_accents(_SEED_RAW_EXT_RE.sub("", nm)).lower()).strip()

    def _is_gdoc(c: dict) -> bool:
        return "vnd.google-apps" in (c.get("mime") or "") or not _SEED_RAW_EXT_RE.search(c["name"])

    groups = {}
    for c in prelim:
        groups.setdefault(_basekey(c["name"]), []).append(c)
    keep = set()
    for grp in groups.values():
        if len(grp) == 1:
            keep.add(grp[0]["drive_id"])
            continue
        gd = [c for c in grp if _is_gdoc(c)]
        for c in (gd or grp[:1]):        # có GDoc → chỉ GDoc; toàn raw trùng tên → giữ 1 (chống double-seed)
            keep.add(c["drive_id"])
    return [{"drive_id": c["drive_id"], "name": c["name"]} for c in prelim if c["drive_id"] in keep]


def _nlm_system_prompt_apply(g, meta_id: str, notebook_id: str, run_id: str | None = None) -> dict:
    """P3 (Q5): sinh NLM System Prompt từ generator (KHÔNG viết tự do) → LƯU `_meta/nlm_system_prompt.md`
    (bản-đã-áp/bản-cần-dán, readback artifact) → TỰ ÁP qua `nlm chat configure --goal custom`.
    CLI fail/quá 10000 chars → status=manual_required (kèm chỉ dẫn dán tay), KHÔNG chặn promote."""
    try:
        import gen_instructions  # type: ignore
        text = gen_instructions.generate("nlm", VERSION)
    except Exception as e:  # noqa: BLE001
        return {"status": "generator_failed", "error": str(e)}
    out = {"chars": len(text)}
    try:    # lưu Drive TRƯỚC (kể cả khi áp fail — bản cần-dán nằm cạnh profile)
        up = g.post("upload", b64=_b64_text(text), name=_PROFILE_SYSPROMPT_NAME,
                    mime="text/markdown", folderId=str(meta_id), convert="false",
                    register="false", share="false", force="true")
        out["file"] = str((up or {}).get("fileId") or (up or {}).get("id") or "")
    except Exception as e:  # noqa: BLE001
        out["file_error"] = str(e)
    if not notebook_id:
        out["status"] = "skipped_no_notebook"
        return out
    if len(text) > 10000:
        out["status"] = "manual_required"
        out["note"] = ("TOO_LONG: prompt vượt trần 10000 chars của `nlm chat configure` — rút gọn hoặc "
                       "dán tay phần lõi vào NotebookLM chat settings.")
        return out
    if run_id:
        _journal_append(run_id, {"t": "intent", "op": "nlm_chat_configure", "key": str(notebook_id),
                                 "set": {"goal": "custom", "chars": len(text)}})
    try:
        nc = _imp("nlm_cli")
        r = nc.chat_configure(str(notebook_id), text)
    except Exception as e:  # noqa: BLE001
        r = {"ok": False, "error": f"CHAT_CONFIGURE_RAISED:{type(e).__name__}"}
    ok = bool((r or {}).get("ok"))
    if run_id:
        _journal_append(run_id, {"t": "commit", "op": "nlm_chat_configure", "key": str(notebook_id),
                                 "ok": ok, "verify": {"error": (r or {}).get("error")}})
    out["status"] = "applied" if ok else "manual_required"
    if not ok:
        out["error"] = (r or {}).get("error")
        out["note"] = (f"Dán tay: `nlm chat configure {notebook_id} --goal custom --prompt <nội dung "
                       f"_meta/{_PROFILE_SYSPROMPT_NAME}>` (hoặc NotebookLM UI → chat settings).")
    return out


def cmd_profile_promote(a) -> int:
    with _ProfileEnvGuard():
        return _cmd_profile_promote_impl(a)


def _cmd_profile_promote_impl(a) -> int:
    """P3 (v1.34.25, Q2+Q3+Q5 grilling 2026-07-10): BIẾN FOLDER DRIVE THƯỜNG THÀNH PROFILE.
    Promote CHỈ dựng hạ tầng còn thiếu (_meta/registry/manifest/notebook/marker/config) + SEED registry
    từ nội dung folder; việc nạp NLM đi đường `ingest-missing --allow-no-sohieu` (idempotent/resume) —
    KHÔNG nạp trọn gói trong lệnh này. Idempotent: asset sẵn có được DÙNG LẠI (khuôn adopt).
    Notebook: --notebook <id> HOẶC --create-notebook (nới điều-kiện-kép CÓ KIỂM SOÁT: chỉ ngữ cảnh tạo
    profile, --apply --confirm yes, journaled + readback notebook_get). NLM System Prompt generator-sinh
    TỰ ÁP + lưu _meta (Q5, fallback manual_required). DRY mặc định. rc: 0 / 1 bước fail / 2 guard."""
    name = (getattr(a, "name", None) or "").strip()
    folder = (getattr(a, "folder", None) or "").strip()
    if not name or not folder:
        print("[tl] profile-promote cần --name và --folder", file=sys.stderr)
        return 2
    if name == DEFAULT_PROFILE:
        print("[tl] REFUSE_PROMOTE_DEFAULT_PROFILE: vbqppl là profile nền.", file=sys.stderr)
        return 2
    nb_flag = (getattr(a, "notebook", None) or "").strip()
    create_nb = bool(getattr(a, "create_notebook", False))
    if nb_flag and create_nb:
        print("[tl] --notebook và --create-notebook loại trừ nhau — chọn một.", file=sys.stderr)
        return 2
    if create_nb and getattr(a, "apply", False) and getattr(a, "confirm", None) != "yes":
        print(json.dumps({"ok": False, "error": "CONFIRM_YES_REQUIRED",
                          "note": "--create-notebook tạo notebook NLM MỚI (điều-kiện-kép nới có kiểm soát) "
                                  "→ --apply cần --confirm yes."}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    path, cfg = _read_config_record(getattr(a, "config", None))
    existing = _profiles_from_config(cfg).get(name) if cfg else None
    existing = existing if isinstance(existing, dict) else None
    if existing and str(existing.get("rootFolderId") or "").strip() not in ("", folder):
        print(json.dumps({"ok": False, "error": "PROFILE_EXISTS_DIFFERENT_FOLDER", "profile": name,
                          "config_rootFolderId": existing.get("rootFolderId"), "requested_folder": folder},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    try:
        load_creds(getattr(a, "config", None), DEFAULT_PROFILE)
    except SystemExit as e:
        print(f"[tl] profile-promote cần webapp LIVE: {e}", file=sys.stderr)
        return 2
    g = _gas()
    try:
        vbt_id = str((g.get("bootstrap") or {}).get("vanBanThuongId") or "")
    except Exception:  # noqa: BLE001
        vbt_id = ""
    if vbt_id and folder == vbt_id:
        print("[tl] REFUSE_PROMOTE_VBT_ROOT: không promote CHÍNH Van_ban_thuong.", file=sys.stderr)
        return 2
    finfo = _gas_get_retry(g, "info", fileId=folder)
    fmime = _mime_from_info(finfo) if isinstance(finfo, dict) else ""
    if not fmime.endswith("apps.folder"):
        print(json.dumps({"ok": False, "error": "FOLDER_ID_INVALID", "mime": fmime},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    try:
        items = _gas_get_retry(g, "list", folderId=folder).get("items") or []
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": f"FOLDER_LIST_FAILED: {e}"}, ensure_ascii=False), file=sys.stderr)
        return 2
    meta = next((x for x in items if str(x.get("type")) == "folder" and str(x.get("name")) == "_meta"), None)
    meta_items = []
    if meta:
        try:
            meta_items = _gas_get_retry(g, "list", folderId=meta.get("id")).get("items") or []
        except Exception:
            pass
    if _marker_find_in_items(meta_items):
        print(json.dumps({"ok": False, "error": "ALREADY_PROFILE", "folder": folder,
                          "note": "folder đã có marker tra_luat_profile.json — dùng `tl profile-sync --apply` "
                                  "(đưa vào config) hoặc profile-adopt, KHÔNG promote lại."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    picked = _adopt_pick_assets(items + meta_items)
    reuse_reg = str((picked.get("registry") or {}).get("id") or "")
    # Manifest chỉ DÙNG LẠI khi JSON tự nhận ĐÚNG profile này — file tên manifest nhưng của profile khác/
    # lạc (ca mj "cu") mà reuse là gán nhầm sổ cái (bài học manifest-lạ của adopt v1.30.0).
    reuse_man, man_warn = "", None
    _man_cand = str((picked.get("manifest") or {}).get("id") or "")
    if _man_cand:
        try:
            _dm = _gas_get_retry(g, "download", fileId=_man_cand)
            _mj = (json.loads(base64.b64decode(_dm.get("b64") or "").decode("utf-8"))
                   if _dm.get("b64") else {})
        except Exception:  # noqa: BLE001
            _mj = {}
        if str((_mj or {}).get("profile") or "") == name:
            reuse_man = _man_cand
        else:
            man_warn = (f"MANIFEST_FOREIGN_IGNORED: {_man_cand} (profile="
                        f"'{(_mj or {}).get('profile')}' ≠ '{name}') — tạo manifest mới riêng.")
    # Seed quét ĐỆ QUY (live-smoke 2026-07-10: folder thường hay lồng subfolder chủ đề) — capped thì LOUD.
    seed_capped = False
    try:
        _rl = _gas_get_retry(g, "list", folderId=folder, recursive="true")
        _ritems = _rl.get("items") or []
        seed_capped = bool(_rl.get("capped"))
    except Exception:  # noqa: BLE001
        _ritems = items
    seeds = _promote_seed_candidates(_ritems)
    nb_plan = {"mode": ("create" if create_nb else ("use" if nb_flag else "missing")),
               "notebookId": nb_flag or None}
    plan = {"ok": True, "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
            "config": path, "profile": name, "folder": folder,
            "vbt_parent": bool(vbt_id and vbt_id in ((finfo.get("file") or {}).get("parents") or [])),
            "steps": {"_meta": "reuse" if meta else "create",
                      "registry": "reuse" if reuse_reg else "create",
                      "manifest": "reuse" if reuse_man else "create",
                      "notebook": nb_plan["mode"], "marker": "create",
                      "config": "write", "seed": len(seeds), "system_prompt": "generate+apply"},
            "notebook_plan": nb_plan, "seed_count": len(seeds),
            "seed_sample": [s["name"][:60] for s in seeds[:10]],
            "reuse": {"registryDocId": reuse_reg or None, "manifestId": reuse_man or None}}
    if man_warn:
        plan.setdefault("warnings", []).append(man_warn)
    if seed_capped:
        plan.setdefault("warnings", []).append(
            "SEED_LIST_CAPPED: danh sách đệ quy bị cắt — seed CHƯA đủ; chạy lại promote sau khi giảm "
            "số file hoặc seed bổ sung bằng `register` tay.")
    if nb_plan["mode"] == "missing":
        plan.setdefault("warnings", []).append(
            "NO_NOTEBOOK: không --notebook/--create-notebook — lệnh NLM sẽ chặn tới khi có "
            "(bổ sung sau qua config/marker + backfill --force).")
    if not getattr(a, "apply", False):
        plan["note"] = ("DRY — --apply dựng hạ tầng + seed registry (journaled). Nạp NLM chạy SAU bằng "
                        "ingest-missing (xem next_steps khi apply).")
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    rid = _apply_journal_start("profile-promote", {"profile": name, "folder": folder, "seed": len(seeds)})
    results, all_ok = {}, True
    meta_id = str((meta or {}).get("id") or "")
    if not meta_id:
        try:
            mr = g.get("resolvefolder", name="_meta", parentId=folder, create="true")
        except Exception as e:  # noqa: BLE001
            mr = {"ok": False, "error": str(e)}
        meta_id = str((mr or {}).get("folderId") or "")
    results["meta_folder_id"] = meta_id
    if not meta_id:
        print(json.dumps({**plan, "ok": False, "error": "META_CREATE_FAILED"}, ensure_ascii=False, indent=2),
              file=sys.stderr)
        return 1
    reg_id = reuse_reg
    if not reg_id:
        reg = _create_profile_registry_sheet(g, meta_id, name)
        if not reg.get("ok"):
            print(json.dumps({**plan, "ok": False, "step": "create_registry_sheet", **reg},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 1
        reg_id = str(reg.get("registryDocId") or "")
    results["registryDocId"] = reg_id
    nb = nb_flag
    if create_nb:
        _journal_append(rid, {"t": "intent", "op": "nlm_notebook_create", "key": name,
                              "set": {"title": name}})
        try:
            nc = _imp("nlm_cli")
            cr = nc.notebook_create(name)
        except Exception as e:  # noqa: BLE001
            cr = {"ok": False, "error": f"NOTEBOOK_CREATE_RAISED:{type(e).__name__}"}
        d = cr.get("data") if isinstance(cr.get("data"), dict) else {}
        nb = str(d.get("id") or d.get("notebook_id") or (d.get("notebook") or {}).get("id") or "")
        nb_ok = bool(cr.get("ok")) and bool(nb)
        if nb_ok:    # readback ĐIỀU-KIỆN-KÉP: notebook_get canary xác nhận id sống
            try:
                nb_ok = bool((nc.notebook_get(nb) or {}).get("ok"))
            except Exception:  # noqa: BLE001
                nb_ok = False
        _journal_append(rid, {"t": "commit", "op": "nlm_notebook_create", "key": name, "ok": nb_ok,
                              "verify": {"notebookId": nb, "error": cr.get("error")}})
        if not nb_ok:
            print(json.dumps({**plan, "ok": False, "error": "NOTEBOOK_CREATE_FAILED", "detail": cr,
                              "note": "Kiểm auth NLM (`nlm login` + canary notebook_get) rồi chạy lại — "
                                      "promote idempotent, hạ tầng đã tạo sẽ được dùng lại."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 1
    results["notebookId"] = nb or None
    man_id = reuse_man
    if not man_id:
        man = _create_profile_manifest_json(g, meta_id, name, folder, nb)
        if not man.get("ok"):
            print(json.dumps({**plan, "ok": False, "step": "create_manifest_json", **man},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 1
        man_id = str(man.get("manifestId") or "")
    results["manifestId"] = man_id
    try:
        g.get("manifest_export", registryDocId=reg_id, manifestId=man_id)
    except Exception as e:  # noqa: BLE001
        results["manifest_export_note"] = f"bootstrap bỏ qua: {e}"
    prof_block = {"rootFolderId": folder, "metaFolderId": meta_id, "notebookId": nb,
                  "registryDocId": reg_id, "manifestId": man_id,
                  "manifestScope": "own", "categories": "own"}
    cfgp = _persist_profile_config(getattr(a, "config", None), name, prof_block)
    results["config_written"] = cfgp
    all_ok = all_ok and bool(cfgp)
    mkw = _marker_write(g, meta_id, _marker_body(name, prof_block), run_id=rid)
    results["marker"] = {"fileId": mkw.get("fileId"), "verified": mkw.get("verified")}
    all_ok = all_ok and bool(mkw.get("verified"))
    seeded, seed_fail = [], []
    for s in seeds:
        payload = {"drive_id": s["drive_id"], "name": s["name"], "row_kind": "own", "corpus": "true"}
        v = _journaled_reg_upsert(rid, g, payload)
        (seeded if v.get("verified") else seed_fail).append(s["drive_id"])
    results["seeded"] = len(seeded)
    if seed_fail:
        results["seed_failed"] = seed_fail[:20]
        all_ok = False
    results["system_prompt"] = _nlm_system_prompt_apply(g, meta_id, nb, run_id=rid)
    out = {**plan, "ok": all_ok, **results, "journal": rid,
           "system_prompt": results["system_prompt"],
           "next_steps": [
               f"tl --profile {name} ingest-missing --allow-no-sohieu --limit 15 --apply   "
               f"(lặp tới rc=0 — nạp {len(seeds)} nguồn lên notebook, idempotent/resume)",
               f"tl profile-load {name}   (Instruction Block phiên)",
               "tl profile-index --rebuild --apply   (cập nhật sổ cái)",
           ]}
    print(json.dumps(out, ensure_ascii=False, indent=2), file=sys.stdout if all_ok else sys.stderr)
    return 0 if all_ok else 1


# ── P4 (v1.34.26, Q4 + materialize_preferred): NOTEBOOK NLM → PROFILE + nguồn nlm-only ──
# Không bump GAS: row nlm-only dùng SENTINEL drive_id 'nlm:<source_id>' (registry key drive_id giữ chuẩn
# journal/undo); materialize_status suy diễn: pending/blocked ghi cột `note`, done = row thật tồn tại.
_NLM_ONLY_SENTINEL_PREFIX = "nlm:"


def _nlm_only_sentinel(sid: str) -> str:
    return _NLM_ONLY_SENTINEL_PREFIX + str(sid or "")


def _from_nlm_row_payload(source: dict, notebook_id: str) -> dict:
    """PURE (Q4): nguồn NLM → payload row registry. Nguồn CÓ file Drive (type=drive/url docs.google) →
    row_kind=ref với drive_id THẬT (file ngoài cây profile); còn lại (text/url/YouTube) → nlm_only
    với sentinel + note=materialize=pending (materialize_preferred sẽ nâng cấp sau)."""
    source = source or {}
    sid = str(source.get("id") or "")
    title = str(source.get("title") or sid)[:120]
    did = _nlm_source_drive_id(source)
    base = {"name": title, "nlm_source_id": sid, "nlm_notebook_id": str(notebook_id or ""),
            "nlm_title": title}
    if did:
        return {**base, "drive_id": str(did), "row_kind": "ref", "corpus": "false", "nlm_status": "pushed"}
    return {**base, "drive_id": _nlm_only_sentinel(sid), "row_kind": "nlm_only", "corpus": "false",
            "nlm_status": "nlm_only", "note": "materialize=pending"}


def cmd_profile_from_nlm(a) -> int:
    with _ProfileEnvGuard():
        return _cmd_profile_from_nlm_impl(a)


def _cmd_profile_from_nlm_impl(a) -> int:
    """P4 (v1.34.26, Q4): BIẾN NOTEBOOK NLM THÀNH PROFILE THƯỜNG — dựng folder riêng (mặc định tạo mới
    dưới Van_ban_thuong; --folder dùng folder sẵn có) + _meta/registry/manifest/marker/config own+own,
    rồi SEED registry từ danh sách nguồn notebook: nguồn có file Drive → row ref; còn lại → row nlm_only
    (sentinel, materialize=pending). KHÔNG tự áp System Prompt (notebook ĐANG DÙNG — không ghi đè cấu
    hình chat sẵn có; khác promote tạo notebook mới). Materialize chạy SAU bằng lệnh riêng resumable
    (chính sách mặc định materialize_preferred — CONTEXT.md). DRY mặc định. rc: 0 / 1 bước fail / 2 guard."""
    name = (getattr(a, "name", None) or "").strip()
    nb = (getattr(a, "notebook", None) or "").strip()
    if not name or not nb:
        print("[tl] profile-from-nlm cần --name và --notebook", file=sys.stderr)
        return 2
    if name == DEFAULT_PROFILE:
        print("[tl] REFUSE_FROM_NLM_DEFAULT_PROFILE: vbqppl là profile nền.", file=sys.stderr)
        return 2
    folder = (getattr(a, "folder", None) or "").strip()
    path, cfg = _read_config_record(getattr(a, "config", None))
    existing = _profiles_from_config(cfg).get(name) if cfg else None
    existing = existing if isinstance(existing, dict) else None
    if existing and str(existing.get("rootFolderId") or "").strip() and folder \
            and str(existing.get("rootFolderId")) != folder:
        print(json.dumps({"ok": False, "error": "PROFILE_EXISTS_DIFFERENT_FOLDER", "profile": name},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    try:
        load_creds(getattr(a, "config", None), DEFAULT_PROFILE)
    except SystemExit as e:
        print(f"[tl] profile-from-nlm cần webapp LIVE: {e}", file=sys.stderr)
        return 2
    g = _gas()
    try:
        nc = _imp("nlm_cli")
        sl = nc.source_list(nb)
    except Exception as e:  # noqa: BLE001
        sl = {"ok": False, "error": f"{type(e).__name__}: {e}"}
    if not sl.get("ok"):
        print(json.dumps({"ok": False, "error": "NLM_SOURCE_LIST_FAILED", "detail": sl.get("error"),
                          "auth_hint": sl.get("auth_hint")}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    sources = sl.get("sources") or []
    payloads = [_from_nlm_row_payload(s, nb) for s in sources]
    n_only = sum(1 for p in payloads if p["row_kind"] == "nlm_only")
    n_ref = len(payloads) - n_only
    # --folder sẵn có: kiểm marker (ALREADY_PROFILE) + dò asset reuse như promote
    reuse_reg = reuse_man = ""
    meta_id = ""
    if folder:
        try:
            items = _gas_get_retry(g, "list", folderId=folder).get("items") or []
        except Exception as e:  # noqa: BLE001
            print(json.dumps({"ok": False, "error": f"FOLDER_LIST_FAILED: {e}"}, ensure_ascii=False),
                  file=sys.stderr)
            return 2
        meta = next((x for x in items if str(x.get("type")) == "folder" and str(x.get("name")) == "_meta"), None)
        meta_id = str((meta or {}).get("id") or "")
        mitems = []
        if meta_id:
            try:
                mitems = _gas_get_retry(g, "list", folderId=meta_id).get("items") or []
            except Exception:
                pass
        if _marker_find_in_items(mitems):
            print(json.dumps({"ok": False, "error": "ALREADY_PROFILE", "folder": folder,
                              "note": "folder đã có marker — dùng profile-sync/adopt."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        picked = _adopt_pick_assets(items + mitems)
        reuse_reg = str((picked.get("registry") or {}).get("id") or "")
        _mc = str((picked.get("manifest") or {}).get("id") or "")
        if _mc:
            try:
                _dm = _gas_get_retry(g, "download", fileId=_mc)
                _mj = (json.loads(base64.b64decode(_dm.get("b64") or "").decode("utf-8"))
                       if _dm.get("b64") else {})
            except Exception:  # noqa: BLE001
                _mj = {}
            if str((_mj or {}).get("profile") or "") == name:
                reuse_man = _mc
    plan = {"ok": True, "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
            "config": path, "profile": name, "notebook": nb, "folder": folder or "(tạo mới dưới Van_ban_thuong)",
            "source_total": len(payloads), "nlm_only_count": n_only, "ref_count": n_ref,
            "source_sample": [p["name"][:60] for p in payloads[:10]],
            "system_prompt": "skipped_existing_notebook (không ghi đè chat config của notebook đang dùng — "
                             "muốn áp: `nlm chat configure <nb> --goal custom --prompt <_meta/nlm_system_prompt.md>`)",
            "note": "DRY — --apply dựng hạ tầng + seed row ref/nlm_only; materialize chạy SAU (lệnh riêng)."}
    if not getattr(a, "apply", False):
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    rid = _apply_journal_start("profile-from-nlm", {"profile": name, "notebook": nb, "sources": len(payloads)})
    root_id = folder
    if not root_id:
        try:
            vbt_id = str((g.get("bootstrap") or {}).get("vanBanThuongId") or "")
            rr = g.get("resolvefolder", name=name, parentId=vbt_id, create="true")
        except Exception as e:  # noqa: BLE001
            rr = {"ok": False, "error": str(e)}
        root_id = str((rr or {}).get("folderId") or "")
    if not root_id:
        print(json.dumps({**plan, "ok": False, "error": "ROOT_CREATE_FAILED"}, ensure_ascii=False, indent=2),
              file=sys.stderr)
        return 1
    if not meta_id:
        try:
            mr = g.get("resolvefolder", name="_meta", parentId=root_id, create="true")
        except Exception as e:  # noqa: BLE001
            mr = {"ok": False, "error": str(e)}
        meta_id = str((mr or {}).get("folderId") or "")
    if not meta_id:
        print(json.dumps({**plan, "ok": False, "error": "META_CREATE_FAILED"}, ensure_ascii=False, indent=2),
              file=sys.stderr)
        return 1
    reg_id = reuse_reg
    if not reg_id:
        reg = _create_profile_registry_sheet(g, meta_id, name)
        if not reg.get("ok"):
            print(json.dumps({**plan, "ok": False, "step": "create_registry_sheet", **reg},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 1
        reg_id = str(reg.get("registryDocId") or "")
    man_id = reuse_man
    if not man_id:
        man = _create_profile_manifest_json(g, meta_id, name, root_id, nb)
        if not man.get("ok"):
            print(json.dumps({**plan, "ok": False, "step": "create_manifest_json", **man},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 1
        man_id = str(man.get("manifestId") or "")
    try:
        g.get("manifest_export", registryDocId=reg_id, manifestId=man_id)
    except Exception:  # noqa: BLE001
        pass
    prof_block = {"rootFolderId": root_id, "metaFolderId": meta_id, "notebookId": nb,
                  "registryDocId": reg_id, "manifestId": man_id,
                  "manifestScope": "own", "categories": "own"}
    cfgp = _persist_profile_config(getattr(a, "config", None), name, prof_block)
    mkw = _marker_write(g, meta_id, _marker_body(name, prof_block), run_id=rid)
    all_ok = bool(cfgp) and bool(mkw.get("verified"))
    seeded, seed_fail = 0, []
    for p in payloads:
        v = _journaled_reg_upsert(rid, g, p)
        if v.get("verified"):
            seeded += 1
        else:
            seed_fail.append(p.get("nlm_source_id"))
    if seed_fail:
        all_ok = False
    out = {**plan, "ok": all_ok, "rootFolderId": root_id, "metaFolderId": meta_id,
           "registryDocId": reg_id, "manifestId": man_id, "config_written": cfgp,
           "marker": {"fileId": mkw.get("fileId"), "verified": mkw.get("verified")},
           "seeded": seeded, "seed_failed": seed_fail[:20], "journal": rid,
           "next_steps": [
               f"tl profile-materialize-sources --profile-name {name} --apply   "
               f"(lặp tới rc=0 & pending=0 — nâng cấp {n_only} nguồn nlm-only thành file Drive)",
               f"tl profile-load {name}   (Instruction Block phiên — nói rõ nguồn nào chỉ có trên NLM)",
               "tl profile-index --rebuild --apply",
           ]}
    print(json.dumps(out, ensure_ascii=False, indent=2), file=sys.stdout if all_ok else sys.stderr)
    return 0 if all_ok else 1


def cmd_profile_materialize_sources(a) -> int:
    with _ProfileEnvGuard():
        return _cmd_profile_materialize_sources_impl(a)


def _cmd_profile_materialize_sources_impl(a) -> int:
    """P4 (materialize_preferred — CONTEXT.md): nâng cấp nguồn nlm-only → file Drive + row thường.
    RESUMABLE: mỗi run xử tối đa --limit nguồn, chạy lặp tới rc=0 & pending=0; blocked chỉ thử lại khi
    --retry-blocked. TẠO-TRƯỚC-XOÁ-SAU: row own ghi verified xong mới reg_delete row sentinel (đứt giữa
    chừng → doctor --deep thấy SENTINEL_STALE, run sau tự dọn). Nguồn không xuất được (URL/YouTube/rỗng)
    → note=materialize=blocked:<reason> — Ở LẠI nlm-only là HỢP LỆ (Q4). DRY mặc định."""
    path, cfg = _read_config_record(getattr(a, "config", None))
    if not cfg:
        print("[tl] Không thấy config; truyền --config.", file=sys.stderr)
        return 2
    profs = _profiles_from_config(cfg)
    name = (getattr(a, "target_profile", None) or "").strip() or _active_profile()
    if name == DEFAULT_PROFILE:
        print("[tl] profile-materialize-sources chỉ dùng cho profile dự án (--profile-name <p>).", file=sys.stderr)
        return 2
    name, prof = _profile_lookup(profs, name)
    if not isinstance(prof, dict):
        print(json.dumps({"ok": False, "error": "PROFILE_NOT_FOUND", "profile": name}, ensure_ascii=False),
              file=sys.stderr)
        return 2
    nb = str(prof.get("notebookId") or "").strip()
    root = str(prof.get("rootFolderId") or "").strip()
    if not nb or not root:
        print(json.dumps({"ok": False, "error": "PROFILE_INCOMPLETE", "notebookId": nb, "rootFolderId": root},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    try:
        load_creds(getattr(a, "config", None), name)   # Cách B: forward registryDocId của profile vào call
    except SystemExit as e:
        print(f"[tl] profile-materialize-sources cần webapp LIVE: {e}", file=sys.stderr)
        return 2
    g = _gas()
    try:
        nc = _imp("nlm_cli")
        sl = nc.source_list(nb)
    except Exception as e:  # noqa: BLE001
        sl = {"ok": False, "error": f"{type(e).__name__}: {e}"}
    if not sl.get("ok"):
        print(json.dumps({"ok": False, "error": "NLM_SOURCE_LIST_FAILED", "detail": sl.get("error"),
                          "auth_hint": sl.get("auth_hint")}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    rows, todo, stale = [], [], []
    for s in (sl.get("sources") or []):
        sid = str(s.get("id") or "")
        title = str(s.get("title") or sid)[:120]
        try:
            rg = _gas_get_retry(g, "reg_get", nlm_source_id=sid, refresh="false")
            rr = rg.get("rows") or []
        except Exception as e:  # noqa: BLE001
            rows.append({"nlm_source_id": sid, "title": title, "status": "read_failed", "error": str(e)})
            continue
        own = [r for r in rr if str(r.get("drive_id") or "")
               and not str(r.get("drive_id")).startswith(_NLM_ONLY_SENTINEL_PREFIX)]
        sent = [r for r in rr if str(r.get("drive_id") or "").startswith(_NLM_ONLY_SENTINEL_PREFIX)]
        if own:
            row = {"nlm_source_id": sid, "title": title, "status": "done", "drive_id": own[0].get("drive_id")}
            if sent:
                row["sentinel_stale"] = sent[0].get("drive_id")
                stale.append({"sid": sid, "sentinel": str(sent[0].get("drive_id"))})
            rows.append(row)
        elif sent:
            blocked = "materialize=blocked" in str(sent[0].get("note") or "")
            row = {"nlm_source_id": sid, "title": title,
                   "status": "blocked" if blocked else "pending",
                   "sentinel": str(sent[0].get("drive_id"))}
            if blocked:
                row["note"] = str(sent[0].get("note") or "")
            rows.append(row)
            if not blocked or getattr(a, "retry_blocked", False):
                todo.append({"sid": sid, "title": title, "sentinel": str(sent[0].get("drive_id"))})
        else:
            rows.append({"nlm_source_id": sid, "title": title, "status": "unregistered",
                         "note": "không có row registry — chạy lại `tl profile-from-nlm` (idempotent)."})
    lim = int(getattr(a, "limit", None) or 10)
    batch = todo[:lim]
    counts = {"done": sum(1 for r in rows if r["status"] == "done"),
              "pending": sum(1 for r in rows if r["status"] == "pending"),
              "blocked": sum(1 for r in rows if r["status"] == "blocked"),
              "unregistered": sum(1 for r in rows if r["status"] == "unregistered")}
    if not getattr(a, "apply", False):
        out = {"ok": True, "mode": "DRY", "profile": name, "notebook": nb, "rows": rows, **counts,
               "would_process": len(batch), "sentinel_stale": len(stale),
               "note": "--apply: source_content → createtext GDoc vào folder profile → row own + xoá sentinel "
                       "(tạo-trước-xoá-sau, journaled). Chạy lặp tới pending=0."}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    rid = _apply_journal_start("profile-materialize-sources", {"profile": name, "batch": len(batch)})
    by_sid = {r.get("nlm_source_id"): r for r in rows}
    failed = []
    def _del_sentinel(sentinel: str, sid: str) -> bool:
        _journal_append(rid, {"t": "intent", "op": "reg_delete", "key": sentinel,
                              "set": {"reason": f"sentinel nlm_only đã materialize (sid={sid})"}})
        try:
            dr = g.post("reg_delete", drive_ids=[sentinel], confirm="yes", require_removed="no")
        except Exception as e:  # noqa: BLE001
            dr = {"ok": False, "error": str(e)}
        _journal_append(rid, {"t": "commit", "op": "reg_delete", "key": sentinel, "ok": bool(dr.get("ok"))})
        return bool(dr.get("ok"))
    for st in stale:   # dọn sentinel sót từ run đứt giữa chừng (idempotent)
        _del_sentinel(st["sentinel"], st["sid"])
        by_sid.get(st["sid"], {})["sentinel_cleaned"] = True
    for t in batch:
        sid, title, sentinel = t["sid"], t["title"], t["sentinel"]
        try:
            cont = nc.source_content(sid)
        except Exception as e:  # noqa: BLE001
            cont = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        d = cont.get("data") if isinstance(cont.get("data"), dict) else {}
        text = str(d.get("content") or d.get("text") or cont.get("text") or "")
        if cont.get("ok") and len(text.strip()) >= 40:
            try:
                up = g.post("createtext", text=text, name=title, folderId=root,
                            register="false", share="false")
            except Exception as e:  # noqa: BLE001
                up = {"ok": False, "error": str(e)}
            fid = str((up or {}).get("fileId") or (up or {}).get("id") or "")
            if not fid:
                by_sid[sid].update({"status": "failed", "error": str((up or {}).get("error") or "CREATETEXT_FAILED")})
                failed.append(sid)
                continue
            newp = {"drive_id": fid, "name": title, "nlm_source_id": sid, "nlm_notebook_id": nb,
                    "nlm_title": title, "row_kind": "own", "corpus": "true", "nlm_status": "pushed",
                    "note": f"materialized_from=nlm:{sid}"}
            v = _journaled_reg_upsert(rid, g, newp)
            if v.get("verified"):
                _del_sentinel(sentinel, sid)
                by_sid[sid].update({"status": "materialized", "drive_id": fid, "chars": len(text)})
            else:
                by_sid[sid].update({"status": "failed", "error": "ROW_UPSERT_UNVERIFIED"})
                failed.append(sid)
        else:
            reason = str(cont.get("error") or "EMPTY_CONTENT")[:120]
            _journaled_reg_upsert(rid, g, {"drive_id": sentinel, "nlm_source_id": sid,
                                           "nlm_notebook_id": nb, "row_kind": "nlm_only",
                                           "note": f"materialize=blocked:{reason}"})
            by_sid[sid].update({"status": "blocked", "note": f"materialize=blocked:{reason}"})
    remaining = sum(1 for r in rows if r.get("status") == "pending")
    out = {"ok": not failed, "mode": "APPLY", "profile": name, "notebook": nb, "rows": rows,
           "processed": len(batch), "failed": failed, "pending_remaining": remaining, "journal": rid,
           "resume_command": (f"tl profile-materialize-sources --profile-name {name} --apply"
                              if remaining else None),
           "note": "nguồn blocked Ở LẠI nlm-only là HỢP LỆ (Q4) — Instruction Block sẽ nói rõ chúng chỉ có trên NLM."}
    print(json.dumps(out, ensure_ascii=False, indent=2), file=sys.stdout if not failed else sys.stderr)
    return 0 if not failed else 1


def _discover_scan_vbthuong(g, vbt_id: str, folder_cap: int = 60) -> dict:
    """B: quét Van_ban_thuong 2 cấp read-only qua GAS `list` — con trực tiếp + trong `_meta` của từng thư mục con
    (registry/manifest kiểu mới nằm trong _meta, kiểu cũ nằm thẳng trong folder). Cap thư mục quét, LOUD khi cắt.
    P1 (v1.34.22): đọc thêm MARKER `tra_luat_profile.json` (ADR-0003) — kèm marker/marker_error/marker_file_id."""
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
        marker, merr, mfid = None, None, ""
        mit = _marker_find_in_items(sitems)
        if mit:
            mfid = str(mit.get("id") or "")
            try:
                d = _gas_get_retry(g, "download", fileId=mfid)
                marker = json.loads(base64.b64decode(d.get("b64") or "").decode("utf-8"))
            except Exception as e:  # noqa: BLE001
                merr = f"MARKER_PARSE_FAILED: {e}"
        out_folders.append({"id": fo.get("id"), "name": fo.get("name"), "items": sitems,
                            "meta_folder_id": (meta or {}).get("id"),
                            "marker": marker, "marker_error": merr, "marker_file_id": mfid})
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
