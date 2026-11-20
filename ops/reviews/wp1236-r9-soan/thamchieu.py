"""Ban tham chieu do corpus cho dac ta wp1236 r9 (KHONG phai ma thi cong)."""
import re, sys, json, hashlib, unicodedata
from pathlib import Path
import yaml

RE_DAU = re.compile(r"# Danh gia Gate output run (\d+) attempt (\d+) head ([0-9a-f]{40}) — .*\(danh_gia_gate\.py sha256 ([0-9a-f]{64})\)")
RE_JOB = re.compile(r"JOB (\d+) (.+?) \[([^\]]*)\] conclusion=(\w+) log_sha256=([0-9a-f]{64}) -> (passed|failed|not_measured): (.*)")
RE_SKIP = re.compile(r"JOB (\d+) (.+?): skipped (\(khong tinh\)|-> not_measured \(khong suy pass\))")
RE_MOC = re.compile(r"MOC_GATE_OUTPUT: (passed|failed|not_measured) \((\d+)/(\d+) job co dau hieu duong\)")
BO_SINH = {"b87f9697345906e01b85e1db164d9aff2f9021db4bed1c63bc165b59583d9fcd": "v1",
           "539fed68fdd6bdeadb3b70b4ce998419b19afc408ba82bc4152b337d28010a24": "v2",
           "0ea9a5e9b5a663ea6050a934b6116b1d8fcc51b23207510fe9cd056342058faf": "v3"}
CHECK_BAT_BUOC = ["gate (ubuntu-latest)", "gate-packet-loop (ubuntu-latest)", "gate-ops (ubuntu-latest)",
                  "gate-registry (ubuntu-latest)", "gate-cong-cu-gop (ubuntu-latest)"]

def doc_danh_gia(p):
    b = p.read_bytes()
    try: t = b.decode("utf-8")
    except UnicodeDecodeError: return None, ["khong_phai_utf8"]
    if t.endswith("\n"): t = t[:-1]
    dong = t.split("\n")
    if any(d.endswith("\r") for d in dong):
        if not all(d.endswith("\r") for d in dong): return None, ["xuong_dong_tron"]
        dong = [d[:-1] for d in dong]
    if any("\r" in d for d in dong): return None, ["cr_le"]
    m = RE_DAU.fullmatch(dong[0]) if dong else None
    if not m: return None, ["dau_tep_sai"]
    dau = dict(run=int(m[1]), attempt=int(m[2]), head=m[3], bo_sinh=m[4])
    jobs, skip, moc, ly = {}, {}, None, []
    for d in dong[1:]:
        if not d: continue
        if (j := RE_JOB.fullmatch(d)):
            if int(j[1]) in jobs or int(j[1]) in skip: ly.append("job_lap")
            jobs[int(j[1])] = dict(name=j[2], labels=j[3], conclusion=j[4], sha=j[5], tt=j[6])
        elif (s := RE_SKIP.fullmatch(d)):
            skip[int(s[1])] = dict(name=s[2], v3=s[3].startswith("->"))
        elif (mm := RE_MOC.fullmatch(d)):
            if moc: ly.append("moc_lap")
            moc = (mm[1], int(mm[2]), int(mm[3]))
        else:
            ly.append("dong_la")
    return dict(dau=dau, jobs=jobs, skip=skip, moc=moc), ly

def tim_prov(goc):
    out = []
    for f in sorted(goc.rglob("*.yaml")):
        try: y = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception: continue
        if isinstance(y, dict) and y.get("schema") == "ci_provenance/1": out.append((f, y))
    return out

