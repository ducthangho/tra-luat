import json, statistics, datetime as dt
from pathlib import Path
HERE = Path(__file__).parent
DO_LUC = "2026-09-07T03:54:32Z"   # UTC, luc goi API (date -u truoc lan goi dau)

runs = {int(k): v for k, v in json.load(open(HERE/"raw/runs.json")).items()}

A = ["Set up job","Force LF checkout (hash parity với manifest)","Run actions/checkout@v4","Run actions/setup-python@v5",
"cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)","cài actionlint cho G5","cài shellcheck cho G5 (cài xong đo lại)",
"cài rg cho G5 (cài xong đo lại)","G5 kiem ban ke cong cu + T1..T8 (packet","cài Ruff 0.15.15 và in probe dương",
"PR head contains required EOL base","py_compile","codex credential selftest (packet #300)","packet-loop selftest","bien-nhan v2 selftest",
"test registry (phạm vi + các bộ chưa được nối)","idiom-ba-ten selftest","eol-policy selftest","pre-push selftest",
"lease-publish selftest (đo lại setup sau G5)","don-nhanh selftest (chốt xoá nhánh)","bo ca gate chay TRONG cgroup duoc uy quyen (Linux)",
"gate lifecycle selftest (nen khong co cgroup)","eol-policy survey","bundled-fragment check (topology gói)","gen_instructions selftest",
"command-registry unit test (AG-T0-03)","tl selftest (luot PR — khong sinh bang chung)","tl selftest (co bang chung exact-identity)",
"tai len gate-evidence","workflow-audit strict","golden-test","doc-claims-check strict","determinism-audit strict",
"ci-phamvi guard (bang phu thuoc khop ma)","ci-phamvi selftest (phan chung — cong co rang)","release-check full",
"release-verify strict (lane LAND — manifest committed)","release-verify strict (lane WORKER — manifest TẠM ngoài repo)",
"release-bundle x2 cùng SHA-256","tl_boot smoke","Post Run actions/setup-python@v5","Post Run actions/checkout@v4","Complete job"]
NUM_A = list(range(1,42)) + [81,82,83]
B = [n for n in A if n != "bien-nhan v2 selftest"]
NUM_B = list(range(1,41)) + [79,80,81]
assert len(A)==44 and len(B)==43
LAYOUT = {"A": (A, NUM_A), "B": (B, NUM_B)}
CONC = {"S":"success","K":"skipped","C":"cancelled"}

def ts(date, hhmmss):
    return dt.datetime.strptime(date + hhmmss, "%Y-%m-%d%H%M%S").replace(tzinfo=dt.timezone.utc)
def iso(t): return t.strftime("%Y-%m-%dT%H:%M:%SZ")
def piso(s): return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)

jobs = []
cur = None
for line in open(HERE/"raw/jobs.txt", encoding="utf-8"):
    line = line.rstrip("\n")
    if not line or line.startswith("#"): continue
    if line.startswith("J "):
        run_id, job_id, name, conc, st, en, lay = line[2:].split("|")
        run_id = int(run_id); r = runs[run_id]; date = r["created_at"][:10]
        cur = dict(run_id=run_id, job_id=int(job_id), name=name, conclusion=conc, started=ts(date, st), completed=ts(date, en), layout=lay, steps=[], date=date)
        jobs.append(cur)
    else:
        c, st, en = line.split()
        cur["steps"].append((CONC[c], ts(cur["date"], st), ts(cur["date"], en)))

# kiem tra hinh dang
khong_do_duoc = []
for j in jobs:
    names, nums = LAYOUT[j["layout"]]
    assert len(j["steps"]) == len(names), (j["run_id"], j["name"], len(j["steps"]))
    prev = None
    for (c, s, e) in j["steps"]:
        assert e >= s, (j["run_id"], j["name"], s, e)
        if prev is not None: assert s >= prev, (j["run_id"], j["name"], s, prev)
        prev = e
    assert j["steps"][0][1] >= j["started"] and j["steps"][-1][2] <= j["completed"], (j["run_id"], j["name"])
