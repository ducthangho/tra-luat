import collections
import csv
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
    rows.append((filename, field, json.dumps(actual, ensure_ascii=False), source,
                 json.dumps(expected, ensure_ascii=False), 'KHOP' if actual == expected else 'LECH'))


for line in (RAW / 'FETCH-LOG.txt').read_text().splitlines():
    if ' -> ' not in line:
        print('FETCH note (no digest; not counted as hash verification):', line)
        continue
    _, tail = line.split(' -> ')
    filename, digest = tail.split()
    actual = hashlib.sha256((RAW / filename).read_bytes()).hexdigest()[:len(digest)]
    check('FETCH-LOG.txt', filename, actual, digest, filename)

filename = 'readback-pr-1111.json'
excerpt, raw = read(PROV / filename), read(RAW / 'pull-1111.json')
mapping = {key: raw[key] for key in ('number', 'state', 'merged', 'merged_at', 'merge_commit_sha')}
mapping.update(merged_by=raw['merged_by']['login'], head=raw['head']['sha'], head_ref=raw['head']['ref'])
assert excerpt.keys() == mapping.keys()
for key in excerpt:
    source_key = {'merged_by': 'merged_by.login', 'head': 'head.sha', 'head_ref': 'head.ref'}.get(key, key)
    check(filename, key, excerpt[key], mapping[key], 'pull-1111.json:' + source_key)

filename = 'readback-commit-4397ee6.json'
excerpt, raw = read(PROV / filename), read(RAW / 'commit-4397ee6.json')
mapping = dict(sha=raw['sha'], parents=[x['sha'] for x in raw['parents']], tree=raw['commit']['tree']['sha'],
               files=[[x['filename'], x['additions'], x['deletions']] for x in raw['files']])
assert excerpt.keys() == mapping.keys()
for key in excerpt:
    check(filename, key, excerpt[key], mapping[key], 'commit-4397ee6.json:' + key)

for run in ('41285898441', '41287486328', '41290009265'):
    filename = f'readback-run-{run}.json'
    excerpt, raw = read(PROV / filename), read(RAW / f'run-{run}.json')
    for key in excerpt:
        check(filename, key, excerpt[key], raw[key], f'run-{run}.json:{key}')
    if run == '41287486328':
        continue
    filename = f'readback-jobs-{run}.json'
    source = f'jobs-{run}-r2.json' if run == '41290009265' else f'jobs-{run}.json'
    excerpt, raw = read(PROV / filename), read(RAW / source)
    assert set(excerpt) == {'total_count', 'jobs'}
    for field, actual, expected in (
        ('total_count', excerpt['total_count'], raw['total_count']),
        ('jobs.length', len(excerpt['jobs']), len(raw['jobs'])),
        ('jobs.ids', [x['id'] for x in excerpt['jobs']], [x['id'] for x in raw['jobs']]),
    ):
        check(filename, field, actual, expected, source + ':' + field)
    assert len(raw['jobs']) == raw['total_count']
    assert len({x['id'] for x in raw['jobs']}) == len(raw['jobs'])
    by_id = {x['id']: x for x in raw['jobs']}
    for job in excerpt['jobs']:
        for key in job:
            check(filename, f'jobs[id={job["id"]}].{key}', job[key], by_id[job['id']][key],
                  f'{source}:jobs[id={job["id"]}].{key}')
    print('JOBS', run, 'total_count=', raw['total_count'], 'returned=', len(raw['jobs']),
          'conclusions=', dict(collections.Counter(x['conclusion'] for x in raw['jobs'])),
          'labels=', dict(collections.Counter(tuple(x['labels']) for x in raw['jobs'])),
          'runner_id=0:', sum(x['runner_id'] == 0 for x in raw['jobs']),
          'head_sha=', sorted({x['head_sha'] for x in raw['jobs']}))

with (HERE / 'readbacks-field-check-r2.tsv').open('w') as out:
    writer = csv.writer(out, delimiter='\t', lineterminator='\n')
    writer.writerow(('file', 'field', 'excerpt_value', 'raw_source', 'raw_value', 'result'))
    writer.writerows(rows)
print('CHECKS', len(rows), 'KHOP', sum(x[-1] == 'KHOP' for x in rows), 'LECH', sum(x[-1] == 'LECH' for x in rows))
for filename in sorted({x[0] for x in rows}):
    selected = [x for x in rows if x[0] == filename]
    print(filename, len(selected), 'checks;', sum(x[-1] == 'LECH' for x in selected), 'mismatches')
for row in rows:
    if row[-1] == 'LECH':
        print('MISMATCH', row)
assert all(x[-1] == 'KHOP' for x in rows)
