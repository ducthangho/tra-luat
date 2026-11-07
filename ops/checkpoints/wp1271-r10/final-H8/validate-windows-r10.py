import pathlib,json,hashlib,zipfile,sys,collections
S=pathlib.Path('/workspace/scratch/proxima-p1-s1-20261107');P='d2fecaa1516c';H='d2fecaa1516cbc8c20b70331a45c8c728e59ddce';C='c6afde62c846f1ef3d6a83c14459966849edf756'
z=S/('windows-'+P+'-final-evidence.zip');expected=sys.argv[1];size=int(sys.argv[2]);count=int(sys.argv[3]);assert z.stat().st_size==size and hashlib.sha256(z.read_bytes()).hexdigest()==expected
D=S/('windows-'+P+'-final-evidence');D.mkdir(exist_ok=False)
with zipfile.ZipFile(z) as f:
 for x in f.infolist():
  p=pathlib.PurePosixPath(x.filename);assert not p.is_absolute() and '..' not in p.parts and not (x.external_attr>>16)&0o170000==0o120000
 f.extractall(D)
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
source=read(D/'source-byte-manifest.json');assert len(source)==count
for p,v in source.items():q=D/p;assert q.stat().st_size==v['bytes'] and sha(q)==v['sha256'],p
M=read(D/'operator-inputs/candidate-final-manifest.json');assert M['candidate']==H and M['baseline']==C
assert M['file_sha256']==read(S/'g10-candidate-identity.json')['file_sha256']
assert sha(D/'operator-inputs/windows-compare-r10.py')==M['operator_sha256']==sha(S/'windows-compare-r10.py')
assert sha(D/'operator-inputs/device-online.json')==M['device_online_sha256']
assert sha(D/'harness/ProximaConfig.Tests.ps1')==M['file_sha256']['.agents/skills/proxima-control/tests/ProximaConfig.Tests.ps1']
a=read(D/'measurement.json');assert a['normal_comparison_passed'] and a['counterexamples_passed'] and not any(a['dirty'].values());assert a['identities']['baseline']['sha']==C and a['identities']['candidate']['sha']==H
assert a['identities']['baseline']['tree']==M['baseline_tree'] and a['identities']['candidate']['tree']==M['tree']
assert read(D/'before-file-hashes.json')==read(D/'after-file-hashes.json')
assert read(D/'lock-release.json')['released'] and read(D/'lock-release.json')['after']==''
assert read(D/'unrelated-mapping-after-tests.json')['unchanged'] and read(D/'unrelated-mapping-cleanup.json')['removed']
commands={x['label']:x for x in a['commands']}
for label,row in commands.items():assert sha(D/'logs'/(label+'.log'))==row['log_sha256'],label
remote=pathlib.PureWindowsPath(r'C:\tl-win\wp1271-r10-g10\final-d2fecaa1516c')
def local(p):return D/pathlib.PureWindowsPath(p).relative_to(remote).as_posix()
phases={};children=0;projection=[]
for name,phase in a['phases'].items():
 r=phase['report'];cx=name.endswith('-counterexamples');base=name.startswith('baseline');culture='tr-TR' if cx else 'en-US';assert r['test_culture']==culture and r['test_ui_culture']==culture
 assert sha(D/'reports'/(name+'.json'))==phase['report_sha256'];assert r==read(D/'reports'/(name+'.json'));assert not r.get('setup_error') and not r.get('setup_error_ids')
 assert r['harness_sha256']==sha(D/'harness/ProximaConfig.Tests.ps1') and r['alias_r']=='Invoke-History'
 clean=r['cleanup'];assert clean['status']=='ok' and clean['keep_sentinel_intact'] and clean['mappings_before']==clean['mappings_after'] and clean['vhd']['removed']
 if base:
  assert phase['rc']==1 and r['total']==23 and r['passed']==0 and all(c['outcome']=='failed' and 'API_ABSENT' in c['reason'] for c in r['cases'])
 else:
  assert phase['rc']==0 and r['passed']==r['total']==(49 if cx else 23) and r['failed']==0 and all(c['outcome']=='passed' for c in r['cases'])
  projection += [{'id':name+':'+c['id'],'ket_qua':'passed'} for c in r['cases']]
 if cx:
  records=r['counterexample_evidence'];assert len(records)==26 and {x['id'] for x in records}==set(M['counterexample_only_ids']);kinds=collections.Counter(x['kind'] for x in records);assert dict(kinds)=={'m':24,'c':1,'i':1}
  for x in records:
   children+=1
   for f in ['report','output','mutant']:
    if x.get(f+'_path'):assert sha(local(x[f+'_path']))==x[f+'_sha256']
   reportpath=local(x['report_path']);child=read(reportpath);record=read(pathlib.Path(str(reportpath).removesuffix('.report.json')+'.record.json'));assert record==x
   cmd=x['command'];assert '-TestCulture' in cmd and cmd[cmd.index('-TestCulture')+1]=='tr-TR' and child['test_culture']=='tr-TR' and child['test_ui_culture']=='tr-TR'
   assert child['harness_sha256']==r['harness_sha256'] and not child.get('setup_error')
   if x['kind']=='i':assert x['rc']==2 and not x['credited'] and child['cleanup']['status']=='failed' and child['passed']==child['total'] and child['total']>0
   else:
    assert x['rc']==1 and child['cleanup']['status']=='ok'
    for w in x['required']:
     cid,token=w.split(':',1);assert any(t['id']==cid and t['outcome']=='failed' and token in str(t['reason']) for t in child['cases']),w
     if x['kind']=='m':assert not token.startswith('WRONG_CODE')
    assert x['credited']==(x['kind']=='m')
 phases[name]={'rc':phase['rc'],'passed':r['passed'],'total':r['total'],'test_culture':culture,'counterexample_children':len(r.get('counterexample_evidence',[]))}
assert len(phases)==6 and children==52
out={'gate_status':'passed','head':H,'tree':M['tree'],'base':C,'archive_sha256':expected,'archive_bytes':size,'source_files_verified':count,'children_verified':children,'phases':phases,'operator_sha256':M['operator_sha256'],'source_path':str(D),'terminal_transport_note':'Actual operator terminal transport saved separately before review'}
(S/'windows-final-r10-evidence-index.json').write_text(json.dumps(out,indent=2)+'\n');(S/'windows-r10-projection.json').write_text(json.dumps({'sha':H,'os':'Windows','tests':projection},indent=2)+'\n');print(json.dumps(out,indent=2))
