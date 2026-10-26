"""Đột biến TOÁN TỬ tự động trên các hàm r4: mỗi token một đột biến, chạy toàn bộ ca, in SONG / TIN_DUNG_GIA."""
import ast, io, json, os, re, subprocess, sys, tempfile, tokenize
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path("/tmp/claude-0/-home-user-tra-luat/eaf2a577-1c02-5642-8186-a4b48145f1ca/scratchpad/r4review6/ws"); SRC = (ROOT / "ops/ci_provenance.py").read_text()
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
TARGETS = {"L154c13:'is not'->'is'": 'c12_marker_khong_khop', "L154c25:'and'->'or'": 'c12_marker_khong_khop', "L154c38:'is not'->'is'": 'c29_che_do_env_job', "L154c50:'or'->'and'": 'c29_che_do_env_job', "L154c53:'any'->'all'": 'c29_che_do_env_job', "L162c26:'is'->'is not'": 'c12_marker_khong_khop', "L162c34:'and'->'or'": 'c32_workflow_khong_doc_duoc', "L162c59:'is'->'is not'": 'c12_marker_khong_khop', "L166c58:'is'->'is not'": 'c12_marker_khong_khop', "L166c65:'and'->'or'": 'c22_thieu_dinh_danh_khong_passed', "L166c77:'is'->'is not'": 'c12_marker_khong_khop', "L166c85:'and'->'or'": 'c22_thieu_dinh_danh_khong_passed', "L166c89:'any'->'all'": 'c12_marker_khong_khop', "L167c16:'is'->'is not'": 'c12_marker_khong_khop', "L167c23:'and'->'or'": 'c33_trung_chu_khac_job', "L167c29:'and'->'or'": 'c33_trung_chu_khac_job', "L167c39:'not in'->'in'": 'c12_marker_khong_khop', "L167c48:'and'->'or'": 'c33_trung_chu_khac_job', "L168c16:'0'->'1'": 'c23_chi_loi_goi_that', "L168c32:'=='->'!='": 'c12_marker_khong_khop', "L168c35:'1'->'2'": 'c12_marker_khong_khop', "L168c35:'1'->'0'": 'c12_marker_khong_khop', "L171c14:'in'->'not in'": 'c23_chi_loi_goi_that', "L172c46:'and'->'or'": 'c37_ghep_lech_ten', "L172c56:'not in'->'in'": 'c31_che_do_duong_khac', "L174c34:'0'->'1'": 'c23_chi_loi_goi_that', "L178c45:'19'->'20'": 'c12_marker_khong_khop', "L178c45:'19'->'18'": 'c38_ghep_lech_gio', "L178c82:'is'->'is not'": 'c12_marker_khong_khop', "L178c89:'and'->'or'": 'c38_ghep_lech_gio', "L187c10:'is'->'is not'": 'c12_marker_khong_khop', "L191c9:'is'->'is not'": 'c12_marker_khong_khop', "L191c17:'or'->'and'": 'c39_ghep_job', "L191c27:'in'->'not in'": 'c12_marker_khong_khop', "L191c44:'or'->'and'": 'c39_ghep_job', "L191c56:'is not'->'is'": 'c12_marker_khong_khop', "L191c68:'or'->'and'": 'c44_ghep_sai_dang', "L191c71:'not'->''": 'c12_marker_khong_khop', "L191c75:'all'->'any'": 'c44_ghep_sai_dang', "L191c87:'is'->'is not'": 'c12_marker_khong_khop', "L193c7:'not'->''": 'c12_marker_khong_khop', "L193c21:'is'->'is not'": 'c12_marker_khong_khop', "L193c29:'and'->'or'": 'c22_thieu_dinh_danh_khong_passed', "L193c33:'all'->'any'": 'c44_ghep_sai_dang', "L193c45:'is'->'is not'": 'c12_marker_khong_khop', "L193c53:'and'->'or'": 'c44_ghep_sai_dang', "L193c78:'1'->'2'": 'c12_marker_khong_khop', "L193c78:'1'->'0'": 'c44_ghep_sai_dang', "L194c12:'and'->'or'": 'c22_thieu_dinh_danh_khong_passed', "L194c47:'=='->'!='": 'c12_marker_khong_khop', "L196c77:'not in'->'in'": 'c12_marker_khong_khop', "L197c11:'and'->'or'": 'c12_marker_khong_khop', "L197c15:'not'->''": 'c12_marker_khong_khop', "L198c64:'!='->'=='": 'c12_marker_khong_khop', "L199c17:'!='->'=='": 'c12_marker_khong_khop', "L201c16:'!='->'=='": 'c12_marker_khong_khop', "L203c7:'any'->'all'": 'c37_ghep_lech_ten', "L203c11:'not'->''": 'c12_marker_khong_khop', "L203c37:'or'->'and'": 'c37_ghep_lech_ten', "L203c54:'!='->'=='": 'c12_marker_khong_khop', "L205c7:'not'->''": 'c12_marker_khong_khop', "L205c11:'all'->'any'": 'c38_ghep_lech_gio', "L205c53:'and'->'or'": 'c38_ghep_lech_gio', "L206c15:'and'->'or'": 'c38_ghep_lech_gio', "L206c41:'and'->'or'": 'c38_ghep_lech_gio', "L206c47:'<='->'<'": 'c12_marker_khong_khop', "L206c52:'<='->'<'": 'c12_marker_khong_khop', "L214c27:'in'->'not in'": 'c12_marker_khong_khop', "L214c33:'or'->'and'": 'c31_che_do_duong_khac', "L214c61:'or'->'and'": 'c31_che_do_duong_khac', "L214c75:'in'->'not in'": 'c12_marker_khong_khop', "L214c80:'or'->'and'": 'c29_che_do_env_job', "L214c107:'or'->'and'": 'c28_che_do_env_buoc', "L215c16:'or'->'and'": 'c28_che_do_env_buoc', "L215c42:'not in'->'in'": 'c12_marker_khong_khop', "L216c16:'or'->'and'": 'c31_che_do_duong_khac', "L216c19:'any'->'all'": 'c42_github_env_cung_job', "L262c91:'True'->'False'": 'c12_marker_khong_khop', "L262c103:'True'->'False'": 'c12_marker_khong_khop', "L262c120:'True'->'False'": 'c12_marker_khong_khop', "L263c35:'19'->'20'": 'c12_marker_khong_khop', "L263c35:'19'->'18'": 'c12_marker_khong_khop', "L264c18:'and'->'or'": 'c23_chi_loi_goi_that', "L264c34:'1'->'2'": 'c12_marker_khong_khop', "L264c34:'1'->'0'": 'c12_marker_khong_khop', "L265c31:'in'->'not in'": 'c12_marker_khong_khop', "L266c17:'=='->'!='": 'c12_marker_khong_khop', "L267c26:'False'->'True'": 'c12_marker_khong_khop', "L268c21:'and'->'or'": 'c12_marker_khong_khop', "L271c48:'and'->'or'": 'c25_f02_env_mang_mau', "L271c52:'not'->''": 'c12_marker_khong_khop', "L271c60:'and'->'or'": 'c25_f02_env_mang_mau', "L271c64:'not'->''": 'c12_marker_khong_khop', "L271c94:'and'->'or'": 'c25_f02_env_mang_mau', "L272c20:'not'->''": 'c47_bien_ghep', "L272c37:'or'->'and'": 'c12_marker_khong_khop', "L272c66:'False'->'True'": 'c12_marker_khong_khop', "L274c18:'1'->'2'": 'c12_marker_khong_khop', "L274c18:'1'->'0'": 'c12_marker_khong_khop', "L275c27:'not'->''": 'c12_marker_khong_khop', "L275c39:'and'->'or'": 'c25_f02_env_mang_mau', "L275c51:'and'->'or'": 'c25_f02_env_mang_mau', "L275c55:'not'->''": 'c12_marker_khong_khop', "L275c72:'and'->'or'": 'c25_f02_env_mang_mau', "L275c89:'1'->'2'": 'c27_f02_yaml_khong_toi_gian', "L275c89:'1'->'0'": 'c12_marker_khong_khop', "L275c92:'=='->'!='": 'c12_marker_khong_khop', "L291c17:'0'->'1'": 'c25_f02_env_mang_mau', "L292c36:'or'->'and'": 'c12_marker_khong_khop', "L294c37:'not in'->'in'": 'c12_marker_khong_khop', "L295c11:'not'->''": 'c23_chi_loi_goi_that', "L295c26:'is'->'is not'": 'c12_marker_khong_khop', "L295c33:'and'->'or'": 'c25_f02_env_mang_mau', "L295c49:'and'->'or'": 'c23_chi_loi_goi_that', "L295c70:'=='->'!='": 'c12_marker_khong_khop', "L297c14:'1'->'2'": 'c27_f02_yaml_khong_toi_gian', "L297c14:'1'->'0'": 'c27_f02_yaml_khong_toi_gian', "L299c35:'or'->'and'": 'c28_che_do_env_buoc', "L299c38:'any'->'all'": 'c46_mien_che_do', "L299c44:'and'->'or'": 'c12_marker_khong_khop', "L299c50:'1'->'2'": 'c12_marker_khong_khop', "L299c50:'1'->'0'": 'c12_marker_khong_khop', "L300c38:'2'->'3'": 'c44_ghep_sai_dang', "L300c38:'2'->'1'": 'c12_marker_khong_khop', "L300c62:'and'->'or'": 'c23_chi_loi_goi_that', "L300c66:'all'->'any'": 'c23_chi_loi_goi_that', "L302c21:'not in'->'in'": 'c12_marker_khong_khop', "L302c32:'or'->'and'": 'c28_che_do_env_buoc', "L303c102:'not in'->'in'": 'c28_che_do_env_buoc', "L307c98:'0'->'1'": 'c12_marker_khong_khop'}
def cases(ma, name):
    code = ("import importlib.util as u,json;s=u.spec_from_file_location('t','/tmp/claude-0/-home-user-tra-luat/eaf2a577-1c02-5642-8186-a4b48145f1ca/scratchpad/r4review6/ws/ops/ci_provenance_test.py');"
            "t=u.module_from_spec(s);s.loader.exec_module(t);print(json.dumps([(c,)+t.chay_ca(c) for c in [CASE_TARGET]]))")
    code = code.replace("CASE_TARGET", repr(TARGETS[name]))
    r = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True,
                       env=dict(os.environ, CI_PROVENANCE_MA=str(ma), PYTHONDONTWRITEBYTECODE="1"), timeout=900)
    try: return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: return [("nap", 4, r.stderr[-300:])]
def mot(m):
    ten, ma = m; d = Path(tempfile.mkdtemp(prefix="tt_", dir='/tmp/claude-0/-home-user-tra-luat/eaf2a577-1c02-5642-8186-a4b48145f1ca/scratchpad/r4review6/ws/.review/tmp')); p = d / "db.py"; p.write_text(ma)
    kq = cases(p, ten); giet = [c for c, rc, o in kq if rc == 3 and o.startswith(f"DO:{c}:")]; vo = [c for c, rc, o in kq if rc not in (0, 3)]
    return {"name": ten, "rank": "GIET" if giet and not vo else "TIN_DUNG_GIA" if vo and not giet else "GIET+NEM" if vo else "SONG", "killed": giet, "other_errors": vo, "cases": kq, "source": str(p)}
out = ROOT / ".review/operators5-target";out.mkdir(exist_ok=True)
rows=[]
print("so dot bien",len(M),flush=True)
with ThreadPoolExecutor(4) as ex:
 for r in ex.map(mot,M):
  rows.append(r);(out/"results.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2))
  print(r["name"],r["rank"],flush=True)
