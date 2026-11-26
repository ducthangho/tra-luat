"""Thử bằng kho giả và dữ liệu bình thường; không tạo mã giả parser hay chuỗi tấn công."""
from pathlib import Path
import ast,os,sys,subprocess,shutil,json,py_compile,datetime
O=Path(__file__).resolve().parent
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'tmp'),GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='commit.gpgsign',GIT_CONFIG_VALUE_0='false')
sys.argv=['fx',str(O),str(O/'base/ops/lease_publish.py')]
s=(O/'sc/fx_tien_kiem.py').read_text(); tree=ast.parse(s); stop=next(n.lineno for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='KB' for t in n.targets))
h={};exec(compile('\n'.join(s.splitlines()[:stop-1]),'fixture_helpers','exec'),h)
h['FX']=O/'tmp/hunt';h['FX'].mkdir(exist_ok=True)
g=h['g']; build=h['dung']; lease=h['lease']; P=h['P1']; L=h['L']; A=h['A']; BN=h['BN']; env=h['ENV']; TK=O/'sc/tien_kiem.py'; rows=[]
def report(name,rc,out,extra=None):
 r=dict(name=name,rc=rc,output=out,extra=extra); rows.append(r); print(json.dumps(r,ensure_ascii=False),flush=True)
 (O/'hunt-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
def check(k,name,B='origin/master',sau=None,ev=None,script=TK,flags=()):
 cmd=[sys.executable,'-B',*flags,str(script),B]+(['--sau-dang',sau] if sau else [])
 r=subprocess.run(cmd,cwd=k,capture_output=True,text=True,env=ev or env)
 report(name,r.returncode,(r.stdout+r.stderr).strip());return r
def case(name,**kw):
 rc,out=build(name,**kw);report(name,rc,' | '.join(out));return h['FX']/name/'kho'
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
# 1. Cùng tên nhánh nhưng OID khác: T1 phải đỏ cả hai chiều.
def same_name_oid(k):
 old=g(k,'rev-parse','origin/master').strip()
 (k/'more.txt').write_text('ordinary data\n');g(k,'add','more.txt');g(k,'commit','-q','-m','advance published head');g(k,'push','-q','origin','master')
 g(k,'update-ref','refs/remotes/origin/master',old)
case('same_names_changed_oid',them=same_name_oid)
# 2. B cũ, lease đăng sau B trên master và trên nhánh mới vẫn phải được đọc.
def later_lease(k):
 old=g(k,'rev-parse','master').strip(); p=k/L/'later.yaml';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(lease(A,[P]))
 g(k,'add','-A');g(k,'commit','-q','-m','later lease');g(k,'push','-q','origin','master');g(k,'fetch','-q','origin');return old
k=case('ancestor_later_master_lease',them=later_lease)
def branch_after(k):
 old=g(k,'rev-parse','master').strip();h['dang_rieng'](k,ten=A);return old
case('ancestor_later_branch_lease',them=branch_after)
# Policy mới đã nằm trong V của khối, còn B là tổ tiên sạch.
saved={}
def later_policy(k):
 old=g(k,'rev-parse','master').strip();saved['old']=old
 p=k/'.github/coordination/change-impact.v1.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}\n')
 g(k,'add','-A');g(k,'commit','-q','-m','new canonical policy');g(k,'push','-q','origin','master');g(k,'fetch','-q','origin');return old
k=case('ancestor_later_policy',them=later_policy)
check(k,'latest_master_policy')
h['dang_rieng'](k);check(k,'ancestor_later_policy_after_publication',B=saved['old'],sau='wp1466-r6-g1-claude')
# 3. Worktree phụ và graft cục bộ không mang vào kho tạm.
def linked(k):
 h['nhanh_cuc_bo'](k);g(k,'worktree','add','-q',str(k.parent/'linked'),'nhap')
