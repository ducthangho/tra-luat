"""Kiem tinh nhat quan cua ho so land PR #621 voi hien vat trong thu muc provenance (Codex PR #723, review 5472526875).

Chay:  python -I kiem_ho_so.py [--repo <clone day du co 6980e5b, 675895d, 8b59185, 658bd0c, 3fc0932>]
Thoat 0 = moi chot dat; 1 = co chot truot (in tung chot); 2 = khong truot nhung thieu --repo nen chot digest
KHONG DO DUOC (khong duoc doc thanh DAT). Chi doc tep; --repo thi goi them `git diff` (chi doc).
KHONG la bang chung luot goc: no chi kiem rang moi loi khai `measured` trong ho so tro toi mot hien vat co that, co dau
duong, va cac moc thoi gian/run/digest khop nhau.
"""
import hashlib, json, re, subprocess, sys
from datetime import datetime
from pathlib import Path

import yaml

P = Path(__file__).resolve().parent
HO_SO = P.parent / "pr621-skill-bai-hoc-land-evidence.yaml"
LOI = []
# H5 — moi lenh git cua bo kiem chay trong moi truong BIET TRUOC: bo GIT_* (GIT_DIR/GIT_WORK_TREE lam `-C` vo hieu: do 09-10-2026,
# GIT_DIR=<kho day du> + `--repo <kho nong>` van ra DAT), khong doc cau hinh toan cuc/he thong (diff.noprefix hoac diff.algorithm
# doi digest => TRUOT gia), khong ap `git replace`.
import os
_GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
_GIT_ENV.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_NO_REPLACE_OBJECTS="1")


def chot(dk, msg):
    print(("DAT  " if dk else "TRUOT ") + msg)
    if not dk:
        LOI.append(msg)


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))




class _Nghiem(yaml.SafeLoader):
    """H6 — `yaml.safe_load` nhan khoa LAP va lay gia tri CUOI: `landed: false` roi `landed: true` doc ra true, con mat nguoi doc ra false."""


def _khong_lap(loader, node, deep=False):
    loader.flatten_mapping(node)
    khoa = [loader.construct_object(k, deep=True) for k, _ in node.value]
    lap = sorted({str(k) for k in khoa if khoa.count(k) > 1})
    if lap:
        raise ValueError(f"YAML: khoa lap {lap}")
    return yaml.SafeLoader.construct_mapping(loader, node, deep)


_Nghiem.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _khong_lap)
h = yaml.load(HO_SO.read_text(encoding="utf-8"), Loader=_Nghiem)
DA_DOC = set()


# Khoa tuong thuat/tro-toi: khong phai loi khai co the doi gia tri (lenh = cach tai lap, readback = ten tep, ...).
_TUONG_THUAT = {"dinh_chinh", "ghi_chu", "lenh", "mo_ta", "kiem_bang_may", "checkout", "pham_vi", "nguon", "readback", "vai_tro"}


def _la_measured(o, p=(), trong=False):
    """H1 — moi la scalar nam trong nut `trang_thai: measured`, hoac chuoi mo dau bang `measured` (tru khoa tuong thuat)."""
    if isinstance(o, dict):
        trong = trong or o.get("trang_thai") == "measured"
        for k, v in o.items():
            if k not in _TUONG_THUAT:
                yield from _la_measured(v, p + (k,), trong)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _la_measured(v, p + (i,), trong)
    elif (trong and not (isinstance(o, str) and o.startswith("not_measured"))) or (isinstance(o, str) and o.startswith("measured")):
        yield p, o


def _doi_so(v):
    if isinstance(v, bool):
        return not v
    if isinstance(v, (int, float)):
        return v + 1
    m = re.search(r"[0-9]", v) if isinstance(v, str) else None
    return v[:m.start()] + str((int(m.group()) + 1) % 10) + v[m.end():] if m else None


