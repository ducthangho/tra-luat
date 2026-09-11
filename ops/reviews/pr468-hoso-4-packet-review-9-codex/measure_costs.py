import collections, csv, datetime as dt, hashlib, json, pathlib, re, shutil, statistics as st, subprocess, sys, yaml
B=pathlib.Path(__file__).resolve().parents[1]; R=B/'cay-kho'; O=B/'do-review9'; SRC=R/'ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5'; DST=O/'nen-a1-a5'
shutil.copytree(SRC,DST,dirs_exist_ok=True); rr=subprocess.run([sys.executable,'-B',str(DST/'tinh.py')],capture_output=True); (O/'nen-replay.log').write_bytes(rr.stdout+rr.stderr)
jobs=list(csv.DictReader((SRC/'job.tsv').open(),delimiter='\t'));steps=list(csv.DictReader((SRC/'buoc.tsv').open(),delimiter='\t'));runs=json.loads((SRC/'raw/runs.json').read_text());spec=(B/'tai-lieu/GATE-TACH-JOB-CAT-CHI-PHI.md').read_text()
report={'regenerate_rc':rr.returncode,'regenerate_equal':{p.name:p.read_bytes()==(DST/p.name).read_bytes() for p in SRC.iterdir() if p.is_file()},'runs':len(runs),'jobs':len(jobs),'steps':len(steps),'columns_job':len(jobs[0]),'columns_step':len(steps[0])}
heads=re.findall(r'^\| `([0-9a-f]{7})` \| \*\*[0-9,]+ p',spec,re.M);assert len(heads)==11
sec=lambda j:(dt.datetime.fromisoformat(j['completed_at'])-dt.datetime.fromisoformat(j['started_at'])).total_seconds()
stat=lambda v:dict(n=len(v),minimum=min(v),maximum=max(v),median=st.median(v),mean=st.mean(v),range=max(v)-min(v))
job=lambda h,p:next(j for j in jobs if j['head7']==h and p in j['job_name'])
report['eleven']=[]
for h in heads:
 j=job(h,'windows');y=yaml.safe_load(subprocess.check_output(['git','-C',str(R),'show',h+':.github/workflows/ci.yml']))
 report['eleven'].append(dict(head=h,run=j['run_id'],branch=j['head_branch'],event=j['event'],steps=len(y['jobs']['gate']['steps']),windows_seconds=sec(j),windows_minutes=sec(j)/60))
report['sample']=dict(master=sum(x['branch']=='master' for x in report['eleven']),other=sum(x['branch']!='master' for x in report['eleven']),workloads=dict(collections.Counter(x['steps'] for x in report['eleven'])),windows_stats=stat([x['windows_minutes'] for x in report['eleven']]))
report['ratios']={}
for prefix in ['test registry','tl selftest','packet-loop selftest','G5 kiem ban ke','lease-publish selftest','bien-nhan v2 selftest','job trọn']:
 pairs=[]
 for h in heads:
  u,w=job(h,'ubuntu'),job(h,'windows')
  if u['conclusion']!='success' or w['conclusion']!='success':continue
  if prefix=='job trọn':us,ws=sec(u),sec(w)
  else:
   matching=lambda p:[s for s in steps if s['run_id']==u['run_id'] and p in s['job_name'] and s['step_name'].startswith(prefix) and s['step_conclusion']=='success']
   a,b=matching('ubuntu'),matching('windows')
   if not a or not b:continue
   assert len(a)==len(b)==1
   us,ws=int(a[0]['giay']),int(b[0]['giay'])
  pairs.append(dict(head=h,run=u['run_id'],ubuntu_seconds=us,windows_seconds=ws,ratio=ws/us,lower=(ws-.5)/(us+.5),upper=(ws+.5)/(us-.5)))
 measured=stat([p['ratio'] for p in pairs]);lo=st.median([p['lower'] for p in pairs]);hi=st.median([p['upper'] for p in pairs])
 row=next(line for line in spec.splitlines() if line.startswith('|') and prefix in line and '×' in line)
 cells=row.split('|')[2:];expected=[re.search(r'\d+(?:,\d+)?',v).group() for v in cells[:4]]
 actual=[str(len(pairs))]+[f'{measured[k]:.2f}'.replace('.',',') for k in ['minimum','maximum','median']]
 dlo=re.findall(r'\d+,\d+',cells[4]); alo=[f'{lo:.2f}'.replace('.',','),f'{hi:.2f}'.replace('.',',')] if dlo else []
 report['ratios'][prefix]=dict(**measured,rounding_lower=lo,rounding_upper=hi,expected=expected,display=actual,cells_match=[a==b for a,b in zip(expected,actual)],range_expected=dlo,range_display=alo,range_matches=dlo==alo,pairs=pairs)
report['costs']={}
for plat in ['ubuntu','windows']:
 j=job('426bfc0',plat);ss=[s for s in steps if s['run_id']==j['run_id'] and plat in s['job_name']];get=lambda p:next(int(s['giay'])/60 for s in ss if s['step_name'].startswith(p))
 setup=sum(int(s['giay']) for s in ss if 1<=int(s['step_number'])<=10)/60;total=sum(int(s['giay']) for s in ss)/60;reg=get('test registry');pkt=get('packet-loop selftest')
 report['costs'][plat]=dict(job=sec(j)/60,step_sum=total,setup=setup,registry=reg,packet=pkt,remaining=total-reg-pkt,split_registry=reg+setup,split_packet=pkt+setup,total_after=total+2*setup)
u,w=report['costs']['ubuntu'],report['costs']['windows'];report['cost_arithmetic']=dict(before=u['job']+2*w['job'],after_raw_seconds=u['total_after']+2*w['total_after'],longest_windows=w['split_registry'],A1_threshold=25,A5_threshold=135)
report['cancelled']=[{k:j[k] for k in ['run_id','head7','head_branch','event','job_name','conclusion']}|dict(seconds=sec(j),minutes=sec(j)/60) for j in jobs if j['conclusion']!='success']
report['step_seconds_match_timestamps']=all(int(s['giay'])==sec(s) for s in steps)
(O/'costs.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({**report,'eleven':report['eleven'],'ratios':{k:{a:b for a,b in v.items() if a!='pairs'} for k,v in report['ratios'].items()}},ensure_ascii=False,indent=2))
