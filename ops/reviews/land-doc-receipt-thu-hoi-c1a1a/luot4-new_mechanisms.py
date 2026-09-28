import contextlib,importlib.util,io,pathlib,sys
sys.dont_write_bytecode=True
OUT=pathlib.Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('audit',OUT/'audit.py'); A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
T=A.T
# Actual child process, not a fake CompletedProcess. Keep the valid measurements, then end abnormally.
original_code=T._CON_TINH
original_run=T.subprocess.run
records=[]
def record_run(*a,**kw):
 r=original_run(*a,**kw)
 records.append({'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'command':r.args})
 return r
T.subprocess.run=record_run
try:
 for label,suffix in [('baseline',''),('exit7','\nraise SystemExit(7)\n'),('crash_after_report','\nraise RuntimeError("review-child-failure")\n')]:
  T._CON_TINH=original_code+suffix
  result=A.target(A.M,A.DEV/'doc_receipt_thu_hoi.py','tinh')
  A.emit(kind='child_status',name=label,oracle=result,**records[-1])
finally:
 T._CON_TINH=original_code; T.subprocess.run=original_run
# Use the exact new DB row on the exact unmodified source, then vary only the new tuple shape.
r=next(r for r in T.DB if r[0]=='M1s7')
variants={
 'valid':r,
 'missing_anchor_equal_length':(*r[:3],(*r[3],'MISSING_REVIEW_ANCHOR'),(*r[4],'replacement'),*r[5:]),
 'missing_anchor_truncated':(*r[:3],(*r[3],'MISSING_REVIEW_ANCHOR'),r[4],*r[5:]),
 'replacement_truncated':(*r[:4],(*r[4],'unused replacement'),*r[5:]),
}
for name,row in variants.items():
 A.emit(kind='multi_exact_head',name=name,old_count=len(row[3]),new_count=len(row[4]),disposition=T.chay_dot_bien(A.SRC,row))
# Change only the malformed declaration in a standalone copy of the suite and run its real main.
old=T.DB
try:
 T.DB=[variants['missing_anchor_truncated'] if row[0]=='M1s7' else row for row in old]
 buf=io.StringIO()
 with contextlib.redirect_stdout(buf):rc=T.main()
 A.emit(kind='multi_malformed_suite',rc=rc,output=buf.getvalue())
finally:T.DB=old
