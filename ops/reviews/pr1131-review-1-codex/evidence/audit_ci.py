from pathlib import Path
import sys,os,subprocess,json,ast,io,contextlib,yaml
S=Path(__file__).resolve().parent;R=S/'work/head';E=S/'evidence'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_GLOBAL=str(S/'audit.gitconfig'),GIT_CONFIG_NOSYSTEM='1',GIT_OPTIONAL_LOCKS='0')
sys.path.insert(0,str(R/'ops'));import ci_duong_nhanh as m;import ci_duong_nhanh_test as t
B='180039c4b791fba4c89991623151cbb7378fce53';H='0e824fe4c1ac674081c93c6f2098e5433c932890'
# Deliberately offline: build only a temporary merge object from the supplied base/head.
# This object is a local simulation, never described as github.sha.
tree=subprocess.check_output(['git','merge-tree','--write-tree','--no-messages',B,H],cwd=R).decode().strip()
env=dict(os.environ,GIT_AUTHOR_NAME='Offline review',GIT_AUTHOR_EMAIL='offline@example.invalid',GIT_COMMITTER_NAME='Offline review',GIT_COMMITTER_EMAIL='offline@example.invalid')
cp=subprocess.run(['git','-c','commit.gpgsign=false','commit-tree',tree,'-p',B,'-p',H],input=b'Offline synthetic merge for review1131\n',cwd=R,env=env,capture_output=True);assert cp.returncode==0,cp.stderr
merge=cp.stdout.decode().strip()
ci_env={m.BIEN_SU_KIEN:'pull_request',m.BIEN_GOC:B,m.BIEN_DAU:H,m.BIEN_MERGE:merge}
calls=[]
def real_run(argv,**kw):
 p=subprocess.run(argv,**kw)
 if '--check' in argv:calls.append(dict(argv=argv,rc=p.returncode,stdout=p.stdout.decode(errors='replace'),stderr=p.stderr.decode(errors='replace')))
 return p
classified=m.phan_loai(ci_env,chay=real_run,kho=R)
output=io.StringIO();rc=m.lenh_kiem_re(ci_env,chay=real_run,kho=R,ra=output)
(E/'ci-local-kiem-re.stdout').write_text(output.getvalue())
# Existing whitespace case: ordinary check must fail on its fixture; CI check must pass.
testout=io.StringIO()
with contextlib.redirect_stdout(testout),contextlib.redirect_stderr(testout):
 t.t20d_kiem_re_khoang_trang_cuoi_dong_khong_do()
(E/'ci-t20d.stdout').write_text(testout.getvalue())
# Enumerate exact --check call sites in executable Python sources (including tests), not prose/artifacts.
files=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
active=[p for p in files if p.endswith('.py') and p.startswith(('.claude/dev/','ops/','scripts/')) and not p.startswith(('ops/reviews/','ops/land/','ops/evidence/','ops/specs/'))]
call_sites=[];parse_failures=[]
for rel in active:
 content=(R/rel).read_text(encoding='utf-8-sig')
 if '--check' not in content:continue
 try:a=ast.parse(content)
 except SyntaxError as e:parse_failures.append(dict(path=rel,error=str(e)));continue
 for node in ast.walk(a):
  if not isinstance(node,ast.Call):continue
  strings=[x.value for x in ast.walk(node) if isinstance(x,ast.Constant) and isinstance(x.value,str)]
  if '--check' in strings and 'diff' in strings:
   # Shortest calls that directly carry the option (ignore enclosing calls with nested calls).
   if any(isinstance(child,ast.Call) and child is not node and any(isinstance(c,ast.Constant) and c.value=='--check' for c in ast.walk(child)) for child in ast.walk(node)):continue
   call_sites.append(dict(path=rel,line=node.lineno,code=ast.get_source_segment(content,node)))
workflow=yaml.safe_load((R/'.github/workflows/ci.yml').read_text())
steps=[dict(job=job,name=step.get('name'),condition=step.get('if'),run=step.get('run')) for job,d in workflow['jobs'].items() for step in d.get('steps',[]) if 'ci_duong_nhanh' in str(step.get('run','')) or 'diff --check' in str(step.get('run',''))]
report=dict(merge_kind='synthetic local only; actual GitHub merge ref KHÔNG ĐO ĐƯỢC',merge=merge,merge_tree=tree,head_tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=R).decode().strip(),classified=classified,kiem_re_rc=rc,kiem_re_output=output.getvalue(),diff_check_calls=calls,t20d='PASS',python_scan_files=len(active),parse_failures=parse_failures,exact_diff_check_call_sites=call_sites,workflow_steps=steps)
(E/'ci.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps({k:v for k,v in report.items() if k not in ('exact_diff_check_call_sites','workflow_steps')},ensure_ascii=False,indent=2))
print('exact diff --check call sites',[(x['path'],x['line']) for x in call_sites])
with (S/'VERDICT.md').open('a') as f:
 f.write(f'\nCI offline: `PYTHONDONTWRITEBYTECODE=1 python3 audit_ci.py`: classifier={classified}, lenh_kiem_re rc={rc}, t20d PASS; mô phỏng merge local cùng tree HEAD, KHÔNG phải merge ref GitHub đã đo. Call sites, argv thực, rc và workflow ở `evidence/ci.json`.\n')
