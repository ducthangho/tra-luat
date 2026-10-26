from pathlib import Path
import sys,subprocess,json,os,shutil,time
R=Path(__file__).resolve().parent;root=R.parent
# The foreground remains free to report progress while the already running real suite finishes.
start=time.monotonic()
while not (R/'suite.stdout.txt').exists():
 if time.monotonic()-start>2400:raise RuntimeError('real suite stdout not produced within wait envelope')
 time.sleep(2)
sample=(R/'suite.stdout.txt').read_text();assert 'CA: 48/48 dat' in sample and 'DOT BIEN: 209/209 bi giet dung ly do' in sample and 'TONG: DAT' in sample
for n in (1,2):
 d=R/f'prior{n}';shutil.copy2(R/'suite.stdout.txt',d/'suite.stdout.txt')
 for name in ('boundary_current.py','composite_current.py'):
  src=R/'prior2/old2'/name;p=d/'old2'/name
  if not p.exists():shutil.copy2(src,p)
  s=p.read_text().replace('.review/prior2/old2/composite/runner-step.sh',f'.review/prior{n}/old2/composite/runner-step.sh');p.write_text(s)
 p=d/'run_old.py';s=p.read_text().replace("for script in ('r4_compare.py',)+ (('composite_case.py','boundary_case.py') if n==2 else ()):","for script in (('r4_compare_current.py' if (R/f'old{n}/r4_compare_current.py').exists() else 'r4_compare.py'),)+ (('composite_current.py','boundary_current.py') if n==2 else ()):");p.write_text(s)
rows=[]
jobs=[]
for n in (1,2):
 d=R/f'prior{n}'
 for name in ('run_old.py','registry_check.py'):jobs.append((f'prior{n}-{name}',d/name))
jobs += [('prove-frontier',R/'prove_frontier.py'),('prove-last',R/'prove_last.py'),('prove-new',R/'prove_new.py')]
for label,p in jobs:
 cmd=[sys.executable,'-B',str(p)];q=subprocess.run(cmd,capture_output=True,timeout=900)
 (R/(label+'-final.stdout')).write_bytes(q.stdout);(R/(label+'-final.stderr')).write_bytes(q.stderr)
 rows.append({'label':label,'command':cmd,'rc':q.returncode,'stdout':q.stdout.decode('utf8','replace')[-1500:],'stderr':q.stderr.decode('utf8','replace')[-1500:]});(R/'legacy-final-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(label,q.returncode,flush=True)
for n in (1,2):
 a=json.loads((R/f'prior{n}/old-cases-results.json').read_text());checks=[z for z in a if 'case' in z];assert len(checks)==12 and all(z['rc']==0 for z in checks),checks
 for z in a:
  if z.get('script') in ('composite_current.py','boundary_current.py'):assert z['rc']==0,z
 a=json.loads((R/f'prior{n}/registry-details.json').read_text());assert not a['normal'][0] and a['removed'][0] and a['accepts_suite'] and all(a['rejects_bad'].values()),a
print('legacy F02 24/24 cases; composite/boundary current, registry+negative+regex DAT; signer not measured if denied')
