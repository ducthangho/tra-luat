# -*- coding: utf-8 -*-
"""tl_core.profile_env — I9a (v1.34.13): hạ tầng CONFIG/CREDS/PROFILE-ENV/webapp-GAS/transport tách NGUYÊN VĂN từ tl.py. Đổi-luật-có-kiểm-soát đã grill; tl giữ stub; bind REBASE __globals__."""
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
    """REBASE __globals__ từng hàm đã chuyển về namespace SỐNG của tl (khuôn I1-I8)."""
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



def _read_json_file(path: str | None) -> dict:
    if not path:
        return {}
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return {}


def _config_candidates(config_path: str | None = None) -> list[str]:
    cands = [config_path] if config_path else []
    # B1: nhận file Context tên `tra_luat_config.v2.json`/`tra_luat_config.json` ở cwd / gốc skill / scripts/
    # → khởi động TRẦN (không --config) tự thấy config, không gãy "Thiếu TL_WEBAPP/TL_TOKEN".
    for d in (Path.cwd(), HERE.parent, HERE):
        for n in ("tra_luat_config.v2.json", "tra_luat_config.json"):
            cands.append(str(d / n))
    cands += [str(Path.home() / ".tra_luat_config.json"), "/tmp/tra_luat_config.json"]
    seen, out = set(), []
    for p in cands:                                  # khử trùng, giữ thứ tự ưu tiên
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return out


def _profiles_from_config(cfg: dict) -> dict:
    profiles = cfg.get("profiles") if isinstance(cfg.get("profiles"), dict) else {}
    if profiles:
        return profiles
    return {
        DEFAULT_PROFILE: {
            "rootFolderId": cfg.get("rootFolderId") or cfg.get("root_id") or cfg.get("root"),
            "notebookId": cfg.get("notebookId") or cfg.get("notebookVbqpplId") or cfg.get("nlmNotebookId"),
            "registryDocId": cfg.get("registryDocId"),
            "manifestId": cfg.get("manifestId") or cfg.get("TL_MANIFEST_ID"),
            "categories": cfg.get("categories"),
        }
    }


def _profile_lookup(profiles: dict, name: str) -> tuple[str, dict | None]:
    """(v1.33.48 — rà Instruction profile 'Luật BHXH'): tra profile CHỊU-LỖI-GÕ — exact trước; miss → so khớp
    KHÔNG-dấu/không-hoa-thường/gộp space-_- ('Luat BHXH'/'luật bhxh'/'luat_bhxh' → 'Luật BHXH') khi DUY NHẤT
    1 ứng viên (≥2 ứng viên mờ → không đoán). Trả (tên CANONICAL trong config, prof|None) — canonical để
    TL_PROFILE/cache-dir/registry scope nhất quán 1 tên."""
    if name in profiles:
        return name, profiles[name]

    def _k(s: str) -> str:
        return re.sub(r"[\s_\-]+", " ", _strip_accents(str(s or "")).lower()).strip()
    want = _k(name)
    cands = [k for k in profiles if _k(k) == want] if want else []
    if len(cands) == 1:
        return cands[0], profiles[cands[0]]
    return name, None


