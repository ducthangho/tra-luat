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
import stat       # noqa: F401
import subprocess # noqa: F401
import sys        # noqa: F401
import tempfile   # noqa: F401
import time       # noqa: F401
import unicodedata # noqa: F401
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
    from tl_core.deterministic import PATHISH_KEYS, VOLATILE_JSON_KEYS, audit_projection, json_dumps as _raw_det_json
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
    scrubbed = audit_projection(scrub_probe, volatile_keys={"out_dir", "seconds"}, path_keys={"path"},
                                  project_root=HERE.parent)
    add("declared_audit_projection", scrubbed.get("path") == "SKILL.md" and scrubbed.get("out_dir") == "<volatile>" and scrubbed.get("seconds") == "<volatile>", json.dumps(scrubbed, ensure_ascii=False))
    semantic_probe = {"regex": r"\d+\w", "legal_code": r"A\B", "created_at": "2020-01-01"}
    semantic_roundtrip = json.loads(_raw_det_json(semantic_probe, deterministic=True))
    add("deterministic_preserves_business_values", semantic_roundtrip == semantic_probe,
        json.dumps(semantic_roundtrip, ensure_ascii=False))

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
                p1 = audit_projection(s1.get("data"), volatile_keys=VOLATILE_JSON_KEYS,
                                      path_keys=PATHISH_KEYS, project_root=HERE.parent)
                p2 = audit_projection(s2.get("data"), volatile_keys=VOLATILE_JSON_KEYS,
                                      path_keys=PATHISH_KEYS, project_root=HERE.parent)
                t1 = _raw_det_json(p1, deterministic=True)
                t2 = _raw_det_json(p2, deterministic=True)
                add("live_state_snapshot_stable", t1 == t2, "snapshot JSON stable across two deterministic runs", diff={} if t1 == t2 else _first_text_diff(t1, t2))
            else:
                add("live_state_snapshot_stable", False, "snapshot child command failed", first={"rc": s1.get("returncode"), "stderr_tail": s1.get("stderr_tail")}, second={"rc": s2.get("returncode"), "stderr_tail": s2.get("stderr_tail")})
            diff = _run_tl_json(["live-state-diff", str(tdp / "before1.json"), str(tdp / "before2.json"), "--json"], timeout=60)
            add("live_state_diff_no_unexpected", bool(diff.get("ok")) and not ((diff.get("data") or {}).get("unexpected_changes")), "diff between two equivalent snapshots has no unexpected changes", diff=(diff.get("data") or {}))

            sample = tdp / "sample_abs.txt"
            sample.write_text("Điều 1. Mẫu kiểm thử deterministic.\n" + ("Nội dung tiếng Việt có dấu để đủ mật độ. " * 20), encoding="utf-8")
            oa = _run_tl_json(["ocr-analyze", str(sample), "--json"], timeout=60)
            od = (_raw_det_json(audit_projection(oa.get("data"), path_keys=PATHISH_KEYS,
                                                 project_root=HERE.parent), deterministic=True)
                  if oa.get("data") else "")
            add("ocr_analyze_path_scrub", bool(oa.get("ok")) and str(sample) not in od and "<tmp>" in od, "absolute tmp path scrubbed from deterministic ocr-analyze output")
            cp = _run_tl_json(["chunk-plan", str(sample), "--mode", "profile", "--json"], timeout=60)
            cd = (_raw_det_json(audit_projection(cp.get("data"), path_keys=PATHISH_KEYS,
                                                 project_root=HERE.parent), deterministic=True)
                  if cp.get("data") else "")
            add("chunk_plan_path_scrub", bool(cp.get("ok")) and str(sample) not in cd and "<tmp>" in cd, "absolute tmp path scrubbed from deterministic chunk-plan output")

            # Same zip contents with different member order must produce same dry-run plan after scrub.
            # Use in-process _zip_plan here to avoid nested CLI fan-out during strict audit; CLI path is covered by golden/smoke cases.
            # r320 (ING-06): filler `.txt` → `.docx`. Chủ đề của check này là ỔN ĐỊNH THỨ TỰ member
            # (`zi1 == zi2`), không liên quan đuôi; `.txt` chỉ tình cờ nằm đúng khe hở planner↔child vừa
            # bịt, làm vế `plan.ok` gãy vì 0 member được nhận. Khẳng định gốc giữ nguyên.
            z1, z2 = tdp / "a.zip", tdp / "b.zip"
            fitems = {"b.docx": "B", "a.docx": "A"}
            for zp, order in [(z1, ["b.docx", "a.docx"]), (z2, ["a.docx", "b.docx"])]:
                with zipfile.ZipFile(zp, "w") as zf:
                    for name in order:
                        zf.writestr(name, fitems[name])
            zp1 = _zip_plan(str(z1), mode="vbqppl", cat="01")
            zp2 = _zip_plan(str(z2), mode="vbqppl", cat="01")
            zi1 = [(i.get("normalized_path"), i.get("status"), i.get("reason")) for i in (zp1.get("items") or [])]
            zi2 = [(i.get("normalized_path"), i.get("status"), i.get("reason")) for i in (zp2.get("items") or [])]
            add("zip_member_order_stable", bool(zp1.get("ok") and zp2.get("ok")) and zi1 == zi2
                and [x[0] for x in zi1] == sorted([x[0] for x in zi1])
                and zp1.get("idempotency_key") == zp2.get("idempotency_key"), f"items={zi1}")

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


def _test_fragments_check(root: str | Path) -> dict:
    """Compare the land-only bundled module with the sole source generator."""
    repo_root = Path(root)
    fragment_root = repo_root / "scripts" / "test_fragments"
    bundled_path = repo_root / "scripts" / "tl_test_fragments_bundled.py"
    payload = {
        "ok": False,
        "schema": "test_fragments_check.v1",
        "fragment_root": "scripts/test_fragments",
        "bundled_module": "scripts/tl_test_fragments_bundled.py",
    }
    if not fragment_root.is_dir():
        return {**payload, "status": "invalid", "error": "FRAGMENT_ROOT_MISSING"}
    if not bundled_path.is_file():
        return {**payload, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}

    try:
        from tl_core.test_fragments import generate_bundled_module_bytes
        expected = generate_bundled_module_bytes(fragment_root)
    except Exception as exc:  # noqa: BLE001 — gate converts generator/input faults to data
        return {
            **payload,
            "status": "invalid",
            "error": "GENERATED_BUNDLE_INPUT_INVALID",
            "detail": f"{type(exc).__name__}: {exc}",
        }
    try:
        actual = bundled_path.read_bytes()
    except OSError as exc:
        return {
            **payload,
            "status": "unreadable",
            "error": "BUNDLED_MODULE_READ_FAILED",
            "detail": f"{type(exc).__name__}: {exc}",
        }

    expected_sha256 = hashlib.sha256(expected).hexdigest()
    actual_sha256 = hashlib.sha256(actual).hexdigest()
    if actual != expected:
        return {
            **payload,
            "status": "stale",
            "error": "GENERATED_BUNDLE_STALE",
            "expected_sha256": expected_sha256,
            "actual_sha256": actual_sha256,
            "expected_bytes": len(expected),
            "actual_bytes": len(actual),
        }
    return {
        **payload,
        "ok": True,
        "status": "current",
        "expected_sha256": expected_sha256,
        "actual_sha256": actual_sha256,
        "expected_bytes": len(expected),
        "actual_bytes": len(actual),
    }


