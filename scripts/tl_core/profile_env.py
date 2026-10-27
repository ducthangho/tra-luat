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


def _path_exists_safe(path) -> bool:
    """Best-effort existence check for report/config discovery paths.

    Sandboxed Windows environments can raise PermissionError even for ``exists()``.
    Discovery must treat that path as unavailable instead of crashing a read-only command.
    """
    try:
        return bool(Path(path).exists())
    except (OSError, PermissionError):
        return False


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
    raw = cfg.get("profiles") if isinstance(cfg.get("profiles"), dict) else {}
    # Malformed blocks are not profiles. Keep an empty dict value: it deliberately
    # represents a known profile whose write scope has not been materialized yet.
    profiles = {str(k): v for k, v in raw.items() if isinstance(v, dict)}
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
    _env_profile_before = (os.environ.get("TL_PROFILE") or "").strip()   # r281: đo TRƯỚC khi :129 ghi đè
    name0 = _selected_profile_name(profile, cfg)
    name, _hit = _profile_lookup(profiles, name0)
    # r281 (P16-F08): scope KHÔNG do người gõ chọn (không --profile, không export TL_PROFILE) mà do
    # `config.defaultProfile` quyết định thì phải NÓI RA MỘT LẦN — scope ghi vô hình đúng là thứ đã biến
    # F08 thành P0. In 1 lần/process, chỉ khi profile THẬT và khác nền (nền = trạng thái mặc định, không ồn).
    if (not profile) and (not _env_profile_before) and name != DEFAULT_PROFILE and name in profiles:
        if not getattr(_apply_profile_env, "_default_profile_noted", False):
            _apply_profile_env._default_profile_noted = True
            print(f"[tl] profile = '{name}' (theo config.defaultProfile — KHÔNG phải --profile). "
                  f"Muốn corpus nền: `--profile {DEFAULT_PROFILE}`.", file=sys.stderr)
    # v1.33.48 (rà Instruction 'Luật BHXH'): profile ĐƯỢC YÊU CẦU TƯỜNG MINH mà KHÔNG có trong config → KHÔNG
    # rơi ÂM THẦM về scope NỀN vbqppl nữa (trước: prof=fallback DEFAULT → TL_REGISTRY_DOC_ID/TL_NOTEBOOK_ID trỏ
    # VBQPPL base trong khi TL_PROFILE=tên-dự-án → ghi/push NHẦM corpus nền, đúng lớp sự cố 1.23.21 mà
    # _resolve_nlm_notebook/NO_NOTEBOOK_ID không bắt được vì env ĐÃ bị điền từ nền). Nay: scope RỖNG + cảnh báo
    # LOUD → guard hạ nguồn tự chặn (NO_NOTEBOOK_ID, PROFILE_CATEGORIES_OWN_REQUIRED, registry-id-empty blocker).
    if _hit is None and name0 != DEFAULT_PROFILE:
        prof = {}
        # r286 (P16-F09): v1.33.48 mới bịt đường GHI (scope rỗng ⇒ guard hạ nguồn chặn). Đường ĐỌC vẫn
        # thủng: `_load_manifest_full` gặp cache-miss sẽ gọi `manifest_export` với scope RỖNG ⇒ GAS trả
        # manifest NỀN ⇒ ghi vào `CACHE/<tên ma>/` (BỀN VỮNG) và `exists`/`reg-query` trả corpus nền dưới
        # NHÃN của tên gõ sai. Marker này là chốt chặn ở ĐÚNG MỘT CHỖ (`_load_manifest_full`) phủ mọi lệnh đọc.
        os.environ["TL_PROFILE_MISSING"] = str(name0)
        print(f"[tl] ⚠ PROFILE_NOT_FOUND: '{name0}' không có trong config.profiles ({', '.join(sorted(profiles)) or '∅'}) "
              f"— KHÔNG dùng scope nền thay thế. Kiểm chính tả (nhận cả gõ không dấu nếu khớp DUY NHẤT) hoặc thêm "
              f"block profiles vào config (xem SKILL.md corpus_profile).", file=sys.stderr)
    else:
        # An empty dict is a valid, explicitly configured profile. Truthiness here
        # used to fall back to vbqppl and could redirect writes into the base corpus.
        prof = _hit if _hit is not None else (profiles.get(DEFAULT_PROFILE) or {})
        os.environ.pop("TL_PROFILE_MISSING", None)   # r286: profile HỢP LỆ ⇒ gỡ chốt (kể cả khi trước đó có)
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
    # r214 (sổ lỗi TL_META_FOLDER_ID_BI_PROFILE_OVERLAY_XOA — đo LIVE 26-07): vòng xoá này TRƯỚC ĐÂY pop VÔ
    # ĐIỀU KIỆN cả 6 khoá, nên env do NGƯỜI DÙNG export trước khi chạy — đúng đường mà `state-get`/`state-put`
    # và RASOAT_HOSO_LOOP §7 chỉ — bị xoá trắng khi block profile thiếu ô tương ứng; lệnh rồi báo
    # META_FOLDER_ID_TRONG và chỉ lại chính cái đường vừa bị nó phá. Mục đích THẬT của vòng xoá chỉ là "đổi
    # profile trong CÙNG process không dính scope cũ" ⇒ chỉ cần xoá đúng khoá do CHÍNH overlay trước ghi.
    # Dấu vết để trong env (KHÔNG dùng biến module: bẫy I11 — mutable/hằng ở tl_core phải re-export sang tl.py
    # mới sống qua rebase globals; env lại đi theo cả process con, đúng ngữ nghĩa "overlay đã ghi").
    # ★NGOẠI LỆ GIỮ NGUYÊN (v1.33.48): PROFILE_NOT_FOUND → xoá SẠCH bất kể ai ghi, để guard hạ nguồn
    # (NO_NOTEBOOK_ID / PROFILE_CATEGORIES_OWN_REQUIRED / registry-id-empty) fail-closed, KHÔNG mượn scope nền
    # từ env còn sót — nới chỗ này là mở lại đúng lớp sự cố 1.23.21 mà v1.33.48 sinh ra để chặn.
    _mark = "TL_PROFILE_ENV_OVERLAY"
    _prev_overlay = {k for k in str(os.environ.get(_mark) or "").split(",") if k}
    _profile_missing = (_hit is None and name0 != DEFAULT_PROFILE)
    _written = []
    for dst in tuple(mapping.values()) + ("TL_CATEGORIES_MODE", "TL_MANIFEST_SCOPE", "TL_BASE_ALSO"):
        if _profile_missing or dst in _prev_overlay:
            os.environ.pop(dst, None)
    for src, dst in mapping.items():
        val = prof.get(src)
        if val:
            os.environ[dst] = str(val)
            _written.append(dst)
    categories = prof.get("categories")
    if isinstance(categories, str):
        os.environ["TL_CATEGORIES_MODE"] = categories.strip().lower()
        _written.append("TL_CATEGORIES_MODE")
    elif isinstance(categories, dict):
        os.environ["TL_CATEGORIES_MODE"] = "own"
        _written.append("TL_CATEGORIES_MODE")
    manifest_scope = str(prof.get("manifestScope") or "").strip().lower()
    if manifest_scope:
        os.environ["TL_MANIFEST_SCOPE"] = manifest_scope
        _written.append("TL_MANIFEST_SCOPE")
    # v1.30.0 (A — profile CỘNG VBQPPL): profile DỰ ÁN mặc định TL_BASE_ALSO=1 — các lệnh ĐỌC (locate/reg-query/
    # source-map/exists/nlm-cross) quét THÊM nền VBQPPL+shards, hit profile ưu tiên (doctrine MULTI_CORPUS_V1_18 §2
    # nay vào CLI, không chỉ Instruction). Opt-out: config.profiles.<p>.baseAlso=false hoặc --no-base-also per-lệnh.
    # vbqppl nền: KHÔNG set (không tự quét chính mình 2 lần). GHI/ingest KHÔNG đụng cờ này (scope profile giữ nguyên).
    # Review v1.30.0 (CONFIRMED): CHỈ set khi profile THẬT có trong config — tên KHÔNG tồn tại rơi về data NỀN
    # (prof=fallback vbqppl ở trên) mà vẫn set cờ ⇒ nền tự quét mình 2 lần (vô hại nhờ dedup drive_id nhưng tốn IO + sai doctrine).
    if name != DEFAULT_PROFILE and name in profiles:
        os.environ["TL_BASE_ALSO"] = "0" if prof.get("baseAlso") is False else "1"
        _written.append("TL_BASE_ALSO")
    os.environ[_mark] = ",".join(_written)   # r214: khoá do overlay NÀY ghi — lượt sau chỉ được xoá đúng chúng
    # r325 (VIỆC 4.2 sổ bảo trì kho): profile dự án CÓ THẬT trong config nhưng `registryDocId` RỖNG.
    # Đường GHI đã fail-closed từ 1.23.21 (PROFILE_REGISTRY_ID_EMPTY_WOULD_CLOBBER_BASE, rc=2) — đó là
    # bản vá cho ĐÚNG sự cố 2026-06-30. Đường ĐỌC thì tới giờ vẫn IM: `TL_REGISTRY_DOC_ID` không được
    # đặt ⇒ webapp `regSS_` rơi nhánh auto-discover = SỔ NỀN, và `reg-query`/`reg_get` trả dòng nền
    # dưới NHÃN profile đang chọn. `scope`+`BASE_SCOPE_HIT` (r179 T7) chỉ nói được KHI ĐÃ CÓ dòng trả
    # về; ca này người dùng đọc thấy 0 dòng / dòng nền mà không biết `--profile` đã thành NO-OP.
    # ★Chỉ CẢNH BÁO, không chặn: lệnh ĐỌC trên sổ nền là chuyện hợp lệ, cái sai là làm nó IM LẶNG.
    #  Nền (vbqppl) để rỗng là BÌNH THƯỜNG — webapp tự tìm Sheet `tra_luat_registry` theo tên.
    if name != DEFAULT_PROFILE and name in profiles \
            and not (os.environ.get("TL_REGISTRY_DOC_ID") or "").strip():
        _noted = getattr(_apply_profile_env, "_reg_empty_noted", None)
        if _noted is None:
            _noted = set()
            _apply_profile_env._reg_empty_noted = _noted
        if name not in _noted:      # 1 lần / profile / process (đổi profile giữa chừng vẫn được báo)
            _noted.add(name)
            print(f"[tl] ⚠ PROFILE_REGISTRY_ID_EMPTY: profile '{name}' KHÔNG có `registryDocId` "
                  f"⇒ mọi lệnh ĐỌC registry rơi về SỔ NỀN '{DEFAULT_PROFILE}' (dòng trả về là của NỀN, "
                  f"không phải của profile này). Đường GHI đã bị chặn sẵn (rc=2). Sửa: thêm "
                  f"`profiles.{name}.registryDocId` vào config, hoặc `tl profile-rebuild-registry "
                  f"--profile \"{name}\"` để tạo registry RIÊNG.", file=sys.stderr)
    return {"profile": name, "profile_found": name in profiles, "profile_data": prof, "profiles": sorted(profiles)}


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