def _apply_profile_env(cfg: dict, profile: str | None = None) -> dict:
    profiles = _profiles_from_config(cfg)
    name0 = _selected_profile_name(profile, cfg)
    name, _hit = _profile_lookup(profiles, name0)
    # v1.33.48 (rà Instruction 'Luật BHXH'): profile ĐƯỢC YÊU CẦU TƯỜNG MINH mà KHÔNG có trong config → KHÔNG
    # rơi ÂM THẦM về scope NỀN vbqppl nữa (trước: prof=fallback DEFAULT → TL_REGISTRY_DOC_ID/TL_NOTEBOOK_ID trỏ
    # VBQPPL base trong khi TL_PROFILE=tên-dự-án → ghi/push NHẦM corpus nền, đúng lớp sự cố 1.23.21 mà
    # _resolve_nlm_notebook/NO_NOTEBOOK_ID không bắt được vì env ĐÃ bị điền từ nền). Nay: scope RỖNG + cảnh báo
    # LOUD → guard hạ nguồn tự chặn (NO_NOTEBOOK_ID, PROFILE_CATEGORIES_OWN_REQUIRED, registry-id-empty blocker).
    if _hit is None and name0 != DEFAULT_PROFILE:
        prof = {}
        print(f"[tl] ⚠ PROFILE_NOT_FOUND: '{name0}' không có trong config.profiles ({', '.join(sorted(profiles)) or '∅'}) "
              f"— KHÔNG dùng scope nền thay thế. Kiểm chính tả (nhận cả gõ không dấu nếu khớp DUY NHẤT) hoặc thêm "
              f"block profiles vào config (xem SKILL.md corpus_profile).", file=sys.stderr)
    else:
        prof = _hit or profiles.get(DEFAULT_PROFILE) or {}
    os.environ["TL_PROFILE"] = name
    mapping = {
        "rootFolderId": "TL_ROOT_FOLDER_ID",
        "metaFolderId": "TL_META_FOLDER_ID",
        "notebookId": "TL_NOTEBOOK_ID",
        "registryDocId": "TL_REGISTRY_DOC_ID",
        "manifestId": "TL_MANIFEST_ID",
        "overflowNotebookId": "TL_OVERFLOW_NOTEBOOK_ID",   # Option 1: đích overflow khi notebook đầy
    }
    # Xóa overlay profile trước đó để chuyển profile trong cùng process không bị dính scope cũ.
    for dst in tuple(mapping.values()) + ("TL_CATEGORIES_MODE", "TL_MANIFEST_SCOPE", "TL_BASE_ALSO"):
        os.environ.pop(dst, None)
    for src, dst in mapping.items():
        val = prof.get(src)
        if val:
            os.environ[dst] = str(val)
    categories = prof.get("categories")
    if isinstance(categories, str):
        os.environ["TL_CATEGORIES_MODE"] = categories.strip().lower()
    elif isinstance(categories, dict):
        os.environ["TL_CATEGORIES_MODE"] = "own"
    manifest_scope = str(prof.get("manifestScope") or "").strip().lower()
    if manifest_scope:
        os.environ["TL_MANIFEST_SCOPE"] = manifest_scope
    # v1.30.0 (A — profile CỘNG VBQPPL): profile DỰ ÁN mặc định TL_BASE_ALSO=1 — các lệnh ĐỌC (locate/reg-query/
    # source-map/exists/nlm-cross) quét THÊM nền VBQPPL+shards, hit profile ưu tiên (doctrine MULTI_CORPUS_V1_18 §2
    # nay vào CLI, không chỉ Instruction). Opt-out: config.profiles.<p>.baseAlso=false hoặc --no-base-also per-lệnh.
    # vbqppl nền: KHÔNG set (không tự quét chính mình 2 lần). GHI/ingest KHÔNG đụng cờ này (scope profile giữ nguyên).
    # Review v1.30.0 (CONFIRMED): CHỈ set khi profile THẬT có trong config — tên KHÔNG tồn tại rơi về data NỀN
    # (prof=fallback vbqppl ở trên) mà vẫn set cờ ⇒ nền tự quét mình 2 lần (vô hại nhờ dedup drive_id nhưng tốn IO + sai doctrine).
    if name != DEFAULT_PROFILE and profiles.get(name):
        os.environ["TL_BASE_ALSO"] = "0" if prof.get("baseAlso") is False else "1"
    return {"profile": name, "profile_found": bool(profiles.get(name)), "profile_data": prof, "profiles": sorted(profiles)}


def _active_profile() -> str:
    return os.environ.get("TL_PROFILE") or DEFAULT_PROFILE


