#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""transport.py — ROUTER transport Drive (gws PRIMARY mọi env | GAS fallback | mcp opt-in).

Kiến trúc env (RUNBOOK §A0):
  Code/Cowork/Chat → backend `gws` (PRIMARY), lỗi/không-sẵn → `[FALLBACK→GAS]` ỒN ÀO.
    (Chat NAY chạy được gws trong shell → định tuyến như Code/Cowork; KHÔNG còn buộc mcp.)
  Pure-chat KHÔNG shell (chỉ có Drive MCP): đặt TL_DRIVE_BACKEND=mcp → read raise DeferToMCP, D raise DeferToShell.
Phân nhóm op (ranh giới cứng, handoff A–E):
  A read  (files_get/files_list/search/read)  — không confirm.
  B write an toàn (upload/copy_convert/mkdir)  — không confirm.
  C write rủi ro  (move/rename/trash/restore)  — CONFIRM gate theo lô (ConfirmRequired).
  D business-logic (register/manifest/preflight/slot/standardize_name/organize/footnote_map/vbhn)
                  — GAS ĐỘC QUYỀN. (LƯU Ý v1.29.0: gws CLI NAY có Sheets API — lý do KHÔNG còn là "thiếu
                    Sheets"; GHI vẫn GAS vì LockService khóa 30s + read-modify-write swap NGUYÊN TỬ + logic
                    dedup/regen2/treeHash ở Apps Script (chuyển=phân kỳ). ĐỌC registry đã áp gws-primary NGOÀI
                    router này: `_load_manifest_full` (tải manifest.json direct-media) + `precheck --gws-live`.)
                    backend mcp (pure-chat) → DeferToShell (defer sang shell Code/Cowork).
