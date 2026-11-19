"""Chay lai toan suite BASE 3b64746 khi Developer Mode bat (cung dieu kien voi head luot 2 9804f64)."""
import datetime, os, re, subprocess, sys
from pathlib import Path

SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
W = Path(sys.argv[1])
BASE = "3b647461db7c8ded1bddd9aafc5c6aa5eead223f"
SRC = W / "wp1342-src"
TS = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
OUT = W / f"wp387b3-out-{TS}"; OUT.mkdir()
B = W / f"r387b-{TS}"
HEAD_LOG = W / "wp387b2-out-20261119T074702Z" / "SUITE-HEAD.stdout.txt"
KHOA = Path(r"F:\tl-win\KHOA.txt")
TT = OUT / "TOM-TAT.txt"
TMP = W / "tmp387"; TMP.mkdir(exist_ok=True)
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP))
ENV.pop("PYTHONUTF8", None)
R387_9 = sorted(["r387_m1_chau_ghi_muon_khai_pham_vi_bam", "r387_m1_doi_chung_ghi_som_lam_ve_bam_do",
                 "r387_m1_con_thuong_chung_minh_cay_chet", "r387_m2_chau_ghi_trong_han_thi_bam_du",
                 "r387_m2_khong_do_duoc_thi_khong_cho", "r387_a_nen_khac_giu_moc_ket_thuc_base",
                 "r387_m1_stop_trong_luc_cho_khong_bi_de", "r387_m1_prompt_linux_xoa_khi_cay_chet",
                 "r387_m2_ngat_trong_luc_doi_ghi_bi_ngat"])


def now():
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def ghi(s):
    with open(TT, "a", encoding="utf-8") as f:
        f.write(s + "\n")


def git(cwd, *a):
    p = subprocess.run(["git", "-C", str(cwd), *a], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def bo_qua(t):
    return sorted(set(re.findall(r"^  BO QUA (\S+?):", t, re.M)))


def hong(t):
    return sorted(set(re.findall(r"^\s*HONG (\S+?):", t, re.M)))


try:
    n = datetime.datetime.now(datetime.UTC)
    KHOA.write_text("\t".join([SID, now(), (n + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                               "native #387 B PR #1414 luot 3: suite base khi Developer Mode bat", now()]), encoding="utf-8")
    import winreg
    k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock")
    ghi(f"bat_dau={now()} devmode={winreg.QueryValueEx(k, 'AllowDevelopmentWithoutDevLicense')[0]}")
    rc, _, e = git(SRC, "clone", "-q", "--no-checkout", str(SRC), str(B))
    git(B, "remote", "set-url", "origin", "https://github.com/ducthangho/tra-luat.git")
    git(B, "config", "core.abbrev", "7")
    git(B, "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", BASE)
    h = git(B, "rev-parse", "HEAD")[1]; s = git(B, "status", "--porcelain")[1]
    ghi(f"CHOT BASE sha={h} sach=[{s}]")
    if h != BASE or s: raise RuntimeError("base khong khop")
    a = now()
    p = subprocess.run([sys.executable, "-X", "utf8", "-B", ".claude/dev/launcher_test.py"], cwd=str(B), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=ENV, timeout=7200)
    (OUT / "SUITE-BASE.stdout.txt").write_text(p.stdout, encoding="utf-8")
    (OUT / "SUITE-BASE.stderr.txt").write_text(p.stderr, encoding="utf-8")
    cuoi = [x for x in p.stdout.splitlines() if "ca DA CHAY QUA" in x][-1:]
    hl = HEAD_LOG.read_text(encoding="utf-8")
    bb, bh = bo_qua(p.stdout), bo_qua(hl)
    ghi(f"SUITE BASE rc={p.returncode} [{a}->{now()}] {cuoi} bo_qua={len(bb)}")
    ghi(f"HONG base={hong(p.stdout)}")
    ghi(f"HONG head(luot2)={hong(hl)}")
    ghi(f"HONG bang nhau={hong(p.stdout) == hong(hl)}")
    ghi(f"base-head={sorted(set(bb) - set(bh))}")
    ghi(f"head-base={sorted(set(bh) - set(bb))}")
    ghi(f"hieu==9 r387: {sorted(set(bb) - set(bh)) == R387_9 and not (set(bh) - set(bb))}")
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"ket_thuc={now()}")
    KHOA.write_text("", encoding="utf-8")
    ghi("XONG (khoa da nha)")