def _resolve_nlm_notebook(explicit: str | None = None) -> tuple[str, str | None]:
    """Group B (log rà): notebook đích cho thao tác NLM theo PROFILE ĐANG DÙNG. Thứ tự: explicit > TL_NOTEBOOK_ID
    (do profile set). Profile MẶC ĐỊNH (vbqppl) thiếu → NLM_BASE_NOTEBOOK. Profile DỰ ÁN thiếu notebookId → KHÔNG
    fallback base (tránh ĐẨY NHẦM corpus dự án vào VBQPPL) → trả ('', NO_NOTEBOOK_ID error). Trả (notebook, err|None)."""
    nb = (str(explicit or "").strip()) or (os.environ.get("TL_NOTEBOOK_ID") or "").strip()
    # E1 (v1.33.10 — log: `tl nlm-get vbqppl` → NLM API NOT_FOUND): nhận TÊN PROFILE quen thay UUID —
    # 'vbqppl'/'base'/tên profile mặc định map về notebook nền; UUID/tên lạ giữ nguyên (shard tự chịu).
    if nb and nb.lower() in ("vbqppl", "base", str(DEFAULT_PROFILE).lower()):
        return NLM_BASE_NOTEBOOK, None
    if nb:
        return nb, None
    if _active_profile() == DEFAULT_PROFILE:
        return NLM_BASE_NOTEBOOK, None
    return "", (f"NO_NOTEBOOK_ID: profile '{_active_profile()}' chưa có notebookId "
                f"(config.profiles.<p>.notebookId) — truyền --notebook-id hoặc bổ sung config; "
                f"KHÔNG tự đẩy về VBQPPL base (tránh nhầm đích).")


def _profile_policy_error(require_registry: bool = True, require_manifest: bool = False,
                          forbid_inherit: bool = True) -> dict | None:
    """Invariant cho profile dự án: own tree + own registry Sheet/manifest. Trả dict lỗi hoặc None."""
    profile = _active_profile()
    if profile == DEFAULT_PROFILE:
        return None
    categories = os.environ.get("TL_CATEGORIES_MODE", "").strip().lower()
    if forbid_inherit and categories == "inherit":
        return {
            "ok": False,
            "error": "PROFILE_CATEGORIES_INHERIT_FORBIDDEN",
            "profile": profile,
            "categories": categories,
            "required": "config.profiles.<p>.categories='own' và manifestScope='own'",
            "note": "Profile dự án phải sở hữu cây riêng; inherit chỉ còn là cấu hình legacy, không dùng cho ghi/quét.",
        }
    if forbid_inherit and categories != "own":
        return {
            "ok": False,
            "error": "PROFILE_CATEGORIES_OWN_REQUIRED",
            "profile": profile,
            "categories": categories or None,
            "required": "config.profiles.<p>.categories='own'",
            "note": "Profile dự án phải khai báo categories='own' để không rơi về cây VBQPPL.",
        }
    reg = os.environ.get("TL_REGISTRY_DOC_ID", "").strip()
    man = os.environ.get("TL_MANIFEST_ID", "").strip()
    if require_registry and not reg:
        return {
            "ok": False,
            "error": "PROFILE_REGISTRY_ID_REQUIRED",
            "profile": profile,
            "required": "registryDocId trỏ tới Google Sheet registry riêng",
            "note": "Chạy `tl profile-create --name <p> --notebook <nb> --apply` hoặc tạo Sheet registry riêng trước.",
        }
    if require_manifest and not man:
        return {
            "ok": False,
            "error": "PROFILE_MANIFEST_ID_REQUIRED",
            "profile": profile,
            "required": "manifestId trỏ tới JSON manifest riêng",
        }
    return None


def _emit_profile_policy_error(err: dict, json_mode: bool = False) -> int:
    msg = json.dumps(err, ensure_ascii=False, indent=2) if json_mode else f"✗ {err.get('error')}: {err.get('note') or err.get('required')}"
    print(msg, file=sys.stderr)
    return 2


def _profile_cache_dir() -> Path:
    prof = _active_profile()
    return CACHE if prof == DEFAULT_PROFILE else CACHE / prof


