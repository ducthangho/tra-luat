"""Kiem tinh nhat quan cua ho so land PR #621 voi hien vat trong thu muc provenance (Codex PR #723, review 5472526875).

Chay:  python -I kiem_ho_so.py [--repo <clone day du co 6980e5b, 675895d, 8b59185, 658bd0c, 3fc0932>] [--tu-kiem]
Thoat 0 = moi chot dat; 1 = co chot truot (in tung chot); 2 = khong truot nhung thieu --repo nen chot digest
KHONG DO DUOC (khong duoc doc thanh DAT). Chi doc tep; --repo thi goi them `git diff` (chi doc).
Che do `--tu-kiem --repo <kho>`: doi tung cum chu so cua tung la `measured` trong BAN SAO (thu muc tam) roi chay lai bo kiem. Thoat 0 =
ban sao KHONG dot bien DAT, so la thu == LA_MEASURED_DU_KIEN, va MOI dot bien bi mot chot ban `TONG: TRUOT`; 1 = nen khong DAT, hoac co
la song sot, hoac co dot bien chet vi LOI (traceback / --repo hong: khong phai chot nen KHONG tinh la "bi giet"; PROTOCOL §10.2.3).
KHONG la bang chung luot goc: no chi kiem rang moi loi khai `measured` trong ho so tro toi mot hien vat co that, co dau
duong, va cac moc thoi gian/run/digest khop nhau.
"""
import hashlib, json, os, re, subprocess, sys
from datetime import datetime
from pathlib import Path

import yaml

# L3 — console khong ma hoa duoc "—" / "·" (cp437/cp1252 qua ong; `python -I` vo hieu PYTHONUTF8/PYTHONIOENCODING nen nguoi dung khong tu chua duoc):
# print() nem UnicodeEncodeError GIUA chung, rc=1 truoc dong TONG (do 10-10-2026, PYTHONIOENCODING=ascii:strict, kho 1191865..d1dec7f). Ep UTF-8 TRUOC khi in.
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

P = Path(__file__).resolve().parent
HO_SO = P.parent / "pr621-skill-bai-hoc-land-evidence.yaml"
LOI = []
# H5 — moi lenh git cua bo kiem chay trong moi truong BIET TRUOC: bo GIT_* (GIT_DIR/GIT_WORK_TREE lam `-C` vo hieu: do 09-10-2026,
# GIT_DIR=<kho day du> + `--repo <kho nong>` van ra DAT), khong doc cau hinh toan cuc/he thong (diff.noprefix hoac diff.algorithm
# doi digest => TRUOT gia), khong ap `git replace`. GIOI HAN (do 10-10-2026, cross-review luot 4; deu TRUOT/crash gia, khong DAT gia): cau hinh CUC BO cua kho
# (`.git/config`, `.git/info/attributes`, `.git/info/grafts`) va tep thuoc tinh toan cuc (`$HOME/.config/git/attributes`, `$XDG_CONFIG_HOME/git/attributes`) VAN
# duoc doc: `diff.suppressBlankEmpty=true` -> TRUOT 3, `* -diff` -> TRUOT 4, `diff.orderFile` hong -> crash. Chay tren clone sach.
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


# Khoa tuong thuat/tro-toi: khong phai loi khai co the doi gia tri (lenh = cach tai lap, readback = ten tep, ...). CHU Y: ca khoa nay, la khong chu so,
# chuoi khong mo dau bang `measured` (landed_ly_do, khong_do_duoc[*].mo_ta...) va khoi khong gan nhan KHONG duoc --tu-kiem thu; su that mang quyet dinh land
# trong do chi co chot rieng o muc 4/6/7 (L3), con lai la van xuoi.
_TUONG_THUAT = {"dinh_chinh", "ghi_chu", "lenh", "mo_ta", "kiem_bang_may", "checkout", "pham_vi", "nguon", "readback", "vai_tro", "hien_vat"}


def _la_measured(o, p=(), trong=False):
    """H1 — moi la scalar nam trong nut `trang_thai: measured`, hoac chuoi mo dau bang `measured` (tru khoa tuong thuat)."""
    if isinstance(o, dict):
        trong = trong or re.search(r"(?<![_\w])measured\b", str(o.get("trang_thai", ""))) is not None
        for k, v in o.items():
            if k not in _TUONG_THUAT:
                yield from _la_measured(v, p + (k,), trong)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _la_measured(v, p + (i,), trong)
    elif (trong and not (isinstance(o, str) and o.startswith("not_measured"))) or (isinstance(o, str) and o.startswith("measured")):
        yield p, o


# So la `measured` MANG CHU SO ma --tu-kiem phai thu. Doi ten/ha cap/them nhan lam so nay doi => phai la quyet dinh co chu dich (cap nhat
# hang so nay trong cung commit), khong duoc troi am tham ra ngoai pham vi roi van in "0 song sot".
LA_MEASURED_DU_KIEN = 30


def _cum_so(v):
    """H1 — moi cach doi MOT cum chu so cua la: bool lat, int +1, chuoi: tung cum chu so lien tiep (khong chi cum dau) +1 o chu so cuoi."""
    if isinstance(v, bool):
        yield "bool", not v
    elif isinstance(v, (int, float)):
        yield "so", v + 1
    elif isinstance(v, str):
        for i, m in enumerate(re.finditer(r"[0-9]+", v)):
            yield f"cum{i}:{m.group()[:8]}", v[:m.end() - 1] + str((int(m.group()[-1]) + 1) % 10) + v[m.end():]


