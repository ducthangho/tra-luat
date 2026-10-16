import importlib.util,pathlib,sys
sys.dont_write_bytecode=True
out=pathlib.Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('audit',out/'audit.py');A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
T=A.T
real_run=T.subprocess.run
children=[]
def recording(*args, **kwargs):
 r=real_run(*args, **kwargs)
 children.append({'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 return r
T.subprocess.run=recording
old=T._DAU
new=old+'\n    if raw == b"{":\n        raise RuntimeError("review-unrelated-error")'
source=A.edit(old,new); p=out/'unrelated_error.py';p.write_text(source);m=A.load(p,'unrelated_error')
row=('REVIEW','pure-process error must not become purity evidence','unrelated_error',old,new,'tinh',None)
A.emit(kind='purity_unrelated_exception',baseline=A.target(A.M,A.DEV/'doc_receipt_thu_hoi.py','tinh'),guard=A.target(m,p,'duong_fixture'),target=A.target(m,p,'tinh'),disposition=T.chay_dot_bien(A.SRC,row))
A.emit(kind='purity_child_processes',processes=children)
