from pathlib import Path
import subprocess,sys,json,os
R=Path(__file__).resolve().parent
p=R/'prior2/trace_c44.py';s=p.read_text().replace('assert len(rows)==5','assert len(rows)==13').replace("print('c44: 5/5 nhánh có gọi công cụ và có assertion; steps YAML luôn list; không number=0')","print('c44: 13/13 nhánh gọi công cụ và assertion; có zero/âm/bool/container')")
p.with_name('trace_c44_current.py').write_text(s)
s=(R/'remaining_survivors.py').read_text().replace("('log_group_close_exact','suffix')","('L3_endgroup_startswith','suffix')")
s=s.replace("R/'frontier'/(name+'.py')", "R/('mutants' if name=='L3_endgroup_startswith' else 'frontier')/(name+'.py')")
(R/'remaining_survivors_current.py').write_text(s)
rows=[]
for name,path in [('frontier-proofs-final',R/'prove_frontier.py'),('prove-last-final',R/'prove_last.py'),('remaining-survivors-final',R/'remaining_survivors_current.py'),('trace-final',p.with_name('trace_c44_current.py'))]:
 cmd=[sys.executable,'-B',str(path)];q=subprocess.run(cmd,capture_output=True)
 rows.append({'label':name,'command':cmd,'rc':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode()})
 (R/'close-legacy-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(name,q.returncode,flush=True)
# Verify child acceptance, not the driver's outer rc.
z=json.loads((R/'prior2/reviewer-cases-r4.json').read_text())
assert len(z)==15 and all(x['rc']==(0 if x['source']=='candidate' else 3) and (x['source']=='candidate' or x['output'].startswith('DO:'+x['case']+':')) for x in z)
assert all(r['rc']==0 for r in rows),rows
print('legacy closure assertions DAT')