def _profile_cache_component(profile: str) -> str:
    """Map an arbitrary profile name to one safe, stable cache-directory component."""
    raw = str(profile or "").strip()
    reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
                *(f"LPT{i}" for i in range(1, 10))}
    invalid = (not raw or raw in (".", "..") or raw.endswith((" ", "."))
               or any(ord(ch) < 32 or ch in '<>:"/\\|?*' for ch in raw)
               or raw.split(".", 1)[0].upper() in reserved
               or Path(raw).name != raw)
    if not invalid:
        return raw
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", _strip_accents(raw)).strip("._-")[:48] or "profile"
    digest = hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()[:12]
    return f"{slug}-{digest}"


def _profile_cache_dir() -> Path:
    prof = _active_profile()
    return CACHE if prof == DEFAULT_PROFILE else CACHE / _profile_cache_component(prof)


def _apply_unconfigured_profile_env(profile: str | None) -> None:
    """Switch an explicit env-only profile without carrying scope from the prior one."""
    name = str(profile or "").strip()
    if not name:
        return
    # r286 (P16-F09): đây là đường HỢP LỆ theo §9 — profile env-only, KHÔNG có file config nào để tra.
    # Phải GỠ chốt PROFILE_NOT_FOUND (nếu lượt trước đặt), nếu không lệnh đọc bị chặn oan.
    os.environ.pop("TL_PROFILE_MISSING", None)
    previous = os.environ.get("TL_PROFILE", "")
    if previous and previous != name:
        for key in ("TL_ROOT_FOLDER_ID", "TL_META_FOLDER_ID", "TL_NOTEBOOK_ID", "TL_REGISTRY_DOC_ID",
                    "TL_MANIFEST_ID", "TL_OVERFLOW_NOTEBOOK_ID", "TL_CATEGORIES_MODE",
                    "TL_MANIFEST_SCOPE", "TL_BASE_ALSO"):
            os.environ.pop(key, None)
        print(f"[tl] ⚠ PROFILE_CONFIG_NOT_FOUND: chuyển '{previous}' → '{name}' bằng env; "
              "đã xóa scope cũ để tránh ghi nhầm đích.", file=sys.stderr)
    os.environ["TL_PROFILE"] = name


