import collections
import csv
import hashlib
import json
import os
import subprocess
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
REPO = ROOT / 'cay-kho'
RAW = ROOT / 'raw-rest'
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
rows = []


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], env=ENV)


def read(name):
    return json.loads((RAW / name).read_text())


def check(claim, source, measured, expected):
    rows.append((claim, source, json.dumps(measured, ensure_ascii=False),
                 json.dumps(expected, ensure_ascii=False), 'KHOP' if measured == expected else 'LECH'))


check('HEAD', 'git rev-parse HEAD', git('rev-parse', 'HEAD').decode().strip(),
      '352d31e03bc846cae5b4ee7bc17bbea6830fb64d')
pr = read('pull-1111.json')
for key, expected in {'number': 1111, 'merged': True, 'merged_at': '2026-11-01T07:43:08Z',
                      'merge_commit_sha': '4397ee616273a97c1503e8359452aef4e78cd75a'}.items():
    check('PR1111 '+key, 'pull-1111.json:'+key, pr[key], expected)
check('PR1111 head', 'pull-1111.json:head.sha', pr['head']['sha'], 'f783bee391ada131df8df195acfd3d4c4ae394c9')
comment = next(x for x in read('comments-1111.json') if x['id'] == 6555093642)
check('comment anchors exact head', 'comments-1111.json:6555093642.body', pr['head']['sha'] in comment['body'], True)
head_time = git('show', '-s', '--format=%cI', pr['head']['sha']).decode().strip().replace('+00:00','Z')
check('head < comment < merge', 'git commit time + comments-1111.json + pull-1111.json',
      head_time < comment['created_at'] < pr['merged_at'], True)
for parent, child in [('4397ee6','165b27a'), ('4397ee6','3bdd987'), ('3bdd987','180039c'), ('cb39aca','40609d4')]:
    p = subprocess.run(['git','-C',str(REPO),'merge-base','--is-ancestor',parent,child],env=ENV)
    check('ancestor '+parent+' -> '+child, 'git merge-base --is-ancestor', p.returncode, 0)
check('merge parents', 'git show 4397ee6 %P', git('show','-s','--format=%P','4397ee6').decode().split(),
      ['c6dd7b33b4f215809bf281ee1533bc1e8fa6920c', 'f783bee391ada131df8df195acfd3d4c4ae394c9'])
check('merge files', 'git diff --name-only 4397ee6^1 4397ee6',
      git('diff','--name-only','4397ee6^1','4397ee6').decode().splitlines(), [
          'ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml',
          'ops/land/pr1065-vm-cap-nhat-cong-cu-provenance/SHA256SUMS.txt',
          'ops/land/pr1065-vm-cap-nhat-cong-cu-provenance/gate-output-41173244891.txt'])
check('3 intervening merges', 'git log --first-parent --reverse 4397ee6..3bdd987',
      git('log','--first-parent','--reverse','--format=%h','4397ee6..3bdd987').decode().splitlines(),
      ['165b27a','2cea625','3bdd987'])
check('4 added specs', 'git diff --name-status 4397ee6 3bdd987',
      git('diff','--name-status','4397ee6','3bdd987').decode().splitlines(), [
          'A\tops/specs/CI-LAN-LUU-TRU-r1.md', 'A\tops/specs/DIEU-KIEN-MERGE-CONG-r1.md',
          'A\tops/specs/launcher-sandbox-lay-mau-r1.md', 'A\tops/specs/launcher-sandbox-lay-mau-r2.md'])
check('no change in dossier or VM', 'git diff --name-status 4397ee6 3bdd987 -- <paths>',
      git('diff','--name-status','4397ee6','3bdd987','--','ops/vm/',
          'ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml').decode(), '')
