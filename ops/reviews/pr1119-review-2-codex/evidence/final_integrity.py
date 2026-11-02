from common import *
import re
original=S/'cay-kho';before=json.loads((E/'original-hashes.json').read_text())
after={str(p.relative_to(original)):digest(p.read_bytes()) for p in sorted(original.rglob('*')) if p.is_file()}
data=dict(original_files_before=len(before),original_files_after=len(after),changed=[p for p in before.keys()&after.keys() if before[p]!=after[p]],added=sorted(after.keys()-before.keys()),removed=sorted(before.keys()-after.keys()),original_status=git('status','--porcelain=v1',root=original).decode(),original_head=git('rev-parse','HEAD',root=original).decode().strip(),original_tree=git('rev-parse','HEAD^{tree}',root=original).decode().strip(),mutant_status=git('status','--porcelain=v1',root=S/'work/mutant').decode())
data['original_diff_check']=logged('original-diff-check',['git','diff','--check',BASE,'HEAD'],original)
data['warnings_equal']=(E/'base-direct.stderr').read_text().replace('/work/base/','/work/REV/')==(E/'head-direct.stderr').read_text().replace('/work/head/','/work/REV/')
data['gate_delta']={}
for name in ['bien-nhan','land','direct','doctrine','diff-check']:
    a=(E/f'base-{name}.stdout').read_text();b=(E/f'head-{name}.stdout').read_text()
    data['gate_delta'][name]=dict(stdout_equal=a==b,base=a if name=='bien-nhan' else a[-220:],head=b if name=='bien-nhan' else b[-220:])
mutation=json.loads((E/'mutations.json').read_text());verification=[]
for d in mutation:
    record=dict(receipt=d['receipt'],results=[])
    for g in d['gates']:
        out=(E/g['stdout']).read_text();err=(E/g['stderr']).read_text()
        lines=[l for l in err.splitlines() if l.lstrip().startswith(('ĐỎ ','AssertionError:'))]
        named=sorted(set(re.findall(r'([\w.-]+\.receipt\.yaml)', '\n'.join(lines))))
        direct='direct.py' in ' '.join(g['cmd'])
        record['results'].append(dict(rc=g['rc'],diagnostic_receipts=named,exact_target=named==[d['receipt']],one_error=out.count(': FAIL')==1 and out.count(': PASS')==2 if direct else '1 vi phạm' in out,positive_error='LỆCH BĂM' in err if direct else 'blob tại `evidence_url`' in err))
    verification.append(record)
data['mutations_verified']=verification
save('final-integrity.json',data)
assert not data['changed'] and not data['added'] and not data['removed']
assert data['original_head']==HEAD and not data['original_status'] and not data['mutant_status']
assert data['original_diff_check']['rc']==0
assert len(verification)==4 and all(g['rc']==1 and g['exact_target'] and g['one_error'] and g['positive_error'] for d in verification for g in d['results'])
print(json.dumps(data,ensure_ascii=False,indent=2))
note('Kiểm cuối — `PYTHONDONTWRITEBYTECODE=1 python3 final_integrity.py`: rc0; '+str(len(before))+' tệp clone gốc trước/sau, changed/added/removed=[]; status rỗng; HEAD/tree không đổi. `git diff --check c82047d HEAD` trên clone gốc rc0, output rỗng. Đọc lại toàn bộ stderr của các đột biến: mỗi lần chỉ nêu đúng một biên nhận lỗi, bien_nhan có đúng 1 vi phạm, t26 FAIL và hai t27 PASS. Chi tiết `evidence/final-integrity.json`.')
