from pathlib import Path
import os,sys,subprocess,json,re,hashlib,datetime,ast,types,collections
O=Path(__file__).resolve().parent;S=O.parent/'cay-kho';M=O.parent/'kho.git';P=O/'prototype'; B='48d372e14f190dae83a75ccbca8ee9a0b25635c5'; H='3c89d87fffbc06a59ad276bb3171e43ef89c2768'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'tmp'),GIT_OPTIONAL_LOCKS='0')
def git(repo,*args):
 r=subprocess.run(['git','-C',str(repo),*args],capture_output=True)
 if r.returncode: raise RuntimeError((args,r.returncode,r.stderr[:500]))
 return r.stdout
def sha(b):return hashlib.sha256(b).hexdigest()
sp=(S/'ops/specs/wp1466.md').read_bytes(); old=git(S,'show','6c4ffe9:ops/specs/wp1466.md');text=sp.decode()
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat())
print('VERSIONS',sys.version.split()[0],git(S,'--version').decode().strip(),'core.abbrev',git(S,'config','core.abbrev').decode().strip())
print('HEAD_TREE',git(S,'rev-parse','HEAD','HEAD^{tree}').decode().splitlines())
print('SPEC',sha(sp),'LINES',len(sp.splitlines()),'BLOB_EQUAL',sp==git(S,'show',H+':ops/specs/wp1466.md'))
prev=(S/'ops/specs/wp1466/review/r6-l6/VERDICT.md').read_bytes();print('PRIOR_VERDICT_SHA256',sha(prev))
blocks=lambda b:dict(re.findall(rb'^~~~ (\S+)\n(.*?)\n~~~$',b,re.S|re.M))
oldblocks,newblocks=blocks(old),blocks(sp)
print('BLOCKS',len(newblocks),'CHANGED',[k.decode() for k in newblocks if newblocks[k]!=oldblocks.get(k)])
for key in newblocks:
 print('BLOCK',key.decode(),'NONEMPTY',sum(bool(x.strip()) for x in newblocks[key].splitlines()),'BYTES_EQUALS_R5',newblocks[key]==oldblocks.get(key))
# Toàn mục 2/4–17 giữ nguyên, ngoài S16 mới và các đoạn tiền kiểm.
for n in [2,*range(4,18)]:
 pat=rb'^## '+str(n).encode()+rb'\. .*?(?=^## '+str(n+1).encode()+rb'\.)'
 a=re.search(pat,old,re.S|re.M);b=re.search(pat,sp,re.S|re.M)
 print('SECTION_UNCHANGED',n,bool(a and b and a.group()==b.group()))
patch=(S/'ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch').read_bytes()
print('PATCH',sha(patch),'LINES',len(patch.splitlines()),'R5_EQUALS',patch==git(S,'show','05d12f1:ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch'))
for bundle in ['tien-kiem-r7','nguyen-mau-r5']:
 d=S/'ops/specs/wp1466'/bundle;lines=(d/'SHA256SUMS').read_text().splitlines();ans=[]
 for line in lines:
  h,f=line.split(maxsplit=1);p=d/f.removeprefix('*');ans.append((f,p.exists() and sha(p.read_bytes())==h))
 print('CHECKSUMS',bundle,len(ans),sum(x[1] for x in ans),'FAILED',[x for x in ans if not x[1]])
master=git(S,'rev-parse','origin/master').decode().strip();print('MASTER',master)
changed=git(S,'diff','--name-only',B,master).decode().splitlines()
measured=['ops/lease_publish.py','.claude/dev/packet_loop.py','.claude/dev/launcher.py','.claude/dev/gate_lifecycle.py','.github/workflows/ci.yml','.github/workflows/ops-publish-lease.yml','docs/PROTOCOL_DA_PHIEN.md','.claude/dev/packet_loop_test.py','.claude/dev/packet_loop_test_manh.py','ops/ci_duong_nhanh.py']
print('DRIFT_BASE',git(S,'rev-list','--count',B+'..'+master).decode().strip(),'COMMITS',len(changed),'PATHS','MEASURED',[p for p in changed if p in measured or p.startswith(('docs/adr/','.githooks/'))])
print('DRIFT_R5_MASTER',git(S,'diff','--name-only','5a152c1',master).decode().splitlines())
for adr,oid,path in [('0053','8ab100793df9831505f495543a74044b91c2c9ab','0053-tran-kich-thuoc-sensitive-len-sau-tep.md'),('0055','d2e3052d479d140b7e7b91df41ec4914fab7d544','0055-tran-loi-goi-codex-len-muoi.md')]:
 rc=[subprocess.run(['git','-C',str(S),'cat-file','-e',o+':docs/adr/'+path],capture_output=True).returncode for o in [oid,oid+'^1']]
 print('OPT_IN',adr,'MATCH_LINES',sum(1 for line in text.splitlines() if line.endswith('ADR-'+adr+'@'+oid)),'RC',rc,'FIRST_PARENT',oid in git(S,'rev-list','--first-parent',master).decode().splitlines())
