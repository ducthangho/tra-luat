"""A3 (spec r9 §7): chạy `tieu_dung` (khối Lệnh kiểm đóng băng, trích từ SPEC r9) trên đầu vào THẬT của từng lượt M9.

Đầu vào: REST run / jobs (filter=all, đủ trang) / artifacts (đủ trang); gói artifact tải về (sha256 gói, từng tệp + băm + nội dung);
`job_ky_vong` do bên tiêu dùng TỰ lập từ tệp workflow tại H (không dùng mã producer). Ghi mọi readback ra thư mục đầu ra.
"""
import hashlib, io, json, os, pathlib, re, subprocess, sys, urllib.error, urllib.request, zipfile

import yaml

KHO = "ducthangho/tra-luat"
API = f"https://api.github.com/repos/{KHO}"
H = "f5af7469c03e7fe421a3704c731f390842260304"
SPEC_OID = "0883d49edc22cf261f471ef71f2dc5f323e8d667"
SPEC_SHA = "280f6f8d0dc97f29a79ed8ef94d3070d8ae1fe0487b549054137bcdbc4acbb0c"
GOC = pathlib.Path(sys.argv[1])            # repo checkout có đủ object
RA = pathlib.Path(sys.argv[2])             # thư mục ghi readback
RUNS = [int(x) for x in sys.argv[3:]]
TOKEN = os.environ["GITHUB_PAT"]


def git(*a):
    return subprocess.run(["git", "-C", str(GOC), *a], check=True, capture_output=True).stdout


class _KhongTheoChuyenHuong(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


_mo_khong_chuyen = urllib.request.build_opener(_KhongTheoChuyenHuong)


def get(url, raw=False):
    req = urllib.request.Request(url if url.startswith("http") else API + url,
                                 headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {TOKEN}"})
    try:
        with _mo_khong_chuyen.open(req) as r:
            b = r.read()
    except urllib.error.HTTPError as e:
        if e.code not in (301, 302, 303, 307, 308):
            raise
        # Artifact zip: GitHub trả 302 sang kho blob ký sẵn; KHÔNG gửi token tới đó.
        with urllib.request.urlopen(e.headers["Location"]) as r:
            b = r.read()
    return b if raw else json.loads(b)


def du_trang(path, key):
    out, page = [], 1
    while True:
        d = get(f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
        out += d[key]
        if len(out) >= d["total_count"] or not d[key]:
            if len(out) != d["total_count"]:
                raise SystemExit(f"{path}: thiếu trang {len(out)}/{d['total_count']}")
            return out
        page += 1


spec = git("show", f"{SPEC_OID}:ops/specs/wp1460-r1/SPEC.md")
assert hashlib.sha256(spec).hexdigest() == SPEC_SHA, "băm SPEC lệch"
txt = spec.decode("utf-8")
khoi = txt.split("## Lệnh kiểm", 1)[1].split("```python", 1)[1].split("```", 1)[0]
ns = {"__name__": "lenh_kiem"}
exec(compile(khoi, "<lenh kiem r9>", "exec"), ns)
S = json.loads(git("show", f"{H}:ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json"))
V = ns["bo_kiem"](S)
tree_h = git("rev-parse", f"{H}^{{tree}}").decode().strip()

# job_ky_vong: tự lập từ workflow tại H — khoá job, job có đúng một trục ma trận dạng danh sách => "<khoá> (<giá trị>)".
wf = yaml.safe_load(git("show", f"{H}:.github/workflows/ci-dot-bien-du.yml"))
E = []
for k, j in wf["jobs"].items():
    m = (j.get("strategy") or {}).get("matrix")
    if isinstance(m, dict):
        (truc,) = m.values()
        E += [f"{k} ({v})" for v in truc]
    else:
        E.append(k)

ket = {}
for rid in RUNS:
    d = RA / str(rid)
    d.mkdir(parents=True, exist_ok=True)
    run = get(f"/actions/runs/{rid}")
    jobs = du_trang(f"/actions/runs/{rid}/jobs?filter=all", "jobs")
    arts = du_trang(f"/actions/runs/{rid}/artifacts", "artifacts")
    for ten, v in (("run", run), ("jobs", jobs), ("artifacts", arts)):
        (d / f"readback-{ten}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    bn_art = [a for a in arts if a["name"] == f"bien-nhan-audit-{rid}-{run['run_attempt']}"]
    assert len(bn_art) == 1, f"run {rid}: không đúng một artifact biên nhận"
    goi = get(bn_art[0]["archive_download_url"], raw=True)
    assert "sha256:" + hashlib.sha256(goi).hexdigest() == bn_art[0]["digest"], "digest gói biên nhận lệch"
    (d / "bien-nhan-audit.zip").write_bytes(goi)
    z = zipfile.ZipFile(io.BytesIO(goi))
    assert z.namelist() == ["bien_nhan_audit.json"], z.namelist()
    b = json.loads(z.read("bien_nhan_audit.json"))
    tai_ve = {}
    for a in [r["dau_job"] for r in b["job"]] + [m["artifact"] for m in b["manh"]]:
        rest_a = next((x for x in arts if x["id"] == a["id"]), None)
        if rest_a is None:
            continue
        g = get(rest_a["archive_download_url"], raw=True)
        zz = zipfile.ZipFile(io.BytesIO(g))
        tep = []
        for n in zz.namelist():
            nd = zz.read(n)
            try:
                nd_json = json.loads(nd)
            except ValueError:
                nd_json = None
            tep.append({"ten": n, "sha256": hashlib.sha256(nd).hexdigest(), "noi_dung": nd_json})
        tai_ve[str(a["id"])] = {"sha256_goi": hashlib.sha256(g).hexdigest(), "tep": tep}
    (d / "tai_ve.json").write_text(json.dumps(tai_ve, ensure_ascii=False, indent=1), encoding="utf-8")
    ngoai = {"job_ky_vong": E, "h": H, "tree_h": tree_h, "tai_ve": tai_ve}
    vp, canh, moc = ns["tieu_dung"](V, b, {"run": run, "jobs": jobs, "artifacts": arts}, ngoai)
    ket[rid] = {"hop_le_schema": V["bien_nhan"].is_valid(b), "ok": b["ok"], "sha": b["su_kien"]["sha"],
                "run_id": b["luot"]["run_id"], "kiem_ke_job": b["kiem_ke_job"], "vi_pham": sorted(vp), "canh_bao": canh,
                "moc": moc, "run_status": run["status"], "run_conclusion": run["conclusion"],
                "jobs": {j["name"]: j["conclusion"] for j in jobs}, "so_artifact_tai": len(tai_ve),
                "definition": b["dinh_danh_definition"]["trang_thai"]}

r1, r2 = (ket[r] for r in RUNS)
tong = {"luot": ket, "job_ky_vong": E, "tree_h": tree_h,
        "cung_kiem_ke_job": r1["kiem_ke_job"] == r2["kiem_ke_job"], "khac_run_id": r1["run_id"] != r2["run_id"]}
(RA / "a3-ket-qua.json").write_text(json.dumps(tong, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(tong, ensure_ascii=False, indent=1))
dat = all(k["hop_le_schema"] and k["ok"] is True and k["sha"] == H and not k["vi_pham"] and k["run_conclusion"] == "success"
          and len(k["jobs"]) == 11 and all(c == "success" for c in k["jobs"].values()) for k in ket.values()) \
      and tong["cung_kiem_ke_job"] and tong["khac_run_id"]
print("A3 TIEU_DUNG:", "DAT" if dat else "KHONG DAT")
sys.exit(0 if dat else 1)
