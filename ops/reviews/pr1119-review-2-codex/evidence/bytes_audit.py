from common import *
import re,yaml
out=[];failures=[]
for pr,turn,src in ITEMS:
    stem=f'pr{pr}-review-{turn}-codex'; dst=R/'ops/reviews'/stem; source=S/'nguon'/src
    omissions={}
    for line in (dst/'OMITTED.txt').read_text().splitlines():
        match=re.match(r'([^\t]+)\tsha256 ([0-9a-f]{64})\tbytes (\d+)\t(.+)',line)
        if match:
            path,sha,size,reason=match.groups();assert path not in omissions;omissions[path]=dict(sha256=sha,bytes=int(size),reason=reason)
    mapping=[];absent=[]
    for p in sorted(source.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(source).as_posix(); parts=p.relative_to(source).parts
        target=rel
        if rel=='launcher.json':target='launcher.out'
        elif parts[0]=='runs':target='/'.join(('run',*parts[2:]))
        elif len(parts)==1 and (p.suffix=='.py' or rel=='audit.gitconfig'):target='evidence/'+rel
        elif rel=='DIFF-TU-LUOT1.patch':target='diff-tu-luot1.patch'
        elif rel=='DIFF-OPS-REVIEWS-TU-LUOT1.patch':target='diff-ops-reviews-tu-luot1.patch'
        elif rel=='nguon/VERDICT-LUOT1.md':target='verdict-cu/luot1-VERDICT.md'
        raw=p.read_bytes();item=dict(source=rel,target=target,sha256=digest(raw),bytes=len(raw))
        if (dst/target).is_file():
            item['equal']=(dst/target).read_bytes()==raw;mapping.append(item)
            if not item['equal']:failures.append([stem,rel,'byte'])
        else:
            d=omissions.get(rel);item['declaration']=d;item['correct']=bool(d and d['sha256']==digest(raw) and d['bytes']==len(raw));absent.append(item)
            if not item['correct']:failures.append([stem,rel,'omission'])
    entries=[]
    for l in (dst/'SHA256SUMS').read_text().splitlines():
        sha,p=l.split(maxsplit=1);entries.append(p.removeprefix('./'))
    actual={p.relative_to(dst).as_posix() for p in dst.rglob('*') if p.is_file()}-{'SHA256SUMS'}
    mapped={i['target'] for i in mapping}|{'OMITTED.txt'}
    checks=dict(manifest_missing=sorted(actual-set(entries)),manifest_extra=sorted(set(entries)-actual),manifest_duplicates=len(entries)-len(set(entries)),unmapped=sorted(actual-mapped),false_omissions=sorted(set(omissions)-{i['source'] for i in absent}),flat_equal=(R/'ops/reviews'/f'{stem}-verdict.md').read_bytes()==(source/'VERDICT.md').read_bytes())
    res=logged(stem+'-sha256sum',['sha256sum','-c','SHA256SUMS'],dst)
    d=yaml.safe_load((R/'ops/reviews'/f'{stem}-verdict.receipt.yaml').read_text())
    generated=git('diff',d['base_sha'],d['reviewed_sha']);checks['git_diff_equal']=generated==(source/'DIFF.patch').read_bytes()
    for item in absent:
        if item['source']=='DIFF.patch':
            a,b=re.search(r'git diff (\w+) (\w+)',item['declaration']['reason']).groups()
            item['reproduce_command']=['git','diff',a,b];item['reproduce_equal']=git('diff',a,b)==(source/'DIFF.patch').read_bytes()
            if not item['reproduce_equal']:failures.append([stem,'declared git diff'])
    if any(checks[k] for k in ('manifest_missing','manifest_extra','manifest_duplicates','unmapped','false_omissions')) or not checks['flat_equal'] or not checks['git_diff_equal'] or res['rc']:failures.append([stem,checks,res])
    save(stem+'-mapping.json',dict(mapping=mapping,absent=absent))
    out.append(dict(stem=stem,source_files=len(mapping)+len(absent),copied=len(mapping),absent=len(absent),declared_correct=sum(i['correct'] for i in absent),manifest_entries=len(entries),manifest_rc=res['rc'],checks=checks))
save('bytes.json',dict(results=out,failures=failures));print(json.dumps(dict(results=out,failures=failures),ensure_ascii=False,indent=2))
note('Byte — `PYTHONDONTWRITEBYTECODE=1 python3 bytes_audit.py`: '+json.dumps(dict(results=out,failures=failures),ensure_ascii=False)+'. Từng hash/bytes/ánh xạ/omission và output sha256sum: `evidence/pr*-mapping.json`, `evidence/pr*-sha256sum.stdout`.')
