"""Đếm neo _DB/_TU_KIEM của các fragment wp433 trên tl_gws base vs candidate; chạy run() từng fragment trên candidate."""
import importlib.util, io, contextlib, sys, os

goc, cand = sys.argv[1], sys.argv[2]   # hai thư mục kho
FR = ["wp433_gws_cred_dich_ngoai_kho", "wp433_gws_cred_dich_ngoai_kho_b", "wp433_nlm_gws_dich_ngoai_kho",
      "wp433_gws_cred_win_duong", "wp433_gws_cred_win_reparse"]


def nap(kho, ten):
    spec = importlib.util.spec_from_file_location(ten + "_" + str(abs(hash(kho))), os.path.join(kho, "scripts/test_fragments", ten + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


src = {k: open(os.path.join(k, "scripts/tl_gws.py"), encoding="utf-8").read() for k in (goc, cand)}
for ten in FR:
    m = nap(cand, ten)
    neo = []
    for bang in ("_DB", "_TU_KIEM"):
        for muc in getattr(m, bang, ()):
            for cap in muc[1]:
                neo.append(cap[0])
    lech = [(n[:60], src[goc].count(n), src[cand].count(n)) for n in dict.fromkeys(neo) if src[goc].count(n) != src[cand].count(n)]
    print(ten, "so_neo", len(neo), "chuoi", len(set(neo)), "lech", lech)
