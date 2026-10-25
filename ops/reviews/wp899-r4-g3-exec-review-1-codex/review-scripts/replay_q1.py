import json,yaml,re,subprocess,hashlib,pathlib,datetime,importlib.util,collections,contextlib,io
R=pathlib.Path('.review').resolve(); root=pathlib.Path.cwd()
s=importlib.util.spec_from_file_location('cp',root/'ops/ci_provenance.py'); m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def stamp(s): return datetime.datetime.fromisoformat(s.replace('Z','+00:00')).replace(microsecond=0)
def name(y):
 if 'name' in y:return y['name'] if isinstance(y['name'],str) and '${{' not in y['name'] else None
 v=y.get('run',y.get('uses'));return 'Run '+v.split('\n')[0] if isinstance(v,str) else None
out={}; table=[]
for rid in (39342960764,40074551995):
 d=root/f'.review-input/a10/out-{rid}'; run=json.loads((d/'run.json').read_bytes()); jobs=json.loads((d/'jobs.json').read_bytes())['jobs']; frozen=yaml.safe_load((d/'provenance.yaml').read_bytes())
 wf=yaml.safe_load(subprocess.run(['git','show',run['head_sha']+':'+run['path']],capture_output=True,check=True).stdout)
 data={}; cnt=collections.Counter()
 for j in jobs:
  b=(root/f'.review-input/log-that/{rid}/{j["id"]}.log').read_bytes();data[j['id']]=b
  h=hashlib.sha256(b).hexdigest(); expected=frozen['log_day_du'][j['id']]
  assert h==expected['sha256'] and len(b)==expected['bytes']
  heads=[]
  for ln in b.decode('utf8').splitlines():
   mt=re.match(r'^(\S+) ##\[group\]Run (.*)$',ln)
   if mt:heads.append(mt.groups())
  keys=[]
  for k,v in wf['jobs'].items():
   for x in (k,v.get('name')):
    if isinstance(x,str) and '${{' not in x and (j['name']==x or (j['name'].startswith(x+' (') and j['name'].endswith(')'))):keys.append(k);break
  assert len(keys)==1,keys
  ys=wf['jobs'][keys[0]]['steps'];rest=[s for s in sorted(j['steps'],key=lambda s:s['number']) if s['name'] not in ('Set up job','Complete job') and not s['name'].startswith('Post ')]
  ran=[s for s in rest if s['conclusion']!='skipped']
  counts_ok=len(heads)==len(ran) and len(rest)==len(ys)
  names_ok=len(rest)==len(ys) and all(s['name']==name(y) for s,y in zip(rest,ys))
  windows_ok=len(heads)==len(ran) and all(stamp(s['started_at'])<=stamp(hh[0])<=stamp(s['completed_at']) for hh,s in zip(heads,ran))
  heq=sum(s['name']=='Run '+hh[1] for hh,s in zip(heads,ran))
  unique=sum(sum(stamp(s['started_at'])<=stamp(hh[0])<=stamp(s['completed_at']) for s in ran)==1 for hh in heads)
  got=next(g for g in frozen['moc']['gate_output']['jobs'] if g['job_id']==j['id'])['ghep_buoc']
  table.append({'run':rid,'job_id':j['id'],'job':j['name'],'yaml_job':keys[0],'groups':len(heads),'rest_ran':len(ran),'rest_yaml':len(rest),'yaml':len(ys),'counts_ok':counts_ok,'names_ok':names_ok,'windows_ok':windows_ok,'name_header_equal':heq,'unique_windows':unique,'tool':got,'log_sha256':h})
  cnt.update(jobs=1,groups=len(heads),ran=len(ran),rest=len(rest),yaml=len(ys),names_equal=sum(s['name']==name(y) for s,y in zip(rest,ys)),windows_equal=sum(stamp(s['started_at'])<=stamp(hh[0])<=stamp(s['completed_at']) for hh,s in zip(heads,ran)),name_header_equal=heq,unique_windows=unique)
  assert counts_ok and names_ok and windows_ok
 calls=[]
 def fake(url):
  calls.append(url)
  if url.endswith(f'/runs/{rid}'):return 200,(d/'run.json').read_bytes()
  if '/attempts/1/jobs?' in url:return 200,json.dumps({'total_count':len(jobs),'jobs':jobs}).encode()
  if '/artifacts?' in url:
   arts=frozen['moc']['gate_output']['artifacts'];return 200,json.dumps({'total_count':len(arts),'artifacts':arts}).encode()
  mt=re.search(r'/jobs/(\d+)/logs$',url)
  if mt:return 200,data[int(mt[1])]
  raise AssertionError(url)
 buf=io.StringIO()
 with contextlib.redirect_stdout(buf):rc=m.main(['thu','--repo','ducthangho/tra-luat','--run',str(rid),'--attempt','1','--out',str(R/f'replay-{rid}')],goi=fake)
 actual=(R/f'replay-{rid}/provenance.yaml').read_bytes();(R/f'replay-{rid}.stdout.txt').write_text(buf.getvalue())
 pv=yaml.safe_load(actual)
 out[str(rid)]={'counts':dict(cnt),'rc':rc,'calls':calls,'provenance_byte_equal':actual==(d/'provenance.yaml').read_bytes(),'replay_hash':hashlib.sha256(actual).hexdigest(),'checkout_states':dict(collections.Counter(z['trang_thai'] for z in pv['moc']['checkout'])),'ghep_states':dict(collections.Counter(z['ghep_buoc']['trang_thai'] for z in pv['moc']['gate_output']['jobs']))}
 assert rc==0 and out[str(rid)]['provenance_byte_equal']
(R/'q1-details.json').write_text(json.dumps(table,ensure_ascii=False,indent=2));(R/'q1-summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False,indent=2))
