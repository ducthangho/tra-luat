from pathlib import Path
import subprocess,hashlib,re,json,ast,datetime,os
W=Path(__file__).resolve().parent.parent;O=W/'out';R=W/'cay-kho';P=O/'prototype';base='48d372e14f190dae83a75ccbca8ee9a0b25635c5'
def git(*a):return subprocess.run(['git','-C',str(R),*a],capture_output=True)
def show(ref,p):
 r=git('show',ref+':'+p);assert r.returncode==0,(ref,p);return r.stdout
spec=(R/'ops/specs/wp1466.md').read_text(); print('AT',datetime.datetime.now(datetime.timezone.utc).isoformat())
print('SPEC_HASH',hashlib.sha256((R/'ops/specs/wp1466.md').read_bytes()).hexdigest(),'BLOB_EQUALS',show('HEAD','ops/specs/wp1466.md')==(R/'ops/specs/wp1466.md').read_bytes())
print('HEAD_TREE',git('rev-parse','HEAD','HEAD^{tree}').stdout.decode().splitlines())
print('SHALLOW_ABBREV',git('rev-parse','--is-shallow-repository').stdout.decode().strip(),git('config','core.abbrev').stdout.decode().strip())
refs=git('for-each-ref','--format=%(refname)','refs/remotes/origin').stdout.decode().splitlines();print('REFS_TOTAL',len(refs));refs=[r for r in refs if not r.endswith('/HEAD')];print('BRANCHES',len(refs))
paths=['ops/lease_publish.py','.claude/dev/packet_loop.py','.claude/dev/launcher.py','.claude/dev/gate_lifecycle.py','.github/workflows/ci.yml','.github/workflows/ops-publish-lease.yml']
print('MASTER',git('rev-parse','origin/master').stdout.decode().strip(),'COMMITS',git('rev-list','--count',base+'..origin/master').stdout.decode().strip())
changes=git('diff','--name-only',base,'origin/master').stdout.decode().splitlines();print('MASTER_CHANGED',len(changes));print('MEASURED_PATHS_CHANGED',git('diff','--name-only',base,'origin/master','--',*paths,'docs/PROTOCOL_DA_PHIEN.md','docs/adr/','.claude/dev/packet_loop_test.py','.claude/dev/packet_loop_test_manh.py','ops/ci_duong_nhanh.py','.githooks/').stdout.decode().splitlines());(O/'master-changed-paths.txt').write_text('\n'.join(changes)+'\n')
first=git('rev-list','--first-parent','origin/master').stdout.decode().splitlines()
for num,oid in [('0055','d2e3052d479d140b7e7b91df41ec4914fab7d544'),('0053','8ab100793df9831505f495543a74044b91c2c9ab')]:
 p=next((R/'docs/adr').glob(num+'-*')).relative_to(R).as_posix();print('OPTIN',num,git('cat-file','-e',oid+':'+p).returncode,git('cat-file','-e',oid+'^1:'+p).returncode,oid in first)
adrpaths=git('ls-tree','-r','--name-only','origin/master','docs/adr').stdout.decode().splitlines();print('ADR_BASE',len(adrpaths),max(int(Path(x).name[:4]) for x in adrpaths))
higher=[r for r in refs if any(re.match(r'\d{4}-',Path(p).name) and int(Path(p).name[:4])>=68 for p in git('ls-tree','-r','--name-only',r,'docs/adr').stdout.decode().splitlines())];print('ADR_68_PLUS',len(higher))
proto=(P/'docs/PROTOCOL_DA_PHIEN.md').read_bytes();src=show(base,'docs/PROTOCOL_DA_PHIEN.md')
adr=(P/'docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md').read_text();adrblock=re.search(r'~~~ adr\n(.*?)\n~~~',spec,re.S)[1]+'\n'; print('ADR_LINES',len(adr.splitlines()))
rows=[x for x in proto.decode().splitlines() if x.startswith('| `INV-')];debts=re.findall(r'^- `([^`]+)`:',adrblock.split('## Nợ')[1].split('## Giới hạn')[0],re.M);rd=set(n for x in rows for n in re.findall(r'(?:còn nợ|nợ): `([^`]+)`',x));print('INV_COUNTS',len(rows),sum('| cổng:' in x for x in rows),sum('còn nợ:' in x for x in rows),sum('kỷ luật, 0 cổng' in x for x in rows),sum('| chưa đo |' in x for x in rows),sum(x.count('ca: ') for x in rows),'DEBTS',len(debts),'REF_DEBTS',len(rd),'MISSING',sorted(rd-set(debts)))
items=re.findall(r'(?ms)^(\d+)\. (.*?)(?=^\d+\. |\Z)',src.decode().split('Các bất biến không được hạ chuẩn:\n\n')[1].split('\n## 2.')[0]);canon=lambda s:' '.join(s.split())
for n,t in items:
 row=next(x for x in rows if f'| §1 ({n}) |' in x);print('INV_SOURCE',n,canon(t)==canon(row.split('|')[2]))
# Independent byte parser. Canonical locked units contain no fenced code/comments: validate this explicitly.
masked=[];fence=None
for line in proto.split(b'\n'):
 if fence:
  masked.append(b' '*len(line))
  if re.fullmatch(b' {0,3}'+re.escape(fence[:1])+b'{'+str(len(fence)).encode()+b',}[ \t]*',line):fence=None
 else:
  m=re.match(b' {0,3}(`{3,}|~{3,})(.*)',line)
  if m and (m[1][:1]!=b'`' or b'`' not in m[2]):fence=m[1];masked.append(b' '*len(line))
  else:masked.append(line)
