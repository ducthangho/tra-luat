from pathlib import Path
import csv, json, statistics as st, collections, re, subprocess, hashlib, datetime as dt
import yaml
R=Path(__file__).resolve().parents[1];T=R/'cay-kho';O=R/'do-review10'
rows=list(csv.DictReader((l for l in (R/'buoc_master.tsv').read_text().splitlines() if not l.startswith('#')),delimiter='\t'))
events=list(csv.DictReader((l for l in (R/'mau-11-run-event-branch.txt').read_text().splitlines() if not l.startswith('#')),delimiter='\t'))
S=T/'ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5'
archived=list(csv.DictReader((S/'buoc.tsv').open(),delimiter='\t'))
archivedjobs=list(csv.DictReader((S/'job.tsv').open(),delimiter='\t'))
spec=(T/'ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md').read_text()
def git(*a):return subprocess.check_output(['git','-C',str(T),*a],text=True)
def stats(v):return {'n':len(v),'min':min(v),'max':max(v),'median':st.median(v),'mean':st.mean(v),'range':max(v)-min(v)}
def num(s):return f'{s:.2f}'.replace('.',',')
jobs={};steps={}
for r in rows:
    key=(r['run_id'],r['nen']);j={k:r[k] for k in ['head','run_concl','job_concl','job_giay','so_buoc','so_skip']}
    assert key not in jobs or jobs[key]==j
    jobs[key]=j;steps.setdefault(key,[]).append(r)
report={'inputs':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'buoc_master.tsv',R/'mau-11-run-event-branch.txt',S/'buoc.tsv',S/'job.tsv']},'original_rows':len(rows),'original_runs':len({r['run_id'] for r in rows}),'eleven':[]}
for e in events:
    run=e['run_id'];u=jobs[(run,'ubuntu')];w=jobs[(run,'windows')]
    assert u['head']==w['head']==e['head'] and u['job_concl']==w['job_concl']=='success'
    oldj=next(x for x in archivedjobs if x['run_id']==run)
    assert (oldj['event'],oldj['head_branch'])==(e['event'],e['head_branch'])
    y=yaml.safe_load(git('show',e['head']+':.github/workflows/ci.yml'))
    report['eleven'].append(dict(e,ubuntu_seconds=int(u['job_giay']),windows_seconds=int(w['job_giay']),yaml_steps=len(y['jobs']['gate']['steps'])))
report['event_counts']=dict(collections.Counter(e['event'] for e in events))
report['branch_counts']=dict(collections.Counter('master' if e['head_branch']=='master' else 'branch' for e in events))
report['yaml_steps_counts']=dict(collections.Counter(e['yaml_steps'] for e in report['eleven']))
report['windows']=stats([e['windows_seconds']/60 for e in report['eleven']])
report['ratios']={}
for prefix in ['test registry','tl selftest','packet-loop selftest','G5 kiem ban ke','lease-publish selftest','bien-nhan v2 selftest','job trọn']:
    pairs=[]
    for e in events:
        run=e['run_id']
        if prefix=='job trọn':us,ws=(int(jobs[(run,p)]['job_giay']) for p in ['ubuntu','windows'])
        else:
            a,b=([x for x in steps[(run,p)] if x['buoc_ten'].startswith(prefix) and x['buoc_concl']=='success'] for p in ['ubuntu','windows'])
            if not a or not b:continue
            assert len(a)==len(b)==1
            us,ws=int(a[0]['buoc_giay']),int(b[0]['buoc_giay'])
        pairs.append({'run':run,'event':e['event'],'u':us,'w':ws,'ratio':ws/us,'lo':(ws-.5)/(us+.5),'hi':(ws+.5)/(us-.5)})
    q=stats([p['ratio'] for p in pairs]);lo=st.median(p['lo'] for p in pairs);hi=st.median(p['hi'] for p in pairs)
    row=next(s for s in spec.splitlines() if s.startswith('|') and prefix in s and '×' in s)
    cells=row.split('|')[2:]
    wanted=[re.search(r'\d+(?:,\d+)?',s).group() for s in cells[:4]]
    actual=[str(q['n']),num(q['min']),num(q['max']),num(q['median'])]
    intervals=re.findall(r'\d+,\d+',cells[4])
    report['ratios'][prefix]=dict(q,display=actual,spec=wanted,cells_match=actual==wanted,rounding_lo=lo,rounding_hi=hi,rounding_display=[num(lo),num(hi)],rounding_matches=not intervals or intervals==[num(lo),num(hi)],by_event={ev:stats([p['ratio'] for p in pairs if p['event']==ev]) for ev in report['event_counts']},pairs=pairs)
