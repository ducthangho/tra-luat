from audit_common import *
import re, yaml
results=[]
for pr,round_,source in CASES:
    stem=f'pr{pr}-review-{round_}-codex'
    arc=REPO/'ops/reviews'/stem
    src=ROOT/'nguon'/source
    sources={str(p.relative_to(src)):p for p in src.rglob('*') if p.is_file()}
    archives={str(p.relative_to(arc)):p for p in arc.rglob('*') if p.is_file()}
    runs=list((src/'runs').iterdir())
    assert len(runs)==1
    def mapped(n):
        if n=='launcher.out': return 'launcher.json'
        if n.startswith('run/'): return 'runs/'+runs[0].name+'/'+n[4:]
        if n.startswith('evidence/') and (n.endswith('.py') or n=='evidence/audit.gitconfig'): return n[9:]
        if n=='diff-tu-luot1.patch': return 'DIFF-TU-LUOT1.patch'
        if n=='diff-ops-reviews-tu-luot1.patch': return 'DIFF-OPS-REVIEWS-TU-LUOT1.patch'
        if n=='verdict-cu/luot1-VERDICT.md': return 'nguon/VERDICT-LUOT1.md'
        return n
    mapping=[]
    seen=set()
    for n,p in sorted(archives.items()):
        if n in ('SHA256SUMS','OMITTED.txt'): continue
        s=mapped(n)
        seen.add(s)
        mapping.append({'archive':n,'source':s,'source_exists':s in sources,
          'equal':s in sources and p.read_bytes()==sources[s].read_bytes(),
          'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size})
    missing=sorted(set(sources)-seen)
    omitted=(arc/'OMITTED.txt').read_text()
    declared={}
    for line in omitted.splitlines():
        m=re.match(r'([^\t]+)\tsha256 ([0-9a-f]{64})\tbytes (\d+)\tly do: (.*)',line)
        if m: declared[m[1]]={'sha256':m[2],'bytes':int(m[3]),'reason':m[4]}
    omissions=[]
    for n in missing:
        p=sources[n]
        row={'source':n,'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size,'declared':n in declared}
        row['matches_declaration']=n in declared and row['sha256']==declared[n]['sha256'] and row['bytes']==declared[n]['bytes']
        row['reason_supported']=n in declared and ((p.stat().st_size>500000 and '>500 KB' in declared[n]['reason']) or (n=='launcher.err' and p.stat().st_size==0) or (pr=='1110' and n=='DIFF.patch' and 'git diff' in declared[n]['reason']))
        if n in declared:
            m=re.search(r'git diff ([0-9a-f]+) ([0-9a-f]+)',declared[n]['reason'])
            if m:
                b=git('diff',m[1],m[2])
                row['reproduction']={'command':f'git diff {m[1]} {m[2]}','equal':b==p.read_bytes(),'bytes':len(b),'sha256':sha(b)}
        omissions.append(row)
    mf={}
    duplicates=[]
    for line in (arc/'SHA256SUMS').read_text().splitlines():
        h,n=line.split('  ',1); n=n.removeprefix('./')
        if n in mf: duplicates.append(n)
        mf[n]=h
    p=run(['sha256sum','-c','SHA256SUMS'],arc)
    (EVID/(stem+'-sha256sum.stdout')).write_bytes(p.stdout)
    (EVID/(stem+'-sha256sum.stderr')).write_bytes(p.stderr)
    receipt=yaml.safe_load((REPO/'ops/reviews'/(stem+'-verdict.receipt.yaml')).read_text())
    original_diff=git('diff',receipt['base_sha'],receipt['reviewed_sha'])
    r={'archive':stem,'source':source,'source_files':len(sources),'archived_source_files':len(mapping),
       'mapping_failures':[x for x in mapping if not x['equal']],
       'flat_equal':(REPO/'ops/reviews'/(stem+'-verdict.md')).read_bytes()==(src/'VERDICT.md').read_bytes(),
       'omissions':omissions,'unexpected_omission_declarations':sorted(set(declared)-set(missing)),
       'manifest_rc':p.returncode,'manifest_entries':len(mf),'manifest_missing':sorted(set(archives)-{'SHA256SUMS'}-set(mf)),
       'manifest_extra':sorted(set(mf)-set(archives)),'manifest_duplicates':duplicates,
       'original_diff_equal':original_diff==(src/'DIFF.patch').read_bytes(),
       'original_diff_sha256':sha(original_diff),'original_diff_bytes':len(original_diff)}
    save(stem+'-mapping.json',mapping)
    results.append(r)
    print(json.dumps(r,ensure_ascii=False))
save('bytes.json',results)
append('Byte — `PYTHONDONTWRITEBYTECODE=1 python3 audit_bytes.py`: kết quả `evidence/bytes.json`, ánh xạ chi tiết `evidence/pr*-mapping.json`; '+str(sum(r['archived_source_files'] for r in results))+' tệp nguồn được đối chiếu. Các lỗi (nếu có) nằm ở mapping_failures/omissions/manifest và original_diff_equal; đây là phép đo mới, không dùng bảng mapping của executor làm đầu vào.')
