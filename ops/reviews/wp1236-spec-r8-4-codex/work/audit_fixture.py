"""Integration model: generation 1 plus reference K7-S; this is NOT an r8 implementation."""
import copy
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import types
import yaml

W = pathlib.Path(__file__).resolve().parent
R = W.parent / "repo"
sys.path.insert(0, str(W / "author"))
import gram

def git(*args, cwd=R, data=None):
    return subprocess.check_output(["git", *args], cwd=cwd, input=data).decode().strip()

raw = git("show", "508d678:ops/gate_output_doi_chieu.py")
raw = raw.replace('Path(__file__).with_name("ci_provenance.py")', repr(str(R / "ops/ci_provenance.py")))
old = 'elif ly := che_do_shell(str(y.get("run", "")), y.get("shell")):\n                nm.append(f"{ly}:{s[\'name\'][:30]}")'
new = 'elif ly := cu_phap_run(y.get("run"), y.get("shell")):\n                nm.append(f"cu_phap_run:{ly}:{p[\'name\']}:{s[\'name\']}")'
assert raw.count(old) == 1
raw = raw.replace(old, new)
(W / "model_module.py").write_text(raw)
module = types.ModuleType("integration_model")
exec(compile(raw, "generation1_plus_K7S", "exec"), module.__dict__)
module.cu_phap_run = gram.cu_phap_run
test = types.ModuleType("fixture_generation1")
test.__file__ = str(W / "test_model.py")
os.environ["GATE_OUTPUT_DOI_CHIEU_GOC"] = str(R)
exec(compile(git("show", "508d678:ops/gate_output_doi_chieu_test.py"), test.__file__, "exec"), test.__dict__)
test.MA = W / "model_module.py"
goc = test.goc()

def commit(wf):
    blob = git("hash-object", "-w", "--stdin", cwd=goc, data=yaml.safe_dump(wf, allow_unicode=True, sort_keys=False).encode())
    tree = git("mktree", cwd=goc, data=f"100644 blob {blob}\tci.yml\n".encode())
    tree = git("mktree", cwd=goc, data=f"040000 tree {tree}\tworkflows\n".encode())
    tree = git("mktree", cwd=goc, data=f"040000 tree {tree}\t.github\n".encode())
    return git("-c", "user.name=review", "-c", "user.email=review@local", "commit-tree", tree,
               "-p", test.SHA_CK, "-m", "scratch fixture", cwd=goc)

wf = yaml.safe_load(test.ci_goc())
rewrite = {
    "tl selftest (co bang chung exact-identity)": "bash .github/checks/tl_selftest_bang_chung.sh\n",
    "release-bundle x2 cùng SHA-256": "bash .github/checks/release_bundle_x2.sh\n",
    "G5 manh ban kinh dot bien (#668)": "python ops/cong_cu_test.py\n",
    "lease-publish selftest (đo lại setup sau G5)": "bash ops/chay_lease_publish_test.sh\n",
    "don-nhanh selftest (chốt xoá nhánh)": "pwsh -NoProfile -File scripts/don-nhanh_test.ps1\n",
    "bo ca gate chay TRONG cgroup duoc uy quyen (Linux)": "bash ops/ci/gate_cgroup.sh\n",
}
for j in wf["jobs"].values():
    for step in j["steps"]:
        if step.get("name") in rewrite:
            step["run"] = rewrite[step["name"]]
            if step["name"].startswith("don-nhanh"):
                step.pop("shell")
sha = commit(wf)
text, original = test.f_ok()
p = copy.deepcopy(original)
for c in p["moc"]["checkout"]:
    c["sha"] = sha
out = {"F_ok": module.kiem(text, p, goc), "F_ok_goc": module.kiem(text, original, goc)}
assert out["F_ok"] == ("passed", [])
assert out["F_ok_goc"][0] == "not_measured" and len(out["F_ok_goc"][1]) == 13

out["A14_i_prime"] = {}
for shell in (None, "bash"):
    change = copy.deepcopy(wf)
    step = next(s for s in change["jobs"]["gate-packet-loop"]["steps"] if s.get("name") == "packet-loop selftest")
    step["run"] = "python .claude/dev/packet_loop_test.py | python ops/tee_test.py"
    if shell:
        step["shell"] = shell
    else:
        step.pop("shell", None)
    q = copy.deepcopy(p)
    ck = commit(change)
    for c in q["moc"]["checkout"]:
        c["sha"] = ck
    out["A14_i_prime"][str(shell)] = module.kiem(text, q, goc)

checks = {}
for name, run in (("remove_initial_bom", "\ufeffpython ops/x.py"), ("lowercase_initial_letter", "Python ops/x.py")):
    ns = {}
    exec(compile((W / (name + ".py")).read_text(), name, "exec"), ns)
    module.cu_phap_run = ns["cu_phap_run"]
    checks[name] = {"F_ok": module.kiem(text, p, goc), "F_ok_goc": module.kiem(text, original, goc)}
    change = copy.deepcopy(wf)
    next(s for s in change["jobs"]["gate-packet-loop"]["steps"] if s.get("name") == "packet-loop selftest")["run"] = run
    q = copy.deepcopy(p)
    ck = commit(change)
    for c in q["moc"]["checkout"]:
        c["sha"] = ck
    checks[name]["witness_mutant"] = module.kiem(text, q, goc)
    module.cu_phap_run = gram.cu_phap_run
    checks[name]["witness_reference"] = module.kiem(text, q, goc)
