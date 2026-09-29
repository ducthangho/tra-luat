import datetime as dt, hashlib, importlib.util, json, pathlib, shutil, subprocess, sys
B=pathlib.Path(__file__).resolve().parents[1]; O=B/'do-review8'; P=B/'cay-kho/ops/reviews/pr468-hoso-4-packet-review-6-codex'; R=O/'rig'; S=R/'source'; D=R/'do-review'
S.mkdir(parents=True,exist_ok=True); D.mkdir(exist_ok=True)
for name in ['harness.py','attack_h.py','extra_checks.py']: shutil.copyfile(P/name,S/name)
for name in ['real-results.json','nhanh-rerun.json']: shutil.copyfile(P/name,D/name)
shutil.copytree(P/'outputs',D/'outputs',dirs_exist_ok=True)
for name,target in [('tai-lieu',B/'tai-lieu'),('cay-kho',B/'cay-kho')]:
 p=R/name
 if not p.exists(): p.symlink_to(target,target_is_directory=True)
runs=[]
for name in ['harness.py','attack_h.py','extra_checks.py']:
 r=subprocess.run([sys.executable,'-B',str(S/name)],cwd=B,capture_output=True); (O/(name+'.log')).write_bytes(r.stdout+r.stderr)
 runs.append(dict(script=name,rc=r.returncode,source_identical=(P/name).read_bytes()==(S/name).read_bytes()))
 assert r.returncode==0,r.stderr
sys.path.insert(0,str(S)); sys.dont_write_bytecode=True
import harness as h
report={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'scripts':runs,'corpus':json.loads((D/'attack-h-summary.json').read_text()),'corpus_byte_matches':{n:(P/n).read_bytes()==(D/n).read_bytes() for n in ['attack-h-cases.json','attack-h-summary.json']},'blocks':{n:hashlib.sha256((D/n).read_bytes()).hexdigest() for n in ['h_tong.py','h_predicate.py']}}
real=json.loads((P/'real-results.json').read_text()); rerun=json.loads((P/'nhanh-rerun.json').read_text()); that=json.loads((P/'d2-that-results.json').read_text())
report['d2']=[]
for row in real:
 p=row['path']; src=P/row['output']; meta=row
 if p==rerun['path']: src=P/'outputs/nhanh_don_duoc_test.rerun.stdout'; meta=rerun
 if p in that['ket_qua']: meta=that['ket_qua'][p]; src=P/'outputs-that'/src.name
 raw=src.read_bytes(); entry={'path':p,'source':str(src.relative_to(B)),'rc_recorded':meta['rc'],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'H_red':h.replay(p,raw.decode(),rc=meta['rc']),'BASE_red':h.replay(p,raw.decode(),rc=meta['rc'],base=True)}
 entry['bytes_match']=meta.get('bytes',len(raw))==len(raw); entry['hash_match']=meta.get('sha256',entry['sha256'])==entry['sha256']; report['d2'].append(entry)
long='9'*5000; pre='.claude/hooks/pretooluse_guard_test.py'; mcp='.claude/dev/mcp_gh_test.py'
fixtures={'pre-ca':(pre,f'TONG: CA {long}/{long} dat · DOT BIEN 34/34 bi giet\nTONG: DAT\n'),'pre-mutant':(pre,f'TONG: CA 39/39 dat · DOT BIEN {long}/{long} bi giet\nTONG: DAT\n'),'mcp-ca':(mcp,f'CA         : {long}/{long} đạt · 0 đỏ · ĐẠT\nĐỘT BIẾN   : đã đo 54/54 tập giết · ĐẠT\nTỔNG: ĐẠT\n'),'mcp-mutant':(mcp,f'CA         : 42/42 đạt · 0 đỏ · ĐẠT\nĐỘT BIẾN   : đã đo {long}/{long} tập giết · ĐẠT\nTỔNG: ĐẠT\n')}
def run(p,t,base):
 try:return h.replay(p,t,base=base)
 except Exception as e:return type(e).__name__
report['d9']={k:dict(path=p,text=t,BASE=run(p,t,True),H=run(p,t,False)) for k,(p,t) in fixtures.items()}
report['MOI']=dict(count=len(h.C.MOI),span_preserved=sum(h.C.MOI[p][0]==s for p,s in h.BASE_MOI.items()),windows_forms=sum(map(len,h.C.MOI_WINDOWS.values())))
report['mutants']=[{k:v for k,v in x.items() if k not in ['changed_cases','exceptions']} for x in json.loads((D/'extra-checks.json').read_text())['mutants_on_1213']]
(O/'replay-h.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({**report,'d9':{k:{a:b for a,b in v.items() if a!='text'} for k,v in report['d9'].items()}},ensure_ascii=False,indent=2))