def cmd_test_fragments_check(a) -> int:
    """Opt-in land gate for committed generated test-bundle freshness."""
    payload = _test_fragments_check(getattr(a, "root", None) or HERE.parent)
    _print_json_or_text(payload, getattr(a, "json", False))
    return 0 if payload.get("ok") else 2


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
        for _mod in ["__init__.py", "deterministic.py", "jsonio.py", "workflow.py", "release.py", "live.py", "zip_ingest.py", "ocr.py", "chunking.py", "command_registry.py", "hygiene.py"]:
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
                         ".claude", ".codex", ".agents", ".githooks", ".github",
                         "claude-code-best-practice",
                         "changelog_archive",
                         "rasoat",
                         "ops",
                         "docs"}   # v1.33.54 dev-side; v1.33.59: +.github (CI); v1.34.68: +kho tham chiếu clone dev-only (Q1); v1.34.69: +changelog_archive (439KB deep-history, runtime agent không cần — best-practice trim); r249: +rasoat (báo cáo/bàn giao của các lượt rà — sản phẩm PHIÊN, runtime Cowork không đọc). Chọn THƯ MỤC chứ không liệt kê từng tên: báo cáo mới sinh liên tục theo ngày, bảng tên sẽ trôi lệch ngay lượt sau. KHÔNG dùng `reports/` sẵn có vì nó bị .gitignore — sẽ mất tệp khỏi git, mà yêu cầu là GIỮ trong repo và chỉ loại khỏi GÓI (cùng khuôn changelog_archive). r291 (T0-G, Q1 user CHỐT 01-08): +docs — 19 tệp (3 `docs/*.md` + 16 `docs/adr/*.md`) là hồ sơ THIẾT KẾ của người giữ (kế hoạch + ADR), runtime agent không đọc, mà chúng ăn 19/200 slot import trong khi quỹ chỉ còn 4 ⇒ trả quỹ về 23. GIỮ trong git y như rasoat/changelog_archive. ⚠ KHÔNG hạ cổng nào: `doc-claims-check` vẫn phủ `docs/` (r264) vì nó quét CÂY DEV qua `_DOC_CLAIMS_DEFAULT_PATHS`, không phải gói. r331: +`.codex` — SONG SINH của `.claude`, cùng lý do, chỉ khác tác nhân: agent Codex đặt worktree ở `.codex/worktrees/<nhánh>/`, mỗi worktree là MỘT BẢN SAO ĐẦY ĐỦ của kho (có `VERSION`/`SKILL.md`/`RELEASE_MANIFEST.json` riêng). Thiếu khoá này thì `release-verify` đếm chúng vào `extra_files` ⇒ gate ĐỎ ở MỌI lượt chạy từ main checkout, trong khi worktree sạch vẫn xanh — đỏ theo NƠI CHẠY chứ không theo nội dung, đúng lớp bệnh khó tin nhất. Đo 04-08-2026: 200 `extra_files`, 100% thuộc `.codex/`, mà `failed: []` và `expected/checked = 177/177` (manifest LÀNH). r357: +`.agents` — ANH EM THỨ BA của `.claude`/`.codex`, là vị trí adapter phía Codex mà `docs/adr/0019-ba-skill-adapter-hai-agent-mot-protocol.md` thiết kế và `docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md:273` khai thẳng "phải bị loại khỏi release bundle". ĐO TRƯỚC KHI VÁ: chép `.agents/` (10 tệp) vào cây rồi hỏi `_release_should_include` ⇒ **10/10 SẼ VÀO GÓI**, tức 180 → 190, ăn 10 trong 20 khe còn lại dưới trần 200 — CÙNG hình dạng với ca `.codex` ngay trên, chỉ khác là lần này bắt được TRƯỚC khi tệp vào git chứ không phải sau khi gate đỏ. ★ Cạm bẫy: WARN của deploy khuyên `release-manifest --out …` — ở ca NÀY là SAI, nướng 4 bản sao kho vào manifest trong khi trần gói là 200 tệp CỨNG; lời khuyên đó chỉ đúng cho ca thêm/xoá tệp THẬT (r238).

_RELEASE_EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".tmp", ".bak", ".swp", ".enc"}   # v1.33.54: +.enc (secrets mã hoá local)

# v1.33.54: file local-only MỌI CẤP — config THẬT (chứa webappUrl/token) + CLAUDE.md dev. Phát hiện khi regen
# manifest trên dev-tree: walk thư mục (không phải git ls-files) đã liệt kê + hash tra_luat_config.v2.json
# vào RELEASE_MANIFEST (rò metadata + file_count lệch zip-set 115≠109 → release-verify trong gói FAIL).
# v1.35.81: 4 script DEPLOY là dev-side thuần — phiên Cowork LIVE bootstrap TỪ zip thì không bao giờ tự
# deploy, nên chúng chỉ chiếm slot. Đã đụng trần THẬT: thêm deploy-package.ps1 + deploy-guard.ps1 +
# pkg_secret_scan.py làm entries 199 → 202 > 200 ⇒ release-bundle chết IMPORT_LIMIT_EXCEEDED. GIỮ trong
# repo/git (dev `git pull` là có), CHỈ loại khỏi GÓI — cùng tiền lệ CLAUDE.md/.claude/Code.2.21.2k.gs.
_RELEASE_EXCLUDE_NAMES_ANYWHERE = {"CLAUDE.md", "tra_luat_config.json", "tra_luat_config.v2.json",
                                   "deploy-package.sh", "deploy-package.ps1", "deploy-package.cmd",
                                   "deploy-guard.ps1", "pkg_secret_scan.py",
                                   # r?: don nhanh remote la viec DEV-SIDE — runtime
                                   # Cowork khong bao gio goi no. Cung ranh gioi voi bon
                                   # script deploy ngay tren: GIU trong kho, LOAI khoi goi.
                                   "don-nhanh.ps1", "don-nhanh.cmd", "don-nhanh_test.ps1",
                                   "command_registry_test.py",  # AG-T0-03: unit-test dev-side, giu trong repo, loai khoi goi de giu file_count <= 200
                                   "Code.2.21.2k.gs",   # v1.34.69: GAS bản cũ 0-ref (193KB) — best-practice trim
                                   "Code.2.21.2l.gs", "Code.2.21.2m.gs", "Code.2.21.2n.gs"}   # r194: bản cũ = dead-weight bundle, GIỮ repo/git chỉ loại khỏi GÓI (tiền lệ 2.21.2k); r198: current nay 2.21.2o — 2.21.2n xuống hàng cũ

_RELEASE_EXCLUDE_NAMES = {
    "RELEASE_MANIFEST.json",
    ".__det_audit_probe__.json",
    "BUNDLE_META.json",
    "before.json", "after.json",
    "live_state_before.json", "live_state_after.json", "live_state_diff.json",
    "release_check_report.json", "determinism_report.json",
    # F2-A (ADR-0018): `.editorconfig` là config DEV-SIDE, cùng hạng với `.githooks/`/`.github/`
    # (đã loại qua _RELEASE_EXCLUDE_DIRS) — runtime agent trong gói không đọc nó. Không loại thì
    # nó vừa ăn 1 khe trong trần 200 (kê khai slot 179 ở tl_selftest r291_docs_ngoai_goi hoá đỏ),
    # vừa bị `release-verify --strict` hô extra_files vì manifest chưa có. Loại theo TÊN vì tệp
    # nằm ở gốc kho, không có thư mục riêng để khoá.
    ".editorconfig",
    # `.mcp.json` khai server MCP ở phạm vi DỰ ÁN cho phiên dev (chỉ tên biến môi
    # trường, không token). Cùng hạng `.editorconfig`: config dev-side, runtime agent
    # trong gói không đọc, và cũng nằm ở gốc kho nên phải loại theo TÊN. Đi cùng
    # khoá `ops` ở `_RELEASE_EXCLUDE_DIRS` — hai thứ sinh ra cùng một đợt (đường đăng
    # lease bằng git) nên cùng thủng một lỗ: `release-verify --strict` hô 5 tệp
    # `extra_files` NGAY TỪ commit đầu của nhánh ops, gate đỏ suốt mà không ai đọc
    # ra vì đỏ ở "file thừa" chứ không ở `failed`. Đo 14-08-2026: extra_files 6 → 0.
    # Bảng loại trừ KHÔNG thêm/bớt mục nào của manifest (`file_count` giữ 179, 0 thêm
    # 0 bớt) — nhưng manifest vẫn phải tái sinh, vì `release.py` NẰM TRONG gói nên sửa
    # chính tệp này là đổi sha của chính nó. Lượt đầu quên bước đó và `release-verify`
    # trả `failed: 1` đúng ngay tệp vừa sửa: cổng nói thật, chỉ là nói về chuyện khác
    # với chuyện mình đang nghĩ. Đổi bảng loại trừ ⇒ luôn chạy lại `release-manifest`
    # rồi ĐỌC diff, đừng ghi đè cho hết đỏ.
    ".mcp.json",
}

_RELEASE_WINDOWS_RESERVED = {
    "con", "prn", "aux", "nul",
    *(f"com{i}" for i in range(1, 10)),
    *(f"lpt{i}" for i in range(1, 10)),
}


