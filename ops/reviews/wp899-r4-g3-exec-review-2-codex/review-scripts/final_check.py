from pathlib import Path
import json,subprocess,re,hashlib
R=Path(__file__).resolve().parent
start=json.loads((R/'snapshot-start.json').read_text())
end=json.loads((R/'snapshot-end.json').read_text())
delta=[p for p in sorted(start['files'].keys()|end['files'].keys()) if start['files'].get(p)!=end['files'].get(p)]
assert not delta,delta
assert start['git']==end['git']
comparison={'files':len(start['files']),'delta':delta,'git_equal':True,
            'scope':'checkout outside .git and .review, including tracked, untracked, ignored; .git through HEAD/tree/status/index/diff'}
(R/'snapshot-comparison.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2))
v=R/'VERDICT.md';s=v.read_text()
assert s.startswith('verdict: changes_requested\n')
assert 'P0=0, P1=1, P2=0, P3=0' in s
assert 'LẶP LỚP' in s and 'DỪNG HẲN' in s
for n in range(1,28):assert f'| A{n} ' in s,n
for n in range(1,12):assert f'| F{n:02d} ' in s,n
assert subprocess.run(['git','rev-parse','HEAD','HEAD^{tree}'],capture_output=True,check=True).stdout.decode().splitlines()==[
 '52e9573d0bd401a629a031a9c32df7bfd17c27c1','64e23a976f261ecdc6ab3535f6561536df3dc765']
p=subprocess.run(['git','status','--porcelain=v1','--untracked-files=all'],capture_output=True,check=True)
assert not p.stdout
mut=json.loads((R/'mutants/results.json').read_text())
assert len(mut)==101
assert sum(x['rank']=='GIET' for x in mut)==99
assert all(x['baseline']['rc']==0 for x in mut)
for path in ('shape-zero-audit.json','shape-audit.json'):
 rows=json.loads((R/path).read_text())
 for row in rows:
  if row['rank']=='SONG_SOT':
   assert len(row['cases'])==44 and all(x['rc']==0 for x in row['cases'])
   assert any(c['rc']==3 and c['output'].startswith('DO:'+c['case']+':') for c in row['counterexamples'])
marker='\n**Snapshot cuối.**'
s=s.split(marker)[0]
s+=marker+' `snapshot-start.json`, `snapshot-end.json`, `snapshot-comparison.json` so size/SHA-256 **6170 tệp** ngoài `.git/` và output `.review/`, gồm ignored/untracked và toàn `.review-input/`: **0 delta**. HEAD/tree đúng OID đầu verdict; Git status không ignored, tracked diff và cached diff rỗng, rc0; danh sách ignored đầu/cuối giống nhau (`.codex/`, `.review-input/`, `.review/`). Metadata `.git/` không được băm toàn bộ, kiểm bằng HEAD/tree/status/index/diff. Hai snapshot chỉ chứng minh không có delta quan sát ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên. Không có repo nguồn ngoài checkout nào được cấp để quan sát. `evidence-manifest.json` băm hiện vật ổn định của lượt này; không băm rollout đang ghi để thay receipt sau run.\n'
v.write_text(s,encoding='utf-8')
files={str(p.relative_to(R)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in R.rglob('*') if p.is_file() and p.name!='evidence-manifest.json'}
(R/'evidence-manifest.json').write_text(json.dumps(files,ensure_ascii=False,indent=1))
print('VERDICT validated:',len(v.read_bytes()),'bytes;',hashlib.sha256(v.read_bytes()).hexdigest())
print('Snapshot:',len(start['files']),'files, 0 delta; HEAD/tree unchanged; git status clean')
print('Mutants: 99 GIET + 2 expected self-checks; 2 reviewer survivors on 44/44 confirmed')
print('Artifacts hashed:',len(files))
