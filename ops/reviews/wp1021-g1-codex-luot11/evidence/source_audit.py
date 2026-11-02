import ast
import hashlib
from pathlib import Path
import subprocess
import tempfile
from record import REPO, ROOT, ENV, record

lines = []
source = (REPO/'ops/bien_nhan_v2.py').read_text()
module = ast.parse(source)
helpers = [n for n in module.body if isinstance(n,ast.FunctionDef) and n.name == '_chon_bien_nhan']
assert len(helpers) == 1
helper = helpers[0]
calls = [(n.func.attr if isinstance(n.func,ast.Attribute) else n.func.id)
         for n in ast.walk(helper) if isinstance(n,ast.Call) and isinstance(n.func,(ast.Name,ast.Attribute))]
assert 'is_file' not in calls and all(x in calls for x in ('iterdir','lower','endswith','sorted'))
for fn_name in ('kiem','_sinh_no'):
    fn = next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name==fn_name)
    count = sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='_chon_bien_nhan' for n in ast.walk(fn))
    assert count==1
    lines.append(fn_name + ': helper calls=' + str(count))
lines.append('helper definitions=1; iterdir/lower/endswith/sorted present; is_file absent')
pattern = r'glob\("\*\.receipt\.yaml"\)'
r = subprocess.run(['rg','-n',pattern,'ops/bien_nhan_v2.py'],cwd=REPO,env=ENV,capture_output=True,text=True)
lines.append('rg -n '+repr(pattern)+' ops/bien_nhan_v2.py: rc='+str(r.returncode)+'; stdout='+repr(r.stdout))
assert r.returncode==1 and not r.stdout
with tempfile.TemporaryDirectory(prefix='rv1040-r11-grep-mutant-') as raw:
    p = Path(raw)/'bien_nhan_v2.py'
    p.write_text(source+'\nif False:\n    Path(".").glob("*.receipt.yaml")\n')
    r = subprocess.run(['rg','-n',pattern,str(p)],env=ENV,capture_output=True,text=True)
    lines.append('C9 reverse probe (scratch copy): rc='+str(r.returncode)+'; stdout='+r.stdout.strip())
    assert r.returncode==0 and len(r.stdout.splitlines())==1
for rel in ('AGENTS.md','docs/PROTOCOL_DA_PHIEN.md','.claude/dev/launcher.py'):
    data = [subprocess.check_output(['git','-C',str(REPO),'show',rev+':'+rel],env=ENV)
            for rev in ('HEAD','HEAD^1','HEAD^2')]
    lines.append(rel+': HEAD==P1='+str(data[0]==data[1])+'; HEAD==P2='+str(data[0]==data[2]))
    assert data[0]==data[1]==data[2]
merge = subprocess.check_output(['git','-C',str(REPO),'show','-s','--format=%H%n%P','c8ff9ed'],env=ENV,text=True)
lines.append('local merge commit:\n'+merge.strip())
r = subprocess.run(['git','-C',str(REPO),'merge-base','--is-ancestor','HEAD','c8ff9ed'],env=ENV)
lines.append('HEAD ancestor of c8ff9ed: rc='+str(r.returncode))
assert r.returncode==0
record('h12','M1/M2/C9 và các nguồn luật/provider mà cổng đọc',
       'PYTHONDONTWRITEBYTECODE=1 python3 evidence/source_audit.py', '\n'.join(lines))
