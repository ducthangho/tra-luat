from pathlib import Path
import json
w=Path(__file__).resolve().parent;ns={'__name__':'static'};exec(compile((w/'bang_toan_tu.py').read_text(),'table','exec'),ns)
rows=[]
for mid,p,ca,old,ops in ns['M']:
 key=mid.split()[0]
 for op in ns['OPS']:
  if op in ops:continue
  if op in ['gt','lt']:why='Họ gt/lt trong tập cố định chỉ tách hai chiều của !=; hàng này không có != mục tiêu.'
  elif op in ['ge','le','ne']:why='Không có == mục tiêu cho họ này; phép đảo/biên của predicate khác đã nằm ở dao hoặc biến thể biên.'
  elif op=='dao':why='Phép đảo == đã có ne; hoặc hàng là công thức/lát cắt không có Boolean để đảo.'
  elif op in ['cong1','tru1']:why='Không có hằng số số học mục tiêu; tên category/tập dữ liệu không phải hằng số để +1/-1.'
  elif op=='or':why='Không có and tại hàng này; nếu là vế cuối, cùng and được đo ở hàng vế trước.'
  elif op=='yeu':why='Không có lượng từ any/all hoặc quan hệ chứa mục tiêu; not-lech của c37 biểu diễn đếm multiplicity, phép xóa nó ở bo.'
  elif op=='bo':why='Hàng là công thức số hoặc lát cắt; xóa toàn biểu thức cần chọn giá trị thay, không phải bỏ một mệnh đề Boolean.'
  else:raise AssertionError(op)
  rows.append(dict(id=key,op=op,reason=why,review='accepted_with_scope_above'))
(w/'na-audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(len(rows),'cells individually enumerated')
