from pathlib import Path,PureWindowsPath as WP
import hashlib,json,importlib.util,shutil,datetime
S=Path('/workspace/scratch/proxima-rest-20261108');R=S/'native-S3-recovery4/extracted';W=WP(r'C:\tl-win\wp1285-r2-g2\H4196fbaaeb13-recovery4');H='4196fbaaeb13b4d26d5f4f452b6c1a8b26150489';B='bf9914cb1a8e6f5047468f4d130b587015f8d73f'
sp=importlib.util.spec_from_file_location('legacy','/workspace/scratch/proxima-p1-s2-20261108/g4_native_evidence.py');legacy=importlib.util.module_from_spec(sp);sp.loader.exec_module(legacy)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
class MissingNestedArtifact(Exception):pass
def verify(root):
 def mp(v):
  p=root/Path(*WP(v).relative_to(W).parts)
  if not p.is_file():raise MissingNestedArtifact(v)
  return p
 manifest=read(root/'source-byte-manifest.json')
 for p,a in manifest.items():
  f=root/p
  if not f.is_file():raise MissingNestedArtifact(p)
  assert sha(f)==a['sha256'] and f.stat().st_size==a['bytes'],p
 assert len(manifest)==407
 m=read(root/'measurement.json');assert m['candidate']==H and m['baseline']==B and all(m[k] is True for k in ['normal_comparison_passed','counterexamples_passed','legacy_S2_normal_passed']);assert m['dirty']=={'baseline':'','candidate':''};assert read(root/'terminal.json')['rc']==0 and read(root/'terminal.json')['phase_count']==8;assert read(root/'lock-release.json')['released'] and read(root/'lock-release.json')['after']=='';assert read(root/'before-file-hashes.json')==read(root/'after-file-hashes.json')
 for name in ['host-before','host-after']:
  h=read(root/(name+'.json'));assert h['host']=='DESKTOP-T9R33P2' and h['service']==h['process']==0;assert 'python' in h and h['memory'][0]['FreeVirtualMemory']>0
 for c in m['commands']:assert sha(root/'logs'/(c['label']+'.log'))==c['log_sha256']
 seen=set();arts=0;cxrows=[];legacyrows=[];normalids={f'PM{i:02d}' for i in range(1,8)}
 def s3(rep):
  nonlocal arts
  assert rep['schema']=='proxima_manifest_tests.v1' and rep['setup_error'] is None and rep['evidence']['check']['status']=='ok'
  assert {x['id'] for x in rep['cases']}>=normalids
  for a in rep['evidence']['artifacts']:assert sha(mp(a['path']))==a['sha256'];arts+=1
  for c in rep['children']:
   assert not c['timed_out'];mp(c['stdout']);mp(c['stderr']);argv=c['argv'];assert '-ExecutionPolicy' not in argv and '-File' in argv;mp(argv[argv.index('-File')+1])
  for cx in rep.get('counterexamples',[]):
   q=read(mp(cx['report_path']));s3(q)
   if cx['id']=='CX00':assert cx['rc']==0 and q['passed']==q['total']==7;continue
   assert cx['rc']==1 and cx['credited'] is True and q['setup_error'] is None
   base=mp(rep['addon_root']+'\\'+cx['mutated_file']);mut=mp(cx['source_dir']+'\\'+cx['mutated_file']);assert sha(base)==cx['sha256_before'] and sha(mut)==cx['sha256_after'];old=base.read_text(encoding='utf-8-sig');new=mut.read_text(encoding='utf-8-sig');assert old.count(cx['anchor'])==1;assert old.replace(cx['anchor'],cx['replacement'].replace('\r\n','\n'))==new
   if cx['id'] in ['CX01','CX02','CX03']:
    assert q['runtime_children']==0;case=next(c for c in q['cases'] if c['id']=='PM02');assert case['outcome']=='failed' and cx['want'].split(':',1)[1] in case['reason'];assert next(c for c in q['cases'] if c['id']=='PM04')['reason'].startswith('NOT_EXECUTED:')
   else:assert cx['id']=='CX04' and next(c for c in q['cases'] if c['id']=='PM05')['outcome']=='failed'
   cxrows.append({'runtime':rep['ps_version'],'id':cx['id'],'rc':cx['rc'],'matched':cx['matched']})
 for label,ph in m['phases'].items():
  assert sha(mp(ph['report_path']))==ph['report_sha256'];rep=read(mp(ph['report_path']));assert rep==ph['report'];seen.add(label)
  if ph['kind']=='legacyS2normal':
   assert ph['rc']==0 and rep['passed']==rep['total']==26;legacyrows.append(legacy.verify_nested(rep,mp));continue
  s3(rep)
  if label.startswith('baseline'):assert ph['rc']==1 and rep['passed']==0 and rep['total']==7 and all(c['outcome']=='failed' and ('ABSENT' in c['reason']) for c in rep['cases'])
  else:assert ph['rc']==0 and rep['passed']==rep['total']==(12 if label.endswith('CX') else 7)
 assert len(seen)==8 and len(cxrows)==8
 return {'passed':True,'source_files_verified':len(manifest),'commands_verified':len(m['commands']),'S3_artifact_refs_verified':arts,'phases':sorted(seen),'counterexamples':cxrows,'legacy_nested':legacyrows}
if __name__=='__main__':
 result=verify(R);negative=S/'native-S3-missing-dependency-negative';
 if not negative.exists():shutil.copytree(R,negative)
 rep=read(negative/'reports/legacy-S2-ps51.json');victimwin=next(a['path'] for a in rep['evidence']['artifacts'] if a['role']=='endpoint-input');victim=negative/Path(*WP(victimwin).relative_to(W).parts);rel=victim.relative_to(negative);victim.unlink()
 try:verify(negative)
 except (MissingNestedArtifact,legacy.MissingNestedArtifact) as e:result['missing_dependency_negative']={'detected':True,'deleted_path':str(rel),'error':str(e)}
 else:raise AssertionError('missing dependency incorrectly accepted')
 result.update({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':H,'baseline':B,'original_archive_sha256':sha(S/'native-S3-recovery4/original-evidence.zip')});(S/'S3-native-ONCE-verifier-receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
