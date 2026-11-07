import importlib.util, sys
from pathlib import Path
R = Path(sys.argv[1])
s = importlib.util.spec_from_file_location("t", R / "ops/gate_output_doi_chieu_test.py"); t = importlib.util.module_from_spec(s); s.loader.exec_module(t)
m = t.nap(); text, p = t.f_ok()
print("goc            ", m.kiem(text, p, t.goc()))
a = "== gen_instructions selftest 44/44 =="
print("co dong 44/44  ", a in text)
print("0/0            ", m.kiem(text.replace(a, "== gen_instructions selftest 0/0 =="), p, t.goc()))
print("RE_PIPEFAIL sau ong:", bool(m.RE_PIPEFAIL.search("python x.py | cat\nset -o pipefail\n")), "ong:", bool(m.RE_ONG.search("python x.py | cat")))
