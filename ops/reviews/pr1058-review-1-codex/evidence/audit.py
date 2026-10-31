import sys, subprocess, pathlib, hashlib, json, re, collections, datetime, unicodedata
import yaml
S=pathlib.Path(__file__).resolve().parent; R=S/'cay-kho'; P=R/'ops/land/pr1047-wp1045-provenance'
REF='origin/ops/wp1045-r1-g1-lease'
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
def sha(b): return hashlib.sha256(b).hexdigest()
def y(p): return yaml.safe_load(pathlib.Path(p).read_bytes())
def j(p): return json.loads(pathlib.Path(p).read_bytes())
def dt(s): return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
def out(k,v): print(k,json.dumps(v,ensure_ascii=False,sort_keys=True))
def ancestor(a,b): return subprocess.run(['git','merge-base','--is-ancestor',a,b],cwd=R).returncode

def byte_checks():
    out('lease_ref',git('rev-parse',REF).decode().strip())
    for n in (1,2,3):
        src=f'ops/handoff/wp1045-g1-claude/luot{n}'
        dst=R/f'ops/reviews/wp1045-g1-codex-luot{n}'
        source=git('ls-tree','-r','--name-only',REF,'--',src).decode().splitlines()
        orig=git('ls-tree','-r','--name-only','4b4f37f','--',src).decode().splitlines()
        target=sorted(str(f.relative_to(dst)) for f in dst.rglob('*') if f.is_file() and f.name!='SHA256SUMS')
        source_rel=sorted(f[len(src)+1:] for f in source)
        assert source_rel==target,(n,source_rel,target)
        assert source==orig
        for f in source:
            rel=f[len(src)+1:]; a=git('show',f'{REF}:{f}'); b=(dst/rel).read_bytes()
            assert a==b and a==git('show',f'4b4f37f:{f}'),f
        flat=R/f'ops/reviews/wp1045-g1-codex-luot{n}-verdict.md'
        assert flat.read_bytes()==(dst/'VERDICT.md').read_bytes()
        out(f'luot{n}_bytes',dict(files=len(source),identical_all=True,at_4b4f37f=True,flat_identical=True,verdict_bytes=flat.stat().st_size,verdict_sha256=sha(flat.read_bytes())))
    manifests=[R/f'ops/reviews/wp1045-g1-codex-luot{n}/SHA256SUMS' for n in (1,2,3)]+[P/'SHA256SUMS']
    logs=[]
    for f in manifests:
        p=subprocess.run(['sha256sum','-c','SHA256SUMS'],cwd=f.parent,capture_output=True,text=True)
        logs.append(f'$ (cd {f.relative_to(R).parent} && sha256sum -c SHA256SUMS)\n{p.stdout}{p.stderr}EXIT={p.returncode}\n')
        assert p.returncode==0,(str(f),p.stdout,p.stderr)
        expected={line.split('  ',1)[1].removeprefix('./') for line in f.read_text().splitlines()}
        actual={str(x.relative_to(f.parent)) for x in f.parent.rglob('*') if x.is_file() and x!=f}
        assert actual==expected,(expected,actual)
        out('SHA256SUMS',dict(path=str(f.relative_to(R)),rc=p.returncode,ok=p.stdout.count(': OK'),coverage_complete=True))
    (S/'evidence/checksums.log').write_text('\n'.join(logs))

