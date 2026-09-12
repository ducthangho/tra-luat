import datetime as dt, hashlib, json, os, pathlib, subprocess, sys, time
B=pathlib.Path(__file__).resolve().parents[1];O=B/'do-review9';name=sys.argv[1];cmd=sys.argv[2:];tmp=O/'tmp';tmp.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(tmp),TMP=str(tmp),TEMP=str(tmp));env['PATH']='/usr/local/bin:'+env.get('PATH','')
t0=time.monotonic();start=dt.datetime.now(dt.timezone.utc).isoformat()
with (O/(name+'.stdout')).open('wb') as out,(O/(name+'.stderr')).open('wb') as err:r=subprocess.run(cmd,cwd=B/'cay-kho',env=env,stdout=out,stderr=err)
meta=dict(name=name,command=cmd,cwd='cay-kho',utc=start,rc=r.returncode,seconds=time.monotonic()-t0)
for kind in ['stdout','stderr']:
 raw=(O/(name+'.'+kind)).read_bytes();meta[kind+'_bytes']=len(raw);meta[kind+'_sha256']=hashlib.sha256(raw).hexdigest()
(O/(name+'.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(json.dumps(meta,ensure_ascii=False));sys.exit(r.returncode)
