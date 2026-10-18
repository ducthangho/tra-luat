import importlib.util, pathlib, sys
sys.dont_write_bytecode=True
s=importlib.util.spec_from_file_location('t','/home/user/rv773/ops/land_evidence_nguon_test.py')
t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
def null_key():
 t.ky("null: 'measured — khong nguon'\nnull: ok\n",{'a.json':'{}'},2,'khoá null trùng phải bị từ chối','khoá trùng')
def collections():
 for hs in ["x: !!set {'measured — khong nguon': null}\n", "x: !!omap [{a: 'measured — khong nguon'}]\n"]:
  t.ky(hs,{'a.json':'{}'},1,'mọi chuỗi YAML phải qua L1','L1')
t.CA.update(r01_null_key=null_key,r02_collections=collections)
rc,line=t.chay_ca(sys.argv[2]); print(line); sys.exit(rc)
