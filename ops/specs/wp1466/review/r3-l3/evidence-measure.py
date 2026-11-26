from pathlib import Path
import subprocess,hashlib,re,json,ast,unicodedata,datetime,os
W=Path(__file__).resolve().parent.parent; O=W/'out'; R=W/'cay-kho'; P=O/'prototype'
def git(*args):return subprocess.run(['git','-C',str(R),*args],capture_output=True,text=True)
def show(ref,path):
 r=git('show',f'{ref}:{path}'); assert r.returncode==0,(ref,path,r.stderr);return r.stdout
spec=(R/'ops/specs/wp1466.md').read_text(); base='48d372e14f190dae83a75ccbca8ee9a0b25635c5'
print('MEASURED_AT',datetime.datetime.now(datetime.timezone.utc).isoformat())
print('HEAD_TREE',git('rev-parse','HEAD','HEAD^{tree}').stdout.strip())
print('HASH',hashlib.sha256((R/'ops/specs/wp1466.md').read_bytes()).hexdigest())
print('SHALLOW',git('rev-parse','--is-shallow-repository').stdout.strip(),'ABBREV',git('config','core.abbrev').stdout.strip())
refs=git('for-each-ref','--format=%(refname)','refs/remotes/origin').stdout.splitlines();refs=[x for x in refs if not x.endswith('/HEAD')];print('REFS',len(refs))
print('MASTER',git('rev-parse','origin/master').stdout.strip());print('MASTER_COMMITS',git('rev-list','--count',base+'..origin/master').stdout.strip());print('MASTER_DIFF',git('diff','--name-only',base,'origin/master').stdout.strip())
first=git('rev-list','--first-parent','origin/master').stdout.splitlines()
for number,oid,fn in [('0055','d2e3052d479d140b7e7b91df41ec4914fab7d544','0055-tran-loi-goi-codex-len-muoi.md'),('0053','8ab100793df9831505f495543a74044b91c2c9ab','0053-tran-kich-thuoc-sensitive-len-sau-tep.md')]:
 path='docs/adr/'+fn;print('OPT_IN',number,[git('cat-file','-e',oid+':'+path).returncode,git('cat-file','-e',oid+'^1:'+path).returncode],oid in first)
adr=git('ls-tree','-r','--name-only','origin/master','docs/adr').stdout.splitlines();print('ADR_BASE',len(adr),max(int(Path(p).name[:4]) for p in adr))
higher=[]
for ref in refs:
 paths=git('ls-tree','-r','--name-only',ref,'docs/adr').stdout.splitlines()
 if any(re.match(r'\d{4}-',Path(p).name) and int(Path(p).name[:4])>=68 for p in paths):higher.append(ref)
print('ADR_0068_PLUS',len(higher))
adr_text=(P/'docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md').read_text()
adr_block=re.search(r'~~~ adr\n(.*?)\n~~~',spec,re.S)[1]+'\n'
print('ADR_LINES',len(adr_text.splitlines()),len(adr_block.splitlines()))
proto=(P/'docs/PROTOCOL_DA_PHIEN.md').read_text();src=show(base,'docs/PROTOCOL_DA_PHIEN.md')
rows=[d for d in proto.splitlines() if d.startswith('| `INV-')]
gates=[d for d in rows if '| cổng:' in d];debts=re.findall(r'^- `([^`]+)`:',adr_block.split('## Nợ')[1].split('## Giới hạn')[0],re.M)
refs_debt=set(n for d in rows for n in re.findall(r'(?:còn nợ|nợ): `([^`]+)`',d))
print('INV',len(rows),'GATES',len(gates),'WITH_DEBT',sum('còn nợ:' in d for d in gates),'DISCIPLINE',sum('kỷ luật, 0 cổng' in d for d in rows),'UNMEASURED',sum('| chưa đo |' in d for d in rows),'CASE_REFS',sum(len(re.findall(r'ca: ',d)) for d in rows),'DEBTS',len(debts),'REFERENCED_DEBTS',len(refs_debt),'MISSING',sorted(refs_debt-set(debts)))
canon=lambda s:' '.join(unicodedata.normalize('NFC',s).split())
sect=src.split('Các bất biến không được hạ chuẩn:\n\n')[1].split('\n## 2.')[0]
items=re.findall(r'(?ms)^(\d+)\. (.*?)(?=^\d+\. |\Z)',sect)
for n,text in items:
 matches=[d for d in rows if f'| §1 ({n}) |' in d];print('INV_SOURCE',n,len(matches),bool(matches) and canon(text)==canon(matches[0].split('|')[2]))
