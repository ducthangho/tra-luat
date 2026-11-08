from pathlib import Path,PureWindowsPath
import json,hashlib,datetime,shutil,re,subprocess,sys
from g4_native_evidence import verify_nested,MissingNestedArtifact
nested=[]
S=Path('/workspace/scratch/proxima-p1-s2-20261108');D=S/'windows-bc16ccff3601-g4-evidence';R=Path('/workspace/scratch/wp1279-g4-claude');H='bc16ccff3601fabeeb783f41b52360ef5851838a';native=PureWindowsPath(r'C:\tl-win\wp1279-r4-g4\final-bc16ccff3601')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def mapped(p):
 rel=PureWindowsPath(p).relative_to(native);assert '..' not in rel.parts;return D.joinpath(*rel.parts)
manifest=read(D/'source-byte-manifest.json');assert len(manifest)>0
for n,x in manifest.items():assert sha(D/n)==x['sha256'] and (D/n).stat().st_size==x['bytes']
m=read(D/'measurement.json');assert m['candidate']==H and m['normal_comparison_passed'] is True and m['counterexamples_passed'] is True and not any(m['dirty'].values());assert read(D/'before-file-hashes.json')==read(D/'after-file-hashes.json');lock=read(D/'lock-release.json');assert lock['released'] is True and lock['after']==''
identity=read(D/'identity.json');M=identity['manifest'];assert M['candidate']==H and M['tree']=='30cbf51650d88f05c0fcae977dd9df286a089204' and M['baseline']=='c15603dcf537fa4beb753b263398d6e6b8c92019';assert identity['lock_session']==lock['session'];assert len(read(D/'ledger-own-rows.json'))==8
orig={p.name:p.read_bytes() for p in (R/'.agents/skills/proxima-control/scripts').iterdir() if p.name in ['ProximaControl.psm1','ProximaConfig.psm1','Run-Px.ps1']};harness=R/'.agents/skills/proxima-control/tests/ProximaControl.Tests.ps1';normal=set(M['mandatory_ids']);verified=[]
atom=r"'((?:''|[^'])*)'"
pattern=r"@\{\s*id\s*=\s*"+atom+r";\s*file\s*=\s*"+atom+r";\s*e\s*=\s*@\(\s*"+atom+r",\s*"+atom+r"\s*\);\s*red\s*=\s*@\((.*?)\)\s*\}"
definitions={}
for z in re.finditer(pattern,harness.read_text(),re.S):
 cid,fn,anchor,repl,red=z.groups();assert cid not in definitions;definitions[cid]={'file':fn.replace("''","'"),'anchor':anchor.replace("''","'"),'replacement':repl.replace("''","'"),'required':[x.replace("''","'") for x in re.findall(atom,red)]}
assert set(definitions)=={'CX%02d'%i for i in range(1,12)}
module=(R/'.agents/skills/proxima-control/scripts/ProximaControl.psm1').read_text();tcp_line=next(l for l in module.splitlines() if re.match(r'\s*GetTcpListener\s*=',l));tcp_block=tcp_line.split('=',1)[1].strip();assert tcp_block.startswith('{') and tcp_block.endswith('}');tcp_body=tcp_block[1:-1].strip()
probe_observations=[]
def probe(rep,where):
 p=rep['listener_probe'];assert isinstance(p,dict) and p['command']==tcp_body and p['port']>0 and p['harness_pid']>0
 assert p['rc'] in ['ok','error'] and p['verdict'] in ['owned_listener_observed','unmeasured_fail_closed_expected']
 if p['verdict']=='owned_listener_observed':
  assert p['rc']=='ok';found=[]
  for row in p['records']:
   vals={k:(v.split(':',1) if isinstance(v,str) else [None,None]) for k,v in row.items()}
   if vals['LocalAddress'][1]=='127.0.0.1' and vals['State'][1]=='2' and vals['OwningProcess'][1]==str(p['harness_pid']):
    assert vals['LocalAddress'][0]=='System.String' and vals['LocalPort'][0] in ['System.Byte','System.SByte','System.Int16','System.UInt16','System.Int32','System.UInt32','System.Int64','System.UInt64'];assert int(vals['LocalPort'][1])==p['port'];found.append(row)
  assert found
 probe_observations.append({'phase':where,'actual_probe':p,'limit':'owned-loopback readonly defaultquery onthisnativeuser only; notsession0remote/realProxima/auth/deployment assurance'})
