from pathlib import Path
import subprocess,json
r=Path(__file__).resolve().parents[1]
rows=[]
for mode in ['control','post-mismatch','keep-mismatch']:
    log=r/'evidence'/f'pinned-{mode}.json'
    cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/pinned-release-round15.ps1'),'-Mode',mode,'-Log',str(log)]
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
    (r/'evidence'/f'pinned-{mode}.log').write_text(p.stdout+p.stderr)
    assert p.returncode==0,(p.stdout,p.stderr)
    d=json.loads(log.read_text())
    assert d['direct']['rc']==0 and len(d['rows'])==1
    assert d['requests'][0]['uri'].endswith('/releases/tags/v'+d['pin'])
    assert d['rows'][0]['hanh_dong']==('giu' if mode=='keep-mismatch' else 'nang_cap')
    assert d['rows'][0]['sau']==d['direct']['stdout']==d['release']
    d['matches_manifest_pin']=d['rows'][0]['sau']==d['pin']
    rows.append(dict(command=cmd,rc=p.returncode,data=d))
    print(json.dumps(d,ensure_ascii=False),flush=True)
(r/'evidence/pinned-release-round15.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('Pinned release observations: control matches manifest; mismatched response tag accepted at post-install and keep')
