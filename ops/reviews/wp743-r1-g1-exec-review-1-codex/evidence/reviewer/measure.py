import importlib.util, pathlib, sys, tempfile
p=pathlib.Path('/tmp/review743-head/.claude/dev/launcher_test.py')
s=importlib.util.spec_from_file_location('lt',p); m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
names=['r743_con_song_tham_do_bang_stat_giu_errno_moi_phien_ban','t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan','t157_giet_cay_khi_stat_EACCES_van_tron_ven','t117_moi_mau_dot_bien_phai_khop_DUNG_MOT_cho']
fail=0
for name in names:
 try:
  with m._co_lap_toan_cuc(): getattr(m,name)()
  print('TARGET PASS',name,flush=True)
 except BaseException as e: print('TARGET FAIL',name,type(e).__name__,str(e),flush=True);fail+=1
source=m.LAUNCHER.read_text()
with tempfile.TemporaryDirectory(prefix='r743-mut-') as td:
 for item in m.DOT_BIEN:
  name, pairs, targets=item[:3]
  if not name.startswith(('wp685_','r743_')): continue
  if isinstance(pairs,tuple): pairs=[pairs]
  code=source
  for old,new in pairs:
   assert code.count(old)==1,(name,code.count(old))
   code=code.replace(old,new,1)
  path=pathlib.Path(td)/(name+'.py');path.write_text(code);m.LAUNCHER_DANG_DUNG=path
  if name=='r743_a_ve_lai_exists': targets=targets+[names[1]]
  for target in targets:
   try:
    with m._co_lap_toan_cuc(): getattr(m,target)()
    print('SURVIVE',name,target,flush=True);fail+=1
   except m.TinHieuChotCa as e: print('KILL_CHOT',name,target,str(e),flush=True)
   except BaseException as e: print('FALSE_CREDIT',name,target,type(e).__name__,str(e),flush=True);fail+=1
print('FAILURES',fail,flush=True)
sys.exit(bool(fail))
