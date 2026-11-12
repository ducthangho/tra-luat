import sys, importlib.util, re
spec=importlib.util.spec_from_file_location('dg', sys.argv[1]); dg=importlib.util.module_from_spec(spec); spec.loader.exec_module(dg)
for p in sys.argv[2:]:
    raw=open(p,'rb').read().decode('utf-8','replace').lstrip('﻿')
    lines=[]; job=None; steps=set()
    for l in raw.splitlines():
        parts=l.split('\t',2)
        if len(parts)==3:
            job=parts[0]; steps.add(parts[1]); lines.append(parts[2].lstrip('﻿'))
        else: lines.append(l)
    ds=dg.buoc('\n'.join(lines).encode())
    tt, ly = dg.danh_gia(job, ds)
    print(p.split('/')[-1], job, '->', tt, '|', ly[:300])
