"""Chay tap con ca + dot bien cua packet_loop_test.py (cong cu nhap cua executor, KHONG phai gate).
dung: chay_ca.py <goc kho> ca <tien to|ten>...        -> nen
      chay_ca.py <goc kho> db <tien to ten dot bien>... -> moi dot bien khop: ap len ban sao, chay ca dich + doi chung
"""
import hashlib, sys, tempfile, time
from pathlib import Path

goc_kho = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(goc_kho / ".claude/dev"))
import packet_loop_test as T  # noqa: E402

che_do, chon = sys.argv[2], sys.argv[3:]
khop = lambda ten: any(ten == c or ten.startswith(c) for c in chon)  # noqa: E731
rc = 0
with tempfile.TemporaryDirectory(prefix="plt_") as td:
    tmp = Path(td)
    if che_do == "ca":
        ten = {t for t, _ in T.CASES if khop(t)}
        t0 = time.time()
        ket = T.chay_suite(T.CANONICAL, tmp / "nen", chi_chay=ten)
        for k, v in ket.items():
            if v is not None:
                rc = 1
                print("DO ", k, "::", T._phan_loai_giet(v), str(v)[:1500])
        print(f"nen: {sum(v is None for v in ket.values())}/{len(ket)} dat ({time.time() - t0:.1f}s)")
    else:
        goc = T.CANONICAL.read_text(encoding="utf-8")
        goc_test = Path(T.__file__).read_text(encoding="utf-8")
        n = 0
        for ten_mut, (tim, thay, phai_chet) in T.MUTANTS.items():
            if not khop(ten_mut):
                continue
            n += 1
            cap = T._cap_thay_the(tim, thay)
            than, dot_bien_test, thieu = T._phan_loai_dot_bien(ten_mut, cap, goc, goc_test)
            if thieu or dot_bien_test:
                rc = 1
                print("DO  mo neo/test-mutant", ten_mut, thieu)
                continue
            d = tmp / ("mut_" + hashlib.sha256(ten_mut.encode()).hexdigest()[:16])
            d.mkdir()
            for t, th in cap:
                than = than.replace(t, th, 1)
            (d / "packet_loop.py").write_text(than, encoding="utf-8", newline="\n")
            (d / "launcher.py").write_text((T.HERE / "launcher.py").read_text(encoding="utf-8"), encoding="utf-8")
            dc = T._doi_chung_khac_ho(phai_chet)
            ket = T.chay_suite(d / "packet_loop.py", d, chi_chay=set(phai_chet) | set(dc))
            hang = {t: T._phan_loai_giet(ket.get(t)) for t in phai_chet}
            oan = [t for t in dc if ket.get(t) is not None]
            ok = all(v == "GIET" for v in hang.values()) and not oan
            rc |= not ok
            print("ok " if ok else "DO ", ten_mut, hang, "oan=", oan, "" if ok else {t: str(ket.get(t))[:300] for t in phai_chet})
        print(f"dot bien: {n}")
sys.exit(rc)