def _portable_release_component(name: str) -> bool:
    """Return whether one path component is safe on Windows/macOS/Linux."""
    if not isinstance(name, str) or not name or name in {".", ".."}:
        return False
    if unicodedata.normalize("NFC", name) != name:
        return False
    # v1.34.47: cấm CẢ '/' và '\\' — một component portable KHÔNG chứa separator (F-01 residual:
    # trước đó `release-bundle --top a/b` lọt gate publish rồi fail chính release-verify của nó).
    if name.endswith((" ", ".")) or re.search(r'[<>:"|?*/\\]|[\x00-\x1f]', name):
        return False
    return name.split(".", 1)[0].casefold() not in _RELEASE_WINDOWS_RESERVED


def _portable_release_relpath(rel: str) -> bool:
    if not isinstance(rel, str) or not rel or "\\" in rel or rel.startswith("/"):
        return False
    if re.match(r"^[A-Za-z]:", rel):
        return False
    parts = rel.split("/")
    return bool(parts) and all(_portable_release_component(part) for part in parts)

_RELEASE_REQUIRED_FILES = [
    "VERSION",
    "scripts/tl_test_fragments_bundled.py",
    "scripts/tl_core/__init__.py",
    "scripts/tl_core/deterministic.py",
    "scripts/tl_core/jsonio.py",
    "scripts/tl_core/workflow.py",
    "scripts/tl_core/release.py",
    "scripts/tl_core/live.py",
    "scripts/tl_core/zip_ingest.py",
    "scripts/tl_core/ocr.py",
    "scripts/tl_core/chunking.py",
    "scripts/tl_core/hygiene.py",
    "scripts/tl_core/nlm_ops.py",
    "scripts/tl_core/extract_cache.py",
    "scripts/tl_core/fetch_web.py",
    "scripts/tl_core/profile_mgmt.py",
    "scripts/tl_core/ingest_ops.py",
    "scripts/tl_core/ingest_contract.py",
    "scripts/tl_core/lookup_ops.py",
    "scripts/tl_core/ops_misc.py",
    "scripts/tl_core/classify.py",
    "scripts/tl_core/profile_env.py",
    "scripts/tl_core/resolve.py",
    "scripts/tl_core/regio.py",
    "scripts/tl_core/cli.py",
    "scripts/tl_core/command_registry.py",
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
    "templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json",   # r209/H1: mẫu bảng master rà soát — bên đọc rasoat_phuluc.py
    "references/RASOAT_HOSO_LOOP.md",               # r210/H3-H4: kịch bản vòng lặp + prompt agent tl-rasoat (SKILL.md trỏ tới)
    "references/RASOAT_PLAN_SCHEMA.md",             # r209/H2: đặc tả state biến động (rasoat_plan.v1)
    "references/QUY_TRINH_RA_SOAT_3_TANG.md",       # r324/REL-05: quy trình rà 3 tầng (PHA0_GATE_v1, BUG_LEDGER_v1)
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
    "references/workflows/bundle_export.json",
    "references/workflows/live_state_diff.json",
    "references/workflows/live_smoke_plan.json",
    "references/workflows/deploy_plan.json",
    "references/workflows/rollback_plan.json",
    "references/workflows/release_manifest.json",
    "references/workflows/release_verify.json",
    "references/workflows/release_bundle.json",
    "references/workflows/final_acceptance.json",
    "references/workflows/go_live_runbook.json",
    "references/workflows/rasoat_hoso.json",   # r209/H2: thẻ quy trình rà soát hồ sơ (lớp điều phối)
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
    if len(rel.parts) > 2 and rel.parts[:2] == ("scripts", "test_fragments"):
        return False
    parts = set(rel.parts)
    if parts & _RELEASE_EXCLUDE_DIRS:
        return False
    if path.suffix.lower() in _RELEASE_EXCLUDE_SUFFIXES:
        return False
    if len(rel.parts) == 1 and rel.name in _RELEASE_EXCLUDE_NAMES:
        # Do not hash generated root-level manifests/snapshots/reports by default; release-bundle adds a fresh manifest.
        return False
    # r193 (sự cố 23-07: `tra_luat_config.v2.json.bak_truoc_shard3_…` LỌT bundle → token LIVE lên Drive —
    # luật cũ chỉ bắt TÊN CHÍNH XÁC + đuôi `.bak` CHÍNH XÁC, đuôi backup BIẾN THỂ lọt): (a) tên loại-trừ
    # mọi-cấp nay bắt CẢ biến thể có hậu tố (`<tên>.bak_*`/`<tên>.old`…); (b) mọi tên chứa `.bak`/`.tmp`
    # (có dấu chấm đứng trước) đều bị loại — backup là file local-only, không bao giờ thuộc gói phát hành.
    _nl93 = rel.name.lower()
    if any(_nl93 == x.lower() or _nl93.startswith(x.lower() + ".") for x in _RELEASE_EXCLUDE_NAMES_ANYWHERE):
        return False
    if ".bak" in _nl93 or ".tmp" in _nl93:
        return False
    if rel.as_posix().startswith("references/golden/fixtures/"):   # v1.33.59: fixtures SINH-TẠI-CHỖ (không commit, không hash)
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
        "root_name": "tra-luat",
        "file_count": len(files),
        "total_bytes": total,
        "package_hash": package_hash,
        "content_hash": package_hash,
        "required_missing": missing_required,
        "files": files,
        "determinism_note": "Manifest không chứa timestamp hay đường dẫn tuyệt đối; package_hash tính từ path,size,sha256 đã sort.",
    }


def _skill_links_findings(skill_text: str, manifest_paths) -> dict:
    """PURE (r184/REL-01): đối chiếu MỌI con trỏ `references/...` trong SKILL.md với FILE-SET của
    release manifest — không phải cây đĩa. Cây dev có thể chứa thư mục dev-only (release exclude) làm
    gate cây XANH nhưng artifact ĐỎ; nguồn sự thật của "link sống lúc runtime" là package-set.
    Link glob (dừng trước `*`) và link thư mục khớp theo PREFIX; manifest rỗng → mọi link fail-closed."""
    links = sorted({m.rstrip(".,;:)]}") for m in re.findall(r"references/[A-Za-z0-9_./\-]+", str(skill_text or ""))})
    paths = [str(p) for p in (manifest_paths or [])]
    missing = []
    for link in links:
        if link.endswith("/"):
            hit = any(p.startswith(link) for p in paths)
        else:
            hit = link in paths or any(p.startswith(link + "/") for p in paths)
        if not hit:
            missing.append(link)
    return {"links_checked": len(links), "links_missing": missing, "links_ok": not missing}


