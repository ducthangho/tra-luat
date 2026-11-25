from pathlib import Path
import subprocess,sys,os,importlib.util,tempfile,json
O=Path(__file__).resolve().parent;P=O/'prototype';D=O/'f14';D.mkdir(exist_ok=True);sys.dont_write_bytecode=True
sys.path.insert(0,str(P/'.claude/dev'));import packet_loop_test as t
src=t.CANONICAL.read_text();needle,repl,_=t.MUTANTS['inv_bo_che_khong_render'];assert src.count(needle)==1
mut=D/'packet_loop.py';mut.write_text(src.replace(needle,repl,1));(D/'launcher.py').write_text((P/'.claude/dev/launcher.py').read_text())
goc=(P/'docs/PROTOCOL_DA_PHIEN.md').read_text();b0=goc.index('| INV | bất biến');b1=goc.index('\n\n',b0)
# Công thức fixture được chép nguyên từ nguyên mẫu r2 ma_tran.py:27 do tác giả cung cấp.
fixture=goc[:b0]+'```\n'+goc[b0:b1]+'\n```'+goc[b1:]
r=D/'root';(r/'docs').mkdir(parents=True,exist_ok=True);(r/'docs/PROTOCOL_DA_PHIEN.md').write_text(fixture)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(P/'.claude/dev'))
needle2,repl2,_=t.MUTANTS['inv_bo_khoa_K01'];assert src.count(needle2)==1
mut2=D/'without_K01.py';mut2.write_text(src.replace(needle2,repl2,1))
for label,script in [('baseline',t.CANONICAL),('without_mask',mut),('without_K01',mut2)]:
 p=subprocess.run([sys.executable,'-B',str(script),'doctrine-scan','--root',str(r)],capture_output=True,env=env)
 error=None
 try:t._doi_ly_do(9,p.returncode,p.stderr,'đơn vị khoá K01 ','bảng trong rào')
 except Exception as e:error=repr(e)
 print(label,'rc',p.returncode,'ASSERTION_PASS',error is None,'error',error,'stderr',p.stderr.decode(),flush=True)
print('R3_TABLE_FENCE_CASES',[n for n,f in t.CASES if n.startswith('doctrine_inv_') and 'bang' in n and 'rao' in n])
