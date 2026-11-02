from audit_common import *

before=json.loads((EVID/'repo-before.json').read_text())
after={str(p.relative_to(REPO)):sha(p.read_bytes()) for p in REPO.rglob('*') if p.is_file() and '.git' not in p.relative_to(REPO).parts}
diffcheck=run(['git','diff','--check',BASE,'HEAD'])
mut=json.loads((EVID/'mutations.json').read_text())
receipts=json.loads((EVID/'receipts.json').read_text())
classifier={ref:git('rev-parse',ref+':ops/lease_publish.py').decode().strip() for ref in [HEAD]+[x['reviewed_sha'] for x in receipts]}
result={'head':git('rev-parse','HEAD').decode().strip(),'tree':git('rev-parse','HEAD^{tree}').decode().strip(),
    'status':git('status','--porcelain','--untracked-files=all').decode(),
    'changed_files':[p for p in before.keys()&after.keys() if before[p]!=after[p]],
    'added_files':sorted(after.keys()-before.keys()),'removed_files':sorted(before.keys()-after.keys()),
    'file_count_before':len(before),'file_count_after':len(after),
    'diff_check_rc':diffcheck.returncode,'diff_check_output':(diffcheck.stdout+diffcheck.stderr).decode(),
    'input_diff_matches':git('diff',BASE,HEAD)==(ROOT/'DIFF.patch').read_bytes(),
    'mutant_status':git('status','--porcelain','--untracked-files=all',cwd=ROOT/'work/mutant').decode(),
    'mutations':len(mut),'mutation_rejections':sum(x[k]['correctly_rejected'] for x in mut for k in ('bien-nhan','direct')),
    'classifier_blob_ids':classifier,'classifier_same_at_all_reviewed':len(set(classifier.values()))==1,
    'commits':git('log','--format=%H %s',BASE+'..'+HEAD).decode().splitlines()}
save('final-integrity.json',result)
print(json.dumps(result,ensure_ascii=False))
assert result['head']==HEAD
assert not result['changed_files'] and not result['added_files'] and not result['removed_files']
assert not result['status'] and not result['mutant_status']
assert result['mutations']==4 and result['mutation_rejections']==8
assert result['diff_check_rc']==0 and result['input_diff_matches']
append('Kiểm cuối — `PYTHONDONTWRITEBYTECODE=1 python3 final_audit.py`: rc=0; '+str(len(before))+' tệp clone gốc trước/sau, changed/added/removed=[]; status rỗng; HEAD/tree giữ nguyên; DIFF.patch vẫn khớp; `git diff --check f4b513d HEAD` rc=0, không output. Bản đột biến đã hồi nguyên, status rỗng; 4 đột biến/8 lần chặn đúng tên. Classifier có cùng blob tại HEAD và cả bốn reviewed_sha. Kết quả: `evidence/final-integrity.json`.')
