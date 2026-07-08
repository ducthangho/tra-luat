# -*- coding: utf-8 -*-
"""tl_core.ocr — Pha D (v1.33.57): tách NGUYÊN VĂN từ scripts/tl.py (kế hoạch nợ-kỹ-thuật D).

Public CLI vẫn là scripts/tl.py (stub ủy quyền). Nhận helper dùng chung của tl qua `bind(tl_module)`
(copy-globals, bỏ tên đã có — xem tl_core.workflow docstring). KHÔNG đọc bare mutable-global của tl.
"""
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
import unicodedata  # noqa: F401
import zipfile    # noqa: F401
from pathlib import Path  # noqa: F401

_TL = None


def bind(tl_module) -> None:
    global _TL
    _TL = tl_module
    g = globals()
    for _n in dir(tl_module):
        if _n.startswith("__") or _n in g:
            continue
        g[_n] = getattr(tl_module, _n)



def cmd_ocr_analyze(a) -> int:
    path = Path(a.file)
    out = {"ok": False, "schema": "ocr_analyze.v1", "file": str(path), "engine": "analyze-only", "warnings": [], "recommendations": []}
    if not path.exists():
        out["warnings"].append("FILE_NOT_FOUND")
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    text, warns = _read_local_text_for_analysis(path)
    out["warnings"].extend(warns)
    out["metrics"] = _text_quality_metrics(text)
    ext = path.suffix.lower()
    out["text_layer_detected"] = out["metrics"]["chars"] >= 200
    if ext == ".pdf" and not out["text_layer_detected"]:
        out["recommendations"].append("PDF_SCAN_OR_NO_TEXT_LAYER: run OCR with Drive ocrLanguage=vi or OCRmyPDF vie+eng, then ocr-verify")
    if out["metrics"]["garbled_ratio"] > 0.001:
        out["recommendations"].append("GARBLED_TEXT_REVIEW_REQUIRED")
    if out["metrics"]["vietnamese_mark_density"] < 0.005 and out["metrics"]["letters"] > 500:
        out["recommendations"].append("LOW_VIETNAMESE_MARK_DENSITY_REVIEW_REQUIRED")
    out["ok"] = bool(out["text_layer_detected"] or ext in {".txt", ".md"})
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2


def cmd_ocr_verify(a) -> int:
    path = Path(a.text_file)
    out = {"ok": False, "schema": "ocr_verify.v2", "text_file": str(path), "source": getattr(a, "source", None), "mode": a.mode, "checks": [], "warnings": []}
    if not path.exists():
        out["warnings"].append("TEXT_FILE_NOT_FOUND")
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    text = path.read_text(encoding="utf-8", errors="replace")
    m = _text_quality_metrics(text)
    out["metrics"] = m
    def check(name, ok, detail=""):
        out["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    check("min_length", m["chars"] >= (500 if a.mode == "vbqppl" else 100), str(m["chars"]))
    check("garbled_ratio", m["garbled_ratio"] <= 0.001, str(m["garbled_ratio"]))
    check("vietnamese_mark_density", m["vietnamese_mark_density"] >= 0.005 or m["letters"] < 500, str(m["vietnamese_mark_density"]))
    check("appendix_markers_counted", m.get("appendix_count", 0) >= 0, str(m.get("appendix_count", 0)))
    source = getattr(a, "source", None) or ""
    if source and Path(source).exists():
        pr = _pdf_page_report(Path(source))
        out["page_report"] = pr
        if Path(source).suffix.lower() == ".pdf":
            if pr.get("page_count") is None:
                out["warnings"].append("PAGE_COUNT_UNKNOWN_REVIEW_REQUIRED")
            page_markers = len(re.findall(r"(?im)^\s*(?:page|trang)\s+\d+\s*$", text))
            out["page_coverage"] = {"source_page_count": pr.get("page_count"), "text_page_markers": page_markers, "status": "markers_present" if page_markers else "markers_absent_or_not_extracted"}
    if a.mode == "vbqppl":
        check("article_sequence_present", m["article_count"] > 0, str(m["article_count"]))
        man, man_warns = _load_ocr_manifest_for_text(path)
        out["manifest"] = man or None
        out["warnings"].extend(man_warns)
        man_ok, man_extra_warns, man_checks = _verify_ocr_manifest_contract(man, text_file=path, source=source, mode=a.mode)
        out["warnings"].extend(man_extra_warns)
        out["checks"].extend(man_checks)
        check("vbqppl_manifest_verified_required", man_ok, "OCR VBQPPL canonical requires ocr_manifest.v1 verification")
    else:
        check("text_present", m["chars"] > 100, str(m["chars"]))
        man, man_warns = _load_ocr_manifest_for_text(path)
        if man:
            out["manifest"] = man
            man_ok, man_extra_warns, man_checks = _verify_ocr_manifest_contract(man, text_file=path, source=source, mode=a.mode)
            out["warnings"].extend(man_extra_warns)
            out["checks"].extend(man_checks)
        else:
            out["warnings"].extend(man_warns)
    out["ok"] = all(c["ok"] for c in out["checks"])
    out["recommendation"] = "Có thể dùng --ocr-verified nếu đã đối chiếu bổ sung bằng mắt/nguồn gốc." if out["ok"] else "Không dùng --ocr-verified; cần OCR lại hoặc kiểm thủ công."
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)) if getattr(a, "json", False) or _deterministic_enabled(a) else json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("ok") else 2