report['archived_seconds_diffs']=[];report['archived_seconds_not_in_supplied_tsv']=[]
for s in archived:
    key=(s['run_id'],'windows' if 'windows' in s['job_name'] else 'ubuntu')
    candidates=[x for x in steps.get(key,[]) if x['buoc_so']==s['step_number']]
    if not candidates:report['archived_seconds_not_in_supplied_tsv'].append({'run':s['run_id'],'step':s['step_number']});continue
    if len(candidates)!=1 or (s['giay'],s['step_conclusion'])!=(candidates[0]['buoc_giay'],candidates[0]['buoc_concl']):report['archived_seconds_diffs'].append({'run':s['run_id'],'step':s['step_number']})
report['archived_jobs_diffs']=[]
for j in archivedjobs:
    key=(j['run_id'],'windows' if 'windows' in j['job_name'] else 'ubuntu')
    duration=(dt.datetime.fromisoformat(j['completed_at'])-dt.datetime.fromisoformat(j['started_at'])).total_seconds()
    if key in jobs and duration!=int(jobs[key]['job_giay']):report['archived_jobs_diffs'].append(key)
report['raw_header_claim']='original TSV header says branch=master; actual data includes branch events. Superseded source per GATE revision 2.'
report['decomposition']={}
for p in ['ubuntu','windows']:
    ss=[{'buoc_so':s['step_number'],'buoc_giay':s['giay'],'buoc_ten':s['step_name']} for s in archived if s['run_id']=='34045664423' and p in s['job_name']]
    oldj=next(j for j in archivedjobs if j['run_id']=='34045664423' and p in j['job_name'])
    job=(dt.datetime.fromisoformat(oldj['completed_at'])-dt.datetime.fromisoformat(oldj['started_at'])).total_seconds()/60
    setup=sum(int(s['buoc_giay']) for s in ss if 1<=int(s['buoc_so'])<=10)/60
    total=sum(int(s['buoc_giay']) for s in ss)/60
    reg=next(int(s['buoc_giay'])/60 for s in ss if s['buoc_ten'].startswith('test registry'))
    pkt=next(int(s['buoc_giay'])/60 for s in ss if s['buoc_ten']=='packet-loop selftest')
    report['decomposition'][p]=dict(job=job,total=total,setup=setup,registry=reg,packet=pkt,remaining=total-reg-pkt,split_registry=reg+setup,split_packet=pkt+setup,after=total+2*setup)
u,w=report['decomposition']['ubuntu'],report['decomposition']['windows']
display_after_u=round(u['total'],2)+2*round(u['setup'],2)
display_after_w=round(w['total'],2)+2*round(w['setup'],2)
report['arithmetic']={'before':u['job']+2*w['job'],'after_raw':u['after']+2*w['after'],'longest_windows':w['split_registry'],'after_display_rounded_inputs':round(display_after_u+2*display_after_w,2),'display_after_by_platform':{'ubuntu':round(display_after_u,2),'windows':round(display_after_w,2)},'relative_increase_raw':(u['after']+2*w['after'])/(u['job']+2*w['job'])-1}
report['decomposition_source']='Archived round6 nen-a1-a5: run34045664423 is absent from supplied 30-run buoc_master.tsv; 11-run ratios above use supplied TSV only.'
report['original_ubuntu_success']=stats([int(j['job_giay'])/60 for (run,p),j in jobs.items() if p=='ubuntu' and j['job_concl']=='success'])
oldreport=json.loads((T/'ops/reviews/pr468-hoso-4-packet-review-9-codex/costs.json').read_text())
report['artifact9_comparison']={k:{'median_equal':abs(v['median']-oldreport['ratios'][k]['median'])<1e-12,'n_equal':v['n']==oldreport['ratios'][k]['n']} for k,v in report['ratios'].items()}
(O/'costs.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['original_rows','original_runs','event_counts','branch_counts','yaml_steps_counts','windows','archived_seconds_diffs','archived_jobs_diffs','arithmetic','original_ubuntu_success']},ensure_ascii=False,indent=2))
for k,v in report['ratios'].items():print(k,v['display'],v['rounding_display'],v['cells_match'],v['rounding_matches'])
