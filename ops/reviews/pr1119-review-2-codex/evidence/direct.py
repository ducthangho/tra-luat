import importlib.util, pathlib, sys, traceback
root=pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/'ops'))
spec=importlib.util.spec_from_file_location('lease_test',root/'ops/lease_publish_test.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
names=sorted(n for n in vars(m) if n.startswith(('t26_','t27_')) and callable(getattr(m,n)))
assert len(names)==3, names
failed=0
for name in names:
    try:getattr(m,name)();print(name+': PASS')
    except Exception:
        failed+=1;print(name+': FAIL');traceback.print_exc()
print(f'{len(names)-failed}/{len(names)} PASS')
sys.exit(bool(failed))
