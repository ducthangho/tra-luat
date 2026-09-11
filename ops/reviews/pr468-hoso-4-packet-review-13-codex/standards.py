import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat
import subprocess

import yaml

from measure import BASE, ROOT, OUT, SHA, PREV, git, note, save

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def changed_leaves(a, b, path=''):
    if isinstance(a, dict) and isinstance(b, dict):
        return sum((changed_leaves(a.get(k), b.get(k), path + '/' + str(k)) for k in a.keys() | b.keys()), [])
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return sum((changed_leaves(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))), [])
    return [] if a == b else [path]

result = {'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'receipts': {}, 'repairs': {}}
for n in (10,11,12):
    path = f'ops/reviews/pr468-hoso-4-packet-review-{n}-codex-verdict.receipt.yaml'
    raw = (ROOT / path).read_bytes()
    d = yaml.safe_load(raw)
    vr = (ROOT / d['verdict_path']).read_bytes()
    commit = re.search('/blob/([0-9a-f]{40})/', d['evidence_url'])[1]
    first = git('log','--reverse','--diff-filter=A','--format=%H',SHA,'--',d['verdict_path']).decode().splitlines()[0]
    row = {'verdict_bytes': len(vr), 'verdict_sha256': sha(vr),
           'bytes_match': len(vr) == d['verdict_bytes'], 'hash_match': sha(vr) == d['verdict_sha256'],
           'reviewed_sha': d['reviewed_sha'], 'anchor_commit': commit,
           'blob_equal': git('show',commit+':'+d['verdict_path']) == vr, 'first_commit': first,
           'anchor_is_first_commit': first == commit,
           'reviewed_ancestor': subprocess.run(['git','-C',str(ROOT),'merge-base','--is-ancestor',d['reviewed_sha'],commit]).returncode == 0,
           'receipt_projection_equal': (BASE/'tai-lieu'/Path(path).name).read_bytes() == raw,
           'assurance': d['assurance'], 'model_reviewer_identity': d['model_reviewer_identity']}
    assert all(row[k] for k in ['bytes_match','hash_match','blob_equal','anchor_is_first_commit','reviewed_ancestor','receipt_projection_equal'])
    result['receipts'][n] = row
    if n != 12:
        oldraw = git('show',PREV+':'+path)
        old = yaml.safe_load(oldraw)
        delta = changed_leaves(old,d)
        expected = ['/github_submitter_identity/phien_van_chuyen','/KHONG_do_duoc/2'] if n == 10 else ['/evidence_url_ghi_chu']
        assert set(delta) == set(expected)
        keys = ['model_reviewer_identity','assurance','verdict','verdict_path','verdict_sha256','verdict_bytes','reviewed_sha','evidence_url','anchor']
        assert all(old[k] == d[k] for k in keys)
        result['repairs'][n] = {'changed_yaml_leaves':delta,'protected_fields_unchanged': keys,
                               'repair_at_df0800c':git('show','df0800c:'+path) == raw,
                               'verdict_unchanged_since12':git('show',PREV+':'+d['verdict_path']) == vr}
        save('standards',result)

body = git('show','-s','--format=%B','17c6901').decode()
session = re.search(r'^Claude-Session:\s*(\S+)',body,re.M)[1]
p10 = ROOT/'ops/reviews/pr468-hoso-4-packet-review-10-codex-verdict.receipt.yaml'
assert session in p10.read_text() and 'KHÔNG phải danh tính reviewer đã xác thực' in p10.read_text()
assert 'launch 11:24:25Z' in p10.read_text() and 'final-check 11:47:28Z' in p10.read_text()
result['round10'] = {'commit_session_trailer':session,
    'final_check':json.loads((ROOT/'ops/reviews/pr468-hoso-4-packet-review-10-codex/do-review10/final-check.json').read_text()),
    'stored_log_launch_lines':[]}
for p in (ROOT/'ops/reviews/pr468-hoso-4-packet-review-10-codex').rglob('*'):
    if p.is_file() and not p.is_symlink():
        for i,line in enumerate(p.read_text(errors='replace').splitlines(),1):
            if '11:24:25' in line or '11:26' in line or '11:29' in line:
                result['round10']['stored_log_launch_lines'].append({'path':str(p.relative_to(ROOT)),'line':i,'text':line})
save('standards',result)
note('- `bien-nhan-luot10-bo-sot-va-tron-dau-vet-phien` [P2]: **ĐÃ VÁ THẬT** tại df0800c. Tự parse YAML trước/sau: chỉ 2 lá prose đổi (phien_van_chuyen và KHONG_do_duoc/2); hai mỏ neo đã sửa đúng nguồn trailer 17c6901 và các mốc lưu trong gói. Model reviewer, assurance review_deferred, verdict/băm/neo giữ nguyên. Không coi URL Claude tự khai là attestation Codex. Bằng chứng: `do-review13/standards.json`.')

rig = 'ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact-repair/rig'
result['rig_commits'] = {c:git('diff-tree','--no-commit-id','--name-status','-r',c,'--',rig).decode().splitlines() for c in ('17c6901','4c18cb2')}
assert len(result['rig_commits']['17c6901']) == 19 and not result['rig_commits']['4c18cb2']
result['commit_times'] = {c:git('show','-s','--format=%aI%n%cI',c).decode().splitlines() for c in ('17c6901','4c18cb2')}
result['commit_gap_seconds'] = (dt.datetime.fromisoformat(result['commit_times']['4c18cb2'][1])-dt.datetime.fromisoformat(result['commit_times']['17c6901'][1])).total_seconds()
incident = (ROOT/'ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md').read_text()
assert 'chênh thời điểm PUSH không đo được (không có log push)' in incident
assert 'P2 19 tệp `rig/` đã được phiên kia vá ở `17c6901`' in incident
result['receipt11_old_anchors_absent'] = all(s not in (ROOT/'ops/reviews/pr468-hoso-4-packet-review-11-codex-verdict.receipt.yaml').read_text() for s in ['# gói lượt 9 thiếu 19 tệp rig/ đã phục dựng) vá ở commit chứa verdict này.','(commit chứa verdict lượt 11 + bản vá 2 P2)'])
save('standards',result)
note('- `ghi-nhan-luot11-gan-sai-commit-va-moc-van-chuyen` [P2]: **ĐÃ VÁ THẬT** tại df0800c. Receipt 11 sửa đúng hai mỏ neo (header/ghi chú), chỉ 1 lá YAML prose đổi; GHI-NHAN đồng bộ 2 chỗ. Git đo 19 tệp rig thêm tại 17c6901, 0 tại 4c18cb2; timestamp commit cách 1598 s, hồ sơ đã bỏ suy luận chênh PUSH 5 s. Identity/assurance/băm/neo/verdict lịch sử giữ nguyên. Bằng chứng: `do-review13/standards.json`.')

p12 = ROOT/'ops/reviews/pr468-hoso-4-packet-review-12-codex'
files = [p for p in p12.rglob('*') if p.is_file() and not p.is_symlink()]
result['round12_package'] = {'regular_count':len(files),
    'symlinks':[str(p.relative_to(p12)) for p in p12.rglob('*') if p.is_symlink()],
    'launcher_source_candidates':[str(p.relative_to(p12)) for p in files if p.name in ('run.json','PROMPT.md','prompt.snapshot') or 'session' in p.name.lower()],
    'files':[str(p.relative_to(p12)) for p in files]}
result['receipt12_verdict_projection_equal'] = (BASE/'tai-lieu/pr468-hoso-4-packet-review-12-codex-verdict.md').read_bytes() == (ROOT/'ops/reviews/pr468-hoso-4-packet-review-12-codex-verdict.md').read_bytes()
result['receipt12_finding_headers'] = re.findall(r'^### ([a-z0-9-]+)  \[(P[123])\]', (ROOT/'ops/reviews/pr468-hoso-4-packet-review-12-codex-verdict.md').read_text(), re.M)
result['round12_final_check'] = json.loads((p12/'final-check.json').read_text())
readme = (ROOT/'ops/reviews/README.md').read_text()
result['round12_readme_rows'] = [l for l in readme.splitlines() if l.startswith('| [`pr468-hoso-4-packet-review-12-codex-verdict.md`]')]
result['round12_durations'] = {'receipt':1166.934,'one_decimal':round(1166.934,1),'integer':round(1166.934)}
save('standards',result)
note('Standards lượt 12: verdict 23631 byte, SHA256 b4b2671d5d053785232486460251a519b6efd47cff196e672260f3258228d0bd; neo df0800c là commit đầu tiên, blob và ancestry đúng. README/GHI-NHAN khớp 2 P1/2 P2 và làm tròn 1166.934→1166.9/1167. Gói không có raw run/session/prompt để tự xác minh thread, model 6/6, prompt hash, runtime 1166.934 s, stdout 536028 B hoặc hai lần preflight rc=11: KHÔNG ĐO ĐƯỢC độc lập; chưa coi lời khai vận chuyển là phép đo của reviewer.')

layout = OUT/'manifest12-layout'
layout.mkdir(exist_ok=True)
manifest = p12/'ARTIFACTS.sha256'
entries=[]
for line in manifest.read_text().splitlines():
    digest, rel = line.split('  ',1)
    rp=Path(rel)
    assert not rp.is_absolute() and '..' not in rp.parts and 'tmp' not in rp.parts
    src = ROOT/'ops/reviews/pr468-hoso-4-packet-review-12-codex-verdict.md' if rel == 'VERDICT.md' else p12/rel.removeprefix('do-review12/')
    assert stat.S_ISREG(src.lstat().st_mode) and not src.is_symlink()
    dest=layout/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(src,dest)
    entries.append({'path':rel,'sha256_equal':sha(src.read_bytes())==digest,'regular_file':True})
shutil.copyfile(manifest,layout/'ARTIFACTS.sha256')
p=subprocess.run(['sha256sum','-c','ARTIFACTS.sha256'],cwd=layout,capture_output=True)
(OUT/'manifest12.stdout').write_bytes(p.stdout)
(OUT/'manifest12.stderr').write_bytes(p.stderr)
result['manifest12']={'entries':len(entries),'unique_paths':len({e['path'] for e in entries}),'rc':p.returncode,'all_hashes_match':all(e['sha256_equal'] for e in entries),'entries_detail':entries}
save('standards',result)
assert p.returncode == 0 and len(entries) == 178
note('Gói lượt 12: sha256sum -c chạy thật sau ánh xạ DOC-MANIFEST, 178/178 ĐẠT rc=0; tất cả entry là tệp thường, không symlink/tmp. Gói có 179 tệp thường = 177 hiện vật + ARTIFACTS + DOC-MANIFEST; verdict ở ngoài. Byte lịch sử được bảo toàn. Bằng chứng: `do-review13/manifest12.stdout`.')
