"""Dung chan_k7 DUNG nhu dac ta r4 (Thiet ke muc 5, K7) roi chay tren ci.yml that.
Chay: cd repo && python -I ../work/k7_r4.py
"""
import re, sys, yaml, importlib.util, subprocess, collections
from pathlib import Path

def nap(ten, p):
    s = importlib.util.spec_from_file_location(ten, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

cp = nap("cp", "ops/ci_provenance.py")
dg = nap("dg", "ops/land/pr1231-wp1105-provenance/danh_gia_gate.py")

def wf_tai(sha, path=".github/workflows/ci.yml"):
    r = subprocess.run(["git", "show", f"{sha}:{path}"], capture_output=True, text=True)
    return cp.doc_wf(r.stdout) if r.returncode == 0 else None

def buoc_luat(steps, nhan):
    if nhan == dg.TL_SELFTEST:
        return [i for i, s in enumerate(steps) if "tl.py --selftest" in str(s.get("run", ""))]
    return [i for i, s in enumerate(steps) if nhan in str(s.get("run", ""))]

BASE = wf_tai("3163f4d")
LUAT = {}
for tt, ds in dg.LUAT:
    if tt == "chuan-bi":
        continue
    ks = [k for k in BASE["jobs"] if (tt.rstrip(" (") == k)]
    if not ks:
        print("KHONG THAY JOB", tt); continue
    steps = BASE["jobs"][ks[0]]["steps"]
    muc = []
    for nhan, _ in ds:
        idx = buoc_luat(steps, nhan)
        if len(idx) != 1:
            print("BUOC KHONG DUY NHAT", tt, nhan, idx)
        if idx:
            muc.append((nhan, {cp.ten_du_kien(steps[i]) for i in idx}, set().union(*[set((steps[i].get("env") or {}).keys()) for i in idx])))
    LUAT[tt] = muc

def pipefail(run):
    return "set -o pipefail" in run or "set -euo pipefail" in run

def co_ong(run, chi_ong_don=True):
    out = []
    for d in run.split("\n"):
        d = re.sub(r"'[^']*'|\"(?:\\.|[^\"\\])*\"", "", d)
        d = re.sub(r"(^|\s)#.*$", "", d)
        out.append(d)
    t = "\n".join(out)
    if chi_ong_don:
        return bool(re.search(r"(?<!\|)\|(?!\|)", t))
    return "|" in t

def chan_k7(wf, k, i, cho_phep_env):
    j, s = wf["jobs"][k], wf["jobs"][k]["steps"][i]
    ly = []
    if "defaults" in wf or "defaults" in j: ly.append("defaults")
    if cp._env_chan(wf) or cp._env_chan(j): ly.append("env_job_wf")
    if set(s) - (cp.KHOA_BUOC | {"env"}): ly.append("khoa_la:" + ",".join(sorted(set(s) - (cp.KHOA_BUOC | {"env"}))))
    if "env" in s and (type(s["env"]) is not dict or set(s["env"]) - cho_phep_env): ly.append("env_buoc")
    if s.get("shell", "bash") not in ("bash", "pwsh", "sh"): ly.append("shell")
    if any(re.search("GITHUB_(ENV|PATH)", str(t.get("run", ""))) for t in j["steps"][:i]): ly.append("github_env_truoc")
    if s.get("continue-on-error") not in (None, False): ly.append("coe")
    return ly

def k7_run(prov, wf):
    J = [j for j in prov["moc"]["gate_output"]["jobs"] if j["conclusion"] != "skipped"
         and "ubuntu-latest" in (j.get("labels") or []) and not j["name"].startswith("chuan-bi")]
    dem = collections.Counter(); chi = []
    for j in J:
        k = cp.ghep_job(j["name"], wf)
        tt = [t for t in LUAT if j["name"].startswith(t)]
        if k is None or len(tt) != 1:
            dem["khong_luat"] += 1; chi.append((j["name"], "khong_luat")); continue
        steps = wf["jobs"][k]["steps"]; ten_yaml = [cp.ten_du_kien(s) for s in steps]
        bn = j["buoc"] if isinstance(j["buoc"], list) else []
        loi_job = []
        for nhan, ten, env in LUAT[tt[0]]:
            rest = [b for b in bn if b["name"] in ten and b["conclusion"] != "skipped"]   # STEP ma tom ghi = buoc da chay
            if len(rest) != 1: loi_job.append(f"rest{len(rest)}:{nhan}:{[b['conclusion'] for b in bn if b['name'] in ten]}"); continue
            if rest[0]["conclusion"] != "success": loi_job.append(f"rest_{rest[0]['conclusion']}:{nhan}"); continue
            if sum(1 for b in bn if b["name"] == rest[0]["name"]) != 1: loi_job.append(f"rest_trung:{nhan}"); continue
            yml = [i for i, n in enumerate(ten_yaml) if n == rest[0]["name"]]
            if len(yml) != 1: loi_job.append(f"yaml{len(yml)}:{nhan}"); continue
            i = yml[0]; s = steps[i]
            c = chan_k7(wf, k, i, env)
            run = str(s.get("run", ""))
            if co_ong(run) and s.get("shell") in (None, "sh") and not pipefail(run): c.append("ong_khong_pipefail")
            if co_ong(run, False) and not co_ong(run) and s.get("shell") in (None, "sh") and not pipefail(run): c.append("CHI_||")
            if c: loi_job.append(f"chan{c}:{nhan}")
        if loi_job:
            dem["job_khong_qua"] += 1; chi.append((j["name"], loi_job))
        else:
            dem["job_qua"] += 1
    return len(J), dem, chi

if __name__ == "__main__":
    print("LUAT gia lap:", {t: len(v) for t, v in LUAT.items()}, "tong buoc", sum(len(v) for v in LUAT.values()))
    for t, v in LUAT.items():
        for nhan, ten, env in v:
            if env: print("  env cho phep", t, nhan, sorted(env))
    prov = yaml.safe_load(open("ops/land/pr1231-wp1105-provenance/ci/provenance.yaml", encoding="utf-8"))
    sha = {c["sha"] for c in prov["moc"]["checkout"] if c.get("trang_thai") == "passed"}
    print("F-that SHA checkout:", sha)
    n, dem, chi = k7_run(prov, wf_tai(sha.pop()))
    print("A15 F-that: J =", n, dict(dem))
    for x in chi: print("   ", x)
