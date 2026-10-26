import concurrent.futures, importlib.util, json, os, pathlib, re, subprocess, sys
R=pathlib.Path(__file__).resolve().parent;root=R.parent;src=(root/'ops/ci_provenance.py').read_text();prior=root/'.review-input/r4-luot7'
names=re.findall(r'^\|([^|]+)\|P1 / F10\|', (prior/'VERDICT.md').read_text(),re.M)
records={z['name']:z for d in ('frontier7','frontier7b') for z in json.loads((prior/d/'results.json').read_text())}
case='c51_mien_luot7';out=R/'prior-f10';out.mkdir(exist_ok=True)
def call(path):
    cmd=[sys.executable,'-B',str(root/'ops/ci_provenance_test.py'),'--mot-ca',case];p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(path)),timeout=300);return {'command':cmd,'source':str(path),'rc':p.returncode,'output':(p.stdout+p.stderr).decode()}
baseline=call(root/'ops/ci_provenance.py');assert baseline['rc']==0
def one(name):
    z=records[name];a,b=z['old'],z['new'];assert src.count(a)==1,(name,src.count(a));p=out/(name+'.py');p.write_text(src.replace(a,b));v=call(p);return {'prior_name':name,'before':a,'after':b,'current_case':case,'measurement':v,'closed':v['rc']==3 and v['output'].startswith('DO:'+case+':')}
with concurrent.futures.ThreadPoolExecutor(4) as ex:rows=list(ex.map(one,names))
(R/'prior-f10-8-results.json').write_text(json.dumps({'baseline':baseline,'count':len(rows),'rows':rows},ensure_ascii=False,indent=1));print('PRIOR F10',len(rows),'closed',sum(x['closed'] for x in rows));print([x['prior_name'] for x in rows if not x['closed']]);assert len(rows)==32 and all(x['closed'] for x in rows)
