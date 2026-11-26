from pathlib import Path
import subprocess,hashlib,re,json,ast,datetime,os,sys
O=Path(__file__).resolve().parent;R=O.parent/'cay-kho';P=O/'prototype';BASE='48d372e14f190dae83a75ccbca8ee9a0b25635c5'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'tmp'))
def git(*a):return subprocess.run(['git','-C',str(R),*a],capture_output=True)
def show(ref,p):
 r=git('show',ref+':'+p);assert r.returncode==0,(ref,p);return r.stdout
sha=lambda b:hashlib.sha256(b).hexdigest()
spec=(R/'ops/specs/wp1466.md').read_text();proto=(P/'docs/PROTOCOL_DA_PHIEN.md').read_bytes();source=show(BASE,'docs/PROTOCOL_DA_PHIEN.md')
print('AT',datetime.datetime.now(datetime.timezone.utc).isoformat());print('SPEC_BLOB_EQUALS',show('HEAD','ops/specs/wp1466.md')==(R/'ops/specs/wp1466.md').read_bytes());print('R4_VERDICT_HASH',sha((R/'ops/specs/wp1466/review/r4-l4/VERDICT.md').read_bytes()))
print('SHALLOW_ABBREV',git('rev-parse','--is-shallow-repository').stdout.decode().strip(),git('config','core.abbrev').stdout.decode().strip())
refs=git('for-each-ref','--format=%(refname)','refs/remotes/origin').stdout.decode().splitlines();print('ORIGIN_REFS',len(refs),'BRANCHES',len([r for r in refs if not r.endswith('/HEAD')]))
changed=git('diff','--name-only',BASE,'origin/master').stdout.decode().splitlines();(O/'master-changed.txt').write_text('\n'.join(changed)+'\n');print('MASTER_DRIFT',git('rev-list','--count',BASE+'..origin/master').stdout.decode().strip(),'commits',len(changed),'paths')
paths=['ops/lease_publish.py','.claude/dev/packet_loop.py','.claude/dev/launcher.py','.claude/dev/gate_lifecycle.py','.github/workflows/ci.yml','.github/workflows/ops-publish-lease.yml']; measured=paths+['docs/PROTOCOL_DA_PHIEN.md','.claude/dev/packet_loop_test.py','.claude/dev/packet_loop_test_manh.py','.claude/dev/ci_dang_ky_test.py','ops/ci_duong_nhanh.py']
print('MEASURED_CHANGED',[p for p in changed if p in measured or p.startswith(('docs/adr/','.githooks/','.claude/skills/','.agents/skills/'))])
first=git('rev-list','--first-parent','origin/master').stdout.decode().splitlines()
for num,oid in [('0055','d2e3052d479d140b7e7b91df41ec4914fab7d544'),('0053','8ab100793df9831505f495543a74044b91c2c9ab')]:
 p=next((R/'docs/adr').glob(num+'-*')).relative_to(R).as_posix();print('OPTIN',num,git('cat-file','-e',oid+':'+p).returncode,git('cat-file','-e',oid+'^1:'+p).returncode,oid in first)
adrfiles=git('ls-tree','-r','--name-only','origin/master','docs/adr').stdout.decode().splitlines();print('ADR_BASE',len(adrfiles),max(int(Path(x).name[:4]) for x in adrfiles))
higher=[r for r in refs if not r.endswith('/HEAD') and any(re.match(r'\d{4}-',Path(p).name) and int(Path(p).name[:4])>=68 for p in git('ls-tree','-r','--name-only',r,'docs/adr').stdout.decode().splitlines())];print('ADR68_PLUS_REFS',len(higher))
# Independent byte parser. Mask fences and comments only for locating headers; slicing always raw bytes.
raw=proto.split(b'\n');vis=[];fence=None
for line in raw:
 if fence:
  vis.append(b' '*len(line))
  if re.fullmatch(b' {0,3}'+re.escape(fence[:1])+b'{'+str(len(fence)).encode()+b',}[ \t]*',line):fence=None
 else:
  m=re.match(b' {0,3}(`{3,}|~{3,})(.*)',line)
  if m and (m[1][:1]!=b'`' or b'`' not in m[2]):fence=m[1];vis.append(b' '*len(line))
  else:vis.append(line)
