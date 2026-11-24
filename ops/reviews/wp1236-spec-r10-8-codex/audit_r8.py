import ast
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

W = Path(__file__).resolve().parent
R = W.parent / 'repo'
TOOL = R / 'ops/reviews/wp1236-r10-soan/quet_dot_bien.py'
BANK = R / 'ops/reviews/wp1236-r10-soan/kho_dot_bien_reviewer_luot6.jsonl'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['TMPDIR'] = str(W / 'tmp')
(W / 'tmp').mkdir(exist_ok=True)
checks = []

def run(args):
    p = subprocess.run(args, cwd=W, capture_output=True, env=os.environ)
    rec = {'command': list(map(str, args)), 'rc': p.returncode,
           'stdout': p.stdout.decode('utf-8', 'replace'), 'stderr': p.stderr.decode('utf-8', 'replace')}
    checks.append(rec)
    return p

def read_jsonl(p):
    return [json.loads(s) for s in Path(p).read_text().splitlines() if s.strip()]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

for name in ['gate_output_doi_chieu.py', 'gate_output_doi_chieu_test.py']:
    p = run(['git', '-C', str(R), 'show', 'c2d606b:ops/' + name])
    assert p.returncode == 0
    (W / name).write_bytes(p.stdout)
    checks[-1]['stdout'] = f'copied exact blob to {W / name}; sha256={sha(W / name)}'

src = (W / 'gate_output_doi_chieu.py').read_text()
(W / 'reformatted.py').write_text('# reviewer formatting-only control\n\n' + ast.unparse(ast.parse(src)) + '\n')
(W / 'no_anchors.py').write_text('pass\n')
(W / 'duplicate_anchors.py').write_text(src + '\n' + src)
(W / 'renamed_local.py').write_bytes((R / 'ops/reviews/wp1236-spec-r10-7-codex/renamed_local.py').read_bytes())
bank = read_jsonl(BANK)
expected = ['kho:' + x['id'] for x in bank]
assert len(expected) == len(set(expected)) == 127
assert sha(BANK) == '6777b1d4fa59f8a2cdca9603bbf86338d440b6656076a0809c55a8c60954a3cd'
regression = {}
for target in ['gate_output_doi_chieu.py', 'reformatted.py', 'renamed_local.py', 'no_anchors.py', 'duplicate_anchors.py']:
    output = W / (target + '.regression.jsonl')
    p = run([sys.executable, '-B', str(TOOL), 'hoi-quy', str(BANK), '-', str(W / target), '--ra', str(output)])
    assert p.returncode == 0
    rows = read_jsonl(output)
    actual = [x['id'] for x in rows]
    assert actual == expected
    assert all('src' in x or (x['trang_thai'] == 'KHONG_AP_DUNG' and x['ly_do']) for x in rows)
    assert all(hashlib.sha256(x['src'].encode()).hexdigest() == x['sha256'] for x in rows if 'src' in x)
    regression[target] = {'rows': len(rows), 'unique_ids': len(set(actual)), 'id_order_matches_bank': True,
                          'applicable': sum('src' in x for x in rows),
                          'not_applicable': [x['id'] for x in rows if 'src' not in x],
                          'source_hashes_match': True, 'file': str(output), 'sha256': sha(output)}
native = read_jsonl(W / 'gate_output_doi_chieu.py.regression.jsonl')
formatted = read_jsonl(W / 'reformatted.py.regression.jsonl')
assert [x['sha256'] for x in native] == [x['sha256'] for x in formatted]
for i in [1, 2]:
    p = run([sys.executable, '-B', str(TOOL), 'sinh', str(W / 'gate_output_doi_chieu.py'), '--ra', str(W / f'manifest{i}.jsonl')])
    assert p.returncode == 0
