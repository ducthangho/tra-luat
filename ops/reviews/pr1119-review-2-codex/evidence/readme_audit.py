from common import *
from collections import Counter
import yaml
base=git('show',BASE+':ops/reviews/README.md').decode();head=(R/'ops/reviews/README.md').read_text()
rows=lambda t:Counter(l for l in t.splitlines() if l.startswith('| '))
b,h=rows(base),rows(head);added=h-b;removed=b-h;expected=Counter();checks=[]
for pr,turn,src in ITEMS:
    stem=f'pr{pr}-review-{turn}-codex';d=yaml.safe_load((R/'ops/reviews'/f'{stem}-verdict.receipt.yaml').read_text())
    for c in d['verdict_usage_caveats']:
        line=f'| `{stem}-verdict.md` | `{c["id"]}` | {c["mo_ta"]} |';expected[line]+=1;checks.append((stem,c['id'],h[line]==1))
    index=[l for l in h if l.startswith(f'| [`{stem}-verdict.md`]')];checks.append((stem,'one index',len(index)==1))
    if len(index)==1:
        line=index[0];expected[line]+=1;cells=[c.strip() for c in line.strip('|').split('|')]
        tokens=[f'({stem}-verdict.receipt.yaml)',f'**`{d["verdict"]}`**',f'`{d["assurance"]}`',f'luot **{turn}**',f'PR **#{pr}**','/'.join(str(d[f'so_p{i}']) for i in range(4)),d['model_reviewer_identity']['session_run_id'][:8],d['model_reviewer_identity']['model'],d['land_merge_commit'][:7],f'({stem}/)']
        for t in tokens:checks.append((stem,t,t in line))
        checks.extend([(stem,'sha cell',cells[-2]==f'`{d["reviewed_sha"][:7]}`'),(stem,'bytes cell',cells[-1]==str(d['verdict_bytes'])),(stem,'head clause',('KHONG phai head cuoi' in line) if turn==1 else ('head da duyet = head PR' in line))])
data=dict(base_rows=sum(b.values()),head_rows=sum(h.values()),added=sum(added.values()),removed=sum(removed.values()),added_rows=list(added.elements()),removed_rows=list(removed.elements()),extra=list((added-expected).elements()),missing=list((expected-added).elements()),checks=checks,failures=[c for c in checks if not c[-1]])
save('readme.json',data);print(json.dumps({k:v for k,v in data.items() if k not in ['added_rows','checks']},ensure_ascii=False,indent=2));note('README — `PYTHONDONTWRITEBYTECODE=1 python3 readme_audit.py`: '+json.dumps({k:v for k,v in data.items() if k not in ['added_rows','checks']},ensure_ascii=False)+'. Multiset mọi hàng bắt đầu `| `, 4 hàng mục lục đối chiếu các ô và 19 hàng caveat so nguyên văn receipt: `evidence/readme.json`.')
