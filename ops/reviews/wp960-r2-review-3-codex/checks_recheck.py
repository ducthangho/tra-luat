import hashlib,json,os,subprocess
from pathlib import Path
root=Path(__file__).resolve().parent/'cay-kho'
def run(*args):
 q=subprocess.run(args,cwd=root,text=True,capture_output=True,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1'})
 print(json.dumps({'command':list(args),'rc':q.returncode,'stdout':q.stdout,'stderr':q.stderr},ensure_ascii=False),flush=True)
for args in [('git','rev-parse','HEAD','HEAD^{tree}'),('git','status','--porcelain'),('git','diff','--check','44884446f71c89e25f9a72ac58e4f597db63c1ba','HEAD'),('git','diff','--name-only','2618eb4e59ab296e5dd8d2bc8543fe8e7e966b40','HEAD'),('git','diff','--numstat','44884446f71c89e25f9a72ac58e4f597db63c1ba','HEAD','--','ops/bien_nhan_v2.py','ops/bien_nhan_v2_test.py'),('rg','-n','"dung_tai"|def _moc_|def _commit_them_cau|def _co_cau','ops/bien_nhan_v2.py'),('python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.'),('git','--version'),('python3','--version')]:run(*args)
for rel in ('ops/bien_nhan_v2.py','ops/bien_nhan_v2_test.py','ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md'):
 data=(root/rel).read_bytes();committed=subprocess.run(['git','show','934a5b063670acfbed410487d8244cd17d586d6e:'+rel],cwd=root,capture_output=True,check=True).stdout
 print(json.dumps({'file':rel,'sha256':hashlib.sha256(data).hexdigest(),'byte_identical_to_reviewed_commit':data==committed}),flush=True)
for what in ('base','head'):
 data=json.loads((root.parent/'evidence-recheck'/('ruff-'+what+'.json')).read_text());print(json.dumps({'ruff':what,'diagnostics':[(Path(x['filename']).name,x['code'],x['location']) for x in data]}))
