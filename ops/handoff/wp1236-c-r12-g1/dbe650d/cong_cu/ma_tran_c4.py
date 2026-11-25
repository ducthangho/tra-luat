"""Ma tran (dot bien x bien the) cua ca cong_d2b_c4_symlink: voi tung dot bien, chay RIENG tung bien the va in bien the nao lech ky vong.
Cong cu nhap cua executor de kiem moi bien the co rang rieng (ca chay that dung o bien the lech DAU TIEN nen khong cho thay dieu nay).
dung: ma_tran_c4.py <goc kho> [tien to dot bien...]"""
import sys, tempfile, warnings
from pathlib import Path

warnings.simplefilter("ignore")
goc = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(goc / ".claude/dev"))
import packet_loop_test as T  # noqa: E402

CA = "cong_d2b_c4_symlink"
o = T._D2B_CA[CA].__closure__
bien_the, kho = next(x.cell_contents for x in o if isinstance(x.cell_contents, tuple)), next(x.cell_contents for x in o if isinstance(x.cell_contents, dict))
bien_the = (("doi_chung_dat", None, 0, [], "tep"), *bien_the)
nguon = T.CANONICAL.read_text(encoding="utf-8")
chon = sys.argv[2:]
ds = [("(goc)", None)] + [(k, v) for k, v in T.MUTANTS.items() if CA in v[2] and (not chon or any(k.startswith(c) for c in chon))]
print(f"{len(bien_the)} bien the · {len(ds) - 1} dot bien")
with tempfile.TemporaryDirectory() as td:
    for i, (ten, mut) in enumerate(ds):
        d = Path(td) / f"m{i}"
        d.mkdir()
        if mut:
            assert nguon.count(mut[0]) == 1, ten
        (d / "packet_loop.py").write_text(nguon.replace(mut[0], mut[1]) if mut else nguon, encoding="utf-8", newline="\n")
        (d / "launcher.py").write_text((goc / ".claude/dev/launcher.py").read_text(encoding="utf-8"), encoding="utf-8")
        (d / "t").mkdir()
        c = T.Ctx(d / "packet_loop.py", d / "t")
        c.b4 = CA
        x = T._d1106_kho(c, **kho)
        lech = []
        for b in bien_the:
            try:
                T._d2b_do(c, x, *b[:5], **(b[5] if len(b) > 5 else {}))
            except Exception as ex:
                lech.append(f"{b[0]} [{type(ex).__name__}]")
        print(f"{ten}: {len(lech)} lech :: " + " · ".join(lech))
