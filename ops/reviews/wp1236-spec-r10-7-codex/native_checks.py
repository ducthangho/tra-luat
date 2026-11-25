import concurrent.futures,hashlib,json,os,subprocess,sys,time
from pathlib import Path
from generate_review import W,R,M,ENV
T=M/'ops/gate_output_doi_chieu_test.py';D=R/'ops/reviews/wp1236-r10-soan'
a=[json.loads(x) for x in (W/'pilot_subset.jsonl').read_text().splitlines()];P={x['id']:x for x in map(json.loads,(D/'pilot_c2d606b_kq.jsonl').read_text().splitlines()) if 'id' in x}
# Execute a native test process, no YAML memo or altered dispatcher; existing mutants only.
def one(m):
 pth=W/'native_sources'/f"{hashlib.sha256(m['id'].encode()).hexdigest()}.py";pth.parent.mkdir(exist_ok=True);pth.write_text(m['src'])
 case=P[m['id']]['giet'][0];cmd=[sys.executable,'-B',str(T),'--mot-ca',case];st=time.monotonic();p=subprocess.run(cmd,cwd=W,env=dict(ENV,GATE_OUTPUT_DOI_CHIEU_MA=str(pth)),capture_output=True)
 return {'id':m['id'],'case':case,'command':cmd,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),'seconds':time.monotonic()-st,'positive':p.returncode==3 and f'DO:{case}:' in p.stdout.decode()}
# Use at most two extra CPUs alongside the 4-way pilot.
rows=[x for x in a if P[x['id']]['phan_hang']=='GIET']
with concurrent.futures.ThreadPoolExecutor(2) as ex:r=list(ex.map(one,rows))
(W/'native_target_replays.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print('NATIVE_KILLS',len(r),sum(x['positive'] for x in r),flush=True)
# Baseline records every actual case result with the unmodified product SafeLoader.
code='''import importlib.util,json,sys,time
p=sys.argv[1]
s=importlib.util.spec_from_file_location("godc_native",p);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
rows=[]
for c in m.CA:
 st=time.monotonic();rc,out=m.chay_ca(c);rows.append({"case":c,"rc":rc,"output":out,"seconds":time.monotonic()-st})
print(json.dumps(rows,ensure_ascii=False))
sys.exit(0 if rows and all(x["rc"]==0 for x in rows) else 1)
'''
p=subprocess.run([sys.executable,'-B','-c',code,str(T)],cwd=W,env=ENV,capture_output=True);(W/'baseline_cases.json').write_bytes(p.stdout);(W/'baseline.stderr').write_bytes(p.stderr)
(W/'baseline_receipt.json').write_text(json.dumps({'command':[sys.executable,'-B','-c',code,str(T)],'rc':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest()},ensure_ascii=False,indent=2))
print('BASELINE',p.returncode,len(json.loads(p.stdout)))