def load_creds(config_path: str | None = None, profile: str | None = None) -> None:
    """Đặt TL_WEBAPP/TL_TOKEN + profile corpus vào env TRƯỚC khi import gas.
    ENV (TL_WEBAPP+TL_TOKEN) ĐỦ để chạy — KHÔNG bắt buộc file config, KỂ CẢ khi có --profile (§9): scope chi tiết
    lấy qua TL_REGISTRY_DOC_ID/TL_MANIFEST_ID/… (env) hoặc config mặc định nếu tình cờ có."""
    if os.environ.get("TL_WEBAPP") and os.environ.get("TL_TOKEN") and not config_path:
        if profile:
            os.environ.setdefault("TL_PROFILE", profile)
            for p in _config_candidates(None):            # best-effort áp scope từ config mặc định nếu có
                if p and Path(p).exists():
                    cfg = _read_json_file(p)
                    if cfg:
                        _apply_profile_env(cfg, profile)
                        break
        return
    for p in _config_candidates(config_path):
        if p and Path(p).exists():
            cfg = _read_json_file(p)
            if not cfg:
                continue
            url = cfg.get("webappUrl") or cfg.get("TL_WEBAPP") or cfg.get("webapp")
            tok = cfg.get("token") or cfg.get("TL_TOKEN")
            if url and tok:
                os.environ["TL_WEBAPP"], os.environ["TL_TOKEN"] = url, tok
                _apply_profile_env(cfg, profile)
                return
    sys.exit(
        "[tl] Thiếu TL_WEBAPP/TL_TOKEN — KHÔI PHỤC (chọn 1, ƯU TIÊN trên xuống):\n"
        f"  • ★ Config v2 nay PUBLIC ở Package → `tl init-config --from-public` (curl drive.usercontent, KHÔNG cần Drive MCP/token).\n"
        "    Hoặc 1 lệnh đủ: `sh scripts/tl_fetch.sh --setup --nlm`.\n"
        f"  • KHÔNG mạng tới Drive → tải fileId {CONFIG_FILEID} qua Drive MCP → /tmp/cfg.json → `tl init-config --file /tmp/cfg.json`.\n"
        f"  • CÓ TL_MASTER_KEY → `tl bootstrap --env cowork --secrets-file <s.enc>` (đủ token+gws+nlm; secrets {SECRETS_FILEID} cũng public Package).\n"
        f"  • Đã có gws cred → `tl init-config --from-drive` (direct-media tự tải).\n"
        "  • Hoặc export TL_WEBAPP/TL_TOKEN, hoặc đặt tra_luat_config.v2.json cạnh skill.\n"
        f"  ↳ SAU khi có token — BẬT gws/direct-media: `tl gws-auth-load` (tải gws cred {GWS_CRED_FILEID} public + giải mã bằng token).\n"
        "  ↳ Rồi `tl doctor --offline` xác nhận nlm CLI + gws; thiếu nlm → `tl nlm-install --uv` → `tl nlm-auth-load`.")


def apply_profile_offline(config_path: str | None = None, profile: str | None = None) -> None:
    """Apply TL_PROFILE/cache scope without requiring webapp credentials."""
    for p in _config_candidates(config_path):
        if p and Path(p).exists():
            cfg = _read_json_file(p)
            if cfg:
                _apply_profile_env(cfg, profile)
                return
    if profile:
        os.environ["TL_PROFILE"] = profile


def _gas():
    """gas.py bản thật (scripts/ gốc) NẾU có → _fallback/gas.py → cuối cùng client nội built-in.
    v1.19: bọc _ScopedGas để forward registryDocId/manifestId theo profile + đo thời gian."""
    try:
        inner = _imp("gas")
    except ModuleNotFoundError:
        if not getattr(_gas, "_warned", False):
            print("[tl] (overlay) không thấy gas.py (kể cả _fallback) — dùng client built-in nội bộ.",
                  file=sys.stderr)
            _gas._warned = True
        inner = _BuiltinGas()
    return _ScopedGas(inner)


def _gws_nlm_note(st: dict) -> str:
    parts = []
    if st.get("gws_cred") is not None:
        parts.append("gws cred ✓ (direct-media)" if st["gws_cred"] else "gws cred chưa nạp")
    if st.get("gws_binary") is not None:
        parts.append("binary ✓" if st["gws_binary"] else "binary lỗi (find/ghi vẫn GAS)")
    if st.get("nlm") is not None:
        if st.get("nlm_partial"):
            parts.append("nlm PARTIAL — chạy tiếp `tl nlm-install --resume`")
        else:
            parts.append(("nlm ✓" if st["nlm"] else "nlm install lỗi") + (" auth✓" if st.get("nlm_auth") else ""))
    return (" · " + " · ".join(parts)) if parts else ""


def _strip_goc_token(text) -> str:
    """Bỏ phần đuôi sau token 'goc'/'_goc-' trong tên file VBHN (vd 'Luat_PPP_goc_64-2020-QH14'
    → 'Luat_PPP'). Năm trong token goc là năm BẢN GỐC được hợp nhất, KHÔNG phải năm ban hành VBHN."""
    return _GOC_TAIL_RE.sub("", str(text or ""))


