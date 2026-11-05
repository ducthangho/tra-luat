"""Phép đo offline của reviewer; không ghi vào cay-kho/."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import time
import yaml

ROOT = Path(__file__).resolve().parent
REPO = ROOT / "cay-kho"
HEAD = "3ca0da3b94a3078199ca8712bc26aa3b04009226"
BASE = "1f0941e9bba1d1d517eda4174167b81963c06bd5"
WORKFLOW = ".github/workflows/ops-publish-lease.yml"
PYBIN = "/tmp/claude-0/-home-user-tra-luat/de0a61d6-485d-5aff-a726-b5b4e3780688/scratchpad/py312/bin"
ENV = dict(os.environ, PATH=PYBIN + ":/root/.local/bin:" + os.environ["PATH"],
           PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1", GIT_OPTIONAL_LOCKS="0")
LOGS = ROOT / "review-evidence"
LOGS.mkdir(exist_ok=True)


def record(identifier, command, rc, result, status="passed", **extra):
    path = ROOT / "VERDICT.md"
    data = yaml.safe_load(path.read_text())
    entry = dict(id=identifier, lenh=command, rc=rc, trang_thai=status, ket_qua=result, **extra)
    data["phep_do"].append(entry)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    print(json.dumps(entry, ensure_ascii=False), flush=True)


def run(identifier, args, cwd=REPO, expected=0, summary=None):
    started = time.monotonic()
    output = LOGS / (identifier + ".log")
    with output.open("w", encoding="utf-8") as stream:
        child = subprocess.run(args, cwd=cwd, env=ENV, stdout=stream, stderr=subprocess.STDOUT)
    text = output.read_text(encoding="utf-8", errors="replace")
    selected = [line for line in text.splitlines() if summary and re.search(summary, line)]
    result = "\n".join(selected[-15:]) if selected else text[-2000:] or "Không có diagnostic."
    okay = child.returncode == expected
    record(identifier, shlex.join(args), child.returncode, result,
           "passed" if okay else "failed", cwd=str(cwd), rc_mong_doi=expected,
           giay=round(time.monotonic()-started, 3), log=str(output.relative_to(ROOT)))
    if not okay:
        raise SystemExit(1)
    return text


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO, env=ENV)


def snapshot():
    result = {}
    for folder, directories, files in os.walk(REPO):
        for name in files:
            path = Path(folder) / name
            key = path.relative_to(REPO).as_posix()
            result[key] = ("symlink:" + os.readlink(path) if path.is_symlink()
                           else hashlib.sha256(path.read_bytes()).hexdigest())
    return result


def preflight():
    assert git("rev-parse", "HEAD").decode().strip() == HEAD
    assert git("cat-file", "-t", BASE).decode().strip() == "commit"
    assert git("merge-base", "--is-ancestor", BASE, HEAD) == b""
    assert git("status", "--porcelain=v1", "--untracked-files=all", "--ignored") == b""
    assert git("diff", "--no-ext-diff", BASE, HEAD) == (ROOT / "diff.patch").read_bytes()
    lease = yaml.safe_load((ROOT / "LEASE.yaml").read_text())
    expected_hash = "8f4f89a1414fd009f5a16be358925332c6c576a132710f5819e5cce7e778f5ce"
    assert hashlib.sha256((ROOT / "SPEC.md").read_bytes()).hexdigest() == expected_hash
    assert lease["spec_sha256"] == lease["spec_hash"] == expected_hash
    assert lease["revision"] == lease["generation"] == 1
    assert lease["base_sha"] == BASE and lease["review_class"] == "sensitive"
    assert lease["write_set"] == [WORKFLOW, "ops/handoff/wp1189-g1-claude.md"]
    (LOGS / "snapshot-before.json").write_text(json.dumps(snapshot(), sort_keys=True))
    record("preflight", "PY312 review_checks.py preflight", 0,
           "HEAD, base, hash SPEC.md và LEASE.yaml, r1/g1, write set, sensitive và diff.patch đều khớp; "
           "tracked/untracked/ignored sạch; tree=" + git("rev-parse", "HEAD^{tree}").decode().strip())


def static():
    source = (REPO / WORKFLOW).read_text()
    previous = git("show", BASE + ":" + WORKFLOW).decode()
    current, old = yaml.safe_load(source), yaml.safe_load(previous)
    steps = current["jobs"]["dang"]["steps"]
    found = [(i, s) for i, s in enumerate(steps) if str(s.get("uses", "")).startswith("actions/setup-python@")]
    assert len(found) == 1
    index, setup = found[0]
    assert setup == {"uses": "actions/setup-python@v5", "with": {"python-version": "3.12"}}
    assert steps[index-1]["uses"] == "actions/checkout@v4"
    assert steps[index+1]["name"] == "cài PyYAML"
    assert all(index < i for i, step in enumerate(steps) if "python3" in str(step.get("run", "")))
    steps.pop(index)
    assert current == old  # gồm on (PyYAML biểu diễn key này là True), permissions, if, env và mọi bước cũ.
    added = [line[1:] for line in (ROOT / "diff.patch").read_text().splitlines()
             if line.startswith("+") and not line.startswith("+++")]
    assert "${{" not in "\n".join(line for line in added if line.lstrip().startswith("#"))
    assert not re.search(r"/(?:usr|opt|bin|sbin)/[^\s\"']*python", source)
    ci = yaml.safe_load((REPO / ".github/workflows/ci.yml").read_text())
    ci_setups = [s for j in ci["jobs"].values() for s in j.get("steps", [])
                 if str(s.get("uses", "")).startswith("actions/setup-python@")]
    assert len(ci_setups) == 8
    assert all(s["uses"] == setup["uses"] and s["with"]["python-version"] == "3.12" for s in ci_setups)
    imports = {}
    for name in ("ops/lease_publish.py", "ops/lease_publish_test.py"):
        imports[name] = sorted({(n.module or "").split(".")[0] for n in ast.walk(ast.parse((REPO/name).read_text()))
                                if isinstance(n, ast.ImportFrom)} |
                               {a.name.split(".")[0] for n in ast.walk(ast.parse((REPO/name).read_text()))
                                if isinstance(n, ast.Import) for a in n.names})
    external = sorted({n for names in imports.values() for n in names if n and n not in sys.stdlib_module_names})
    (LOGS / "static.json").write_text(json.dumps(dict(setup_index=index, imports=imports,
        external_imports=external, ci_setup_count=len(ci_setups)), ensure_ascii=False, indent=2))
    record("static", "PY312 review_checks.py static", 0,
           "Đúng một setup-python@v5, python-version là chuỗi 3.12; steps[1], liền sau checkout, trước cài PyYAML "
           "và mọi run python3. Bỏ đúng bước mới thì toàn bộ YAML bằng base. 8/8 bước CI cùng @v5/3.12; "
           "chú thích mới không có biểu thức Actions; không có Python tuyệt đối trong workflow. "
           "Import ngoài stdlib của hai script: " + repr(external), log="review-evidence/static.json")
    actual = git("diff", "--numstat", BASE, HEAD)
    assert actual == (ROOT/"numstat.txt").read_bytes()
    rows = actual.decode().splitlines()
    assert len(rows) == 1
    insertions, deletions, path = rows[0].split("\t")
    assert path == WORKFLOW and int(insertions) <= 450
    record("A4", "git diff --numstat " + BASE + " " + HEAD, 0, actual.decode().strip())


def a1():
    run("A1", [PYBIN+"/python", "a1_check.py", "cay-kho/"+WORKFLOW], cwd=ROOT)
    folder = LOGS / "mutants"
    folder.mkdir(exist_ok=True)
    original = (REPO/WORKFLOW).read_text()
    block = '      - uses: actions/setup-python@v5\n        with:\n          python-version: "3.12"\n\n'
    assert original.count(block) == 1
    without = original.replace(block, "", 1)
    anchor = '        run: python3 -m pip install --quiet PyYAML==6.0.3\n'
    assert without.count(anchor) == 1
    mutants = dict(bo_buoc=without, phien_ban_3x=original.replace('python-version: "3.12"', 'python-version: "3.x"', 1),
                   sau_cai_PyYAML=without.replace(anchor, anchor + "\n" + block, 1))
    for name, text in mutants.items():
        path = folder / (name+".yml")
        path.write_text(text, encoding="utf-8")
        result = run("A1_"+name, [PYBIN+"/python", "a1_check.py", str(path)], cwd=ROOT, expected=1)
        assert result.strip() == "DO"


def tools():
    result = run("python_tools", ["python3", "-c",
        "import sys,yaml,shutil; print(sys.executable); print(sys.version); print('PyYAML='+yaml.__version__); "
        "print('python='+str(shutil.which('python'))); print('python3='+str(shutil.which('python3'))); "
        "print('actionlint='+str(shutil.which('actionlint'))); print('shellcheck='+str(shutil.which('shellcheck'))); "
        "assert sys.version_info[:2]==(3,12); assert yaml.__version__=='6.0.3'; "
        "assert shutil.which('actionlint'); assert shutil.which('shellcheck')"])
    run("actionlint_version", ["actionlint", "-version"])
    run("shellcheck_version", ["shellcheck", "--version"])


def a2():
    text = run("A2", ["python3", "ops/lease_publish_test.py"], summary=r"^lease_publish:|^  ĐỎ|^  BỎ QUA")
    match = re.search(r"^lease_publish: (\d+)/(\d+) đạt.*bỏ qua=(\d+)", text, re.M)
    okay = bool(match and int(match[1]) > 0 and match[1] == match[2] and match[3] == "0")
    record("A2_positive_evidence", "Đọc dòng tổng kết A2 (không chỉ rc)", 0 if okay else 1,
           match[0] if match else "Thiếu dòng tổng kết", "passed" if okay else "failed")
    assert okay


def a3():
    assert shutil.which("shellcheck", path=ENV["PATH"])
    run("A3", ["actionlint", "cay-kho/"+WORKFLOW], cwd=ROOT)


def a5():
    identifier = "A5_selftest_fixture_signing_off" if ENV.get("REVIEW_FIXTURE_SIGNING_OFF") == "1" else "A5_selftest"
    text = run(identifier, ["python", "scripts/tl.py", "--selftest"], summary=r"^== tl selftest|^  \[FAIL\]")
    match = re.search(r"^== tl selftest (\d+)/(\d+) ==", text, re.M)
    okay = bool(match and int(match[1]) > 0 and match[1] == match[2])
    record("A5_positive_evidence", "Đọc dòng tổng kết tl selftest", 0 if okay else 1,
           match[0] if match else "Thiếu dòng tổng kết", "passed" if okay else "failed")
    assert okay
    run("A5_diff_check", ["git", "diff", "--check", BASE, HEAD])


def a5_unsigned_fixture():
    count = int(ENV.get("GIT_CONFIG_COUNT", "0"))
    ENV.update({"GIT_CONFIG_COUNT": str(count+1), f"GIT_CONFIG_KEY_{count}": "commit.gpgsign",
                f"GIT_CONFIG_VALUE_{count}": "false", "REVIEW_FIXTURE_SIGNING_OFF": "1"})
    record("A5_fixture_environment", "Chỉ thêm process env GIT_CONFIG_COUNT/KEY_n=commit.gpgsign/VALUE_n=false", 0,
           "Tắt ký commit cho kho mẫu trong lượt selftest; không ghi config nào trong cay-kho hoặc config toàn cục. "
           "Giữ nguyên code và mọi case. Đây không phải phép xác minh chữ ký commit thật.")
    a5()


def final_snapshot():
    before = json.loads((LOGS/"snapshot-before.json").read_text())
    after = snapshot()
    changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
    (LOGS/"snapshot-after.json").write_text(json.dumps(after, sort_keys=True))
    assert not changed, changed
    assert git("rev-parse", "HEAD").decode().strip() == HEAD
    assert git("status", "--porcelain=v1", "--untracked-files=all", "--ignored") == b""
    record("read_only_final", "PY312 review_checks.py final_snapshot", 0,
           f"SHA-256 của toàn bộ {len(after)} tệp (gồm .git, tracked/untracked/ignored) không đổi; HEAD/tree không đổi; "
           "git status --porcelain=v1 --untracked-files=all --ignored rỗng. Snapshot chỉ chứng minh không có delta ở hai mốc.")


if __name__ == "__main__":
    globals()[sys.argv[1]]()
