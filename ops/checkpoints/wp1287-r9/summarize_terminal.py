"""Read-only post-run proof checks; export only allowlisted summary/hashes."""
import sys,json,hashlib,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from contract import cleanup,same_identity,load_module_probes
from native_observer import identity,stamp
R=Path(r'C:\tl-win\wp1287-r9-timeout-20261110');E=R/'evidence';NONCE='tl-pw-128709101110';LOCK=Path(r'C:\tl-win\KHOA.txt')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
terminal=load(E/'terminal.json');commands=load(E/'commands.json');own=load(E/'ownership.json');by={x['label']:x for x in commands};rows=[]
for label in ['close','delete-data','verify-closed']:
 x=by.get(label,{});rows.append({'rc':None if x.get('timed_out') else x.get('rc'),'stdout':(E/(label+'.stdout')).read_bytes(),'stderr':(E/(label+'.stderr')).read_bytes()})
remaining=[]
for old in own['identities']:
 x=identity(old['pid'])
 if x and same_identity(old,x) and x['alive']:remaining.append(old['pid'])
verified=cleanup(NONCE,rows,remaining,bool(own['gaps']));cfg=load(E/'browser.json');assert cfg['timeouts']['action']==10000 and cfg['browser']['launchOptions']['timeout']==30000
probes=load_module_probes(E);schedule=load(E/'probe-schedule.json');samples=load(E/'observer-overhead.json')['samples']
raw=''
for ext in ['stdout','stderr']:
 p=E/('screenshot.'+ext)
 if p.exists():raw+=p.read_text(encoding='utf-8',errors='replace')+'\n'
summary={'schema':'wp1287.r9.allowlisted_summary.v1','at':stamp(),'terminal':terminal,'actual_transport_shell_rc':int(sys.argv[1]),'original_measurement_preserved':True,'timeout_config':{'action_ms':10000,'launch_ms':30000,'cleanup_seconds':20},'screenshot_error_timeout_reported':bool(re.search('Timeout|timed out',raw,re.I)),'screenshot_error_timeout_values_ms':re.findall(r'(\d+)ms',raw),'screenshot_call_log_categories':[s for s in ['taking page screenshot','waiting for fonts','fonts loaded','waiting for animations','scrolling into view'] if s in raw],'cleanup_independent_readback':verified,'owned_remaining_count':len(remaining),'ownership_gap_count':len(own['gaps']),'lock_readback_empty':not LOCK.read_bytes(),'probe_count':len(probes),'module_walk_states':{s:sum(p.get('state')==s for p in probes) for s in ['complete_walk','partial','unavailable','inconsistent','empty_snapshot']},'module_presence_counts':{s:sum(any(m['name'].lower()==s for m in p.get('modules',[])) for p in probes) for s in ['chrome.dll','chrome_elf.dll','uvh64.dll']},'post_open_scheduled_count':sum(x.get('post_open',False) for x in schedule),'post_open_completed_count':sum(x.get('post_open',False) and x.get('worker_rc')==0 for x in schedule),'probe_worker_deadlines':sum(x.get('state')=='deadline_exhausted' for x in schedule),'min_free_RAM_bytes':min((x['free_bytes'] for x in samples if x.get('ok')),default=None),'max_observer_peak_working_set_bytes':max((x.get('observer_memory',{}).get('peak_working_set_bytes') or 0 for x in samples),default=None),'commands':[{'label':x['label'],'rc':x['rc'],'timed_out':x.get('timed_out',False),'elapsed_ms':(x['end']['mono_ns']-x['start']['mono_ns'])/1000000,'stdout_sha256':x['stdout_sha256'],'stderr_sha256':x['stderr_sha256']} for x in commands],'evidence_sha256':{p.name:sha(p) for p in E.iterdir() if p.is_file()},'stage_terminal_sha256':sha(R/'stage-terminal.json'),'stage_commands_sha256':sha(R/'stage-commands.json'),'captures':load(E/'captures.json') if (E/'captures.json').exists() else None,'U10':'OPEN','OP-F01':'formal_OPEN','sensitive_assurance':'HOLD'}
p=R/'allowlisted-summary.json';assert not p.exists();p.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'native_summary_sha256':sha(p),'summary':summary}),flush=True)