if "--tu-kiem" in sys.argv:
    # H1 — `measured` chi duoc dung cho loi khai ma DOI DI THI BO KIEM DO. Ba dieu kien de "bi giet" la that (PROTOCOL §10.2.3: receipt
    # DUONG + AM; mutant chet vi setup/import/permission KHONG chung minh tinh chat): (a) ban sao KHONG dot bien phai DAT; (b) mutant chi
    # tinh GIET khi bo kiem chay toi cuoi va in `TONG: TRUOT` (mot chot ban); chet vi traceback / --repo hong = CHET VI LOI, khong phai chot;
    # (c) so la thu duoc == LA_MEASURED_DU_KIEN. Gia tri sau --repo phai la thu muc that (khong bat dau bang `--`): neu khong, tien trinh con
    # nhan `--tu-kiem` lam doi so va de quy vo han.
    import copy, shutil, tempfile
    i_repo = sys.argv.index("--repo") if "--repo" in sys.argv else -1
    repo_tk = sys.argv[i_repo + 1] if 0 <= i_repo < len(sys.argv) - 1 else ""
    if not repo_tk or repo_tk.startswith("--") or not Path(repo_tk).is_dir():
        sys.exit("TRUOT TU-KIEM can --repo <kho day du> la thu muc that (thieu/rong/bat dau bang `--`: tien trinh con chet vi ly do khac se bi dem nham la 'bi giet')")

    def chay_con(o):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / "ops" / "land"
            d.mkdir(parents=True)
            shutil.copytree(P, d / P.name)
            (d / HO_SO.name).write_text(yaml.safe_dump(o, allow_unicode=True, sort_keys=False, width=100000), encoding="utf-8")
            return subprocess.run([sys.executable, "-I", str(d / P.name / Path(__file__).name), "--repo", repo_tk],
                                  capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})

    goc = yaml.safe_load(HO_SO.read_text(encoding="utf-8"))
    r0 = chay_con(goc)
    if r0.returncode != 0 or not r0.stdout.rstrip().endswith("TONG: DAT"):
        sys.exit(f"TRUOT TU-KIEM: ban sao KHONG dot bien khong DAT (rc={r0.returncode}) — khong ket luan duoc gi ve la nao: "
                 + ((r0.stdout + r0.stderr).strip().splitlines() or [""])[-1][:160])
    la = [(p, v) for p, v in _la_measured(h) if any(True for _ in _cum_so(v))]
    giet, song_sot, chet_loi = 0, [], []
    for p, v in la:
        for ten, m in _cum_so(v):
            o = copy.deepcopy(goc)
            x = o
            for k in p[:-1]:
                x = x[k]
            x[p[-1]] = m
            r = chay_con(o)
            if r.returncode == 0:
                song_sot.append(".".join(map(str, p)) + " [" + ten + "]")
            elif r.returncode == 1 and "\nTONG: TRUOT" in "\n" + r.stdout:
                giet += 1
            else:
                chet_loi.append(".".join(map(str, p)) + " [" + ten + "]: " + ((r.stdout + r.stderr).strip().splitlines() or [""])[-1][:100])
    for p in song_sot:
        print("LOT  " + p)
    for p in chet_loi:
        print("LOI  " + p)
    dung = len(la) == LA_MEASURED_DU_KIEN
    print(f"TU-KIEM: {len(la)} la measured co chu so (du kien {LA_MEASURED_DU_KIEN}), {giet + len(song_sot) + len(chet_loi)} dot bien: "
          f"{giet} bi MOT CHOT ban TRUOT · {len(song_sot)} song sot · {len(chet_loi)} chet vi loi (khong phai chot)"
          + ("" if dung else " · SO LA LECH du kien (nhan bi doi ten/ha cap?)")
          + (" => day la loi khai, khong phai phep do" if song_sot or chet_loi else ""))
    sys.exit(0 if dung and not song_sot and not chet_loi else 1)


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
rj = json.loads(doc(f"run-{h['post_merge_checks'][0]['run_id']}.json"))
chot(rj["updated_at"] == h["gate_hau_merge"]["hoan_tat"] and h["gate_hau_merge"]["hoan_tat"] in h["gate_hau_merge"]["ket_qua"],
     f"gate hau merge: hoan_tat khai == updated_at REST ({rj['updated_at']})")
# 4b. TUNG check run, khong chi total_count (Codex PR #723, comment 4232301588): moi object phai completed, head dung,
#     va dem theo (run_id, conclusion) phai khop dong `check_runs` khai cho run do; tong theo conclusion phai khop
#     tom tat khai (skipped dem RIENG, khong gop vao success).
def cr(f):
    d = json.loads(doc(f))
    chot(d["total_count"] == len(d["check_runs"]), f"{f}: total_count == so object ({len(d['check_runs'])})")
    for c in d["check_runs"]:
        # Danh tinh job Actions (Codex PR #723, comment 4232647485): app github-actions + URL Actions chinh tac cua kho
        # nay, job id trong URL == id cua check run. Khong khop thi KHONG trich run id tu URL.
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
n_th = sum(1 for c in bang["658bd0c"] if c[4] == "thu-hoi")
chot(kq6 == f"{len(bang['658bd0c'])} check run = {n6['success']} success (gom {n_th} thu-hoi) + {n6['skipped']} skipped (mo) (readback checkruns-658bd0c.json).",
     "ci_pr_tren_ung_vien.ket_qua BANG van xuoi dung tu dem tren checkruns-658bd0c.json (ke ca so thu-hoi)")
