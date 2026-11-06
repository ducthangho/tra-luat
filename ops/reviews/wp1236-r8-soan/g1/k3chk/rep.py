import copy, importlib.util, sys, yaml
from pathlib import Path
R = Path(sys.argv[1])
s = importlib.util.spec_from_file_location("t", R / "ops/gate_output_doi_chieu_test.py"); t = importlib.util.module_from_spec(s); s.loader.exec_module(t)
text, p = t.f_ok()
cay = {"merge_commit": t.SHA_CK, "pmc": t.neo_map()}
print("A: chi attempt 1      ", t.ho_so(cay))
q = copy.deepcopy(p); q["attempt_yeu_cau"] = 2
tep = {"provenance.yaml": yaml.safe_dump(p, allow_unicode=True), "provenance-a2.yaml": yaml.safe_dump(q, allow_unicode=True), t.GO2: text}
print("B: them provenance a2 ", t.ho_so(cay, tep=tep))
