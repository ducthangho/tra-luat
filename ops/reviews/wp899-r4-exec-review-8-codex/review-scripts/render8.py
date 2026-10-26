import collections, hashlib, json, pathlib
R=pathlib.Path(__file__).resolve().parent
a=json.loads((R/'audit8-results.json').read_text())
notes={
 'Return':'Có: tra_None (2 phép không đổi nguồn được loại đúng).',
 'BoolOp':'Có: and↔or, bỏ từng vế.', 'Compare':'Có: DOI_SO_SANH, từng toán tử trong chuỗi.',
 'Constant':'Một phần: bool, int ±1, chuỗi khác rỗng; None/chuỗi rỗng không có toán tử riêng.',
 'Call':'Một phần: chỉ bỏ đối số khi ≥2 đối số vị trí (14/109 nút); 95 nút còn lại không có toán tử riêng.',
 'comprehension':'Một phần: bỏ if-filter (4/16 nút có filter); không đổi iterable/target.',
 'IfExp':'Có: lấy từng nhánh.', 'If':'Có: cố định test True/False.',
 'UnaryOp':'Một phần: bỏ Not (11/13); USub không có toán tử riêng.',
 'ExceptHandler':'Không. Bỏ RecursionError khỏi tuple bắt lỗi: mutant sống 52/52 và đổi A18 (F10/P2).',
 'Tuple':'Không. Tuple trong ExceptHandler là lỗ đã đo; xem gap8-results.json.',
 'Try':'Không có toán tử riêng; lỗ nhánh bắt lỗi như trên.',
 'Subscript':'Không có toán tử riêng; thử dịch i±1, GIET trong operator probe.',
 'Slice':'Không có toán tử riêng; thử step/reverse/biên động. :1:2 sống nhưng tương đương.',
 'Attribute':'Không có toán tử riêng; thử startswith/endswith, rstrip/lstrip, fullmatch/match, search/match; 2 survivor tương đương.',
 'BinOp':'Không; thử bỏ từng vế (Add/BitOr), không có survivor phân biệt được.',
 'AugAssign':'Không; đổi cộng thành trừ bị giết.',
 'NamedExpr':'Không; hai thay đổi h:=a/z bị giết; các binding khác chưa thử riêng.',
 'Name':'Không; thử đổi any/all tại tên hàm gọi, bị giết.',
 'For':'Không; các mẫu số bước/thứ tự được đo qua tests; chưa thử toán tử For riêng.',
 'Continue':'Không; chưa thử xóa Continue riêng.',
 'keyword':'Không; key= của sorted chưa thử riêng.',
 'Load':'Nút context, không có toán tử riêng.', 'Store':'Nút context, không có toán tử riêng.',
 'And':'Được đổi qua BoolOp.', 'Or':'Được đổi qua BoolOp.', 'Not':'Được bỏ qua UnaryOp.',
 'Eq':'Được đổi qua Compare.', 'NotEq':'Được đổi qua Compare.', 'Is':'Được đổi qua Compare.', 'IsNot':'Được đổi qua Compare.', 'In':'Được đổi qua Compare.', 'NotIn':'Được đổi qua Compare.', 'LtE':'Được đổi qua Compare.',
 'Add':'Không có toán tử số học riêng; probe BinOp/AugAssign ở trên.',
 'Sub':'Không có toán tử riêng; probe giữ từng vế BinOp.', 'BitOr':'Không có toán tử riêng; probe giữ từng vế BinOp.', 'USub':'Không có toán tử riêng (hằng int con vẫn được đổi).',
}
table=['| kiểu AST | số nút | toán tử / phép đo |','|---|---:|---|']
for k,v in sorted(a['counts'].items()):table.append(f'| `{k}` | {v} | {notes.get(k,"Không có toán tử riêng; các nút con có thể được đột biến. Chưa có mutant sống phân biệt được được chứng minh cho riêng kiểu này.")} |')
(R/'ast-table8.md').write_text('\n'.join(table)+'\n')
closed=json.loads((R/'closed8-results.json').read_text());selection=json.loads((R/'closed8-selection.json').read_text())
summary={'measured':len(closed),'ranks':dict(collections.Counter(x['rank'] for x in closed)),'per_function':dict(collections.Counter(x['id'].split('#')[0] for x in closed)),'sample_count':len(selection['sample']),'sample_missing':sorted(set(selection['sample'])-set(x['id'] for x in closed)),'initial_not_killed':len(selection['initial_not_killed']),'initial_missing':sorted(set(selection['initial_not_killed'])-set(x['id'] for x in closed)),'unmeasured_count':1009-len(closed),'zero_process_failures':all(x['process_rc']==0 for x in closed)}
(R/'summary8.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))
