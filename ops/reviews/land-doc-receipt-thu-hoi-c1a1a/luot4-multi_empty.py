import importlib.util,pathlib,sys
sys.dont_write_bytecode=True
p=pathlib.Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('audit',p/'audit.py');A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
r=next(r for r in A.T.DB if r[0]=="M2b'")
row=(*r[:3],(),(),*r[5:])
A.emit(kind='empty_multi',old_count=0,new_count=0,source_changed=False,disposition=A.T.chay_dot_bien(A.SRC,row))
