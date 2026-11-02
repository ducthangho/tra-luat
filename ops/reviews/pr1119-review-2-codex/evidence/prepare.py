import hashlib, json, os, pathlib, shutil, subprocess
S=pathlib.Path(__file__).resolve().parent
os.environ['PYTHONDONTWRITEBYTECODE']='1'
os.environ['GIT_CONFIG_COUNT']='1'
os.environ['GIT_CONFIG_KEY_0']='core.abbrev'
os.environ['GIT_CONFIG_VALUE_0']='7'
os.environ['GIT_OPTIONAL_LOCKS']='0'
E=S/'evidence'; E.mkdir(exist_ok=True)
R=S/'cay-kho'
def snapshot(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file()}
def git(*args,root=R):
    return subprocess.check_output(['git',*args],cwd=root)
before=snapshot(R)
(E/'original-hashes.json').write_text(json.dumps(before,indent=2))
W=S/'work'; W.mkdir(exist_ok=True)
for name,rev in [('head','8715ac9f591b27d9b176e9d656437ef4b71b54dc'),('base','c82047da4d6f9546ce1d68282c37acf9567b74bc')]:
    dst=W/name
    if not dst.exists(): shutil.copytree(R,dst)
    subprocess.run(['git','config','core.abbrev','7'],cwd=dst,check=True)
    subprocess.run(['git','checkout','--detach',rev],cwd=dst,check=True,capture_output=True)
changed=git('diff','--name-only','c82047d','HEAD').decode().splitlines()
data={'head':git('rev-parse','HEAD').decode().strip(),'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'merge_base':git('merge-base','HEAD','origin/master').decode().strip(),'status':git('status','--porcelain=v1').decode(),'changed_count':len(changed),'out_of_scope':[p for p in changed if not p.startswith('ops/reviews/')],'input_diff_equal':git('diff','c82047d','HEAD')==(S/'DIFF.patch').read_bytes(),'round2_diff_equal':git('diff','a8f7470','HEAD','--','ops/reviews')==(S/'DIFF-OPS-REVIEWS-TU-LUOT1.patch').read_bytes(),'round2_changed':git('diff','--name-only','a8f7470','HEAD','--','ops/reviews').decode().splitlines(),'original_file_count':len(before)}
(E/'preflight.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)); print(json.dumps(data,ensure_ascii=False,indent=2))
with (S/'VERDICT.md').open('a') as f:f.write('\nPreflight — `PYTHONDONTWRITEBYTECODE=1 python3 prepare.py`: '+json.dumps(data,ensure_ascii=False)+'\n')
