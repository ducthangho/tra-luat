"""Do native Windows N4/N5 cho PR #1414 (#387 packet B). Chi doc kho, chi ghi trong thu muc phien."""
import ast, datetime, hashlib, json, os, platform, py_compile, re, shutil, subprocess, sys, tarfile, io, time
from pathlib import Path

SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
W = Path(sys.argv[1])
HEAD = "9804f642ad9c7abcc9e7ae4877c2ff133ef31f00"
HTREE = "13c48c05ed0a87c288c79386876c5f78315828f6"
BASE = "3b647461db7c8ded1bddd9aafc5c6aa5eead223f"
SRC = W / "wp1342-src"
TS = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
OUT = W / f"wp387b2-out-{TS}"
BASE_LOG = W / "wp387b-out-20261119T071249Z" / "SUITE-BASE.stdout.txt"
H = W / f"r387h-{TS}"
B = W / f"r387b-{TS}"
M = W / f"r387m-{TS}"
KHOA = Path(r"F:\tl-win\KHOA.txt")
OUT.mkdir(parents=True)
TT = OUT / "TOM-TAT.txt"
BD = datetime.datetime.utcnow()
GH = "https://github.com/ducthangho/tra-luat.git"
TMP = W / "tmp387"; TMP.mkdir(exist_ok=True)
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP))
ENV.pop("PYTHONUTF8", None)

R387_9 = ["r387_m1_chau_ghi_muon_khai_pham_vi_bam", "r387_m1_doi_chung_ghi_som_lam_ve_bam_do",
          "r387_m1_con_thuong_chung_minh_cay_chet", "r387_m2_chau_ghi_trong_han_thi_bam_du",
          "r387_m2_khong_do_duoc_thi_khong_cho", "r387_a_nen_khac_giu_moc_ket_thuc_base",
          "r387_m1_stop_trong_luc_cho_khong_bi_de", "r387_m1_prompt_linux_xoa_khi_cay_chet",
          "r387_m2_ngat_trong_luc_doi_ghi_bi_ngat"]
L1 = ["r387_m2_han_chung_cho_moi_lan_do", "r387_fixture_teardown_bao_loi_giu_loi_goc"] + R387_9 + [
    "t71_ban_chup_prompt_phai_KIN_va_bi_XOA", "t77_ban_chup_qua_han_bi_QUET_du_khong_xoa_duoc_ngay"]
W_IDS = ["r387_b_windows_khong_do", "r387_b_windows_dung_nhom", "r387_b_job_none_thanh_rong",
         "r387_b_windows_long_cay_da_chet", "r387_b_windows_xoa_prompt_khi_job_rong", "r387_b_linux_di_nhanh_job"]
H_IDS = ["r387_fx_dong_truoc_khi_cho", "r387_fx_bao_gan_truoc_khi_gan", "r387_fx_bo_kiem_closehandle",
         "r387_fx_khong_dong_job", "r387_fx_phat_dau_khi_gan_hong", "r387_fx_don_dep_ngoai_finally",
         "r387_fx_loi_bam_nuot_teardown"]


def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def ghi(s):
    with open(TT, "a", encoding="utf-8") as f:
        f.write(s + "\n")