def kiem_tep(p, goc):
    d, ly = doc_danh_gia(p)
    if d is None: return "not_measured", ly
    dau = d["dau"]
    if dau["bo_sinh"] not in BO_SINH: ly.append("bo_sinh_la")
    pv = [(f, y) for f, y in tim_prov(goc) if y["moc"]["run"].get("run_id") == dau["run"]
          and y.get("attempt_yeu_cau") == dau["attempt"] and y["moc"]["run"].get("head_sha") == dau["head"]]
    if len(pv) != 1: return "not_measured", ly + [f"provenance_{len(pv)}"]
    y = pv[0][1]; r = y["moc"]["run"]
    if not (r.get("event") == "push" and r.get("loi_khai_rest_path") == ".github/workflows/ci.yml"): ly.append("khong_phai_run_land")
    go = y["moc"].get("gate_output") or {}
    if not (r.get("trang_thai") == "passed" and (go.get("tap_jobs") or {}).get("trang_thai") == "passed"
            and all(isinstance(c, dict) and c.get("trang_thai") in ("passed", "skipped") for c in y["moc"].get("checkout") or [None])
            and all(c.get("trang_thai") == "passed" for c in y["moc"].get("checkout") if c.get("trang_thai") != "skipped" or c.get("job_id") not in {q.get("job_id") for q in y["moc"]["gate_output"]["jobs"] if isinstance(q, dict) and q.get("conclusion") == "skipped"})):
        ly.append("provenance_chua_du")
    pj = {j["job_id"]: j for j in y["moc"]["gate_output"]["jobs"] if isinstance(j, dict)}
    khong_skip = {k for k, j in pj.items() if j.get("conclusion") != "skipped"}
    if set(d["jobs"]) != khong_skip: ly.append(f"tap_job_lech:{len(d['jobs'])}/{len(khong_skip)}")
    if set(d["skip"]) != set(pj) - khong_skip: ly.append("tap_skip_lech")
    ldd = y.get("log_day_du") or {}
    for k, j in d["jobs"].items():
        q = pj.get(k)
        if q is None: continue
        if q.get("name") != j["name"] or q.get("conclusion") != j["conclusion"] or ",".join(q.get("labels") or []) != j["labels"]: ly.append(f"job_lech:{k}")
        if str((ldd.get(k) or {}).get("sha256")) != j["sha"]: ly.append(f"log_sha_lech:{k}")
        if (j["tt"] == "passed" and j["conclusion"] != "success") or (j["conclusion"] != "success" and j["tt"] != "failed"): ly.append(f"ket_luan_lech:{k}")
    if d["moc"] is None: ly.append("thieu_moc")
    if ly: return "not_measured", ly
    v3 = BO_SINH[dau["bo_sinh"]] == "v3"
    if any(s["v3"] != v3 for s in d["skip"].values()): return "not_measured", ["dong_skip_sai_phien_ban"]
    tts = [j["tt"] for j in d["jobs"].values()] + (["not_measured"] * len(d["skip"]) if v3 else [])
    moc_tu = "passed" if tts and all(t == "passed" for t in tts) else ("failed" if "failed" in tts else "not_measured")
    if d["moc"] != (moc_tu, tts.count("passed"), len(tts)): return "not_measured", [f"moc_lech:{d['moc']}"]
    if "failed" in tts: return "failed", []
    ten = {j["name"]: j["tt"] for j in d["jobs"].values()}
    thieu = [c for c in CHECK_BAT_BUOC if ten.get(c) != "passed"]
    if d["skip"]: return "not_measured", ["co_job_skipped"]
    if thieu: return "not_measured", ["check_bat_buoc:" + c for c in thieu]
    return moc_tu, []

if __name__ == "__main__":
    root = Path(sys.argv[1])
    kq = []
    for p in sorted(root.glob("ops/land/**/danh-gia-gate-output-*.txt")):
        rel = p.relative_to(root / "ops/land").parts[0]
        goc = root / "ops/land" / rel
        tt, ly = kiem_tep(p, goc)
        kq.append((str(p.relative_to(root)), tt, ly))
    for k in kq: print(k[1], k[0], ",".join(k[2])[:200])
    from collections import Counter; print(Counter(k[1] for k in kq))
