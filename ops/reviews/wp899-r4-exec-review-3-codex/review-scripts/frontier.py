from pathlib import Path
import ast,sys,os,json,subprocess,importlib.util,concurrent.futures,collections
R=Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('ct',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text();out=R/'frontier';out.mkdir(exist_ok=True)
M=[
('job_rest_type','if type(ten) is str and type(j) is dict and any(', 'if type(j) is dict and any('),
('job_match_search','and re.fullmatch(re.escape(x)', 'and re.search(re.escape(x)'),
('job_matrix_nonempty',r'r"(?: \(.*\))?"',r'r"(?: \(.+\))?"'),
('job_dotall_add','ten) for x in (k, j.get("name"))','ten, re.S) for x in (k, j.get("name"))'),
('job_alias_exact_drop','type(x) is str and x and "${{" not in x and re.fullmatch', 'type(x) is str and x and ten != j.get("name") and "${{" not in x and re.fullmatch'),
('name_use_last_line','v.split("\\n")[0] if _chuoi(v)','v.rstrip("\\n").split("\\n")[-1] if _chuoi(v)'),
('name_rest_strip','s.get("name") != ten_du_kien(y)','s.get("name").strip() != ten_du_kien(y)'),
('time_drop_type','if type(v) is str and RE_GIO.fullmatch(v) else None','if RE_GIO.fullmatch(v) else None'),
('time_year0_drop','    except ValueError:\n        return None', '    except KeyError:\n        return None'),
('time_calendar_date_only','strptime(v[:19], "%Y-%m-%dT%H:%M:%S")','strptime(v[:10], "%Y-%m-%d")'),
('time_low_strict','a <= h <= z','a < h <= z'),
('time_hi_strict','a <= h <= z','a <= h < z'),
('time_or_bounds','a <= h <= z','(a <= h or h <= z)'),
('time_low_only','a <= h <= z','a <= h'),
('time_hi_only','a <= h <= z','h <= z'),
('rest_number_float','_so(s.get("number"), 1)','(isinstance(s.get("number"), (int, float)) and not isinstance(s.get("number"), bool) and s["number"] >= 1)'),
('rest_number_bool','_so(s.get("number"), 1)','(isinstance(s.get("number"), int) and s["number"] >= 1)'),
('rest_steps_list_drop','type(st) is list and all(', 'all('),
('rest_steps_all_any','all(type(s) is dict and _so(s.get("number"), 1)', 'any(type(s) is dict and _so(s.get("number"), 1)'),
('yaml_steps_all_any','not all(type(s) is dict for s in sy)','not any(type(s) is dict for s in sy)'),
('number_sort_desc','key=lambda s: s["number"])','key=lambda s: -s["number"])'),
('metadata_keep_setup','not in ("Set up job", "Complete job")','not in ("Complete job",)'),
('metadata_keep_complete','not in ("Set up job", "Complete job")','not in ("Set up job",)'),
('metadata_post_anywhere','str(s.get("name")).startswith("Post ")','("Post " in str(s.get("name")))'),
('mode_env_shape_drop','type(v) is not dict or any(str(k)', 'False or any(str(k)'),
('mode_env_prefix_exact','str(k).startswith("CI_DANG_KY_")','str(k) == "CI_DANG_KY_"'),
('mode_shell_no_pwsh','("bash", "pwsh", "sh")','("bash", "sh")'),
('mode_shell_no_sh','("bash", "pwsh", "sh")','("bash", "pwsh")'),
('mode_shell_null_default','s.get("shell", "bash")','(s.get("shell") or "bash")'),
('mode_env_presence_not_value','_env_chan(wf.get("env"))','("env" in wf)'),
('mode_env_job_presence','_env_chan(j.get("env"))','("env" in j)'),
('mode_key_id_drop','{"name", "id", "if", "run", "shell",','{"name", "if", "run", "shell",'),
('mode_key_if_drop','{"name", "id", "if", "run", "shell",','{"name", "id", "run", "shell",'),
('mode_key_timeout_drop','"timeout-minutes", "continue-on-error"}','"continue-on-error"}'),
('mode_key_coe_drop','"timeout-minutes", "continue-on-error"}','"timeout-minutes"}'),
('mode_prior_skip_first','for t in j["steps"][:i]))','for t in j["steps"][1:i]))'),
('mode_prior_only_first','for t in j["steps"][:i]))','for t in j["steps"][:1]))'),
('mode_prior_only_last','for t in j["steps"][:i]))','for t in j["steps"][max(i-1,0):i]))'),
('mode_prior_include_current','for t in j["steps"][:i]))','for t in j["steps"][:i+1]))'),
('run_rstrip_all','run.rstrip("\\n") == "\\n".join(b["in_lai"])','run.rstrip() == "\\n".join(b["in_lai"])'),
('run_type_coerce','type(run) is str and b["hop_le"] and run.rstrip','b["hop_le"] and str(run).rstrip'),
('dd_group_reverse','for b, (k, i) in zip(buoc, ghep or []):','for b, (k, i) in zip(reversed(buoc), ghep or []):'),
('dd_map_reverse','for b, (k, i) in zip(buoc, ghep or []):','for b, (k, i) in zip(buoc, list(reversed(ghep or []))):'),
('dd_output_dedupe','for duong in dict.fromkeys([g[2] for g in goi] if goi and all(goi) else []):','for duong in ([g[2] for g in goi] if goi and all(goi) else []):'),
('log_group_close_exact','if t.startswith("##[endgroup]"):','if t == "##[endgroup]":'),
('log_shell_suffix','t.startswith("shell: ")','t.startswith("shell:")'),
('log_nested_before_only','and not t.startswith("##[group]") and (','and not (t.startswith("##[group]") and b["tien_to"]) and ('),
('log_nested_after_only','and not t.startswith("##[group]") and (','and not (t.startswith("##[group]") and not b["tien_to"]) and ('),
('log_prefix_drop_ok','b["ok"] and not mau and','not mau and'),
('log_close_ignore_prefix','not b["tien_to"] and b["in_lai"][:1]','b["in_lai"][:1]'),
]
# Compare against the executor's two immutable mutation inventories; don't call a duplicate a new probe.
executed=[]
for name in ('tu_dot_bien.py','tu_dot_bien2.py'):
 tree=ast.parse((root/'.review-input/tu-dot-bien'/name).read_text())
 for node in ast.walk(tree):
  if isinstance(node,ast.Tuple) and len(node.elts)==3:
   try:v=ast.literal_eval(node)
   except Exception:continue
   if all(isinstance(x,str) for x in v):executed.append(v)
known={(o,n) for _,o,n in executed}
M=[(name,o,n, (o,n) not in known) for name,o,n in M]
def cases(path):
 code="import importlib.util as u,json;s=u.spec_from_file_location('t',%r);t=u.module_from_spec(s);s.loader.exec_module(t);print(json.dumps([(c,)+t.chay_ca(c) for c in t.CA]))"%str(root/'ops/ci_provenance_test.py')
 cmd=[sys.executable,'-B','-c',code]
 p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CI_PROVENANCE_MA=str(path)),timeout=600)
 return p,json.loads(p.stdout)
p,baseline=cases(root/'ops/ci_provenance.py');assert all(rc==0 for c,rc,o in baseline)
(out/'baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2))
def one(v):
 name,old,new,isnew=v;rec={'name':name,'old':old,'new':new,'new_vs_executor':isnew,'count':src.count(old)}
 if src.count(old)!=1:return rec|{'rank':'HONG_NEO'}
 path=out/(name+'.py');path.write_text(src.replace(old,new));p,res=cases(path)
 (out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr)
 killed=[c for c,rc,o in res if rc==3 and o.startswith('DO:'+c+':')];bad=[{'case':c,'rc':rc,'output':o} for c,rc,o in res if rc and not (rc==3 and o.startswith('DO:'+c+':'))]
 return rec|{'rc':p.returncode,'rank':'GIET' if killed else 'TIN_DUNG_GIA' if bad else 'SONG_SOT','killed':killed,'other_errors':bad,'cases':res}
rows=[]
with concurrent.futures.ThreadPoolExecutor(4) as ex:
 for v in ex.map(one,M):
  rows.append(v);(out/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(v['name'],v['rank'],v.get('killed'), 'OTHER',len(v.get('other_errors',[])),flush=True)
print(collections.Counter(r['rank'] for r in rows))
