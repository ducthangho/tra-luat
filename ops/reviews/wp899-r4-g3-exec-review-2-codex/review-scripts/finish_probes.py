import pathlib,sys,subprocess,json,os,importlib.util,datetime,copy,hashlib
R=pathlib.Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text();out=R/'extra-r4';rows=[]
for name,old,new in (
 ('gio_thieu_header_lay_rest','(h := _gio(b["gio"], TS))','(h := _gio(b["gio"], TS) or a)'),
 ('gio_bo_can_duoi','a <= h <= z','h <= z'),
 ('gio_bo_can_tren','a <= h <= z','a <= h')):
 assert src.count(old)==1
 p=out/(name+'.py');p.write_text(src.replace(old,new))
 env=dict(os.environ,CI_PROVENANCE_MA=str(p),PYTHONDONTWRITEBYTECODE='1')
 q=subprocess.run([sys.executable,'-B',str(R/'extra_mutants_r4.py'),'cases'],capture_output=True,env=env)
 cases=json.loads(q.stdout);(out/(name+'.stdout.txt')).write_bytes(q.stdout)
 bad=[c for c in cases if c['rc']]
 rows.append({'name':name,'old':old,'new':new,'cases':cases,'rc':q.returncode,
              'rank':t.phan_hang(next(c['rc'] for c in cases if c['case']=='c38_ghep_lech_gio'),next(c['output'] for c in cases if c['case']=='c38_ghep_lech_gio'),'c38_ghep_lech_gio')})
 print(name,rows[-1]['rank'],[(c['case'],c['rc']) for c in bad],flush=True)
 (R/'adapted-time-mutants.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))

# Keep the checkout log and workflow fixed; vary only header/REST timestamps.
w=t.wf_tu(t.X);lg=t.log_voi(t.buoc(t.X,'THU: 4/4 dat'));st0=t.buoc_rest(lg,w)
cases=[]
for label,header,start,end,expected in (
 ('year0','0000-10-19T23:45:04Z','0000-10-19T23:45:04Z','0000-10-19T23:45:04Z','not_measured'),
 ('leap2024','2024-02-29T23:45:04.123456789012345678901234567890Z','2024-02-29T23:45:04Z','2024-02-29T23:45:04Z','passed'),
 ('notleap2026','2026-02-29T23:45:04.1Z','2026-02-28T00:00:00Z','2026-03-01T00:00:00Z','not_measured'),
 ('century1900','1900-02-29T23:45:04Z','1900-02-28T00:00:00Z','1900-03-01T00:00:00Z','not_measured'),
 ('century2000','2000-02-29T23:45:04Z','2000-02-29T23:45:04Z','2000-02-29T23:45:04Z','passed'),
 ('minyear','0001-01-01T00:00:00Z','0001-01-01T00:00:00Z','0001-01-01T00:00:00Z','passed'),
 ('maxyear','9999-12-31T23:59:59.999999999Z','9999-12-31T23:59:59Z','9999-12-31T23:59:59Z','passed'),
 ('space_in_timestamp','2026-10-19 23:45:04Z','2026-10-19T23:45:04Z','2026-10-19T23:45:04Z','not_measured'),
 ('tab_after_timestamp',t.T+'\t',t.T[:19]+'Z',t.T[:19]+'Z','not_measured'),
 ('double_space_after_timestamp',t.T+' ',t.T[:19]+'Z',t.T[:19]+'Z','not_measured'),
 ('longfraction',t.T[:19]+'.'+'7'*10000+'Z',t.T[:19]+'Z',t.T[:19]+'Z','passed'),
 ('reversed_window',t.T,t.T[:19]+'Z','2026-10-19T23:45:03Z','not_measured')):
 st=copy.deepcopy(st0);st[2].update(started_at=start,completed_at=end)
 log=lg.replace(t.T+' ##[group]Run ',header+' ##[group]Run ',1)
 rc,stdout,p,_=t.chay([(t.job(1,steps=st),log)],wf=w)
 g=t.gate(p);good=g['ghep_buoc']['trang_thai']==expected and (g['trang_thai']=='passed' if expected=='passed' else g['dau_duong']==[])
 cases.append({'case':label,'header_sha256':hashlib.sha256(header.encode()).hexdigest(),'header_length':len(header),'start':start,'end':end,'expected':expected,'ok':good,'rc':rc,'gate':g})
 print(label,good,g['ghep_buoc'],flush=True)
assert all(c['ok'] for c in cases)
m=t.nap();dt=m._gio(t.T,m.TS);assert dt.tzinfo is None and dt.microsecond==0
(R/'calendar-extra.json').write_text(json.dumps({'rows':cases,'naive_utc':{'type':type(dt).__name__,'tzinfo':None,'microsecond':dt.microsecond}},ensure_ascii=False,indent=2))
