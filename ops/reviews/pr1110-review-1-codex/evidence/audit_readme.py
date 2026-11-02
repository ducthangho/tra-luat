from collections import Counter
import re
import yaml
from audit_common import *

d = yaml.safe_load((REPO / RECEIPT).read_text())
path = 'ops/reviews/README.md'
base = git('show', BASE + ':' + path)
head = git('show', HEAD + ':' + path)
def rows(b):
    return Counter(l for l in b.decode().splitlines() if l.startswith('| '))
br, hr = rows(base), rows(head)
added = list((hr-br).elements())
removed = list((br-hr).elements())
checks = {}
checks['all_base_rows_preserved'] = not removed
checks['exact_four_rows_added'] = len(added) == 4
head_without_added = b''.join(l for l in head.splitlines(keepends=True) if l.decode().rstrip('\r\n') not in added)
checks['whole_readme_minus_four_equals_base'] = head_without_added == base
name = Path(d['verdict_path']).name
index = [l for l in added if l.startswith('| [`' + name + '`]')]
caveats = [l for l in added if l.startswith('| `' + name + '` |')]
checks['one_index_three_caveats'] = len(index) == 1 and len(caveats) == 3
for c in d['verdict_usage_caveats']:
    expected = f"| `{name}` | `{c['id']}` | {c['mo_ta']} |"
    checks['caveat/' + c['id']] = caveats.count(expected) == 1
m = d['model_reviewer_identity']
tokens = {
    'verdict': '**`' + d['verdict'] + '`**', 'assurance': '`' + d['assurance'] + '`',
    'round': 'luot **' + str(d['luot']) + '**', 'pr': 'PR **#' + str(d['target_pull_request']) + '**',
    'count': '/'.join(str(d[f'so_p{i}']) for i in range(4)) + ' (P0/P1/P2/P3)',
    'run': 'launcher.py run ' + m['session_run_id'][:8], 'model': '`' + m['model'] + '` do_may',
    'merge': 'merge `' + d['land_merge_commit'][:7] + '`',
    'head': '| `' + d['reviewed_sha'][:7] + '` |', 'bytes': '| ' + str(d['verdict_bytes']) + ' |',
    'receipt_link': '(' + Path(RECEIPT).name + ')', 'archive_link': '(' + Path(ARCHIVE).name + '/)',
}
for key, token in tokens.items():
    checks['index/' + key] = len(index) == 1 and token in index[0]
for link in re.findall(r'\]\(([^)]+)\)', '\n'.join(added)):
    checks['link/' + link] = (REPO / 'ops/reviews' / link).exists()
history = []
for ref in ['f0c4ed6', '6af4c9a', HEAD]:
    commit = git('rev-parse', ref).decode().strip()
    parents = git('rev-list', '--parents', '-n', '1', commit).decode().split()[1:]
    changes = git('diff', '--name-only', parents[0], commit).decode().splitlines()
    entry = dict(commit=commit, parents=parents, changed_count=len(changes),
                 changed_paths=changes, parent_readme_comparisons=[])
    if len(parents) == 2:
        cr = rows(git('show', commit + ':' + path))
        for parent in parents:
            pr = rows(git('show', parent + ':' + path))
            missing = list((pr-cr).elements())
            entry['parent_readme_comparisons'].append(dict(parent=parent, rows=sum(pr.values()), missing=missing))
            checks['merge_preserves/' + parent] = not missing
    history.append(entry)
checks['artifact_commit_only_expected_files'] = set(history[0]['changed_paths']) == {p for p in git('diff', '--name-only', BASE, HEAD).decode().splitlines() if p not in [RECEIPT, path]}
checks['receipt_commit_only_readme_receipt'] = set(history[1]['changed_paths']) == {path, RECEIPT}
checks['merge_second_parent_is_base'] = history[2]['parents'][1] == BASE
checks['archive_receipt_unchanged_by_merge'] = not git('diff', '6af4c9a', HEAD, '--', ARCHIVE, ARCHIVE + '-verdict.md', RECEIPT)
out = dict(base_rows=sum(br.values()), head_rows=sum(hr.values()), added=added, removed=removed,
           index_rows=len(index), caveat_rows=len(caveats), checks=checks, history=history,
           errors=[k for k, ok in checks.items() if not ok])
save('readme.json', out)
print(json.dumps({k:v for k,v in out.items() if k != 'history'}, ensure_ascii=False, indent=2))
print(json.dumps({'history': [{k:v for k,v in x.items() if k != 'changed_paths'} for x in history]}, ensure_ascii=False, indent=2))
assert not out['errors']
