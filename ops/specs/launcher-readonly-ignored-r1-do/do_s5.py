import os,hashlib,sys,time
goc=sys.argv[1];n=0;b=0;t=time.monotonic()
for r,ds,fs in os.walk(goc):
    for f in fs:
        p=os.path.join(r,f)
        if os.path.islink(p): continue
        h=hashlib.sha256()
        with open(p,'rb') as fh:
            for k in iter(lambda: fh.read(1<<20), b''): h.update(k); b+=len(k)
        n+=1
print(f"tep={n} byte={b} giay={time.monotonic()-t:.2f}")