assert fence is None
rawmasked=b'\n'.join(masked)
rawmasked=re.sub(b'<!--.*?-->',lambda m:re.sub(b'[^\n]',b' ',m[0]),rawmasked,flags=re.S)
lines=rawmasked.split(b'\n');head=[i for i,d in enumerate(lines) if d.startswith(b'#')]+[len(lines)];stack=[];sections=[];sha=lambda b:hashlib.sha256(b).hexdigest()
for a,b in zip(head,head[1:]):
 level=len(lines[a])-len(lines[a].lstrip(b'#'));stack=[p for p in stack if p[0]<level]+[(level,lines[a])]
 part=lines[a:b]
 while part and not part[-1].strip():part.pop()
 blocks=[];acc=[]
 for d in part[1:]+[b'']:
  if d.strip():acc.append(d)
  elif acc:blocks.append(b'\n'.join(acc));acc=[]
 sections.append((sha(b'\n'.join(x[1] for x in stack)),[b'\n'.join(part)]+blocks,a,b))
locks={}
for name,addr,num,digest in re.findall(r'^(K\d+) \| ([a-f0-9]{64}) \| (\d+) \| ([a-f0-9]{64})',spec,re.M):
 ss=[s for s in sections if s[0]==addr];assert len(ss)==1;unit=ss[0][1][int(num)];assert b'<!--' not in unit and b'```' not in unit and b'~~~' not in unit;print('LOCK',name,'ADDRESS_COUNT',len(ss),'BYTE_HASH',sha(unit),'MATCH',sha(unit)==digest);locks[name]={'unit':unit.decode(),'address':addr,'index':int(num),'digest':digest,'section_start':ss[0][2],'section_end':ss[0][3]}
(O/'locks.json').write_text(json.dumps(locks,ensure_ascii=False,indent=2))
n8=re.search(r'~~~ do-pham-vi\n(.*?)\n~~~',spec,re.S)[1]+'\n';(O/'n8_spec.py').write_text(n8);print('N8_LINES_NONBLANK',sum(bool(x.strip()) for x in n8.splitlines()),'SUPPLIED_EQUAL',n8==(R/'ops/specs/wp1466/nguyen-mau-r4/do_pham_vi.py').read_text())
for f in ['packet_loop.py','packet_loop_test.py']:(O/('base-'+f)).write_bytes(show(base,'.claude/dev/'+f))
# Independently reconstruct all protocol edits from spec and base; compare bytes to prototype.
b={key:re.search(r'~~~ '+key+r'\n(.*?)\n~~~',spec,re.S)[1] for key in ['p1-moi','p2-moi','p3-moi','p4-cu','p4-moi','p5-cu','p5-moi','p6-moi']}
r=src.decode();anchors=['    workflow trigger và prompt chỉ là worker/client có thể thay thế, không tự cấp quyền hoặc tự nối chuỗi vai trò.','## 2. Thành phần và quyền','### 8.3 Lịch sử lớp finding và giới hạn nghiệm thu\n\n',b['p4-cu'],b['p5-cu'],next(x for x in r.splitlines() if x.startswith('| `ADR-0067` |'))];print('INSERT_ANCHORS',[r.count(x) for x in anchors]);r=r.replace(anchors[0],anchors[0]+'\n'+b['p1-moi']).replace(anchors[1],b['p2-moi']+'\n\n'+anchors[1]).replace(anchors[2],anchors[2]+b['p3-moi']+'\n\n').replace(b['p4-cu'],b['p4-moi']).replace(b['p5-cu'],b['p5-moi']).replace(anchors[5],anchors[5]+'\n'+b['p6-moi']);print('PROTO_EXACT_RECONSTRUCTION',r.encode()==proto)
patterns=['bang_lop','class_slug','review_verdict','KET_LUAN','numstat','ADR-0068|INV_|_inv_','ai-dang-giu|ai_dang_giu|RC_DANG_GIU','refs/pull/','eol|EOL|gitattributes','RC_PROVIDER','reviewed_sha|reviewing_head_sha','spec_hash|spec_sha256','model_family|ho_model','effective_review_class|_kiem_lop_review|RC_LOP','chup-workspace|chup_workspace|ghi_workspace','MOC_10_2_2|moc_10_2_2','codex_review_calls|RC_TRAN','NGUOI_CO_THAM_QUYEN|RC_TU_CAP','doctrine','mien_p3',r'\bLIVE\b','changed_paths','tested_sha','ADR-0067|uy_quyen_quyet_dinh','Drive MCP|Sheets MCP','integration','label|assignee|board','diff --check','push_them|so_lan_push|M5','writer_slot|hai writer|max_writers|executor_writers']
texts=[show('origin/master',p).decode() for p in paths]
for pat in patterns:print('VECTOR',pat,[sum(bool(re.search(pat,d)) for d in t.splitlines()) for t in texts])
print('VECTOR_CANDIDATE_ADR',[sum(bool(re.search('ADR-0068|INV_|_inv_',d)) for d in (P/p).read_text().splitlines()) for p in paths])
receipts=[x for x in git('ls-tree','-r','--name-only','origin/master','ops/reviews').stdout.decode().splitlines() if x.endswith('.receipt.yaml')];print('RECEIPTS',len(receipts),'BANG_LOP',sum(b'bang_lop' in show('origin/master',x) for x in receipts))
num=subprocess.run(['git','-C',str(P),'diff','--numstat'],capture_output=True,text=True).stdout;print('NUMSTAT',num.strip().replace('\n','; '),'ADR',len(adr.splitlines()),'TOTAL_ADDED',sum(int(x.split('\t')[0]) for x in num.splitlines())+len(adr.splitlines()))
print('DIFF_CHECK',subprocess.run(['git','-C',str(P),'diff','--check'],capture_output=True,text=True).returncode)
