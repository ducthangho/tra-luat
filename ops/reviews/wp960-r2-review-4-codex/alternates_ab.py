import subprocess,tempfile,shutil,os,types
from pathlib import Path
import replay_probe_recheck as h
with tempfile.TemporaryDirectory(prefix='r4-alternates-ab-') as d:
 base=Path(d);p=base/'repo';p.mkdir();k,sha,al=h.anc(p);pool=base/'pool';shutil.move(p/'.git/objects',pool);(p/'.git/objects').mkdir()
 env={'GIT_ALTERNATE_OBJECT_DIRECTORIES':str(pool)}
 h.log(fsck=h.git(p,'fsck','--full',env=env),before_borrow=h.raw(p,al,env=env))
 (p/'.git/objects/info').mkdir();(p/'.git/objects/info/alternates').write_text(str(pool)+'\n')
 h.log(file_alternate=h.raw(p,al),fsck_file=h.git(p,'fsck','--full'))
 (p/'.git/objects/info/alternates').unlink()
 oldcode=subprocess.check_output(['git','-C',str(h.ROOT/'cay-kho'),'show','934a5b063670acfbed410487d8244cd17d586d6e:ops/bien_nhan_v2.py'],text=True)
 previous=base/'previous-repo';shutil.copytree(h.COPY,previous,symlinks=True);f=previous/'ops/bien_nhan_v2.py';f.write_text(oldcode);old=h.b.__file__;h.b.__file__=str(f)
 try:h.log(previous_revision_with_env=h.raw(p,al,env=env))
 finally:h.b.__file__=old
