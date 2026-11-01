from pathlib import Path
import os,subprocess,json,re,yaml,hashlib,collections
S=Path(__file__).resolve().parent;R=S/'work/head';E=S/'evidence'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_GLOBAL=str(S/'audit.gitconfig'),GIT_CONFIG_NOSYSTEM='1',GIT_OPTIONAL_LOCKS='0')
checks=[];commands=[]
def sh(b):return hashlib.sha256(b).hexdigest()
def run(*a):
 p=subprocess.run(['git',*a],cwd=R,env=env,capture_output=True);commands.append(dict(cmd=['git',*a],rc=p.returncode,stdout=p.stdout.decode(errors='replace'),stderr=p.stderr.decode(errors='replace')));return p

def blob(rev,path):
 p=run('show',rev+':'+path);assert p.returncode==0;return p.stdout

def ck(name,a,e):checks.append(dict(name=name,actual=a,expected=e,ok=a==e))
old='a8f74709578f3c68833d366ed80b66fc10fbf0a3';new='8715ac9f591b27d9b176e9d656437ef4b71b54dc';fix='6379bc5d784eb9af103b79cc074e4766c0516ae5';B='180039c4b791fba4c89991623151cbb7378fce53'
ck('old_ancestor_fix',run('merge-base','--is-ancestor',old,fix).returncode,0);ck('fix_ancestor_new',run('merge-base','--is-ancestor',fix,new).returncode,0)
paths=run('diff-tree','--no-commit-id','--name-only','-r',fix).stdout.decode().splitlines()
ck('fix_five_paths',paths,sorted(['ops/reviews/README.md','ops/reviews/pr1114-review-1-codex-verdict.receipt.yaml','ops/reviews/pr1114-review-1-codex/OMITTED.txt','ops/reviews/pr1114-review-1-codex/SHA256SUMS','ops/reviews/pr1114-review-2-codex-verdict.receipt.yaml']))
for p in paths:ck('fix_retained_at_review2.'+p,sh(blob(fix,p)),sh(blob(new,p)))
closure=json.loads((S/'nguon/review1119c/evidence/closure.json').read_text())
omit_path='ops/reviews/pr1114-review-1-codex/OMITTED.txt';o=blob(old,omit_path).decode();f=blob(fix,omit_path).decode();n=blob(new,omit_path).decode()
for c in closure['cache']:
 rel=c['source'];ck('cache_old_missing.'+rel,rel not in o,True)
 match=re.search(r'^'+re.escape(rel)+r'\tsha256 ([0-9a-f]{64})\tbytes (\d+)\t',n,re.M)
 ck('cache_declared.'+rel,bool(match),True)
 if match:ck('cache_declaration_vs_run_evidence.'+rel,[match[1],int(match[2])],[c['sha256'],c['bytes']])
 # Raw cache not supplied, so cannot independently rehash these historic files.
 ck('cache_not_archived.'+rel,run('cat-file','-e',new+':ops/reviews/pr1114-review-1-codex/'+rel).returncode!=0,True)
for c in closure['diffs']:
 stem=c['stem'];rp='ops/reviews/'+stem+'-verdict.receipt.yaml';values={rev:yaml.safe_load(blob(rev,rp)) for rev in (old,fix,new)}
 vals={rev:next(x['mo_ta'] for x in values[rev]['verdict_usage_caveats'] if x['id']=='TEP-LON-KHONG-VAO-KHO') for rev in values}
 ck(stem+'.old_claim',vals[old],c['old_claim']);ck(stem+'.new_claim',vals[new],c['new_claim']);ck(stem+'.fix_claim',vals[fix],c['new_claim'])
 diff=blob(new,'ops/reviews/'+stem+'/DIFF.patch');ck(stem+'.diff_size',len(diff),c['bytes']);ck(stem+'.diff_sha',sh(diff),c['sha256'])
 rd=values[new];reconstructed=run('diff',rd['base_sha'],rd['reviewed_sha']).stdout;ck(stem+'.diff_reconstructed',diff==reconstructed,True)
 sums=blob(new,'ops/reviews/'+stem+'/SHA256SUMS').decode();ck(stem+'.manifest',sh(diff)+'  ./DIFF.patch' in sums,True)
 for rev in (fix,new):
  row=f"| `{stem}-verdict.md` | `TEP-LON-KHONG-VAO-KHO` | {vals[rev]} |";ck(stem+'.readme.'+rev,row in blob(rev,'ops/reviews/README.md').decode().splitlines(),True)