"""
from __future__ import annotations
import os
import sys as _sys
from pathlib import Path

# Bootstrap path: cho phép import gws_bridge/mcp_bridge/gas khi transport được import độc lập.
_HERE = Path(__file__).resolve().parent
for _p in (str(_HERE), str(_HERE / "_fallback")):
    if _p not in _sys.path:
        _sys.path.insert(0, _p)

import gws_bridge          # noqa: E402
import mcp_bridge          # noqa: E402
from mcp_bridge import DeferToMCP  # noqa: E402,F401  (re-export)


# ───────────────────────── phân nhóm op ─────────────────────────
OP_GROUP = {
    # A — read
    "files_get": "A", "files_list": "A", "search": "A", "read": "A", "download": "A",
    # B — write an toàn
    "upload": "B", "copy_convert": "B", "mkdir": "B",
    # C — write rủi ro (confirm theo lô)
    "move": "C", "rename": "C", "trash": "C", "restore": "C",
    # D — business-logic (GAS độc quyền; backend mcp/pure-chat defer)
    "register": "D", "manifest": "D", "preflight": "D", "slot": "D",
    "standardize_name": "D", "organize": "D", "footnote_map": "D", "vbhn": "D",
}

# gws PRIMARY cho MỌI env (Chat nay chạy được gws trong shell). GAS = fallback tự động khi gws lỗi/thiếu.
# ÉP mcp cho pure-chat KHÔNG shell (Claude chỉ có Drive MCP, không có Python gws): TL_DRIVE_BACKEND=mcp.
_BACKEND_BY_ENV = {"code": "gws", "cowork": "gws", "chat": "gws"}


def _resolve_backend(env: str) -> str:
    """Backend Drive cho env; cho phép ÉP qua TL_DRIVE_BACKEND ∈ {gws, mcp} (mcp = pure-chat không shell)."""
    ov = (os.environ.get("TL_DRIVE_BACKEND") or "").strip().lower()
    if ov in ("gws", "mcp"):
        return ov
    return _BACKEND_BY_ENV.get(env, "gws")


class TransportError(RuntimeError):
    pass


class ConfirmRequired(TransportError):
    """Op nhóm C (ghi rủi ro) gọi mà chưa confirmed=True (gate theo lô)."""


class DeferToShell(TransportError):
    """Op nhóm D (business-logic) ở env Chat — KHÔNG chạy được, defer Code/Cowork."""


# ───────────────────────── env ─────────────────────────
def runtime_env(override: str | None = None) -> str:
    """Env cho TRANSPORT. transport.py CHỈ chạy được trong shell (Python) ⇒ heuristic KHÔNG BAO GIỜ trả
    'chat' (chat thật không thực thi Python — nó gọi Drive MCP trực tiếp). Nếu để default 'chat' thì Cowork
    (không set COWORK) bị nhận nhầm là chat → SKIP gws + định tuyến MCP SAI. Ưu tiên:
      override(--env) → TL_RUNTIME_ENV → marker Code → marker Cowork → MẶC ĐỊNH 'cowork' (shell chưa nhãn).
    'chat' CHỈ khi chủ đích (--env chat / TL_RUNTIME_ENV=chat) — dùng cho sinh spec/parity-test."""
    v = (override or "").strip().lower()
    if v in ("code", "cowork", "chat"):
        return v
    ev = (os.environ.get("TL_RUNTIME_ENV") or "").strip().lower()
    if ev in ("code", "cowork", "chat"):
        return ev
    if os.environ.get("CLAUDECODE") or os.environ.get("CLAUDE_CODE_ENTRYPOINT") or os.environ.get("CLAUDE_CODE"):
        return "code"
    if os.environ.get("CLAUDE_COWORK") or os.environ.get("COWORK"):
        return "cowork"
    return "cowork"   # shell chưa nhãn ⇒ Cowork (gws→GAS), KHÔNG phải chat


# ───────────────────────── GAS backend (fallback + nhóm D) ─────────────────────────
# op → (action, builder params). Chỉ map những op có ĐỐI XỨNG Drive thuần ở GAS.
def _gas_module(gas=None):
    if gas is not None:
        return gas
    import importlib
    return importlib.import_module("gas")


def _gas_files_get(gas, file_id, **_):
    r = gas.get("info", fileId=file_id)
    if isinstance(r, dict) and r.get("ok") and isinstance(r.get("file"), dict):
        return {"ok": True, "file": gws_bridge.normalize_file(r["file"])}
    return {"ok": False, "error": (r or {}).get("error", "GAS info: thiếu file"), "raw": r}


def _gas_read(gas, file_id, offset=0, limit=None, **_):
    kw = {"id": file_id, "offset": offset}
    if limit is not None:
        kw["limit"] = limit
    return gas.get("read", **kw)


def _gas_download(gas, file_id, dest, **_):
    """Fallback download qua webapp `download` (b64) → decode THẲNG xuống đĩa (KHÔNG vào context).
    LƯU Ý: cap webapp DOWNLOAD_MAX_BYTES_ ~9MB; file lớn hơn PHẢI dùng gws."""
    import base64 as _b64
    r = gas.get("download", fileId=file_id)
    if not isinstance(r, dict) or not r.get("ok") or not r.get("b64"):
        return {"ok": False, "error": (r or {}).get("error", "GAS download: thiếu b64"), "raw": r}
    raw = _b64.b64decode(r["b64"])
    with open(dest, "wb") as f:
        f.write(raw)
    return {"ok": True, "path": os.path.abspath(dest), "bytes": len(raw)}


def _gas_copy_convert(gas, file_id, name=None, parents=None, **_):
    kw = {"fileId": file_id}
    if name:
        kw["name"] = name
    if parents:
        kw["folderId"] = parents[0] if isinstance(parents, (list, tuple)) else parents
    return gas.get("copy_convert", **kw)


# Webapp GAS có guard riêng cho hành động phá hủy/nặng (cần confirm=yes). Router đã qua confirm-gate
# (confirmed=True) TRƯỚC khi tới đây → forward confirm="yes" cho C-ops GAS là đúng phân quyền.
def _gas_move(gas, file_id, to_folder, **_):
    return gas.get("move", fileId=file_id, folderId=to_folder, confirm="yes")


def _gas_rename(gas, file_id, name, **_):
    return gas.get("rename", fileId=file_id, name=name, confirm="yes")


def _gas_trash(gas, file_id, **_):
    return gas.get("trash", fileId=file_id, confirm="yes")


def _gas_restore(gas, file_id, **_):
    return gas.get("restore", fileId=file_id, confirm="yes")


def _gas_mkdir(gas, name, parents=None, **_):
    kw = {"name": name}
    if parents:
        kw["folderId"] = parents[0] if isinstance(parents, (list, tuple)) else parents
    return gas.get("mkdir", **kw)


_GAS_READ = {"files_get": _gas_files_get, "read": _gas_read, "download": _gas_download}
_GAS_B = {"copy_convert": _gas_copy_convert, "mkdir": _gas_mkdir}   # nhóm B GAS server-side
_GAS_C = {"move": _gas_move, "rename": _gas_rename, "trash": _gas_trash, "restore": _gas_restore}
# Ánh xạ op nhóm D → action GAS (gọi thẳng, business-logic).
_GAS_D_ACTION = {
    "register": "register", "manifest": "manifest", "preflight": "nlm_preflight",
    "slot": "nlm_slots", "organize": "organize", "footnote_map": "footnote_map",
}
# Op KHÔNG có đối xứng GAS (webapp không nhận binary local) → KHÔNG fallback GAS, để lộ lỗi gws rõ.
_NO_GAS_FALLBACK = {"upload"}
# B3: gom cảnh báo FALLBACK→GAS — gws CHƯA nạp cả phiên thì in 1 LẦN/phiên (thay vì mỗi read), tránh nhiễu log
# khiến script gọi tự động tưởng có lỗi. Key "gws-unavailable" cho ca systemic; "<op>:<err>" cho lỗi gws cá biệt.
_GWS_FALLBACK_WARNED: set = set()


def _gas_call(op, *, gas=None, **kw):
    gas = _gas_module(gas)
    if op in _GAS_READ:
        return _GAS_READ[op](gas, **kw)
    if op in _GAS_B:
        return _GAS_B[op](gas, **kw)
    if op in _GAS_C:
        return _GAS_C[op](gas, **kw)
    if op in _GAS_D_ACTION:
        return gas.get(_GAS_D_ACTION[op], **kw)
    raise TransportError(f"GAS chưa map op: {op}")


# ───────────────────────── backend gws ─────────────────────────
def via_gws(op, **kw):
    return gws_bridge.call(op, **kw)


def via_gas(op, *, gas=None, **kw):
    return _gas_call(op, gas=gas, **kw)


def mcp_spec(op, **kw):
    return mcp_bridge.spec(op, **kw)


# ───────────────────────── ROUTER ─────────────────────────
def drive_op(op, *, env=None, confirmed=False, gas=None, _quiet=False, **kw):
    """Định tuyến 1 op Drive theo env + nhóm. Trả kết quả JSON-dict (hoặc spec MCP nếu backend=mcp).

    Raise: TransportError (op lạ) · ConfirmRequired (C chưa confirm) · DeferToShell (D khi backend=mcp) ·
           DeferToMCP (read khi backend=mcp). gws lỗi/không-sẵn ⇒ tự FALLBACK→GAS (ồn ào).
    backend = _resolve_backend(env): mặc định gws MỌI env; ÉP mcp qua TL_DRIVE_BACKEND=mcp (pure-chat không shell)."""
    group = OP_GROUP.get(op)
    if group is None:
        raise TransportError(f"op không khai báo OP_GROUP: {op}")
    env = runtime_env(env)
    backend = _resolve_backend(env)

    # D — business-logic: GAS độc quyền (gws-bridge chưa có Sheets API + logic ở Apps Script).
    # Chỉ defer khi backend mcp (pure-chat KHÔNG shell); mọi shell (Code/Cowork/Chat-có-gws) chạy GAS thẳng.
    if group == "D":
        if backend == "mcp":
            raise DeferToShell(f"[{op}] business-logic (GAS độc quyền) — pure-chat (mcp) defer sang shell Code/Cowork.")
        return _gas_call(op, gas=gas, **kw)

    # C — ghi rủi ro: cổng confirm theo lô.
    if group == "C" and not confirmed:
        raise ConfirmRequired(f"[{op}] ghi rủi ro — cần confirm theo LÔ (confirmed=True) trước khi chạy.")

    # backend mcp (pure-chat KHÔNG shell) → Python không thực thi Drive; trả/raise spec cho Claude Drive MCP.
    if backend == "mcp":
        return mcp_bridge.call(op, **kw)   # raise DeferToMCP(spec)

    # download: ƯU TIÊN DIRECT-MEDIA (raw alt=media/export, byte-exact MỌI loại kể cả text/JSON, token-cache,
    # nhanh nhất theo benchmark) nếu có gws cred. Lỗi → rơi xuống chuỗi gws→GAS bên dưới.
    if op == "download" and kw.get("dest"):
        try:
            import importlib
            _tlg = importlib.import_module("tl_gws")
            _cred = _tlg._read_gws_cred()
            if _cred:
                return _tlg._drive_media_download(kw["file_id"], kw["dest"], _cred,
                                                  export_mime=kw.get("export_mime"))
        except Exception as e:  # noqa: BLE001
            if not _quiet:
                _sys.stderr.write(f"[download] direct-media lỗi ({type(e).__name__}: {e}); thử gws/GAS…\n")

    # Code/Cowork → gws PRIMARY, lỗi → FALLBACK→GAS ồn ào.
    try:
        if not gws_bridge.is_available():
            raise gws_bridge.GwsError("gws not available (PATH/version/auth) hoặc TL_GWS_DISABLE=1")
        return via_gws(op, **kw)
    except NotImplementedError:
        raise   # op chưa hiện thực ở gws (GĐ3) → KHÔNG nuốt thành fallback (để lộ rõ giai đoạn)
    except Exception as e:  # noqa: BLE001
        if op in _NO_GAS_FALLBACK:
            raise   # không có đối xứng GAS (vd upload binary) → ném lỗi gws, không giả vờ fallback
        if not _quiet:
            _msg = str(e)
            _systemic = "not available" in _msg          # gws CHƯA nạp cả phiên (ca hay gặp khi thiếu cred)
            _key = "gws-unavailable" if _systemic else f"{op}:{_msg[:60]}"
            if _key not in _GWS_FALLBACK_WARNED:          # B3: chỉ in LẦN ĐẦU mỗi loại → hết spam mỗi read
                _GWS_FALLBACK_WARNED.add(_key)
                if _systemic:
                    # B6: PHÂN BIỆT thiếu-CRED vs thiếu-BINARY (trước nói "gws CHƯA nạp" gây hiểu nhầm cred lỗi).
                    _has_cred = False
                    try:
                        import importlib
                        _has_cred = bool(importlib.import_module("tl_gws")._read_gws_cred())
                    except Exception:  # noqa: BLE001
                        _has_cred = False
                    if _has_cred:
                        _sys.stderr.write("[FALLBACK→GAS] gws CÓ CRED nhưng THIẾU BINARY → op này (find/ghi) đi GAS. "
                                          "Bật binary: `tl gws-bootstrap-cowork`. (extract/đọc đã dùng direct-media bằng cred.) "
                                          "[ẩn lặp sau]\n")
                    else:
                        _sys.stderr.write("[FALLBACK→GAS] gws THIẾU CRED phiên này → đọc Drive đi GAS (ĐÚNG, chậm hơn). "
                                          "Bật: `tl gws-auth-load` (cred public, không cần master key). [ẩn lặp sau]\n")
                else:
                    _sys.stderr.write(f"[FALLBACK→GAS] op={op} backend=gws lỗi: {e} [ẩn lặp sau]\n")
        return _gas_call(op, gas=gas, **kw)


def _kw_brief(kw: dict) -> str:
    keys = ("file_id", "name", "to_folder")
    parts = [f"{k}={kw[k]}" for k in keys if k in kw]
    return ", ".join(parts) or ",".join(map(str, kw))


def run_batch(items, *, env=None, confirmed=False, gas=None):
    """Chạy 1 LÔ thao tác Drive với CONFIRM-GATE THEO LÔ (handoff nhóm C).

    items: list[(op, kwargs)]. Nếu lô có op nhóm C và `confirmed=False` → raise ConfirmRequired LIỆT KÊ
    cả lô (xác nhận 1 lần, không hỏi từng file). `confirmed=True` → chạy tuần tự (mỗi op confirmed=True).
    Op nhóm A/B trong lô vẫn chạy bình thường. Trả list kết quả theo thứ tự (op lỗi → {'ok':False,...})."""
    env = runtime_env(env)
    risky = [(op, kw) for op, kw in items if OP_GROUP.get(op) == "C"]
    if risky and not confirmed:
        lines = "; ".join(f"{op}({_kw_brief(kw)})" for op, kw in risky)
        raise ConfirmRequired(
            f"LÔ {len(risky)}/{len(items)} thao tác GHI RỦI RO (nhóm C) — xác nhận 1 LẦN cho cả lô "
            f"(confirmed=True) trước khi chạy: {lines}")
    results = []
    for op, kw in items:
        try:
            results.append(drive_op(op, env=env, confirmed=True, gas=gas, **kw))
        except Exception as e:  # noqa: BLE001
            results.append({"ok": False, "op": op, "error": f"{type(e).__name__}: {e}"})
    return results


# ───────────────────────── selftest (logic thuần, KHÔNG mạng) ─────────────────────────
def selftest() -> int:
    cases = []
    cases.append(("pin_sync", gws_bridge.PINNED_VERSION == "0.22.5"))
    cases.append(("op_group_complete", all(OP_GROUP.get(o) for o in
                  ("files_get", "search", "move", "rename", "register", "manifest"))))
    cases.append(("env_explicit", runtime_env("chat") == "chat" and runtime_env("code") == "code"
                  and runtime_env("cowork") == "cowork"))
    # heuristic KHÔNG trả 'chat' khi không có marker (Cowork không set COWORK vẫn là shell, KHÔNG SKIP)
    _saved = {k: os.environ.pop(k, None) for k in
              ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE", "CLAUDE_COWORK", "COWORK", "TL_RUNTIME_ENV")}
    try:
        _heur_not_chat = runtime_env() in ("code", "cowork")
        _envvar_forces_chat = (os.environ.update({"TL_RUNTIME_ENV": "chat"}) or runtime_env() == "chat")
    finally:
        os.environ.pop("TL_RUNTIME_ENV", None)
        for _k, _v in _saved.items():
            if _v is not None:
                os.environ[_k] = _v
    cases.append(("env_heuristic_never_chat", _heur_not_chat))
    cases.append(("env_var_can_force_chat", _envvar_forces_chat))
    # Chat mặc định = gws PRIMARY (nay chạy được gws trong shell), KHÔNG còn mcp mặc định
    cases.append(("chat_default_gws", _resolve_backend("chat") == "gws" and _BACKEND_BY_ENV["chat"] == "gws"))
    # C chưa confirm → ConfirmRequired (env code, không chạm mạng vì raise trước backend)
    try:
        drive_op("move", env="code", confirmed=False, file_id="x")
        cases.append(("C_confirm_gate", False))
    except ConfirmRequired:
        cases.append(("C_confirm_gate", True))
    except Exception:
        cases.append(("C_confirm_gate", False))
    # ÉP mcp (pure-chat không shell) qua TL_DRIVE_BACKEND=mcp → D defer shell, read defer mcp
    _prev_be = os.environ.get("TL_DRIVE_BACKEND")
    os.environ["TL_DRIVE_BACKEND"] = "mcp"
    try:
        try:
            drive_op("register", env="chat")
            cases.append(("D_mcp_defershell", False))
        except DeferToShell:
            cases.append(("D_mcp_defershell", True))
        except Exception:
            cases.append(("D_mcp_defershell", False))
        try:
            drive_op("files_get", env="chat", file_id="abc")
            cases.append(("mcp_read_defermcp", False))
        except DeferToMCP as e:
            ok = e.spec.get("tool_basename") == "get_file_metadata" and e.spec.get("args", {}).get("fileId") == "abc"
            cases.append(("mcp_read_defermcp", ok))
        except Exception:
            cases.append(("mcp_read_defermcp", False))
    finally:
        if _prev_be is None:
            os.environ.pop("TL_DRIVE_BACKEND", None)
        else:
            os.environ["TL_DRIVE_BACKEND"] = _prev_be
    # mcp spec search dùng 'query'
    try:
        sp = mcp_spec("search", q="title contains 'x'")
        cases.append(("mcp_spec_search", sp.get("args", {}).get("query") == "title contains 'x'"))
    except Exception:
        cases.append(("mcp_spec_search", False))
    # normalize parity-shape khớp giữa gws & mcp
    nf_g = gws_bridge.normalize_file({"id": "1", "name": "a", "size": "5", "md5Checksum": "m", "parents": ["p"]})
    nf_m = mcp_bridge.normalize_file({"id": "1", "name": "a", "size": 5, "md5": "m", "parents": "p"})
    cases.append(("normalize_parity_shape", nf_g == nf_m))
    # run_batch: lô có op C + chưa confirm → ConfirmRequired (chặn TRƯỚC backend, không mạng)
    try:
        run_batch([("rename", {"file_id": "x", "name": "n"}), ("trash", {"file_id": "y"})],
                  env="code", confirmed=False)
        cases.append(("batch_confirm_gate", False))
    except ConfirmRequired:
        cases.append(("batch_confirm_gate", True))
    except Exception:
        cases.append(("batch_confirm_gate", False))

    ok = sum(1 for _, p in cases if p)
    for n, p in cases:
        print(f"  [{'OK' if p else 'FAIL'}] {n}")
    print(f"== transport selftest {ok}/{len(cases)} ==")
    return 0 if ok == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(selftest())