run_ids = (41285898441,41287486328,41290009265)
for run_id, sha, conclusion, created, updated in [
    (41285898441,'4397ee6','cancelled','07:43:11','09:07:12'),
    (41287486328,'165b27a','success','09:07:11','09:23:36'),
    (41290009265,'3bdd987','success','09:42:53','10:22:24'),
]:
    run = read(f'run-{run_id}.json')
    expected = {'id':run_id,'event':'push','path':'.github/workflows/ci.yml','run_attempt':1,
                'head_sha':git('rev-parse',sha).decode().strip(),'status':'completed','conclusion':conclusion,
                'created_at':f'2026-11-01T{created}Z','updated_at':f'2026-11-01T{updated}Z'}
    for key,value in expected.items():
        check(f'run {run_id} {key}',f'run-{run_id}.json:{key}',run[key],value)
    check(f'run {run_id} repository',f'run-{run_id}.json:repository.full_name',
          run['repository']['full_name'],'ducthangho/tra-luat')
cancelled_jobs = read('jobs-41285898441.json')
check('cancelled run total_count / jobs', 'jobs-41285898441.json',
      [cancelled_jobs['total_count'],cancelled_jobs['jobs']], [0,[]])
run = read('run-41290009265.json')
jobs_data = read('jobs-41290009265-r2.json')
jobs = jobs_data['jobs']
for claim, measured, expected in [
    ('returned / total_count', [len(jobs),jobs_data['total_count']], [23,23]),
    ('success', sum(j['conclusion']=='success' for j in jobs),23),
    ('ubuntu-latest',sum(j['labels']==['ubuntu-latest'] for j in jobs),23),
    ('runner_id != 0',sum(j['runner_id']!=0 for j in jobs),23),
    ('started_at < run.created_at',sum(j['started_at']<run['created_at'] for j in jobs),22),
    ('completed_at < run.created_at',sum(j['completed_at']<run['created_at'] for j in jobs),15),
    ('min started_at',min(j['started_at'] for j in jobs),'2026-11-01T09:23:37Z'),
    ('all job run_id/attempt/head match',all((j['run_id'],j['run_attempt'],j['head_sha'])==
        (run['id'],run['run_attempt'],run['head_sha']) for j in jobs),True),
]:
    check(claim,'jobs-41290009265-r2.json + run-41290009265.json',measured,expected)
all_runs = read('runs-master-push.json')['workflow_runs']
window = sorted((r for r in all_runs if read('run-41285898441.json')['created_at'] <= r['created_at']
                 <= run['created_at'] and r['path']=='.github/workflows/ci.yml'), key=lambda r:r['created_at'])
check('successful run order in supplied window', 'runs-master-push.json',
      [r['id'] for r in window if r['conclusion']=='success'],[41287486328,41290009265])
for path,prefix in [('ops/vm/cap-nhat-cong-cu.ps1','8efc063a'),('ops/cong_cu.yaml','71631bb6'),('requirements.txt','97733a88')]:
    blob=git('show','cb39aca:'+path)
    check('static hash '+path,'git show cb39aca:'+path,hashlib.sha256(blob).hexdigest()[:8],prefix)
    check('static bytes same at merge '+path,'git show cb39aca/40609d4:'+path,blob==git('show','40609d4:'+path),True)
schedule = git('show','cb39aca:ops/vm/cap-nhat-cong-cu.ps1').decode()
check('static schedule', 'cb39aca:ops/vm/cap-nhat-cong-cu.ps1',
      "New-ScheduledTaskTrigger -Weekly -WeeksInterval 2 -DaysOfWeek Sunday -At '02:30'" in schedule,True)
data=yaml.safe_load((REPO/'ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml').read_text())
check('landed bool', 'YAML trang_thai_packet.landed', type(data['trang_thai_packet']['landed']) is bool,True)
check('VM label', 'YAML van_hanh_tren_vm.trang_thai',data['van_hanh_tren_vm']['trang_thai'],'thuat_lai')
check('post_merge labels', 'YAML post_merge_checks', [x['trang_thai'] for x in data['post_merge_checks']],
      ['measured','measured','thuat_lai'])
with (HERE/'claims-field-check-r2.tsv').open('w') as f:
    writer=csv.writer(f,delimiter='\t',lineterminator='\n')
    writer.writerow(('claim','source','measured','expected','result')); writer.writerows(rows)
for row in rows:
    print(row[0], row[-1], row[2])
print('CLAIMS',len(rows),'KHOP',sum(r[-1]=='KHOP' for r in rows),'LECH',sum(r[-1]=='LECH' for r in rows))
assert all(r[-1]=='KHOP' for r in rows)
