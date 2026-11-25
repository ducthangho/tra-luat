import hashlib,json,os,subprocess,sys,platform,time
from pathlib import Path
W=Path(__file__).resolve().parent; R=W.parent/'repo'; M=W.parent/'ma_r9_git'
def sha(b):return hashlib.sha256(b).hexdigest()
def snap():
 d={}
 for root in [R,M]:
  f={}
  for p in root.rglob('*'):
   if '.git' in p.relative_to(root).parts:continue
   if p.is_symlink(): f[str(p.relative_to(root))]={'link':os.readlink(p)}
   elif p.is_file():f[str(p.relative_to(root))]={'sha256':sha(p.read_bytes()),'mode':p.stat().st_mode}
  git={}
  for args in [['rev-parse','HEAD','HEAD^{tree}'],['status','--porcelain=v1','--untracked-files=all','--ignored=matching'],['diff','--binary'],['diff','--cached','--binary'],['config','--get','core.abbrev']]:
   p=subprocess.run(['git','-C',str(root),*args],capture_output=True);git[' '.join(args)]={'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()}
  d[root.name]={'files':f,'git':git}
 return d
if __name__=='__main__':
 (W/'snapshot_before.json').write_text(json.dumps(snap(),ensure_ascii=False))
 p={'spec_sha256':sha((W.parent/'SPEC.md').read_bytes()),'vong':7,'reviewed_sha':subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD']).decode().strip(),'reviewed_tree':subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD^{tree}']).decode().strip(),'findings':[],'class_table':[],'prior_class_status':[],'bang_noi_slug':[],'hoi_tu':{'vong6_sang_7':'DANG_DO','lop_lap_lan_ba':[]},'da_do_khop':[],'verdict':'changes_requested','review_status':'in_progress'}
 (W/'VERDICT.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
 print('PREFLIGHT',p['spec_sha256'],p['reviewed_sha'],p['reviewed_tree'])
 print('ENV',platform.platform(),sys.version)
