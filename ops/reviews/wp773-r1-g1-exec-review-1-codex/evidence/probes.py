import sys,importlib.util,pathlib,json,subprocess,tempfile
sys.dont_write_bytecode=True
p='/home/user/rv773/ops/land_evidence_nguon_test.py'
s=importlib.util.spec_from_file_location('t',p); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
pv={'a.json':'{}','readback-pr-9001.json':t.RB_PR}
cases={
'duplicate_key':("x: 'measured — khong nguon'\nx: ok\n",pv),
'pmc_dict_key':("pre_merge_checks:\n  '2026-10-16T02:59:00Z': ok\n",pv),
'fraction':("pre_merge_checks: ['2026-10-16T02:58:26.100Z']\n",pv),
'offset_quoted':("pre_merge_checks: ['2026-10-16T02:59:00+00:00']\n",pv),
'offset_unquoted':("pre_merge_checks: [2026-10-16T02:59:00+00:00]\n",pv),
'positive_number':("positive: 123\nnguon_positive: a.json\n",pv),
'bad_date':("pre_merge_checks: ['2026-99-16T02:59:00Z']\n",pv),
'nonstring':('x: 123\n',pv),
'list_key':('? [a,b]\n: ok\n',pv),
}
for name,(hs,pr) in cases.items():
 try:
  rc,ra=t.chay(hs,pr); print(name,'rc=',rc,ra.strip(),sep='\n')
 except Exception as e: print(name,'EXCEPTION',type(e).__name__,str(e))
with t.cay("x: 'measured — *.json'\n",{}) as root:
 (root/'ops/land'/t.PROV/'folder.json').mkdir()
 print('glob_directory',t.kiem(t.nap(),root))
# Uncovered mutation: suppress all L2 content checking; whole target must turn red.
source=pathlib.Path('/home/user/rv773/ops/land_evidence_nguon.py').read_text()
mutations={
 'l2_content':('if not any(mau.search(nd) for nd in noi_dung):','if False:' ,'c05_l2_luot2_positive_phai_co_nguon_chua_nguyen_van'),
 'dict_walk':('list(pmc.values()) if isinstance(pmc, dict)','[] if isinstance(pmc, dict)','c06_l3_luot2_moc_sau_merged_at'),
 'glob_file':('and x.exists()]','and x.is_file()]','c02_l1_glob_va_thu_muc'),
 'rename_allowlist':('plat-x8-land-evidence.yaml','plat-x9-land-evidence.yaml','c10_l5_danh_sach_dong_bang'),
}
for name,(old,new,ca) in mutations.items():
 assert source.count(old)==1
 dest=pathlib.Path('/tmp/rv773-review')/(name+'.py');dest.write_text(source.replace(old,new))
 rc,ra=t.chay_con(ca,dest);print('MUTATION',name,'rc=',rc,ra.strip())
