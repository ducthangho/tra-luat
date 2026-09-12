import datetime as dt
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

import yaml

from measure import BASE, ROOT, OUT, PREV, SHA, git, note, save

result={'utc':dt.datetime.now(dt.timezone.utc).isoformat()}
sys.path.insert(0,str(ROOT/'ops'))
spec=importlib.util.spec_from_file_location('review13_lease',ROOT/'ops/lease_publish.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
items=mod._quet_lease_toan_kho(ROOT,doi_chieu_ref=False,chan_nhanh_tut_sau=True)
result['snapshot_blob_path_pairs']=len(items)
result['old456']=[]
result['wp461']=[]
for item in items:
    d=item['lease']
    if d.get('packet_issue') not in (456,461):
        continue
    row={'lease_id':d.get('lease_id'),'blob':item['blob'],'path':item['path'],'representative_ref':item['ref'],
         'expiry':str(d.get('lease_expires_at_utc')),'state':mod._phan_loai_lease(d),
         'write_set':d.get('write_set'),'tombstone':d.get('da_bi_thay_the'),
         'symmetric_tombstone':mod._bia_mo_doi_xung(d,items)}
    result['old456' if d['packet_issue']==456 else 'wp461'].append(row)
by_id={}
for item in items:
    by_id.setdefault(item['lease'].get('lease_id'),[]).append(item['lease'])
links=[]
for p in sorted((ROOT/'ops/leases').glob('gate-tach-job-cat-chi-phi-exec-1*.yaml')):
    d=yaml.safe_load(p.read_bytes())
    for prev in mod._danh_sach_thay_the_cho(d.get('thay_the_cho')):
        reverse=[x.get('da_bi_thay_the') for x in by_id[prev]]
        links.append({'old':prev,'new':d['lease_id'],'old_reverse_values':reverse,'at_least_one_reverse':d['lease_id'] in reverse})
result['replacement_links']=links
assert len(links)==4 and all(e['at_least_one_reverse'] for e in links)
contracts=[]
for name,issue in [('gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906.yaml',463),
                   ('lo-319-linux-bang-chung-xanh-exec-1-claude-20260906.yaml.nhap',464),
                   ('mutant-windows-subagent-ghi-detect-exec-1-claude-20260906.yaml.nhap',465),
                   ('mutant-windows-nhanh-don-duoc-exec-1-claude-20260906.yaml.nhap',466)]:
    p=ROOT/'ops/leases'/name
    d=yaml.safe_load(p.read_bytes())
    raw=(ROOT/d['spec_path']).read_bytes()
    h=hashlib.sha256(raw).hexdigest()
    issuep=next((ROOT/'ops/issues').glob(str(issue)+'-*.md'))
    text=issuep.read_text()
    anchors=re.findall('`'+re.escape(d['spec_path'])+r'` @ `([0-9a-f]{40})`',text)
    row={'issue':issue,'revision':d['revision'],'generation':d['generation'],'spec_sha256':h,
         'aliases_equal':d['spec_hash']==d['spec_sha256']==h,
         'spec_projection_equal':(BASE/'tai-lieu'/Path(d['spec_path']).name).read_bytes()==raw,
         'lease_projection_equal':(BASE/'tai-lieu'/name).read_bytes()==p.read_bytes(),
         'issue_projection_equal':(BASE/'tai-lieu'/issuep.name).read_bytes()==issuep.read_bytes(),
         'issue_hash_present':h in text,'anchor_commits':anchors,
         'anchor_blobs_equal':all(git('show',a+':'+d['spec_path'])==raw for a in anchors),
         'null_fields':[k for k,v in d.items() if v is None],
         'write_set':d['write_set']}
    assert all(row[k] for k in ['aliases_equal','spec_projection_equal','lease_projection_equal','issue_projection_equal','issue_hash_present','anchor_blobs_equal']) and anchors
    if issue==463:
        row['write_set_sha256']=hashlib.sha256(('\n'.join(sorted(d['write_set']))+'\n').encode()).hexdigest()
        assert row['write_set_sha256']==d['write_set_hash']
        row['lease_minutes']=(dt.datetime.fromisoformat(d['lease_expires_at_utc'].replace('Z','+00:00'))-dt.datetime.fromisoformat(d['leased_at_utc'].replace('Z','+00:00'))).total_seconds()/60
        row['git_anchors']={k:d[k] for k in ['base_sha','start_from_sha','reviewed_sha_required']}
    contracts.append(row)
result['contracts']=contracts
result['spec_lease_issue_runtime_delta_since12']=git('diff','--name-only',PREV,SHA,'--','ops/specs','ops/leases','ops/issues','.github','.claude','scripts','ops/lease_publish.py').decode().splitlines()
doc=ROOT/'ops/reviews/DOC-READBACK-SAU-HAN-456.md'
result['readback_projection_equal']=doc.read_bytes()==(BASE/'tai-lieu'/doc.name).read_bytes()
result['readback_delay_seconds']=(dt.datetime.fromisoformat('2026-09-07T14:39:17+00:00')-dt.datetime.fromisoformat('2026-09-07T14:30:07+00:00')).total_seconds()
result['readback_blob_delay_seconds']=180
result['readback_changes']=git('diff','e377c42','f77f198','--','ops/reviews/DOC-READBACK-SAU-HAN-456.md').decode()
result['source_readbacks_equal_reviewer_stdout']={p:(BASE/('ai-dang-giu-'+p+'.txt')).read_bytes()==(OUT/('ai-dang-giu-'+p+'.stdout')).read_bytes() for p in ['ci.yml','ci_dang_ky_test.py','pretooluse_guard_test.py']}
docclaims=json.loads((OUT/'doc-claims.stdout').read_text())
result['doc_claims_summary']={k:v for k,v in docclaims.items() if k not in ['advisory','basis']}
save('supplement',result)
note('Bổ sung Spec/readback: 4/4 spec hash/alias/bản chiếu Issue/lease/blob neo đều khớp; r4 1440 phút, 2 path, 3 neo d28c4b1 và write-set hash đúng; 4/4 cạnh thay thế đúng hai chiều theo từng bản có bia mộ. Không đổi spec/lease/Issue/runtime sau 02b0b86. Readback mới trùng byte stdout executor 20:45Z trên cả 3 path. 303 remote + 1 local = 304 ref trong sandbox này; số 306 ở DOC thuộc máy khác lúc 14:39Z, KHÔNG ĐO ĐƯỢC lại từ snapshot chỉ có 1 local head, không coi 304/306 là mâu thuẫn. 14:39:17−14:30:07 = 550 s = 9 phút 10 giây. Bằng chứng: do-review13/supplement.json.')
note('Cổng còn lại đã xong: lease_publish_test rc=0, 121/121, chạy 121/bỏ qua 0; bien_nhan_v2 rc=0, 27 v2 + 11 legacy + 42 nợ = 80, vi phạm 0; doc-claims strict rc=0 ok:true, 106 tệp/367 advisory/0 cờ cứng, không quét ops; lease r4 check rc=0 có ĐĂNG ĐƯỢC, tự khai không đo hai lớp GitHub. Không dùng các số của lượt lịch sử làm kết quả cổng vừa chạy.')
