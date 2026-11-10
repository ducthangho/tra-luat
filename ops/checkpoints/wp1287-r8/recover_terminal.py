"""Append-only terminal recovery after reporting error. Never opens or controls a browser."""
import sys,json,hashlib,re,datetime
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from contract import cleanup,readiness,same_identity
from native_observer import identity,stamp
R=Path(r'C:\tl-win\wp1287-r8-fullflow-20261110');E=R/'evidence';NONCE='tl-pw-128708101110';LOCK=Path(r'C:\tl-win\KHOA.txt')
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
assert not (E/'terminal-recovery.json').exists(),'RECOVERY_ALREADY_RECORDED'
commands=load(E/'commands.json');by={x['label']:x for x in commands};own=load(E/'ownership.json');fixture=load(E/'fixture.json');rows=[]
for label in ['close','delete-data','verify-closed']:
 x=by.get(label,{});rows.append({'rc':None if x.get('timed_out') else x.get('rc'),'stdout':(E/(label+'.stdout')).read_bytes(),'stderr':(E/(label+'.stderr')).read_bytes()})
remaining=[];reused=[]
for old in own['identities']:
 current=identity(old['pid'])
 if current and same_identity(old,current) and current['alive']:remaining.append({'pid':old['pid'],'birth':old['birth']})
 elif current and not same_identity(old,current):reused.append(old['pid'])
clean=cleanup(NONCE,rows,remaining,bool(own['gaps']))
opened=load(E/'open.stdout');startup='acknowledged' if by['open']['rc']==0 and opened.get('session')==NONCE and type(opened.get('pid')) is int else 'failed'
tabs=load(E/'tabs.stdout')['result'];request=load(E/'requests.stdout')['result'];final=fixture['expected_final'];wanted=fixture['requested'];validtab=tabs.count('(current)')==1 and len([l for l in tabs.splitlines() if '(current)' in l and final in l])==1
statuses=[302,200] if len([l for l in request.splitlines() if wanted in l and 'GET' in l and '302' in l])==1 and len([l for l in request.splitlines() if final in l and 'GET' in l and '200' in l])==1 else []
body=(E/'source.html').read_bytes();body_valid=hashlib.sha256(body).hexdigest()==fixture['body_sha256'] and NONCE.encode() in body
ready='fixture_verified' if startup=='acknowledged' and validtab and statuses==[302,200] and body_valid else 'failed'
probes=[]
for p in E.glob('probe-[0-9]*.json'):
 if p.name.endswith('-identity.json'):continue
 v=load(p);assert isinstance(v,dict);probes.append(v)
schedule=load(E/'probe-schedule.json');overhead=load(E/'observer-overhead.json');samples=overhead['samples']
text=(E/'screenshot.stdout').read_text(encoding='utf-8',errors='replace')+'\n'+(E/'screenshot.stderr').read_text(encoding='utf-8',errors='replace')
walks={s:sum(p.get('state')==s for p in probes) for s in ['complete_walk','partial','unavailable','inconsistent','empty_snapshot']}
modules={name:sum(any(m['name'].lower()==name for m in p.get('modules',[])) for p in probes) for name in ['chrome.dll','chrome_elf.dll','uvh64.dll']}
result={'schema':'wp1287.native_recovery_summary.v1','at':stamp(),'candidate':'2a5803e17b7ca4910c7188bfcc2276190e2d0b4b','session':NONCE,'startup':startup,'open_cli_rc':by['open']['rc'],'readiness':ready,'fullflow':'failed','PNG':'failed','PDF':'not_run','screenshot_cli_rc':by['screenshot']['rc'],'screenshot_timeout_reported':bool(re.search(r'Timeout|timed out',text,re.I)),'screenshot_timeout_values_ms':re.findall(r'(\d+)ms',text),'cleanup':clean,'cleanup_rcs':[r['rc'] for r in rows],'owned_remaining_count':len(remaining),'ownership_gap_count':len(own['gaps']),'PID_reuse_after_run_count':len(reused),'observer_quality':'partial' if any(x.get('state') in ['deadline_exhausted','not_run_cleanup_priority'] for x in schedule) else 'complete_walk' if probes and all(p.get('state')=='complete_walk' for p in probes) else 'unavailable','module_walk_states':walks,'module_presence_counts':modules,'probe_count':len(probes),'post_open_scheduled_count':sum(x.get('post_open',False) for x in schedule),'post_open_worker_completed_count':sum(x.get('post_open',False) and x.get('worker_rc')==0 for x in schedule),'probe_worker_deadlines':sum(x.get('state')=='deadline_exhausted' for x in schedule),'min_free_RAM_bytes':min((x['free_bytes'] for x in samples if x.get('ok')),default=None),'min_free_commit_bytes':min((x['free_commit_bytes'] for x in samples if x.get('ok')),default=None),'max_observer_peak_working_set_bytes':max((x.get('observer_memory',{}).get('peak_working_set_bytes') or 0 for x in samples),default=None),'original_transport_shell_rc':1,'original_operator_reporting_failure':'AttributeError: list has no get; probe-schedule.json accidentally matched probe-*.json','planned_operator_rc_after_measurement':2,'recovery_rc':0 if clean=='verified' else 2,'allowance_used':1,'allowance_limit':1,'no_browser_relaunch':True,'U10':'OPEN','OP-F01':'formal_OPEN','sensitive_assurance':'HOLD','commands':[{'label':x['label'],'rc':x['rc'],'timed_out':x.get('timed_out',False),'start':x['start'],'end':x['end'],'stdout_sha256':x['stdout_sha256'],'stderr_sha256':x['stderr_sha256']} for x in commands]}
line=LOCK.read_text(encoding='utf-8-sig');result['lock_owned_before_recovery']=line.split('\t')[0]==NONCE
if clean=='verified' and result['lock_owned_before_recovery']:
 assert LOCK.read_text(encoding='utf-8-sig')==line;LOCK.write_bytes(b'')
result['lock_released']=not LOCK.read_bytes();result['paused_handoff']=not result['lock_released'];result['source_body_sha256']=sha(E/'source.html');result['evidence_sha256']={p.name:sha(p) for p in E.iterdir() if p.is_file() and p.name!='terminal-recovery.json'}
save(E/'terminal-recovery.json',result)
with Path(r'C:\tl-win\do-luong.csv').open('a',encoding='utf-8',newline='') as f:f.write(f"{datetime.datetime.now(datetime.timezone.utc).isoformat()},{NONCE},wp1287,{result['candidate']},r8-terminal-recovery,0,0,{result['recovery_rc']},0,operator,{clean},no,may=DESKTOP-T9R33P2;original_shell_rc1;screenshot_failed;readiness={ready};no_browser_relaunch\n")
# Explicitly allowlisted summary only; no raw stdout, paths, profiles or command lines exported.
print(json.dumps(result),flush=True)
sys.exit(result['recovery_rc'])
