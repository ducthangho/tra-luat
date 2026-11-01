from common import *
import shutil,re
root=S/'work/mutant'
if not root.exists():shutil.copytree(R,root)
out=[]
for pr,turn,src in ITEMS:
    stem=f'pr{pr}-review-{turn}-codex';path=root/'ops/reviews'/f'{stem}-verdict.receipt.yaml';raw=path.read_bytes()
    old=re.search(rb'^verdict_sha256: ([0-9a-f]{64})$',raw,re.M)[1];new=(b'0' if old[:1]!=b'0' else b'1')+old[1:]
    try:
        path.write_bytes(raw.replace(b'verdict_sha256: '+old,b'verdict_sha256: '+new,1))
        status=git('diff','--name-only',root=root).decode().splitlines();assert status==[str(path.relative_to(root))],status
        data=dict(receipt=path.name,field='verdict_sha256',before=old.decode(),after=new.decode(),changed=status,gates=[])
        for name,cmd in [('bien-nhan',['python3','ops/bien_nhan_v2.py','--root','.']),('direct',['python3',str(S/'direct.py'),'.'])]:
            res=logged('mutant-'+stem+'-'+name,cmd,root);txt=(E/res['stdout']).read_text()+(E/res['stderr']).read_text()
            # Validator emits debt/legacy lists; restrict foreign matching to lines that flag a failure.
            badlines=[l for l in txt.splitlines() if ('VI PHẠM' in l or 'LỆCH BĂM' in l or 'blob tại evidence_url' in l)]
            res.update(target_named=path.name in txt,foreign_new_receipts=sorted(set(re.findall(r'pr111[04]-review-[12]-codex-verdict.receipt.yaml','\n'.join(badlines)))-{path.name}),failure_lines=badlines)
            data['gates'].append(res)
        out.append(data);save('mutations.json',out);print(stem,[(g['rc'],g['target_named'],g['foreign_new_receipts']) for g in data['gates']],flush=True)
    finally:path.write_bytes(raw)
save('mutations.json',out)
assert git('status','--porcelain=v1',root=root)==b''
assert all(g['rc']!=0 and g['target_named'] and not g['foreign_new_receipts'] for d in out for g in d['gates'])
note('Đột biến — `PYTHONDONTWRITEBYTECODE=1 python3 mutations.py`: 4/4 đổi riêng verdict_sha256 trên bản sao; 8/8 lần bien_nhan_v2 và t26 đỏ, nêu đúng tệp. Bản sao đã hồi nguyên. Command/rc/stdout/stderr từng lần: `evidence/mutations.json`. Không suy đã thử riêng reviewed_sha/evidence_url.')
