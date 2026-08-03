#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gws_bridge.py — GĐ1: bọc subprocess `gws` (@googleworkspace/cli, pin) → JSON, cho transport.py.

Vai: backend transport Drive direct-API ở env Code/Cowork (PRIMARY; GAS = FALLBACK qua transport.py).
Cú pháp gws (v0.22): `gws <service> <resource> <method> --params '{JSON}'` (KHÔNG key=value).
Nhóm A (read) hiện thực đầy đủ ở GĐ1; B (write an toàn) / C (write rủi ro) scaffold → GĐ2/GĐ3.
is_available(): PATH + version==pin + auth!=none, cache theo phiên (env TL_GWS_DISABLE=1 → False để test fallback).
Timeout CHỈNH ĐƯỢC bằng env (r327): TL_GWS_AUTH_TIMEOUT · TL_GWS_VERSION_TIMEOUT (đè riêng từng phép dò)
và TL_GWS_TIMEOUT (SÀN chung cho MỌI lệnh gws — chỉ NÂNG, không hạ). Xem `_timeout()`.
BẢO MẬT: KHÔNG in/echo credential — chỉ gọi --version / auth status / drive files.
"""
from __future__ import annotations
import json, os, re, shutil, subprocess
from typing import Any

# Đồng bộ với tl.GWS_PINNED_VERSION (selftest tl đối chiếu khớp). KHÔNG import tl (tránh circular).
PINNED_VERSION = "0.22.5"

_AVAIL_CACHE: dict | None = None
_GET_FIELDS = "id,name,mimeType,size,md5Checksum,parents,trashed,modifiedTime,appProperties"


class GwsError(RuntimeError):
    pass


def gws_exe() -> str | None:
    """Tìm binary gws KHÔNG chỉ dựa PATH: TL_GWS_BIN → PATH → ~/.local/bin → /usr/local/bin.
    Cowork: bootstrap đặt gws ở ~/.local/bin nhưng shell không-login có thể KHÔNG có nó trên PATH →
    tìm trực tiếp để `tl`/gws_bridge dùng được mà KHÔNG cần `export PATH` mỗi lệnh."""
    cand = os.environ.get("TL_GWS_BIN")
    if cand and os.path.exists(cand):
        return cand
    w = shutil.which("gws")
    if w:
        return w
    for p in (os.path.expanduser("~/.local/bin/gws"), os.path.expanduser("~/.local/bin/gws.exe"),
              "/usr/local/bin/gws"):
        if os.path.exists(p):
            return p
    return None


# ───────────────────────── timeout: hằng CỨNG là BỆNH (r327) ─────────────────────────
# `gws auth status` liệt kê 34 API + gọi mạng. ĐO trên máy chuẩn Windows, CÙNG đường mã này:
#   02-08-2026: 29,1 / 39,7 / 50,5 s   ·   03-08-2026: 18,9 / 15,4 / 17,1 s
# ⇒ phí thật DAO ĐỘNG 15–50 s quanh trần CŨ 20 s: phép dò LẬT đỏ/xanh theo mạng, không phải hỏng hẳn —
# nên `gws auth status` chạy tay vẫn ra `oauth2` mà tl lại kết luận "gws chưa sẵn". Hậu quả dây chuyền:
# auth_method()=None → is_available()=False → drive-push rơi xuống gcloud (thiếu Drive scope) ⇒ [FAIL]
# mọi lượt deploy, dù gws hoàn toàn SỐNG. Chẩn đoán cũ «chạy lại là được» SAI vì bệnh phụ thuộc mạng.
# ★Bất đối xứng chi phí: chờ THỪA chỉ tốn giây trong ca ĐÃ hỏng (phép dò cache 1 lần/phiên, và chỉ chạy
#  khi binary gws CÓ THẬT); chờ THIẾU trả lời SAI rồi định tuyến ngầm sang đường chết ⇒ hào phóng có lãi.
def _env_timeout(name: str) -> float | None:
    """Đọc timeout từ env; CHỈ nhận số DƯƠNG HỮU HẠN. Rỗng/rác/≤0/nan/inf ⇒ None → dùng mặc định.
    (0 hay âm truyền vào subprocess.run là timeout TỨC THÌ, inf là treo vô hạn — env méo KHÔNG được
    biến knob "chỉnh cho dễ thở" thành công tắc vô hiệu hoá timeout.)"""
    raw = (os.environ.get(name) or "").strip()
    if not raw:
        return None
    try:
        v = float(raw)
    except ValueError:
        return None
    return v if (v > 0 and v != float("inf")) else None   # nan: mọi so sánh False ⇒ tự rơi về None


def _timeout(default: float, knob: str | None = None) -> float:
    """Timeout hiệu lực = knob RIÊNG (đè hẳn) → TL_GWS_TIMEOUT (SÀN, chỉ NÂNG) → default.
    SÀN chứ KHÔNG phải đè: máy chậm khai TL_GWS_TIMEOUT=120 phải nâng phép dò 30s lên 120s mà KHÔNG
    được hạ download (300s) xuống 120s — hạ trần một cách vô tình chính là cái bẫy đang vá ở đây."""
    if knob:
        v = _env_timeout(knob)
        if v is not None:
            return v
    floor = _env_timeout("TL_GWS_TIMEOUT")
    return max(default, floor) if floor is not None else default


def _run(args: list[str], *, timeout: float = 30.0, cwd: str | None = None,
         knob: str | None = None) -> str:
    """Chạy `gws <args>` → stdout. gws thiếu / rc!=0 / timeout → GwsError (transport sẽ fallback GAS).
    cwd: gws giới hạn --output PHẢI trong thư mục làm việc → export đặt cwd=thư mục tạm + tên file tương đối.
    knob: tên env đè timeout cho RIÊNG lệnh này (phép dò); mọi lệnh đều ăn SÀN TL_GWS_TIMEOUT."""
    timeout = _timeout(timeout, knob)   # giải ở ĐÚNG MỘT chỗ ⇒ thông điệp lỗi khai timeout THẬT đã dùng
    exe = gws_exe()
    if not exe:
        raise GwsError("gws not found (PATH / ~/.local/bin)")
    try:
        p = subprocess.run([exe, *args], capture_output=True, text=True, cwd=cwd,
                           timeout=timeout, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired as e:
        raise GwsError(f"gws timeout sau {timeout}s") from e
    if p.returncode != 0:
        # A6/P7: bỏ dòng nhiễu 'Using keyring backend: …' khỏi thông điệp lỗi (đỡ rò ra [FALLBACK→GAS] của transport).
        _err = "\n".join(ln for ln in (p.stderr or p.stdout or "").splitlines()
                         if "using keyring backend" not in ln.lower()).strip()
        raise GwsError(f"gws rc={p.returncode}: {_err[:300]}")
    return p.stdout or ""


def _json(out: str):
    """Parse JSON; bỏ qua preamble không-JSON (vd 'Using keyring backend: ...' nếu lọt stdout)."""
    out = (out or "").strip()
    if not out:
        return {}
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        idxs = [i for i in (out.find("{"), out.find("[")) if i >= 0]
        if idxs:
            return json.loads(out[min(idxs):])
        raise


def _drive(method: list[str], params: dict, *, timeout: float = 30.0):
    args = [*method, "--params", json.dumps(params, ensure_ascii=False), "--format", "json"]
    return _json(_run(args, timeout=timeout))


# ───────────────────────── availability ─────────────────────────
def version() -> str:
    # 30s: bù gws cold-start (keyring/kết nối lần đầu phiên). ĐO 03-08-2026 (lệnh gws ĐẦU của tiến trình,
    # tức ĐÃ gánh cold-start): 3,7s ⇒ dư 8× — giữ nguyên mặc định, chỉ thêm knob (r327).
    out = _run(["--version"], timeout=30.0, knob="TL_GWS_VERSION_TIMEOUT")
    m = re.search(r"(\d+\.\d+\.\d+)", out)
    if m:
        return m.group(1)
    lines = out.strip().splitlines()
    return lines[0] if lines else ""


def _auth_probe() -> tuple[str | None, str]:
    """(auth_method, err) — 120s vì phí ĐO được là 15–50s (xem khối ghi chú timeout ở trên): trần cũ 20s
    nằm GIỮA vùng dao động nên phép dò lật đỏ/xanh theo mạng. 120s ≈ 2,4× ca chậm nhất từng đo.
    Tách khỏi auth_method() để is_available() KHAI ĐƯỢC LÝ DO hỏng: bệnh này sống lâu vì lỗi bị NUỐT —
    probe-timeout và «chưa auth bao giờ» CÙNG trả None, availability_detail() không phân biệt nổi, nên
    người vận hành đọc `auth=None` rồi đi `gws auth login` (sai hướng, không phải lỗi quyền)."""
    try:
        st = _json(_run(["auth", "status"], timeout=120.0, knob="TL_GWS_AUTH_TIMEOUT"))
    except GwsError as e:
        return None, str(e)
    return (st.get("auth_method") if isinstance(st, dict) else None), ""


def auth_method() -> str | None:
    return _auth_probe()[0]


def is_available(force: bool = False) -> bool:
    """True ⇔ gws trên PATH + version==pin + đã auth. Cache phiên; TL_GWS_DISABLE=1 ⇒ False (test fallback)."""
    global _AVAIL_CACHE
    if os.environ.get("TL_GWS_DISABLE") == "1":
        return False
    if _AVAIL_CACHE is not None and not force:
        return bool(_AVAIL_CACHE["ok"])
    info: dict[str, Any] = {"ok": False, "version": None, "version_match": False, "auth_method": None,
                            "probe_error": ""}   # r327: KHAI lý do — "không dò được" ≠ "dò xong, chưa auth"
    try:
        info["version"] = version()
        info["version_match"] = (info["version"] == PINNED_VERSION)
        info["auth_method"], info["probe_error"] = _auth_probe()
        info["ok"] = bool(info["version_match"] and info["auth_method"] and info["auth_method"] != "none")
    except GwsError as e:
        info["ok"] = False
        info["probe_error"] = str(e)    # version() ném ⇒ auth chưa kịp chạy; giữ lỗi ĐẦU TIÊN gặp
    _AVAIL_CACHE = info
    return bool(info["ok"])


def availability_detail(force: bool = False) -> dict:
    is_available(force=force)
    return dict(_AVAIL_CACHE or {})


def reset_cache() -> None:
    global _AVAIL_CACHE
    _AVAIL_CACHE = None


# ───────────────────────── chuẩn hoá ─────────────────────────
def normalize_file(f: dict) -> dict:
    """Field cốt lõi để ĐỐI CHỨNG parity 3-backend (gws ≡ MCP ≡ GAS). size→str (gws trả chuỗi)."""
    f = f or {}
    size = f.get("size")
    return {
        "id": f.get("id"),
        "name": f.get("name"),
        "mimeType": f.get("mimeType"),
        "size": str(size) if size is not None else None,
        "md5": f.get("md5Checksum") or f.get("md5"),
        "parents": list(f.get("parents") or []),
        "trashed": bool(f.get("trashed")),
        "modifiedTime": f.get("modifiedTime"),
    }


# ───────────────────────── Nhóm A: READ (GĐ1) ─────────────────────────
def files_get(file_id: str, fields: str = _GET_FIELDS, **_) -> dict:
    """get-meta — đối xứng GAS doInfo_ (action 'info'). Trả {ok, file: <normalize>}."""
    f = _drive(["drive", "files", "get"],
               {"fileId": file_id, "fields": fields, "supportsAllDrives": True})
    return {"ok": True, "file": normalize_file(f)}


def files_list(q: str, fields: str = "id,name,mimeType,parents,trashed",
               page_size: int = 100, **_) -> dict:
    """Drive files.list theo query nguyên bản (name contains/fullText/parents…)."""
    r = _drive(["drive", "files", "list"],
               {"q": q, "fields": "nextPageToken,files(" + fields + ")", "pageSize": page_size,
                "supportsAllDrives": True, "includeItemsFromAllDrives": True})
    files = r.get("files", []) if isinstance(r, dict) else []
    return {"ok": True, "count": len(files),
            "files": [normalize_file(x) for x in files],
            "nextPageToken": r.get("nextPageToken", "") if isinstance(r, dict) else ""}


# ───────────────────────── Nhóm A: READ GDoc (GĐ2) ─────────────────────────
def _slice_text(file_id: str, mime: str, text: str, offset: int = 0, limit: int | None = None) -> dict:
    """Lát cắt đối xứng GAS readSlice_ (stripBom; default 60000, hardMax 200000) → parity với action 'read'."""
    text = (text or "").lstrip("﻿")
    DFLT, HARDMAX = 60000, 200000
    off = max(0, int(offset or 0))
    lim = int(limit) if limit else DFLT
    lim = max(1, min(lim, HARDMAX))
    chunk = text[off:off + lim]
    return {"ok": True, "id": file_id, "mime": mime, "total": len(text),
            "offset": off, "returned": len(chunk), "more": off + len(chunk) < len(text), "text": chunk}


def read_text(file_id: str, mime: str = "text/plain", offset: int = 0, limit: int | None = None, **_) -> dict:
    """Đọc text GDoc/Sheet/Slide qua `gws drive files export` (binary→file tạm→đọc). Đối xứng GAS doRead_."""
    import tempfile
    from pathlib import Path as _P
    d = tempfile.mkdtemp(prefix="gwsexp_")
    try:
        # gws giới hạn --output trong cwd → chạy gws với cwd=d và tên file tương đối.
        _run(["drive", "files", "export",
              "--params", json.dumps({"fileId": file_id, "mimeType": mime}),
              "--output", "export.bin"], timeout=90.0, cwd=d)
        data = (_P(d) / "export.bin").read_text(encoding="utf-8", errors="replace")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return _slice_text(file_id, mime, data, offset, limit)


# ───────────────────────── Nhóm B: WRITE an toàn (GĐ2) ─────────────────────────
def upload(name: str, path: str, parents=None, mime: str | None = None,
           convert_to: str | None = None, **_) -> dict:
    """Tải file local → Drive (vd _HOP_NAP). convert_to='application/vnd.google-apps.document' để
    docx→GDoc ngay khi upload. (GAS webapp KHÔNG nhận binary local → đây là năng lực gws/MCP.)"""
    body: dict[str, Any] = {"name": name}
    if parents:
        body["parents"] = list(parents)
    if convert_to:
        body["mimeType"] = convert_to
    # gws giới hạn --upload PHẢI trong cwd → chạy gws với cwd=thư mục file + tên tương đối.
    ap = os.path.abspath(path)
    updir, upbase = os.path.dirname(ap), os.path.basename(ap)
    args = ["drive", "files", "create",
            "--json", json.dumps(body, ensure_ascii=False),
            "--params", json.dumps({"supportsAllDrives": True}),
            "--upload", upbase, "--format", "json"]
    if mime:
        args += ["--upload-content-type", mime]
    f = _json(_run(args, timeout=180.0, cwd=updir))
    return {"ok": True, "file": normalize_file(f)}


def download(file_id: str, dest: str, export_mime: str | None = None, **_) -> dict:
    """Tải NỘI DUNG file Drive → đĩa (streaming, KHÔNG base64, KHÔNG vào context, KHÔNG cap 9MB).
    File thường: `files get alt=media`. Google-native (Doc/Sheet/Slide): `files export` + export_mime.
    Nhanh nhất cho download — 1 hop googleapis trực tiếp."""
    exe = gws_exe()
    if not exe:
        raise GwsError("gws not found (PATH / ~/.local/bin)")
    ap = os.path.abspath(dest)
    ddir, dbase = os.path.dirname(ap), os.path.basename(ap)  # gws giới hạn --output trong cwd
    if export_mime:
        args = [exe, "drive", "files", "export",
                "--params", json.dumps({"fileId": file_id, "mimeType": export_mime}), "--output", dbase]
    else:
        args = [exe, "drive", "files", "get",
                "--params", json.dumps({"fileId": file_id, "alt": "media", "supportsAllDrives": True}),
                "--output", dbase]
    try:
        # KHÔNG đi qua _run (stdout phải là BYTES, không decode) ⇒ gọi _timeout() TAY, nếu không đây là
        # lệnh gws DUY NHẤT mà SÀN TL_GWS_TIMEOUT không với tới (r327).
        p = subprocess.run(args, cwd=ddir, capture_output=True, timeout=_timeout(300.0))
    except subprocess.TimeoutExpired as e:
        raise GwsError("gws download timeout") from e
    if p.returncode != 0:
        raise GwsError(f"gws download rc={p.returncode}: {(p.stderr or b'').decode('utf-8', 'replace')[:300]}")
    outfile = os.path.join(ddir, dbase)
    if os.path.exists(outfile) and os.path.getsize(outfile) > 0:   # binary → gws ghi raw vào --output (byte-exact)
        if os.path.abspath(outfile) != ap:
            shutil.move(outfile, ap)
        return {"ok": True, "path": ap, "bytes": os.path.getsize(ap)}
    # text/JSON: gws KHÔNG ghi --output, lại REFORMAT khi in stdout (đổi thứ tự key JSON) → KHÔNG raw.
    # Raise để transport FALLBACK→GAS (download b64 = raw byte-exact). export_mime (GDoc export) cũng vào đây.
    raise GwsError("gws download không cho raw text/JSON (reformat) → fallback GAS để byte-exact")


def update_content(file_id: str, path: str, mime: str | None = None, **_) -> dict:
    """Thay NỘI DUNG file Drive sẵn (giữ nguyên fileId) — cho xoay vòng secrets tại chỗ.
    `files update --params {fileId} --upload <path>`."""
    ap = os.path.abspath(path)
    updir, upbase = os.path.dirname(ap), os.path.basename(ap)
    args = ["drive", "files", "update",
            "--params", json.dumps({"fileId": file_id, "supportsAllDrives": True}),
            "--upload", upbase, "--format", "json"]
    if mime:
        args += ["--upload-content-type", mime]
    f = _json(_run(args, timeout=120.0, cwd=updir))
    return {"ok": True, "file": normalize_file(f)}


def copy_convert(file_id: str, name: str | None = None, parents=None, **_) -> dict:
    """Convert file Drive sẵn (docx/doc) → Google Doc server-side (đối xứng GAS doCopyConvert_).
    `files copy` với target mimeType=google-apps.document."""
    body: dict[str, Any] = {"mimeType": "application/vnd.google-apps.document"}
    if name:
        body["name"] = name
    if parents:
        body["parents"] = list(parents)
    f = _json(_run(["drive", "files", "copy",
                    "--params", json.dumps({"fileId": file_id, "supportsAllDrives": True}),
                    "--json", json.dumps(body, ensure_ascii=False), "--format", "json"], timeout=180.0))
    return {"ok": True, "file": normalize_file(f)}


def delete(file_id: str, **_) -> dict:
    """Tiện ích dọn artifact TEST (hard-delete vĩnh viễn). Vận hành thật dùng `trash` (nhóm C, có confirm)."""
    _run(["drive", "files", "delete",
          "--params", json.dumps({"fileId": file_id, "supportsAllDrives": True})], timeout=30.0)
    return {"ok": True, "deleted": file_id}


def mkdir(name: str, parents=None, **_) -> dict:
    """Tạo folder Drive (nhóm B). parents=[folderId] để đặt trong cây đích."""
    body: dict[str, Any] = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parents:
        body["parents"] = list(parents)
    f = _json(_run(["drive", "files", "create",
                    "--json", json.dumps(body, ensure_ascii=False),
                    "--params", json.dumps({"supportsAllDrives": True}), "--format", "json"], timeout=60.0))
    return {"ok": True, "file": normalize_file(f)}


# ───────────────────────── Nhóm C: WRITE rủi ro (GĐ3) ─────────────────────────
def _files_update(file_id: str, body: dict | None = None, params_extra: dict | None = None,
                  fields: str = "id,name,parents,trashed", timeout: float = 60.0) -> dict:
    params = {"fileId": file_id, "supportsAllDrives": True, "fields": fields}
    if params_extra:
        params.update(params_extra)
    return _json(_run(["drive", "files", "update",
                       "--params", json.dumps(params, ensure_ascii=False),
                       "--json", json.dumps(body or {}, ensure_ascii=False), "--format", "json"], timeout=timeout))


def move(file_id: str, to_folder: str, **_) -> dict:
    """2-BƯỚC (gws KHÔNG tự removeParents): files get fields=parents → update addParents/removeParents.
    Đối xứng GAS doMove_ (loại to_folder khỏi removeParents để idempotent)."""
    cur = _drive(["drive", "files", "get"],
                 {"fileId": file_id, "fields": "parents", "supportsAllDrives": True})
    parents = list((cur or {}).get("parents") or [])
    remove = ",".join(p for p in parents if p != to_folder)
    f = _files_update(file_id, body={},
                      params_extra={"addParents": to_folder, "removeParents": remove})
    return {"ok": True, "fileId": file_id, "toFolderId": to_folder,
            "removedFrom": remove, "file": normalize_file(f)}


def rename(file_id: str, name: str, **_) -> dict:
    # name PHẢI ở --json body (đã đúng trong _files_update); ASSERT chống NUỐT LỖI IM LẶNG:
    # gws/API có thể trả 200 nhưng KHÔNG đổi tên (vd name lọt --params, lệch pin) → đọc lại name trong
    # response (fields=...,name,...) và đối chiếu; lệch ⇒ raise RÕ thay vì báo ok giả.
    f = _files_update(file_id, body={"name": name})
    got = (f or {}).get("name")
    if got != name:
        raise GwsError(
            f"rename KHÔNG hiệu lực (gws trả 200 nhưng tên KHÔNG đổi): yêu cầu={name!r} nhận={got!r} "
            f"fileId={file_id}. Kiểm tra: name PHẢI ở --json body (KHÔNG phải --params/requestBody) "
            f"+ gws version == pin {PINNED_VERSION}.")
    return {"ok": True, "fileId": file_id, "file": normalize_file(f)}


def trash(file_id: str, **_) -> dict:
    f = _files_update(file_id, body={"trashed": True})
    return {"ok": True, "fileId": file_id, "trashed": True, "file": normalize_file(f)}


def restore(file_id: str, **_) -> dict:
    f = _files_update(file_id, body={"trashed": False})
    return {"ok": True, "fileId": file_id, "trashed": False, "file": normalize_file(f)}


_DISPATCH = {
    "files_get": files_get,
    "files_list": files_list,
    "search": files_list,
    "read": read_text,
    "download": download,
    "upload": upload,
    "copy_convert": copy_convert,
    "mkdir": mkdir,
    "move": move,
    "rename": rename,
    "trash": trash,
    "restore": restore,
}


def call(op: str, **kw):
    fn = _DISPATCH.get(op)
    if fn is None:
        raise GwsError(f"gws_bridge: op chưa hỗ trợ: {op}")
    return fn(**kw)