run_ids_seen = {j["run_id"] for j in jobs}
for rid in runs:
    n = sum(1 for j in jobs if j["run_id"]==rid)
    if n != 2: khong_do_duoc.append(f"KHONG_DO_DUOC {rid} chi doc duoc {n}/2 job")
assert len(jobs) == 26

# job.tsv
rows = []
for j in jobs:
    r = runs[j["run_id"]]
    phut = (j["completed"]-j["started"]).total_seconds()/60
    rc, ru = piso(r["created_at"]), piso(r["updated_at"])
    rows.append(dict(run_id=j["run_id"], head7=r["head_sha"][:7], head_branch=r["head_branch"], event=r["event"], job_name=j["name"],
        conclusion=j["conclusion"], started_at=iso(j["started"]), completed_at=iso(j["completed"]), phut=f"{phut:.2f}",
        so_muc_liet_ke=len(j["steps"]), so_skipped=sum(1 for s in j["steps"] if s[0]=="skipped"),
        run_created_at=r["created_at"], run_updated_at=r["updated_at"], run_dau_cuoi_phut=f"{(ru-rc).total_seconds()/60:.2f}", _phut=phut))
cols = ["run_id","head7","head_branch","event","job_name","conclusion","started_at","completed_at","phut","so_muc_liet_ke","so_skipped","run_created_at","run_updated_at","run_dau_cuoi_phut"]
with open(HERE/"job.tsv","w",encoding="utf-8") as f:
    f.write("\t".join(cols)+"\n")
    for row in rows: f.write("\t".join(str(row[c]) for c in cols)+"\n")

# buoc.tsv
bcols = ["run_id","head7","job_name","step_number","step_name","step_conclusion","started_at","completed_at","giay"]
buoc = []
with open(HERE/"buoc.tsv","w",encoding="utf-8") as f:
    f.write("\t".join(bcols)+"\n")
    for j in jobs:
        names, nums = LAYOUT[j["layout"]]
        for (c,s,e), nm, num in zip(j["steps"], names, nums):
            g = int((e-s).total_seconds())
            buoc.append(dict(run_id=j["run_id"], job=j["name"], name=nm, num=num, conc=c, giay=g))
            f.write("\t".join(map(str,[j["run_id"], runs[j["run_id"]]["head_sha"][:7], j["name"], num, nm, c, iso(s), iso(e), g]))+"\n")

with open(HERE/"khong_do_duoc.txt","w",encoding="utf-8") as f:
    f.write("\n".join(khong_do_duoc) + ("\n" if khong_do_duoc else ""))

# tom_tat
def thongke(vals):
    if not vals: return "n=0"
    return (f"n={len(vals)} · min={min(vals):.2f} · max={max(vals):.2f} · biên độ={max(vals)-min(vals):.2f} · "
            f"trung vị={statistics.median(vals):.2f} · trung bình={statistics.mean(vals):.2f}")
def job_of(rid, nen):
    return next(r for r in rows if r["run_id"]==rid and r["job_name"]==f"gate ({nen}-latest)")
win_master = [r["_phut"] for r in rows if r["job_name"]=="gate (windows-latest)" and r["conclusion"]=="success" and r["head_branch"]=="master"]
ubu_master = [r["_phut"] for r in rows if r["job_name"]=="gate (ubuntu-latest)" and r["conclusion"]=="success" and r["head_branch"]=="master"]
win_all_ok = [r["_phut"] for r in rows if r["job_name"]=="gate (windows-latest)" and r["conclusion"]=="success"]
ubu_all_ok = [r["_phut"] for r in rows if r["job_name"]=="gate (ubuntu-latest)" and r["conclusion"]=="success"]

