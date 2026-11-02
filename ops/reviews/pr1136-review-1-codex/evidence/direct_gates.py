import importlib.util, pathlib, sys, traceback
root=pathlib.Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/'ops'))
s=importlib.util.spec_from_file_location('audit_lease_tests',root/'ops/lease_publish_test.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
names=sorted(n for n in vars(m) if n.startswith(('t26_','t27_')) and callable(getattr(m,n)))
failed=0
for n in names:
 try:getattr(m,n)();print(n,'PASS',flush=True)
 except Exception as e:failed+=1;print(n,'FAIL',str(e),flush=True)
print(f'DIRECT total={len(names)} failed={failed}');sys.exit(bool(failed))
