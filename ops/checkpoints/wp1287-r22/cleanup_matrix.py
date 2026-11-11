"""Run exact documented helpers/Cleanup against controlled CLI-shaped processes."""
import pathlib,re,sys,json,os,subprocess,hashlib,base64
src=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);out.mkdir(exist_ok=False)
text=src.read_text(encoding='utf-8-sig');blocks={x:re.findall('```'+x+r'\n(.*?)\n```',text,re.S) for x in ['bash','powershell']}
nonce='tl-pw-abcdef123456';fixture=out/'fixture.py'
fixture.write_text('''import os,sys,json,pathlib
c=os.environ['MATRIX_CASE'];a=sys.argv[1:];session=next(x.split('=',1)[1] for x in a if x.startswith('--session='));verb=next(x for x in a if x in ['close','delete-data','tab-list']);root=pathlib.Path(os.environ['TL_PW_RUN']);log=root/'fixture-invocations.txt';log.open('ab').write((verb+'\\n').encode())
v={'session':session,'status':'closed'} if verb=='close' else {'session':session,'deleted':c!='positive-false'} if verb=='delete-data' else {'isError':True,'error':"The browser '"+session+"' is not open, please run open first"};rc=1 if verb=='tab-list' else 0
if c=='close-rc' and verb=='close':rc=17
if c=='delete-rc' and verb=='delete-data':rc=18
if c=='verify-rc' and verb=='tab-list':rc=19
if c=='still-open' and verb=='tab-list':rc=0
if c=='unrelated-error' and verb=='tab-list':v={'isError':True,'error':'unrelated transport failure'}
label={'close':'close','delete-data':'delete','tab-list':'verify'}[verb]
if c==label+'-nonce':
 if verb=='tab-list':v['error']="The browser 'tl-pw-fedcba654321' is not open, please run open first"
 else:v['session']='tl-pw-fedcba654321'
if c=='delete-nonboolean' and verb=='delete-data':v['deleted']='false'
data=(json.dumps(v,indent=2)+'\\n').encode()
if c==label+'-json':data=b'not json'
if c==label+'-empty':data=b''
if c==label+'-format':data=(json.dumps(v)+'\\n').encode()
if c==label+'-stderr':sys.stderr.buffer.write(b'controlled stderr')
sys.stdout.buffer.write(data);sys.exit(rc)
''',encoding='utf-8')
cases=['positive-true','positive-false','close-rc','delete-rc','verify-rc','still-open','unrelated-error','delete-nonboolean','missing-executable','missing-cli','invalid-nonce','stale-json','stale-stderr']+[v+'-'+s for v in ['close','delete','verify'] for s in ['nonce','json','empty','format','stderr']]
rows=[];engines=([('ps51',r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'),('ps7',r'C:\Program Files\PowerShell\7\pwsh.exe')] if os.name=='nt' else [('bash','bash')])
for tag,exe in engines:
 b=blocks['bash' if tag=='bash' else 'powershell']
 helper=b[2][b[2].index('chay_ghi()' if tag=='bash' else 'function Invoke-PwGhi'):b[2].index('# Chạy khối')]
 definitions='' if tag=='bash' else b[0][b[0].index('function Need'):b[0].index('function Test-PwEnv')]
 for case in cases+(['missing-process','malformed-process'] if tag!='bash' else [])+['mutant-close-rc','mutant-delete-rc','mutant-any-negative']:
  label=tag+'-'+case;root=out/label;run=root/'run';run.mkdir(parents=True);(root/'work').mkdir();env={k:v for k,v in os.environ.items() if not k.startswith(('TL_','GIT_'))};env.update(TL_PW_ROOT=str(root),TL_PW_RUN=str(run),TL_PW_NODE=sys.executable,TL_PW_CLI=str(fixture),TL_PW_SESSION=nonce,MATRIX_CASE=case,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
  if case=='missing-executable':env['TL_PW_NODE']=str(root/'missing.exe')
  if case=='missing-cli':env['TL_PW_CLI']=str(root/'missing.py')
  if case=='invalid-nonce':env['TL_PW_SESSION']='not-owned'
  stale=None
  if case in ['stale-json','stale-stderr']:stale=run/('08-close.json' if case=='stale-json' else '08-close.err');stale.write_bytes(b'STALE_EVIDENCE')
  body=b[4];h=helper;stub=''
  mutant=case.startswith('mutant-')
  if mutant:
   env['MATRIX_CASE']={'mutant-close-rc':'close-rc','mutant-delete-rc':'delete-rc','mutant-any-negative':'verify-rc'}[case]
   if tag=='bash':
    if case=='mutant-any-negative':body=body.replace('[ "$rc" -eq 1 ]','[ "$rc" -ne 0 ]')
    else:
     step='08-close close' if case=='mutant-close-rc' else '09-delete-data delete-data';body=re.sub(re.escape('chay_ghi '+step)+r' \|\| \{[^\n]+\}', 'chay_ghi '+step+' || true',body,count=1)
   else:
    old='Need ($rc -eq $expectedRc)';replacement='Need (($PhaiLoi -and $rc -ne 0) -or (-not $PhaiLoi -and $rc -eq 0))' if case=='mutant-any-negative' else 'Need (($PhaiLoi -and $rc -eq 1) -or (-not $PhaiLoi -and $Ten -eq '+("'08-close'" if case=='mutant-close-rc' else "'09-delete-data'")+') -or $rc -eq $expectedRc)';assert old in h;h=h.replace(old,replacement)
  if tag!='bash':
   modules=r'C:\Windows\System32\WindowsPowerShell\v1.0\Modules' if tag=='ps51' else r'C:\Program Files\PowerShell\7\Modules';env['PSModulePath']=modules+r';C:\Program Files\WindowsPowerShell\Modules'
   if case=='missing-process':stub='function Start-Process { $null }\n'
   if case=='malformed-process':stub="function Start-Process { 'NOT_A_PROCESS' }\n"
   code="Import-Module Microsoft.PowerShell.Management,Microsoft.PowerShell.Utility -ErrorAction Stop\n"+definitions+'\n'+stub+h+"\n'SOURCE_TEST_ENTERED'\n"+body+'\n';path=out/(label+'.ps1');path.write_bytes(code.encode('utf-8-sig'));encoded=base64.b64encode(code.encode('utf-16le')).decode();assert len(encoded)<30000;cmd=[exe,'-NoProfile','-NonInteractive','-EncodedCommand',encoded]
  else:code=h+'\necho SOURCE_TEST_ENTERED\n'+body+'\n';path=out/(label+'.bash');path.write_text(code,encoding='utf-8');cmd=[exe,'--noprofile','--norc',str(path)]
  cp=subprocess.run(cmd,env=env,capture_output=True,timeout=40);(out/(label+'.stdout')).write_bytes(cp.stdout);(out/(label+'.stderr')).write_bytes(cp.stderr);marker=b'CLEANUP OK' in cp.stdout;entered=b'SOURCE_TEST_ENTERED' in cp.stdout;positive=case in ['positive-true','positive-false'];passed=entered and ((cp.returncode==0 and marker) if positive or mutant else (cp.returncode!=0 and not marker))
  if stale:passed=passed and stale.read_bytes()==b'STALE_EVIDENCE' and not (run/'fixture-invocations.txt').exists()
  row={'id':label,'case':case,'rc':cp.returncode,'source_entered':entered,'cleanup_ok':marker,'expected':'unsafe mutant accepted (negative criterion detects regression)' if mutant else 'success' if positive else 'fail closed','passed':passed,'mutant_control':mutant};rows.append(row);print(json.dumps(row),flush=True)
summary={'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'source_head':'0bf2a8a7a094d9df0a84eec807c5c5e5d89d87c2','platform':sys.platform,'total':len(rows),'passed':sum(x['passed'] for x in rows),'failed':[x['id'] for x in rows if not x['passed']],'rows':rows,'scope':'actual source helper/Cleanup with process fixture, not real browser acceptance'};(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='rows'}));sys.exit(bool(summary['failed']))
