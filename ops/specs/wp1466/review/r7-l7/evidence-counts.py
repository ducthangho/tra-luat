from pathlib import Path
import os,sys,subprocess,json,re,ast,hashlib
O=Path(__file__).resolve().parent;S=O.parent/'cay-kho';P=O/'prototype';env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'tmp'))
for case in ['policy_co_mat','tien_to_thu_muc','tien_to_khong_gach','khac_kieu_chu','chi_effective','planned_gach_nguoc','lien_ket_thu_muc']:
 k=O/'tmp/fx2'/case/'kho';r=subprocess.run([sys.executable,'-B',str(k/'ops/lease_publish.py'),'ai-dang-giu','.claude/dev/packet_loop.py','--root',str(k)],capture_output=True,text=True,env=env)
 print('RAW_MATCHER',case,r.returncode,(r.stdout+r.stderr).strip().splitlines()[-1])
sys.dont_write_bytecode=True;sys.path.insert(0,str(P/'.claude/dev'));import packet_loop_test as t,packet_loop_test_manh as m
new={k:v for k,v in t.MUTANTS.items() if k.startswith(('inv_','t1466_'))};newcases={n for n,f in t.CASES if n.startswith('doctrine_inv_')};alltargets=set().union(*(set(v[2]) for v in new.values()))
print('NEW_CASES',len(newcases),'NEW_MUTANTS',len(new),'TARGETED',len(newcases&alltargets),'MISSING',sorted(newcases-alltargets))
for name,(old,newtext,targets) in new.items():
 path=P/'.claude/dev'/('packet_loop_test.py' if name in t.MUTANTS_NHAM_TEST else 'packet_loop.py');print('MARKER',name,'OCCURRENCES',path.read_text().count(old),'TARGETS',len(targets))
for log in ['moi','cu']:
 text=(O/(log+'.log')).read_text();ok=re.findall(r'^\s+ok\s+(\S+) → giết (\d+) ca đích · 3 đối chứng khác họ còn sống',text,re.M)
 print('MUTANT_LOG',log,'OK',len(ok),'PASSED_FINAL','TỔNG: ĐẠT' in text,'KILL_COUNTS',dict(ok))
 print('BASELINE',log,[x for x in text.splitlines() if 'nền:' in x or 'BỎ QUA:' in x][:3])
spec=(S/'ops/specs/wp1466.md').read_text();history=spec.split('## 19.',1)[1];slugs=re.findall(r'^\| `([a-z0-9-]+)` · P[0-3] \|',history,re.M);print('HISTORICAL_CLASSES',len(slugs),len(set(slugs)))
for label,path in [('code','packet_loop.py'),('test','packet_loop_test.py')]:
 for root in ['base','prototype']:
  s=(O/root/'.claude/dev'/path).read_text();chars=[c for c in s if '\u3400'<=c<='\u9fff'];print('CJK',label,root,len(chars),sorted(set(chars)))
print('RUFF_VERSION',subprocess.run(['ruff','--version'],capture_output=True,text=True).stdout.strip())