# r209 (H9 Đợt-1 rà-hồ-sơ): guard RATCHET con trỏ tài liệu — mở rộng vùng phủ REL-01 từ «references/ trong
# SKILL.md» ra «references/|templates/|scripts/ trong SKILL.md + references/*.md». Đo 26-07 trên v1.35.44:
# 80 cặp (tài_liệu, con_trỏ) đứt — 65 trong DOCTRINE_APPENDIX (LƯU TRỮ → advisory), 5 tầng A+B vá ở H0/H1,
# 10 nợ cũ khoanh BASELINE dưới. Fail-closed CHỈ với cặp MỚI ở tài liệu SỐNG — không baseline thì guard đỏ
# 80 mục ngay ngày đầu và sẽ bị vô hiệu hoá (bài học §0.8 kế hoạch). Gỡ nợ = XOÁ mục baseline (ratchet:
# sửa baseline = sửa code = qua ruff→selftest→CHANGELOG→review; test r209 khoá số đếm).
# r308 (T0-F/GATE-04): doc-set mở từ «references/*.md KHÔNG đệ quy + SKILL.md» ra «MỌI *.md CÓ TRONG
# MANIFEST» — xem chỗ gọi trong _verify_release_manifest. Đo 02-08 trên gói 177 tệp: 34 .md, tầm cũ phủ
# 30, ngoài tầm 4 (CHANGELOG · INSTALL · CONTEXT · scripts/_fallback/README). Mở tầm ⇒ pointer FAIL 0→40
# (CHANGELOG 24 + INSTALL 16), bare-tool FAIL 0→0 (advisory 73→95 — lớp trần mở MIỄN PHÍ).
# Hai tệp dưới vào hạng LƯU TRỮ vì bản chất là SỬ, không phải chỉ dẫn vận hành sống:
#   CHANGELOG.md — chép các bản phát hành ĐÃ QUA nên tất yếu nhắc tên tệp TỪNG tồn tại
#     (`Code.2.21.2n.gs`, `changelog_archive/`, 4 script deploy dev-side). Sửa thân = viết lại lịch sử.
#   INSTALL.md   — khối `:7` TỰ KHAI "layout GỐC v1.x (tham chiếu lịch sử), nguồn chân lý = VERSION +
#     SKILL.md + CHANGELOG" (Q3 chốt 01-08; r289 đã sửa 3 dòng MỆNH LỆNH deploy về `2.21.2p`, 14 nhắc
#     `.gs` còn lại CỐ Ý giữ vì đang kể lịch sử bản vá).
# CONTEXT.md + scripts/_fallback/README.md vào thẳng FAIL-CLOSED, 0 đồng (đo: 0 fail).
_POINTER_ARCHIVE_DOCS = frozenset({
    "references/DOCTRINE_APPENDIX.md",
    "CHANGELOG.md",
    "INSTALL.md",
})
# r218: TRẢ NỢ 6/10 mục. `doc-claims-check` (lệnh mới, đường quét độc lập) dựng lại ĐÚNG 6 cặp dưới đây
# từ con số 0 — tức danh sách khoanh nợ này chính xác, chỉ là chưa ai trả. Đã sửa thân tài liệu nên chúng
# không còn là hit; ratchet hạ 10 → 4, đi ĐÚNG chiều (ratchet chặn THÊM miễn trừ, không chặn bớt):
#   API_CONTRACT→scripts/manifest_build.py · DELTA_v1.19→Code.2.21.2h.gs · DEV_TOOLING_GUIDE→Code.2.21.2i.gs
#   PATCH_v2.21.1→APPSSCRIPT_MANIFEST.restricted-egress.json · QUY_TRINH_RA_SOAT→BANG_PHAN_TANG_RUI_RO.md
#   SKILL_KERNEL_MAPPING→changelog_archive/CHANGELOG-2026H1.md
# Bốn cặp còn lại KHÔNG phải nợ — false-positive có chủ đích; sửa thân sẽ làm tài liệu SAI đi.
_POINTER_BASELINE = frozenset({
    ("references/COWORK_EDIT_SAFETY.md", "scripts/ten_file.py"),        # placeholder ví dụ trong prose
    ("references/GOTCHAS.md", "scripts/.tl_state"),                     # thư mục runtime, cố ý ngoài gói
    # (r226 TRẢ NỢ: cặp SKILL_KERNEL_MAPPING.md → references/SKILL_KERNEL_DRAFT.md đã gỡ khỏi baseline —
    #  `doc-claims-check` L1 bắt đúng rằng tệp đó CHƯA BAO GIỜ có trong kho, nên tài liệu đã sửa lời cho
    #  đúng thay vì khoanh nợ tiếp. Ratchet siết 4 → 3.)
    ("references/THE_THUC_TRINH_BAY.md", "templates/_nguon-goc/"),      # đường DRIVE `_meta/templates/…` — false-positive giữ chủ đích
})


def _doc_pointer_findings(doc_texts: dict, manifest_paths, *, archive_docs=_POINTER_ARCHIVE_DOCS,
                          baseline=_POINTER_BASELINE) -> dict:
    """PURE (r209/H9): quét con trỏ `references/|templates/|scripts/…` trong TỪNG tài liệu, đối chiếu
    PACKAGE-SET (như REL-01: nguồn sự thật là manifest, không phải cây đĩa). Ratchet 2 tầng:
    (a) tài liệu trong `archive_docs` → chỉ ADVISORY (lưu trữ lịch sử, không sửa thân);
    (b) cặp (tài_liệu, con_trỏ) trong `baseline` → nợ cũ đã khoanh, im lặng; MỌI cặp khác thiếu trong
    package ⇒ fail-closed. Khớp theo CẶP: con trỏ được miễn ở doc này KHÔNG tự miễn ở doc khác.
    Link glob (chứa `*`) bỏ qua; link thư mục (đuôi `/`) khớp PREFIX; manifest rỗng ⇒ fail-closed."""
    paths = [str(p) for p in (manifest_paths or [])]

    def _hit(link):
        if link.endswith("/"):
            return any(p.startswith(link) for p in paths)
        return link in paths or any(p.startswith(link + "/") for p in paths)

    fail, advisory, baseline_hits, checked = [], [], [], 0
    for doc in sorted(doc_texts or {}):
        text = str(doc_texts.get(doc) or "")
        links = sorted({m.rstrip(".,;:)]}»*`") for m in
                        re.findall(r"(?:references|templates|scripts)/[A-Za-z0-9_./\-]+", text)})
        for link in links:
            if "*" in link or not link:
                continue
            checked += 1
            if _hit(link):
                continue
            pair = (doc, link)
            if doc in archive_docs:
                advisory.append(pair)
            elif pair in baseline:
                baseline_hits.append(pair)
            else:
                fail.append(pair)
    return {"pointers_checked": checked, "pointers_fail": fail, "pointers_advisory": advisory,
            "pointers_baseline": baseline_hits, "pointers_ok": not fail}


# r289 (H9b): LỚP THỨ HAI của guard con trỏ — tên công cụ viết TRẦN trong backtick, KHÔNG tiền tố thư mục.
# `_doc_pointer_findings` đòi tiền tố `references/|templates/|scripts/` nên MÙ với dạng `nlm_qa.py verify`.
# Ca thật đã trả giá: chỉ dẫn SỐNG «Ghi mỗi truy vấn NLM bằng `nlm_log.py add`» (QUY_TRINH) sống từ
# v1.29.4 tới v1.35.44 mà KHÔNG cổng nào kêu — chỉ bị bắt bằng rà tay. Đo 01-08 trên gói 195 file:
# 82 tên trần thiếu / 30 tài liệu, trong đó 57 nằm ở DOCTRINE_APPENDIX (lưu trữ). Vì vậy fail-closed
# CHỈ cho tài liệu CHỈ-DẪN-VẬN-HÀNH-SỐNG; phần còn lại advisory — bật fail-closed toàn bộ = 82 mục đỏ
# ngày đầu và guard sẽ bị vô hiệu hoá cho xong (đúng bài học §0.8 của H9).
# Đối chiếu theo BASENAME trong package-set: `boot.py` nằm ở `scripts/_fallback/boot.py` vẫn hợp lệ.
_BARE_TOOL_STRICT_DOCS = frozenset({
    "SKILL.md",                                   # LÕI: bản đồ script + đường boot/cấp cứu
    "references/QUY_TRINH_RA_SOAT_3_TANG.md",     # quy trình rà 3 tầng (PHA0_GATE_v1, BUG_LEDGER_v1)
    "references/RASOAT_HOSO_LOOP.md",             # kịch bản vòng lặp + prompt agent tl-rasoat
})
_BARE_TOOL_BASELINE = frozenset({
    # placeholder mô tả DẠNG con trỏ (`file.py:dòng`), không phải tệp thật — cùng họ `scripts/ten_file.py`
    ("references/RASOAT_HOSO_LOOP.md", "file.py"),
})
_BARE_TOOL_SPAN_RE = re.compile(r"`([^`\n]{1,200})`")
_BARE_TOOL_NAME_RE = re.compile(
    r"(?<![A-Za-z0-9_./\-])([A-Za-z0-9_][A-Za-z0-9_.\-]*\.(?:py|sh|ps1|cmd|gs))(?![A-Za-z0-9_.\-/])")