order = sorted(runs, key=lambda k: runs[k]["created_at"])
L = []
L.append("# Tóm tắt đo GitHub Actions — `ducthangho/tra-luat`, workflow `ci.yml`, job `gate`")
L.append("")
L.append(f"- Thời điểm đo (UTC): **{DO_LUC}** (lời gọi `get_workflow_run` + `list_workflow_jobs` qua MCP github, filter=all, perPage=100).")
L.append("- Đơn vị: **phút** (2 chữ số lẻ, = giây/60, KHÔNG làm tròn lên từng phút như GitHub tính tiền) trừ khi ghi `giây`. Mọi mốc thời gian là UTC.")
L.append("- `phut` của job = `completed_at − started_at` của JOB (theo API jobs). `run_dau_cuoi_phut` = `updated_at − created_at` của RUN.")
L.append(f"- Phạm vi: 13 run, 26 job (13 ubuntu + 13 windows), {len(buoc)} bước liệt kê. Run có 2 hình dạng: 44 mục (41 bước + 3 hậu xử lý) ở 11 run; 43 mục ở 2 run (`34048685345`, `34045664423` — chưa có bước `bien-nhan v2 selftest`).")
L.append(f"- Run không đọc được: **{len(khong_do_duoc)}** (xem `khong_do_duoc.txt`). Run duy nhất KHÔNG success: `34048229370` (workflow_dispatch, head 4cd80c5) — job windows `cancelled` ở bước 16 `test registry` sau 45 ph 18 s (17:34:14 → 18:19:32), job ubuntu success.")
L.append("")
L.append("## 1. Thống kê `phut` theo job — chỉ conclusion=success VÀ head_branch=master")
L.append("")
L.append(f"- `gate (windows-latest)`, master, success: {thongke(win_master)}")
L.append(f"- `gate (ubuntu-latest)`,  master, success: {thongke(ubu_master)}")
L.append("")
L.append("Tham khảo (KHÔNG thuộc yêu cầu, chỉ để so): mọi job success bất kể nhánh —")
L.append(f"- windows: {thongke(win_all_ok)}")
L.append(f"- ubuntu:  {thongke(ubu_all_ok)}")
L.append("")
L.append("## 2. Bảng theo run (sắp theo `created_at`)")
L.append("")
L.append("`phút tính tiền` = ubuntu×1 + windows×2 trên số phút THÔ (chưa làm tròn lên từng phút, chưa loại job cancelled); job `cancelled` vẫn tính phút chạy thật.")
L.append("")
L.append("| run_id | head7 | branch / event | ubuntu (ph) | windows (ph) | tính tiền (ph) | run_dau_cuoi (ph) | ghi chú |")
L.append("|---|---|---|---:|---:|---:|---:|---|")
tong_tien = 0.0
for rid in order:
    r = runs[rid]; u = job_of(rid,"ubuntu"); w = job_of(rid,"windows")
    tien = u["_phut"]*1 + w["_phut"]*2; tong_tien += tien
    gc = []
    if u["conclusion"]!="success": gc.append(f"ubuntu={u['conclusion']}")
    if w["conclusion"]!="success": gc.append(f"windows={w['conclusion']}")
    L.append(f"| {rid} | {r['head_sha'][:7]} | {r['head_branch']} / {r['event']} | {u['_phut']:.2f} | {w['_phut']:.2f} | {tien:.2f} | {u['run_dau_cuoi_phut']} | {'; '.join(gc)} |")
