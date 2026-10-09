import importlib.util
import pathlib
import sys
sys.dont_write_bytecode=True
OUT=pathlib.Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('audit',OUT/'audit.py');A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
T=A.T
row=next(r for r in T.DB if r[0]=='M2b3')
# Same decoding semantics at the original guarded location, different spelling.
# Copy the declared anchor exactly once into an unrelated diagnostic AFTER K1 is already recorded red.
start=A.SRC.index('            chuoi = raw.decode(')
end=A.SRC.index('    loi = [f')
old=A.SRC[start:end]
new=old.replace('chuoi = raw.decode("utf-8", "strict")','chuoi = raw.decode(encoding="utf-8", errors="strict")')
new=new.replace('    if loi:\n','    if loi:\n        chuoi = raw.decode("utf-8", "strict")\n')
r=(*row[:2],'same_line_wrong_phase',old,new,row[5],row[6])
source=A.edit(old,new)
p=OUT/'same_line_wrong_phase.py';p.write_text(source);m=A.load(p,'wrong_phase')
events=[]
def trace(frame,event,arg):
    if frame.f_code.co_filename==str(p) and event=='exception':
        events.append({'line':frame.f_lineno,'exception':arg[0].__name__,'luat':dict(frame.f_locals.get('luat',{})),'loi':list(frame.f_locals.get('loi',[]))})
    return trace
sys.settrace(trace)
try: target=A.target(m,p,'byte_0x80')
finally:sys.settrace(None)
A.emit(kind='stage_credit',baseline=A.target(A.M,A.DEV/'doc_receipt_thu_hoi.py','byte_0x80'),positive=A.target(m,p,'duong_fixture'),target=target,original_catches_preserved=A.SRC.count('except UnicodeDecodeError:')==source.count('except UnicodeDecodeError:'),anchor_lines=[i for i,l in enumerate(source.splitlines(),1) if l.strip()==row[6][1]],events=events,disposition=T.chay_dot_bien(A.SRC,r))
# All four positive output-shape rows can have an actual positive control, using an existing alternative positive input.
for ident,field,replacement in [('M1o2','"ok": all(v == "qua" for v in luat.values())','"ok": (1 if r["checkout_commit"] == '+repr(T.X40)+' else all(v == "qua" for v in luat.values()))'),
                              ('M1u2','"luat": luat','"luat": (list(luat.items()) if r["checkout_commit"] == '+repr(T.X40)+' else luat)'),
                              ('M1w3','"ly_do": ly_do','"ly_do": (tuple(ly_do) if r["checkout_commit"] == '+repr(T.X40)+' else ly_do)'),
                              ('M1x2','"ly_do": ly_do','"ly_do": ly_do, **({"extra": 1} if r["checkout_commit"] == '+repr(T.X40)+' else {})')]:
    old=T._TRA;new=old.replace(field,replacement)
    r=(ident,'positive shape with A1','scoped_'+ident,old,new,'duong_c_khac_s',None)
    A.emit(kind='a1_alternative',id=ident,target='duong_c_khac_s',guard='duong_fixture',disposition=T.chay_dot_bien(A.SRC,r))