def _doc_bare_tool_findings(doc_texts: dict, manifest_paths, *, strict_docs=_BARE_TOOL_STRICT_DOCS,
                            baseline=_BARE_TOOL_BASELINE) -> dict:
    """PURE (r289/H9b): quét tên công cụ viết TRẦN (`nlm_qa.py`, `tl_rebuild.sh`) bên trong span backtick
    và đối chiếu BASENAME với PACKAGE-SET. Chỉ xét token KHÔNG chứa `/` — dạng có tiền tố thư mục đã do
    `_doc_pointer_findings` gác. Ratchet 2 tầng: tài liệu ngoài `strict_docs` → ADVISORY; cặp
    (tài_liệu, tên) trong `baseline` → im lặng; cặp MỚI ở tài liệu SỐNG ⇒ fail-closed.
    Manifest rỗng ⇒ mọi tên fail-closed (đồng nhất với hai guard anh em)."""
    names = {str(p).rsplit("/", 1)[-1] for p in (manifest_paths or [])}
    fail, advisory, baseline_hits, checked = [], [], [], 0
    for doc in sorted(doc_texts or {}):
        text = str(doc_texts.get(doc) or "")
        hits = set()
        for span in _BARE_TOOL_SPAN_RE.findall(text):
            for tok in _BARE_TOOL_NAME_RE.findall(span):
                if "/" not in tok:
                    hits.add(tok)
        for tok in sorted(hits):
            checked += 1
            if tok in names:
                continue
            pair = (doc, tok)
            if pair in baseline:
                baseline_hits.append(pair)
            elif doc in strict_docs:
                fail.append(pair)
            else:
                advisory.append(pair)
    return {"bare_tools_checked": checked, "bare_tools_fail": fail, "bare_tools_advisory": advisory,
            "bare_tools_baseline": baseline_hits, "bare_tools_ok": not fail}


def _verify_release_manifest(root: Path, manifest: dict, *, strict: bool = False) -> dict:
    root = root.resolve()
    raw_files = manifest.get("files") if isinstance(manifest, dict) else None
    checks = []
    errors = []
    ok = isinstance(raw_files, list) and manifest.get("schema") == "release_manifest.v1"
    if not isinstance(raw_files, list):
        raw_files = []
        errors.append("MANIFEST_FILES_NOT_LIST")
    if manifest.get("schema") != "release_manifest.v1":
        errors.append("MANIFEST_SCHEMA_INVALID")
    expected = {}
    for meta in raw_files:
        if not isinstance(meta, dict):
            errors.append("MANIFEST_FILE_ENTRY_NOT_OBJECT")
            ok = False
            continue
        rel = str((meta or {}).get("path") or "").replace("\\", "/")
        parts = rel.split("/") if rel else []
        if (not rel or rel.startswith("/") or re.match(r"^[A-Za-z]:", rel)
                or any(p in {"", ".", ".."} for p in parts)):
            errors.append(f"MANIFEST_PATH_UNSAFE:{rel}")
            ok = False
            continue
        try:
            declared_size = int(meta.get("size", -1))
        except (TypeError, ValueError):
            errors.append(f"MANIFEST_SIZE_INVALID:{rel}")
            ok = False
            continue
        declared_sha = str(meta.get("sha256") or "")
        if declared_size < 0 or not re.fullmatch(r"[0-9a-f]{64}", declared_sha):
            errors.append(f"MANIFEST_FILE_METADATA_INVALID:{rel}")
            ok = False
            continue
        portable_key = unicodedata.normalize("NFC", rel).casefold()
        if any(unicodedata.normalize("NFC", prior).casefold() == portable_key for prior in expected):
            errors.append(f"MANIFEST_PATH_DUPLICATE:{rel}")
            ok = False
            continue
        expected[rel] = {**meta, "size": declared_size, "sha256": declared_sha}
    manifest_basis = "\n".join(
        f"{rel}\0{int(meta.get('size', -1))}\0{meta.get('sha256')}" for rel, meta in sorted(expected.items())
    )
    manifest_package_hash = hashlib.sha256(manifest_basis.encode("utf-8")).hexdigest()
    package_hash_self_match = bool(expected) and manifest.get("package_hash") == manifest_package_hash
    if not package_hash_self_match:
        errors.append("MANIFEST_PACKAGE_HASH_MISMATCH")
        ok = False
    for rel, meta in sorted(expected.items()):
        p = (root / rel).resolve()
        try:
            p.relative_to(root)
        except ValueError:
            checks.append({"path": rel, "ok": False, "error": "PATH_ESCAPES_ROOT"})
            ok = False
            continue
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
        item_ok = (size == meta.get("size") and sha == meta.get("sha256"))
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
    # r184 (REL-01): con trỏ runtime trong SKILL.md phải nằm trong PACKAGE-SET (expected của manifest) —
    # kiểm exists() trên cây đĩa để lọt thư mục dev-only bị release-exclude (gate cây xanh, artifact đỏ).
    skill_links = {"links_checked": 0, "links_missing": [], "links_ok": True, "skipped": "NO_SKILL_MD"}
    _sk_path = root / "SKILL.md"
    if _sk_path.exists():
        try:
            _sk_text = _sk_path.read_text(encoding="utf-8", errors="replace")
        except OSError as _sk_err:
            _sk_text = None
            errors.append(f"SKILL_LINKS_UNREADABLE:{type(_sk_err).__name__}")
            ok = False
        if _sk_text is not None:
            skill_links = _skill_links_findings(_sk_text, sorted(expected))
            if not skill_links["links_ok"]:
                errors.append("SKILL_LINKS_NOT_IN_PACKAGE:" + ",".join(skill_links["links_missing"][:10]))
                ok = False
    # r209 (H9): guard RATCHET con trỏ tài liệu SỐNG (references/|templates/|scripts/) — xem
    # _doc_pointer_findings. Cặp MỚI đứt ⇒ fail-closed.
    # r308 (T0-F/GATE-04): doc-set lấy từ MANIFEST (`expected`), không còn glob đĩa `references/*.md`.
    # Hai khoảng mù của nguồn cũ, cả hai đều đo được trên gói 177 tệp:
    #   (a) THIẾU — .md trong gói nhưng ngoài `references/` mức 1: CHANGELOG · INSTALL · CONTEXT ·
    #       scripts/_fallback/README (4 tệp). Tài liệu ĐI THEO GÓI mà không cổng nào gác con trỏ.
    #   (b) THỪA — .md nằm trong `references/` trên ĐĨA nhưng bị release-exclude: quét chúng là bắt
    #       gate CÂY chịu trách nhiệm cho thứ KHÔNG vào artifact (cùng họ xanh-giả của REL-01).
    # Đọc theo `expected` nên cũng tự đóng theo mọi thay đổi kiểm kê — thêm .md vào gói là guard phủ ngay.
    # r309 (T0-F/1c): thêm THẺ MÁY ĐỌC `references/workflows/*.json` vào doc-set. Thẻ là chỉ dẫn vận hành
    # y như .md, chỉ khác định dạng, mà TRƯỚC r309 không guard nào với tới vì lọc theo đuôi `.md`.
    # Đo 02-08 (gói 177 tệp): 27 thẻ · 4 con trỏ · 1 ĐỨT — `doc_claims_check.json` trỏ
    # `references/changelog_archive/` (dev-only, `_RELEASE_EXCLUDE_DIRS`). Đã SỬA LỜI THẺ, KHÔNG baseline:
    # đúng tiền lệ r184 trên CHÍNH con trỏ này ở SKILL.md — «không nới auditor, sửa con trỏ».
    # CỐ Ý KHÔNG mở sang `.json` khác: `references/golden/*.json` là ĐẦU RA GHI SẴN của test, đo được
    # 11 con trỏ đứt mà PHẢI đứt — gồm `references/KHONG_CO_FILE.md`, chính là mồi cho bộ dò tệp-thiếu.
    # Gác chúng = đỏ oan ngày đầu ⇒ guard bị vô hiệu hoá (bài học §0.8). Ranh giới này có test khoá.
    def _guarded_doc(rel: str) -> bool:
        low = rel.lower()
        return low.endswith(".md") or (low.startswith("references/workflows/") and low.endswith(".json"))

    _doc_texts = {}
    for _rel in sorted(k for k in expected if _guarded_doc(k)):
        _dp = root / _rel
        if not _dp.is_file():
            continue          # tệp thiếu/không phải tệp đã do vòng `checks` ở trên báo — không báo hai lần
        try:
            _doc_texts[_rel] = _dp.read_text(encoding="utf-8", errors="replace")
        except OSError as _dp_err:
            errors.append(f"DOC_POINTER_UNREADABLE:{_rel}:{type(_dp_err).__name__}")
            ok = False
    doc_pointers = _doc_pointer_findings(_doc_texts, sorted(expected))
    if not doc_pointers["pointers_ok"]:
        errors.append("DOC_POINTERS_NOT_IN_PACKAGE:" +
                      ",".join(f"{d}->{l}" for d, l in doc_pointers["pointers_fail"][:10]))
        ok = False
    # r289 (H9b): lớp con trỏ TRẦN — xem _doc_bare_tool_findings. Fail-closed cho tài liệu SỐNG.
    bare_tools = _doc_bare_tool_findings(_doc_texts, sorted(expected))
    if not bare_tools["bare_tools_ok"]:
        errors.append("DOC_BARE_TOOLS_NOT_IN_PACKAGE:" +
                      ",".join(f"{d}->{t}" for d, t in bare_tools["bare_tools_fail"][:10]))
        ok = False
    package_hash_current_expected = hashlib.sha256("\n".join(
        f"{c['path']}\0{c.get('actual_size', -1)}\0{c.get('actual_sha256')}"
        for c in checks if c.get("actual_sha256")
    ).encode("utf-8")).hexdigest()
    package_hash_match = (not any(not c.get("ok") for c in checks)
                          and package_hash_self_match
                          and package_hash_current_expected == manifest.get("package_hash"))
    if not package_hash_match:
        ok = False
    return {
        "ok": bool(ok),
        "schema": "release_verify.v1",
        "strict": bool(strict),
        "root_name": "tra-luat",
        "manifest_schema": manifest.get("schema"),
        "skill_version": manifest.get("skill_version"),
        "expected_file_count": len(expected),
        "checked_file_count": len(checks),
        "failed": [c for c in checks if not c.get("ok")][:50],
        "extra_files": extra[:200],
        "missing_from_current_manifest": missing_from_current_manifest[:200],
        "required_missing": required_missing,
        "skill_links": skill_links,
        "doc_pointers": doc_pointers,
        "bare_tools": bare_tools,
        "errors": errors,
        "package_hash_expected": manifest.get("package_hash"),
        "package_hash_current": package_hash_current_expected,
        "package_hash_full_tree": current.get("package_hash"),
        "package_hash_self_match": package_hash_self_match,
        "package_hash_match": package_hash_match,
        "note": "strict=true coi file thừa là lỗi; strict=false chỉ cảnh báo extra_files.",
    }


