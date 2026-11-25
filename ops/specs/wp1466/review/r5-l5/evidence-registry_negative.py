from pathlib import Path
import subprocess,os,sys
O=Path(__file__).resolve().parent;R=O.parent/'cay-kho';q=O/'registry-negative';env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for cmd in [['git','clone','--shared','--no-checkout',str(O.parent/'kho.git'),str(q)],['git','-C',str(q),'checkout','--detach','48d372e14f190dae83a75ccbca8ee9a0b25635c5'],['git','-C',str(q),'apply','-p1',str(R/'ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch')]]:
 r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0,r.stderr
p=q/'.claude/dev/packet_loop_test.py';s=p.read_text();marker='\n\nif __name__ ==';assert marker in s
for name,new in [('overwrite_old_mutant',s.replace(marker,'\nMUTANTS.update({"r1187_drop_doc_guard": ("a", "b", [])})\n'+marker,1)),('reverse_old_cases',s.replace(marker,'\nCASES.reverse()\n'+marker,1))]:
 p.write_text(new)
 r=subprocess.run([sys.executable,'-B',str(O/'sc/so_dang_ky.py'),str(O/'base'),str(q)],capture_output=True,text=True,env=env);print(name,'rc',r.returncode,r.stdout.strip(),r.stderr[-200:])
p.write_text(s)