def receipt_checks():
    readme=(R/'ops/reviews/README.md').read_text()
    leases=[y(P/'lease-wp1045-r1-g1.yaml.txt'),y(P/'lease-wp1045-r1-g2.yaml.txt')]
    for n in (1,2,3):
        receipt=y(R/f'ops/reviews/wp1045-g1-codex-luot{n}-verdict.receipt.yaml')
        folder=R/f'ops/reviews/wp1045-g1-codex-luot{n}'; run=j(folder/'run/run.json')
        v=(folder/'VERDICT.md').read_text(); b=(folder/'VERDICT.md').read_bytes()
        verdict=v.splitlines()[0].split(': ',1)[1]; head=v.splitlines()[1].split(': ',1)[1]
        counts=[len(re.findall(rf'^- \[P{k}\]',v,re.M)) for k in range(4)]
        ids=[dict(hang='P'+k,id=name) for k,name in re.findall(r'^- \[P([0-3])\] ([\w-]+):',v,re.M)]
        assert receipt['verdict']=={'request_changes':'changes_requested','approve':'approve'}[verdict]
        assert head==run['head']==receipt['reviewed_sha']
        assert counts==[receipt[f'so_p{k}'] for k in range(4)]
        assert ids==receipt['findings_ids']
        assert len(b)==receipt['verdict_bytes'] and sha(b)==receipt['verdict_sha256']
        assert receipt['model_reviewer_identity']['session_run_id']==run['run_id']
        assert sha((folder/'PROMPT.md').read_bytes())==run['prompt_sha256']
        for kind in ('stdout','stderr'):
            data=(folder/f'run/{kind}.log').read_bytes()
            assert len(data)==run[f'{kind}_byte'] and sha(data)==run[f'{kind}_sha256']
        assert sha((folder/'run/checkpoint.json').read_bytes())==run['checkpoint_sha256']
        elapsed=(dt(run['ket_thuc_utc'])-dt(run['bat_dau_utc'])).total_seconds()
        assert abs(elapsed-run['thoi_luong_giay'])<.001
        assert run['ma_thoat']==0 and run['trang_thai']=='xong' and run['worktree_sach'] is True
        events=run['model_phuc_vu']; models=collections.Counter(e['model'] for e in events)
        assert models=={'gpt-6-astra':[25,42,43][n-1]}
        assert run['model_phuc_vu_trang_thai']=='DO_DUOC'
        assert run['effort_phuc_vu']==['xhigh'] and run['effort_phuc_vu_trang_thai']=='DO_DUOC'
        assert run['sandbox_trang_thai']=='KHONG_DO_DUOC'
        assert run['sandbox_ly_do']=='luong lay mau sandbox hong (DanhTinhDoi)'
        lease=leases[0 if n<3 else 1]
        start=dt(lease['leased_at_utc']); end=dt(leases[1]['leased_at_utc'] if n<3 else lease['lease_until'])
        assert start<=dt(run['bat_dau_utc'])<end
        assert receipt['lease_id']==lease['lease_id'] and receipt['generation']==lease['generation']
        anc=ancestor(head,'b2d5f06'); assert anc==0
        m=re.fullmatch(r'https://github.com/ducthangho/tra-luat/blob/([0-9a-f]{40})/(.+)',receipt['evidence_url']); assert m
        anchor,path=m.groups(); assert path==receipt['verdict_path']
        assert ancestor(anchor,'HEAD')==0 and git('show',f'{anchor}:{path}')==b
        for c in receipt['verdict_usage_caveats']:
            assert any(pathlib.Path(path).name in line and c['id'] in line for line in readme.splitlines())
        out(f'luot{n}',dict(verdict=verdict,receipt_verdict=receipt['verdict'],counts=counts,ids=ids,head=head,ancestor_b2d5f06_rc=anc,evidence_commit=anchor,evidence_ancestor_HEAD_rc=0,evidence_bytes_equal=True,run_id=run['run_id'],ma_thoat=run['ma_thoat'],trang_thai=run['trang_thai'],duration=run['thoi_luong_giay'],duration_from_timestamps=elapsed,model_events=models,model_state=run['model_phuc_vu_trang_thai'],effort=run['effort_phuc_vu'],prompt_sha256=run['prompt_sha256'],sandbox_state=run['sandbox_trang_thai'],lease=lease['lease_id'],window=[start.isoformat(),end.isoformat()],start=run['bat_dau_utc'],end=run['ket_thuc_utc'],in_window=True,hashes='prompt/stdout/stderr/checkpoint PASS'))