def cmd_release_manifest(a) -> int:
    root = _release_root_from_arg(getattr(a, "root", None))
    m = _build_release_manifest(root)
    if getattr(a, "out", None):
        _write_text_atomic(Path(a.out), json.dumps(m, ensure_ascii=False, indent=2))
    _print_json_or_text(m, getattr(a, "json", False))
    return 0 if m.get("ok") else 2


def _verify_release_archive(zip_path: Path, manifest: dict, *, expected_archive_sha256: str = "") -> dict:
    """Verify canonical ZIP topology, metadata, embedded manifest, and member bytes in O(n)."""
    out = {"archive": str(zip_path), "archive_ok": False, "errors": []}
    if not zip_path.is_file():
        out["errors"].append("ARCHIVE_NOT_FOUND")
        return out
    actual_sha = _sha256_file(zip_path)
    out["archive_sha256"] = actual_sha
    exp = str(expected_archive_sha256 or "").strip().lower()
    if exp:
        out["archive_sha256_expected"] = exp
        if exp != actual_sha:
            out["errors"].append(f"ARCHIVE_SHA256_MISMATCH:{actual_sha}!={exp}")
    expected = {}
    expected_keys = {}
    for record in manifest.get("files", []):
        rel = str(record.get("path") or "")
        if not _portable_release_relpath(rel):
            out["errors"].append(f"ARCHIVE_MANIFEST_PATH_UNSAFE:{rel}")
            continue
        key = rel.casefold()
        if key in expected_keys:
            out["errors"].append(f"ARCHIVE_MANIFEST_PATH_DUPLICATE:{rel}->{expected_keys[key]}")
            continue
        expected_keys[key] = rel
        expected[rel] = record

    def _metadata_errors(info) -> list[str]:
        errors = []
        # r194 (AMEND ADR-0007): chấp nhận CẢ STORED (bundle cũ) lẫn DEFLATED (canon mới, mức 9 cố định);
        # loại nén khác vẫn là lỗi. Check compress_size==file_size CHỈ áp cho STORED.
        if info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
            errors.append("COMPRESSION_NOT_STORED_OR_DEFLATED")
        if info.date_time != (1980, 1, 1, 0, 0, 0):
            errors.append("TIMESTAMP_NOT_FIXED")
        if info.create_system != 3:
            errors.append("CREATE_SYSTEM_NOT_FIXED")
        if info.extra or info.comment:
            errors.append("ENTRY_EXTRA_OR_COMMENT_PRESENT")
        mode = (int(info.external_attr) >> 16) & 0xFFFF
        kind = stat.S_IFMT(mode)
        if kind and kind != stat.S_IFREG:
            errors.append("SPECIAL_ENTRY")
        if mode != 0o100644:
            errors.append("PERMISSION_NOT_FIXED")
        if info.compress_type == zipfile.ZIP_STORED and info.compress_size != info.file_size:
            errors.append("STORED_SIZE_MISMATCH")
        return errors

    def _member_sha256(zf, info) -> str:
        digest = hashlib.sha256()
        with zf.open(info, "r") as stream:
            while True:
                chunk = stream.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
        return digest.hexdigest()

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            if zf.comment:
                out["errors"].append("ARCHIVE_COMMENT_PRESENT")
            infos = zf.infolist()
            if len(infos) > len(expected) + 2:
                out["errors"].append(f"ARCHIVE_ENTRY_COUNT_EXCESS:{len(infos)}>{len(expected) + 2}")
            roots = {}
            seen_full = {}
            seen = set()
            manifest_infos = []
            bundle_meta_infos = []
            for info in infos:
                name = info.filename
                if info.is_dir() or name.endswith("/"):
                    out["errors"].append(f"ARCHIVE_UNEXPECTED_DIRECTORY:{name}")
                    continue
                if not _portable_release_relpath(name) or "/" not in name:
                    out["errors"].append(f"ARCHIVE_UNSAFE_PATH:{name}")
                    continue
                top, rel = name.split("/", 1)
                # v1.34.47: key theo top CHÍNH XÁC (không casefold) — 2 root khác-hoa (tra-luat + TRA-LUAT)
                # là mơ hồ trên fs không-phân-biệt-hoa và LÀ 2 thư mục trên fs phân-biệt-hoa → phải bắt ROOT_NOT_SINGLE.
                roots[top] = top
                full_key = name.casefold()
                if full_key in seen_full:
                    out["errors"].append(f"ARCHIVE_DUPLICATE_PATH:{name}->{seen_full[full_key]}")
                    continue
                seen_full[full_key] = name
                for err in _metadata_errors(info):
                    out["errors"].append(f"ARCHIVE_METADATA_INVALID:{name}:{err}")
                if rel == "RELEASE_MANIFEST.json":
                    manifest_infos.append(info)
                    continue
                if rel == "BUNDLE_META.json":
                    bundle_meta_infos.append(info)
                    continue
                want = expected.get(rel)
                if want is None:
                    out["errors"].append(f"ARCHIVE_EXTRA_FILE:{rel}")
                    continue
                seen.add(rel)
                try:
                    declared_size = int(want.get("size"))
                except (TypeError, ValueError):
                    out["errors"].append(f"ARCHIVE_MANIFEST_SIZE_INVALID:{rel}")
                    continue
                if info.file_size != declared_size:
                    out["errors"].append(f"ARCHIVE_MEMBER_SIZE_MISMATCH:{rel}:{info.file_size}!={declared_size}")
                    continue
                got = _member_sha256(zf, info)
                if got != str(want.get("sha256") or "").lower():
                    out["errors"].append(f"ARCHIVE_MEMBER_SHA_MISMATCH:{rel}")

            if len(roots) != 1:
                out["errors"].append(f"ARCHIVE_ROOT_NOT_SINGLE:{sorted(roots.values())}")
            else:
                out["root"] = next(iter(roots.values()))
            for miss in sorted(set(expected) - seen):
                out["errors"].append(f"ARCHIVE_MISSING_FILE:{miss}")

            if len(manifest_infos) != 1:
                out["errors"].append(f"ARCHIVE_EMBEDDED_MANIFEST_COUNT:{len(manifest_infos)}")
            elif manifest_infos[0].file_size > 8 * 1024 * 1024:
                out["errors"].append("ARCHIVE_EMBEDDED_MANIFEST_TOO_LARGE")
            else:
                try:
                    embedded_manifest = json.loads(zf.read(manifest_infos[0]).decode("utf-8"))
                    if embedded_manifest != manifest:
                        out["errors"].append("ARCHIVE_EMBEDDED_MANIFEST_MISMATCH")
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    out["errors"].append(f"ARCHIVE_EMBEDDED_MANIFEST_INVALID:{type(exc).__name__}")

            if len(bundle_meta_infos) > 1:
                out["errors"].append(f"ARCHIVE_BUNDLE_META_COUNT:{len(bundle_meta_infos)}")
            elif bundle_meta_infos:
                info = bundle_meta_infos[0]
                if info.file_size > 1024 * 1024:
                    out["errors"].append("ARCHIVE_BUNDLE_META_TOO_LARGE")
                else:
                    try:
                        bundle_meta = json.loads(zf.read(info).decode("utf-8"))
                        if bundle_meta.get("schema") != "bundle_meta.v1":
                            out["errors"].append("ARCHIVE_BUNDLE_META_SCHEMA_INVALID")
                        if bundle_meta.get("package_hash") != manifest.get("package_hash"):
                            out["errors"].append("ARCHIVE_BUNDLE_META_PACKAGE_HASH_MISMATCH")
                        if bundle_meta.get("file_count") != manifest.get("file_count"):
                            out["errors"].append("ARCHIVE_BUNDLE_META_FILE_COUNT_MISMATCH")
                        if bundle_meta.get("version_forked") != manifest.get("skill_version"):
                            out["errors"].append("ARCHIVE_BUNDLE_META_VERSION_MISMATCH")
                    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                        out["errors"].append(f"ARCHIVE_BUNDLE_META_INVALID:{type(exc).__name__}")
    except (zipfile.BadZipFile, OSError, KeyError, RuntimeError) as e:
        out["errors"].append(f"ARCHIVE_READ_FAILED:{type(e).__name__}:{e}")
    out["archive_ok"] = not out["errors"]
    return out


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
    archive_arg = getattr(a, "archive", None)
    if archive_arg:
        arch = _verify_release_archive(Path(archive_arg).expanduser(), manifest,
                                       expected_archive_sha256=getattr(a, "expected_archive_sha256", "") or "")
        out["archive_verification"] = arch
        if not arch.get("archive_ok"):
            out["ok"] = False
    _print_json_or_text(out, getattr(a, "json", False))
    return 0 if out.get("ok") else 2


