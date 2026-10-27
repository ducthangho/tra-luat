from pathlib import Path
import concurrent.futures,json,os,re,subprocess,yaml
from audit import BASE,OUT,SHA,record
copy=Path((OUT/'copy-path.txt').read_text()); env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
readme=copy/'ops/reviews/README.md'; receipt=copy/'ops/reviews/pr896-review-5-codex-verdict.receipt.yaml'
originals={readme:readme.read_bytes(),receipt:receipt.read_bytes()}
row_prefixes={'remove-round5-index':'| [`pr896-review-5-codex-verdict.md`]','remove-round5-caveat-readme':'| `pr896-review-5-codex-verdict.md` | `HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO` |'}
results=[]
def run(item):
 tag,case=item;cmd=['python3','ops/lease_publish_test.py','--chi-ca='+case+'_']
 p=subprocess.run(cmd,cwd=copy,env=env,capture_output=True,text=True)
 (OUT/(tag+'-'+case+'.log')).write_text(p.stdout+'\nSTDERR:\n'+p.stderr)
 return case,{'rc':p.returncode,'summary':next((l for l in p.stdout.splitlines() if l.startswith('lease_publish:')),None),'error':[l for l in p.stdout.splitlines() if any(w in l for w in ['KHÔNG','LỖI','FAIL','ĐỎ'])]}
for tag in [*row_prefixes,'remove-round5-receipt-caveat']:
 for p,b in originals.items():p.write_bytes(b)
 if tag in row_prefixes:
  lines=readme.read_text().splitlines(keepends=True);removed=[l for l in lines if l.startswith(row_prefixes[tag])];assert len(removed)==1
  readme.write_text(''.join(l for l in lines if not l.startswith(row_prefixes[tag])))
 else:
  node=yaml.compose(receipt.read_text());seq=next(v for k,v in node.value if k.value=='verdict_usage_caveats')
  item=next(n for n in seq.value if next(v.value for k,v in n.value if k.value=='id')=='HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO')
  # YAML marks start after '- '; remove entire sequence item, preserve rest byte for byte.
  lines=receipt.read_text().splitlines(keepends=True);start=item.start_mark.line;end=item.end_mark.line
  removed=lines[start:end];receipt.write_text(''.join(lines[:start]+lines[end:]))
  after=yaml.safe_load(receipt.read_text());assert len(after['verdict_usage_caveats'])==3
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:cases=dict(pool.map(run,[(tag,c) for c in ['t26','t27','t138']]))
 results.append({'mutation':tag,'removed_bytes':len(''.join(removed).encode()),'cases':cases})
 print(tag,json.dumps(cases,ensure_ascii=False),flush=True)
for p,b in originals.items():p.write_bytes(b)
status=subprocess.check_output(['git','-C',str(copy),'status','--porcelain=v1','--untracked-files=all']).decode();assert status=='',status
(OUT/'mutations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
output='clone='+str(copy)+'\ncheckout='+subprocess.check_output(['git','-C',str(copy),'rev-parse','HEAD']).decode().strip()+'\n'+json.dumps(results,ensure_ascii=False,indent=2)+'\nstatus_after_restore='+repr(status)
record(5,'Xoá hàng/caveat mới trên clone độc lập','git clone --no-hardlinks --no-checkout mirror.git <tmp>/copy; git -C <copy> checkout --detach '+SHA+'; python3 review_evidence/mutations.py',output,'KHÔNG PHẢI LỖI hiện hành; giới hạn răng được ghi theo từng ca, không suy cổng kiểm đủ ngữ nghĩa')