# Parser độc lập, không gọi _inv_khoi/_inv_bam của nguyên mẫu.
def mask(s):
 out=[]; fence=None; comment=False
 for d in s.splitlines():
  if comment:
   if '-->' in d:comment=False
   out.append('');continue
  if fence:
   if re.fullmatch(r' {0,3}'+re.escape(fence[0])+r'{'+str(fence[1])+r',}[ \t]*',d):fence=None
   out.append('');continue
  m=re.match(r' {0,3}(`{3,}|~{3,})(.*)',d)
  if m and (m[1][0]!='`' or '`' not in m[2]):fence=(m[1][0],len(m[1]));out.append('');continue
  if '<!--' in d:
   d,_,tail=d.partition('<!--');comment='-->' not in tail
   if not comment:d+=tail.partition('-->')[2]
  out.append(d)
 return '\n'.join(out)
def blocks(s):
 out=[];acc=[]
 def flush():
  if acc:
   out.append('\n'.join(canon(x) for x in acc) if acc[0].startswith('|') else ('    ' if acc[0].startswith('    ') else '')+canon(' '.join(acc)))
   acc.clear()
 for d in mask(s).splitlines():
  if not d.strip() or d.startswith('#'):
   flush()
   if d.startswith('#'):out.append(canon(d))
  else:acc.append(d)
 flush();return out
b=blocks(proto);ms=[]
for x in b:
 if x.startswith('#'):ms.append([x])
 elif ms:ms[-1].append(x)
units={'khoi':b,'muc':['\n\n'.join(x) for x in ms]}
lock=[]
for n,kind,h in re.findall(r'^(K\d+) \| (\w+) \| ([a-f0-9]{64}) \|',spec,re.M):
 matched=[x for x in units[kind] if hashlib.sha256(x.encode()).hexdigest()==h]
 print('LOCK',n,kind,len(matched),h);lock.append((n,kind,h))
(O/'independent-locks.json').write_text(json.dumps({n:[x for x in units[k] if hashlib.sha256(x.encode()).hexdigest()==h] for n,k,h in lock},ensure_ascii=False,indent=2))
# Khối script N8 nguyên văn từ spec.
N8=re.search(r'~~~ do-pham-vi\n(.*?)\n~~~',spec,re.S)[1]+'\n';(O/'n8_spec.py').write_text(N8);print('N8_NONBLANK',sum(bool(x.strip()) for x in N8.splitlines()))
for name in ('packet_loop.py','packet_loop_test.py'):(O/('base-'+name)).write_text(show(base,'.claude/dev/'+name))
# Vector sáu vị trí, một số = số dòng có match.
paths=['ops/lease_publish.py','.claude/dev/packet_loop.py','.claude/dev/launcher.py','.claude/dev/gate_lifecycle.py','.github/workflows/ci.yml','.github/workflows/ops-publish-lease.yml']
patterns=['bang_lop','class_slug','review_verdict','KET_LUAN','numstat','ADR-0068|INV_|_inv_','ai-dang-giu|ai_dang_giu|RC_DANG_GIU','refs/pull/','eol|EOL|gitattributes','RC_PROVIDER','reviewed_sha|reviewing_head_sha','spec_hash|spec_sha256','model_family|ho_model','effective_review_class|_kiem_lop_review|RC_LOP','chup-workspace|chup_workspace|ghi_workspace','MOC_10_2_2|moc_10_2_2','codex_review_calls|RC_TRAN','NGUOI_CO_THAM_QUYEN|RC_TU_CAP','doctrine','mien_p3',r'\bLIVE\b','changed_paths','tested_sha','ADR-0067|uy_quyen_quyet_dinh','Drive MCP|Sheets MCP','integration','label|assignee|board','diff --check','push_them|so_lan_push|M5','writer_slot|hai writer|max_writers|executor_writers']
texts=[show('origin/master',p) for p in paths]
for pat in patterns:print('VECTOR',pat,[sum(bool(re.search(pat,d)) for d in t.splitlines()) for t in texts])
for p,t in zip(paths,texts):
 if p in paths[2:]:
  for i,d in enumerate(t.splitlines(),1):
   if re.search('label|assignee|board',d):print('LABEL_READ',p,i,d.strip())
receipts=[x for x in git('ls-tree','-r','--name-only','origin/master','ops/reviews').stdout.splitlines() if x.endswith('.receipt.yaml')];print('RECEIPTS',len(receipts),'BANG_LOP',sum('bang_lop' in show('origin/master',x) for x in receipts))
print('PROTO_DIFF',subprocess.run(['git','-C',str(P),'diff','--numstat'],capture_output=True,text=True).stdout.strip(),'ADR',len(adr_text.splitlines()))
print('TOTAL_ADDED',sum(int(x.split('\t')[0]) for x in subprocess.run(['git','-C',str(P),'diff','--numstat'],capture_output=True,text=True).stdout.splitlines())+len(adr_text.splitlines()))
