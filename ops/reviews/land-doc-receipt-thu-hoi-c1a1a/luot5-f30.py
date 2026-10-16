import audit as A
T=A.T
# Nguyên phép F30 trong luot3-supplement.py: chỉ gọi ca thuộc lớp A, không gọi extra khác.
A.suite('debt_stale_message',A.edit('stale, chay lai','fresh, khong can chay lai'),T.ma(T.FIX).replace(T.S.encode(),T.X40.encode()))
for ident in ('M5e','M5f'):
 r=next(r for r in T.DB if r[0]==ident)
 p=A.OUT/(ident+'.py');p.write_text(A.edit(r[3],r[4]));m=A.load(p,ident)
 A.emit(id=ident,baseline=A.target(A.M,A.DEV/'doc_receipt_thu_hoi.py',r[5]),guard=A.target(m,p,'duong_fixture'),target=A.target(m,p,r[5]),disposition=T.chay_dot_bien(A.SRC,r))
