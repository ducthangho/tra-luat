from pathlib import Path
import os,sys,subprocess,ast,json,shutil,tempfile
O=Path(__file__).resolve().parent;os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'tmp'),GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='commit.gpgsign',GIT_CONFIG_VALUE_0='false')
sys.argv=['fx',str(O),str(O/'base/ops/lease_publish.py')]
s=(O/'sc/fx_tien_kiem.py').read_text();stop=next(n.lineno for n in ast.parse(s).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='KB' for t in n.targets));h={};exec(compile('\n'.join(s.splitlines()[:stop-1]),'fixture_helpers','exec'),h)
h['FX']=O/'tmp/followup';h['FX'].mkdir(exist_ok=True);g=h['g'];env=h['ENV'];TK=O/'sc/tien_kiem.py'
def run(k,label,B='origin/master',sau=None,flags=(),script=TK,env=env):
 cmd=[sys.executable,'-B',*flags,str(script),B]+(['--sau-dang',sau] if sau else []);r=subprocess.run(cmd,cwd=k,capture_output=True,text=True,env=env)
 print(label,'rc',r.returncode,r.stdout.strip().replace('\n',' | '),flush=True)
 if '-v' in flags:
  trace=[x for x in r.stderr.splitlines() if str(k/'yaml') in x and 'code object' in x];print(label,'LOCAL_DEPENDENCY',bool(trace),'TRACE',trace[:1],flush=True)
  (O/(label+'.log')).write_text(r.stdout+r.stderr)
 return r
for label,path in [('policy','.github/coordination/change-impact.v1.json'),('schema','.github/coordination/schemas/change-impact.v1.schema.json'),('irrelevant','notes.txt')]:
 rc,out=h['dung']('sequence_'+label);k=h['FX']/('sequence_'+label)/'kho';B=g(k,'rev-parse','origin/master').strip();print(label,'3A_BASE',B,'3D_INITIAL_RC',rc,out[-1],flush=True)
 h['dang_rieng'](k);run(k,label+'_3E_before_master_change',B,'wp1466-r6-g1-claude')
 p=k/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}\n');g(k,'add','-A');g(k,'commit','-q','-m','ordinary canonical change');g(k,'push','-q','origin','master');g(k,'fetch','-q','origin')
 server=set(g(k,'ls-remote','--heads','origin').splitlines());cache={oid+'\t'+ref.replace('refs/remotes/origin/','refs/heads/') for oid,ref in (line.split(' ',1) for line in g(k,'for-each-ref','--format=%(objectname) %(refname)','refs/remotes/origin').splitlines())};print(label,'PAIRS_EQUAL_BEFORE_3E',server==cache,flush=True)
 run(k,label+'_3E_old_B_after_master_change',B,'wp1466-r6-g1-claude');run(k,label+'_3E_current_master_after_master_change',sau='wp1466-r6-g1-claude')
# Dương/âm provenance import: không sửa mã PyYAML, chỉ thay vị trí script và chế độ cô lập.
import yaml
rc,out=h['dung']('imports_clean');k=h['FX']/'imports_clean/kho';shutil.copytree(Path(yaml.__file__).parent,k/'yaml',ignore=shutil.ignore_patterns('__pycache__'));p=k/'preflight-review.py';shutil.copyfile(TK,p)
run(k,'imports_clean_local_script',flags=('-v',),script=p)
run(k,'imports_clean_local_script_isolated',flags=('-I','-v'),script=p)
run(k,'imports_clean_external_pythonpath',flags=('-v',),env=dict(env,PYTHONPATH=str(k)))
run(k,'imports_clean_external_pythonpath_isolated',flags=('-I','-v'),env=dict(env,PYTHONPATH=str(k)))
# Alternates chỉ cung cấp object: object riêng có thể đọc, nhưng ref riêng không xuất hiện.
rc,out=h['dung']('alternates',nhanh=h['GIU_A'],them=h['nhanh_cuc_bo']);k=h['FX']/'alternates/kho';private=g(k,'rev-parse','nhap').strip()
with tempfile.TemporaryDirectory(dir=O/'tmp',prefix='refset-') as td:
 td=Path(td);g(k,'init','-q','--bare',str(td));(td/'objects/info/alternates').write_text(g(k,'rev-parse','--path-format=absolute','--git-path','objects'))
 refs=[]
 for line in g(k,'ls-remote','--heads','origin').splitlines():
  oid,ref=line.split('\t');ref=ref.replace('refs/heads/','refs/remotes/origin/');g(td,'update-ref',ref,oid);refs.append(ref)
 observed=g(td,'for-each-ref','--format=%(refname)').splitlines();print('ALTERNATES_REFSET_EXACT',set(observed)==set(refs),'REF_COUNT',len(observed),'PRIVATE_OBJECT_READABLE',g(td,'cat-file','-t',private).strip(),'PRIVATE_REF_VISIBLE',any('nhap' in x for x in observed),flush=True)