n3 = len(bang["3fc0932"])
rid3 = h["post_merge_checks"][0]["run_id"]
chot(f"{n3}/{n3} check run success" in h["gate_hau_merge"]["ket_qua"]
     and h["post_merge_checks"][0]["ket_qua"] == f"measured — run-{rid3}.json completed success; checkruns-{h['merge_commit'][:7]}.json: {n3} check run, {n3} success.",
     "hau merge: gate_hau_merge.ket_qua + post_merge_checks[0].ket_qua BANG van xuoi (dem, run_id, ten tep readback)")
ids = {int(re.search(r"/runs/(\d+)/", c["details_url"]).group(1))
       for c in json.loads(doc("checkruns-658bd0c.json"))["check_runs"]}
khai = {x["run_id"] for x in h["pre_merge_checks"] if "run_id" in x}
chot(ids == khai, f"run truoc merge: checkruns {sorted(ids)} == khai {sorted(khai)}")
# 4c. Thu tu thoi gian cua quyet dinh land (truoc day chi do "Codex xong SAU merge", muc 8): CI truoc merge phai xong <= merged_at,
#     run hau merge phai duoc tao >= merged_at.
pre_xong = [c["completed_at"] for c in json.loads(doc("checkruns-658bd0c.json"))["check_runs"]]
chot(bool(pre_xong) and all(ts(x) <= ts(merged) for x in pre_xong), f"thu tu: {len(pre_xong)} check run truoc merge deu hoan tat <= merged_at {merged}")
chot(ts(rj["created_at"]) >= ts(merged), "thu tu: run hau merge duoc tao >= merged_at")

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
ha = h["review_tai_head_da_merge"]["human_audit"]
chot(ha["assurance"] == "human_audited" and ha["verdict"] == "approve" and dong_au[0].startswith("Human audit — approve ")
     and str(ha.get("assurance_dat", "")).startswith("KHAI, CHUA DAT"),
     "human_audit: assurance/verdict khop dong dau than comment; assurance_dat con khai thieu hut (nhan khong duoc lat manh hon bang chung)")
ad = str(ha.get("assurance_dat", ""))
chot(f"luot {h['review_ai_truoc_drift']['luot']} (stale)" in ad and f"lượt {h['review_ai_truoc_drift']['luot']}" in au["body"] and "'CI 15/15'" in ad and "15/15 success" in au["body"]
     and f"do duoc {len(bang['658bd0c'])} ({dem(bang['658bd0c'])['success']}+{dem(bang['658bd0c'])['skipped']})" in ad
     and "khong co dong `Reviewed commit:`" in ad and not any(x.startswith("Reviewed commit:") for x in dong_au),
     "human_audit.assurance_dat: su that (luot stale, 'CI 15/15', 17 = 16+1, khong co Reviewed commit) khop than comment va dem check run (L3)")
chot(h["merge_method"] == "merge" and dong_au.count(
    f"- Uỷ quyền: merge đúng SHA {sha[:7]} bằng merge commit (không squash), rồi chạy hậu-merge gate và bookkeeping. "
    "Head đổi thêm thì uỷ quyền này hết hiệu lực.") == 1, "uy quyen: dong uy quyen merge commit dung nguyen van, mot lan")
