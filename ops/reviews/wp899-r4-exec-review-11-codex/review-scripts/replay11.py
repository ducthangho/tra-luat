import collections, hashlib, importlib.util, json, pathlib, urllib.parse, yaml
R=pathlib.Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('product8',root/'ops/ci_provenance.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
checks=[]
for line in (root/'.review-input/log-that/SHA256SUMS').read_text().splitlines():
    want,name=line.split(maxsplit=1);p=root/'.review-input/log-that'/name.lstrip('*')
    if not p.exists():
        matches=list((root/'.review-input/log-that').rglob(pathlib.Path(name).name));assert len(matches)==1;p=matches[0]
    actual=hashlib.sha256(p.read_bytes()).hexdigest();checks.append({'path':str(p.relative_to(root)),'expected':want,'actual':actual});assert actual==want
reports=[]
for rid in (39342960764,40074551995):
    src=root/f'.review-input/a10/out-{rid}';runbytes=(src/'run.json').read_bytes();r=json.loads(runbytes);jobs=json.loads((src/'jobs.json').read_bytes())['jobs']
    oldbytes=(src/'provenance.yaml').read_bytes();old=yaml.safe_load(oldbytes);arts=old['moc']['gate_output']['artifacts'];calls=[]
    def goi(url):
        calls.append(url);u=urllib.parse.urlsplit(url);q=urllib.parse.parse_qs(u.query);base='/repos/ducthangho/tra-luat/actions'
        if u.path==f'{base}/runs/{rid}':return 200,runbytes
        if u.path==f'{base}/runs/{rid}/attempts/1/jobs':data,key=jobs,'jobs'
        elif u.path==f'{base}/runs/{rid}/artifacts':data,key=arts,'artifacts'
        elif u.path.startswith(base+'/jobs/') and u.path.endswith('/logs'):
            jid=u.path.split('/')[-2];return 200,(root/f'.review-input/log-that/{rid}/{jid}.log').read_bytes()
        else:raise AssertionError(url)
        per=int(q['per_page'][0]);page=int(q['page'][0]);return 200,json.dumps({'total_count':len(data),key:data[(page-1)*per:page*per]}).encode()
    prov,files=m.thu('ducthangho/tra-luat',rid,1,goi,m.git_cuc_bo,wf=m.git_blob)
    m.ghi_nguyen_tu(R/f'replay-{rid}',files)
    newbytes=files['provenance.yaml'];gs=prov['moc']['gate_output']['jobs'];cs=prov['moc']['checkout']
    row={'run':rid,'byte_equal':newbytes==oldbytes,'new_sha256':hashlib.sha256(newbytes).hexdigest(),'old_sha256':hashlib.sha256(oldbytes).hexdigest(),'run_state':prov['moc']['run']['trang_thai'],'checkout':dict(collections.Counter(x['trang_thai'] for x in cs)),'ghep':dict(collections.Counter(x.get('ghep_buoc',{}).get('trang_thai') for x in gs)),'gate':dict(collections.Counter(x['trang_thai'] for x in gs)),'markers':[{'job':g['name'],**x} for g in gs for x in g.get('dau_duong',[])],'labels':list({tuple(x['labels']) for x in gs}),'calls':calls}
    if newbytes!=oldbytes:
        import difflib
        (R/f'replay-{rid}.diff').write_text(''.join(difflib.unified_diff(oldbytes.decode().splitlines(True),newbytes.decode().splitlines(True))))
    reports.append(row)
(R/'replay8-results.json').write_text(json.dumps({'log_hashes':checks,'runs':reports},ensure_ascii=False,indent=2))
print('LOG HASHES',len(checks),'/',len(checks));print(json.dumps(reports,ensure_ascii=False,indent=2))
assert all(x['byte_equal'] for x in reports)
