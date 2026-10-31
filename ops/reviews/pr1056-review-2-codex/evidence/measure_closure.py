from pathlib import Path
import subprocess,importlib.util,sys,yaml
base=Path(__file__).resolve().parent.parent
r=base/'cay-kho'; c=base/'review-copy'
def run(cmd,folder=c):
 p=subprocess.run(cmd,cwd=folder,capture_output=True,text=True); print('$',' '.join(cmd),'rc',p.returncode); print(p.stdout or '(empty)');print(p.stderr or '',end='');return p
run(['git','checkout','--force','--detach','1aae17b5534f78767856f93f7d6089adda224f21'])
run(['patch','--dry-run','--fuzz=0','-p0','-i',str(base/'verdict-cu/luot1-HINT.patch')])
run(['patch','--fuzz=0','-p0','-i',str(base/'verdict-cu/luot1-HINT.patch')])
run(['git','diff','--exit-code','047eaa4d26a5bb1e702199c870f42480aebed673','--'])
run(['git','checkout','--force','--detach','047eaa4d26a5bb1e702199c870f42480aebed673'])
spec=importlib.util.spec_from_file_location('lp',r/'ops/lease_publish.py');m=importlib.util.module_from_spec(spec);sys.modules['lp']=m;spec.loader.exec_module(m)
for n,oid in [(1,'c24875d00e93e6a98e0a0abd0837e0cbcad65d4d'),(2,'f37b5195978f1fe35b9cb55b6f79a2e09d165af0')]:
 paths=subprocess.check_output(['git','diff','--name-only','b29da0b',oid],cwd=r,text=True).splitlines()
 rec=yaml.safe_load((r/f'ops/reviews/pr1050-review-{n}-codex-verdict.receipt.yaml').read_text())
 print('ROUND',n,'DIFF_PATH_COUNT',len(paths),'OUTSIDE', [p for p in paths if not p.startswith(('ops/reviews/','ops/land/'))], 'CLASSIFIER',m._tinh_lop_tu_write_set(paths),'DECLARED',rec['review_class'],'EFFECTIVE',rec['effective_review_class'])
 print('CHANGED_KEYS', [k for k in rec if yaml.safe_load(subprocess.check_output(['git','show',f'1aae17b:ops/reviews/pr1050-review-{n}-codex-verdict.receipt.yaml'],cwd=r)).get(k)!=rec[k]])
run(['git','diff','--exit-code'],folder=c)
