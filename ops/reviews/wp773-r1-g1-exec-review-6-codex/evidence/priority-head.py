import importlib.util, pathlib,sys
sys.dont_write_bytecode=True
p=pathlib.Path('/home/user/rv773/ops/land_evidence_nguon_test.py');s=importlib.util.spec_from_file_location('t',p);t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
for name,pr,la,ro in [('prov-vs-land','2/2','1/1','1/1'),('land-vs-root',None,'2/2','1/1')]:
 with t.cay("positive: '1/1'\nnguon_positive: r.txt\n",{'r.txt':pr} if pr else {}) as root:
  (root/'ops/land/r.txt').write_text(la);(root/'r.txt').write_text(ro)
  rc,out=t.kiem(t.nap(),root); print(name,'rc=',rc);print(out)
