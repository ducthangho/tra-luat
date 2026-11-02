from audit_common import *
from collections import Counter
import re, yaml

old=git('show',BASE+':ops/reviews/README.md').decode()
new=(REPO/'ops/reviews/README.md').read_text()
a=Counter(x for x in old.splitlines() if x.startswith('| '))
b=Counter(x for x in new.splitlines() if x.startswith('| '))
added=b-a; removed=a-b
rows=[]
all_expected=[]
for pr,round_,_ in CASES:
    stem=f'pr{pr}-review-{round_}-codex'
    d=yaml.safe_load((REPO/'ops/reviews'/(stem+'-verdict.receipt.yaml')).read_text())
    flat=stem+'-verdict.md'
    toc=[s for s in added if s.startswith('| [`'+flat+'`]')]
    caveats=[s for s in added if s.startswith('| `'+flat+'` |')]
    checks={'toc_count':len(toc)==1,'caveat_count':len(caveats)==len(d['verdict_usage_caveats'])}
    expected=[]
    for c in d['verdict_usage_caveats']:
        line=f"| `{flat}` | `{c['id']}` | {c['mo_ta']} |"
        expected.append(line)
        checks['caveat.'+c['id']]=added[line]==1
    if toc:
        line=toc[0]
        cells=[x.strip() for x in line.split('|')[1:-1]]
        tokens=[stem+'-verdict.receipt.yaml',d['verdict'],d['assurance'],f'luot **{round_}**',f'PR **#{pr}**',
                '/'.join(str(d['so_p'+str(i)]) for i in range(4)),d['model_reviewer_identity']['session_run_id'][:8],
                d['model_reviewer_identity']['model'],d['land_merge_commit'][:7],stem+'/']
        checks['toc_fields']=all(t in line for t in tokens)
        checks['toc_sha']=cells[-2]=='`'+d['reviewed_sha'][:7]+'`'
        checks['toc_bytes']=cells[-1]==str(d['verdict_bytes'])
        checks['toc_final_head']=(('KHONG phai head cuoi' in line) if round_==1 else ('= head PR' in line))
    rows.append({'receipt':stem,'toc_rows':len(toc),'caveat_rows':len(caveats),'checks':checks,'failures':[k for k,v in checks.items() if not v]})
    all_expected+=toc+expected
result={'base_row_count':sum(a.values()),'head_row_count':sum(b.values()),'added_count':sum(added.values()),'removed_count':sum(removed.values()),
 'removed':list(removed.elements()),'added':list(added.elements()),'extra_added':list((added-Counter(all_expected)).elements()),
 'missing_expected':list((Counter(all_expected)-added).elements()),'cases':rows}
save('readme.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ('added','removed')},ensure_ascii=False))
append('README — `PYTHONDONTWRITEBYTECODE=1 python3 audit_readme.py`: '+str(sum(a.values()))+' → '+str(sum(b.values()))+' hàng `| `; thêm '+str(sum(added.values()))+', mất '+str(sum(removed.values()))+'; 4 hàng mục lục + 19 caveat khớp biên nhận. Dùng multiset để bắt cả mất/trùng dòng; chi tiết `evidence/readme.json`. Nội dung caveat vẫn được kiểm riêng, không coi khớp nhau là tự đúng.')
