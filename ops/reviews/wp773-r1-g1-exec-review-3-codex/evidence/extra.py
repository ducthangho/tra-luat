import importlib.util,pathlib,subprocess,os
from unittest.mock import patch
K=pathlib.Path('/home/user/rv773'); SP=pathlib.Path.cwd().parent
s=importlib.util.spec_from_file_location('t',K/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
for v in ['3.11','3.12','3.13','3.14']:
 for name,hs in [('merge_duplicate',"x: {<<: {a: 'measured — khong', a: ok}}\n"),('unquoted_date','x: 2026-02-30\n')]:
  with t.cay(hs,{'a.json':'{}'}) as g:
   r=subprocess.run(['python'+v,'-B',str(K/'ops/land_evidence_nguon.py'),'--root',str(g)],capture_output=True,text=True,env=dict(os.environ,PYTHONPATH=str(SP/('yaml-python'+v))))
  print('CROSS_VERSION',v,name,r.returncode,r.stdout[-200:],r.stderr.splitlines()[-1:] )
# Existing official cases all miss source read error branch.
for ca in t.CA:
 r=subprocess.run(['python3.13','-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca',ca],capture_output=True,text=True,env=dict(os.environ,LAND_EVIDENCE_NGUON_MA='/tmp/rv773-r3-read_error_green.py'))
 print('READ_ERROR_MUTATION',ca,r.returncode,r.stdout.strip())
for ma in [K/'ops/land_evidence_nguon.py',pathlib.Path('/tmp/rv773-r3-read_error_green.py')]:
 ss=importlib.util.spec_from_file_location('m',ma);m=importlib.util.module_from_spec(ss);ss.loader.exec_module(m)
 with t.cay('positive: 1/1\nnguon_positive: a.txt\n',{'a.txt':'1/1'}) as g:
  old=pathlib.Path.read_bytes
  def read(p):
   if p.name=='a.txt':raise OSError('review controlled source read failure')
   return old(p)
  with patch.object(pathlib.Path,'read_bytes',read): r=t.kiem(m,g)
  print('CONTROLLED_READ_ERROR',str(ma),r)
# Internal symlink and relative resolution order (no out-of-tree path created).
with t.cay("x: 'measured — link.json'\npositive: 1/1\nnguon_positive: a.txt\n",{'a.json':'{}','a.txt':'1/1'}) as g:
 prov=g/'ops/land'/t.PROV
 (prov/'link.json').symlink_to(prov/'a.json')
 (g/'ops/land/a.txt').write_text('0/1')
 print('INTERNAL_SYMLINK_AND_PRECEDENCE',t.kiem(t.nap(),g))
