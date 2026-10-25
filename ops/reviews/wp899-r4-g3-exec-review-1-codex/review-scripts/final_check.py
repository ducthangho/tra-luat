from pathlib import Path
import json,hashlib,subprocess,re
R=Path('.review');v=R/'VERDICT.md';s=v.read_text()
# Classify the inherited F08 scripts using their exact target result.
old=[]
for n in (1,2):
 for row in json.loads((R/f'old{n}/extra-mutants/results.json').read_text()):
  bad=[c for c in row['cases'] if c['rc']];ok=len(row['cases'])==43 and len(bad)==1 and bad[0]['case']=='c34_git_blob_that' and bad[0]['rc']==3 and bad[0]['output'].startswith('DO:c34_git_blob_that:')
  old.append({'round':n,'name':row['name'],'rank':'GIET' if ok else 'HONG','green':43-len(bad),'target':bad})
assert all(r['rank']=='GIET' for r in old)
(R/'inherited-f08-classified.json').write_text(json.dumps(old,ensure_ascii=False,indent=2))
s=s.replace('Chạy lại hai script extra_mutants r3 trên43 ca, đọc chi tiết ở evidence tương ứng.', 'Chạy lại hai script extra_mutants r3 trên43 ca: mỗi mutant chỉ đỏ c34 (rc3/DO đúng ca),42 ca khác xanh; `inherited-f08-classified.json` giữ phân hạng, không nhận nhãn CHECK_OUTPUT thô của script làm GIET.')
s=s.replace('mỗi bản85 nhóm;', 'mỗi bản85 nhóm;')
v.write_text(s)
assert s.startswith('verdict: changes_requested\n')
assert re.search(r'^reviewed_sha: [0-9a-f]{40}$',s,re.M)
for n in range(1,28):assert f'| A{n} ' in s
for n in range(1,9):assert f'| F{n:02d} ' in s
for n in range(9,12):assert f'F{n:02d}' in s
p=subprocess.run(['git','rev-parse','HEAD','HEAD^{tree}'],capture_output=True,check=True)
assert p.stdout.decode().splitlines()==['ca11a6f1a7eb5286eeb6efc730d99beb33e2dcd1','68a0f79e542d383acebf38313be7ea51c697ccfd']
p=subprocess.run(['git','status','--porcelain=v1','--untracked-files=all'],capture_output=True,check=True);assert not p.stdout
files={str(p.relative_to(R)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in R.rglob('*') if p.is_file() and p.name!='evidence-manifest.json'}
(R/'evidence-manifest.json').write_text(json.dumps(files,ensure_ascii=False,indent=1))
print('VERDICT validated',len(v.read_bytes()),'bytes',hashlib.sha256(v.read_bytes()).hexdigest());print('Artifacts hashed',len(files));print('Inherited F08',[(x['round'],x['name'],x['rank']) for x in old]);print('HEAD/tree match; git status clean')
