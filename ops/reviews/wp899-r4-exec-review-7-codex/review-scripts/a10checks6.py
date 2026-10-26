from pathlib import Path
import json,yaml,subprocess,hashlib,collections
root=Path.cwd();R=root/'.review';d=root/'.review-input/log-that';checks=[]
for line in (d/'SHA256SUMS').read_text().splitlines():
 h,name=line.split(maxsplit=1);name=name.lstrip('*')
 p=d/name
 if not p.exists():
  matches=list(d.rglob(Path(name).name));assert len(matches)==1,(name,matches);p=matches[0]
 b=p.read_bytes();actual=hashlib.sha256(b).hexdigest();checks.append({'path':str(p.relative_to(root)),'bytes':len(b),'expected':h,'actual':actual,'equal':h==actual})
assert len(checks)==37 and all(x['equal'] for x in checks)
rows=[]
for rid in (39342960764,40074551995):
 src=root/f'.review-input/a10/out-{rid}';pv=yaml.safe_load((R/f'prior2/replay-{rid}/provenance.yaml').read_bytes());run=json.loads((src/'run.json').read_bytes());p=subprocess.run(['git','cat-file','blob',f'{run["head_sha"]}:{run["path"]}'],capture_output=True);assert p.returncode==0
 wf=yaml.safe_load(p.stdout);nulls=[]
 for scope,v in [('workflow',wf)]+[('job '+k,v) for k,v in wf['jobs'].items()]:
  if 'env' in v and v['env'] is None:nulls.append(scope)
 gs=pv['moc']['gate_output']['jobs'];markers=[{'job':j['name'],'path':x['duong_dan'],'state':x['trang_thai'],'reason':x.get('ly_do')} for j in gs for x in j['dau_duong']]
 rows.append({'run':rid,'workflow_sha256':hashlib.sha256(p.stdout).hexdigest(),'workflow_git_command':['git','cat-file','blob',f'{run["head_sha"]}:{run["path"]}'],'rc':p.returncode,'null_env_scopes':nulls,'labels':list({tuple(j['labels']) for j in gs}),'run_state':pv['moc']['run']['trang_thai'],'gate_states':dict(collections.Counter(j['trang_thai'] for j in gs)),'checkout_states':dict(collections.Counter(j['trang_thai'] for j in pv['moc']['checkout'])),'ghep_states':dict(collections.Counter(j['ghep_buoc']['trang_thai'] for j in gs)),'all_markers':markers,'provenance_sha256':hashlib.sha256((R/f'prior2/replay-{rid}/provenance.yaml').read_bytes()).hexdigest()})
 assert not nulls and not any(j['trang_thai']=='failed' for j in gs)
(R/'a10checks6-results.json').write_text(json.dumps({'sha256sums':checks,'runs':rows},ensure_ascii=False,indent=2));print('37/37 SHA256SUMS DAT');print(json.dumps(rows,ensure_ascii=False,indent=2))
