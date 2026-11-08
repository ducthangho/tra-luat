from pathlib import Path,PureWindowsPath
import json,hashlib,datetime,shutil
from g3_native_evidence import verify_nested,MissingNestedArtifact
nested=[]
S=Path('/workspace/scratch/proxima-p1-s2-20261108');D=S/'windows-b75d9e4e61e5-g3-evidence';R=Path('/workspace/scratch/wp1279-g3-claude');H='b75d9e4e61e5fd16aa9d4870f5fa844fb6029766';native=PureWindowsPath(r'C:\tl-win\wp1279-r3-g3\final-b75d9e4e61e5')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def mapped(p):
 rel=PureWindowsPath(p).relative_to(native);assert '..' not in rel.parts;return D.joinpath(*rel.parts)
manifest=read(D/'source-byte-manifest.json');assert len(manifest)==1031
for n,x in manifest.items():assert sha(D/n)==x['sha256'] and (D/n).stat().st_size==x['bytes']
m=read(D/'measurement.json');assert m['candidate']==H and m['normal_comparison_passed'] is True and m['counterexamples_passed'] is True and not any(m['dirty'].values());assert read(D/'before-file-hashes.json')==read(D/'after-file-hashes.json');lock=read(D/'lock-release.json');assert lock['released'] is True and lock['after']==''
identity=read(D/'identity.json');M=identity['manifest'];assert M['candidate']==H and M['tree']=='fbd7b8407eaa6ce08eb475e74b07546abe09a0a7' and M['baseline']=='c15603dcf537fa4beb753b263398d6e6b8c92019';assert identity['lock_session']==lock['session'];assert len(read(D/'ledger-own-rows.json'))==8
orig={p.name:p.read_bytes() for p in (R/'.agents/skills/proxima-control/scripts').iterdir() if p.name in ['ProximaControl.psm1','ProximaConfig.psm1','Run-Px.ps1']};harness=R/'.agents/skills/proxima-control/tests/ProximaControl.Tests.ps1';normal=set(M['mandatory_ids']);verified=[]
for name,phase in m['phases'].items():
 rep=phase['report'];rp=D/'reports'/(name+'.json');assert read(rp)==rep and sha(rp)==phase['report_sha256'];assert not rep['setup_error'] and not rep['setup_error_ids'];assert rep['harness_sha256']==sha(harness) and rep['cleanup']['status']=='ok' and phase['operator_validated'] is True
 cx=name.endswith('counterexamples');ids={c['id'] for c in rep['cases']};expected=normal|({'CX%02d'%i for i in range(11)} if cx else set());assert len(rep['cases'])==len(ids)==len(expected) and ids==expected and rep['total']==len(expected)
 assert rep['ps_edition']==('Desktop' if '-ps51' in name else 'Core');assert rep['ps_version'].startswith('5.1.' if '-ps51' in name else '7.')
 if name.startswith('baseline'):
  assert phase['rc']==1 and rep['failed']==25 and rep['passed']==0 and rep['api_state']=='module_absent' and all(c['outcome']=='failed' and 'API_ABSENT' in c['reason'] for c in rep['cases']);continue
 if name.startswith('old-h2'):
  assert phase['rc']==1 and rep['passed']==24 and rep['failed']==1
  v=verify_nested(rep,mapped,False);nested.append({'phase':name,'verification':v});assert all((x['valid_path_fqid'] and x['valid_path_result'] is None) if name.endswith('ps51') else (not x['valid_path_fqid'] and x['valid_path_result']['outcome']=='ok') for x in v['endpoint_observations']);continue
 v=verify_nested(rep,mapped,True);nested.append({'phase':name,'verification':v})
 assert phase['rc']==0 and rep['passed']==len(expected) and rep['failed']==0 and rep['cleanup']['tree_removed'] is True and rep['cleanup']['keep_sentinel_intact'] is True and rep['cleanup']['wire_servers_stopped'] is True and rep['primitives_replaced']=='9/9 asserted before any product call'
 assert rep['test_culture']==('tr-TR' if cx else 'en-US') and rep['test_ui_culture']==rep['test_culture'];assert rep['module_sha256']==hashlib.sha256(orig['ProximaControl.psm1']).hexdigest()
 for child in rep['children']:
  if child['kind'].startswith('counterexample'):continue
  assert child['culture']==rep['test_culture'] and child['ui_culture']==rep['test_culture'] and child['ps_version'] and child['ps_edition']
 if not cx:continue
 records=rep['counterexample_evidence'];assert len(records)==11 and {c['id'] for c in records}=={'CX%02d'%i for i in range(11)}
 for x in records:
  cp=mapped(x['report_path']);op=mapped(x['output_path']);assert sha(cp)==x['report_sha256'] and sha(op)==x['output_sha256'];assert read(Path(str(cp).removesuffix('.report.json')+'.record.json'))==x
  src=cp.parent/x['id']
  for fn,key in [('ProximaControl.psm1','module_sha256'),('Run-Px.ps1','wrapper_sha256'),('ProximaConfig.psm1','config_module_sha256')]:
   actual=(src/fn).read_bytes();assert hashlib.sha256(actual).hexdigest()==x[key];want=orig[fn]
   if x['mutated_file']==fn:
    anchor=x['anchor'].encode();replacement=x['replacement'].encode();assert want.count(anchor)==1;want=want.replace(anchor,replacement,1)
   assert actual==want,('source reconstruction',name,x['id'],fn)
  cr=read(cp);nested.append({'phase':name+'/'+x['id'],'verification':verify_nested(cr,mapped,x['id']=='CX00')});cmd=x['command'];assert mapped(cmd[cmd.index('-ReportPath')+1])==cp and cmd[cmd.index('-TestCulture')+1]=='tr-TR';assert cr['module_sha256']==x['module_sha256'] and cr['wrapper_sha256']==x['wrapper_sha256'] and cr['harness_sha256']==sha(harness) and cr['api_state']=='present';assert cr['test_culture']==cr['test_ui_culture']=='tr-TR' and cr['ps_edition']==rep['ps_edition'] and cr['ps_version']==rep['ps_version'];assert not cr['setup_error'] and not cr['setup_error_ids'] and cr['cleanup']['status']=='ok' and cr['cleanup']['keep_sentinel_intact'] is True and cr['cleanup']['wire_servers_stopped'] is True;assert {c['id'] for c in cr['cases']}==normal and cr['total']==25
  for child in cr['children']:assert child['culture']==child['ui_culture']=='tr-TR' and child['ps_version'] and child['ps_edition']
  if x['id']=='CX00':assert x['rc']==0 and cr['passed']==25 and cr['failed']==0 and x['credited'] is False
  else:
   assert x['rc']==1 and x['credited'] is True and x['verdict'].startswith('KILLED')
   for w in x['required']:
    cid,tok=w.split(':',1);assert any(c['id']==cid and c['outcome']=='failed' and tok in str(c['reason']) for c in cr['cases'])
  verified.append({'phase':name,'id':x['id'],'rc':x['rc'],'source_reconstructed':True,'named_required':x['required'],'report_sha256':sha(cp),'output_sha256':sha(op),'actual_ps_edition':cr['ps_edition'],'actual_ps_version':cr['ps_version'],'actual_culture':cr['test_culture']})
