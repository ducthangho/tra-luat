#!/usr/bin/env python3
"""Gỡ riêng từng chốt trên bản sao; gọi TOÀN BỘ CA sẵn có, không chạy mutant harness lồng nhau."""
from concurrent.futures import ProcessPoolExecutor
import importlib.util,json,sys,shutil
from pathlib import Path
ROOT=Path('/tmp/wp960-r2-Dt2G8H/repo')
EV=Path('/tmp/claude-0/rv/wp960-review-2-codex/evidence')
MUTANTS=[
('r1-moc-oid40','    if not moc or not _HEX40.match(moc):\n','    if not moc:\n'),
('r2-luot-other','if luot_nay is None or any(lu is None for _, lu in sau):','if luot_nay is None:'),
('r3-merge-error','                        if rc != 0:\n                            chua.setdefault(k, f"{ten}: `{duong}` — `merge-base` rc={rc} cho `{x}`")\n                            continue\n',''),
('r4-run-invalid','        if not s_that:\n            chua[k_sf]','        if not s_that:\n            sf_chua.append(rj)\n            continue\n            chua[k_sf]'),
('r5-history-none','    if them is None:\n        return None\n','    if them is None:\n        return False\n'),
('r6-first-file','        if _co_cau(van, cau):\n','        if True:\n'),
('r7-default-fallback','("refs/remotes/origin/HEAD", "refs/remotes/origin/master", "refs/heads/master")','("refs/remotes/origin/HEAD",)'),
('r8-history-utf8','        except UnicodeDecodeError:\n            return None\n','        except UnicodeDecodeError:\n            continue\n'),
]
def run(item):
 name,old,new=item
 spec=importlib.util.spec_from_file_location('bt',ROOT/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
 f=(EV/(name+'.log')).open('w');print(json.dumps({'name':name,'old':old,'new':new},ensure_ascii=False),file=f,flush=True)
 t._dot_bien_tep(old,new)
 outer_dirs=tuple(t._TAM_DOT_BIEN);t._TAM_DOT_BIEN.clear()
 outer_path=t.CONG;outer_bytes=outer_path.read_bytes()
 red=[];passed=0
 try:
  for fn in t.CA:
   status,detail=t._chay_1(fn)
   if t.CONG!=outer_path or not outer_path.exists() or outer_path.read_bytes()!=outer_bytes:
    raise RuntimeError('RIG: source mutant bị đổi/mất sau '+fn.__name__)
   if status=='qua':passed+=1
   else:red.append((fn.__name__,status,detail))
   print(json.dumps({'case':fn.__name__,'status':status,'detail':detail},ensure_ascii=False),file=f,flush=True)
  r={'mutant':name,'passed':passed,'total':len(t.CA),'red':red};print(json.dumps(r,ensure_ascii=False),file=f,flush=True);return r
 finally:
  f.close()
  for p in (*t._TAM_DOT_BIEN,*outer_dirs):shutil.rmtree(p,ignore_errors=True)
if __name__=='__main__':
 with ProcessPoolExecutor(max_workers=3) as pool:
  for r in pool.map(run,MUTANTS):print(json.dumps(r,ensure_ascii=False),flush=True)
