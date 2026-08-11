# -*- coding: utf-8 -*-
"""F2-A (ADR-0018) — chay cac bundled fragment case THAT tren topology bundle da giai nen.

Vi sao can rieng mot cong: canonical selftest chay o CAY DEV, noi `scripts/test_fragments/` va
`.editorconfig` deu co mat. Ban phat hanh KHONG co hai thu do — `_RELEASE_EXCLUDE_DIRS` loai
`scripts/test_fragments/` va `_RELEASE_EXCLUDE_NAMES` loai `.editorconfig` — nen mot fragment co
the XANH o cay dev va NO o goi. Da xay ra that: `wp49_eol_policy_index_blobs` doc `.editorconfig`,
selftest dev 1696/1696 nhung selftest trong bundle giai nen bao FAIL. Khong co cong nay thi lop
hong do chi lo ra o phien Cowork, sau khi da deploy.

Cong nay KHONG doi "selftest bundle xanh tron". Da DO nen o base `fc50a54`: selftest trong bundle
giai nen = 1692/1695, rc=1, do san ba ca phu thuoc cay dev (`r291_docs_ngoai_goi`,
`r330_deploy_msg_khong_chay_lenh`, `r264_doc_claims_phu_docs`) vi bundle khong mang `docs/` lan
script deploy. Doi bundle xanh tron la doi thu chua tung dung o base. Vi vay pham vi dung la:
MOI bundled fragment case phai xanh, va tap TEST_ID trong bundle phai TRUNG tap fragment cay dev.

Hop dong fragment — nap, doc TEST_ID, kiem `run`, chay — THUOC VE `scripts/tl_core/test_fragments.py`.
Cong nay CHI la NGUOI GOI: `discover_fragment_test_ids` cho cay dev, `load_runtime_fragment_cases`
ben trong goi da giai nen (cung duong ma canonical selftest di trong mot ban phat hanh). KHONG dung
loader hay parser thu hai. Ly do khong phai thi hieu: mot ban sao SE troi lech khoi canonical, va no
noi doi theo CA HAI huong. Da do THAT bang probe `wp999_file_probe` trong vong review 4 —

    exec(compile(source, name, "exec"), {})   khong seed `__file__` nen mot fragment HOP LE dung
                                             `__file__` chet `NameError: name '__file__' is not
                                             defined`, trong khi canonical seed du
                                             `__file__`/`__name__`/`__package__`.
    regex TEST_ID kieu ^TEST_ID = "..."       bo sot `TEST_ID: str = 'wp999_file_probe'` (annotated
                                             + nhay don) ma hop dong AST canonical nhan binh thuong.

Ban sao con lam RUNG mat cac chot canonical: kiem `run` callable + chu ky, tu choi coroutine/
generator, `PATH_ID_MISMATCH`, va bat trung TEST_ID.

Dev-side: nam duoi `.github/` nen bi loai khoi goi, khong an khe nao trong tran 200 tep.

Dung:
    python .github/checks/bundle_fragment_check.py [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

# Driver chay BEN TRONG cay da giai nen: nap tl that cua goi roi giao TOAN BO viec nap fragment cho
# hop dong canonical. Nhan goc goi qua argv (tuyet doi) thay vi duong dan tuong doi theo cwd.
# Khuon nay TRUNG voi `.githooks/eol_policy_test.py::case_release_bundle_chay_real_wp49_fragment`.
_DRIVER = r'''
import json, sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
import tl as tl_module
from tl_core.test_fragments import load_runtime_fragment_cases

payload = {"cases": [], "load_error": None}
try:
    cases = load_runtime_fragment_cases(root / "scripts")
except BaseException as exc:
    payload["load_error"] = "%s: %s" % (type(exc).__name__, exc)
    cases = ()
for case in cases:
    try:
        ok, err = bool(case.run(tl_module)), None
    except BaseException as exc:
        ok, err = False, "%s: %s" % (type(exc).__name__, exc)
    payload["cases"].append({"name": Path(case.source_path).name, "test_id": case.test_id,
                             "ok": ok, "error": err})
sys.stdout.write(json.dumps(payload, ensure_ascii=False))
'''


def _run(args, cwd=None):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    return subprocess.run(args, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _repo_root():
    p = _run(["git", "rev-parse", "--show-toplevel"])
    if p.returncode != 0:
        return Path.cwd()
    return Path(p.stdout.decode("utf-8", "replace").strip())


def _dev_test_ids(root):
    """TEST_ID khai trong cay dev, doc qua hop dong AST canonical (van KHONG chay code fragment).

    Fail CLOSED: fragment sai hop dong lam `discover_fragment_test_ids` nem, va nguoi goi bien no
    thanh `DEV_FRAGMENT_DISCOVERY_FAILED`. Regex cu lang le BO QUA tep khong khop — nghia la mot
    fragment hong lai lam tap ID CO LAI, va phep so sanh voi bundle dung mot cach vo nghia.
    """
    sys.path.insert(0, str(root / "scripts"))
    from tl_core.test_fragments import discover_fragment_test_ids
    entries = discover_fragment_test_ids(root / "scripts" / "test_fragments")
    return {entry.test_id for entry in entries}


def _extracted_root(base):
    """Zip goi noi duoi mot thu muc goc; tim dung thu muc co `scripts/tl.py`."""
    if (base / "scripts" / "tl.py").is_file():
        return base
    for child in sorted(base.iterdir()):
        if child.is_dir() and (child / "scripts" / "tl.py").is_file():
            return child
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Chay bundled fragment cases tren bundle da giai nen.")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    root = _repo_root()
    payload = {"schema": "bundle_fragment_check.v1", "ok": False}

    with tempfile.TemporaryDirectory(prefix="bundle_frag_") as tmp:
        tmpd = Path(tmp)
        zip_path = tmpd / "bundle.zip"
        built = _run([sys.executable, "scripts/tl.py", "release-bundle",
                      "--out", str(zip_path), "--json"], cwd=str(root))
        if built.returncode != 0 or not zip_path.is_file():
            payload["error"] = "RELEASE_BUNDLE_FAILED"
            payload["detail"] = built.stderr.decode("utf-8", "replace")[-500:]
            return _emit(payload, a.json)

        xdir = tmpd / "x"
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(xdir)
        xroot = _extracted_root(xdir)
        if xroot is None:
            payload["error"] = "EXTRACTED_ROOT_NOT_FOUND"
            return _emit(payload, a.json)

        # Topology phai DUNG la topology goi, neu khong ca test nay do sai thu.
        payload["topology"] = {
            "has_bundled_module": (xroot / "scripts" / "tl_test_fragments_bundled.py").is_file(),
            "dev_fragments_absent": not (xroot / "scripts" / "test_fragments").exists(),
            "editorconfig_absent": not (xroot / ".editorconfig").exists(),
            "gitattributes_present": (xroot / ".gitattributes").is_file(),
        }

        driver = tmpd / "driver.py"
        driver.write_text(_DRIVER, encoding="utf-8", newline="\n")
        got = _run([sys.executable, str(driver), str(xroot)], cwd=str(xroot))
        try:
            driver_out = json.loads(got.stdout.decode("utf-8", "replace"))
            cases = driver_out["cases"]
            load_error = driver_out["load_error"]
        except (ValueError, KeyError, TypeError):
            payload["error"] = "DRIVER_NON_JSON"
            payload["detail"] = (got.stdout + got.stderr).decode("utf-8", "replace")[-800:]
            return _emit(payload, a.json)

    # Hong luc NAP khac hong luc CHAY: gop chung vao `BUNDLED_FRAGMENT_FAILED` la bao sai benh.
    dev_error = None
    try:
        dev_ids = _dev_test_ids(root)
    except BaseException as exc:
        dev_ids, dev_error = set(), "%s: %s" % (type(exc).__name__, exc)
    bundle_ids = {c["test_id"] for c in cases}
    failed = [c for c in cases if not c["ok"]]

    payload.update({
        "cases": cases,
        "case_count": len(cases),
        "dev_test_ids": sorted(dev_ids),
        "bundle_test_ids": sorted(bundle_ids),
        "failed": failed,
        "load_error": load_error,
        "dev_discovery_error": dev_error,
    })

    # Chong RONG va chong TROI: bundle rong thi "khong ca nao hong" la dung mot cach vo nghia;
    # bundle thieu mot fragment cua cay dev thi goi da mat mot cong ma khong ai thay.
    # Thu tu CO CHU DICH: `payload["error"]` lay `problems[0]`, nen hong luc NAP phai dung TRUOC.
    # Loader nem ⇒ `cases` rong ⇒ `NO_BUNDLED_CASES` cung do, nhung do la TRIEU CHUNG; bao no thay
    # cho nguyen nhan se dua nguoi doc di sai huong.
    problems = []
    if load_error:
        problems.append("BUNDLED_FRAGMENT_LOAD_FAILED")
    if dev_error:
        problems.append("DEV_FRAGMENT_DISCOVERY_FAILED")
    if not cases:
        problems.append("NO_BUNDLED_CASES")
    if dev_ids != bundle_ids:
        problems.append("TEST_ID_SET_MISMATCH")
    if failed:
        problems.append("BUNDLED_FRAGMENT_FAILED")
    if not all(payload["topology"].values()):
        problems.append("UNEXPECTED_TOPOLOGY")

    payload["ok"] = not problems
    if problems:
        payload["error"] = problems[0]
        payload["problems"] = problems
    return _emit(payload, a.json)


def _emit(payload, as_json):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if as_json:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    else:
        sys.stdout.write("bundle_fragment_check: ok=%s cases=%s\n"
                         % (payload.get("ok"), payload.get("case_count")))
        for c in payload.get("failed", []):
            sys.stdout.write("  FAIL %s: %s\n" % (c.get("test_id"), c.get("error")))
        if payload.get("load_error"):
            sys.stdout.write("  load_error=%s\n" % payload["load_error"])
        if payload.get("dev_discovery_error"):
            sys.stdout.write("  dev_discovery_error=%s\n" % payload["dev_discovery_error"])
        if payload.get("error"):
            sys.stdout.write("  error=%s\n" % payload["error"])
    return 0 if payload.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