def khoa(viec):
    n = datetime.datetime.utcnow()
    KHOA.write_text("\t".join([SID, BD.strftime("%Y-%m-%dT%H:%M:%SZ"), (n + datetime.timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                               "native #387 B PR #1414 luot 2: " + viec, n.strftime("%Y-%m-%dT%H:%M:%SZ")]), encoding="utf-8")


def git(cwd, *a):
    p = subprocess.run(["git", "-C", str(cwd), *a], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def chay(nhan, cwd, args, timeout=7200):
    khoa(nhan)
    t0 = time.monotonic(); a = now()
    p = subprocess.run([sys.executable, "-X", "utf8", "-B", *args], cwd=str(cwd), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=ENV, timeout=timeout)
    b = now(); dt = round(time.monotonic() - t0, 1)
    (OUT / f"{nhan}.stdout.txt").write_text(p.stdout, encoding="utf-8")
    (OUT / f"{nhan}.stderr.txt").write_text(p.stderr, encoding="utf-8")
    return p, a, b, dt


def dung(cay, sha, ten):
    rc, _, e = git(SRC, "clone", "-q", "--no-checkout", str(SRC), str(cay))
    if rc: raise RuntimeError(f"clone {ten}: {e}")
    git(cay, "remote", "set-url", "origin", GH)
    git(cay, "config", "core.abbrev", "7")
    rc, _, e = git(cay, "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", sha)
    if rc: raise RuntimeError(f"checkout {ten}: {e}")
    h = git(cay, "rev-parse", "HEAD")[1]; t = git(cay, "rev-parse", "HEAD^{tree}")[1]; s = git(cay, "status", "--porcelain")[1]
    ghi(f"CHOT {ten} sha={h} tree={t} sach=[{s}]")
    if h != sha or s != "": raise RuntimeError(f"{ten} khong khop")
    return t


def bo_qua(txt):
    return sorted(set(re.findall(r"^  BO QUA (\S+?):", txt, re.M)))


def loc_ban_sao(test):
    src = test.read_text(encoding="utf-8")
    mod = ast.parse(src)
    lines = src.splitlines(keepends=True)
    thay = []
    dem = {}
    for node in mod.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in ("DOT_BIEN", "DOT_BIEN_HOOK", "DOT_BIEN_HARNESS"):
            ten = node.targets[0].id
            if ten == "DOT_BIEN_HOOK":
                moi = "DOT_BIEN_HOOK = []\n"; dem[ten] = []
            else:
                giu = [e for e in node.value.elts if isinstance(e.elts[0], ast.Constant) and str(e.elts[0].value).startswith("r387_")]
                dem[ten] = [e.elts[0].value for e in giu]
                moi = f"{ten} = [\n" + "".join("    " + ast.get_source_segment(src, e) + ",\n" for e in giu) + "]\n"
            thay.append((node.lineno, node.end_lineno, moi))
    for a, b, moi in sorted(thay, reverse=True):
        lines[a - 1:b] = [moi]
    out = "".join(lines)
    test.write_text(out, encoding="utf-8")
    return out, dem


def main():
    khoa("chuan bi")
    ghi(f"bat_dau={now()} python={sys.version.split()[0]} platform={platform.platform()} exe={sys.executable}")
    for ref in ("agent/wp387-r2-g1-claude", "master"):
        rc, _, e = git(SRC, "fetch", "-q", "origin", f"+refs/heads/{ref}:refs/remotes/origin/{ref}")
        ghi(f"fetch {ref} rc={rc} {e[:200]}")
    th = dung(H, HEAD, "HEAD")
    if th != HTREE: raise RuntimeError("tree head khong khop")
    # L1 tung ca
    l1_ok = 0
    for c in L1:
        p, a, b, dt = chay(f"L1-{c}", H, [".claude/dev/launcher_test.py", "--lap-ca", c, "--lan", "1"])
        m = re.search(r"^LAP .*$", p.stdout, re.M)
        ok = p.returncode == 0 and m and "1/1 qua, 0 bo qua, 0 hong" in m.group(0)
        l1_ok += bool(ok)
        hong = re.findall(r"^\s*HONG .*$", p.stdout, re.M)[:1]
        ghi(f"L1 {c} rc={p.returncode} {dt}s [{a}->{b}] {m.group(0) if m else 'KHONG CO DONG LAP'} {'DAT' if ok else 'DO'} {hong}")
    ghi(f"L1 TONG {l1_ok}/{len(L1)}")
    # L3
    for c in ("r387_m1_chau_ghi_muon_khai_pham_vi_bam", "r387_m2_chau_ghi_trong_han_thi_bam_du"):
        p, a, b, dt = chay(f"L3-{c}", H, [".claude/dev/launcher_test.py", "--lap-ca", c, "--lan", "5"])
        m = re.search(r"^LAP .*$", p.stdout, re.M)
        ok = p.returncode == 0 and m and "5/5 qua, 0 bo qua, 0 hong" in m.group(0)
        ghi(f"L3 {c} rc={p.returncode} {dt}s [{a}->{b}] {m.group(0) if m else 'KHONG CO DONG LAP'} {'DAT' if ok else 'DO'}")
    # N5
    rr = W / f"n5-rr-{TS}"
    p, a, b, dt = chay("N5", H, [".claude/dev/launcher.py", "run", "--run-root", str(rr), "--name", "n5", "--json", "--",
                                 sys.executable, "-c", "import time;time.sleep(2);print(1)"])
    rj = list(rr.rglob("run.json"))
    ghi(f"N5 rc={p.returncode} {dt}s [{a}->{b}] run.json={[str(x) for x in rj]}")
    if rj:
        d = json.loads(rj[0].read_text(encoding="utf-8"))
        shutil.copy2(rj[0], OUT / "N5-run.json")
        k = {x: d.get(x) for x in ("version", "ma_thoat", "job_windows", "log_bam_cay_da_chet", "log_bam_cho_giay", "log_bam_luc_utc", "ket_thuc_utc")}
        ok = (k["version"] == "1.6.2" and k["ma_thoat"] == 0 and k["job_windows"] is True and k["log_bam_cay_da_chet"] is True
              and isinstance(k["log_bam_cho_giay"], (int, float)) and k["log_bam_cho_giay"] < 10)
        ghi(f"N5 khoa={json.dumps(k)} {'DAT' if ok else 'DO'}")
    # L2
    khoa("L2 dung ban sao")
    tar = subprocess.run(["git", "-C", str(H), "archive", "--format=tar", HEAD], capture_output=True).stdout
    M.mkdir()
    with tarfile.open(fileobj=io.BytesIO(tar)) as tf:
        tf.extractall(M)
    test = M / ".claude/dev/launcher_test.py"
    out, dem = loc_ban_sao(test)
    py_compile.compile(str(test), cfile=str(OUT / "loc.pyc"), doraise=True)
    sha = hashlib.sha256(test.read_bytes()).hexdigest()
    lens = {k: len(v) for k, v in dem.items()}
    ids = dem["DOT_BIEN"] + dem["DOT_BIEN_HARNESS"]
    moc = ("\nDOT_BIEN_HARNESS = [" in out, out.count("\n]\n\n\ndef chay_dot_bien()"))
    ghi(f"L2 loc sha256={sha} len={lens} trung={len(ids) - len(set(ids))} tong={len(ids)} moc={moc}")
    ghi(f"L2 W co mat={all(x in dem['DOT_BIEN'] for x in W_IDS)} H co mat={all(x in dem['DOT_BIEN_HARNESS'] for x in H_IDS)}")
    if lens != {"DOT_BIEN": 22, "DOT_BIEN_HOOK": 0, "DOT_BIEN_HARNESS": 9} or len(set(ids)) != 31 or moc != (True, 1):
        ghi("L2 LOC KHONG DAT - khong chay dot bien")
    else:
        p, a, b, dt = chay("L2-dot-bien", M, [".claude/dev/launcher_test.py", "--dot-bien"])
        ghi(f"L2 dot-bien rc={p.returncode} {dt}s [{a}->{b}]")
        for ln in p.stdout.splitlines():
            if "r387_" in ln or "DOT BIEN" in ln or " SAI" in ln:
                ghi("  " + ln.rstrip())
    # nhan W5, W7
    src = test.read_text(encoding="utf-8")
    mod = ast.parse(src)
    cap = {}
    for node in mod.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "DOT_BIEN":
            for e in node.value.elts:
                if e.elts[0].value in ("r387_b_windows_xoa_prompt_khi_job_rong", "r387_ket_thuc_sau_vong_cho"):
                    cap[e.elts[0].value] = (ast.literal_eval(e.elts[1]), ast.literal_eval(e.elts[2])[0])
    la = M / ".claude/dev/launcher.py"
    goc = la.read_text(encoding="utf-8")
    for ten, ((tim, thay), dich) in cap.items():
        n = goc.count(tim)
        la.write_text(goc.replace(tim, thay, 1), encoding="utf-8")
        shutil.rmtree(M / ".claude/dev/__pycache__", ignore_errors=True)
        try:
            p, a, b, dt = chay(f"NHAN-{ten}", M, [".claude/dev/launcher_test.py", "--lap-ca", dich, "--lan", "1"])
        finally:
            la.write_text(goc, encoding="utf-8")
        hong = re.findall(r"^\s*HONG .*$", p.stdout, re.M)
        ghi(f"NHAN {ten} khop={n} dich={dich} rc={p.returncode} so_HONG={len(hong)} dong={hong[:1]}")
    # suite head roi base
    kq = {}
    kq["BASE"] = bo_qua(BASE_LOG.read_text(encoding="utf-8"))
    ghi(f"SUITE BASE dung lai log luot 1 {BASE_LOG} bo_qua={len(kq['BASE'])}")
    for ten, cay in (("HEAD", H),):
        p, a, b, dt = chay(f"SUITE-{ten}", cay, [".claude/dev/launcher_test.py"])
        ghi("  HONG: " + " ".join(re.findall(r"^\s*HONG (\S+?):", p.stdout, re.M)))
        cuoi = [x for x in p.stdout.splitlines() if "ca DA CHAY QUA" in x or "tong " in x][-1:]
        kq[ten] = bo_qua(p.stdout)
        ghi(f"SUITE {ten} rc={p.returncode} {dt}s [{a}->{b}] {cuoi} bo_qua={len(kq[ten])}")
        ghi(f"  dong BO QUA r387 = {len(re.findall(r'^  BO QUA r387', p.stdout, re.M))}")
    hieu = sorted(set(kq["BASE"]) - set(kq["HEAD"])); them = sorted(set(kq["HEAD"]) - set(kq["BASE"]))
    ghi(f"SUITE base-head={hieu}")
    ghi(f"SUITE head-base={them}")
    ghi(f"SUITE hieu==9 r387: {hieu == sorted(R387_9) and them == []}")


try:
    main()
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"TONG {round((datetime.datetime.utcnow() - BD).total_seconds(), 1)}s ket_thuc={now()}")
    KHOA.write_text("", encoding="utf-8")
    ghi("XONG (khoa da nha)")