def load_creds(config_path: str | None = None, profile: str | None = None) -> None:
    """Đặt TL_WEBAPP/TL_TOKEN + profile corpus vào env TRƯỚC khi import gas.
    ENV (TL_WEBAPP+TL_TOKEN) ĐỦ để chạy — KHÔNG bắt buộc file config, KỂ CẢ khi có --profile (§9): scope chi tiết
    lấy qua TL_REGISTRY_DOC_ID/TL_MANIFEST_ID/… (env) hoặc config mặc định nếu tình cờ có."""
    if os.environ.get("TL_WEBAPP") and os.environ.get("TL_TOKEN") and not config_path:
        # r281 (P16-F08, P0 ghi nhầm corpus): vòng quét config này TRƯỚC ĐÂY nằm trong `if profile:` ⇒ khi
        # env đã có TL_WEBAPP/TL_TOKEN mà người dùng KHÔNG gõ --profile thì `config.defaultProfile` bị BỎ QUA
        # HOÀN TOÀN — `_apply_profile_env` không chạy, TL_PROFILE không được đặt, `_active_profile()` trả
        # vbqppl ⇒ MỌI lệnh GHI non-lazy đổ vào corpus NỀN trong im lặng, và mọi guard profile đều return
        # sớm vì profile == DEFAULT_PROFILE. Nay quét KỂ CẢ khi profile=None: `_selected_profile_name` tự
        # xếp hạng --profile > env TL_PROFILE > config.defaultProfile > vbqppl, nên bỏ guard là đủ và
        # KHÔNG đảo thứ tự ưu tiên nào (env TL_PROFILE do người dùng export vẫn thắng defaultProfile).
        applied = False
        for p in _config_candidates(None):            # best-effort áp scope từ config mặc định nếu có
            if p and _path_exists_safe(p):
                cfg = _read_json_file(p)
                if cfg:
                    _apply_profile_env(cfg, profile)
                    applied = True
                    break
        if not applied and profile:
            _apply_unconfigured_profile_env(profile)
        return
    for p in _config_candidates(config_path):
        if p and _path_exists_safe(p):
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
        if p and _path_exists_safe(p):
            cfg = _read_json_file(p)
            if cfg:
                _apply_profile_env(cfg, profile)
                return
    if profile:
        _apply_unconfigured_profile_env(profile)


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


