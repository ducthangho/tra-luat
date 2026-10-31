from pathlib import Path
import hashlib, json, re, subprocess, yaml

root = Path(__file__).resolve().parent.parent / 'cay-kho'
sha = lambda b: hashlib.sha256(b).hexdigest()
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])

for n in (1, 2):
    p = root / f'ops/reviews/pr1050-review-{n}-codex'
    r = yaml.safe_load((root / f'ops/reviews/pr1050-review-{n}-codex-verdict.receipt.yaml').read_text())
    manifest = [line.split('  ', 1) for line in (p / 'SHA256SUMS').read_text().splitlines()]
    names = [str(Path(s[1])) for s in manifest]
    actual = {str(f.relative_to(p)) for f in p.rglob('*') if f.is_file() and f.name != 'SHA256SUMS'}
    bad = [name for h, name in manifest if not (p / name).is_file() or sha((p / name).read_bytes()) != h]
    print(f'ROUND {n}: manifest={len(names)}, actual={len(actual)}, missing={sorted(actual-set(names))}, extra={sorted(set(names)-actual)}, duplicate={len(names)-len(set(names))}, bad_hash={bad}')
    b = (p / 'VERDICT.md').read_bytes()
    print('flat_equal=', b == (root / r['verdict_path']).read_bytes(), 'sha256=', sha(b), 'bytes=', len(b))
    print('verdict_header=', b.decode().splitlines()[:3])
    d = json.loads((p / 'run/run.json').read_text())
    print('run_fields=', json.dumps({k:d[k] for k in ['run_id','head','worktree_sach','ma_thoat','trang_thai','thoi_luong_giay','provider','execution_surface','transport','model_phuc_vu_trang_thai','effort_phuc_vu','effort_phuc_vu_trang_thai']}, ensure_ascii=False))
    print('prompt_sha256=', sha((p / 'PROMPT.md').read_bytes()), 'matches_run=', sha((p / 'PROMPT.md').read_bytes())==d['prompt_sha256'])
    print('model_events=',len(d['model_phuc_vu']), 'models=', sorted({e['model'] for e in d['model_phuc_vu']}))
    for name in ['stdout', 'stderr']:
        b = (p / f'run/{name}.log').read_bytes()
        print(name, 'bytes=', len(b), 'hash=', sha(b), 'matches_run=', len(b)==d[f'{name}_byte'] and sha(b)==d[f'{name}_sha256'])
    diff = git('diff', r['base_sha'], r['reviewed_sha'])
    omitted = (p / 'OMITTED.txt').read_text()
    print('regenerated_diff bytes=', len(diff), 'sha256=', sha(diff), 'matches_OMITTED=', str(len(diff)) in omitted and sha(diff) in omitted)
    tree = git('rev-parse', r['reviewed_sha']+'^{tree}').decode().strip()
    url = r['evidence_url'].split('/blob/',1)[1]
    commit, path = url.split('/',1)
    print('tree=',tree, 'matches_receipt=', tree==r['reviewed_tree'], 'blob_equal=', git('show',commit+':'+path)==(root/r['verdict_path']).read_bytes())
    print('receipt_counts=', [r[f'so_p{i}'] for i in range(4)], 'receipt_assurance=',r['assurance'], 'review_class=',r['review_class'])
    if n == 2:
        prev = root / 'ops/reviews/pr1050-review-1-codex'
        for name,old in [('luot1-VERDICT.md','VERDICT.md'),('luot1-HINT.patch','HINT.patch')]:
            print('verdict-cu/'+name, 'matches_round1=',(p/'verdict-cu'/name).read_bytes()==(prev/old).read_bytes())
        d2 = git('diff', 'c24875d', 'f37b519')
        print('diff-tu-luot1.patch_equal=', d2==(p/'diff-tu-luot1.patch').read_bytes(), 'git_diff_bytes=',len(d2))
