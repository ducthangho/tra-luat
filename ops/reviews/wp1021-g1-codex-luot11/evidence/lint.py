from pathlib import Path
from collections import Counter
import difflib
import json
import subprocess
import tempfile
from record import ROOT, REPO, ENV, record

ruff = '/root/.local/bin/ruff'
files = ['ops/bien_nhan_v2.py', 'ops/bien_nhan_v2_test.py']
version = subprocess.check_output([ruff,'--version'],env=ENV,text=True).strip()
lines = [version, 'python3 -m ruff --version: /usr/bin/python3: No module named ruff',
         'Dùng executable Ruff có sẵn; không cài đặt và không tải mạng.']
with tempfile.TemporaryDirectory(prefix='rv1040-r11-ruff-base-') as raw:
    base_root = Path(raw)
    for p in files:
        target = base_root/p
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(subprocess.check_output(['git','-C',str(REPO),'show','3dfb973:'+p],env=ENV))
    result = {}
    for label, cwd in [('base',base_root),('head',REPO)]:
        cmd = [ruff,'check','--no-cache','--select','F','--output-format','json',*files]
        r = subprocess.run(cmd,cwd=cwd,env=ENV,capture_output=True,text=True)
        assert r.returncode in (0,1), r.stderr
        rows = json.loads(r.stdout)
        result[label] = rows
        (ROOT/'evidence'/('ruff-'+label+'.json')).write_text(r.stdout)
        lines += ['COMMAND: cwd='+str(cwd)+' '+ ' '.join(cmd),f'{label}: rc={r.returncode}; diagnostics={len(rows)}',
                  f'{label} codes='+str(dict(Counter(x['code'] for x in rows)))]
    def normalized(rows, root):
        return Counter((str(Path(x['filename']).relative_to(root)),x['code'],x['message']) for x in rows)
    before = normalized(result['base'],base_root)
    after = normalized(result['head'],REPO)
    added, removed = after-before, before-after
    lines += ['added='+str(dict(added)), 'removed='+str(dict(removed)),
              'delta_count='+str(sum(after.values())-sum(before.values()))]
    # Vị trí lỗi cũ cũng phải ánh xạ đúng qua diff, không chỉ cùng số lượng.
    mapped = {}
    for p in files:
        a = (base_root/p).read_text().splitlines()
        b = (REPO/p).read_text().splitlines()
        mp = {}
        for match in difflib.SequenceMatcher(None,a,b,autojunk=False).get_matching_blocks():
            for offset in range(match.size):
                mp[match.a+offset+1] = match.b+offset+1
        mapped[p] = mp
    old_locations = Counter()
    for x in result['base']:
        p = str(Path(x['filename']).relative_to(base_root))
        loc = x['location']
        old_locations[(p,x['code'],x['message'],mapped[p].get(loc['row']),loc['column'])] += 1
    new_locations = Counter((str(Path(x['filename']).relative_to(REPO)),x['code'],x['message'],
                             x['location']['row'],x['location']['column']) for x in result['head'])
    lines.append('diagnostics_equal_after_line_mapping='+str(old_locations == new_locations))
    assert not added and not removed and old_locations == new_locations
record('h07','Bare Ruff --select F: delta so cha master, so cả vị trí sau ánh xạ dòng',
       'PYTHONDONTWRITEBYTECODE=1 python3 evidence/lint.py', '\n'.join(lines))
