from pathlib import Path
import os,sys,json,subprocess,concurrent.futures,collections
R=Path(__file__).resolve().parent;root=R.parent
src=(root/'ops/ci_provenance.py').read_text();out=R/'new-frontier';out.mkdir(exist_ok=True)
M=[
('job_escape_alias','re.escape(x)', 'x'),
('job_alias_strip','re.escape(x)', 're.escape(x.strip())'),
('job_casefold','ten) for x in (k, j.get("name"))','ten, re.I) for x in (k, j.get("name"))'),
('name_explicit_strip','return s["name"] if _chuoi(s["name"])','return s["name"].strip() if _chuoi(s["name"])'),
('name_explicit_casefold','return s["name"] if _chuoi(s["name"])','return s["name"].casefold() if _chuoi(s["name"])'),
('metadata_setup_prefix','s.get("name") not in ("Set up job", "Complete job")','not str(s.get("name")).startswith("Set up job") and s.get("name") != "Complete job"'),
('metadata_complete_prefix','s.get("name") not in ("Set up job", "Complete job")','s.get("name") != "Set up job" and not str(s.get("name")).startswith("Complete job")'),
('metadata_post_suffix','str(s.get("name")).startswith("Post ")','str(s.get("name")).endswith("Post ")'),
('ran_neutral_excluded','s.get("conclusion") != "skipped"]','s.get("conclusion") not in ("skipped", "neutral")]'),
('ran_cancelled_excluded','s.get("conclusion") != "skipped"]','s.get("conclusion") not in ("skipped", "cancelled")]'),
('env_prefix_empty_suffix','str(k).startswith("CI_DANG_KY_")','(str(k).startswith("CI_DANG_KY_") and len(str(k)) > len("CI_DANG_KY_"))'),
('env_prefix_casefold','str(k).startswith("CI_DANG_KY_")','str(k).upper().startswith("CI_DANG_KY_")'),
('mode_step_key_truthy','set(s) - KHOA_BUOC','{key for key in s if s[key]} - KHOA_BUOC'),
('mode_shell_strip','s.get("shell", "bash") not in','str(s.get("shell", "bash")).strip() not in'),
('mode_shell_casefold','s.get("shell", "bash") not in','str(s.get("shell", "bash")).lower() not in'),
('mode_prior_requires_ran','for t in j["steps"][:i]))','for t in j["steps"][:i] if t.get("if") != "false"))'),
('run_compare_strip_newlines','run.rstrip("\\n") == "\\n".join(b["in_lai"])','run.strip("\\n") == "\\n".join(b["in_lai"])'),
('header_lstrip','b["in_lai"][:1] == [b["lenh"]]','b["in_lai"][:1] == [b["lenh"].lstrip()]'),
('shell_lstrip','t.startswith("shell: ")','t.lstrip().startswith("shell: ")'),
('number_contiguous','and len({s["number"] for s in st}) == len(st)','and {s["number"] for s in st} == set(range(1, len(st) + 1))'),
]
def cases(path):
 code="import importlib.util as u,json;s=u.spec_from_file_location('t',%r);t=u.module_from_spec(s);s.loader.exec_module(t);print(json.dumps([(c,)+t.chay_ca(c) for c in t.CA]))"%str(root/'ops/ci_provenance_test.py')
 cmd=[sys.executable,'-B','-c',code]
 p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CI_PROVENANCE_MA=str(path)),timeout=900)
 return cmd,p,json.loads(p.stdout)
cmd,p,base=cases(root/'ops/ci_provenance.py');assert p.returncode==0 and len(base)==47 and all(rc==0 for c,rc,o in base)
(out/'baseline.json').write_text(json.dumps(base,ensure_ascii=False,indent=2))
def one(v):
 name,old,new=v;rec={'name':name,'old':old,'new':new,'count':src.count(old)}
 if src.count(old)!=1:return rec|{'rank':'HONG_NEO'}
 path=out/(name+'.py');path.write_text(src.replace(old,new));cmd,p,res=cases(path)
 (out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr)
 killed=[c for c,rc,o in res if rc==3 and o.startswith('DO:'+c+':')];bad=[{'case':c,'rc':rc,'output':o} for c,rc,o in res if rc and not (rc==3 and o.startswith('DO:'+c+':'))]
 return rec|{'command':cmd,'source':str(path),'rc':p.returncode,'rank':'GIET' if killed else 'TIN_DUNG_GIA' if bad else 'SONG_SOT','killed':killed,'other_errors':bad,'cases':res}
rows=[]
with concurrent.futures.ThreadPoolExecutor(4) as ex:
 for v in ex.map(one,M):
  rows.append(v);(out/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(v['name'],v['rank'],v.get('killed'),flush=True)
print(collections.Counter(r['rank'] for r in rows))
