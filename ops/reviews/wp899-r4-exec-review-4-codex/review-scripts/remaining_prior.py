from pathlib import Path
import subprocess,sys,os,json,shutil
R=Path(__file__).resolve().parent
for n in (1,2):
 d=R/f'prior{n}';shutil.copy2(R/'suite.stdout.txt',d/'suite.stdout.txt')
 p=d/'registry_check.py';s=p.read_text().replace("sample.replace('44/44','43/44')","sample.replace('47/47','46/47')").replace("sample.replace('99/99','0/0')","sample.replace('155/155','0/0')")
 p.write_text(s)
 for f in ('composite_case.py','composite_current.py'):
  p=d/'old2'/f
  if p.exists():p.write_text(p.read_text().replace('.review/composite/runner-step.sh',str((p.parent/'composite/runner-step.sh').relative_to(R.parent))))
rows=[]
def run(label,cmd):
 p=subprocess.run(cmd,capture_output=True,timeout=1500)
 (R/(label+'.stdout')).write_bytes(p.stdout);(R/(label+'.stderr')).write_bytes(p.stderr)
 rows.append({'label':label,'command':cmd,'rc':p.returncode,'stdout':p.stdout.decode('utf8','replace')[-4000:],'stderr':p.stderr.decode('utf8','replace')[-1000:]})
 (R/'remaining-prior-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)); print(label,p.returncode,flush=True)
# Catalogue audit is byte-identical in rounds 1 and 2; .review/audit_mutants.py already executed it on this HEAD.
for n in (1,2):
 for name in ('registry_check.py','replay_q1.py'):
  run(f'prior{n}-{name}',[sys.executable,'-B',str(R/f'prior{n}'/name)])
run('composite-current-fixed',[sys.executable,'-B',str(R/'prior2/old2/composite_current.py')])
run('extra-original',[sys.executable,'-B',str(R/'prior2/extra_mutants_r4.py')])
run('shape-now',[sys.executable,'-B',str(R/'prior2/shape_audit.py')])
run('shape-containers-now',[sys.executable,'-B',str(R/'prior2/shape_audit.py'),'--containers'])
# Rebase legacy anchors only where the candidate replaced the implementation (not its property).
p=R/'prior2/extra_mutants_r4.py';s=p.read_text()
s=s.replace("'if any(s.get(\"name\") != ten_du_kien(y)', 'if False and any(s.get(\"name\") != ten_du_kien(y)'", "'if any(not _chuoi(s.get(\"name\")) or', 'if False and any(not _chuoi(s.get(\"name\")) or'")
s=s.replace("'re.search(\"GITHUB_(ENV|PATH)\", t[\"run\"])','re.search(\"GITHUB_ENV\", t[\"run\"])'", "'re.search(\"GITHUB_(ENV|PATH)\",','re.search(\"GITHUB_ENV\",'")
# The time mutants are prepared by finish_probes, which adapts to datetime checking.
p.with_name('extra_mutants_r4_adapted.py').write_text(s)
run('extra-adapted',[sys.executable,'-B',str(p.with_name('extra_mutants_r4_adapted.py'))])
run('finish-probes',[sys.executable,'-B',str(R/'prior2/finish_probes.py')])
run('reviewer-cases',[sys.executable,'-B',str(R/'prior2/verify_new_cases.py')])
run('trace-c44',[sys.executable,'-B',str(R/'prior2/trace_c44.py')])
