from pathlib import Path
import hashlib,re,json,subprocess,ast,os,sys
O=Path(__file__).resolve().parent;S=O.parent/'cay-kho';P=O/'prototype';spec=(S/'ops/specs/wp1466.md').read_bytes();base=(O/'base/docs/PROTOCOL_DA_PHIEN.md').read_bytes();proto=(P/'docs/PROTOCOL_DA_PHIEN.md').read_bytes()
blocks=dict(re.findall(rb'^~~~ (\S+)\n(.*?)\n~~~$',spec,re.S|re.M));H=lambda b:hashlib.sha256(b).hexdigest()
# Tự ráp sáu phép sửa từ khối spec; không dùng parser/gate sản phẩm.
anchors=[b'    workflow trigger v\xc3\xa0 prompt ch\xe1\xbb\x89 l\xc3\xa0 worker/client c\xc3\xb3 th\xe1\xbb\x83 thay th\xe1\xba\xbf, kh\xc3\xb4ng t\xe1\xbb\xb1 c\xe1\xba\xa5p quy\xe1\xbb\x81n ho\xe1\xba\xb7c t\xe1\xbb\xb1 n\xe1\xbb\x91i chu\xe1\xbb\x97i vai tr\xc3\xb2.', '## 2. Thành phần và quyền'.encode(), '### 8.3 Lịch sử lớp finding và giới hạn nghiệm thu'.encode(),blocks[b'p4-cu'],blocks[b'p5-cu'],next(x for x in base.split(b'\n') if x.startswith(b'| `ADR-0067` | '))]
print('SIX_ANCHORS',[base.count(x) for x in anchors]);rebuilt=base
rebuilt=rebuilt.replace(anchors[0]+b'\n',anchors[0]+b'\n'+blocks[b'p1-moi']+b'\n',1)
rebuilt=rebuilt.replace(anchors[1],blocks[b'p2-moi']+b'\n\n'+anchors[1],1)
rebuilt=rebuilt.replace(anchors[2]+b'\n\n',anchors[2]+b'\n\n'+blocks[b'p3-moi']+b'\n\n',1)
for i in [4,5]:rebuilt=rebuilt.replace(blocks[f'p{i}-cu'.encode()],blocks[f'p{i}-moi'.encode()],1)
rebuilt=rebuilt.replace(anchors[5]+b'\n',anchors[5]+b'\n'+blocks[b'p6-moi']+b'\n',1)
print('PROTOCOL_EXACT_ASSEMBLY',rebuilt==proto)
# Khoá tại các địa chỉ khai trong spec: xác định heading và biên trực tiếp trên byte LF.
lines=proto.split(b'\n');heading_indices=[];fence=None;comment=False;got=[]
for i,line in enumerate(lines):
 marker=re.match(rb' {0,3}(`{3,}|~{3,})(.*)$',line)
 if fence:
  if marker and marker[1][:1]==fence[:1] and len(marker[1])>=len(fence) and not marker[2].strip():fence=None
  continue
 if marker and not (marker[1].startswith(b'`') and b'`' in marker[2]):fence=marker[1];continue
 if comment:
  if b'-->' in line:comment=False
  continue
 if b'<!--' in line:
  comment=b'-->' not in line.split(b'<!--',1)[1]
  continue
 if re.match(rb'#{1,6} ',line):heading_indices.append(i)
for row in blocks[b'khoa'].decode().splitlines():
 key,addr,index,expected,title=[x.strip() for x in row.split('|')];index=int(index);start=lines.index(title.encode());end=next((i for i in heading_indices if i>start),len(lines));stack=[]
 for i in heading_indices:
  if i>start:break
  depth=lines[i].index(b' ')
  while stack and stack[-1][0]>=depth:stack.pop()
  stack.append((depth,lines[i]))
 address=H(b'\n'.join(x[1] for x in stack));section=lines[start:end]
 while section and section[-1]==b'':section.pop()
 if index==0:unit=b'\n'.join(section)
 else:
  paragraphs=[x for x in re.split(rb'\n(?:\n)+',b'\n'.join(lines[start+1:end]).strip(b'\n')) if x]
  unit=paragraphs[index-1]
 got.append((key,address,index,H(unit)));print('INDEPENDENT_LOCK',key,'ADDRESS_MATCH',address==addr,'HASH_MATCH',H(unit)==expected,'RAW_OCCURRENCES',proto.count(unit))