b_au = au["body"].encode("utf-8")
khai_au = h["review_tai_head_da_merge"]["human_audit"]["do_duoc"]
chot(f"than {len(b_au)} byte sha256 {hashlib.sha256(b_au).hexdigest()}" in khai_au
     and '"Human audit — approve #' + str(h["pr"]) + " tai head " + sha[:7] + '..."' in khai_au,
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
chot(sorted(f["filename"] for f in cm["files"]) == sorted(h["write_set"]) and len(cm["files"]) == tm["kiem_tra"]["diff_stat"]["tep"],
     "merge: tep doi trong commit-3fc0932.json == write_set YAML (nen cua lap luan `workflow khong nam trong diff`)")
chot(h["gate_hau_merge"]["head_sha"] == h["merge_commit"] and h["gate_hau_merge"]["run"] == h["post_merge_checks"][0]["run_id"],
     "gate hau merge: head_sha == merge_commit, run == post_merge_checks[0].run_id")
chot(pr["merged_by"]["login"] == h["approver"] and f"merged_by trong pr-621.json la tai khoan {pr['merged_by']['login']}"
     in h["land_operator"], f"pr: merged_by {pr['merged_by']['login']} == tac nhan khai trong land_operator (Codex 4232647519)")
chot(pr["merged"] is True and pr["html_url"] == f"https://github.com/ducthangho/tra-luat/pull/{h['pr']}" and pr["number"] == h["pr"] and pr["base"]["ref"] == "master", "pr: merged, dung so, base master")
tp = h["trang_thai_packet"]
chot(tp["merged"] is pr["merged"] and isinstance(tp["landed"], bool), "trang_thai_packet: merged == pr-621.json, landed la bool")
# L3 — landed_ly_do va mo_ta cua khong_do_duoc la CHINH van ban chu kho doc de quyet dinh; khong nam trong nut `measured` nen --tu-kiem khong thu (do 10-10-2026: 20/20
# cum chu so cua landed_ly_do, 18/18 cua khong_do_duoc[2].mo_ta song sot). Buoc cac su that co the do: tap run id, dem hau merge, SHA, OID merge ref.
chot({int(x) for x in re.findall(r"(?<!\d)\d{11}(?!\d)", tp["landed_ly_do"])} == khong_skip and f"{n3}/{n3}" in tp["landed_ly_do"]
     and h["merge_commit"][:7] in tp["landed_ly_do"] and sha[:7] in tp["landed_ly_do"],
     "trang_thai_packet.landed_ly_do: tap run id == run khong skipped (pham_vi_run), dem hau merge, SHA merge/ung vien khop hien vat")
m_mr = re.search(r"refs/pull/621/merge = ([0-9a-f]{7})(?![0-9a-f])", next(k for k in h["khong_do_duoc"] if k["id"] == "CHECKOUT-IDENTITY")["mo_ta"])
chot(bool(m_mr) and a_truoc.get("refs/pull/621/merge", "")[:7] == m_mr.group(1), "khong_do_duoc CHECKOUT-IDENTITY.mo_ta: OID merge ref == anh ls-remote truoc merge")
qd = h.get("quyet_dinh_chu_kho") or {}
PR_GHI_SO = 723   # quyet dinh chu kho phai nam tren CHINH PR mang ho so nay (bookkeeping: "chu ky moi tren head hien hanh cua PR #723")


# L7 — THAN = DUNG CAC DONG MAU, KHONG GI KHAC. L3..L6 moi vong deu tim them mot cach de GitHub hien mot dong mau la trich dan/code/thuoc tinh HTML/an ma bo kiem
# van dem la quyet dinh (khoi rao khac loai, chu thich HTML, thut 4, trich dan lazy, CR don, NBSP, dau cach roi tab, lien ket/anh nhieu dong, BOM...). Bon vong cung MOT
# hinh dang loi => sai o QUYET DINH GOC: co doc mot than Markdown TU DO roi doan dong nao HIEN THUONG. Bo quyet dinh do: than chi duoc gom cac dong mau (bat dau o cot 0,
# toan ASCII in duoc) va dong trong. Mot dong bat dau bang chu cai, khong co ky tu dac biet cua Markdown dau dong, chi co the la doan van thuong => khong con cau truc nao
# phai mo hinh hoa. Doi lai: chu kho KHONG viet them loi trong comment ky (y kien viet o comment khac).
_MAU = {"Reviewed commit": r"Reviewed commit: ([0-9a-f]{40})", "assurance_dat": r"assurance_dat: (chap_nhan)",
        **{c: re.escape(c) + r": chap_nhan ([0-9]{11}(?:, ?[0-9]{11})*)" for c in can}}


def than_sai(cua, reviewed_sha, run_cua):
    """L7 — DANH SACH ly do than comment KHONG doc duoc la CHAP NHAN (rong = hop le), moi ly do gan voi mot dong neu so dong. Than chi gom: `Reviewed commit: <40 hex>`
    == reviewed_sha; moi diem `<ID>: chap_nhan <run>,<run>,...` (dung tap run cua pham_vi_run, cach bang `,` hoac `, `); `assurance_dat: chap_nhan`; va dong trong.
    Duoc: CRLF, dau cach cuoi dong. Moi dong khac (van xuoi, dau danh sach, thut, rao, trich dan, HTML, in dam...) va moi ky tu ngoai ASCII in duoc (BOM, NBSP, tab,
    CR don, U+2028, ky tu vo hinh) => TU CHOI CA THAN."""
    cua = cua.replace("\r\n", "\n")
    bad = sorted({f"U+{ord(x):04X}" for x in cua if x != "\n" and not " " <= x <= "~"})
    if bad:
        return [f"than co ky tu ngoai ASCII in duoc ({', '.join(bad[:5])}): BOM, NBSP, tab, CR don, U+2028... - than ky chi duoc co dong mau"]
    sai, thay = [], {k: [] for k in _MAU}
    for i, d in enumerate(cua.split("\n"), 1):
        d = d.rstrip(" ")
        if not d:
            continue
        km = [(k, m) for k, m in ((k, re.fullmatch(p, d)) for k, p in _MAU.items()) if m]   # khop MOT lan, dung chinh ket qua do
        if km:
            thay[km[0][0]].append((i, km[0][1].group(1)))
        else:
            sai.append(f"dong {i}: khong phai dong mau - than ky chi duoc co dong mau (bat dau o cot 0) va dong trong")
    for k, v in thay.items():
        if len(v) != 1:
            sai.append(f"`{k}`: can DUNG MOT dong theo mau, co {len(v)}" + (f" (dong {', '.join(str(i) for i, _ in v)})" if v else ""))
    if len(thay["Reviewed commit"]) == 1 and thay["Reviewed commit"][0][1] != reviewed_sha:
        sai.append(f"dong {thay['Reviewed commit'][0][0]}: Reviewed commit != quyet_dinh_chu_kho.reviewed_sha")
    for c in can:
        if len(thay[c]) == 1 and sorted(int(x) for x in thay[c][0][1].split(",")) != sorted(run_cua[c]):
            sai.append(f"dong {thay[c][0][0]}: tap run cua `{c}` != pham_vi_run {sorted(run_cua[c])}")
    return sai


def _ca_than():
    """L5/L7 — phan chung CHAY DUOC cho than_sai, o MOI lan chay bo kiem. Du lieu CO DINH, khong doc tu ho so: --tu-kiem doi chu so cua ho so khong lam lech bang nay.
    Than hop le phai ra rong; than bi tu choi phai ra DUNG ly do. Cac ca tu choi giu lai MOI hinh dang da lot o L3..L6 (rao, HTML, thut, trich dan, NBSP, BOM, `[`...)."""
    rs, sha_, run = "11111111111,22222222222,33333333333,44444444444", "0123456789abcdef" * 2 + "01234567", {c: {11111111111, 22222222222, 33333333333, 44444444444} for c in can}
    L = [f"Reviewed commit: {sha_}", *(f"{c}: chap_nhan {rs}" for c in can), "assurance_dat: chap_nhan"]
    sua, nl = (lambda i, s: L[:i] + [s] + L[i + 1:]), "\n".join
    hop = {"LF": nl(L), "CRLF": "\r\n".join(L), "dau cach cuoi dong": nl(x + "  " for x in L), "run cach ', '": nl(L).replace(",", ", "),
           "dong trong xen giua, dau, cuoi": nl(["", *[y for x in L for y in (x, "")], ""]), "thu tu dong dao": nl(L[::-1])}
    ngoai, khac = "than co ky tu ngoai ASCII", "dong 1: khong phai dong mau"
    bad = {"diem tu_choi": (nl(sua(3, f"CHECKOUT-IDENTITY: tu_choi {rs}")), "dong 4: khong phai dong mau"), "thieu diem": (nl(L[:3] + L[4:]), "`CHECKOUT-IDENTITY`: can DUNG MOT dong"),
           "diem lap": (nl(L + [L[3]]), "co 2"), "thieu 1 run": (nl(sua(3, "CHECKOUT-IDENTITY: chap_nhan 11111111111,22222222222,33333333333")), "tap run cua `CHECKOUT-IDENTITY`"),
           "commit lap sai dang": (nl(L + ["Reviewed commit: abcdef0"]), "dong 6: khong phai dong mau"), "commit lech": (nl(sua(0, "Reviewed commit: " + "0" * 40)), "!= quyet_dinh_chu_kho.reviewed_sha"),
           "thieu assurance": (nl(L[:4]), "`assurance_dat`: can DUNG MOT dong"), "assurance hau to": (nl(sua(4, "assurance_dat: chap_nhan (chua dat)")), "dong 5: khong phai dong mau"),
           "van xuoi xen giua": (nl(["Toi quyet:", "", *L]), khac), "rao": (nl(["```", *L, "```"]), khac), "trich dan": (nl(["> y kien cu", "", *L]), khac),
           "chu thich HTML": (nl(["<!--", *L, "-->"]), khac), "gach dau dong": (nl("- " + x for x in L), khac), "so thu tu": (nl(f"{i + 1}. " + x for i, x in enumerate(L)), khac),
           "thut 1 dau cach": (nl(" " + x for x in L), khac), "thut 4": (nl("    " + x for x in L), khac), "in dam": (nl("**" + x + "**" for x in L), khac),
           "viet thuong": (nl(sua(0, L[0].lower())), khac), "lien ket mo nhieu dong": (nl(['[a]: /u "', *L, '"']), khac), "anh alt nhieu dong": (nl(["![", *L, "](/x.png)"]), khac),
           "tab": (nl("\t" + x for x in L), ngoai), "dau cach roi tab": (nl(" \t" + x for x in L), ngoai), "NBSP sau trich dan": (nl(["> y", " ", *L]), ngoai),
           "BOM": ("﻿" + nl(L), ngoai), "CR don": ("\r".join(L), ngoai), "U+2028": (" ".join(L), ngoai), "tieng Viet": (nl(L + ["Ky tên"]), ngoai),
           "ky tu vo hinh": (nl(sua(4, "assurance_dat: chap_nhan​")), ngoai), "rong": ("", "can DUNG MOT dong")}
    return ([f"hop le `{k}` bi tu choi: {than_sai(b, sha_, run)}" for k, b in hop.items() if than_sai(b, sha_, run)]
            + [f"`{k}` khong ra ly do `{s}`: {than_sai(b, sha_, run)}" for k, (b, s) in bad.items() if not any(s in r for r in than_sai(b, sha_, run))], len(hop), len(bad))


_loi_than, _n_hop, _n_bad = _ca_than()
chot(not _loi_than, f"than_sai (L7): {_n_hop} than hop le DAT, {_n_bad} than bi tu choi voi DUNG ly do (du lieu co dinh, khong doc tu ho so)" + "".join(f"\n      -> {s}" for s in _loi_than))


def landed_hop_le(qd_, tep, doc_, approver, merged_, pham_vi_):
    """N04 + L3 + L5 + L6 — `landed: true` can quyet dinh chu kho co NEO doc duoc VA THAN comment DOC DUOC la CHAP NHAN: URL comment tren PR_GHI_SO + readback trong provenance
    (id/URL/issue_url khop, tac gia == approver, OWNER, khong qua app, tao SAU merge, chua sua) + than comment theo MAU (than_sai). Tra ve DANH SACH ly do khong hop le
    (rong = hop le) de chot `landed` chi dung dong/dieu kien sai. HAM THUAN (L6): moi dau vao la doi so (quyet dinh, ten tep co trong provenance, ham doc tep, tac gia, gio merge,
    pham_vi) de `_ca_landed` chay no o MOI lan chay bo kiem — khi `landed: false` ham nay khong bao gio duoc goi voi ho so that. (L3 do 10-10-2026: comment THAT 6084105994 — quyet
    dinh CU tren 06fc9a8, chi 2 diem, chi 1 run — lot ban truoc khi buoc than; L4: ban chi doi SU CO MAT cua id/run; L5: ban doc theo dong nhung mo hinh Markdown con ho.) Khong do
    duoc offline: comment ky tren DUNG head hien hanh cua PR ghi so; KHONG doc van xuoi: mot cau tu choi viet bang loi khong phai dong mau thi khong bi bat."""
    nb = str(qd_.get("neo_ben", ""))
    m_nb = re.fullmatch(rf"https://github\.com/ducthangho/tra-luat/pull/{PR_GHI_SO}#issuecomment-(\d+)", nb)
    ten = str(qd_.get("readback", ""))
    if not m_nb or not ten or "/" in ten or ten not in tep:
        return ["neo_ben khong phai URL comment tren PR ghi so, hoac readback thieu / khong la ten tep trong provenance"]
    rb = json.loads(doc_(ten))
    dk = [(rb.get("html_url") == nb and str(rb.get("id")) == m_nb.group(1), "readback: html_url/id != neo_ben"),
          ((rb.get("user") or {}).get("login") == approver, f"readback: tac gia != approver {approver}"),
          (rb.get("author_association") == "OWNER", "readback: author_association != OWNER"),
          ("performed_via_github_app" in rb and rb["performed_via_github_app"] is None, "readback: dang qua app, hoac THIEU khoa performed_via_github_app"),
          (ts(rb["created_at"]) > ts(merged_), "readback: created_at khong SAU merge"),
          (rb.get("updated_at") == rb.get("created_at"), "readback: comment da bi sua (updated_at != created_at)"),
          (str(rb.get("issue_url", "")).endswith(f"/repos/ducthangho/tra-luat/issues/{PR_GHI_SO}"), f"readback: issue_url khong tro toi PR #{PR_GHI_SO}"),
          (all(set(qd_.get("pham_vi_run", [])) == pham_vi_[c] for c in can), "quyet_dinh_chu_kho.pham_vi_run != pham_vi_run cua tung diem"),
          (qd_.get("assurance_dat") == "chap_nhan", "quyet_dinh_chu_kho.assurance_dat != chap_nhan")]
    return [s for ok, s in dk if not ok] + than_sai(rb.get("body") or "", str(qd_.get("reviewed_sha", "")), pham_vi_)


def sai_landed_cua(landed, ly_do, *args):
    """L6 — chot `landed`: false => khong doc quyet dinh (rong); true => landed_hop_le + `landed_ly_do` het `CON THIEU`. Tach thanh ham de `_ca_landed` chay duoc nhanh `landed is False`
    va `CON THIEU` (dot bien `[] if True` hay bo `CON THIEU` khong con song sot)."""
    return [] if landed is False else landed_hop_le(*args) + (["landed_ly_do con `CON THIEU`"] if "CON THIEU" in ly_do else [])


def _ca_landed():
    """L6 — phan chung CHAY DUOC cho landed_hop_le, o MOI lan chay (landed: false thi ho so that khong goi no: thay no bang `return []` van ra DAT — do 10-10-2026, 15/15 dot bien
    cua readback + keo noi song sot). Du lieu CO DINH. Mot readback hop le phai ra rong; moi dieu kien readback/quyet dinh bi pha rieng le phai ra DUNG ly do cua no."""
    sha_, rs, merged_ = "0123456789abcdef" * 2 + "01234567", "11111111111,22222222222,33333333333,44444444444", "2026-10-09T14:14:34Z"
    run, neo = {c: {11111111111, 22222222222, 33333333333, 44444444444} for c in can}, "https://github.com/ducthangho/tra-luat/pull/723#issuecomment-1"
    body = "\n".join([f"Reviewed commit: {sha_}", *(f"{c}: chap_nhan {rs}" for c in can), "assurance_dat: chap_nhan"])
    rb0 = {"html_url": neo, "id": 1, "user": {"login": "chu-kho"}, "author_association": "OWNER", "performed_via_github_app": None, "created_at": "2026-10-09T15:00:00Z",
           "updated_at": "2026-10-09T15:00:00Z", "issue_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/723", "body": body}
    qd0 = {"neo_ben": neo, "readback": "rb.json", "reviewed_sha": sha_, "pham_vi_run": sorted(run[can[0]]), "assurance_dat": "chap_nhan"}

    def chay(mut, landed=True, ly_do="xong"):
        rb, q, tep = json.loads(json.dumps(rb0)), json.loads(json.dumps(qd0)), {"rb.json"}
        mut(rb, q, tep)
        return sai_landed_cua(landed, ly_do, q, tep, lambda ten: json.dumps(rb), "chu-kho", merged_, run)
    hop = {"nguyen ban": (lambda rb, q, t: None, {}), "landed false: khong doc quyet dinh (than sai van ra rong)": (lambda rb, q, t: rb.update(body="x"), {"landed": False}),
           "than CRLF": (lambda rb, q, t: rb.update(body=body.replace("\n", "\r\n")), {})}
    bad = {"tac gia khac approver": (lambda rb, q, t: rb["user"].update(login="khac"), "tac gia != approver"), "author_association != OWNER": (lambda rb, q, t: rb.update(author_association="MEMBER"), "!= OWNER"),
           "qua app": (lambda rb, q, t: rb.update(performed_via_github_app={"slug": "claude"}), "dang qua app"), "THIEU khoa performed_via_github_app": (lambda rb, q, t: rb.pop("performed_via_github_app"), "THIEU khoa"),
           "created_at TRUOC merge": (lambda rb, q, t: rb.update(created_at="2026-10-09T14:14:00Z", updated_at="2026-10-09T14:14:00Z"), "khong SAU merge"),
           "created_at BANG merge": (lambda rb, q, t: rb.update(created_at=merged_, updated_at=merged_), "khong SAU merge"), "da sua": (lambda rb, q, t: rb.update(updated_at="2026-10-09T16:00:00Z"), "da bi sua"),
           "issue_url sang PR khac": (lambda rb, q, t: rb.update(issue_url="https://api.github.com/repos/ducthangho/tra-luat/issues/621"), "issue_url khong tro toi PR #723"),
           "id lech neo_ben": (lambda rb, q, t: rb.update(id=2), "html_url/id != neo_ben"), "pham_vi_run thieu mot run": (lambda rb, q, t: q.update(pham_vi_run=q["pham_vi_run"][:3]), "pham_vi_run != pham_vi_run"),
           "assurance_dat != chap_nhan": (lambda rb, q, t: q.update(assurance_dat="tu_choi"), "assurance_dat != chap_nhan"),
           "neo_ben sang PR khac": (lambda rb, q, t: q.update(neo_ben=neo.replace("pull/723", "pull/621")), "neo_ben khong phai URL comment tren PR ghi so"),
           "readback co dau /": (lambda rb, q, t: (q.update(readback="../rb.json"), t.add("../rb.json")), "neo_ben khong phai URL"), "readback khong co trong provenance": (lambda rb, q, t: t.clear(), "neo_ben khong phai URL"),
           "reviewed_sha lech than": (lambda rb, q, t: q.update(reviewed_sha="0" * 40), "Reviewed commit != quyet_dinh_chu_kho.reviewed_sha"),
           "than tu_choi mot diem": (lambda rb, q, t: rb.update(body=body.replace("CHECKOUT-IDENTITY: chap_nhan", "CHECKOUT-IDENTITY: tu_choi")), "dong 4: khong phai dong mau"),
           "than null": (lambda rb, q, t: rb.update(body=None), "can DUNG MOT dong"),
           "landed_ly_do con CON THIEU": (lambda rb, q, t: None, "landed_ly_do con `CON THIEU`", {"ly_do": "CON THIEU"})}
    return ([f"hop le `{k}` bi tu choi: {chay(m, **kw)}" for k, (m, kw) in hop.items() if chay(m, **kw)]
            + [f"`{k}` khong ra ly do `{sub_}`: {chay(m, **(kw[0] if kw else {}))}" for k, (m, sub_, *kw) in bad.items() if not any(sub_ in r for r in chay(m, **(kw[0] if kw else {})))], len(hop), len(bad))


_loi_landed, _n_hop_l, _n_bad_l = _ca_landed()
chot(not _loi_landed, f"landed_hop_le (L6): {_n_hop_l} readback hop le DAT, {_n_bad_l} bi tu choi voi DUNG ly do (du lieu co dinh, khong doc tu ho so)" + "".join(f"\n      -> {x}" for x in _loi_landed))
sai_landed = sai_landed_cua(tp["landed"], tp["landed_ly_do"], qd, {x.name for x in P.iterdir() if x.is_file()}, doc, h["approver"], merged, pham_vi)
chot(not sai_landed,
     "landed: true chi khi quyet_dinh_chu_kho co neo_ben (URL tren PR ghi so) + readback (OWNER, khong app, SAU merge, chua sua) + THAN comment THEO MAU (dong `Reviewed commit: <40 hex>` == reviewed_sha; moi diem `<ID>: chap_nhan <4 run id cach nhau dau phay>`; dong `assurance_dat: chap_nhan`; than CHI gom dong mau va dong trong, toan ASCII in duoc - moi dong/ky tu khac bi TU CHOI) + pham_vi_run + assurance_dat: chap_nhan; landed_ly_do het `CON THIEU`"
     + "".join(f"\n      -> {x}" for x in sai_landed))

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
chot(f"comment-{cx['id']}-codex.json, reviews-{h['pr']}.json, review-comments-{h['pr']}.json" in kq_cx["ket_qua"]
     and f"PR #{h['pr']} co 0 review object va 0 review comment" in kq_cx["ket_qua"] and md["commit"] in kq_cx["ket_qua"] and md["luc"][:19] in kq_cx["ket_qua"] and md["trigger"] in kq_cx["ket_qua"]
     and kq_cx["thu_tu_thoi_gian"].startswith(f"measured — merge {merged[11:19]}Z (merged_at, pr-{h['pr']}.json) TRUOC khi Codex hoan tat ({md['luc'][11:19]}Z).") ,
     "connector: ket_qua + thu_tu_thoi_gian (van xuoi) khop readback")

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
chot(ls_["ket_qua"].startswith(f"{len(ag)}/{len(ag)} rc=0, NGUOI_GIU 0 (readback ai-dang-giu-write-set.txt;") and f"({len(ag)} duong dan" in ls_["lenh"]
     and f"{len(mc_l)}/{len(cb_l)}," in ls_["lenh"], "lease: so duong dan, NGUOI_GIU 0 va so nhanh trong YAML khop hien vat")
m_ag = re.match(r"# ai-dang-giu [^\n]*checkout origin/master (\w+), \d{4}-\d\d-\d\dT(\d\d:\d\d):\d\dZ\)", ag_tho)
chot(bool(m_ag) and m_ag.group(1)[:7] in ls_["lenh"] and m_ag.group(2) + "Z" in ls_["lenh"], "lease: oid origin/master va gio (HH:MM) cua dong dau hien vat co trong lenh YAML")

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
    # N05 — GIT_CONFIG_GLOBAL=devnull bo luon `safe.directory` cua nguoi dung: kho do uid khac / thu muc chia se => git tu choi ("dubious
    # ownership"), va dong duoi doc loi do thanh "nong hoac khong phai kho git". Bo kiem chi chay git DOC tren kho nguoi dung CHI DINH bang --repo
    # => tin tuong tuong minh qua bien moi truong (cung pham vi "protected"). Tin tuong do CHI an toan khi MOI lenh `diff` mang --no-ext-diff
    # --no-textconv (qua _AN): do 10-10-2026, thieu hai co nay o d40 thi `diff.external` / `diff.<drv>.textconv` trong .git/config cua kho do
    # uid khac CHAY lenh tuy y va bo kiem van ra `TONG: DAT`.
    _GIT_ENV.update(GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="safe.directory", GIT_CONFIG_VALUE_0="*")
    if subprocess.run(["git", "-C", repo, "rev-parse", "--is-shallow-repository"], capture_output=True, text=True, env=_GIT_ENV).stdout.strip() != "false":
        raise SystemExit("TRUOT repo: nong hoac khong phai kho git (digest va dem commit tren kho nong la sai)")

    _AN = ("--no-ext-diff", "--no-textconv")
    _DIFF = ["--no-color", *_AN, "--src-prefix=a/", "--dst-prefix=b/", "-U3", "--diff-algorithm=myers", "--indent-heuristic", "-M"]

    def d(a, b):
        out = subprocess.run(["git", "-C", repo, "-c", "core.abbrev=7", "diff", *_DIFF, a, b], capture_output=True, check=True, env=_GIT_ENV).stdout
        return hashlib.sha256(out).hexdigest()

    chot(d("6980e5bf04e4e5b8b75e5817578f1aba13f2f5ab", "675895db34e9a7c1357f8d8ad8925bf8f01ad21c") == DG, "diff truoc drift (OID ghim)")
    chot(d("8b59185975a938504de5963d2310e574dd4858b2", "658bd0cdc56bbd3445f489dcfc571e22eee7d675") == DG, "diff ung vien (OID ghim)")
    chot(d("3fc0932a3d1617c4352e5a7982f2e6e4208ca3f7", "658bd0cdc56bbd3445f489dcfc571e22eee7d675") != DG, "ref SAU merge cho digest KHAC")

    def d40(a, b):
        return hashlib.sha256(subprocess.run(["git", "-C", repo, "-c", "core.abbrev=40", "diff", *_DIFF, a, b], capture_output=True, check=True, env=_GIT_ENV).stdout).hexdigest()

    hd = h["ung_vien"]["head_drift"]
    dg40, rong = d40("6980e5bf04e4e5b8b75e5817578f1aba13f2f5ab", "675895db34e9a7c1357f8d8ad8925bf8f01ad21c"), hashlib.sha256(b"").hexdigest()
    chot(DG in hd["lenh"] and dg40 == d40("8b59185975a938504de5963d2310e574dd4858b2", "658bd0cdc56bbd3445f489dcfc571e22eee7d675") and dg40 in hd["phan_chung"] and "core.abbrev=40" in hd["phan_chung"]
         and d("3fc0932a3d1617c4352e5a7982f2e6e4208ca3f7", "658bd0cdc56bbd3445f489dcfc571e22eee7d675") == rong and rong in hd["phan_chung"]
         and h["merge_commit"] in hd["phan_chung"],
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
    ns = g("diff", *_AN, "--shortstat", tm["cha"][0], h["merge_commit"])
    m_ns = re.fullmatch(r"(\d+) files? changed(?:, (\d+) insertions?\(\+\))?(?:, (\d+) deletions?\(-\))?", ns)
    ds = {"tep": int(m_ns.group(1)), "them": int(m_ns.group(2) or 0), "xoa": int(m_ns.group(3) or 0)} if m_ns else None
    chot(ds == tm["kiem_tra"]["diff_stat"] and f"=> {ds['tep']} tep, +{ds['them']}" in tm["kiem_tra"]["ket_qua"],
         f"merge (git): diff --shortstat {ns!r} == khai")
    chot(sorted(g("diff", *_AN, "--name-only", tm["cha"][0], h["merge_commit"]).splitlines()) == sorted(h["write_set"]), "merge (git): tep doi 8b59185..3fc0932 == write_set YAML")

if LOI:
    print(f"TONG: TRUOT {len(LOI)}")
    sys.exit(1)
if "--repo" not in sys.argv:
    print("TONG: CHUA DU — moi chot doc tep dat, chot digest KHONG DO DUOC (thieu --repo)")
    sys.exit(2)
print("TONG: DAT")
sys.exit(0)