def _token_set(s: str) -> set[str]:
    text = _strip_accents(_expand_abbrev(s)).lower()
    toks = re.findall(r"[a-z0-9]{3,}", text)
    return {t for t in toks if t not in _STOP_TOKENS and not t.isdigit()}


def _ref_tokens(s) -> set[str]:
    text = _strip_accents(json.dumps(s, ensure_ascii=False) if isinstance(s, (dict, list, tuple)) else str(s or "")).upper()
    pats = re.findall(r"\b\d{1,5}[-/]\d{4}[-/][A-Z0-9-]+\b|\b\d{1,5}[-/]LCT[-/]HDNN\d+\b|\b\d{1,5}[-/](?:\d{1,5}[-/])?VBHN[-/][A-Z0-9D]{2,20}\b|\b\d{1,5}[-/](?:VBHN-)?[A-Z0-9]{2,12}\b", text)
    return {norm_sohieu(x) for x in pats}


def _gas_get_retry(g, action: str, _retries: int = 2, _backoff: float = 1.5, **kw) -> dict:
    """v1.29.4 (i5): GET action ĐỌC idempotent với RETRY backoff — CHỈ retry khi lỗi TRANSIENT (timeout/URLError/
    'Response không phải JSON' = webapp trả trang lỗi tạm). KHÔNG dùng cho action mutate (retry mù = at-least-once,
    nguy hiểm với createtext/copy_convert). Gốc sự cố: sau bust-cache, lệnh kế rebuild manifest đúng lúc webapp
    chậm → 1 lỗi transient = PARSEERR/timeout hàng loạt, phải boot --refresh tay."""
    import time as _t
    r = {}
    for _i in range(_retries + 1):
        r = g.get(action, **kw)
        if not (isinstance(r, dict) and r.get("ok") is False):
            return r
        _msg = str(r.get("error") or "")
        if not any(s in _msg for s in ("TimeoutError", "timed out", "URLError", "RemoteDisconnected",
                                       "ConnectionReset", "IncompleteRead", "Response không phải JSON", "HTTPError: 5")):
            return r          # lỗi THẬT từ webapp (JSON ok:false) → không retry
        if _i < _retries:
            print(f"[gas-retry] {action}: lỗi transient ({_msg[:60]}…) → thử lại {_i + 1}/{_retries} sau {_backoff * (_i + 1):.1f}s",
                  file=sys.stderr, flush=True)
            _t.sleep(_backoff * (_i + 1))
    return r


def _download_link_rank(url: str) -> tuple[int, str]:
    u = (url or "").lower()
    if "thuvienphapluat.vn" in u:
        return (1, "thuvienphapluat.vn")
    if "luatvietnam.vn" in u:
        return (2, "luatvietnam.vn")
    if "congbao.chinhphu.vn" in u:
        return (3, "congbao.chinhphu.vn")
    if "vbpl.vn" in u or "vanban.chinhphu.vn" in u or ".gov.vn" in u or ".chinhphu.vn" in u:
        return (4, "official_other")
    return (5, "other")


def _download_link_plan(urls: list[str]) -> list[dict]:
    rows = []
    for u in urls:
        rank, source = _download_link_rank(u)
        rows.append({"url": u, "rank": rank, "source": source})
    rows.sort(key=lambda x: (x["rank"], x["url"]))
    return rows


