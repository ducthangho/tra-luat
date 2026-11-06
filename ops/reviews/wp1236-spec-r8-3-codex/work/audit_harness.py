"""Replay supplied harmless probes only; compare the harness body with its original bytes."""
import collections, json, os, subprocess, sys, tempfile
from pathlib import Path
W=Path(__file__).resolve().parent
tempfile.tempdir=str(W/'tmp')
sys.path.insert(0,str(W/'soan'))
import gram, sinh_r8 as s, dot_bien_r8 as d
rows=[]
for name,f in d.DB_SINH.items():
    if not name.startswith('m-S15['):continue
    char=int(name.split('[')[1].split(']')[0],16)
    if char not in map(ord,";&|()<>'\""):continue
    counts=collections.Counter(); example=None
    for body in s.kho():
        for sh in s.SHELL:
            for run in (body,body+'\n'):
                if f(run,sh) is not None or gram.cp(run,sh) is None:continue
                for k,rc,ran in s.chay_tung_thanh_phan(run,sh):
                    counts['checks']+=1
                    counts['rc0_and_ran']+=int(rc==0 and ran)
                    counts['rc0_not_ran']+=int(rc==0 and not ran)
                    counts['rc_nonzero_not_ran']+=int(rc!=0 and not ran)
                    counts['rc_nonzero_ran']+=int(rc!=0 and ran)
                    if char in (ord("'"),ord('"')) and example is None:
                        with tempfile.TemporaryDirectory() as tmp:
                            p=Path(tmp); (p/'s.sh').write_text(run)
                            argv=s.SHELL_LENH[sh][:];argv[0]='/usr/bin/bash' if argv[0]=='bash' else '/bin/sh'
                            c=subprocess.run(argv+[str(p/'s.sh')],cwd=p,env={'PATH':'/usr/bin:/bin','HOME':tmp},stdin=subprocess.DEVNULL,capture_output=True)
                            example={'char_code':char,'shell':sh,'harness':[k,rc,ran],
                              'original_rc':c.returncode,'original_ran':(p/'DA_CHAY').exists(),
                              'original_stderr':c.stderr.decode(errors='replace').replace(tmp,'<scratch>')}
    rows.append({'mutant':name,**dict(counts),'original_comparison':example})
print(json.dumps(rows,ensure_ascii=False,indent=2),flush=True)
(W/'harness.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
operators=[]
for name,f in d.DB_SINH.items():
    if name.startswith('m-S15['):continue
    found=False
    for body in s.kho():
        if found:break
        for sh in s.SHELL:
            if found:break
            if f(body,sh) is None and gram.cp(body,sh) is not None:
                found=any(rc==0 and ran for _,rc,ran in s.chay_tung_thanh_phan(body,sh))
    operators.append({'mutant':name,'actual_rc0_and_ran':found})
print(json.dumps(operators),flush=True)
(W/'harness_operators.json').write_text(json.dumps(operators,indent=2))
