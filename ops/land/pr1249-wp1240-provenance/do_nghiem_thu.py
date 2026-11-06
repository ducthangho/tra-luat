"""Do lai A1–A11 cua ops/specs/assurance-81-model-effort-tuy-chon-r1.md tren BLOB MERGE — phien ghi so #1240 (PR #1249).

Chay tu goc kho (can ruff): python3 ops/land/pr1249-wp1240-provenance/do_nghiem_thu.py <merge_sha>
Moi tieu chi: ve DUONG tren cay merge (git archive ra thu muc tam) + ve AM bang dot bien tren BAN SAO tam,
kem ve NEN (cha mot cua merge) khi dac ta noi "Tren nen". Khong ghi gi vao checkout.
A7 do tren cay merge (= origin/master luc do), A10 selftest chay trong ban sao tam (khong trong checkout).
"""
import hashlib, importlib.util, io, json, re, shutil, subprocess, sys, tarfile, tempfile, unicodedata
from pathlib import Path

SPEC = "ops/specs/assurance-81-model-effort-tuy-chon-r1.md"
ADR = "docs/adr/0065-model-effort-phuc-vu-tuy-chon.md"
PROTO = "docs/PROTOCOL_DA_PHIEN.md"
KQ = []


def git(*a, cwd="."):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, check=True).stdout


def xuat(sha, dich):
    tarfile.open(fileobj=io.BytesIO(git("archive", sha)), mode="r:").extractall(dich, filter="data")
    return Path(dich)


