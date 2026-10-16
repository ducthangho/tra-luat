import importlib.util,json,os,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
def probe():
 try: json.loads('1'*4500);return 'parsed_4500'
 except Exception as e:return type(e).__name__
def snapshot():
 cmd=[sys.executable,'-B','-c','import sys,json; print(json.dumps({"child_limit":sys.get_int_max_str_digits()}))']
 r=subprocess.run(cmd,capture_output=True,text=True)
 return dict(limit=sys.get_int_max_str_digits(),env=os.environ.get('PYTHONINTMAXSTRDIGITS'),parse=probe(),child=json.loads(r.stdout),child_rc=r.returncode)
before=snapshot()
p=root/'.claude/dev/doc_receipt_thu_hoi_test.py';sp=importlib.util.spec_from_file_location('receipt_test',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
after=snapshot()
print(json.dumps(dict(before=before,after_import=after,called_main=False)))
# Observe existing helper child startup config, without changing product source.
run=subprocess.run;seen=[]
def traced(cmd,*args,**kw):
 env=kw.get('env',os.environ)
 p=run([cmd[0],'-B','-c','import sys; print(sys.get_int_max_str_digits())'],env=env,capture_output=True,text=True)
 seen.append(dict(argv=cmd[:3],effective_env_limit=env.get('PYTHONINTMAXSTRDIGITS'),child_limit=p.stdout.strip(),probe_rc=p.returncode))
 return run(cmd,*args,**kw)
m.subprocess.run=traced
try:
 sp=importlib.util.spec_from_file_location('receipt_module',root/'.claude/dev/doc_receipt_thu_hoi.py');prod=importlib.util.module_from_spec(sp);sp.loader.exec_module(prod)
 m.ca_cli('cli',m.MODUN,prod);m.ca_tinh('tinh',prod)
 print(json.dumps(dict(real_helper_controls='pass',children=seen)))
finally:m.subprocess.run=run