# Historic numbers in current receipt are a report of round2's verdict/evidence, not newly executed historical review.
src=S/'nguon/review1119c/evidence';b=json.loads((src/'bytes.json').read_text());r=json.loads((src/'receipts.json').read_text());m=json.loads((src/'readme.json').read_text())
ck('historic_copied_total',sum(x['copied'] for x in b['results']),237);ck('historic_omitted_total',sum(x['declared_correct'] for x in b['results']),13);ck('historic_byte_failures',b['failures'],[]);ck('historic_receipt_failures',r['failures'],[]);ck('historic_receipt_count',len(r['summary']),4);ck('historic_readme_added',m['added'],23);ck('historic_readme_removed',m['removed'],0)
# Current usage caveats: actual excluded diffs, >500k file, script path dependence, writable sandbox observation.
for n,letter in [(1,'b'),(2,'c')]:
 stem=f'pr1119-review-{n}-codex';root=R/'ops/reviews'/stem;d=yaml.safe_load((R/'ops/reviews'/f'{stem}-verdict.receipt.yaml').read_text());src=S/'nguon'/('review1119'+letter);run_data=json.loads((root/'run/run.json').read_text())
 ck(stem+'.DIFF_absent',not (root/'DIFF.patch').exists(),True)
 big=[]
 for p in src.rglob('*'):
  if p.is_file() and p.stat().st_size>500000:big.append(p.relative_to(src).as_posix())
 ck(stem+'.big_files_omitted',all(x in (root/'OMITTED.txt').read_text() for x in big),True)
 scripts=[p.relative_to(src).as_posix() for p in src.rglob('*') if p.is_file() and (p.suffix=='.py' or 'evidence' in p.relative_to(src).parts) and b'/tmp/' in p.read_bytes()];ck(stem+'.scripts_or_evidence_absolute_paths',bool(scripts),True)
 write_obs=any(['to_tien_workspace','write'] in x.get('permission_profile',{}).get('muc',[]) for x in run_data['sandbox_quan_sat']);ck(stem+'.checkout_writable_observation',write_obs,True)
 # Control terminal rc0 is separate from incomplete failed review; neither counted as an extra review.
 ck(stem+'.run_complete',run_data['trang_thai'],'xong')
master=run('merge-base','HEAD','origin/master').stdout.decode().strip();ck('candidate_merge_base_origin_master',master,B)
res=dict(check_count=len(checks),failures=[x for x in checks if not x['ok']],checks=checks,commands=commands,limitations=['Raw historic ruff-cache files under original review1114 sandbox are not supplied; their hash/bytes declarations are checked against recorded round2 evidence, not independently rehashed.', 'Run e9bd disk-full cause is recorded in stdout; actual historic disk/inode state cannot be rerun.', 'Git author/session trailers and receipt statements do not independently authenticate server-side provider/session/approval.'])
(E/'history.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print('checks',len(checks),'failures',res['failures'])
with (S/'VERDICT.md').open('a') as out:out.write(f'\nXử lý finding/lời khai lịch sử: `PYTHONDONTWRITEBYTECODE=1 python3 audit_history.py`: {len(checks)} đối chiếu, failures={res["failures"]}; neo 6379bc5, hai DIFF #1114 tái lập và README/caveat đều khớp. Chi tiết và giới hạn hiện vật nguồn trong `evidence/history.json`.\n')
