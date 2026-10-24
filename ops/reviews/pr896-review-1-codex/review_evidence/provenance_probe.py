import json
from pathlib import Path
import re
import subprocess

p = Path('ops/land/pr889-claude-md-bai-hoc-c-provenance')
def git(*a):
    return subprocess.check_output(['git', *a], text=True)
def comment(filename, cid):
    return next(c for c in json.loads((p/filename).read_text()) if c['id'] == cid)
def state(c):
    return json.loads(re.search(r'codex-review-state:v1 (.*?) -->', c['body']).group(1))['code_review']

new = 'readback-comments-889-sau-review-lai.json'
request = comment(new,6366307732)
receipt = comment(new,6366338141)
summary = comment(new,6360319005)
old = comment('readback-comments-889.json',6360319005)
for c in (request,receipt,summary):
    print(f'comment {c["id"]}: author={c["user"]["login"]}; created_at={c["created_at"]}; updated_at={c["updated_at"]}')
print('request body:', request['body'].split('\n---')[0].strip())
print('receipt body:', receipt['body'].split('<details>')[0].strip())
print('old summary:', json.dumps(state(old),sort_keys=True))
print('new summary:', json.dumps(state(summary),sort_keys=True))
assert request['user']['login'] == 'ducthangho' and request['created_at'] == '2026-10-23T13:43:34Z'
assert request['body'].startswith('@codex review')
assert receipt['user']['login'] == 'chatgpt-codex-connector[bot]' and receipt['created_at'] == '2026-10-23T13:45:03Z'
assert "Didn't find any major issues" in receipt['body'] and '`6ac385fdd7`' in receipt['body']
assert state(old)['commit_sha'] == '094e8d17ae4dfcf21dca63702c9262267bdc072c' and state(old)['status'] == 'running'
assert state(summary) == {'commit_sha':'6ac385fdd7325f532ac4b4b6eb861292bfa7e970','has_any_findings':False,'has_unresolved_findings':False,'status':'completed'}
assert summary['updated_at'] == '2026-10-23T13:45:05Z'
assert old['id'] == summary['id'] and old['created_at'] == summary['created_at'] and old['body'] != summary['body']
for filename in ('readback-reactions-pr-889.json','readback-reactions-pr-889-sau-review-lai.json'):
    reactions = json.loads((p/filename).read_text())
    print(filename, [(r['user']['login'],r['content'],r['created_at']) for r in reactions])
reactions = json.loads((p/'readback-reactions-pr-889-sau-review-lai.json').read_text())
assert len(reactions) == 1 and reactions[0]['content'] == '+1' and reactions[0]['created_at'] == '2026-10-23T13:45:08Z'
assert reactions[0]['user']['login'] == 'chatgpt-codex-connector[bot]'
print('PR #891 merge in committed history:')
print(git('show','-s','--format=%H%n%P%n%cI%n%B','8324567').strip())
assert git('merge-base','--is-ancestor','0390130','8324567') == ''
merge_time = git('show','-s','--format=%cI','8324567').strip()
from datetime import datetime
assert datetime.fromisoformat(merge_time) < datetime.fromisoformat(request['created_at'])
print('request after #891 merge: True')

blobs = [git('rev-parse', s + ':CLAUDE.md').strip() for s in ('094e8d1','6ac385f')]
print('CLAUDE.md blobs at 094e8d1 / 6ac385f:', blobs)
assert blobs == ['975cd94ff851a3a0ee3aa0493e90184e5f81c874'] * 2
stat = git('diff','--stat','094e8d1','6ac385f')
print('$ git diff --stat 094e8d1 6ac385f\n' + stat, end='')
assert (p/'readback-blob-claude-md-094e8d1-6ac385f.txt').read_text().splitlines()[3:] == stat.splitlines()
print('blob readback stat byte-for-byte lines: True')
paths = git('diff','--name-only','094e8d1','6ac385f').splitlines()
assert paths == ['.claude/hooks/subagent_ghi_detect_test.py','ops/land_evidence_nguon_test.py']
print('master changes #872/#877:')
print(git('show','-s','--format=%h %s','9d4cb6a','daf8961').strip())

base = '1ccc31498b7d37c12305e8f1b5bf2d1fc217b92e'
head = '816f43988eb3012726120ad00166a989cc2b9af6'
land = 'ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml'
before = git('show',base+':'+land)
after = git('show',head+':'+land)
assert after.startswith(before)
assert before == git('show','0390130:'+land)
print('land-evidence prefix unchanged from base and 0390130: True; old lines=', len(before.splitlines()), '; added lines=',len(after.splitlines())-len(before.splitlines()))
delta = git('diff','--numstat',base,head,'--','ops/land/')
print('$ git diff --numstat <base> <head> -- ops/land/\n'+delta, end='')
assert all(line.split('\t')[1] == '0' for line in delta.splitlines())
patch = git('diff',base,head,'--','ops/land/')
assert not [x for x in patch.splitlines() if x.startswith('-') and not x.startswith('---')]
print('land diff: removed content lines=0')

# Establish what is and is not preserved offline, without querying GitHub.
matches = git('grep','-l','6366218495',head,'--','ops/land/','ops/reviews/').splitlines()
print('6366218495 references available at reviewed SHA:', matches)
print('comment #891 6366218495 body/authorization and measurement timestamp 15:16:09Z: KHÔNG ĐO ĐƯỢC independently; no raw readback in this tree.')
print('Current GitHub status: KHÔNG ĐO ĐƯỢC; observations limited to frozen before/after readbacks.')
print('All measured fields with cited readback: matched.')
