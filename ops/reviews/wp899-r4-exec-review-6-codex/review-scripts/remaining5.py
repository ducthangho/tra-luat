from pathlib import Path
import sys,subprocess,json,os
R=Path(__file__).resolve().parent;rows=[]
# Historical old counterexample source and closures, not historical verdict generators.
for n in (1,2):
 for name in ('boundary_current.py','composite_current.py'):
  p=R/f'prior{n}/old2'/name
  if p.exists():
   s=p.read_text().replace('r4review4/ws','r4review5/ws').replace('.review/prior2/old2/composite/runner-step.sh',f'.review/prior{n}/old2/composite/runner-step.sh');p.write_text(s)
for label,p,args in [('extra2',R/'prior2/extra_mutants_r4.py',[]),('shapezero',R/'prior2/shape_audit.py',[]),('shapecontainers',R/'prior2/shape_audit.py',['--containers']),('finishprobes',R/'prior2/finish_probes.py',[]),('reanchor',R/'repair_legacy_anchors.py',[]),('reviewercases',R/'prior2/verify_new_cases.py',[])]+[(f'prior{n}-{name}',R/f'prior{n}/old2'/name,[]) for n in (1,2) for name in ('boundary_current.py','composite_current.py')]:
 if not p.exists():continue
 cmd=[sys.executable,'-B',str(p),*args];q=subprocess.run(cmd,capture_output=True,timeout=1800)
 (R/(label+'.stdout')).write_bytes(q.stdout);(R/(label+'.stderr')).write_bytes(q.stderr)
 rows.append({'label':label,'command':cmd,'rc':q.returncode,'stdout_tail':q.stdout.decode('utf8','replace')[-2500:],'stderr_tail':q.stderr.decode('utf8','replace')[-1500:]});(R/'remaining5-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(label,q.returncode,flush=True)
