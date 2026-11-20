import contextlib, importlib.util, io, sys
sys.path.insert(0, "scripts"); import tl  # noqa
for ten in ["wp433_gws_cred_dich_ngoai_kho", "wp433_gws_cred_dich_ngoai_kho_b", "wp433_nlm_gws_dich_ngoai_kho", "wp433_gws_cred_win_duong", "wp433_gws_cred_win_reparse"]:
    s = importlib.util.spec_from_file_location(ten, "scripts/test_fragments/%s.py" % ten); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    err, out = io.StringIO(), io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
        r = m.run(tl)
    print(ten, r, "stdout_len", len(out.getvalue()), "|", " ".join(l for l in err.getvalue().splitlines() if "ĐỎ" in l or "CA" in l or "BIẾN" in l or "BIEN" in l)[:300])
