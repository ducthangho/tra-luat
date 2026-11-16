"""Danh gia moc Gate output §10.2.2 cho MOT run, THEO TUNG BUOC: moi job (tru job skipped) phai co DU cac buoc bat buoc cua loai
job, va MOI buoc phai co dau hieu ket qua duong NAM TRONG CHINH output cua buoc ay (connector P1 r4469885562 tren PR #1190: ban truoc
nhan bat ky "TỔNG: ĐẠT" nao trong log job, ma idiom_py_test in dung dong ay doc lap voi tl selftest/golden/release).

Thieu buoc, hoac buoc thieu dau hieu => job `not_measured` => moc `not_measured` (khong bao gio suy pass tu conclusion + ##[error]=0).
Buoc bi `if:` bo qua khong co trong log => thieu => not_measured (lane Windows/duong nhanh ra not_measured la DUNG, khong phai loi).

Cach goi:
  python3 danh_gia_gate.py <run_id> <tep_ra>
  python3 danh_gia_gate.py <run_id> - --am-buoc <TIEN_TO_JOB> <CHUOI_BUOC>   phan chung: xoa DAU HIEU cua mot buoc (giu nguyen buoc
      khac, ke ca "TỔNG: ĐẠT" cua buoc khac) roi danh gia lai job ay; PHAI ra not_measured (rc 0), ra passed thi rc 1.
"""
import hashlib, json, os, re, sys, urllib.error, urllib.request

TOK = os.environ.get("GITHUB_PAT", "")
API = "https://api.github.com/repos/ducthangho/tra-luat/"