def _gas_get_retry(g, action: str, _retries: int = 2, _backoff: float = 1.5, _schedule=None, **kw) -> dict:
    """v1.29.4 (i5): GET action ĐỌC idempotent với RETRY backoff — CHỈ retry khi lỗi TRANSIENT (timeout/URLError/
    'Response không phải JSON' = webapp trả trang lỗi tạm). KHÔNG dùng cho action mutate (retry mù = at-least-once,
    nguy hiểm với createtext/copy_convert). Gốc sự cố: sau bust-cache, lệnh kế rebuild manifest đúng lúc webapp
    chậm → 1 lỗi transient = PARSEERR/timeout hàng loạt, phải boot --refresh tay.
    F6 r192: (a) `_schedule` = lịch chờ TƯỜNG MINH theo giây, số retry = len(schedule) (vd (5, 15) cho
    ingest_claim/reg_get); (b) GAS 404 CHẬP CHỜN ('HTTPError: 404' từ chính URL webapp — hạ tầng deploy,
    KHÁC NOT_FOUND nghiệp vụ vốn trả JSON ok:false) nay coi là transient (đo 23-07)."""
    import time as _t
    if _schedule is not None:
        _retries = len(_schedule)
    r = {}
    for _i in range(_retries + 1):
        r = g.get(action, **kw)
        if not (isinstance(r, dict) and r.get("ok") is False):
            return r
        _msg = str(r.get("error") or "")
        if not any(s in _msg for s in ("TimeoutError", "timed out", "URLError", "RemoteDisconnected",
                                       "ConnectionReset", "IncompleteRead", "Response không phải JSON",
                                       "HTTPError: 5", "HTTPError: 404")):
            return r          # lỗi THẬT từ webapp (JSON ok:false) → không retry
        if _i < _retries:
            _delay = float(_schedule[_i]) if _schedule is not None else _backoff * (_i + 1)
            print(f"[gas-retry] {action}: lỗi transient ({_msg[:60]}…) → thử lại {_i + 1}/{_retries} sau {_delay:.1f}s",
                  file=sys.stderr, flush=True)
            _t.sleep(_delay)
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
    # #11 (v1.34.19, ca thật #10): ứng viên = _config_candidates (CÙNG thứ tự resolution với ĐỌC config —
    # cwd/skill-side v2 TRƯỚC ~/.tra_luat_config.json). Trước đây hardcode home-config → adopt/create không
    # --config GHI LẠC vào file KHÔNG active, im lặng; profile-list vẫn inherit mà không ai biết vì sao.
    target, data, err = _mutable_config_target(config_path)
    if target is None or err:
        return None
    try:
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
        _write_json_atomic(target, data)
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