out["logic_mutants"] = checks
module.cu_phap_run = gram.cu_phap_run

# Existing suite's real-run fixture, built with moc_gate and no network calls.
test.nap = lambda: module
test.kq = lambda txt, pv, g=None: module.kiem(txt, pv, g or goc)
test.f_ok = lambda: (text, copy.deepcopy(p))
results = {}
for name in ("a03k_run_duong_nhanh_that", "a20_so_luat", "a21_pham_vi_land"):
    if name in test.__dict__:
        try:
            test.__dict__[name]()
            results[name] = "passed"
        except Exception as e:
            results[name] = type(e).__name__ + ": " + str(e)
out["existing_tests"] = results
out["registry_cases"] = {}
for label, before, after in (
    ("e_prime", '(sum(m[1] is None for m in mien) != 1)', 'False'),
    ("f", '(len(ds) != len(set(ds)))', 'False'),
    ("g", 'not set(CHECK_BAT_BUOC) <= set(ds)', 'False'),
    ("h", 'len(_muc(v, t)) != 1', 'len(_muc(v, t)) > 1'),
    ("i", 'len(_muc(v, t)) != 1', 'len(_muc(v, t)) < 1'),
    ("i_prime", 'MIEN_HIEU_LUC.get(k, (0, 0))[1] is None and', 'True and'),
):
    pair = []
    for mutate in (False, True):
        ns = {"__name__": "registry_model"}
        assert raw.count(before) == 1
        exec(compile(raw.replace(before, after) if mutate else raw, "registry_model", "exec"), ns)
        ns["cu_phap_run"] = gram.cu_phap_run
        law = copy.deepcopy(ns["LUAT_v1"])
        if label == "f":
            law["JOB_BAT_BUOC"].append(law["JOB_BAT_BUOC"][0])
        elif label in ("g", "i_prime"):
            law["JOB_BAT_BUOC"].remove("gate-ops (ubuntu-latest)")
        elif label == "h":
            law["JOB_BAT_BUOC"].append("khac (ubuntu-latest)")
        elif label == "i":
            law["MUC"].append(copy.deepcopy(law["MUC"][0]))
        key = ns["bam"](law)
        ns["LUAT_PHIEN_BAN"] = {key: law}
        ns["MIEN_HIEU_LUC"] = {key: (1, 9 if label in ("e_prime", "i_prime") else None)}
        if label == "i_prime":
            other = ns["LUAT_v1"]
            ns["LUAT_PHIEN_BAN"][ns["bam"](other)] = other
            ns["MIEN_HIEU_LUC"][ns["bam"](other)] = (10, None)
        pair.append({"registry": ns["kiem_so_luat"](), "kiem_has_registry_error": "so_luat_hong" in ns["kiem"](text, p, goc)[1]})
    out["registry_cases"][label] = pair
    assert pair[0]["kiem_has_registry_error"] != pair[1]["kiem_has_registry_error"]

# A15: match actual REST-success steps, not all YAML step names.
original_wf = yaml.safe_load(test.ci_goc())
a15 = []
for job in original["moc"]["gate_output"]["jobs"]:
    if job["conclusion"] == "skipped" or "ubuntu-latest" not in job["labels"] or job["name"] == "chuan-bi":
        continue
    rule = module._muc(module.LUAT_v1, job["name"])[0]
    ky = module.cp.ghep_job(job["name"], original_wf)
    for step in rule["buoc"]:
        actual = [b for b in job["buoc"] if b["name"] in step["ten"] and b["conclusion"] == "success"]
        assert len(actual) == 1
        ys = [s for s in original_wf["jobs"][ky]["steps"] if module.cp.ten_du_kien(s) == actual[0]["name"]]
        assert len(ys) == 1
        s = ys[0]
        a15.append((actual[0]["name"], gram.cp(s.get("run"), s.get("shell"))))
out["A15"] = {"pairs": len(a15), "accepted_pairs": sum(r is None for _, r in a15), "names": len(set(a15)),
              "accepted_names": len({n for n, r in a15 if r is None})}
out["fixture_parent"] = git("rev-parse", sha + "^", cwd=goc)
out["luat_sha256"] = module.bam(module.LUAT_v1)
(W / "audit_fixture.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"F_ok": out["F_ok"], "F_ok_goc": [out["F_ok_goc"][0], len(out["F_ok_goc"][1])],
                  "A14_i_prime": out["A14_i_prime"], "mutant_witnesses": {n: {k: v for k, v in r.items() if k.startswith("witness")} for n, r in checks.items()},
                  "existing_tests": results, "luat_sha256": out["luat_sha256"]}, ensure_ascii=False, indent=2))