assert len(verified)==22
negative=D.parent/'g3-f02-negative-private-copy';negative.mkdir(exist_ok=False);shutil.copytree(D,negative/'proof');copy=negative/'proof'
rep=m['phases']['candidate-ps51']['report'];victim=next(a for a in rep['evidence']['artifacts'] if a['role']=='endpoint-report');original=mapped(victim['path']);before=sha(original);relative=original.relative_to(D);(copy/relative).unlink()
def copy_map(p):return copy/mapped(p).relative_to(D)
try:verify_nested(rep,copy_map,True)
except MissingNestedArtifact as e:
 token=str(e);assert token.startswith('MISSING_NESTED_ARTIFACT:endpoint-report:');assert sha(original)==before;(negative/'result.json').write_text(json.dumps({'expected_rejection':True,'reason':token,'deleted_copy_relative':str(relative),'original_sha256_unchanged':before,'verifier_sha256':sha(Path(__file__))},indent=2)+'\n')
else:raise AssertionError('missing nested artifact accepted')
index={'gate_status':'passed','formal_code_approval':False,'head':H,'tree':M['tree'],'base':M['baseline'],'archive_sha256':sha(S/'windows-b75d9e4e61e5-g3-evidence.zip'),'archive_bytes':(S/'windows-b75d9e4e61e5-g3-evidence.zip').stat().st_size,'source_files_verified':len(manifest),'operator_input_harness_sha256':sha(harness),'verified_counterexample_children':verified,'nested_verifications':nested,'F02_negative':json.loads((negative/'result.json').read_text()),'normal':'both25/25rc0/en-US;baselineboth25API_ABSENTrc1/no setup','focused':'both36/36rc0/tr-TR; unmodifiedcontrolplus10actualnamedkillsperruntime','cleanup':'before/after measuredGit/filesystembytes identical; parenttree removed, sentinel intact, wires stopped, lockreleasedempty','measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verifier_sha256':sha(Path(__file__)),'limitations':'Native isolated language/serialization/ownedfixtures only, no realWinRM/service/gateway/auth/provenance/activation; modelreview pending. Archive source-byte hashes are native retained original file bytes; DesktopCommander terminal transport is received Unicode serialization, no remote raw-byte claim.'};(S/'windows-b75d9e4e61e5-g3-evidence-index.json').write_text(json.dumps(index,indent=2)+'\n');print({'gate_status':index['gate_status'],'verified_sources':len(manifest),'verified_children':len(verified),'archive_sha256':index['archive_sha256']})
