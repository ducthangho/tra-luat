import pathlib,subprocess,os,shutil,json
R=pathlib.Path.cwd();O=R/'out';S=R/'cay-kho';B='48d372e14f190dae83a75ccbca8ee9a0b25635c5';(O/'tmp').mkdir(exist_ok=True)
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(O/'tmp'),'GIT_OPTIONAL_LOCKS':'0'}
def call(args,cwd=R):
 p=subprocess.run(args,cwd=cwd,capture_output=True,text=True,env=env);print('CMD',args,'RC',p.returncode,'OUTPUT',p.stdout.strip(),p.stderr.strip(),flush=True);return p
for name in ['base','prototype']:
 p=O/name;assert call(['git','clone','--shared','--no-checkout','-q',str(R/'kho.git'),str(p)]).returncode==0
 assert call(['git','config','core.abbrev','7'],p).returncode==0
 assert call(['git','checkout','-q','--detach',B],p).returncode==0
assert call(['git','apply','--index',str(S/'ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch')],O/'prototype').returncode==0
for name in ['base','prototype']:
 for cmd in ['doctrine-scan','adr-song']:
  call(['/usr/bin/python3','-B','.claude/dev/packet_loop.py',cmd,'--root','.'],O/name)
call(['git','diff','--cached','--numstat'],O/'prototype');call(['git','diff','--cached','--check'],O/'prototype')
shutil.copyfile(S/'ops/specs/wp1466/review/r7-l7/evidence-independent.py',O/'independent.py')
# Reuse prior independent parser verbatim; it reads current r8 and the new private copies.
call(['/usr/bin/python3','-B',str(O/'independent.py')])
# Exact reviewed SHA parity, source command is read-only; second checkout only changes under out.
assert call(['git','checkout','-q','--detach','e215940d15286add6fe30947cfccda09a09d82c0'],O/'base').returncode==0
for repo in [S,O/'base']:
 for cmd in ['doctrine-scan','adr-song']:
  call(['/usr/bin/python3','-B','.claude/dev/packet_loop.py',cmd,'--root','.'],repo)
