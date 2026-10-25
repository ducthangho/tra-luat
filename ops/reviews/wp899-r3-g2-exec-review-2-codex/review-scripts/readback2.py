import json,hashlib,re,runpy,subprocess,sys,contextlib,io
from pathlib import Path
import yaml
R=Path(__file__).resolve().parent; root=R.parent
m=runpy.run_path(str(root/'ops/ci_provenance.py')); reg=runpy.run_path(str(root/'.claude/dev/ci_dang_ky_test.py'))
out={'a10':{},'registry':{}}
for rid in (39342960764,40074551995):
    path=root/f'.review-input/a10/provenance-{rid}.yaml'; b=path.read_bytes(); frozen=yaml.safe_load(b); mc=frozen['moc']
    jpath=root/f'.review-input/a10/jobs-{rid}.json'; jdata=json.loads(jpath.read_bytes())
    if type(jdata) is list: jobs=[j for page in jdata for j in page['jobs']]
    else: jobs=jdata['jobs']
    run=mc['run']; rawrun={'id':rid,'run_attempt':run['run_attempt'],'event':run['event'],'head_sha':run['head_sha'],
                         'path':run['loi_khai_rest_path'],'check_suite_id':run['check_suite_id']}
    counts={'calls':[], 'verified_full_log_hashes':[]}
    def fake(url):
        counts['calls'].append(url)
        if re.search(rf'/runs/{rid}$',url):return 200,json.dumps(rawrun).encode()
        if '/attempts/1/jobs?' in url:return 200,json.dumps({'total_count':len(jobs),'jobs':jobs}).encode()
        if '/artifacts?' in url:return 200,json.dumps({'total_count':len(mc['gate_output']['artifacts']),'artifacts':mc['gate_output']['artifacts']}).encode()
        k=re.search(r'/jobs/(\d+)/logs$',url)
        if k:
            by=(root/f'.review-input/log-that/{k[1]}.log').read_bytes()
            given=frozen['log_day_du'][int(k[1])]
            counts['verified_full_log_hashes'].append({'job':int(k[1]),'sha256':hashlib.sha256(by).hexdigest(),'matches':hashlib.sha256(by).hexdigest()==given['sha256'] and len(by)==given['bytes']})
            return 200,by
        raise AssertionError(url)
    prov,files=m['thu']('ducthangho/tra-luat',rid,1,fake,m['git_cuc_bo'])
    target=R/f'a10-replay-{rid}'; m['ghi_nguyen_tu'](target,files)
    actual=files['provenance.yaml']; gs=prov['moc']['gate_output']['jobs']; co=prov['moc']['checkout']
    out['a10'][str(rid)]={'frozen_hash':hashlib.sha256(b).hexdigest(),'replay_hash':hashlib.sha256(actual).hexdigest(),
                         'byte_equal':b==actual,'counts':counts,'jobs':len(gs),
                         'checkout_states':{s:sum(c['trang_thai']==s for c in co) for s in ('passed','not_measured','failed')},
                         'gate_states':{s:sum(c['trang_thai']==s for c in gs) for s in ('passed','not_measured','failed')},
                         'marker_paths':[(g['name'],g.get('dau_duong',[])) for g in gs if g.get('dau_duong')],
                         'all_ubuntu':all(j['labels']==['ubuntu-latest'] for j in gs),
                         'not_measured':m['cac_trang_thai'](prov).count('not_measured')}
normal=reg['kiem'](root=root); removed=reg['kiem'](root=root,registry=reg['DANG_KY']-{'ops/ci_provenance_test.py'})
out['registry']['normal']=normal; out['registry']['removed']=removed
out['registry']['ruff_contract']=reg['loi_ruff_ci']()
sample=(R/'suite.stdout.txt').read_text(); pattern=reg['MOI']['ops/ci_provenance_test.py']
out['registry']['regex_equal_precedent']=pattern==reg['MOI']['ops/land_evidence_nguon_test.py']
out['registry']['accepts_suite']=reg['bang_chung_xanh'](sample,pattern)
bad={'unequal':sample.replace('CA: 35/35','CA: 34/35'), 'zero_mutants':sample.replace('74/74','0/0'), 'red':sample.replace('TONG: DAT','TONG: DO')}
assert all(s!=sample for s in bad.values())
out['registry']['rejects_bad']={k:not reg['bang_chung_xanh'](s,pattern) for k,s in bad.items()}
try:
    with contextlib.redirect_stdout(io.StringIO()):reg['phan_chung']()
except subprocess.CalledProcessError as e:out['registry']['fixture_failure']={'command':e.cmd,'rc':e.returncode,'stdout':e.stdout,'stderr':e.stderr}
out['yaml_version']=yaml.__version__
(R/'readback2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
