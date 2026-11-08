import base64,csv,ctypes,datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,threading,time,traceback
I=pathlib.Path(r'C:\tl-win\wp1279-r4-g4-inputs');M=json.loads((I/'g4-candidate-manifest.json').read_text());W=pathlib.Path(r'C:\tl-win\wp1279-r4-g4')/('final-'+M['candidate'][:12]);LOCK=pathlib.Path(r'C:\tl-win\KHOA.txt');SID='wp1279-g4-'+M['candidate'][:12]
GIT=r'C:\tl-win\wp1271-tools\mingit-2.56.0.4\cmd\git.exe';PS51=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe';PS7=r'C:\Program Files\PowerShell\7\pwsh.exe'
REL='.agents/skills/proxima-control/scripts/ProximaControl.psm1';TEST='.agents/skills/proxima-control/tests/ProximaControl.Tests.ps1';stop=threading.Event();taken=False;start=None;thread=None;results=[];phases={}
def now():return datetime.datetime.now(datetime.timezone.utc)
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
def say(v):print(json.dumps(v,ensure_ascii=True),flush=True)
def own():return LOCK.exists() and LOCK.read_text(encoding='utf-8-sig').split('\t')[0]==SID
def beat():
 if not own():raise RuntimeError('machine-lock ownership lost')
 n=now()
 if n>start+datetime.timedelta(hours=2):raise RuntimeError('machine-lock deadline exceeded')
 LOCK.write_text('\t'.join([SID,start.isoformat(),(start+datetime.timedelta(hours=2)).isoformat(),'wp1279 focused native PS51/7',n.isoformat()])+'\n',encoding='utf-8')
 with (W/'heartbeat-readbacks.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'at':n.isoformat(),'readback':LOCK.read_text(encoding='utf-8-sig')})+'\n')
def heart():
 while not stop.wait(60):
  try:beat()
  except Exception as e:say({'heartbeat_error':str(e)});stop.set();return

def run(args,label,env=None,cwd=None,timeout=1200,check=True):
 if stop.is_set() or (start and now()>start+datetime.timedelta(hours=2)):raise RuntimeError('ownership/deadline lost')
 say({'start':label});t=time.monotonic();p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,cwd=cwd)
 try:out,_=p.communicate(timeout=timeout)
 except subprocess.TimeoutExpired:
  subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);out,_=p.communicate();(W/'logs'/f'{label}.log').write_bytes(out);raise RuntimeError('owned test timeout '+label)
 log=W/'logs'/f'{label}.log';log.write_bytes(out);row={'label':label,'command':args,'rc':p.returncode,'seconds':round(time.monotonic()-t,3),'log_sha256':sha(log)};results.append(row)
 with (W/'command-receipts.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row)+'\n')
 say({'finished':label,'rc':p.returncode,'seconds':row['seconds']})
 if check and p.returncode:raise RuntimeError(label+' failed rc='+str(p.returncode))
 return p.returncode,out.decode('utf-8',errors='replace').strip()
def git(repo,*args,label):return run([GIT,'-C',str(repo),*args],label)[1]
def ledger(label,rep,rc,seconds):
 p=pathlib.Path(r'C:\tl-win\do-luong.csv');exists=p.exists() and p.stat().st_size>0
 with p.open('a',encoding='utf-8',newline='') as f:
  w=csv.writer(f)
  if not exists:w.writerow(['thoi_diem','session','packet','sha','bo_test','dat','tong','ca_do','thoi_luong_s','phat_hien_boi','loi_that','da_va','ghi_chu'])
  w.writerow([now().isoformat(),SID,'wp1279',M['baseline'] if label.startswith('baseline') else (M['old_h3'] if label.startswith('old-h3') else M['candidate']),label,rep.get('passed',0),rep.get('total',0),'|'.join(rep.get('failed_ids',[])),seconds,'focused-local','not_classified','no',f'may=DESKTOP-T9R33P2;device=a5f7076e-a491-4f84-829b-8d1fbcc1c767;ngat=khong;rc={rc}'])
def files(repo):return {str(p.relative_to(repo)).replace(chr(92),'/'):sha(p) for p in repo.rglob('*') if p.is_file() and '.git' not in p.relative_to(repo).parts}
def validate_cx(rep,exe,evidence):
 xs=rep['counterexample_evidence'];assert len(xs)==12 and {x['id'] for x in xs}=={'CX%02d'%i for i in range(12)}
 original={p.name:p.read_text(encoding='utf-8-sig') for p in (W/'candidate'/REL).parent.iterdir() if p.is_file()}
 for x in xs:
  cp=pathlib.Path(x['report_path']);op=pathlib.Path(x['output_path']);assert cp.resolve().is_relative_to(evidence.resolve()) and op.resolve().is_relative_to(evidence.resolve())
  assert sha(cp)==x['report_sha256'] and sha(op)==x['output_sha256'];child=json.loads(cp.read_text(encoding='utf-8-sig'));record=pathlib.Path(str(cp).removesuffix('.report.json')+'.record.json');assert json.loads(record.read_text(encoding='utf-8-sig'))==x
  cmd=x['command'];assert cmd[0].lower()==exe.lower() and cmd[cmd.index('-ReportPath')+1]==str(cp) and cmd[cmd.index('-TestCulture')+1]=='tr-TR'
  assert child['test_culture']=='tr-TR' and child['test_ui_culture']=='tr-TR' and child['harness_sha256']==M['file_sha256'][TEST] and child['api_state']=='present' and not child['setup_error'] and not child['setup_error_ids'] and child['cleanup']['status']=='ok'
  src=cp.parent/x['id']
  for fn,key in [('ProximaControl.psm1','module_sha256'),('Run-Px.ps1','wrapper_sha256'),('ProximaConfig.psm1','config_module_sha256')]:
   assert sha(src/fn)==x[key];actual=(src/fn).read_text(encoding='utf-8-sig');want=original[fn]
   if fn==x['mutated_file']:assert want.count(x['anchor'])==1;want=want.replace(x['anchor'],x['replacement'],1)
   assert actual==want,'source mutation mismatch '+x['id']
  for c in child['children']:
   if c['kind'].startswith('counterexample'):continue
   assert c['culture']=='tr-TR' and c['ui_culture']=='tr-TR' and c['ps_version'] and c['ps_edition']
  if x['id']=='CX00':assert x['rc']==0 and child['passed']==child['total']==26 and not x['credited']
  else:
   assert x['rc']==1 and x['credited'] is True and x['verdict'].startswith('KILLED')
   for w in x['required']:
    cid,tok=w.split(':',1);assert any(c['id']==cid and c['outcome']=='failed' and tok in str(c['reason']) for c in child['cases'])
 return {'source_reconstructed':12,'positive_control':1,'named_behavioural_kills':11}
sys.path.insert(0,str(I))
from g4_native_evidence import verify_nested,MissingNestedArtifact
def main():
 global start,taken,thread
 assert os.name=='nt';before=LOCK.read_text(encoding='utf-8-sig') if LOCK.exists() else '';assert not before.strip(),'foreign machine lock';assert not W.exists(),'do not overwrite evidence'
 for d in ['logs','reports','scratch','harness','evidence']:(W/d).mkdir(parents=True,exist_ok=False)
 start=now();LOCK.write_text('\t'.join([SID,start.isoformat(),(start+datetime.timedelta(hours=2)).isoformat(),'wp1279 focused native',start.isoformat()])+'\n',encoding='utf-8');taken=True;assert own();save(W/'lock-acquisition.json',{'session':SID,'before':before,'readback':LOCK.read_text(encoding='utf-8-sig'),'at':start.isoformat()});beat();thread=threading.Thread(target=heart,daemon=True);thread.start()
 shutil.copyfile(I/'device-online.json',W/'device-online.json');online=json.loads((W/'device-online.json').read_text());assert online['online'] is True and online['device_id']=='a5f7076e-a491-4f84-829b-8d1fbcc1c767'
 env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1');env['PATH']=str(pathlib.Path(GIT).parent)+';'+str(pathlib.Path(PS7).parent)+';'+env.get('PATH','')
 for k in list(env):
  if k.startswith('TL_') or k in ['GH_TOKEN','GITHUB_TOKEN','GITHUB_PAT','ANTHROPIC_API_KEY','CLAUDE_CODE_OAUTH_TOKEN','CODEX_AUTH_JSON','OPENAI_API_KEY','PROXIMA_API_KEY']:env.pop(k,None)
 pre="$ErrorActionPreference='Stop'; $env:PSModulePath=(Join-Path $PSHOME 'Modules')+';C:\\Program Files\\WindowsPowerShell\\Modules'; "
 probe=pre+"[pscustomobject]@{ host=$env:COMPUTERNAME; service=@(Get-CimInstance Win32_Service -Filter \"Name='ProximaGateway'\").Count; process=@(Get-CimInstance Win32_Process -Filter \"Name='Proxima.exe'\").Count; python=@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Select-Object ProcessId,ParentProcessId,CreationDate); policy=@(Get-ExecutionPolicy -List) } | ConvertTo-Json -Depth 4 -Compress"
 _,out=run([PS51,'-NoProfile','-NonInteractive','-Command',probe],'host-preflight',env=env);host=json.loads(out);host['win32_GetACP']=ctypes.windll.kernel32.GetACP();save(W/'host-preflight.json',host);assert host['win32_GetACP']==1252,'need actual ANSI1252';assert host['service']==host['process']==0;assert any(p['ProcessId']==os.getpid() for p in host['python']);assert all(str(p['ExecutionPolicy']) in ['5','Undefined'] for p in host['policy'] if str(p['Scope']) in ['4','3','MachinePolicy','UserPolicy'])
 bundle=W/'candidate.bundle';bundle.write_bytes(base64.b64decode((I/'g4-candidate.bundle.b64').read_text()));assert sha(bundle)==M['bundle_sha256']
 base=W/'baseline';cand=W/'candidate';run([GIT,'-c','core.autocrlf=false','clone','--no-checkout','--single-branch','--branch','master','https://github.com/ducthangho/tra-luat.git',str(base)],'clone-baseline');git(base,'fetch','origin',M['baseline'],label='fetch-base-exact');run([GIT,'clone','--no-hardlinks','--no-checkout',str(base),str(cand)],'clone-candidate')
 for name,repo in [('baseline',base),('candidate',cand)]:
  for k,v in [('core.autocrlf','false'),('core.eol','lf'),('core.abbrev','7')]:git(repo,'config',k,v,label=name+'-'+k)
  git(repo,'sparse-checkout','set','--no-cone','/.gitattributes','/.agents/skills/proxima-control/',label=name+'-sparse')
 git(base,'checkout','--detach',M['baseline'],label='checkout-base');git(cand,'bundle','verify',str(bundle),label='bundle-verify');git(cand,'fetch',str(bundle),'HEAD:refs/heads/measured-candidate',label='import-candidate');git(cand,'checkout','--detach',M['candidate'],label='checkout-candidate')
 identities={}
 for name,repo in [('baseline',base),('candidate',cand)]:
  ident={'sha':git(repo,'rev-parse','HEAD',label=name+'-sha'),'tree':git(repo,'rev-parse','HEAD^{tree}',label=name+'-tree'),'parents':git(repo,'show','-s','--format=%P','HEAD',label=name+'-parents').split()};identities[name]=ident;assert ident['sha']==M[name] and ident['tree']==M['baseline_tree' if name=='baseline' else 'tree'] and ident['parents']==M['baseline_parents' if name=='baseline' else 'parents']
 for f,h in M['file_sha256'].items():assert sha(cand/f)==h
 old=W/'old-h3';run([GIT,'clone','--no-hardlinks','--no-checkout',str(cand),str(old)],'clone-old-h3')
 for k,v in [('core.autocrlf','false'),('core.eol','lf'),('core.abbrev','7')]:git(old,'config',k,v,label='old-'+k)
 git(old,'sparse-checkout','set','--no-cone','/.gitattributes','/.agents/skills/proxima-control/',label='old-sparse');git(old,'checkout','--detach',M['old_h3'],label='checkout-old-h3')
 identities['old_h3']={'sha':git(old,'rev-parse','HEAD',label='old-sha'),'tree':git(old,'rev-parse','HEAD^{tree}',label='old-tree'),'parents':git(old,'show','-s','--format=%P','HEAD',label='old-parents').split()};assert identities['old_h3']=={'sha':M['old_h3'],'tree':M['old_h3_tree'],'parents':M['old_h3_parents']}
 for f,h in M['old_h3_file_sha256'].items():assert sha(old/f)==h
 save(W/'identity.json',{'manifest':M,'actual':identities,'host':host['host'],'account':os.environ.get('USERNAME'),'lock_session':SID});harness=W/'harness'/'ProximaControl.Tests.ps1';shutil.copyfile(cand/TEST,harness);before_files={'baseline':files(base),'candidate':files(cand),'old_h3':files(old)};save(W/'before-file-hashes.json',before_files)
 parse=pre+"$bad=0; foreach($f in @("+','.join("'"+str(cand/p).replace("'","''")+"'" for p in [REL,REL.replace('ProximaControl.psm1','Run-Px.ps1'),TEST])+")){ $t=$null;$e=$null;[void][Management.Automation.Language.Parser]::ParseFile($f,[ref]$t,[ref]$e); foreach($x in $e){Write-Output ($f+':'+$x.Extent.StartLineNumber+':'+$x.Message);$bad++}}; Write-Output ('PARSE_ERRORS='+$bad);if($bad){exit 1}"
 for psid,exe in [('ps51',PS51),('ps7',PS7)]:run([exe,'-NoProfile','-NonInteractive','-Command',parse],'parse-'+psid,env=env)
 def measure(name,repo,exe,psid,cx=False):
  label=name+'-'+psid+('-counterexamples' if cx else '');scratch=W/'scratch'/label;scratch.mkdir();ev=W/'evidence'/label;ev.mkdir();rp=W/'reports'/(label+'.json');pe=env.copy();pe['PSModulePath']=str(pathlib.Path(exe).parent/'Modules')+r';C:\Program Files\WindowsPowerShell\Modules';pe['TEMP']=str(scratch);pe['TMP']=str(scratch)
  args=[exe,'-NoLogo','-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(harness),'-ModulePath',str(repo/REL),'-ScratchRoot',str(scratch),'-ReportPath',str(rp),'-EvidenceRoot',str(ev),'-TestCulture','tr-TR' if cx else 'en-US']
  if cx:args+=['-Counterexamples']
  t=time.monotonic();rc,_=run(args,label,env=pe,check=False);rep=json.loads(rp.read_text(encoding='utf-8-sig')) if rp.exists() else {'setup_error':'report absent','total':0,'passed':0,'cases':[]};ledger(label,rep,rc,round(time.monotonic()-t,3));phases[label]={'rc':rc,'report':rep,'report_sha256':sha(rp) if rp.exists() else None};save(W/'phase-progress.json',{'candidate':M['candidate'],'phases':phases,'commands':results,'at':now().isoformat()})
  if name=='old-h3':
   assert rc==1 and not rep['setup_error'] and not rep['setup_error_ids'] and rep['harness_sha256']==sha(harness) and rep['module_sha256']==M['old_h3_file_sha256'][REL] and rep['cleanup']['status']=='ok'
   assert rep['total']==26 and {c['id'] for c in rep['cases']}==set(M['mandatory_ids']) and rep['test_culture']==rep['test_ui_culture']=='en-US'
   failures=[c for c in rep['cases'] if c['outcome']!='passed'];target=next(c for c in failures if c['id']=='X5-09');reason=str(target['reason']);log=(W/'logs'/(label+'.log')).read_text(encoding='utf-8',errors='replace')
   for token in M['f03_failure_tokens']:assert token in reason and token in log,'missing actual named F03 behavior '+token
   import re
   assert re.search(r'LISTENER_OWNERSHIP_BYPASS\[wire px models\] requests=[1-9][0-9]* auth=[1-9][0-9]*',reason),'no actual wrong-listener wire/auth observation'
   observations=verify_nested(rep,lambda p:pathlib.Path(p),True)
   phases[label]['F03_behavior']={'reproduced':True,'actual_named_mock_and_wire_auth_observations':reason,'other_diagnostics_not_credited':[c for c in failures if c['id']!='X5-09'],'listener_probe':rep.get('listener_probe'),'nested':observations};phases[label]['operator_validated']=True;save(W/'phase-progress.json',{'candidate':M['candidate'],'phases':phases,'commands':results,'at':now().isoformat()});return True
  ids=[c['id'] for c in rep['cases']];expected=set(M['mandatory_ids'])|({'CX%02d'%i for i in range(12)} if cx else set());valid=not rep.get('setup_error') and not rep.get('setup_error_ids') and len(ids)==len(set(ids)) and set(ids)==expected and rep.get('total')==len(expected) and rep.get('harness_sha256')==sha(harness) and rep.get('test_culture')==('tr-TR' if cx else 'en-US') and rep.get('cleanup',{}).get('status')=='ok'
  if name=='baseline':valid=valid and rc==1 and rep.get('failed')==26 and all(c['outcome']=='failed' and 'API_ABSENT' in str(c['reason']) for c in rep['cases'])
  else:
   valid=valid and rc==0 and rep.get('passed')==len(expected) and rep.get('failed')==0 and rep.get('api_state')=='present' and rep.get('module_sha256')==M['file_sha256'][REL] and rep.get('primitives_replaced')=='10/10 asserted before any product call'
   if valid:
    valid=rep['cleanup']['keep_sentinel_intact'] is True and rep['cleanup']['tree_removed'] is True and rep['cleanup']['wire_servers_stopped'] is True
    for c in rep['children']:
     if c['kind'].startswith('counterexample'):continue
     valid=valid and c['ps_version'] and c['ps_edition'] and c['culture']==('tr-TR' if cx else 'en-US')
  if name=='candidate' and valid:
   phases[label]['listener_probe']=rep.get('listener_probe');assert rep.get('primitive_table')=='r4 (10 keys)'
   phases[label]['nested_artifact_verification']=verify_nested(rep,lambda p:pathlib.Path(p),True)
  if cx and valid:phases[label]['independently_verified_counterexamples']=validate_cx(rep,exe,ev)
  if cx and valid:
   for rec in rep['counterexample_evidence']:
    cr=json.loads(pathlib.Path(rec['report_path']).read_text(encoding='utf-8-sig'));verify_nested(cr,lambda p:pathlib.Path(p),rec['id']=='CX00')
  phases[label]['operator_validated']=bool(valid);save(W/'phase-progress.json',{'candidate':M['candidate'],'phases':phases,'commands':results,'at':now().isoformat()});return bool(valid)
 normal=True
 for psid,exe in [('ps51',PS51),('ps7',PS7)]:
  b=measure('baseline',base,exe,psid);c=measure('candidate',cand,exe,psid);normal=normal and b and c
 closure=True
 if normal:
  for psid,exe in [('ps51',PS51),('ps7',PS7)]:closure=measure('old-h3',old,exe,psid) and closure
 cxok=False
 if normal and closure:
  cxok=True
  for psid,exe in [('ps51',PS51),('ps7',PS7)]:ok=measure('candidate',cand,exe,psid,True);cxok=cxok and ok
 dirty={name:git(repo,'status','--porcelain','--untracked-files=all',label=name+'-status-after') for name,repo in [('baseline',base),('candidate',cand),('old_h3',old)]};after_files={'baseline':files(base),'candidate':files(cand),'old_h3':files(old)};save(W/'after-file-hashes.json',after_files);assert before_files==after_files
 _,out=run([PS51,'-NoProfile','-NonInteractive','-Command',probe],'host-after',env=env);afterhost=json.loads(out);afterhost['win32_GetACP']=ctypes.windll.kernel32.GetACP();assert afterhost['win32_GetACP']==host['win32_GetACP'] and afterhost['service']==afterhost['process']==0;save(W/'host-after.json',afterhost)
 with pathlib.Path(r'C:\tl-win\do-luong.csv').open(encoding='utf-8-sig',newline='') as f:rows=[x for x in csv.DictReader(f) if x.get('session')==SID]
 assert len(rows)==len(phases);save(W/'ledger-own-rows.json',rows);final={'candidate':M['candidate'],'normal_comparison_passed':normal,'counterexamples_passed':cxok,'F03_closure_comparison_passed':closure,'counterexamples_not_run_reason':None if normal else 'normal comparison failed; blocked','phases':phases,'identities':identities,'dirty':dirty,'commands':results,'finished_at':now().isoformat()};save(W/'measurement.json',final);say({'measurement':str(W/'measurement.json'),'normal_comparison_passed':normal,'counterexamples_passed':cxok});return 0 if normal and cxok and not any(dirty.values()) else 1
try:rc=main()
except Exception as e:
 say({'operator_error':type(e).__name__+': '+str(e)})
 if W.exists():save(W/'operator-error.json',{'error':str(e),'commands':results,'traceback':traceback.format_exc()})
 rc=2
finally:
 stop.set()
 if thread:thread.join(timeout=3)
 if taken:
  if own():
   before=LOCK.read_text(encoding='utf-8-sig');LOCK.write_text('',encoding='utf-8');after=LOCK.read_text(encoding='utf-8-sig');save(W/'lock-release.json',{'session':SID,'at':now().isoformat(),'before':before,'after':after,'released':after==''});rc=rc if after=='' else 2
  else:save(W/'lock-release.json',{'session':SID,'released':False,'error':'ownership lost; foreign lock untouched'});rc=2
sys.exit(rc)