def _zip_write_file_deterministic(zf, src: Path, arcname: str):
    info = zipfile.ZipInfo(arcname)
    info.date_time = (1980, 1, 1, 0, 0, 0)
    info.compress_type = zipfile.ZIP_DEFLATED   # r194: cùng canon nén với _zip_write_bytes_deterministic
    info.create_system = 3
    info.extra = b""
    info.comment = b""
    # 0644 regular file; keep deterministic permissions.
    info.external_attr = 0o100644 << 16
    zf.writestr(info, src.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def _zip_write_bytes_deterministic(zf, data: bytes, arcname: str):
    # r194 (AMEND ADR-0007, user yêu cầu hạ size 24-07): ZIP_STORED → ZIP_DEFLATED mức 9 CỐ ĐỊNH —
    # bundle 6.4MB → ~1.5MB. Tính tất định GIỮ NGUYÊN cách ĐO: build ×2 CÙNG MÔI TRƯỜNG phải cùng SHA
    # (gate/CI vốn đo vậy — CI so 2 bản build CỦA CHÍNH NÓ, không so hash cố định xuyên máy); per-file
    # sha256 trong RELEASE_MANIFEST tính trên NỘI DUNG GIẢI NÉN nên bất biến với mức nén — release-verify
    # trong gói không đổi. Metadata vẫn đóng băng (date/attrs/extra) như ADR-0007.
    info = zipfile.ZipInfo(arcname)
    info.date_time = (1980, 1, 1, 0, 0, 0)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.extra = b""
    info.comment = b""
    info.external_attr = 0o100644 << 16
    zf.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)