def _persist_profile_config(config_path: str | None, name: str, prof: dict) -> str | None:
    """A1 (log rà): GHI BỀN config.profiles.<name> vào file config (MERGE — giữ profile khác + field cũ) →
    `tl profile-info`/`--profile <name>` resolve ĐÚNG thay vì fallback VBQPPL. Trả path đã ghi, None nếu không ghi được."""
    cands = [Path(config_path)] if config_path else [Path.home() / ".tra_luat_config.json", Path("/tmp/tra_luat_config.json")]
    target = next((p for p in cands if p and p.exists()), None) or (Path(config_path) if config_path else None)
    if target is None:
        return None
    try:
        data = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
        if not isinstance(data, dict):
            return None
        profs = data.get("profiles") if isinstance(data.get("profiles"), dict) else {}
        cur = profs.get(name) if isinstance(profs.get(name), dict) else {}
        _before = dict(cur)                                 # snapshot block CŨ cho journal (undo tay/forensic)
        cur.update({k: v for k, v in prof.items() if v})    # merge: chỉ set field CÓ giá trị; KHÔNG xoá field cũ
        profs[name] = cur
        data["profiles"] = profs
        # v1.29.3 (AUDIT B1 #6): JOURNAL ghi config (op config_write, non-reg → resume/undo KHÔNG đụng) — trước đây
        # đường ghi config KHÔNG dấu vết (nguy cơ hỏng config im lặng, vd registryDocId bị đổi mà không ai biết từ đâu).
        # Best-effort: journal lỗi KHÔNG chặn ghi config.
        _rid = None
        try:
            _rid = _apply_journal_start("config-write", {"target": str(target), "profile_block": name})
            _journal_append(_rid, {"t": "intent", "op": "config_write", "key": name, "key_field": "profile",
                                   "set": {k: v for k, v in prof.items() if v}, "before": _before})
        except Exception:
            _rid = None
        # Ghi NGUYÊN TỬ (temp cùng thư mục + os.replace) → crash giữa chừng KHÔNG làm hỏng config.
        _tmp = target.with_suffix(target.suffix + ".tmp")
        _tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(str(_tmp), str(target))
        if _rid:
            try:                                            # verify READ-BACK: block trên đĩa == block định ghi
                _rb = json.loads(target.read_text(encoding="utf-8"))
                _ok = (_rb.get("profiles") or {}).get(name) == cur
                _journal_append(_rid, {"t": "commit", "op": "config_write", "key": name, "ok": bool(_ok),
                                       "verify": {"readback_match": bool(_ok)}})
            except Exception:
                pass
        return str(target)
    except Exception:
        return None


def _read_config_record(config_path: str | None = None) -> tuple[str | None, dict]:
    """Đọc config-of-record theo cùng thứ tự load_creds, nhưng KHÔNG đòi webapp token."""
    for p in _config_candidates(config_path):
        if p and Path(p).exists():
            cfg = _read_json_file(p)
            if isinstance(cfg, dict) and cfg:
                return str(p), cfg
    return None, {}


def _write_json_atomic(target: Path, data: dict) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    _fd, _tmp = tempfile.mkstemp(prefix=target.name + ".", suffix=".tmp", dir=str(target.parent))
    with os.fdopen(_fd, "w", encoding="utf-8", errors="replace", newline="\n") as _f:   # v1.33.56 (F7): tmp duy nhất
        _f.write(json.dumps(data, ensure_ascii=False, indent=2))
    os.replace(_tmp, str(target))


