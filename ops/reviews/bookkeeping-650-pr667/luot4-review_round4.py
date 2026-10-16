import pathlib, subprocess, json, hashlib, re, unicodedata
from run_checks import ROOT, OUT, ENV, run

def git(*args):
    p=subprocess.run(['git',*args],cwd=ROOT,env=ENV,check=True,capture_output=True)
    return p.stdout

def emit(k,v): print(k+'='+json.dumps(v,ensure_ascii=False))
landpath='ops/land/pr666-wp650-land-evidence.yaml'
errpath='ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a-r5.ERRATA.md'
landtext=(ROOT/landpath).read_text(); errtext=(ROOT/errpath).read_text()
import yaml
land=yaml.safe_load(landtext)
old_err=git('show','9a6f48f:'+errpath).decode()
emit('packet_status',land['trang_thai_packet'])
emit('K1_old_direct_claim','packet đã land' in old_err)
emit('K1_current_direct_claim','packet đã land' in errtext)
emit('K1_explicit_merged_not_landed','`merged`, CHƯA `landed`' in errtext)
emit('land_yaml_unchanged_since_r3',not git('diff','9a6f48f','HEAD','--',landpath))
emit('L1_current_sau_land', 'CHI duoc ghi sau land' in land['nang_tran'][0]['ghi_chu'])
emit('L1_already_at_r3', 'CHI duoc ghi sau land' in git('show','9a6f48f:'+landpath).decode())
emit('L1_already_at_r1', 'CHI duoc ghi sau land' in git('show','392199d:'+landpath).decode())
emit('H1_all_three_runs_and_four_anchors',all(x in ' '.join(land['trang_thai_packet']['dieu_kien_con_thieu_de_landed']) for x in ['36379712476','36387278453','36387278424','Run','Checkout','Workflow definition','Gate output']))
emit('A14_denies_pass','KHÔNG biến A14 của r5 thành đạt' in errtext)
emit('validator_named_debt',next(x for x in land['khong_do_duoc'] if 'LAND-EVIDENCE-VALIDATOR' in x))
emit('full_PR_paths',git('diff','--name-only','origin/master..HEAD').decode().splitlines())
emit('r3_delta_paths',git('diff','--name-only','9a6f48f..HEAD').decode().splitlines())
rows=[]
for rel in [landpath,errpath]:
    b=(ROOT/rel).read_bytes()
    emit('full_new_prose_read',{'path':rel,'lines':len(b.decode().splitlines()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'new_vs_base':not git('ls-tree','origin/master','--',rel)})
    for n,s in enumerate(b.decode().splitlines(),1):
        fold=''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c)).lower()
        if re.search(r'land|merge|complete|passed|success|xanh|dat|do duoc|do duoc|suy_ra|not_measured',fold): rows.append(f'{rel}:{n}: {s}')
(OUT/'claims-scan.txt').write_text('\n'.join(rows)+'\n')
emit('claims_scan_hits',len(rows))
print('L1_EXACT_EXCERPT')
for start,end in [(27,42),(198,210),(222,226)]:
    for n,s in enumerate(landtext.splitlines(),1):
        if start<=n<=end: print(f'{landpath}:{n}: {s}')
print('K1_CURRENT_EXCERPT')
for n,s in enumerate(errtext.splitlines(),1): print(f'{errpath}:{n}: {s}')
for n in [1,2,3]:
    p=ROOT/f'ops/reviews/bookkeeping-650-pr667/luot{n}-verdict-day-du.md'; q=pathlib.Path(f'/tmp/review667-r{n}-output/VERDICT.md')
    emit('verdict_original',{'round':n,'same_bytes':p.read_bytes()==q.read_bytes(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
attrs=[f'ops/reviews/bookkeeping-650-pr667/luot{n}-verdict-day-du.md' for n in [1,2,3]]+['ops/reviews/bookkeeping-650-pr667/luot3-VERDICT.md','ops/reviews/bookkeeping-650-pr667/luot1-audit_facts.py','ops/reviews/bookkeeping-650-pr667/luot2-input-github-readback.json','ops/reviews/bookkeeping-650-pr667/probe.yaml',landpath,errpath,'ops/reviews/other/luot1-verdict-day-du.md']
p=run('attributes',['git','check-attr','whitespace','text','eol','--',*attrs]); print(p.stdout.decode(),end='')
