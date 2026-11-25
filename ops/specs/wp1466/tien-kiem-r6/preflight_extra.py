from pathlib import Path
import ast,sys,subprocess,os,json
O=Path(__file__).resolve().parent;os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='commit.gpgsign',GIT_CONFIG_VALUE_0='false')
sys.argv=['fx',str(O),str(O/'base/ops/lease_publish.py')]
s=(O/'sc/fx_tien_kiem.py').read_text();tree=ast.parse(s);stop=next(n.lineno for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='KB' for t in n.targets));g={};exec(compile('\n'.join(s.splitlines()[:stop-1]),'fixture_helpers','exec'),g)
lease=g['lease'];build=g['dung'];git=g['g'];P=g['P1'];L=g['L'];FX=g['FX'];old='fxa-r1-g1-claude';new='fxb-r1-g1-claude'
def check(k,tag,sau=None):
 cmd=[sys.executable,'-B',str(O/'sc/tien_kiem.py'),'origin/master']+(['--sau-dang',sau] if sau else []);r=subprocess.run(cmd,cwd=k,capture_output=True,text=True,env=g['ENV']);print(tag,'rc',r.returncode,(r.stdout+r.stderr).strip().replace('\n',' | '));return r.returncode
for typ in ['local_head','other_remote']:
 name='extra_'+typ
 rc,out=build(name,nhanh=[('ops/a',[(L+'a.yaml',lease(old,[P],da_bi_thay_the=new))])]);k=FX/name/'kho';print(typ,'SERVER_ONLY_BEFORE',rc,out[-1]);assert rc!=0
 git(k,'checkout','-q','-b','draft-retirement','master');p=k/L/'b.yaml';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(lease(new,['ops/khac.py'],thay_the_cho=[old]))
 git(k,'add',L+'b.yaml');git(k,'commit','-q','-m','private unpublished retirement draft');oid=git(k,'rev-parse','HEAD').strip();git(k,'checkout','-q','master')
 if typ=='other_remote':
  git(k,'update-ref','refs/remotes/backup/draft-retirement',oid);git(k,'branch','-D','draft-retirement')
 mc=git(k,'ls-remote','--heads','origin');print(typ,'PRIVATE_SHA_ON_SERVER',oid in mc)
 r=subprocess.run([sys.executable,'-B',str(k/'ops/lease_publish.py'),'ai-dang-giu',P,'--root','.'],cwd=k,capture_output=True,text=True,env=g['ENV']);print(typ,'STEP_3C',r.returncode,(r.stdout+r.stderr).strip().splitlines()[-1])
 check(k,typ+'_STEP_3D')
 # Publish a second lease only to this private fake origin, then exercise step 3e.
 own='wp1466-r5-g1-claude';git(k,'checkout','-q','-b','ops/w','master')
 p=k/L/'w.yaml';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(lease(own,[P]));git(k,'add',L+'w.yaml');git(k,'commit','-q','-m','fixture own lease');git(k,'push','-q','origin','ops/w');git(k,'checkout','-q','master');git(k,'branch','-D','ops/w')
 check(k,typ+'_STEP_3E',own)
 # Remove only the private fixture ref, leaving remote and every server lease unchanged.
 git(k,'update-ref','-d','refs/heads/draft-retirement' if typ=='local_head' else 'refs/remotes/backup/draft-retirement')
 check(k,typ+'_AFTER_REMOVING_PRIVATE_REF',own)
# Fail-closed checks beyond declared 19: invalid date and empty server advertisement.
for name,kw in [('invalid_expiry',dict(nhanh=[('ops/a',[(L+'a.yaml',lease(old,[P],han='unknown'))])])),('empty_write_set',dict(nhanh=[('ops/a',[(L+'a.yaml',lease(old,[]))])]))]:
 rc,out=build('extra_'+name,**kw);print(name,'rc',rc,' | '.join(out))
