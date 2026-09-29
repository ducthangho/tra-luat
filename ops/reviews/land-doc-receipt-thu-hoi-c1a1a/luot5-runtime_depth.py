import audit as A
import json,sys,time,pathlib,subprocess,traceback
T=A.T
raw=T.ma(T.FIX)
# Sản phẩm HEAD giữ nguyên. Dựng bytes JSON bằng thay literal hex C, không đệ quy json.dumps.
for depth in (900,990,1000,1200,2000,5000):
 nested=b'['*depth+b'0'+b']'*depth
 data=raw
 for k in T.C3:
  old=('"'+k+'": "'+T.S+'"').encode();assert data.count(old)==1
  data=data.replace(old,('"'+k+'": ').encode()+nested)
 dest=A.OUT/('runtime-'+sys.version.split()[0]);dest.mkdir(exist_ok=True)
 p=dest/('C-depth-'+str(depth)+'.json')
 # Each interpreter runs in a separate output directory so no concurrent fixture writes.
 p.write_bytes(data)
 start=time.perf_counter()
 try:q=A.call(A.M,data);api={'ok':q['ok'],'luat':q['luat'],'ly_do':q['ly_do']}
 except Exception as e:api={'exception':type(e).__name__,'message':str(e),'frames':[(f.filename,f.lineno) for f in traceback.extract_tb(e.__traceback__)]}
 try:json.loads(data);parser='parsed'
 except Exception as e:parser=type(e).__name__
 cmd=[sys.executable,'-B',str(A.DEV/'doc_receipt_thu_hoi.py'),'kiem-json','--receipt',str(p),'--kho',T.KHO,'--nhanh-mac-dinh','master','--base-hien-hanh',T.S,'--head-hien-hanh',T.H]
 proc=subprocess.run(cmd,capture_output=True,text=True,timeout=15)
 A.emit(kind='runtime_depth',depth=depth,bytes=len(data),parser=parser,api=api,cli_command=cmd,rc=proc.returncode,stdout=proc.stdout,stderr=proc.stderr,elapsed=time.perf_counter()-start)
