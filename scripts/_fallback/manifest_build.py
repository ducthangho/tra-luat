# [tra-luat _fallback] Phiên bản TỐI GIẢN chạy độc lập khi overlay KHÔNG nằm trên bộ skill đầy đủ.
# Gốc: gói runtime-hotfix của reviewer (đã rà & giữ nguyên logic). Chỉ dùng khi scripts/manifest_build.py thật VẮNG.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""manifest_build.py — wrapper regen2 + manifest_export cho tl manifest."""
from __future__ import annotations
import sys, time
import os
from pathlib import Path

# UTF-8 hardening (Windows codepage / tiếng Việt)
import sys as _sys
for _s in (getattr(_sys, "stdout", None), getattr(_sys, "stderr", None)):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent
DEFAULT_PROFILE = "vbqppl"


def _scope_params() -> dict:
    if (os.environ.get("TL_PROFILE") or DEFAULT_PROFILE) == DEFAULT_PROFILE:
        return {}
    out = {}
    if os.environ.get("TL_REGISTRY_DOC_ID"):
        out["registryDocId"] = os.environ["TL_REGISTRY_DOC_ID"]
    if os.environ.get("TL_MANIFEST_ID"):
        out["manifestId"] = os.environ["TL_MANIFEST_ID"]
    if os.environ.get("TL_ROOT_FOLDER_ID"):
        out["rootFolderId"] = os.environ["TL_ROOT_FOLDER_ID"]
    if os.environ.get("TL_CATEGORIES_MODE"):
        out["categoriesMode"] = os.environ["TL_CATEGORIES_MODE"]
    out["profileName"] = os.environ.get("TL_PROFILE") or DEFAULT_PROFILE
    return out


def build(no_regen: bool = True, manifest_scope: str | None = None,
          confirm_blowup: str | None = None, confirm_inherited: str | None = None) -> dict:
    sys.path.insert(0, str(HERE))
    import gas  # noqa
    t0 = time.time()
    scope = _scope_params()
    regen = None
    if not no_regen:
        regen_params = dict(scope)
        regen_params["confirm"] = "yes"
        if manifest_scope:
            regen_params["manifestScope"] = manifest_scope
        if confirm_blowup:
            regen_params["confirmBlowup"] = confirm_blowup
        if confirm_inherited:
            regen_params["confirmInherited"] = confirm_inherited
        regen = gas.get("regen2", **regen_params)
        if regen.get("ok") is False:
            regen["total_ms"] = int((time.time()-t0)*1000)
            return regen
    man = gas.get("manifest_export", **scope)
    out = dict(man)
    out.setdefault("profile", os.environ.get("TL_PROFILE") or DEFAULT_PROFILE)
    out.setdefault("registryDocId", scope.get("registryDocId", ""))
    out.setdefault("manifestId_requested", scope.get("manifestId", ""))
    if regen:
        out["regen2"] = regen
        if regen.get("treeHash") and man.get("treeHash"):
            out["treeHash_match"] = (regen.get("treeHash") == man.get("treeHash"))
        if regen.get("corpus_count") is not None and man.get("corpus_count") is not None:
            out["corpus_count_match"] = (regen.get("corpus_count") == man.get("corpus_count"))
    out["total_ms"] = int((time.time()-t0)*1000)
    return out
