from collections import Counter
import hashlib
import json
import subprocess
import re
import yaml
from audit import BASE, ROOT, SHA, PARENT, git, record

results = []
def check(label, value):
    results.append({'claim': label, 'result': value})

land = yaml.safe_load((ROOT / 'ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml').read_text())
readme = (ROOT / 'ops/reviews/README.md').read_text().splitlines()
rp = 'ops/reviews/pr896-review-4-codex-verdict.receipt.yaml'
receipt = yaml.safe_load((ROOT / rp).read_text())
vp = ROOT / receipt['verdict_path']
check('previous_verdict_supplied_equals_flat_and_directory', (BASE.parent/'verdict-cu/pr896-review-4-codex-VERDICT.md').read_bytes() == vp.read_bytes() == (ROOT/'ops/reviews/pr896-review-4-codex/VERDICT.md').read_bytes())
check('previous_hint_supplied_equals_stored_artifact', (BASE.parent/'verdict-cu/pr896-review-4-codex-HINT.patch').read_bytes() == (ROOT/'ops/reviews/pr896-review-4-codex/HINT.patch').read_bytes())
check('previous_verdict_bytes_sha256', {'bytes':len(vp.read_bytes()),'sha256':hashlib.sha256(vp.read_bytes()).hexdigest(),'matches_receipt':hashlib.sha256(vp.read_bytes()).hexdigest()==receipt['verdict_sha256']})
for base, target, hint in [('578fb4b','82359c4','ops/reviews/pr896-review-2-codex/HINT.patch'), ('c8c1ee0','2e4183b','ops/reviews/pr896-review-3-codex/HINT.patch')]:
    wanted = (ROOT / hint).read_text()
    missing = []
    for section in re.split(r'(?=^--- )', wanted,flags=re.M):
        match = re.search(r'^\+\+\+ (\S+)',section,re.M)
        if not match:
            continue
        p = match[1]
        expected = Counter(l for l in section.splitlines() if l[:1] in ['+','-'] and not l.startswith(('+++','---')))
        actual = Counter(l for l in git('diff','--unified=0',base,target,'--',p).decode().splitlines() if l[:1] in ['+','-'] and not l.startswith(('+++','---')))
        if expected-actual:
            missing.append({'path':p,'missing':list((expected-actual).elements())})
    check('hint_at_' + target, {'parent':git('show','-s','--format=%P',target).decode().strip(), 'missing_plus_minus_lines':missing})

for ref,roundno in [('8879165',3),('c8c1ee0',3),('ff4ab57',4),('77a0a45',4)]:
    past = git('show',ref+':ops/reviews/pr896-review-'+str(roundno)+'-codex-verdict.receipt.yaml').decode()
    d = yaml.safe_load(past)
    check('CHUA_AP_snapshot_'+ref, {'oid':git('rev-parse',ref).decode().strip(),'caveat_ids':[c['id'] for c in d['verdict_usage_caveats'] if 'HINT' in c['id']], 'land_has_block':('cap_nhat_20261026_luot'+str(roundno)+':') in git('show',ref+':ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml').decode()})

for turn in [3,4]:
    p=ROOT/f'ops/reviews/pr896-review-{turn}-codex-verdict.receipt.yaml'
    d=yaml.safe_load(p.read_text())
    c=next(c for c in d['verdict_usage_caveats'] if c['id'].startswith('HINT-'))
    rows=[(i,l) for i,l in enumerate(readme,1) if l.startswith(f'| `pr896-review-{turn}-codex-verdict.md` | `'+c['id']+'` |')]
    index=[(i,l) for i,l in enumerate(readme,1) if l.startswith(f'| [`pr896-review-{turn}-codex-verdict.md`]')]
    check('round_'+str(turn)+'_readme_and_receipt', {'id':c['id'],'caveat_rows':len(rows),'same_description':len(rows)==1 and c['mo_ta'] in rows[0][1],'index_line':index[0][0],'index':index[0][1]})

check('new_land_block',land['cap_nhat_review_4_moc_lich_su'])
check('review_2_3_recorded_conclusions', {'round2':(ROOT/'ops/reviews/pr896-review-2-codex-verdict.md').read_text().splitlines()[6:8], 'round3':(ROOT/'ops/reviews/pr896-review-3-codex-verdict.md').read_text().splitlines()[5]})
check('successor_after_77a0a45',git('rev-list','--ancestry-path','--reverse',PARENT+'..'+SHA).decode().splitlines())
check('extra_receipt_round4_delta',git('diff','--numstat',PARENT,SHA,'--',rp).decode().strip())
(BASE/'claims.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
summary=[]
for x in results:
    if x['claim'] in ['new_land_block','review_2_3_recorded_conclusions']:
        summary.append(x['claim']+'='+json.dumps(x['result'],ensure_ascii=False))
    else:
        summary.append(x['claim']+'='+json.dumps(x['result'],ensure_ascii=False))
record('HƯỚNG 9 - moc lich su va cau moi', 'PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/claims.py', '\n'.join(summary), 'KHÔNG PHẢI LỖI mới ở các câu 1a276a1 thêm/sửa: mốc hint cũ, commit áp, OID, lời kết luận các verdict tiếp theo và supplementary YAML đều khớp dữ liệu được lưu. Câu chưa merge PR947 đo được đúng; chưa land không bị đánh đồng với ancestry. Các trường cũ ngoài hunk còn sai đã ghi ở H6/H7.')
