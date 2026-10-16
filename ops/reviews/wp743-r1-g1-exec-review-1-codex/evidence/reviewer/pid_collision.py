exec(open('measure.py').read().split('fail=0')[0])
for tree in ('base','head'):
 m.LAUNCHER_DANG_DUNG=pathlib.Path('/tmp/review743-'+tree+'/.claude/dev/launcher.py')
 original=m.os.getpid
 try:
  m.os.getpid=lambda:int(sys.argv[1])
  with m._co_lap_toan_cuc(): m.t81_chup_cay_windows_thieu_creationdate_phai_fail_closed()
  print(tree,'PASS')
 except m.TinHieuChotCa as e: print(tree,'EXPECTED_CHOT',e)
 finally: m.os.getpid=original
