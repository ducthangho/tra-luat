import concurrent.futures, json, os, pathlib, re, subprocess, sys, time
root=pathlib.Path(__file__).resolve().parents[1]
mode, workers, loops=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
script=root/'nguon'/('repro_a11.py' if mode=='before' else 'repro_a11_va.py')
def run(i):
 cmd=['python3',str(script),str(root/'work/head'),str(loops)]
 t=time.monotonic()
 r=subprocess.run(cmd,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=loops+60)
 (root/'evidence'/f'repro-{mode}-{i:02}.log').write_text(r.stdout+r.stderr)
 match=re.search(r'song_ngay_sau_giet (\d+) / (\d+)',r.stdout)
 return dict(worker=i,rc=r.returncode,seconds=round(time.monotonic()-t,6),bad=int(match[1]) if match else None,total=int(match[2]) if match else None,empty=r.stdout.count('rong'),states=re.findall(r'^SONG \d+ (.+)$',r.stdout,re.M))
t=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
 rows=list(pool.map(run,range(workers)))
summary=dict(mode=mode,workers=workers,loops=loops,seconds=round(time.monotonic()-t,6),bad=sum(x['bad'] or 0 for x in rows),total=sum(x['total'] or 0 for x in rows),empty=sum(x['empty'] for x in rows),all_rc_zero=all(x['rc']==0 for x in rows),rows=rows)
(root/'evidence'/f'repro-{mode}.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False),flush=True)
