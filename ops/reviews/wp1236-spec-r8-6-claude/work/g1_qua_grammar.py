"""Phân loại 26 + 26 biến thể shell của reviewer generation 1 (g1/rv-a1-8/work/probes.py, g1/rv-a1-9/work/extra_shell_probes.py)
bằng cài đặt tham chiếu K7-S. Chỉ đọc danh sách `cases` qua ast, không chạy script gốc. Chạy từ gốc kho bằng python3 -I."""
import ast, json, os, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from gram import cu_phap_run
CMD = "python .claude/dev/packet_loop_test.py"; PIPE = CMD + " | cat"
out, hong = {}, 0
for f in ("g1/rv-a1-8/work/probes.py", "g1/rv-a1-9/work/extra_shell_probes.py"):
    cs = next(eval(compile(ast.Expression(n.value), f, "eval"), {"CMD": CMD, "PIPE": PIPE})
              for n in ast.walk(ast.parse(open(os.path.join(D, f), encoding="utf-8").read()))
              if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "cases")
    hang = [(c[0], c[1], cu_phap_run(c[2] + "\n", c[1])) if "rv-a1-8" in f else (c[0], c[2], cu_phap_run(c[1] + "\n", c[2])) for c in cs]
    out[f] = hang; nhan = [h[0] for h in hang if h[2] is None]; hong += len(nhan)
    print(f, len(hang), "bi tu choi:", len(hang) - len(nhan), "nhan:", nhan)
json.dump(out, open(os.path.join(D, "g1_probes_qua_grammar.json"), "w"), ensure_ascii=False, indent=1)
sys.exit(1 if hong else 0)