L.append(f"| **Tổng 13 run** | | | {sum(job_of(r,'ubuntu')['_phut'] for r in order):.2f} | {sum(job_of(r,'windows')['_phut'] for r in order):.2f} | **{tong_tien:.2f}** | | |")
L.append("")
L.append("## 3. Hai bước nặng + tổng 9 bước thiết lập (bước 2–10) theo run và nền — đơn vị phút")
L.append("")
L.append("`thiết lập 2–10` = tổng 9 bước có tên từ `Force LF checkout (hash parity với manifest)` tới `cài Ruff 0.15.15 và in probe dương` (số thứ tự API 2..10; `Set up job` #1 KHÔNG tính). Hai bước nặng: `test registry (phạm vi + các bộ chưa được nối)` và `packet-loop selftest`.")
L.append("")
L.append("| run_id | head7 | ubuntu: test registry | ubuntu: packet-loop | ubuntu: thiết lập 2–10 | windows: test registry | windows: packet-loop | windows: thiết lập 2–10 | ghi chú |")
L.append("|---|---|---:|---:|---:|---:|---:|---:|---|")
TR = "test registry (phạm vi + các bộ chưa được nối)"; PL = "packet-loop selftest"
SETUP = A[1:10]; assert SETUP[0].startswith("Force LF") and SETUP[-1].startswith("cài Ruff") and len(SETUP)==9
agg = {("ubuntu",TR):[],("ubuntu",PL):[],("ubuntu","setup"):[],("windows",TR):[],("windows",PL):[],("windows","setup"):[]}
for rid in order:
    cells = []; gc = []
    for nen in ("ubuntu","windows"):
        bs = [b for b in buoc if b["run_id"]==rid and b["job"]==f"gate ({nen}-latest)"]
        tr = next(b for b in bs if b["name"]==TR); pl = next(b for b in bs if b["name"]==PL)
        su = sum(b["giay"] for b in bs if b["name"] in SETUP)
        assert sum(1 for b in bs if b["name"] in SETUP)==9
        for key,val,conc in ((TR,tr["giay"],tr["conc"]),(PL,pl["giay"],pl["conc"]),("setup",su,"success")):
            if conc=="success": agg[(nen,key)].append(val/60)
        cells += [f"{tr['giay']/60:.2f}" + ("" if tr["conc"]=="success" else f" ({tr['conc']})"), f"{pl['giay']/60:.2f}", f"{su/60:.2f}"]
        if tr["conc"]!="success": gc.append(f"{nen} test registry {tr['conc']} — KHÔNG đưa vào thống kê")
    L.append(f"| {rid} | {runs[rid]['head_sha'][:7]} | " + " | ".join(cells) + f" | {'; '.join(gc)} |")
L.append("")
L.append("Thống kê theo nền, chỉ bước success (đơn vị phút):")
L.append("")
for nen in ("ubuntu","windows"):
    for key,label in ((TR,"test registry"),(PL,"packet-loop selftest"),("setup","thiết lập 2–10")):
        L.append(f"- {nen} · {label}: {thongke(agg[(nen,key)])}")
L.append("")
L.append("## 4. Bước `skipped` theo nền")
L.append("")
for nen in ("ubuntu","windows"):
    cnt = {}
    for b in buoc:
        if b["job"]==f"gate ({nen}-latest)" and b["conc"]=="skipped" and b["run_id"]!=34048229370:
            cnt[b["name"]] = cnt.get(b["name"],0)+1
    L.append(f"- {nen} (12 job, loại run cancelled): " + "; ".join(f"`{k}`×{v}" for k,v in sorted(cnt.items(), key=lambda kv:-kv[1])))
L.append("")
L.append("Ghi chú đọc: `PR head contains required EOL base` skipped ở mọi lượt KHÔNG phải pull_request (push/workflow_dispatch); `tl selftest (luot PR)` ↔ `tl selftest (exact-identity)` và `release-verify LAND` ↔ `WORKER` là cặp loại trừ theo lane; `don-nhanh`, `cgroup (Linux)`, `ci-phamvi selftest` chỉ chạy ubuntu; `gate lifecycle (nen khong co cgroup)` chỉ chạy windows.")
L.append("")
L.append("## 5. Nguồn")
L.append("")
L.append("- `job.tsv` (26 dòng), `buoc.tsv` (%d dòng), `khong_do_duoc.txt`, dữ liệu thô đã chép: `raw/runs.json`, `raw/jobs.txt`; script: `tinh.py`." % len(buoc))
L.append("- Dữ liệu bước được chép tay từ phản hồi MCP vào `raw/jobs.txt` rồi kiểm hình dạng bằng máy (số mục đúng layout, thời gian đơn điệu, nằm trong khung job). Số job/bước khớp 26 / %d." % len(buoc))
(HERE/"tom_tat.md").write_text("\n".join(L)+"\n", encoding="utf-8")
print("\n".join(L))