k=case('linked_private_retirement',nhanh=h['GIU_A'],them=linked)
check(k.parent/'linked','invoked_from_linked_worktree')
def graft(k):
 old=g(k,'rev-parse','master').strip();private=h['nhap'](k)
 (k/'.git/info/grafts').write_text(old+' '+private+'\n')
 rc=subprocess.run(['git','merge-base','--is-ancestor',private,old],cwd=k,env=env,capture_output=True).returncode
 report('graft_original_clone_ancestry',rc,'private commit becomes ancestor only in clone')
 return private
case('graft_private_B',them=graft)
# 4. Fail-closed: thiếu dữ liệu, YAML hỏng, hàm thiếu, không master, server rỗng.
case('yaml_unreadable',nhanh=[('ops/a',[(L+'a.yaml','[')])])
def missing_function(k):
 p=k/'ops/lease_publish.py'; s=p.read_text();p.write_text(s.replace('def _quet_lease_toan_kho(', 'def _quet_lease_toan_kho_unavailable(',1));g(k,'add','-A');g(k,'commit','-q','-m','published missing function');g(k,'push','-q','origin','master');g(k,'fetch','-q','origin')
case('missing_scanner_function',them=missing_function)
def absent_master(k):
 g(k,'push','-q','origin','master:refs/heads/main');g(k.parent/'origin.git','update-ref','-d','refs/heads/master');g(k,'fetch','-q','--prune','origin');return g(k,'rev-parse','HEAD').strip()
case('server_without_master',them=absent_master)
def no_heads(k):
 g(k.parent/'origin.git','update-ref','-d','refs/heads/master');g(k,'update-ref','-d','refs/remotes/origin/master')
case('server_empty',them=no_heads)
def remote_missing(k): g(k,'remote','set-url','origin',str(k.parent/'unavailable.git'))
case('server_unavailable',them=remote_missing)
# 5. Cấu hình/biến Git được công bố là tiền đề: kiểm các ảnh hưởng cơ bản, chỉ trên fixture.
k=case('env_clean',nhanh=h['GIU_A'])
for name,value in [('GIT_DIR',str(k/'.git')),('GIT_WORK_TREE',str(k)),('GIT_OBJECT_DIRECTORY',str(k/'.git/objects')),('GIT_NAMESPACE','review-probe')]:
 check(k,'env_'+name,ev=dict(env,**{name:value}))
# 6. Dependency Python: chỉ chép PyYAML chính hãng, không thay thuật toán hay tạo payload.
import yaml
k=case('python_dependencies_baseline',nhanh=h['GIU_A']);pkg=k/'yaml'
shutil.copytree(Path(yaml.__file__).parent,pkg,ignore=shutil.ignore_patterns('__pycache__'))
local_script=k/'preflight-review.py';shutil.copyfile(TK,local_script)
for label,sc,extra_env in [('external_script',TK,{}),('script_in_clone',local_script,{}),('external_script_pythonpath',TK,{'PYTHONPATH':str(k)})]:
 cmd=[sys.executable,'-B','-v',str(sc),'origin/master'];r=subprocess.run(cmd,cwd=k,env=dict(env,**extra_env),capture_output=True,text=True)
 (O/(label+'-trace.log')).write_text(r.stdout+r.stderr)
 imported=[x for x in r.stderr.splitlines() if str(pkg) in x and ('code object' in x or 'matches' in x)]
 report(label,r.returncode,r.stdout.strip(),dict(local_yaml_trace=imported[:4],yaml_tracked=g(k,'ls-files','yaml').strip(),command=cmd))
py_compile.compile(str(pkg/'__init__.py'),cfile=str(pkg/'__init__.pyc'),doraise=True);(pkg/'__init__.py').unlink()
r=subprocess.run([sys.executable,'-B','-v',str(local_script),'origin/master'],cwd=k,env=env,capture_output=True,text=True)
(O/'sourceless-pyc-trace.log').write_text(r.stdout+r.stderr)
report('script_in_clone_sourceless_pyc',r.returncode,r.stdout.strip(),[x for x in r.stderr.splitlines() if str(pkg/'__init__.pyc') in x])
