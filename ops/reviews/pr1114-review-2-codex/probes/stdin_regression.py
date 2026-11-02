import ast,importlib.util,json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parents[1]
old=subprocess.check_output(['git','-C',str(root/'cay-kho'),'show','e101b11:ops/cloud_agent_creds_test.py']).decode()
new=(root/'work/head/ops/cloud_agent_creds_test.py').read_text()
def extract(s):
 nodes=ast.parse(s).body
 return {n.name:ast.dump(n,include_attributes=False) for n in nodes if isinstance(n,ast.FunctionDef) and n.name in ('chay_b','p3b4_co_blob')} | {n.targets[0].id:ast.dump(n.value,include_attributes=False) for n in nodes if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('JS_GIA','JS_CHAY')}
assert extract(old)==extract(new)
print('ROUND1_STDIN_CODE_IDENTICAL=True')
rows=[]
for variant in ('base','head'):
 spec=importlib.util.spec_from_file_location('review_test_'+variant,root/'work'/variant/'ops/cloud_agent_creds_test.py')
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 real=subprocess.run;calls=[]
 def limited(argv,*a,**kw):
  units=len(subprocess.list2cmdline(argv).encode('utf-16-le'))//2+1
  calls.append(dict(argc=len(argv),units=units,input_bytes=len(kw.get('input',b''))))
  if units>32767:return subprocess.CompletedProcess(argv,206,b'',b'REVIEW_LIMIT_32767')
  return real(argv,*a,**kw)
 subprocess.run=limited
 try: rc,output=m.chay_ca('p3b4_co_blob')
 finally: subprocess.run=real
 row=dict(variant=variant,rc=rc,output=output,calls=calls);rows.append(row)
 print(json.dumps(row,ensure_ascii=False))
assert rows[0]['rc']==3 and rows[1]['rc']==0
(root/'evidence/stdin-regression.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
