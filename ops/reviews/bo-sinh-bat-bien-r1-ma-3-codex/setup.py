from pathlib import Path
import subprocess, json, hashlib, sys, platform, unicodedata
w=Path(__file__).resolve().parent;r=w.parent/'repo'
def git(*a):
 p=subprocess.run(['git','-C',str(r),*a],capture_output=True,text=True);return {'command':list(a),'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
snapshot={k:git(*a) for k,a in {'head':['rev-parse','HEAD','HEAD^{tree}'],'status':['status','--porcelain=v1','--untracked-files=all','--ignored=matching'],'diff':['diff','--binary'],'index':['diff','--cached','--binary'],'numstat':['diff','--numstat','a89c83a','HEAD'],'check':['diff','--check','a89c83a','HEAD']}.items()}
snapshot['runtime']={'python':sys.version,'os':platform.platform(),'unicode':unicodedata.unidata_version,'tmp_git_exists':Path('/tmp/.git').exists()}
(w/'snapshot-before.json').write_text(json.dumps(snapshot,indent=2))
for v,sha in [('base','a89c83acf998008caecba9084a7d295845bf1976'),('head','485387fb1e0e6e49837623ba9df7843d5dca782f')]:
 d=w/v
 subprocess.run(['git','clone','-q','--no-hardlinks',str(r),str(d)],check=True)
 subprocess.run(['git','-C',str(d),'checkout','-q','--detach',sha],check=True)
 for k,x in [('core.abbrev','7'),('core.autocrlf','false'),('core.eol','lf')]:subprocess.run(['git','-C',str(d),'config',k,x],check=True)
verdict={'reviewed_sha':'485387fb1e0e6e49837623ba9df7843d5dca782f','reviewed_tree':'dd18e43c2781f3ec0d227832083c5f46d40a14cd','base_sha':'a89c83acf998008caecba9084a7d295845bf1976','spec_sha256':hashlib.sha256((w.parent/'SPEC.md').read_bytes()).hexdigest(),'vong':3,'findings':[],'class_table':[],'prior_class_status':[{'slug':'nghiem-thu-khong-co-lap-chot-dich','status':'KHONG_DO_DUOC','evidence':'Review đang chạy; chưa kết luận.'}],'verdict':'in_progress','not_run':[],'limits':[]}
(w/'VERDICT.json').write_text(json.dumps(verdict,ensure_ascii=False,indent=2))
(w/'VERDICT.md').write_text('# Review lượt 3 — đang đo\n\nHEAD 485387fb1e0e6e49837623ba9df7843d5dca782f. Chưa có kết luận.\n')
print(json.dumps(snapshot,ensure_ascii=False))