def _persist_profiles_config_bulk(config_path: str | None, blocks: dict) -> dict:
    """r185/WP5 (D6 — profile-sync): ghi NHIỀU block profile trong MỘT lần read-modify-write nguyên tử
    (trước: _persist_profile_config ×N = N lần đọc/ghi file + N journal run). blocks = {name: {field: value}}.
    Cùng semantics merge (chỉ set field CÓ giá trị, không xoá field cũ) + journal MỘT run (intent per profile,
    before đầy đủ) + readback verify per profile. Trả {ok, config, verified: {name: bool}}."""
    blocks = {str(k): dict(v) for k, v in (blocks or {}).items() if isinstance(v, dict)}
    if not blocks:
        return {"ok": True, "config": None, "verified": {}}
    target, data, err = _mutable_config_target(config_path)
    if target is None or err or not isinstance(data, dict):
        return {"ok": False, "config": None, "verified": {k: False for k in blocks}}
    try:
        profs = data.get("profiles") if isinstance(data.get("profiles"), dict) else {}
        _rid = None
        try:
            _rid = _apply_journal_start("config-write", {"target": str(target),
                                                         "profile_blocks": sorted(blocks)})
        except Exception:  # noqa: BLE001
            _rid = None
        expected = {}
        for name in sorted(blocks):
            cur = profs.get(name) if isinstance(profs.get(name), dict) else {}
            _before = dict(cur)
            cur.update({k: v for k, v in blocks[name].items() if v})
            profs[name] = cur
            expected[name] = dict(cur)
            if _rid:
                try:
                    _journal_append(_rid, {"t": "intent", "op": "config_write", "key": name,
                                           "key_field": "profile",
                                           "set": {k: v for k, v in blocks[name].items() if v},
                                           "before": _before})
                except Exception:  # noqa: BLE001
                    pass
        data["profiles"] = profs
        _write_json_atomic(target, data)   # MỘT lần ghi nguyên tử cho TOÀN BỘ diff
        verified = {}
        try:
            _rb = json.loads(target.read_text(encoding="utf-8"))
            _rb_profs = _rb.get("profiles") or {}
            for name in blocks:
                verified[name] = _rb_profs.get(name) == expected.get(name)
        except Exception:  # noqa: BLE001
            verified = {k: False for k in blocks}
        if _rid:
            for name in sorted(blocks):
                try:
                    _journal_append(_rid, {"t": "commit", "op": "config_write", "key": name,
                                           "ok": bool(verified.get(name)),
                                           "verify": {"readback_match": bool(verified.get(name))}})
                except Exception:  # noqa: BLE001
                    pass
        return {"ok": all(verified.values()), "config": str(target), "verified": verified}
    except Exception:  # noqa: BLE001
        return {"ok": False, "config": None, "verified": {k: False for k in blocks}}


