from pathlib import Path
import subprocess,json,collections
root=Path('cay-kho').resolve();out=Path('evidence')
base=Path('/tmp/wp960-r4-ruff-base');head=Path('/tmp/wp960-r4-ruff-head')
for dst,rev in [(base,'44884446f71c89e25f9a72ac58e4f597db63c1ba'),(head,'3a52e6d194d08a755793cf449f393fb15b56757b')]:
 (dst/'ops').mkdir(parents=True,exist_ok=True)
 for name in ['bien_nhan_v2.py','bien_nhan_v2_test.py']:
  (dst/'ops'/name).write_bytes(subprocess.check_output(['git','-C',str(root),'show',f'{rev}:ops/{name}']))
 p=subprocess.run(['python3','-m','ruff','check','--no-cache','--select','F','--output-format','json',str(dst/'ops')],capture_output=True,text=True)
 (out/f'ruff-{dst.name}.json').write_text(p.stdout)
 items=json.loads(p.stdout);print(dst.name,'rc',p.returncode,'findings',[(x['code'],Path(x['filename']).name,x['location']['row'],x['message']) for x in items])
p=subprocess.run(['git','-C',str(root),'diff','--check','44884446f71c89e25f9a72ac58e4f597db63c1ba','HEAD'],text=True,capture_output=True);print('diff-check rc=',p.returncode,'stdout=',repr(p.stdout),'stderr=',repr(p.stderr))
p=subprocess.run(['git','-C',str(root),'diff','--name-only','43b96f0','HEAD'],text=True,capture_output=True);print('diff since merged parent rc=',p.returncode,'files=',p.stdout)
