import re,sys,json,subprocess,yaml
jobsmap={'108792765482':('ci','gate-registry'),'108792765497':('ci','gate-ops'),'108792765498':('ci','gate'),'108792765529':('ci','gate-packet-loop'),
'108815233211':('ci','gate-ops'),'108815233275':('ci','gate-registry'),'108815233290':('ci','gate-packet-loop'),'108815233339':('ci','gate'),
'108815209421':('lw','launcher'),'108815209553':('lw','launcher')}
wf={'ci':'.github/workflows/ci.yml','lw':'.github/workflows/launcher-windows.yml'}
defs={k:yaml.safe_load(subprocess.run(['git','show','f8a7829:'+p],capture_output=True,text=True).stdout) for k,p in wf.items()}
TS=re.compile(r'^\S+Z ')
out={}
for jid,(w,name) in jobsmap.items():
    steps=defs[w]['jobs'][name]['steps']
    want=[(s['run'].rstrip('\n').split('\n') if 'run' in s else None) for s in steps]
    L=[TS.sub('',x.rstrip('\r\n')) for x in open(f'/tmp/do650/log-{jid}.txt',encoding='utf-8',errors='replace')]
    got=[];cur=None
    for x in L:
        if x.startswith('##[group]Run '):
            cur=[];got.append(cur);continue
        if cur is not None and x.startswith('\x1b[36;1m'):
            cur.append(x[len('\x1b[36;1m'):].replace('\x1b[0m',''))
        elif cur is not None and cur and not x.startswith('\x1b[36;1m'):
            cur=None
    runs=[w_ for w_ in want if w_ is not None]
    gotruns=[g for g in got if g]
    # match: every executed run body equals some defined run body in order (steps may be skipped via if:)
    i=0;ok=True;matched=0
    for g in gotruns:
        while i<len(runs) and [l.rstrip() for l in runs[i]]!=[l.rstrip() for l in g]: i+=1
        if i==len(runs): ok=False;break
        matched+=1;i+=1
    out[jid]=dict(job=name,wf=wf[w],runs_defined=len(runs),runs_in_log=len(gotruns),matched=matched,all_in_order=ok)
print(json.dumps(out,indent=1))
