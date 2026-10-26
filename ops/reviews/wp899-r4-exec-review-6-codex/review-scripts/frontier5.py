from pathlib import Path
import ast,sys,os,json,subprocess,concurrent.futures,collections
R=Path(__file__).resolve().parent;root=R.parent
src=(root/'ops/ci_provenance.py').read_text();out=R/'frontier5';out.mkdir(exist_ok=True)
M=[
('wf_env_dict_only','_env_chan(wf)','(type(wf.get("env")) is dict and _env_chan(wf))'),
('wf_env_nonempty_only','_env_chan(wf)','(bool(wf.get("env")) and _env_chan(wf))'),
('job_env_only_first_key','any(str(k).startswith("CI_DANG_KY_") for k in d["env"])','any(str(k).startswith("CI_DANG_KY_") for k in list(d["env"])[:1])'),
('job_env_only_last_key','any(str(k).startswith("CI_DANG_KY_") for k in d["env"])','any(str(k).startswith("CI_DANG_KY_") for k in list(d["env"])[-1:])'),
('mode_last_step','j, s = wf["jobs"][k], wf["jobs"][k]["steps"][i]','j, s = wf["jobs"][k], wf["jobs"][k]["steps"][-1]'),
('mode_first_run_step','j, s = wf["jobs"][k], wf["jobs"][k]["steps"][i]','j, s = wf["jobs"][k], wf["jobs"][k]["steps"][1]'),
('mode_first_job','j, s = wf["jobs"][k], wf["jobs"][k]["steps"][i]','j, s = next(iter(wf["jobs"].values())), wf["jobs"][k]["steps"][i]'),
('dd_first_job','s = wf["jobs"][k]["steps"][i]','s = next(iter(wf["jobs"].values()))["steps"][i]'),
('job_match_exact_preference','return khop[0] if len(khop) == 1 else None','return (ten if ten in khop else khop[0] if len(khop) == 1 else None)'),
('job_first_prefix_only','for x in (k, j.get("name"))','for x in (k, j.get("name")) if ten == k or len(ten)<80'),
('metadata_first_setup_only','s.get("name") not in ("Set up job", "Complete job")','(s.get("name") != "Set up job" or s.get("number") != 1) and s.get("name") != "Complete job"'),
('metadata_complete_last_only','s.get("name") not in ("Set up job", "Complete job")','s.get("name") != "Set up job" and (s.get("name") != "Complete job" or s.get("number") != max(z["number"] for z in st))'),
('time_name_first_key','_gio(ung[i].get("started_at"))','_gio(ung[chay[0]].get("started_at"))'),
('time_name_last_key','_gio(ung[i].get("completed_at"))','_gio(ung[chay[-1]].get("completed_at"))'),
('time_only_first_group','for b, i in zip(buoc, chay)):','for b, i in list(zip(buoc, chay))[:1]):'),
('time_only_last_group','for b, i in zip(buoc, chay)):','for b, i in list(zip(buoc, chay))[-1:]):'),
('name_skip_first_yaml','for s, y in zip(ung, sy)):','for s, y in list(zip(ung, sy))[1:]):'),
('name_skip_last_yaml','for s, y in zip(ung, sy)):','for s, y in list(zip(ung, sy))[:-1]):'),
('rest_sort_lexical','key=lambda s: s["number"]','key=lambda s: str(s["number"])'),
('rest_sort_input','sorted(st, key=lambda s: s["number"])','st'),
('rest_number_integral_float','_so(s.get("number"), 1)','(_so(s.get("number"), 1) or (type(s.get("number")) is float and s["number"].is_integer() and s["number"] >= 1))'),
('ghep_zero_groups_reject','if len(buoc) != len(chay):','if not buoc or len(buoc) != len(chay):'),
('env_false_accept','return "env" in d and (type(d["env"]) is not dict','return "env" in d and d["env"] not in (None, False) and (type(d["env"]) is not dict'),
('env_int_accept','return "env" in d and (type(d["env"]) is not dict','return "env" in d and type(d["env"]) is not int and (type(d["env"]) is not dict'),
('env_empty_str_accept','return "env" in d and (type(d["env"]) is not dict','return "env" in d and d["env"] not in (None, "") and (type(d["env"]) is not dict'),
('prior_run_only_strings','str(t.get("run", ""))','(t.get("run", "") if type(t.get("run", "")) is str else "")'),
('prior_github_match','re.search("GITHUB_(ENV|PATH)",','re.match("GITHUB_(ENV|PATH)",'),
('prior_path_suffix','re.search("GITHUB_(ENV|PATH)",','re.search("GITHUB_(ENV|PATH)$",'),
('prior_env_word_boundary','re.search("GITHUB_(ENV|PATH)",','re.search(r"\\bGITHUB_(ENV|PATH)\\b",'),
('nested_exact_only','not t.startswith("##[group]")','t != "##[group]"'),
('nested_only_after_shell','not t.startswith("##[group]")','not (t.startswith("##[group]") and not b["tien_to"])'),
('nested_only_before_shell','not t.startswith("##[group]")','not (t.startswith("##[group]") and b["tien_to"])'),
('header_colored_exact','mau = "\\x1b[36;1m" in d','mau = bool(re.search(r"\\x1b\\[36;1m.*\\x1b\\[0m$", d))'),
('header_seconds_18','"gio": d[:19] + "Z"','"gio": d[:18] + "Z"'),
('header_seconds_round','"gio": d[:19] + "Z"','"gio": (datetime.datetime.strptime(d[:19], "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%SZ")'),
('run_blank_tail_only','run.rstrip("\\n") == "\\n".join(b["in_lai"])','run.rstrip("\\n") == "\\n".join(b["in_lai"]).rstrip("\\n")'),
('run_trailing_lf_exact','run.rstrip("\\n") == "\\n".join(b["in_lai"])','run.removesuffix("\\n") == "\\n".join(b["in_lai"])'),
('run_first_group_only','for b, (k, i) in zip(buoc, ghep or []):','for b, (k, i) in list(zip(buoc, ghep or []))[:1]:'),
('run_last_group_only','for b, (k, i) in zip(buoc, ghep or []):','for b, (k, i) in list(zip(buoc, ghep or []))[-1:]:'),
('minimal_reverse_lines','dong_logic(run.rstrip("\\n").split("\\n"))','reversed(dong_logic(run.rstrip("\\n").split("\\n")))'),
('minimal_first_line_only','dong_logic(run.rstrip("\\n").split("\\n"))','dong_logic(run.rstrip("\\n").split("\\n"))[:1]'),
('name_uses_strip','v = s.get("run", s.get("uses"))','v = s.get("run", str(s.get("uses")).strip())'),
('name_run_prefer_uses','v = s.get("run", s.get("uses"))','v = s.get("uses", s.get("run"))'),
('name_remove_blank_lines','v.split("\\n")[0] if _chuoi(v)','next((z for z in v.split("\\n") if z), "") if _chuoi(v)'),
('name_reject_empty_line','return "Run " + v.split("\\n")[0] if _chuoi(v) else None','return "Run " + v.split("\\n")[0] if _chuoi(v) and v.split("\\n")[0] else None'),
('env_prefix_value_only','str(k).startswith("CI_DANG_KY_")','(str(k).startswith("CI_DANG_KY_") and bool(v[k]))'),
]
# Inventory identity means mutations already attempted are marked as inherited, never called new.
known=set()
for base in (root/'.review-input/tu-dot-bien',root/'.review-input/r4-luot4'):
 for p in base.glob('*.py'):
  try: parsed=ast.parse(p.read_text())
  except SyntaxError: continue
  for n in ast.walk(parsed):
   if isinstance(n,(ast.List,ast.Tuple)) and len(n.elts)>=3:
    try:v=ast.literal_eval(n)
    except Exception:continue
    if all(isinstance(x,str) for x in v[:3]):known.add((v[1],v[2]))
