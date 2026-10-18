import os, sys, subprocess, tempfile, pathlib, importlib.util, json, hashlib, tarfile, io
K = pathlib.Path('/home/user/rv773')
OUT = pathlib.Path(__file__).resolve().parent
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
def run(label, cmd, env=None):
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    (OUT / (label+'.log')).write_text('COMMAND: '+repr(cmd)+'\nRC: '+str(r.returncode)+'\n'+r.stdout+r.stderr)
    print(label, 'rc='+str(r.returncode), (r.stdout+r.stderr)[-350:].strip())
    return r
def load(name, path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
t=load('tests',K/'ops/land_evidence_nguon_test.py')
run('tree',[sys.executable,'-B',str(K/'ops/land_evidence_nguon.py'),'--root',str(K)])
for c in ('c6e2401','1a4c417','d60b9e6'):
    r=subprocess.run(['git','-C',str(K),'archive',c,'ops/land'],capture_output=True)
    assert r.returncode==0
    with tempfile.TemporaryDirectory() as d:
        with tarfile.open(fileobj=io.BytesIO(r.stdout)) as a: a.extractall(d,filter='data')
        run('history-'+c,[sys.executable,'-B',str(K/'ops/land_evidence_nguon.py'),'--root',d,'--tep','ops/land/pr765-wp743-land-evidence.yaml'])
m=t.nap(); m.MIEN_TRU_CUTOVER={}
rc,ra=t.kiem(m,K); (OUT/'no-exempt.log').write_text('RC: '+str(rc)+'\n'+ra)
print('no-exempt',rc,ra[-200:])
paths=subprocess.check_output(['git','-C',str(K),'ls-tree','-r','--name-only','c73af7b','ops/land'],text=True).splitlines()
ds={pathlib.Path(p).name:hashlib.sha256(subprocess.check_output(['git','-C',str(K),'show','c73af7b:'+p])).hexdigest() for p in paths if p.endswith('-land-evidence.yaml')}
assert ds==t.nap().MIEN_TRU_CUTOVER
print('cutover independent',len(ds),hashlib.sha256(json.dumps(sorted(ds.items())).encode()).hexdigest())
probes=[('duplicate',"x: 'measured - no source'\nx: ok\n",{'a.json':'{}'}),
 ('positive-number', 'x: {positive: 123, nguon_positive: a.txt}\n',{'a.txt':'text'}),
 ('source-number', 'x: {positive: 123, nguon_positive: 123}\n',{'a.txt':'text'}),
 ('fraction', "pre_merge_checks: ['2026-10-16T02:58:26.001Z']\n",{'readback-pr-9001.json':t.RB_PR}),
 ('offset-minus',"pre_merge_checks: ['2026-10-16T02:00:00-01:00']\n",{'readback-pr-9001.json':t.RB_PR}),
 ('offset-plus',"pre_merge_checks: ['2026-10-16T03:00:00+01:00']\n",{'readback-pr-9001.json':t.RB_PR}),
 ('mapping-key',"pre_merge_checks: {'2026-10-16T03:00:00Z': ok}\n",{'readback-pr-9001.json':t.RB_PR}),
 ('directory',"x: 'measured - ./ '\n",{}),
 ('multi-source',"x: {positive: '195/195 hong 0', nguon_positive: [a.txt, b.txt]}\n",{'a.txt':'195/195','b.txt':'hong 0'})]
for name,hs,p in probes:
    with t.cay(hs,p) as d:
        run('probe-'+name,[sys.executable,'-B',str(K/'ops/land_evidence_nguon.py'),'--root',str(d)])
for target in ('a.txt',t.TEN):
    with t.cay("x: {positive: '195/195 hong 0', nguon_positive: alias.txt}\n",{'a.txt':t.LOG}) as d:
        (d/'ops/land'/t.PROV/'alias.txt').symlink_to(d/'ops/land'/t.PROV/'a.txt' if target=='a.txt' else d/'ops/land'/t.TEN)
        run('symlink-'+('source' if target=='a.txt' else 'self'),[sys.executable,'-B',str(K/'ops/land_evidence_nguon.py'),'--root',str(d)])
src=(K/'ops/land_evidence_nguon.py').read_text()
mutations=[('tz', 'return t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)', 'return t.replace(tzinfo=datetime.timezone.utc)', 'c06'),
 ('tz-negative-only', 'return t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)', 'return t.replace(tzinfo=datetime.timezone.utc) if t.tzinfo and t.utcoffset().total_seconds() < 0 else t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)', 'c06'),
 ('rename','plat-x8-land-evidence.yaml','plat-x9-land-evidence.yaml','c10'),
 ('l2-content','if not any(mau.search(nd) for nd in noi_dung):','if False:','c05')]
for name,old,new,prefix in mutations:
    assert src.count(old)==1
    with tempfile.TemporaryDirectory() as d:
        p=pathlib.Path(d)/'validator.py'; p.write_text(src.replace(old,new))
        ca=next(c for c in t.CA if c.startswith(prefix+'_'))
        r=run('mutation-'+name,[sys.executable,'-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca',ca],dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(p)))
        assert r.returncode==3 and 'DO:'+ca+':' in r.stdout