if "--tu-kiem" in sys.argv:
    # H1 — `measured` chi duoc dung cho loi khai ma DOI DI THI BO KIEM DO. Moi la fact-bearing trong nut measured bi doi (so/SHA
    # +1) trong BAN SAO, chay lai bo kiem; la nao doi di ma van `TONG: DAT` thi nhan measured o do la lời khai, khong phai phep do.
    import os, shutil, tempfile
    if "--repo" not in sys.argv:
        sys.exit("TU-KIEM can --repo <kho day du> (thieu thi chot git khong do duoc, la nao cung song sot gia)")
    song_sot, tong = [], 0
    for p, v in _la_measured(h):
        m = _doi_so(v)
        if m is None:
            continue
        tong += 1
        o = yaml.safe_load(HO_SO.read_text(encoding="utf-8"))
        x = o
        for k in p[:-1]:
            x = x[k]
        x[p[-1]] = m
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / "ops" / "land"
            d.mkdir(parents=True)
            shutil.copytree(P, d / P.name)
            (d / HO_SO.name).write_text(yaml.safe_dump(o, allow_unicode=True, sort_keys=False, width=100000), encoding="utf-8")
            r = subprocess.run([sys.executable, "-I", str(d / P.name / Path(__file__).name), "--repo", sys.argv[sys.argv.index("--repo") + 1]],
                               capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        if r.returncode == 0:
            song_sot.append(".".join(map(str, p)))
    for p in song_sot:
        print("LOT  " + p)
    print(f"TU-KIEM: {tong} la measured, {len(song_sot)} song sot" + (" (doi di ma van TONG: DAT) => day la loi khai, khong phai phep do" if song_sot else " - moi la doi di deu lam bo kiem DO"))
    sys.exit(1 if song_sot else 0)


def doc(ten, nhi_phan=False):
    """Moi lan doc NGU NGHIA mot hien vat di qua day; muc 11 doi MOI hien vat phai qua it nhat mot lan."""
    DA_DOC.add(str(ten))
    return (P / ten).read_bytes() if nhi_phan else (P / ten).read_text(encoding="utf-8")

# 1. SHA256SUMS: PHU DU — tap ten trong manifest == tap tep trong thu muc (tru dung SHA256SUMS.txt), moi tep DUNG MOT
#    dong, ten tuong doi an toan (khong '/', khong '..'); roi moi dong khop tep. Chi kiem cac dong CON LAI trong
#    manifest thi xoa mot dong la mat chot ma van DAT (Codex PR #723, comment 4232301600).
dong_mf = [d for d in doc("SHA256SUMS.txt").splitlines() if d.strip()]
mf = []
for dong in dong_mf:
    dg, ten = dong.split(None, 1)
    mf.append((dg, ten.lstrip("*")))
ten_mf = [t for _, t in mf]
tep_that = sorted(x.name for x in P.iterdir() if x.name != "SHA256SUMS.txt")
chot(all("/" not in t and "\\" not in t and t not in ("", ".", "..") for t in ten_mf), "manifest: moi ten la ten tep tuong doi an toan")
chot(len(ten_mf) == len(set(ten_mf)), "manifest: khong ten nao lap")
chot(sorted(set(ten_mf)) == tep_that,
     f"manifest phu du: thieu {sorted(set(tep_that) - set(ten_mf))} thua {sorted(set(ten_mf) - set(tep_that))}")
for dg, ten in mf:
    f = P / ten
    chot(f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest() == dg, f"sha256 {ten}")

# 2. Moi cong `measured` do lai -> co khoi LENH, dau duong, RC dung trong hien vat.
cong = h["ung_vien"]["cong_tai_cho_tren_ung_vien"]["do_lai_luc_ghi_so"]
van = doc(cong["hien_vat"].split()[0])
# `[^\n]*` cho dong lenh: voi re.S, `.*` se nuot qua nhieu khoi.
# Neo checkout (Codex PR #723, comment 4232647532): dong DAU va dong CUOI cua hien vat la rev-parse + status cua CHINH
# clone da chay 5 lenh; ca hai phai la HEAD == authorized_head_sha, TREE == tree merge, SACH=co.
dau = re.match(r"### CHECKOUT: HEAD=([0-9a-f]{40}) TREE=([0-9a-f]{40}) SACH=(\w+) ", van)
cuoi = re.search(r"^### CHECKOUT-SAU: HEAD=([0-9a-f]{40}) TREE=([0-9a-f]{40}) SACH=(\w+)\n?\Z", van, re.M)
chot(bool(dau and cuoi) and dau.groups() == cuoi.groups() == (h["authorized_head_sha"], h["thao_tac_merge"]["tree"], "co"),
     f"cong do lai: checkout truoc/sau == ung vien sach ({dau and dau.groups()}, {cuoi and cuoi.groups()})")
luc_do = re.match(r"### CHECKOUT: [^\n]* LUC=(\S+)\n", van)
chot(bool(luc_do) and luc_do.group(1)[11:16] in cong["pham_vi"], f"cong do lai: gio LUC cua hien vat ({luc_do and luc_do.group(1)}) co trong pham_vi")
bo = re.findall(r"^### LENH: ([^\n]*)\n(.*?)^### RC=(\d+)$", van, re.S | re.M)
khoi = {l: o for l, o, _ in bo}
rcs = {l: rc for l, _, rc in bo}
for r in cong["ket_qua"]:
    l = r["lenh"]
    chot(l in khoi and r["dau_duong"] in khoi[l] and rcs.get(l) == str(r["rc"]),
         f"cong `{l}`: co khoi, dau duong, RC={r['rc']}")

# 3. Thoi diem ref fence: truoc < merged_at < sau.
td = doc("thoi-diem-ls-remote.txt")
truoc = re.search(r"^truoc .*mtime (\S+)", td, re.M).group(1)
sau = re.search(r"^sau .*birth (\S+)", td, re.M).group(1)
merged = json.loads(doc("pr-621.json"))["merged_at"]
chot(ts(truoc) < ts(merged) < ts(sau), f"truoc {truoc} < merge {merged} < sau {sau}")
for ten, nhan in (("ls-remote-truoc-merge.sorted.txt", "truoc"), ("ls-remote-sau-merge.sorted.txt", "sau")):
    dg = re.search(rf"^{nhan} .*sha256sum (\w+)", td, re.M).group(1)
    chot(hashlib.sha256(doc(ten, nhi_phan=True)).hexdigest() == dg, f"anh {nhan} khop digest trong thoi-diem")

# 3a. Ma thoat CUA HAI LENH ls-remote (Codex PR #723, comment 4232431541): moi lenh dung mot dong
#     `git ls-remote origin (<truoc|sau> merge, ...) rc=<n>`, n phai = 0; dong `ca hai: LC_ALL=C sort...` khong la lenh.
rc_ls = re.findall(r"^git ls-remote origin \((truoc|sau) merge,[^\n]*\) rc=(\d+)$",
                   doc("ls-remote-rc.txt"), re.M)
for nhan in ("truoc", "sau"):
    v = [rc for n, rc in rc_ls if n == nhan]
    chot(v == ["0"], f"ls-remote {nhan} merge: dung mot dong, rc=0 (doc duoc {v})")

# 3b. Ref delta: AP that delta khai trong refs-delta.txt vao anh truoc, so KHOP TUNG ref/OID voi anh sau (Codex PR
#     #723, comment 4232301580). ABSENT = ref khong co o phia do; ten ref lap trong anh hay trong delta => TRUOT.
def anh(ten):
    d, lap = {}, []
    for dong in doc(ten).splitlines():
        oid, ref = dong.split("\t")
        if ref in d:
            lap.append(ref)
        d[ref] = oid
    return d, lap


a_truoc, lap_t = anh("ls-remote-truoc-merge.sorted.txt")
a_sau, lap_s = anh("ls-remote-sau-merge.sorted.txt")
chot(not lap_t and not lap_s, f"anh ref khong co ten lap (truoc {lap_t}, sau {lap_s})")
delta, lap_d, cu_sai = {}, [], []
for dong in doc("refs-delta.txt").splitlines():
    cot = dong.split("\t")
    if dong.startswith("#") or len(cot) != 3 or cot[0] in ("truoc", "sau"):
        continue
    ref, cu, moi = cot
    if ref in delta:
        lap_d.append(ref)
    delta[ref] = (cu, moi)
    if a_truoc.get(ref, "ABSENT") != cu:
        cu_sai.append(ref)
dem = dict(re.findall(r"^(truoc|sau)\t(\d+)\t", doc("refs-delta.txt"), re.M))
chot(dem == {"truoc": str(len(a_truoc)), "sau": str(len(a_sau))}, f"so ref khai {dem} == dem tren anh ({len(a_truoc)}, {len(a_sau)})")
chot(bool(delta) and not lap_d, f"delta: co dong, khong ref lap ({lap_d})")
chot(not cu_sai, f"delta: gia tri CU khop anh truoc ({cu_sai})")
ap = dict(a_truoc)
for ref, (cu, moi) in delta.items():
    if moi == "ABSENT":
        ap.pop(ref, None)
    else:
        ap[ref] = moi
chot(ap == a_sau, f"ap delta vao anh truoc ({len(a_truoc)} ref) == anh sau ({len(a_sau)} ref); lech "
     f"{sorted(set(ap.items()) ^ set(a_sau.items()))[:4]}")
rf = h["ref_fence"]
chot(all(ref in rf["delta"] and cu[:7] in rf["delta"] and (moi[:7] if moi != "ABSENT" else moi) in rf["delta"] for ref, (cu, moi) in delta.items())
     and set(re.findall(r"refs/[\w/]+", rf["delta"])) == {r for r in delta if r.startswith("refs/")} and f"({len(a_truoc)} ref)" in rf["kiem_doc_lap"] and f"({len(a_sau)} ref)" in rf["kiem_doc_lap"],
     "ref_fence.delta + kiem_doc_lap (van xuoi) khop refs-delta.txt va so ref hai anh")
tk = re.findall(r"\d\d:\d\d:\d\d(?:\.\d+)?Z", "\n".join(l for l in td.splitlines() if l.split()[:1] in (["truoc"], ["merge"], ["sau"])))
chot(len(tk) == 5 and all(x in rf["thoi_diem"]["ket_qua"] for x in tk), f"ref_fence.thoi_diem.ket_qua nhac dung 5 moc gio cua thoi-diem-ls-remote.txt ({tk})")

# 4. Moi run CI: moc REST khop run-<id>.json; run khong skipped phai nam trong pham_vi_run cua CA BA muc khong_do_duoc.
pham_vi = {k["id"]: set(k.get("pham_vi_run", [])) for k in h["khong_do_duoc"]}
can = ("MOC-WORKFLOW-DEFINITION", "RC-SO-CHI-CO-STEP-CONCLUSION", "CHECKOUT-IDENTITY")
khong_skip = set()
for r in [x for x in h["pre_merge_checks"] + h["post_merge_checks"] if "run_id" in x]:
    j = json.loads(doc(f"run-{r['run_id']}.json"))
    chot(j["id"] == r["run_id"] and j["html_url"] == f"https://github.com/ducthangho/tra-luat/actions/runs/{r['run_id']}",
         f"run {r['run_id']}: id + html_url cua chinh readback khop run_id")
    chot(j["event"] == r["event"] and j["run_attempt"] == r["run_attempt"] and j["head_sha"] == r["head_sha"]
         and r["workflow"].split(" (")[0] == j["path"] and j["head_commit"]["id"] == r["head_sha"]
         and j["repository"]["full_name"] == "ducthangho/tra-luat", f"run {r['run_id']}: event/attempt/head/path/head_commit/repo khop REST (path BANG, khong tien to)")
    # status + conclusion cua CHINH workflow run (Codex PR #723, comment 4232431526); skipped giu rieng.
    kl_khai = re.search(r"— \d* ?(success|skipped)", r["check_runs"]).group(1)
    chot(j["status"] == "completed" and j["conclusion"] == kl_khai,
         f"run {r['run_id']}: status/conclusion REST {j['status']}/{j['conclusion']} == completed/{kl_khai}")
    if j["conclusion"] != "skipped":
        khong_skip.add(r["run_id"])
# Pham vi mien tru phai BANG DUNG tap run khong skipped — khong nhan tap cha (Codex PR #723, comment 4232647602).
for c in can:
    chot(pham_vi[c] == khong_skip, f"pham_vi_run {c} == dung tap run khong skipped {sorted(khong_skip)}")
# Thoi diem hoan tat run hau merge (Codex PR #723, comment 4232647556).
rj = json.loads(doc(f"run-{h['gate_hau_merge']['run']}.json"))
chot(rj["updated_at"] == h["gate_hau_merge"]["hoan_tat"] and h["gate_hau_merge"]["hoan_tat"] in h["gate_hau_merge"]["ket_qua"],
     f"gate hau merge: hoan_tat khai == updated_at REST ({rj['updated_at']})")
# 4b. TUNG check run, khong chi total_count (Codex PR #723, comment 4232301588): moi object phai completed, head dung,
#     va dem theo (run_id, conclusion) phai khop dong `check_runs` khai cho run do; tong theo conclusion phai khop
#     tom tat khai (skipped dem RIENG, khong gop vao success).
def cr(f):
    d = json.loads(doc(f))
    chot(d["total_count"] == len(d["check_runs"]), f"{f}: total_count == so object ({len(d['check_runs'])})")
    for c in d["check_runs"]:
        # Danh tinh job Actions (Codex PR #723, comment 4232647485): app github-actions + URL Actions chinh tac cua https://github.com/ducthangho/tra-luat
        # nay, job id trong URL == id cua check run. Khong khop thi https://github.com/ducthangho/tra-luatNG trich run id tu URL.
        m_url = re.fullmatch(r"https://github.com/ducthangho/tra-luat/actions/runs/(\d+)/job/(\d+)", c["details_url"] or "")
        chot(c["app"]["slug"] == "github-actions" and m_url is not None and int(m_url.group(2)) == c["id"]
             and c["html_url"] == c["details_url"], f"{f}: check {c['id']} la job Actions cua kho (app + URL chinh tac)")
    return [(int(re.search(r"/runs/(\d+)/", c["details_url"]).group(1)), c["status"], c["conclusion"], c["head_sha"],
             re.sub(r" \(ubuntu-latest(, \d+)?\)$", "", c["name"])) for c in d["check_runs"]]


def dem(ds):
    out = {}
    for _, _, kl, _, _ in ds:
        out[kl] = out.get(kl, 0) + 1
    return out


bang = {"658bd0c": cr("checkruns-658bd0c.json"), "3fc0932": cr("checkruns-3fc0932.json")}
for r in [x for x in h["pre_merge_checks"] + h["post_merge_checks"] if "run_id" in x]:
    ds = [c for c in bang[r["head_sha"][:7]] if c[0] == r["run_id"]]
    m = re.match(r"(\d+) .*— \d* ?(success|skipped)", r["check_runs"])
    # Ten check: so MULTISET ten (chi bo hau to ma tran `(ubuntu-latest[, N])`) voi `ten_check` khai (Codex PR #723,
    # comment 4232431534) — thay mot cong bang ten la phai DO.
    chot(sorted(c[4] for c in ds) == sorted(r["ten_check"]), f"run {r['run_id']}: multiset ten check == ten_check khai")
    chot(m is not None and len(ds) == int(m.group(1)) and all(st == "completed" and kl == m.group(2) and hd == r["head_sha"]
                                                              for _, st, kl, hd, _ in ds),
         f"run {r['run_id']}: {len(ds)} check run, tat ca completed/{m and m.group(2)}/head dung == khai `{r['check_runs'][:24]}...`")
tong_pre = next(x["tong"] for x in h["pre_merge_checks"] if "tong" in x)
m = re.search(r"= (\d+) check run = (\d+) success \+ (\d+) skipped", tong_pre)
chot(m is not None and dem(bang["658bd0c"]) == {"success": int(m.group(2)), "skipped": int(m.group(3))}
     and len(bang["658bd0c"]) == int(m.group(1)), f"658bd0c: {dem(bang['658bd0c'])} == tom tat khai")
m = re.search(r"(\d+) check run, (\d+) success", h["post_merge_checks"][0]["ket_qua"])
chot(m is not None and dem(bang["3fc0932"]) == {"success": int(m.group(2))} and len(bang["3fc0932"]) == int(m.group(1)),
     f"3fc0932: {dem(bang['3fc0932'])} == tom tat khai")
# 4d. (H1b) Ban van xuoi cua cac con so trong YAML phai khop dem tren hien vat (khong chi mot ban sao trong cung YAML).
mm = re.search(r"measured — (\d+) \+ (\d+) \+ (\d+) \+ (\d+) = (\d+) check run", tong_pre)
tung_run = [len([c for c in bang["658bd0c"] if c[0] == x["run_id"]]) for x in h["pre_merge_checks"] if "run_id" in x]
chot(mm is not None and [int(x) for x in mm.groups()[:4]] == tung_run and sum(tung_run) == int(mm.group(5)), f"pre_merge tong: cac so hang khop so check run tung run {tung_run}")
n6 = dem(bang["658bd0c"])
kq6 = h["ung_vien"]["ci_pr_tren_ung_vien"]["ket_qua"]
chot(kq6.startswith(f"{len(bang['658bd0c'])} check run = {n6['success']} success") and f"+ {n6['skipped']} skipped" in kq6, "ci_pr_tren_ung_vien.ket_qua khop dem tren checkruns-658bd0c.json")
n3 = len(bang["3fc0932"])
chot(f"{n3}/{n3} check run success" in h["gate_hau_merge"]["ket_qua"] and f"run-{h['post_merge_checks'][0]['run_id']}.json" in h["post_merge_checks"][0]["ket_qua"],
     "hau merge: gate_hau_merge.ket_qua + post_merge_checks[0].ket_qua khop dem va run_id")
ids = {int(re.search(r"/runs/(\d+)/", c["details_url"]).group(1))
       for c in json.loads(doc("checkruns-658bd0c.json"))["check_runs"]}
khai = {x["run_id"] for x in h["pre_merge_checks"] if "run_id" in x}
chot(ids == khai, f"run truoc merge: checkruns {sorted(ids)} == khai {sorted(khai)}")
# 4c. Thu tu thoi gian cua quyet dinh land (truoc day chi do "Codex xong SAU merge", muc 8): CI truoc merge phai xong <= merged_at,
#     run hau merge phai duoc tao >= merged_at.
pre_xong = [c["completed_at"] for c in json.loads(doc("checkruns-658bd0c.json"))["check_runs"]]
chot(bool(pre_xong) and all(ts(x) <= ts(merged) for x in pre_xong), f"thu tu: {len(pre_xong)} check run truoc merge deu hoan tat <= merged_at {merged}")
chot(ts(json.loads(doc(f"run-{h['gate_hau_merge']['run']}.json"))["created_at"]) >= ts(merged), "thu tu: run hau merge duoc tao >= merged_at")

# 6. Uy quyen ben (Codex PR #723, comment 4232431549): doc NGU NGHIA comment uy quyen, so voi khoa chuan.
#    So DONG DAU nguyen van va DONG uy quyen nguyen van — khong substring long (tranh khop chu trich dan / phu dinh).
au = json.loads(doc("comment-6082660033.json"))
sha = h["authorized_head_sha"]
# H7 — khoa chuan §7 co mat, nhan khong bi nang cap (T01/T02/T06/T07 chi sua DU LIEU; khong chot nao canh viec tai tao loi cu)
KHOA_CHUAN = ("schema_version", "mission_id", "generation", "provider", "role", "model_family", "execution_surface", "transport", "session_id",
              "input_packet_generations", "authorized_head_sha", "approver", "authorization_url", "land_operator", "merge_method", "merge_commit",
              "pre_merge_checks", "post_merge_checks", "bookkeeping")
chot(all(k in h for k in KHOA_CHUAN) and h["schema_version"] == 1 and isinstance(h["generation"], int), f"schema S7: du khoa chuan (thieu {[k for k in KHOA_CHUAN if k not in h]})")
ra0 = h["review_ai_truoc_drift"]
chot(ra0["reviewed_sha"] != sha and str(ra0["trang_thai"]).startswith("stale"), "review AI truoc drift: reviewed_sha != head da merge, nhan stale")
pm = h["post_merge_checks"][0]
chot(all(str(pm[k]).startswith("not_measured") for k in ("moc_checkout", "moc_workflow_definition", "rc")) and str(h["gate_hau_merge"]["moc_checkout"]).startswith("not_measured"),
     "hau merge: checkout/workflow_definition/rc con nhan not_measured (khong bi nang cap thanh measured)")
chot(au["html_url"] == h["authorization_url"] == h["uy_quyen"]["neo_ben"]
     and h["authorization_url"].endswith(f"#issuecomment-{au['id']}"), "uy quyen: id/url comment == authorization_url")
chot(au["issue_url"].endswith(f"/repos/ducthangho/tra-luat/issues/{h['pr']}")
     and h["review_tai_head_da_merge"]["human_audit"]["reviewed_sha"] == sha
     and h["review_tai_head_da_merge"]["human_audit"]["url"] == h["authorization_url"],
     "uy quyen: comment thuoc PR nay; human_audit.reviewed_sha + url == ban uy quyen (Codex 4232647613)")
chot(au["user"]["login"] == h["approver"] and au["author_association"] == "OWNER" and au["performed_via_github_app"] is None,
     f"uy quyen: tac gia {au['user']['login']}/{au['author_association']} == approver OWNER, khong qua app")
chot(au["created_at"] == au["updated_at"] == h["uy_quyen"]["luc"], "uy quyen: created_at == updated_at == luc khai (chua sua)")
chot(ts(au["created_at"]) < ts(merged), "uy quyen: created_at TRUOC merged_at (uy quyen phai co truoc thao tac)")
chot(h["ung_vien"]["head_sha"] == sha and sha in h["uy_quyen"]["noi_dung"], "ung_vien.head_sha == authorized_head_sha, uy_quyen.noi_dung nhac dung SHA")
dong_au = au["body"].split("\n")
chot(dong_au[0] == f"Human audit — approve #{h['pr']} tại head {sha}", "uy quyen: dong dau dung nguyen van, SHA day du")
chot(h["merge_method"] == "merge" and dong_au.count(
    f"- Uỷ quyền: merge đúng SHA {sha[:7]} bằng merge commit (không squash), rồi chạy hậu-merge gate và bookkeeping. "
    "Head đổi thêm thì uỷ quyền này hết hiệu lực.") == 1, "uy quyen: dong uy quyen merge commit dung nguyen van, mot lan")
b_au = au["body"].encode("utf-8")
khai_au = h["review_tai_head_da_merge"]["human_audit"]["do_duoc"]
chot(f"than {len(b_au)} byte" in khai_au and hashlib.sha256(b_au).hexdigest() in khai_au,
     "human_audit: so byte + sha256 than khai == do tren readback")
chot(f"comment-{au['id']}.json" in khai_au and f"comments/{au['id']}" in khai_au and au["created_at"] in khai_au and f"LF x{au['body'].count(chr(10))}" in khai_au
     and ("khong LF cuoi" in khai_au) == (not au["body"].endswith("\n")) and f'{au["body"].count("&#")} "&#"' in khai_au
     and au["body"].count(sha) == 1 and "xuat hien 1 lan" in khai_au, "human_audit.do_duoc: id/gio/LF/&#/SHA khop readback")

# 7. Cau truc merge (Codex PR #723, comment 4232431560): commit readback, pr readback, khoa YAML; --repo thi git.
cm = json.loads(doc("commit-3fc0932.json"))
pr = json.loads(doc("pr-621.json"))
tm = h["thao_tac_merge"]
cha = [x["sha"] for x in cm["parents"]]
chot(cm["sha"] == h["merge_commit"] == tm["merge_commit"] == pr["merge_commit_sha"], "merge: sha commit == khoa YAML == pr")
chot(cha == tm["cha"] and cha[1] == sha == pr["head"]["sha"] == tm["expected_head_sha"],
     f"merge: cha THEO THU TU {cha} == khai; cha thu hai == authorized_head_sha == pr head")
chot(cm["commit"]["tree"]["sha"] == tm["tree"], "merge: tree readback == khai")
mg7, c0, c1, ds_ = h["merge_commit"][:7], tm["cha"][0][:7], tm["cha"][1][:7], tm["kiem_tra"]["diff_stat"]
chot(tm["kiem_tra"]["ket_qua"] == (f"git show -s --format='%H %P %T' {mg7} => cha [{c0}, {c1}]; tree({mg7}) == tree({c1}); "
                                  f"git diff --stat {c0} {mg7} => {ds_['tep']} tep, +{ds_['them']}")
     and h["trang_thai_packet"]["merged_nguon"] == f"measured — pr-{h['pr']}.json: merged true, merge_commit_sha {h['merge_commit']}",
     "merge: kiem_tra.ket_qua va merged_nguon BANG van xuoi dung tu cac khoa chuan")
chot(pr["base"]["sha"] == cha[0], f"merge: pr.base.sha {pr['base']['sha']} == cha thu nhat (nhanh dich)")
chot(h["gate_hau_merge"]["head_sha"] == h["merge_commit"] and h["gate_hau_merge"]["run"] == h["post_merge_checks"][0]["run_id"],
     "gate hau merge: head_sha == merge_commit, run == post_merge_checks[0].run_id")
chot(pr["merged_by"]["login"] == h["approver"] and f"merged_by trong pr-621.json la tai khoan {pr['merged_by']['login']}"
     in h["land_operator"], f"pr: merged_by {pr['merged_by']['login']} == tac nhan khai trong land_operator (Codex 4232647519)")
chot(pr["merged"] is True and pr["html_url"] == f"https://github.com/ducthangho/tra-luat/pull/{h['pr']}" and pr["number"] == h["pr"] and pr["base"]["ref"] == "master", "pr: merged, dung so, base master")
tp = h["trang_thai_packet"]
chot(tp["merged"] is pr["merged"] and isinstance(tp["landed"], bool), "trang_thai_packet: merged == pr-621.json, landed la bool")
qd = h.get("quyet_dinh_chu_kho") or {}
chot(tp["landed"] is False or bool(qd.get("neo_ben") and all(set(qd.get("pham_vi_run", [])) == pham_vi[c] for c in can)),
     "landed: true chi khi co quyet_dinh_chu_kho.neo_ben + pham_vi_run == pham_vi khong_do_duoc (tien le #719 -> #720)")

# 8. Review connector sach (Codex PR #723, comment 4232431571): actor, commit, trang thai cuoi, luc; hai danh sach rong.
cx = json.loads(doc("comment-6082682461-codex.json"))
md = h["review_tai_head_da_merge"]["codex_connector"]["may_doc"]
hang = re.findall(r"^\| 📝 \*\*Code Review\*\* \| \S+ \*\*(\w+)\*\* <relative-time datetime=\"([^\"]+)\">[^|]*\| `([0-9a-f]+)` \| ([^|]+?) \|$",
                  cx["body"], re.M)
chot(cx["user"]["login"] == md["tac_gia"] and cx["user"]["type"] == "Bot", "connector: tac gia la bot connector")
chot(cx["html_url"] == f"https://github.com/ducthangho/tra-luat/pull/{h['pr']}#issuecomment-{cx['id']}" and cx["id"] == 6082682461
     and cx["issue_url"].endswith(f"/repos/ducthangho/tra-luat/issues/{h['pr']}")
     and (cx.get("performed_via_github_app") or {}).get("slug") == "chatgpt-codex-connector",
     "connector: dung comment 6082682461 cua PR nay, qua app chatgpt-codex-connector (Codex 4232647572)")
chot(hang == [(md["trang_thai"], md["luc"], md["commit"], md["trigger"])] and md["trang_thai"] == "Completed"
     and sha.startswith(md["commit"]), f"connector: DUNG MOT hang review, Completed, dung commit ung vien ({hang})")
chot(json.loads(doc("reviews-621.json")) == []
     and json.loads(doc("review-comments-621.json")) == [], "connector: 0 review, 0 review comment")
chot(ts(merged) < ts(md["luc"]), "connector: thu tu khai (merge TRUOC khi Codex xong) dung theo readback")
kq_cx = h["review_tai_head_da_merge"]["codex_connector"]
chot(str(cx["id"]) in kq_cx["ket_qua"] and md["commit"] in kq_cx["ket_qua"] and md["luc"][:19] in kq_cx["ket_qua"] and md["trigger"] in kq_cx["ket_qua"]
     and merged[11:19] in kq_cx["thu_tu_thoi_gian"] and md["luc"][11:19] in kq_cx["thu_tu_thoi_gian"], "connector: ket_qua + thu_tu_thoi_gian (van xuoi) khop readback")

# 9. Review AI truoc drift (stale): readback la verdict approve tren reviewed_sha, TONG khop.
st = json.loads(doc("comment-5917112447.json"))
ra = h["review_ai_truoc_drift"]
chot(st["html_url"] == ra["neo"] and st["body"].split("\n")[0] ==
     f"## Cross-review lượt {ra['luot']} — PR #{h['pr']} @ {ra['reviewed_sha'][:7]} (commit cục bộ, chưa push theo chỉ đạo chủ kho) "
     f"— approve ({ra['tong']})", "review truoc drift: url + dong dau (luot, sha, approve, TONG) khop khai")

# 10. Bang ai-dang-giu: tap duong dan == write set THAT (tep ho so + moi tep provenance), moi dong rc=0 NGUOI_GIU 0.
ag_tho = doc("ai-dang-giu-write-set.txt")
ag = [d.split("\t") for d in ag_tho.splitlines() if not d.startswith("#")]
# Do phu ref (Codex 4232647509): hai TAP ten nhanh luu kem (ls-remote --heads / for-each-ref) phai BANG NHAU, khong
# trong, khong lap; dong dau bang khai dung so do. Khong co hai tap thi cac dong NGUOI_GIU 0 khong co gia tri.
mc_l = doc("nhanh-may-chu.txt").splitlines()
cb_l = doc("nhanh-cuc-bo.txt").splitlines()
chot(mc_l and len(set(mc_l)) == len(mc_l) and set(mc_l) == set(cb_l) and len(cb_l) == len(set(cb_l)),
     f"ai-dang-giu: tap nhanh may chu ({len(mc_l)}) == cuc bo ({len(cb_l)}), khong lap")
chot(f"# tap nhanh: may chu {len(mc_l)} cuc bo {len(cb_l)} thieu 0 thua 0" in ag_tho.splitlines(),
     "ai-dang-giu: dong khai do phu khop hai tap luu kem")
ws = {f"ops/land/{HO_SO.name}"} | {f"ops/land/{P.name}/{x.name}" for x in P.iterdir()}
chot(sorted(x[0] for x in ag) == sorted(ws), "ai-dang-giu: tap duong dan == write set that, khong lap")
chot(all(x[1] == "rc=0" and x[2].startswith("NGƯỜI_GIỮ 0") for x in ag), "ai-dang-giu: moi dong rc=0 NGUOI_GIU 0")
ls_ = h["lease_tren_duong_ghi_so"]
chot(f"{len(ag)}/{len(ag)} rc=0" in ls_["ket_qua"] and f"({len(ag)} duong dan" in ls_["lenh"] and f"{len(mc_l)}/{len(cb_l)}," in ls_["lenh"],
     "lease: so duong dan va so nhanh trong YAML khop hien vat")

# 6b. Tom tat operator (nguon cua cong_tai_cho.luot_goc_truoc_merge, nhan thuat_lai): dung comment, chu kho, dung head.
op = json.loads(doc("comment-6080596360.json"))
nguon_id = int(re.search(r"comment-(\d+)\.json", h["ung_vien"]["cong_tai_cho_tren_ung_vien"]["luot_goc_truoc_merge"]["nguon"]).group(1))
chot(op["id"] == nguon_id and op["html_url"] == f"https://github.com/ducthangho/tra-luat/pull/{h['pr']}#issuecomment-{nguon_id}"
     and op["issue_url"].endswith(f"/repos/ducthangho/tra-luat/issues/{h['pr']}")
     and (op.get("performed_via_github_app") or {}).get("slug") == "claude",
     "tom tat operator: id/url comment == ten hien vat, thuoc PR nay, qua app claude")
chot(op["user"]["login"] == h["approver"] and op["author_association"] == "OWNER"
     and op["body"].split("\n")[0] == f"## Land prepare — #{h['pr']} (head `{sha}`)",
     "tom tat operator: chu kho, dong dau neo dung head ung vien")
# Ket qua cong luot goc phai CO NGUYEN VAN trong dong "Cong tai cho" cua chinh comment nguon (Codex 4232647493).
dong_cong = [d for d in op["body"].split("\n") if d.startswith(f"**Cổng tại chỗ trên `{sha[:7]}`**")]
luot_goc = h["ung_vien"]["cong_tai_cho_tren_ung_vien"]["luot_goc_truoc_merge"]
chot(len(dong_cong) == 1 and len(luot_goc["trich_nguyen_van"]) == 5
     and all(m in dong_cong[0] for m in luot_goc["trich_nguyen_van"]),
     "tom tat operator: dung mot dong cong, chua nguyen van ca 5 ket qua thuat lai")

# 11. PHU NGU NGHIA: moi hien vat (tru SHA256SUMS.txt — da kiem o muc 1 — va chinh script nay) phai duoc DOC NOI DUNG
#     o mot muc tren, khong chi bam. Them hien vat ma quen viet chot thi muc nay DO (Codex PR #723 lượt 5: sau tep
#     chi bi bam ma khong bi doc).
can_doc = {x.name for x in P.iterdir()} - {"SHA256SUMS.txt", Path(__file__).name}
chot(DA_DOC >= can_doc, f"phu ngu nghia: hien vat chua co chot doc noi dung {sorted(can_doc - DA_DOC)}")

# 5. Digest diff PR (chi luu digest, khong luu diff tho): --repo thi tai lap bang OID ghim, va ref sau merge PHAI
#    cho digest khac. Thieu --repo => chot nay KHONG DO DUOC (in ra, khong tinh DAT).
DG = "e5bde9ba8623b16b34066da23b361db604b324f020cc43f4e3efdc9755ba872e"
if "--repo" not in sys.argv:
    print("KHONG DO DUOC digest diff PR: can --repo <clone day du>")
else:
    repo = sys.argv[sys.argv.index("--repo") + 1] if sys.argv.index("--repo") + 1 < len(sys.argv) else ""
    if not repo or not Path(repo).is_dir():
        raise SystemExit("TRUOT --repo rong hoac khong phai thu muc (git -C '' la khong lam gi: do kho cua thu muc hien tai)")
    if subprocess.run(["git", "-C", repo, "rev-parse", "--is-shallow-repository"], capture_output=True, text=True, env=_GIT_ENV).stdout.strip() != "false":
        raise SystemExit("TRUOT repo: nong hoac khong phai kho git (digest va dem commit tren kho nong la sai)")

    def d(a, b):
        out = subprocess.run(["git", "-C", repo, "-c", "core.abbrev=7", "diff", "--no-color", "--no-ext-diff", "--no-textconv", "--src-prefix=a/",
                              "--dst-prefix=b/", "-U3", "--diff-algorithm=myers", "--indent-heuristic", "-M", a, b],
                             capture_output=True, check=True, env=_GIT_ENV).stdout
        return hashlib.sha256(out).hexdigest()

    chot(d("6980e5bf04e4e5b8b75e5817578f1aba13f2f5ab", "675895db34e9a7c1357f8d8ad8925bf8f01ad21c") == DG, "diff truoc drift (OID ghim)")
    chot(d("8b59185975a938504de5963d2310e574dd4858b2", "658bd0cdc56bbd3445f489dcfc571e22eee7d675") == DG, "diff ung vien (OID ghim)")
    chot(d("3fc0932a3d1617c4352e5a7982f2e6e4208ca3f7", "658bd0cdc56bbd3445f489dcfc571e22eee7d675") != DG, "ref SAU merge cho digest KHAC")

    def d40(a, b):
        return hashlib.sha256(subprocess.run(["git", "-C", repo, "-c", "core.abbrev=40", "diff", a, b], capture_output=True, check=True, env=_GIT_ENV).stdout).hexdigest()

    hd = h["ung_vien"]["head_drift"]
    dg40, rong = d40("6980e5bf04e4e5b8b75e5817578f1aba13f2f5ab", "675895db34e9a7c1357f8d8ad8925bf8f01ad21c"), hashlib.sha256(b"").hexdigest()
    chot(DG in hd["lenh"] and dg40 == d40("8b59185975a938504de5963d2310e574dd4858b2", "658bd0cdc56bbd3445f489dcfc571e22eee7d675") and dg40 in hd["phan_chung"] and "core.abbrev=40" in hd["phan_chung"]
         and d("3fc0932a3d1617c4352e5a7982f2e6e4208ca3f7", "658bd0cdc56bbd3445f489dcfc571e22eee7d675") == rong and rong in hd["phan_chung"],
         "head_drift: digest abbrev=7 trong lenh, abbrev=40 va diff rong trong phan_chung khop do lai")

    def rp(x):
        return subprocess.run(["git", "-C", repo, "rev-parse", x], capture_output=True, text=True, check=True, env=_GIT_ENV).stdout.strip()

    mg = h["merge_commit"]
    chot([rp(f"{mg}^{{commit}}"), rp(f"{mg}^1"), rp(f"{mg}^2"), rp(f"{mg}^{{tree}}")] == [mg, *tm["cha"], tm["tree"]],
         "merge (git): commit, cha ^1 ^2 THEO THU TU, tree == khai")
    chot(rp(f"{sha}^{{tree}}") == tm["tree"], "merge (git): tree(ung vien) == tree(merge)")

    def g(*a):
        return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True, env=_GIT_ENV).stdout.strip()

    # So dem drift (Codex 4232647592): tinh lai tren clone day du, so voi so khai VA voi chu trong lenh khai.
    dc = h["ung_vien"]["head_drift"]["dem_commit"]
    chot(g("rev-parse", "--is-shallow-repository") == "false", "repo: KHONG nong (dem commit tren kho nong la sai)")
    so = {"base_den_master": int(g("rev-list", "--count", "6980e5bf04e4e5b8b75e5817578f1aba13f2f5ab..8b59185975a938504de5963d2310e574dd4858b2"))}
    so["rieng_nhanh"], so["rieng_master"] = map(int, g("rev-list", "--left-right", "--count",
                                                        "675895db34e9a7c1357f8d8ad8925bf8f01ad21c...8b59185975a938504de5963d2310e574dd4858b2").split())
    chot(so == dc["so"] and f"=> {so['base_den_master']};" in dc["lenh"] and f"=> {so['rieng_nhanh']} {so['rieng_master']}." in dc["lenh"]
         and f"di truoc {so['base_den_master']} commit" in h["ung_vien"]["head_drift"]["mo_ta"], f"drift (git): {so} == khai")
    # diff --stat merge (Codex 4232647622)
    ns = g("diff", "--shortstat", tm["cha"][0], h["merge_commit"])
    m_ns = re.fullmatch(r"(\d+) files? changed(?:, (\d+) insertions?\(\+\))?(?:, (\d+) deletions?\(-\))?", ns)
    ds = {"tep": int(m_ns.group(1)), "them": int(m_ns.group(2) or 0), "xoa": int(m_ns.group(3) or 0)} if m_ns else None
    chot(ds == tm["kiem_tra"]["diff_stat"] and f"=> {ds['tep']} tep, +{ds['them']}" in tm["kiem_tra"]["ket_qua"],
         f"merge (git): diff --shortstat {ns!r} == khai")

if LOI:
    print(f"TONG: TRUOT {len(LOI)}")
    sys.exit(1)
if "--repo" not in sys.argv:
    print("TONG: CHUA DU — moi chot doc tep dat, chot digest KHONG DO DUOC (thieu --repo)")
    sys.exit(2)
print("TONG: DAT")
sys.exit(0)
