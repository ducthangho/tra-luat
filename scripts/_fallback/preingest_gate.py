# [tra-luat _fallback] Phiên bản TỐI GIẢN chạy độc lập khi overlay KHÔNG nằm trên bộ skill đầy đủ.
# Gốc: gói runtime-hotfix của reviewer (đã rà & giữ nguyên logic). Chỉ dùng khi scripts/preingest_gate.py thật VẮNG.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""preingest_gate.py — cổng tiền-nạp tối thiểu, ưu tiên an toàn.

Bản này không cố quyết thay người vận hành. Khi thiếu dữ liệu hoặc có xung đột, trả REVIEW.
"""
from __future__ import annotations
import argparse, datetime as _dt, json, re, sys
from pathlib import Path

# UTF-8 hardening (Windows codepage / tiếng Việt)
import sys as _sys
for _s in (getattr(_sys, "stdout", None), getattr(_sys, "stderr", None)):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent


def is_vbhn_name(s: str) -> bool:
    return bool(re.search(r"\bVBHN\b|văn\s*bản\s*hợp\s*nhất", s or "", re.I))


def is_amendment_name(s: str) -> bool:
    return bool(re.search(r"sửa\s*đổi|bổ\s*sung|thay\s*thế|bãi\s*bỏ", s or "", re.I))


def _on_nlm(st: dict) -> bool:
    return bool(st.get("on_nlm") or st.get("nlm_source_id") or str(st.get("status","")).endswith("_ON_NLM"))


# (port Codex hotfix) cổng CHỦ ĐỀ cho status VBHN-first: chống webapp gợi ý USE_VBHN sang văn bản LỆCH chủ đề
# (ca §1.1: Dân số 113/2025 bị webapp tính superseded_by = VBHN Bộ luật Lao động vì goc nhiễm). Best-effort: chỉ hoạt
# động khi superseded_by mang tên/tiêu đề; thiếu tên → no-op (giữ hành vi cũ, KHÔNG false-reject).
_STOP = {
    "bo", "luat", "phap", "lenh", "nghi", "dinh", "thong", "tu", "quyet",
    "van", "ban", "hop", "nhat", "vbhn", "qh", "vpqh", "cp", "tt",
    "hieu", "cua", "va", "cac", "mot", "nhung", "quy", "dinh",
}


def _plain(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFD", str(s or ""))
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return s.replace("đ", "d").replace("Đ", "D").lower()


def _subject_text(st: dict) -> str:
    raw = " ".join(str(st.get(k) or "") for k in (
        "name", "title", "title_vn", "trichyeu", "trich_yeu", "ten", "ten_van_ban", "nlm_title"
    ))
    raw = re.sub(r"\b\d{1,4}[/_-]\d{4}[/_-][A-ZĐ0-9_-]+\b", " ", raw, flags=re.I)
    raw = re.sub(r"[_./-]+", " ", raw)
    return _plain(raw)


def _subject_tokens(st: dict) -> set:
    return {t for t in re.findall(r"[a-z0-9]{2,}", _subject_text(st)) if t not in _STOP and not t.isdigit()}


def _relation_subject_compatible(current: dict, vbhn: dict) -> bool:
    """Best-effort: chỉ redirect VBHN-first khi tên/chủ đề đủ giống. Thiếu tên 2 bên → True (no-op an toàn)."""
    a, b = _subject_tokens(current), _subject_tokens(vbhn)
    if not a or not b:
        return True
    compact_a = re.sub(r"[^a-z0-9]+", "", _subject_text(current))
    compact_b = re.sub(r"[^a-z0-9]+", "", _subject_text(vbhn))
    if len(compact_a) >= 4 and (compact_a in compact_b or compact_b in compact_a):
        return True
    overlap = a & b
    needed = 1 if min(len(a), len(b)) == 1 else 2
    return len(overlap) >= needed


def _redirect_vbhn(current: dict) -> tuple:
    """VBHN-first: bản GỐC đã được hợp nhất (status *CONSOLIDATED*) → chọn VBHN hợp nhất
    (trong superseded_by) đang hiệu lực/đã trên NLM để TRỎ THẲNG sang, thay vì REVIEW mơ hồ.
    KHÔNG trỏ nếu chính nó là VBHN. Trả (target|None, rejected[]) — rejected = VBHN gợi ý nhưng LỆCH chủ đề (§1.1)."""
    status = str(current.get("status") or current.get("vb_status") or "").upper()
    if "CONSOLIDATED" not in status or current.get("is_vbhn") or is_vbhn_name(str(current.get("sohieu") or "")):
        return None, []
    rejected = []
    for t in (current.get("superseded_by") or []):
        if is_vbhn_name(str(t.get("sohieu") or "")) and (t.get("on_nlm") or str(t.get("hieuluc") or "").strip()):
            if not _relation_subject_compatible(current, t):
                rejected.append(t)
                continue
            return t, rejected
    return None, rejected


def _sohieu_year_pg(s: str):
    m = re.search(r"[-/_](20\d{2}|19\d{2})(?:[-/_]|$)", s or "")
    return int(m.group(1)) if m else None


def _effective_iso(st: dict) -> str | None:
    raw = str(st.get("hieuluc") or st.get("hieu_luc") or "")
    m = re.search(r"(\d{1,2})\s*[/\-.]\s*(\d{1,2})\s*[/\-.]\s*(\d{4})", raw)
    if m:
        return f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
    m = re.search(r"ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})", raw, re.I)
    if m:
        return f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
    return None


def decide(current: dict, targets: list[dict] | None = None, is_amendment: bool = False, is_vbhn: bool = False) -> dict:
    targets = targets or []
    status = str(current.get("status") or current.get("vb_status") or "").upper()
    eff = _effective_iso(current)
    if eff and eff > _dt.date.today().isoformat():
        return {"decision": "REVIEW", "reason": "Văn bản có ngày hiệu lực tương lai", "surface": "PENDING_EFFECT",
                "effective_date": eff, "actions": ["Không coi là IN_FORCE; đọc Điều hiệu lực/footnote-map trước khi rà."]}
    if "VBHN_IN_FORCE" in status and _on_nlm(current):
        return {"decision": "SKIP", "reason": "VBHN còn hiệu lực đã có/NLM", "surface": status,
                "actions": ["Dùng VBHN hiện có, không nạp bản rời."]}
    if is_amendment and any("VBHN_IN_FORCE" in str(t.get("status","")).upper() for t in targets):
        return {"decision": "REVIEW", "reason": "Văn bản sửa đổi có VBHN liên quan", "surface": status,
                "actions": ["Đối chiếu VBHN trước khi nạp bản sửa đổi rời."]}
    vb, rejected_vbhn = _redirect_vbhn(current)
    if rejected_vbhn:
        # §1.1 (status): webapp gợi ý VBHN nhưng tên/chủ đề LỆCH bản gốc (goc nhiễm) → KHÔNG tự SKIP/USE_VBHN.
        return {"decision": "REVIEW", "reason": "VBHN được gợi ý nhưng tên/chủ đề lệch văn bản gốc",
                "surface": "VBHN_GOC_SUBJECT_MISMATCH",
                "rejected_vbhn": [str(t.get("sohieu") or "") for t in rejected_vbhn],
                "actions": ["KHÔNG dùng USE_VBHN tự động; chạy `tl source-map <số hiệu> --json` và kiểm goc/cat/tên "
                            "rút gọn trước khi rà (source-map đã có cổng goc-corroboration)."]}
    if vb:
        _vbsh = str(vb.get("sohieu") or "")
        _today = _dt.date.today().isoformat()
        _pend = [str(t.get("sohieu") or "") for t in targets if (_effective_iso(t) or "") > _today]
        return {"decision": "SKIP", "reason": f"Bản gốc đã được hợp nhất — dùng VBHN {_vbsh}",
                "surface": f"USE_VBHN: {_vbsh}", "use_vbhn": _vbsh,
                "caution": "PENDING_AMENDMENT_NOT_IN_VBHN", "pending_amendments": _pend,
                "actions": [f"Dùng VBHN hợp nhất {_vbsh} (đang hiệu lực/đã trên NLM), không nạp bản gốc rời.",
                            f"CHƯA kết luận xong: KIỂM footnote-map/Điều hiệu lực của {_vbsh} có phản ánh ĐỦ sửa đổi HIỆU LỰC TƯƠNG LAI (pending) chưa — VBHN có thể ra đời TRƯỚC sửa đổi pending."
                            + ((" Pending nghi ngờ: " + ", ".join(_pend)) if _pend else "")]}
    if status in ("NOT_FOUND", "MISSING", ""):
        return {"decision": "ADD", "reason": "Chưa thấy trong registry/NLM", "surface": status or "UNKNOWN",
                "actions": ["Có thể nạp, nhưng vẫn cần kiểm số hiệu/tên văn bản."]}
    # §1.8 (log rà): luật MỚI ban hành (vd 74-2025, 134-2025) trường `hieuluc` để TRỐNG → status IN_REGISTRY_HIEULUC_UNKNOWN
    # → REVIEW máy móc dù văn bản rõ ràng còn hiệu lực. Vẫn REVIEW (không tự kết luận) NHƯNG nêu rõ là GAP dữ liệu +
    # gợi ý backfill, và nếu số hiệu mang năm gần đây thì nói rõ "nhiều khả năng còn hiệu lực" để bớt ma sát.
    if "HIEULUC_UNKNOWN" in status:
        yr = _sohieu_year_pg(str(current.get("sohieu") or ""))
        recent = yr is not None and yr >= _dt.date.today().year - 1
        acts = ["Backfill trường `hieuluc` cho dòng này (registry hygiene); đọc Điều hiệu lực thi hành để xác nhận."]
        reason = "Thiếu trường hiệu lực trong registry (gap dữ liệu, không phải lỗi logic)"
        if recent:
            reason += f" — văn bản ban hành {yr}, nhiều khả năng CÒN hiệu lực"
            acts.insert(0, f"Văn bản mới ({yr}): ưu tiên backfill hieuluc cho nhóm luật cùng kỳ họp Quốc hội vừa nạp.")
        return {"decision": "REVIEW", "reason": reason, "surface": status,
                "hieuluc_unknown": True, "recent_issue_year": yr, "actions": acts}
    return {"decision": "REVIEW", "reason": "Trạng thái cần xác minh", "surface": status,
            "actions": ["Kiểm registry/NLM và quyết định thủ công trước khi nạp."]}


def verdict_exit(decision: str, strict: bool=False) -> int:
    """A3 (EXIT CODE doctrine): verdict ADD/SKIP/REVIEW là PHÁT HIỆN dữ liệu, KHÔNG phải lệnh lỗi → rc=0
    (không phá &&/CI; driver agentic không hiểu nhầm REVIEW = lệnh hỏng). Chỉ `--strict` mới rc=1 khi REVIEW
    (mirror `xref --strict`). rc≠0 KHÁC = lệnh THỰC SỰ lỗi (gas/vb_status ném exception → non-zero tự nhiên)."""
    return 1 if (strict and decision == "REVIEW") else 0


def run_live(sohieu: str, targets: list[str] | None, amendment: bool, vbhn: bool, as_json: bool=False, strict: bool=False) -> int:
    sys.path.insert(0, str(HERE))
    import gas  # noqa
    cur = gas.get("vb_status", q=sohieu)
    tstats = [dict(gas.get("vb_status", q=t), sohieu=t) for t in (targets or [])]
    res = decide(cur, tstats, amendment or is_amendment_name(sohieu), vbhn or is_vbhn_name(sohieu))
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"{res['decision']} — {res['reason']} — {res['surface']}")
        for a in res["actions"]:
            print(" -", a)
    return verdict_exit(res["decision"], strict)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("sohieu")
    ap.add_argument("--targets", default="")
    ap.add_argument("--amendment", action="store_true")
    ap.add_argument("--vbhn", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    targets = [t.strip() for t in a.targets.split(",") if t.strip()]
    return run_live(a.sohieu, targets, a.amendment, a.vbhn, a.json, a.strict)


if __name__ == "__main__":
    raise SystemExit(main())
