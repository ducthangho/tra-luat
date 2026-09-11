import ast, hashlib, json, re, subprocess
from pathlib import Path
from collections import Counter
from datetime import datetime
import yaml
P=Path(__file__).resolve().parent; R=P.parent/'cay-kho'; G=P.parent

def git(*a):
 p=subprocess.run(['git','--no-optional-locks',*a],cwd=R,capture_output=True,check=True);return p.stdout.decode()
def save(n,x): (P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def h(b): return hashlib.sha256(b).hexdigest()
def snap():
 fs=git('ls-files','-z').split('\0');fs=[f for f in fs if f]
 return dict(head=git('rev-parse','HEAD').strip(),tree=git('rev-parse','HEAD^{tree}').strip(),status=git('status','--porcelain=v1'),shallow=git('rev-parse','--is-shallow-repository').strip(),branch=git('branch','--show-current').strip(),refs=git('for-each-ref','--format=%(refname) %(objectname)').splitlines(),tracked={f:h((R/f).read_bytes()) for f in fs})
if not (P/'tree-before.json').exists():save('tree-before.json',snap())
manifest=[]
for line in (G/'ARTIFACTS.sha256').read_text().splitlines():
 expected,path=line.split('  ',1);actual=h((G/path).read_bytes());manifest.append(dict(path=path,expected=expected,actual=actual,match=expected==actual))
save('manifest.json',manifest)
refs={}
for name in ['nguon-refs.tsv','mirror-refs.tsv','cay-kho-refs.tsv']:
 refs[name]=sorted((G/name).read_text().splitlines())
refs['actual_heads']=sorted(git('for-each-ref','--format=%(objectname)\t%(refname)','refs/heads').splitlines())
save('refs.json',refs)
receipts=[]
for i in range(1,6):
 path=f'ops/reviews/pr490-review-{i}-codex-verdict.receipt.yaml';s=(R/path).read_text();x=yaml.safe_load(s);v=(R/x['verdict_path']).read_bytes();vs=v.decode()
 headings=re.findall(r'^###\s+(\S+)\s+\[(P[123])\].*$',vs,re.M)
 first=git('log','--all','--diff-filter=A','--format=%H','--',x['verdict_path']).splitlines()
 sha=re.search(r'^reviewed_sha:\s*(\w+)',vs,re.M).group(1);result=re.search(r'^verdict:\s*(\w+)',vs,re.M).group(1)
 actual=dict(verdict_sha256=h(v),verdict_bytes=len(v),reviewed_sha=sha,verdict=result,evidence_url='https://github.com/ducthangho/tra-luat/blob/'+first[0]+'/'+x['verdict_path'],**{'so_'+sev.lower():sum(y[1]==sev for y in headings) for sev in ['P1','P2','P3']})
 checks=[dict(field=k,claimed=x[k],measured=a,match=x[k]==a) for k,a in actual.items()]
 identity=x['model_reviewer_identity'];duration=(datetime.fromisoformat(identity['ket_thuc_utc'])-datetime.fromisoformat(identity['bat_dau_utc'])).total_seconds()
 receipts.append(dict(file=path,checks=checks,headings=headings,first_add_commits=first,verdict_same_as_first_add=h(git('show',first[0]+':'+x['verdict_path']).encode())==h(v),identity=identity,duration_arithmetic=duration,duration_round3=round(duration,3),duration_round3_matches=round(duration,3)==identity['thoi_luong_giay'],source=identity['nguon_cac_scalar_tren'],numeric_leaves=[]))
 def walk(v,p):
  if isinstance(v,dict):
   for k,w in v.items():walk(w,p+'.'+str(k))
  elif isinstance(v,list):
   for k,w in enumerate(v):walk(w,p+f'[{k}]')
  elif isinstance(v,(int,float,bool)):receipts[-1]['numeric_leaves'].append(dict(path=p,value=v))
 walk(x,'$')
save('receipts.json',receipts)
# Full workflow steps, retaining shell commands and conditions, without YAML 1.1's on->bool.
w=yaml.load((R/'.github/workflows/ci.yml').read_text(),Loader=yaml.BaseLoader)
steps=w['jobs']['gate']['steps'];save('ci-steps.json',[dict(index=i+1,**s) for i,s in enumerate(steps)])
save('commit-messages.json',{sha:git('show','-s','--format=%H%n%B',sha) for sha in ['63c639a','f7872ac','c42fc74','dccce0a','b43d784','16663ca','13ba87d']})
rows=[s for s in (R/'ops/reviews/README.md').read_text().splitlines() if s.startswith('| [`pr490-review-')]
save('index-rows.json',rows)
# Numeric lexemes including prose, each with a precise line; IDs/versions stay distinct from counts.
num=[]
for path in ['ops/land/pr489-land-evidence.yaml']+[r['file'] for r in receipts]:
 for n,line in enumerate((R/path).read_text().splitlines(),1):
  if re.search(r'\d',line):num.append(dict(file=path,line=n,text=line))
save('numeric-inventory.json',num)
landpath='ops/land/pr489-land-evidence.yaml';save('copies.json',dict(land=(G/'BAN-DANG-REVIEW.yaml').read_bytes()==(R/landpath).read_bytes(),verdict5=(G/'VERDICT-luot5.md').read_bytes()==(R/'ops/reviews/pr490-review-5-codex-verdict.md').read_bytes(),ledger4=(G/'LEDGER-luot4.json').read_bytes()==(R/'ops/reviews/pr490-review-4-phep-do/claim-audit.json').read_bytes(),land_unchanged_since_5=git('diff','dccce0a..HEAD','--',landpath)==''))
print(json.dumps(dict(manifest=len(manifest),manifest_bad=sum(not m['match'] for m in manifest),receipt_fields=sum(len(x['checks']) for x in receipts),receipt_mismatches=[dict(file=x['file'],check=c) for x in receipts for c in x['checks'] if not c['match']],durations=[(x['duration_round3'],x['duration_round3_matches']) for x in receipts],steps=len(steps)),ensure_ascii=False))
