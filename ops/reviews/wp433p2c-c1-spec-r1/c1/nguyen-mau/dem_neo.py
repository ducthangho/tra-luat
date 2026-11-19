import runpy, sys, collections
src = open("scripts/tl_gws.py", encoding="utf-8").read()
for f in ("scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py", "scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py"):
    g = runpy.run_path(f, run_name="frag")
    c = collections.Counter()
    for bang in ("_DB", "_TU_KIEM"):
        for muc in g.get(bang, ()):
            for neo, _ in muc[1]:
                c[(bang, muc[0], src.count(neo))] += 1
    tom = collections.Counter((b, n) for (b, _, n) in c)
    print(f, dict(tom), [k for k in c if k[2] != 1])
