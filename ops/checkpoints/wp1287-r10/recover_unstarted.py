"""Append recovery for a blocked script transport: no browser was started."""
import sys,json,hashlib,datetime
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from native_observer import identity,census,stamp
from contract import same_identity
B=Path(r'C:\tl-win\wp1287-r10-ps-positive-20261110');R=B/'ps51';E=R/'evidence';L=Path(r'C:\tl-win\KHOA.txt');nonce='tl-pw-128710105101'
t=json.loads((E/'terminal.json').read_text());o=json.loads((E/'ownership.json').read_text())
assert t['open_cli_rc'] is None and not (E/'commands.tsv').exists() and not (E/'shell-version-open.json').exists()
assert not o['gaps']
live=[]
for old in o['identities']:
 x=identity(old['pid'])
 if x and same_identity(x,old) and x['alive']:live.append(x['pid'])
assert not live
chrome=r'C:\tl-win\wp1287-H1-native-recovery2\browser-cache\chromium-1252\chrome-win64\chrome.exe'.lower()
assert not [x for x in census() if x['exe'].lower()=='chrome.exe' and (identity(x['pid']) or {}).get('image')==chrome]
assert L.read_text(encoding='utf-8-sig').split('\t')[0]==nonce
L.write_bytes(b'')
v={'at':stamp(),'original_operator_child_rc':1,'original_transport_shell_rc':1,'planned_terminal_rc_not_actual':2,'original_cleanup':'failed','recovery':'preexecution_failure_no_CLI_or_browser_started','browser_opens_actual':0,'owned_remaining':0,'ownership_gaps':0,'lock_readback_empty':not L.read_bytes(),'ps7':'not_run','recovery_rc':0,'original_terminal_sha256':hashlib.sha256((E/'terminal.json').read_bytes()).hexdigest(),'no_policy_or_process_changes':True}
p=E/'unstarted-recovery.json';assert not p.exists();p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');print(json.dumps(v))
with Path(r'C:\tl-win\do-luong.csv').open('a',encoding='utf-8',newline='') as f:f.write(f"{datetime.datetime.now(datetime.timezone.utc).isoformat()},{nonce},wp1287,{t['candidate']},r10-unstarted-recovery,0,0,0,0,operator,no_CLI_started,no,original_child1;no_browser_opens;lock_released\n")
