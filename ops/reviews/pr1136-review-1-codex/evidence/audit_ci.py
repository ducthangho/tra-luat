from pathlib import Path
import subprocess,os,json,importlib.util,sys,ast
S=Path(__file__).resolve().parent;R=S/'work/head';E=S/'evidence';os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['GIT_CONFIG_GLOBAL']=str(S/'audit.gitconfig');os.environ['GIT_CONFIG_NOSYSTEM']='1';os.environ['GIT_OPTIONAL_LOCKS']='0';sys.path.insert(0,str(R/'ops'))
B='62e629156fd0729b743f15eed2f32487786b9adc';H='1a87a863174ef104b2df8bc98b77724fb6796d9b'
import ci_duong_nhanh as ci
calls=[]
def trace(cmd,**kw):
 r=subprocess.run(cmd,**kw)
 if '--check' in cmd:calls.append({'command':cmd,'rc':r.returncode,'stdout':str(r.stdout),'stderr':str(r.stderr)})
 return r
out={'base_function':ci.kiem_diff_check({ci.BIEN_SU_KIEN:'pull_request',ci.BIEN_GOC:B,ci.BIEN_DAU:B},trace,R),'head_function':ci.kiem_diff_check({ci.BIEN_SU_KIEN:'pull_request',ci.BIEN_GOC:B,ci.BIEN_DAU:H},trace,R)}
tree=subprocess.check_output(['git','merge-tree','--write-tree',B,H],cwd=R).decode().strip().splitlines()[0]
env=dict(os.environ,GIT_AUTHOR_NAME='Local audit',GIT_AUTHOR_EMAIL='audit@example.invalid',GIT_COMMITTER_NAME='Local audit',GIT_COMMITTER_EMAIL='audit@example.invalid')
merge=subprocess.check_output(['git','commit-tree',tree,'-p',B,'-p',H],cwd=R,input=b'Local audit simulated merge, not GitHub\n',env=env).decode().strip()
env.update({ci.BIEN_SU_KIEN:'pull_request',ci.BIEN_GOC:B,ci.BIEN_DAU:H,ci.BIEN_MERGE:merge})
import io
buf=io.StringIO();cl=ci.phan_loai_day_du(env,trace,R);out['classification']=[sorted(cl[0]) if cl[0] is not None else None,*cl[1:]];out['local_kiem_re_rc']=ci.lenh_kiem_re(env,trace,R,buf);out['local_kiem_re_stdout']=buf.getvalue();out['simulated_merge']=merge;out['merge_tree_matches_head']=tree==subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=R).decode().strip();out['check_calls']=calls
spec=importlib.util.spec_from_file_location('ci_tests',R/'ops/ci_duong_nhanh_test.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.t20d_kiem_re_khoang_trang_cuoi_dong_khong_do();out['t20d']='PASS'
paths=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0');active=[p for p in paths if p and not p.startswith(('ops/reviews/','ops/land/','ops/specs/','docs/','rasoat/'))]
rg=subprocess.run(['git','grep','-n','-e','--check','--',*active],cwd=R,capture_output=True);(E/'all-check-calls.txt').write_bytes(rg.stdout)
out['ast_scan_files']=0;out['ast_parse_errors']=[];out['diff_check_call_sites']=[]
for p in active:
 if not p.endswith('.py'):continue
 try:
  source=(R/p).read_text(encoding='utf-8-sig');a=ast.parse(source)
 except Exception as e:out['ast_parse_errors'].append([p,str(e)]);continue
 out['ast_scan_files']+=1
 for n in ast.walk(a):
  if not isinstance(n,ast.Call):continue
  strings=[x.value for x in ast.walk(n) if isinstance(x,ast.Constant) and isinstance(x.value,str)]
  if 'diff' in strings and '--check' in strings:
   out['diff_check_call_sites'].append({'path':p,'line':n.lineno,'expression':ast.get_source_segment(source,n)[:1200]})
(E/'ci.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='classification'},ensure_ascii=False,indent=2));print('classification',out['classification'][1:])
with (S/'VERDICT.md').open('a') as f:f.write('\nCI local — `python3 audit_ci.py`: kết quả đầy đủ tại evidence/ci.json; '+str({k:v for k,v in out.items() if k in ['base_function','head_function','local_kiem_re_rc','local_kiem_re_stdout','t20d','ast_scan_files','ast_parse_errors']})+'\n')
