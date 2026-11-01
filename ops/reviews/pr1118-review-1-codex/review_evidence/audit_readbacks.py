import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RAW = ROOT / 'raw-rest'
PROV = ROOT / 'cay-kho/ops/land/pr1065-vm-cap-nhat-cong-cu-provenance'
rows = []


def read(path):
    return json.loads(path.read_text())


def check(filename, field, actual, expected, source):
    rows.append((filename, field, json.dumps(actual, ensure_ascii=False),
                 source, json.dumps(expected, ensure_ascii=False),
                 'KHOP' if actual == expected else 'LECH'))


for line in (RAW / 'FETCH-LOG.txt').read_text().splitlines():
    _, tail = line.split(' -> ')
    filename, digest = tail.split()
    actual = hashlib.sha256((RAW / filename).read_bytes()).hexdigest()[:len(digest)]
    check('FETCH-LOG.txt', filename, actual, digest, filename)

filename = 'readback-pr-1111.json'
excerpt, raw = read(PROV / filename), read(RAW / 'pull-1111.json')
mapping = {key: raw[key] for key in ('number', 'state', 'merged', 'merged_at', 'merge_commit_sha')}
mapping.update(merged_by=raw['merged_by']['login'], head=raw['head']['sha'], head_ref=raw['head']['ref'])
assert excerpt.keys() == mapping.keys(), 'Unmapped excerpt fields'
for key in excerpt:
    path = {'merged_by': 'merged_by.login', 'head': 'head.sha', 'head_ref': 'head.ref'}.get(key, key)
    check(filename, key, excerpt[key], mapping[key], 'pull-1111.json:' + path)

filename = 'readback-commit-4397ee6.json'
excerpt, raw = read(PROV / filename), read(RAW / 'commit-4397ee6.json')
mapping = dict(sha=raw['sha'], parents=[x['sha'] for x in raw['parents']], tree=raw['commit']['tree']['sha'],
               files=[[x['filename'], x['additions'], x['deletions']] for x in raw['files']])
assert excerpt.keys() == mapping.keys(), 'Unmapped excerpt fields'
for key in excerpt:
    check(filename, key, excerpt[key], mapping[key], 'commit-4397ee6.json:' + key)

for run in ('41285898441', '41290009265'):
    filename = f'readback-run-{run}.json'
    excerpt, raw = read(PROV / filename), read(RAW / f'run-{run}.json')
    for key in excerpt:
        check(filename, key, excerpt[key], raw[key], f'run-{run}.json:{key}')
    filename = f'readback-jobs-{run}.json'
    excerpt, raw = read(PROV / filename), read(RAW / f'jobs-{run}.json')
    check(filename, 'total_count', excerpt['total_count'], raw['total_count'], f'jobs-{run}.json:total_count')
    check(filename, 'jobs.length', len(excerpt['jobs']), len(raw['jobs']), f'jobs-{run}.json:jobs.length')
    check(filename, 'jobs.ids', [x['id'] for x in excerpt['jobs']], [x['id'] for x in raw['jobs']], f'jobs-{run}.json:jobs[*].id')
    assert len(raw['jobs']) == raw['total_count'], 'Pagination incomplete'
    by_id = {x['id']: x for x in raw['jobs']}
    for job in excerpt['jobs']:
        for key in job:
            check(filename, f'jobs[id={job["id"]}].{key}', job[key], by_id[job['id']][key],
                  f'jobs-{run}.json:jobs[id={job["id"]}].{key}')
    print('JOBS', run, 'total_count=', raw['total_count'], 'returned=', len(raw['jobs']),
          'conclusions=', dict(collections.Counter(x['conclusion'] for x in raw['jobs'])),
          'labels=', dict(collections.Counter(tuple(x['labels']) for x in raw['jobs'])),
          'runner_id=0:', sum(x['runner_id'] == 0 for x in raw['jobs']),
          'head_sha=', sorted({x['head_sha'] for x in raw['jobs']}))

with (HERE / 'readbacks-field-check.tsv').open('w') as out:
    out.write('file\tfield\texcerpt_value\traw_source\traw_value\tresult\n')
    for row in rows:
        out.write('\t'.join(row) + '\n')
print('CHECKS', len(rows), 'KHOP', sum(x[-1] == 'KHOP' for x in rows), 'LECH', sum(x[-1] == 'LECH' for x in rows))
for filename in sorted({x[0] for x in rows}):
    selected = [x for x in rows if x[0] == filename]
    print(filename, len(selected), 'checks;', sum(x[-1] == 'LECH' for x in selected), 'mismatches')
for row in rows:
    if row[-1] == 'LECH':
        print('MISMATCH', row)
