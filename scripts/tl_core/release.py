# -*- coding: utf-8 -*-
"""tl_core.release — Pha C (v1.33.56): tách NGUYÊN VĂN từ scripts/tl.py (kế hoạch nợ-kỹ-thuật C2).

KHÔNG gọi trực tiếp từ ngoài — public CLI vẫn là scripts/tl.py (stub ủy quyền). Module nhận các helper
dùng chung của tl qua `bind(tl_module)`: copy MỌI tên public/private của tl vào globals() TRỪ tên đã có
(def riêng của module thắng; tên thuộc module anh em resolve qua STUB đã định nghĩa trong tl trước bind).
Hàm tl là hàm THẬT (đọc global của tl lúc gọi) nên không stale; module KHÔNG đọc bare mutable-global của tl.
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



def _determinism_audit(*, strict: bool = False, full: bool = False) -> dict:
    checks = []

    def add(name: str, ok: bool, detail="", **extra):
        rec = {"name": name, "ok": bool(ok), "detail": detail}
        rec.update(extra)
        checks.append(rec)

    try:
        wa = _workflow_cards_audit()
        add(
            "workflow_card_schema",
            bool(wa.get("ok")) and (not strict or not wa.get("warnings")),
            f"cards={wa.get('summary', {}).get('cards')} warnings={len(wa.get('warnings', []))}",
            errors=wa.get("errors"),
            warnings=wa.get("warnings")[:20],
        )
    except Exception as e:  # noqa: BLE001
        add("workflow_card_schema", False, f"{type(e).__name__}: {e}")

    try:
        rm1 = _build_release_manifest(HERE.parent)
        rm2 = _build_release_manifest(HERE.parent)
        stable = rm1.get("package_hash") == rm2.get("package_hash") and rm1.get("file_count") == rm2.get("file_count")
        add("release_manifest_stable", stable and bool(rm1.get("ok")), f"files={rm1.get('file_count')} package_hash={rm1.get('package_hash')}", required_missing=rm1.get("required_missing"))
    except Exception as e:  # noqa: BLE001
        add("release_manifest_stable", False, f"{type(e).__name__}: {e}")

    smoke_cases = [
        ["route-task", "--task", "ingest_zip", "--json"],
        ["nlm-query-plan", "Trích Điều 1 của văn bản mẫu", "--source-id", "src_A", "--source-id", "src_B", "--json"],
        ["workflow-audit", "--json"],
    ]
    for args in smoke_cases:
        r1 = _run_tl_json(args)
        r2 = _run_tl_json(args)
        if not (r1.get("ok") and r2.get("ok")):
            add(f"deterministic_child:{args[0]}", False, "child command failed", first={"returncode": r1.get("returncode"), "stderr_tail": r1.get("stderr_tail")}, second={"returncode": r2.get("returncode"), "stderr_tail": r2.get("stderr_tail")})
            continue
        t1 = _json_dumps(r1.get("data"), deterministic=True)
        t2 = _json_dumps(r2.get("data"), deterministic=True)
        same = t1 == t2
        add(f"deterministic_child:{args[0]}", same, "stdout JSON stable across two runs", sha256=hashlib.sha256(t1.encode("utf-8")).hexdigest(), diff={} if same else _first_text_diff(t1, t2))

    scrub_probe = {
        "path": str(HERE.parent / "SKILL.md"),
        "out_dir": str(Path(tempfile.gettempdir()) / "tl_probe_random"),
        "seconds": 12.345,
    }
    scrubbed = _scrub_volatile(scrub_probe)
    add("volatile_scrub_contract", scrubbed.get("path") == "SKILL.md" and scrubbed.get("out_dir") == "<volatile>" and scrubbed.get("seconds") == "<volatile>", json.dumps(scrubbed, ensure_ascii=False))

    if strict or full:
        try:
            gt = _golden_test(write=False)
            add("golden_test", bool(gt.get("ok")), f"cases={gt.get('case_count')}", cases=gt.get("cases"))
        except Exception as e:  # noqa: BLE001
            add("golden_test", False, f"{type(e).__name__}: {e}")

    if strict or full:
        with tempfile.TemporaryDirectory(prefix="tl_det_audit_") as td:
            tdp = Path(td)
            # Snapshot deterministic stability, including generatedEpoch in volatile.
            s1 = _run_tl_json(["live-state-snapshot", "--no-contract", "--out", str(tdp / "before1.json"), "--json"], timeout=90)
            s2 = _run_tl_json(["live-state-snapshot", "--no-contract", "--out", str(tdp / "before2.json"), "--json"], timeout=90)
            if s1.get("ok") and s2.get("ok"):
                t1 = _json_dumps(s1.get("data"), deterministic=True)
                t2 = _json_dumps(s2.get("data"), deterministic=True)
                add("live_state_snapshot_stable", t1 == t2, "snapshot JSON stable across two deterministic runs", diff={} if t1 == t2 else _first_text_diff(t1, t2))
            else:
                add("live_state_snapshot_stable", False, "snapshot child command failed", first={"rc": s1.get("returncode"), "stderr_tail": s1.get("stderr_tail")}, second={"rc": s2.get("returncode"), "stderr_tail": s2.get("stderr_tail")})
            diff = _run_tl_json(["live-state-diff", str(tdp / "before1.json"), str(tdp / "before2.json"), "--json"], timeout=60)
            add("live_state_diff_no_unexpected", bool(diff.get("ok")) and not ((diff.get("data") or {}).get("unexpected_changes")), "diff between two equivalent snapshots has no unexpected changes", diff=(diff.get("data") or {}))

            sample = tdp / "sample_abs.txt"
            sample.write_text("Điều 1. Mẫu kiểm thử deterministic.\n" + ("Nội dung tiếng Việt có dấu để đủ mật độ. " * 20), encoding="utf-8")
            oa = _run_tl_json(["ocr-analyze", str(sample), "--json"], timeout=60)
            od = _json_dumps(oa.get("data"), deterministic=True) if oa.get("data") else ""
            add("ocr_analyze_path_scrub", bool(oa.get("ok")) and str(sample) not in od and "<tmp>" in od, "absolute tmp path scrubbed from deterministic ocr-analyze output")
            cp = _run_tl_json(["chunk-plan", str(sample), "--mode", "profile", "--json"], timeout=60)
            cd = _json_dumps(cp.get("data"), deterministic=True) if cp.get("data") else ""
            add("chunk_plan_path_scrub", bool(cp.get("ok")) and str(sample) not in cd and "<tmp>" in cd, "absolute tmp path scrubbed from deterministic chunk-plan output")

            # Same zip contents with different member order must produce same dry-run plan after scrub.
            # Use in-process _zip_plan here to avoid nested CLI fan-out during strict audit; CLI path is covered by golden/smoke cases.
            z1, z2 = tdp / "a.zip", tdp / "b.zip"
            fitems = {"b.txt": "B", "a.txt": "A"}
            for zp, order in [(z1, ["b.txt", "a.txt"]), (z2, ["a.txt", "b.txt"])]:
                with zipfile.ZipFile(zp, "w") as zf:
                    for name in order:
                        zf.writestr(name, fitems[name])
            zp1 = _zip_plan(str(z1), mode="vbqppl", cat="01")
            zp2 = _zip_plan(str(z2), mode="vbqppl", cat="01")
            zi1 = [(i.get("normalized_path"), i.get("status"), i.get("reason")) for i in (zp1.get("items") or [])]
            zi2 = [(i.get("normalized_path"), i.get("status"), i.get("reason")) for i in (zp2.get("items") or [])]
            add("zip_member_order_stable", bool(zp1.get("ok") and zp2.get("ok")) and zi1 == zi2 and [x[0] for x in zi1] == sorted([x[0] for x in zi1]), f"items={zi1}")

            zdup = tdp / "dup.zip"
            with zipfile.ZipFile(zdup, "w") as zf:
                zf.writestr("a.txt", "one")
                zf.writestr("./a.txt", "two")
            zdata = _zip_plan(str(zdup), mode="vbqppl", cat="01")
            add("zip_duplicate_normalized_guard", bool(zdata.get("errors")) and any("DUPLICATE_NORMALIZED_ZIP_PATH" in str(e) for e in zdata.get("errors", [])), "duplicate normalized zip paths rejected", errors=zdata.get("errors"))

            rm_before = _build_release_manifest(HERE.parent)
            # v1.33.56 (review F3): KHÔNG mượn before.json (file baseline THẬT của user theo deploy-plan;
            # bị kill giữa write→restore là mất). Probe tên riêng đã EXCLUDE, từ chối nếu tồn tại; leftover
            # sau kill vô hại vì excluded.
            runtime_art = HERE.parent / ".__det_audit_probe__.json"
            if runtime_art.exists():
                add("release_manifest_ignores_runtime_artifacts", False,
                    "probe file đã tồn tại (lần chạy trước bị kill?) — xoá .__det_audit_probe__.json rồi chạy lại")
            else:
                try:
                    runtime_art.write_text("{\"runtime\": true}\n", encoding="utf-8")
                    rm_after = _build_release_manifest(HERE.parent)
                    add("release_manifest_ignores_runtime_artifacts",
                        rm_before.get("package_hash") == rm_after.get("package_hash")
                        and rm_before.get("file_count") == rm_after.get("file_count")
                        and not _release_should_include(runtime_art, HERE.parent),
                        f"before={rm_before.get('package_hash')} after={rm_after.get('package_hash')}")
                finally:
                    try: runtime_art.unlink()
                    except FileNotFoundError: pass

    ok = all(c.get("ok") for c in checks)
    return {"ok": ok, "schema": "determinism_audit.v1", "strict": bool(strict), "full": bool(full), "checks": checks}


def cmd_determinism_audit(a) -> int:
    out = _determinism_audit(strict=bool(getattr(a, "strict", False)), full=bool(getattr(a, "full", False)))
    if not out.get("ok"):
        # v1.33.56: flake 'ok:false 1 lần không tái hiện' đã xảy ra 2 lần mà không giữ được JSON đầy đủ →
        # tự lưu report (đường reports/ + tên file ĐÃ được release-manifest exclude sẵn) để lần sau có diff.
        try:
            _rp = HERE.parent / "reports"
            _rp.mkdir(parents=True, exist_ok=True)
            _write_text_atomic(_rp / "determinism_report.json", json.dumps(out, ensure_ascii=False, indent=2))
            print("[tl] determinism-audit FAIL → report đầy đủ: reports/determinism_report.json "
                  "(xem checks[].diff để biết đường lệch)", file=sys.stderr)
        except Exception as _e:  # noqa: BLE001
            print(f"[tl] determinism-audit: không lưu được report ({_e})", file=sys.stderr)
    _print_json_or_text(out, getattr(a, "json", False))
    return 0 if out.get("ok") else 2


def cmd_release_check(a) -> int:
    """Offline deterministic acceptance harness. No subprocess, no Drive/NLM writes."""
    out_dir = Path(getattr(a, "out_dir", None) or tempfile.mkdtemp(prefix="tl_release_check_"))
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    def add(name: str, ok: bool, detail="", **extra):
        rec = {"name": name, "ok": bool(ok), "detail": detail}
        rec.update(extra)
        results.append(rec)

    try:
        import py_compile
        py_compile.compile(str(HERE / "tl.py"), doraise=True)
        py_compile.compile(str(HERE / "gen_instructions.py"), doraise=True)
        for _mod in ["__init__.py", "deterministic.py", "jsonio.py", "workflow.py", "release.py", "live.py", "zip_ingest.py", "ocr.py", "chunking.py"]:
            py_compile.compile(str(HERE / "tl_core" / _mod), doraise=True)
        add("py_compile", True, "scripts/tl.py + scripts/gen_instructions.py + scripts/tl_core/*.py")
    except Exception as e:  # noqa: BLE001
        add("py_compile", False, f"{type(e).__name__}: {e}")

    try:
        gi = _imp("gen_instructions")
        project = gi.generate("project", VERSION)
        nlm = gi.generate("nlm", VERSION)
        pa = gi.audit(project, "project")
        na = gi.audit(nlm, "nlm")
        add("instruction_project_audit", bool(pa.get("ok")), json.dumps(pa, ensure_ascii=False)[:500])
        add("instruction_nlm_audit", bool(na.get("ok")), json.dumps(na, ensure_ascii=False)[:500])
        if getattr(a, "full", False):
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = gi.selftest()
            add("gen_instructions_selftest", rc == 0, buf.getvalue()[-800:])
    except Exception as e:  # noqa: BLE001
        add("gen_instructions_import_or_audit", False, f"{type(e).__name__}: {e}")

    try:
        wa = _workflow_cards_audit()
        add("workflow_audit", bool(wa.get("ok")), json.dumps(wa.get("summary", {}), ensure_ascii=False), errors=wa.get("errors"), warnings=wa.get("warnings")[:10])
    except Exception as e:  # noqa: BLE001
        add("workflow_audit", False, f"{type(e).__name__}: {e}")

    if getattr(a, "strict_determinism", False):
        try:
            da = _determinism_audit(strict=True, full=False)
            failed = [c for c in da.get("checks", []) if not c.get("ok")]
            add("determinism_audit", bool(da.get("ok")), f"checks={len(da.get('checks', []))} failed={len(failed)}", failed=failed[:5])
        except Exception as e:  # noqa: BLE001
            add("determinism_audit", False, f"{type(e).__name__}: {e}")

    for task in ["write_new_tool", "ingest_local", "ingest_zip", "ocr_ingest", "profile_ingest_ocr", "profile_ingest_chunks", "convert_rename", "ocr_pdf_scan", "large_doc_chunk", "workflow_audit", "determinism_audit", "golden_test", "release_check", "live_readiness", "live_contract_check", "live_state_snapshot", "live_state_diff", "live_smoke_plan", "deploy_plan", "rollback_plan", "final_acceptance", "go_live_runbook"]:
        try:
            wf_id = _TASK_TO_WORKFLOW.get(task, task)
            card = _load_workflow_card(wf_id)
            add(f"route_task:{task}", bool(card.get("ok", True)), f"workflow={wf_id} risk={card.get('risk')}")
        except Exception as e:  # noqa: BLE001
            add(f"route_task:{task}", False, f"{type(e).__name__}: {e}")

    sample = out_dir / "sample_vb.txt"
    sample.write_text(("Điều 1. Phạm vi điều chỉnh\nVăn bản này dùng để kiểm thử.\n\nĐiều 2. Đối tượng áp dụng\nCơ quan, tổ chức, cá nhân có liên quan.\n") * 6, encoding="utf-8")
    try:
        text, warns = _read_local_text_for_analysis(sample)
        m = _text_quality_metrics(text)
        add("ocr_text_quality_metrics", m.get("chars", 0) > 100 and m.get("article_count", 0) >= 2, json.dumps(m, ensure_ascii=False), warnings=warns)
        class _OA: pass
        oa = _OA(); oa.file = str(sample); oa.engine = "none"; oa.lang = "vi"; oa.mode = "vbqppl"; oa.out_dir = str(out_dir / "ocr_sidecar"); oa.force_ocr = False; oa.timeout = 60; oa.json = True; oa.deterministic = True
        # Exercise manifest writer without relying on external OCR engines. Capture stdout to keep release JSON clean.
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_ocr = cmd_ocr_run(oa)
        ocr_payload = json.loads(buf.getvalue())
        _od, _sidecar, _ocr_pdf = _ocr_out_paths(sample, str(out_dir / "ocr_sidecar"))
        manifest_path = _ocr_manifest_path_for_text(_sidecar)
        add("ocr_manifest_sidecar", rc_ocr == 0 and manifest_path.exists(), str(manifest_path))
        va = _OA(); va.text_file = str(_sidecar); va.source = str(sample); va.mode = "vbqppl"; va.json = True; va.deterministic = True
        buf2 = io.StringIO()
        with contextlib.redirect_stdout(buf2):
            rc_ver = cmd_ocr_verify(va)
        ver_payload = json.loads(buf2.getvalue())
        add("ocr_verify_manifest_contract", rc_ver == 0 and bool(ver_payload.get("ok")), json.dumps({"checks": len(ver_payload.get("checks", [])), "warnings": ver_payload.get("warnings", [])}, ensure_ascii=False))
    except Exception as e:  # noqa: BLE001
        add("ocr_text_quality_metrics", False, f"{type(e).__name__}: {e}")

    try:
        text = sample.read_text(encoding="utf-8")
        plan = _chunk_plan_from_text(text, name="sample_vb", mode="profile", max_chars=80)
        add("chunk_plan_profile", bool(plan.get("ok")) and plan.get("chunk_count", 0) >= 2, f"chunks={plan.get('chunk_count')} strategy={plan.get('strategy')}")
        guard = _chunk_plan_from_text(text, name="sample_vb", mode="vbqppl-canonical", max_chars=80)
        add("chunk_plan_vbqppl_canonical_guard", not guard.get("ok") and guard.get("error") == "DO_NOT_SPLIT_VBQPPL_CANONICAL", guard.get("error"))
    except Exception as e:  # noqa: BLE001
        add("chunk_plan", False, f"{type(e).__name__}: {e}")

    try:
        rm = _build_release_manifest(HERE.parent)
        add("release_manifest", bool(rm.get("ok")) and rm.get("file_count", 0) > 0, f"files={rm.get('file_count')} package_hash={rm.get('package_hash')}", required_missing=rm.get("required_missing"))
        rv = _verify_release_manifest(HERE.parent, rm, strict=False)
        add("release_verify_self", bool(rv.get("ok")) and bool(rv.get("package_hash_match")), f"checked={rv.get('checked_file_count')} match={rv.get('package_hash_match')}", failed=rv.get("failed"))
        lr = _live_readiness_report(profile=getattr(a, "profile", None) or "", include_ocr=True)
        add("live_readiness_report", bool(lr.get("ok")) and "checks" in lr, f"ready={lr.get('ready_for_live_smoke')} checks={len(lr.get('checks', []))}")
        lp = _live_smoke_plan(profile=getattr(a, "profile", None) or "", include_ocr=True)
        add("live_smoke_plan", bool(lp.get("ok")) and len(lp.get("steps", [])) >= 8, f"steps={len(lp.get('steps', []))}")
        dp = _deploy_plan(profile=getattr(a, "profile", None) or "", include_ocr=True)
        add("deploy_plan", bool(dp.get("ok")) and len(dp.get("steps", [])) >= 6, f"steps={len(dp.get('steps', []))}")
        rp = _rollback_plan()
        add("rollback_plan", bool(rp.get("ok")) and len(rp.get("steps", [])) >= 4, f"steps={len(rp.get('steps', []))}")
    except Exception as e:  # noqa: BLE001
        add("live_smoke_plan", False, f"{type(e).__name__}: {e}")

    ok = all(r.get("ok") for r in results)
    report = {"ok": ok, "schema": "release_check.v2", "mode": "in_process_offline", "full": bool(getattr(a, "full", False)), "strict_determinism": bool(getattr(a, "strict_determinism", False)), "out_dir": str(out_dir), "results": results,
              "note": "Offline only: không gọi Drive/NLM, không ghi registry. Dùng live-smoke-plan cho test live có auth."}
    report_path = out_dir / "release_check_report.json"
    _write_text_atomic(report_path, _json_dumps(report))
    if getattr(a, "out", None):
        _write_text_atomic(Path(a.out), _json_dumps(report))
    _print_json_or_text(report, getattr(a, "json", False))
    return 0 if ok else 2

# ───────────────────────── release/package integrity ─────────────────────────
_RELEASE_EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules", ".tl_state", "tmp", "reports", "dist",
                         ".claude", ".githooks"}   # v1.33.54: dev-side (không vào zip skill — upload script cũng strip)

_RELEASE_EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".tmp", ".bak", ".swp", ".enc"}   # v1.33.54: +.enc (secrets mã hoá local)

# v1.33.54: file local-only MỌI CẤP — config THẬT (chứa webappUrl/token) + CLAUDE.md dev. Phát hiện khi regen
# manifest trên dev-tree: walk thư mục (không phải git ls-files) đã liệt kê + hash tra_luat_config.v2.json
# vào RELEASE_MANIFEST (rò metadata + file_count lệch zip-set 115≠109 → release-verify trong gói FAIL).
_RELEASE_EXCLUDE_NAMES_ANYWHERE = {"CLAUDE.md", "tra_luat_config.json", "tra_luat_config.v2.json"}

_RELEASE_EXCLUDE_NAMES = {
    "RELEASE_MANIFEST.json",
    ".__det_audit_probe__.json",
    "before.json", "after.json",
    "live_state_before.json", "live_state_after.json", "live_state_diff.json",
    "release_check_report.json", "determinism_report.json",
}

_RELEASE_REQUIRED_FILES = [
    "VERSION",
    "scripts/tl_core/__init__.py",
    "scripts/tl_core/deterministic.py",
    "scripts/tl_core/jsonio.py",
    "scripts/tl_core/workflow.py",
    "scripts/tl_core/release.py",
    "scripts/tl_core/live.py",
    "scripts/tl_core/zip_ingest.py",
    "scripts/tl_core/ocr.py",
    "scripts/tl_core/chunking.py",
    "SKILL.md",
    "CHANGELOG.md",
    "scripts/tl.py",
    "scripts/gen_instructions.py",
    "references/API_CONTRACT.md",
    "references/workflows/workflow_card.schema.json",
    "references/golden/route_task_ingest_zip.json",
    "references/golden/nlm_query_plan_3_sources.json",
    "references/golden/workflow_audit.json",
    "references/golden/tool_inventory_inventory_decision.json",
    "references/golden/route_task_ocr_ingest.json",
    "references/golden/route_task_profile_ingest_chunks.json",
]

_RELEASE_REQUIRED_WORKFLOWS = [
    "references/workflows/write_new_tool.json",
    "references/workflows/nlm_query_quality.json",
    "references/workflows/ingest_local.json",
    "references/workflows/convert_rename.json",
    "references/workflows/ingest_zip.json",
    "references/workflows/ocr_pdf_scan.json",
    "references/workflows/large_doc_chunk.json",
    "references/workflows/chunk_ingest.json",
    "references/workflows/ocr_ingest.json",
    "references/workflows/workflow_audit.json",
    "references/workflows/release_check.json",
    "references/workflows/live_readiness.json",
    "references/workflows/live_contract_check.json",
    "references/workflows/live_state_snapshot.json",
    "references/workflows/live_state_diff.json",
    "references/workflows/live_smoke_plan.json",
    "references/workflows/deploy_plan.json",
    "references/workflows/rollback_plan.json",
    "references/workflows/release_manifest.json",
    "references/workflows/release_verify.json",
    "references/workflows/release_bundle.json",
    "references/workflows/final_acceptance.json",
    "references/workflows/go_live_runbook.json",
]


def _release_root_from_arg(p: str | None) -> Path:
    root = Path(p).expanduser().resolve() if p else HERE.parent.resolve()
    if root.name == "scripts" and (root.parent / "SKILL.md").exists():
        root = root.parent.resolve()
    return root


def _release_should_include(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    parts = set(rel.parts)
    if parts & _RELEASE_EXCLUDE_DIRS:
        return False
    if path.suffix.lower() in _RELEASE_EXCLUDE_SUFFIXES:
        return False
    if len(rel.parts) == 1 and rel.name in _RELEASE_EXCLUDE_NAMES:
        # Do not hash generated root-level manifests/snapshots/reports by default; release-bundle adds a fresh manifest.
        return False
    if rel.name in _RELEASE_EXCLUDE_NAMES_ANYWHERE:   # v1.33.54: config thật/CLAUDE.md ở MỌI cấp
        return False
    if len(rel.parts) == 1 and rel.name.endswith("-release.zip"):   # v1.33.56 (F6): bundle rơi vào root không nhiễm hash
        return False
    try:
        if path.is_symlink():   # v1.33.56 (F4): không hash xuyên symlink/junction (thoát cây repo)
            return False
    except OSError:
        return False
    return path.is_file()


def _build_release_manifest(root: Path) -> dict:
    root = root.resolve()
    files = []
    total = 0
    for p in sorted(root.rglob("*"), key=lambda x: str(x.relative_to(root)).replace(os.sep, "/")):
        if not _release_should_include(p, root):
            continue
        rel = str(p.relative_to(root)).replace(os.sep, "/")
        size = p.stat().st_size
        total += size
        files.append({"path": rel, "size": size, "sha256": _sha256_file(p)})
    by_path = {f["path"] for f in files}
    required = list(_RELEASE_REQUIRED_FILES) + list(_RELEASE_REQUIRED_WORKFLOWS)
    missing_required = [x for x in required if x not in by_path]
    version_text = ""
    try:
        version_text = (root / "VERSION").read_text(encoding="utf-8", errors="replace").strip()
    except Exception:
        version_text = VERSION
    package_hash = hashlib.sha256("\n".join(f"{f['path']}\0{f['size']}\0{f['sha256']}" for f in files).encode("utf-8")).hexdigest()
    return {
        "ok": not missing_required,
        "schema": "release_manifest.v1",
        "skill": "tra-luat",
        "skill_version": version_text or VERSION,
        "webapp_target": globals().get("EXPECT_VERSION", ""),
        "root_name": root.name,
        "file_count": len(files),
        "total_bytes": total,
        "package_hash": package_hash,
        "required_missing": missing_required,
        "files": files,
        "determinism_note": "Manifest không chứa timestamp hay đường dẫn tuyệt đối; package_hash tính từ path,size,sha256 đã sort.",
    }


def _verify_release_manifest(root: Path, manifest: dict, *, strict: bool = False) -> dict:
    root = root.resolve()
    expected = {f.get("path"): f for f in manifest.get("files", []) if f.get("path")}
    checks = []
    ok = True
    for rel, meta in sorted(expected.items()):
        p = root / rel
        if not p.exists():
            checks.append({"path": rel, "ok": False, "error": "MISSING"})
            ok = False
            continue
        if not p.is_file():
            checks.append({"path": rel, "ok": False, "error": "NOT_FILE"})
            ok = False
            continue
        size = p.stat().st_size
        sha = _sha256_file(p)
        item_ok = (size == int(meta.get("size", -1)) and sha == meta.get("sha256"))
        checks.append({"path": rel, "ok": item_ok, "expected_size": meta.get("size"), "actual_size": size,
                       "expected_sha256": meta.get("sha256"), "actual_sha256": sha})
        ok = ok and item_ok
    current = _build_release_manifest(root)
    current_paths = {f["path"] for f in current.get("files", [])}
    expected_paths = set(expected)
    extra = sorted(current_paths - expected_paths)
    missing_from_current_manifest = sorted(expected_paths - current_paths)
    if strict and extra:
        ok = False
    required_missing = [x for x in (list(_RELEASE_REQUIRED_FILES) + list(_RELEASE_REQUIRED_WORKFLOWS)) if not (root / x).exists()]
    if required_missing:
        ok = False
    return {
        "ok": bool(ok),
        "schema": "release_verify.v1",
        "strict": bool(strict),
        "root_name": root.name,
        "manifest_schema": manifest.get("schema"),
        "skill_version": manifest.get("skill_version"),
        "expected_file_count": len(expected),
        "checked_file_count": len(checks),
        "failed": [c for c in checks if not c.get("ok")][:50],
        "extra_files": extra[:200],
        "missing_from_current_manifest": missing_from_current_manifest[:200],
        "required_missing": required_missing,
        "package_hash_expected": manifest.get("package_hash"),
        "package_hash_current": current.get("package_hash"),
        "package_hash_match": manifest.get("package_hash") == current.get("package_hash"),
        "note": "strict=true coi file thừa là lỗi; strict=false chỉ cảnh báo extra_files.",
    }


def cmd_release_manifest(a) -> int:
    root = _release_root_from_arg(getattr(a, "root", None))
    m = _build_release_manifest(root)
    if getattr(a, "out", None):
        _write_text_atomic(Path(a.out), json.dumps(m, ensure_ascii=False, indent=2))
    _print_json_or_text(m, getattr(a, "json", False))
    return 0 if m.get("ok") else 2


def cmd_release_verify(a) -> int:
    root = _release_root_from_arg(getattr(a, "root", None))
    mf = Path(getattr(a, "manifest", "")).expanduser()
    try:
        manifest = json.loads(mf.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        out = {"ok": False, "error": "MANIFEST_READ_FAILED", "detail": f"{type(e).__name__}: {e}", "manifest": str(mf)}
        _print_json_or_text(out, getattr(a, "json", False))
        return 2
    out = _verify_release_manifest(root, manifest, strict=bool(getattr(a, "strict", False)))
    _print_json_or_text(out, getattr(a, "json", False))
    return 0 if out.get("ok") else 2


def _zip_write_file_deterministic(zf, src: Path, arcname: str):
    info = zipfile.ZipInfo(arcname)
    info.date_time = (1980, 1, 1, 0, 0, 0)
    info.compress_type = zipfile.ZIP_DEFLATED
    # 0644 regular file; keep deterministic permissions.
    info.external_attr = 0o100644 << 16
    zf.writestr(info, src.read_bytes())


def _zip_write_bytes_deterministic(zf, data: bytes, arcname: str):
    info = zipfile.ZipInfo(arcname)
    info.date_time = (1980, 1, 1, 0, 0, 0)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    zf.writestr(info, data)


def cmd_release_bundle(a) -> int:
    root = _release_root_from_arg(getattr(a, "root", None))
    out_path = Path(getattr(a, "out", None) or f"{root.name}-release.zip").expanduser().resolve()
    # v1.33.56 (review F6): out mặc định theo CWD → hay rơi NGAY TRONG repo root → lần regen manifest sau
    # nhiễm gói cũ / gói lồng gói. Nằm trong root mà không thuộc dir excluded → tự chuyển ra CẠNH root + warn.
    _warn_redirect = None
    try:
        _relo = out_path.relative_to(root.resolve())
        if not (_relo.parts and _relo.parts[0] in _RELEASE_EXCLUDE_DIRS):
            _warn_redirect = f"OUT_INSIDE_SKILL_ROOT → chuyển {root.parent / out_path.name}"
            out_path = (root.parent / out_path.name).resolve()
    except ValueError:
        pass
    top = getattr(a, "top", None) or root.name
    if not top or "/" in top or "\\" in top:
        res = {"ok": False, "error": "INVALID_TOP_NAME", "top": top}
        _print_json_or_text(res, getattr(a, "json", False)); return 2
    manifest = _build_release_manifest(root)
    if not manifest.get("ok"):
        res = {"ok": False, "error": "MANIFEST_NOT_OK", "required_missing": manifest.get("required_missing"), "root": str(root)}
        _print_json_or_text(res, getattr(a, "json", False)); return 2
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    if tmp.exists():
        tmp.unlink()
    _sha_by_rel = {f["path"]: f.get("sha256") for f in manifest.get("files", [])}
    files = [root / f["path"] for f in manifest.get("files", [])]
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(files, key=lambda x: str(x.relative_to(root)).replace(os.sep, "/")):
            rel = str(p.relative_to(root)).replace(os.sep, "/")
            data = p.read_bytes()
            # v1.33.56 (review F5 — TOCTOU): hash tính lúc build manifest, bytes đọc LẠI lúc zip — file đổi
            # giữa 2 thời điểm → gói tự-mâu-thuẫn ÂM THẦM (manifest trong gói không khớp nội dung). Đọc 1 LẦN,
            # đối chiếu sha với manifest; lệch → DỪNG loud.
            if _sha_by_rel.get(rel) and hashlib.sha256(data).hexdigest() != _sha_by_rel[rel]:
                try:
                    tmp.unlink()
                except FileNotFoundError:
                    pass
                res = {"ok": False, "error": "RELEASE_BUNDLE_FILE_CHANGED", "file": rel,
                       "note": "File đổi giữa lúc build manifest và lúc zip (process khác đang ghi?) — chạy lại khi cây ổn định."}
                _print_json_or_text(res, getattr(a, "json", False))
                return 2
            _zip_write_bytes_deterministic(zf, data, f"{top}/{rel}")
        _zip_write_bytes_deterministic(zf, json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"), f"{top}/RELEASE_MANIFEST.json")
    os.replace(tmp, out_path)
    bundle_sha = _sha256_file(out_path)
    res = {"ok": True, "schema": "release_bundle.v1", "out": str(out_path), "top": top,
           "file_count": manifest.get("file_count"), "total_bytes": manifest.get("total_bytes"),
           "package_hash": manifest.get("package_hash"), "bundle_sha256": bundle_sha,
           "warnings": ([_warn_redirect] if _warn_redirect else []),
           "note": "Zip dùng thứ tự file sort + timestamp 1980-01-01 để giảm drift đóng gói."}
    _print_json_or_text(res, getattr(a, "json", False))
    return 0
