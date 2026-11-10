"""Named recovery after invalid argv prevented a browser open; never launch a browser."""
import sys,json,subprocess,time,hashlib,datetime
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from native_observer import identity,census,stamp
from contract import same_identity
B=Path(r'C:\tl-win\wp1287-r11-ps-inline-20261110');E=B/'ps51/evidence';L=Path(r'C:\tl-win\KHOA.txt');nonce='tl-pw-128711105101';node=r'C:\Program Files\nodejs\node.exe';cli=r'C:\tl-win\wp1287-r9-timeout-20261110\installation\node_modules\@playwright\cli\playwright-cli.js'
t=json.loads((E/'terminal.json').read_text());o=json.loads((E/'ownership.json').read_text());err=json.loads((E/'open.json').read_text());assert err['isError'] and 'Unknown command' in err['error'] and 'open about:blank --config' in err['error']
assert json.loads((E/'08-close.json').read_text())=={'session':nonce,'status':'not-open'}
rows=[]
for label,args,expected in [('recovery-delete',['delete-data'],0),('recovery-verify',['tab-list'],1)]:
 out=E/(label+'.stdout');se=E/(label+'.stderr');assert not out.exists();r=subprocess.run([node,cli,'--session='+nonce,*args,'--json'],cwd=B,capture_output=True,timeout=20);out.write_bytes(r.stdout);se.write_bytes(r.stderr);v=json.loads(r.stdout);assert r.returncode==expected and not r.stderr
 if expected==0:assert v.get('session')==nonce and type(v.get('deleted')) is bool
 else:assert v=={'isError':True,'error':f"The browser '{nonce}' is not open, please run open first"}
 rows.append({'action':label,'rc':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_empty':True})
remaining=[]
for old in o['identities']:
 x=identity(old['pid'])
 if x and same_identity(x,old) and x['alive']:remaining.append(old['pid'])
assert not remaining and not o['gaps']
chrome=r'C:\tl-win\wp1287-H1-native-recovery2\browser-cache\chromium-1252\chrome-win64\chrome.exe'.lower();assert not [x for x in census() if x['exe'].lower()=='chrome.exe' and (identity(x['pid']) or {}).get('image')==chrome]
assert L.read_text(encoding='utf-8-sig').split('\t')[0]==nonce;L.write_bytes(b'')
v={'at':stamp(),'actual_child_rc':2,'actual_shell_rc':2,'original_cleanup':'failed','original_input_error':'PS5 JSON array flattened into one command argument','browser_opens_actual':0,'owned_remaining':0,'ownership_gaps':0,'named_recovery':rows,'lock_readback_empty':not L.read_bytes(),'ps7':'not_run','recovery_rc':0,'no_policy_or_browser_changes':True};p=E/'input-failure-recovery.json';assert not p.exists();p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');print(json.dumps(v))
with Path(r'C:\tl-win\do-luong.csv').open('a',encoding='utf-8',newline='') as f:f.write(f"{datetime.datetime.now(datetime.timezone.utc).isoformat()},{nonce},wp1287,{t['candidate']},r11-input-recovery,0,0,0,0,operator,no_browser_started,no,original_child2;named_delete_verify;lock_released\n")
