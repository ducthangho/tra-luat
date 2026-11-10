"""Allowlisted native PowerShell positive-proof projection; raw evidence stays native."""
import json,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from contract import cleanup,same_identity
from native_observer import identity,stamp
B=Path(r'C:\tl-win\wp1287-r11-ps-inline-20261110');out={'schema':'wp1287.ps_inline_summary.v1','at':stamp(),'shells':{},'outer_transport_shell_rc':int(sys.argv[1]),'candidate':'2a5803e17b7ca4910c7188bfcc2276190e2d0b4b','no_policy_changes':True}
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for kind in ['ps51','ps7']:
 E=B/kind/'evidence'
 if not (E/'terminal.json').exists():out['shells'][kind]={'status':'not_run'};continue
 t=load(E/'terminal.json');o=load(E/'ownership.json');d=load(E/'documented-cleanup-receipt.json') if (E/'documented-cleanup-receipt.json').exists() else None
 live=[]
 for old in o['identities']:
  current=identity(old['pid'])
  if current and same_identity(old,current) and current['alive']:live.append(old['pid'])
 rows=[]
 for label,rc in [('08-close',0),('09-delete-data',0),('10-verify',1)]:
  step=next((x for x in (d or {}).get('steps',[]) if x['documented_step']==label),None)
  rows.append({'rc':step['rc'] if step else None,'stdout':(E/(label+'.json')).read_bytes() if (E/(label+'.json')).exists() else b'','stderr':(E/(label+'.err')).read_bytes() if (E/(label+'.err')).exists() else b''})
 summary={k:t.get(k) for k in ['success','operator_child_rc','observer_quality','startup','open_cli_rc','readiness','fullflow','cleanup','allowance_used','limit','lock_released','paused_handoff','action_timeout_ms','launch_timeout_ms','cleanup_timeout_seconds']}
 summary.update(actual_shell_receipt=load(E/'documented-shell-receipt.json') if (E/'documented-shell-receipt.json').exists() else None,captures=load(E/'captures.json') if (E/'captures.json').exists() else None,documented_cleanup=d,independent_cleanup=cleanup('tl-pw-128711105101' if kind=='ps51' else 'tl-pw-128711100701',rows,live,bool(o['gaps'])),owned_remaining_count=len(live),ownership_gap_count=len(o['gaps']),native_terminal_sha256=sha(E/'terminal.json'),commands=[{'label':x['label'],'powershell_rc':x.get('powershell_rc',x['rc']),'actual_CLI_rc':x.get('documented_cli_rc'),'elapsed_ms':(x['end']['mono_ns']-x['start']['mono_ns'])/1e6,'stdout_sha256':x['stdout_sha256'],'stderr_sha256':x['stderr_sha256']} for x in load(E/'commands.json')],evidence_sha256={p.name:sha(p) for p in E.iterdir() if p.is_file()})
 if t.get('error'):summary['error_category']=t['error'].split(':',1)[0]
 out['shells'][kind]=summary
out['lock_readback_empty']=not Path(r'C:\tl-win\KHOA.txt').read_bytes();out['U10']='OPEN_pending_formal_acceptance';out['OP-F01']='formal_OPEN';out['sensitive_assurance']='HOLD'
p=B/'allowlisted-summary.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({'native_summary_sha256':sha(p),'summary':out}),flush=True)