def chay(lenh, cwd):
    p = subprocess.run(lenh, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def ghi(ma, ok, chi_tiet):
    KQ.append((ma, ok, chi_tiet))
    print(f"{ma}: {'DAT' if ok else 'DO'} — {chi_tiet}")


def doan_noi(txt):
    """Gop khoang trang trong tung doan; khong noi qua dong trong (L6 b)."""
    return [re.sub(r"\s+", " ", d).strip() for d in re.split(r"\n\s*\n", unicodedata.normalize("NFC", txt))]


def muc_81(txt):
    i = txt.index("### 8.1"); j = txt.index("### 8.2", i)
    return txt[i:j]


def dem(doan, cum, bo_nhay=False):
    return sum((d.replace("`", "") if bo_nhay else d).count(cum) for d in doan)


A2_CUM = ("model và effort phục vụ của reviewer là trường ghi nếu đo được",
          "KHONG_DO_DUOC ở hai trường này không làm assurance thành CHUA_DAT",
          "exact SHA, ma_thoat, stdout_sha256, verdict và sandbox mode")
A3_CUM = ("Nếu Packet đòi reviewer cùng model nhưng effort cao hơn",
          "Evidence fallback hoặc không đủ nhận dạng thì chưa nhận assurance")
A11_CUM = ("ghi nếu đo được", "không chặn landed", "sandbox mode", "identity provider", "hồi tố", "launcher")
TOKEN_A9 = re.compile(r"os\.name|sys\.platform|platform\.system|subprocess|encoding=|os\.sep|pathlib")


def nap_cong(goc):
    spec = importlib.util.spec_from_file_location("len_tam", goc / "ops/land_evidence_nguon.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def l7(mod, thuc_thi_yaml, a81="DAT"):
    """Ho so tam: tra danh sach vi pham L7 cua kiem_ho_so tren dung ham cua cay dang do."""
    import yaml
    with tempfile.TemporaryDirectory() as t:
        g = Path(t); land = g / "ops/land"; prov = land / "pr9999-wpx-provenance"; prov.mkdir(parents=True)
        (prov / "run.json").write_text("{}")
        tep = land / "pr9999-wpx-land-evidence.yaml"
        b = f"assurance_81:\n  reviewer_assurance_81: {a81}\n  thuc_thi:\n{thuc_thi_yaml}".encode()
        tep.write_bytes(b)
        vp, _ = mod.kiem_ho_so(tep, b, g, yaml)
        return [v for v in vp if v.startswith("L7")]


def dot_bien_tep(goc, rel, cu, moi):
    p = goc / rel; s = p.read_text(encoding="utf-8")
    assert s.count(cu) == 1, f"chuoi goc dot bien xuat hien {s.count(cu)} lan trong {rel}: {cu!r}"
    p.write_text(s.replace(cu, moi), encoding="utf-8")


def main():
    sha = sys.argv[1]
    cha = git("rev-parse", f"{sha}^1").decode().strip()
    tam = Path(tempfile.mkdtemp(prefix="nt1240-"))
    # M: CLONE tai merge SHA (selftest/doctrine-scan doc lich su git); N: git archive cua cha mot (chi doc van ban/ma)
    subprocess.run(["git", "clone", "-q", "--no-checkout", str(Path(".").resolve()), str(tam / "m")], check=True)
    M = tam / "m"; git("checkout", "-q", "--detach", sha, cwd=M); git("config", "core.abbrev", "7", cwd=M)
    git("fetch", "-q", "origin", "+refs/remotes/origin/master:refs/remotes/origin/master", cwd=M)
    N = xuat(cha, tam / "nen")
    print(f"merge {sha} · nen (cha mot) {cha} · spec sha256 {hashlib.sha256((M / SPEC).read_bytes()).hexdigest()}")

    # A1
    rc, out = chay([sys.executable, ".claude/dev/packet_loop.py", "adr-song", "--root", "."], M)
    so = len(re.findall(r"^\| `ADR-0065`", (M / PROTO).read_text(encoding="utf-8"), re.M))
    so_nen = len(re.findall(r"^\| `ADR-0065`", (N / PROTO).read_text(encoding="utf-8"), re.M))
    D = tam / "a1"; shutil.copytree(M, D)
    t = (D / PROTO).read_text(encoding="utf-8"); dong = [l for l in t.splitlines(True) if l.startswith("| `ADR-0065`")]
    (D / PROTO).write_text(t.replace(dong[0], ""), encoding="utf-8")
    rc_db, out_db = chay([sys.executable, ".claude/dev/packet_loop.py", "adr-song", "--root", "."], D)
    ghi("A1", rc == 0 and so == 1 and so_nen == 0 and (N / ADR).exists() is False and rc_db != 0,
        f"adr-song rc {rc}; dong §20 ADR-0065 = {so} (nen {so_nen}, ADR nen ton tai {(N / ADR).exists()}); "
        f"dot bien xoa dong §20 => adr-song rc {rc_db} ({out_db.strip().splitlines()[-1][:120] if out_db.strip() else ''})")

    d81 = doan_noi(muc_81((M / PROTO).read_text(encoding="utf-8")))
    n81 = doan_noi(muc_81((N / PROTO).read_text(encoding="utf-8")))
    # A2
    duong = [dem(d81, c, True) for c in A2_CUM]; nen = [dem(n81, c, True) for c in A2_CUM]
    db = doan_noi(muc_81((M / PROTO).read_text(encoding="utf-8")).replace("ghi nếu đo được", "bắt buộc"))
    am = dem(db, A2_CUM[0], True)
    ghi("A2", duong == [1, 1, 1] and nen == [0, 0, 0] and am == 0,
        f"merge {duong} · nen {nen} · dot bien 'ghi nếu đo được'->'bắt buộc' cum 1 = {am}")
    # A3
    duong3 = [dem(d81, c) for c in A3_CUM]; nen3 = [dem(n81, c) for c in A3_CUM]
    ghi("A3", duong3 == [0, 0] and nen3 == [1, 1],
        f"merge {duong3} · nen {nen3} (nen = 1,1 la mau 'chua lam'; A2 chan duong xoa trang)")

    mm, mn = nap_cong(M), nap_cong(N)
    SB = '    sandbox_mode: "measured — run.json"\n'
    KD = '    model: "not_measured — khong co"\n    effort: "not_measured — khong co"\n'
    # dot bien m1/m2/m3 tren ban sao cay merge
    def cong_dot_bien(ten, cu, moi):
        D = tam / ten; shutil.copytree(M / "ops", D / "ops")
        dot_bien_tep(D, "ops/land_evidence_nguon.py", cu, moi); return nap_cong(D)
    m1 = cong_dot_bien("m1", 'L7_KHOA = ("sandbox_mode",)', 'L7_KHOA = ("model", "effort", "sandbox_mode")')
    m2 = cong_dot_bien("m2", 'L7_KHOA = ("sandbox_mode",)', 'L7_KHOA = ()')
    m3 = cong_dot_bien("m3", "for k in L7_KHOA_TUY_CHON if k in tt7 and not _khai_tuy_chon(tt7[k])]",
                       "for k in L7_KHOA_TUY_CHON if False]")
    # A4
    a, b, c = l7(mm, SB + KD), l7(mn, SB + KD), l7(m1, SB + KD)
    ghi("A4", len(a) == 0 and len(b) == 2 and len(c) > 0,
        f"merge {len(a)} vi pham L7 · nen {len(b)} · m1 (bat buoc lai) {len(c)}")
    # A5
    a5a, a5a_m1 = l7(mm, SB), l7(m1, SB)
    me = '    model: "measured — run.json"\n    effort: "measured — run.json"\n'
    a5b, a5b_m2 = l7(mm, me), l7(m2, me)
    ok5 = (len(a5a) == 0 and len(a5a_m1) > 0 and len(a5b) == 1 and "thuc_thi.sandbox_mode" in a5b[0] and len(a5b_m2) == 0)
    ghi("A5", ok5, f"(a) chi sandbox: merge {len(a5a)}, m1 {len(a5a_m1)} · (b) thieu sandbox: merge {len(a5b)} "
        f"{a5b[0][:60] if a5b else ''!r}, m2 {len(a5b_m2)} (m2 lam ca (b) mat vi pham => DO)")
    # A6
    rac = [('    model: "DAT"\n', "model"), ('    effort: ""\n', "effort"), ("    model: 5\n", "model")]
    ds = [(k, len(l7(mm, SB + y)), len(l7(m3, SB + y)), [v for v in l7(mm, SB + y) if f"thuc_thi.{k}" in v]) for y, k in rac]
    ghi("A6", all(n == 1 and n3 == 0 and len(dung) == 1 for _, n, n3, dung in ds),
        "; ".join(f"{k}: merge {n} (dung khoa {len(dung)}), m3 {n3}" for k, n, n3, dung in ds))

    # A7 — tren cay merge (= master sau merge)
    rc7, out7 = chay([sys.executable, "-I", "ops/land_evidence_nguon.py", "--root", "."], M)
    rct, outt = chay([sys.executable, "-I", "ops/land_evidence_nguon_test.py"], M)
    d7 = [l for l in out7.splitlines() if l.startswith("land_evidence_nguon:")]
    dbt = re.search(r"DOT BIEN: (\d+)/(\d+)", outt); ca = re.search(r"CA: (\d+)/(\d+)", outt)
    m13 = [l for l in outt.splitlines() if re.search(r"\bm[123]_", l)]
    ok7 = (rc7 == 0 and d7 and " 0 vi phạm" in d7[-1] and rct == 0 and "TONG: DAT" in outt and dbt
           and dbt.group(1) == dbt.group(2) and int(dbt.group(1)) >= 109)
    ghi("A7", bool(ok7), f"cong rc {rc7}: {d7[-1] if d7 else '?'} · test rc {rct}: CA {ca.group(0) if ca else '?'}, "
        f"{dbt.group(0) if dbt else '?'}, TONG: DAT {'TONG: DAT' in outt}; dong m1–m3 trong output: {len(m13)}")
    (tam / "A7-cong.txt").write_text(out7); (tam / "A7-test.txt").write_text(outt)

    # A8
    blob = lambda s: git("rev-parse", f"{s}:ops/kiem_ho_so_land.py").decode().strip()
    p8 = subprocess.run(["git", "diff", "--exit-code", f"{cha}..{sha}", "--", "ops/kiem_ho_so_land.py"], capture_output=True)
    p8b = subprocess.run(["git", "diff", "--exit-code", "3163f4d02a583787a9340c63a1f5eebd3780d970..ecd30737e10cb7cdffe0e17178c28b3a12448874",
                          "--", "ops/kiem_ho_so_land.py"], capture_output=True)
    ghi("A8", p8.returncode == 0 and p8b.returncode == 0 and blob(sha) == blob(cha) == blob("3163f4d"),
        f"diff cha..merge rc {p8.returncode}; diff base 3163f4d..head ecd3073 rc {p8b.returncode}; blob merge {blob(sha)[:12]} "
        f"= cha {blob(cha)[:12]} = base {blob('3163f4d')[:12]}")
    # A9
    them = [l for l in git("diff", "-U0", f"{cha}..{sha}", "--", "*.py").decode().splitlines()
            if l.startswith("+") and not l.startswith("+++")]
    n9 = sum(1 for l in them if TOKEN_A9.search(l))
    them_db = them + ['+    p.write_text(x, encoding="utf-8")']
    ghi("A9", n9 == 0 and sum(1 for l in them_db if TOKEN_A9.search(l)) == 1,
        f"{len(them)} dong them trong *.py, token nen = {n9}; dot bien them encoding= => 1")
    # A10
    rcd, outd = chay([sys.executable, ".claude/dev/packet_loop.py", "doctrine-scan", "--root", "."], M)
    def ruff(g):
        p = subprocess.run([sys.executable, "-m", "ruff", "check", "--select", "F", "--output-format", "concise",
                            "ops/land_evidence_nguon.py", "ops/land_evidence_nguon_test.py"], cwd=g, capture_output=True, text=True)
        if p.returncode not in (0, 1) or "No module named" in p.stderr:
            raise SystemExit(f"KHONG DO DUOC ruff: rc {p.returncode} {p.stderr[:200]}")
        return len([l for l in p.stdout.splitlines() if re.match(r"\S+:\d+:\d+:", l)])
    rm, rn = ruff(M), ruff(N)
    rcs, outs = chay([sys.executable, "scripts/tl.py", "--selftest"], M)
    st = re.findall(r"^== tl selftest (\d+)/(\d+) ==$", outs, re.M)
    rcr, outr = chay([sys.executable, "scripts/tl.py", "release-verify", "RELEASE_MANIFEST.json", "--strict", "--json"], M)
    try:
        rv = json.loads(outr[outr.index("{"):]); rv_ok = rv.get("ok") is True and rv.get("strict") is True and rv.get("expected_file_count") == rv.get("checked_file_count")
        rv_s = f"ok {rv.get('ok')}, strict {rv.get('strict')}, {rv.get('checked_file_count')}/{rv.get('expected_file_count')}, failed {rv.get('failed')}"
    except Exception as e:
        rv_ok, rv_s = False, f"khong doc duoc: {e}"
    ok10 = rcd == 0 and rm == rn and rcs == 0 and st and st[-1][0] == st[-1][1] and rcr == 0 and rv_ok
    ghi("A10", bool(ok10), f"doctrine-scan rc {rcd}; ruff F merge {rm} / nen {rn} (delta {rm - rn}); selftest rc {rcs} "
        f"{'/'.join(st[-1]) if st else 'KHONG THAY dong == tl selftest N/N =='}; release-verify rc {rcr} {rv_s}")
    (tam / "A10-selftest.txt").write_text(outs); (tam / "A10-release-verify.txt").write_text(outr)
    # A11
    adr = doan_noi((M / ADR).read_text(encoding="utf-8"))
    c11 = [dem(adr, c, True) for c in A11_CUM]
    adr_db = [d for d in adr if "identity provider" not in d]
    ghi("A11", all(x >= 1 for x in c11) and dem(adr_db, "identity provider", True) == 0 and not (N / ADR).exists(),
        f"cum {dict(zip(A11_CUM, c11))}; dot bien xoa doan chua (iv) => 'identity provider' = "
        f"{dem(adr_db, 'identity provider', True)}; nen: ADR vang = {not (N / ADR).exists()}")

    print(f"TONG: {sum(o for _, o, _ in KQ)}/{len(KQ)} DAT · thu muc tam {tam}")
    return 0 if all(o for _, o, _ in KQ) else 1


if __name__ == "__main__":
    sys.exit(main())