for name,phase in m['phases'].items():
 rep=phase['report'];rp=D/'reports'/(name+'.json');assert read(rp)==rep and sha(rp)==phase['report_sha256'];assert not rep['setup_error'] and not rep['setup_error_ids'];assert rep['harness_sha256']==sha(harness) and rep['cleanup']['status']=='ok' and phase['operator_validated'] is True
 cx=name.endswith('counterexamples');ids={c['id'] for c in rep['cases']};expected=normal|({'CX%02d'%i for i in range(12)} if cx else set());assert len(rep['cases'])==len(ids)==len(expected) and ids==expected and rep['total']==len(expected)
 assert rep['ps_edition']==('Desktop' if '-ps51' in name else 'Core');assert rep['ps_version'].startswith('5.1.' if '-ps51' in name else '7.')
 if name.startswith('baseline'):
  assert phase['rc']==1 and rep['failed']==26 and rep['passed']==0 and rep['api_state']=='module_absent' and all(c['outcome']=='failed' and 'API_ABSENT' in c['reason'] for c in rep['cases']);continue
 if name.startswith('old-h3'):
  assert phase['rc']==1 and rep['api_state']=='present' and rep['module_sha256']==M['old_h3_file_sha256']['.agents/skills/proxima-control/scripts/ProximaControl.psm1']
  bad=next(c for c in rep['cases'] if c['id']=='X5-09');assert bad['outcome']=='failed';reason=str(bad['reason']);rawlog=(D/'logs'/(name+'.log')).read_text(encoding='utf-8',errors='replace')
  for token in M['f03_failure_tokens']:assert token in reason and token in rawlog
  assert re.search(r'LISTENER_OWNERSHIP_BYPASS\[wire px models\] requests=[1-9][0-9]* auth=[1-9][0-9]*',reason)
  v=verify_nested(rep,mapped,True);nested.append({'phase':name,'verification':v,'F03_named_actual_wrong_listener':reason,'other_diagnostics_not_credited':[c for c in rep['cases'] if c['outcome']=='failed' and c['id']!='X5-09']});continue
 v=verify_nested(rep,mapped,True);nested.append({'phase':name,'verification':v});probe(rep,name);assert rep['primitive_table']=='r4 (10 keys)'
 assert phase['rc']==0 and rep['passed']==len(expected) and rep['failed']==0 and rep['cleanup']['tree_removed'] is True and rep['cleanup']['keep_sentinel_intact'] is True and rep['cleanup']['wire_servers_stopped'] is True and rep['primitives_replaced']=='10/10 asserted before any product call'
 assert rep['test_culture']==('tr-TR' if cx else 'en-US') and rep['test_ui_culture']==rep['test_culture'];assert rep['module_sha256']==hashlib.sha256(orig['ProximaControl.psm1']).hexdigest()
 for child in rep['children']:
  if child['kind'].startswith('counterexample'):continue
  assert child['culture']==rep['test_culture'] and child['ui_culture']==rep['test_culture'] and child['ps_version'] and child['ps_edition']
 if not cx:continue
 records=rep['counterexample_evidence'];assert len(records)==12 and {c['id'] for c in records}=={'CX%02d'%i for i in range(12)}
 for x in records:
  if x['id']!='CX00':
   df=definitions[x['id']];assert x['mutated_file']==df['file'] and x['anchor']==df['anchor'] and x['replacement']==df['replacement'] and x['required']==df['required']
  cp=mapped(x['report_path']);op=mapped(x['output_path']);assert sha(cp)==x['report_sha256'] and sha(op)==x['output_sha256'];assert read(Path(str(cp).removesuffix('.report.json')+'.record.json'))==x
  src=cp.parent/x['id']
  for fn,key in [('ProximaControl.psm1','module_sha256'),('Run-Px.ps1','wrapper_sha256'),('ProximaConfig.psm1','config_module_sha256')]:
   actual=(src/fn).read_bytes();assert hashlib.sha256(actual).hexdigest()==x[key];want=orig[fn]
   if x['mutated_file']==fn:
    anchor=x['anchor'].encode();replacement=x['replacement'].encode();assert want.count(anchor)==1;want=want.replace(anchor,replacement,1)
   assert actual==want,('source reconstruction',name,x['id'],fn)
  cr=read(cp);assert not PureWindowsPath(cr['evidence']['dir']).is_relative_to(PureWindowsPath(rep['scratch'])) and not PureWindowsPath(cr['evidence']['dir']).is_relative_to(PureWindowsPath(x['source_dir']));probe(cr,name+'/'+x['id']);nested.append({'phase':name+'/'+x['id'],'verification':verify_nested(cr,mapped,x['id']=='CX00')});cmd=x['command'];assert mapped(cmd[cmd.index('-ReportPath')+1])==cp and cmd[cmd.index('-TestCulture')+1]=='tr-TR';assert cr['module_sha256']==x['module_sha256'] and cr['wrapper_sha256']==x['wrapper_sha256'] and cr['harness_sha256']==sha(harness) and cr['api_state']=='present';assert cr['test_culture']==cr['test_ui_culture']=='tr-TR' and cr['ps_edition']==rep['ps_edition'] and cr['ps_version']==rep['ps_version'];assert not cr['setup_error'] and not cr['setup_error_ids'] and cr['cleanup']['status']=='ok' and cr['cleanup']['keep_sentinel_intact'] is True and cr['cleanup']['wire_servers_stopped'] is True;assert {c['id'] for c in cr['cases']}==normal and cr['total']==26
  for child in cr['children']:assert child['culture']==child['ui_culture']=='tr-TR' and child['ps_version'] and child['ps_edition']
  if x['id']=='CX00':assert x['rc']==0 and cr['passed']==26 and cr['failed']==0 and x['credited'] is False
  else:
   assert x['rc']==1 and x['credited'] is True and x['verdict'].startswith('KILLED')
   for w in x['required']:
    cid,tok=w.split(':',1);assert any(c['id']==cid and c['outcome']=='failed' and tok in str(c['reason']) for c in cr['cases'])
  verified.append({'phase':name,'id':x['id'],'rc':x['rc'],'source_reconstructed':True,'named_required':x['required'],'report_sha256':sha(cp),'output_sha256':sha(op),'actual_ps_edition':cr['ps_edition'],'actual_ps_version':cr['ps_version'],'actual_culture':cr['test_culture']})
