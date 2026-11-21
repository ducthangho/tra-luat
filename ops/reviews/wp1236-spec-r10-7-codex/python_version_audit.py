import ast,json,subprocess,hashlib,time
from generate_review import W,R,M,Q,K,G,ENV
out=[]
for name,args in [('hoi_quy_py312',['hoi-quy',K,'-',G,'--ra',W/'h_py312.jsonl']),('sinh_py312',['sinh',G,'--ra',W/'m_py312.jsonl'])]:
 cmd=['/usr/bin/python3.12','-B',str(Q),*map(str,args)];st=time.monotonic();p=subprocess.run(cmd,cwd=W,env=ENV,capture_output=True)
 (W/(name+'.stdout')).write_bytes(p.stdout);(W/(name+'.stderr')).write_bytes(p.stderr);out.append({'command':cmd,'rc':p.returncode,'seconds':time.monotonic()-st,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()});print(name,p.returncode,p.stdout.decode(),flush=True)
h=[json.loads(x) for x in (W/'h_py312.jsonl').read_text().splitlines()];a={x['id']:x for x in map(json.loads,(W/'m1.jsonl').read_text().splitlines())};b={x['id']:x for x in map(json.loads,(W/'m_py312.jsonl').read_text().splitlines())}
out={'receipts':out,'regression_312_applicable':sum('src' in x for x in h),'regression_not_applicable':[x for x in h if 'src' not in x],'manifest_313':len(a),'manifest_312':len(b),'id_diff':sorted(set(a)^set(b)),'same_ids_different_src_hash':sum(a[k]['sha256']!=b[k]['sha256'] for k in set(a)&set(b)),'per_op_312':{op:sum(x['op']==op for x in b.values()) for op in sorted({x['op'] for x in b.values()})}}
(W/'python_version_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print('VERSION_AUDIT_COMPLETE',out['regression_312_applicable'],out['manifest_312'],out['same_ids_different_src_hash'])
