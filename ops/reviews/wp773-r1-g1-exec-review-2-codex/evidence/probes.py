import sys, pathlib, importlib.util, subprocess, os, json, hashlib
sys.dont_write_bytecode=True
K=pathlib.Path('/home/user/rv773')
s=importlib.util.spec_from_file_location('t', K/'ops/land_evidence_nguon_test.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
cases={
 'duplicate': "x: 'measured — khong nguon'\nx: ok\n",
 'duplicate_null': "null: 'measured — khong nguon'\nnull: ok\n",
 'set_string': "x: !!set {'measured — khong nguon': null}\n",
 'omap_string': "x: !!omap [{a: 'measured — khong nguon'}]\n",
 'unhashable': "? [a, b]\n: ok\n",
 'alias': "a: &n {x: 'measured — khong nguon'}\nb: *n\n",
 'merge_ok': "a: &n {x: 1}\nb: {<<: *n, x: 2, y: 'measured — a.json'}\n",
 'pmc_key': "pre_merge_checks: {'2026-10-16T02:59:00Z': ok}\n",
 'bad_date': "pre_merge_checks: ['2026-99-16T02:59:00Z']\n",
 'fraction': "pre_merge_checks: ['2026-10-16T02:59:00.1Z']\n",
 'offset_quoted': "pre_merge_checks: ['2026-10-16T02:59:00+00:00']\n",
 'positive_num': "positive: 123\nnguon_positive: a.json\n",
 'positive_bad_source': "positive: '195/195'\nnguon_positive: [123]\n",
}
for name,hs in cases.items():
 with t.cay(hs, {'a.json':'{}','readback-pr-9001.json':t.RB_PR}) as g:
  r=subprocess.run(['python3.13','-B',str(K/'ops/land_evidence_nguon.py'),'--root',str(g)],capture_output=True,text=True)
  print(name,'RC',r.returncode,'\n'+r.stdout+r.stderr)
for name,rb in [('absent',None),('null','{"merged_at":null}'),('neighbor',None)]:
 p={} if name=='absent' else {'readback-pr-9002.json':t.RB_PR} if name=='neighbor' else {'readback-pr-9001.json':rb}
 print('readback_'+name,t.chay("pre_merge_checks: ['2026-10-16T02:59:00Z']\n",p))
with t.cay("x: 'measured - *.json'\n",{'a.txt':''}) as g:
 (g/'ops/land'/t.PROV/'folder.json').mkdir()
 print('glob_directory',t.kiem(t.nap(),g))
with t.cay("x: 'measured - link.json'\n",{'a.json':'{}'}) as g:
 (g/'ops/land'/t.PROV/'link.json').symlink_to('a.json')
 print('symlink_internal',t.kiem(t.nap(),g))
m=t.nap(); m.MIEN_TRU_CUTOVER={}
print('NO_EXEMPT',t.kiem(m,K))
a=subprocess.run(['git','-C',str(K),'ls-tree','-r','--name-only','c73af7b','ops/land'],capture_output=True,text=True)
ds={}
for p in a.stdout.splitlines():
 if p.endswith('-land-evidence.yaml'):
  b=subprocess.run(['git','-C',str(K),'show','c73af7b:'+p],capture_output=True,check=True).stdout
  ds[pathlib.Path(p).name]=hashlib.sha256(b).hexdigest()
print('independent_fingerprint',len(ds),hashlib.sha256(json.dumps(sorted(ds.items())).encode()).hexdigest())
# Bỏ một chốt chỉ ở bản sao, chạy MỌI ca để tìm nhánh không được canh.
source=(K/'ops/land_evidence_nguon.py').read_text()
mutations={
 'null_duplicate_fix': ('if khoa is not None and khoa in da:', 'if k.tag != "tag:yaml.org,2002:merge" and khoa in da:'),
 'l2_no_content': ('if not any(mau.search(nd) for nd in noi_dung):','if False:'),
 'l3_null_skip': ('if (v := d.get("merged_at") if isinstance(d, dict) else None) is None and (not so or not t.exists()):','if (v := d.get("merged_at") if isinstance(d, dict) else None) is None:'),
 'rename_exempt': ('"plat-x8-land-evidence.yaml":','"plat-x9-land-evidence.yaml":'),
}
for name,(old,new) in mutations.items():
 assert source.count(old)==1
 p=pathlib.Path('/tmp/rv773-'+name+'.py'); p.write_text(source.replace(old,new))
 for ca in t.CA:
  if name=='null_duplicate_fix' and not ca.startswith('c08'): continue
  if name=='l2_no_content' and not ca.startswith('c05'): continue
  if name=='rename_exempt' and not ca.startswith('c10'): continue
  r=subprocess.run(['python3.13','-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca',ca],env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(p),PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
  print('MUTATION',name,ca,r.returncode,r.stdout.strip(),r.stderr[-100:])
