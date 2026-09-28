import ast
import hashlib
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(__file__).resolve().parent
ENV = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'GIT_CONFIG_COUNT': '1',
       'GIT_CONFIG_KEY_0': 'commit.gpgsign', 'GIT_CONFIG_VALUE_0': 'false'}

def run(name, cmd, inp=None):
    p = subprocess.run(cmd, cwd=ROOT, env=ENV, input=inp, capture_output=True)
    (OUT / (name+'.stdout')).write_bytes(p.stdout)
    (OUT / (name+'.stderr')).write_bytes(p.stderr)
    row = dict(name=name, command=cmd, rc=p.returncode, output=p.stdout.decode(errors='replace')[-2000:], stderr=p.stderr.decode(errors='replace')[-1000:])
    with (OUT/'checks.jsonl').open('a') as f: f.write(json.dumps(row, ensure_ascii=False)+'\n')
    print(json.dumps(row, ensure_ascii=False), flush=True)
    return p

def snap(name):
    r = {}
    for k, args in {'oids':['rev-parse','HEAD','HEAD^{tree}','origin/master'], 'status':['status','--porcelain=v1','--untracked-files=all','--ignored=matching'], 'diff':['diff','--binary'], 'index':['diff','--cached','--binary']}.items():
        p=run(name+'-'+k,['git',*args]); r[k]=hashlib.sha256(p.stdout).hexdigest()
    r['files']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts}
    (OUT/(name+'.json')).write_text(json.dumps(r, indent=2))

if sys.argv[2]=='snapshot': snap(sys.argv[3]); sys.exit()
if sys.argv[2]=='producer':
    blocks=[]
    for rev in ['5618f61c6ac2fa14aab52b0f5ce3d065aee8e022','origin/master','HEAD']:
        data=subprocess.check_output(['git','show',rev+':ops/lease_publish.py'],cwd=ROOT)
        tree=ast.parse(data)
        ds=[n for n in ast.walk(tree) if isinstance(n,ast.Dict) and any(isinstance(v,ast.Constant) and v.value=='thu_hoi_admission_receipt' for v in n.values)]
        assert len(ds)==1
        n=ds[0]; block=b''.join(data.splitlines(keepends=True)[n.lineno-1:n.end_lineno]); blocks.append(block)
        print(json.dumps(dict(rev=rev,start=n.lineno,end=n.end_lineno,bytes=len(block),sha256=hashlib.sha256(block).hexdigest(),keys=[k.value for k in n.keys])),flush=True)
    print('receipt_blocks_byte_equal',blocks[0]==blocks[1]==blocks[2]);sys.exit()

run('suite',[sys.executable,'-B','.claude/dev/doc_receipt_thu_hoi_test.py'])
run('registry',[sys.executable,'-B','.claude/dev/ci_dang_ky_test.py'])
run('ruff-version',[sys.executable,'-m','ruff','--version'])
paths=['.claude/dev/doc_receipt_thu_hoi.py','.claude/dev/doc_receipt_thu_hoi_test.py','.claude/dev/ci_dang_ky_test.py']
run('ruff-head',[sys.executable,'-m','ruff','check','--no-cache','--select','F',*paths])
base=subprocess.check_output(['git','show','origin/master:.claude/dev/ci_dang_ky_test.py'],cwd=ROOT)
run('ruff-base',[sys.executable,'-m','ruff','check','--no-cache','--select','F','--stdin-filename',str(ROOT/paths[-1]),'-'],base)
for gate in ['doctrine-scan','adr-song']:
    run(gate,[sys.executable,'-B','.claude/dev/packet_loop.py',gate,'--root','.'])
run('numstat',['git','diff','--numstat','origin/master..HEAD'])
run('diffcheck',['git','diff','--check','origin/master..HEAD'])
