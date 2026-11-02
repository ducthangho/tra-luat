import collections
import json
import os
import re
import subprocess
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE/'work/head'
BASE = '3574cb07dba8a8f7f32384ee3d1d3dfbf3a4f70e'
README = 'ops/reviews/README.md'
NAME = 'pr1071-review-1-codex-verdict.md'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
errors = []
checks = {}
def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,env=env)
def check(label,value):
    checks[label]=bool(value)
    if not value: errors.append(label)
def text_at(rev):
    return git('show',rev+':'+README).decode()
def rows(text):
    return collections.Counter(line for line in text.splitlines() if line.startswith('| '))
base_text, head_text = text_at(BASE), text_at('HEAD')
base_rows, head_rows = rows(base_text), rows(head_text)
added = list((head_rows-base_rows).elements())
removed = list((base_rows-head_rows).elements())
check('base_rows_all_preserved',not removed)
check('exact_four_added',len(added)==4 and all(NAME in x for x in added))
check('whole_readme_minus_four_equals_base_bytewise', ''.join(x for x in head_text.splitlines(keepends=True) if NAME not in x)==base_text)
receipt=yaml.safe_load((ROOT/'ops/reviews'/NAME.replace('.md','.receipt.yaml')).read_text())
index=[x for x in added if '.receipt.yaml' in x]
caveats=[x for x in added if '.receipt.yaml' not in x]
check('one_index_three_caveat_rows',len(index)==1 and len(caveats)==3)
row=index[0]
for key, value in {
    'verdict': receipt['verdict'], 'assurance': receipt['assurance'],
    'round': 'luot **'+str(receipt['luot'])+'**', 'pr': '**#'+str(receipt['target_pull_request'])+'**',
    'head': receipt['reviewed_sha'][:7], 'merge': receipt['land_merge_commit'][:7],
    'bytes': str(receipt['verdict_bytes']), 'model':receipt['model_reviewer_identity']['model'],
    'run':receipt['model_reviewer_identity']['session_run_id'][:8],
    'count':'/'.join(str(receipt[f'so_p{i}']) for i in range(4)),
    'receipt_link': NAME.replace('.md','.receipt.yaml'), 'archive_link':'(pr1071-review-1-codex/)'
}.items():
    check('index_'+key,value in row)
for caveat in receipt['verdict_usage_caveats']:
    matches = [line for line in caveats if '| `'+caveat['id']+'` |' in line]
    check('caveat_'+caveat['id'],len(matches)==1 and caveat['mo_ta'] in matches[0])
links=[]
for line in added:
    for path in re.findall(r'\]\(([^)]+)\)',line):
        exists=(ROOT/'ops/reviews'/path).exists()
        links.append({'path':path,'exists':exists})
        check('link_'+path,exists)

history=[]
for revision in ['629543d','16f9658','1907678','907c474']:
    parents=git('show','-s','--format=%P',revision).decode().strip().split()
    changed=git('diff','--name-only',parents[0],revision).decode().splitlines()
    record={'commit':git('rev-parse',revision).decode().strip(),'parents':parents,
            'changed_vs_first_parent':changed, 'parent_readme_comparisons':[]}
    if len(parents)==2:
        result_rows=rows(text_at(revision))
        for p in parents:
            previous=rows(text_at(p))
            missing=list((previous-result_rows).elements())
            record['parent_readme_comparisons'].append({'parent':p, 'parent_rows':sum(previous.values()),
                                                       'result_rows':sum(result_rows.values()),'missing':missing})
            check('merge_preserves_'+revision+'_'+p,not missing)
    history.append(record)

output={'base_rows':sum(base_rows.values()),'head_rows':sum(head_rows.values()),
        'added':added,'removed':removed,'index_rows':len(index),'caveat_rows':len(caveats),
        'checks':checks,'links':links,'history':history,'errors':errors}
(HERE/'evidence/readme-history.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
(HERE/'evidence/readme.diff').write_bytes(git('diff',BASE,'HEAD','--',README))
print(json.dumps({k:v for k,v in output.items() if k not in ('added','checks','history','links')},ensure_ascii=False))
print(json.dumps({'checks':checks,'merges':[{'commit':x['commit'],'parent_readme_comparisons':x['parent_readme_comparisons']} for x in history if len(x['parents'])==2]},ensure_ascii=False))
raise SystemExit(bool(errors))
