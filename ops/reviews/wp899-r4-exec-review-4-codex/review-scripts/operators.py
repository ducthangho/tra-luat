"""Đột biến TOÁN TỬ tự động trên các hàm r4: mỗi token một đột biến, chạy toàn bộ ca, in SONG / TIN_DUNG_GIA."""
import ast, io, json, os, re, subprocess, sys, tempfile, tokenize
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path("/tmp/claude-0/-home-user-tra-luat/eaf2a577-1c02-5642-8186-a4b48145f1ca/scratchpad/r4review4/ws"); SRC = (ROOT / "ops/ci_provenance.py").read_text()
HAM = {"_env_chan", "doc_wf", "ghep_job", "ten_du_kien", "_gio", "ghep_buoc", "chan_buoc", "tach_buoc", "do_dau_duong"}
cay = ast.parse(SRC); dong = set()
for n in cay.body:
    if isinstance(n, ast.FunctionDef) and n.name in HAM:
        dong |= set(range(n.lineno + 1, n.end_lineno + 1))   # bỏ dòng def
DOI = {"==": ["!="], "!=": ["=="], "<=": ["<"], ">=": [">"], "<": ["<="], ">": [">="], "and": ["or"], "or": ["and"],
       "is": ["is not"], "in": ["not in"], "not": [""], "True": ["False"], "False": ["True"], "any": ["all"], "all": ["any"]}
lines = SRC.splitlines(True); off = [0]
for l in lines: off.append(off[-1] + len(l))
M = []
toks = list(tokenize.generate_tokens(io.StringIO(SRC).readline))
for i, t in enumerate(toks):
    if t.start[0] not in dong or lines[t.start[0] - 1].lstrip().startswith("#"):
        continue
    if t.type == tokenize.STRING and (t.string.startswith('"""') or t.string.startswith("r'") ):
        continue
    a, b = off[t.start[0] - 1] + t.start[1], off[t.end[0] - 1] + t.end[1]
    cands = []
    if t.type in (tokenize.OP, tokenize.NAME) and t.string in DOI:
        nxt = toks[i + 1].string if i + 1 < len(toks) else ""
        if t.string == "is" and nxt == "not": cands = [("is", 2 + 1 + 3, "is")]   # `is not` -> `is`
        elif t.string == "not" and toks[i - 1].string in ("is",): continue
        elif t.string == "not" and nxt == "in": cands = [("not", 3 + 1 + 2, "in")]
        elif t.string == "in" and toks[i - 1].string == "not": continue
        else: cands = [(t.string, len(t.string), r) for r in DOI[t.string]]
    elif t.type == tokenize.NUMBER:
        v = int(t.string) if t.string.isdigit() else None
        if v is not None: cands = [(t.string, len(t.string), str(v + 1)), (t.string, len(t.string), str(max(v - 1, 0)))]
    for cu, n, moi in cands:
        m = SRC[:a] + moi + SRC[a + n:]
        try: compile(m, "x", "exec")
        except SyntaxError: continue
        if m != SRC: M.append((f"L{t.start[0]}c{t.start[1]}:{SRC[a:a+n]!r}->{moi!r}", m))
def cases(ma):
    code = ("import importlib.util as u,json;s=u.spec_from_file_location('t','/tmp/claude-0/-home-user-tra-luat/eaf2a577-1c02-5642-8186-a4b48145f1ca/scratchpad/r4review4/ws/ops/ci_provenance_test.py');"
            "t=u.module_from_spec(s);s.loader.exec_module(t);print(json.dumps([(c,)+t.chay_ca(c) for c in t.CA]))")
    r = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True,
                       env=dict(os.environ, CI_PROVENANCE_MA=str(ma), PYTHONDONTWRITEBYTECODE="1"), timeout=900)
    try: return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: return [("nap", 4, r.stderr[-300:])]
def mot(m):
    ten, ma = m; d = Path(tempfile.mkdtemp(prefix="tt_", dir='/tmp/claude-0/-home-user-tra-luat/eaf2a577-1c02-5642-8186-a4b48145f1ca/scratchpad/r4review4/ws/.review/tmp')); p = d / "db.py"; p.write_text(ma)
    kq = cases(p); giet = [c for c, rc, o in kq if rc == 3 and o.startswith(f"DO:{c}:")]; vo = [c for c, rc, o in kq if rc not in (0, 3)]
    return {"name": ten, "rank": "GIET" if giet and not vo else "TIN_DUNG_GIA" if vo and not giet else "GIET+NEM" if vo else "SONG", "killed": giet, "other_errors": vo, "cases": kq, "source": str(p)}
out = ROOT / ".review/operators";out.mkdir(exist_ok=True)
rows=[]
print("so dot bien",len(M),flush=True)
with ThreadPoolExecutor(4) as ex:
 for r in ex.map(mot,M):
  rows.append(r);(out/"results.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2))
  print(r["name"],r["rank"],flush=True)
