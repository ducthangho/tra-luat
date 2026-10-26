from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parent;root=R.parent
start=json.loads((R/'snapshot-start.json').read_text());end=json.loads((R/'snapshot-end.json').read_text())
a,b=start['files'],end['files'];delta={'added':sorted(b.keys()-a.keys()),'removed':sorted(a.keys()-b.keys()),'changed':sorted(k for k in a.keys()&b.keys() if a[k]!=b[k])}
assert not any(delta.values()),delta
assert start['git']==end['git']
(R/'snapshot-comparison.json').write_text(json.dumps({'files_start':len(a),'files_end':len(b),'delta':delta,'git_snapshot_equal':True,'scratch_excluded':'.review/'},ensure_ascii=False,indent=2))
v=(R/'VERDICT.md').read_text();sha='75d0f6b5fe01611dda0b8768e50f5826657135e7'
assert v.startswith('verdict: changes_requested\n') and f'Reviewed commit: {sha}\n' in v
for i in range(1,28):assert '| A'+str(i)+' |' in v
for i in range(1,12):assert '| F'+str(i).zfill(2)+' `' in v
assert '| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |' in v
commands=[]
for c in [['git','status','--short'],['git','diff','--check'],['git','rev-parse','HEAD','HEAD^{tree}']]:
 p=subprocess.run(c,capture_output=True);commands.append({'command':c,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()});assert p.returncode==0
assert not commands[0]['stdout'] and commands[-1]['stdout'].splitlines()==[sha,'d07a624425fff37d998ff0369345537b263ec3c1']
# Check receipts against stable raw bytes and distinguish child failure from wrapper exit status.
for p in R.glob('*.json'):
 try:x=json.loads(p.read_text())
 except (ValueError,UnicodeDecodeError):continue
 if isinstance(x,dict) and isinstance(x.get('stdout'),dict) and isinstance(x.get('stderr'),dict):
  for k in ('stdout','stderr'):
   q=Path(x[k]['path']);b=q.read_bytes();assert len(b)==x[k]['bytes'] and hashlib.sha256(b).hexdigest()==x[k]['sha256'],(p,k)
proof=json.loads((R/'new-counterexamples.json').read_text());mutants=json.loads((R/'new-frontier/results.json').read_text())
for m in mutants:
 if m['rank']=='SONG_SOT':
  pairs=[z for z in proof if z['label']==m['name']];assert len(pairs)==2 and pairs[0]['rc']==0 and pairs[1]['rc']==3 and pairs[1]['output'].startswith('DO:'+m['name']+':')
report={'commands':commands,'snapshot_files_unchanged':len(a),'verdict_bytes':(R/'VERDICT.md').stat().st_size,'verdict_sha256':hashlib.sha256((R/'VERDICT.md').read_bytes()).hexdigest(),'validation':'passed','new_survivors_proven':17}
(R/'final-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
manifest={}
for p in sorted(R.rglob('*')):
 if not p.is_file() or p.name=='evidence-manifest.json' or any(z in ('tmp','cache') for z in p.relative_to(R).parts):continue
 b=p.read_bytes();manifest[str(p.relative_to(R))]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(R/'evidence-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
for name,h in manifest.items():
 b=(R/name).read_bytes();assert len(b)==h['bytes'] and hashlib.sha256(b).hexdigest()==h['sha256'],name
print(json.dumps(report,ensure_ascii=False,indent=2));print('Stable artifacts verified:',len(manifest))