def cmd_bundle_export(a) -> int:
    """v1.33.59 (ADR-0001 — quyết định grilling #2): sản phẩm CHUẨN của nhánh song song. Zip GIỮ NGUYÊN
    VERSION fork-point + nhúng BUNDLE_META.json (KHÔNG ghi ra đĩa — file META trên đĩa chính là cái bẫy
    khiến drive-push từ chối, đúng thiết kế: cây giải nén từ bundle không được publish)."""
    root = _release_root_from_arg(getattr(a, "root", None))
    out_path = Path(getattr(a, "out", None) or f"{root.name}-bundle.zip").expanduser().resolve()
    try:
        _relo = out_path.relative_to(root.resolve())
        if not (_relo.parts and _relo.parts[0] in _RELEASE_EXCLUDE_DIRS):
            out_path = (root.parent / out_path.name).resolve()
    except ValueError:
        pass
    top = "tra-luat"
    manifest = _build_release_manifest(root)
    if not manifest.get("ok"):
        res = {"ok": False, "error": "MANIFEST_NOT_OK", "required_missing": manifest.get("required_missing")}
        _print_json_or_text(res, getattr(a, "json", False)); return 2
    version_forked = ""
    try:
        version_forked = (root / "VERSION").read_text(encoding="utf-8").strip()
    except Exception:  # noqa: BLE001
        pass
    meta = {"schema": "bundle_meta.v1", "version_forked": version_forked,
            "package_hash": manifest.get("package_hash"), "file_count": manifest.get("file_count"),
            "note": str(getattr(a, "note", "") or ""),
            "protocol": ("ADR-0001: bundle KHÔNG mang version mới, KHÔNG được drive-push. Canonical merge "
                         "bundle rồi mới đánh số + publish. drive-push từ chối khi thấy BUNDLE_META.json.")}
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    if tmp.exists():
        tmp.unlink()
    _sha_by_rel = {f["path"]: f.get("sha256") for f in manifest.get("files", [])}
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_STORED) as zf:
        for f in manifest.get("files", []):
            p = root / f["path"]
            data = p.read_bytes()
            if _sha_by_rel.get(f["path"]) and hashlib.sha256(data).hexdigest() != _sha_by_rel[f["path"]]:
                try:
                    tmp.unlink()
                except FileNotFoundError:
                    pass
                res = {"ok": False, "error": "BUNDLE_EXPORT_FILE_CHANGED", "file": f["path"]}
                _print_json_or_text(res, getattr(a, "json", False)); return 2
            _zip_write_bytes_deterministic(zf, data, f"{top}/{f['path']}")
        _zip_write_bytes_deterministic(zf, json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"), f"{top}/RELEASE_MANIFEST.json")
        _zip_write_bytes_deterministic(zf, json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8"), f"{top}/BUNDLE_META.json")
    os.replace(tmp, out_path)
    _bundle_sha = _sha256_file(out_path)
    res = {"ok": True, "schema": "bundle_export.v1", "out": str(out_path), "version_forked": version_forked,
           "package_hash": manifest.get("package_hash"), "content_hash": manifest.get("content_hash"),
           "file_count": manifest.get("file_count"),
           "bundle_sha256": _bundle_sha, "archive_sha256": _bundle_sha,
           "note": "Giao zip này cho canonical merge. KHÔNG tự đánh version, KHÔNG drive-push (ADR-0001)."}
    _print_json_or_text(res, getattr(a, "json", False))
    return 0


def _release_secret_findings(rel: str, data: bytes) -> list:
    """r193 (PURE — sự cố 23-07: token webapp THẬT trong file backup config lọt bundle, nằm LIVE trên
    Drive tới khi script ship của user quét ra): quét NỘI DUNG từng member TRƯỚC khi ghi zip theo khuôn
    token `tl_[A-Za-z0-9]{20,}`. Trả list mô tả finding (token CẮT 10 ký tự — không in trọn secret);
    dữ liệu không decode utf-8 được → [] (token luôn nằm trong file text/JSON)."""
    if not data:
        return []
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return []
    return [f"{rel}: {t[:10]}…" for t in re.findall(r"tl_[A-Za-z0-9]{20,}", text)]


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
    top = getattr(a, "top", None) or "tra-luat"
    if not _portable_release_component(top):
        res = {"ok": False, "error": "INVALID_TOP_NAME", "top": top}
        _print_json_or_text(res, getattr(a, "json", False)); return 2
    manifest = _build_release_manifest(root)
    if not manifest.get("ok"):
        res = {"ok": False, "error": "MANIFEST_NOT_OK", "required_missing": manifest.get("required_missing"), "root": str(root)}
        _print_json_or_text(res, getattr(a, "json", False)); return 2
    # v1.34.58 (C-#13 — Q10): NLM import Capabilities nhận ≤200 file/zip — vượt là gói KHÔNG import được
    # (suýt dính 205 file khi `zip -r` tay cuốn .tl_state/golden/reports). FAIL sớm TRƯỚC khi ghi zip;
    # liệt kê 20 entry MỚI NHẤT theo mtime để lộ thủ phạm (thường artifact/report lọt vào cây).
    _n_entries = len(manifest.get("files") or []) + 1   # +1 = RELEASE_MANIFEST.json ghi thêm vào zip
    if _n_entries > 200:
        _newest = sorted((manifest.get("files") or []),
                         key=lambda f: ((root / f["path"]).stat().st_mtime
                                        if (root / f["path"]).exists() else 0.0),
                         reverse=True)[:20]
        res = {"ok": False, "error": "IMPORT_LIMIT_EXCEEDED", "entries": _n_entries, "limit": 200,
               "newest_20": [f["path"] for f in _newest],
               "note": "NLM import Capabilities nhận ≤200 file/zip — dọn file lạ khỏi cây skill (xem "
                       "newest_20) hoặc archive bớt references/ rồi build lại. KHÔNG ghi zip."}
        _print_json_or_text(res, getattr(a, "json", False))
        return 2
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    if tmp.exists():
        tmp.unlink()
    _sha_by_rel = {f["path"]: f.get("sha256") for f in manifest.get("files", [])}
    files = [root / f["path"] for f in manifest.get("files", [])]
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_STORED) as zf:
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
            # r193: CỔNG QUÉT TOKEN trong chính release-bundle (trước đây chỉ script ship của user quét
            # SAU khi build — bundle chứa token đã kịp lên Drive ở lượt deploy trước). Thấy token thật →
            # XOÁ zip tạm, FAIL rc=2, KHÔNG bao giờ phát hành.
            _sec93 = _release_secret_findings(rel, data)
            if _sec93:
                try:
                    tmp.unlink()
                except FileNotFoundError:
                    pass
                res = {"ok": False, "error": "TOKEN_IN_BUNDLE", "findings": _sec93[:10],
                       "note": "Member chứa token webapp thật (khuôn tl_…) — KHÔNG phát hành. Đưa file "
                               "config/backup ra khỏi cây skill (hoặc thêm exclude) rồi build lại; nếu "
                               "token từng lên Drive ở bản trước: XOAY TOKEN."}
                _print_json_or_text(res, getattr(a, "json", False))
                return 2
            _zip_write_bytes_deterministic(zf, data, f"{top}/{rel}")
        _zip_write_bytes_deterministic(zf, json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"), f"{top}/RELEASE_MANIFEST.json")
    bundle_sha = _sha256_file(tmp)
    # v1.34.45 (audit merge, ADR-0007): prove byte-for-byte reproducibility AT THE GATE — build the
    # bundle a second time and require an identical archive SHA-256. Prior releases only asserted
    # reproducibility by construction; this makes it a fail-closed check.
    _verify_tmp = out_path.with_suffix(out_path.suffix + ".verify.tmp")
    try:
        if _verify_tmp.exists():
            _verify_tmp.unlink()
        with zipfile.ZipFile(_verify_tmp, "w", compression=zipfile.ZIP_STORED) as zf2:
            for p in sorted(files, key=lambda x: str(x.relative_to(root)).replace(os.sep, "/")):
                rel = str(p.relative_to(root)).replace(os.sep, "/")
                _zip_write_bytes_deterministic(zf2, p.read_bytes(), f"{top}/{rel}")
            _zip_write_bytes_deterministic(zf2, json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"), f"{top}/RELEASE_MANIFEST.json")
        rebuild_sha = _sha256_file(_verify_tmp)
    except Exception as _rex:  # noqa: BLE001
        # v1.34.47 (F-05 residual): rebuild lỗi (vd source đổi giữa 2 lần build) → dọn CẢ tmp chính
        # (chưa os.replace) lẫn verify tmp, KHÔNG rò file + KHÔNG propagate uncaught.
        for _t in (tmp, _verify_tmp):
            try:
                _t.unlink()
            except FileNotFoundError:
                pass
        res = {"ok": False, "error": "RELEASE_BUNDLE_REBUILD_FAILED",
               "detail": f"{type(_rex).__name__}: {_rex}",
               "note": "Lần build thứ 2 (repro-gate) lỗi — cây có thể đang bị ghi; chạy lại khi ổn định."}
        _print_json_or_text(res, getattr(a, "json", False))
        return 2
    finally:
        try:
            _verify_tmp.unlink()
        except FileNotFoundError:
            pass
    if rebuild_sha != bundle_sha:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass
        res = {"ok": False, "error": "RELEASE_BUNDLE_NOT_REPRODUCIBLE", "out": str(out_path),
               "archive_sha256": bundle_sha, "archive_sha256_rebuild": rebuild_sha,
               "note": "Hai lần build cho SHA-256 khác nhau — bundle KHÔNG tái lập byte-for-byte (ADR-0007)."}
        _print_json_or_text(res, getattr(a, "json", False))
        return 2
    # Publish only after both independent builds agree. A failed reproducibility gate never
    # overwrites a previously valid release at ``out_path``.
    os.replace(tmp, out_path)
    res = {"ok": True, "schema": "release_bundle.v1", "out": str(out_path), "top": top,
           "file_count": manifest.get("file_count"), "total_bytes": manifest.get("total_bytes"),
           "package_hash": manifest.get("package_hash"), "bundle_sha256": bundle_sha,
           "warnings": ([_warn_redirect] if _warn_redirect else []),
           "content_hash": manifest.get("content_hash"),
           "archive_sha256": bundle_sha, "archive_sha256_rebuild": rebuild_sha, "reproducible": True,
           "note": "ZIP_DEFLATED-9 (r194 amend ADR-0007) root/thứ tự/timestamp/permission cố định; build ×2 cùng SHA."}
    _print_json_or_text(res, getattr(a, "json", False))
    return 0

# ── I11 (v1.34.18): leftover-sweep từ tl.py (affinity-tốt-nhất) ──


def _canonical_text(text: str) -> str:
    """CRLF và CR đơn lẻ -> LF. Đây là phép chuẩn hoá text canonical của ADR-0018.

    F2-A dựng hàm này vì `newline="\\n"` KHÔNG đủ và chỗ hụt rất dễ đọc nhầm: nó chỉ tắt phép
    dịch `\\n`→`\\r\\n` của Python lúc GHI, nó không đụng tới `\\r` đã nằm sẵn TRONG chuỗi. Tức là
    mọi artifact phái sinh dựng từ nội dung đọc ở một tệp CRLF (hoặc từ stdout một tiến trình
    Windows) vẫn ra CRLF, kể cả khi ghi qua writer "đã ghim LF". Đúng lớp hỏng mà `.gitattributes`
    một mình không chặn được, vì tệp phái sinh sinh ra rồi mới tới lượt git nhìn thấy.
    """
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _write_text_atomic(path: Path, text: str) -> None:
    """Writer text CANONICAL + NGUYÊN TỬ: UTF-8, LF, không phụ thuộc OS hay `core.autocrlf`.

    Đây là seam DUY NHẤT cho artifact tracked/derived — golden (`workflow.py` `golden-test
    --write`), `RELEASE_MANIFEST.json`, determinism/release report, chunk manifest, OCR text.
    Giữ nguyên ngữ nghĩa nguyên tử của v1.33.56 (F7): ghi ra tmp CÙNG thư mục rồi `os.replace`,
    nên không ai đọc được bản nửa vời và không có race đổi-tên-qua-volume.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    text = _canonical_text(text)
    _fd, _tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    with os.fdopen(_fd, "w", encoding="utf-8", errors="replace", newline="\n") as _f:   # v1.33.56 (F7): tmp duy nhất
        _f.write(text)
    os.replace(_tmp, str(path))

def _sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()