assert len(verified)==24
negative=D.parent/'g4-f02-negative-private-copy';negative.mkdir(exist_ok=False);shutil.copytree(D,negative/'proof');copy=negative/'proof'
rep=m['phases']['candidate-ps51']['report'];victim=next(a for a in rep['evidence']['artifacts'] if a['role']=='endpoint-report');original=mapped(victim['path']);before=sha(original);relative=original.relative_to(D);(copy/relative).unlink()
def copy_map(p):return copy/mapped(p).relative_to(D)
negative_script=S/'g4-f02-negative-check.py'
negative_script.write_text("from pathlib import Path,PureWindowsPath\nimport json\nfrom g4_native_evidence import verify_nested\nD=Path("+repr(str(copy))+")\nW=PureWindowsPath("+repr(str(native))+ ")\nrep=json.loads((D/'measurement.json').read_text(encoding='utf-8-sig'))['phases']['candidate-ps51']['report']\ndef mapped(p):return D.joinpath(*PureWindowsPath(p).relative_to(W).parts)\nverify_nested(rep,mapped,True)\n")
cmd=[sys.executable,'-B',str(negative_script)];q=subprocess.run(cmd,capture_output=True);(negative/'stdout.log').write_bytes(q.stdout);(negative/'stderr.log').write_bytes(q.stderr);assert q.returncode!=0 and b'MissingNestedArtifact: MISSING_NESTED_ARTIFACT:endpoint-report:' in q.stderr;assert sha(original)==before
(negative/'result.json').write_text(json.dumps({'expected_rejection':True,'strict_checker_child_rc':q.returncode,'command':cmd,'reason':q.stderr.decode().strip().splitlines()[-1],'deleted_copy_relative':str(relative),'original_sha256_unchanged':before,'negative_script_sha256':sha(negative_script),'stdout_sha256':sha(negative/'stdout.log'),'stderr_sha256':sha(negative/'stderr.log'),'parent_verifier_sha256':sha(Path(__file__))},indent=2)+'\n')
assert read(D/'host-preflight.json')['win32_GetACP']==read(D/'host-after.json')['win32_GetACP']==1252
index={'gate_status':'passed','formal_code_approval':False,'head':H,'tree':M['tree'],'base':M['baseline'],'archive_sha256':sha(S/'windows-bc16ccff3601-g4-evidence.zip'),'archive_bytes':(S/'windows-bc16ccff3601-g4-evidence.zip').stat().st_size,'source_files_verified':len(manifest),'operator_input_harness_sha256':sha(harness),'verified_counterexample_children':verified,'listener_default_query_observations':probe_observations,'committed_mutant_definitions_independently_parsed':definitions,'F03_native_closure_only':'namedmock+actualwireauth failures onoldH3bothruntimes, H4normal26/focused38 passed; formalreview3pending','nested_verifications':nested,'F02_negative':json.loads((negative/'result.json').read_text()),'normal':'both26/26rc0/en-US;baselineboth26API_ABSENTrc1/no setup','focused':'both38/38rc0/tr-TR; unmodifiedcontrolplus11actualnamedkillsperruntime','cleanup':'before/after measuredGit/filesystembytes identical; parenttree removed, sentinel intact, wires stopped, lockreleasedempty','measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verifier_sha256':sha(Path(__file__)),'limitations':'Native isolated language/serialization/ownedfixtures only, no realWinRM/service/gateway/auth/provenance/activation; modelreview pending. Archive source-byte hashes are native retained original file bytes; DesktopCommander terminal transport is received Unicode serialization, no remote raw-byte claim.'};(S/'windows-bc16ccff3601-g4-evidence-index.json').write_text(json.dumps(index,indent=2)+'\n');print({'gate_status':index['gate_status'],'verified_sources':len(manifest),'verified_children':len(verified),'archive_sha256':index['archive_sha256']})
