"""Offline measurements on real fixtures; not an implementation of L8/D2b."""
import ast, collections, contextlib, copy, hashlib, importlib.util, io, json, os, pathlib, re, shutil, subprocess, sys, tarfile
import yaml
R=pathlib.Path.cwd(); W=R.parent/'work'; S=R/'ops/reviews/wp1236-r9-soan'
sys.dont_write_bytecode=True
sys.path[:0]=[str(S),str(R/'ops')]
import thamchieu as t
import kiem_ho_so_land as kh
import land_evidence_nguon as le
ns={'__file__':str(S/'do_loi_khai.py')}
exec(compile((S/'do_loi_khai.py').read_text().split('root = Path(sys.argv[1]);')[0],str(S/'do_loi_khai.py'),'exec'),ns)
out={}
def git(*args):
 p=subprocess.run(['git',*args],capture_output=True); return {'command':['git',*args],'rc':p.returncode,'out':p.stdout.decode(errors='replace'),'err':p.stderr.decode(errors='replace')}
def mod(src):
 d={'__name__':'scratch_reference','__file__':str(S/'thamchieu.py')}; exec(compile(src,'scratch_reference','exec'),d); return d
src=(S/'thamchieu.py').read_text()
fixtures={
 'v3':('pr1440-wp1319-provenance','danh-gia-gate-output-44669622916.txt'),
 'v2':('pr1453-wp433-provenance','hau-due-66eae51/danh-gia-gate-output-44717155521.txt'),
 'v1':('pr1231-wp1105-provenance','danh-gia-gate-output-42032872356.txt'),
 'fail':('pr1453-wp433-provenance','danh-gia-gate-output-44711337223.txt'),
 'skip':('pr1344-wp1343-provenance','danh-gia-gate-output-43969906464.txt'),
 'no_prov':('pr1130-wp1122-provenance','danh-gia-gate-output-41365578430.txt')}
def fixture(key,tag):
 d,f=fixtures[key]; dest=W/'fixtures'/tag
 if dest.exists(): shutil.rmtree(dest)
 shutil.copytree(R/'ops/land'/d,dest)
 return dest/f,dest
out['fixtures']={k:t.kiem_tep(R/'ops/land'/d/f,R/'ops/land'/d) for k,(d,f) in fixtures.items()}
p,d=fixture('v3','parser'); b=p.read_bytes(); txt=b.decode(); lines=txt.splitlines()
variants={'lf':b,'crlf':b.replace(b'\n',b'\r\n'),'mixed':b.replace(b'\n',b'\r\n',2),'cr_le':b.replace(b' -> passed: ',b' -> passed: \r',1)}
m45=mod(src.replace('if any("\\r" in d for d in dong): return None, ["cr_le"]','if False: return None, ["cr_le"]'))
m46=mod(src.replace('if not all(d.endswith("\\r") for d in dong): return None, ["xuong_dong_tron"]','if False: return None, ["xuong_dong_tron"]').replace('dong = [d[:-1] for d in dong]','dong = [d[:-1] if d.endswith("\\r") else d for d in dong]'))
out['parser_ab']={}
for k,bb in variants.items():
 p.write_bytes(bb); out['parser_ab'][k]={'base':t.kiem_tep(p,d),'m45':m45['kiem_tep'](p,d),'m46':m46['kiem_tep'](p,d)}
p.write_bytes(b)
# Duplicate provenance row: the contract requires an explicit duplicate-ID rejection.
prov_path,prov=t.tim_prov(d)[0]; orig=copy.deepcopy(prov)
prov['moc']['gate_output']['jobs'].append(copy.deepcopy(prov['moc']['gate_output']['jobs'][0]))
prov_path.write_text(yaml.safe_dump(prov,sort_keys=False,allow_unicode=True))
out['duplicate_provenance']={'reference':t.kiem_tep(p,d),'duplicate_ids':[k for k,n in collections.Counter(j['job_id'] for j in prov['moc']['gate_output']['jobs']).items() if n>1],'spec_required':'not_measured/job_id_trung_provenance'}
# All four K3 controls from the revised spec.
out['k3']={}
for tag in ('run','tap','checkout','empty'):
 v=copy.deepcopy(orig)
 if tag=='run': v['moc']['run']['trang_thai']='not_measured'
 if tag=='tap': v['moc']['gate_output']['tap_jobs']['trang_thai']='failed'
 if tag=='checkout': v['moc']['checkout'][0]['trang_thai']='not_measured'
 if tag=='empty': v['moc']['checkout']=[]
 prov_path.write_text(yaml.safe_dump(v,sort_keys=False,allow_unicode=True)); out['k3'][tag]=t.kiem_tep(p,d)
