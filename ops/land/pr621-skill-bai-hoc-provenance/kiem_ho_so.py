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


def chot(dk, msg):
    print(("DAT  " if dk else "TRUOT ") + msg)
    if not dk:
        LOI.append(msg)


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


h = yaml.safe_load(HO_SO.read_text(encoding="utf-8"))

# 1. SHA256SUMS: PHU DU — tap ten trong manifest == tap tep trong thu muc (tru dung SHA256SUMS.txt), moi tep DUNG MOT
#    dong, ten tuong doi an toan (khong '/', khong '..'); roi moi dong khop tep. Chi kiem cac dong CON LAI trong
#    manifest thi xoa mot dong la mat chot ma van DAT (Codex PR #723, comment 4232301600).
dong_mf = [d for d in (P / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines() if d.strip()]
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
van = (P / cong["hien_vat"].split()[0]).read_text(encoding="utf-8")
# `[^\n]*` cho dong lenh: voi re.S, `.*` se nuot qua nhieu khoi.
bo = re.findall(r"^### LENH: ([^\n]*)\n(.*?)^### RC=(\d+)$", van, re.S | re.M)
khoi = {l: o for l, o, _ in bo}
rcs = {l: rc for l, _, rc in bo}
for r in cong["ket_qua"]:
    l = r["lenh"]
    chot(l in khoi and r["dau_duong"] in khoi[l] and rcs.get(l) == str(r["rc"]),
         f"cong `{l}`: co khoi, dau duong, RC={r['rc']}")

# 3. Thoi diem ref fence: truoc < merged_at < sau.
td = (P / "thoi-diem-ls-remote.txt").read_text(encoding="utf-8")
truoc = re.search(r"^truoc .*mtime (\S+)", td, re.M).group(1)
sau = re.search(r"^sau .*birth (\S+)", td, re.M).group(1)
merged = json.loads((P / "pr-621.json").read_text(encoding="utf-8"))["merged_at"]
chot(ts(truoc) < ts(merged) < ts(sau), f"truoc {truoc} < merge {merged} < sau {sau}")
for ten, nhan in (("ls-remote-truoc-merge.sorted.txt", "truoc"), ("ls-remote-sau-merge.sorted.txt", "sau")):
    dg = re.search(rf"^{nhan} .*sha256sum (\w+)", td, re.M).group(1)
    chot(hashlib.sha256((P / ten).read_bytes()).hexdigest() == dg, f"anh {nhan} khop digest trong thoi-diem")

# 3b. Ref delta: AP that delta khai trong refs-delta.txt vao anh truoc, so KHOP TUNG ref/OID voi anh sau (Codex PR
#     #723, comment 4232301580). ABSENT = ref khong co o phia do; ten ref lap trong anh hay trong delta => TRUOT.
def anh(ten):
    d, lap = {}, []
    for dong in (P / ten).read_text(encoding="utf-8").splitlines():
        oid, ref = dong.split("\t")
        if ref in d:
            lap.append(ref)
        d[ref] = oid
    return d, lap


a_truoc, lap_t = anh("ls-remote-truoc-merge.sorted.txt")
a_sau, lap_s = anh("ls-remote-sau-merge.sorted.txt")
chot(not lap_t and not lap_s, f"anh ref khong co ten lap (truoc {lap_t}, sau {lap_s})")
delta, lap_d, cu_sai = {}, [], []
for dong in (P / "refs-delta.txt").read_text(encoding="utf-8").splitlines():
    cot = dong.split("\t")
    if dong.startswith("#") or len(cot) != 3 or cot[0] in ("truoc", "sau"):
        continue
    ref, cu, moi = cot
    if ref in delta:
        lap_d.append(ref)
    delta[ref] = (cu, moi)
    if a_truoc.get(ref, "ABSENT") != cu:
        cu_sai.append(ref)
dem = dict(re.findall(r"^(truoc|sau)\t(\d+)\t", (P / "refs-delta.txt").read_text(encoding="utf-8"), re.M))
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

# 4. Moi run CI: moc REST khop run-<id>.json; run khong skipped phai nam trong pham_vi_run cua CA BA muc khong_do_duoc.
pham_vi = {k["id"]: set(k.get("pham_vi_run", [])) for k in h["khong_do_duoc"]}
can = ("MOC-WORKFLOW-DEFINITION", "RC-SO-CHI-CO-STEP-CONCLUSION", "CHECKOUT-IDENTITY")
tong = 0
for r in [x for x in h["pre_merge_checks"] + h["post_merge_checks"] if "run_id" in x]:
    j = json.loads((P / f"run-{r['run_id']}.json").read_text(encoding="utf-8"))
    chot(j["event"] == r["event"] and j["run_attempt"] == r["run_attempt"] and j["head_sha"] == r["head_sha"]
         and r["workflow"].startswith(j["path"]), f"run {r['run_id']}: event/attempt/head/path khop REST")
    if j["conclusion"] != "skipped":
        chot(all(r["run_id"] in pham_vi[c] for c in can), f"run {r['run_id']}: nam trong pham_vi_run cua ca 3 muc")
for f, mong in (("checkruns-658bd0c.json", 17), ("checkruns-3fc0932.json", 14)):
    chot(json.loads((P / f).read_text(encoding="utf-8"))["total_count"] == mong, f"{f}: total_count {mong}")
ids = {int(re.search(r"/runs/(\d+)/", c["details_url"]).group(1))
       for c in json.loads((P / "checkruns-658bd0c.json").read_text(encoding="utf-8"))["check_runs"]}
khai = {x["run_id"] for x in h["pre_merge_checks"] if "run_id" in x}
chot(ids == khai, f"run truoc merge: checkruns {sorted(ids)} == khai {sorted(khai)}")

# 5. Digest diff PR (chi luu digest, khong luu diff tho): --repo thi tai lap bang OID ghim, va ref sau merge PHAI
#    cho digest khac. Thieu --repo => chot nay KHONG DO DUOC (in ra, khong tinh DAT).
DG = "e5bde9ba8623b16b34066da23b361db604b324f020cc43f4e3efdc9755ba872e"
if "--repo" not in sys.argv:
    print("KHONG DO DUOC digest diff PR: can --repo <clone day du>")
else:
    repo = sys.argv[sys.argv.index("--repo") + 1]

    def d(a, b):
        out = subprocess.run(["git", "-C", repo, "-c", "core.abbrev=7", "diff", a, b], capture_output=True, check=True).stdout
        return hashlib.sha256(out).hexdigest()

    chot(d("6980e5bf04e4e5b8b75e5817578f1aba13f2f5ab", "675895db34e9a7c1357f8d8ad8925bf8f01ad21c") == DG, "diff truoc drift (OID ghim)")
    chot(d("8b59185975a938504de5963d2310e574dd4858b2", "658bd0cdc56bbd3445f489dcfc571e22eee7d675") == DG, "diff ung vien (OID ghim)")
    chot(d("3fc0932a3d1617c4352e5a7982f2e6e4208ca3f7", "658bd0cdc56bbd3445f489dcfc571e22eee7d675") != DG, "ref SAU merge cho digest KHAC")

if LOI:
    print(f"TONG: TRUOT {len(LOI)}")
    sys.exit(1)
if "--repo" not in sys.argv:
    print("TONG: CHUA DU — moi chot doc tep dat, chot digest KHONG DO DUOC (thieu --repo)")
    sys.exit(2)
print("TONG: DAT")
sys.exit(0)
