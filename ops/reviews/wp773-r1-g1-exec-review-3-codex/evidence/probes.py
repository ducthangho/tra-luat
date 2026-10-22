import importlib.util, pathlib, subprocess, os, hashlib, json, contextlib, io
K=pathlib.Path('/home/user/rv773')
s=importlib.util.spec_from_file_location('t',K/'ops/land_evidence_nguon_test.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
def probe(name,hs,p=None):
 with t.cay(hs,{'a.json':'{}'} if p is None else p) as g:
  r=subprocess.run(['python3.13','-B',str(K/'ops/land_evidence_nguon.py'),'--root',str(g)],capture_output=True,text=True)
 print(name,repr(hs),'RC',r.returncode,'\n'+r.stdout+r.stderr)
for name,hs in [
 ('null_root',"null: 'measured — khong'\n~: ok\n"),
 ('set',"x: !!set {'measured — khong': null}\n"),
 ('omap',"x: !!omap [{a: 'measured — khong'}]\n"),
 ('pairs',"x: !!pairs [{a: 'measured — khong'}]\n"),
 ('binary',"x: !!binary bWVhc3VyZWQgLSBraG9uZw==\n"),
 ('merge_duplicate',"x: {<<: {a: 'measured — khong nguon', a: ok}}\n"),
 ('merge_null_duplicate',"x: {<<: {null: 'measured — khong nguon', null: ok}}\n"),
 ('merge_control_bad',"x: {<<: {a: 'measured — khong nguon'}}\n"),
 ('merge_control_good',"x: {<<: {a: 'measured — a.json'}}\n"),
 ('unquoted_bad_date',"pre_merge_checks: [2026-99-16T02:00:00Z]\n"),
 ('unquoted_bad_date_plain',"x: 2026-02-30\n"),
 ('positive_number',"positive: 123\nnguon_positive: a.json\n")]: probe(name,hs)
probe('fraction',"pre_merge_checks: ['2026-10-16T02:58:26.5Z']\n",{'readback-pr-9001.json':t.RB_PR})
probe('offset_quoted',"pre_merge_checks: ['2026-10-16T03:58:26+01:00']\n",{'readback-pr-9001.json':t.RB_PR})
probe('neighbor',"pre_merge_checks: ['2026-10-16T03:58:26Z']\n",{'readback-pr-9002.json':t.RB_PR})
probe('null_readback',"pre_merge_checks: ['2026-10-16T02:00:00Z']\n",{'readback-pr-9001.json':t.RB_PR.replace('"2026-10-16T02:58:26Z"','null')})
m=t.nap();m.MIEN_TRU_CUTOVER={}
print('NO_EXEMPT',t.kiem(m,K))
files=subprocess.check_output(['git','-C',str(K),'ls-tree','-r','--name-only','c73af7b','ops/land'],text=True).splitlines()
ds={pathlib.Path(f).name:hashlib.sha256(subprocess.check_output(['git','-C',str(K),'show','c73af7b:'+f])).hexdigest() for f in files if f.endswith('-land-evidence.yaml')}
print('FINGERPRINT',len(ds),hashlib.sha256(json.dumps(sorted(ds.items())).encode()).hexdigest())
for name,cu,moi,ca in t.DOT_BIEN:
 if name in ['F01_null_lam_dau_bo_qua','F05_bo_tu_choi_kieu_la','L3_readback_null_bo_qua']:
  print('TARGET_MUTATION',name,t.chay_dot_bien(name,cu,moi,ca))
# Additional meaningful mutation not in official matrix.
src=(K/'ops/land_evidence_nguon.py').read_text()
for name,cu,moi,ca in [
 ('content_l2','if not any(mau.search(nd) for nd in noi_dung):','if False:','c05_l2_luot2_positive_phai_co_nguon_chua_nguyen_van'),
 ('read_error_green','raise KhongDoDuoc(f"đọc nguon_positive: {e}")','return [], []','c05_l2_luot2_positive_phai_co_nguon_chua_nguyen_van'),
 ('rename_exempt','plat-x8-land-evidence.yaml','plat-x9-land-evidence.yaml','c10_l5_danh_sach_dong_bang')]:
 assert src.count(cu)==1
 p=pathlib.Path('/tmp/rv773-r3-'+name+'.py');p.write_text(src.replace(cu,moi))
 r=subprocess.run(['python3.13','-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca',ca],env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(p)),text=True,capture_output=True)
 print('EXTRA_MUTATION',name,'RC',r.returncode,r.stdout,r.stderr)