class _KhongChuyenHuong(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def raw(u):
    """GET REST. Log job tra 302 sang kho blob: theo TAY, KHONG mang token sang host khac (nhu ops/ci_provenance.py:goi_that;
    connector P2 r4469672182 — urlopen mac dinh chuyen ca header Authorization theo redirect)."""
    req = urllib.request.Request(API + u, headers={"Authorization": "Bearer " + TOK, "Accept": "application/vnd.github+json"})
    try:
        return urllib.request.build_opener(_KhongChuyenHuong).open(req, timeout=120).read()
    except urllib.error.HTTPError as e:
        loc = e.headers.get("Location") if e.code in (301, 302, 303, 307, 308) else None
        if not loc:
            raise
    return urllib.request.urlopen(urllib.request.Request(loc), timeout=120).read()   # chuoi tran: khong header token


JSON_OK = "JSON_OK"   # dau hieu dac biet: object JSON dau tien trong output cua buoc co khoa cap ngoai `ok` == True
# "CUOI:<regex>": dong TONG/TỔNG CUOI CUNG cua buoc phai khop (bo con trong cung buoc cung in "TỔNG: ĐẠT" — chi dong cuoi la tong ket).
# "KHONG:<regex>": KHONG dong nao cua buoc duoc khop (vd mot bo con ĐỎ trong ci_dang_ky_test).
TL_SELFTEST = "== tl selftest"   # buoc tl selftest: than lenh la khoi bash dai, nhan dien bang dau hieu cua chinh no
TL_SELFTEST_PATS = [r"^== tl selftest (\d+)/\1 ==$", r'^\{"ok": true, "status": "pass", "name": "tl-selftest", "returncode": 0']

# (tien to ten job, [(chuoi nhan dien BUOC trong than lenh `run`, [regex dau hieu duong BAT BUOC trong output buoc ay])])
LUAT = [
    ("chuan-bi", [("ops/ci_duong_nhanh.py", [r"^che_do=(day_du|duong_nhanh)$"])]),
    ("gate-cong-cu-gop", [("ops/cong_cu_test.py --gop", [r"^SỐ LIỆU GOM: ca=(\d+) · đột biến=(\d+) · lỗi đột biến=0$"])]),
    ("gate-cong-cu (", [("ops/cong_cu.py kiem-tra", [r"^cong_cu_test: (\d+)/\1 đạt;", r"^MẢNH \d+/\d+: (\d+)/\1 đột biến bán kính 1"])]),
    ("gate-nhanh-manh", [("ops/nhanh_don_duoc_test.py", [r"^targeted_mutant_gate MANH \d+/\d+: rc=0 · passed (\d+)/\1$"])]),
    ("gate-nhanh-gop", [("--gop-dich", [r"^targeted_mutant_gate: DAT"])]),
    ("gate-packet-loop", [(".claude/dev/packet_loop_test.py", ["CUOI:^TỔNG: ĐẠT$"])]),
    ("gate-ops", [
        ("ops/ci_duong_nhanh_test.py", ["CUOI:^TONG: DAT$"]),
        ("ops/bien_nhan_v2_test.py", [r"^bien_nhan_v2_test: (\d+)/\1 ca đạt", "CUOI:^TỔNG: ĐẠT$"]),
        ("ops/chay_lease_publish_test.sh", [r"^lease_publish: (\d+)/\1 đạt; đã chạy=\1, bỏ qua=0$"]),
        ("scripts/don-nhanh_test.ps1", [r"^don-nhanh: (\d+)/\1 dat$"]),
        (".claude/dev/gate_lifecycle_test.py", [r"^gate lifecycle tests: (\d+)/\1 ca QUA \(bo qua 0, hong 0\)$"]),
    ]),
    ("gate-registry", [(".claude/dev/ci_dang_ky_test.py --chay", ["CUOI:^TỔNG: ĐẠT$", r"KHONG:^CI_DANG_KY \S+: ĐỎ"])]),
    ("gate (", [
        (".claude/dev/codex_cred_test.py", ["CUOI:^TỔNG: ĐẠT$"]),
        (".claude/dev/idiom_py_test.py", ["CUOI:^TỔNG: ĐẠT$"]),
        (".githooks/eol_policy_test.py", [r"^(\d+)/\1 dat$"]),
        (".githooks/pre_push_test.py", [r"^(\d+)/\1 dat$"]),
        (".githooks/eol_policy.py --all --json", [JSON_OK]),
        (".github/checks/bundle_fragment_check.py --json", [JSON_OK]),
        ("scripts/gen_instructions.py --selftest", [r"^== gen_instructions selftest (\d+)/\1 ==$"]),
        ("scripts/tl_core/command_registry_test.py", [r"^OK$"]),
        (TL_SELFTEST, TL_SELFTEST_PATS),
        ("scripts/tl.py workflow-audit --strict --json", [JSON_OK]),
        ("scripts/tl.py golden-test --json", [JSON_OK]),
        ("scripts/tl.py doc-claims-check --strict --json", [JSON_OK]),
        ("scripts/tl.py determinism-audit --strict --json", [JSON_OK]),
        (".github/checks/ci_phamvi.py --kiem-bam", [r"^OK ci_phamvi"]),
        (".github/checks/ci_phamvi_test.py", [r"^== ci_phamvi_test (\d+)/\1 ==$"]),
        ("scripts/tl.py release-check --full --json", [JSON_OK]),
        ("scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json", [JSON_OK]),
        ("scripts/tl.py release-bundle --out dist/a.zip", [r"^bundle sha256 = [0-9a-f]{64}$"]),
    ]),
    ("launcher (", [("launcher_test.py", [r"^(\d+)/\1 ca DA CHAY QUA", r"^DOT BIEN: (\d+)/\1 dat"])]),
]


def buoc(b):
    """Tach log job thanh cac buoc `##[group]Run`: lenh = dong dau + cac dong echo (mau 36;1m), ra = output con lai."""
    out, cur = [], None
    for l in b.decode("utf-8", "replace").splitlines():
        l = re.sub(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ", "", l).rstrip("\r")
        if l.startswith("##[group]Run "):
            cur = {"lenh": [l[13:]], "ra": []}
            out.append(cur)
        elif cur is None:
            continue
        elif "\x1b[36;1m" in l:
            cur["lenh"].append(re.sub(r"\x1b\[[0-9;]*m", "", l))
        elif not l.startswith("##["):
            cur["ra"].append(l)
    return out


def json_ok(ra):
    txt = "\n".join(ra)
    for m in re.finditer(r"^\{", txt, re.M):
        try:
            obj = json.JSONDecoder().raw_decode(txt[m.start():])[0]
        except ValueError:
            continue
        return isinstance(obj, dict) and obj.get("ok") is True
    return False


def khop(pat, ra):
    if pat.startswith("CUOI:"):
        tong = [l.strip() for l in ra if re.match(r"^(TỔNG|TONG):", l)]
        return tong[-1] if tong and re.search(pat[5:], tong[-1]) else None
    if pat.startswith("KHONG:"):
        xau = next((l for l in ra if re.search(pat[6:], l)), None)
        return None if xau else f"khong co /{pat[6:]}/"
    if pat == JSON_OK:
        return "ok:true" if json_ok(ra) else None
    return next((l.strip() for l in ra if re.search(pat, l)), None)


def tim_buoc(ds, nhan):
    if nhan == TL_SELFTEST:
        return [b for b in ds if any(x.strip().startswith("python scripts/tl.py --selftest") or "tl.py --selftest" in x for x in b["lenh"])
                and any(re.search(TL_SELFTEST_PATS[0], l) for l in b["ra"])]
    return [b for b in ds if any(nhan in x for x in b["lenh"])]


def danh_gia(ten, ds):
    for tien_to, buoc_luat in LUAT:
        if not ten.startswith(tien_to):
            continue
        bang = []
        for nhan, pats in buoc_luat:
            bs = tim_buoc(ds, nhan)
            if not bs:
                return "not_measured", f"thieu buoc [{nhan}]"
            for p in pats:
                m = next((x for x in (khop(p, b["ra"]) for b in bs) if x), None)
                if m is None:
                    return "not_measured", f"buoc [{nhan}] thieu dau hieu duong /{p}/"
                bang.append(f"[{nhan[:40]}] {m[:90]}")
        return "passed", " | ".join(bang)
    return "not_measured", "khong co luat cho loai job nay"


def am(ds, nhan):
    """Phan chung: xoa dau hieu duong CHI cua buoc `nhan` (cac buoc khac giu nguyen)."""
    for _, buoc_luat in LUAT:
        for n, pats in buoc_luat:
            if n == nhan:
                for b in tim_buoc(ds, n):
                    b["ra"] = [l for l in b["ra"] if not any(p != JSON_OK and not p.startswith("KHONG:") and re.search(p.split(":", 1)[1] if p.startswith("CUOI:") else p, l) for p in pats)]
                    if JSON_OK in pats:
                        b["ra"] = [l.replace('"ok": true', '"ok": false') for l in b["ra"]]
                return ds
    raise SystemExit(f"khong co buoc {nhan!r} trong LUAT")


def main():
    run_id, ra = sys.argv[1], sys.argv[2]
    am_job = am_buoc = None
    if len(sys.argv) > 5 and sys.argv[3] == "--am-buoc":
        am_job, am_buoc = sys.argv[4], sys.argv[5]
    run = json.loads(raw(f"actions/runs/{run_id}"))
    jobs = json.loads(raw(f"actions/runs/{run_id}/jobs?per_page=100"))["jobs"]
    kq, out = [], [f"# Danh gia Gate output run {run_id} attempt {run['run_attempt']} head {run['head_sha']} — luat dau hieu duong THEO BUOC"
                   f" (danh_gia_gate.py sha256 {hashlib.sha256(open(__file__, 'rb').read()).hexdigest()})", ""]
    for j in sorted(jobs, key=lambda j: j["name"]):
        if am_job and not j["name"].startswith(am_job):
            continue
        if j["conclusion"] == "skipped":
            out.append(f"JOB {j['id']} {j['name']}: skipped (khong tinh)")
            continue
        b = raw(f"actions/jobs/{j['id']}/logs")
        ds = buoc(b)
        if am_job:
            ds = am(ds, am_buoc)
        tt, ct = danh_gia(j["name"], ds)
        if j["conclusion"] != "success":
            tt, ct = "failed", f"conclusion={j['conclusion']}"
        kq.append(tt)
        out.append(f"JOB {j['id']} {j['name']} [{','.join(j['labels'])}] conclusion={j['conclusion']} log_sha256={hashlib.sha256(b).hexdigest()} -> {tt}: {ct}")
    moc = "passed" if kq and all(x == "passed" for x in kq) else ("failed" if "failed" in kq else "not_measured")
    out += ["", f"MOC_GATE_OUTPUT: {moc} ({kq.count('passed')}/{len(kq)} job co dau hieu duong)"]
    if am_job:
        print(out[-1])
        return 0 if moc != "passed" else 1
    open(ra, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(out[-1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
