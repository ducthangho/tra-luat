import os, sys, subprocess, pathlib, importlib.util, contextlib, io, json, hashlib, tarfile
K=pathlib.Path('/home/user/rv773'); O=pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('t',K/'ops/land_evidence_nguon_test.py'); t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
def run(args, name, env=None):
 r=subprocess.run(args,capture_output=True,text=True,env=env); (O/(name+'.log')).write_text(r.stdout+r.stderr); print(name, 'rc=',r.returncode, (r.stdout+r.stderr)[-350:]); return r
run([sys.executable,'-B',str(K/'ops/land_evidence_nguon.py'),'--root',str(K)],'tree')
for c in ['c6e2401','1a4c417','d60b9e6']:
 root=pathlib.Path('/tmp/rv773-r6-history')/c; root.mkdir(parents=True,exist_ok=True)
 r=subprocess.run(['git','-C',str(K),'archive',c,'ops/land'],capture_output=True); print('archive',c,r.returncode)
 import io as i
 with tarfile.open(fileobj=i.BytesIO(r.stdout)) as a:a.extractall(root,filter='data')
 run([sys.executable,'-B',str(K/'ops/land_evidence_nguon.py'),'--root',str(root),'--tep','ops/land/pr765-wp743-land-evidence.yaml'],'history-'+c)
m=t.nap(); m.MIEN_TRU_CUTOVER={}
rc, out=t.kiem(m,K); (O/'no-exemption.log').write_text(out); print('no-exemption',rc,out[-200:])
paths=subprocess.check_output(['git','-C',str(K),'ls-tree','-r','--name-only','c73af7b','ops/land'],text=True).splitlines()
ds={pathlib.Path(p).name:hashlib.sha256(subprocess.check_output(['git','-C',str(K),'show','c73af7b:'+p])).hexdigest() for p in paths if p.endswith('-land-evidence.yaml')}
print('independent-cutover',len(ds),hashlib.sha256(json.dumps(sorted(ds.items())).encode()).hexdigest())
src=(K/'ops/land_evidence_nguon.py').read_text()
for name,replacement in [('reverse','(goc, goc / THU_MUC, prov)'),('middle-first','(goc / THU_MUC, prov, goc)'),('root-before-middle','(prov, goc, goc / THU_MUC)')]:
 ma=pathlib.Path('/tmp/rv773-r6-'+name+'.py'); ma.write_text(src.replace('(prov, goc / THU_MUC, goc)',replacement)); env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(ma),PYTHONDONTWRITEBYTECODE='1')
 for ca in t.CA:
  r=run([sys.executable,'-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca',ca],name+'-'+ca,env)
 for loc, ptxt, ltxt, rtxt in [('prov-vs-land','2/2','1/1','1/1'),('land-vs-root',None,'2/2','1/1')]:
  with t.cay("positive: '1/1'\nnguon_positive: r.txt\n",{'r.txt':ptxt} if ptxt else {}) as root:
   (root/'ops/land/r.txt').write_text(ltxt); (root/'r.txt').write_text(rtxt)
   head_rc,head_out=t.kiem(t.nap(),root)
   r=run([sys.executable,'-B',str(ma),'--root',str(root)],name+'-'+loc)
   print('priority A/B',name,loc,'head',head_rc,'mutant',r.returncode)
# probes without composing escape tokens
probes=[('numeric-positive',"positive: 123\nnguon_positive: r.txt\n",{'r.txt':'nothing'}),('fractional',"pre_merge_checks: ['2026-10-16T02:58:26.1Z']\n",{'readback-pr-9001.json':t.RB_PR}),('offset-quoted',"pre_merge_checks: ['2026-10-16T03:58:26+01:00']\n",{'readback-pr-9001.json':t.RB_PR}),('dict-key',"pre_merge_checks: {'2026-10-16T02:59:00Z': ok}\n",{'readback-pr-9001.json':t.RB_PR}),('internal-symlink',"x: 'measured - link.txt'\n",{'r.txt':'data'}),('non-string-source',"positive: '1/1'\nnguon_positive: 123\n",{'r.txt':'1/1'}),('duplicate',"x: 'measured - missing'\nx: ok\n",{}),('glob',"x: 'measured - *.txt'\n",{'r.txt':'data'}),('directory',"x: 'measured - sub/'\n",{'sub/r.txt':'data'})]
for name, hs, prov in probes:
 with t.cay(hs,prov) as root:
  if name=='internal-symlink':(root/'ops/land'/t.PROV/'link.txt').symlink_to('r.txt')
  rc,out=t.kiem(t.nap(),root); (O/('probe-'+name+'.log')).write_text(out); print('probe',name,rc,out[-180:])
# independent rename mutation
ma=pathlib.Path('/tmp/rv773-r6-rename.py'); ma.write_text(src.replace('"plat-x8-land-evidence.yaml":','"plat-x9-land-evidence.yaml":'))
run([sys.executable,'-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca','c10_l5_danh_sach_dong_bang'],'rename',dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(ma)))
