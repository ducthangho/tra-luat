import collections, importlib.util, json, re, subprocess, sys
from pathlib import Path
import yaml
W=Path(__file__).resolve().parent; R=W.parent/'repo'
sys.path[:0]=[str(W),str(W/'soan')]
import gram, gate_output_doi_chieu as m
def git(*args):
    return subprocess.check_output(['git','-C',str(R),*args]).decode().strip()
names={n for rule in m.LUAT_v1['MUC'] for b in rule['buoc'] for n in b['ten']}
out={'workflows':{}}
for ref in ['d26b36f','fe84620','8983e1b']:
    wf=yaml.safe_load(git('show',ref+':.github/workflows/ci.yml'))
    rows=[s for j in wf['jobs'].values() for s in j.get('steps',[]) if s.get('name') in names]
    accepted=[s for s in rows if gram.cp(s.get('run'),s.get('shell')) is None]
    uses=[s['uses'] for j in wf['jobs'].values() for s in j.get('steps',[]) if 'uses' in s]
    out['workflows'][ref]={'steps':len(rows),'accepted':len(accepted),'with_args':sum(len(s['run'].split())>2 for s in accepted),
      'shells':dict(collections.Counter(str(s.get('shell')) for s in rows)),'uses':dict(collections.Counter(uses)),
      'pinned_sha':sum(bool(re.search(r'@[0-9a-f]{40}$',s)) for s in uses)}
    out['workflows'][ref]['actionlint_GITHUB_PATH_lines']=[i for i,l in enumerate(git('show',ref+':ops/cai_actionlint.sh').splitlines(),1) if 'GITHUB_PATH' in l]
    if ref=='fe84620': original=wf
    if ref=='8983e1b':
        out['changed_rule_steps']=[s['name'] for k,j in wf['jobs'].items() for s in j.get('steps',[]) if s.get('name') in names and s!=next(z for z in original['jobs'][k]['steps'] if z.get('name')==s['name'])]
pv=[]
for path in git('ls-tree','-r','--name-only','d26b36f','--','ops/land').splitlines():
    if '-provenance/' not in path or not path.endswith('.yaml'):continue
    p=yaml.safe_load(git('show','d26b36f:'+path))
    if isinstance(p,dict) and p.get('schema')=='ci_provenance/1':pv.append((path,p))
land=[];head_diff=[];blob_match=[]
for path,p in pv:
    run=p['moc']['run']; ck=[c for c in p['moc']['checkout'] if c['trang_thai']=='passed']
    if any(c['sha']!=run['head_sha'] for c in ck):head_diff.append(path)
    wd=p['moc'].get('workflow_definition',{})
    if wd.get('trang_thai')=='passed':
        matches=[git('rev-parse',c['sha']+':'+run['loi_khai_rest_path'])==wd['blob'] for c in ck]
        blob_match.append((path,bool(matches) and all(matches)))
    if run['event']=='push' and run['loi_khai_rest_path']=='.github/workflows/ci.yml':
        jobs=[j for j in p['moc']['gate_output']['jobs'] if j['conclusion']!='skipped' and 'ubuntu-latest' in (j['labels'] or []) and j['name']!='chuan-bi']
        land.append((run['run_id'],path,sorted(j['name'] for j in jobs)==sorted(m.LUAT_v1['JOB_BAT_BUOC'])))
out['provenance']={'total':len(pv),'checkout_head_different':head_diff,'workflow_passed':len(blob_match),'workflow_blob_match':sum(b for _,b in blob_match),
 'ci_push':len(land),'jobs_match':sum(b for _,_,b in land),'earliest':min(land)}
out['new_estimate_arithmetic']=1620+(25-15)+(-40+120+55+45+65+40+22+60+5+20)
out['declared_estimate_arithmetic']=1620+10+390
out['ceiling']=2150
print(json.dumps(out,ensure_ascii=False,indent=2))
(W/'round3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