def _mutable_config_target(config_path: str | None = None) -> tuple[Path | None, dict, str | None]:
    """Chọn file config có thể ghi để thao tác profile. Không ghi đè template trong bundle nếu thiếu --config."""
    cands = [Path(config_path)] if config_path else [Path.home() / ".tra_luat_config.json",
                                                     Path("/tmp/tra_luat_config.json")]
    target = next((p for p in cands if p and p.exists()), None) or (Path(config_path) if config_path else None)
    if target is None:
        return None, {}, "CONFIG_NOT_FOUND: truyền --config hoặc chạy `tl init-config --from-public` trước."
    data = {}
    if target.exists():
        try:
            data = json.loads(target.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            return target, {}, f"CONFIG_JSON_INVALID: {e}"
    if not isinstance(data, dict):
        return target, {}, "CONFIG_JSON_NOT_OBJECT"
    return target, data, None


def _profile_config_rows(cfg: dict, active: str | None = None) -> list[dict]:
    profs = _profiles_from_config(cfg)
    default = cfg.get("defaultProfile") or DEFAULT_PROFILE
    rows = []
    for name, prof in sorted(profs.items()):
        prof = prof if isinstance(prof, dict) else {}
        rows.append({
            "profile": name,
            "default": name == default,
            "active": name == active,
            "rootFolderId": prof.get("rootFolderId") or "",
            "metaFolderId": prof.get("metaFolderId") or "",
            "notebookId": prof.get("notebookId") or "",
            "registryDocId": prof.get("registryDocId") or "",
            "manifestId": prof.get("manifestId") or "",
            "categories": prof.get("categories") or "",
            "manifestScope": prof.get("manifestScope") or "",
        })
    return rows


def _rename_profile_config(config_path: str | None, old: str, new: str, force: bool = False) -> dict:
    old, new = (old or "").strip(), (new or "").strip()
    target, data, err = _mutable_config_target(config_path)
    if err:
        return {"ok": False, "error": err, "path": str(target) if target else None}
    if old == DEFAULT_PROFILE:
        return {"ok": False, "error": "REFUSE_RENAME_DEFAULT_PROFILE"}
    if not old or not new or old == new:
        return {"ok": False, "error": "PROFILE_RENAME_NEEDS_DISTINCT_OLD_NEW"}
    profs = data.get("profiles") if isinstance(data.get("profiles"), dict) else {}
    if old not in profs:
        return {"ok": False, "error": "PROFILE_NOT_FOUND", "profile": old, "path": str(target)}
    if new in profs and not force:
        return {"ok": False, "error": "PROFILE_TARGET_EXISTS", "profile": new, "path": str(target)}
    prof = profs.pop(old)
    if isinstance(profs.get(new), dict) and isinstance(prof, dict):
        merged = dict(profs[new])
        merged.update(prof)
        profs[new] = merged
    else:
        profs[new] = prof
    if data.get("defaultProfile") == old:
        data["defaultProfile"] = new
    data["profiles"] = profs
    _write_json_atomic(target, data)
    return {"ok": True, "path": str(target), "old": old, "new": new, "defaultProfile": data.get("defaultProfile")}


def _remove_profile_config(config_path: str | None, name: str) -> dict:
    name = (name or "").strip()
    target, data, err = _mutable_config_target(config_path)
    if err:
        return {"ok": False, "error": err, "path": str(target) if target else None}
    if name == DEFAULT_PROFILE:
        return {"ok": False, "error": "REFUSE_DELETE_DEFAULT_PROFILE"}
    profs = data.get("profiles") if isinstance(data.get("profiles"), dict) else {}
    if name not in profs:
        return {"ok": False, "error": "PROFILE_NOT_FOUND", "profile": name, "path": str(target)}
    removed = profs.pop(name)
    if data.get("defaultProfile") == name:
        data["defaultProfile"] = DEFAULT_PROFILE
    data["profiles"] = profs
    _write_json_atomic(target, data)
    return {"ok": True, "path": str(target), "profile": name, "removed": removed,
            "defaultProfile": data.get("defaultProfile") or DEFAULT_PROFILE}


def _set_default_profile_config(config_path: str | None, name: str) -> dict:
    name = (name or "").strip()
    target, data, err = _mutable_config_target(config_path)
    if err:
        return {"ok": False, "error": err, "path": str(target) if target else None}
    profs = _profiles_from_config(data)
    if name not in profs:
        return {"ok": False, "error": "PROFILE_NOT_FOUND", "profile": name, "path": str(target)}
    data["defaultProfile"] = name
    _write_json_atomic(target, data)
    return {"ok": True, "path": str(target), "defaultProfile": name}


def _profile_asset_ids(prof: dict) -> list[dict]:
    roles = [("root", "rootFolderId"), ("meta", "metaFolderId"), ("registry", "registryDocId"),
             ("manifest", "manifestId")]
    out, seen = [], set()
    for role, key in roles:
        fid = str((prof or {}).get(key) or "").strip()
        if fid and fid not in seen:
            out.append({"role": role, "fileId": fid})
            seen.add(fid)
    return out


def _profile_live_source_ids(entries: list[dict]) -> list[str]:
    out, seen = [], set()
    for e in entries or []:
        sid = (_entry_nlm(e) or "").strip()
        st = str(e.get("nlm_status") or "").strip().lower()
        if sid and sid not in seen and not st.startswith("removed") and st not in {"deleted", "gone"}:
            out.append(sid)
            seen.add(sid)
    return out


def _profile_asset_owners(profiles: dict, file_id: str) -> list[str]:
    """Review v1.30.0 (PURE): các profile trong config đang trỏ registryDocId/manifestId == file_id.
    Dùng chặn mutate/move asset DÙNG CHUNG ≥2 profile (doctrine: registry/manifest RIÊNG theo profile)."""
    fid = str(file_id or "").strip()
    if not fid:
        return []
    out = []
    for n, p in (profiles or {}).items():
        p = p if isinstance(p, dict) else {}
        if fid in (str(p.get("registryDocId") or "").strip(), str(p.get("manifestId") or "").strip()):
            out.append(n)
    return sorted(out)


def cmd_profile_file_add(a) -> int:
    return cmd_profile_ingest(a)


def _profile_file_slug(name: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", _strip_accents(name or "").strip())
    return (slug.strip("._-") or "profile")[:80]


def _doctor_check_profile(name: str, prof: dict, infos: dict) -> list[dict]:
    """D (PURE, test offline): kiểm bất biến layout + hạ tầng 1 profile dự án. infos: {fileId: {mimeType, parents,
    trashed, name}} (từ action `info`, best-effort — thiếu info thì bỏ qua check phụ thuộc).
    BẤT BIẾN: registry+manifest nằm TRONG thư mục profile (root hoặc _meta của nó)."""
    finds = []
    root = str((prof or {}).get("rootFolderId") or "").strip()
    meta = str((prof or {}).get("metaFolderId") or "").strip()
    ok_parents = {x for x in (root, meta) if x}
    if not root:
        finds.append({"check": "NO_ROOT_FOLDER", "severity": "warn", "profile": name,
                      "note": "profile thiếu rootFolderId — không kiểm được layout."})
    if not str((prof or {}).get("notebookId") or "").strip():
        finds.append({"check": "NO_NOTEBOOK_ID", "severity": "warn", "profile": name,
                      "note": "thiếu notebookId — lệnh NLM sẽ chặn (đúng thiết kế); bổ sung khi cần push/query."})
    for role, key in (("registry", "registryDocId"), ("manifest", "manifestId")):
        fid = str((prof or {}).get(key) or "").strip()
        if not fid:
            finds.append({"check": f"NO_{role.upper()}_ID", "severity": "critical" if role == "registry" else "warn",
                          "profile": name, "note": f"profile thiếu {key} — seed bằng profile-adopt/profile-create."})
            continue
        if role == "registry" and fid == _LEGACY_REGISTRY_DOC_ID:
            finds.append({"check": "REGISTRY_LEGACY_DOC", "severity": "critical", "profile": name, "fileId": fid,
                          "note": "registryDocId là Doc legacy 1mATG… (đọc RỖNG count=0 ảo) — trỏ lại Sheet thật."})
            continue
        info = (infos or {}).get(fid) or {}
        mime = str(info.get("mimeType") or "")
        if role == "registry" and mime and mime != REGISTRY_SHEET_MIME:
            finds.append({"check": "REGISTRY_NOT_SHEET_MIME", "severity": "critical", "profile": name,
                          "fileId": fid, "mime": mime, "note": "registry PHẢI là Google Sheet."})
        if info.get("trashed"):
            finds.append({"check": f"{role.upper()}_TRASHED", "severity": "critical", "profile": name,
                          "fileId": fid, "note": f"{role} đang trong Trash — restore hoặc trỏ file khác."})
        parents = [str(x) for x in (info.get("parents") or [])]
        if parents and ok_parents and not (set(parents) & ok_parents):
            finds.append({"check": "MISPLACED_ASSET", "severity": "warn", "profile": name, "role": role,
                          "fileId": fid, "parents": parents,
                          "note": f"{role} nằm NGOÀI thư mục profile (bất biến layout: root hoặc _meta).",
                          "fix": {"action": "move", "fileId": fid, "to": meta or root}})
    return finds


def _hopnap_upload_md() -> str:
    return f"- [Mở thư mục _HOP_NAP để tải lên](https://drive.google.com/drive/folders/{HOPNAP_FOLDER_ID})"


def _profile_deletable_sources(entries: list, source_ids: list) -> tuple:
    """(MERGE Claude, an toàn) Tách nguồn NLM xóa-được / bị-CHẶN vì shared_source_id (xóa 1 gãy link kia). Dùng cho
    profile-delete/profile-file-remove trước khi `nlm source delete`. Trả (deletable[], blocked[])."""
    shared = {g["source_id"] for g in _shared_source_id_groups(entries)}
    return ([s for s in source_ids if s not in shared], [s for s in source_ids if s in shared])
