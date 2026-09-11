import collections
import csv
import datetime as dt
import hashlib
import json
import pathlib
import shutil
import statistics
import subprocess
import yaml

BASE = pathlib.Path(__file__).resolve().parents[1]
ROOT = BASE / 'cay-kho'
SRC = ROOT/'ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5'
OUT = BASE/'do-review7'
DST = OUT/'nen-a1-a5'
shutil.copytree(SRC, DST, dirs_exist_ok=True)
r = subprocess.run(['python3', str(DST/'tinh.py')], capture_output=True, text=True)
(OUT/'nen-replay.log').write_text(r.stdout+r.stderr)
report = {'rc':r.returncode,'equal':{p.name:p.read_bytes()==(DST/p.name).read_bytes() for p in SRC.iterdir() if p.is_file()}}
jobs=list(csv.DictReader((SRC/'job.tsv').open(), delimiter='\t'))
steps=list(csv.DictReader((SRC/'buoc.tsv').open(), delimiter='\t'))
runs=json.loads((SRC/'raw/runs.json').read_text())
report.update(runs=len(runs),jobs=len(jobs),steps=len(steps),job_columns=len(jobs[0]),step_columns=len(steps[0]))
report['conclusions']=dict(collections.Counter(j['conclusion'] for j in jobs))
report['branch_count']=dict(collections.Counter(v['head_branch'] for v in runs.values()))
def stat(vals): return dict(n=len(vals),min=min(vals),max=max(vals),range=max(vals)-min(vals),median=statistics.median(vals),mean=statistics.mean(vals))
def minutes(j): return (dt.datetime.fromisoformat(j['completed_at'])-dt.datetime.fromisoformat(j['started_at'])).total_seconds()/60
report['summary']={}
for platform in ['ubuntu','windows']:
    for filt in ['master-success','all-success']:
        rows=[j for j in jobs if platform in j['job_name'] and j['conclusion']=='success' and (filt!='master-success' or j['head_branch']=='master')]
        report['summary'][platform+'-'+filt]=stat([minutes(j) for j in rows])
heads=['8ce02fd','82e01a4','1b3caa1','c0f18ac','28cb898','b912e5f','cacaba3','d28c4b1','62a6385','771c6ed','0c3405f']
report['eleven']=[]
for head in heads:
    j=next(j for j in jobs if j['head7']==head and 'windows' in j['job_name'])
    ci=subprocess.check_output(['git','-C',str(ROOT),'show',head+':.github/workflows/ci.yml'],text=True)
    s=yaml.safe_load(ci)['jobs']['gate']['steps']
    report['eleven'].append(dict(head=head,run=j['run_id'],branch=j['head_branch'],event=j['event'],minutes=j['phut'],steps=len(s),receipt_v2=any('bien-nhan v2' in st.get('name','') for st in s)))
report['eleven_stats']=stat([minutes(j) for j in jobs if j['head7'] in heads and 'windows' in j['job_name']])
report['eleven_master_count']=sum(j['branch']=='master' for j in report['eleven'])
report['split_costs']={}
for platform in ['ubuntu','windows']:
    ss=[s for s in steps if s['run_id']=='34045664423' and platform in s['job_name']]
    setup1=sum(int(s['giay']) for s in ss if 1<=int(s['step_number'])<=10)/60
    setup2=sum(int(s['giay']) for s in ss if 2<=int(s['step_number'])<=10)/60
    tr=next(int(s['giay'])/60 for s in ss if s['step_name'].startswith('test registry'))
    pl=next(int(s['giay'])/60 for s in ss if s['step_name']=='packet-loop selftest')
    job=next(minutes(j) for j in jobs if j['run_id']=='34045664423' and platform in j['job_name'])
    step_sum=sum(int(s['giay']) for s in ss)/60
    report['split_costs'][platform]=dict(job=job,step_sum=step_sum,setup1_10=setup1,setup2_10=setup2,registry=tr,packet_loop=pl,
        remaining=step_sum-tr-pl,split_registry=tr+setup1,split_packet=pl+setup1,total_steps=step_sum+2*setup1)
report['ratios']={}
for prefix in ['test registry','tl selftest','packet-loop selftest','G5 kiem ban ke','lease-publish selftest','bien-nhan v2 selftest']:
    vals=[]; pairs=[]
    for head in heads:
        ss=[s for s in steps if s['head7']==head and s['step_name'].startswith(prefix) and s['step_conclusion']=='success']
        u=[s for s in ss if 'ubuntu' in s['job_name']];w=[s for s in ss if 'windows' in s['job_name']]
        if not (u and w): continue
        assert len(u)==len(w)==1,(head,prefix)
        val=int(w[0]['giay'])/int(u[0]['giay']); vals.append(val)
        pairs.append(dict(head=head,ubuntu=int(u[0]['giay']),windows=int(w[0]['giay'])))
    report['ratios'][prefix]=dict(stat(vals),pairs=pairs,
        rounding_lower=statistics.median([(p['windows']-.5)/(p['ubuntu']+.5) for p in pairs]),
        rounding_upper=statistics.median([(p['windows']+.5)/(p['ubuntu']-.5) for p in pairs]))
report['ratios']['job']=stat([minutes(next(j for j in jobs if j['head7']==head and 'windows' in j['job_name']))/minutes(next(j for j in jobs if j['head7']==head and 'ubuntu' in j['job_name'])) for head in heads])
u=report['split_costs']['ubuntu'];w=report['split_costs']['windows']
report['billing_estimate']=dict(before=u['job']+2*w['job'],after=u['total_steps']+2*w['total_steps'])
(OUT/'nen-measurements.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['eleven','ratios']},ensure_ascii=False,indent=2))
print('ratios',json.dumps({k:{a:b for a,b in v.items() if a!='pairs'} for k,v in report['ratios'].items()},ensure_ascii=False))
