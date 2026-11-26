import pathlib,re,sys,shutil,subprocess,unicodedata,collections,json
root=pathlib.Path('cay-kho').resolve(); out=pathlib.Path('out').resolve(); proto=(root/'docs/PROTOCOL_DA_PHIEN.md').read_text(); spec=(root/'ops/specs/wp1466.md').read_text()
b=dict(re.findall(r'^~~~ ([^\n]+)\n(.*?)^~~~$',spec,re.M|re.S))
anchors=['    workflow trigger và prompt chỉ là worker/client có thể thay thế, không tự cấp quyền hoặc tự nối chuỗi vai trò.\n','## 2. Thành phần và quyền\n','### 8.3 Lịch sử lớp finding và giới hạn nghiệm thu\n\n',b['p4-cu'],b['p5-cu']]
print('P1..P5_ANCHOR_COUNTS',[proto.count(a) for a in anchors]); print('P6_ANCHOR_COUNT',sum(l.startswith('| `ADR-0067` | ') for l in proto.splitlines()))
new=proto.replace(anchors[0],anchors[0]+b['p1-moi'],1).replace(anchors[1],b['p2-moi']+'\n'+anchors[1],1).replace(anchors[2],anchors[2]+b['p3-moi']+'\n',1).replace(b['p4-cu'],b['p4-moi'],1).replace(b['p5-cu'],b['p5-moi'],1)
a6=next(l+'\n' for l in proto.splitlines() if l.startswith('| `ADR-0067` | '));new=new.replace(a6,a6+b['p6-moi'],1)
(out/'protocol-before.md').write_text(proto);(out/'protocol-after.md').write_text(new)
p=subprocess.run(['git','diff','--no-index','--numstat',str(out/'protocol-before.md'),str(out/'protocol-after.md')],text=True,capture_output=True)
print('PROTO_NUMSTAT',p.stdout.strip(),'rc',p.returncode)
sys.path.insert(0,str(root/'.claude/dev')); import packet_loop as pl
vis,err=pl._che_khong_render(new)
norm=lambda s:re.sub(r'\s+',' ',unicodedata.normalize('NFC',s)).strip()
paras=[norm(p) for p in re.split(r'\n\s*\n',vis)]
n4=norm(b['p1-moi'].split('12. ')[0]);n5=norm('12. '+b['p1-moi'].split('12. ')[1])
n7=next(l.split('|')[2].strip() for l in b['p2-moi'].splitlines() if l.startswith('| `INV-12`'))
neo=['### 8.3 Lịch sử lớp finding và giới hạn nghiệm thu','**Bảng lớp của mỗi lượt.**','`ĐÃ VÁ THẬT` · `VÁ HỜ` · `VÁ SINH LỖI MỚI` · `CHƯA VÁ`',n4,n5,norm(b['p3-moi']),n7,'Một lớp xuất hiện ở ba lượt review khác nhau đòi xem lại cách làm tại checkpoint']
for i,n in enumerate(neo,1):
 hits=[p for p in paras if n in p]; print('NEO',i,'FULL',sum(p==n for p in paras),'CONTAINS',len(hits),'PARA_LENGTH',[len(x) for x in hits],'NEEDLE_LENGTH',len(n))
print('MASK_ERRORS',err)
for label,change in [('delete_search_class','Reviewer khái quát mỗi biểu hiện thành lớp và quét mọi biểu hiện cùng lớp trên candidate trước khi báo theo ADR-0060 M2; không báo từng lỗi riêng lẻ.'),('delete_convergence','Tỷ lệ = |F|/|U|; nhiều finding cùng lớp chỉ tính một lần.'),('delete_repeat_history','ba biểu hiện của lớp trong cùng một lượt chỉ là một lần xuất hiện. Revision/scope\ncut không reset lịch sử đó, không tự cấp thêm review call hoặc attempt.'),('delete_checkpoint_journal',b['p5-moi'].strip())]:
 trial=new.replace(change,'')
 v,e=pl._che_khong_render(trial)
 print('SEMANTIC_REMOVAL',label,'SOURCE_COUNT',new.count(change),'ALL_EIGHT_SUBSTRING_PRESENT',all(n in norm(v) for n in neo),'ERR',e)
# Number of rows and cell grammar.
patterns=b['mau-o-cong'].splitlines(); kinds=collections.Counter()
for l in b['p2-moi'].splitlines():
 if not l.startswith('| `INV'):continue
 cells=[c.strip().replace('`','') for c in l.strip('|').split('|')]; gate=cells[3]
 kinds.update(i for i,p in enumerate(patterns) if re.fullmatch(p,gate))
print('CELL_GRAMMAR_COUNTS',dict(kinds))
# Build only the scratch inputs needed by existing read-only commands.
scratch=out/'proposed-tree'
for p in [*root.glob('docs/adr/*.md'),*root.glob('.claude/skills/**/*.md'),*root.glob('.agents/skills/**/*.md'),root/'CLAUDE.md']:
 dest=scratch/p.relative_to(root);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
(scratch/'docs/PROTOCOL_DA_PHIEN.md').write_text(new)
adr=b['adr'].replace('{{TRANG_THAI}}','- **Trạng thái:** Proposed (bản dựng đo của reviewer; không phải approval)')
for i in range(1,7):adr=adr.replace('{{N%d}}'%i,'KHONG_DO_DUOC')
(scratch/'docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md').write_text(adr)
for tree in [root,scratch]:
 for command in ['adr-song','doctrine-scan','bat-bien']:
  p=subprocess.run([sys.executable,'-B',str(root/'.claude/dev/packet_loop.py'),command,'--root',str(tree)],text=True,capture_output=True)
  print('GATE',tree.name,command,'RC',p.returncode,'STDOUT',p.stdout.strip(),'STDERR',p.stderr.strip()[:300])
reg=json.loads((out/'registry-names.json').read_text()); counts=collections.Counter(reg['cases']);print('REGISTRY_ENTRIES',len(reg['cases']),'UNIQUE',len(counts),'DUPLICATES',[x for x,n in counts.items() if n>1])