assert sha(W / 'manifest1.jsonl') == sha(W / 'manifest2.jsonl')
manifest = read_jsonl(W / 'manifest1.jsonl')
for label, selected in [('all_no_src', []), ('one_src', [0])]:
    rows = [dict(m) if i in selected else {k:v for k,v in m.items() if k != 'src'} for i,m in enumerate(manifest)]
    path = W / (label + '.jsonl')
    path.write_text(''.join(json.dumps(m, ensure_ascii=False) + '\n' for m in rows))
    p = run([sys.executable, '-B', str(TOOL), 'chay', str(path), str(W / 'gate_output_doi_chieu_test.py'), '--goc', str(W / 'gate_output_doi_chieu.py'), '--ra', str(W / (label + '.kq.jsonl'))])
    assert p.returncode == 2 and b'HOAN_TAT' not in p.stdout

pilot = read_jsonl(R / 'ops/reviews/wp1236-r10-soan/pilot_c2d606b_kq.jsonl')
inventory = {m['id']: m['sha256'] for m in manifest + native}
results = [m for m in pilot if 'id' in m]
assert len(results) == len(inventory) == 927
assert all(inventory[x['id']] == x['sha256'] for x in results)
assert set(inventory) == {x['id'] for x in results}
counts = dict(collections.Counter(x['phan_hang'] for x in results))

spec = (W.parent / 'SPEC.md').read_text()
table_a = spec.split('### Đợt A —')[1].split('### Đợt B —')[0]
case_ids = re.findall(r'^\| (A[12]-\d+)(?= )', table_a, re.M)
assert len(case_ids) == len(set(case_ids)) == 30
mutants = []
for m in re.finditer(r'\bm(\d+)(?:…m(\d+)|–m(\d+))?', table_a):
    a, b = int(m[1]), int(m[2] or m[3] or m[1])
    mutants.extend(range(a, b+1))
assert set(mutants) == set(range(1,51))
matrix = spec.split('### Ma trận chốt–ca–đột biến')[1].split('### Đợt A —')[0]
law_ids = re.findall(r'^(\d)\. \*\*', matrix, re.M)
assert law_ids == ['1','2','3','4','5']
base = '8048551a9b1eb886c126d2a1a4df0f95fb285964'
p = run(['git','-C',str(R),'diff','--numstat',base,'c2d606b','--','ops/gate_output_doi_chieu.py','ops/gate_output_doi_chieu_test.py','.claude/dev/ci_dang_ky_test.py'])
assert p.returncode == 0
numstat = [s.split('\t') for s in p.stdout.decode().splitlines()]
assert sum(int(x[0]) for x in numstat) == 1324

refs = [{'line':i,'text':s} for i,s in enumerate(spec.splitlines(),1) if re.search(r'luật 3|bộ quét|HOAN_TAT|mẫu số|0 đột biến|153 sống|nang_tran',s)]
out = {'status':'passed', 'checks':checks, 'python':sys.version, 'tool_sha256':sha(TOOL), 'bank_sha256':sha(BANK),
       'regression':regression, 'formatting_same_127_source_hashes':True,
       'system_manifest':{'rows':len(manifest),'repeat_same_hash':True,'sha256':sha(W/'manifest1.jsonl')},
       'pilot':{'rows':len(results),'inventory_id_hash_matches':True,'counts':counts,'rerun':False},
       'counts':{'A_cases':case_ids,'A1':sum(s.startswith('A1-') for s in case_ids),'A2':sum(s.startswith('A2-') for s in case_ids),
                 'numbered_mutant_ids':sorted(set(mutants)),'matrix_laws':law_ids,'mandatory_laws':[1,2,4,5],
                 'numstat_r9':numstat, 'additions_r9':1324, 'r10_size':'KHONG_DO_DUOC'},
       'law3_reference_scan':refs}
(W / 'audit_r8.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'passed','regression':{k:{'rows':v['rows'],'applicable':v['applicable'],'not_applicable':len(v['not_applicable'])} for k,v in regression.items()},'manifest':len(manifest),'pilot':counts,'cases':len(case_ids),'numbered_mutants':len(set(mutants)),'r9_additions':1324},ensure_ascii=False,indent=2))
