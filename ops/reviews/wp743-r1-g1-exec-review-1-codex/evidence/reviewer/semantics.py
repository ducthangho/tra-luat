exec(open('measure.py').read().split('fail=0')[0])
import errno, os
from pathlib import Path
for root in ('base','head'):
 m.LAUNCHER_DANG_DUNG=Path('/tmp/review743-'+root+'/.claude/dev/launcher.py')
 for err in (OSError(errno.EBADF,'probe'),OSError(errno.ELOOP,'probe'),ValueError('probe')):
  with m._CsSeam([os.getpid()],stat=err,kill_dem=True) as seam:
   try: result=m._tai_launcher_thu()._con_song(os.getpid())
   except BaseException as e: result=type(e).__name__
   print(root,type(err).__name__,getattr(err,'errno',None),result,'stat',seam.n_stat,'read',seam.n_doc,'kill',seam.n_kill)