def git_checks():
    land=y(R/'ops/land/pr1047-wp1045-land-evidence.yaml'); merge=land['merge_commit']; head=land['authorized_head_sha']
    cat=git('cat-file','-p',merge).decode().splitlines(); tree=git('rev-parse',head+'^{tree}').decode().strip()
    assert tree==land['authorized_head_tree']; assert cat[0]=='tree '+land['merge_commit_tree']
    assert [a.split(' ',1)[1] for a in cat if a.startswith('parent ')]==land['merge_commit_parents']
    diff1=git('diff','5e458f4','2014602'); diff2=git('diff','b2d5f06^1','b2d5f06')
    assert diff1==diff2
    assert sha(diff1)=='65b4fa2e33f4c39fec5d4a287d3b1c94decdcde532141d25ab0bd82b046a69d7'
    p=P/'merge-va-diff.txt'; source=p.read_text()
    outputs=[git('cat-file','-p','b2d5f06').decode().splitlines()[:4],tree,git('diff','--name-only','5e458f4','2014602').decode().strip(),git('diff','--stat','b2d5f06^1','b2d5f06').decode().rstrip()]
    for text in outputs:
        if isinstance(text,list): text='\n'.join(text)
        assert text in source,repr(text)
    assert ancestor('5e458f4','b2d5f06^1')==0
    out('merge_local',dict(cat_first4=cat[:4],authorized_tree=tree,identical_diffs=True,sha256=sha(diff1),numstat=git('diff','--numstat','b2d5f06^1','b2d5f06').decode().splitlines(),base_ancestor_rc=0,all_source_outputs_equal=True))
    for ref,src,dst in [('4b4f37f','ops/leases/wp1045-r1-g1-claude.yaml','lease-wp1045-r1-g1.yaml.txt'),('4b4f37f','ops/leases/wp1045-r1-g2-claude.yaml','lease-wp1045-r1-g2.yaml.txt'),('a430543','ops/leases/wp1045-r1-g2-claude.yaml','lease-wp1045-r1-g2-sau-rut-han-a430543.yaml.txt')]:
        assert git('show',f'{ref}:{src}')==(P/dst).read_bytes(),dst
        out('lease_snapshot',dict(ref=ref,source=src,provenance=dst,identical=True,ancestor_lease_ref_rc=ancestor(ref,REF)))
    spec=git('show',f'{REF}:ops/specs/wp1045.md'); assert sha(spec)==land['spec']['sha256']
    l1=y(P/'lease-wp1045-r1-g1.yaml.txt'); l2=y(P/'lease-wp1045-r1-g2.yaml.txt'); later=y(P/'lease-wp1045-r1-g2-sau-rut-han-a430543.yaml.txt')
    assert sha(spec)==l1['spec_hash']==l2['spec_hash']
    assert l1['da_bi_thay_the']==l2['lease_id'] and l1['lease_id'] in l2['thay_the_cho']
    norm=sorted(unicodedata.normalize('NFC',s).casefold() for s in l2['write_set']); wh=sha(json.dumps(norm,separators=(',',':'),ensure_ascii=False).encode())
    assert land['lease']['write_set']==l2['write_set'] and wh==land['lease']['write_set_hash']==l2['write_set_hash']
    assert later['lease_until']==later['lease_expires_at_utc']=='2026-10-31T00:20:00Z'
    delta=(dt(later['lease_until'])-dt(later['lease_sua_lan_cuoi'])).total_seconds(); assert delta==1200
    assert git('show','a430543:ops/leases/wp1045-r1-g1-claude.yaml')==git('show','a430543^:ops/leases/wp1045-r1-g1-claude.yaml')
    out('lease_spec',dict(spec_sha256=sha(spec),write_set_sha256=wh,mutual_replacement=True,old_until=l2['lease_until'],new_until=later['lease_until'],shorten_seconds_after_edit=delta,g1_unchanged_at_a430543=True))

if __name__=='__main__':
    sections={'bytes':byte_checks,'receipts':receipt_checks,'git':git_checks}
    for name in sys.argv[1:] or list(sections):
        sections[name]()
        print(name,'PASS')
