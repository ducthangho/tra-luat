from pathlib import Path
import subprocess,sys,json,os,hashlib,runpy
R=Path(__file__).resolve().parent
p=R/'prior2/trace_c44.py';s=p.read_text().replace('assert len(rows)==5','assert len(rows)==13').replace("print('c44: 5/5 nhánh có gọi công cụ và có assertion; steps YAML luôn list; không number=0')","print('c44: 13/13 nhánh có gọi công cụ; gồm zero/âm/bool và YAML absent/null/int')");p.with_name('trace_c44_current.py').write_text(s)
q=subprocess.run([sys.executable,'-B',str(p.with_name('trace_c44_current.py'))],capture_output=True);(R/'trace-current.stdout').write_bytes(q.stdout);(R/'trace-current.stderr').write_bytes(q.stderr)
print('trace-current',q.returncode,q.stdout.decode(),q.stderr.decode())
p=R/'prior1/registry_check.py';s=p.read_text().replace("sample.replace('43/43','42/43')","sample.replace('45/45','44/45')").replace("sample.replace('87/87','0/0')","sample.replace('125/125','0/0')");p.write_text(s)
q2=subprocess.run([sys.executable,'-B',str(p)],capture_output=True);(R/'registry-current.stdout').write_bytes(q2.stdout);(R/'registry-current.stderr').write_bytes(q2.stderr)
print('registry-current',q2.returncode)
# Independently check outcomes from the legacy verifier; a driver rc=0 is not acceptance.
z=json.loads((R/'prior2/reviewer-cases-r4.json').read_text());print('legacy reviewer baseline',[(a['case'],a['rc']) for a in z if a['source']=='candidate']);print('legacy reviewer mutant',[(a['case'],a['source'],a['rc']) for a in z if a['source']!='candidate'])
assert all(a['rc']==0 if a['source']=='candidate' else a['rc']==3 and a['output'].startswith('DO:'+a['case']+':') for a in z)
# Script inventory shows exact duplicate producers and separates historical output renderers from properties.
inv=[]
for n in (1,2):
 for p in (R.parent/f'.review-input/r4-luot{n}').glob('*.py'):
  inv.append({'round':n,'path':str(p.relative_to(R.parent)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':'historical_infrastructure' if p.name in ('write_verdict.py','final_check.py','prepare.py','snapshot.py','run.py','emit.py') else 'verification'})
(R/'prior-script-inventory.json').write_text(json.dumps(inv,ensure_ascii=False,indent=2))
(R/'close-prior.json').write_text(json.dumps({'trace_rc':q.returncode,'registry_rc':q2.returncode,'legacy_verifier_assertion':'passed'},indent=2))
