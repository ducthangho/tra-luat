from pathlib import Path
import hashlib,json,subprocess,os,re,collections
S=Path(__file__).resolve().parent; R=S/'work/head'; E=S/'evidence'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_GLOBAL=str(S/'audit.gitconfig'),GIT_CONFIG_NOSYSTEM='1',GIT_OPTIONAL_LOCKS='0')
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,env=ENV)
# Content snapshot includes ignored and hidden files; excludes only .git object internals.
original=S/'cay-kho'
snapshot={str(p.relative_to(original)):sha(p.read_bytes()) for p in original.rglob('*') if p.is_file() and '.git' not in p.relative_to(original).parts}

if not (E/'original-before.json').exists(): (E/'original-before.json').write_text(json.dumps(snapshot,sort_keys=True))
pre=dict(head=git('rev-parse','HEAD').decode().strip(),tree=git('rev-parse','HEAD^{tree}').decode().strip(),status=git('status','--porcelain=v1','--untracked-files=all').decode(),base='180039c4b791fba4c89991623151cbb7378fce53')
pre['changed_paths']=git('diff','--name-only',pre['base'],'HEAD').decode().splitlines()
pre['outside_scope']=[p for p in pre['changed_paths'] if not p.startswith('ops/reviews/')]
pre['diff_equal']=git('diff',pre['base'],'HEAD')==(S/'DIFF.patch').read_bytes()
pre['commits']=git('log','--format=%H %s',pre['base']+'..HEAD').decode().splitlines()
pre['abbrev']=git('config','core.abbrev').decode().strip()
(E/'preflight.json').write_text(json.dumps(pre,indent=2,ensure_ascii=False))
print('preflight', {k:v for k,v in pre.items() if k!='changed_paths'}, 'changed_count',len(pre['changed_paths']))
results=[]
for letter,sub,runid in [('b','pr1119-review-1-codex','feeb867a'),('a','pr1119-review-1-codex/luot-hong-dia','e9bd8492'),('c','pr1119-review-2-codex','89d65076')]:
    src=S/'nguon'/('review1119'+letter); dst=R/'ops/reviews'/sub
    sourcefiles={p.relative_to(src).as_posix():p for p in src.rglob('*') if p.is_file()}
    destfiles={p.relative_to(dst).as_posix():p for p in dst.rglob('*') if p.is_file() and (letter!='b' or 'luot-hong-dia' not in p.relative_to(dst).parts)}
    omit={}
    for line in (dst/'OMITTED.txt').read_text().splitlines():
        m=re.fullmatch(r'([^\t]+)\tsha256 ([0-9a-f]{64})\tbytes (\d+)\t(.*)',line)
        if m:omit[m[1]]={'sha256':m[2],'bytes':int(m[3]),'reason':m[4]}
    mapped=[]; omitted=[]; errors=[]; used=set()
    for rel,p in sourcefiles.items():
        if rel=='launcher.json':target='launcher.out'
        elif rel.startswith('runs/'+runid+'/'):target='run/'+rel.split('/',2)[2]
        elif '/' not in rel and (rel.endswith('.py') or rel=='audit.gitconfig'):target='evidence/'+rel
        elif rel=='DIFF-OPS-REVIEWS-TU-LUOT1.patch':target='diff-ops-reviews-tu-luot1.patch'
        elif rel=='nguon/VERDICT-LUOT1.md':target='verdict-cu/luot1-VERDICT.md'
        else:target=rel
        raw=p.read_bytes(); measured=dict(source=rel,target=target,sha256=sha(raw),bytes=len(raw))
        if target in destfiles:
            measured['equal']=raw==destfiles[target].read_bytes(); mapped.append(measured); used.add(target)
            if not measured['equal']:errors.append({'byte_mismatch':measured})
        elif rel in omit:
            measured['declaration']=omit[rel]; measured['valid']=all(measured[k]==omit[rel][k] for k in ('sha256','bytes'));omitted.append(measured)
            if not measured['valid']:errors.append({'wrong_omission':measured})
        else:errors.append({'undeclared_missing':measured})
    extras=set(destfiles)-used-{'SHA256SUMS','OMITTED.txt'}
    if extras:errors.append({'dest_no_source':sorted(extras)})
    stale=set(omit)-set(sourcefiles)
    if stale:errors.append({'omitted_not_in_source':sorted(stale)})
    manifest_root=dst if (dst/'SHA256SUMS').exists() else dst.parent
    manifest_paths=[]
    for line in (manifest_root/'SHA256SUMS').read_text().splitlines():
        m=re.fullmatch(r'([0-9a-f]{64}) [ *](.*)',line)
        if not m:errors.append({'bad_manifest_line':line});continue
        manifest_paths.append(m[2].removeprefix('./'))
    all_files={p.relative_to(manifest_root).as_posix() for p in manifest_root.rglob('*') if p.is_file()}
    missing=all_files-set(manifest_paths)-{'SHA256SUMS'}
    extra=set(manifest_paths)-all_files
    cp=subprocess.run(['sha256sum','-c','SHA256SUMS'],cwd=manifest_root,capture_output=True,env=ENV)
    (E/f'bytes-{letter}-sha256sum.stdout').write_bytes(cp.stdout);(E/f'bytes-{letter}-sha256sum.stderr').write_bytes(cp.stderr)
    result=dict(source=str(src),dest=sub,source_count=len(sourcefiles),dest_count=len(destfiles),mapped=mapped,omitted=omitted,errors=errors,manifest=dict(root=str(manifest_root.relative_to(R)),rc=cp.returncode,entries=len(manifest_paths),all_files=len(all_files),missing=sorted(missing),extra=sorted(extra),duplicates=[p for p,n in collections.Counter(manifest_paths).items() if n>1]))
    results.append(result)
    print(sub,'source',len(sourcefiles),'mapped',len(mapped),'omitted',len(omitted),'errors',errors,'manifest',result['manifest'])
flats=[]
for n in (1,2):
    folder=R/f'ops/reviews/pr1119-review-{n}-codex/VERDICT.md';flat=R/f'ops/reviews/pr1119-review-{n}-codex-verdict.md'
    data=flat.read_bytes();flats.append(dict(round=n,equal=data==folder.read_bytes(),bytes=len(data),sha256=sha(data),tail_hex=data[-12:].hex(),ends_blank_line=data.endswith(b'\n\n')))
print('flat verdicts',flats)
(E/'bytes.json').write_text(json.dumps(dict(runs=results,flats=flats),ensure_ascii=False,indent=2))
with (S/'VERDICT.md').open('a') as f:
    f.write('\nByte audit: `PYTHONDONTWRITEBYTECODE=1 python3 audit_bytes.py`; output chi tiết `evidence/bytes.json`.\n')
    for r in results:f.write(f"- `{r['dest']}`: nguồn={r['source_count']}, khớp={len(r['mapped'])}, bỏ có khai={len(r['omitted'])}, lỗi={r['errors']}; SHA256SUMS={r['manifest']}.\n")
    f.write(f'- Bản phẳng: {flats}.\n')