def _read_config_record(config_path: str | None = None) -> tuple[str | None, dict]:
    """Đọc config-of-record theo cùng thứ tự load_creds, nhưng KHÔNG đòi webapp token."""
    for p in _config_candidates(config_path):
        if p and _path_exists_safe(p):
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


class BackupTrongCaySkill(RuntimeError):
    """v1.36.69 (#972): đích backup config nằm trong cây skill — từ chối, KHÔNG dựng thư mục nào."""


def _goc_cay_skill() -> Path:
    """Gốc cây skill = thư mục tổ tiên gần nhất có SKILL.md, tính từ tệp mã đang chạy; không thấy thì
    lùi về cha của thư mục chứa tệp (quy ước ca r202: `tl.py` → `scripts/` → gốc)."""
    tep = Path(__file__).resolve()
    for d in tep.parents:
        if (d / "SKILL.md").is_file():
            return d
    return tep.parent.parent


def _trong_cay_skill(dich: Path, goc: Path) -> bool:
    """`dich` (đã resolve) nằm trong `goc` theo ĐƯỜNG DẪN, hoặc có một tổ tiên đang tồn tại CÙNG danh tính hệ tệp
    với `goc` — review l972a F01: volume không phân biệt hoa thường (APFS) cho `package/` trỏ `Package/` mà phép so
    PosixPath phân biệt hoa thường để lọt."""
    if dich == goc or goc in dich.parents:
        return True
    try:
        st_goc = goc.stat()
    except OSError:
        return False
    for p in (dich, *dich.parents):
        try:
            if os.path.samestat(p.stat(), st_goc):
                return True
        except OSError:
            continue
    return False


