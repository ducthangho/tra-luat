import json, os, sys, importlib.util
sys.path.insert(0, os.getcwd())
import gram
spec = importlib.util.spec_from_file_location("dbt", os.path.join(os.getcwd(), "..", "dot_bien_them_v2.py"))
g1 = json.load(open("g1_probes_qua_grammar.json"))
ves = []
for f, hang in g1.items():
    for h in hang: pass
# lấy lại thân thật: dựng như g1_qua_grammar
import ast
CMD = "python .claude/dev/packet_loop_test.py"; PIPE = CMD + " | cat"
for f in ("g1/rv-a1-8/work/probes.py", "g1/rv-a1-9/work/extra_shell_probes.py"):
    cs = next(eval(compile(ast.Expression(n.value), f, "eval"), {"CMD": CMD, "PIPE": PIPE})
              for n in ast.walk(ast.parse(open(f, encoding="utf-8").read()))
              if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "cases")
    for c in cs:
        ves.append((c[0], c[2] + "\n", c[1]) if "rv-a1-8" in f else (c[0], c[1] + "\n", c[2]))
print(len(ves))
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for ten, (fn, moi) in m.DB.items():
    doi = [v[0] for v in ves if fn(v[1], v[2]) != gram.cu_phap_run(v[1], v[2])]
    if doi or not ten.startswith("yP"): print(ten, "g1 doi ly do:", doi)
for v in ves:
    if "||" in v[1] or "&" in v[1] or v[1].lstrip().startswith("!"): print(repr(v[0]), repr(v[1][:90]), v[2])