assert fence is None
vis=re.sub(b'<!--.*?-->',lambda m:re.sub(b'[^\n]',b' ',m[0]),b'\n'.join(vis),flags=re.S).split(b'\n')
headers=[i for i,x in enumerate(vis) if x.startswith(b'#')];sections=[];stack=[]
for a,b in zip(headers,headers[1:]+[len(raw)]):
 level=len(vis[a])-len(vis[a].lstrip(b'#'));stack=[v for v in stack if v[0]<level]+[(level,raw[a])];end=b
 while end>a and raw[end-1]==b'':end-=1
 spans=[(a,end)];start=None
 for i in range(a+1,b+1):
  if i<b and raw[i]!=b'':
   if start is None:start=i
  elif start is not None:spans.append((start,i));start=None
 sections.append(dict(address=sha(b'\n'.join(v[1] for v in stack)),spans=spans))
locks={};parsed=[]
for name,address,n,digest in re.findall(r'^(K\d+) \| ([a-f0-9]{64}) \| (\d+) \| ([a-f0-9]{64})',spec,re.M):
 matches=[s for s in sections if s['address']==address];assert len(matches)==1
 a,b=matches[0]['spans'][int(n)];unit=b'\n'.join(raw[a:b]);actual=sha(unit);print('LOCK',name,'LOCATION',a+1,b,'HASH_MATCH',actual==digest,'VISIBLE',raw[a:b]==vis[a:b]);assert actual==digest
 locks[name]=dict(dong=[a+1,b],thu_tu=int(n),unit=unit.decode(),address=address,digest=digest);parsed.append((name,address,int(n),digest))