def cases(path):
 code="import importlib.util as u,json;s=u.spec_from_file_location('t',%r);t=u.module_from_spec(s);s.loader.exec_module(t);print(json.dumps([(c,)+t.chay_ca(c) for c in t.CA]))"%str(root/'ops/ci_provenance_test.py')
 cmd=[sys.executable,'-B','-c',code];p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CI_PROVENANCE_MA=str(path)),timeout=900)
 return cmd,p,json.loads(p.stdout)
cmd,p,base=cases(root/'ops/ci_provenance.py');assert len(base)==49 and all(rc==0 for c,rc,o in base)
(out/'baseline.json').write_text(json.dumps(base,ensure_ascii=False,indent=2))
def one(v):
 name,old,new=v;rec={'name':name,'old':old,'new':new,'new_vs_inventory':(old,new) not in known,'count':src.count(old)}
 if src.count(old)!=1:return rec|{'rank':'HONG_NEO'}
 path=out/(name+'.py');path.write_text(src.replace(old,new));cmd,p,res=cases(path)
 (out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr)
 killed=[c for c,rc,o in res if rc==3 and o.startswith('DO:'+c+':')];bad=[{'case':c,'rc':rc,'output':o} for c,rc,o in res if rc and not(rc==3 and o.startswith('DO:'+c+':'))]
 return rec|{'command':cmd,'source':str(path),'rc':p.returncode,'rank':'GIET+NEM' if killed and bad else 'GIET' if killed else 'TIN_DUNG_GIA' if bad else 'SONG_SOT','killed':killed,'other_errors':bad,'cases':res}
rows=[]
with concurrent.futures.ThreadPoolExecutor(3) as ex:
 for r in ex.map(one,M):
  rows.append(r);(out/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(r['name'],r['rank'],r.get('killed'),flush=True)
print(collections.Counter(x['rank'] for x in rows))