# ───────────────────────── OCR run + deterministic chunk apply/verify ─────────────────────────
def _ocr_out_paths(src: Path, out_dir: str | None) -> tuple[Path, Path, Path]:
    base = src.stem
    od = Path(out_dir) if out_dir else (src.parent / f"{base}_ocr_out")
    od.mkdir(parents=True, exist_ok=True)
    return od, od / f"{base}.ocr.txt", od / f"{base}.ocr.pdf"


def _extract_text_layer_to_file(src: Path, dest: Path) -> tuple[bool, list[str], dict]:
    warnings: list[str] = []
    text = ""
    if src.suffix.lower() in {".txt", ".md"}:
        text = src.read_text(encoding="utf-8", errors="replace")
    elif src.suffix.lower() == ".pdf":
        exe = shutil.which("pdftotext")
        if not exe:
            return False, ["PDFTOTEXT_NOT_AVAILABLE"], {}
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out.txt"
            try:
                cp = subprocess.run([exe, "-layout", str(src), str(out)], timeout=60, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if cp.returncode != 0:
                    warnings.append(f"PDFTOTEXT_RC_{cp.returncode}")
                if out.exists():
                    text = out.read_text(encoding="utf-8", errors="replace")
            except Exception as e:  # noqa: BLE001
                return False, [f"PDFTOTEXT_ERROR:{type(e).__name__}:{e}"], {}
    else:
        return False, ["TEXT_LAYER_EXTRACTION_UNSUPPORTED_EXT:" + src.suffix.lower()], {}
    _write_text_atomic(dest, text)
    return bool(text.strip()), warnings, _text_quality_metrics(text)


def _ocr_manifest_path_for_text(text_file: Path) -> Path:
    # foo.ocr.txt -> foo.ocr.manifest.json; fallback -> <stem>.manifest.json
    name = text_file.name
    if name.endswith(".ocr.txt"):
        return text_file.with_name(name[:-4] + ".manifest.json")
    return text_file.with_suffix(text_file.suffix + ".manifest.json")


def _pdf_page_report(src: Path) -> dict:
    if src.suffix.lower() != ".pdf":
        return {"page_count": None, "method": "not_pdf", "ok": True, "warnings": []}
    warnings = []
    exe = shutil.which("pdfinfo")
    if exe:
        try:
            cp = subprocess.run([exe, str(src)], timeout=20, check=False, text=True, capture_output=True)
            m = re.search(r"(?im)^Pages:\s*(\d+)", cp.stdout or "")
            if m:
                return {"page_count": int(m.group(1)), "method": "pdfinfo", "ok": True, "warnings": []}
            warnings.append("PDFINFO_PAGES_NOT_FOUND")
        except Exception as e:  # noqa: BLE001
            warnings.append(f"PDFINFO_ERROR:{type(e).__name__}")
    try:
        raw = src.read_bytes()[:20_000_000]
        # Approximation fallback only. Good enough for warning when pdfinfo absent.
        n = len(re.findall(rb"/Type\s*/Page\b", raw))
        return {"page_count": (n or None), "method": "pdf_page_token_scan", "ok": bool(n), "warnings": warnings + ([] if n else ["PDF_PAGE_COUNT_UNKNOWN"])}
    except Exception as e:  # noqa: BLE001
        return {"page_count": None, "method": "fallback_failed", "ok": False, "warnings": warnings + [f"PDF_PAGE_COUNT_ERROR:{type(e).__name__}"]}


def _ocr_engine_version(engine: str) -> str:
    if engine == "none":
        return "text-layer-extract"
    exe = shutil.which(engine) if engine in {"ocrmypdf", "tesseract"} else None
    if not exe:
        return "unknown"
    try:
        cp = subprocess.run([exe, "--version"], timeout=10, check=False, text=True, capture_output=True)
        first = ((cp.stdout or cp.stderr or "").splitlines() or [""])[0].strip()
        return first[:120] or "unknown"
    except Exception:
        return "unknown"


def _ocr_manifest_build(*, src: Path, text_file: Path, engine_used: str, engine_requested: str, lang: str, mode: str, ocr_pdf: Path | None, metrics: dict, verify: dict | None, warnings: list[str]) -> dict:
    text_hash = _sha256_bytes_file_local(text_file) if text_file.exists() else ""
    source_hash = _sha256_bytes_file_local(src) if src.exists() else ""
    page_report = _pdf_page_report(src)
    coverage = {
        "source_page_count": page_report.get("page_count"),
        "page_count_method": page_report.get("method"),
        "text_has_page_markers": bool(re.search(r"(?im)^\s*(?:page|trang)\s+\d+\s*$", text_file.read_text(encoding="utf-8", errors="replace")[:1_000_000] if text_file.exists() else "")),
        "page_coverage_status": "unknown" if page_report.get("page_count") else "not_available",
    }
    if coverage["source_page_count"] and coverage["text_has_page_markers"]:
        coverage["page_coverage_status"] = "has_page_markers"
    elif coverage["source_page_count"]:
        coverage["page_coverage_status"] = "page_count_known_text_markers_absent"
    verification_ok = bool((verify or {}).get("ok"))
    status = "verified" if verification_ok else "unverified"
    return {
        "ok": verification_ok,
        "schema": "ocr_manifest.v1",
        "mode": mode,
        "source_file": str(src),
        "source_sha256": source_hash,
        "source_size_bytes": src.stat().st_size if src.exists() else None,
        "text_file": str(text_file),
        "text_sha256": text_hash,
        "text_size_bytes": text_file.stat().st_size if text_file.exists() else None,
        "engine_requested": engine_requested,
        "engine_used": engine_used,
        "engine_version": _ocr_engine_version(engine_used),
        "language": lang,
        "outputs": {"text_file": str(text_file), "ocr_pdf": str(ocr_pdf) if ocr_pdf and ocr_pdf.exists() else None},
        "page_report": page_report,
        "page_coverage": coverage,
        "metrics": metrics or {},
        "verification_status": status,
        "verification": verify or {},
        "warnings": list(warnings or []) + list(page_report.get("warnings") or []),
        "canonical_allowed": bool(verification_ok and mode != "vbqppl") or bool(verification_ok and mode == "vbqppl"),
        "volatile": {"created_at_utc": "<created_at_runtime>"},
    }


def _load_ocr_manifest_for_text(text_file: Path) -> tuple[dict | None, list[str]]:
    candidates = [_ocr_manifest_path_for_text(text_file), text_file.with_suffix(text_file.suffix + ".manifest.json")]
    seen = set()
    for mp in candidates:
        if str(mp) in seen:
            continue
        seen.add(str(mp))
        if mp.exists():
            try:
                _man = json.loads(mp.read_text(encoding="utf-8", errors="replace"))
            except Exception as e:  # noqa: BLE001
                return None, [f"OCR_MANIFEST_INVALID:{type(e).__name__}"]
            if not isinstance(_man, dict):   # v1.33.56 (PH2-06): JSON string/list/number → không crash .get
                return None, ["OCR_MANIFEST_INVALID:NOT_A_JSON_OBJECT"]
            return _man, []
    return None, ["OCR_MANIFEST_NOT_FOUND"]


def _verify_ocr_manifest_contract(man: dict | None, *, text_file: Path, source: str = "", mode: str = "profile") -> tuple[bool, list[str], list[dict]]:
    warnings: list[str] = []
    checks: list[dict] = []
    def check(name: str, ok: bool, detail: str = ""):
        checks.append({"name": name, "ok": bool(ok), "detail": detail})
    if not man:
        check("manifest_present", False, "missing")
        return False, warnings, checks
    check("manifest_schema", man.get("schema") == "ocr_manifest.v1", str(man.get("schema")))
    check("manifest_text_file_matches", Path(str(man.get("text_file") or "")).name == text_file.name, str(man.get("text_file") or ""))
    if text_file.exists() and man.get("text_sha256"):
        h = _sha256_bytes_file_local(text_file)
        check("manifest_text_hash_matches", h == man.get("text_sha256"), h[:12])
    else:
        check("manifest_text_hash_present", bool(man.get("text_sha256")), str(man.get("text_sha256") or ""))
    if source:
        src = Path(source)
        if src.exists() and man.get("source_sha256"):
            h = _sha256_bytes_file_local(src)
            check("manifest_source_hash_matches", h == man.get("source_sha256"), h[:12])
        else:
            warnings.append("SOURCE_HASH_CHECK_SKIPPED")
    check("manifest_verification_status", man.get("verification_status") == "verified", str(man.get("verification_status")))
    if mode == "vbqppl":
        pr = man.get("page_report") or {}
        if pr.get("method") != "not_pdf":
            if pr.get("page_count") is None:
                warnings.append("VBQPPL_PAGE_COUNT_UNKNOWN_REVIEW_REQUIRED")
            cov = (man.get("page_coverage") or {}).get("page_coverage_status")
            if cov in {"not_available", "unknown"}:
                warnings.append("VBQPPL_PAGE_COVERAGE_UNKNOWN_REVIEW_REQUIRED")
    return all(c.get("ok") for c in checks), warnings, checks


def cmd_ocr_run(a) -> int:
    """OCR/extract local sidecar text. Safe phase: local files only; Drive/Paddle/DocumentAI engines are guarded unless available."""
    src = Path(a.file)
    out = {"ok": False, "schema": "ocr_run.v1", "file": str(src), "engine_requested": a.engine, "warnings": [], "outputs": {}, "verify": None}
    if not src.exists():
        out["warnings"].append("FILE_NOT_FOUND")
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    od, sidecar, ocr_pdf = _ocr_out_paths(src, getattr(a, "out_dir", None))
    out["outputs"]["out_dir"] = str(od)
    engine = a.engine
    if engine == "auto":
        text, warns = _read_local_text_for_analysis(src)
        out["warnings"].extend(warns)
        metrics = _text_quality_metrics(text)
        if src.suffix.lower() in {".txt", ".md"} and metrics.get("chars", 0) > 0:
            engine = "none"
        elif metrics.get("chars", 0) >= 200:
            engine = "none"
        elif shutil.which("ocrmypdf") and src.suffix.lower() == ".pdf":
            engine = "ocrmypdf"
        else:
            out["engine_used"] = "none"
            out["warnings"].append("NO_TEXT_LAYER_AND_NO_LOCAL_OCR_ENGINE")
            out["recommendations"] = [
                "Cài OCRmyPDF + Tesseract vie để chạy local: ocr-run --engine ocrmypdf --lang vie+eng",
                "Hoặc dùng Drive OCR với ocrLanguage=vi trong pipeline Drive live rồi chạy ocr-verify trên sidecar text.",
                "Không dùng OCR chưa verify làm canonical VBQPPL.",
            ]
            print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    out["engine_used"] = engine
    if engine == "none":
        ok, warns, metrics = _extract_text_layer_to_file(src, sidecar)
        out["warnings"].extend(warns)
        out["outputs"]["text_file"] = str(sidecar)
        out["metrics"] = metrics
        out["ok"] = bool(ok and metrics.get("chars", 0) >= 1)
    elif engine == "ocrmypdf":
        if src.suffix.lower() != ".pdf":
            out["warnings"].append("OCRMYPDF_REQUIRES_PDF")
            print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
        exe = shutil.which("ocrmypdf")
        if not exe:
            out["warnings"].append("OCRMYPDF_NOT_AVAILABLE")
            out["recommendations"] = ["Cài ocrmypdf và tesseract language pack vie, hoặc dùng engine drive/paddle ngoài CLI local."]
            print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
        cmd = [exe, "--language", a.lang or "vie+eng", "--sidecar", str(sidecar), str(src), str(ocr_pdf)]
        if getattr(a, "force_ocr", False):
            cmd.insert(1, "--force-ocr")
        try:
            cp = subprocess.run(cmd, timeout=getattr(a, "timeout", 600), check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out["returncode"] = cp.returncode
            out["stdout_tail"] = cp.stdout.decode("utf-8", "replace")[-1200:]
            out["stderr_tail"] = cp.stderr.decode("utf-8", "replace")[-1200:]
            out["outputs"]["text_file"] = str(sidecar)
            out["outputs"]["ocr_pdf"] = str(ocr_pdf)
            if sidecar.exists():
                txt = sidecar.read_text(encoding="utf-8", errors="replace")
                out["metrics"] = _text_quality_metrics(txt)
            out["ok"] = (cp.returncode == 0 and sidecar.exists() and out.get("metrics", {}).get("chars", 0) > 0)
        except Exception as e:  # noqa: BLE001
            out["warnings"].append(f"OCRMYPDF_ERROR:{type(e).__name__}:{e}")
            out["ok"] = False
    elif engine in {"drive", "paddle", "documentai"}:
        out["warnings"].append(f"ENGINE_{engine.upper()}_NOT_ENABLED_IN_LOCAL_STAGE3")
        out["recommendations"] = [
            "Stage 3 chỉ mở local sidecar/text-layer an toàn. Engine này cần plugin live/config riêng.",
            "Dùng route-task --task ocr_pdf_scan để xem workflow; sau khi tạo text sidecar thì chạy ocr-verify.",
        ]
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    else:
        out["warnings"].append("UNKNOWN_ENGINE")
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    if out.get("outputs", {}).get("text_file") and Path(out["outputs"]["text_file"]).exists():
        class _A: pass
        va = _A(); va.text_file = out["outputs"]["text_file"]; va.source = str(src); va.mode = a.mode; va.json = True
        txt = Path(va.text_file).read_text(encoding="utf-8", errors="replace")
        m = _text_quality_metrics(txt)
        checks = []
        def check(name, ok, detail=""):
            checks.append({"name": name, "ok": bool(ok), "detail": detail})
        check("min_length", m["chars"] >= (500 if a.mode == "vbqppl" else 100), str(m["chars"]))
        check("garbled_ratio", m["garbled_ratio"] <= 0.001, str(m["garbled_ratio"]))
        check("vietnamese_mark_density", m["vietnamese_mark_density"] >= 0.005 or m["letters"] < 500, str(m["vietnamese_mark_density"]))
        if a.mode == "vbqppl":
            check("article_sequence_present", m["article_count"] > 0, str(m["article_count"]))
        else:
            check("text_present", m["chars"] > 100, str(m["chars"]))
        out["verify"] = {"schema": "ocr_verify.inline.v1", "mode": a.mode, "metrics": m, "checks": checks, "ok": all(c["ok"] for c in checks)}
        if not out["verify"]["ok"]:
            out.setdefault("warnings", []).append("OCR_VERIFY_NOT_OK")
        manifest = _ocr_manifest_build(src=src, text_file=Path(out["outputs"]["text_file"]), engine_used=out.get("engine_used") or engine, engine_requested=a.engine, lang=a.lang or "vi", mode=a.mode, ocr_pdf=ocr_pdf, metrics=m, verify=out.get("verify"), warnings=out.get("warnings", []))
        manifest_path = _ocr_manifest_path_for_text(Path(out["outputs"]["text_file"]))
        _write_text_atomic(manifest_path, json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
        out["outputs"]["manifest"] = str(manifest_path)
        out["manifest"] = {k: manifest.get(k) for k in ("schema", "ok", "verification_status", "source_sha256", "text_sha256", "engine_used", "engine_version", "language", "page_report", "page_coverage", "canonical_allowed")}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)) if getattr(a, "json", False) or _deterministic_enabled(a) else json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("ok") else 2

# ───────────────────────── Stage 4 bridges: verified OCR/chunks -> existing ingest pipelines ─────────────────────────
def _bridge_common_ocr_verify(text_file: str, *, mode: str, source: str = "") -> dict:
    """Run ocr-verify as a child command and return its JSON envelope."""
    args = ["ocr-verify", text_file, "--mode", mode, "--json"]
    if source:
        args += ["--source", source]
    return _run_child_tl(args)


def _bridge_ocr_plan(a, *, mode: str) -> dict:
    verify = _bridge_common_ocr_verify(a.text_file, mode=mode, source=getattr(a, "file", "") or "")
    source = Path(a.file)
    text = Path(a.text_file)
    out = {
        "ok": bool(verify.get("ok")),
        "schema": "ocr_ingest_bridge.v1",
        "mode": mode,
        "file": str(source),
        "text_file": str(text),
        "apply": bool(getattr(a, "apply", False)),
        "verification": verify,
        "warnings": [],
        "planned_child_command": [],
        "note": "Bridge không ghi trực tiếp; apply chỉ gọi lại ingest-local/profile-ingest hiện có với --source-quality ocr --ocr-verified.",
        "idempotency": _idempotency_contract_for_workflow("ocr_ingest"),
    }
    if not source.exists():
        out["ok"] = False; out["warnings"].append("SOURCE_FILE_NOT_FOUND")
    if not text.exists():
        out["ok"] = False; out["warnings"].append("TEXT_FILE_NOT_FOUND")
    man = ((verify.get("json") or {}).get("manifest") if isinstance(verify.get("json"), dict) else None)
    if mode == "vbqppl" and not (isinstance(man, dict) and man.get("verification_status") == "verified"):
        out["ok"] = False
        out["warnings"].append("VBQPPL_OCR_REQUIRES_VERIFIED_MANIFEST")
    if mode == "vbqppl":
        if not getattr(a, "cat", None):
            out["ok"] = False; out["warnings"].append("CAT_REQUIRED_FOR_VBQPPL_OCR_INGEST")
        child = ["ingest-local", str(source), "--text-file", str(text), "--source-quality", "ocr", "--ocr-verified", "--auto-plan", "--json"]
        for opt in ("name", "sohieu", "cat", "goc", "hieuluc", "loai"):
            val = getattr(a, opt, None)
            if val:
                child += ["--" + opt.replace("_", "-"), str(val)]
        for flag in ("force_cat", "allow_large", "skip_nlm_preflight", "skip_live_check"):
            if getattr(a, flag, False):
                child.append("--" + flag.replace("_", "-"))
    else:
        child = ["profile-ingest", str(source), "--text-file", str(text), "--source-quality", "ocr", "--ocr-verified", "--json"]
        for opt in ("name", "hieuluc"):
            val = getattr(a, opt, None)
            if val:
                child += ["--" + opt.replace("_", "-"), str(val)]
        if getattr(a, "chunk_max_chars", None):
            child += ["--chunk-max-chars", str(a.chunk_max_chars)]
        for flag in ("allow_default", "skip_live_check"):
            if getattr(a, flag, False):
                child.append("--" + flag.replace("_", "-"))
        prof = getattr(a, "profile", None)
        if prof:
            child += ["--profile", prof]
    if getattr(a, "apply", False):
        child.append("--apply")
    out["planned_child_command"] = child
    return out


def cmd_ingest_ocr(a) -> int:
    ok, err = _bridge_confirm_apply(a, what="ingest-ocr")
    if not ok:
        print(_json_dumps(err, deterministic=_deterministic_enabled(a))); return 2
    plan = _bridge_ocr_plan(a, mode="vbqppl")
    if not getattr(a, "apply", False):
        print(_json_dumps(plan, deterministic=_deterministic_enabled(a))); return 0 if plan.get("ok") else 2
    if not plan.get("ok"):
        print(_json_dumps(plan, deterministic=_deterministic_enabled(a))); return 2
    child = _run_child_tl(plan["planned_child_command"])
    out = {**plan, "child_result": child, "ok": bool(child.get("ok")), "schema": "ocr_ingest_bridge_apply.v1"}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2


def cmd_profile_ingest_ocr(a) -> int:
    ok, err = _bridge_confirm_apply(a, what="profile-ingest-ocr")
    if not ok:
        print(_json_dumps(err, deterministic=_deterministic_enabled(a))); return 2
    plan = _bridge_ocr_plan(a, mode="profile")
    if not getattr(a, "apply", False):
        print(_json_dumps(plan, deterministic=_deterministic_enabled(a))); return 0 if plan.get("ok") else 2
    if not plan.get("ok"):
        print(_json_dumps(plan, deterministic=_deterministic_enabled(a))); return 2
    child = _run_child_tl(plan["planned_child_command"])
    out = {**plan, "child_result": child, "ok": bool(child.get("ok")), "schema": "ocr_ingest_bridge_apply.v1"}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2