(O/'locks.json').write_text(json.dumps(locks,ensure_ascii=False,indent=2))
module=ast.parse((P/'.claude/dev/packet_loop.py').read_text());constants=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='INV_KHOA_PROTOCOL' for t in n.targets));print('CODE_LOCK_TABLE_MATCH',tuple(parsed)==constants)
blocks={k:re.search(r'~~~ '+k+r'\n(.*?)\n~~~',spec,re.S)[1] for k in ['p1-moi','p2-moi','p3-moi','p4-cu','p4-moi','p5-cu','p5-moi','p6-moi','adr']};s=source.decode();anchors=['    workflow trigger và prompt chỉ là worker/client có thể thay thế, không tự cấp quyền hoặc tự nối chuỗi vai trò.','## 2. Thành phần và quyền','### 8.3 Lịch sử lớp finding và giới hạn nghiệm thu\n\n',blocks['p4-cu'],blocks['p5-cu'],next(x for x in s.splitlines() if x.startswith('| `ADR-0067` |'))];print('SIX_ANCHORS',[s.count(a) for a in anchors])
s=s.replace(anchors[0],anchors[0]+'\n'+blocks['p1-moi']).replace(anchors[1],blocks['p2-moi']+'\n\n'+anchors[1]).replace(anchors[2],anchors[2]+blocks['p3-moi']+'\n\n').replace(blocks['p4-cu'],blocks['p4-moi']).replace(blocks['p5-cu'],blocks['p5-moi']).replace(anchors[5],anchors[5]+'\n'+blocks['p6-moi']);print('PROTOCOL_EXACT',s.encode()==proto)
adr=(P/'docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md').read_text();rows=[l for l in proto.decode().splitlines() if l.startswith('| `INV-')];debts=re.findall(r'^- `([^`]+)`:',blocks['adr'].split('## Nợ')[1].split('## Giới hạn')[0],re.M);rd=set(n for x in rows for n in re.findall(r'(?:còn nợ|nợ): `([^`]+)`',x));print('INV_COUNTS',len(rows),sum('| cổng:' in x for x in rows),sum('còn nợ:' in x for x in rows),sum('kỷ luật, 0 cổng' in x for x in rows),sum('| chưa đo |' in x for x in rows),sum(x.count('ca: ') for x in rows),'DEBTS',len(debts),'REF_DEBTS',len(rd),'MISSING',sorted(rd-set(debts)))
items=re.findall(r'(?ms)^(\d+)\. (.*?)(?=^\d+\. |\Z)',source.decode().split('Các bất biến không được hạ chuẩn:\n\n')[1].split('\n## 2.')[0]);canon=lambda s:' '.join(s.split());print('SOURCE_ITEMS',[(n,canon(t)==canon(next(x for x in rows if f'| §1 ({n}) |' in x).split('|')[2])) for n,t in items])
pat=re.escape(blocks['adr']+'\n');pat=pat.replace(re.escape('{{TRANG_THAI}}'),r'[^\n]+')
for i in range(1,7):pat=pat.replace(re.escape('{{N'+str(i)+'}}'),r'\d+')
print('ADR_TEMPLATE',re.fullmatch(pat,adr) is not None,'LINES',len(adr.splitlines()))
for tree in ['prototype','master']:
 q=O/tree; num=subprocess.run(['git','-C',str(q),'diff','--numstat'],capture_output=True,text=True).stdout;print('NUMSTAT',tree,num.strip().replace('\n','; '),'ADR',len(adr.splitlines()),'TOTAL',sum(int(x.split('\t')[0]) for x in num.splitlines())+len(adr.splitlines()));print('DIFF_CHECK',tree,subprocess.run(['git','-C',str(q),'diff','--check'],capture_output=True,text=True).returncode)
 for gate in ['doctrine-scan','adr-song']:
  r=subprocess.run([sys.executable,'-B',str(q/'.claude/dev/packet_loop.py'),gate,'--root',str(q)],capture_output=True,text=True);print('GATE',tree,gate,r.returncode,r.stdout.strip(),r.stderr.strip())
patterns=['bang_lop','class_slug','review_verdict','KET_LUAN','numstat','ADR-0068|INV_|_inv_','ai-dang-giu|ai_dang_giu|RC_DANG_GIU','refs/pull/','eol|EOL|gitattributes','RC_PROVIDER','reviewed_sha|reviewing_head_sha','spec_hash|spec_sha256','model_family|ho_model','effective_review_class|_kiem_lop_review|RC_LOP','chup-workspace|chup_workspace|ghi_workspace','MOC_10_2_2|moc_10_2_2','codex_review_calls|RC_TRAN','NGUOI_CO_THAM_QUYEN|RC_TU_CAP','doctrine','mien_p3',r'\bLIVE\b','changed_paths','tested_sha','ADR-0067|uy_quyen_quyet_dinh','Drive MCP|Sheets MCP','integration','label|assignee|board','diff --check','push_them|so_lan_push|M5','writer_slot|hai writer|max_writers|executor_writers']
texts=[show('origin/master',p).decode() for p in paths]
for pat in patterns:print('VECTOR',pat,[sum(bool(re.search(pat,l)) for l in t.splitlines()) for t in texts])
print('ADR_ENFORCEMENT',[sum(bool(re.search('ADR-0068|INV_|_inv_',l)) for l in (P/p).read_text().splitlines()) for p in paths])
receipts=[x for x in git('ls-tree','-r','--name-only','origin/master','ops/reviews').stdout.decode().splitlines() if x.endswith('.receipt.yaml')];print('RECEIPTS',len(receipts),'BANG_LOP',sum(b'bang_lop' in show('origin/master',x) for x in receipts))
print('ATTR',git('check-attr','eol','--','docs/PROTOCOL_DA_PHIEN.md').stdout.decode().strip())
