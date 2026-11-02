from pathlib import Path
import subprocess,json
r=Path(__file__).resolve().parents[1]
rows=[]
for tree in ['head','system-post-mutant']:
    for kind in ['dich','zero','git-marker']:
        log=r/'evidence'/f'post-{tree}-{kind}.json'
        cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/measure-system-post.ps1'),'-Product',str(r/'copies'/tree/'ops/vm/cap-nhat-cong-cu.ps1'),'-Kind',kind,'-Log',str(log)]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
        (r/'evidence'/f'post-{tree}-{kind}.log').write_text(p.stdout+p.stderr)
        assert p.returncode==0,(p.stdout,p.stderr)
        d=json.loads(log.read_text());tools=[x for x in d['rows'] if x['cong_cu']!='commander']
        assert len(d['installs'])==4 and len(tools)==4 and len(d['direct'])==4
        assert all(x['rc']==0 and x['installed'] for x in d['direct'])
        expected=['nang_cap']*4 if tree!='head' or kind=='dich' else ['loi']*4 if kind=='zero' else ['loi','nang_cap','nang_cap','nang_cap']
        assert [x['hanh_dong'] for x in tools]==expected
        summary=dict(tree=tree,kind=kind,installs=d['installs'],actions=[(x['cong_cu'],x['hanh_dong']) for x in tools],direct=d['direct'])
        rows.append(dict(command=cmd,rc=p.returncode,summary=summary))
        print(json.dumps(summary,ensure_ascii=False),flush=True)
(r/'evidence/post-observations-round15.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('Post identity stateful observations: 6/6 PASS; head rejects aliases, mutant accepts; all 4 installers/markers/native rc0')