print('NO_0052',not bool(re.search(r'^tran_loi_goi_codex: ADR-0052@',text,re.M)),'SHALLOW',git(S,'rev-parse','--is-shallow-repository').decode().strip(),'CALLS_ASSIGNED','8/10')
stat=git(P,'diff','--numstat').decode().splitlines();plus=minus=0
for line in stat:
 a,b,p=line.split('\t');plus+=int(a);minus+=int(b);print('NUMSTAT',line)
# git apply tạo ADR untracked; cộng riêng theo đúng tập 4 tệp.
adrpath='docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md';adrlines=len((P/adrpath).read_bytes().splitlines());plus+=adrlines
print('ADR_NEW',adrlines,'TOTAL',plus,minus,'FILES',len(stat)+1,'HEADROOM',450-plus,'DIFF_CHECK_RC',subprocess.run(['git','-C',str(P),'diff','--check'],capture_output=True).returncode)
for name in ['base','prototype','master']:
 adr=list((O/name/'docs/adr').glob('[0-9][0-9][0-9][0-9]-*.md'));print('ADR_COUNT',name,len(adr),'MAX',max(p.name[:4] for p in adr))
refs=git(S,'for-each-ref','--format=%(objectname) %(refname)','refs/remotes/origin').decode().splitlines(); refs=[x.split(' ',1) for x in refs if not x.endswith('refs/remotes/origin/HEAD')]
print('BRANCH_REFS',len(refs));candidates=[]
for oid,ref in refs:
 files=git(S,'ls-tree','-r','--name-only',oid,'--','docs/adr').decode().splitlines()
 found=[p for p in files if re.search(r'/\d{4}-.*\.md$',p) and int(p.split('/')[-1][:4])>=68]
 if found:candidates.append((ref,found))
print('ADR_COMPETING_REFS',len(candidates),candidates[:2])
receipts=[p for p in git(S,'ls-tree','-r','--name-only',master,'--','ops/reviews').decode().splitlines() if p.endswith('.receipt.yaml')]
print('RECEIPTS',len(receipts),'WITH_BANG_LOP',sum(b'bang_lop' in git(S,'show',master+':'+p) for p in receipts))
lp=types.ModuleType('lease_publish');sys.modules['lease_publish']=lp
exec(compile(git(S,'show',master+':ops/lease_publish.py'),master+':ops/lease_publish.py','exec'),lp.__dict__)
lease_data=lp._quet_lease_toan_kho(O/'master',chan_nhanh_tut_sau=True)
for tm in ['2026-11-21T04:57:23+00:00',datetime.datetime.now(datetime.timezone.utc).isoformat()]:
 now=datetime.datetime.fromisoformat(tm);live=[x for x in lease_data if lp._phan_loai_lease(x['lease'],now)=='CÒN_HẠN'];retired=[x for x in live if lp._bia_mo_doi_xung(x['lease'],lease_data) is True];active=[x for x in live if x not in retired]
 print('LEASES',tm,len(lease_data),len(live),len(retired),len(active),sorted(x['lease']['lease_id'] for x in active))
for path in ['.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py','docs/PROTOCOL_DA_PHIEN.md',adrpath]:
 r=subprocess.run([sys.executable,'-B',str(O/'master/ops/lease_publish.py'),'ai-dang-giu',path,'--root',str(O/'master')],capture_output=True,text=True)
 print('HOLDER',path,'RC',r.returncode,r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[:200])
r=subprocess.run([sys.executable,'-B',str(O/'sc/tien_kiem.py'),'origin/master'],cwd=O/'master',capture_output=True,text=True)
(O/'snapshot-preflight.log').write_text(r.stdout+r.stderr);print('SNAPSHOT_PREFLIGHT_RC',r.returncode,(r.stdout+r.stderr).strip().replace('\n',' | '))
for root in ['base','prototype']:
 files=[str(O/root/'.claude/dev'/f) for f in ['packet_loop.py','packet_loop_test.py']]
 r=subprocess.run(['ruff','check','--select','F','--no-cache','--isolated','--output-format','json',*files],capture_output=True,text=True)
 (O/(root+'-ruff.json')).write_text(r.stdout);d=json.loads(r.stdout);norm=[]
 for x in d:
  p=Path(x['filename']);line=p.read_text().splitlines()[x['location']['row']-1];norm.append((p.name,x['code'],re.sub(r'from line \d+','from line N',x['message']),line.strip()))
 globals()['ruff_'+root]=set(norm);print('RUFF',root,'RC',r.returncode,'N',len(d),dict(collections.Counter(x['code'] for x in d)))
print('RUFF_DELTA_NEW',sorted(ruff_prototype-ruff_base),'REMOVED',sorted(ruff_base-ruff_prototype))
