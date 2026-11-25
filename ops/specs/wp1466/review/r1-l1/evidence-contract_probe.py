import pathlib,sys,re,ast,subprocess,json,collections,shutil,hashlib
root=pathlib.Path('cay-kho').resolve();out=pathlib.Path('out').resolve();sys.path[:0]=[str(root/'.claude/dev'),str(root/'ops')]
import packet_loop as pl, packet_loop_test as pt, ci_duong_nhanh as ci
src=(root/'.claude/dev/packet_loop.py').read_text(); spec=(root/'ops/specs/wp1466.md').read_text();b=dict(re.findall(r'^~~~ ([^\n]+)\n(.*?)^~~~$',spec,re.M|re.S))
for n in ['cmd_init','cmd_kiem_merge','cmd_kiem_dong_wp','cmd_record_codex_call','_che_khong_render']:
 node=next(nod for nod in ast.walk(ast.parse(src)) if isinstance(nod,(ast.FunctionDef,ast.AsyncFunctionDef)) and nod.name==n)
 text=ast.get_source_segment(src,node)
 print('FUNCTION',n,'LINES',node.lineno,node.end_lineno,'session_id',text.count('session_id'),'authorization',text.count('authorization'),'attempts',text.count('attempts'),'review_rounds',text.count('review_rounds'))
 if n=='cmd_kiem_merge':
  k0=next(no for no in ast.walk(node) if isinstance(no,ast.FunctionDef) and no.name=='k0');print('K0_SOURCE',ast.get_source_segment(src,k0))
 if n=='_che_khong_render': print('MASK_BRANCHES',{'fence': '_RAO_MO' in text,'html_comment':'<!--' in text,'html_block_parser': bool(re.search(r'HTMLParser|markdown|commonmark',text))})
for p in ['docs/PROTOCOL_DA_PHIEN.md','docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md','.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py','.claude/dev/launcher_test.py','.githooks/eol_policy_test.py','ops/bien_nhan_v2_test.py','ops/lease_publish_test.py']:
 print('SELECTOR',p,*ci.phan_loai_packet_loop('pull_request',[p]))
# Apply plain-text removals only in a scratch copy, and call the current public gate.
scratch=out/'proposed-tree'; pp=scratch/'docs/PROTOCOL_DA_PHIEN.md'; before=pp.read_text()
start=before.index('### 8.3 Lịch sử'); end=before.index('## 9.',start)
try:
 pp.write_text(before[:start]+before[end:])
 p=subprocess.run([sys.executable,'-B',str(root/'.claude/dev/packet_loop.py'),'doctrine-scan','--root',str(scratch)],capture_output=True,text=True)
 print('DOCTRINE_WITHOUT_8_3',p.returncode,p.stdout.strip(),p.stderr.strip())
finally:pp.write_text(before)
# Check source scope promised for debt matching, without constructing hidden material.
print('DEBT_REFERENCES',{n:b['adr'].count('`'+n+'`') for n in re.findall(r'kỷ luật, 0 cổng · nợ: `([^`]+)`',b['p2-moi'])})
print('G8_SCOPE',next(l for l in spec.splitlines() if l.startswith('| G8 |')))
print('AUDIT_COVERAGE_ROWS',[l.split('|')[1].strip() for l in spec.split('## 15. Điểm audit khác: gộp hay nợ')[1].split('## 16.')[0].splitlines() if l.startswith('| ')][1:])
# Exact deletion-count counterexample; add a harmless pass inside an old function, plus the specified epilog edit.
epilog='9 bảng ADR §20 lệch với docs/adr/'
print('EPILOG_MATCH',src.count(epilog))
changed=src.replace(epilog,'9 bảng ADR §20 hoặc bảng bất biến §1.1 lệch',1).replace('def cmd_doctrine_scan(a, state_dir: Path) -> int:\n','def cmd_doctrine_scan(a, state_dir: Path) -> int:\n    pass  # chỉ để đo giới hạn numstat, không phải bản vá\n',1)
(out/'numstat-before.py.txt').write_text(src);(out/'numstat-after.py.txt').write_text(changed)
p=subprocess.run(['git','diff','--no-index','--numstat',str(out/'numstat-before.py.txt'),str(out/'numstat-after.py.txt')],capture_output=True,text=True)
print('EXISTING_FUNCTION_CHANGED_NUMSTAT',p.returncode,p.stdout.strip())
schema=json.loads((root/'.github/coordination/schemas/review_verdict.v1.schema.json').read_text());print('SCHEMA_V1_PROVIDER',schema['properties']['provider']['enum'],'GENERATION_TYPE',schema['properties']['generation'])
print('CUTOVER_TRUTH_TABLE review_before,head_before,ADR_apply,KN1_union_apply,KN1_intersection_apply')
for review_before,head_before in [(True,True),(True,False),(False,True),(False,False)]:
 print('CUTOVER',review_before,head_before,not review_before,(not review_before or not head_before),(not review_before and not head_before))
# Counts on matching scope, separate registration from applicable Linux inventory.
print('CA_COUNT_REGISTRY',len(pt.CASES),'UNIQUE',len(set(n for n,f in pt.CASES)))
import packet_loop_test_manh as sh
print('CA_COUNT_LINUX',len(sh.ca_dang_ky(pt)))
print('DECLARED_MISSING_WINDOWS',set(n for n,f in pt.CASES)-set(sh.ca_dang_ky(pt)))