tree=ast.parse((P/'.claude/dev/packet_loop.py').read_text());assigned=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='INV_KHOA_PROTOCOL' for t in n.targets))
print('CODE_LOCKS_EQUALS_INDEPENDENT',list(assigned)==got)
iv=[x for x in blocks[b'p2-moi'].decode().splitlines() if x.startswith('| `INV-')];print('INV_COUNTS',len(iv),sum('| cổng:' in x for x in iv),sum('| kỷ luật' in x for x in iv),sum('| chưa đo' in x for x in iv),'GATE_WITH_DEBT',sum('| cổng:' in x and 'còn nợ:' in x for x in iv),'TEST_REFS',sum(x.count('ca:') for x in iv))
debts=set(re.findall(r'(?:còn nợ|nợ): `([^`]+)`',blocks[b'p2-moi'].decode()));debtpart=blocks[b'adr'].split('## Nợ'.encode(),1)[1].split('## Giới hạn'.encode(),1)[0];names=set(re.findall(rb'^- `([^`]+)`',debtpart,re.M));print('DEBT_REFERENCED',len(debts),'DEBT_TOTAL',len(names),'MISSING',sorted(x for x in debts if x.encode() not in names))
# Chuẩn hoá ngắt dòng riêng từng mục gốc, không ghép qua mục.
section=base.split('Các bất biến không được hạ chuẩn:\n\n'.encode(),1)[1].split(b'\n## 2.',1)[0].decode();items=re.findall(r'^\d+\. (.*?)(?=^\d+\. |\Z)',section,re.S|re.M);mapn={1:1,2:2,3:3,4:19,5:4,6:5,7:23,8:6,9:7,10:22}
for n,content in enumerate(items,1):
 dest=next(x for x in iv if x.startswith(f'| `INV-{mapn[n]:02}` |'));cl=dest.split(' | ')[1];print('SOURCE_INVARIANT',n,'EXACT_AFTER_REFLOW',' '.join(content.split())==' '.join(cl.split()))
six=['ops/lease_publish.py','.claude/dev/packet_loop.py','.claude/dev/launcher.py','.claude/dev/gate_lifecycle.py','.github/workflows/ci.yml','.github/workflows/ops-publish-lease.yml'];src=[(O/'base'/p).read_text() for p in six]
patterns={'bang_lop':[0,7,0,0,0,0],'class_slug':[0]*6,'review_verdict':[0]*6,'KET_LUAN':[0,2,0,0,0,0],'ai-dang-giu|ai_dang_giu|RC_DANG_GIU':[11,5,0,0,0,0],'refs/pull/':[0,1,1,0,0,0],'eol|EOL|gitattributes':[0,0,0,0,24,0],'RC_PROVIDER':[0,9,0,0,0,0],'reviewed_sha|reviewing_head_sha':[4,49,0,0,0,0],'spec_hash|spec_sha256':[0,28,0,0,0,0],'model_family|ho_model':[15,33,0,0,0,0],'effective_review_class|_kiem_lop_review|RC_LOP':[15,0,0,0,0,0],'chup-workspace|chup_workspace|ghi_workspace':[0,0,21,0,0,0],'MOC_10_2_2|moc_10_2_2':[0,3,0,0,0,0],'codex_review_calls|RC_TRAN':[0,34,0,0,0,0],'NGUOI_CO_THAM_QUYEN|RC_TU_CAP':[13,15,0,0,0,1],'doctrine':[1,27,5,0,5,1],'mien_p3':[0,3,0,0,0,0],r'\bLIVE\b':[0]*6,'changed_paths':[0]*6,'tested_sha':[0]*6,'ADR-0067|uy_quyen_quyet_dinh':[0]*6,'Drive MCP|Sheets MCP':[0]*6,'integration':[0,1,0,0,0,0],'label|assignee|board':[1,2,8,6,1,0],'diff --check':[0,0,0,0,1,0],'push_them|so_lan_push|M5':[0,5,3,0,0,0],'writer_slot|hai writer|max_writers|executor_writers':[0,0,1,0,0,0],'numstat':[0]*6}
for pat,expected in patterns.items():
 actual=[sum(bool(re.search(pat,line)) for line in s.splitlines()) for s in src];print('VECTOR',pat,actual,'MATCH',actual==expected)
print('VECTORS_TOTAL',len(patterns))
for fn,marker in [('packet_loop.py','    proto_words = _doc_nguon_protocol(root)'),('packet_loop.py','9 bảng ADR §20 lệch với docs/adr/'),('packet_loop_test.py','protocol if protocol is not None else _PROTO_TRUNG_TINH, encoding=')]:
 print('N8_ANCHOR',fn,marker,(O/'base/.claude/dev'/fn).read_text().count(marker))
# ADR đúng template trừ trạng thái và sáu số cưỡng chế.
ad=(P/'docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md').read_bytes();pattern=re.escape(blocks[b'adr']+b'\n');pattern=pattern.replace(re.escape(b'{{TRANG_THAI}}'),rb'[^\n]+')
for i in range(1,7):pattern=pattern.replace(re.escape(('{{N%d}}'%i).encode()),rb'\d+')
print('ADR_TEMPLATE_EQUALS',bool(re.fullmatch(pattern,ad)))
print('AUDIT_LINES',len(subprocess.check_output(['git','-C',str(S),'show','a8affd58c0a7db2668f8de8c542edd225ccc2586:ops/specs/wp1172-kiem83/AUDIT_TUAN_THU_PHIEN_DIEU_PHOI_20261120.md']).splitlines()))