def _config_backup_dir() -> Path:
    """r202 (doctrine r193 — backup config CHỨA token KHÔNG BAO GIỜ nằm trong cây skill; sự cố token
    lọt bundle 23-07 + profile-delete để `.bak.json` ở gốc cây 25-07): thư mục đích cho MỌI backup
    config. Ưu tiên TL_CONFIG_BACKUP_DIR (test/override) → `D:\\Quốc hội\\_config_backups` (máy chuẩn,
    chỉ khi ĐÃ tồn tại — không tự dựng cây ngoài) → `%LOCALAPPDATA%\\tra-luat\\_config_backups` →
    (POSIX) `$XDG_STATE_HOME/tra-luat/_config_backups`, mặc định `~/.local/state/...`.
    v1.36.69 (#972): bỏ nhánh `~/tra-luat/_config_backups` — kho clone ở `~/tra-luat` thì đích ấy NẰM TRONG
    cây skill (selftest r202 đỏ trên máy chủ kho, HOME=/home/agent). Chốt cứng sau cùng áp cho MỌI nguồn,
    kể cả env, và chạy TRƯỚC mkdir: đích trong cây ⇒ BackupTrongCaySkill, không dựng gì."""
    env = (os.environ.get("TL_CONFIG_BACKUP_DIR") or "").strip()
    if env:
        target = Path(env).expanduser()
    else:
        preferred = Path("D:/Quốc hội/_config_backups")
        if preferred.is_dir():
            target = preferred
        elif os.environ.get("LOCALAPPDATA"):
            target = Path(os.environ["LOCALAPPDATA"]) / "tra-luat" / "_config_backups"
        else:
            state = (os.environ.get("XDG_STATE_HOME") or "").strip()
            target = Path(state).expanduser() if state else Path.home() / ".local" / "state"
            target = target / "tra-luat" / "_config_backups"
    goc, dich = _goc_cay_skill().resolve(), target.resolve()
    if _trong_cay_skill(dich, goc):
        raise BackupTrongCaySkill(f"đích backup config {dich} nằm trong cây skill {goc} — backup chứa token; "
                                  "đặt TL_CONFIG_BACKUP_DIR ra NGOÀI cây rồi chạy lại")
    target.mkdir(parents=True, exist_ok=True)
    return target


def _mutable_config_target(config_path: str | None = None) -> tuple[Path | None, dict, str | None]:
    """Choose the same config-of-record used for reads, then mutate that exact file.

    Invalid implicit candidates are skipped just like ``_read_config_record``. An
    explicit invalid file is reported, and an explicit new path is allowed only
    when no existing valid candidate wins the normal resolution order.
    """
    explicit = Path(config_path) if config_path else None
    for raw in _config_candidates(config_path):
        target = Path(raw)
        if not _path_exists_safe(target):
            continue
        try:
            data = json.loads(target.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            if explicit is not None and target == explicit:
                return target, {}, f"CONFIG_JSON_INVALID: {e}"
            continue
        if not isinstance(data, dict):
            if explicit is not None and target == explicit:
                return target, {}, "CONFIG_JSON_NOT_OBJECT"
            continue
        if data or (explicit is not None and target == explicit):
            return target, data, None
    if explicit is not None:
        return explicit, {}, None
    return None, {}, "CONFIG_NOT_FOUND: truyền --config hoặc chạy `tl init-config --from-public` trước."


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
        # r320 (PRO-05): TRƯỚC ĐÂY kiểm MIME bị khoá sau `role == "registry"` ⇒ nhánh manifest KHÔNG có
        # phép kiểm loại nào. Một Google Doc đặt ở `manifestId`, parent đúng, đi qua doctor SẠCH TRƠN
        # (đo: 0 finding) trong khi chính nó là thứ không đọc được — manifest được upload
        # `mime=application/json`, `convert=false` (`_create_profile_manifest_json`) rồi tải về JSON-parse.
        # Cố ý KHÔNG đòi đúng `application/json`: Drive có thể trả `text/plain` cho JSON upload, và bản
        # text đó vẫn parse được — siết theo chuỗi MIME chính xác là đỏ OAN. Bất biến THẬT là "không phải
        # tệp Google-native": native cần export mới ra nội dung, nên KHÔNG có đường nào đọc thành JSON.
        if role == "manifest" and mime and mime.startswith("application/vnd.google-apps."):
            finds.append({"check": "MANIFEST_NOT_JSON_MIME", "severity": "critical", "profile": name,
                          "fileId": fid, "mime": mime,
                          "note": "manifest PHẢI là tệp JSON thường (upload convert=false) — bản "
                                  "Google-native không JSON-parse được; trỏ lại file .json thật."})
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
