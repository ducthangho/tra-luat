import audit as A
import contextlib,io,sys,pathlib,tempfile,json
T=A.T
if sys.argv[2]=='limit':
 r=next(r for r in T.DB if r[0]=='M2j')
 with tempfile.TemporaryDirectory() as td:
  p=pathlib.Path(td)/'m.py';p.write_text(A.edit(r[3],r[4]));m=A.load(p,'limit_mutant')
  A.emit(kind='limit_credit',actual_limit=sys.get_int_max_str_digits(),suite_limit=T.LIM,baseline=A.target(A.M,A.DEV/'doc_receipt_thu_hoi.py','so_dai_vuot'),mutant=A.target(m,p,'so_dai_vuot'),disposition=T.chay_dot_bien(A.SRC,r))
elif sys.argv[2]=='wording':
 old='[f"{k} stale';new='[f"{k} receipt stale'
 with tempfile.TemporaryDirectory() as td:
  p=pathlib.Path(td)/'m.py';p.write_text(A.edit(old,new));m=A.load(p,'wording')
  raw=T.ma(T.FIX);params=dict(kho=T.KHO,nhanh='master',base_hien_hanh=T.X40,head_hien_hanh=T.H)
  A.emit(kind='valid_wording',baseline=A.M.kiem_json(raw,**params),alternative=m.kiem_json(raw,**params),guard=A.target(m,p,'duong_fixture'),oracle=A.target(m,p,'k4_base'))
elif sys.argv[2]=='receipt':
 p=A.ROOT.parent/'receipt589_for_review.json';raw=p.read_bytes();d=json.loads(raw)
 A.emit(kind='real_receipt',fixture_equal=d==T.FIX,result=A.call(A.M,raw))
 r=T._cli(A.DEV/'doc_receipt_thu_hoi.py',raw,{})
 A.emit(kind='real_receipt_cli',rc=r.returncode,stdout=r.stdout,stderr=r.stderr)