prov_path.write_text(yaml.safe_dump(orig,sort_keys=False,allow_unicode=True))
# Duplicate skipped row: repeated ID is lost by reference's dict assignment.
ps,ds=fixture('skip','duplicate_skip'); bs=ps.read_bytes(); sl=next(x for x in bs.splitlines() if b': skipped ' in x)
ps.write_bytes(bs+sl+b'\n'); parsed,errs=t.doc_danh_gia(ps)
out['duplicate_skip']={'reference_parse_reasons':errs,'reference_result':t.kiem_tep(ps,ds),'spec_required':'job_lap','skip_id':sl.decode().split()[1]}
# Flip the failure only in a copy of the genuine T-fail fixture.
pf,df=fixture('fail','conclusion'); raw=pf.read_bytes(); pf.write_bytes(raw.replace(b'-> failed: conclusion=failure',b'-> passed: x').replace(b'MOC_GATE_OUTPUT: failed (38/39',b'MOC_GATE_OUTPUT: passed (39/39'))
out['conclusion_control']=t.kiem_tep(pf,df)
# Independent per-file landed parity plus claim-token denominator.
rows=[]; pairs=set(); wrong=[]
for f in sorted((R/'ops/land').glob('*-land-evidence.yaml')):
 doc=yaml.safe_load(f.read_bytes()); expected=kh._xet_mot_tep(f,yaml)[2]; actual=ns['la_landed'](doc)
 rows.append((f.name,expected,actual))
 parent=f.parent/(f.name[:-len('-land-evidence.yaml')]+'-provenance')
 for path,value in ns['loi_khai'](doc):
  if isinstance(value,str):
   for token in ns['RE_DG'].findall(value): pairs.add((f.name,token))
for name,token in sorted(pairs):
 parent=R/'ops/land'/(name[:-len('-land-evidence.yaml')]+'-provenance')
 if not (parent/token).is_file(): wrong.append((name,token))
out['landed_parity']={'total':len(rows),'expected_true':sum(e for _,e,a in rows),'actual_true':sum(a for _,e,a in rows),'mismatches':[r for r in rows if r[1]!=r[2]]}
out['claim_tokens']={'distinct_record_token_pairs':len(pairs),'resolves':len(pairs)-len(wrong),'wrong':wrong}
# Existing cutover bytes and source gate.
f=R/'ops/land/pr680-wp676-land-evidence.yaml'
out['cutover']={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'constant':le.MIEN_TRU_CUTOVER[f.name]}
cp=subprocess.run([sys.executable,'-B','ops/land_evidence_nguon.py','--root',str(R),'--tep',str(f)],capture_output=True,text=True)
out['cutover']['gate']={'rc':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr}
# Mutant inventory and ADR land anchors.
spec=(R.parent/'SPEC.md').read_text(); part=spec.split('### Đợt A —')[1].split('### Đợt B —')[0]
ids=re.findall(r'\bm(\d+)\b',part); ids=[int(x) for x in ids]
ids += list(range(29,35))  # m28–m35 written as one interval
out['inventory']={'a_cases':len(re.findall(r'^\| A[12]-\d+ ',part,re.M)),'a_mutants':sorted(ids),'duplicates':[k for k,n in collections.Counter(ids).items() if n>1]}
first=set(subprocess.run(['git','rev-list','--first-parent','refs/remotes/origin/master'],capture_output=True,text=True,check=True).stdout.split())
out['adrs']={}
for n,h in [('0053','8ab100793df9831505f495543a74044b91c2c9ab'),('0055','d2e3052d479d140b7e7b91df41ec4914fab7d544')]:
 path=str(next((R/'docs/adr').glob(n+'*')).relative_to(R)); out['adrs'][n]={'present':git('cat-file','-e',h+':'+path),'parent_absent':git('cat-file','-e',h+'^1:'+path),'on_supplied_first_parent':h in first}
# Bytes actually read through Git archive, not worktree path normalization.
a=subprocess.run(['git','archive','176feba','ops/land/pr1440-wp1319-provenance'],capture_output=True,check=True); ad=W/'archive'; ad.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(a.stdout)) as tf: tf.extractall(ad,filter='data')
ap=ad/'ops/land'/fixtures['v3'][0]/fixtures['v3'][1]
out['archive']={'rc':0,'byte_match':ap.read_bytes()==(R/'ops/land'/fixtures['v3'][0]/fixtures['v3'][1]).read_bytes(),'result':t.kiem_tep(ap,ap.parent)}
# Literal C5(c) regex revisions and passed-only attempt guard.
pat=r'ops/land/[^/]+-provenance/(?:[^/]+/)*danh-gia-gate-output-\d+\.txt'; c1='ops/land/'+fixtures['v3'][0]+'/'+fixtures['v3'][1]; c5=c1.replace('ops/land/','ops/khac/',1)
out['c5_regex']={'base':[bool(re.fullmatch(pat,p)) for p in [c1,c5]],'literal_old_mutant':[bool(re.fullmatch(pat.removeprefix('ops/land/'),p)) for p in [c1,c5]],'revised_mutant':[bool(re.fullmatch(pat.replace('ops/land/','ops/[^/]+/'),p)) for p in [c1,c5]]}
out['attempt_types']={repr(x):type(x) is int and x>=1 for x in [1,2,None,True,1.0,0]}
out['scope']='Reference/fixtures and literal specification predicates only; no r9 production module or future L8/D2b CLI executed.'
(W/'audit_r4.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['adrs','inventory']},ensure_ascii=False,indent=2))
print('AUDIT_R4_COMPLETE')
