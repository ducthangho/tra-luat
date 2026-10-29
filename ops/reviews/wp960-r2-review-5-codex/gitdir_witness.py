import tempfile,os,shutil
from pathlib import Path
import replay_probe_recheck as h
old=h.t.bnv2
sample='_GIT_GIU = frozenset({"GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_EXEC_PATH"})'
mutant='_GIT_GIU = frozenset({"GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_EXEC_PATH", "GIT_DIR"})'
h.t._dot_bien_tep(sample,mutant);mod=h.t.bnv2
try:
 h.log(test='c95',result=h.t._chay_1(h.t.c95_moi_truong_git_KHONG_doi_ket_qua_do))
 h.t.bnv2=old
 with tempfile.TemporaryDirectory(prefix='r5-gitdir-witness-') as d:
  base=Path(d);root=base/'root';root.mkdir();k,sha,al=h.anc(root);other=base/'other';other.mkdir();q=h.t._kho_cau(other)
  h.log(fixture='same-M-before-reset',root_M=k['M'],other_M=q['M'],other_master=q['g']('rev-parse','master'))
  q['g']('reset','--hard',q['X']);h.log(fixture='different-master-after-reset',other_master=q['g']('rev-parse','master'),fsck=h.git(other,'fsck','--full'),root_ancestor=h.git(root,'merge-base','--is-ancestor',sha,'master'),foreign_ancestor=h.git(other,'merge-base','--is-ancestor',sha,'master'))
  for debt in ((),(h.KEY,)):
   for name,m in [('head',old),('u7-allow-GIT_DIR',mod)]:
    h.b=m
    try:h.log(module=name,debt=bool(debt),result=h.raw(root,al,debt,env={'GIT_DIR':str(other/'.git')}))
    finally:h.b=old
finally:
 h.t.bnv2=old
 for p in h.t._TAM_DOT_BIEN:shutil.rmtree(p,ignore_errors=True)
 h.t._TAM_DOT_BIEN.clear()
