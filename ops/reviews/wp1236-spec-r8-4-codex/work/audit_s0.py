"""Read-only specification audit. Mutants and harmless witnesses stay in work/."""
import ast
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "author"))
import gram
import probes_r8
import sinh_r8

source = (HERE / "author/gram.py").read_text()
canonical_node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == "cu_phap_run")
anchor = '    b = run[:-1] if run.endswith("\\n") else run\n'
assert source.count(anchor) == 1
sources = {
    "remove_initial_bom": source.replace(anchor, anchor + '    b = b.removeprefix("\\ufeff")\n'),
    "lowercase_initial_letter": source.replace(anchor, anchor + '    b = b[:1].lower() + b[1:]\n'),
    "ong_match_control": source.replace('RE_ONG.fullmatch(b)', 'RE_ONG.match(b)'),
}
g1 = []
cmd = "python .claude/dev/packet_loop_test.py"
for name in ("g1/rv-a1-8/work/probes.py", "g1/rv-a1-9/work/extra_shell_probes.py"):
    tree = ast.parse((HERE / "author" / name).read_text())
    value = next(n.value for n in ast.walk(tree) if isinstance(n, ast.Assign)
                 and getattr(n.targets[0], "id", None) == "cases")
    rows = eval(compile(ast.Expression(value), name, "eval"), {"CMD": cmd, "PIPE": cmd + " | cat"})
    g1.extend((c[2] + "\n", c[1]) if "rv-a1-8" in name else (c[1] + "\n", c[2]) for c in rows)
table = list(probes_r8.AM.values()) + list(probes_r8.DUONG.values()) + g1
corpus = [(run, sh) for body in sinh_r8.kho() for sh in sinh_r8.SHELL for run in (body, body + "\n")]
out = {}
for name, src in sources.items():
    (HERE / (name + ".py")).write_text(src)
    ns = {}
    exec(compile(src, name, "exec"), ns)
    fn = ns["cu_phap_run"]
    node = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "cu_phap_run")
    regex_refs = sorted({n.id for n in ast.walk(node) if isinstance(n, ast.Name) and n.id.startswith("RE_")})
    calls = [ast.unparse(n.func) for n in ast.walk(node) if isinstance(n, ast.Call)]
    constants = all(ns[k] == getattr(gram, k) for k in ("P", "W", "DANG", "LENH"))
    patterns = all(ns[k].pattern == getattr(gram, k).pattern and ns[k].flags == re.compile("", re.ASCII).flags
                   for k in ("RE_DON", "RE_ONG"))
    third_regex = [c for c in calls if c.startswith("re.")]
    row = {"six_constants_and_flags": constants and patterns, "regex_refs": regex_refs,
           "canonical_function_ast_equal": ast.dump(node, include_attributes=False) == ast.dump(canonical_node, include_attributes=False),
           "third_regex_calls": third_regex, "regex_calls": [c for c in calls if c.startswith("RE_")],
           "table_cases": len(table), "table_diff": sum(fn(r, s) != gram.cp(r, s) for r, s in table),
           "generated_cases": len(corpus), "generated_diff": sum(fn(r, s) != gram.cp(r, s) for r, s in corpus)}
    if name != "ong_match_control":
        run = ("\ufeffpython" if name == "remove_initial_bom" else "Python") + " ops/x.py"
        row["harmless_witness"] = {"run": run, "reference": gram.cp(run, None), "mutant": fn(run, None)}
    out[name] = row
print(json.dumps(out, ensure_ascii=True, indent=2))
(HERE / "audit_s0.json").write_text(json.dumps(out, ensure_ascii=True, indent=2) + "\n")
